from typing import List, Optional
from pydantic import BaseModel, Field

class JobCriteria(BaseModel):
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    competencies: List[str] = Field(default_factory=list)
    seniority_level: str = "mid"

class SkillMatchAnalysis(BaseModel):
    matching_skills: List[str] = Field(default_factory=list)
    missing_or_gap_skills: List[str] = Field(default_factory=list)
    match_score: float = Field(default=0.0, ge=0.0, le=100.0)  # 0 to 100

class CandidateJobAnalysisSchema(BaseModel):
    candidate_summary: str = Field(description="2-3 sentence overview of the candidate's background and technical profile")
    skills: List[str] = Field(default_factory=list, description="All technical & domain skills extracted from candidate resume")
    experience_level: str = Field(default="mid", description="Detected experience level: entry, mid, or senior")
    key_projects_or_roles: List[str] = Field(default_factory=list, description="Notable projects, achievements, or employment roles")
    job_requirements: JobCriteria = Field(default_factory=JobCriteria, description="Extracted core requirements from the job description")
    skill_match_analysis: SkillMatchAnalysis = Field(default_factory=SkillMatchAnalysis, description="Detailed alignment between candidate and JD requirements")
    recommended_focus_areas: List[str] = Field(default_factory=list, description="3-5 recommended competency topics to assess during the interview")
    raw_analysis_notes: Optional[str] = None

class CandidateJobAnalysisRequest(BaseModel):
    resume_text: Optional[str] = None
    resume_id: Optional[str] = None
    job_title: Optional[str] = ""
    job_description: str

class CandidateJobAnalysisResponse(BaseModel):
    status: str = "success"
    analysis: CandidateJobAnalysisSchema
    source: str = "llm"  # 'llm' or 'heuristic_fallback'

class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    file_size: int
    char_count: int
    text_preview: str
    storage_mode: str = "mongodb"
