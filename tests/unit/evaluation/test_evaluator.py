from app.models.response import SimplifyResponse
from app.evaluation.evaluator import (
    EVALUATION_REASON_INVALID_TEXT_LENGTH,
    EVALUATION_REASON_MISSING_TRACE_ID,
    EVALUATION_REASON_PASSED,
    EVALUATION_REASON_UNEXPECTED_STATUS,
    evaluate_response,
)

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

def test_evaluate_response_denies_unexpected_status() -> None:
    response = SimplifyResponse(
        status="failed",
        text_length=10,
        trace_id="trace-123",
    )

    decision = evaluate_response(response)

    assert decision.allowed is False
    assert decision.reason == "unexpected_response_status"
    assert decision.rule_version == "v1"

def test_evaluate_response_denies_non_positive_text_length() -> None:
    response = SimplifyResponse(
        status="success",
        text_length=0,
        trace_id="trace-123",
    )

    decision = evaluate_response(response)

    assert decision.allowed is False
    assert decision.reason == "invalid_text_length"
    assert decision.rule_version == "v1"

def test_evaluation_reason_constants_match_expected_values() -> None:
    assert EVALUATION_REASON_MISSING_TRACE_ID == "missing_trace_id"
    assert EVALUATION_REASON_UNEXPECTED_STATUS == "unexpected_response_status"
    assert EVALUATION_REASON_INVALID_TEXT_LENGTH == "invalid_text_length"
    assert EVALUATION_REASON_PASSED == "evaluation_passed"
