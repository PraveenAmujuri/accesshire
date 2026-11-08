import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status

from app.schemas.state import (
    InterviewState,
    TopicMastery,
    TurnRecord,
    TurnEvaluation,
    AccessibilityStateConfig,
)
from app.schemas.planner import InterviewPlanSchema
from app.schemas.interview import QuestionResponse, SubmitAnswerResponse

logger = logging.getLogger("accesshire.state_engine")

class InterviewStateEngine:
    """
    Centralized Interview State Engine:
    - Maintains the formal, validated InterviewState schema
    - Tracks current question, turn index, remaining questions, and candidate progress
    - Tracks topic mastery vectors and difficulty level
    - Atomically updates turn records with candidate answers and evaluation data
    - Enforces consistent state transitions across the interview lifecycle
    """

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def initialize_state(
        cls,
        session_id: str,
        user_id: str,
        job_title: str,
        job_description: str,
        resume_id: Optional[str] = None,
        plan: Optional[InterviewPlanSchema] = None,
        questions: Optional[List[Dict[str, Any]]] = None,
        accessibility_settings: Optional[Dict[str, Any]] = None,
        storage_mode: str = "mongodb",
    ) -> InterviewState:
        """
        Initializes a new centralized InterviewState object from planner blueprint or baseline questions.
        """
        now = cls.now_iso()
        a11y_dict = accessibility_settings or {}
        a11y_config = AccessibilityStateConfig(
            simplified_language=a11y_dict.get("simplified_language", False),
            voice_enabled=a11y_dict.get("voice_enabled", False),
            extended_time=a11y_dict.get("extended_time", True),
            high_contrast=a11y_dict.get("high_contrast", False),
        )

        turns: List[TurnRecord] = []
        topics: Dict[str, TopicMastery] = {}
        starting_diff = "medium"
        seniority = "mid"

        if plan:
            starting_diff = plan.starting_difficulty
            seniority = plan.seniority_level
            for dom in plan.planned_topics:
                topics[dom.id] = TopicMastery(
                    topic_id=dom.id,
                    topic_name=dom.name,
                    target_weight=dom.weight,
                    questions_asked=0,
                    questions_allocated=dom.allocated_questions,
                    cumulative_score=0.0,
                    current_mastery_level=0.0,
                    status="pending"
                )

        if questions:
            for q in questions:
                tid = q.get("topic_id", "top_1")
                tname = q.get("topic_name", "Core Fundamentals")
                if tid not in topics:
                    topics[tid] = TopicMastery(
                        topic_id=tid,
                        topic_name=tname,
                        target_weight=1.0,
                        questions_asked=0,
                        questions_allocated=1,
                        cumulative_score=0.0,
                        current_mastery_level=0.0,
                        status="pending"
                    )
                else:
                    topics[tid].questions_allocated += 1

                turn = TurnRecord(
                    turn_index=q["turn_index"],
                    question_id=q["question_id"],
                    topic_id=tid,
                    topic_name=tname,
                    question_text=q["question_text"],
                    simplified_question_text=q.get("simplified_question_text"),
                    difficulty=q.get("difficulty", starting_diff),
                    status=q.get("status", "pending"),
                    candidate_answer=q.get("candidate_answer"),
                    answered_at=q.get("answered_at"),
                    action_decided="NEW_QUESTION"
                )
                turns.append(turn)

        total_q = len(turns)
        first_tid = turns[0].topic_id if turns else "top_1"
        first_tname = turns[0].topic_name if turns else "Core Fundamentals"
        first_diff = turns[0].difficulty if turns else starting_diff

        # Set first topic status to active
        if first_tid in topics:
            topics[first_tid].status = "active"

        state = InterviewState(
            session_id=session_id,
            user_id=user_id,
            job_title=job_title.strip() or "General Software Engineer",
            job_description=job_description.strip(),
            resume_id=resume_id,
            seniority_level=seniority,
            status="in_progress",
            current_turn=1,
            total_questions=total_q,
            remaining_questions=total_q,
            current_topic_id=first_tid,
            current_topic_name=first_tname,
            current_difficulty=first_diff,
            topics=topics,
            turns=turns,
            answered_count=0,
            cumulative_score=0.0,
            average_score=None,
            active_action="NEW_QUESTION",
            accessibility=a11y_config,
            created_at=now,
            updated_at=now,
            completed_at=None,
            is_completed=False,
            storage_mode=storage_mode,
        )

        return state

    @classmethod
    def get_active_turn(cls, state: InterviewState) -> Optional[TurnRecord]:
        """Returns the TurnRecord corresponding to state.current_turn."""
        for turn in state.turns:
            if turn.turn_index == state.current_turn:
                return turn
        return None

    @classmethod
    def record_answer_and_progress(
        cls,
        state: InterviewState,
        question_id: Optional[str],
        answer_text: str,
        modality: str = "text",
        duration_seconds: Optional[int] = None,
        evaluation: Optional[TurnEvaluation] = None,
    ) -> InterviewState:
        """
        Records candidate answer for the current active turn, validates question matching,
        updates topic mastery statistics, updates remaining questions count,
        and advances current_turn or marks the session completed.
        """
        if state.status == "completed" or state.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot submit answer: this interview session is already completed."
            )

        active_turn = cls.get_active_turn(state)
        if not active_turn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No active question found for turn {state.current_turn}."
            )

        # Validate question ID if provided
        if question_id and question_id != active_turn.question_id:
            # Check if attempting to answer an already answered turn
            existing_match = next((t for t in state.turns if t.question_id == question_id), None)
            if existing_match and existing_match.status == "answered":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"An answer has already been submitted for question '{question_id}'."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Submitted question ID '{question_id}' does not match active question '{active_turn.question_id}'."
            )

        if active_turn.status == "answered":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An answer has already been submitted for turn {state.current_turn}."
            )

        now = cls.now_iso()
        active_turn.status = "answered"
        active_turn.candidate_answer = answer_text.strip()
        active_turn.answered_at = now
        active_turn.duration_seconds = duration_seconds
        active_turn.evaluation = evaluation

        # Update topic mastery metrics
        tid = active_turn.topic_id
        if tid in state.topics:
            topic_record = state.topics[tid]
            topic_record.questions_asked += 1
            if evaluation and evaluation.overall_turn_score is not None:
                topic_record.cumulative_score += evaluation.overall_turn_score
                topic_record.current_mastery_level = min(1.0, max(0.0, topic_record.cumulative_score / max(1, topic_record.questions_asked * 100)))
                if topic_record.current_mastery_level >= 0.75:
                    topic_record.status = "mastered"
                elif topic_record.current_mastery_level < 0.4:
                    topic_record.status = "deficiency_detected"
                else:
                    topic_record.status = "active"

        # Update aggregated metrics
        state.answered_count += 1
        state.remaining_questions = max(0, state.total_questions - state.answered_count)
        if evaluation and evaluation.overall_turn_score is not None:
            state.cumulative_score += evaluation.overall_turn_score
            state.average_score = round(state.cumulative_score / state.answered_count, 1)

        state.updated_at = now

        # Check if interview is completed
        if state.answered_count >= state.total_questions or state.current_turn >= state.total_questions:
            state.status = "completed"
            state.is_completed = True
            state.completed_at = now
            state.active_action = "END_INTERVIEW"
            logger.info("InterviewStateEngine: Session %s completed all %d turns.", state.session_id, state.total_questions)
        else:
            state.current_turn += 1
            next_turn = cls.get_active_turn(state)
            if next_turn:
                state.current_topic_id = next_turn.topic_id
                state.current_topic_name = next_turn.topic_name
                state.current_difficulty = next_turn.difficulty
                if next_turn.topic_id in state.topics and state.topics[next_turn.topic_id].status == "pending":
                    state.topics[next_turn.topic_id].status = "active"
            state.active_action = "NEW_QUESTION"
            logger.info("InterviewStateEngine: Session %s advanced to turn %d (%d remaining).", state.session_id, state.current_turn, state.remaining_questions)

        return state

    @classmethod
    def apply_policy_decision(
        cls,
        state: InterviewState,
        decision: Any,
    ) -> InterviewState:
        """
        Applies a PolicyDecision to the state, updating current difficulty, target topic,
        active action, and transparent explanation reasoning.
        """
        state.active_action = decision.action
        state.action_reason = decision.reason
        state.current_topic_id = decision.target_topic_id
        state.current_topic_name = decision.target_topic_name
        state.current_difficulty = decision.target_difficulty
        if decision.is_terminal:
            state.status = "completed"
            state.is_completed = True
            state.remaining_questions = 0
            if not state.completed_at:
                state.completed_at = cls.now_iso()
        return state

    @classmethod
    def end_interview_early(cls, state: InterviewState) -> InterviewState:
        """Concludes the interview state immediately upon candidate request."""
        now = cls.now_iso()
        state.status = "completed"
        state.is_completed = True
        state.completed_at = now
        state.updated_at = now
        state.active_action = "END_INTERVIEW"
        state.remaining_questions = 0
        logger.info("InterviewStateEngine: Session %s ended early.", state.session_id)
        return state
