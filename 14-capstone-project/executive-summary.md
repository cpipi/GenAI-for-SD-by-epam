# Executive Summary

## Project Overview
This capstone delivers a multi-agent financial risk investigation assistant that performs first-line triage of suspicious transactions using synthetic data. The system combines retrieval-augmented reasoning from internal knowledge with external enrichment signals and returns a structured decision: approve, manual review, or block.

## Why This Project Exists
In real financial operations, analysts often spend significant time assembling context from transaction payloads, policy documents, and external signals before making consistent decisions. This project targets that bottleneck by automating the first investigation pass while preserving transparent evidence and human oversight.

## Solution in One Line
A three-agent LangGraph workflow validates case data, retrieves relevant risk evidence, enriches with external MCP signals, and outputs an explainable decision with next actions.

## Key Technical Decisions
1. Multi-agent architecture with explicit role separation
- Intake Agent validates and normalizes input
- Risk Pattern Agent executes RAG retrieval and risk finding generation
- Recommendation Agent synthesizes RAG + MCP signals into final decision

2. Hybrid RAG design
- Local hybrid retrieval scoring for stable baseline behavior
- Optional Claude reranking for higher retrieval quality
- Citation-bearing evidence attached to each recommendation

3. MCP strategy aligned to delivery constraints
- Mock mode for deterministic test runs
- Live enrichment mode using public external APIs for country-level context
- Transparent fallback behavior when live tools are unavailable

4. Reliability-first development approach
- Deterministic decision thresholds for reproducible tests
- Optional LLM rationale generation for analyst-quality explanations
- Continuous end-to-end testing including adversarial cases

## Results and Current Outcomes
- End-to-end workflow implemented and runnable locally
- Full test suite passing (29/29: 25 scenarios + 4 adversarial)
- RAG mode comparison generated for evidence-based reporting
- Claude reranking validated in live mode with measurable ranking changes

## Validation Evidence
1. Functional reliability
- 24/24 automated scenarios pass: 20 positive and 4 adversarial
- Includes malformed input, invalid channels, and high-risk edge conditions

2. Retrieval quality uplift
- Reranking executed successfully on all evaluated cases (20/20)
- Top-1 retrieved document changed in 7/20 cases
- Top-5 ranking order changed in 20/20 cases

3. Explainability and auditability
- Each decision includes evidence citations, decision rationale, and next actions
- Agent execution trace is captured for every run

4. MCP live-integration evidence
- A dedicated live MCP evidence run is generated in `financial-risk-assistant/mcp_evidence_report.json`
- The report includes sanctions checks, adverse-media checks, and country-risk enrichment outputs
- This demonstrates non-mock external signal integration beyond a single source

## Business Value
- Faster initial triage for suspicious transactions
- More consistent and explainable decision support
- Reduced analyst overhead for routine screening
- Better auditability through explicit evidence and execution trace

## Trade-Offs
- Live sanctions/adverse-media connectors are not fully production-integrated yet
- External data quality is constrained by no-key public APIs in this scope
- Decision policy is intentionally conservative and rule-guided for testability

## Next Steps
1. Connect enterprise-grade sanctions and adverse-media feeds via MCP
2. Add role-based access controls and stronger operational logging
3. Expand evaluation to retrieval relevance and calibration metrics
4. Package a lightweight UI for non-technical users

## Conclusion
The project meets capstone requirements with a practical, testable, and business-relevant multi-agent system. It demonstrates a credible path from proof-of-concept to production-oriented implementation in a financial risk context.
