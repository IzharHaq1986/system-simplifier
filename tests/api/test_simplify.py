from fastapi.testclient import TestClient

from app.main import app


def test_simplify_response_does_not_expose_evaluation_signal() -> None:
    """
    Evaluation fields must remain internal and unavailable in API responses.
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={"text": "This is a valid input for simplification."},
    )

    assert response.status_code == 200

    body = response.json()

    assert "evaluation_status" not in body
    assert "evaluation_reason" not in body
    assert "evaluation_rule_version" not in body


def test_simplify_evaluation_remains_non_blocking() -> None:
    """
    Evaluation warnings must stay internal.

    Expected flow:
    - request passes validation
    - guardrails pass
    - policy allows the request
    - response is shaped successfully
    - evaluation runs internally
    - API response remains successful
    """

    client = TestClient(app)

    response = client.post(
        "/v1/simplify",
        json={
            "text": "Keep the system simple and observable.",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "accepted"
    assert body["text_length"] > 0
    assert body["trace_id"] == response.headers["X-Trace-ID"]

    # Evaluation details must not leak through the public API contract.
    assert "evaluation_status" not in body
    assert "evaluation_reason" not in body
    assert "evaluation_rule_version" not in body
