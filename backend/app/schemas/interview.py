from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class PlannedTopic(BaseModel):
    id: str
    name: str
    priority: Literal["low", "medium", "high"] = "medium"
    weight: float = 1.0

class InterviewPlanCreate(BaseModel):
    job_title: str
    job_description: str
    resume_text: Optional[str] = None
    target_question_count: int = 6

class InterviewSessionCreate(BaseModel):
    job_title: str
    job_description: str
    resume_id: Optional[str] = None
    simplified_language: bool = False
    voice_enabled: bool = False
    extended_time: bool = True

class CandidateAnswerSubmit(BaseModel):
    answer_text: str
    modality: Literal["text", "voice"] = "text"
    duration_seconds: Optional[int] = None

class QuestionResponse(BaseModel):
    question_id: str
    turn_index: int
    topic_id: str
    topic_name: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: str
    action_type: str

class EvaluationResponse(BaseModel):
    relevance_score: float
    technical_depth_score: float
    clarity_score: float
    feedback: str
    next_action: str
