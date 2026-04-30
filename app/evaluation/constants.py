"""
Stable evaluation constants.

These values are internal but telemetry-facing.
Do not rename them without updating regression tests.
"""

EVALUATION_RULE_VERSION = "v1"

EVALUATION_REASON_MISSING_TRACE_ID = "missing_trace_id"
EVALUATION_REASON_UNEXPECTED_STATUS = "unexpected_response_status"
EVALUATION_REASON_INVALID_TEXT_LENGTH = "invalid_text_length"
EVALUATION_REASON_PASSED = "evaluation_passed"
