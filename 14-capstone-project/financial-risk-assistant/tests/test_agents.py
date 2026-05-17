"""Unit tests for agent modules: intake, rag, recommendation, rationale_utils."""

import unittest

import agents.agents as agent_facade
from agents.modules.intake_agent import intake_agent
from agents.modules.rag_agent import rag_agent
from agents.modules.rationale_utils import build_fallback_rationale, generate_claude_rationale
from agents.modules.recommendation_agent import recommendation_agent
from graph_state import RiskFindings, State


class TestIntakeAgent(unittest.TestCase):
    def test_missing_required_fields(self):
        state = State(
            case_id=None,
            customer_id=None,
            transaction_amount=100,
            transaction_type="transfer",
            channel="online",
            conversation_log=[],
        )
        result = intake_agent(state)
        self.assertFalse(result["intake_valid"])
        self.assertIn("Missing required field", str(result["intake_errors"]))

    def test_valid_input(self):
        state = State(
            case_id="c1",
            customer_id="u1",
            transaction_amount=100,
            transaction_type="transfer",
            channel="online",
            conversation_log=[],
        )
        result = intake_agent(state)
        self.assertTrue(result["intake_valid"])


class TestRagAgent(unittest.TestCase):
    def test_rag_agent_runs(self):
        state = State(
            case_id="c1",
            customer_id="u1",
            transaction_amount=100,
            transaction_type="transfer",
            channel="online",
            conversation_log=[],
        )
        result = rag_agent(state)
        self.assertIn("rag_findings", result)


class TestRecommendationAgent(unittest.TestCase):

    def test_recommendation_agent_runs(self):
        # Provide all required fields for State
        findings = RiskFindings(
            risk_score=0.2,
            risk_category="low",
            pattern_matches=[],
            policy_violations=[],
            evidence=[],
            reasoning="test",
        )
        state = {
            "case_id": "c1",
            "customer_id": "u1",
            "transaction_amount": 100,
            "transaction_type": "transfer",
            "channel": "online",
            "device_location": "US",
            "timestamp": "2026-05-16T12:00:00Z",
            "customer_profile": {},
            "transaction_context": {},
            "intake_valid": True,
            "intake_errors": [],
            "rag_findings": findings,
            "retrieved_documents": [],
            "mcp_signals": {},
            "conversation_log": [],
        }
        result = recommendation_agent(state)
        self.assertIsInstance(result, dict)
        self.assertIn("recommendation", result)

    def test_recommendation_agent_handles_missing_rag(self):
        # Should return a recommendation with manual_review if rag_findings is missing
        state = {
            "case_id": "c2",
            "customer_id": "u2",
            "transaction_amount": 100,
            "transaction_type": "transfer",
            "channel": "online",
            "device_location": "US",
            "timestamp": "2026-05-16T12:00:00Z",
            "customer_profile": {},
            "transaction_context": {},
            "intake_valid": True,
            "intake_errors": [],
            "rag_findings": None,
            "retrieved_documents": [],
            "mcp_signals": {},
            "conversation_log": [],
        }
        result = recommendation_agent(state)
        self.assertIsInstance(result, dict)
        self.assertIn("recommendation", result)
        self.assertEqual(result["recommendation"].decision, "manual_review")

    def test_recommendation_agent_error_path(self):
        # Should return a state with recommendation=None if an exception occurs
        # Remove a required field to trigger an error
        state = {
            "case_id": "c3",
            "customer_id": "u3",
            "transaction_amount": 100,
            "transaction_type": "transfer",
            "channel": "online",
            # "device_location" is missing
            "timestamp": "2026-05-16T12:00:00Z",
            "customer_profile": {},
            "transaction_context": {},
            "intake_valid": True,
            "intake_errors": [],
            "rag_findings": None,
            "retrieved_documents": [],
            "mcp_signals": {},
            "conversation_log": [],
        }
        result = recommendation_agent(state)
        self.assertIsInstance(result, dict)
        self.assertIn("recommendation", result)


class TestAgentFacade(unittest.TestCase):
    def test_facade_exports_module_functions(self):
        self.assertIs(agent_facade.intake_agent, intake_agent)
        self.assertIs(agent_facade.rag_agent, rag_agent)
        self.assertIs(agent_facade.recommendation_agent, recommendation_agent)


class TestRationaleUtils(unittest.TestCase):
    def test_build_fallback_rationale(self):
        findings = RiskFindings(
            risk_score=0.5,
            risk_category="medium",
            pattern_matches=[],
            policy_violations=[],
            evidence=[],
            reasoning="test reason",
        )
        rationale = build_fallback_rationale(0.5, findings, "test reason")
        self.assertIn("Combined risk score", rationale)

    def test_generate_claude_rationale_fallback(self):
        findings = RiskFindings(
            risk_score=0.5,
            risk_category="medium",
            pattern_matches=[],
            policy_violations=[],
            evidence=[],
            reasoning="test reason",
        )
        rationale = generate_claude_rationale(
            "approve",
            0.5,
            findings,
            ["process_transaction"],
            {"risk_indicators": {"reason": "test"}},
        )
        self.assertIsInstance(rationale, str)


if __name__ == "__main__":
    unittest.main()
