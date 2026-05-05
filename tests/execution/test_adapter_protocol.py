from app.execution import ExecutionAdapter, NoOpExecutionAdapter


def test_no_op_adapter_satisfies_execution_adapter_protocol() -> None:
    adapter: ExecutionAdapter = NoOpExecutionAdapter()

    result = adapter.execute(
        text="hello",
        trace_id="test-trace-id",
    )

    assert result.status == "success"
