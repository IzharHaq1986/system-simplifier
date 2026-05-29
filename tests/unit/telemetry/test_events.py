import pytest
from pydantic import ValidationError

from app.runtime.policy import RuntimeOutcome
from app.telemetry.events import ExecutionTelemetryEvent


def test_execution_telemetry_event_accepts_valid_runtime_event():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    assert event.trace_id == "trace-123"
    assert event.stage == "execution"
    assert event.decision_allowed is True
    assert event.execution_status == "success"
    assert event.runtime_outcome == RuntimeOutcome.SUCCESS
    assert event.text_length == 25


def test_execution_telemetry_event_rejects_empty_trace_id():
    with pytest.raises(ValidationError):
        ExecutionTelemetryEvent(
            trace_id="",
            stage="execution",
            decision_allowed=True,
            execution_status="success",
            runtime_outcome=RuntimeOutcome.SUCCESS,
            text_length=25,
        )


def test_execution_telemetry_event_rejects_empty_stage():
    with pytest.raises(ValidationError):
        ExecutionTelemetryEvent(
            trace_id="trace-123",
            stage="",
            decision_allowed=True,
            execution_status="success",
            runtime_outcome=RuntimeOutcome.SUCCESS,
            text_length=25,
        )


def test_execution_telemetry_event_rejects_empty_execution_status():
    with pytest.raises(ValidationError):
        ExecutionTelemetryEvent(
            trace_id="trace-123",
            stage="execution",
            decision_allowed=True,
            execution_status="",
            runtime_outcome=RuntimeOutcome.SUCCESS,
            text_length=25,
        )


def test_execution_telemetry_event_rejects_negative_text_length():
    with pytest.raises(ValidationError):
        ExecutionTelemetryEvent(
            trace_id="trace-123",
            stage="execution",
            decision_allowed=True,
            execution_status="success",
            runtime_outcome=RuntimeOutcome.SUCCESS,
            text_length=-1,
        )

def test_execution_telemetry_event_defaults_quality_signal_to_none():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
    )

    assert event.quality_signal is None


def test_execution_telemetry_event_accepts_internal_quality_signal_payload():
    event = ExecutionTelemetryEvent(
        trace_id="trace-123",
        stage="execution",
        decision_allowed=True,
        execution_status="success",
        runtime_outcome=RuntimeOutcome.SUCCESS,
        text_length=25,
        quality_signal={
            "status": "acceptable",
            "source": "evaluation",
            "reason": "evaluation passed",
            "score": 100,
        },
    )

    assert event.quality_signal == {
        "status": "acceptable",
        "source": "evaluation",
        "reason": "evaluation passed",
        "score": 100,
    }
