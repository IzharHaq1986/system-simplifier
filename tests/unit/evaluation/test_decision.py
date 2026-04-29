from app.evaluation.decision import EvaluationDecision


def test_evaluation_decision_accepts_allowed_result() -> None:
    decision = EvaluationDecision(
        allowed=True,
        reason="evaluation_passed",
        rule_version="v1",
    )

    assert decision.allowed is True
    assert decision.reason == "evaluation_passed"
    assert decision.rule_version == "v1"


def test_evaluation_decision_accepts_denied_result() -> None:
    decision = EvaluationDecision(
        allowed=False,
        reason="missing_trace_id",
        rule_version="v1",
    )

    assert decision.allowed is False
    assert decision.reason == "missing_trace_id"
    assert decision.rule_version == "v1"
