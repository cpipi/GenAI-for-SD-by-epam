"""
RAG Pipeline implementation for financial reports analysis.
Handles query expansion, retrieval, and answer generation.
"""
import anthropic
import weaviate
import weaviate.classes as wvc
from typing import List, Dict, Tuple
import time
from config import Config


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""
    
    def __init__(self):
        """Initialize RAG pipeline components."""
        self.config = Config()
        self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.weaviate_client = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Connect to Weaviate."""
        try:
            self.weaviate_client = weaviate.connect_to_local(
                host="localhost",
                port=8080,
                grpc_port=50051
            )
            self.collection = self.weaviate_client.collections.get(Config.COLLECTION_NAME)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Weaviate: {e}")
    
    def expand_query(self, query: str) -> str:
        """
        Expand user query to be more descriptive for better retrieval.
        Args:
            query: Original user question
        Returns:
            Expanded, more detailed query
        """
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
                messages=[
                    {"role": "user", "content": expansion_prompt}
                ]
            )
            expanded = message.content[0].text.strip()
            return expanded
        except Exception as e:
            print(f"Warning: Query expansion failed ({e}), using original query")
            return query
    
    def create_query_embedding(self, text: str) -> List[float]:
        """
        Create embedding for query text.
        Uses same method as ingestion for consistency.
        """
        import hashlib
        import struct
        
        dim = 1024
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        embedding = []
        for i in range(0, min(len(hash_bytes), dim // 8), 4):
            value = struct.unpack('f', hash_bytes[i:i+4])[0] if i+4 <= len(hash_bytes) else 0.0
            embedding.append(float(value))
        
        while len(embedding) < dim:
            embedding.append(0.0)
        
        magnitude = sum(x**2 for x in embedding) ** 0.5
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding[:dim]
    
    def retrieve_documents(
        self,
        query_vector: List[float],
        top_k: int = None
    ) -> List[Dict]:
        """
        Retrieve most relevant documents from Weaviate.
        Args:
            query_vector: Embedding vector of the query
            top_k: Number of documents to retrieve
        Returns:
            List of retrieved documents with metadata
        """
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # Perform vector search
        results = self.collection.query.near_vector(
            near_vector=query_vector,
            limit=top_k,
            return_metadata=wvc.query.MetadataQuery(distance=True)
        )
        
        # Format results
        documents = []
        for obj in results.objects:
            doc = {
                "bank_name": obj.properties.get("bank_name"),
                "quarter": obj.properties.get("quarter"),
                "year": obj.properties.get("year"),
                "report_type": obj.properties.get("report_type"),
                "content": obj.properties.get("content"),
                "distance": obj.metadata.distance,
                "similarity": 1 - obj.metadata.distance  # Convert distance to similarity
            }
            documents.append(doc)
        
        return documents
    
    def generate_answer(self, query: str, documents: List[Dict]) -> Dict:
        """
        Generate answer using retrieved documents as context.
        Args:
            query: Original user question
            documents: Retrieved relevant documents
        Returns:
            Dictionary with answer and metadata
        """
        # Build context from retrieved documents
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"Document {i} ({doc['bank_name']} - {doc['quarter']} {doc['year']} - {doc['report_type']}):\n"
                f"{doc['content']}\n"
            )
        
        context = "\n---\n".join(context_parts)
        
        # Create prompt for answer generation
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
                messages=[
                    {"role": "user", "content": generation_prompt}
                ]
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
    
    def query(
        self,
        user_query: str,
        expand_query: bool = True,
        top_k: int = None
    ) -> Dict:
        """
        Complete RAG pipeline: expand query, retrieve, generate answer.
        Args:
            user_query: User's original question
            expand_query: Whether to expand the query
            top_k: Number of documents to retrieve
        Returns:
            Dictionary with answer, sources, and metadata
        """
        start_time = time.time()
        
        # Step 1: Optionally expand query
        if expand_query:
            expanded_query = self.expand_query(user_query)
            search_query = expanded_query
        else:
            expanded_query = user_query
            search_query = user_query
        
        # Step 2: Create embedding for search
        query_vector = self.create_query_embedding(search_query)
        
        # Step 3: Retrieve relevant documents
        documents = self.retrieve_documents(query_vector, top_k)
        
        # Step 4: Generate answer
        result = self.generate_answer(user_query, documents)
        
        # Add metadata
        result.update({
            "original_query": user_query,
            "expanded_query": expanded_query,
            "num_sources": len(documents),
            "processing_time": time.time() - start_time
        })
        return result
    
    def close(self):
        """Close connections."""
        if self.weaviate_client:
            self.weaviate_client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    print("🔍 Testing RAG Pipeline...\n")
    
    with RAGPipeline() as rag:
        test_queries = [
            "What was Kaspi Bank's net profit in Q3 2024?",
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