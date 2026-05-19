from app.evaluation import (
    EVALUATION_REASON_INVALID_TEXT_LENGTH,
    EVALUATION_REASON_MISSING_TRACE_ID,
    EVALUATION_REASON_PASSED,
    EVALUATION_REASON_UNEXPECTED_STATUS,
    EVALUATION_RULE_VERSION,
    EvaluationDecision,
    evaluate_response,
    QualitySignal,
    QualitySignalStatus,
    build_quality_signal,
    build_quality_signal_from_evaluation,
    build_quality_signal_payload,
    summarize_quality_signal,
    format_quality_signal,
    is_blocked_quality_signal,
    is_needs_review_quality_signal,
    serialize_quality_signal,
    normalize_quality_signal_text,
    quality_signals_match,
)


def test_evaluation_package_exports_stable_contracts() -> None:
    assert EVALUATION_RULE_VERSION == "v1"
    assert EVALUATION_REASON_MISSING_TRACE_ID == "missing_trace_id"
    assert EVALUATION_REASON_UNEXPECTED_STATUS == "unexpected_response_status"
    assert EVALUATION_REASON_INVALID_TEXT_LENGTH == "invalid_text_length"
    assert EVALUATION_REASON_PASSED == "evaluation_passed"
    assert EvaluationDecision is not None
    assert evaluate_response is not None
    assert QualitySignal is not None
    assert QualitySignalStatus is not None
    assert build_quality_signal is not None
    assert build_quality_signal_from_evaluation is not None
    assert build_quality_signal_payload is not None
    assert format_quality_signal is not None
    assert summarize_quality_signal is not None
    assert is_blocked_quality_signal is not None
    assert is_needs_review_quality_signal is not None
    assert serialize_quality_signal is not None
    assert normalize_quality_signal_text is not None
    assert quality_signals_match is not None
