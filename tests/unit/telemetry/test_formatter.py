from app.runtime.policy import RuntimeOutcome
from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.formatter import format_execution_telemetry_event


def test_format_execution_telemetry_event_returns_internal_dictionary():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert formatted_event == {
        "trace_id": "trace-123",
        "stage": "execution",
        "decision_allowed": True,
        "execution_status": "success",
        "runtime_outcome": RuntimeOutcome.SUCCESS,
        "text_length": 25,
    }


def test_format_execution_telemetry_event_excludes_unapproved_fields():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert set(formatted_event) == {
        "trace_id",
        "stage",
        "decision_allowed",
        "execution_status",
        "runtime_outcome",
        "text_length",
    }

    assert "internal_state" not in formatted_event
    assert "raw_result" not in formatted_event
    assert "model_output" not in formatted_event

def test_format_execution_telemetry_event_supports_retry_outcome():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="retry",
        runtime_outcome=RuntimeOutcome.RETRY,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert formatted_event["runtime_outcome"] == RuntimeOutcome.RETRY


def test_format_execution_telemetry_event_supports_fallback_outcome():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="fallback",
        runtime_outcome=RuntimeOutcome.FALLBACK,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert formatted_event["runtime_outcome"] == RuntimeOutcome.FALLBACK


def test_format_execution_telemetry_event_supports_degraded_response_outcome():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="degraded_response",
        runtime_outcome=RuntimeOutcome.DEGRADED_RESPONSE,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert (
        formatted_event["runtime_outcome"]
        == RuntimeOutcome.DEGRADED_RESPONSE
    )


def test_format_execution_telemetry_event_supports_failure_outcome():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=False,
        execution_status="failure",
        runtime_outcome=RuntimeOutcome.FAILURE,
        text_length=25,
    )

    formatted_event = format_execution_telemetry_event(event)

    assert formatted_event["runtime_outcome"] == RuntimeOutcome.FAILURE
