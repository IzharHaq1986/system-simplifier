"""
No-op execution adapter.

This adapter satisfies the execution boundary without introducing model,
tool, network, or external service execution.
"""

from app.execution.adapter_protocol import ExecutionAdapter
from app.execution.result import ExecutionResult, build_execution_result


class NoOpExecutionAdapter(ExecutionAdapter):
    """
    Controlled execution adapter for the current phase.

    Expected flow:
    - Route or orchestration code provides text and trace_id.
    - Adapter accepts the execution request.
    - Adapter returns the existing no-op execution result envelope.
    - No external execution is performed.
    """

    def execute(
        self,
        text: str,
        trace_id: str,
    ) -> ExecutionResult:
        """
        Return the deterministic no-op execution result.

        The input values are accepted at the adapter boundary for future
        execution modes, but they are intentionally unused while execution
        remains no-op.
        """
        _ = text
        _ = trace_id

        return build_execution_result()
