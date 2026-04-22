from typing import Optional


def get_input_rejection_reason(text: str) -> Optional[str]:
    """
    Return a deterministic rejection reason for clearly invalid input.

    This helper is intentionally narrow:
    - no model-based classification
    - no semantic policy engine
    - no side effects

    Returning None means the input is allowed to proceed.
    """

    # Reject obvious control-character payloads except common whitespace
    blocked_characters = {"\x00"}

    for character in blocked_characters:
        if character in text:
            return "Input contains unsupported control characters."

    return None
