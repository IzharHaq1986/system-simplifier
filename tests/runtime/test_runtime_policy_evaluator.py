from app.runtime.evaluator import evaluate_runtime_policy
from app.runtime.policy import RuntimeOutcome


def test_retry_is_allowed_when_attempt_is_within_limit() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.RETRY,
        trace_id="trace-123",
        retry_attempts=0,
    )

    assert decision.allowed is True
    assert decision.outcome == RuntimeOutcome.RETRY
    assert decision.trace_id == "trace-123"


def test_retry_fails_closed_when_limit_is_exceeded() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.RETRY,
        trace_id="trace-123",
        retry_attempts=1,
    )

    assert decision.allowed is False
    assert decision.outcome == RuntimeOutcome.FAILURE
    assert decision.reason == "retry limit exceeded"


def test_runtime_policy_fails_closed_without_trace_id() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.RETRY,
        trace_id="",
        retry_attempts=0,
    )

    assert decision.allowed is False
    assert decision.outcome == RuntimeOutcome.FAILURE
    assert decision.reason == "missing trace_id"

def test_fallback_is_allowed_when_outcome_is_explicit() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.FALLBACK,
        trace_id="trace-123",
    )

    assert decision.allowed is True
    assert decision.outcome == RuntimeOutcome.FALLBACK
    assert decision.reason == "controlled fallback allowed"
    assert decision.trace_id == "trace-123"


def test_fallback_fails_closed_without_trace_id() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.FALLBACK,
        trace_id="",
    )

    assert decision.allowed is False
    assert decision.outcome == RuntimeOutcome.FAILURE
    assert decision.reason == "missing trace_id"

def test_degraded_response_is_allowed_when_outcome_is_explicit() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.DEGRADED_RESPONSE,
        trace_id="trace-123",
    )

    assert decision.allowed is True
    assert decision.outcome == RuntimeOutcome.DEGRADED_RESPONSE
    assert decision.reason == "controlled degraded response allowed"
    assert decision.trace_id == "trace-123"


def test_degraded_response_fails_closed_without_trace_id() -> None:
    decision = evaluate_runtime_policy(
        outcome=RuntimeOutcome.DEGRADED_RESPONSE,
        trace_id="",
    )

    assert decision.allowed is False
    assert decision.outcome == RuntimeOutcome.FAILURE
    assert decision.reason == "missing trace_id"
