from app.telemetry.hooks import handle_structured_telemetry


def test_handle_structured_telemetry_accepts_formatted_event_without_returning_data():
    formatted_event = {
        "trace_id": "trace-123",
        "stage": "execution",
        "decision_allowed": True,
        "execution_status": "success",
        "text_length": 25,
    }

    result = handle_structured_telemetry(formatted_event)

    assert result is None
