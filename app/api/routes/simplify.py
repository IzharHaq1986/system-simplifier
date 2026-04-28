from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.input_guardrails import get_input_rejection_reason
from app.core.response_shaper import shape_simplify_response
from app.execution.decision import build_execution_decision
from app.execution.result import build_execution_result
from app.models.error import ErrorResponse
from app.models.request import SimplifyRequest
from app.models.response import SimplifyResponse
from app.policy.evaluator import evaluate_policy

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
def simplify(request: Request, payload: SimplifyRequest) -> SimplifyResponse | JSONResponse:
    """
    Accept a simplify request through explicit validation, guardrail,
    policy, execution-decision, execution-result, and response-shaping
    boundaries.

    No model or tool execution happens in this route yet.
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

    execution_decision = build_execution_decision()
    _ = execution_decision

    execution_result = build_execution_result()

    return shape_simplify_response(
        execution_result=execution_result,
        text_length=len(payload.text),
        trace_id=request.state.trace_id,
    )
