from app.models.policy import PolicyDecision


# Keep the first policy boundary intentionally small.
# This step establishes the structure, not a full rule engine.
_BLOCKED_TERMS = {
    "blocked-term",
    "forbidden-term",
}


def evaluate_policy(text: str) -> PolicyDecision:
    # Input is expected to be normalized before reaching this function.
    lowered_text = text.lower()

    for blocked_term in _BLOCKED_TERMS:
        if blocked_term in lowered_text:
            return PolicyDecision(
                decision="deny",
                reason_code="policy_blocked_term",
            )

    return PolicyDecision(
        decision="allow",
        reason_code="allowed",
    )
