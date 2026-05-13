from enum import StrEnum
from pydantic import BaseModel, Field


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
