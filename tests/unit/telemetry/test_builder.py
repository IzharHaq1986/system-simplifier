from app.execution.decision import ExecutionDecision
from app.execution.result import ExecutionResult
from app.telemetry.builder import build_execution_telemetry_event


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
