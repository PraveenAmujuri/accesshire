"""
Dataset Preparation CLI for AccessHire AI
Command-line interface to download, verify, clean, and organize all interview
and benchmark datasets for AccessHire AI without running on server startup.
"""

import sys
import os
import json
import logging

# Ensure backend directory is in sys.path when executed directly
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.services.dataset_manager import DatasetManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("accesshire.dataset_cli")

def main():
    print("=" * 70)
    print("AccessHire AI - Dataset Preparation & Quality Verification Pipeline")
    print("=" * 70)

    manager = DatasetManager()
    try:
        report = manager.run_all()
        print("\nPipeline execution completed successfully!")
        print("-" * 70)
        print(f"Total Questions Prepared for RAG Corpus: {report['rag_corpus_totals']}")
        print(f"Total Questions Prepared for Evaluation Benchmarks: {report['evaluation_benchmark_totals']}")
        print("-" * 70)
        print("\nBreakdown by Dataset:")
        for ds in report["datasets_processed"]:
            print(f"  * {ds['dataset']}:")
            print(f"      Raw Count: {ds['total_raw']}")
            print(f"      RAG Corpus: {ds['rag_records']}")
            print(f"      Evaluation Benchmark: {ds['eval_records']}")
            print(f"      License: {ds['license']}")
            if "policy" in ds:
                print(f"      Policy: {ds['policy']}")
            if "deduplication_ratio" in ds:
                print(f"      Dedup: {ds['deduplication_ratio']}")
        
        print("\nExcluded Datasets:")
        for ex in report["excluded_datasets"]:
            print(f"  * {ex['dataset']}: {ex['reason']}")
            
        print("=" * 70)
        print(f"Cleaning report saved to: {manager.cleaning_report_file}")
        print("=" * 70)
    except Exception as exc:
        logger.error("Dataset pipeline failed: %s", exc, exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
