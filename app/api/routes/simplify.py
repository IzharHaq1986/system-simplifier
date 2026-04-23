from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.input_guardrails import get_input_rejection_reason
from app.models.error import ErrorResponse
from app.models.request import SimplifyRequest
from app.models.response import SimplifyResponse

router = APIRouter()


@router.post("/v1/simplify", response_model=SimplifyResponse)
def simplify(request: Request, payload: SimplifyRequest):
    """
    Minimal validation endpoint.

    Business logic is intentionally deferred.
    This route proves that request validation and trace propagation are active.
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

    return SimplifyResponse(
        status="accepted",
        text_length=len(payload.text),
        trace_id=request.state.trace_id,
    )
