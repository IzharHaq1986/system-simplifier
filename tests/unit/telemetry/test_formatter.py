from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.formatter import format_execution_telemetry_event


def test_format_execution_telemetry_event_returns_internal_dictionary():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert formatted_event == {
        "trace_id": "trace-123",
        "stage": "execution",
        "decision_allowed": True,
        "execution_status": "success",
        "text_length": 25,
    }
