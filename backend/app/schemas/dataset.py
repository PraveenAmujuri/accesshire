"""
Dataset Question Schema for AccessHire AI
Normalized schema representation for knowledge-base interview questions and evaluation benchmarks.
"""

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class DatasetQuestionSchema(BaseModel):
    """
    Normalized Common Question Schema for AccessHire AI RAG Knowledge Base
    and Evaluation Benchmarks.

    Maps diverse source fields from MBPP, Spider, SParC, CS-Bench, CodeMMLU, etc.
    into a structured, predictable format suitable for embedding, BM25 retrieval,
    and adaptive question generation.
    """
    question_id: str = Field(..., description="Unique deterministic identifier (e.g., 'mbpp_12', 'spider_train_42')")
    question: str = Field(..., description="Primary problem prompt or interview question text")
    answer_or_solution: Optional[str] = Field(None, description="Ground truth answer, canonical solution code, or reference SQL")
    domain: str = Field(..., description="High-level engineering domain: 'Programming Fundamentals', 'Databases & SQL', 'Computer Science Core', 'Software Engineering'")
    topic: str = Field(..., description="Specific subtopic or technology (e.g., 'Python Algorithms', 'SQL Joins & Grouping', 'Data Structures', 'DBMS Architecture')")
    difficulty: Optional[str] = Field(None, description="'easy', 'medium', or 'hard' (normalized, null if original source doesn't provide)")
    question_type: str = Field(..., description="Question modality: 'coding_problem', 'sql_query', 'multiple_choice', 'conceptual_qa'")
    source_dataset: str = Field(..., description="Name of the originating dataset: 'MBPP', 'Spider', 'SParC', 'CS-Bench', 'CodeMMLU', etc.")
    source_reference: Optional[str] = Field(None, description="Original record ID, citation, or paper reference")
    license: str = Field(..., description="Verified dataset license (e.g., 'CC-BY-4.0', 'CC-BY-SA-4.0', 'CC-BY-NC-4.0', 'MIT')")
    tags: List[str] = Field(default_factory=list, description="Categorical tags for filtering (e.g., ['python', 'recursion', 'sqlite'])")
    split: str = Field("train", description="'rag_corpus' (train/knowledge base) or 'evaluation' (validation/test/held-out)")
    context: Optional[str] = Field(None, description="Additional context such as database schema, multi-turn history, or test imports")
    extra_metadata: Dict[str, Any] = Field(default_factory=dict, description="Dataset-specific raw attributes for inspection")
