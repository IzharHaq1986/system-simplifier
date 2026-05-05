from typing import Protocol

from app.execution.result import ExecutionResult


class ExecutionAdapter(Protocol):
    """Contract required by all execution adapters."""

    def execute(self, text: str) -> ExecutionResult:
        """Execute the adapter behavior and return a typed execution result."""
        ...
