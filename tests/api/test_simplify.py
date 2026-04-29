from fastapi.testclient import TestClient

from app.main import app


def test_simplify_response_does_not_expose_evaluation_signal() -> None:
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
