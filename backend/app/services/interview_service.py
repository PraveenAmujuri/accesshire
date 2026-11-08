import uuid
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from app.core.database import db_instance
from app.schemas.interview import (
    InterviewSessionCreate,
    CandidateAnswerSubmit,
    QuestionResponse,
    SubmitAnswerResponse,
    SessionDetailResponse,
    SessionSummaryItem,
    SessionReportResponse,
    TranscriptTurnItem,
)

logger = logging.getLogger("accesshire.interviews")

# In-memory storage fallback when MongoDB is running in offline/disconnected mode
_in_memory_sessions: Dict[str, Dict[str, Any]] = {}

# Session concurrency lock registry to prevent race conditions on simultaneous answer submissions
_session_locks: Dict[str, asyncio.Lock] = {}
_locks_guard = asyncio.Lock()

class InterviewService:
    """
    Core Interview Service:
    - Handles interview session creation, persistence, state tracking, and progression.
    - Persists to MongoDB when available; seamlessly falls back to memory repository in offline/test mode.
    - Strictly checks session ownership against the authenticated user on every operation.
    - Protects against concurrent submissions using per-session async locks and status checks.
    - Exposes transparent storage mode information (mongodb vs in_memory_fallback).
    """

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def get_storage_mode(cls, session: Optional[Dict[str, Any]] = None) -> str:
        """Returns the active storage backend identifier for a session or the system."""
        if session and session.get("storage_mode"):
            return session["storage_mode"]
        if db_instance.client is not None and db_instance.db is not None:
            return "mongodb"
        return "in_memory_fallback"

    @classmethod
    async def _get_session_lock(cls, session_id: str) -> asyncio.Lock:
        """Acquires or creates an async lock for the given session to prevent race conditions."""
        async with _locks_guard:
            if session_id not in _session_locks:
                _session_locks[session_id] = asyncio.Lock()
            return _session_locks[session_id]

    @classmethod
    def _verify_ownership(cls, session: Dict[str, Any], user_id: str) -> None:
        """Verifies that the session belongs to the requesting authenticated user."""
        session_owner = session.get("user_id")
        if session_owner != user_id:
            logger.warning(
                "Access denied: User '%s' attempted to access session '%s' owned by '%s'",
                user_id, session.get("session_id"), session_owner
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You do not have permission to access this interview session."
            )

    @classmethod
    def _generate_baseline_questions(
        cls,
        job_title: str,
        job_description: str,
        target_count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generates baseline questions for the interview flow based on job role.
        Dedicated integration point for Agent 1, Agent 2, and Agent 4 in subsequent phases.
        """
        title_lower = job_title.lower()
        desc_lower = job_description.lower()

        if "python" in title_lower or "python" in desc_lower:
            topics = [
                {
                    "topic_id": "top_python_core",
                    "topic_name": "Python Fundamentals & Memory",
                    "question": "Can you explain how the Python Global Interpreter Lock (GIL) affects multi-threaded CPU-bound tasks versus I/O-bound tasks?",
                    "simplified": "What does Python's GIL do, and how is using threads different for CPU tasks versus network/file tasks?",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_python_arch",
                    "topic_name": "Asynchronous Programming & FastAPIs",
                    "question": "How do Python asyncio event loops handle non-blocking concurrent requests, and when would you use background tasks versus Celery?",
                    "simplified": "How does async/await allow a server to handle many users at once without freezing?",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_python_design",
                    "topic_name": "API Reliability & Error Handling",
                    "question": "Describe how you would implement structured validation, exception handling, and rate limiting in a production REST service.",
                    "simplified": "How do you make sure an API safely handles bad user input without crashing?",
                    "difficulty": "medium",
                },
            ]
        elif "react" in title_lower or "frontend" in title_lower or "web" in title_lower:
            topics = [
                {
                    "topic_id": "top_frontend_state",
                    "topic_name": "Frontend State & Lifecycle",
                    "question": "How does React manage the virtual DOM reconciliation process, and how do hooks like useEffect prevent memory leaks during component unmounting?",
                    "simplified": "How does React know when to update the screen, and how do you clean up background tasks when a page changes?",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_frontend_perf",
                    "topic_name": "Web Accessibility & Rendering Performance",
                    "question": "What techniques do you employ to ensure high accessibility (WCAG compliance, screen reader support, keyboard navigation) in complex UI components?",
                    "simplified": "How do you make sure a website can be easily used by people using keyboards or screen readers?",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_frontend_arch",
                    "topic_name": "Client-Server Data Synchronization",
                    "question": "How do you design robust client-side error boundaries and handle optimistic UI updates during slow or failing network connections?",
                    "simplified": "What should a website do when the internet is slow or a server request fails?",
                    "difficulty": "medium",
                },
            ]
        else:
            topics = [
                {
                    "topic_id": "top_general_core",
                    "topic_name": "Software Engineering Fundamentals",
                    "question": f"Given your interest in the {job_title} role, could you describe a challenging technical problem you solved and your trade-off analysis?",
                    "simplified": "Tell me about a difficult technical problem you worked on and the choices you made to solve it.",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_general_arch",
                    "topic_name": "System Architecture & Quality",
                    "question": "How do you ensure code maintainability, test coverage, and modularity when developing scalable services for this domain?",
                    "simplified": "How do you write and organize code so that other engineers can test and update it easily?",
                    "difficulty": "medium",
                },
                {
                    "topic_id": "top_general_collab",
                    "topic_name": "Problem Solving & Delivery",
                    "question": "When faced with conflicting technical requirements or ambiguous specifications from stakeholders, how do you clarify requirements and proceed?",
                    "simplified": "What steps do you take when a project requirement is unclear or conflicting?",
                    "difficulty": "medium",
                },
            ]

        selected_topics = topics[:max(1, min(target_count, len(topics)))]

        questions = []
        for idx, item in enumerate(selected_topics, start=1):
            questions.append({
                "question_id": f"q_{idx}_{uuid.uuid4().hex[:6]}",
                "turn_index": idx,
                "topic_id": item["topic_id"],
                "topic_name": item["topic_name"],
                "question_text": item["question"],
                "simplified_question_text": item["simplified"],
                "difficulty": item["difficulty"],
                "status": "pending",
                "candidate_answer": None,
                "answered_at": None,
            })

        return questions

    @classmethod
    async def _save_session(cls, session: Dict[str, Any]) -> str:
        """Persists the session to MongoDB or the memory repository and returns the storage mode used."""
        session["updated_at"] = cls._now_iso()
        db = db_instance.db
        if db is not None:
            try:
                session_to_save = dict(session)
                session_to_save["storage_mode"] = "mongodb"
                await db.interview_sessions.replace_one(
                    {"session_id": session["session_id"]},
                    session_to_save,
                    upsert=True
                )
                session["storage_mode"] = "mongodb"
                return "mongodb"
            except Exception as exc:
                logger.warning("MongoDB write failed (%s); falling back to in-memory store.", exc)

        session["storage_mode"] = "in_memory_fallback"
        _in_memory_sessions[session["session_id"]] = session
        return "in_memory_fallback"

    @classmethod
    async def _find_session(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a session from MongoDB or the in-memory fallback store."""
        db = db_instance.db
        if db is not None:
            try:
                doc = await db.interview_sessions.find_one({"session_id": session_id})
                if doc:
                    doc.pop("_id", None)
                    doc["storage_mode"] = doc.get("storage_mode", "mongodb")
                    return doc
            except Exception as exc:
                logger.warning("MongoDB read failed (%s); reading from in-memory store.", exc)

        session = _in_memory_sessions.get(session_id)
        if session:
            session["storage_mode"] = "in_memory_fallback"
        return session

    @classmethod
    async def create_session(
        cls,
        payload: InterviewSessionCreate,
        user_id: str
    ) -> SessionDetailResponse:
        """Initializes a new interview session dynamically using the Interview Planner Agent (Agent 2)."""
        session_id = f"sess_{uuid.uuid4().hex[:10]}"
        now = cls._now_iso()

        target_count = max(1, min(payload.target_question_count, 10))

        # Dynamically execute Interview Planner Agent (Agent 2)
        plan = None
        try:
            from app.agents.interview_planner_agent import InterviewPlannerAgent
            from app.services.resume_service import ResumeService
            from app.core.orchestrator import orchestrator

            analysis_schema = None
            if payload.resume_id:
                resume_text = await ResumeService.get_resume_text(payload.resume_id, user_id=user_id)
                if resume_text:
                    try:
                        analysis_res = await orchestrator.run_candidate_job_analysis(
                            resume_text=resume_text,
                            job_description=payload.job_description,
                            job_title=payload.job_title
                        )
                        analysis_schema = analysis_res.get("analysis")
                    except Exception:
                        analysis_schema = None

            plan_res = await orchestrator.run_interview_planner(
                job_title=payload.job_title,
                job_description=payload.job_description,
                target_question_count=target_count,
                analysis=analysis_schema,
                simplified_language=payload.simplified_language,
                extended_time=payload.extended_time,
                voice_enabled=payload.voice_enabled
            )
            plan = plan_res.get("plan")
            
            questions = []
            turn_idx = 1
            if plan and plan.planned_topics:
                for domain in plan.planned_topics:
                    for _ in range(domain.allocated_questions):
                        if turn_idx > target_count:
                            break
                        questions.append({
                            "question_id": f"q_{turn_idx}_{uuid.uuid4().hex[:6]}",
                            "turn_index": turn_idx,
                            "topic_id": domain.id,
                            "topic_name": domain.name,
                            "question_text": domain.sample_question_prompt or f"Can you explain your experience in {domain.name}?",
                            "simplified_question_text": domain.simplified_prompt or f"How have you worked with {domain.name}?",
                            "difficulty": plan.starting_difficulty,
                            "status": "pending",
                            "candidate_answer": None,
                            "answered_at": None,
                        })
                        turn_idx += 1
            if not questions:
                questions = cls._generate_baseline_questions(
                    job_title=payload.job_title,
                    job_description=payload.job_description,
                    target_count=target_count
                )
        except Exception as exc:
            logger.warning("Dynamic planner failed during create_session (%s); using baseline generation.", exc)
            questions = cls._generate_baseline_questions(
                job_title=payload.job_title,
                job_description=payload.job_description,
                target_count=target_count
            )

        # Initialize formal InterviewState via Orchestrator State Engine
        from app.core.orchestrator import orchestrator
        initial_state = orchestrator.initialize_interview_state(
            session_id=session_id,
            user_id=user_id,
            job_title=payload.job_title,
            job_description=payload.job_description,
            resume_id=payload.resume_id,
            plan=plan,
            questions=questions,
            accessibility_settings={
                "simplified_language": payload.simplified_language,
                "voice_enabled": payload.voice_enabled,
                "extended_time": payload.extended_time,
            },
            storage_mode="mongodb"
        )

        session_doc = {
            "session_id": session_id,
            "user_id": user_id,
            "job_title": initial_state.job_title,
            "job_description": initial_state.job_description,
            "resume_id": payload.resume_id,
            "status": initial_state.status,
            "current_turn": initial_state.current_turn,
            "total_questions": initial_state.total_questions,
            "remaining_questions": initial_state.remaining_questions,
            "current_topic_id": initial_state.current_topic_id,
            "current_topic_name": initial_state.current_topic_name,
            "current_difficulty": initial_state.current_difficulty,
            "accessibility_settings": {
                "simplified_language": payload.simplified_language,
                "voice_enabled": payload.voice_enabled,
                "extended_time": payload.extended_time,
            },
            "questions": questions,
            "interview_state": initial_state.model_dump(),
            "created_at": now,
            "updated_at": now,
            "completed_at": None,
        }

        storage_mode = await cls._save_session(session_doc)
        initial_state.storage_mode = storage_mode
        session_doc["interview_state"]["storage_mode"] = storage_mode
        await cls._save_session(session_doc)

        logger.info(
            "Created interview session %s for user %s with %d questions (storage: %s)",
            session_id, user_id, len(questions), storage_mode
        )

        return SessionDetailResponse(
            session_id=session_id,
            user_id=user_id,
            job_title=session_doc["job_title"],
            job_description=session_doc["job_description"],
            status=session_doc["status"],
            current_turn=session_doc["current_turn"],
            total_questions=session_doc["total_questions"],
            remaining_questions=session_doc.get("remaining_questions", len(questions)),
            current_topic_id=session_doc.get("current_topic_id"),
            current_topic_name=session_doc.get("current_topic_name"),
            current_difficulty=session_doc.get("current_difficulty"),
            accessibility_settings=session_doc["accessibility_settings"],
            created_at=now,
            updated_at=now,
            is_completed=False,
            storage_mode=storage_mode,
        )

    @classmethod
    async def get_session(cls, session_id: str, user_id: str) -> SessionDetailResponse:
        """Fetches session metadata with ownership verification."""
        session = await cls._find_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{session_id}' not found."
            )

        cls._verify_ownership(session, user_id)

        is_completed = session["status"] == "completed" or session["current_turn"] > session["total_questions"]
        state_dict = session.get("interview_state", {})
        remaining_q = state_dict.get("remaining_questions", max(0, session["total_questions"] - session["current_turn"] + 1))
        
        return SessionDetailResponse(
            session_id=session["session_id"],
            user_id=session["user_id"],
            job_title=session["job_title"],
            job_description=session["job_description"],
            status=session["status"],
            current_turn=session["current_turn"],
            total_questions=session["total_questions"],
            remaining_questions=remaining_q,
            current_topic_id=session.get("current_topic_id") or state_dict.get("current_topic_id"),
            current_topic_name=session.get("current_topic_name") or state_dict.get("current_topic_name"),
            current_difficulty=session.get("current_difficulty") or state_dict.get("current_difficulty"),
            accessibility_settings=session["accessibility_settings"],
            created_at=session["created_at"],
            updated_at=session["updated_at"],
            is_completed=is_completed,
            storage_mode=cls.get_storage_mode(session),
        )

    @classmethod
    async def get_current_question(cls, session_id: str, user_id: str) -> QuestionResponse:
        """Retrieves active question for the current turn with ownership verification."""
        session = await cls._find_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{session_id}' not found."
            )

        cls._verify_ownership(session, user_id)

        if session["status"] == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interview session has already been completed."
            )

        current_turn = session["current_turn"]
        questions = session.get("questions", [])

        matched_q = next((q for q in questions if q["turn_index"] == current_turn), None)
        if not matched_q:
            session["status"] = "completed"
            await cls._save_session(session)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All questions for this session have been answered."
            )

        is_last = current_turn >= len(questions)
        state_dict = session.get("interview_state", {})
        remaining_turns = state_dict.get("remaining_questions", max(0, len(questions) - current_turn + 1))
        active_action = state_dict.get("active_action", "ASK_NEW_QUESTION")
        action_reason = state_dict.get("action_reason")

        return QuestionResponse(
            question_id=matched_q["question_id"],
            turn_index=matched_q["turn_index"],
            total_turns=len(questions),
            remaining_turns=remaining_turns,
            topic_id=matched_q["topic_id"],
            topic_name=matched_q["topic_name"],
            question_text=matched_q["question_text"],
            simplified_question_text=matched_q.get("simplified_question_text"),
            difficulty=matched_q["difficulty"],
            action_type=active_action,
            action_reason=action_reason,
            is_last_question=is_last,
        )

    @classmethod
    async def submit_answer(
        cls,
        session_id: str,
        payload: CandidateAnswerSubmit,
        user_id: str
    ) -> SubmitAnswerResponse:
        """
        Validates, records candidate answer, and transitions the session state to the next question.
        Guards against concurrent submissions, duplicate submissions, and cross-user access.
        """
        trimmed_answer = payload.answer_text.strip()
        if not trimmed_answer:
            raise HTTPException(
                status_code=422,
                detail="Answer text cannot be blank."
            )

        # Acquire concurrency lock for this session
        session_lock = await cls._get_session_lock(session_id)

        async with session_lock:
            # Re-fetch latest session state inside the critical section
            session = await cls._find_session(session_id)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Interview session '{session_id}' not found."
                )

            cls._verify_ownership(session, user_id)

            if session["status"] == "completed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot submit answer: this interview session is already completed."
                )

            current_turn = session["current_turn"]
            questions = session.get("questions", [])

            active_q = next((q for q in questions if q["turn_index"] == current_turn), None)
            if not active_q:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No active question found for turn {current_turn}."
                )

            # Check if submitted question was already answered in this session
            if payload.question_id:
                matching_q = next((q for q in questions if q.get("question_id") == payload.question_id), None)
                if matching_q and matching_q.get("status") == "answered":
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"An answer has already been submitted for question '{payload.question_id}'."
                    )
                if matching_q and matching_q.get("question_id") != active_q["question_id"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Submitted question ID '{payload.question_id}' does not match active question '{active_q['question_id']}'."
                    )

            # Concurrent & duplicate submission guard for active turn
            if active_q["status"] == "answered":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"An answer has already been submitted for turn {current_turn}."
                )

            if payload.question_id and payload.question_id != active_q["question_id"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Submitted question ID '{payload.question_id}' does not match active question '{active_q['question_id']}'."
                )

            # Record answer atomically using Orchestrator InterviewStateEngine
            from app.core.orchestrator import orchestrator
            from app.schemas.state import InterviewState, TurnRecord, TurnEvaluation

            # Load or reconstruct structured InterviewState
            state_dict = session.get("interview_state")
            if state_dict:
                current_state = InterviewState(**state_dict)
            else:
                current_state = orchestrator.initialize_interview_state(
                    session_id=session_id,
                    user_id=user_id,
                    job_title=session["job_title"],
                    job_description=session["job_description"],
                    resume_id=session.get("resume_id"),
                    questions=questions,
                    accessibility_settings=session.get("accessibility_settings"),
                    storage_mode=cls.get_storage_mode(session)
                )

            # Advance state through central orchestrator
            updated_state = orchestrator.update_state_on_answer(
                state=current_state,
                question_id=payload.question_id or active_q["question_id"],
                answer_text=trimmed_answer,
                modality=payload.modality,
                duration_seconds=payload.duration_seconds,
                evaluation=None # Prepared integration point for Evaluation Agent (Agent 5)
            )

            # Evaluate Adaptive Decision Policy Agent (Agent 3)
            policy_decision = orchestrator.evaluate_decision_policy(
                state=updated_state,
                plan=None
            )

            # Synchronize session document with state and policy decision
            active_q["status"] = "answered"
            active_q["candidate_answer"] = trimmed_answer
            active_q["answered_at"] = cls._now_iso()
            active_q["action_decided"] = policy_decision.action

            session["status"] = updated_state.status
            session["current_turn"] = updated_state.current_turn
            session["remaining_questions"] = updated_state.remaining_questions
            session["current_topic_id"] = updated_state.current_topic_id
            session["current_topic_name"] = updated_state.current_topic_name
            session["current_difficulty"] = updated_state.current_difficulty
            session["interview_state"] = updated_state.model_dump()

            if updated_state.is_completed:
                session["completed_at"] = updated_state.completed_at
                await cls._save_session(session)
                logger.info(
                    "Session %s completed. Decision: %s (Reason: %s)",
                    session_id, policy_decision.action, policy_decision.reason
                )
                return SubmitAnswerResponse(
                    session_id=session_id,
                    turn_index=current_turn,
                    status="completed",
                    is_completed=True,
                    next_turn=None,
                    remaining_questions=0,
                    action_decided=policy_decision.action,
                    action_reason=policy_decision.reason,
                    message=f"Final answer recorded. Decision: {policy_decision.action}.",
                    next_question=None,
                )
            else:
                await cls._save_session(session)

                next_q = next((q for q in questions if q["turn_index"] == session["current_turn"]), None)
                next_q_resp = None
                if next_q:
                    next_q_resp = QuestionResponse(
                        question_id=next_q["question_id"],
                        turn_index=next_q["turn_index"],
                        total_turns=len(questions),
                        remaining_turns=updated_state.remaining_questions,
                        topic_id=updated_state.current_topic_id,
                        topic_name=updated_state.current_topic_name,
                        question_text=next_q["question_text"],
                        simplified_question_text=next_q.get("simplified_question_text"),
                        difficulty=updated_state.current_difficulty,
                        action_type=policy_decision.action,
                        action_reason=policy_decision.reason,
                        is_last_question=session["current_turn"] >= len(questions),
                    )

                logger.info(
                    "Session %s advanced to turn %d. Decision: %s (Reason: %s)",
                    session_id, session["current_turn"], policy_decision.action, policy_decision.reason
                )
                return SubmitAnswerResponse(
                    session_id=session_id,
                    turn_index=current_turn,
                    status="in_progress",
                    is_completed=False,
                    next_turn=session["current_turn"],
                    remaining_questions=updated_state.remaining_questions,
                    action_decided=policy_decision.action,
                    action_reason=policy_decision.reason,
                    message=f"Answer recorded. Next action: {policy_decision.action}.",
                    next_question=next_q_resp,
                )

    @classmethod
    async def end_session(cls, session_id: str, user_id: str) -> SessionDetailResponse:
        """Concludes an interview session prematurely with ownership verification."""
        session = await cls._find_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{session_id}' not found."
            )

        cls._verify_ownership(session, user_id)

        # Update state via Central Orchestrator State Engine
        from app.core.orchestrator import orchestrator
        from app.schemas.state import InterviewState

        state_dict = session.get("interview_state")
        if state_dict:
            current_state = InterviewState(**state_dict)
            orchestrator.end_state_early(current_state)
            session["interview_state"] = current_state.model_dump()

        session["status"] = "completed"
        session["remaining_questions"] = 0
        session["completed_at"] = cls._now_iso()
        await cls._save_session(session)
        logger.info("Session %s ended early by user %s.", session_id, user_id)

        return SessionDetailResponse(
            session_id=session["session_id"],
            user_id=session["user_id"],
            job_title=session["job_title"],
            job_description=session["job_description"],
            status="completed",
            current_turn=session["current_turn"],
            total_questions=session["total_questions"],
            remaining_questions=0,
            current_topic_id=session.get("current_topic_id"),
            current_topic_name=session.get("current_topic_name"),
            current_difficulty=session.get("current_difficulty"),
            accessibility_settings=session["accessibility_settings"],
            created_at=session["created_at"],
            updated_at=session["updated_at"],
            is_completed=True,
            storage_mode=cls.get_storage_mode(session),
        )

    @classmethod
    async def list_user_sessions(cls, user_id: str) -> List[SessionSummaryItem]:
        """Lists all interview sessions for the specified user."""
        db = db_instance.db
        results = []

        if db is not None:
            try:
                cursor = db.interview_sessions.find({"user_id": user_id}).sort("created_at", -1)
                async for doc in cursor:
                    results.append(SessionSummaryItem(
                        session_id=doc["session_id"],
                        job_title=doc.get("job_title", "Interview"),
                        status=doc.get("status", "in_progress"),
                        current_turn=doc.get("current_turn", 1),
                        total_questions=doc.get("total_questions", len(doc.get("questions", []))),
                        created_at=doc.get("created_at", ""),
                    ))
                return results
            except Exception as exc:
                logger.warning("MongoDB list failed (%s); using in-memory list.", exc)

        for s in _in_memory_sessions.values():
            if s.get("user_id") == user_id:
                results.append(SessionSummaryItem(
                    session_id=s["session_id"],
                    job_title=s.get("job_title", "Interview"),
                    status=s.get("status", "in_progress"),
                    current_turn=s.get("current_turn", 1),
                    total_questions=s.get("total_questions", len(s.get("questions", []))),
                    created_at=s.get("created_at", ""),
                ))

        results.sort(key=lambda x: x.created_at, reverse=True)
        return results

    @classmethod
    async def get_session_report(cls, session_id: str, user_id: str) -> SessionReportResponse:
        """Retrieves session report and transcript with ownership verification."""
        session = await cls._find_session(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session '{session_id}' not found."
            )

        cls._verify_ownership(session, user_id)

        questions = session.get("questions", [])
        transcript: List[TranscriptTurnItem] = []
        completed_turns = 0

        for q in questions:
            if q["status"] == "answered":
                completed_turns += 1
            transcript.append(TranscriptTurnItem(
                turn_index=q["turn_index"],
                topic_name=q["topic_name"],
                question_text=q["question_text"],
                simplified_question_text=q.get("simplified_question_text"),
                difficulty=q["difficulty"],
                candidate_answer=q.get("candidate_answer"),
                answered_at=q.get("answered_at"),
            ))

        is_completed = session["status"] == "completed"
        return SessionReportResponse(
            session_id=session_id,
            user_id=session["user_id"],
            job_title=session["job_title"],
            status=session["status"],
            total_questions=len(questions),
            completed_turns=completed_turns,
            is_completed=is_completed,
            accessibility_settings=session["accessibility_settings"],
            transcript=transcript,
            created_at=session["created_at"],
            completed_at=session.get("completed_at"),
            storage_mode=cls.get_storage_mode(session),
        )
