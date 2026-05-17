"""Facade module exposing agent callables used by workflow orchestration.

Keep this module intentionally thin: agent business logic lives in
agents.modules so orchestration imports remain stable.
"""

from agents.modules.intake_agent import intake_agent
from agents.modules.rag_agent import rag_agent
from agents.modules.recommendation_agent import recommendation_agent

__all__ = ["intake_agent", "rag_agent", "recommendation_agent"]
