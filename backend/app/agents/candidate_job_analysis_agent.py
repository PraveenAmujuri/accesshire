import re
import json
import logging
from typing import Dict, Any, List, Set, Optional
from app.core.config import settings
from app.schemas.analysis import (
    CandidateJobAnalysisSchema,
    JobCriteria,
    SkillMatchAnalysis
)

logger = logging.getLogger("accesshire.agents.candidate_job_analysis")

# Comprehensive technology and skill lexicon for deterministic keyword extraction and matching
TECH_LEXICON: Dict[str, List[str]] = {
    "languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "sql", "html", "css"
    ],
    "frameworks": [
        "react", "next.js", "vue", "angular", "fastapi", "django", "flask", "express",
        "node.js", "spring boot", "asp.net", "tailwind", "redux", "graphql", "rest api"
    ],
    "data_storage": [
        "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "sqlite",
        "cassandra", "dynamodb", "neo4j", "kafka", "rabbitmq"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "git", "terraform",
        "linux", "nginx", "prometheus", "grafana"
    ],
    "ai_ml": [
        "machine learning", "deep learning", "langchain", "langgraph", "llm", "rag",
        "pytorch", "tensorflow", "scikit-learn", "nlp", "computer vision", "pandas", "numpy"
    ],
    "practices": [
        "unit testing", "system design", "microservices", "agile", "tdd",
        "concurrency", "asyncio", "security", "accessibility", "wcag"
    ]
}

ALL_KNOWN_SKILLS: Set[str] = {
    skill for group in TECH_LEXICON.values() for skill in group
}

class CandidateJobAnalysisAgent:
    """
    Agent 1: Candidate & Job Analysis Agent.
    Combines resume extraction analysis and job requirement parsing into a single unified agent.
    Extracts candidate skills, experience level, job criteria, identifies skill gaps,
    and produces structured output for the Interview Planner.
    """

    @classmethod
    def _extract_skills_from_text(cls, text: str) -> List[str]:
        """Extracts recognized technical skills and tools from plaintext using regex word boundaries."""
        lower_text = text.lower()
        found_skills = []
        for skill in ALL_KNOWN_SKILLS:
            # Handle multi-word vs single-word boundary checks
            escaped = re.escape(skill)
            if re.search(r'(?:\b|\A)' + escaped + r'(?:\b|\Z)', lower_text):
                found_skills.append(skill.title() if len(skill) > 3 and not skill.isupper() else skill.upper())
        return sorted(list(set(found_skills)))

    @classmethod
    def _detect_experience_level(cls, text: str) -> str:
        """Determines approximate candidate experience level from keywords and years."""
        lower = text.lower()
        if re.search(r'\b(senior|lead|principal|staff|architect|8\+|10\+|7\+ years)\b', lower):
            return "senior"
        elif re.search(r'\b(entry|junior|graduate|intern|internship|freshman|sophomore|0-1 years|0-2 years)\b', lower):
            return "entry"
        return "mid"

    @classmethod
    def _detect_projects(cls, text: str) -> List[str]:
        """Extracts key project names or role headings from the resume text."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        projects = []
        capture = False
        for line in lines:
            if re.search(r'^(projects|experience|work history|employment|key projects)', line, re.IGNORECASE):
                capture = True
                continue
            if capture:
                if re.search(r'^(education|skills|certifications|awards|interests|summary)', line, re.IGNORECASE):
                    break
                # Lines that look like project titles or role headers
                if len(line) < 80 and not line.startswith("-") and not line.startswith("•"):
                    clean_title = re.sub(r'[\*\#\_\|]', '', line).strip()
                    if clean_title and len(clean_title) > 5 and clean_title not in projects:
                        projects.append(clean_title)
                        if len(projects) >= 4:
                            break
        return projects or ["Technical Software Project", "Core Domain Implementation"]

    @classmethod
    def heuristic_analysis(
        cls,
        resume_text: str,
        job_description: str,
        job_title: str = ""
    ) -> CandidateJobAnalysisSchema:
        """
        Deterministic, offline-resilient heuristic analysis.
        Runs when LLM is unavailable or when LLM API keys are not configured.
        """
        # Extract candidate skills
        candidate_skills = cls._extract_skills_from_text(resume_text)
        if not candidate_skills:
            candidate_skills = ["Software Engineering", "Problem Solving", "Object-Oriented Programming"]

        # Extract job required skills
        combined_jd = f"{job_title} {job_description}"
        jd_skills = cls._extract_skills_from_text(combined_jd)
        if not jd_skills:
            jd_skills = ["Software Engineering", "REST APIs", "Testing"]

        candidate_lower = {s.lower() for s in candidate_skills}
        jd_lower = {s.lower() for s in jd_skills}

        matching = [s for s in jd_skills if s.lower() in candidate_lower]
        missing = [s for s in jd_skills if s.lower() not in candidate_lower]

        # Calculate matching percentage
        total_jd = len(jd_skills)
        match_score = round((len(matching) / max(1, total_jd)) * 100, 1)

        exp_level = cls._detect_experience_level(resume_text)
        projects = cls._detect_projects(resume_text)

        # Generate focus areas based on matching and missing skills
        focus_areas = []
        if matching:
            focus_areas.append(f"In-depth discussion on {matching[0]} and applied projects")
        if missing:
            focus_areas.append(f"Assessment of foundational readiness in {missing[0]}")
        focus_areas.append("System architecture and clean code maintainability")
        focus_areas.append("Error handling, testing, and debugging strategies")

        summary = (
            f"Candidate profile demonstrates hands-on experience in {', '.join(candidate_skills[:4])}. "
            f"Evaluated for the {job_title or 'target technical'} role, showing strong alignment in "
            f"{', '.join(matching[:3]) if matching else 'core development fundamentals'}."
        )

        return CandidateJobAnalysisSchema(
            candidate_summary=summary,
            skills=candidate_skills,
            experience_level=exp_level,
            key_projects_or_roles=projects[:4],
            job_requirements=JobCriteria(
                required_skills=jd_skills,
                preferred_skills=jd_skills[3:],
                competencies=[
                    "Core Programming & Language Internals",
                    "System Architecture & API Design",
                    "Reliability & Error Handling"
                ],
                seniority_level=cls._detect_experience_level(combined_jd)
            ),
            skill_match_analysis=SkillMatchAnalysis(
                matching_skills=matching,
                missing_or_gap_skills=missing,
                match_score=min(100.0, max(20.0, match_score if matching else 50.0))
            ),
            recommended_focus_areas=focus_areas[:4],
            raw_analysis_notes="Generated via deterministic heuristic analysis (fallback mode)."
        )

    @classmethod
    async def analyze(
        cls,
        resume_text: str,
        job_description: str,
        job_title: str = ""
    ) -> Dict[str, Any]:
        """
        Executes unified candidate and job analysis.
        Uses Gemini LLM with structured JSON output if API key is configured;
        gracefully falls back to deterministic heuristic analysis if unavailable.
        """
        api_key = settings.LLM_API_KEY
        if not api_key:
            # Check standard environment variable fallback
            import os
            api_key = os.environ.get("GEMINI_API_KEY", "")

        # If no LLM key is configured, immediately run deterministic heuristic analysis
        if not api_key or api_key == "your-llm-api-key-here":
            logger.info("CandidateJobAnalysisAgent: No LLM API key detected; utilizing deterministic heuristic analysis.")
            result_schema = cls.heuristic_analysis(resume_text, job_description, job_title)
            return {
                "analysis": result_schema,
                "source": "heuristic_fallback"
            }

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            prompt = f"""You are the Candidate & Job Analysis Agent for AccessHire AI, an accessible mock interview platform.
Analyze the following candidate resume and job description.

Candidate Resume Text:
\"\"\"
{resume_text[:4000]}
\"\"\"

Target Job Title: {job_title}
Job Description Text:
\"\"\"
{job_description[:3000]}
\"\"\"

Instructions:
1. Extract candidate technical skills, estimated experience level (entry, mid, or senior), and past projects/roles.
2. Extract required skills and core competency areas from the job description.
3. Compare the candidate skills against the job requirements to determine matching skills, missing skill gaps, and a match score percentage (0-100).
4. Recommend 3 to 5 clear focus areas to assess during the mock interview.
5. Provide a constructive 2-3 sentence candidate summary.
"""

            response = client.models.generate_content(
                model=settings.LLM_MODEL or "gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=CandidateJobAnalysisSchema,
                    temperature=0.2,
                ),
            )

            if response.text:
                parsed_json = json.loads(response.text)
                analysis_obj = CandidateJobAnalysisSchema(**parsed_json)
                return {
                    "analysis": analysis_obj,
                    "source": "llm"
                }
            else:
                raise ValueError("Empty response received from LLM.")

        except Exception as exc:
            logger.warning(
                "CandidateJobAnalysisAgent: LLM execution failed (%s); engaging heuristic fallback.", exc
            )
            fallback_schema = cls.heuristic_analysis(resume_text, job_description, job_title)
            return {
                "analysis": fallback_schema,
                "source": "heuristic_fallback"
            }
