"""Unit tests for synthetic data generation helpers."""

import unittest

from data_generator import generate_edge_test_cases, generate_test_cases


class TestDataGenerator(unittest.TestCase):
    def test_generate_test_cases_has_expected_mix(self):
        cases = generate_test_cases()
        self.assertEqual(len(cases), 25)

        expected_counts = {"approve": 12, "manual_review": 5, "block": 8}
        counts = {"approve": 0, "manual_review": 0, "block": 0}
        for case in cases:
            counts[case["expected_decision"]] += 1

        self.assertEqual(counts, expected_counts)

    def test_generate_edge_test_cases_shape(self):
        edge_cases = generate_edge_test_cases()
        self.assertGreaterEqual(len(edge_cases), 6)

        required_fields = {
            "case_id",
            "customer_id",
            "transaction_amount",
            "transaction_type",
            "channel",
            "device_location",
            "timestamp",
            "customer_profile",
            "expected_decision",
            "edge_case_tag",
        }

        tags = set()
        for case in edge_cases:
            self.assertTrue(required_fields.issubset(case.keys()))
            tags.add(case["edge_case_tag"])

        self.assertIn("missing_required_field", tags)
        self.assertIn("invalid_amount", tags)
        self.assertIn("invalid_channel", tags)
        self.assertIn("hard_gate_amount", tags)


if __name__ == "__main__":
    unittest.main()
