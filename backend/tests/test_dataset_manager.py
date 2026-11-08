"""
Test suite for Dataset Management, Schema Normalization, and Storage Providers
"""

import os
import pytest
from app.schemas.dataset import DatasetQuestionSchema
from app.services.storage_provider import LocalFileSystemStorageProvider, get_storage_provider
from app.services.dataset_manager import DatasetManager
from data.datasets.metadata.registry import DATASET_REGISTRY


def test_dataset_question_schema_validation():
    """Verify common question schema enforces structure and allows null for missing fields."""
    q = DatasetQuestionSchema(
        question_id="test_mbpp_1",
        question="Write a function to return maximum of three numbers.",
        answer_or_solution="def max_of_three(a, b, c): return max(a, b, c)",
        domain="Programming Fundamentals",
        topic="Python Functions",
        difficulty="easy",
        question_type="coding_problem",
        source_dataset="MBPP",
        source_reference="Task 1",
        license="CC-BY-4.0",
        tags=["python", "basic"],
        split="rag_corpus"
    )
    dumped = q.model_dump()
    assert dumped["question_id"] == "test_mbpp_1"
    assert dumped["answer_or_solution"] is not None
    assert dumped["split"] == "rag_corpus"

    # Schema allows answer_or_solution to be None without fabricating answers
    q_null_ans = DatasetQuestionSchema(
        question_id="test_conceptual_1",
        question="Explain the difference between L1 and L2 regularization.",
        domain="Machine Learning",
        topic="Regularization",
        question_type="conceptual_qa",
        source_dataset="Interview Bank",
        license="MIT",
        split="rag_corpus"
    )
    assert q_null_ans.answer_or_solution is None
    assert q_null_ans.difficulty is None


def test_storage_provider_local_lifecycle(tmp_path):
    """Test LocalFileSystemStorageProvider write, read, and existence checks."""
    provider = LocalFileSystemStorageProvider(str(tmp_path))
    assert not provider.exists("test.json")

    sample_data = {"key": "accesshire", "records": [1, 2, 3]}
    provider.write_json("test.json", sample_data)
    assert provider.exists("test.json")

    loaded = provider.read_json("test.json")
    assert loaded["key"] == "accesshire"
    assert loaded["records"] == [1, 2, 3]


def test_dataset_registry_integrity():
    """Check dataset registry covers all investigated datasets and identifies exclusions."""
    assert "mbpp" in DATASET_REGISTRY
    assert "spider" in DATASET_REGISTRY
    assert "sparc" in DATASET_REGISTRY
    assert "cs_bench" in DATASET_REGISTRY
    assert "codemmlu" in DATASET_REGISTRY
    assert "tiqa" in DATASET_REGISTRY

    # Ensure TIQA is explicitly marked excluded
    assert DATASET_REGISTRY["tiqa"]["status"] == "excluded"
    assert DATASET_REGISTRY["tiqa"]["suitable_for_rag"] is False

    # Ensure CS-Bench and CodeMMLU are isolated from RAG corpus
    assert DATASET_REGISTRY["cs_bench"]["suitable_for_rag"] is False
    assert DATASET_REGISTRY["codemmlu"]["suitable_for_rag"] is False


def test_dataset_manager_idempotency_and_splits(tmp_path):
    """Verify DatasetManager respects directory bounds and produces valid schema records."""
    manager = DatasetManager(base_dir=str(tmp_path))
    res = manager.prepare_mbpp()
    assert res["rag_records"] > 0
    assert res["eval_records"] > 0
    assert manager.storage.exists("processed/mbpp_rag.json")
    assert manager.storage.exists("evaluation/mbpp_eval.json")

    # Second call should be idempotent and not fail
    res2 = manager.prepare_mbpp()
    assert res2["rag_records"] == res["rag_records"]
