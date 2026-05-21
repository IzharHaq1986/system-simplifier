## Summary

Adds a Phase 6 quality signal telemetry integration plan.

## Problem Statement

Quality signal helpers are now stable, but telemetry integration needs an explicit boundary before implementation to avoid leaking internal quality fields or mutating runtime behavior.

## Motivation

Planning the telemetry boundary first keeps the next implementation slice small, safe, and aligned with internal-only visibility guarantees.

## Implementation

- Added a quality signal telemetry integration plan.
- Defined allowed and disallowed future behavior.
- Documented the proposed future integration flow.
- Added required guardrails before implementation.
- Updated `project_state.md` with the new planning document and next recommended slice.
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
