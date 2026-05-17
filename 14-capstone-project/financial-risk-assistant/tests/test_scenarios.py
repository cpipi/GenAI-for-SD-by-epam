"""Test harness for positive, negative, and adversarial scenarios."""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow import run_investigation


def run_test_suite():
    """Run all test scenarios."""

    test_cases_path = Path("data") / "test_cases.json"

    if not test_cases_path.exists():
        print("Test cases not found. Run data_generator.py first.")
        return

    with open(test_cases_path) as f:
        test_cases = json.load(f)

    print("\n" + "=" * 80)
    print("STARTING TEST SUITE")
    print("=" * 80 + "\n")

    passed = 0
    failed = 0

    for test_case in test_cases:
        case_id = test_case.get("case_id")
        expected_decision = test_case.get("expected_decision")

        print(f"Running: {case_id}")
        print(f"  Expected: {expected_decision}")

        try:
            # Prepare input (remove expected_decision from test case)
            case_input = {k: v for k, v in test_case.items() if k != "expected_decision"}

            # Run investigation
            result = run_investigation(case_input)

            # Check recommendation
            recommendation = result.get("recommendation")
            if not recommendation:
                print("  [FAIL] No recommendation produced")
                failed += 1
                continue

            actual_decision = recommendation.decision
            print(f"  Actual: {actual_decision}")
            print(f"  Confidence: {recommendation.confidence:.2f}")
            print(f"  Rationale: {recommendation.rationale[:100]}...")

            # Simple pass/fail logic (in real scenario, could be more nuanced)
            if actual_decision.lower() == expected_decision.lower():
                print("  [PASS]\n")
                passed += 1
            else:
                print("  [FAIL] Decision mismatch\n")
                failed += 1

        except Exception as e:
            print(f"  [FAIL] Exception: {str(e)}\n")
            failed += 1

    print("=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
    print("=" * 80)

    return {"passed": passed, "failed": failed}


def run_adversarial_tests():
    """Run adversarial/edge-case tests."""

    adversarial_cases = [
        {
            "name": "Missing Required Field",
            "case": {
                "case_id": "adv_001",
                "customer_id": None,  # Invalid
                "transaction_amount": 1000,
                "transaction_type": "transfer",
                "channel": "online",
                "device_location": "US",
            },
            "should_flag": True,
        },
        {
            "name": "Negative Transaction Amount",
            "case": {
                "case_id": "adv_002",
                "customer_id": "cust_9999",
                "transaction_amount": -5000,  # Invalid
                "transaction_type": "transfer",
                "channel": "online",
                "device_location": "US",
            },
            "should_flag": True,
        },
        {
            "name": "Invalid Channel",
            "case": {
                "case_id": "adv_003",
                "customer_id": "cust_9999",
                "transaction_amount": 5000,
                "transaction_type": "transfer",
                "channel": "pigeon_mail",  # Invalid
                "device_location": "US",
            },
            "should_flag": True,
        },
        {
            "name": "High-Risk Country + Large Amount",
            "case": {
                "case_id": "adv_004",
                "customer_id": "cust_9999",
                "transaction_amount": 500000,
                "transaction_type": "wire_transfer",
                "channel": "international",
                "device_location": "IR",  # High risk
                "customer_profile": {"account_age_days": 5, "avg_monthly_volume": 100},
            },
            "should_flag": True,
        },
    ]

    print("\n" + "=" * 80)
    print("ADVERSARIAL TEST SUITE")
    print("=" * 80 + "\n")

    passed = 0
    failed = 0

    for test in adversarial_cases:
        print(f"Running: {test['name']}")

        try:
            result = run_investigation(test["case"])

            intake_valid = result.get("intake_valid", True)
            recommendation = result.get("recommendation")

            # Check if properly flagged
            properly_flagged = (not intake_valid) or (
                recommendation and recommendation.decision != "approve"
            )

            if properly_flagged == test["should_flag"]:
                print("  [PASS]\n")
                passed += 1
            else:
                print(f"  [FAIL] Expected flag={test['should_flag']}, got={properly_flagged}\n")
                failed += 1

        except Exception as e:
            print(f"  [FAIL] Exception: {str(e)}\n")
            failed += 1

    print("=" * 80)
    print(f"ADVERSARIAL RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
    print("=" * 80)

    return {"passed": passed, "failed": failed}


if __name__ == "__main__":
    # Generate test data first
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from data_generator import save_synthetic_data

    save_synthetic_data()

    # Run test suites
    normal_results = run_test_suite()
    adversarial_results = run_adversarial_tests()

    total_passed = normal_results["passed"] + adversarial_results["passed"]
    total_failed = normal_results["failed"] + adversarial_results["failed"]

    print(f"\n[SUMMARY] Overall: {total_passed} passed, {total_failed} failed")
