## task: 
project description (main idea, concepts, design details, dataset concept, system technical details, requirements, and limitations)

# RAG-based Financial Reports Analysis System for Kazakhstani Banks

## Main Idea

This project implements a Retrieval-Augmented Generation (RAG) system to analyze and query financial reports of major Kazakhstani banks. The system allows users to ask natural language questions about bank financial performance, operational metrics, and comparative analysis across institutions.

## Project Overview

### Concept
The system processes quarterly financial reports from three major Kazakhstani banks (Halyk Bank, Kaspi Bank, and ForteBank):
- Vector-based semantic search
- Context-aware answer generation
- Citation of sources
- Comparative financial analysis

## System Architecture

### Components

Streamlit UI (Front-end)
RAG Pipeline + Anthropic Claude (Back-end)
Weaviate Vector Database (Storage)


### Design Details

1. JSON files containing structured financial reports
2. Weaviate vector database with cosine similarity search
3. LangChain-based RAG pipeline with query expansion
4. Streamlit web interface

## 📊 Dataset Concept

### Data Structure

The dataset consists of synthetic but realistic financial reports for Q1-Q4 2024 covering:

**Financial Metrics**:
- Total Assets (billion KZT)
- Loans Portfolio (billion KZT)
- Customer Deposits (billion KZT)
- Net Profit (billion KZT)
- Return on Equity (ROE %)
- Return on Assets (ROA %)
- Capital Adequacy Ratio (%)

**Operational Metrics**:
- Number of branches
- Number of ATMs
- Employee count
- Active clients
- Digital banking users

**Risk & Market Data**:
- Non-performing loans ratio
- Cost-to-income ratio
- Market share
- Year-over-year growth rates

### Data Annotation

Each document is annotated with:
- `bank_name`: Halyk Bank | Kaspi Bank | ForteBank
- `quarter`: Q1 | Q2 | Q3 | Q4
- `year`: 2024
- `report_type`: financial_statement | operational_metrics | market_analysis
- `content`: Full text report with embedded metrics

### Banks Covered

1. Halyk Bank
2. Kaspi Bank
3. ForteBank

## 🔧 System Technical Details

### Vector Database Configuration

- **Database**: Weaviate (via Docker)
- **Collection**: FinancialReports
- **Vector Dimensions**: 1024 (Anthropic embeddings)
- **Distance Metric**: Cosine similarity
- **Index Type**: HNSW (Hierarchical Navigable Small World)

### Embedding Strategy

- **Model**: Anthropic Voyage (via Claude API)
- **Chunking**: By report section (financial/operational/market)
- **Vector Size**: 1024 dimensions
- **Batch Size**: 10 documents per API call

### RAG Pipeline

1. **Query Processing**:
   - User query received
   - Query expanded using Claude LLM
   - Embedded using Anthropic API

2. **Retrieval**:
   - Vector search in Weaviate
   - Top 5 most similar documents retrieved
   - Minimum similarity threshold: 0.7

3. **Generation**:
   - Context assembled from retrieved documents
   - Claude prompted with context + original query
   - Answer generated with citations

### Rate Limiting

- Anthropic API: 50 requests/minute
- Automatic retry with exponential backoff
- Request queuing for batch operations