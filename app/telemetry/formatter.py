from typing import Any

from app.telemetry.events import ExecutionTelemetryEvent


def format_execution_telemetry_event(
    event: ExecutionTelemetryEvent,
) -> dict[str, Any]:
    """
    Convert an internal telemetry event into a structured log-safe dictionary.

    This remains internal-only and must not be returned from API responses.
    """

    return {
        "trace_id": event.trace_id,
        "stage": event.stage,
        "decision_allowed": event.decision_allowed,
        "execution_status": event.execution_status,
        "runtime_outcome": event.runtime_outcome,
        "text_length": event.text_length,
    }
