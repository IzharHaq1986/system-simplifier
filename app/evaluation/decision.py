from pydantic import BaseModel, Field


class EvaluationDecision(BaseModel):
    """
    Internal evaluation decision.

    This model is not exposed through API responses.
    """

    allowed: bool = Field(
        description="Whether the response passed deterministic evaluation checks.",
    )

    reason: str = Field(
        description="Stable internal reason for the evaluation decision.",
    )
