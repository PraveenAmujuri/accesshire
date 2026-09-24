from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class TopicMastery(BaseModel):
    topic_id: str
    topic_name: str
    target_weight: float = 1.0
    questions_asked: int = 0
    cumulative_score: float = 0.0
    current_mastery_level: float = 0.0
    status: Literal["pending", "active", "mastered", "deficiency_detected"] = "pending"

class AccessibilityStateConfig(BaseModel):
    simplified_language: bool = False
    voice_enabled: bool = False
    extended_time: bool = True
    high_contrast: bool = False

class TurnRecord(BaseModel):
    turn_index: int
    topic_id: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"]
    candidate_answer: Optional[str] = None
    scores: Dict[str, float] = Field(default_factory=dict)
    feedback_notes: List[str] = Field(default_factory=list)
    action_decided: Optional[str] = None

class InterviewState(BaseModel):
    interview_id: str
    user_id: str
    job_title: str
    total_planned_questions: int = 6
    current_turn: int = 0
    current_topic_id: str = "init"
    current_difficulty: Literal["easy", "medium", "hard"] = "medium"
    topics: Dict[str, TopicMastery] = Field(default_factory=dict)
    history: List[TurnRecord] = Field(default_factory=list)
    cumulative_overall_score: float = 0.0
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
    is_completed: bool = False
