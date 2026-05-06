from app.runtime.policy import RuntimeOutcome

from pydantic import BaseModel, Field


class ExecutionTelemetryEvent(BaseModel):
    """
    Internal telemetry event for execution observability.

    This model is intentionally internal-only.
    It must not be returned from API responses.
    """

    trace_id: str = Field(min_length=1)
    stage: str = Field(min_length=1)
    decision_allowed: bool
    execution_status: str = Field(min_length=1)
    runtime_outcome: RuntimeOutcome
    text_length: int = Field(ge=0)
