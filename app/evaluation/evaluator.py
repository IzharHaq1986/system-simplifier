"""
Pure evaluation boundary.

This evaluator performs deterministic post-response checks.
It does not call models, tools, external services, or telemetry systems.
"""

from app.evaluation.decision import EvaluationDecision
from app.models.response import SimplifyResponse


def evaluate_response(
    response: SimplifyResponse,
) -> EvaluationDecision:
    """
    Evaluate a shaped response before future externalization.

    The current minimum rule is intentionally small:
    a response must contain a trace ID.
    """

    if not response.trace_id:
        return EvaluationDecision(
            allowed=False,
            reason="missing_trace_id",
        )

    return EvaluationDecision(
        allowed=True,
        reason="evaluation_passed",
    )
