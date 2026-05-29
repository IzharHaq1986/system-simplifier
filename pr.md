## Summary

Adds internal quality signal preparation support to execution telemetry.

## Problem Statement

Quality signal helpers are stable, but execution telemetry did not yet have a controlled internal-only path for carrying serialized quality signal data.

## Motivation

Preparing quality signal data internally enables future observability work while preserving public API stability and deterministic runtime behavior.

## Implementation

- Added optional internal quality signal payload support to execution telemetry.
- Serialized quality signals using the existing deterministic helper.
- Preserved existing telemetry behavior when no quality signal is provided.
- Added telemetry event validation coverage.
- Added telemetry builder coverage.
- Preserved public API boundaries.
## Validation

```text
ruff check .
pytest -q

All checks passed!
145 passed
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
