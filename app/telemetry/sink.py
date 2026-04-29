from app.telemetry.events import ExecutionTelemetryEvent


def emit_execution_telemetry(event: ExecutionTelemetryEvent) -> None:
    """
    Internal telemetry sink.

    For now, this intentionally performs no external I/O.
    It exists to define the telemetry emission boundary without
    adding logging, metrics, queues, or vendor coupling yet.
    """

    _ = event
