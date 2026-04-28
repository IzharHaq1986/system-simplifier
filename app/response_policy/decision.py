from typing import Literal

from pydantic import BaseModel


class ResponsePolicyDecision(BaseModel):
    """
    Typed decision returned by the response policy boundary.

    This model does not enforce behavior by itself. It only defines the
    contract that future response policy checks must return.
    """

    decision: Literal["allow", "deny"]
    reason_code: Literal["response_contract_allowed", "response_contract_denied"]
