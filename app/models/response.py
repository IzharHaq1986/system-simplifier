from pydantic import BaseModel, Field


class SimplifyResponse(BaseModel):
    """
    Baseline response contract for the simplify endpoint.

    Keeps the external interface explicit, stable, and easy to extend.
    """

    status: str = Field(
        ...,
        description="Processing status for the request.",
    )
    text_length: int = Field(
        ...,
        ge=0,
        description="Length of normalized input text.",
    )
    trace_id: str = Field(
        ...,
        min_length=1,
        description="Request trace identifier for correlation.",
    )
