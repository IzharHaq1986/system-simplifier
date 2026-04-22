from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Basic health endpoint.
    Used for smoke validation, CI checks, and future observability hooks.
    """
    return {"status": "ok"}
