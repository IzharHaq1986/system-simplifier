from typing import Any

from app.observability.hook import ObservabilityHook


class RecordingAdapter:
    """
    Test adapter that records telemetry passed through the hook.
    """

    def __init__(self) -> None:
        self.emitted_telemetry: list[dict[str, Any]] = []

    def emit(self, telemetry: dict[str, Any]) -> None:
        self.emitted_telemetry.append(telemetry)


def test_observability_hook_forwards_telemetry_to_adapter():
    adapter = RecordingAdapter()
    hook = ObservabilityHook(adapter=adapter)

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    hook.emit(telemetry)

    assert adapter.emitted_telemetry == [telemetry]


def test_observability_hook_does_not_mutate_telemetry():
    adapter = RecordingAdapter()
    hook = ObservabilityHook(adapter=adapter)

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    original_telemetry = telemetry.copy()

    hook.emit(telemetry)

    assert telemetry == original_telemetry

def test_observability_hook_preserves_runtime_outcome():
    adapter = RecordingAdapter()
    hook = ObservabilityHook(adapter=adapter)

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "runtime_outcome": "success",
        "text_length": 42,
    }

    hook.emit(telemetry)

    assert adapter.emitted_telemetry == [telemetry]
    assert adapter.emitted_telemetry[0]["runtime_outcome"] == "success"
