from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.schemas.analysis import (
    CandidateJobAnalysisRequest,
    CandidateJobAnalysisResponse
)
from app.services.resume_service import ResumeService
from app.core.orchestrator import orchestrator

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/candidate-job", response_model=CandidateJobAnalysisResponse)
async def analyze_candidate_and_job(
    payload: CandidateJobAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Agent 1: Candidate & Job Analysis Agent.
    Analyzes candidate background (skills, experience, projects) from resume
    and matches against job description criteria, producing structured competencies,
    gap analysis, and recommended interview focus areas.
    """
    user_id = current_user.get("id") or "user_candidate"
    resume_text = payload.resume_text or ""

    # If resume_id is provided, retrieve the extracted text from storage
    if payload.resume_id and not resume_text:
        extracted = await ResumeService.get_resume_text(payload.resume_id, user_id)
        if not extracted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume with ID '{payload.resume_id}' not found."
            )
        resume_text = extracted

    if not resume_text and not payload.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Either candidate resume text (or resume_id) or a job description must be provided."
        )

    result = await orchestrator.run_candidate_job_analysis(
        resume_text=resume_text,
        job_description=payload.job_description,
        job_title=payload.job_title or ""
    )

    return CandidateJobAnalysisResponse(
        status="success",
        analysis=result["analysis"],
        source=result.get("source", "llm")
    )
