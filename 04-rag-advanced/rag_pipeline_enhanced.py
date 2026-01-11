"""
Enhanced RAG Pipeline with multiple improvements:
- Iteration 1: Hybrid Search (Vector + BM25)
- Iteration 2: Cross-Encoder Re-ranking
- Iteration 3: Query Decomposition + Metadata Filtering
- Iteration 4: Context Compression
"""
import anthropic
import weaviate
import weaviate.classes as wvc
from typing import List, Dict, Optional, Tuple
import time
import re
from collections import Counter
from config import Config
from embeddings import EmbeddingModel


class EnhancedRAGPipeline:
    """Enhanced Retrieval-Augmented Generation pipeline with advanced techniques."""

    def __init__(self, iteration: int = 4):
        """
        Initialize enhanced RAG pipeline.
        
        Args:
            iteration: Which enhancements to enable (1-4)
                1: Hybrid Search
                2: + Cross-Encoder Re-ranking
                3: + Query Decomposition
                4: + Context Compression
        """
        self.iteration = iteration
        self.config = Config()
        self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        
        print(f"📥 Initializing Enhanced RAG Pipeline (Iteration {iteration})...")
        self.embedding_model = EmbeddingModel()
        print("   ✅ Embedding model loaded")
        
        # Load cross-encoder for iteration 2+
        if iteration >= 2:
            try:
                from sentence_transformers import CrossEncoder
                self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
                print("   ✅ Cross-encoder loaded")
            except Exception as e:
                print(f"   ⚠️  Cross-encoder failed to load: {e}")
                self.cross_encoder = None
        
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

    # ============================================================
    # ITERATION 3: Query Decomposition
    # ============================================================
    
    def decompose_query(self, query: str) -> Tuple[List[str], Dict]:
        """
        Decompose complex queries into simpler sub-queries.
        Extract metadata filters (bank names, quarters, years).
        """
        if self.iteration < 3:
            return [query], {}
        
        # Extract metadata from query
        metadata = self._extract_metadata(query)
        
        # Check if query needs decomposition (comparisons, trends)
        if any(keyword in query.lower() for keyword in ['compare', 'comparison', 'versus', 'vs', 'between']):
            # Comparison query - might need multiple lookups
            sub_queries = self._decompose_comparison(query, metadata)
            return sub_queries, metadata
        
        elif any(keyword in query.lower() for keyword in ['trend', 'change', 'evolve', 'growth', 'over time']):
            # Trend query - needs temporal data
            sub_queries = self._decompose_trend(query, metadata)
            return sub_queries, metadata
        
        else:
            # Simple query - no decomposition needed
            return [query], metadata
    
    def _extract_metadata(self, query: str) -> Dict:
        """Extract bank names, quarters, and years from query."""
        metadata = {
            "banks": [],
            "quarters": [],
            "years": []
        }
        
        # Extract bank names
        query_lower = query.lower()
        for bank in Config.BANKS:
            if bank.lower() in query_lower:
                metadata["banks"].append(bank)
        
        # Extract quarters
        quarter_patterns = [r'\bQ[1-4]\b', r'\b(?:first|second|third|fourth) quarter\b']
        for pattern in quarter_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            for match in matches:
                if match.upper().startswith('Q'):
                    metadata["quarters"].append(match.upper())
                else:
                    quarter_map = {'first': 'Q1', 'second': 'Q2', 'third': 'Q3', 'fourth': 'Q4'}
                    for word, q in quarter_map.items():
                        if word in match.lower():
                            metadata["quarters"].append(q)
        
        # Extract years
        year_matches = re.findall(r'\b(202[0-9])\b', query)
        metadata["years"] = [int(y) for y in year_matches]
        
        return metadata
    
    def _decompose_comparison(self, query: str, metadata: Dict) -> List[str]:
        """Decompose comparison queries into individual lookups."""
        banks = metadata.get("banks", [])
        
        if len(banks) >= 2:
            # Multi-bank comparison
            sub_queries = []
            for bank in banks:
                sub_query = query.replace("compare", f"What is {bank}'s")
                sub_query = re.sub(r'\b(all|three|both)\s+(banks?)\b', bank, sub_query, flags=re.IGNORECASE)
                sub_queries.append(sub_query)
            return sub_queries if len(sub_queries) > 1 else [query]
        
        return [query]
    
    def _decompose_trend(self, query: str, metadata: Dict) -> List[str]:
        """Decompose trend queries to get all temporal data points."""
        # For trends, we want all quarters if not specified
        if not metadata.get("quarters"):
            # Query all quarters
            return [query]  # Single query but will use metadata filtering
        
        return [query]

    # ============================================================
    # ITERATION 1: Hybrid Search (Vector + BM25)
    # ============================================================
    
    def bm25_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """
        Perform BM25 keyword search.
        Returns documents ranked by keyword relevance.
        """
        if self.iteration < 1:
            return []
        
        try:
            # Use Weaviate's BM25 search with score metadata
            results = self.collection.query.bm25(
                query=query,
                limit=top_k,
                return_metadata=wvc.query.MetadataQuery(score=True)
            )
            
            documents = []
            for obj in results.objects:
                doc = {
                    "bank_name": obj.properties.get("bank_name"),
                    "quarter": obj.properties.get("quarter"),
                    "year": obj.properties.get("year"),
                    "report_type": obj.properties.get("report_type"),
                    "content": obj.properties.get("content"),
                    "score": obj.metadata.score if hasattr(obj.metadata, 'score') else 1.0,
                    "source": "bm25"
                }
                documents.append(doc)
            
            return documents
        
        except Exception as e:
            print(f"⚠️  BM25 search failed: {e}")
            return []
    
    def vector_search(self, query: str, top_k: int = 20, metadata_filter: Dict = None) -> List[Dict]:
        """
        Perform vector similarity search with optional metadata filtering.
        """
        query_vector = self.embedding_model.encode(query)
        
        # Build metadata filter if provided
        where_filter = None
        if metadata_filter and self.iteration >= 3:
            where_filter = self._build_where_filter(metadata_filter)
        
        try:
            # Build query with optional filter
            query_builder = self.collection.query.near_vector(
                near_vector=query_vector,
                limit=top_k,
                return_metadata=wvc.query.MetadataQuery(distance=True)
            )
            
            # Apply filter if provided (using separate method for v4 API)
            if where_filter:
                results = self.collection.query.near_vector(
                    near_vector=query_vector,
                    limit=top_k,
                    return_metadata=wvc.query.MetadataQuery(distance=True),
                    filters=where_filter
                )
            else:
                results = query_builder
            
            documents = []
            for obj in results.objects:
                doc = {
                    "bank_name": obj.properties.get("bank_name"),
                    "quarter": obj.properties.get("quarter"),
                    "year": obj.properties.get("year"),
                    "report_type": obj.properties.get("report_type"),
                    "content": obj.properties.get("content"),
                    "distance": obj.metadata.distance,
                    "similarity": 1 - obj.metadata.distance,
                    "source": "vector"
                }
                documents.append(doc)
            
            return documents
        
        except Exception as e:
            print(f"⚠️  Vector search failed: {e}")
            return []
    
    def _build_where_filter(self, metadata: Dict) -> Optional[wvc.query.Filter]:
        """Build Weaviate filter from metadata using v4 API."""
        filters = []
        
        if metadata.get("banks"):
            # For multiple banks, create OR condition
            if len(metadata["banks"]) == 1:
                filters.append(wvc.query.Filter.by_property("bank_name").equal(metadata["banks"][0]))
            else:
                # Chain multiple OR conditions
                bank_filter = wvc.query.Filter.by_property("bank_name").equal(metadata["banks"][0])
                for bank in metadata["banks"][1:]:
                    bank_filter = bank_filter | wvc.query.Filter.by_property("bank_name").equal(bank)
                filters.append(bank_filter)
        
        if metadata.get("quarters"):
            if len(metadata["quarters"]) == 1:
                filters.append(wvc.query.Filter.by_property("quarter").equal(metadata["quarters"][0]))
            else:
                quarter_filter = wvc.query.Filter.by_property("quarter").equal(metadata["quarters"][0])
                for q in metadata["quarters"][1:]:
                    quarter_filter = quarter_filter | wvc.query.Filter.by_property("quarter").equal(q)
                filters.append(quarter_filter)
        
        if metadata.get("years"):
            if len(metadata["years"]) == 1:
                filters.append(wvc.query.Filter.by_property("year").equal(metadata["years"][0]))
            else:
                year_filter = wvc.query.Filter.by_property("year").equal(metadata["years"][0])
                for y in metadata["years"][1:]:
                    year_filter = year_filter | wvc.query.Filter.by_property("year").equal(y)
                filters.append(year_filter)
        
        if not filters:
            return None
        
        if len(filters) == 1:
            return filters[0]
        
        # Chain multiple AND conditions using & operator
        combined_filter = filters[0]
        for f in filters[1:]:
            combined_filter = combined_filter & f
        
        return combined_filter
    
    def hybrid_search(self, query: str, top_k: int = 10, metadata_filter: Dict = None, 
                     alpha: float = 0.5) -> List[Dict]:
        """
        Combine vector and BM25 search results.
        
        Args:
            alpha: Weight for vector search (0=only BM25, 1=only vector, 0.5=balanced)
        """
        if self.iteration < 1:
            # Fall back to vector only
            return self.vector_search(query, top_k, metadata_filter)
        
        # Get results from both methods
        vector_results = self.vector_search(query, top_k=top_k*2, metadata_filter=metadata_filter)
        bm25_results = self.bm25_search(query, top_k=top_k*2)
        
        # Handle empty results
        if not vector_results and not bm25_results:
            return []
        if not vector_results:
            return bm25_results[:top_k]
        if not bm25_results:
            return vector_results[:top_k]
        
        # Normalize scores - handle None and missing values
        if vector_results:
            similarities = [doc.get('similarity', 0) or 0 for doc in vector_results]
            max_sim = max(similarities) if similarities else 1
            for doc in vector_results:
                sim_value = doc.get('similarity', 0) or 0
                doc['normalized_score'] = sim_value / max_sim if max_sim > 0 else 0
        
        if bm25_results:
            scores = [doc.get('score', 0) or 0 for doc in bm25_results]
            max_bm25 = max(scores) if scores else 1
            for doc in bm25_results:
                score_value = doc.get('score', 0) or 0
                doc['normalized_score'] = score_value / max_bm25 if max_bm25 > 0 else 0
        
        # Merge results by content (deduplicate) - handle None values
        merged = {}
        for doc in vector_results:
            # Create key, handling None values
            bank = doc.get('bank_name') or 'unknown'
            quarter = doc.get('quarter') or 'unknown'
            year = doc.get('year') or 0
            report_type = doc.get('report_type') or 'unknown'
            key = f"{bank}_{quarter}_{year}_{report_type}"
            doc['hybrid_score'] = alpha * doc.get('normalized_score', 0)
            merged[key] = doc
        
        for doc in bm25_results:
            # Create key, handling None values
            bank = doc.get('bank_name') or 'unknown'
            quarter = doc.get('quarter') or 'unknown'
            year = doc.get('year') or 0
            report_type = doc.get('report_type') or 'unknown'
            key = f"{bank}_{quarter}_{year}_{report_type}"
            if key in merged:
                merged[key]['hybrid_score'] += (1 - alpha) * doc.get('normalized_score', 0)
                merged[key]['source'] = 'hybrid'
            else:
                doc['hybrid_score'] = (1 - alpha) * doc.get('normalized_score', 0)
                merged[key] = doc
        
        # Sort by hybrid score and return top_k
        results = sorted(merged.values(), key=lambda x: x['hybrid_score'], reverse=True)
        return results[:top_k]

    # ============================================================
    # ITERATION 2: Cross-Encoder Re-ranking
    # ============================================================
    
    def rerank_documents(self, query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Re-rank documents using cross-encoder for better precision.
        """
        if self.iteration < 2 or not self.cross_encoder or not documents:
            return documents[:top_k]
        
        try:
            # Prepare query-document pairs
            pairs = [[query, doc['content'][:512]] for doc in documents]  # Limit content length
            
            # Get cross-encoder scores
            scores = self.cross_encoder.predict(pairs)
            
            # Add scores to documents
            for doc, score in zip(documents, scores):
                doc['rerank_score'] = float(score)
            
            # Sort by rerank score
            reranked = sorted(documents, key=lambda x: x['rerank_score'], reverse=True)
            
            return reranked[:top_k]
        
        except Exception as e:
            print(f"⚠️  Re-ranking failed: {e}")
            return documents[:top_k]

    # ============================================================
    # ITERATION 4: Context Compression
    # ============================================================
    
    def compress_context(self, query: str, documents: List[Dict]) -> List[Dict]:
        """
        Remove irrelevant parts from retrieved documents to improve precision.
        Uses LLM to extract only relevant information.
        """
        if self.iteration < 4 or not documents:
            return documents
        
        compressed_docs = []
        
        for doc in documents:
            try:
                compression_prompt = f"""Extract only the information relevant to this query from the document below.

Query: {query}

Document Content:
{doc['content'][:1500]}

Instructions:
1. Extract only facts and figures directly relevant to the query
2. Keep specific numbers, percentages, and metrics mentioned
3. Remove introductory text, disclaimers, and unrelated information
4. Keep the response concise (max 300 words)
5. If nothing is relevant, return "NO_RELEVANT_INFO"

Relevant Information:"""

                message = self.anthropic_client.messages.create(
                    model=Config.CHAT_MODEL,
                    max_tokens=400,
                    temperature=0,
                    messages=[{"role": "user", "content": compression_prompt}]
                )
                
                compressed_content = message.content[0].text.strip()
                
                if compressed_content != "NO_RELEVANT_INFO" and len(compressed_content) > 20:
                    doc_copy = doc.copy()
                    doc_copy['original_content'] = doc['content']
                    doc_copy['content'] = compressed_content
                    doc_copy['compressed'] = True
                    compressed_docs.append(doc_copy)
                else:
                    # Keep original if compression failed or found nothing relevant
                    doc['compressed'] = False
                    compressed_docs.append(doc)
            
            except Exception as e:
                print(f"⚠️  Compression failed for document: {e}")
                doc['compressed'] = False
                compressed_docs.append(doc)
        
        return compressed_docs

    # ============================================================
    # Query Expansion (from base pipeline)
    # ============================================================
    
    def expand_query(self, query: str) -> str:
        """Expand query with financial terminology."""
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
            print(f"⚠️  Query expansion failed: {e}")
            return query

    # ============================================================
    # Answer Generation
    # ============================================================
    
    def generate_answer(self, query: str, documents: List[Dict]) -> Dict:
        """Generate answer from retrieved documents."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"Document {i} ({doc['bank_name']} - {doc['quarter']} {doc['year']} - {doc['report_type']}):\n"
                f"{doc['content']}\n"
            )
        
        context = "\n---\n".join(context_parts)
        
        generation_prompt = f"""You are a financial analyst assistant. Your task is to answer questions about bank financial reports based ONLY on the provided context.

Context (Retrieved Financial Reports):
{context}

User Question: {query}

Instructions:
1. Answer the question using ONLY information from the provided documents
2. If specific numbers or metrics are asked, provide exact values with units (billion KZT, %, etc.)
3. When comparing banks, present data in a clear, structured format
4. Include the source (bank name, quarter, report type) for each piece of information
5. If the information is not in the provided documents, say "The provided documents do not contain this information"
6. Format numbers clearly with appropriate separators and units
7. Be concise but comprehensive

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

    # ============================================================
    # Main Query Method
    # ============================================================
    
    def query(self, user_query: str, expand_query: bool = True, top_k: int = 5) -> Dict:
        """
        Execute enhanced RAG query pipeline.
        
        Args:
            user_query: User's question
            expand_query: Whether to expand the query
            top_k: Number of final documents to use
        """
        start_time = time.time()
        
        # Step 1: Query expansion
        if expand_query:
            expanded_query = self.expand_query(user_query)
            search_query = expanded_query
        else:
            expanded_query = user_query
            search_query = user_query
        
        # Step 2: Query decomposition + metadata extraction (Iteration 3+)
        sub_queries, metadata = self.decompose_query(search_query)
        
        # Step 3: Hybrid search (Iteration 1+) or vector search
        all_documents = []
        for sub_query in sub_queries:
            if self.iteration >= 1:
                docs = self.hybrid_search(sub_query, top_k=top_k*2, metadata_filter=metadata)
            else:
                docs = self.vector_search(sub_query, top_k=top_k*2, metadata_filter=metadata)
            all_documents.extend(docs)
        
        # Deduplicate documents - handle None values
        seen = set()
        unique_docs = []
        for doc in all_documents:
            bank = doc.get('bank_name') or 'unknown'
            quarter = doc.get('quarter') or 'unknown'
            year = doc.get('year') or 0
            report_type = doc.get('report_type') or 'unknown'
            key = f"{bank}_{quarter}_{year}_{report_type}"
            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)
        
        # Step 4: Re-ranking (Iteration 2+)
        if self.iteration >= 2:
            reranked_docs = self.rerank_documents(search_query, unique_docs, top_k=top_k*2)
        else:
            reranked_docs = unique_docs[:top_k*2]
        
        # Step 5: Context compression (Iteration 4)
        if self.iteration >= 4:
            final_docs = self.compress_context(search_query, reranked_docs[:top_k])
        else:
            final_docs = reranked_docs[:top_k]
        
        # Step 6: Answer generation
        result = self.generate_answer(user_query, final_docs)
        
        # Add metadata
        result.update({
            "original_query": user_query,
            "expanded_query": expanded_query,
            "sub_queries": sub_queries,
            "metadata_filters": metadata,
            "num_sources": len(final_docs),
            "processing_time": time.time() - start_time,
            "iteration": self.iteration
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
    print("🔍 Testing Enhanced RAG Pipeline...\n")
    
    test_queries = [
        "What was Kaspi Bank's net profit in Q3 2024?",
        "Compare the ROE of all three banks in Q4 2024",
        "How did Halyk Bank's total assets change throughout 2024?"
    ]
    
    for iteration in [1, 2, 3, 4]:
        print(f"\n{'='*70}")
        print(f"ITERATION {iteration} TEST")
        print(f"{'='*70}\n")
        
        with EnhancedRAGPipeline(iteration=iteration) as rag:
            query = test_queries[0]
            print(f"Query: {query}\n")
            
            result = rag.query(query, top_k=3)
            
            print(f"Answer: {result['answer'][:200]}...")
            print(f"\nSources: {result['num_sources']} documents")
            print(f"Processing time: {result['processing_time']:.2f}s")
