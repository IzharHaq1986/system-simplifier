from app.evaluation import QualitySignal, serialize_quality_signal
from app.execution.decision import ExecutionDecision
from app.execution.result import ExecutionResult
from app.runtime.policy import RuntimeOutcome
from app.telemetry.events import ExecutionTelemetryEvent


def build_execution_telemetry_event(
    trace_id: str,
    decision: ExecutionDecision,
    result: ExecutionResult,
    text_length: int,
    quality_signal: QualitySignal | None = None,
) -> ExecutionTelemetryEvent:
    """
    Build internal execution telemetry from execution boundary outputs.

    Runtime outcome categorization and quality signals are internal-only.
    They must never be returned from the public API response.
    """

    quality_payload = None

    if quality_signal is not None:
        quality_payload = serialize_quality_signal(quality_signal)

    return ExecutionTelemetryEvent(
        trace_id=trace_id,
        stage="execution",
        decision_allowed=(decision.decision == "proceed"),
        execution_status=result.status,
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=text_length,
        quality_signal=quality_payload,
    )
