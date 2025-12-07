"""
Configuration management for the RAG Financial Reports system.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Weaviate Configuration
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_GRPC_URL = os.getenv("WEAVIATE_GRPC_URL", "localhost:50051")
    
    # Model Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "claude-haiku-4-5")
    CHAT_MODEL = os.getenv("CHAT_MODEL", "claude-haiku-4-5")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # Weaviate Collection
    COLLECTION_NAME = "FinancialReports"
    
    # Data Paths
    DATA_DIR = "data"
    
    # Bank Names
    BANKS = ["Halyk Bank", "Kaspi Bank", "ForteBank"]
    
    # Quarters
    QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
    
    # Report Types
    REPORT_TYPES = [
        "financial_statement",
        "operational_metrics",
        "market_analysis"
    ]
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required.  Please set it in .env file")
        return True


# Validate configuration on import
Config.validate()