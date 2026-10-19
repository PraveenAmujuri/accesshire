import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_full_interview_lifecycle(client):
    # 1. Create a session
    payload = {
        "job_title": "Python Backend Developer",
        "job_description": "Building asynchronous APIs using FastAPI, async/await, and distributed workers.",
        "target_question_count": 2,
        "simplified_language": True,
        "extended_time": True,
        "voice_enabled": False
    }
    create_res = client.post("/api/interviews/start", json=payload)
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["session_id"]
    assert session_data["status"] == "in_progress"
    assert session_data["current_turn"] == 1
    assert session_data["total_questions"] == 2
    assert session_data["is_completed"] is False

    # 2. Fetch current question (Turn 1)
    q1_res = client.get(f"/api/interviews/{session_id}/current-question")
    assert q1_res.status_code == 200
    q1 = q1_res.json()
    assert q1["turn_index"] == 1
    assert q1["total_turns"] == 2
    assert len(q1["question_text"]) > 10
    assert q1["simplified_question_text"] is not None
    assert q1["is_last_question"] is False
    q1_id = q1["question_id"]

    # 3. Reject empty answer
    empty_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={"question_id": q1_id, "answer_text": "   ", "modality": "text"}
    )
    assert empty_res.status_code == 422

    # 4. Submit valid answer for Turn 1
    ans1_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q1_id,
            "answer_text": "The Python GIL restricts bytecode execution to one thread at a time in CPython.",
            "modality": "text"
        }
    )
    assert ans1_res.status_code == 200
    ans1_data = ans1_res.json()
    assert ans1_data["is_completed"] is False
    assert ans1_data["next_turn"] == 2
    assert ans1_data["next_question"] is not None

    # 5. Prevent duplicate submission for Turn 1
    dup_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q1_id,
            "answer_text": "Duplicate submission attempt",
            "modality": "text"
        }
    )
    # Rejects because q1 is already answered and/or doesn't match active turn 2
    assert dup_res.status_code in [400, 409]

    # 6. Fetch Question for Turn 2
    q2_res = client.get(f"/api/interviews/{session_id}/current-question")
    assert q2_res.status_code == 200
    q2 = q2_res.json()
    assert q2["turn_index"] == 2
    assert q2["is_last_question"] is True
    q2_id = q2["question_id"]

    # 7. Submit answer for final Turn 2
    ans2_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q2_id,
            "answer_text": "Asyncio uses an event loop with non-blocking sockets to yield control via await points.",
            "modality": "text"
        }
    )
    assert ans2_res.status_code == 200
    ans2_data = ans2_res.json()
    assert ans2_data["is_completed"] is True
    assert ans2_data["status"] == "completed"

    # 8. Prevent submission after completion
    post_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q2_id,
            "answer_text": "Post completion attempt",
            "modality": "text"
        }
    )
    assert post_res.status_code == 400

    # 9. Verify Report & Transcript
    report_res = client.get(f"/api/reports/{session_id}")
    assert report_res.status_code == 200
    report = report_res.json()
    assert report["is_completed"] is True
    assert report["completed_turns"] == 2
    assert len(report["transcript"]) == 2
    assert "GIL" in report["transcript"][0]["candidate_answer"]
    assert "Asyncio" in report["transcript"][1]["candidate_answer"]

    # 10. Verify List in User Interviews
    list_res = client.get("/api/interviews")
    assert list_res.status_code == 200
    items = list_res.json()
    found = any(item["session_id"] == session_id for item in items)
    assert found is True
