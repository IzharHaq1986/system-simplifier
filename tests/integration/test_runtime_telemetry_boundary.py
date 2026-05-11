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

def test_public_response_exposes_only_single_trace_id_field():
    """
    Validates that the public API exposes one stable trace_id field
    without leaking duplicate or internal trace metadata.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate trace id boundary consistency."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["trace_id"]
    assert list(payload).count("trace_id") == 1

    assert "trace" not in payload
    assert "traceId" not in payload
    assert "request_id" not in payload
    assert "correlation_id" not in payload
    assert "internal_trace_id" not in payload
