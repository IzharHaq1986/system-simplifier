from app.execution.decision import ExecutionDecision
from app.execution.result import ExecutionResult
from app.telemetry.builder import build_execution_telemetry_event
from app.evaluation import QualitySignal, QualitySignalStatus

def test_build_execution_telemetry_event_from_execution_outputs():
    decision = ExecutionDecision(
        decision="proceed",
        allowed=True,
        mode="no_op",
        reason_code="policy_allowed",
    )

    result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
        text_length=25,
        trace_id="trace-123",
    )

    event = build_execution_telemetry_event(
        trace_id="trace-123",
        decision=decision,
        result=result,
        text_length=25,
    )

    assert event.trace_id == "trace-123"
    assert event.stage == "execution"
    assert event.decision_allowed is True
    assert event.execution_status == "success"
    assert event.text_length == 25

def test_build_execution_telemetry_event_defaults_quality_signal_to_none():
    decision = ExecutionDecision(
        decision="proceed",
        allowed=True,
        mode="no_op",
        reason_code="policy_allowed",
    )
    result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
        text_length=25,
        trace_id="trace-123",
    )

    event = build_execution_telemetry_event(
        trace_id="trace-123",
        decision=decision,
        result=result,
        text_length=25,
    )

    assert event.quality_signal is None


def test_build_execution_telemetry_event_serializes_internal_quality_signal():
    decision = ExecutionDecision(
        decision="proceed",
        allowed=True,
        mode="no_op",
        reason_code="policy_allowed",
    )
    result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
        text_length=25,
        trace_id="trace-123",
    )
    quality_signal = QualitySignal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
        score=100,
    )

    event = build_execution_telemetry_event(
        trace_id="trace-123",
        decision=decision,
        result=result,
        text_length=25,
        quality_signal=quality_signal,
    )

    assert event.quality_signal == {
        "status": "acceptable",
        "source": "evaluation",
        "reason": "evaluation passed",
        "score": 100,
    }
