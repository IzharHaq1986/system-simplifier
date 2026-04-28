from typing import Literal

from pydantic import BaseModel


class ExecutionResult(BaseModel):
    # Internal execution result envelope.
    # This represents the outcome of the execution decision without invoking models or tools.
    status: Literal["success"]
    mode: Literal["no_op"]
    reason_code: Literal["execution_prepared"]
