from app.models.response import SimplifyResponse
from app.response_policy.decision import ResponsePolicyDecision


def evaluate_response_policy(response: SimplifyResponse) -> ResponsePolicyDecision:
    """
    Evaluate the public response contract before it leaves the system.

    Valid responses must preserve traceability and must not expose internal
    execution fields.
    """
    if not response.trace_id:
        return ResponsePolicyDecision(
            decision="deny",
            reason_code="response_contract_denied",
        )

    if hasattr(response, "mode") or hasattr(response, "reason_code"):
        return ResponsePolicyDecision(
            decision="deny",
            reason_code="response_contract_denied",
        )

    return ResponsePolicyDecision(
        decision="allow",
        reason_code="response_contract_allowed",
    )
