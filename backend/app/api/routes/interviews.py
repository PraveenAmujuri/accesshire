from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_current_user
from app.schemas.interview import (
    InterviewSessionCreate,
    InterviewPlanCreate,
    CandidateAnswerSubmit,
    QuestionResponse
)

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/plan")
async def generate_interview_plan(
    payload: InterviewPlanCreate,
    current_user: dict = Depends(get_current_user)
):
    return {
        "status": "planned",
        "target_role": payload.job_title,
        "planned_topics": [
            {"id": "top_1", "name": "Technical Fundamentals", "weight": 0.3},
            {"id": "top_2", "name": "System Architecture", "weight": 0.4},
            {"id": "top_3", "name": "Problem Solving & Scenarios", "weight": 0.3}
        ],
        "target_question_count": payload.target_question_count
    }

@router.post("/start")
async def start_interview_session(
    payload: InterviewSessionCreate,
    current_user: dict = Depends(get_current_user)
):
    session_id = "sess_" + str(abs(hash(payload.job_title)))[:8]
    return {
        "session_id": session_id,
        "status": "in_progress",
        "message": "Interview session initialized. Ready for question turn 1."
    }

@router.get("/{interview_id}/current-question", response_model=QuestionResponse)
async def get_current_question(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    return QuestionResponse(
        question_id="q_1",
        turn_index=1,
        topic_id="top_1",
        topic_name="Technical Fundamentals",
        question_text="Can you explain how the Python GIL impacts multi-threaded CPU-bound tasks versus I/O-bound tasks?",
        simplified_question_text="What does Python's GIL do, and how does it change how fast CPU and I/O tasks run?",
        difficulty="medium",
        action_type="NEW_QUESTION"
    )

@router.post("/{interview_id}/submit-answer")
async def submit_answer(
    interview_id: str,
    payload: CandidateAnswerSubmit,
    current_user: dict = Depends(get_current_user)
):
    return {
        "status": "evaluated",
        "turn_index": 1,
        "evaluation": {
            "relevance_score": 8.0,
            "technical_depth_score": 7.5,
            "clarity_score": 8.5
        },
        "next_action": "FOLLOW_UP",
        "message": "Evaluation and Decision Policy loop executed."
    }
