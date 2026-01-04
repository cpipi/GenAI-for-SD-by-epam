"""LangChain-based agent orchestrator for weather and news queries."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from .mcp_clients import MCPNewsClient, MCPOpenMeteoClient


@dataclass
class OrchestratorConfig:
    model: str = os.getenv("CHAT_MODEL", "claude-3-5-sonnet-latest")
    temperature: float = 0.0
    news_limit: int = 5


class AgentOrchestrator:
    """Routes user intents to MCP-backed tools and aggregates responses."""

    def __init__(self, config: Optional[OrchestratorConfig] = None) -> None:
        self.config = config or OrchestratorConfig()
        self.weather_client = MCPOpenMeteoClient()
        self.news_client = MCPNewsClient()
        self.llm = ChatAnthropic(model=self.config.model, temperature=self.config.temperature)
        self.intent_chain = self._build_intent_chain()

    def _build_intent_chain(self) -> RunnableSequence:
        prompt = PromptTemplate(
            template=(
                "You are an intent classifier for a multi-tool assistant. "
                "Given the user query, answer with one of: weather, news, both, unknown.\n"
                "Respond with a single lowercase word.\n"
                "Query: {query}"
            )
        )
        return prompt | self.llm

    def _fallback_intents(self, query: str) -> Set[str]:
        lowered = query.lower()
        intents: Set[str] = set()
        weather_keywords = ["weather", "temperature", "rain", "forecast", "wind"]
        news_keywords = ["news", "headline", "latest", "update", "breaking"]

        if any(word in lowered for word in weather_keywords):
            intents.add("weather")
        if any(word in lowered for word in news_keywords):
            intents.add("news")
        return intents

    def classify_intent(self, query: str) -> Set[str]:
        heuristic = self._fallback_intents(query)
        if heuristic:
            return heuristic

        try:
            llm_result = self.intent_chain.invoke({"query": query})
            raw = llm_result.content.strip().lower()
            if "weather" in raw:
                heuristic.add("weather")
            if "news" in raw:
                heuristic.add("news")
        except Exception:
            pass

        return heuristic or {"unknown"}

    def handle_query(self, query: str) -> Dict[str, any]:
        intents = self.classify_intent(query)
        response: Dict[str, any] = {"intents": list(intents)}

        if "weather" in intents:
            response["weather"] = self.weather_client.fetch_weather(query)
        if "news" in intents:
            response["news"] = self.news_client.fetch_news(query, limit=self.config.news_limit)

        if intents == {"unknown"}:
            response["message"] = "I could not determine if you want weather or news. Please ask about either."
        return response
