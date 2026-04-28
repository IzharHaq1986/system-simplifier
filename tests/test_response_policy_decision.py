from app.response_policy.decision import ResponsePolicyDecision


def test_response_policy_decision_allows_valid_decision():
    decision = ResponsePolicyDecision(
        decision="allow",
        reason_code="response_contract_allowed",
    )

    assert decision.decision == "allow"
    assert decision.reason_code == "response_contract_allowed"
