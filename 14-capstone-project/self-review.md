# Self-Review

## What Was Implemented Well
1. Clear separation of agent responsibilities
- The workflow follows a strict 3-agent sequence with explicit state transfer.
- Agent trace is visible in outputs, making behavior easier to audit.

2. Strong reliability baseline
- Deterministic decision logic keeps regression tests stable.
- Adversarial tests are included and currently pass.

3. Practical RAG upgrades
- Transitioned from simple matching to hybrid retrieval.
- Added optional Claude reranking for quality improvements without sacrificing fallback reliability.

4. Real-world alignment
- Problem framing and architecture align with financial risk investigation use cases.
- MCP integration path is realistic and incrementally extendable.

## What Could Be Better
1. MCP depth
- Live country enrichment, sanctions list lookup, and adverse-media scanning are all implemented via public APIs (World Bank, OFAC SDN, Google News RSS).
- Configurable mock/live modes available for testing and production use.

2. Evaluation depth
- Current testing emphasizes correctness and robustness.
- Retrieval precision/recall and decision calibration metrics should be expanded.

3. User experience
- Streamlit web UI implemented with decision-first evidence layout, executive rationale, and one-click demo presets.
- Live/mock MCP mode badge provides clear operational status visibility.

## Key Trade-Offs Made
1. Deterministic policy vs fully generative decisions
- Chosen for reproducibility and test reliability under deadline constraints.

2. Public APIs vs enterprise connectors
- Chosen to avoid credentials and infrastructure overhead during capstone delivery.

3. Incremental scope control
- Focused on a strong end-to-end system first, then layered advanced RAG quality improvements.

## Risks and Mitigations
1. External API instability
- Mitigated by fallback defaults and mock mode.

2. LLM model availability drift
- Mitigated by environment-configurable model IDs and runtime diagnostics.

3. Cost drift from LLM usage
- Mitigated via optional toggles for reranking and rationale generation.

## Production Readiness Assessment
Current readiness: PoC/MVP+.

Needed for production:
- Enterprise MCP connectors for sanctions/news
- Security hardening and access control
- Expanded monitoring and SLOs
- Human review workflow integration

## Final Assessment
The project is technically solid for capstone evaluation and demonstrates meaningful business applicability. The architecture and testing approach show a clear understanding of both AI engineering and operational constraints.
