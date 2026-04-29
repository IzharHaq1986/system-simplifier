from app.telemetry.events import ExecutionTelemetryEvent
from app.telemetry.formatter import format_execution_telemetry_event
from app.telemetry.hooks import handle_structured_telemetry

def emit_execution_telemetry(event: ExecutionTelemetryEvent) -> None:
    """
    Internal telemetry sink.

    For now, this prepares a structured internal telemetry payload
    and sends it to an internal observability hook without external I/O,
    logging vendors, queues, or metrics systems.
    """

    formatted_event = format_execution_telemetry_event(event)
    handle_structured_telemetry(formatted_event)
