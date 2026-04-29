"""
Internal telemetry event construction.

Telemetry is an observation boundary only.
It must not affect API responses, policy decisions, or control flow.
"""

from pydantic import BaseModel, ConfigDict

from app.evaluation.decision import EvaluationDecision


class TelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str
    status: str
    trace_id: str
    text_length: int

    evaluation_status: str | None = None
    evaluation_reason: str | None = None
    evaluation_rule_version: str | None = None


def build_telemetry_event(
    *,
    event_type: str,
    status: str,
    trace_id: str,
    text_length: int,
    evaluation_decision: EvaluationDecision | None = None,
) -> TelemetryEvent:
    return TelemetryEvent(
        event_type=event_type,
        status=status,
        trace_id=trace_id,
        text_length=text_length,
        evaluation_status=(
            "passed"
            if evaluation_decision is not None and evaluation_decision.allowed
            else "failed"
            if evaluation_decision is not None
            else None
        ),
        evaluation_reason=(
            evaluation_decision.reason
            if evaluation_decision is not None
            else None
        ),
        evaluation_rule_version=(
            evaluation_decision.rule_version
            if evaluation_decision is not None
            else None
        ),
    )
