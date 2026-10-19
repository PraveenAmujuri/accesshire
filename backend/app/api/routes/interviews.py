from typing import List
from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_current_user
from app.schemas.interview import (
    InterviewSessionCreate,
    InterviewPlanCreate,
    CandidateAnswerSubmit,
    QuestionResponse,
    SubmitAnswerResponse,
    SessionDetailResponse,
    SessionSummaryItem,
)
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/plan")
async def generate_interview_plan(
    payload: InterviewPlanCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Blueprint generation endpoint.
    Prepares topic weighting and question distribution.
    """
    return {
        "status": "planned",
        "target_role": payload.job_title,
        "planned_topics": [
            {"id": "top_1", "name": f"{payload.job_title} Core Fundamentals", "weight": 0.4},
            {"id": "top_2", "name": "System Architecture & Design", "weight": 0.3},
            {"id": "top_3", "name": "Problem Solving & Trade-offs", "weight": 0.3}
        ],
        "target_question_count": payload.target_question_count
    }

@router.post("/start", response_model=SessionDetailResponse, status_code=status.HTTP_201_CREATED)
async def start_interview_session(
    payload: InterviewSessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """Creates and persists a new mock interview session."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.create_session(payload, user_id=user_id)

@router.get("", response_model=List[SessionSummaryItem])
async def list_interviews(
    current_user: dict = Depends(get_current_user)
):
    """Lists past and current interview sessions for the logged-in candidate."""
    user_id = current_user.get("id", "dev_candidate")
    return await InterviewService.list_user_sessions(user_id=user_id)

@router.get("/{interview_id}", response_model=SessionDetailResponse)
async def get_interview_session(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves session metadata, status, and turn progress."""
    return await InterviewService.get_session(interview_id)

@router.get("/{interview_id}/current-question", response_model=QuestionResponse)
async def get_current_question(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves the active question for the current turn."""
    return await InterviewService.get_current_question(interview_id)

@router.post("/{interview_id}/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(
    interview_id: str,
    payload: CandidateAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    """
    Records candidate answer, prevents duplicate submissions,
    and advances interview state to the next turn or marks completion.
    """
    return await InterviewService.submit_answer(interview_id, payload)

@router.post("/{interview_id}/end", response_model=SessionDetailResponse)
async def end_interview(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Concludes the interview session prematurely."""
    return await InterviewService.end_session(interview_id)
