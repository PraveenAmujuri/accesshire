import io
import pymupdf
import docx
import pytest
from app.core.security import create_access_token
from app.schemas.analysis import CandidateJobAnalysisSchema
from app.services.resume_service import ResumeService
from app.agents.candidate_job_analysis_agent import CandidateJobAnalysisAgent

def create_sample_pdf_bytes(name: str, skills: str, experience: str) -> bytes:
    """Creates an in-memory PDF document for test uploads."""
    doc = pymupdf.open()
    page = doc.new_page()
    content = f"""
    {name}
    Full Stack Software Engineer
    
    Technical Skills:
    {skills}
    
    Professional Experience:
    {experience}
    
    Projects:
    - Distributed Task Worker Platform
    - Real-time Analytics Dashboard
    """
    page.insert_text((50, 72), content)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def create_sample_docx_bytes(name: str, skills: str, experience: str) -> bytes:
    """Creates an in-memory DOCX document for test uploads."""
    doc = docx.Document()
    doc.add_heading(name, 0)
    doc.add_paragraph(f"Technical Profile: {experience}")
    doc.add_heading("Skills", level=1)
    doc.add_paragraph(skills)
    doc.add_heading("Projects", level=1)
    doc.add_paragraph("High Performance Microservices Architecture with Docker and Redis")
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def test_resume_parser_direct_extraction():
    """Verifies that PyMuPDF and python-docx extract expected text from memory streams."""
    pdf_bytes = create_sample_pdf_bytes(
        name="Sarah Connor",
        skills="Python, FastAPI, Docker, PostgreSQL, Redis",
        experience="5 years developing high-throughput web applications."
    )
    extracted_pdf = ResumeService.extract_text("sarah_resume.pdf", pdf_bytes)
    assert "Sarah Connor" in extracted_pdf
    assert "FastAPI" in extracted_pdf
    assert "PostgreSQL" in extracted_pdf

    docx_bytes = create_sample_docx_bytes(
        name="John Doe",
        skills="React, TypeScript, GraphQL, Tailwind",
        experience="Frontend Engineer building accessible interfaces."
    )
    extracted_docx = ResumeService.extract_text("john_resume.docx", docx_bytes)
    assert "John Doe" in extracted_docx
    assert "React" in extracted_docx
    assert "TypeScript" in extracted_docx

def test_resume_upload_pdf_endpoint(client):
    """Verifies POST /api/resumes/upload with a valid PDF resume."""
    token = create_access_token("user_sarah")
    headers = {"Authorization": f"Bearer {token}"}

    pdf_bytes = create_sample_pdf_bytes(
        name="Sarah Connor",
        skills="Python, FastAPI, MongoDB, Docker, Git",
        experience="Backend developer with experience in asynchronous APIs."
    )

    files = {"file": ("sarah_resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    res = client.post("/api/resumes/upload", files=files, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["filename"] == "sarah_resume.pdf"
    assert data["char_count"] > 50
    assert "Sarah Connor" in data["text_preview"]
    assert data["resume_id"].startswith("res_")

    # Verify retrieval
    resume_id = data["resume_id"]
    get_res = client.get(f"/api/resumes/{resume_id}", headers=headers)
    assert get_res.status_code == 200
    assert "Python" in get_res.json()["text"]

def test_resume_upload_docx_endpoint(client):
    """Verifies POST /api/resumes/upload with a valid DOCX resume."""
    token = create_access_token("user_john")
    headers = {"Authorization": f"Bearer {token}"}

    docx_bytes = create_sample_docx_bytes(
        name="John Doe",
        skills="JavaScript, React, Node.js, CSS, HTML",
        experience="Frontend specialist with WCAG accessibility experience."
    )

    files = {"file": ("john_resume.docx", io.BytesIO(docx_bytes), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    res = client.post("/api/resumes/upload", files=files, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["filename"] == "john_resume.docx"
    assert data["char_count"] > 50
    assert "John Doe" in data["text_preview"]

def test_resume_upload_invalid_file_extension(client):
    """Verifies rejection of unsupported file extensions."""
    token = create_access_token("user_attacker")
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("script.exe", io.BytesIO(b"malicious executable"), "application/octet-stream")}
    res = client.post("/api/resumes/upload", files=files, headers=headers)
    assert res.status_code == 400
    assert "Only .pdf and .docx documents are supported" in res.json()["detail"]

def test_cross_user_resume_access_forbidden(client):
    """Verifies User B cannot access User A's uploaded resume."""
    alice_token = create_access_token("user_alice_resume")
    bob_token = create_access_token("user_bob_resume")

    pdf_bytes = create_sample_pdf_bytes("Alice Smith", "Python, SQL", "Data Engineer")
    files = {"file": ("alice.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    upload_res = client.post("/api/resumes/upload", files=files, headers={"Authorization": f"Bearer {alice_token}"})
    assert upload_res.status_code == 200
    resume_id = upload_res.json()["resume_id"]

    # Bob attempts to read Alice's resume
    bob_res = client.get(f"/api/resumes/{resume_id}", headers={"Authorization": f"Bearer {bob_token}"})
    assert bob_res.status_code == 403
    assert "Access denied" in bob_res.json()["detail"]

def test_candidate_job_analysis_heuristic():
    """Directly tests CandidateJobAnalysisAgent deterministic heuristic analysis."""
    resume = """
    Jane Developer
    Skills: Python, FastAPI, Docker, PostgreSQL, Git, CI/CD
    Experience: 4 years as mid-level backend developer building scalable microservices.
    Key Projects:
    - Asynchronous Event Pipeline
    - Distributed Auth Microservice
    """
    jd = """
    We are seeking a Backend Software Engineer.
    Must have experience with Python, FastAPI, and Kubernetes.
    Experience with Redis and PostgreSQL is preferred.
    """
    analysis = CandidateJobAnalysisAgent.heuristic_analysis(
        resume_text=resume,
        job_description=jd,
        job_title="Backend Software Engineer"
    )

    assert isinstance(analysis, CandidateJobAnalysisSchema)
    assert len(analysis.skills) >= 3
    assert "Python" in [s.title() for s in analysis.skills]
    assert "Fastapi" in [s.title() for s in analysis.skills]
    assert analysis.experience_level in ["entry", "mid", "senior"]
    assert len(analysis.recommended_focus_areas) >= 3
    assert analysis.skill_match_analysis.match_score > 0

    # Matching skills should identify shared tech
    matching_lower = [m.lower() for m in analysis.skill_match_analysis.matching_skills]
    assert "python" in matching_lower
    assert "fastapi" in matching_lower

def test_candidate_job_analysis_api_endpoint(client):
    """Verifies POST /api/analysis/candidate-job using an uploaded resume ID."""
    token = create_access_token("user_agent1_tester")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Upload resume
    pdf_bytes = create_sample_pdf_bytes(
        name="Alex River",
        skills="Python, Django, FastAPI, PostgreSQL, Docker, AWS",
        experience="Senior Software Engineer with 6 years experience in distributed cloud systems."
    )
    files = {"file": ("alex_resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    up_res = client.post("/api/resumes/upload", files=files, headers=headers)
    assert up_res.status_code == 200
    resume_id = up_res.json()["resume_id"]

    # 2. Call analysis endpoint referencing the uploaded resume_id
    analysis_payload = {
        "resume_id": resume_id,
        "job_title": "Senior Python Backend Engineer",
        "job_description": "Looking for a Senior Python Engineer skilled in FastAPI, Docker, and AWS microservices."
    }
    ana_res = client.post("/api/analysis/candidate-job", json=analysis_payload, headers=headers)
    assert ana_res.status_code == 200
    data = ana_res.json()
    assert data["status"] == "success"
    analysis = data["analysis"]
    assert len(analysis["skills"]) > 0
    assert len(analysis["recommended_focus_areas"]) >= 3
    assert analysis["skill_match_analysis"]["match_score"] > 0
    assert "Fastapi" in [s.title() for s in analysis["skill_match_analysis"]["matching_skills"]]
    assert data["source"] in ["llm", "heuristic_fallback"]
