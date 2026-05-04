"""
Execution boundary package exports.
"""

from app.execution.adapter import ExecutionAdapter
from app.execution.no_op_adapter import NoOpExecutionAdapter
from app.execution.result import ExecutionResult

__all__ = [
    "ExecutionAdapter",
    "ExecutionResult",
    "NoOpExecutionAdapter",
]
