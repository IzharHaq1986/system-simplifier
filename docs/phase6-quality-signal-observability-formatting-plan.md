# Phase 6 Quality Signal Observability Formatting Plan

## Purpose

Define how internal quality signals should be represented in future observability output without changing public API behavior, runtime control flow, or telemetry emission semantics.

## Current State

Phase 6 quality signal helpers are stable and internal-only.

Current helpers support:

- signal creation
- normalization
- formatting
- summarization
- serialization
- comparison
- priority ordering
- sorting
- highest-priority selection

## Formatting Boundary

Quality signal observability formatting must remain internal-only.

Allowed future behavior:

- format quality signals for internal logs
- include quality status in internal observability output
- include quality source in internal observability output
- include quality priority in internal observability output
- include highest-priority quality signal summary in internal observability output

Disallowed behavior:

- no public API response changes
- no request or response schema changes
- no telemetry exposure changes without a separate implementation PR
- no runtime control-flow mutation
- no model calls
- no tool calls
- no external I/O
- no hidden mutable state
- no quality signal fields returned to clients

## Proposed Internal Output Shape

Future observability output should use deterministic field names:

```text
quality_status=<status>
quality_source=<source>
quality_priority=<priority>
quality_reason=<reason>
```

For a selected highest-priority signal:

```text
quality_highest_status=<status>
quality_highest_source=<source>
quality_highest_priority=<priority>
quality_highest_reason=<reason>
```
## Formatting Rules

Future formatting must preserve these rules:

- field names must be stable
- field ordering must be deterministic
- values must come from existing quality signal helpers
- whitespace must be normalized before formatting
- blocked signals must remain highest urgency
- acceptable signals must remain lowest urgency
- formatting must not mutate the original signal
- formatting must not emit public response fields

## Proposed Future Flow

```text
quality signal
→ priority helper
→ internal formatting helper
→ observability adapter
→ internal logs only
→ public API response remains unchanged
```

## Required Guardrails Before Implementation

Before observability formatting is implemented, tests must prove:

- formatted output is deterministic
- formatting does not mutate quality signals
- public API responses do not include quality fields
- observability remains side-effect free
- no external systems are called
- runtime outcome remains unchanged

## Future Implementation Slice

The next implementation slice should be limited to:

- adding a deterministic quality observability formatter
- reusing existing quality signal helpers
- adding unit tests for output shape
- adding boundary tests proving public API stability

## Validation Expectations

Future implementation must pass:

```text
ruff check .
pytest -q
```
It must also preserve:

- public API stability
- internal-only quality visibility
- deterministic runtime behavior
- fail-closed validation
- side-effect free observability
