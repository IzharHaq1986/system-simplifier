import pytest

from app.execution.mode import validate_execution_mode


def test_validate_execution_mode_accepts_no_op() -> None:
    assert validate_execution_mode("no_op") == "no_op"


def test_validate_execution_mode_rejects_unknown_mode() -> None:
    with pytest.raises(ValueError, match="Unsupported execution mode"):
        validate_execution_mode("model")
