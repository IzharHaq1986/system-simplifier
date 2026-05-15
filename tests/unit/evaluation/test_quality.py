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
    summarize_quality_signal,
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

    signal = build_quality_signal_from_evaluation(
        decision=decision,
    )

    assert signal.status == QualitySignalStatus.ACCEPTABLE
    assert signal.source == "evaluation"

def test_quality_signal_from_evaluation_blocks_denied_decision():
    decision = EvaluationDecision(
        allowed=False,
        reason="evaluation failed",
        rule_version=EVALUATION_RULE_VERSION,
    )

    signal = build_quality_signal_from_evaluation(
        decision=decision,
    )

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
