"""Configuration for the Financial Risk Assistant."""

import os

from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
USE_CLAUDE_RATIONALE = os.getenv("USE_CLAUDE_RATIONALE", "false").lower() == "true"
CLAUDE_RATIONALE_MAX_TOKENS = int(os.getenv("CLAUDE_RATIONALE_MAX_TOKENS", "220"))

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 5
RAG_CANDIDATE_POOL = int(os.getenv("RAG_CANDIDATE_POOL", "12"))
RAG_USE_CLAUDE_RERANK = os.getenv("RAG_USE_CLAUDE_RERANK", "true").lower() == "true"

# Data Configuration
SYNTHETIC_DATA_DIR = "data"
NUM_RISK_PATTERNS = 100
NUM_POLICY_DOCS = 50

# MCP Configuration
MCP_ENABLE_MOCK = os.getenv("MCP_ENABLE_MOCK", "true").lower() == "true"
MCP_TIMEOUT = 5

# Logging
LOG_LEVEL = "INFO"
