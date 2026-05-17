"""Intake agent logic for input validation and structuring."""

import logging

from graph_state import State


def intake_agent(state: State) -> State:
    """
    Intake Agent: Validates and structures case input.
    Args:
        state: The workflow state dictionary.
    Returns:
        Updated state with validation results and errors.
    """
    try:
        errors = []
        # Validate required fields
        required_fields = [
            "case_id",
            "customer_id",
            "transaction_amount",
            "transaction_type",
            "channel",
        ]
        for field in required_fields:
            if field not in state or not state[field]:
                errors.append(f"Missing required field: {field}")
        # Validate transaction amount
        if state.get("transaction_amount", 0) < 0:
            errors.append("Transaction amount must be non-negative")
        # Validate channel
        valid_channels = ["online", "mobile_app", "atm", "branch", "wire_transfer", "international"]
        if state.get("channel") not in valid_channels:
            errors.append(f"Invalid channel. Must be one of: {valid_channels}")
        state["intake_valid"] = len(errors) == 0
        state["intake_errors"] = errors
        log_entry = {
            "agent": "intake",
            "action": "validation",
            "valid": state["intake_valid"],
            "errors": errors,
        }
        state["conversation_log"].append(log_entry)
        return state
    except Exception as e:
        logging.error(f"Error in intake_agent: {e}")
        state["intake_valid"] = False
        state["intake_errors"] = [f"Internal error: {e}"]
        return state
