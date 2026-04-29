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

    Current minimum rule:
    a response must contain a trace ID.
    """

    if not response.trace_id:
        return EvaluationDecision(
            allowed=False,
            reason="missing_trace_id",
            rule_version=EVALUATION_RULE_VERSION,
        )

    return EvaluationDecision(
        allowed=True,
        reason="evaluation_passed",
        rule_version=EVALUATION_RULE_VERSION,
    )
