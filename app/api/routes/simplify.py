from fastapi import APIRouter, HTTPException, Request

from app.core.input_guardrails import get_input_rejection_reason
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
        raise HTTPException(status_code=422, detail=rejection_reason)

    return SimplifyResponse(
        status="accepted",
        text_length=len(payload.text),
        trace_id=request.state.trace_id,
    )
