from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field

PolicyActionType = Literal[
    "ASK_NEW_QUESTION",
    "ASK_FOLLOW_UP",
    "INCREASE_DIFFICULTY",
    "DECREASE_DIFFICULTY",
    "CHANGE_TOPIC",
    "CLARIFY_QUESTION",
    "CONTINUE_INTERVIEW",
    "END_INTERVIEW",
]

class PolicyDecision(BaseModel):
    action: PolicyActionType = Field(
        description="The decided next interview policy action."
    )
    reason: str = Field(
        description="Transparent, deterministic rationale explaining why this action was selected based on state, mastery, and quotas."
    )
    target_topic_id: str = Field(
        description="The target topic ID for the upcoming question/follow-up."
    )
    target_topic_name: str = Field(
        description="Display name of the target topic."
    )
    target_difficulty: Literal["easy", "medium", "hard"] = Field(
        description="The calibrated difficulty level ('easy', 'medium', 'hard') for the next turn."
    )
    remaining_quota: int = Field(
        description="Number of questions remaining in the interview session."
    )
    is_terminal: bool = Field(
        default=False,
        description="True if the action concludes the interview."
    )
    metrics_snapshot: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Snapshot of relevant state metrics (mastery, score, turn) that justified the decision."
    )

class DecisionPolicyEvaluationRequest(BaseModel):
    session_id: str
