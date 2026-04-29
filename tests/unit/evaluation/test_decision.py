from app.evaluation.decision import EvaluationDecision


def test_evaluation_decision_accepts_allowed_result():
    decision = EvaluationDecision(
        allowed=True,
        reason="evaluation_passed",
    )

    assert decision.allowed is True
    assert decision.reason == "evaluation_passed"


def test_evaluation_decision_accepts_denied_result():
    decision = EvaluationDecision(
        allowed=False,
        reason="missing_trace_id",
    )

    assert decision.allowed is False
    assert decision.reason == "missing_trace_id"
