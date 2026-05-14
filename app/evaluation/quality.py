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

def build_quality_signal(
    *,
    status: QualitySignalStatus,
    source: str,
    reason: str,
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
    else:
        status = QualitySignalStatus.BLOCKED

    return build_quality_signal(
        status=status,
        source=source,
        reason=decision.reason,
    )

def build_quality_signal_payload(
    *,
    signal: QualitySignal,
) -> dict[str, str]:
    """
    Builds an internal-only quality payload for future telemetry preparation.
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
    Formats an internal quality signal as deterministic text.
    """

    return (
        f"quality_status={signal.status.value} "
        f"quality_source={signal.source} "
        f"quality_reason={signal.reason}"
    )
