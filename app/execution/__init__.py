"""
Execution package exports.
"""

from app.execution.adapter_protocol import ExecutionAdapter
from app.execution.adapter_selector import (
    EXECUTION_ADAPTER_MODE,
    build_execution_adapter,
)
from app.execution.mode import ALLOWED_EXECUTION_MODES, validate_execution_mode
from app.execution.no_op_adapter import NoOpExecutionAdapter
from app.execution.result import ExecutionResult, build_execution_result
from app.execution.feature_gate import ENABLE_NON_NO_OP_EXECUTION

__all__ = [
    "ALLOWED_EXECUTION_MODES",
    "EXECUTION_ADAPTER_MODE",
    "ExecutionAdapter",
    "ExecutionResult",
    "NoOpExecutionAdapter",
    "build_execution_adapter",
    "build_execution_result",
    "validate_execution_mode",
    "ENABLE_NON_NO_OP_EXECUTION",
]
