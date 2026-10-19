from typing import List, Dict, Any, Optional, Literal
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
    target_question_count: int = 3

class InterviewSessionCreate(BaseModel):
    job_title: str
    job_description: str
    resume_id: Optional[str] = None
    target_question_count: int = 3
    simplified_language: bool = False
    voice_enabled: bool = False
    extended_time: bool = True

class CandidateAnswerSubmit(BaseModel):
    question_id: Optional[str] = None
    answer_text: str
    modality: Literal["text", "voice"] = "text"
    duration_seconds: Optional[int] = None

class QuestionItem(BaseModel):
    question_id: str
    turn_index: int
    topic_id: str
    topic_name: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    status: Literal["pending", "answered"] = "pending"
    candidate_answer: Optional[str] = None
    answered_at: Optional[str] = None

class QuestionResponse(BaseModel):
    question_id: str
    turn_index: int
    total_turns: int
    topic_id: str
    topic_name: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: str
    action_type: str = "NEW_QUESTION"
    is_last_question: bool = False

class SubmitAnswerResponse(BaseModel):
    session_id: str
    turn_index: int
    status: str
    is_completed: bool
    next_turn: Optional[int] = None
    message: str
    next_question: Optional[QuestionResponse] = None

class SessionDetailResponse(BaseModel):
    session_id: str
    user_id: str
    job_title: str
    job_description: str
    status: Literal["planned", "in_progress", "completed", "abandoned"]
    current_turn: int
    total_questions: int
    accessibility_settings: Dict[str, Any]
    created_at: str
    updated_at: str
    is_completed: bool
    storage_mode: str = "in_memory_fallback"

class SessionSummaryItem(BaseModel):
    session_id: str
    job_title: str
    status: str
    current_turn: int
    total_questions: int
    created_at: str

class TranscriptTurnItem(BaseModel):
    turn_index: int
    topic_name: str
    question_text: str
    simplified_question_text: Optional[str] = None
    difficulty: str
    candidate_answer: Optional[str] = None
    answered_at: Optional[str] = None

class SessionReportResponse(BaseModel):
    session_id: str
    user_id: str
    job_title: str
    status: str
    total_questions: int
    completed_turns: int
    is_completed: bool
    accessibility_settings: Dict[str, Any]
    transcript: List[TranscriptTurnItem]
    created_at: str
    completed_at: Optional[str] = None
    storage_mode: str = "in_memory_fallback"
