from app.execution.result import build_execution_result
from app.models.execution_result import ExecutionResult


def test_build_execution_result_returns_typed_result():
    # The execution result envelope should return a typed result object.
    result = build_execution_result()

    assert isinstance(result, ExecutionResult)


def test_build_execution_result_uses_no_op_success_envelope():
    # This phase records a prepared execution result without model or tool execution.
    result = build_execution_result()

    assert result.status == "success"
    assert result.mode == "no_op"
    assert result.reason_code == "execution_prepared"
