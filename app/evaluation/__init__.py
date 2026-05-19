"""
Evaluation package exports.

This module exposes stable internal evaluation contracts.
"""

from app.evaluation.constants import (
    EVALUATION_REASON_INVALID_TEXT_LENGTH,
    EVALUATION_REASON_MISSING_TRACE_ID,
    EVALUATION_REASON_PASSED,
    EVALUATION_REASON_UNEXPECTED_STATUS,
    EVALUATION_RULE_VERSION,
)
from app.evaluation.decision import EvaluationDecision
from app.evaluation.evaluator import evaluate_response
from app.evaluation.quality import (
    QualitySignal,
    QualitySignalStatus,
    build_quality_signal,
    build_quality_signal_from_evaluation,
    build_quality_signal_payload,
    format_quality_signal,
    is_blocked_quality_signal,
    summarize_quality_signal,
    is_needs_review_quality_signal,
    serialize_quality_signal,
    normalize_quality_signal_text,
    quality_signals_match,
    get_quality_signal_priority,
)

__all__ = [
    "EVALUATION_REASON_INVALID_TEXT_LENGTH",
    "EVALUATION_REASON_MISSING_TRACE_ID",
    "EVALUATION_REASON_PASSED",
    "EVALUATION_REASON_UNEXPECTED_STATUS",
    "EVALUATION_RULE_VERSION",
    "EvaluationDecision",
    "evaluate_response",
    "QualitySignal",
    "QualitySignalStatus",
    "build_quality_signal",
    "build_quality_signal_from_evaluation",
    "build_quality_signal_payload",
    "format_quality_signal",
    "summarize_quality_signal",
    "is_blocked_quality_signal",
    "is_needs_review_quality_signal",
    "serialize_quality_signal",
    "normalize_quality_signal_text",
    "quality_signals_match",
    "get_quality_signal_priority",
]
