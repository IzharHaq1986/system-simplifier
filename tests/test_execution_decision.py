from app.execution.decision import build_execution_decision
from app.models.execution import ExecutionDecision


def test_build_execution_decision_returns_typed_decision():
    # The execution boundary should return a typed decision object.
    decision = build_execution_decision()

    assert isinstance(decision, ExecutionDecision)


def test_build_execution_decision_uses_no_op_mode():
    # This phase prepares execution control without model or tool execution.
    decision = build_execution_decision()

    assert decision.decision == "proceed"
    assert decision.mode == "no_op"
    assert decision.reason_code == "policy_allowed"
