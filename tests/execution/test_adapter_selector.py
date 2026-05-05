from app.execution import (
    ExecutionAdapter,
    NoOpExecutionAdapter,
    build_execution_adapter,
)


def test_build_execution_adapter_returns_no_op_adapter() -> None:
    """
    Expected flow:
    - Selector uses the configured execution mode.
    - Selector validates the mode internally.
    - Selector returns the controlled no-op adapter.
    """
    adapter = build_execution_adapter()

    assert isinstance(adapter, NoOpExecutionAdapter)


def test_build_execution_adapter_returns_adapter_contract() -> None:
    """
    Expected flow:
    - Selector returns an adapter through the shared execution contract.
    - Adapter remains callable through the protocol interface.
    - Execution behavior stays deterministic and no-op.
    """
    adapter: ExecutionAdapter = build_execution_adapter()

    result = adapter.execute(
        text="hello",
        trace_id="test-trace-id",
    )

    assert result.status == "success"


def test_build_execution_adapter_does_not_return_stub_adapter() -> None:
    """
    Expected flow:
    - Adapter selector uses only the approved execution mode.
    - Stub adapter remains internal and unreachable.
    - Selector continues returning the controlled no-op adapter only.
    """
    adapter = build_execution_adapter()

    assert adapter.__class__.__name__ != "StubExecutionAdapter"
