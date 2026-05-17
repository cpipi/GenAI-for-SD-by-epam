# Streamlit Web App Demo

## Quick Start

The interactive web app is your demo interface for presentations and evaluations.

### Installation

From the `financial-risk-assistant/` directory:

```bash
pip install -r requirements.txt
```

(Streamlit is now included in `requirements.txt`)

### Running the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

### Features

1. **Input Methods**:
   - Manual Entry: Type transaction details directly
   - Upload File: Load a JSON file with transaction data
   - Load Test Scenario: Run pre-built positive/negative/adversarial test cases

2. **Agent Timeline**: Watch each agent execute in sequence with detailed traces

3. **Decision Display**: See final decision with confidence score and risk level

4. **RAG Evidence**: View source documents retrieved from the knowledge base

5. **MCP Evidence**: Display external data (sanctions, adverse media, FX rates, etc.)

6. **Full Debug Trace**: Export raw JSON for technical review

7. **Download Results**: Export case analysis as JSON for records

### Demo Recording Tips

1. Run a **positive case** first (fast, shows happy path)
2. Then run a **negative case** (shows how system catches risk)
3. Use the sidebar to narrate what the system is doing
4. Point out the agent timeline to explain orchestration
5. Highlight specific evidence to show RAG and MCP integration
6. Export a result to show data transparency

### For Investors/Committee

The UI is designed to:
- ✅ Show multi-agent orchestration in real-time
- ✅ Demonstrate RAG retrieval with source attribution
- ✅ Display external data integration (MCP)
- ✅ Provide full transparency (trace logs, evidence)
- ✅ Highlight business value (automated risk decisions)

### Troubleshooting

If imports fail:
```bash
# Ensure you're in the financial-risk-assistant directory
cd financial-risk-assistant

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run again
streamlit run streamlit_app.py
```

If data generator is missing:
- Ensure `data_generator.py` exists in the same directory
- Check that all agent modules (agents/, rag/, mcp/) are present

---

**Next Steps**: Record your demo video using this interface!
