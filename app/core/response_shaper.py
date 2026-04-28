from app.execution.result import ExecutionResult
from app.models.response import SimplifyResponse


def shape_simplify_response(
    execution_result: ExecutionResult,
    text_length: int,
    trace_id: str,
) -> SimplifyResponse:
    """
    Convert internal execution result into the public API response.

    This is the only place allowed to construct SimplifyResponse.
    Internal execution details must not leak outside this boundary.
    """

    # ExecutionResult is currently a no-op placeholder.
    # Enforce expected internal contract explicitly.
    if (
        execution_result.status != "success"
        or execution_result.mode != "no_op"
        or execution_result.reason_code != "execution_prepared"
    ):
        raise ValueError("Unexpected execution result state.")

    return SimplifyResponse(
        status="accepted",
        text_length=text_length,
        trace_id=trace_id,
    )
