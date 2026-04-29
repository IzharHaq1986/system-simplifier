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

def test_emit_execution_telemetry_uses_internal_formatter(monkeypatch):
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        text_length=25,
    )

    captured_events = []

    def capture_format_call(received_event):
        captured_events.append(received_event)
        return {
            "trace_id": received_event.trace_id,
            "stage": received_event.stage,
            "decision_allowed": received_event.decision_allowed,
            "execution_status": received_event.execution_status,
            "text_length": received_event.text_length,
        }

    monkeypatch.setattr(
        "app.telemetry.sink.format_execution_telemetry_event",
        capture_format_call,
    )

    emit_execution_telemetry(event)

    assert captured_events == [event]
