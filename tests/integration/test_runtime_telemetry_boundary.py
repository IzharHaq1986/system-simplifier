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
        json={"text": "Validate runtime policy decision isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 43
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "execution_status" not in payload
    assert "decision_allowed" not in payload
    assert "stage" not in payload


def test_degraded_response_runtime_outcome_remains_internal():
    """
    Validates that degraded-response runtime metadata remains internal-only
    and does not expand the public API response contract.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Explain degraded response telemetry clearly."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 44
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "degraded_response" not in payload
    assert "retry_metadata" not in payload
    assert "fallback_metadata" not in payload
    assert "policy_decision" not in payload
    assert "evaluation_decision" not in payload


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
        json={"text": "Validate runtime policy decision isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 43
    assert payload["trace_id"]

    assert "allowed" not in payload
    assert "reason" not in payload
    assert "outcome" not in payload
    assert "runtime_outcome" not in payload
    assert "decision_allowed" not in payload


def test_evaluation_decision_fields_do_not_leak_into_public_response():
    """
    Validates that evaluation decision metadata remains internal-only and
    does not become part of the public API response.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate evaluation decision isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 39
    assert payload["trace_id"]

    assert "evaluation_allowed" not in payload
    assert "evaluation_reason" not in payload
    assert "evaluation_decision" not in payload
    assert "rule_version" not in payload


def test_public_response_contains_only_allowed_fields():
    """
    Validates that the public simplify response remains constrained to the
    approved response contract fields.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate public response allowlist."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {
        "status",
        "text_length",
        "trace_id",
    }


def test_public_trace_id_boundary_exposes_only_single_trace_id():
    """
    Validates that the public API exposes only the approved trace_id field
    and does not leak internal trace metadata.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate public trace boundary."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["trace_id"]

    assert "trace" not in payload
    assert "trace_metadata" not in payload
    assert "runtime_trace_id" not in payload
    assert "internal_trace_id" not in payload

def test_retry_runtime_outcome_remains_internal():
    """
    Validates that retry-related runtime metadata remains internal-only
    and never expands the public API response contract.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate retry telemetry isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 35
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "retry_count" not in payload
    assert "retry_metadata" not in payload
    assert "retry_attempt" not in payload
    assert "retry_reason" not in payload

def test_fallback_runtime_outcome_remains_internal():
    """
    Validates that fallback-related runtime metadata remains internal-only
    and never expands the public API response contract.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate fallback telemetry isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 38
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "fallback_used" not in payload
    assert "fallback_reason" not in payload
    assert "fallback_metadata" not in payload
    assert "fallback_attempt" not in payload

def test_runtime_outcome_transition_fields_remain_internal():
    """
    Validates that runtime outcome transition metadata remains internal-only
    and does not expand the public API response contract.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "Validate runtime outcome transition isolation."},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "accepted"
    assert payload["text_length"] == 46
    assert payload["trace_id"]

    assert "runtime_outcome" not in payload
    assert "previous_runtime_outcome" not in payload
    assert "next_runtime_outcome" not in payload
    assert "outcome_transition" not in payload
    assert "transition_reason" not in payload
