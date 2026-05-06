from app.runtime.policy import RuntimeOutcome
from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.sink import emit_execution_telemetry


def test_emit_execution_telemetry_accepts_internal_event_without_returning_data():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
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
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    captured_event = {}

    def fake_formatter(received_event):
        captured_event["event"] = received_event
        return {
            "trace_id": received_event.trace_id,
            "stage": received_event.stage,
            "decision_allowed": received_event.decision_allowed,
            "execution_status": received_event.execution_status,
            "runtime_outcome": received_event.runtime_outcome,
            "text_length": received_event.text_length,
        }

    monkeypatch.setattr(
        "app.telemetry.sink.format_execution_telemetry_event",
        fake_formatter,
    )

    emit_execution_telemetry(event)

    assert captured_event["event"] == event


def test_emit_execution_telemetry_calls_observability_hook(monkeypatch):
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    captured_payload = {}

    def fake_observability_hook(payload):
        captured_payload["payload"] = payload

    monkeypatch.setattr(
        "app.telemetry.sink.handle_structured_telemetry",
        fake_observability_hook,
    )

    emit_execution_telemetry(event)

    assert captured_payload["payload"] == {
        "trace_id": "trace-123",
        "stage": "execution",
        "decision_allowed": True,
        "execution_status": "success",
        "runtime_outcome": RuntimeOutcome.SUCCESS,
        "text_length": 25,
    }
