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

def test_runtime_response_does_not_expose_failure_or_retry_metadata():
    """
    Validates that runtime failure, retry, and fallback metadata remain
    internal-only and never become part of the public API response.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate runtime metadata boundary isolation."},
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
    assert "failure_reason" not in payload
    assert "retry_count" not in payload
    assert "fallback_used" not in payload


def test_runtime_policy_decision_fields_do_not_leak_into_public_response():
    """
    Validates that runtime policy decision metadata remains internal-only
    during the public simplify request lifecycle.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Explain degraded response telemetry clearly."},
        json={"text": "Validate runtime policy decision isolation."},
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
    assert payload["text_length"] == 43
    assert payload["trace_id"]

    assert "allowed" not in payload
    assert "reason" not in payload
    assert "outcome" not in payload
    assert "runtime_outcome" not in payload
    assert "decision_allowed" not in payload
    assert "execution_status" not in payload
    assert "stage" not in payload


def test_evaluation_decision_fields_do_not_leak_into_public_response():
    """
    Validates that internal evaluation decision metadata remains hidden
    from the public API response during the simplify request lifecycle.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate evaluation decision boundary isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 48
    assert payload["trace_id"]

    assert "evaluation" not in payload
    assert "evaluation_allowed" not in payload
    assert "evaluation_reason" not in payload
    assert "evaluation_status" not in payload
    assert "rule_version" not in payload
    assert "warnings" not in payload


def test_public_simplify_response_only_contains_allowed_fields():
    """
    Validates the public API response allowlist so internal runtime,
    telemetry, policy, and evaluation fields cannot leak accidentally.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate public response allowlist."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert set(payload) == {
        "status",
        "text_length",
        "trace_id",
    }

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 35
    assert payload["trace_id"]


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
