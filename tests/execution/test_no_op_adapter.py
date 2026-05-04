from app.execution import NoOpExecutionAdapter


def test_no_op_execution_adapter_returns_existing_result_envelope() -> None:
    """
    No-op adapter must preserve the current execution contract.

    Expected flow:
    - adapter receives text and trace_id
    - adapter performs no external execution
    - adapter returns the existing execution result envelope
    """

    adapter = NoOpExecutionAdapter()

    result = adapter.execute(
        text="Prepare controlled execution.",
        trace_id="trace-123",
    )

    assert result.status == "success"
    assert result.mode == "no_op"
    assert result.reason_code == "execution_prepared"
