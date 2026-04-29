"""
Observability factory.

Creates the internal observability pipeline:

LoggingAdapter
    -> ObservabilityHook
    -> TelemetrySink

This keeps construction logic out of route handlers.
"""

from app.observability.adapters.logging_adapter import LoggingAdapter
from app.observability.hook import ObservabilityHook
from app.observability.sink import TelemetrySink


def build_telemetry_sink() -> TelemetrySink:
    """
    Build the default internal telemetry sink.
    """

    adapter = LoggingAdapter()
    hook = ObservabilityHook(adapter=adapter)

    return TelemetrySink(hook=hook)
