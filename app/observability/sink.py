"""
Telemetry sink boundary.

The sink is responsible for sending already-formatted telemetry
to the configured observability hook.

It does not format telemetry.
It does not expose telemetry through API responses.
It does not call external systems directly.
"""

from typing import Any

from app.observability.hook import ObservabilityHook


class TelemetrySink:
    """
    Internal sink for formatted telemetry events.
    """

    def __init__(self, hook: ObservabilityHook) -> None:
        self._hook = hook

    def emit(self, telemetry: dict[str, Any]) -> None:
        """
        Emit formatted telemetry through the observability hook.
        """

        self._hook.emit(telemetry)
