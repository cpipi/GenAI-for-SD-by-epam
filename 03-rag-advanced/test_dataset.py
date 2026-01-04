"""
Test dataset with ground truth queries for RAG evaluation.
Contains 45 queries covering fact lookup, comparisons, and trends.
"""
import json
from typing import List, Dict


class TestDataset:
    """Financial reports test dataset with ground truth."""
    
    @staticmethod
    def get_test_queries() -> List[Dict]:
        """
        Returns test queries with expected answers and relevant documents.
        
        Query types:
        - Fact Lookup: Simple information retrieval
        - Comparisons: Multi-bank or multi-period comparisons
        - Trends: Temporal analysis and changes
        """
        return [
            # ===== FACT LOOKUP QUERIES (15 queries) =====
            {
                "id": 1,
                "query": "What was Kaspi Bank's net profit in Q3 2024?",
                "type": "fact_lookup",
                "expected_answer": "220.03 billion KZT",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 2,
                "query": "What is Halyk Bank's capital adequacy ratio in Q4 2024?",
                "type": "fact_lookup",
                "expected_answer": "17.07%",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 3,
                "query": "How many branches does ForteBank operate?",
                "type": "fact_lookup",
                "expected_answer": "146 branches",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 4,
                "query": "What was Halyk Bank's ROE in Q1 2024?",
                "type": "fact_lookup",
                "expected_answer": "11.76%",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 5,
                "query": "What is Kaspi Bank's total assets in Q2 2024?",
                "type": "fact_lookup",
                "expected_answer": "8528.00 billion KZT",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q2"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 6,
                "query": "What is ForteBank's NPL ratio in Q4 2024?",
                "type": "fact_lookup",
                "expected_answer": "5.05%",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 7,
                "query": "How many digital banking users does Kaspi Bank have in Q3 2024?",
                "type": "fact_lookup",
                "expected_answer": "1,343,171 digital banking users",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 8,
                "query": "What is Halyk Bank's market share by assets?",
                "type": "fact_lookup",
                "expected_answer": "20.94% market share by assets",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 9,
                "query": "What was ForteBank's net interest margin in Q2 2024?",
                "type": "fact_lookup",
                "expected_answer": "6.42%",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q2"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 10,
                "query": "How many employees does Halyk Bank have?",
                "type": "fact_lookup",
                "expected_answer": "8,816 employees",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 11,
                "query": "What is Kaspi Bank's loan-to-deposit ratio in Q4 2024?",
                "type": "fact_lookup",
                "expected_answer": "78.6%",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 12,
                "query": "What is ForteBank's total active clients count in Q3 2024?",
                "type": "fact_lookup",
                "expected_answer": "452,291 active clients",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 13,
                "query": "What was Halyk Bank's cost-to-income ratio in Q2 2024?",
                "type": "fact_lookup",
                "expected_answer": "36.1%",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q2"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 14,
                "query": "What is Kaspi Bank's ranking in Kazakhstan?",
                "type": "fact_lookup",
                "expected_answer": "#2 ranking",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            {
                "id": 15,
                "query": "What is ForteBank's liquidity coverage ratio in Q1 2024?",
                "type": "fact_lookup",
                "expected_answer": "149.8%",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1"],
                "expected_years": [2024],
                "complexity": "simple"
            },
            
            # ===== COMPARISON QUERIES (15 queries) =====
            # NOTE: Expected answers for comparison queries are approximations
            # based on the generated financial data. LLM-as-judge should be
            # more lenient for these complex queries.
            {
                "id": 16,
                "query": "Compare the ROE of all three banks in Q4 2024",
                "type": "comparison",
                "expected_answer": "Kaspi Bank: 19.98%, Halyk Bank: 19.65%, ForteBank: 16.87%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 17,
                "query": "Which bank has the highest total assets in Q3 2024?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with 12544.00 billion KZT",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 18,
                "query": "Compare Kaspi Bank and Halyk Bank's net profit in Q2 2024",
                "type": "comparison",
                "expected_answer": "Halyk Bank: 234.25 billion KZT, Kaspi Bank: 198.48 billion KZT",
                "expected_banks": ["Kaspi Bank", "Halyk Bank"],
                "expected_quarters": ["Q2"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 19,
                "query": "Which bank has the best capital adequacy ratio in Q1 2024?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with 19.38%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q1"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 20,
                "query": "Compare the NPL ratios of all banks in Q4 2024",
                "type": "comparison",
                "expected_answer": "Kaspi Bank: 3.71%, Halyk Bank: 3.87%, ForteBank: 4.39%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 21,
                "query": "Which bank has the most branches?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with around 120-121 branches",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 22,
                "query": "Compare digital banking users between Kaspi Bank and ForteBank in Q3 2024",
                "type": "comparison",
                "expected_answer": "Kaspi Bank: 781,290, ForteBank: 272,267",
                "expected_banks": ["Kaspi Bank", "ForteBank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 23,
                "query": "Which bank has the highest market share by loans?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with around 31-32%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 24,
                "query": "Compare the cost-to-income ratios in Q3 2024",
                "type": "comparison",
                "expected_answer": "Halyk Bank: 36.3%, Kaspi Bank: 38.7%, ForteBank: 44.9%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 25,
                "query": "Which bank has the most ATMs?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with around 640-645 ATMs",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 26,
                "query": "Compare loan-to-deposit ratios of all banks in Q2 2024",
                "type": "comparison",
                "expected_answer": "Kaspi Bank: 77.3%, Halyk Bank: 74.8%, ForteBank: 75.1%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q2"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 27,
                "query": "Which bank has the highest ROA in Q4 2024?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with 2.43%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 28,
                "query": "Compare the number of employees across all three banks in Q1 2024",
                "type": "comparison",
                "expected_answer": "Halyk Bank: 2,698, Kaspi Bank: 1,445, ForteBank: 952",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q1"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 29,
                "query": "Which bank has the best Tier 1 capital ratio in Q3 2024?",
                "type": "comparison",
                "expected_answer": "Halyk Bank with 17.82%",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q3"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 30,
                "query": "Compare total active clients for all banks in Q4 2024",
                "type": "comparison",
                "expected_answer": "Halyk Bank: 1,634,320, Kaspi Bank: 932,677, ForteBank: 346,950",
                "expected_banks": ["Kaspi Bank", "Halyk Bank", "ForteBank"],
                "expected_quarters": ["Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            
            # ===== TREND QUERIES (15 queries) =====
            {
                "id": 31,
                "query": "How did Kaspi Bank's net profit change from Q1 to Q4 2024?",
                "type": "trend",
                "expected_answer": "Increased from 190.76 to 222.88 billion KZT (16.8% growth)",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 32,
                "query": "What is the trend of Halyk Bank's total assets throughout 2024?",
                "type": "trend",
                "expected_answer": "Grew from 12296.00 to 12744.00 billion KZT (3.6% growth)",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 33,
                "query": "How did ForteBank's ROE evolve in 2024?",
                "type": "trend",
                "expected_answer": "Varied between 15.99% (Q1) and 17.01% (Q2), ended at 16.87% (Q4)",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 34,
                "query": "Show the trend of Kaspi Bank's digital banking users in 2024",
                "type": "trend",
                "expected_answer": "Grew from 753,202 (Q1) to 795,463 (Q4), showing 5.6% growth",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 35,
                "query": "How did Halyk Bank's NPL ratio change throughout 2024?",
                "type": "trend",
                "expected_answer": "Improved from 4.50% (Q1) to 3.87% (Q4)",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 36,
                "query": "What is the quarterly net profit trend for ForteBank in 2024?",
                "type": "trend",
                "expected_answer": "Q1: 42.96, Q2: 45.77, Q3: 48.16, Q4: 49.21 billion KZT (consistent growth)",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 37,
                "query": "How did Kaspi Bank's capital adequacy ratio change in 2024?",
                "type": "trend",
                "expected_answer": "Increased from 18.97% (Q1) to 20.89% (Q4)",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 38,
                "query": "Show the trend of Halyk Bank's loan portfolio growth in 2024",
                "type": "trend",
                "expected_answer": "Grew from 8295.99 (Q1) to 8619.60 (Q4) billion KZT (3.9% growth)",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 39,
                "query": "How did ForteBank's branch network change in 2024?",
                "type": "trend",
                "expected_answer": "Increased from 45 (Q1) to 47 (Q4) branches",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 40,
                "query": "What is the trend of Kaspi Bank's cost-to-income ratio in 2024?",
                "type": "trend",
                "expected_answer": "Decreased from 42.1% (Q1) to 37.2% (Q4), showing improved efficiency",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 41,
                "query": "How did Halyk Bank's market share by assets evolve in 2024?",
                "type": "trend",
                "expected_answer": "Remained stable around 28.88-29.06%",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 42,
                "query": "Show ForteBank's total active clients growth trend in 2024",
                "type": "trend",
                "expected_answer": "Grew from 332,485 (Q1) to 346,950 (Q4), 4.4% increase",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 43,
                "query": "How did Kaspi Bank's net interest margin trend in 2024?",
                "type": "trend",
                "expected_answer": "Increased from 4.50% (Q1) to 7.38% (Q4)",
                "expected_banks": ["Kaspi Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 44,
                "query": "What is the trend of Halyk Bank's customer deposits in 2024?",
                "type": "trend",
                "expected_answer": "Grew from 9724.03 (Q1) to 10061.15 (Q4) billion KZT (3.5% growth)",
                "expected_banks": ["Halyk Bank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            },
            {
                "id": 45,
                "query": "How did ForteBank's liquidity coverage ratio change throughout 2024?",
                "type": "trend",
                "expected_answer": "Increased from 156.0% (Q1) to 169.5% (Q4)",
                "expected_banks": ["ForteBank"],
                "expected_quarters": ["Q1", "Q2", "Q3", "Q4"],
                "expected_years": [2024],
                "complexity": "medium"
            }
        ]
    
    @staticmethod
    def get_statistics():
        """Get dataset statistics."""
        queries = TestDataset.get_test_queries()
        
        stats = {
            "total_queries": len(queries),
            "by_type": {},
            "by_complexity": {},
            "by_bank": {}
        }
        
        for query in queries:
            # Count by type
            qtype = query["type"]
            stats["by_type"][qtype] = stats["by_type"].get(qtype, 0) + 1
            
            # Count by complexity
            complexity = query["complexity"]
            stats["by_complexity"][complexity] = stats["by_complexity"].get(complexity, 0) + 1
            
            # Count by bank
            for bank in query["expected_banks"]:
                stats["by_bank"][bank] = stats["by_bank"].get(bank, 0) + 1
        
        return stats
    
    @staticmethod
    def save_to_file(filepath: str = "test_dataset.json"):
        """Save test dataset to JSON file."""
        queries = TestDataset.get_test_queries()
        stats = TestDataset.get_statistics()
        
        output = {
            "metadata": {
                "description": "Test dataset for RAG financial reports evaluation",
                "version": "1.0",
                "total_queries": len(queries),
                "statistics": stats
            },
            "queries": queries
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Test dataset saved to {filepath}")
        print(f"   Total queries: {len(queries)}")
        print(f"   By type: {stats['by_type']}")


if __name__ == "__main__":
    # Generate and save test dataset
    TestDataset.save_to_file("test_dataset.json")
    
    # Print sample queries
    queries = TestDataset.get_test_queries()
    print("\n📋 Sample queries:")
    for i, query in enumerate(queries[:5], 1):
        print(f"\n{i}. [{query['type'].upper()}] {query['query']}")
        print(f"   Expected: {query['expected_answer']}")
