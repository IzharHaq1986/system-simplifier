from enum import StrEnum
from pydantic import BaseModel


class RuntimeOutcome(StrEnum):
    SUCCESS = "success"
    RETRY = "retry"
    FALLBACK = "fallback"
    DEGRADED_RESPONSE = "degraded_response"
    FAILURE = "failure"


class RuntimePolicyDecision(BaseModel):
    allowed: bool
    outcome: RuntimeOutcome
    reason: str
    trace_id: str
