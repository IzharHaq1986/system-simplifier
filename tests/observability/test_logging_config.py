import logging

from app.observability.logging_config import (
    OBSERVABILITY_LOGGER_NAME,
    configure_observability_logging,
)


def test_configure_observability_logging_sets_expected_logger_level():
    configure_observability_logging()

    logger = logging.getLogger(OBSERVABILITY_LOGGER_NAME)

    assert logger.level == logging.INFO


def test_configure_observability_logging_allows_log_propagation():
    configure_observability_logging()

    logger = logging.getLogger(OBSERVABILITY_LOGGER_NAME)

    assert logger.propagate is True
