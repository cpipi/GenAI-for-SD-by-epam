"""
Streamlit UI for RAG Financial Reports Analysis System.
"""
import streamlit as st
import pandas as pd
from rag_pipeline import RAGPipeline
from config import Config
import time


# Page configuration
st.set_page_config(
    page_title="RAG Financial Reports Analyzer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6 !important;   /* Soft gray background */
        color: #222 !important;                 /* Dark font color */
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-size: 1.15rem;
        font-weight: 400;
    }
    .source-doc {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
        color: #222 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_rag_pipeline():
    """Initialize and cache RAG pipeline."""
    return RAGPipeline()


def format_metadata(doc):
    """Format document metadata for display."""
    return f"{doc['bank_name']} | {doc['quarter']} {doc['year']} | {doc['report_type'].replace('_', ' ').title()}"


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 RAG Financial Reports Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; font-size: 1.1rem; color: #666;">
        Analyze financial reports of Kazakhstani banks using AI-powered Retrieval-Augmented Generation
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("Search Settings")
        top_k = st.slider(
            "Number of documents to retrieve",
            min_value=1,
            max_value=10,
            value=Config.TOP_K_RESULTS,
            help="How many relevant documents to retrieve from the database"
        )
        
        expand_query = st.checkbox(
            "Expand query",
            value=True,
            help="Use LLM to expand and clarify your question for better retrieval"
        )
        
        st.divider()
        
        st.subheader("📊 About the Data")
        st.info("""
        **Banks**: Halyk Bank, Kaspi Bank, ForteBank
        
        **Period**: Q1-Q4 2024
        
        **Report Types**:
        - Financial Statements
        - Operational Metrics  
        - Market Analysis
        """)
        
        st.divider()
        
        st.subheader("💡 Example Questions")
        example_queries = [
            "What was Kaspi Bank's net profit in Q3 2024?",
            "Compare total assets of all banks in Q4 2024",
            "How many branches does Halyk Bank operate? ",
            "What is ForteBank's capital adequacy ratio? ",
            "Which bank has the highest ROE? ",
            "Show me digital banking statistics for all banks"
        ]
        
        for i, example in enumerate(example_queries):
            if st.button(example, key=f"example_{i}"):
                st.session_state.query_input = example
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Query input
        query = st.text_input(
            "🔍 Ask a question about the financial reports:",
            value=st.session_state.get('query_input', ''),
            placeholder="e.g., What was Kaspi Bank's ROE in Q2 2024? ",
            key="query_field"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        search_button = st.button("🚀 Search", type="primary", use_container_width=True)
    
    # Process query
    if search_button and query:
        try:
            # Initialize RAG pipeline
            with st.spinner("🔄 Initializing RAG pipeline..."):
                rag = get_rag_pipeline()
            
            # Execute query
            with st.spinner("🔍 Searching financial reports..."):
                result = rag.query(
                    user_query=query,
                    expand_query=expand_query,
                    top_k=top_k
                )
            
            # Display results
            st.success(f"✅ Found {result['num_sources']} relevant documents in {result['processing_time']:.2f}s")
            
            # Show expanded query if enabled
            if expand_query and result['expanded_query'] != result['original_query']:
                with st.expander("🔄 Expanded Query", expanded=False):
                    st.info(result['expanded_query'])
            
            # Answer section
            st.markdown("---")
            st.subheader("💬 Answer")
            st.markdown(f"""
            <div class="metric-card">
                {result['answer']}
            </div>
            """, unsafe_allow_html=True)
            
            # Sources section
            st.markdown("---")
            st.subheader("📚 Source Documents")
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📄 Document View", "📊 Table View"])
            
            with tab1:
                for i, doc in enumerate(result['sources'], 1):
                    similarity_pct = doc['similarity'] * 100
                    
                    with st.expander(
                        f"Document {i}: {format_metadata(doc)} (Similarity: {similarity_pct:.1f}%)",
                        expanded=(i == 1)
                    ):
                        # Metadata
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Bank", doc['bank_name'])
                        with col_b:
                            st.metric("Period", f"{doc['quarter']} {doc['year']}")
                        with col_c:
                            st.metric("Similarity", f"{similarity_pct:.1f}%")
                        
                        # Content
                        st.markdown("**Content:**")
                        st.text(doc['content'][:1000] + ("..." if len(doc['content']) > 1000 else ""))
            
            with tab2:
                # Create summary table
                df = pd.DataFrame([
                    {
                        "Rank": i,
                        "Bank": doc['bank_name'],
                        "Period": f"{doc['quarter']} {doc['year']}",
                        "Report Type": doc['report_type'].replace('_', ' ').title(),
                        "Similarity": f"{doc['similarity']*100:.1f}%"
                    }
                    for i, doc in enumerate(result['sources'], 1)
                ])
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Metadata section
            with st.expander("ℹ️ Query Metadata"):
                meta_col1, meta_col2 = st.columns(2)
                with meta_col1:
                    st.write(f"**Model**: {result['model']}")
                    st.write(f"**Documents Retrieved**: {result['num_sources']}")
                with meta_col2:
                    st.write(f"**Processing Time**: {result['processing_time']:.2f}s")
                    st.write(f"**Context Length**: {result['context_length']} characters")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)
    
    elif search_button and not query:
        st.warning("⚠️ Please enter a question first")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; color: #888; font-size: 0.9rem;">
        RAG Financial Reports Analyzer | Powered by Anthropic Claude & Weaviate | 
        <a href="https://github.com" target="_blank">View on GitHub</a>
    </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()