from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class InterviewSessionModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    job_title: str
    job_description: str
    resume_id: Optional[str] = None
    status: str = "in_progress"  # planned, in_progress, completed, abandoned
    accessibility_settings: Dict[str, Any] = Field(default_factory=dict)
    interview_plan: Dict[str, Any] = Field(default_factory=dict)
    state_vector: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
