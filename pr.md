## Summary

Adds deterministic normalization for internal quality signal text fields.

## Problem Statement

Quality signal source and reason fields could be valid but inconsistently formatted because of extra whitespace. That can create noise in future telemetry, serialization, and comparison work.

## Motivation

A small normalization helper keeps internal quality signal text stable before it is formatted, summarized, serialized, or reviewed.

## Implementation

- Added `normalize_quality_signal_text`.
- Updated `build_quality_signal` to normalize source and reason.
- Exported the helper through `app.evaluation`.
- Added deterministic normalization test coverage.
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
