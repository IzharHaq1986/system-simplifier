"""
Pure evaluation boundary.

This evaluator performs deterministic post-response checks.
It does not call models, tools, external services, telemetry systems,
or control-flow enforcement code.
"""

# Centralized evaluation imports (stable contract)
from app.evaluation import (
    EVALUATION_REASON_INVALID_TEXT_LENGTH,
    EVALUATION_REASON_MISSING_TRACE_ID,
    EVALUATION_REASON_PASSED,
    EVALUATION_REASON_UNEXPECTED_STATUS,
    EVALUATION_RULE_VERSION,
    EvaluationDecision,
)
from app.models.response import SimplifyResponse

def evaluate_response(
    response: SimplifyResponse,
) -> EvaluationDecision:
    """
    Evaluate a shaped response before telemetry emission.

    Current rules:
    - response must contain a trace ID
    - response status must be "success"
    - response text_length must be greater than 0
    """

    if not response.trace_id:
        return EvaluationDecision(
            allowed=False,
            reason=EVALUATION_REASON_MISSING_TRACE_ID,
            rule_version=EVALUATION_RULE_VERSION,
        )

    if response.status != "success":
        return EvaluationDecision(
            allowed=False,
            reason=EVALUATION_REASON_UNEXPECTED_STATUS,
            rule_version=EVALUATION_RULE_VERSION,
        )

    if response.text_length <= 0:
        return EvaluationDecision(
            allowed=False,
            reason=EVALUATION_REASON_INVALID_TEXT_LENGTH,
            rule_version=EVALUATION_RULE_VERSION,
        )

    return EvaluationDecision(
        allowed=True,
        reason=EVALUATION_REASON_PASSED,
        rule_version=EVALUATION_RULE_VERSION,
    )
