from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{interview_id}")
async def get_interview_report(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    return {
        "interview_id": interview_id,
        "overall_score": 78.0,
        "feedback_summary": {
            "strengths": ["Strong conceptual grasp of Python internals", "Structured articulation"],
            "areas_for_growth": ["Deepen understanding of multiprocessing edge cases"]
        },
        "skill_gaps": [
            {"skill": "Multiprocessing vs AsyncIO", "severity": "medium"}
        ],
        "learning_roadmap": [
            {"step": 1, "topic": "ProcessPoolExecutor & Subprocess management", "hours": 4}
        ]
    }
