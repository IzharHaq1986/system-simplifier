from app.models.execution import ExecutionDecision


def build_execution_decision() -> ExecutionDecision:
    # This boundary prepares the request for future execution.
    # It intentionally performs no model or tool work in this phase.
    return ExecutionDecision(
        decision="proceed",
        mode="no_op",
        reason_code="policy_allowed",
    )
