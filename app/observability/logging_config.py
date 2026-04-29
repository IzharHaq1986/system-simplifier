"""
Minimal logging configuration for internal observability.

The configuration keeps telemetry logs structured and single-line.
It does not introduce external logging systems or runtime dependencies.
"""

import logging


OBSERVABILITY_LOGGER_NAME = "system_simplifier.observability"


def configure_observability_logging() -> None:
    """
    Configure internal observability logging.

    This function is safe to call multiple times.
    """

    logger = logging.getLogger(OBSERVABILITY_LOGGER_NAME)

    logger.setLevel(logging.INFO)
    logger.propagate = True
