# Financial Risk Investigation Assistant

Multi-agent system for investigating suspicious financial transactions using RAG-augmented analysis and MCP-integrated external data.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Generate Synthetic Data

```bash
python data_generator.py
```

This generates:
- 100 historical risk patterns
- 50 policy documents
- 20 investigation playbooks
- 25 test cases (12 approve, 5 manual_review, 8 block)
- edge-case test scenarios in `data/edge_test_cases.json`

### 3. Run Tests

```bash
python -m unittest discover tests -p "test_*.py"
```

This runs:
- Positive test cases (normal investigation flow)
- Negative/adversarial test cases (edge cases, invalid inputs)
- Reports pass/fail for each scenario

### 3.3 Linting and Formatting

```bash
ruff check .
black --check .
```

Auto-fix commands:

```bash
ruff check . --fix
black .
```

### 3.1 Compare RAG Modes (for report evidence)

```bash
python evaluate_rag_modes.py
```

This creates `rag_mode_comparison.json` showing top-5 retrieval differences between:
- local-only hybrid retrieval
- hybrid retrieval + Claude reranking

### 3.2 Generate MCP Evidence Report

```bash
python mcp_evidence_runner.py
```

This creates `mcp_evidence_report.json` with compact live evidence for:
- sanctions checks
- adverse-media checks
- country risk enrichment

### 4. Run Interactive CLI Demo

```bash
python main.py
```

Loads a test case and runs the complete multi-agent investigation workflow.

## System Architecture

### Multi-Agent Workflow (LangGraph)

```
INPUT (Case) 
    ↓
[Intake Agent] → Validates case structure
    ↓
[RAG Agent] → Retrieves patterns/policies from vector store
    ↓
[Recommendation Agent] → Synthesizes findings + MCP signals → OUTPUT (Decision)
```

### Agents

1. **Intake Agent**
   - Validates required fields (case_id, customer_id, transaction details)
   - Sanitizes input
   - Produces intake_valid flag

2. **RAG Agent**
   - Queries vector store with case context
   - Retrieves similar risk patterns and relevant policies
   - Produces RiskFindings with citations and evidence

3. **Recommendation Agent**
   - Combines RAG findings with MCP external signals (sanctions, country risk, adverse media)
    - Optionally uses Claude to produce analyst-grade rationale text (decision remains deterministic)
   - Produces final Recommendation: {decision, confidence, rationale, next_actions}
   - Decision: approve | manual_review | block

### RAG Pipeline

- **Corpus**: 100 risk patterns + 50 policy docs + 20 playbooks = ~170 documents
- **Primary Retrieval**: Hybrid local scoring (token overlap + sequence similarity + source/severity weighting)
- **Candidate Stage**: Top-N candidate pool per query
- **Re-ranking**: Optional Claude re-ranker (Sonnet/Opus) over candidate pool
- **Fallback**: Fully local deterministic ranking when API key is missing or API call fails

### MCP Integration

MCP adapter supports both deterministic mock mode and live public-data enrichment:

```python
from mcp.mcp_adapter import get_mcp_adapter

mcp = get_mcp_adapter(use_mock=False)
sanctions_check = mcp.lookup_sanctions_list("entity_name")
risk_signals = mcp.get_risk_indicators("country_code")
media_check = mcp.check_adverse_media("entity_name")
```

Live tools (no API key):
- `lookup_sanctions_list()` - OFAC SDN public list lookup
- `get_risk_indicators()` - World Bank + RestCountries + FX context (`open.er-api.com`)
- `check_adverse_media()` - Google News RSS risk-keyword scan

Mock tools remain available for deterministic testing.

## Agent vs Tool Roles

| Component | Role | Responsibility | File |
|-----------|------|----------------|------|
| Intake Agent | Agent | Validate input structure and required fields | `agents/modules/intake_agent.py` |
| RAG Agent | Agent | Retrieve policy/pattern evidence and compute risk findings | `agents/modules/rag_agent.py` |
| Recommendation Agent | Agent | Fuse RAG + MCP signals and produce decision | `agents/modules/recommendation_agent.py` |
| MCP Adapter | Tool Adapter | Call external/mock data sources (sanctions, risk indicators, adverse media) | `mcp/mcp_adapter.py` |
| RAG System | Tool Adapter | Retrieve and rerank relevant documents | `rag/rag_setup.py` |

Design note:
- Agents own decision logic and workflow state transitions.
- Tools provide external capabilities or data retrieval and should remain side-effect-light from the agent perspective.

## Project Structure

```
financial-risk-assistant/
├── agents/
│   ├── agents.py           # Stable facade re-exporting agent callables
│   ├── modules/
│   │   ├── intake_agent.py
│   │   ├── rag_agent.py
│   │   ├── recommendation_agent.py
│   │   └── rationale_utils.py
│   └── __init__.py
├── rag/
│   ├── rag_setup.py        # Vector store + retrieval logic
│   └── __init__.py
├── mcp/
│   ├── mcp_adapter.py      # MCP tool adapter (mock + real)
│   └── __init__.py
├── tests/
│   ├── test_agents.py      # Unit tests for agent modules and facade exports
│   ├── test_data_generator.py
│   ├── test_scenarios.py   # Test matrix (positive, negative, adversarial)
│   └── __init__.py
├── data/
│   ├── risk_patterns.json       # Generated: 100 risk patterns
│   ├── policies.json            # Generated: 50 policy documents
│   ├── playbooks.json           # Generated: 20 playbooks
│   ├── test_cases.json          # Generated: mixed approve/review/block cases
│   └── edge_test_cases.json     # Generated: deterministic edge-case scenarios
├── rag_mode_comparison.json    # Generated: retrieval mode evidence
├── config.py                   # Configuration
├── graph_state.py              # LangGraph state definitions
├── workflow.py                 # LangGraph workflow orchestration
├── data_generator.py           # Synthetic data generation
├── main.py                     # CLI entry point
├── requirements.txt            # Runtime + code quality dependencies
├── pyproject.toml              # Ruff/Black linting and formatting configuration
├── .env.example                # Environment template
└── README.md                   # This file
```

## Test Strategy

### Positive Tests (12 cases)
- Low-risk transactions (long-standing customers, normal amounts/channels)
- Expected decision: `approve`

### Medium-Risk Tests (5 cases)
- Higher-value but explainable activity that should escalate
- Expected decision: `manual_review`

### High-Risk Tests (8 cases)
- Large amounts, new accounts, high-risk countries
- Expected decision: `block`

### Adversarial Tests (4 scenarios)
- Missing required fields
- Negative transaction amounts
- Invalid channels
- High-risk country + large amount combinations
- Expected: All properly flagged/escalated

## Next Steps (Implementation Roadmap)

### Remaining Work (by May 18)
- [ ] Record demo video (2-5 min)
- [ ] Final README polish and runbook verification
- [ ] Final submission file links update

## Configuration Reference

See `config.py` for:
- LLM model and temperature
- RAG settings (top-K retrieval, candidate pool, Claude rerank toggle)
- MCP behavior (mock vs real)
- Logging level

## Troubleshooting

**RAG comparison report:**
```bash
python evaluate_rag_modes.py
```

**Missing synthetic data:**
```bash
python data_generator.py
```

**Import errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

## License

Educational project for EPAM GenAI Course (May 2026)

## Author

Anuar Sultan
