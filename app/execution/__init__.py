"""
Execution boundary package exports.
"""

from app.execution.adapter import ExecutionAdapter
from app.execution.no_op_adapter import NoOpExecutionAdapter
from app.execution.result import ExecutionResult
from app.execution.adapter_selector import build_execution_adapter
from app.execution.adapter_selector import EXECUTION_ADAPTER_MODE
from app.execution.mode import ALLOWED_EXECUTION_MODES, validate_execution_mode

__all__ = [
    "ExecutionAdapter",
    "ExecutionResult",
    "NoOpExecutionAdapter",
    "build_execution_adapter",
    "EXECUTION_ADAPTER_MODE",
    "ALLOWED_EXECUTION_MODES",
    "validate_execution_mode",
]
