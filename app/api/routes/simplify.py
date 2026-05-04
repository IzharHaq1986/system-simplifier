from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.input_guardrails import get_input_rejection_reason
from app.core.response_shaper import shape_simplify_response
from app.evaluation import evaluate_response
from app.execution import build_execution_adapter
from app.execution.decision import build_execution_decision
from app.models.error import ErrorResponse
from app.models.request import SimplifyRequest
from app.models.response import SimplifyResponse
from app.observability.factory import build_telemetry_sink
from app.policy.evaluator import evaluate_policy
from app.response_policy.evaluator import evaluate_response_policy
from app.telemetry.builder import build_execution_telemetry_event
from app.telemetry.formatter import format_execution_telemetry_event
from app.telemetry.sink import emit_execution_telemetry

router = APIRouter()

telemetry_sink = build_telemetry_sink()


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
        500: {
            "model": ErrorResponse,
            "description": "Response denied by response policy boundary.",
        },
    },
)
def simplify(request: Request, payload: SimplifyRequest) -> SimplifyResponse | JSONResponse:
    """
    Accept a simplify request through explicit validation, guardrail,
    policy, execution-decision, execution-result, response-shaping,
    response-policy, evaluation, telemetry, and observability boundaries.

    No model, tool, network, or external service execution happens here.
    """

    trace_id = request.state.trace_id

    rejection_reason = get_input_rejection_reason(payload.text)

    if rejection_reason:
        error_response = ErrorResponse(
            error={
                "code": "invalid_input",
                "message": rejection_reason,
            },
            trace_id=trace_id,
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
            trace_id=trace_id,
        )

        return JSONResponse(
            status_code=403,
            content=error_response.model_dump(),
        )

    execution_decision = build_execution_decision()

    # Execution is routed through the controlled adapter selector.
    # The active adapter remains NoOpExecutionAdapter, so no model, tool,
    # network, or external service execution is introduced.
    execution_adapter = build_execution_adapter()
    execution_result = execution_adapter.execute(
        text=payload.text,
        trace_id=trace_id,
    )

    shaped_response = shape_simplify_response(
        execution_result=execution_result,
        text_length=len(payload.text),
        trace_id=trace_id,
    )

    response_policy_decision = evaluate_response_policy(shaped_response)

    if response_policy_decision.decision == "deny":
        error_response = ErrorResponse(
            error={
                "code": "response_policy_denied",
                "message": "Response denied by response policy.",
            },
            trace_id=trace_id,
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(),
        )

    # Evaluation remains non-blocking. Its result is recorded only in telemetry.
    evaluation_decision = evaluate_response(shaped_response)

    telemetry_event = build_execution_telemetry_event(
        trace_id=trace_id,
        decision=execution_decision,
        result=execution_result,
        text_length=len(payload.text),
    )

    formatted_telemetry = format_execution_telemetry_event(telemetry_event)

    api_telemetry = {
        "event_type": "simplify.execution",
        "status": formatted_telemetry["execution_status"],
        "trace_id": formatted_telemetry["trace_id"],
        "text_length": formatted_telemetry["text_length"],
        "evaluation_allowed": evaluation_decision.allowed,
        "evaluation_reason": evaluation_decision.reason,
    }

    telemetry_sink.emit(api_telemetry)
    emit_execution_telemetry(telemetry_event)

    return shaped_response
