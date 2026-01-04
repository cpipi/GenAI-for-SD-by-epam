"""Lightweight MCP-style clients for weather and news data.

These wrappers mimic the idea of MCP tool calls: a thin, typed adapter layer
that shields the orchestrator from raw HTTP details and provides graceful
fallbacks when a primary service is unavailable.
"""
from __future__ import annotations

import os
import re
import time
from typing import Any, Dict, List, Optional

import requests


class MCPOpenMeteoClient:
    """Client for the Open-Meteo MCP server.

    The client first geocodes a location string, then fetches the current
    weather using the returned latitude and longitude. Both endpoints are
    public and require no API key.
    """

    GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()

    def _extract_location_hint(self, query: str) -> str:
        """Return a best-effort location string for geocoding."""
        match = re.search(r"in\s+([A-Za-z\s\-]+)", query, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1)
            # Stop at common conjunctions or punctuation to avoid trailing words like "and headlines".
            candidate = re.split(r"\b(and|with|for|,|\.|\?)\b", candidate, maxsplit=1)[0]
        else:
            candidate = query

        cleaned = re.sub(r"[^A-Za-z\s\-]", "", candidate)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return self._normalize_alias(cleaned) or "Almaty"

    def _normalize_alias(self, city: str) -> str:
        """Map common aliases to improve geocoding hits."""
        aliases = {
            "nursultan": "Astana",
            "nur sultan": "Astana",
            "nur-sultan": "Astana",
            "astana": "Astana",
        }
        key = city.lower()
        return aliases.get(key, city)

    def _fallback_city_from_query(self, query: str) -> Optional[str]:
        """Fallback city extraction: last capitalized token chunk."""
        tokens = re.findall(r"[A-Z][a-zA-Z\-]+", query)
        if tokens:
            return tokens[-1]
        return None

    def geocode(self, query: str) -> Optional[Dict[str, Any]]:
        payload = {
            "name": self._extract_location_hint(query),
            "count": 1,
            "language": "en",
            "format": "json",
        }
        try:
            resp = self.session.get(self.GEO_URL, params=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            return None

        results = data.get("results") or []
        return results[0] if results else None

    def fetch_weather(self, query: str) -> Dict[str, Any]:
        geo = self.geocode(query)
        if not geo:
            fallback_city = self._fallback_city_from_query(query)
            if fallback_city:
                geo = self.geocode(fallback_city)
        if not geo:
            return {
                "error": "Could not resolve a location. Please provide a city or coordinates.",
                "provider": "open-meteo",
            }

        q_lower = query.lower()
        wants_tomorrow = "tomorrow" in q_lower
        wants_snow = "snow" in q_lower
        wants_future = wants_tomorrow or wants_snow
        params = {
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
            "current_weather": True,
        }
        if wants_future:
            params["daily"] = "precipitation_probability_max,temperature_2m_max,temperature_2m_min,snowfall_sum"
            params["forecast_days"] = 2
        try:
            resp = self.session.get(self.WEATHER_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            cw = data.get("current_weather", {})
            rain_chance = None
            snow_cm = None
            temp_max = None
            temp_min = None
            if wants_future:
                daily = data.get("daily", {})
                probs = daily.get("precipitation_probability_max") or []
                snow_list = daily.get("snowfall_sum") or []
                tmax_list = daily.get("temperature_2m_max") or []
                tmin_list = daily.get("temperature_2m_min") or []
                if len(probs) >= 2:
                    rain_chance = probs[1]
                if len(snow_list) >= 2:
                    snow_cm = snow_list[1]
                if len(tmax_list) >= 2:
                    temp_max = tmax_list[1]
                if len(tmin_list) >= 2:
                    temp_min = tmin_list[1]
            return {
                "provider": "open-meteo",
                "location": geo.get("name"),
                "latitude": geo.get("latitude"),
                "longitude": geo.get("longitude"),
                "temperature_c": cw.get("temperature"),
                "windspeed_kph": cw.get("windspeed"),
                "weathercode": cw.get("weathercode"),
                "timestamp": cw.get("time"),
                "rain_chance_tomorrow_pct": rain_chance,
                "snowfall_tomorrow_cm": snow_cm,
                "temp_max_tomorrow_c": temp_max,
                "temp_min_tomorrow_c": temp_min,
                "tomorrow_requested": wants_tomorrow,
                "snow_requested": wants_snow,
            }
        except Exception:
            return {
                "error": "Weather service is unavailable right now. Please try again soon.",
                "provider": "open-meteo",
            }


class MCPNewsClient:
    """Client for news data with a built-in fallback.

    Primary: TheNews API (no key needed for demo; optional token from env).
    Fallback: Hacker News front page via Algolia API.
    """

    PRIMARY_BASE = "https://api.thenewsapi.com/v1/news"
    FALLBACK_BASE = "https://hn.algolia.com/api/v1/search"

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.api_token = os.getenv("NEWS_API_TOKEN", "demo")

    def _shape_primary(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        shaped: List[Dict[str, Any]] = []
        for item in items:
            shaped.append(
                {
                    "title": item.get("title"),
                    "summary": item.get("description"),
                    "url": item.get("url"),
                    "source": item.get("source"),
                    "published_at": item.get("published_at"),
                }
            )
        return shaped

    def _shape_fallback(self, hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        shaped: List[Dict[str, Any]] = []
        for item in hits:
            shaped.append(
                {
                    "title": item.get("title") or item.get("story_title"),
                    "summary": item.get("story_text"),
                    "url": item.get("url") or item.get("story_url"),
                    "source": "Hacker News",
                    "published_at": item.get("created_at"),
                }
            )
        return shaped

    def fetch_primary(self, query: Optional[str], limit: int = 5) -> Optional[List[Dict[str, Any]]]:
        endpoint = f"{self.PRIMARY_BASE}/all" if query else f"{self.PRIMARY_BASE}/top"
        params = {
            "language": "en",
            "limit": limit,
            "api_token": self.api_token,
        }
        if query:
            params["search"] = query
        try:
            resp = self.session.get(endpoint, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            articles = data.get("data") or []
            return self._shape_primary(articles)
        except Exception:
            return None

    def fetch_fallback(self, query: Optional[str], limit: int = 5) -> List[Dict[str, Any]]:
        # Prefer recent items (last 14 days) to avoid stale results.
        recent_cutoff = int(time.time()) - 14 * 24 * 60 * 60
        params = {
            "tags": "front_page" if not query else "story",
            "query": query or "news",
            "hitsPerPage": limit,
            "numericFilters": f"created_at_i>{recent_cutoff}",
            "restrictSearchableAttributes": "title,url",
        }
        try:
            resp = self.session.get(self.FALLBACK_BASE, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            hits = data.get("hits") or []
            return self._shape_fallback(hits)
        except Exception:
            return []

    def fetch_news(self, query: Optional[str], limit: int = 5) -> Dict[str, Any]:
        primary = self.fetch_primary(query, limit)
        if primary:
            return {"provider": "thenewsapi", "articles": primary}

        fallback = self.fetch_fallback(query, limit)
        if not fallback and query:
            # Retry with a neutral query to ensure we return something fresh.
            fallback = self.fetch_fallback(None, limit)
        if fallback:
            return {"provider": "hackernews", "articles": fallback, "warning": "Primary news source unavailable; using fallback."}

        return {"provider": "thenewsapi", "error": "News services are unavailable right now."}
