from app.execution import EXECUTION_ADAPTER_MODE, build_execution_adapter
from app.execution.no_op_adapter import NoOpExecutionAdapter


def test_build_execution_adapter_returns_no_op_adapter() -> None:
    adapter = build_execution_adapter()

    assert isinstance(adapter, NoOpExecutionAdapter)


def test_execution_adapter_mode_is_explicit() -> None:
    assert EXECUTION_ADAPTER_MODE == "no_op"
