"""Rationale generation utilities for agent explanations."""

import logging

from anthropic import Anthropic

from config import (
    CLAUDE_API_KEY,
    CLAUDE_RATIONALE_MAX_TOKENS,
    LLM_MODEL,
    LLM_TEMPERATURE,
    USE_CLAUDE_RATIONALE,
)
from graph_state import RiskFindings


def build_fallback_rationale(
    combined_risk: float, rag_findings: RiskFindings, mcp_risk_reason: str
) -> str:
    """
    Build a fallback rationale string if LLM rationale is unavailable.
    Args:
        combined_risk: The combined risk score for the case.
        rag_findings: The RAG agent's findings object.
        mcp_risk_reason: The reason string from MCP risk indicators.
    Returns:
        A string explanation for the decision rationale.
    """
    try:
        result = (
            f"Combined risk score: {combined_risk:.2f}. {rag_findings.reasoning}. "
            f"MCP risk indicators: {mcp_risk_reason}"
        )
        return result
    except Exception as e:
        logging.error(f"Error building fallback rationale: {e}")
        return "Unable to generate fallback rationale due to error."


def generate_claude_rationale(
    decision: str,
    combined_risk: float,
    rag_findings: RiskFindings,
    next_actions: list[str],
    mcp_signals: dict[str, object],
) -> str:
    """
    Generate a concise analyst-style explanation using Claude; fallback to deterministic text.
    Args:
        decision: The case decision (approve, block, manual_review).
        combined_risk: The combined risk score for the case.
        rag_findings: The RAG agent's findings object.
        next_actions: List of next actions recommended.
        mcp_signals: Dictionary of MCP signals (sanctions, risk indicators, adverse media).
    Returns:
        A string explanation for the decision rationale.
    """
    fallback = build_fallback_rationale(
        combined_risk=combined_risk,
        rag_findings=rag_findings,
        mcp_risk_reason=mcp_signals.get("risk_indicators", {}).get("reason", "n/a"),
    )
    if not (USE_CLAUDE_RATIONALE and CLAUDE_API_KEY):
        logging.info("Claude rationale disabled or API key missing; using fallback rationale.")
        return fallback
    try:
        client = Anthropic(api_key=CLAUDE_API_KEY)
        prompt = (
            "You are a senior risk analyst assistant. Produce a concise rationale for a case decision.\n"
            "Rules:\n"
            "1) Be factual and grounded in provided evidence only.\n"
            "2) Mention top risk drivers, policy impact, and why the decision is proportionate.\n"
            "3) Keep it under 90 words.\n"
            "4) No markdown or bullet points.\n\n"
            f"Decision: {decision}\n"
            f"Combined risk score: {combined_risk:.2f}\n"
            f"Risk category: {rag_findings.risk_category}\n"
            f"Pattern matches: {', '.join(rag_findings.pattern_matches) if rag_findings.pattern_matches else 'none'}\n"
            f"Policy considerations: {', '.join(rag_findings.policy_violations) if rag_findings.policy_violations else 'none'}\n"
            f"MCP sanctions status: {mcp_signals.get('sanctions', {}).get('status', 'unknown')}\n"
            f"MCP risk reason: {mcp_signals.get('risk_indicators', {}).get('reason', 'n/a')}\n"
            f"Adverse media severity: {mcp_signals.get('adverse_media', {}).get('severity', 'unknown')}\n"
            f"Next actions: {', '.join(next_actions)}"
        )
        response = client.messages.create(
            model=LLM_MODEL,
            max_tokens=CLAUDE_RATIONALE_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
        )
        if response.content:
            text = response.content[0].text.strip()
            if text:
                return text
        logging.warning("Claude response empty; using fallback rationale.")
        return fallback
    except Exception as e:
        logging.error(f"Error generating Claude rationale: {e}")
        return fallback
