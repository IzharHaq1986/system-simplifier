from pydantic import BaseModel, Field, field_validator


class SimplifyRequest(BaseModel):
    """
    Baseline request contract for the system simplifier.

    Adds minimal input guardrails:
    - normalize whitespace
    - reject empty input after normalization
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Input text to be processed by the system simplifier.",
    )

    @field_validator("text")
    @classmethod
    def normalize_and_validate_text(cls, value: str) -> str:
        # Normalize leading/trailing whitespace
        normalized = value.strip()

        # Reject empty or whitespace-only input
        if not normalized:
            raise ValueError("Input text cannot be empty.")

        return normalized
