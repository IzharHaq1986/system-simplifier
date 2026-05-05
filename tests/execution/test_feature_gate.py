from app.execution.feature_gate import ENABLE_NON_NO_OP_EXECUTION


def test_non_no_op_execution_feature_gate_defaults_disabled() -> None:
    """
    Expected flow:
    - Feature gate is imported from the execution boundary.
    - Non-no-op execution remains disabled by default.
    - Future execution modes cannot activate accidentally.
    """
    assert ENABLE_NON_NO_OP_EXECUTION is False
