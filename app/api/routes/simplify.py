from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.input_guardrails import get_input_rejection_reason
from app.execution.decision import build_execution_decision
from app.models.error import ErrorResponse
from app.models.request import SimplifyRequest
from app.models.response import SimplifyResponse
from app.policy.evaluator import evaluate_policy
from app.execution.result import build_execution_result

router = APIRouter()


@router.post(
    "/v1/simplify",
    response_model=SimplifyResponse,
    responses={
        403: {
            "model": ErrorResponse,
            "description": "Request denied by policy boundary.",
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid input rejected by validation or deterministic guardrails.",
        },
    },
)
def simplify(request: Request, payload: SimplifyRequest):
    """
    Minimal validation endpoint with deterministic policy and execution decisions.
    """
    rejection_reason = get_input_rejection_reason(payload.text)

    if rejection_reason:
        error_response = ErrorResponse(
            error={
                "code": "invalid_input",
                "message": rejection_reason,
            },
            trace_id=request.state.trace_id,
        )

        return JSONResponse(
            status_code=422,
            content=error_response.model_dump(),
        )

    # Policy evaluation runs only after validation and guardrails succeed.
    # This keeps input control separate from execution control.
    policy_decision = evaluate_policy(payload.text)

    if policy_decision.decision == "deny":
        error_response = ErrorResponse(
            error={
                "code": "policy_denied",
                "message": "Request denied by policy.",
            },
            trace_id=request.state.trace_id,
        )

        return JSONResponse(
            status_code=403,
            content=error_response.model_dump(),
        )

    # Build the execution decision only after policy allows the request.
    # This prepares the route for future execution without running models or tools.
    execution_decision = build_execution_decision()
    _ = execution_decision

     # Build the no-op execution result after the execution decision.
    # This records the prepared execution outcome without running models or tools.
    execution_result = build_execution_result()
    _ = execution_result

    return SimplifyResponse(
        status="accepted",
        text_length=len(payload.text),
        trace_id=request.state.trace_id,
    )
