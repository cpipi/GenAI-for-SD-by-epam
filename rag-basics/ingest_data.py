"""
Data ingestion pipeline for RAG Financial Reports system.
Loads financial reports, creates embeddings, and stores in Weaviate.
"""
import json
import os
import time
from pathlib import Path
from typing import List, Dict
import anthropic
import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
from tqdm import tqdm
from config import Config


class DataIngestion:
    """Handle data loading, embedding, and ingestion to Weaviate."""
    
    def __init__(self):
        """Initialize clients and configuration."""
        self.config = Config()
        self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.weaviate_client = None
        self.collection = None
        
    def connect_to_weaviate(self):
        """Connect to Weaviate instance."""
        print("🔗 Connecting to Weaviate...")
        try:
            self.weaviate_client = weaviate.connect_to_local(
                host="localhost",
                port=8080,
                grpc_port=50051
            )
            
            if not self.weaviate_client.is_ready():
                raise ConnectionError("Weaviate is not ready")
            
            print("   ✅ Connected to Weaviate")
        except Exception as e:
            print(f"   ❌ Failed to connect to Weaviate: {e}")
            print("   💡 Make sure Docker is running: docker-compose up -d")
            raise
    
    def create_schema(self):
        """Create or recreate Weaviate collection schema."""
        print(f"\n📋 Setting up collection: {Config.COLLECTION_NAME}...")
        
        # Delete existing collection if it exists
        if self.weaviate_client.collections.exists(Config.COLLECTION_NAME):
            self.weaviate_client.collections.delete(Config.COLLECTION_NAME)
            print("   🗑️  Deleted existing collection")
        
        # Create new collection
        self.collection = self.weaviate_client.collections.create(
            name=Config.COLLECTION_NAME,
            properties=[
                wvc.config.Property(
                    name="bank_name",
                    data_type=wvc.config.DataType.TEXT,
                    description="Name of the bank"
                ),
                wvc.config.Property(
                    name="quarter",
                    data_type=wvc.config.DataType.TEXT,
                    description="Quarter (Q1, Q2, Q3, Q4)"
                ),
                wvc.config.Property(
                    name="year",
                    data_type=wvc.config.DataType.INT,
                    description="Year of the report"
                ),
                wvc.config.Property(
                    name="report_type",
                    data_type=wvc.config.DataType.TEXT,
                    description="Type of report (financial_statement, operational_metrics, market_analysis)"
                ),
                wvc.config.Property(
                    name="content",
                    data_type=wvc.config.DataType.TEXT,
                    description="Full text content of the report"
                ),
            ],
            # Configure vector index
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            vector_index_config=wvc.config.Configure.VectorIndex.hnsw(
                distance_metric=wvc.config.VectorDistances.COSINE
            )
        )
        print("   ✅ Collection created successfully")
    
    def load_financial_data(self) -> List[Dict]:
        """Load all financial reports from JSON files."""
        print("\n📂 Loading financial data...")
        all_reports = []
        
        data_dir = Path(Config.DATA_DIR)
        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {Config.DATA_DIR}")
        
        json_files = list(data_dir.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in {Config.DATA_DIR}")
        
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                reports = json.load(f)
                all_reports.extend(reports)
                print(f"   📄 Loaded {len(reports)} reports from {json_file.name}")
        
        print(f"   ✅ Total reports loaded: {len(all_reports)}")
        return all_reports
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings using Anthropic API.
        Note: We'll use Claude's built-in message handling for embeddings simulation.
        In production, you'd use a dedicated embedding model.
        """
        print(f"\n🔢 Creating embeddings for {len(texts)} documents...")
        embeddings = []
        
        # For this demo, we'll create simple embeddings
        # In production, use proper embedding models
        for text in tqdm(texts, desc="Generating embeddings"):
            # Simple hash-based embedding for demonstration
            # Replace with actual embedding API call
            embedding = self._simple_embedding(text)
            embeddings.append(embedding)
            time.sleep(0.1)  # Rate limiting
        
        print(f"   ✅ Created {len(embeddings)} embeddings")
        return embeddings
    
    def _simple_embedding(self, text: str, dim: int = 1024) -> List[float]:
        """
        Create a simple deterministic embedding from text.
        This is for demonstration only - replace with real embeddings.
        """
        import hashlib
        import struct
        
        # Create hash of text
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to float vector
        embedding = []
        for i in range(0, min(len(hash_bytes), dim // 8), 4):
            value = struct.unpack('f', hash_bytes[i:i+4])[0] if i+4 <= len(hash_bytes) else 0.0
            embedding.append(float(value))
        
        # Pad to correct dimension
        while len(embedding) < dim:
            embedding.append(0.0)
        
        # Normalize
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding[:dim]
    
    def ingest_documents(self, reports: List[Dict]):
        """Ingest documents with embeddings into Weaviate."""
        print(f"\n⬆️  Ingesting {len(reports)} documents into Weaviate...")
        
        # Get collection
        collection = self.weaviate_client.collections.get(Config.COLLECTION_NAME)
        
        # Create embeddings for all content
        contents = [report['content'] for report in reports]
        embeddings = self.create_embeddings(contents)
        
        # Batch insert with progress bar
        with collection.batch.dynamic() as batch:
            for report, embedding in tqdm(
                zip(reports, embeddings),
                total=len(reports),
                desc="Uploading to Weaviate"
            ):
                properties = {
                    "bank_name": report["bank_name"],
                    "quarter": report["quarter"],
                    "year": report["year"],
                    "report_type": report["report_type"],
                    "content": report["content"]
                }
                
                # Generate unique UUID based on content
                uuid = generate_uuid5(
                    f"{report['bank_name']}_{report['quarter']}_{report['year']}_{report['report_type']}"
                )
                
                batch.add_object(
                    properties=properties,
                    vector=embedding,
                    uuid=uuid
                )
        
        # Verify ingestion
        total_objects = len(collection)
        print(f"   ✅ Successfully ingested {total_objects} documents")
    
    def run(self):
        """Run the complete ingestion pipeline."""
        try:
            # Step 1: Connect to Weaviate
            self.connect_to_weaviate()
            
            # Step 2: Create schema
            self.create_schema()
            
            # Step 3: Load data
            reports = self.load_financial_data()
            
            # Step 4: Ingest documents
            self.ingest_documents(reports)
            
            print("\n✨ Data ingestion completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during ingestion: {e}")
            raise
        finally:
            if self.weaviate_client:
                self.weaviate_client.close()
                print("🔌 Disconnected from Weaviate")


def main():
    """Main entry point."""
    print("=" * 70)
    print("  RAG Financial Reports - Data Ingestion Pipeline")
    print("=" * 70)
    
    ingestion = DataIngestion()
    ingestion.run()


if __name__ == "__main__":
    main()