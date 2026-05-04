"""
Execution adapter boundary.

This module defines a narrow interface between internal execution decisions
and future model or tool execution.

No model, tool, network, or external service call is performed here.
"""

from typing import Protocol

from app.execution.result import ExecutionResult


class ExecutionAdapter(Protocol):
    """
    Stable execution adapter contract.

    Expected flow:
    - execution decision is created before this boundary
    - adapter receives controlled input after approval
    - adapter returns a typed execution result
    - route code remains isolated from implementation details
    """

    def execute(
        self,
        text: str,
        trace_id: str,
    ) -> ExecutionResult:
        """
        Execute controlled work and return a typed result.

        Implementations must not leak internal execution details into
        public API responses.
        """
        
