"""
No-op execution adapter.

This adapter satisfies the execution boundary without introducing model,
tool, network, or external service execution.
"""

from app.execution.result import ExecutionResult, build_execution_result


class NoOpExecutionAdapter:
    """
    Controlled execution adapter for the current phase.

    Expected flow:
    - route or orchestration code provides text and trace_id
    - adapter accepts the execution request
    - adapter returns the existing no-op execution result envelope
    - no external execution is performed
    """

    def execute(
        self,
        text: str,
        trace_id: str,
    ) -> ExecutionResult:
        # Inputs are accepted at the adapter boundary for future execution.
        # They are intentionally unused while execution remains no-op.
        _ = text
        _ = trace_id

        return build_execution_result()
