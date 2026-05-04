"""
Execution boundary package exports.
"""

from app.execution.adapter import ExecutionAdapter
from app.execution.no_op_adapter import NoOpExecutionAdapter
from app.execution.result import ExecutionResult
from app.execution.adapter_selector import build_execution_adapter

__all__ = [
    "ExecutionAdapter",
    "ExecutionResult",
    "NoOpExecutionAdapter",
    "build_execution_adapter",
]
