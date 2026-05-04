"""
Execution adapter selection.

This module centralizes adapter selection so route code does not need to know
which concrete adapter is currently active.
"""

from app.execution.adapter import ExecutionAdapter
from app.execution.no_op_adapter import NoOpExecutionAdapter


# Explicit execution mode for controlled integration.
# This remains fixed to "no_op" until real execution is introduced.
EXECUTION_ADAPTER_MODE = "no_op"


def build_execution_adapter() -> ExecutionAdapter:
    """
    Build the active execution adapter.

    Expected flow:
    - adapter mode remains explicit
    - selector returns the no-op adapter
    - execution stays deterministic
    - no model, tool, network, or external service call is introduced
    """

    return NoOpExecutionAdapter()
