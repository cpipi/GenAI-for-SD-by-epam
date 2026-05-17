"""Compare retrieval outputs with and without Claude reranking.

Usage:
  py -3.12 evaluate_rag_modes.py
"""

import json
from pathlib import Path

from rag.rag_setup import get_rag_system


def build_query(case: dict) -> str:
    profile = case.get("customer_profile") or {}
    return (
        f"transaction_type={case.get('transaction_type', 'unknown')}; "
        f"channel={case.get('channel', 'unknown')}; "
        f"location={case.get('device_location', 'unknown')}; "
        f"amount={case.get('transaction_amount', 0)}; "
        f"account_age_days={profile.get('account_age_days', 'unknown')}; "
        f"previous_txn_count={profile.get('previous_txn_count', 'unknown')}; "
        f"customer_id={case.get('customer_id', 'unknown')}; "
        "find relevant fraud patterns, AML policy checks, and escalation playbooks"
    )


def summarize_docs(docs: list) -> list:
    summary = []
    for d in docs:
        summary.append(
            {
                "source": d.get("source", ""),
                "type": d.get("type", ""),
                "score": round(float(d.get("similarity_score", 0.0)), 4),
            }
        )
    return summary


def main():
    cases_path = Path("data") / "test_cases.json"
    if not cases_path.exists():
        raise FileNotFoundError("data/test_cases.json not found. Run data_generator.py first.")

    with open(cases_path, encoding="utf-8") as f:
        cases = json.load(f)

    rag = get_rag_system()

    # Evaluate all generated cases for stronger evidence.
    chosen = cases

    report = []
    rerank_status_counts = {}
    sample_error = ""
    for case in chosen:
        query = build_query(case)
        local_docs = rag.retrieve(query, k=5, use_claude_rerank=False)
        llm_docs = rag.retrieve(query, k=5, use_claude_rerank=True)
        status = getattr(rag, "last_rerank_status", "unknown")
        rerank_status_counts[status] = rerank_status_counts.get(status, 0) + 1
        if not sample_error:
            sample_error = getattr(rag, "last_rerank_error", "")

        local_signature = [(d.get("source"), d.get("type")) for d in local_docs]
        llm_signature = [(d.get("source"), d.get("type")) for d in llm_docs]

        item = {
            "case_id": case.get("case_id"),
            "expected_decision": case.get("expected_decision"),
            "rerank_status": status,
            "local_only_top5": summarize_docs(local_docs),
            "claude_rerank_top5": summarize_docs(llm_docs),
            "top1_changed": (
                (
                    (local_docs[0].get("source"), local_docs[0].get("type"))
                    != (llm_docs[0].get("source"), llm_docs[0].get("type"))
                )
                if local_docs and llm_docs
                else False
            ),
            "top5_order_changed": local_signature != llm_signature,
        }
        report.append(item)

    out_path = Path("rag_mode_comparison.json")
    payload = {
        "summary": {
            "cases_evaluated": len(report),
            "rerank_status_counts": rerank_status_counts,
            "sample_error": sample_error,
        },
        "cases": report,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    changed_top1 = sum(1 for x in report if x["top1_changed"])
    changed_top5 = sum(1 for x in report if x["top5_order_changed"])
    print(f"Saved comparison report to {out_path}")
    print(f"Top-1 document changed in {changed_top1}/{len(report)} cases")
    print(f"Top-5 ranking changed in {changed_top5}/{len(report)} cases")
    print(f"Rerank status counts: {rerank_status_counts}")
    if sample_error:
        print(f"Sample rerank error: {sample_error}")


if __name__ == "__main__":
    main()
