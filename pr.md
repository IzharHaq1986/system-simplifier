## Summary

Adds deterministic internal serialization for quality signals.

## Problem Statement

Quality signals had builders, formatters, summaries, and status helpers, but no single trusted helper for converting a signal into a stable internal dictionary.

## Motivation

A dedicated serializer prevents ad-hoc internal payload construction later and keeps quality visibility deterministic, explicit, and internal-only.

## Implementation

- Added `score` to `QualitySignal` with deterministic validation.
- Added `serialize_quality_signal`.
- Exported the serializer through `app.evaluation`.
- Added serialization test coverage.
- Updated package and boundary export enforcement tests.

## Validation

```text
ruff check .
pytest -q

All checks passed!
132 passed
```

## Pre-Flight Check

- [x] Public API response unchanged.
- [x] No telemetry exposure changes.
- [x] No runtime control-flow mutation.
- [x] No external I/O.
- [x] No model calls.
- [x] No tool calls.
- [x] No hidden mutable state.
- [x] Deterministic behavior preserved.
- [x] Internal-only quality visibility preserved.
