from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.schemas.planner import (
    InterviewPlanRequest,
    InterviewPlanResponse,
    InterviewPlanSchema
)
from app.schemas.interview import (
    InterviewSessionCreate,
    CandidateAnswerSubmit,
    QuestionResponse,
    SubmitAnswerResponse,
    SessionDetailResponse,
    SessionSummaryItem,
)
from app.services.interview_service import InterviewService
from app.services.resume_service import ResumeService
from app.core.orchestrator import orchestrator

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/plan", response_model=InterviewPlanResponse)
async def generate_interview_plan(
    payload: InterviewPlanRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Agent 2: Interview Planner Agent endpoint.
    Builds structured interview topic blueprints, question quotas,
    difficulty calibration, and accessibility configurations based on
    job role and optional candidate resume/analysis.
    """
    user_id = current_user.get("id", "dev_candidate")
    resume_text = payload.resume_text or ""

    # Fetch resume text if resume_id is provided
    if payload.resume_id and not resume_text:
        fetched_text = await ResumeService.get_resume_text(payload.resume_id, user_id=user_id)
        if fetched_text:
            resume_text = fetched_text

    # Run Candidate & Job Analysis (Agent 1) if resume text is present to ground planning
    analysis_schema = None
    if resume_text:
        try:
            analysis_result = await orchestrator.run_candidate_job_analysis(
                resume_text=resume_text,
                job_description=payload.job_description,
                job_title=payload.job_title
            )
            analysis_schema = analysis_result.get("analysis")
        except Exception:
            analysis_schema = None

    # Execute Agent 2 (Interview Planner) through orchestrator supervisor
    plan_result = await orchestrator.run_interview_planner(
        job_title=payload.job_title,
        job_description=payload.job_description,
        target_question_count=payload.target_question_count,
        analysis=analysis_schema,
        simplified_language=payload.simplified_language,
        extended_time=payload.extended_time,
        voice_enabled=payload.voice_enabled
    )

    return InterviewPlanResponse(
        status="success",
        plan=plan_result["plan"],
        source=plan_result.get("source", "llm")
    )

@router.post("/start", response_model=SessionDetailResponse, status_code=status.HTTP_201_CREATED)
async def start_interview_session(
    payload: InterviewSessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Creates and persists a new mock interview session for the authenticated user."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.create_session(payload, user_id=user_id)

@router.get("", response_model=List[SessionSummaryItem])
async def list_interviews(
    current_user: dict = Depends(get_current_user)
):
    """Lists past and current interview sessions for the authenticated candidate."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.list_sessions(user_id=user_id)

@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_interview_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves session metadata, accessibility settings, and completion status."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.get_session(session_id, user_id=user_id)

@router.get("/{session_id}/current-question", response_model=QuestionResponse)
async def get_current_question(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves the active question for the current turn."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.get_current_question(session_id, user_id=user_id)

@router.post("/{session_id}/submit-answer", response_model=SubmitAnswerResponse)
async def submit_candidate_answer(
    session_id: str,
    payload: CandidateAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    """Submits candidate answer for the current question turn."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.submit_answer(session_id, payload, user_id=user_id)

@router.post("/{session_id}/end", response_model=SessionDetailResponse)
async def end_interview_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Concludes the interview session prematurely upon candidate request."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.end_session(session_id, user_id=user_id)
