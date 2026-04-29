from app.evaluation.evaluator import evaluate_response
from app.models.response import SimplifyResponse


def test_evaluate_response_allows_response_with_trace_id():
    response = SimplifyResponse(
        status="success",
        text_length=11,
        trace_id="trace-123",
    )

    decision = evaluate_response(response)

    assert decision.allowed is True
    assert decision.reason == "evaluation_passed"


def test_evaluate_response_allows_valid_response_contract():
    response = SimplifyResponse(
        status="success",
        text_length=11,
        trace_id="trace-456",
    )

    decision = evaluate_response(response)

    assert decision.allowed is True
    assert decision.reason == "evaluation_passed"
