from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.formatter import format_execution_telemetry_event


def emit_execution_telemetry(event: ExecutionTelemetryEvent) -> None:
    """
    Internal telemetry sink.

    For now, this prepares a structured internal telemetry payload
    without external I/O, logging vendors, queues, or metrics systems.
    """

    formatted_event = format_execution_telemetry_event(event)
    _ = formatted_event
