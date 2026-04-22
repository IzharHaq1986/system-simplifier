from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    # Basic uptime probe for local and CI validation
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Trace-ID" in response.headers


def test_simplify_accepts_valid_request():
    # Valid request should pass schema validation and return trace metadata
    response = client.post(
        "/v1/simplify",
        json={"text": "Simplify this system design."},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "accepted"
    assert body["text_length"] == len("Simplify this system design.")
    assert "trace_id" in body
    assert body["trace_id"] == response.headers["X-Trace-ID"]


def test_simplify_rejects_empty_text():
    # Empty payload should be rejected by schema validation
    response = client.post(
        "/v1/simplify",
        json={"text": ""},
    )

    assert response.status_code == 422
    assert "X-Trace-ID" in response.headers
