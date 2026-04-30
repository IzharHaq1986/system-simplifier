"""
Pure evaluation boundary.

This evaluator performs deterministic post-response checks.
It does not call models, tools, external services, telemetry systems,
or control-flow enforcement code.
"""

from app.evaluation.decision import EvaluationDecision
from app.models.response import SimplifyResponse


EVALUATION_RULE_VERSION = "v1"
EVALUATION_REASON_MISSING_TRACE_ID = "missing_trace_id"
EVALUATION_REASON_UNEXPECTED_STATUS = "unexpected_response_status"
EVALUATION_REASON_INVALID_TEXT_LENGTH = "invalid_text_length"
EVALUATION_REASON_PASSED = "evaluation_passed"

def evaluate_response(
    response: SimplifyResponse,
) -> EvaluationDecision:
    """
    Evaluate a shaped response before telemetry emission.

    Current rules:
    - response must contain a trace ID
    - response status must be "success"
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
