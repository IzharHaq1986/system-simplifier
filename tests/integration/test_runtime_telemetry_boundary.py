from fastapi.testclient import TestClient

from app.main import app


def test_runtime_telemetry_remains_internal_during_simplify_request():
    """
    Validates that runtime telemetry can execute during a real request
    without leaking internal runtime fields into the public API response.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Explain runtime telemetry boundaries clearly."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 45
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "execution_status" not in payload
    assert "decision_allowed" not in payload
    assert "stage" not in payload

def test_degraded_response_runtime_outcome_remains_internal():
    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Explain degraded response telemetry clearly."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["trace_id"]
    assert payload["text_length"] == 44

    assert "runtime_outcome" not in payload
    assert "degraded_response" not in payload
    assert "retry_metadata" not in payload
    assert "fallback_metadata" not in payload
    assert "policy_decision" not in payload
    assert "evaluation_decision" not in payload
