"""
Observability hook boundary.

This module defines the internal boundary between formatted telemetry
and observability adapters such as structured logging.

No API response should import from this module directly.
"""

from typing import Any, Protocol


class ObservabilityAdapter(Protocol):
    """
    Contract for internal observability adapters.
    """

    def emit(self, telemetry: dict[str, Any]) -> None:
        """
        Emit formatted telemetry through an internal mechanism.
        """


class ObservabilityHook:
    """
    Internal observability boundary.

    The hook forwards already-formatted telemetry to the configured adapter.
    """

    def __init__(self, adapter: ObservabilityAdapter) -> None:
        self._adapter = adapter

    def emit(self, telemetry: dict[str, Any]) -> None:
        """
        Forward formatted telemetry to the configured adapter.
        """

        self._adapter.emit(telemetry)
