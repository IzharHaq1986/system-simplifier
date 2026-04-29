from app.telemetry.event import TelemetryEvent


def test_telemetry_event_accepts_execution_result_metadata():
    event = TelemetryEvent(
        event_type="execution_result_recorded",
        trace_id="test-trace-id",
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    assert event.event_type == "execution_result_recorded"
    assert event.trace_id == "test-trace-id"
    assert event.status == "success"
    assert event.mode == "no_op"
    assert event.reason_code == "execution_prepared"
