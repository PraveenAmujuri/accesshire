from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field

class TopicMastery(BaseModel):
    topic_id: str
    topic_name: str
    target_weight: float = 1.0
    questions_asked: int = 0
    questions_allocated: int = 1
    cumulative_score: float = 0.0
    current_mastery_level: float = 0.0  # 0.0 to 1.0
    status: Literal["pending", "active", "mastered", "deficiency_detected"] = "pending"

class AccessibilityStateConfig(BaseModel):
    simplified_language: bool = False
    voice_enabled: bool = False
    extended_time: bool = True
    high_contrast: bool = False

class TurnEvaluation(BaseModel):
    relevance_score: Optional[float] = None
    technical_accuracy_score: Optional[float] = None
    depth_score: Optional[float] = None
    overall_turn_score: Optional[float] = None
    feedback_notes: List[str] = Field(default_factory=list)
    raw_evaluator_output: Optional[Dict[str, Any]] = None

class TurnRecord(BaseModel):
    turn_index: int
    question_id: str
    topic_id: str
    topic_name: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    status: Literal["pending", "answered"] = "pending"
    candidate_answer: Optional[str] = None
    answered_at: Optional[str] = None
    duration_seconds: Optional[int] = None
    evaluation: Optional[TurnEvaluation] = None
    action_decided: Optional[str] = None

class InterviewState(BaseModel):
    """
    Centralized interview state representation.
    Tracks turn execution, topic mastery vectors, candidate answers, and evaluation metrics.
    """
    session_id: str
    user_id: str
    job_title: str
    job_description: str
    resume_id: Optional[str] = None
    seniority_level: str = "mid"
    status: Literal["planned", "in_progress", "completed", "abandoned"] = "in_progress"
    current_turn: int = 1
    total_questions: int = 3
    remaining_questions: int = 3
    current_topic_id: str = "top_1"
    current_topic_name: str = "Core Fundamentals"
    current_difficulty: Literal["easy", "medium", "hard"] = "medium"
    
    # Mastery and Turn tracking
    topics: Dict[str, TopicMastery] = Field(default_factory=dict)
    turns: List[TurnRecord] = Field(default_factory=list)
    
    # Progress & evaluation aggregates
    answered_count: int = 0
    cumulative_score: float = 0.0
    average_score: Optional[float] = None
    
    # Active policy action
    active_action: Literal[
        "NEW_QUESTION",
        "FOLLOW_UP",
        "INCREASE_DIFFICULTY",
        "DECREASE_DIFFICULTY",
        "CHANGE_TOPIC",
        "CLARIFICATION",
        "CONTINUE",
        "END_INTERVIEW"
    ] = "NEW_QUESTION"
    
    accessibility: AccessibilityStateConfig = Field(default_factory=AccessibilityStateConfig)
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
    is_completed: bool = False
    storage_mode: str = "mongodb"
