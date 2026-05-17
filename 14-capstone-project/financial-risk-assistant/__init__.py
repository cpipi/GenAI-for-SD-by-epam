"""Financial Risk Investigation Assistant - Multi-Agent System

This is a multi-agent system that investigates suspicious financial transactions
using RAG-augmented analysis and external data enrichment via MCP.

Agents:
  - Intake Agent: Validates and structures case input
  - RAG Agent: Retrieves relevant patterns and policies; produces risk findings
  - Recommendation Agent: Synthesizes findings and produces final recommendations

Technology Stack:
  - LLM: Claude API
  - Orchestration: LangGraph
  - RAG: LangChain + FAISS
  - External Data: MCP Adapter (mock + real)
"""

# __init__.py for the package
from workflow import build_workflow, run_investigation

__version__ = "0.1.0"
__all__ = ["run_investigation", "build_workflow"]
