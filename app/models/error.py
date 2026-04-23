from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """
    Stable error detail contract for client-facing failures.
    """

    code: str = Field(
        ...,
        min_length=1,
        description="Machine-readable error code.",
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Short human-readable error message.",
    )


class ErrorResponse(BaseModel):
    """
    Stable error response contract for rejected requests.
    """

    error: ErrorDetail
    trace_id: str = Field(
        ...,
        min_length=1,
        description="Request trace identifier for correlation.",
    )
