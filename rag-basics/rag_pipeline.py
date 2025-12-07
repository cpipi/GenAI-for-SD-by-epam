"""
RAG Pipeline implementation for financial reports analysis.
Handles query expansion, retrieval, and answer generation.
"""
import anthropic
import weaviate
import weaviate.classes as wvc
from typing import List, Dict
import time
from config import Config
from embeddings import EmbeddingModel


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(self):
        self.config = Config()
        self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        
        # Load the same embedding model used during ingestion
        print("📥 Loading embedding model...")
        self.embedding_model = EmbeddingModel()
        print("   ✅ Model loaded")
        
        self.weaviate_client = None
        self.collection = None
        self.connect()

    def connect(self):
        try:
            self.weaviate_client = weaviate.connect_to_local(
                host="localhost",
                port=8080,
                grpc_port=50051
            )
            self.collection = self.weaviate_client.collections.get(Config.COLLECTION_NAME)
            print("✅ Connected to Weaviate")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Weaviate: {e}")

    def expand_query(self, query: str) -> str:
        expansion_prompt = f"""You are an expert in financial analysis and information retrieval.
                    The user asked: "{query}"
                    Please rephrase this question to be more detailed and specific, suitable for searching a database of financial reports.
                    Include relevant financial terminology and clarify what specific metrics or information the user is seeking.
                    Return only the rephrased query, without any additional explanation."""
        try:
            message = self.anthropic_client.messages.create(
                model=Config.CHAT_MODEL,
                max_tokens=200,
                temperature=0.3,
                messages=[{"role": "user", "content": expansion_prompt}]
            )
            expanded = message.content[0].text.strip()
            return expanded
        except Exception as e:
            print(f"Warning: Query expansion failed ({e}), using original query")
            return query

    def create_query_embedding(self, text: str) -> List[float]:
        """
        Create embedding for query text using local Sentence Transformer model.
        MUST match the embedding model used during data ingestion.
        """
        try:
            embedding = self.embedding_model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True  # Normalize for cosine similarity
            )
            return embedding.tolist()
        except Exception as e:
            print(f"❌ Embedding error for query: {e}")
            emb_dim = 384  # all-MiniLM-L6-v2 dimension
            return [0.0] * emb_dim

    def retrieve_documents(self, query_vector: List[float], top_k: int = None) -> List[Dict]:
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        results = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=top_k,
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )
        documents = []
        for obj in results.objects:
            doc = {
                "bank_name": obj.properties.get("bank_name"),
                "quarter": obj.properties.get("quarter"),
                "year": obj.properties.get("year"),
                "report_type": obj.properties.get("report_type"),
                "content": obj.properties.get("content"),
                "distance": obj.metadata.distance,
                "similarity": 1 - obj.metadata.distance
            }
            documents.append(doc)
        return documents

    def generate_answer(self, query: str, documents: List[Dict]) -> Dict:
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"Document {i} ({doc['bank_name']} - {doc['quarter']} {doc['year']} - {doc['report_type']}):\n"
                f"{doc['content']}\n"
            )
        context = "\n---\n".join(context_parts)
        generation_prompt = f"""You are a financial analyst assistant.Your task is to answer questions about bank financial reports based ONLY on the provided context.
            Context (Retrieved Financial Reports):
            {context}
            User Question: {query}
            Instructions:
            1.Answer the question using ONLY information from the provided documents
            2.If specific numbers or metrics are asked, provide exact values with units (billion KZT, %, etc.)
            3.When comparing banks, present data in a clear, structured format
            4.Include the source (bank name, quarter, report type) for each piece of information
            5.If the information is not in the provided documents, say "The provided documents do not contain this information"
            6.Format numbers clearly with appropriate separators and units
            7.Be concise but comprehensive
            Answer:"""
        try:
            message = self.anthropic_client.messages.create(
                model=Config.CHAT_MODEL,
                max_tokens=1500,
                temperature=0.1,
                messages=[{"role": "user", "content": generation_prompt}]
            )
            answer = message.content[0].text.strip()
            return {
                "answer": answer,
                "sources": documents,
                "context_length": len(context),
                "model": Config.CHAT_MODEL
            }
        except Exception as e:
            return {
                "answer": f"Error generating answer: {e}",
                "sources": documents,
                "context_length": len(context),
                "model": Config.CHAT_MODEL
            }

    def query(self, user_query: str, expand_query: bool = True, top_k: int = None) -> Dict:
        start_time = time.time()
        if expand_query:
            expanded_query = self.expand_query(user_query)
            search_query = expanded_query
        else:
            expanded_query = user_query
            search_query = user_query
        query_vector = self.embedding_model.encode(search_query)
        documents = self.retrieve_documents(query_vector, top_k)
        result = self.generate_answer(user_query, documents)
        result.update({
            "original_query": user_query,
            "expanded_query": expanded_query,
            "num_sources": len(documents),
            "processing_time": time.time() - start_time
        })
        return result

    def close(self):
        if self.weaviate_client:
            self.weaviate_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    print("🔍 Testing RAG Pipeline...\n")
    with RAGPipeline() as rag:
        test_queries = [
            "What was Kaspi Bank's net profit in Q3 2024? ",
            "Compare the total assets of all three banks in Q4 2024",
            "How many branches does Halyk Bank operate?"
        ]
        for query in test_queries:
            print(f"\n{'='*70}")
            print(f"Query: {query}")
            print('='*70)
            result = rag.query(query)
            print(f"\nExpanded Query: {result['expanded_query']}")
            print(f"\nAnswer:\n{result['answer']}")
            print(f"\nSources: {result['num_sources']} documents")
            print(f"Processing time: {result['processing_time']:.2f}s")