"""LangGraph state definitions for the multi-agent workflow."""

from dataclasses import dataclass, field
from typing import Any, TypedDict


@dataclass
class Evidence:
    """Source citation for RAG-retrieved evidence."""

    source: str
    score: float
    text: str


@dataclass
class RiskFindings:
    """Risk analysis results from RAG agent."""

    risk_score: float  # 0.0 to 1.0
    risk_category: str  # "low", "medium", "high"
    pattern_matches: list[str]
    policy_violations: list[str]
    evidence: list[Evidence] = field(default_factory=list)
    reasoning: str = ""


@dataclass
class Recommendation:
    """Final recommendation from recommendation agent."""

    decision: str  # "approve", "manual_review", "block"
    confidence: float  # 0.0 to 1.0
    rationale: str
    risk_level: str
    next_actions: list[str]
    supporting_evidence: list[Evidence] = field(default_factory=list)


class State(TypedDict):
    """LangGraph state that flows through all agents."""

    # Input: case information
    case_id: str
    customer_id: str
    transaction_amount: float
    transaction_type: str
    channel: str  # "online", "mobile_app", "atm", "branch"
    device_location: str
    timestamp: str
    customer_profile: dict[str, Any]  # age, account_age, previous_txn_count, etc.
    transaction_context: dict[str, Any]  # raw transaction details

    # Processed: intake validation
    intake_valid: bool
    intake_errors: list[str] = field(default_factory=list)

    # Intermediate: RAG findings
    rag_findings: RiskFindings | None = None
    retrieved_documents: list[dict[str, Any]] = field(default_factory=list)

    # Intermediate: MCP external signals
    mcp_signals: dict[str, Any] = field(default_factory=dict)

    # Output: final recommendation
    recommendation: Recommendation | None = None

    # Metadata
    conversation_log: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
