"""
Runtime policy models.

These models define internal runtime reliability decisions.
They do not enable model, tool, network, or external service execution.
"""

from dataclasses import dataclass
from typing import Literal


RuntimeOutcome = Literal[
    "success",
    "retry",
    "fallback",
    "degraded_response",
    "failure",
]


@dataclass(frozen=True)
class RuntimePolicyDecision:
    """
    Internal runtime policy decision.

    Expected flow:
    - runtime condition is evaluated
    - decision records the safe outcome category
    - trace_id is preserved for internal observability
    - public API contract remains unchanged
    """

    outcome: RuntimeOutcome
    trace_id: str
    reason: str
