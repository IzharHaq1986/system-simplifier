from app.runtime.policy import RuntimeOutcome, RuntimePolicyDecision


MAX_RETRY_ATTEMPTS = 1


def evaluate_runtime_policy(
    *,
    outcome: RuntimeOutcome,
    trace_id: str,
    retry_attempts: int = 0,
) -> RuntimePolicyDecision:
    """
    Evaluate runtime behavior without enabling real execution.

    Runtime policy decisions are internal-only and must not call models,
    tools, networks, or external services.
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

    if outcome == RuntimeOutcome.FALLBACK:
        return RuntimePolicyDecision(
            allowed=True,
            outcome=RuntimeOutcome.FALLBACK,
            reason="controlled fallback allowed",
            trace_id=trace_id,
        )

    return RuntimePolicyDecision(
        allowed=False,
        outcome=RuntimeOutcome.FAILURE,
        reason="runtime outcome denied",
        trace_id=trace_id,
    )
