"""
Typed evaluation decision model.

Evaluation is internal and non-blocking.
It describes response correctness signals without controlling API flow.
"""

from pydantic import BaseModel, ConfigDict


class EvaluationDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed: bool
    reason: str
    rule_version: str
