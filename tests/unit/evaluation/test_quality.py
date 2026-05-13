import pytest
from pydantic import ValidationError

from app.evaluation.quality import (
    QualitySignal,
    QualitySignalStatus,
    build_quality_signal,
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
