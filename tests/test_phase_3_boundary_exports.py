import app.evaluation as evaluation
import app.execution as execution


def test_execution_package_exports_only_intentional_boundaries() -> None:
    """
    Execution package exports must stay intentional.

    Expected flow:
    - route code imports stable execution boundaries
    - adapter mode remains explicit
    - controlled execution remains no-op
    """

    expected_exports = {
        "EXECUTION_ADAPTER_MODE",
        "ExecutionAdapter",
        "ExecutionResult",
        "NoOpExecutionAdapter",
        "build_execution_adapter",
        "ALLOWED_EXECUTION_MODES",
        "validate_execution_mode",
        "build_execution_result",
    }

    assert set(execution.__all__) == expected_exports


def test_evaluation_package_exports_only_intentional_boundaries() -> None:
    """
    Evaluation package exports must stay intentional.

    Evaluation remains internal, deterministic, versioned, and non-blocking.
    """

    expected_exports = {
        "EVALUATION_REASON_INVALID_TEXT_LENGTH",
        "EVALUATION_REASON_MISSING_TRACE_ID",
        "EVALUATION_REASON_PASSED",
        "EVALUATION_REASON_UNEXPECTED_STATUS",
        "EVALUATION_RULE_VERSION",
        "EvaluationDecision",
        "evaluate_response",
    }

    assert set(evaluation.__all__) == expected_exports
