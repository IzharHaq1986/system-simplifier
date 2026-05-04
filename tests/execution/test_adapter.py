from app.execution import ExecutionAdapter, ExecutionResult


class StaticExecutionAdapter:
    """
    Test adapter used to verify the execution boundary contract.

    Expected flow:
    - adapter receives text and trace_id
    - adapter returns the existing typed ExecutionResult envelope
    - no external execution is performed
    """

    def execute(
        self,
        text: str,
        trace_id: str,
    ) -> ExecutionResult:
        # Inputs are accepted by the adapter boundary.
        # The current phase still returns a no-op execution envelope.
        _ = text
        _ = trace_id

        return ExecutionResult(
            status="success",
            mode="no_op",
            reason_code="execution_prepared",
        )


def test_execution_adapter_contract_returns_typed_result() -> None:
    adapter: ExecutionAdapter = StaticExecutionAdapter()

    result = adapter.execute(
        text="Controlled execution boundary test.",
        trace_id="trace-123",
    )

    assert result.status == "success"
    assert result.mode == "no_op"
    assert result.reason_code == "execution_prepared"
