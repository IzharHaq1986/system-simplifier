from app.evaluation import (
    EVALUATION_REASON_INVALID_TEXT_LENGTH,
    EVALUATION_REASON_MISSING_TRACE_ID,
    EVALUATION_REASON_PASSED,
    EVALUATION_REASON_UNEXPECTED_STATUS,
    EVALUATION_RULE_VERSION,
    EvaluationDecision,
    evaluate_response,
)


def test_evaluation_package_exports_stable_contracts() -> None:
    assert EVALUATION_RULE_VERSION == "v1"
    assert EVALUATION_REASON_MISSING_TRACE_ID == "missing_trace_id"
    assert EVALUATION_REASON_UNEXPECTED_STATUS == "unexpected_response_status"
    assert EVALUATION_REASON_INVALID_TEXT_LENGTH == "invalid_text_length"
    assert EVALUATION_REASON_PASSED == "evaluation_passed"
    assert EvaluationDecision is not None
    assert evaluate_response is not None
