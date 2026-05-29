import pytest
from pydantic import ValidationError

from app.evaluation import EVALUATION_RULE_VERSION
from app.evaluation.decision import EvaluationDecision
from app.evaluation.quality import (
    QualitySignal,
    QualitySignalStatus,
    build_quality_signal,
    build_quality_signal_from_evaluation,
    build_quality_signal_payload,
    format_quality_signal,
    is_acceptable_quality_signal,
    is_blocked_quality_signal,
    is_needs_review_quality_signal,
    serialize_quality_signal,
    summarize_quality_signal,
    normalize_quality_signal_text,
    quality_signals_match,
    get_quality_signal_priority,
    get_highest_priority_quality_signal,
    format_quality_signal_for_observability,
)


def test_quality_signal_accepts_valid_internal_signal():
    signal = QualitySignal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="Response passed deterministic quality checks.",
    )

    assert signal.status == QualitySignalStatus.ACCEPTABLE
    assert signal.source == "evaluation"
    assert signal.reason == "Response passed deterministic quality checks."


@pytest.mark.parametrize("field_name", ["source", "reason"])
def test_quality_signal_rejects_empty_text_fields(field_name):
    payload = {
        "status": QualitySignalStatus.NEEDS_REVIEW,
        "source": "evaluation",
        "reason": "Fallback path requires review.",
    }
    payload[field_name] = ""

    with pytest.raises(ValidationError):
        QualitySignal(**payload)


def test_quality_signal_rejects_invalid_status():
    with pytest.raises(ValidationError):
        QualitySignal(
            status="unknown",
            source="evaluation",
            reason="Invalid status should fail closed.",
        )


def test_build_quality_signal_returns_internal_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="response_policy",
        reason="Public response boundary validation failed.",
    )

    assert signal.status == QualitySignalStatus.BLOCKED
    assert signal.source == "response_policy"
    assert signal.reason == "Public response boundary validation failed."


def test_build_quality_signal_from_allowed_evaluation_decision():
    decision = EvaluationDecision(
        allowed=True,
        reason="Response passed deterministic evaluation.",
        rule_version=EVALUATION_RULE_VERSION,
    )

    signal = build_quality_signal_from_evaluation(decision=decision)

    assert signal.status == QualitySignalStatus.ACCEPTABLE
    assert signal.source == "evaluation"
    assert signal.reason == "Response passed deterministic evaluation."


def test_build_quality_signal_from_blocked_evaluation_decision():
    decision = EvaluationDecision(
        allowed=False,
        reason="Response failed deterministic evaluation.",
        rule_version=EVALUATION_RULE_VERSION,
    )

    signal = build_quality_signal_from_evaluation(
        decision=decision,
        source="response_policy",
    )

    assert signal.status == QualitySignalStatus.BLOCKED
    assert signal.source == "response_policy"
    assert signal.reason == "Response failed deterministic evaluation."


def test_quality_signal_from_evaluation_accepts_allowed_decision():
    decision = EvaluationDecision(
        allowed=True,
        reason="evaluation passed",
        rule_version=EVALUATION_RULE_VERSION,
    )

    signal = build_quality_signal_from_evaluation(decision=decision)

    assert signal.status == QualitySignalStatus.ACCEPTABLE
    assert signal.source == "evaluation"


def test_quality_signal_from_evaluation_blocks_denied_decision():
    decision = EvaluationDecision(
        allowed=False,
        reason="evaluation failed",
        rule_version=EVALUATION_RULE_VERSION,
    )

    signal = build_quality_signal_from_evaluation(decision=decision)

    assert signal.status == QualitySignalStatus.BLOCKED
    assert signal.source == "evaluation"


def test_quality_signal_payload_contains_internal_quality_fields():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    payload = build_quality_signal_payload(signal=signal)

    assert payload == {
        "quality_status": "acceptable",
        "quality_source": "evaluation",
    }


def test_format_quality_signal_returns_deterministic_text():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    formatted = format_quality_signal(signal=signal)

    assert formatted == (
        "quality_status=acceptable "
        "quality_source=evaluation "
        "quality_reason=evaluation passed"
    )


def test_summarize_quality_signal_returns_deterministic_payload():
    signal = build_quality_signal(
        status=QualitySignalStatus.NEEDS_REVIEW,
        source="evaluation",
        reason="length warning",
    )

    summary = summarize_quality_signal(signal=signal)

    assert summary == {
        "status": "needs_review",
        "source": "evaluation",
        "reason": "length warning",
    }


def test_is_blocked_quality_signal_returns_true_for_blocked_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="evaluation",
        reason="policy denied",
    )

    assert is_blocked_quality_signal(signal=signal) is True


def test_is_blocked_quality_signal_returns_false_for_non_blocked_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    assert is_blocked_quality_signal(signal=signal) is False


def test_is_needs_review_quality_signal_returns_true_for_review_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.NEEDS_REVIEW,
        source="evaluation",
        reason="length warning",
    )

    assert is_needs_review_quality_signal(signal=signal) is True


def test_is_needs_review_quality_signal_returns_false_for_non_review_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    assert is_needs_review_quality_signal(signal=signal) is False


def test_is_acceptable_quality_signal_returns_true_for_acceptable_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    assert is_acceptable_quality_signal(signal=signal) is True


def test_is_acceptable_quality_signal_returns_false_for_non_acceptable_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="evaluation",
        reason="policy denied",
    )

    assert is_acceptable_quality_signal(signal=signal) is False


def test_serialize_quality_signal_returns_deterministic_payload():
    signal = QualitySignal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="quality signal is acceptable",
        score=100,
    )

    payload = serialize_quality_signal(signal)

    assert payload == {
        "status": "acceptable",
        "source": "evaluation",
        "reason": "quality signal is acceptable",
        "score": 100,
    }

def test_normalize_quality_signal_text_collapses_extra_whitespace():
    normalized = normalize_quality_signal_text(
        "  evaluation   passed   deterministic   checks  "
    )

    assert normalized == "evaluation passed deterministic checks"


def test_build_quality_signal_normalizes_internal_text_fields():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="  evaluation  ",
        reason="  evaluation   passed  ",
    )

    assert signal.source == "evaluation"
    assert signal.reason == "evaluation passed"

def test_quality_signals_match_returns_true_for_matching_signals():
    left = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
        score=100,
    )
    right = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
        score=100,
    )

    assert quality_signals_match(left=left, right=right) is True


def test_quality_signals_match_returns_false_for_different_signals():
    left = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
        score=100,
    )
    right = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="evaluation",
        reason="policy denied",
        score=0,
    )

    assert quality_signals_match(left=left, right=right) is False

def test_get_quality_signal_priority_returns_zero_for_acceptable_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )

    assert get_quality_signal_priority(signal=signal) == 0


def test_get_quality_signal_priority_returns_one_for_review_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.NEEDS_REVIEW,
        source="evaluation",
        reason="manual review needed",
    )

    assert get_quality_signal_priority(signal=signal) == 1


def test_get_quality_signal_priority_returns_two_for_blocked_signal():
    signal = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="evaluation",
        reason="policy denied",
    )

    assert get_quality_signal_priority(signal=signal) == 2

def test_get_highest_priority_quality_signal_returns_most_urgent_signal():
    acceptable = build_quality_signal(
        status=QualitySignalStatus.ACCEPTABLE,
        source="evaluation",
        reason="evaluation passed",
    )
    blocked = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="evaluation",
        reason="policy denied",
        score=0,
    )
    needs_review = build_quality_signal(
        status=QualitySignalStatus.NEEDS_REVIEW,
        source="evaluation",
        reason="manual review needed",
    )

    highest_priority = get_highest_priority_quality_signal(
        signals=[acceptable, blocked, needs_review],
    )

    assert highest_priority == blocked


def test_get_highest_priority_quality_signal_returns_none_for_empty_list():
    highest_priority = get_highest_priority_quality_signal(signals=[])

    assert highest_priority is None

def test_format_quality_signal_for_observability_returns_deterministic_text():
    signal = build_quality_signal(
        status=QualitySignalStatus.NEEDS_REVIEW,
        source="evaluation",
        reason="manual review needed",
    )

    formatted = format_quality_signal_for_observability(signal=signal)

    assert formatted == (
        "quality_status=needs_review "
        "quality_source=evaluation "
        "quality_priority=1 "
        "quality_reason=manual review needed"
    )


def test_format_quality_signal_for_observability_uses_blocked_priority():
    signal = build_quality_signal(
        status=QualitySignalStatus.BLOCKED,
        source="response_policy",
        reason="policy denied",
        score=0,
    )

    formatted = format_quality_signal_for_observability(signal=signal)

    assert formatted == (
        "quality_status=blocked "
        "quality_source=response_policy "
        "quality_priority=2 "
        "quality_reason=policy denied"
    )
