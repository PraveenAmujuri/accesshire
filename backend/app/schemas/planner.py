from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class PlannedTopicDomain(BaseModel):
    id: str = Field(description="Unique identifier for the planned domain (e.g., 'top_1')")
    name: str = Field(description="Display title of the domain (e.g., 'Python Concurrency & Memory')")
    category: str = Field(description="High-level category (e.g., 'core_skills', 'system_design', 'problem_solving')")
    priority: Literal["low", "medium", "high"] = Field(default="medium", description="Topic importance")
    weight: float = Field(default=1.0, ge=0.1, le=5.0, description="Relative scoring weight")
    allocated_questions: int = Field(default=1, ge=1, description="Target question count allocated to this topic")
    sample_question_prompt: Optional[str] = Field(default=None, description="Starting sample interview question")
    simplified_prompt: Optional[str] = Field(default=None, description="Plain-language variant for accessibility")

class InterviewPlanSchema(BaseModel):
    job_title: str = Field(description="Target job title or role")
    target_question_count: int = Field(default=3, ge=1, le=10, description="Total planned question count")
    starting_difficulty: Literal["easy", "medium", "hard"] = Field(default="medium", description="Starting difficulty level")
    seniority_level: str = Field(default="mid", description="Detected or requested seniority (entry, mid, senior)")
    assessment_strategy: str = Field(description="2-3 sentence overview of how the interview plan evaluates the candidate")
    planned_topics: List[PlannedTopicDomain] = Field(default_factory=list, description="3-5 structured assessment topic domains")
    accessibility_accommodations_applied: List[str] = Field(default_factory=list, description="List of accommodations activated")

class InterviewPlanRequest(BaseModel):
    job_title: str
    job_description: str
    resume_id: Optional[str] = None
    resume_text: Optional[str] = None
    target_question_count: int = 3
    simplified_language: bool = False
    extended_time: bool = True
    voice_enabled: bool = False

class InterviewPlanResponse(BaseModel):
    status: str = "success"
    plan: InterviewPlanSchema
    source: str = "llm"  # 'llm' or 'heuristic_fallback'
