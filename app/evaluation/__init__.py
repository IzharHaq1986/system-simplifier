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


__all__ = [
    "EVALUATION_REASON_INVALID_TEXT_LENGTH",
    "EVALUATION_REASON_MISSING_TRACE_ID",
    "EVALUATION_REASON_PASSED",
    "EVALUATION_REASON_UNEXPECTED_STATUS",
    "EVALUATION_RULE_VERSION",
    "EvaluationDecision",
    "evaluate_response",
]
