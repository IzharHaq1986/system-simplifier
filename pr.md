## Summary

Adds deterministic observability formatting for internal quality signals.

## Problem Statement

Quality signals could be built, serialized, prioritized, and added to internal telemetry preparation, but there was no dedicated helper for stable observability text output.

## Motivation

A deterministic observability formatter avoids ad-hoc internal log formatting and keeps future quality visibility consistent, internal-only, and easy to validate.

## Implementation

- Added `format_quality_signal_for_observability`.
- Reused existing quality signal priority behavior.
- Exported the formatter through `app.evaluation`.
- Added deterministic formatter test coverage.
- Updated package and boundary export enforcement tests.
## Validation

```text
ruff check .
pytest -q

All checks passed!
147 passed
## Pre-Flight Check

- [x] Public API response unchanged.
- [x] No telemetry exposure changes to clients.
- [x] No runtime control-flow mutation.
- [x] No external I/O.
- [x] No model calls.
- [x] No tool calls.
- [x] No hidden mutable state.
- [x] Deterministic behavior preserved.
- [x] Internal-only quality visibility preserved.
