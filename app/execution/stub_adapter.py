"""
Stub execution adapter.

This adapter is intentionally disabled and not reachable through
the adapter selector. It exists only to prepare the system for
future controlled execution modes.
"""

from app.execution.adapter_protocol import ExecutionAdapter
from app.execution.result import ExecutionResult

class StubExecutionAdapter(ExecutionAdapter):
    """
    Placeholder adapter for future execution modes.

    Expected flow:
    - Selector does NOT route to this adapter.
    - Adapter should never be executed in current phase.
    - If executed, it fails explicitly to protect system guarantees.
    """

    def execute(
        self,
        text: str,
        trace_id: str,
    ) -> ExecutionResult:
        """
        This adapter must not be used in current system state.
        """
        raise RuntimeError("StubExecutionAdapter is not enabled")
