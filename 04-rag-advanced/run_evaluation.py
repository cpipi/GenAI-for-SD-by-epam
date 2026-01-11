"""
Main evaluation script to measure baseline and enhanced RAG performance.
Runs all iterations and generates comparative reports.
"""
import sys
import time
from test_dataset import TestDataset
from evaluation import RAGEvaluator
from rag_pipeline import RAGPipeline
from rag_pipeline_enhanced import EnhancedRAGPipeline


def run_baseline_evaluation(sample_size=15):
    """Run evaluation on baseline RAG pipeline."""
    print("\n" + "="*70)
    print("📊 BASELINE EVALUATION - Naive RAG Pipeline")
    print("="*70)
    print("\nConfiguration:")
    print("   - Query Expansion: DISABLED (direct user query)")
    print("   - Top-K Documents: 15 (high noise, low precision)")
    print("   - No re-ranking or filtering")
    print("   - This represents un-optimized starting point\n")
    
    try:
        evaluator = RAGEvaluator()
        rag_pipeline = RAGPipeline()
        
        # Override query method to use naive settings
        original_query = rag_pipeline.query
        def naive_query(user_query: str, expand_query: bool = False, top_k: int = 15):
            return original_query(user_query, expand_query=False, top_k=15)
        rag_pipeline.query = naive_query
        
        results = evaluator.evaluate_pipeline(rag_pipeline, sample_size=sample_size)
        
        evaluator.print_summary(results["metrics"])
        evaluator.save_results(results, "evaluation_baseline.json")
        
        rag_pipeline.close()
        
        return results
    
    except Exception as e:
        print(f"❌ Baseline evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_iteration_evaluation(iteration: int, sample_size=15):
    """Run evaluation on enhanced RAG pipeline for specific iteration."""
    print("\n" + "="*70)
    print(f"📊 ITERATION {iteration} EVALUATION - Enhanced RAG Pipeline")
    print("="*70)
    
    iteration_names = {
        1: "Hybrid Search (Vector + BM25)",
        2: "Hybrid Search + Cross-Encoder Re-ranking",
        3: "Hybrid Search + Re-ranking + Query Decomposition",
        4: "Full Pipeline (All Enhancements)"
    }
    
    print(f"\nEnhancements: {iteration_names.get(iteration, 'Unknown')}\n")
    
    try:
        evaluator = RAGEvaluator()
        rag_pipeline = EnhancedRAGPipeline(iteration=iteration)
        
        results = evaluator.evaluate_pipeline(rag_pipeline, sample_size=sample_size)
        
        evaluator.print_summary(results["metrics"])
        evaluator.save_results(results, f"evaluation_iteration{iteration}.json")
        
        rag_pipeline.close()
        
        return results
    
    except Exception as e:
        print(f"❌ Iteration {iteration} evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_results(baseline_results, iteration_results):
    """Compare baseline vs iteration results."""
    if not baseline_results or not iteration_results:
        print("⚠️  Cannot compare - missing results")
        return
    
    iteration = iteration_results["metrics"]["by_query_type"]
    
    print("\n" + "="*70)
    print("📈 IMPROVEMENT ANALYSIS")
    print("="*70)
    
    baseline_metrics = baseline_results["metrics"]
    iteration_metrics = iteration_results["metrics"]
    
    # Answer Relevancy improvement
    baseline_ar = baseline_metrics["answer_relevancy"]["mean"]
    iteration_ar = iteration_metrics["answer_relevancy"]["mean"]
    ar_improvement = ((iteration_ar - baseline_ar) / baseline_ar * 100) if baseline_ar > 0 else 0
    
    print(f"\n🎯 Answer Relevancy:")
    print(f"   Baseline:  {baseline_ar:.1f}/100")
    print(f"   Iteration: {iteration_ar:.1f}/100")
    print(f"   Change:    {ar_improvement:+.1f}%")
    
    if ar_improvement >= 30:
        print(f"   ✅ PASSED 30% improvement threshold!")
    elif ar_improvement > 0:
        print(f"   ⚠️  Improvement below 30% threshold")
    else:
        print(f"   ❌ Performance decreased")
    
    # Context Precision improvement
    baseline_cp = baseline_metrics["context_precision"]["mean"]
    iteration_cp = iteration_metrics["context_precision"]["mean"]
    cp_improvement = ((iteration_cp - baseline_cp) / baseline_cp * 100) if baseline_cp > 0 else 0
    
    print(f"\n🎯 Context Precision:")
    print(f"   Baseline:  {baseline_cp:.3f}")
    print(f"   Iteration: {iteration_cp:.3f}")
    print(f"   Change:    {cp_improvement:+.1f}%")
    
    if cp_improvement >= 30:
        print(f"   ✅ PASSED 30% improvement threshold!")
    elif cp_improvement > 0:
        print(f"   ⚠️  Improvement below 30% threshold")
    else:
        print(f"   ❌ Performance decreased")
    
    # Processing time comparison
    baseline_time = baseline_metrics["processing_time"]["mean"]
    iteration_time = iteration_metrics["processing_time"]["mean"]
    time_change = ((iteration_time - baseline_time) / baseline_time * 100) if baseline_time > 0 else 0
    
    print(f"\n⏱️  Processing Time:")
    print(f"   Baseline:  {baseline_time:.2f}s")
    print(f"   Iteration: {iteration_time:.2f}s")
    print(f"   Change:    {time_change:+.1f}%")
    
    print("\n" + "="*70)


def main():
    """Main evaluation workflow."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         RAG PIPELINE EVALUATION & ENHANCEMENT SYSTEM            ║
║                                                                  ║
║  This script will:                                              ║
║  1. Generate test dataset (45 queries)                          ║
║  2. Evaluate baseline RAG pipeline                              ║
║  3. Evaluate all enhancement iterations (1-4)                   ║
║  4. Generate comparative analysis                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration
    SAMPLE_SIZE = 15  # Test on subset to save API costs (15 queries ~$1-2)
    RUN_FULL_TEST = False  # Set to True for full 45 queries
    
    if RUN_FULL_TEST:
        SAMPLE_SIZE = None
        print("⚠️  Running FULL evaluation (45 queries) - will use more API credits\n")
    else:
        print(f"📋 Running evaluation on {SAMPLE_SIZE} queries (sample mode)\n")
    
    # Skip interactive prompt for automated runs
    # input("Press Enter to start evaluation...")
    print("Starting evaluation in 2 seconds...")
    time.sleep(2)
    
    # Step 1: Generate test dataset
    print("\n" + "="*70)
    print("📋 GENERATING TEST DATASET")
    print("="*70)
    TestDataset.save_to_file("test_dataset.json")
    
    # Step 2: Baseline evaluation
    baseline_results = run_baseline_evaluation(sample_size=SAMPLE_SIZE)
    
    if not baseline_results:
        print("\n❌ Baseline evaluation failed. Cannot continue.")
        sys.exit(1)
    
    time.sleep(2)
    
    # Step 3: Run all iterations
    all_iteration_results = {}
    
    for iteration in [1, 2, 3, 4]:
        print(f"\n⏳ Waiting 3 seconds before next iteration...")
        time.sleep(3)
        
        iteration_results = run_iteration_evaluation(iteration, sample_size=SAMPLE_SIZE)
        
        if iteration_results:
            all_iteration_results[iteration] = iteration_results
            
            # Compare with baseline
            compare_results(baseline_results, iteration_results)
    
    # Step 4: Final summary
    print("\n" + "="*70)
    print("🎉 EVALUATION COMPLETE!")
    print("="*70)
    
    print("\n📁 Generated files:")
    print("   - test_dataset.json")
    print("   - evaluation_baseline.json")
    for i in range(1, 5):
        if i in all_iteration_results:
            print(f"   - evaluation_iteration{i}.json")
    
    print("\n📊 Next steps:")
    print("   1. Review evaluation JSON files")
    print("   2. Run: python generate_report.py (to create ENHANCEMENT_REPORT.md)")
    print("   3. Analyze which iteration provides best improvement")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
