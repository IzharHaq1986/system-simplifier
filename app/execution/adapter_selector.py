"""
Execution adapter selection.

This module centralizes adapter selection so route code does not need to know
which concrete adapter is currently active.
"""

from app.execution.no_op_adapter import NoOpExecutionAdapter
from app.execution.adapter import ExecutionAdapter


def build_execution_adapter() -> ExecutionAdapter:
    """
    Build the active execution adapter.

    The system currently allows only the no-op adapter. This keeps execution
    deterministic and prevents model, tool, or network calls from entering the
    request path prematurely.
    """
    return NoOpExecutionAdapter()
