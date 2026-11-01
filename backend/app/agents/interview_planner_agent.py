import json
import logging
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.schemas.analysis import CandidateJobAnalysisSchema
from app.schemas.planner import (
    InterviewPlanSchema,
    PlannedTopicDomain,
    InterviewPlanResponse
)

logger = logging.getLogger("accesshire.agents.interview_planner")

class InterviewPlannerAgent:
    """
    Agent 2: Interview Planner Agent.
    - Determines interview blueprint from Candidate & Job Analysis output (or direct inputs)
    - Allocates topic domains balancing candidate strengths and detected gaps
    - Sets question quotas, topic weights, starting difficulty, and accessibility configurations
    - Supports LLM structured generation via Google Gemini and deterministic heuristic fallback
    """

    @classmethod
    def heuristic_plan(
        cls,
        job_title: str,
        job_description: str,
        target_question_count: int = 3,
        analysis: Optional[CandidateJobAnalysisSchema] = None,
        simplified_language: bool = False,
        extended_time: bool = True,
        voice_enabled: bool = False,
    ) -> InterviewPlanSchema:
        """
        Deterministic heuristic planner ensuring the interview plan is always generated
        without external service reliance or network dependency.
        """
        total_questions = max(1, min(10, target_question_count))
        title_lower = job_title.lower() if job_title else ""
        desc_lower = job_description.lower() if job_description else ""

        # Determine seniority & starting difficulty
        seniority = "mid"
        difficulty = "medium"

        if analysis:
            seniority = analysis.experience_level
            if seniority == "entry":
                difficulty = "easy"
            elif seniority == "senior":
                difficulty = "hard"
            else:
                difficulty = "medium"
        else:
            if any(k in title_lower or k in desc_lower for k in ["junior", "entry", "intern", "associate"]):
                seniority = "entry"
                difficulty = "easy"
            elif any(k in title_lower or k in desc_lower for k in ["senior", "lead", "staff", "principal"]):
                seniority = "senior"
                difficulty = "hard"

        # Accommodations record
        accommodations = []
        if simplified_language:
            accommodations.append("Simplified plain-language question phrasing")
        if extended_time:
            accommodations.append("Extended deliberation and untimed pause tolerance")
        if voice_enabled:
            accommodations.append("Voice modality and speech accommodations")

        # Extract focus topics
        topic_candidates: List[PlannedTopicDomain] = []

        if analysis and analysis.recommended_focus_areas:
            # Plan topics directly aligned with Agent 1 analysis
            for idx, area in enumerate(analysis.recommended_focus_areas[:4], start=1):
                clean_name = area.replace("In-depth discussion on ", "").replace("Assessment of foundational readiness in ", "")
                weight = 1.2 if "foundational" in area.lower() or "depth" in area.lower() else 1.0
                priority = "high" if idx <= 2 else "medium"
                topic_candidates.append(
                    PlannedTopicDomain(
                        id=f"top_{idx}",
                        name=clean_name.capitalize(),
                        category="core_competency" if idx <= 2 else "applied_architecture",
                        priority=priority,
                        weight=weight,
                        allocated_questions=1,
                        sample_question_prompt=f"Can you walk through your practical experience with {clean_name}?",
                        simplified_prompt=f"How have you used {clean_name} in your projects?"
                    )
                )

        if not topic_candidates:
            # Domain-specific heuristic templates
            if "python" in title_lower or "fastapi" in title_lower or "django" in title_lower:
                topic_candidates = [
                    PlannedTopicDomain(
                        id="top_1",
                        name="Python Internals & Asynchronous Flow",
                        category="core_skills",
                        priority="high",
                        weight=1.2,
                        allocated_questions=1,
                        sample_question_prompt="Can you explain how Python asyncio event loops operate and how GIL impact is managed?",
                        simplified_prompt="How does Python handle multiple tasks at the same time using async and threads?"
                    ),
                    PlannedTopicDomain(
                        id="top_2",
                        name="REST API Architecture & Error Handling",
                        category="system_design",
                        priority="high",
                        weight=1.0,
                        allocated_questions=1,
                        sample_question_prompt="How do you structure validation, error handling, and rate limiting in scalable REST APIs?",
                        simplified_prompt="How do you make sure an API handles bad input and high traffic safely?"
                    ),
                    PlannedTopicDomain(
                        id="top_3",
                        name="Database Integration & Persistence",
                        category="data_persistence",
                        priority="medium",
                        weight=1.0,
                        allocated_questions=1,
                        sample_question_prompt="Describe indexing and transaction isolation considerations when querying relational or document databases.",
                        simplified_prompt="How do database indexes help queries run faster and avoid data conflicts?"
                    )
                ]
            elif "react" in title_lower or "frontend" in title_lower or "javascript" in title_lower or "typescript" in title_lower:
                topic_candidates = [
                    PlannedTopicDomain(
                        id="top_1",
                        name="Modern React State & Lifecycle Management",
                        category="core_skills",
                        priority="high",
                        weight=1.2,
                        allocated_questions=1,
                        sample_question_prompt="How does React virtual DOM reconciliation work, and how do you prevent component memory leaks?",
                        simplified_prompt="How does React decide when to re-render, and how do you clean up background events?"
                    ),
                    PlannedTopicDomain(
                        id="top_2",
                        name="Web Accessibility & Inclusive UI Standards",
                        category="accessibility_wcag",
                        priority="high",
                        weight=1.1,
                        allocated_questions=1,
                        sample_question_prompt="What techniques do you employ to guarantee WCAG compliance, screen reader compatibility, and keyboard navigation?",
                        simplified_prompt="What steps make sure a website is fully accessible to people using keyboards and screen readers?"
                    ),
                    PlannedTopicDomain(
                        id="top_3",
                        name="Client-Server Synchronization & Error Resilience",
                        category="system_design",
                        priority="medium",
                        weight=1.0,
                        allocated_questions=1,
                        sample_question_prompt="How do you implement optimistic UI updates and recover cleanly from network disconnects?",
                        simplified_prompt="How should the UI update smoothly when server requests take long or fail?"
                    )
                ]
            else:
                topic_candidates = [
                    PlannedTopicDomain(
                        id="top_1",
                        name=f"{job_title} Core Fundamentals",
                        category="core_skills",
                        priority="high",
                        weight=1.2,
                        allocated_questions=1,
                        sample_question_prompt=f"What are the core technical patterns and principles critical for a {job_title}?",
                        simplified_prompt=f"What are the most important everyday technical skills for a {job_title}?"
                    ),
                    PlannedTopicDomain(
                        id="top_2",
                        name="System Architecture & Scalability",
                        category="system_design",
                        priority="high",
                        weight=1.0,
                        allocated_questions=1,
                        sample_question_prompt="How do you architect modular systems that gracefully scale under increasing throughput?",
                        simplified_prompt="How do you structure code so it can handle more users without slowing down?"
                    ),
                    PlannedTopicDomain(
                        id="top_3",
                        name="Testing, Debugging & Reliability",
                        category="engineering_practices",
                        priority="medium",
                        weight=1.0,
                        allocated_questions=1,
                        sample_question_prompt="Can you describe your methodology for root-cause analysis, unit testing, and deployment verification?",
                        simplified_prompt="How do you find bugs and test your code before shipping it?"
                    )
                ]

        # Allocate questions to topics based on target_question_count
        topic_count = len(topic_candidates)
        base_alloc = total_questions // topic_count
        remainder = total_questions % topic_count

        for i, topic in enumerate(topic_candidates):
            topic.allocated_questions = base_alloc + (1 if i < remainder else 0)

        strategy = (
            f"Evaluates candidate for the {job_title} role at {seniority} seniority starting at {difficulty} difficulty. "
            f"Balances candidate core strengths against detected skill gaps across {len(topic_candidates)} targeted domains."
        )

        return InterviewPlanSchema(
            job_title=job_title,
            target_question_count=total_questions,
            starting_difficulty=difficulty,
            seniority_level=seniority,
            assessment_strategy=strategy,
            planned_topics=topic_candidates,
            accessibility_accommodations_applied=accommodations
        )

    @classmethod
    async def plan(
        cls,
        job_title: str,
        job_description: str,
        target_question_count: int = 3,
        analysis: Optional[CandidateJobAnalysisSchema] = None,
        simplified_language: bool = False,
        extended_time: bool = True,
        voice_enabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Executes Agent 2 (Interview Planner Agent):
        Attempts LLM generation with Gemini structured schema output;
        gracefully engages deterministic heuristic fallback if LLM is unavailable.
        """
        api_key = settings.LLM_API_KEY.strip()
        if not api_key:
            logger.info("InterviewPlannerAgent: No LLM_API_KEY configured; using heuristic planning engine.")
            plan_schema = cls.heuristic_plan(
                job_title=job_title,
                job_description=job_description,
                target_question_count=target_question_count,
                analysis=analysis,
                simplified_language=simplified_language,
                extended_time=extended_time,
                voice_enabled=voice_enabled,
            )
            return {
                "plan": plan_schema,
                "source": "heuristic_fallback"
            }

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            analysis_context = ""
            if analysis:
                analysis_context = f"""
Candidate Summary: {analysis.candidate_summary}
Detected Seniority: {analysis.experience_level}
Matching Skills: {', '.join(analysis.skill_match_analysis.matching_skills)}
Missing Skill Gaps: {', '.join(analysis.skill_match_analysis.missing_or_gap_skills)}
Recommended Focus Areas: {', '.join(analysis.recommended_focus_areas)}
"""

            prompt = f"""You are the Interview Planner Agent (Agent 2) for AccessHire AI, an accessible mock interview platform.
Construct a comprehensive interview blueprint for the following position and candidate profile.

Target Job Title: {job_title}
Job Description:
\"\"\"
{job_description[:3000]}
\"\"\"

Target Question Count: {target_question_count}
Simplified Language Requested: {simplified_language}
Extended Deliberation Time: {extended_time}
Voice Modality: {voice_enabled}

{analysis_context}

Instructions:
1. Determine the optimal starting difficulty ('easy', 'medium', or 'hard') based on candidate seniority and job requirements.
2. Formulate between 3 and 5 structured assessment topic domains with unique IDs ('top_1', 'top_2', 'top_3', ...), names, categories, and relative weights. You MUST return at least 3 distinct topic domains.
3. Distribute the {target_question_count} total questions across the topic domains so the sum of allocated_questions equals {target_question_count}. Each domain should have at least 1 allocated question unless total questions is smaller than topic count.
4. Provide a realistic sample technical question and a simplified plain-English variant for each domain.
5. Provide a concise 2-3 sentence assessment strategy overview.
"""

            response = client.models.generate_content(
                model=settings.LLM_MODEL or "gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=InterviewPlanSchema,
                    temperature=0.2,
                ),
            )

            if response.text:
                parsed_json = json.loads(response.text)
                plan_obj = InterviewPlanSchema(**parsed_json)
                return {
                    "plan": plan_obj,
                    "source": "llm"
                }
            else:
                raise ValueError("Empty response received from LLM.")

        except Exception as exc:
            logger.warning(
                "InterviewPlannerAgent: LLM planning execution failed (%s); falling back to heuristic planner.", exc
            )
            plan_schema = cls.heuristic_plan(
                job_title=job_title,
                job_description=job_description,
                target_question_count=target_question_count,
                analysis=analysis,
                simplified_language=simplified_language,
                extended_time=extended_time,
                voice_enabled=voice_enabled,
            )
            return {
                "plan": plan_schema,
                "source": "heuristic_fallback"
            }
