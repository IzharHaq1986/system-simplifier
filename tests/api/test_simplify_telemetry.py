import json
import logging

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_simplify_emits_telemetry_log(caplog):
    payload = {
        "text": "   Hello world   "
    }

    with caplog.at_level(logging.INFO, logger="system_simplifier.observability"):
        response = client.post("/v1/simplify", json=payload)

    assert response.status_code == 200

    # ensure at least one log emitted
    assert len(caplog.records) >= 1

    # parse last log entry (telemetry)
    log_message = caplog.records[-1].message
    telemetry = json.loads(log_message)

    assert telemetry["event_type"] == "simplify.execution"
    assert telemetry["status"] == "success"
    assert telemetry["text_length"] > 0
    assert "trace_id" in telemetry
