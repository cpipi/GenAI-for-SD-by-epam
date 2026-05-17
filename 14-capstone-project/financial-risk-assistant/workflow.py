"""LangGraph workflow orchestration."""

from langgraph.graph import END, StateGraph

from agents.agents import intake_agent, rag_agent, recommendation_agent
from graph_state import State


def build_workflow():
    """Build the LangGraph workflow."""

    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("intake", intake_agent)
    workflow.add_node("rag", rag_agent)
    workflow.add_node("recommendation", recommendation_agent)

    # Add edges
    workflow.add_edge("intake", "rag")
    workflow.add_edge("rag", "recommendation")
    workflow.add_edge("recommendation", END)

    # Set entry point
    workflow.set_entry_point("intake")

    # Compile to runnable graph
    graph = workflow.compile()
    return graph


def run_investigation(case_data: dict):
    """Run a complete investigation workflow."""

    # Initialize state from case data
    initial_state = State(
        case_id=case_data.get("case_id", "unknown"),
        customer_id=case_data.get("customer_id", "unknown"),
        transaction_amount=case_data.get("transaction_amount", 0),
        transaction_type=case_data.get("transaction_type", "unknown"),
        channel=case_data.get("channel", "unknown"),
        device_location=case_data.get("device_location", "unknown"),
        timestamp=case_data.get("timestamp", "unknown"),
        customer_profile=case_data.get("customer_profile", {}),
        transaction_context=case_data.get("transaction_context", {}),
        intake_valid=False,
        intake_errors=[],
        conversation_log=[],
        errors=[],
    )

    # Build and run workflow
    graph = build_workflow()
    result = graph.invoke(initial_state)

    return result
