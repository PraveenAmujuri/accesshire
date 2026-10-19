from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.schemas.interview import SessionReportResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{interview_id}", response_model=SessionReportResponse)
async def get_interview_report(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retrieves session report and complete turn-by-turn question/answer transcript."""
    return await InterviewService.get_session_report(interview_id)
