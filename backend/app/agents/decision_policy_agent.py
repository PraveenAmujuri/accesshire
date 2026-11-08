import logging
from typing import Optional, Dict, Any, List
from app.schemas.state import InterviewState, TurnRecord, TurnEvaluation, TopicMastery
from app.schemas.planner import InterviewPlanSchema
from app.schemas.policy import PolicyDecision, PolicyActionType

logger = logging.getLogger("accesshire.agents.decision_policy")

class DecisionPolicyAgent:
    """
    Adaptive Decision Policy Agent (Core Research Contribution):
    Evaluates candidate interview trajectory, topic mastery vectors, turn scores,
    quota bounds, and accessibility settings to determine the optimal next action.
    
    Supported Actions:
    - ASK_NEW_QUESTION: Candidate answered adequately and quota allows proceeding to next question on the topic/plan.
    - ASK_FOLLOW_UP: Candidate answer is partial or superficial (e.g. depth score < 60) and quota permits probing.
    - INCREASE_DIFFICULTY: Candidate demonstrated strong mastery (e.g. score >= 85) on current difficulty and quota remains.
    - DECREASE_DIFFICULTY: Candidate struggled significantly (e.g. score < 45) on 'medium' or 'hard' and needs a confidence-building ramp.
    - CHANGE_TOPIC: Current topic quota exhausted or topic mastery achieved, advancing to next unaddressed planned domain.
    - CLARIFY_QUESTION: Candidate indicates confusion, requests rephrasing, or answer is off-topic with high confusion cues.
    - CONTINUE_INTERVIEW: Standard progression when current topic has remaining quota and difficulty remains calibrated.
    - END_INTERVIEW: All question quotas exhausted or completion conditions met.
    """

    DIFFICULTY_LADDER = ["easy", "medium", "hard"]

    @classmethod
    def _get_higher_difficulty(cls, current: str) -> str:
        if current == "easy":
            return "medium"
        return "hard"

    @classmethod
    def _get_lower_difficulty(cls, current: str) -> str:
        if current == "hard":
            return "medium"
        return "easy"

    @classmethod
    def _detect_clarification_intent(cls, answer_text: str) -> bool:
        """
        Detects if the candidate's response is an explicit clarification or confusion request
        rather than a technical answer attempt.
        """
        text = answer_text.strip().lower()
        if len(text) < 5:
            return False
        
        clarification_phrases = [
            "could you clarify",
            "can you clarify",
            "what do you mean by",
            "i don't understand the question",
            "i do not understand the question",
            "can you rephrase",
            "could you rephrase",
            "could you explain what you mean",
            "please clarify",
            "repeat the question",
            "i am confused by the question",
            "i'm confused by the question",
            "not sure what is being asked",
            "can you provide more context on the question",
        ]
        return any(phrase in text for phrase in clarification_phrases)

    @classmethod
    def decide(
        cls,
        state: InterviewState,
        plan: Optional[InterviewPlanSchema] = None,
    ) -> PolicyDecision:
        """
        Evaluates the current state, latest answer & evaluation, and selects a deterministic,
        transparent policy decision with clear reasoning.
        """
        remaining_quota = state.remaining_questions
        current_diff = state.current_difficulty
        current_topic_id = state.current_topic_id
        current_topic_name = state.current_topic_name

        # 1. Termination Rule: Quota exhausted or interview already marked completed
        if remaining_quota <= 0 or state.is_completed or state.status == "completed":
            logger.info("DecisionPolicyAgent: Quota exhausted (%d remaining) -> END_INTERVIEW", remaining_quota)
            return PolicyDecision(
                action="END_INTERVIEW",
                reason=f"Interview question quota exhausted ({state.answered_count}/{state.total_questions} questions completed). Transitioning to final report.",
                target_topic_id=current_topic_id,
                target_topic_name=current_topic_name,
                target_difficulty=current_diff,
                remaining_quota=0,
                is_terminal=True,
                metrics_snapshot={
                    "answered_count": state.answered_count,
                    "total_questions": state.total_questions,
                    "cumulative_score": state.cumulative_score,
                }
            )

        # Retrieve the most recent answered turn
        answered_turns = [t for t in state.turns if t.status == "answered"]
        last_turn: Optional[TurnRecord] = answered_turns[-1] if answered_turns else None

        # If no questions answered yet (session start), initiate interview with first question
        if not last_turn:
            return PolicyDecision(
                action="ASK_NEW_QUESTION",
                reason=f"Session initiated at {current_diff} difficulty. Commencing first assessment turn in topic '{current_topic_name}'.",
                target_topic_id=current_topic_id,
                target_topic_name=current_topic_name,
                target_difficulty=current_diff,
                remaining_quota=remaining_quota,
                is_terminal=False,
                metrics_snapshot={
                    "current_turn": state.current_turn,
                    "seniority": state.seniority_level,
                    "starting_difficulty": current_diff,
                }
            )

        answer_text = (last_turn.candidate_answer or "").strip()
        last_eval = last_turn.evaluation
        word_count = len(answer_text.split())
        depth_score = last_eval.depth_score if last_eval and last_eval.depth_score is not None else None
        overall_score = last_eval.overall_turn_score if last_eval and last_eval.overall_turn_score is not None else None

        # 2. Clarification Rule: Candidate explicitly asked for clarification or rephrasing
        if cls._detect_clarification_intent(answer_text):
            reason = (
                f"Candidate requested question clarification in turn {last_turn.turn_index}. "
                f"Selecting CLARIFY_QUESTION to provide accessible, simplified framing on '{last_turn.topic_name}'."
            )
            return PolicyDecision(
                action="CLARIFY_QUESTION",
                reason=reason,
                target_topic_id=last_turn.topic_id,
                target_topic_name=last_turn.topic_name,
                target_difficulty="easy" if current_diff == "hard" else current_diff,
                remaining_quota=remaining_quota,
                is_terminal=False,
                metrics_snapshot={
                    "turn_index": last_turn.turn_index,
                    "clarification_triggered": True,
                    "simplified_language_preference": state.accessibility.simplified_language,
                }
            )

        # 3. Topic Rotation Rule: Check if the last answered topic quota is exhausted,
        # or if the current active topic domain has reached its allocated questions.
        last_topic_id = last_turn.topic_id if last_turn else current_topic_id
        last_topic_obj: Optional[TopicMastery] = state.topics.get(last_topic_id)
        current_topic_obj: Optional[TopicMastery] = state.topics.get(current_topic_id)

        # Check topic completion on the topic just answered
        if last_topic_obj and last_topic_obj.questions_asked >= last_topic_obj.questions_allocated:
            # Find an unfulfilled topic domain
            next_topic: Optional[TopicMastery] = None
            for top in state.topics.values():
                if top.questions_asked < top.questions_allocated:
                    next_topic = top
                    break

            if next_topic and next_topic.topic_id != last_topic_id:
                reason = (
                    f"Quota allocated for topic '{last_topic_obj.topic_name}' is fulfilled "
                    f"({last_topic_obj.questions_asked}/{last_topic_obj.questions_allocated} asked). "
                    f"Transitioning to next planned domain: '{next_topic.topic_name}'."
                )
                return PolicyDecision(
                    action="CHANGE_TOPIC",
                    reason=reason,
                    target_topic_id=next_topic.topic_id,
                    target_topic_name=next_topic.topic_name,
                    target_difficulty=current_diff,
                    remaining_quota=remaining_quota,
                    is_terminal=False,
                    metrics_snapshot={
                        "previous_topic": last_topic_id,
                        "next_topic": next_topic.topic_id,
                        "questions_asked_on_previous": last_topic_obj.questions_asked,
                    }
                )

        # 4. Difficulty Scaling Rules:
        # High performance (overall_score >= 85) on non-hard questions triggers difficulty escalation
        if overall_score is not None and overall_score >= 85.0 and current_diff != "hard":
            new_diff = cls._get_higher_difficulty(current_diff)
            reason = (
                f"High performance achieved in turn {last_turn.turn_index} "
                f"(turn score: {overall_score:.1f} >= 85.0). Escalating difficulty from '{current_diff}' to '{new_diff}' "
                f"to measure candidate mastery ceiling."
            )
            return PolicyDecision(
                action="INCREASE_DIFFICULTY",
                reason=reason,
                target_topic_id=current_topic_id,
                target_topic_name=current_topic_name,
                target_difficulty=new_diff,
                remaining_quota=remaining_quota,
                is_terminal=False,
                metrics_snapshot={
                    "previous_difficulty": current_diff,
                    "new_difficulty": new_diff,
                    "score": overall_score,
                }
            )

        # Low performance (overall_score < 45) on medium or hard questions triggers difficulty de-escalation
        if overall_score is not None and overall_score < 45.0 and current_diff != "easy":
            new_diff = cls._get_lower_difficulty(current_diff)
            reason = (
                f"Candidate struggled on turn {last_turn.turn_index} "
                f"(turn score: {overall_score:.1f} < 45.0). De-escalating difficulty from '{current_diff}' to '{new_diff}' "
                f"to assess foundational knowledge and prevent cognitive overload."
            )
            return PolicyDecision(
                action="DECREASE_DIFFICULTY",
                reason=reason,
                target_topic_id=current_topic_id,
                target_topic_name=current_topic_name,
                target_difficulty=new_diff,
                remaining_quota=remaining_quota,
                is_terminal=False,
                metrics_snapshot={
                    "previous_difficulty": current_diff,
                    "new_difficulty": new_diff,
                    "score": overall_score,
                }
            )

        # 5. Follow-up Rule: On current topic, if answer had low depth (< 50) or was very short (< 15 words)
        # but overall performance is not severely failing (< 45 handled above), probe with follow-up
        if (depth_score is not None and depth_score < 50.0 and remaining_quota > 1) or (word_count < 15 and remaining_quota > 1):
            reason = (
                f"Candidate provided brief or surface-level technical answer on '{last_turn.topic_name}' "
                f"(word count: {word_count}, depth score: {depth_score if depth_score is not None else 'N/A'}). "
                f"Quota allows ({remaining_quota} remaining); issuing targeted follow-up probe."
            )
            return PolicyDecision(
                action="ASK_FOLLOW_UP",
                reason=reason,
                target_topic_id=last_turn.topic_id,
                target_topic_name=last_turn.topic_name,
                target_difficulty=current_diff,
                remaining_quota=remaining_quota,
                is_terminal=False,
                metrics_snapshot={
                    "word_count": word_count,
                    "depth_score": depth_score,
                    "overall_score": overall_score,
                }
            )

        # 6. Default Action: Continue interview with a standard new question
        reason = (
            f"Candidate provided adequate response (turn score: {overall_score if overall_score is not None else 'calibrated'}, "
            f"mastery: {current_topic_obj.current_mastery_level if current_topic_obj else 0.5:.2f}). "
            f"Proceeding with next scheduled question in '{current_topic_name}' at '{current_diff}' difficulty."
        )
        return PolicyDecision(
            action="ASK_NEW_QUESTION",
            reason=reason,
            target_topic_id=current_topic_id,
            target_topic_name=current_topic_name,
            target_difficulty=current_diff,
            remaining_quota=remaining_quota,
            is_terminal=False,
            metrics_snapshot={
                "current_topic": current_topic_id,
                "current_turn": state.current_turn,
                "remaining_quota": remaining_quota,
            }
        )
