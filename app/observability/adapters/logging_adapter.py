"""
Structured logging adapter for internal observability telemetry.

This adapter is intentionally small:
- accepts already-formatted telemetry
- emits one JSON log line
- does not mutate telemetry
- does not call external systems
"""

import json
import logging
from typing import Any


logger = logging.getLogger("system_simplifier.observability")


class LoggingAdapter:
    """
    Emits formatted telemetry as structured JSON logs.
    """

    def emit(self, telemetry: dict[str, Any]) -> None:
        """
        Emit telemetry as a single-line JSON log entry.
        """

        serialized_telemetry = json.dumps(
            telemetry,
            sort_keys=True,
            separators=(",", ":"),
        )

        logger.info(serialized_telemetry)
