"""Recommendation agent logic for synthesizing findings and producing recommendations."""

import logging

from agents.modules.rationale_utils import generate_claude_rationale
from config import MCP_ENABLE_MOCK
from graph_state import Recommendation, State
from mcp.mcp_adapter import get_mcp_adapter


def recommendation_agent(state: State) -> State:
    """
    Recommendation Agent: Synthesizes findings and produces final recommendation.
    Args:
        state: The workflow state dictionary.
    Returns:
        Updated state with recommendation and rationale.
    """
    try:
        mcp = get_mcp_adapter(use_mock=MCP_ENABLE_MOCK)
        device_location = state.get("device_location") or "UNKNOWN"
        customer_id = state.get("customer_id") or "unknown"

        mcp_sanctions = mcp.lookup_sanctions_list(customer_id)
        mcp_risk = mcp.get_risk_indicators(device_location)
        mcp_adverse = mcp.check_adverse_media(customer_id)

        state["mcp_signals"] = {
            "sanctions": mcp_sanctions,
            "risk_indicators": mcp_risk,
            "adverse_media": mcp_adverse,
        }

        rag_findings = state.get("rag_findings")
        if not rag_findings:
            recommendation = Recommendation(
                decision="manual_review",
                confidence=0.5,
                rationale="Unable to perform RAG analysis; escalating to manual review",
                risk_level="unknown",
                next_actions=["manual_review", "contact_risk_team"],
            )
        else:
            rag_score = float(rag_findings.risk_score)
            mcp_score = float(mcp_risk.get("risk_score", 0.0))
            amount = float(state.get("transaction_amount", 0.0) or 0.0)

            combined_risk = (0.75 * rag_score) + (0.25 * mcp_score)
            combined_risk = min(max(combined_risk, 0.0), 1.0)

            sanctions_hit = mcp_sanctions.get("status") == "found"
            extreme_country_risk = mcp_score >= 0.85
            very_large_amount = amount >= 50000
            high_combined_risk = combined_risk >= 0.60

            if (
                sanctions_hit
                or very_large_amount
                or high_combined_risk
                or (extreme_country_risk and very_large_amount)
            ):
                decision = "block"
                next_actions = [
                    "block_transaction",
                    "file_suspicious_activity_report",
                    "contact_compliance",
                ]
            elif combined_risk >= 0.22:
                decision = "manual_review"
                next_actions = [
                    "escalate_to_risk_team",
                    "request_additional_kyc",
                    "monitor_account",
                ]
            else:
                decision = "approve"
                next_actions = ["process_transaction", "log_case", "monitor_for_patterns"]

            evidence_list = rag_findings.evidence.copy() if rag_findings.evidence else []

            rationale = generate_claude_rationale(
                decision=decision,
                combined_risk=combined_risk,
                rag_findings=rag_findings,
                next_actions=next_actions,
                mcp_signals=state["mcp_signals"],
            )

            profile = state.get("customer_profile") or {}
            account_age = profile.get("account_age_days", 0)
            txn_count = profile.get("previous_txn_count", 0)
            is_established = (
                isinstance(account_age, (int, float))
                and account_age > 180
                and isinstance(txn_count, (int, float))
                and txn_count > 100
            )

            if decision == "approve":
                if combined_risk < 0.15 and is_established:
                    confidence = 0.96 + (0.02 * (1 - combined_risk))
                elif combined_risk < 0.25:
                    confidence = 0.92 + (0.03 * (1 - combined_risk))
                else:
                    confidence = 0.80 + (0.10 * (1 - combined_risk))
            elif decision == "block":
                confidence = 0.88 + (0.08 * combined_risk)
            else:
                confidence = 0.75 + (0.15 * abs(combined_risk - 0.22))

            confidence = min(max(confidence, 0.5), 0.98)

            recommendation = Recommendation(
                decision=decision,
                confidence=round(confidence, 2),
                rationale=rationale,
                risk_level=rag_findings.risk_category,
                next_actions=next_actions,
                supporting_evidence=evidence_list,
            )

        state["recommendation"] = recommendation

        log_entry = {
            "agent": "recommendation",
            "action": "decision",
            "decision": recommendation.decision,
            "confidence": recommendation.confidence,
            "risk_level": recommendation.risk_level,
        }
        state["conversation_log"].append(log_entry)

        return state
    except Exception as e:
        logging.error(f"Error in recommendation_agent: {e}")
        try:
            state["recommendation"] = None
            return state
        except Exception:
            return {"recommendation": None}
