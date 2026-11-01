import pytest
from app.core.security import create_access_token
from app.agents.interview_planner_agent import InterviewPlannerAgent
from app.schemas.planner import InterviewPlanSchema, InterviewPlanRequest
from app.schemas.analysis import (
    CandidateJobAnalysisSchema,
    JobCriteria,
    SkillMatchAnalysis
)

def create_sample_analysis(role: str, exp_level: str = "mid") -> CandidateJobAnalysisSchema:
    return CandidateJobAnalysisSchema(
        candidate_summary="Experienced developer with background in asynchronous Python and cloud databases.",
        skills=["Python", "FastAPI", "Docker", "PostgreSQL", "Redis"],
        experience_level=exp_level,
        key_projects_or_roles=["Distributed Data Pipeline", "Async REST Service"],
        job_requirements=JobCriteria(
            required_skills=["Python", "FastAPI", "Kubernetes", "System Design"],
            preferred_skills=["GraphQL", "Terraform"],
            competencies=["Core Concurrency", "Scalable Architecture", "Error Handling"],
            seniority_level=exp_level
        ),
        skill_match_analysis=SkillMatchAnalysis(
            matching_skills=["Python", "FastAPI"],
            missing_or_gap_skills=["Kubernetes", "System Design"],
            match_score=50.0
        ),
        recommended_focus_areas=[
            "In-depth discussion on Python and applied projects",
            "Assessment of foundational readiness in Kubernetes",
            "System architecture and clean code maintainability",
            "Error handling, testing, and debugging strategies"
        ]
    )

def test_interview_planner_heuristic_direct():
    """Verifies that InterviewPlannerAgent creates structured plans deterministically."""
    analysis = create_sample_analysis(role="Python Engineer", exp_level="senior")

    plan: InterviewPlanSchema = InterviewPlannerAgent.heuristic_plan(
        job_title="Senior Python Backend Architect",
        job_description="Architecting fault-tolerant microservices using FastAPI and Kubernetes.",
        target_question_count=4,
        analysis=analysis,
        simplified_language=True,
        extended_time=True
    )

    assert plan.job_title == "Senior Python Backend Architect"
    assert plan.target_question_count == 4
    assert plan.starting_difficulty == "hard"
    assert plan.seniority_level == "senior"
    assert len(plan.planned_topics) >= 3
    # Check allocated questions equals target question count
    total_allocated = sum(t.allocated_questions for t in plan.planned_topics)
    assert total_allocated == 4
    assert "Simplified plain-language question phrasing" in plan.accessibility_accommodations_applied
    assert "Extended deliberation and untimed pause tolerance" in plan.accessibility_accommodations_applied

def test_interview_planner_entry_level_calibration():
    """Verifies that entry-level candidate profiles start at 'easy' difficulty."""
    analysis = create_sample_analysis(role="Junior Frontend Developer", exp_level="entry")

    plan: InterviewPlanSchema = InterviewPlannerAgent.heuristic_plan(
        job_title="Junior Frontend Engineer",
        job_description="Developing accessible React interfaces.",
        target_question_count=3,
        analysis=analysis,
        simplified_language=False
    )

    assert plan.starting_difficulty == "easy"
    assert plan.seniority_level == "entry"
    assert sum(t.allocated_questions for t in plan.planned_topics) == 3

def test_interview_plan_endpoint_authenticated(client):
    """Verifies POST /api/interviews/plan generates a verified blueprint."""
    token = create_access_token(subject="planner_test_user")

    payload = {
        "job_title": "Python Developer",
        "job_description": "Building microservices using Python and FastAPI.",
        "target_question_count": 3,
        "simplified_language": True,
        "extended_time": True,
        "voice_enabled": False
    }

    res = client.post(
        "/api/interviews/plan",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "plan" in data
    plan = data["plan"]
    assert plan["job_title"] == "Python Developer"
    assert plan["target_question_count"] == 3
    assert len(plan["planned_topics"]) >= 2
    assert any(t["priority"] in ["high", "medium", "low"] for t in plan["planned_topics"])

def test_interview_plan_endpoint_unauthorized_rejected(client):
    """Verifies that POST /api/interviews/plan strictly requires Bearer authentication."""
    res = client.post(
        "/api/interviews/plan",
        json={
            "job_title": "Backend Developer",
            "job_description": "FastAPI development",
            "target_question_count": 3
        }
    )
    assert res.status_code == 401
