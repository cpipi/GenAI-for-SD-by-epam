Project title:
Multi-Agent Financial Risk Investigation Assistant (Synthetic Data)

Problem the system solves:
Risk/fraud analysts spend too much time manually reviewing suspicious transaction patterns, checking internal policy documents, and searching external context before deciding whether to escalate a case.
The system reduces investigation time and improves consistency by using a multi-agent workflow that automatically analyzes a suspicious scenario, retrieves relevant historical/policy knowledge, and produces a structured recommendation with evidence.

Why this is a real-world problem:
Financial organizations need faster and more explainable first-line triage for suspicious behavior (fraud/AML-like patterns), while keeping human-in-the-loop for final decisions.

Agent architecture (minimum 3 agents):

Case Intake Agent

Validates and structures user/case input (transaction sequence, customer profile, channel/device metadata).
Detects missing fields and asks follow-up questions.
Risk Pattern Agent (RAG Agent)

Retrieves similar historical synthetic fraud/risk patterns and internal rule snippets from vector DB.
Scores pattern similarity and produces evidence-based risk indicators with citations.
Recommendation Agent (Decision/Synthesis Agent)

Combines findings from intake + RAG outputs + external signals.
Returns final recommendation: approve / manual review / block, confidence, rationale, and next actions.
(Optional 4th for stronger scope)
4. External Context Agent (MCP Tool Agent)

Uses MCP tools to pull external signals (e.g., sanctions list snapshot, geo-risk index, adverse-news feed, exchange-rate anomalies) and passes normalized context to the Recommendation Agent.
RAG usage (what it is used for):

Domain knowledge retrieval over a synthetic corpus:
Synthetic historical risk/fraud cases
Internal policy/rulebook documents
Investigation playbooks and escalation guidelines
Purpose:
Ground model responses in evidence
Improve consistency of recommendations
Provide source attribution to reduce hallucinations
Planned RAG stack: LangChain + embeddings + vector store (FAISS or Chroma) + retrieval evaluation on test set.

MCP usage (what it is used for):

MCP is used to connect agents to external tools/data sources in a standardized way.
Initial scope can start with 1–2 MCP integrations (real or mocked adapter, depending on access), such as:
Regulatory/watchlist lookup
External risk indicators (country/merchant/category risk metadata)
Purpose:
Demonstrate tool-augmented agent behavior
Enrich decisions beyond internal RAG corpus
Satisfy requirement for external data/tool integration
Data approach and compliance:

No real bank data will be used.
Entire dataset will be synthetic (generated transactions, entities, case histories, policies).
This avoids privacy/compliance risks while preserving realistic behavior for testing.
Technology choices:

LLM: Claude API (primary, already available budget), OpenAI as fallback
Orchestration: LangGraph
RAG framework: LangChain
App layer: simple Streamlit or CLI demo (final choice after MVP)
Testing: automated positive/negative/adversarial scenario suite
Validation scope (aligned to course criteria):

Positive tests: normal investigation flow, clear high-risk patterns, clear low-risk patterns
Negative/adversarial tests: prompt injection attempts, missing/contradictory data, ambiguous patterns, irrelevant retrieval context
Outputs validated for: consistency, citation presence, robustness, and safe fallback behavior
Expected project outcome:
A working, demonstrable multi-agent assistant that performs end-to-end synthetic case triage with RAG-grounded evidence and MCP-based external context enrichment, delivered with architecture blueprint, test suite, README, self-review, executive summary, and short demo video.