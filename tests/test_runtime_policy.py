from app.runtime_policy import RuntimePolicyDecision


def test_runtime_policy_decision_preserves_trace_id() -> None:
    decision = RuntimePolicyDecision(
        outcome="success",
        trace_id="trace-123",
        reason="runtime completed safely",
    )

    assert decision.outcome == "success"
    assert decision.trace_id == "trace-123"
    assert decision.reason == "runtime completed safely"
