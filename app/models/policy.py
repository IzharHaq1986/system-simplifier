from typing import Literal

from pydantic import BaseModel


class PolicyDecision(BaseModel):
    # Internal result for the policy boundary.
    # This keeps allow/deny behavior typed, explicit, and easy to test.
    decision: Literal["allow", "deny"]
    reason_code: Literal["allowed", "policy_blocked_term"]
