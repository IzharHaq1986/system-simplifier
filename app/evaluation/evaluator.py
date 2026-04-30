"""
Pure evaluation boundary.

This evaluator performs deterministic post-response checks.
It does not call models, tools, external services, telemetry systems,
or control-flow enforcement code.
"""

from app.evaluation.decision import EvaluationDecision
from app.models.response import SimplifyResponse


EVALUATION_RULE_VERSION = "v1"


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
            reason="missing_trace_id",
            rule_version=EVALUATION_RULE_VERSION,
        )

    if response.status != "success":
        return EvaluationDecision(
            allowed=False,
            reason="unexpected_response_status",
            rule_version=EVALUATION_RULE_VERSION,
        )

    if response.text_length <= 0:
        return EvaluationDecision(
            allowed=False,
            reason="invalid_text_length",
            rule_version=EVALUATION_RULE_VERSION,
        )

    return EvaluationDecision(
        allowed=True,
        reason="evaluation_passed",
        rule_version=EVALUATION_RULE_VERSION,
    )
