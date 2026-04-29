from typing import Any

from app.observability.sink import TelemetrySink


class RecordingHook:
    """
    Test hook that records formatted telemetry passed through the sink.
    """

    def __init__(self) -> None:
        self.emitted_telemetry: list[dict[str, Any]] = []

    def emit(self, telemetry: dict[str, Any]) -> None:
        self.emitted_telemetry.append(telemetry)


def test_telemetry_sink_forwards_telemetry_to_hook():
    hook = RecordingHook()
    sink = TelemetrySink(hook=hook)

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    sink.emit(telemetry)

    assert hook.emitted_telemetry == [telemetry]


def test_telemetry_sink_does_not_mutate_telemetry():
    hook = RecordingHook()
    sink = TelemetrySink(hook=hook)

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    original_telemetry = telemetry.copy()

    sink.emit(telemetry)

    assert telemetry == original_telemetry
