"""
Execution mode validation.

This module defines the allowed execution modes for controlled execution
evolution. It does not enable model, tool, network, or external execution.
"""

ALLOWED_EXECUTION_MODES = {"no_op"}


def validate_execution_mode(mode: str) -> str:
    """
    Validate an execution mode before adapter selection.

    Expected flow:
    - caller provides a mode string
    - mode is checked against the allowed set
    - valid mode is returned unchanged
    - unknown modes fail closed
    """

    if mode not in ALLOWED_EXECUTION_MODES:
        raise ValueError(f"Unsupported execution mode: {mode}")

    return mode
