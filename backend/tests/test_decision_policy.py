import pytest
from app.core.security import create_access_token
from app.services.state_engine import InterviewStateEngine
from app.agents.decision_policy_agent import DecisionPolicyAgent
from app.schemas.state import InterviewState, TurnEvaluation
from app.schemas.policy import PolicyDecision

def create_mock_state(remaining: int = 3, current_diff: str = "medium") -> InterviewState:
    questions = [
        {
            "turn_index": 1,
            "question_id": "q1",
            "topic_id": "top_python",
            "topic_name": "Python Internals",
            "question_text": "Explain Python GIL.",
            "difficulty": current_diff,
            "status": "pending"
        },
        {
            "turn_index": 2,
            "question_id": "q2",
            "topic_id": "top_python",
            "topic_name": "Python Internals",
            "question_text": "Explain memory management and reference counting in Python.",
            "difficulty": current_diff,
            "status": "pending"
        },
        {
            "turn_index": 3,
            "question_id": "q3",
            "topic_id": "top_fastapi",
            "topic_name": "FastAPI Architecture",
            "question_text": "How do dependency injection and background tasks work in FastAPI?",
            "difficulty": current_diff,
            "status": "pending"
        }
    ]
    state = InterviewStateEngine.initialize_state(
        session_id="test_policy_sess",
        user_id="user_policy_test",
        job_title="Senior Python Engineer",
        job_description="FastAPI, async, microservices",
        questions=questions
    )
    return state

def test_decision_policy_initial_action():
    """At interview start with no answers yet, action should be ASK_NEW_QUESTION."""
    state = create_mock_state()
    decision: PolicyDecision = DecisionPolicyAgent.decide(state)
    assert decision.action == "ASK_NEW_QUESTION"
    assert "Commencing first assessment turn" in decision.reason
    assert decision.target_difficulty == "medium"
    assert decision.is_terminal is False

def test_decision_policy_clarification_rule():
    """Candidate requesting clarification triggers CLARIFY_QUESTION with transparent reason."""
    state = create_mock_state()
    # Record candidate asking for clarification
    InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="Could you clarify what you mean by the GIL and rephrase the question?",
    )
    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "CLARIFY_QUESTION"
    assert "Candidate requested question clarification" in decision.reason
    assert decision.is_terminal is False

def test_decision_policy_follow_up_rule():
    """Superficial or brief answer triggers ASK_FOLLOW_UP to probe for technical depth."""
    state = create_mock_state()
    eval_brief = TurnEvaluation(
        relevance_score=60.0,
        technical_accuracy_score=60.0,
        depth_score=35.0,  # Below 50 depth threshold
        overall_turn_score=50.0
    )
    InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="It is a thread lock.",
        evaluation=eval_brief
    )
    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "ASK_FOLLOW_UP"
    assert "depth score: 35.0" in decision.reason or "brief" in decision.reason
    assert decision.target_topic_id == "top_python"

def test_decision_policy_increase_difficulty():
    """High score (>= 85.0) escalates difficulty from medium to hard."""
    state = create_mock_state(current_diff="medium")
    eval_high = TurnEvaluation(
        relevance_score=95.0,
        technical_accuracy_score=90.0,
        depth_score=90.0,
        overall_turn_score=92.0
    )
    InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="The GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously. For I/O bound tasks, the GIL is released.",
        evaluation=eval_high
    )
    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "INCREASE_DIFFICULTY"
    assert decision.target_difficulty == "hard"
    assert "Escalating difficulty" in decision.reason

def test_decision_policy_decrease_difficulty():
    """Low score (< 45.0) on hard/medium de-escalates difficulty."""
    state = create_mock_state(current_diff="medium")
    eval_low = TurnEvaluation(
        relevance_score=30.0,
        technical_accuracy_score=35.0,
        depth_score=30.0,
        overall_turn_score=32.0
    )
    InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="I don't know much about GIL, maybe it has to do with variables in functions.",
        evaluation=eval_low
    )
    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "DECREASE_DIFFICULTY"
    assert decision.target_difficulty == "easy"
    assert "De-escalating difficulty" in decision.reason

def test_decision_policy_change_topic_on_quota_fulfillment():
    """When a topic's allocated questions are fulfilled, policy rotates to the next planned domain."""
    # Custom 2-topic state with 1 question allocated each
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
            "topic_name": "FastAPI Architecture",
            "question_text": "Explain async endpoints in FastAPI.",
            "difficulty": "medium",
            "status": "pending"
        }
    ]
    state = InterviewStateEngine.initialize_state(
        session_id="test_policy_sess",
        user_id="user_policy_test",
        job_title="Senior Python Engineer",
        job_description="FastAPI, async, microservices",
        questions=questions
    )
    # 'top_python' has questions_allocated = 1. Submitting turn 1 fulfills it.
    eval_ok = TurnEvaluation(
        relevance_score=75.0,
        technical_accuracy_score=75.0,
        depth_score=75.0,
        overall_turn_score=75.0
    )
    InterviewStateEngine.record_answer_and_progress(
        state=state,
        question_id="q1",
        answer_text="The GIL serializes thread access to CPython memory management structures, making single-threaded execution fast.",
        evaluation=eval_ok
    )
    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "CHANGE_TOPIC"
    assert decision.target_topic_id == "top_fastapi"
    assert "Transitioning to next planned domain" in decision.reason

def test_decision_policy_end_interview_when_quota_exhausted():
    """When all planned questions are completed, policy must decide END_INTERVIEW."""
    state = create_mock_state()
    state.remaining_questions = 0
    state.answered_count = state.total_questions

    decision = DecisionPolicyAgent.decide(state)
    assert decision.action == "END_INTERVIEW"
    assert decision.is_terminal is True
    assert decision.remaining_quota == 0
    assert "quota exhausted" in decision.reason.lower()

def test_api_submit_answer_returns_policy_decision(client):
    """Verifies that submitting an answer via API returns the transparent decision action and reason."""
    token = create_access_token(subject="policy_api_test_user")

    # Start session with 2 questions
    start_res = client.post(
        "/api/interviews/start",
        json={
            "job_title": "Python Developer",
            "job_description": "FastAPI REST microservices",
            "target_question_count": 2,
            "simplified_language": False,
            "extended_time": True,
            "voice_enabled": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert start_res.status_code == 201
    sess_id = start_res.json()["session_id"]

    # Submit first answer
    ans_res = client.post(
        f"/api/interviews/{sess_id}/submit-answer",
        json={
            "answer_text": "In Python, async and await use an event loop to handle concurrent network sockets.",
            "modality": "text"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["status"] == "in_progress"
    assert "action_decided" in ans_data
    assert ans_data["action_decided"] in [
        "ASK_NEW_QUESTION",
        "ASK_FOLLOW_UP",
        "INCREASE_DIFFICULTY",
        "DECREASE_DIFFICULTY",
        "CHANGE_TOPIC",
        "CLARIFY_QUESTION",
        "CONTINUE_INTERVIEW"
    ]
    assert ans_data["action_reason"] is not None
    assert len(ans_data["action_reason"]) > 10
