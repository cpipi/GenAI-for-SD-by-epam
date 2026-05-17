"""RAG agent logic for risk pattern and policy retrieval and scoring."""

import logging

from graph_state import Evidence, RiskFindings, State
from rag.rag_setup import get_rag_system


def rag_agent(state: State) -> State:
    try:
        transaction_type = state.get("transaction_type") or "unknown"
        channel = state.get("channel") or "unknown"
        customer_id = state.get("customer_id") or "unknown"
        location = state.get("device_location") or "unknown"
        amount = state.get("transaction_amount", 0)
        profile = state.get("customer_profile") or {}
        account_age = profile.get("account_age_days", "unknown")
        txn_count = profile.get("previous_txn_count", "unknown")

        query = (
            f"transaction_type={transaction_type}; channel={channel}; location={location}; "
            f"amount={amount}; account_age_days={account_age}; previous_txn_count={txn_count}; "
            f"customer_id={customer_id}; find relevant fraud patterns, AML policy checks, and escalation playbooks"
        )

        # Retrieve from vector store
        rag_system = get_rag_system()
        retrieved_docs = rag_system.retrieve(query, k=5)
        state["retrieved_documents"] = retrieved_docs

        # Analyze patterns and determine risk
        similarity_scores = []
        pattern_matches = []
        policy_violations = []
        evidence_list = []

        for doc in retrieved_docs:
            similarity = doc.get("similarity_score", 0.5)
            similarity_scores.append(float(similarity))

            source = doc.get("source", "")
            doc_type = doc.get("type", "")

            if source == "risk_pattern":
                pattern_matches.append(doc_type)
            elif source == "policy":
                policy_violations.append(doc_type)

            evidence = Evidence(
                source=f"{source}/{doc_type}", score=similarity, text=doc.get("content", "")[:200]
            )
            evidence_list.append(evidence)

        avg_similarity = sum(similarity_scores) / max(1, len(similarity_scores))

        # Add deterministic transaction/profile signals so scores vary with case data.
        # More discriminative amount_signal: small amounts reduce risk significantly
        if amount < 1000:
            amount_signal = min(
                (float(amount) / 100000.0), 0.05
            )  # Very low for typical daily transactions
        elif amount < 5000:
            amount_signal = min((float(amount) / 50000.0) ** 0.7, 0.15)  # Low for routine business
        else:
            amount_signal = min(
                (float(amount) / 50000.0) ** 0.5, 1.0
            )  # Original scaling for larger amounts

        channel_signal_map = {
            "online": 0.02,
            "mobile_app": 0.05,
            "atm": 0.08,
            "branch": 0.01,
            "wire_transfer": 0.18,
            "international": 0.22,
        }
        transaction_signal_map = {
            "transfer": 0.04,
            "withdrawal": 0.10,
            "deposit": 0.02,
            "payment": 0.05,
        }
        channel_signal = channel_signal_map.get(str(channel), 0.03)
        transaction_signal = transaction_signal_map.get(str(transaction_type), 0.03)
        location_signal = 0.25 if str(location).upper() in ["RU", "IR", "KP", "SY", "CU"] else 0.0
        account_age_signal = (
            0.15 if isinstance(account_age, (int, float)) and account_age < 30 else 0.0
        )
        low_history_signal = 0.1 if isinstance(txn_count, (int, float)) and txn_count < 10 else 0.0

        # Calculate base risk
        risk_score = (
            (0.45 * avg_similarity)
            + (0.22 * amount_signal)
            + (0.12 * channel_signal)
            + (0.08 * transaction_signal)
            + location_signal
            + account_age_signal
            + low_history_signal
        )

        # Apply customer profile quality multiplier: established customers with low-amount transactions get reduced risk
        profile_quality_multiplier = 1.0
        if (
            isinstance(account_age, (int, float))
            and account_age > 180
            and isinstance(txn_count, (int, float))
            and txn_count > 100
            and amount < 5000
        ):
            # Established customer, good history, reasonable amount → reduce risk by 40-50%
            profile_quality_multiplier = 0.55
        elif (
            isinstance(account_age, (int, float))
            and account_age > 90
            and isinstance(txn_count, (int, float))
            and txn_count > 50
            and amount < 2000
        ):
            # Moderately established customer → reduce risk by 20-30%
            profile_quality_multiplier = 0.75

        risk_score = risk_score * profile_quality_multiplier
        risk_score = min(max(risk_score, 0.0), 1.0)

        # Determine risk category
        risk_category = "low"
        if risk_score > 0.6:
            risk_category = "high"
        elif risk_score > 0.3:
            risk_category = "medium"

        # Create findings
        findings = RiskFindings(
            risk_score=risk_score,
            risk_category=risk_category,
            pattern_matches=pattern_matches,
            policy_violations=policy_violations,
            evidence=evidence_list,
            reasoning=(
                f"Avg retrieval similarity {avg_similarity:.2f}; amount signal {amount_signal:.2f}; "
                f"channel signal {channel_signal:.2f}; transaction signal {transaction_signal:.2f}; "
                f"location signal {location_signal:.2f}. "
                f"Identified {len(pattern_matches)} matching patterns and {len(policy_violations)} policy considerations"
            ),
        )

        state["rag_findings"] = findings

        log_entry = {
            "agent": "rag",
            "action": "retrieval_and_analysis",
            "risk_score": findings.risk_score,
            "risk_category": findings.risk_category,
            "patterns_found": len(pattern_matches),
        }
        state["conversation_log"].append(log_entry)

        return state
    except Exception as e:
        logging.error(f"Error in rag_agent: {e}")
        state["rag_findings"] = None
        state["retrieved_documents"] = []
        return state
