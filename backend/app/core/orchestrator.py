import logging
from typing import Dict, Any, Optional
from app.schemas.analysis import CandidateJobAnalysisSchema
from app.schemas.planner import InterviewPlanSchema
from app.schemas.state import InterviewState, TurnEvaluation

logger = logging.getLogger("accesshire.orchestrator")

class CentralOrchestrator:
    """
    Central Orchestrator & Supervisor Component:
    - Coordinates execution of multi-agent tasks (Agent 1, Agent 2, etc.)
    - Manages lifecycle state transitions via the centralized InterviewStateEngine
    - Monitors agent outputs and validates structured Pydantic responses
    - Implements retries and controlled fallback heuristics
    - Logs telemetry for system observability
    """

    def __init__(self):
        self.logger = logger

    async def execute_task_with_resilience(
        self,
        task_name: str,
        agent_callable,
        state_payload: Dict[str, Any],
        max_retries: int = 2,
        fallback_handler: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes an agent task with error trapping, retries, and fallback to ensure
        one failed LLM call does not crash the interview session.
        """
        self.logger.info("CentralOrchestrator: Dispatching task '%s'", task_name)
        attempts = 0
        while attempts <= max_retries:
            try:
                attempts += 1
                result = await agent_callable(state_payload)
                self.logger.info("CentralOrchestrator: Task '%s' completed successfully.", task_name)
                return result
            except Exception as exc:
                self.logger.error(
                    "CentralOrchestrator: Error executing '%s' (Attempt %d/%d): %s",
                    task_name, attempts, max_retries + 1, exc
                )
                if attempts > max_retries:
                    if fallback_handler:
                        self.logger.warning("CentralOrchestrator: Triggering fallback handler for '%s'", task_name)
                        return await fallback_handler(state_payload)
                    raise exc

    async def run_candidate_job_analysis(
        self,
        resume_text: str,
        job_description: str,
        job_title: str = ""
    ) -> Dict[str, Any]:
        """Runs Agent 1 (Candidate & Job Analysis) with orchestrator resilience and fallbacks."""
        async def agent_task(payload):
            from app.agents.candidate_job_analysis_agent import CandidateJobAnalysisAgent
            return await CandidateJobAnalysisAgent.analyze(
                resume_text=payload["resume_text"],
                job_description=payload["job_description"],
                job_title=payload.get("job_title", "")
            )

        async def fallback_task(payload):
            from app.agents.candidate_job_analysis_agent import CandidateJobAnalysisAgent
            schema = CandidateJobAnalysisAgent.heuristic_analysis(
                resume_text=payload["resume_text"],
                job_description=payload["job_description"],
                job_title=payload.get("job_title", "")
            )
            return {"analysis": schema, "source": "heuristic_fallback"}

        payload = {
            "resume_text": resume_text,
            "job_description": job_description,
            "job_title": job_title
        }

        return await self.execute_task_with_resilience(
            task_name="candidate_job_analysis",
            agent_callable=agent_task,
            state_payload=payload,
            max_retries=1,
            fallback_handler=fallback_task
        )

    async def run_interview_planner(
        self,
        job_title: str,
        job_description: str,
        target_question_count: int = 3,
        analysis: Optional[CandidateJobAnalysisSchema] = None,
        simplified_language: bool = False,
        extended_time: bool = True,
        voice_enabled: bool = False,
    ) -> Dict[str, Any]:
        """Runs Agent 2 (Interview Planner Agent) with orchestrator resilience and fallbacks."""
        async def agent_task(payload):
            from app.agents.interview_planner_agent import InterviewPlannerAgent
            return await InterviewPlannerAgent.plan(
                job_title=payload["job_title"],
                job_description=payload["job_description"],
                target_question_count=payload["target_question_count"],
                analysis=payload.get("analysis"),
                simplified_language=payload.get("simplified_language", False),
                extended_time=payload.get("extended_time", True),
                voice_enabled=payload.get("voice_enabled", False),
            )

        async def fallback_task(payload):
            from app.agents.interview_planner_agent import InterviewPlannerAgent
            schema = InterviewPlannerAgent.heuristic_plan(
                job_title=payload["job_title"],
                job_description=payload["job_description"],
                target_question_count=payload["target_question_count"],
                analysis=payload.get("analysis"),
                simplified_language=payload.get("simplified_language", False),
                extended_time=payload.get("extended_time", True),
                voice_enabled=payload.get("voice_enabled", False),
            )
            return {"plan": schema, "source": "heuristic_fallback"}

        payload = {
            "job_title": job_title,
            "job_description": job_description,
            "target_question_count": target_question_count,
            "analysis": analysis,
            "simplified_language": simplified_language,
            "extended_time": extended_time,
            "voice_enabled": voice_enabled,
        }

        return await self.execute_task_with_resilience(
            task_name="interview_planner",
            agent_callable=agent_task,
            state_payload=payload,
            max_retries=1,
            fallback_handler=fallback_task
        )

    def initialize_interview_state(
        self,
        session_id: str,
        user_id: str,
        job_title: str,
        job_description: str,
        resume_id: Optional[str] = None,
        plan: Optional[InterviewPlanSchema] = None,
        questions: Optional[list] = None,
        accessibility_settings: Optional[Dict[str, Any]] = None,
        storage_mode: str = "mongodb",
    ) -> InterviewState:
        """Initializes standardized interview state using the InterviewStateEngine."""
        from app.services.state_engine import InterviewStateEngine
        self.logger.info("CentralOrchestrator: Initializing interview state for session '%s'", session_id)
        return InterviewStateEngine.initialize_state(
            session_id=session_id,
            user_id=user_id,
            job_title=job_title,
            job_description=job_description,
            resume_id=resume_id,
            plan=plan,
            questions=questions,
            accessibility_settings=accessibility_settings,
            storage_mode=storage_mode,
        )

    def update_state_on_answer(
        self,
        state: InterviewState,
        question_id: Optional[str],
        answer_text: str,
        modality: str = "text",
        duration_seconds: Optional[int] = None,
        evaluation: Optional[TurnEvaluation] = None,
    ) -> InterviewState:
        """Dispatches answer recording and state advancement to the InterviewStateEngine."""
        from app.services.state_engine import InterviewStateEngine
        self.logger.info("CentralOrchestrator: Updating state for session '%s' on turn %d", state.session_id, state.current_turn)
        return InterviewStateEngine.record_answer_and_progress(
            state=state,
            question_id=question_id,
            answer_text=answer_text,
            modality=modality,
            duration_seconds=duration_seconds,
            evaluation=evaluation,
        )

    def end_state_early(self, state: InterviewState) -> InterviewState:
        """Dispatches early termination to the InterviewStateEngine."""
        from app.services.state_engine import InterviewStateEngine
        self.logger.info("CentralOrchestrator: Ending state early for session '%s'", state.session_id)
        return InterviewStateEngine.end_interview_early(state)

    def evaluate_decision_policy(
        self,
        state: InterviewState,
        plan: Optional[InterviewPlanSchema] = None,
    ) -> Any:
        """
        Executes the Adaptive Decision Policy Agent to select the next interview action
        and applies the decision to the state model.
        """
        from app.agents.decision_policy_agent import DecisionPolicyAgent
        from app.services.state_engine import InterviewStateEngine

        self.logger.info(
            "CentralOrchestrator: Evaluating Decision Policy for session '%s' (turn %d, quota %d)",
            state.session_id, state.current_turn, state.remaining_questions
        )
        decision = DecisionPolicyAgent.decide(state=state, plan=plan)
        self.logger.info(
            "CentralOrchestrator: Decision Policy chosen: %s (Reason: %s)",
            decision.action, decision.reason
        )
        InterviewStateEngine.apply_policy_decision(state, decision)
        return decision

orchestrator = CentralOrchestrator()
