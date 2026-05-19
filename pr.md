## Summary

Adds deterministic selection for the highest-priority internal quality signal.

## Problem Statement

Quality signals can now be prioritized and sorted, but there is no single trusted helper for selecting the most urgent signal from a collection.

## Motivation

A dedicated selector prevents duplicate ad-hoc logic and prepares quality signals for future telemetry, observability, and reporting summaries.

## Implementation

- Added `get_highest_priority_quality_signal`.
- Reused `sort_quality_signals_by_priority`.
- Returned `None` for empty input to keep behavior explicit and deterministic.
- Exported the helper through `app.evaluation`.
- Added deterministic selector test coverage.
- Updated package and boundary export enforcement tests.

## Validation

```text
ruff check .
pytest -q

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
