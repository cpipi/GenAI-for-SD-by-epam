"""Generate a compact MCP evidence report for demo/documentation.

Usage:
  py -3.12 mcp_evidence_runner.py

Environment:
  MCP_ENABLE_MOCK=false   # recommended for live evidence
"""

import json
from datetime import UTC, datetime
from pathlib import Path

from mcp.mcp_adapter import get_mcp_adapter


def build_report(use_mock: bool) -> dict:
    mcp = get_mcp_adapter(use_mock=use_mock)

    entities = [
        "Vladimir Putin",
        "John Smith",
        "Acme Trading LLC",
    ]
    countries = ["KZ", "RU", "IR"]

    sanctions = []
    for entity in entities:
        sanctions.append(
            {
                "entity": entity,
                "result": mcp.lookup_sanctions_list(entity),
            }
        )

    adverse_media = []
    for entity in entities:
        adverse_media.append(
            {
                "entity": entity,
                "result": mcp.check_adverse_media(entity),
            }
        )

    country_risk = []
    for code in countries:
        country_risk.append(
            {
                "country": code,
                "result": mcp.get_risk_indicators(code),
            }
        )

    return {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "mode": "mock" if use_mock else "live",
        "summary": {
            "entity_count": len(entities),
            "country_count": len(countries),
        },
        "sanctions_checks": sanctions,
        "adverse_media_checks": adverse_media,
        "country_risk_checks": country_risk,
    }


def main() -> None:
    # Force live evidence by default for report usefulness.
    use_mock = False
    report = build_report(use_mock=use_mock)

    out_path = Path("mcp_evidence_report.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Saved MCP evidence report: {out_path}")
    print(f"Mode: {report['mode']}")
    print(
        "Checks: "
        f"sanctions={len(report['sanctions_checks'])}, "
        f"adverse_media={len(report['adverse_media_checks'])}, "
        f"country_risk={len(report['country_risk_checks'])}"
    )


if __name__ == "__main__":
    main()
