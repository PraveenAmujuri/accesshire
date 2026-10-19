import pytest
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_full_interview_lifecycle(client):
    """Verifies standard sequential mock interview progression."""
    alice_token = create_access_token("user_alice")
    headers = {"Authorization": f"Bearer {alice_token}"}

    payload = {
        "job_title": "Python Backend Developer",
        "job_description": "Building asynchronous APIs using FastAPI, async/await, and distributed workers.",
        "target_question_count": 2,
        "simplified_language": True,
        "extended_time": True,
        "voice_enabled": False
    }
    create_res = client.post("/api/interviews/start", json=payload, headers=headers)
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["session_id"]
    assert session_data["user_id"] == "user_alice"
    assert session_data["status"] == "in_progress"
    assert session_data["current_turn"] == 1
    assert session_data["total_questions"] == 2
    assert session_data["is_completed"] is False
    assert "storage_mode" in session_data

    # Fetch current question (Turn 1)
    q1_res = client.get(f"/api/interviews/{session_id}/current-question", headers=headers)
    assert q1_res.status_code == 200
    q1 = q1_res.json()
    assert q1["turn_index"] == 1
    assert q1["total_turns"] == 2
    assert len(q1["question_text"]) > 10
    assert q1["simplified_question_text"] is not None
    assert q1["is_last_question"] is False
    q1_id = q1["question_id"]

    # Reject empty answer
    empty_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={"question_id": q1_id, "answer_text": "   ", "modality": "text"},
        headers=headers
    )
    assert empty_res.status_code == 422

    # Submit valid answer for Turn 1
    ans1_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q1_id,
            "answer_text": "The Python GIL restricts bytecode execution to one thread at a time in CPython.",
            "modality": "text"
        },
        headers=headers
    )
    assert ans1_res.status_code == 200
    ans1_data = ans1_res.json()
    assert ans1_data["is_completed"] is False
    assert ans1_data["next_turn"] == 2
    assert ans1_data["next_question"] is not None

    # Duplicate submission for Turn 1 rejected
    dup_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q1_id,
            "answer_text": "Duplicate submission attempt",
            "modality": "text"
        },
        headers=headers
    )
    assert dup_res.status_code in [400, 409]

    # Fetch Question for Turn 2
    q2_res = client.get(f"/api/interviews/{session_id}/current-question", headers=headers)
    assert q2_res.status_code == 200
    q2 = q2_res.json()
    assert q2["turn_index"] == 2
    assert q2["is_last_question"] is True
    q2_id = q2["question_id"]

    # Submit answer for final Turn 2
    ans2_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q2_id,
            "answer_text": "Asyncio uses an event loop with non-blocking sockets to yield control via await points.",
            "modality": "text"
        },
        headers=headers
    )
    assert ans2_res.status_code == 200
    ans2_data = ans2_res.json()
    assert ans2_data["is_completed"] is True
    assert ans2_data["status"] == "completed"

    # Submission after completion rejected
    post_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={
            "question_id": q2_id,
            "answer_text": "Post completion attempt",
            "modality": "text"
        },
        headers=headers
    )
    assert post_res.status_code == 400

    # Verify Report & Transcript
    report_res = client.get(f"/api/reports/{session_id}", headers=headers)
    assert report_res.status_code == 200
    report = report_res.json()
    assert report["user_id"] == "user_alice"
    assert report["is_completed"] is True
    assert report["completed_turns"] == 2
    assert len(report["transcript"]) == 2
    assert "GIL" in report["transcript"][0]["candidate_answer"]
    assert "Asyncio" in report["transcript"][1]["candidate_answer"]

def test_cross_user_session_authorization(client):
    """Verifies that User B cannot read or modify User A's session or report."""
    alice_token = create_access_token("user_alice")
    bob_token = create_access_token("user_bob")

    alice_headers = {"Authorization": f"Bearer {alice_token}"}
    bob_headers = {"Authorization": f"Bearer {bob_token}"}

    # Alice creates a session
    create_res = client.post(
        "/api/interviews/start",
        json={"job_title": "React Frontend Engineer", "job_description": "Building accessible UI components."},
        headers=alice_headers
    )
    assert create_res.status_code == 201
    session_id = create_res.json()["session_id"]

    # 1. Bob attempts GET session details -> 403 Forbidden
    res = client.get(f"/api/interviews/{session_id}", headers=bob_headers)
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # 2. Bob attempts GET active question -> 403 Forbidden
    res = client.get(f"/api/interviews/{session_id}/current-question", headers=bob_headers)
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # 3. Bob attempts POST submit-answer -> 403 Forbidden
    res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={"answer_text": "Unauthorized answer injection attempt.", "modality": "text"},
        headers=bob_headers
    )
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # 4. Bob attempts POST end interview early -> 403 Forbidden
    res = client.post(f"/api/interviews/{session_id}/end", headers=bob_headers)
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # 5. Bob attempts GET report & transcript -> 403 Forbidden
    res = client.get(f"/api/reports/{session_id}", headers=bob_headers)
    assert res.status_code == 403
    assert "Access denied" in res.json()["detail"]

    # Alice accesses her own session -> 200 OK
    res_alice = client.get(f"/api/interviews/{session_id}", headers=alice_headers)
    assert res_alice.status_code == 200
    assert res_alice.json()["user_id"] == "user_alice"

def test_nonexistent_session_returns_404(client):
    """Verifies that requesting an invalid or nonexistent session returns 404."""
    token = create_access_token("user_charlie")
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/interviews/sess_nonexistent_12345", headers=headers)
    assert res.status_code == 404

    res_q = client.get("/api/interviews/sess_nonexistent_12345/current-question", headers=headers)
    assert res_q.status_code == 404

    res_rep = client.get("/api/reports/sess_nonexistent_12345", headers=headers)
    assert res_rep.status_code == 404

def test_end_session_prematurely(client):
    """Verifies that ending a session early transitions status to completed."""
    token = create_access_token("user_david")
    headers = {"Authorization": f"Bearer {token}"}

    create_res = client.post(
        "/api/interviews/start",
        json={"job_title": "Full Stack Engineer", "job_description": "Node and Python APIs", "target_question_count": 3},
        headers=headers
    )
    assert create_res.status_code == 201
    session_id = create_res.json()["session_id"]

    end_res = client.post(f"/api/interviews/{session_id}/end", headers=headers)
    assert end_res.status_code == 200
    data = end_res.json()
    assert data["status"] == "completed"
    assert data["is_completed"] is True

    # Further answer submission rejected
    sub_res = client.post(
        f"/api/interviews/{session_id}/submit-answer",
        json={"answer_text": "Late answer", "modality": "text"},
        headers=headers
    )
    assert sub_res.status_code == 400

    # Report shows completed status
    rep_res = client.get(f"/api/reports/{session_id}", headers=headers)
    assert rep_res.status_code == 200
    rep = rep_res.json()
    assert rep["is_completed"] is True
    assert rep["completed_turns"] == 0

def test_concurrent_submissions_safeguard(client):
    """
    Verifies that simultaneous answer submissions cannot advance the turn twice
    or record duplicate responses for the same question.
    """
    token = create_access_token("user_concurrent")
    headers = {"Authorization": f"Bearer {token}"}

    create_res = client.post(
        "/api/interviews/start",
        json={"job_title": "Distributed Systems Engineer", "job_description": "Concurrency and messaging.", "target_question_count": 3},
        headers=headers
    )
    session_id = create_res.json()["session_id"]

    q1_res = client.get(f"/api/interviews/{session_id}/current-question", headers=headers)
    q1_id = q1_res.json()["question_id"]

    def send_submission(worker_id):
        return client.post(
            f"/api/interviews/{session_id}/submit-answer",
            json={
                "question_id": q1_id,
                "answer_text": f"Concurrent answer submission from worker {worker_id}",
                "modality": "text"
            },
            headers=headers
        )

    # Fire 2 concurrent submission requests simultaneously
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(send_submission, 1)
        future2 = executor.submit(send_submission, 2)
        res1 = future1.result()
        res2 = future2.result()

    statuses = [res1.status_code, res2.status_code]
    # Exactly one request must succeed (200), and the second must be rejected (409 Conflict)
    assert 200 in statuses
    assert 409 in statuses

    # Verify session advanced exactly by one turn to Turn 2
    session_check = client.get(f"/api/interviews/{session_id}", headers=headers).json()
    assert session_check["current_turn"] == 2
    assert session_check["status"] == "in_progress"

def test_storage_backend_transparency(client):
    """Verifies that the backend health endpoint and session details explicitly report storage mode."""
    health_res = client.get("/api/health")
    assert health_res.status_code == 200
    data = health_res.json()
    assert "storage_backend" in data
    assert data["storage_backend"] in ["mongodb", "in_memory_fallback"]

    # When MongoDB is disconnected, database_connected must be False and storage_backend must be in_memory_fallback
    if not data["database_connected"]:
        assert data["storage_backend"] == "in_memory_fallback"
