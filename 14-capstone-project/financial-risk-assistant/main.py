"""CLI entry point for the Financial Risk Assistant."""

import json
from datetime import datetime
from pathlib import Path

from data_generator import save_synthetic_data
from workflow import run_investigation


def format_recommendation(result):
    """Pretty-print recommendation."""
    recommendation = result.get("recommendation")
    if not recommendation:
        print("[FAIL] No recommendation produced")
        return

    print("\n" + "=" * 80)
    print("INVESTIGATION RESULT")
    print("=" * 80)
    print(f"Case ID: {result.get('case_id')}")
    print(f"Customer ID: {result.get('customer_id')}")
    print(f"Transaction: {result.get('transaction_amount')} {result.get('transaction_type')}")
    print()
    print(f"Decision: {recommendation.decision.upper()}")
    print(f"Confidence: {recommendation.confidence*100:.0f}%")
    print(f"Risk Level: {recommendation.risk_level.upper()}")
    print()
    print(f"Rationale:\n  {recommendation.rationale}")
    print()
    print("Next Actions:")
    for action in recommendation.next_actions:
        print(f"  - {action}")
    print()
    if recommendation.supporting_evidence:
        print(f"Supporting Evidence ({len(recommendation.supporting_evidence)} citations):")
        for i, ev in enumerate(recommendation.supporting_evidence[:3], 1):
            print(f"  {i}. {ev.source} (score: {ev.score:.2f})")
            print(f"     {ev.text[:80]}...")
    print()
    print("Agent Trace:")
    for step in result.get("conversation_log", []):
        agent = step.get("agent", "unknown")
        action = step.get("action", "")
        print(f"  - {agent}: {action}")
    print("=" * 80 + "\n")


def main():
    """Main CLI interface."""

    print("Financial Risk Investigation Assistant")
    print("=" * 80)

    # Step 1: Initialize synthetic data
    data_dir = Path("data")
    if not (data_dir / "risk_patterns.json").exists():
        print("\n[1/3] Generating synthetic data...")
        save_synthetic_data()
    else:
        print("\n[1/3] Synthetic data already exists")

    # Step 2: Warm up RAG system
    print("[2/3] Initializing RAG system...")
    from rag.rag_setup import get_rag_system

    rag = get_rag_system()
    _ = rag.retrieve("warmup risk policy query", k=1, use_claude_rerank=False)
    print("      [OK] RAG system ready")

    # Step 3: Get test case or custom input
    print("\n[3/3] Running investigation...")

    # Load and run a test case
    test_cases_path = Path("data") / "test_cases.json"
    if test_cases_path.exists():
        with open(test_cases_path) as f:
            test_cases = json.load(f)

        # Show options
        print(f"\nAvailable test cases: {len(test_cases)}")
        for i, case in enumerate(test_cases[:3]):
            print(f"  {i+1}. {case['case_id']} (Expected: {case['expected_decision']})")
        print(f"  ... and {len(test_cases)-3} more")

        print("\nSelect test case number (or 'q' to quit):")
        choice = input("> ").strip()

        if choice.lower() == "q":
            print("Exiting.")
            return

        try:
            idx = int(choice) - 1
            test_case = test_cases[idx]
        except (ValueError, IndexError):
            print("Running first test case...")
            test_case = test_cases[0]

        # Prepare input (remove expected_decision)
        case_input = {k: v for k, v in test_case.items() if k != "expected_decision"}

        # Run investigation
        result = run_investigation(case_input)
        format_recommendation(result)

        # Save result
        output_file = (
            f"investigation_{result['case_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(output_file, "w") as f:
            # Convert result to serializable format
            serializable = {
                k: v for k, v in result.items() if k not in ["rag_findings", "recommendation"]
            }
            if result.get("recommendation"):
                serializable["recommendation"] = {
                    "decision": result["recommendation"].decision,
                    "confidence": result["recommendation"].confidence,
                    "rationale": result["recommendation"].rationale,
                    "risk_level": result["recommendation"].risk_level,
                    "next_actions": result["recommendation"].next_actions,
                }
            json.dump(serializable, f, indent=2)
        print(f"Result saved to: {output_file}")


if __name__ == "__main__":
    main()
