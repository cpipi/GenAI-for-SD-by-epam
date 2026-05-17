"""RAG setup: hybrid local retrieval with optional Claude reranking."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from config import (
    CLAUDE_API_KEY,
    LLM_MODEL,
    RAG_CANDIDATE_POOL,
    RAG_USE_CLAUDE_RERANK,
    TOP_K_RETRIEVAL,
)


class HybridRAGSystem:
    """Hybrid in-memory retriever with lexical scoring + optional LLM rerank."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.documents: list[dict[str, Any]] = []
        self.client = Anthropic(api_key=CLAUDE_API_KEY) if CLAUDE_API_KEY else None
        self.last_rerank_status = "not_attempted"
        self.last_rerank_error = ""

    def load_corpus(self) -> list[dict[str, Any]]:
        """Load all documents into memory."""
        documents = []

        patterns_path = Path(self.data_dir) / "risk_patterns.json"
        if patterns_path.exists():
            with open(patterns_path, encoding="utf-8") as f:
                patterns = json.load(f)
            for p in patterns:
                documents.append(
                    {
                        "content": (
                            f"Risk Pattern: {p['risk_type']}\n"
                            f"Description: {p['description']}\n"
                            f"Indicators: {', '.join(p['indicators'])}\n"
                            f"Outcome: {p.get('historical_outcome', 'unknown')}"
                        ),
                        "source": "risk_pattern",
                        "type": p["risk_type"],
                        "severity": p.get("severity", "medium"),
                    }
                )

        policies_path = Path(self.data_dir) / "policies.json"
        if policies_path.exists():
            with open(policies_path, encoding="utf-8") as f:
                policies = json.load(f)
            for pol in policies:
                documents.append(
                    {
                        "content": (
                            f"Policy: {pol['title']}\n"
                            f"Type: {pol['type']}\n"
                            f"Content: {pol['content']}\n"
                            f"Version: {pol['version']}"
                        ),
                        "source": "policy",
                        "type": pol["type"],
                        "severity": pol.get("severity_level", "warning"),
                    }
                )

        playbooks_path = Path(self.data_dir) / "playbooks.json"
        if playbooks_path.exists():
            with open(playbooks_path, encoding="utf-8") as f:
                playbooks = json.load(f)
            for pb in playbooks:
                documents.append(
                    {
                        "content": (
                            f"Playbook Scenario: {pb['scenario']}\n"
                            f"Escalation: {pb.get('escalation_threshold', 'amber')}\n"
                            f"Steps: {', '.join(pb['investigation_steps'])}"
                        ),
                        "source": "playbook",
                        "type": pb.get("scenario", "general"),
                        "severity": pb.get("escalation_threshold", "amber"),
                    }
                )

        print(f"Loaded {len(documents)} documents for RAG corpus")
        return documents

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[a-zA-Z0-9_]+", text.lower())

    def _lexical_overlap(self, query: str, text: str) -> float:
        query_tokens = set(self._tokenize(query))
        text_tokens = set(self._tokenize(text))
        if not query_tokens:
            return 0.0
        return len(query_tokens.intersection(text_tokens)) / len(query_tokens)

    def _sequence_similarity(self, query: str, text: str) -> float:
        return SequenceMatcher(None, query.lower(), text.lower()).ratio()

    def _severity_boost(self, severity: str) -> float:
        severity_map = {
            "high": 1.0,
            "critical": 1.0,
            "red": 1.0,
            "medium": 0.7,
            "warning": 0.7,
            "amber": 0.7,
            "low": 0.4,
            "info": 0.4,
        }
        return severity_map.get(str(severity).lower(), 0.5)

    def _source_boost(self, source: str) -> float:
        # Policies and risk patterns are generally higher-value for this use case.
        source_map = {
            "risk_pattern": 1.0,
            "policy": 0.9,
            "playbook": 0.8,
        }
        return source_map.get(source, 0.7)

    def _hybrid_score(self, query: str, doc: dict[str, Any]) -> float:
        content = doc.get("content", "")
        lexical = self._lexical_overlap(query, content)
        seq = self._sequence_similarity(query, content)
        severity = self._severity_boost(doc.get("severity", "medium"))
        source = self._source_boost(doc.get("source", ""))

        # Weighted blend keeps scoring deterministic and explainable.
        return (0.45 * lexical) + (0.25 * seq) + (0.2 * severity) + (0.1 * source)

    def _claude_rerank(
        self, query: str, candidates: list[dict[str, Any]], k: int, enabled: bool
    ) -> list[dict[str, Any]]:
        if not self.client or not enabled:
            self.last_rerank_status = "disabled_or_no_key"
            return candidates[:k]

        numbered_docs = []
        for idx, doc in enumerate(candidates):
            numbered_docs.append(
                f"[{idx}] source={doc['source']} type={doc.get('type', '')}\n{doc['content'][:600]}"
            )

        prompt = (
            "You are a retrieval reranker for a financial risk investigation assistant.\n"
            f"Query: {query}\n\n"
            "Return ONLY a comma-separated list of the best document indexes in descending relevance.\n"
            f"Choose exactly {k} indexes from the list below.\n\n" + "\n\n".join(numbered_docs)
        )

        try:
            response = self.client.messages.create(
                model=LLM_MODEL,
                max_tokens=60,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text if response.content else ""
            idxs = []
            for part in text.split(","):
                part = part.strip().replace("[", "").replace("]", "")
                if part.isdigit():
                    idx = int(part)
                    if 0 <= idx < len(candidates):
                        idxs.append(idx)
            if not idxs:
                self.last_rerank_status = "fallback_parse_failure"
                return candidates[:k]
            reranked = [candidates[i] for i in idxs[:k]]
            # Ensure exact k documents.
            if len(reranked) < k:
                used = set(idxs)
                for i, cand in enumerate(candidates):
                    if i in used:
                        continue
                    reranked.append(cand)
                    if len(reranked) == k:
                        break
            self.last_rerank_status = "claude_success"
            return reranked
        except Exception as e:
            # Fall back to deterministic local rank in case of API or parsing issues.
            self.last_rerank_status = "fallback_exception"
            self.last_rerank_error = str(e)[:200]
            return candidates[:k]

    def retrieve(
        self,
        query: str,
        k: int = TOP_K_RETRIEVAL,
        candidate_pool: int = RAG_CANDIDATE_POOL,
        use_claude_rerank: bool = None,
    ) -> list[dict[str, Any]]:
        """Retrieve with hybrid scoring + optional Claude reranking."""
        if not self.documents:
            self.documents = self.load_corpus()

        rerank_enabled = RAG_USE_CLAUDE_RERANK if use_claude_rerank is None else use_claude_rerank

        scored_docs = []
        for doc in self.documents:
            score = self._hybrid_score(query, doc)
            scored_docs.append((doc, score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_candidates = [
            {
                "content": doc["content"],
                "source": doc["source"],
                "type": doc.get("type", ""),
                "similarity_score": float(score),
            }
            for doc, score in scored_docs[: max(candidate_pool, k)]
        ]

        reranked = self._claude_rerank(query, top_candidates, k=k, enabled=rerank_enabled)
        return reranked


_rag_system = None


def get_rag_system(data_dir: str = "data"):
    """Get or create the global RAG system."""
    global _rag_system
    if _rag_system is None:
        _rag_system = HybridRAGSystem(data_dir=data_dir)
        _rag_system.documents = _rag_system.load_corpus()
    return _rag_system
