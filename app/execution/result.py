from app.models.execution_result import ExecutionResult


def build_execution_result() -> ExecutionResult:
    # This envelope represents a completed no-op execution result.
    # No model or tool execution is performed in this phase.
    return ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )
