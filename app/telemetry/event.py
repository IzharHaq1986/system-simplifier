from typing import Literal

from pydantic import BaseModel


class TelemetryEvent(BaseModel):
    """
    Internal telemetry envelope for recording execution metadata.

    This model is internal only and must not be returned through the public API.
    """

    event_type: Literal["execution_result_recorded"]
    trace_id: str
    status: Literal["success"]
    mode: Literal["no_op"]
    reason_code: Literal["execution_prepared"]
