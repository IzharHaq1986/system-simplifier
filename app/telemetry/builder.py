from app.execution.decision import ExecutionDecision
from app.execution.result import ExecutionResult
from app.telemetry.events import ExecutionTelemetryEvent

def build_execution_telemetry_event(
    trace_id: str,
    decision: ExecutionDecision,
    result: ExecutionResult,
    text_length: int,
) -> ExecutionTelemetryEvent:

    """
    Build internal execution telemetry from execution boundary outputs.

    This event is internal-only and must never be returned
    from the public API response.
    """

    return ExecutionTelemetryEvent(
        trace_id=trace_id,
        stage="execution",
        decision_allowed=(decision.decision == "proceed"),
        execution_status=result.status,
        text_length=text_length,
    )
