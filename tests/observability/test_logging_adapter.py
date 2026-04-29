import json
import logging
from copy import deepcopy

from app.observability.adapters.logging_adapter import LoggingAdapter


def test_logging_adapter_emits_single_json_log_line(caplog):
    adapter = LoggingAdapter()

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    with caplog.at_level(logging.INFO, logger="system_simplifier.observability"):
        adapter.emit(telemetry)

    assert len(caplog.records) == 1

    log_message = caplog.records[0].message
    parsed_log = json.loads(log_message)

    assert parsed_log == {
        "event_type": "simplify.execution",
        "status": "success",
        "text_length": 42,
        "trace_id": "test-trace-id",
    }


def test_logging_adapter_does_not_mutate_telemetry(caplog):
    adapter = LoggingAdapter()

    telemetry = {
        "event_type": "simplify.execution",
        "trace_id": "test-trace-id",
        "status": "success",
        "text_length": 42,
    }

    original_telemetry = deepcopy(telemetry)

    with caplog.at_level(logging.INFO, logger="system_simplifier.observability"):
        adapter.emit(telemetry)

    assert telemetry == original_telemetry
