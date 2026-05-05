
from app.execution.adapter_selector import build_execution_adapter

def test_selector_builds_no_op_adapter_only() -> None:
    adapter = build_execution_adapter()

    assert adapter.__class__.__name__ == "NoOpExecutionAdapter"
