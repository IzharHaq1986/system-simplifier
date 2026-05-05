"""
Execution adapter selection.

This module centralizes adapter selection so route code does not need to know
which concrete adapter is currently active.
"""

from app.execution.adapter_protocol import ExecutionAdapter
from app.execution.mode import validate_execution_mode
from app.execution.no_op_adapter import NoOpExecutionAdapter


# Explicit execution mode for controlled integration.
# This remains fixed to "no_op" until real execution is introduced.
EXECUTION_ADAPTER_MODE = "no_op"


def build_execution_adapter() -> ExecutionAdapter:
    """
    Build the active execution adapter.

    Expected flow:
    - adapter mode is validated before adapter selection
    - selector returns the no-op adapter
    - execution stays deterministic
    - no model, tool, network, or external service call is introduced
    """

    validated_mode = validate_execution_mode(EXECUTION_ADAPTER_MODE)

    if validated_mode == "no_op":
        return NoOpExecutionAdapter()

    raise ValueError(f"Unsupported execution mode: {validated_mode}")
