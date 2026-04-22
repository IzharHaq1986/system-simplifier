from fastapi import APIRouter, Request

from app.models.request import SimplifyRequest

router = APIRouter()


@router.post("/v1/simplify")
def simplify(request: Request, payload: SimplifyRequest):
    """
    Minimal validation endpoint.

    Business logic is intentionally deferred.
    This route proves that request validation and trace propagation are active.
    """
    return {
        "status": "accepted",
        "text_length": len(payload.text),
        "trace_id": request.state.trace_id,
    }
