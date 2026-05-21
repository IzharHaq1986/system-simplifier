# Phase 6 Quality Signal Telemetry Integration Plan

## Purpose

Define how internal quality signals can be prepared for future telemetry integration without changing public API behavior, runtime control flow, or observability side effects.

## Current State

Phase 6 quality signal helpers are available for internal use.

Stable helpers include:

- build_quality_signal
- build_quality_signal_from_evaluation
- build_quality_signal_payload
- format_quality_signal
- summarize_quality_signal
- is_blocked_quality_signal
- is_needs_review_quality_signal
- is_acceptable_quality_signal
- serialize_quality_signal
- normalize_quality_signal_text
- quality_signals_match
- get_quality_signal_priority
- sort_quality_signals_by_priority
- get_highest_priority_quality_signal
## Integration Boundary

Quality signal telemetry integration must remain internal-only.

Allowed future behavior:

- build quality signals from existing internal evaluation decisions
- serialize quality signals for internal telemetry preparation
- summarize quality status for internal observability review
- keep quality fields out of public API responses

Disallowed behavior:

- no public API response changes
- no request or response schema changes
- no runtime control-flow mutation
- no model calls
- no tool calls
- no external I/O
- no hidden mutable state
- no telemetry-driven runtime decisions
## Proposed Future Flow

```text
evaluation decision
→ quality signal builder
→ quality signal serialization
→ internal telemetry preparation
→ telemetry sink
→ observability hook
→ public API response remains unchanged
```
