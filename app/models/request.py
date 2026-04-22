from pydantic import BaseModel, Field


class SimplifyRequest(BaseModel):
    """
    Baseline request contract for the system simplifier.
    Keeps the first input surface small and explicit.
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Input text to be processed by the system simplifier.",
    )
