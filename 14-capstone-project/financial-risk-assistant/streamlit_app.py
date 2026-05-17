"""Streamlit web app for Financial Risk Assistant demo with agent visualization."""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import MCP_ENABLE_MOCK
from data_generator import generate_test_cases
from workflow import run_investigation


def _new_case_id() -> str:
    return f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def _new_customer_id() -> str:
    return f"CUST-{str(uuid.uuid4())[:8].upper()}"


def _demo_preset_case(target: str) -> dict:
    """Return deterministic demo payloads for each decision path."""
    timestamp = datetime.now().isoformat()

    if target == "approve":
        return {
            "case_id": "DEMO-APPROVE-001",
            "customer_id": "CUST-DEMO-APPROVE",
            "transaction_amount": 3200,
            "transaction_type": "payment",
            "channel": "mobile_app",
            "device_location": "US",
            "customer_profile": {
                "account_age_days": 900,
                "avg_monthly_volume": 12000,
                "previous_txn_count": 340,
                "country_of_residence": "US",
            },
            "timestamp": timestamp,
        }

    if target == "manual_review":
        return {
            "case_id": "DEMO-REVIEW-001",
            "customer_id": "CUST-UX-001",
            "transaction_amount": 18000,
            "transaction_type": "transfer",
            "channel": "online",
            "device_location": "US",
            "customer_profile": {
                "account_age_days": 40,
                "avg_monthly_volume": 1500,
                "previous_txn_count": 3,
                "country_of_residence": "US",
            },
            "timestamp": timestamp,
        }

    return {
        "case_id": "DEMO-BLOCK-001",
        "customer_id": "vladimir putin",
        "transaction_amount": 5200,
        "transaction_type": "transfer",
        "channel": "online",
        "device_location": "RU",
        "customer_profile": {
            "account_age_days": 90,
            "avg_monthly_volume": 8000,
            "previous_txn_count": 12,
            "country_of_residence": "RU",
        },
        "timestamp": timestamp,
    }


# Initialize session state for form defaults
if "default_case_id" not in st.session_state:
    st.session_state.default_case_id = _new_case_id()
if "default_customer_id" not in st.session_state:
    st.session_state.default_customer_id = _new_customer_id()
if "manual_case_id" not in st.session_state:
    st.session_state.manual_case_id = st.session_state.default_case_id
if "manual_customer_id" not in st.session_state:
    st.session_state.manual_customer_id = st.session_state.default_customer_id

# Apply deferred ID updates before widgets are created.
if "pending_manual_case_id" in st.session_state:
    pending_case_id = st.session_state.pop("pending_manual_case_id")
    st.session_state.default_case_id = pending_case_id
    st.session_state.manual_case_id = pending_case_id
if "pending_manual_customer_id" in st.session_state:
    pending_customer_id = st.session_state.pop("pending_manual_customer_id")
    st.session_state.default_customer_id = pending_customer_id
    st.session_state.manual_customer_id = pending_customer_id


def _evidence_to_dict(evidence_items):
    """Convert list of Evidence dataclasses to plain dicts."""
    out = []
    for evidence_item in evidence_items or []:
        out.append(
            {
                "source": getattr(evidence_item, "source", "unknown"),
                "score": float(getattr(evidence_item, "score", 0.0)),
                "text": getattr(evidence_item, "text", ""),
            }
        )
    return out


def _serialize_result(state_result):
    """Convert workflow state to JSON-serializable dict."""
    recommendation_obj = state_result.get("recommendation")
    rag_findings = state_result.get("rag_findings")

    recommendation_dict = None
    if recommendation_obj:
        recommendation_dict = {
            "decision": recommendation_obj.decision,
            "confidence": recommendation_obj.confidence,
            "rationale": recommendation_obj.rationale,
            "risk_level": recommendation_obj.risk_level,
            "next_actions": recommendation_obj.next_actions,
            "supporting_evidence": _evidence_to_dict(recommendation_obj.supporting_evidence),
        }

    rag_dict = None
    if rag_findings:
        rag_dict = {
            "risk_score": rag_findings.risk_score,
            "risk_category": rag_findings.risk_category,
            "pattern_matches": rag_findings.pattern_matches,
            "policy_violations": rag_findings.policy_violations,
            "reasoning": rag_findings.reasoning,
            "evidence": _evidence_to_dict(rag_findings.evidence),
        }

    return {
        "case_id": state_result.get("case_id"),
        "customer_id": state_result.get("customer_id"),
        "transaction_amount": state_result.get("transaction_amount"),
        "transaction_type": state_result.get("transaction_type"),
        "channel": state_result.get("channel"),
        "device_location": state_result.get("device_location"),
        "timestamp": state_result.get("timestamp"),
        "conversation_log": state_result.get("conversation_log", []),
        "intake_valid": state_result.get("intake_valid"),
        "intake_errors": state_result.get("intake_errors", []),
        "mcp_signals": state_result.get("mcp_signals", {}),
        "rag_findings": rag_dict,
        "recommendation": recommendation_dict,
    }


def _calculate_decision_drivers(serialized):
    """Recreate key decision inputs so UI can explain outcome clearly."""
    rag_findings = serialized.get("rag_findings") or {}
    mcp_info = serialized.get("mcp_signals") or {}
    sanctions = mcp_info.get("sanctions") or {}
    risk_indicators = mcp_info.get("risk_indicators") or {}

    rag_score = float(rag_findings.get("risk_score", 0.0) or 0.0)
    mcp_score = float(risk_indicators.get("risk_score", 0.0) or 0.0)
    amount = float(serialized.get("transaction_amount", 0.0) or 0.0)

    combined = min(max((0.75 * rag_score) + (0.25 * mcp_score), 0.0), 1.0)
    sanctions_hit = sanctions.get("status") == "found"
    large_amount_hit = amount >= 50000
    extreme_country_risk = mcp_score >= 0.85

    return {
        "rag_score": rag_score,
        "mcp_score": mcp_score,
        "combined_score": combined,
        "sanctions_hit": sanctions_hit,
        "large_amount_hit": large_amount_hit,
        "extreme_country_risk": extreme_country_risk,
        "hard_rule_triggered": sanctions_hit
        or large_amount_hit
        or (extreme_country_risk and large_amount_hit),
    }


def _decision_badge(decision_upper):
    if decision_upper == "APPROVE":
        return "🟢 APPROVED"
    if decision_upper == "BLOCK":
        return "🔴 BLOCKED"
    return "🟡 MANUAL REVIEW"


def _top_evidence_items(recommendation_view: dict, limit: int = 3) -> list:
    """Return highest-scoring evidence snippets for decision traceability."""
    evidence = recommendation_view.get("supporting_evidence", []) or []
    ranked = sorted(
        evidence,
        key=lambda row: float(row.get("score", 0.0) or 0.0),
        reverse=True,
    )
    return ranked[:limit]


def _executive_decision_line(decision_upper: str, drivers: dict, confidence: float) -> str:
    """Build one concise sentence explaining the primary decision path."""
    reasons = []
    if drivers.get("sanctions_hit"):
        reasons.append("sanctions match")
    if drivers.get("large_amount_hit"):
        reasons.append("amount exceeded the $50k hard gate")
    if drivers.get("extreme_country_risk"):
        reasons.append("extreme country-risk prior")

    if reasons:
        if len(reasons) == 1:
            reason_text = reasons[0]
        elif len(reasons) == 2:
            reason_text = f"{reasons[0]} and {reasons[1]}"
        else:
            reason_text = f"{', '.join(reasons[:-1])}, and {reasons[-1]}"
        return (
            f"Decision: {decision_upper}. This case is primarily driven by {reason_text}. "
            f"Model confidence is {confidence:.0f}%."
        )

    return (
        f"Decision: {decision_upper}. No hard policy gates triggered; outcome is based on fused RAG+MCP risk "
        f"assessment (confidence {confidence:.0f}%)."
    )


def _mcp_mode_badge() -> str:
    """Return a small visual badge for current MCP runtime mode."""
    if MCP_ENABLE_MOCK:
        return (
            '<span style="display:inline-block;padding:0.2rem 0.55rem;border-radius:999px;'
            'background:#fff3cd;color:#7a5d00;font-size:0.8rem;font-weight:600;">'
            "MCP Mode: MOCK</span>"
        )
    return (
        '<span style="display:inline-block;padding:0.2rem 0.55rem;border-radius:999px;'
        'background:#d4edda;color:#1f5f2e;font-size:0.8rem;font-weight:600;">'
        "MCP Mode: LIVE</span>"
    )


st.set_page_config(
    page_title="Multi-Agent Financial Risk Investigation Demo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better visuals
st.markdown(
    """
<style>
    .agent-step {
        padding: 12px;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
        margin-bottom: 8px;
        border-radius: 4px;
    }
    .decision-approved {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .decision-rejected {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .decision-escalated {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🕵️ Multi-Agent Financial Risk Investigation System")
st.markdown(_mcp_mode_badge(), unsafe_allow_html=True)
st.markdown(
    "**Interactive Demo**: Visualize agents in action, explore evidence, and understand decisions."
)

# Sidebar: Input selection
st.sidebar.header("📥 Input Selection")
input_mode = st.sidebar.radio(
    "Choose how to submit a case:",
    ["Manual Entry", "Upload File", "Load Test Scenario"],
    help="Select the way you want to provide transaction/customer data",
)

user_input = None

with st.sidebar.expander("⚡ One-Click Demo Presets", expanded=False):
    st.caption("Load a deterministic case for each decision path.")
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    with preset_col1:
        if st.button("Approve", key="preset_approve", use_container_width=True):
            user_input = _demo_preset_case("approve")
    with preset_col2:
        if st.button("Review", key="preset_review", use_container_width=True):
            user_input = _demo_preset_case("manual_review")
    with preset_col3:
        if st.button("Block", key="preset_block", use_container_width=True):
            user_input = _demo_preset_case("block")

if input_mode == "Manual Entry":
    st.sidebar.subheader("Enter Transaction Details")

    st.sidebar.info(
        "💡 **Tip**: Edit Case ID and Customer ID fields below if needed. "
        "To test sanctions detection, use a name like `vladimir putin` as Customer ID."
    )

    case_refresh_col_left, case_refresh_col_right = st.sidebar.columns([4, 1])
    with case_refresh_col_left:
        st.caption("Need a fresh generated case ID?")
    with case_refresh_col_right:
        if st.button("↻", key="refresh_case_id", help="Generate new case ID"):
            st.session_state.pending_manual_case_id = _new_case_id()
            st.rerun()

    customer_refresh_col_left, customer_refresh_col_right = st.sidebar.columns([4, 1])
    with customer_refresh_col_left:
        st.caption("Need a fresh generated customer ID?")
    with customer_refresh_col_right:
        if st.button("↻", key="refresh_customer_id", help="Generate new customer ID"):
            st.session_state.pending_manual_customer_id = _new_customer_id()
            st.rerun()

    with st.sidebar.form("manual_entry_form"):
        case_id = st.text_input(
            "Case ID", key="manual_case_id", help="Auto-generated, can be overridden"
        )
        customer_id = st.text_input(
            "Customer ID or Name",
            key="manual_customer_id",
            help="Use a sanctioned name to test: vladimir putin, bashar al-assad, etc.",
        )

        transaction_amount = st.number_input(
            "Transaction Amount (USD)", min_value=0.0, value=50000.0, step=1000.0
        )
        transaction_type = st.selectbox(
            "Transaction Type", ["transfer", "withdrawal", "deposit", "payment"]
        )
        channel = st.selectbox(
            "Channel", ["online", "mobile_app", "atm", "branch", "wire_transfer", "international"]
        )
        device_location = st.text_input("Device Location (Country Code)", value="US")

        st.divider()
        st.subheader("📋 Sample Sanctioned Names")
        st.caption(
            "To trigger **sanctions hit**, paste one of these into Customer ID field:\n\n"
            "`vladimir putin` | `mohammad zarif` | `kim jong un` | `bashar al-assad` | `russian federation`"
        )

        submitted = st.form_submit_button("Submit Transaction", use_container_width=True)
        if submitted:
            user_input = {
                "case_id": case_id,
                "customer_id": customer_id,
                "transaction_amount": transaction_amount,
                "transaction_type": transaction_type,
                "channel": channel,
                "device_location": device_location,
                "customer_profile": {
                    "account_age_days": 365,
                    "avg_monthly_volume": 10000,
                    "previous_txn_count": 120,
                    "country_of_residence": device_location,
                },
                "timestamp": datetime.now().isoformat(),
            }

            # Prepare fresh IDs for the next manual entry on the next rerun.
            st.session_state.pending_manual_case_id = _new_case_id()
            st.session_state.pending_manual_customer_id = _new_customer_id()

elif input_mode == "Upload File":
    st.sidebar.subheader("Upload Transaction File")
    uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type=["json"])
    submit = st.sidebar.button("Process File", use_container_width=True)
    if uploaded_file and submit:
        try:
            user_input = json.load(uploaded_file)
            user_input.setdefault("channel", "online")
            user_input.setdefault("device_location", "US")
            user_input.setdefault("customer_profile", {})
            user_input.setdefault("transaction_type", "transfer")
            st.sidebar.success("File loaded successfully!")
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            st.sidebar.error(f"Error loading file: {e}")

elif input_mode == "Load Test Scenario":
    st.sidebar.subheader("Select Test Scenario")

    # Generate all test cases
    all_test_cases = generate_test_cases()

    # Organize by expected decision and create display labels
    low_risk_cases = [tc for tc in all_test_cases if tc.get("expected_decision") == "approve"]
    high_risk_cases = [tc for tc in all_test_cases if tc.get("expected_decision") == "block"]

    # Create categorized scenario list
    scenario_options = []

    # Low-risk section
    scenario_options.extend(
        [
            f"🟢 [LOW-RISK] {tc['case_id']} - {tc['customer_id'][:20]} | ${tc['transaction_amount']:,.0f}"
            for tc in low_risk_cases
        ]
    )

    # High-risk section
    scenario_options.extend(
        [
            f"🔴 [HIGH-RISK] {tc['case_id']} - {tc['customer_id'][:20]} | ${tc['transaction_amount']:,.0f}"
            for tc in high_risk_cases
        ]
    )

    if scenario_options:
        scenario_name = st.sidebar.selectbox(
            "Choose a test case:",
            scenario_options,
            help=f"Total: {len(low_risk_cases)} low-risk + {len(high_risk_cases)} high-risk cases",
        )
        submit = st.sidebar.button("Run Test Scenario", use_container_width=True)
        if submit:
            # Find the selected case
            selected_idx = scenario_options.index(scenario_name)
            user_input = all_test_cases[selected_idx]
            st.sidebar.success(f"✅ Loaded: {user_input['case_id']}")
    else:
        st.sidebar.warning("No test scenarios available")

# Process if user submitted input
if user_input:
    st.success("🔄 Processing case... Please wait.")

    # Run the investigation workflow
    with st.spinner("Agents are analyzing the transaction..."):
        try:
            workflow_result = run_investigation(user_input)
            serializable_result = _serialize_result(workflow_result)
            drivers = _calculate_decision_drivers(serializable_result)
        except (RuntimeError, TypeError, ValueError) as e:
            st.error(f"Error during investigation: {e}")
            st.stop()

    recommendation_view = serializable_result.get("recommendation") or {}
    raw_decision = recommendation_view.get("decision", "unknown")
    decision = str(raw_decision).upper()
    confidence = recommendation_view.get("confidence", 0) * 100
    risk_level = recommendation_view.get("risk_level", "unknown").upper()

    st.subheader("📌 Decision Summary")
    top_col1, top_col2, top_col3, top_col4 = st.columns(4)
    with top_col1:
        st.metric("Final Decision", _decision_badge(decision))
    with top_col2:
        st.metric("Confidence", f"{confidence:.0f}%")
    with top_col3:
        st.metric("Risk Level", risk_level)
    with top_col4:
        st.metric("Combined Risk Score", f"{drivers['combined_score']:.2f}")

    # Transaction Details
    st.subheader("💳 Transaction Details")
    txn_col1, txn_col2, txn_col3 = st.columns(3)
    with txn_col1:
        st.metric("Case ID", serializable_result.get("case_id", "N/A"))
    with txn_col2:
        st.metric("Customer ID", serializable_result.get("customer_id", "N/A"))
    with txn_col3:
        st.metric("Amount", f"${serializable_result.get('transaction_amount', 0):,.2f}")

    txn_col4, txn_col5, txn_col6 = st.columns(3)
    with txn_col4:
        st.metric("Type", serializable_result.get("transaction_type", "N/A"))
    with txn_col5:
        st.metric("Channel", serializable_result.get("channel", "N/A"))
    with txn_col6:
        st.metric("Location", serializable_result.get("device_location", "N/A"))

    if decision == "BLOCK" and risk_level == "LOW" and drivers["hard_rule_triggered"]:
        st.warning(
            "Decision/risk-level mismatch is expected here: case was blocked by a hard policy gate "
            "(e.g., transaction amount threshold or sanctions hit), even though model risk category is low."
        )

    tabs = st.tabs(["Executive View", "Agent Timeline", "Evidence", "Debug & Export"])

    with tabs[0]:
        st.subheader("📊 Risk Breakdown")
        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("RAG Risk Score", f"{drivers['rag_score']:.2f}")
            st.progress(min(max(drivers["rag_score"], 0.0), 1.0))
        with k2:
            st.metric("MCP Risk Score", f"{drivers['mcp_score']:.2f}")
            st.progress(min(max(drivers["mcp_score"], 0.0), 1.0))
        with k3:
            st.metric("Fused Risk Score", f"{drivers['combined_score']:.2f}")
            st.progress(min(max(drivers["combined_score"], 0.0), 1.0))

        st.subheader("🚦 Policy Gate Signals")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.metric("Sanctions Hit", "YES" if drivers["sanctions_hit"] else "NO")
        with g2:
            st.metric("High-Amount Gate (>=50k)", "YES" if drivers["large_amount_hit"] else "NO")
        with g3:
            st.metric("Extreme Country Risk", "YES" if drivers["extreme_country_risk"] else "NO")

        # MCP Diagnostics
        st.subheader("🔍 MCP Sanctions Lookup (Diagnostic)")
        mcp_signals = serializable_result.get("mcp_signals") or {}
        sanctions_result = mcp_signals.get("sanctions") or {}

        diag_col1, diag_col2, diag_col3 = st.columns(3)
        with diag_col1:
            st.metric("Status", sanctions_result.get("status", "unknown").upper())
        with diag_col2:
            st.metric("Entity Searched", serializable_result.get("customer_id", "N/A")[:25])
        with diag_col3:
            st.metric("Confidence", f"{sanctions_result.get('confidence', 0):.2f}")

        if sanctions_result.get("lists"):
            st.success(f"**Matched lists**: {', '.join(sanctions_result.get('lists', []))}")
        if sanctions_result.get("matched_name"):
            st.info(f"**Matched entity**: {sanctions_result.get('matched_name')}")
        if sanctions_result.get("reason"):
            st.caption(f"Reason: {sanctions_result.get('reason')}")

        st.subheader("📝 Rationale")
        st.info(recommendation_view.get("rationale", "No rationale provided"))

        st.subheader("✅ Next Actions")
        actions = recommendation_view.get("next_actions", [])
        if actions:
            for action in actions:
                st.write(f"• {action}")
        else:
            st.write("No actions provided")

    with tabs[1]:
        st.subheader("🔎 Agent Timeline")

        # Extract and display agent trace
        agent_trace = serializable_result.get("conversation_log", [])
        if not agent_trace:
            st.info("No agent trace available")
        else:
            for i, step in enumerate(agent_trace, 1):
                with st.expander(
                    f"**Step {i}**: {step.get('agent', 'Unknown Agent')} - {step.get('action', 'No action')}"
                ):
                    st.write(f"**Agent**: {step.get('agent')}")
                    st.write(f"**Action**: {step.get('action')}")
                    st.code(json.dumps(step, indent=2), language="json")

    with tabs[2]:
        st.subheader("🎯 Decision Evidence Snapshot")

        rag_evidence = serializable_result.get("rag_findings") or {}
        mcp_evidence = serializable_result.get("mcp_signals") or {}
        sanctions_result = mcp_evidence.get("sanctions") or {}
        risk_result = mcp_evidence.get("risk_indicators") or {}
        adverse_result = mcp_evidence.get("adverse_media") or {}
        top_evidence = _top_evidence_items(recommendation_view, limit=3)

        snap_col1, snap_col2, snap_col3, snap_col4 = st.columns(4)
        with snap_col1:
            st.metric("Decision", _decision_badge(decision))
        with snap_col2:
            st.metric("Confidence", f"{confidence:.0f}%")
        with snap_col3:
            st.metric("Hard Rule Gate", "YES" if drivers["hard_rule_triggered"] else "NO")
        with snap_col4:
            st.metric(
                "Evidence Used", str(len(recommendation_view.get("supporting_evidence", []) or []))
            )

        signal_labels = []
        if drivers["sanctions_hit"]:
            signal_labels.append("Sanctions match")
        if drivers["large_amount_hit"]:
            signal_labels.append("Large-amount policy gate")
        if drivers["extreme_country_risk"]:
            signal_labels.append("Extreme country-risk prior")
        if not signal_labels:
            signal_labels.append("No hard policy gates triggered")

        st.info(_executive_decision_line(decision, drivers, confidence))
        st.caption("Primary decision signals: " + ", ".join(signal_labels))

        left_col, right_col = st.columns([1.15, 1])

        with left_col:
            st.subheader("📄 Highest-Impact RAG Evidence")
            if top_evidence:
                for idx, evidence_row in enumerate(top_evidence, 1):
                    source = evidence_row.get("source", "Unknown source")
                    score = float(evidence_row.get("score", 0.0) or 0.0)
                    text = evidence_row.get("text", "No excerpt available")
                    st.markdown(f"**{idx}. {source}**")
                    st.caption(f"Relevance: {score:.2f}")
                    st.write(text[:240] + ("..." if len(text) > 240 else ""))
            else:
                st.info("No supporting RAG evidence was attached to this recommendation.")

            pattern_matches = rag_evidence.get("pattern_matches", []) or []
            policy_violations = rag_evidence.get("policy_violations", []) or []
            if pattern_matches or policy_violations:
                st.markdown("**Detected patterns and policy references**")
                if pattern_matches:
                    st.write("Patterns: " + ", ".join(pattern_matches[:5]))
                if policy_violations:
                    st.write("Policies: " + ", ".join(policy_violations[:5]))

            with st.expander("View Full RAG Findings JSON"):
                st.json(rag_evidence)

        with right_col:
            st.subheader("🌐 MCP Signals Used For Decision")

            sanctions_status = str(sanctions_result.get("status", "unknown")).upper()
            sanctions_conf = float(sanctions_result.get("confidence", 0.0) or 0.0)
            if sanctions_status == "FOUND":
                st.error(f"Sanctions status: {sanctions_status} (confidence: {sanctions_conf:.2f})")
            elif sanctions_status == "UNAVAILABLE":
                st.warning(f"Sanctions status: {sanctions_status}")
            else:
                st.success(
                    f"Sanctions status: {sanctions_status} (confidence: {sanctions_conf:.2f})"
                )

            matched_name = sanctions_result.get("matched_name")
            if matched_name:
                st.caption(f"Matched entity: {matched_name}")

            mcp_risk_score = float(risk_result.get("risk_score", 0.0) or 0.0)
            st.metric("Country Risk Prior", f"{mcp_risk_score:.2f}")
            st.caption(risk_result.get("reason", "No country-risk rationale returned"))

            adverse_severity = str(adverse_result.get("severity", "unknown")).upper()
            adverse_mentions = int(adverse_result.get("mentions_found", 0) or 0)
            st.metric("Adverse Media Severity", adverse_severity)
            st.caption(f"Mentions found: {adverse_mentions}")

            with st.expander("View Full MCP Evidence JSON"):
                st.json(mcp_evidence)

    with tabs[3]:
        rag_evidence = serializable_result.get("rag_findings") or {}
        mcp_evidence = serializable_result.get("mcp_signals") or {}
        agent_trace = serializable_result.get("conversation_log", [])

        with st.expander("📋 Full Debug Trace"):
            st.code(
                json.dumps(
                    {
                        "input": user_input,
                        "agent_trace": agent_trace,
                        "rag_evidence": rag_evidence,
                        "mcp_evidence": mcp_evidence,
                        "result": serializable_result,
                    },
                    indent=2,
                ),
                language="json",
            )

        st.subheader("📥 Export Results")
        json_str = json.dumps(serializable_result, indent=2)
        st.download_button(
            label="Download Full Results (JSON)",
            data=json_str,
            file_name=f"case_{user_input.get('case_id', 'unknown')}_result.json",
            mime="application/json",
        )

else:
    st.info("👈 Select an input method in the sidebar and submit to begin the analysis.")

    with st.expander("📋 Sample Sanctioned Entities (For Demo)"):
        st.markdown("""
**Use these names to trigger a sanctions hit and see how the system detects it:**

| Entity Name | Type | Impact |
|-------------|------|--------|
| `vladimir putin` | Person | ✅ Triggers sanctions block |
| `mohammad zarif` | Person | ✅ Triggers sanctions block |
| `kim jong un` | Person | ✅ Triggers sanctions block |
| `bashar al-assad` | Person | ✅ Triggers sanctions block |
| `russian federation` | Organization | ✅ Triggers sanctions block |
| `bank of iran` | Organization | ✅ Triggers sanctions block |
| `supreme leader of iran` | Person/Title | ✅ Triggers sanctions block |

**How to use:**
1. Select "Manual Entry" in the sidebar
2. Copy one of the names above
3. Paste into the "Customer ID" field (or use it as the customer name)
4. The system will detect it on OFAC SDN list and flag as sanctions hit
5. Final decision will be BLOCKED with "file_suspicious_activity_report" action
        """)

    st.markdown("---")
    st.subheader("💡 How It Works")
    st.markdown("""
1. **Choose Input**: Manual entry, file upload, or test scenario
2. **Submit**: The system processes the transaction through multiple agents
3. **View Results**: 
   - Decision with confidence score
   - Agent timeline showing what each agent did
   - RAG evidence with source documents
   - MCP evidence from external data sources
   - Full trace log for transparency
    """)

    st.markdown("---")
    st.subheader("🎯 Multi-Agent System")
    st.markdown("""
- **Intake Agent**: Receives and validates transaction data
- **RAG Agent**: Retrieves relevant policies and historical patterns
- **Recommendation Agent**: Combines evidence and makes final decision
    """)
