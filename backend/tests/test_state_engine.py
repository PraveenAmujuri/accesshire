import pytest
from app.core.security import create_access_token
from app.services.state_engine import InterviewStateEngine
from app.schemas.state import InterviewState, TurnEvaluation
from app.core.orchestrator import orchestrator

def test_state_engine_initialization():
    """Verifies that InterviewStateEngine initializes state with topics, turns, and progress tracking."""
    questions = [
        {
            "turn_index": 1,
            "question_id": "q1",
            "topic_id": "top_python",
            "topic_name": "Python Internals",
            "question_text": "Explain Python GIL.",
            "difficulty": "medium",
            "status": "pending"
        },
        {
            "turn_index": 2,
            "question_id": "q2",
            "topic_id": "top_fastapi",
            "topic_name": "FastAPI Async",
            "question_text": "Explain async endpoints in FastAPI.",
            "difficulty": "medium",
            "status": "pending"
        }
    ]

    state = InterviewStateEngine.initialize_state(
        session_id="test_sess_1",
        user_id="user_123",
        job_title="Python Backend Engineer",
        job_description="FastAPI, async/await, microservices",
        questions=questions,
        accessibility_settings={"simplified_language": True, "extended_time": True}
    )

    assert state.session_id == "test_sess_1"
    assert state.current_turn == 1
    assert state.total_questions == 2
    assert state.remaining_questions == 2
    assert state.answered_count == 0
    assert state.status == "in_progress"
    assert state.current_topic_id == "top_python"
    assert state.current_topic_name == "Python Internals"
    assert state.topics["top_python"].status == "active"
    assert state.topics["top_fastapi"].status == "pending"
    assert len(state.turns) == 2

def test_state_engine_turn_progression_and_completion():
    """Verifies that state progresses turns, tracks remaining questions, and updates topic mastery."""
    questions = [
        {
            "turn_index": 1,
            "question_id": "q1",
            "topic_id": "top_python",
            "topic_name": "Python Internals",
            "question_text": "Explain Python GIL.",
            "difficulty": "medium",
            "status": "pending"
        },
        {
            "turn_index": 2,
            "question_id": "q2",
            "topic_id": "top_fastapi",
            "topic_name": "FastAPI Async",
            "question_text": "Explain async endpoints in FastAPI.",
            "difficulty": "medium",
            "status": "pending"
        }
    ]

    state = InterviewStateEngine.initialize_state(
        session_id="test_sess_2",
        user_id="user_123",
        job_title="Python Engineer",
        job_description="FastAPI development",
        questions=questions
    )

    # First turn submission with sample evaluation data
    eval_turn1 = TurnEvaluation(
        relevance_score=90.0,
        technical_accuracy_score=85.0,
        depth_score=80.0,
        overall_turn_score=85.0,
        feedback_notes=["Good explanation of GIL concurrency impacts."]
    )

    state = InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="The GIL is a mutex that protects Python objects from concurrent threads.",
        evaluation=eval_turn1
    )

    assert state.current_turn == 2
    assert state.answered_count == 1
    assert state.remaining_questions == 1
    assert state.status == "in_progress"
    assert state.is_completed is False
    assert state.current_topic_id == "top_fastapi"
    assert state.topics["top_python"].questions_asked == 1
    assert state.topics["top_python"].cumulative_score == 85.0
    assert state.topics["top_python"].status == "mastered"
    assert state.topics["top_fastapi"].status == "active"

    # Second and final turn submission
    eval_turn2 = TurnEvaluation(
        relevance_score=95.0,
        technical_accuracy_score=90.0,
        depth_score=90.0,
        overall_turn_score=92.0,
        feedback_notes=["Clear description of async event loops."]
    )

    state = InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q2",
        answer_text="Async endpoints run concurrently on an event loop without blocking threads.",
        evaluation=eval_turn2
    )

    assert state.status == "completed"
    assert state.is_completed is True
    assert state.answered_count == 2
    assert state.remaining_questions == 0
    assert state.average_score == 88.5
    assert state.active_action == "END_INTERVIEW"
    assert state.completed_at is not None

def test_state_engine_early_termination():
    """Verifies that early termination marks state as completed and zeroes remaining questions."""
    questions = [
        {
            "turn_index": 1,
            "question_id": "q1",
            "topic_id": "top_python",
            "topic_name": "Python Internals",
            "question_text": "Explain Python GIL.",
            "difficulty": "medium",
            "status": "pending"
        }
    ]

    state = InterviewStateEngine.initialize_state(
        session_id="test_sess_3",
        user_id="user_123",
        job_title="Python Engineer",
        job_description="FastAPI development",
        questions=questions
    )

    ended_state = InterviewStateEngine.end_interview_early(state)
    assert ended_state.status == "completed"
    assert ended_state.is_completed is True
    assert ended_state.remaining_questions == 0
    assert ended_state.active_action == "END_INTERVIEW"

def test_api_session_state_lifecycle(client):
    """Verifies end-to-end API session creation, state inspection, and progression."""
    token = create_access_token(subject="state_test_user")

    # Start session
    start_res = client.post(
        "/api/interviews/start",
        json={
            "job_title": "Python Developer",
            "job_description": "FastAPI REST API engineer",
            "target_question_count": 2,
            "simplified_language": True,
            "extended_time": True,
            "voice_enabled": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_res.status_code == 201
    start_data = start_res.json()
    sess_id = start_data["session_id"]
    assert start_data["current_turn"] == 1
    assert start_data["total_questions"] == 2
    assert start_data["remaining_questions"] == 2
    assert start_data["current_topic_id"] is not None
    assert start_data["current_difficulty"] is not None

    # Get active question
    q_res = client.get(
        f"/api/interviews/{sess_id}/current-question",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert q_data["turn_index"] == 1
    assert q_data["total_turns"] == 2
    assert q_data["remaining_turns"] == 2

    # Submit first answer
    ans_res = client.post(
        f"/api/interviews/{sess_id}/submit-answer",
        json={
            "question_id": q_data["question_id"],
            "answer_text": "Python uses reference counting and a generational garbage collector.",
            "modality": "text"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["status"] == "in_progress"
    assert ans_data["next_turn"] == 2
    assert ans_data["remaining_questions"] == 1
    assert ans_data["is_completed"] is False

    # Inspect updated session detail
    detail_res = client.get(
        f"/api/interviews/{sess_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["current_turn"] == 2
    assert detail_data["remaining_questions"] == 1

    # Submit second answer to conclude
    next_q = ans_data["next_question"]
    final_res = client.post(
        f"/api/interviews/{sess_id}/submit-answer",
        json={
            "question_id": next_q["question_id"],
            "answer_text": "FastAPI leverages Pydantic and Starlette for high-performance async APIs.",
            "modality": "text"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert final_res.status_code == 200
    final_data = final_res.json()
    assert final_data["status"] == "completed"
    assert final_data["is_completed"] is True
    assert final_data["remaining_questions"] == 0
