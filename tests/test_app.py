from fastapi.testclient import TestClient
from app.main import app
from app.response_policy.decision import ResponsePolicyDecision

client = TestClient(app)


def test_health_check():
    # Basic uptime probe for local and CI validation
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Trace-ID" in response.headers


def test_simplify_accepts_valid_request():
    # Valid request should pass schema validation, guardrails, and policy evaluation
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    body = response.json()

    assert response.status_code == 200
    assert set(body.keys()) == {"status", "text_length", "trace_id"}
    assert body["status"] == "accepted"
    assert body["text_length"] == len("Simplify this system design.")
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_simplify_trims_surrounding_whitespace():
    # Surrounding whitespace should be normalized before processing
    response = client.post(
        "/v1/simplify",
        json={"text": "  Simplify this system design.  "},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "accepted"
    assert body["text_length"] == len("Simplify this system design.")
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_simplify_rejects_whitespace_only_text():
    # Whitespace-only input should fail after normalization
    response = client.post(
        "/v1/simplify",
        json={"text": "   "},
    )

    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "invalid_input"
    assert body["error"]["message"] == "Request validation failed."
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]

def test_simplify_success_response_uses_normalized_text_length():
    response = client.post(
        "/v1/simplify",
        json={"text": "  Simplify this system design.  "},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert response_payload["text_length"] == len("Simplify this system design.")

def test_simplify_rejects_unsupported_control_characters():
    # Unsupported control characters should be rejected deterministically
    response = client.post(
        "/v1/simplify",
        json={"text": "Hello\u0000World"},
    )

    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "invalid_input"
    assert body["error"]["message"] == "Input contains unsupported control characters."
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_simplify_rejects_empty_text():
    # Empty payload should be rejected by schema validation
    response = client.post(
        "/v1/simplify",
        json={"text": ""},
    )

    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "invalid_input"
    assert body["error"]["message"] == "Request validation failed."
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_simplify_denies_policy_blocked_input():
    # Policy-blocked input should be rejected after guardrails succeed
    response = client.post(
        "/v1/simplify",
        json={"text": "Please process forbidden-term now."},
    )

    body = response.json()

    assert response.status_code == 403
    assert set(body.keys()) == {"error", "trace_id"}
    assert body["error"]["code"] == "policy_denied"
    assert body["error"]["message"] == "Request denied by policy."
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_policy_denial_matches_error_response_contract():
    # Policy denial should preserve the shared typed error response structure
    response = client.post(
        "/v1/simplify",
        json={"text": "blocked-term"},
    )

    body = response.json()

    assert response.status_code == 403
    assert set(body.keys()) == {"error", "trace_id"}
    assert set(body["error"].keys()) == {"code", "message"}
    assert body["error"]["code"] == "policy_denied"
    assert body["error"]["message"] == "Request denied by policy."


def test_policy_denial_preserves_trace_id():
    # Trace metadata must remain available on the policy denial path
    response = client.post(
        "/v1/simplify",
        json={"text": "forbidden-term"},
    )

    body = response.json()

    assert response.status_code == 403
    assert "trace_id" in body
    assert isinstance(body["trace_id"], str)
    assert body["trace_id"]
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_guardrails_run_before_policy_evaluation():
    # Invalid input should fail at the earlier boundary instead of reaching policy denial
    response = client.post(
        "/v1/simplify",
        json={"text": "   "},
    )

    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "invalid_input"
    assert body["error"]["code"] != "policy_denied"
    assert body["error"]["message"] == "Request validation failed."
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]

def test_simplify_response_does_not_expose_internal_execution_fields():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert "status" in response_payload
    assert "text_length" in response_payload
    assert "trace_id" in response_payload

    assert "mode" not in response_payload
    assert "reason_code" not in response_payload

def test_simplify_success_response_has_exact_public_fields():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert set(response_payload.keys()) == {
        "status",
        "text_length",
        "trace_id",
    }

    assert response_payload["status"] == "accepted"
    assert response_payload["text_length"] == len("Simplify this system design.")
    assert isinstance(response_payload["trace_id"], str)
    assert response_payload["trace_id"]

def test_simplify_success_response_trace_id_matches_header():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert "X-Trace-ID" in response.headers
    assert response_payload["trace_id"] == response.headers["X-Trace-ID"]

def test_simplify_success_response_excludes_placeholder_output_fields():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert "output" not in response_payload
    assert "result" not in response_payload
    assert "message" not in response_payload

def test_simplify_success_passes_response_policy_boundary():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 200

    response_payload = response.json()

    assert response_payload["status"] == "accepted"
    assert response_payload["text_length"] == len("Simplify this system design.")
    assert response_payload["trace_id"] == response.headers["X-Trace-ID"]

def test_simplify_response_policy_denial_returns_stable_error(monkeypatch):
    def deny_response_policy(_response):
        return ResponsePolicyDecision(
            decision="deny",
            reason_code="response_contract_denied",
        )

    monkeypatch.setattr(
        "app.api.routes.simplify.evaluate_response_policy",
        deny_response_policy,
    )

    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    assert response.status_code == 500

    response_payload = response.json()

    assert response_payload["error"]["code"] == "response_policy_denied"
    assert response_payload["error"]["message"] == "Response denied by response policy."
    assert response_payload["trace_id"] == response.headers["X-Trace-ID"]

def test_simplify_openapi_documents_response_policy_denial_error():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi_schema = response.json()
    simplify_responses = openapi_schema["paths"]["/v1/simplify"]["post"]["responses"]

    assert "500" in simplify_responses
    assert simplify_responses["500"]["description"] == (
        "Response denied by response policy boundary."
    )

def test_simplify_response_does_not_expose_telemetry_fields():
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this telemetry boundary."},
    )

    assert response.status_code == 200

    body = response.json()

    assert "stage" not in body
    assert "decision_allowed" not in body
    assert "execution_status" not in body
