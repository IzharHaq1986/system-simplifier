import pytest
from app.core.response_shaper import shape_simplify_response
from app.execution.result import ExecutionResult
from app.models.response import SimplifyResponse


def test_shape_simplify_response_returns_public_response_contract():
    execution_result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    response = shape_simplify_response(
        execution_result=execution_result,
        text_length=24,
        trace_id="test-trace-id",
    )

    assert isinstance(response, SimplifyResponse)
    assert response.status == "accepted"
    assert response.text_length == 24
    assert response.trace_id == "test-trace-id"


def test_shape_simplify_response_does_not_expose_internal_execution_fields():
    execution_result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    response = shape_simplify_response(
        execution_result=execution_result,
        text_length=24,
        trace_id="test-trace-id",
    )

    response_payload = response.model_dump()

    assert "status" in response_payload
    assert "text_length" in response_payload
    assert "trace_id" in response_payload

    assert "mode" not in response_payload
    assert "reason_code" not in response_payload

def test_shape_simplify_response_rejects_unexpected_execution_result_state():
    execution_result = ExecutionResult.model_construct(
        status="failed",
        mode="model",
        reason_code="unexpected_execution_state",
    )

    with pytest.raises(ValueError, match="Unexpected execution result state."):
        shape_simplify_response(
            execution_result=execution_result,
            text_length=24,
            trace_id="test-trace-id",
        )

def test_shape_simplify_response_error_message_is_stable():
    execution_result = ExecutionResult.model_construct(
        status="failed",
        mode="model",
        reason_code="unexpected_execution_state",
    )

    with pytest.raises(ValueError) as error_info:
        shape_simplify_response(
            execution_result=execution_result,
            text_length=24,
            trace_id="test-trace-id",
        )

    assert str(error_info.value) == "Unexpected execution result state."

def test_shape_simplify_response_returns_model_not_dictionary():
    execution_result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    response = shape_simplify_response(
        execution_result=execution_result,
        text_length=24,
        trace_id="test-trace-id",
    )

    assert isinstance(response, SimplifyResponse)
    assert not isinstance(response, dict)

def test_shape_simplify_response_preserves_text_length():
    execution_result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    response = shape_simplify_response(
        execution_result=execution_result,
        text_length=31,
        trace_id="test-trace-id",
    )

    assert response.text_length == 31

def test_shape_simplify_response_preserves_trace_id():
    execution_result = ExecutionResult(
        status="success",
        mode="no_op",
        reason_code="execution_prepared",
    )

    response = shape_simplify_response(
        execution_result=execution_result,
        text_length=24,
        trace_id="test-trace-id",
    )

    assert response.trace_id == "test-trace-id"

def test_shape_simplify_response_documents_translation_boundary():
    assert shape_simplify_response.__doc__ is not None
    assert "public API response" in shape_simplify_response.__doc__
    assert "Internal execution details" in shape_simplify_response.__doc__
