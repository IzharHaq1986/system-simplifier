from app.runtime.policy import RuntimeOutcome, RuntimePolicyDecision


MAX_RETRY_ATTEMPTS = 1


def evaluate_runtime_policy(
    *,
    outcome: RuntimeOutcome,
    trace_id: str,
    retry_attempts: int = 0,
) -> RuntimePolicyDecision:
    """
    Evaluates runtime behavior without enabling real execution.

    Retries are allowed only when:
    - outcome is explicitly retry
    - trace_id exists
    - retry_attempts stay within the bounded limit
    """

    if not trace_id.strip():
        return RuntimePolicyDecision(
            allowed=False,
            outcome=RuntimeOutcome.FAILURE,
            reason="missing trace_id",
            trace_id=trace_id,
        )

    if outcome == RuntimeOutcome.SUCCESS:
        return RuntimePolicyDecision(
            allowed=True,
            outcome=RuntimeOutcome.SUCCESS,
            reason="runtime outcome allowed",
            trace_id=trace_id,
        )

    if outcome == RuntimeOutcome.RETRY:
        if retry_attempts >= MAX_RETRY_ATTEMPTS:
            return RuntimePolicyDecision(
                allowed=False,
                outcome=RuntimeOutcome.FAILURE,
                reason="retry limit exceeded",
                trace_id=trace_id,
            )

        return RuntimePolicyDecision(
            allowed=True,
            outcome=RuntimeOutcome.RETRY,
            reason="bounded retry allowed",
            trace_id=trace_id,
        )

    return RuntimePolicyDecision(
        allowed=False,
        outcome=RuntimeOutcome.FAILURE,
        reason="runtime outcome denied",
        trace_id=trace_id,
    )
