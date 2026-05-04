from app.execution import build_execution_adapter
from app.execution.no_op_adapter import NoOpExecutionAdapter


def test_build_execution_adapter_returns_no_op_adapter() -> None:
    adapter = build_execution_adapter()

    assert isinstance(adapter, NoOpExecutionAdapter)
