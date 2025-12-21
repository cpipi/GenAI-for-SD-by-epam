"""
Automated evaluation pipeline for RAG system.
Measures Answer Relevancy and Context Precision using LLM-as-judge.
"""
import anthropic
import json
import time
from typing import List, Dict, Tuple
from config import Config
from test_dataset import TestDataset


class RAGEvaluator:
    """Automated evaluation system for RAG pipeline."""
    
    def __init__(self):
        self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.test_queries = TestDataset.get_test_queries()
    
    def evaluate_answer_relevancy(self, query: str, answer: str, expected_answer: str) -> Dict:
        """
        Evaluate if the answer is relevant to the query.
        Uses LLM-as-judge to score on scale 0-100.
        """
        prompt = f"""You are an expert financial analyst evaluating the quality of AI-generated answers.

QUERY: {query}

EXPECTED ANSWER: {expected_answer}

ACTUAL ANSWER: {answer}

Evaluate the ACTUAL ANSWER on the following criteria:
1. **Accuracy**: Does it provide correct information? (0-40 points)
2. **Completeness**: Does it fully answer the question? (0-30 points)
3. **Relevance**: Is it focused on what was asked? (0-30 points)

Provide your evaluation in this exact JSON format:
{{
  "accuracy_score": <0-40>,
  "completeness_score": <0-30>,
  "relevance_score": <0-30>,
  "total_score": <0-100>,
  "reasoning": "<brief explanation>"
}}

Be strict but fair. Consider:
- For fact lookups: exact numbers matter
- For comparisons: all requested entities should be compared
- For trends: temporal changes should be described
"""
        
        try:
            message = self.anthropic_client.messages.create(
                model=Config.CHAT_MODEL,
                max_tokens=1024,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            result = json.loads(json_str)
            return {
                "accuracy": result["accuracy_score"],
                "completeness": result["completeness_score"],
                "relevance": result["relevance_score"],
                "total": result["total_score"],
                "reasoning": result["reasoning"]
            }
        
        except Exception as e:
            print(f"⚠️  Error in answer relevancy evaluation: {e}")
            return {
                "accuracy": 0,
                "completeness": 0,
                "relevance": 0,
                "total": 0,
                "reasoning": f"Evaluation failed: {str(e)}"
            }
    
    def evaluate_context_precision(self, query: str, sources: List[Dict], 
                                   expected_banks: List[str], 
                                   expected_quarters: List[str],
                                   expected_years: List[int]) -> Dict:
        """
        Evaluate the precision of retrieved context.
        Measures if retrieved documents are relevant to the query.
        """
        if not sources:
            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1": 0.0,
                "relevant_docs": 0,
                "total_docs": 0,
                "reasoning": "No sources retrieved"
            }
        
        # Check metadata match
        relevant_count = 0
        for doc in sources:
            bank_match = doc.get('bank_name') in expected_banks
            quarter_match = doc.get('quarter') in expected_quarters
            year_match = doc.get('year') in expected_years
            
            # A document is relevant if it matches the expected criteria
            if bank_match and quarter_match and year_match:
                relevant_count += 1
        
        total_docs = len(sources)
        precision = relevant_count / total_docs if total_docs > 0 else 0
        
        # Recall: how many of the expected documents were retrieved
        # For simplicity, we estimate based on number of expected banks/quarters
        expected_docs = len(expected_banks) * len(expected_quarters)
        recall = relevant_count / expected_docs if expected_docs > 0 else 0
        
        # F1 score
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "precision": precision,
            "recall": min(recall, 1.0),  # Cap at 1.0
            "f1": f1,
            "relevant_docs": relevant_count,
            "total_docs": total_docs,
            "reasoning": f"{relevant_count}/{total_docs} documents matched expected criteria"
        }
    
    def evaluate_single_query(self, rag_pipeline, test_query: Dict) -> Dict:
        """Evaluate RAG pipeline on a single test query."""
        query = test_query["query"]
        
        print(f"\n🔍 Evaluating: {query}")
        
        # Get RAG result
        start_time = time.time()
        try:
            result = rag_pipeline.query(
                user_query=query,
                expand_query=True,
                top_k=5
            )
            processing_time = time.time() - start_time
        except Exception as e:
            print(f"   ❌ Query failed: {e}")
            return {
                "query_id": test_query["id"],
                "query": query,
                "success": False,
                "error": str(e),
                "processing_time": 0
            }
        
        # Evaluate answer relevancy
        answer_eval = self.evaluate_answer_relevancy(
            query=query,
            answer=result["answer"],
            expected_answer=test_query["expected_answer"]
        )
        
        # Evaluate context precision
        context_eval = self.evaluate_context_precision(
            query=query,
            sources=result["sources"],
            expected_banks=test_query["expected_banks"],
            expected_quarters=test_query["expected_quarters"],
            expected_years=test_query["expected_years"]
        )
        
        print(f"   📊 Answer Relevancy: {answer_eval['total']}/100")
        print(f"   📊 Context Precision: {context_eval['precision']:.2%}")
        print(f"   ⏱️  Time: {processing_time:.2f}s")
        
        return {
            "query_id": test_query["id"],
            "query": query,
            "query_type": test_query["type"],
            "complexity": test_query["complexity"],
            "success": True,
            "processing_time": processing_time,
            "answer_relevancy": answer_eval,
            "context_precision": context_eval,
            "num_sources": len(result["sources"]),
            "answer": result["answer"],
            "expected_answer": test_query["expected_answer"]
        }
    
    def evaluate_pipeline(self, rag_pipeline, sample_size: int = None) -> Dict:
        """
        Evaluate RAG pipeline on test dataset.
        
        Args:
            rag_pipeline: RAG pipeline instance to evaluate
            sample_size: Number of queries to test (None = all queries)
        """
        queries_to_test = self.test_queries
        if sample_size:
            queries_to_test = self.test_queries[:sample_size]
        
        print(f"\n{'='*60}")
        print(f"🧪 Starting RAG Evaluation")
        print(f"{'='*60}")
        print(f"Total queries: {len(queries_to_test)}")
        
        results = []
        for i, test_query in enumerate(queries_to_test, 1):
            print(f"\n[{i}/{len(queries_to_test)}]", end=" ")
            result = self.evaluate_single_query(rag_pipeline, test_query)
            results.append(result)
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        # Calculate aggregate metrics
        metrics = self._calculate_aggregate_metrics(results)
        
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_queries": len(results),
            "successful_queries": sum(1 for r in results if r["success"]),
            "failed_queries": sum(1 for r in results if not r["success"]),
            "metrics": metrics,
            "results": results
        }
    
    def _calculate_aggregate_metrics(self, results: List[Dict]) -> Dict:
        """Calculate aggregate metrics from individual results."""
        successful_results = [r for r in results if r["success"]]
        
        if not successful_results:
            return {
                "answer_relevancy": {"mean": 0, "median": 0, "min": 0, "max": 0},
                "context_precision": {"mean": 0, "median": 0, "min": 0, "max": 0},
                "processing_time": {"mean": 0, "median": 0, "min": 0, "max": 0}
            }
        
        # Answer relevancy scores
        relevancy_scores = [r["answer_relevancy"]["total"] for r in successful_results]
        
        # Context precision scores
        precision_scores = [r["context_precision"]["precision"] for r in successful_results]
        
        # Processing times
        times = [r["processing_time"] for r in successful_results]
        
        # By query type
        by_type = {}
        for result in successful_results:
            qtype = result["query_type"]
            if qtype not in by_type:
                by_type[qtype] = {
                    "count": 0,
                    "answer_relevancy": [],
                    "context_precision": []
                }
            by_type[qtype]["count"] += 1
            by_type[qtype]["answer_relevancy"].append(result["answer_relevancy"]["total"])
            by_type[qtype]["context_precision"].append(result["context_precision"]["precision"])
        
        # Calculate type averages
        type_metrics = {}
        for qtype, data in by_type.items():
            type_metrics[qtype] = {
                "count": data["count"],
                "avg_answer_relevancy": sum(data["answer_relevancy"]) / len(data["answer_relevancy"]),
                "avg_context_precision": sum(data["context_precision"]) / len(data["context_precision"])
            }
        
        return {
            "answer_relevancy": {
                "mean": sum(relevancy_scores) / len(relevancy_scores),
                "median": sorted(relevancy_scores)[len(relevancy_scores)//2],
                "min": min(relevancy_scores),
                "max": max(relevancy_scores)
            },
            "context_precision": {
                "mean": sum(precision_scores) / len(precision_scores),
                "median": sorted(precision_scores)[len(precision_scores)//2],
                "min": min(precision_scores),
                "max": max(precision_scores)
            },
            "context_recall": {
                "mean": sum(r["context_precision"]["recall"] for r in successful_results) / len(successful_results)
            },
            "processing_time": {
                "mean": sum(times) / len(times),
                "median": sorted(times)[len(times)//2],
                "min": min(times),
                "max": max(times)
            },
            "by_query_type": type_metrics
        }
    
    def save_results(self, evaluation_results: Dict, filepath: str):
        """Save evaluation results to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved to {filepath}")
    
    def print_summary(self, metrics: Dict):
        """Print evaluation summary."""
        print(f"\n{'='*60}")
        print(f"📊 EVALUATION SUMMARY")
        print(f"{'='*60}")
        
        print(f"\n🎯 Answer Relevancy (0-100):")
        print(f"   Mean:   {metrics['answer_relevancy']['mean']:.1f}")
        print(f"   Median: {metrics['answer_relevancy']['median']:.1f}")
        print(f"   Range:  {metrics['answer_relevancy']['min']:.1f} - {metrics['answer_relevancy']['max']:.1f}")
        
        print(f"\n🎯 Context Precision (0-1):")
        print(f"   Mean:   {metrics['context_precision']['mean']:.3f}")
        print(f"   Median: {metrics['context_precision']['median']:.3f}")
        print(f"   Range:  {metrics['context_precision']['min']:.3f} - {metrics['context_precision']['max']:.3f}")
        
        if 'context_recall' in metrics:
            print(f"\n🎯 Context Recall (0-1):")
            print(f"   Mean:   {metrics['context_recall']['mean']:.3f}")
        
        print(f"\n⏱️  Processing Time:")
        print(f"   Mean:   {metrics['processing_time']['mean']:.2f}s")
        print(f"   Median: {metrics['processing_time']['median']:.2f}s")
        
        if 'by_query_type' in metrics and metrics['by_query_type']:
            print(f"\n📋 By Query Type:")
            for qtype, data in metrics['by_query_type'].items():
                print(f"\n   {qtype.upper()} ({data['count']} queries):")
                print(f"      Answer Relevancy: {data['avg_answer_relevancy']:.1f}/100")
                print(f"      Context Precision: {data['avg_context_precision']:.3f}")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    print("RAG Evaluator - Run this via run_evaluation.py")
