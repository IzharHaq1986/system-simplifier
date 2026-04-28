from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.sink import emit_execution_telemetry


def test_emit_execution_telemetry_accepts_internal_event_without_returning_data():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        text_length=25,
    )

    result = emit_execution_telemetry(event)

    assert result is None
