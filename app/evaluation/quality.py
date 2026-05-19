from enum import StrEnum

from pydantic import BaseModel, Field

from app.evaluation.decision import EvaluationDecision


class QualitySignalStatus(StrEnum):
    """
    Internal-only quality status used for deterministic review signals.

    This model is not part of the public API response contract.
    """

    ACCEPTABLE = "acceptable"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


class QualitySignal(BaseModel):
    """
    Internal quality signal for future evaluation and review workflows.

    The signal is intentionally small and side-effect free.
    It does not call models, tools, networks, or external systems.
    """

    status: QualitySignalStatus
    source: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    score: int = Field(default=100, ge=0)


def build_quality_signal(
    *,
    status: QualitySignalStatus,
    source: str,
    reason: str,
    score: int = 100,
) -> QualitySignal:
    """
    Build an internal-only quality signal.

    This helper keeps signal creation consistent while preserving
    deterministic, side-effect free behavior.
    """

    return QualitySignal(
        status=status,
        source=source,
        reason=reason,
        score=score,
    )


def build_quality_signal_from_evaluation(
    *,
    decision: EvaluationDecision,
    source: str = "evaluation",
) -> QualitySignal:
    """
    Convert an internal evaluation decision into an internal quality signal.

    This helper is deterministic and side-effect free.
    It does not mutate runtime behavior, telemetry, or public API responses.
    """

    if decision.allowed:
        status = QualitySignalStatus.ACCEPTABLE
        score = 100
    else:
        status = QualitySignalStatus.BLOCKED
        score = 0

    return build_quality_signal(
        status=status,
        source=source,
        reason=decision.reason,
        score=score,
    )


def build_quality_signal_payload(
    *,
    signal: QualitySignal,
) -> dict[str, str]:
    """
    Build an internal-only quality payload for future telemetry preparation.
    """

    return {
        "quality_status": signal.status.value,
        "quality_source": signal.source,
    }


def format_quality_signal(
    *,
    signal: QualitySignal,
) -> str:
    """
    Format an internal quality signal as deterministic text.
    """

    return (
        f"quality_status={signal.status.value} "
        f"quality_source={signal.source} "
        f"quality_reason={signal.reason}"
    )


def summarize_quality_signal(
    *,
    signal: QualitySignal,
) -> dict[str, str]:
    """
    Build a deterministic internal summary for a quality signal.
    """

    return {
        "status": signal.status.value,
        "source": signal.source,
        "reason": signal.reason,
    }


def is_blocked_quality_signal(
    *,
    signal: QualitySignal,
) -> bool:
    """
    Check whether an internal quality signal is blocked.
    """

    return signal.status == QualitySignalStatus.BLOCKED


def is_needs_review_quality_signal(
    *,
    signal: QualitySignal,
) -> bool:
    """
    Check whether an internal quality signal needs review.
    """

    return signal.status == QualitySignalStatus.NEEDS_REVIEW


def is_acceptable_quality_signal(
    *,
    signal: QualitySignal,
) -> bool:
    """
    Check whether an internal quality signal is acceptable.
    """

    return signal.status == QualitySignalStatus.ACCEPTABLE


def serialize_quality_signal(
    signal: QualitySignal,
) -> dict[str, str | int]:
    """
    Convert an internal quality signal into a deterministic dictionary.

    This helper preserves internal-only visibility while keeping
    serialization explicit, stable, and side-effect free.
    """

    return {
        "status": signal.status.value,
        "source": signal.source,
        "reason": signal.reason,
        "score": signal.score,
    }
