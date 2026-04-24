from typing import Literal

from pydantic import BaseModel


class ExecutionDecision(BaseModel):
    # Internal execution boundary result.
    # This prepares the system for future model or tool execution without adding execution yet.
    decision: Literal["proceed"]
    mode: Literal["no_op"]
    reason_code: Literal["policy_allowed"]
