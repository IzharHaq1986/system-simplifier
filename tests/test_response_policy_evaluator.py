from app.models.response import SimplifyResponse
from app.response_policy.evaluator import evaluate_response_policy


def test_evaluate_response_policy_allows_stable_simplify_response():
    response = SimplifyResponse(
        status="accepted",
        text_length=24,
        trace_id="test-trace-id",
    )

    decision = evaluate_response_policy(response)

    assert decision.decision == "allow"
    assert decision.reason_code == "response_contract_allowed"

def test_evaluate_response_policy_denies_empty_trace_id():
    response = SimplifyResponse.model_construct(
        status="accepted",
        text_length=24,
        trace_id="",
    )

    decision = evaluate_response_policy(response)

    assert decision.decision == "deny"
    assert decision.reason_code == "response_contract_denied"

def test_evaluate_response_policy_denies_internal_execution_fields():
    response = SimplifyResponse.model_construct(
        status="accepted",
        text_length=24,
        trace_id="test-trace-id",
    )

    response.__dict__["mode"] = "no_op"
    response.__dict__["reason_code"] = "execution_prepared"

    decision = evaluate_response_policy(response)

    assert decision.decision == "deny"
    assert decision.reason_code == "response_contract_denied"

def test_evaluate_response_policy_uses_stable_deny_reason_code_for_leaked_fields():
    response = SimplifyResponse.model_construct(
        status="accepted",
        text_length=24,
        trace_id="test-trace-id",
    )

    response.__dict__["mode"] = "no_op"

    decision = evaluate_response_policy(response)

    assert decision.decision == "deny"
    assert decision.reason_code == "response_contract_denied"

def test_evaluate_response_policy_uses_stable_allow_reason_code():
    response = SimplifyResponse(
        status="accepted",
        text_length=24,
        trace_id="test-trace-id",
    )

    decision = evaluate_response_policy(response)

    assert decision.decision == "allow"
    assert decision.reason_code == "response_contract_allowed"
