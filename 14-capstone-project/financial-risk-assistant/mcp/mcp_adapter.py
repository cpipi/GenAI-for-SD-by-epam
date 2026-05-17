"""MCP adapter for external data sources (mock and real implementations)."""

import csv
import io
import json
import random
import re
import xml.etree.ElementTree as ET
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def _http_get_json(url: str, timeout: int = 5) -> Any:
    """Small helper for HTTP GET JSON with a user-agent and timeout."""
    req = Request(url, headers={"User-Agent": "financial-risk-assistant/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


class MCPAdapter:
    """Adapter for Model Context Protocol tools."""

    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self._ofac_names_cache = None

    def lookup_sanctions_list(
        self, entity_name: str, entity_type: str = "person"
    ) -> dict[str, Any]:
        """Check if entity is on sanctions list."""
        if self.use_mock:
            return self._mock_sanctions_lookup(entity_name, entity_type)
        return self._real_sanctions_lookup(entity_name, entity_type)

    def get_risk_indicators(
        self, country_code: str, merchant_category: str = None
    ) -> dict[str, Any]:
        """Get risk indicators for a country or merchant."""
        if self.use_mock:
            return self._mock_risk_indicators(country_code, merchant_category)
        return self._real_risk_indicators(country_code, merchant_category)

    def check_adverse_media(self, entity_name: str) -> dict[str, Any]:
        """Check if entity appears in adverse media."""
        if self.use_mock:
            return self._mock_adverse_media(entity_name)
        return self._real_adverse_media(entity_name)

    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""
        return re.sub(r"[^a-z0-9 ]+", " ", str(text).lower()).strip()

    def _load_ofac_names(self) -> list:
        """Load OFAC SDN names into memory (cached)."""
        if self._ofac_names_cache is not None:
            return self._ofac_names_cache

        names = []
        try:
            data = _http_get_json("https://www.treasury.gov/ofac/downloads/sdn.csv", timeout=12)
        except Exception:
            # sdn.csv is CSV, so read as text if JSON loader fails.
            req = Request(
                "https://www.treasury.gov/ofac/downloads/sdn.csv",
                headers={"User-Agent": "financial-risk-assistant/1.0"},
            )
            with urlopen(req, timeout=12) as resp:
                text = resp.read().decode("utf-8", errors="ignore")
            reader = csv.reader(io.StringIO(text))
            for row in reader:
                if len(row) > 1:
                    name = self._normalize_text(row[1])
                    if name:
                        names.append(name)
        else:
            # Defensive path if endpoint behavior changes.
            if isinstance(data, list):
                for row in data:
                    if isinstance(row, list) and len(row) > 1:
                        name = self._normalize_text(row[1])
                        if name:
                            names.append(name)

        self._ofac_names_cache = names
        return names

    def _real_sanctions_lookup(
        self, entity_name: str, entity_type: str = "person"
    ) -> dict[str, Any]:
        """Real sanctions lookup using OFAC SDN public list."""
        if not entity_name:
            return {
                "status": "not_found",
                "entity_name": entity_name,
                "entity_type": entity_type,
                "lists": [],
                "confidence": 0.0,
                "reason": "Empty entity name",
            }

        try:
            names = self._load_ofac_names()
            query = self._normalize_text(entity_name)
            q_tokens = [t for t in query.split() if len(t) > 2]
            if not names or not q_tokens:
                return {
                    "status": "unavailable",
                    "entity_name": entity_name,
                    "entity_type": entity_type,
                    "lists": [],
                    "confidence": 0.0,
                    "reason": "OFAC data unavailable or insufficient query tokens",
                }

            best = ""
            best_score = 0.0
            for n in names:
                token_hits = sum(1 for t in q_tokens if t in n)
                score = token_hits / max(1, len(q_tokens))
                if score > best_score:
                    best_score = score
                    best = n

            is_match = best_score >= 0.8
            return {
                "status": "found" if is_match else "not_found",
                "entity_name": entity_name,
                "entity_type": entity_type,
                "lists": ["OFAC SDN"] if is_match else [],
                "confidence": round(best_score, 2),
                "matched_name": best if is_match else "",
                "reason": "OFAC SDN token match",
            }
        except Exception as e:
            return {
                "status": "unavailable",
                "entity_name": entity_name,
                "entity_type": entity_type,
                "lists": [],
                "confidence": 0.0,
                "reason": f"OFAC lookup error: {str(e)[:120]}",
            }

    def _real_adverse_media(self, entity_name: str) -> dict[str, Any]:
        """Real adverse-media approximation via Google News RSS."""
        if not entity_name:
            return {
                "entity_name": entity_name,
                "mentions_found": 0,
                "severity": "unknown",
                "sources": [],
                "last_scan": "live",
                "reason": "Empty entity name",
            }

        keywords = ["fraud", "sanction", "corruption", "laundering", "bribery", "crime"]
        try:
            query = quote(f"{entity_name} fraud sanctions corruption")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            req = Request(url, headers={"User-Agent": "financial-risk-assistant/1.0"})
            with urlopen(req, timeout=10) as resp:
                xml_bytes = resp.read()

            root = ET.fromstring(xml_bytes)
            items = root.findall(".//item")[:15]
            titles = [it.findtext("title") or "" for it in items]

            keyword_hits = 0
            for title in titles:
                low = title.lower()
                if any(k in low for k in keywords):
                    keyword_hits += 1

            mentions = len(items)
            if mentions >= 10 and keyword_hits >= 6:
                severity = "high"
            elif mentions >= 5 and keyword_hits >= 3:
                severity = "medium"
            else:
                severity = "low"

            return {
                "entity_name": entity_name,
                "mentions_found": mentions,
                "severity": severity,
                "sources": titles[:5],
                "last_scan": "live",
                "keyword_hits": keyword_hits,
                "reason": "Google News RSS risk-keyword scan",
            }
        except Exception as e:
            return {
                "entity_name": entity_name,
                "mentions_found": 0,
                "severity": "unknown",
                "sources": [],
                "last_scan": "live",
                "reason": f"News scan error: {str(e)[:120]}",
            }

    def _real_risk_indicators(
        self, country_code: str, merchant_category: str = None
    ) -> dict[str, Any]:
        """Real external enrichment via public APIs (World Bank + RestCountries)."""
        if not country_code:
            country_code = "UNKNOWN"
        code = str(country_code).upper()

        # Default fallback profile.
        result = {
            "country": code,
            "risk_score": 0.45,
            "reason": "Fallback profile (external sources unavailable)",
            "merchant_category": merchant_category,
            "last_updated": "live",
            "external_signals": {},
        }

        # Domain override for commonly used synthetic high-risk codes.
        high_risk_codes = {"RU": 0.85, "IR": 0.9, "KP": 0.95, "SY": 0.88, "UNKNOWN": 0.8}
        if code in high_risk_codes:
            result["risk_score"] = high_risk_codes[code]
            result["reason"] = "High-risk jurisdiction override"

        try:
            wb_url = f"https://api.worldbank.org/v2/country/{code}?format=json"
            wb_data = _http_get_json(wb_url)
            if isinstance(wb_data, list) and len(wb_data) > 1 and wb_data[1]:
                country_obj = wb_data[1][0]
                income = (country_obj.get("incomeLevel") or {}).get("id", "")
                lending = (country_obj.get("lendingType") or {}).get("id", "")
                result["external_signals"]["world_bank"] = {
                    "income_level": income,
                    "lending_type": lending,
                }

                # Heuristic mapping for risk prior.
                income_risk = {
                    "HIC": 0.2,
                    "UMC": 0.35,
                    "LMC": 0.5,
                    "LIC": 0.65,
                }
                mapped = income_risk.get(income)
                if mapped is not None and code not in high_risk_codes:
                    result["risk_score"] = mapped
                    result["reason"] = f"World Bank income-level prior ({income})"
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
            pass

        try:
            # Adds regional context as an explainability signal.
            rc_url = f"https://restcountries.com/v3.1/alpha/{code}?fields=name,region,subregion"
            rc_data = _http_get_json(rc_url)
            if isinstance(rc_data, list) and rc_data:
                c = rc_data[0]
                result["external_signals"]["rest_countries"] = {
                    "name": (c.get("name") or {}).get("common", ""),
                    "region": c.get("region", ""),
                    "subregion": c.get("subregion", ""),
                }
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
            pass

        # Add FX context from open exchange-rate API.
        try:
            fx = _http_get_json("https://open.er-api.com/v6/latest/USD")
            if isinstance(fx, dict) and fx.get("result") == "success":
                rates = fx.get("rates", {})
                if code == "KZ":
                    fx_value = rates.get("KZT")
                else:
                    # Try country code as currency when possible, fallback none.
                    fx_value = rates.get(code)
                result["external_signals"]["fx"] = {
                    "base": fx.get("base_code", "USD"),
                    "quote_value": fx_value,
                    "provider": "open.er-api.com",
                }
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
            pass

        # Merchant category adjustment retained from mock behavior.
        if merchant_category:
            result["risk_score"] = min(
                1.0, max(0.0, result["risk_score"] + random.uniform(-0.05, 0.05))
            )

        return result

    # Mock implementations
    def _mock_sanctions_lookup(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Mock sanctions list lookup with expanded demo names."""
        # Test names that trigger sanctions hits (for demo/testing)
        high_risk_names = [
            "putin",
            "medvedev",
            "khamenei",
            "maduro",
            "vladimir putin",
            "mohammad zarif",
            "kim jong un",
            "bashar al-assad",
            "russian federation",
            "bank of iran",
            "supreme leader of iran",
            "khomenei",
            "zarif",  # partial matches for robustness
        ]

        is_sanctioned = False
        matched_name = ""

        if entity_name:
            entity_lower = str(entity_name).lower().strip()

            # Check for exact or substring matches
            for name in high_risk_names:
                if name in entity_lower or entity_lower in name:
                    is_sanctioned = True
                    matched_name = name
                    break

        return {
            "status": "found" if is_sanctioned else "not_found",
            "entity_name": entity_name,
            "entity_type": entity_type,
            "lists": ["OFAC SDN", "EU Consolidated List"] if is_sanctioned else [],
            "confidence": 0.95 if is_sanctioned else 0.99,
            "matched_name": matched_name if is_sanctioned else "",
            "reason": "Mock sanctions check" if is_sanctioned else "No match in test list",
        }

    def _mock_risk_indicators(
        self, country_code: str, merchant_category: str = None
    ) -> dict[str, Any]:
        """Mock risk indicator lookup."""
        high_risk_countries = {"RU": 0.85, "IR": 0.9, "KP": 0.95, "SY": 0.88, "UNKNOWN": 0.8}

        base_risk = high_risk_countries.get(country_code, 0.2)
        category_adjustment = random.uniform(-0.1, 0.1) if merchant_category else 0

        return {
            "country": country_code,
            "risk_score": min(1.0, base_risk + category_adjustment),
            "reason": "High-risk jurisdiction" if base_risk > 0.5 else "Standard risk profile",
            "merchant_category": merchant_category,
            "last_updated": "2024-05-03",
        }

    def _mock_adverse_media(self, entity_name: str) -> dict[str, Any]:
        """Mock adverse media check."""
        trigger_names = ["corruption", "fraud", "sanctions", "terrorist"]
        entity_text = str(entity_name).lower() if entity_name else ""
        has_adverse_media = any(word.lower() in entity_text for word in trigger_names)

        return {
            "entity_name": entity_name,
            "mentions_found": random.randint(5, 50) if has_adverse_media else 0,
            "severity": random.choice(["high", "medium"]) if has_adverse_media else "low",
            "sources": ["Reuters", "Bloomberg", "WSJ"] if has_adverse_media else [],
            "last_scan": "2024-05-03",
        }


# Global MCP instance
_mcp_adapter = None


def get_mcp_adapter(use_mock: bool = True) -> MCPAdapter:
    """Get or create the global MCP adapter."""
    global _mcp_adapter
    if _mcp_adapter is None:
        _mcp_adapter = MCPAdapter(use_mock=use_mock)
    return _mcp_adapter
