# Phase 6 Lightweight Scoring Model

## Objective

Define a simple scoring model for evaluating system quality without adding runtime complexity.

The scoring model should make quality review easier while preserving deterministic behavior, internal-only evaluation visibility, and strict runtime boundaries.

## Scoring Categories

### Acceptable

The response or runtime outcome satisfies the minimum quality expectations.

Signals may include:

- valid trace identifier
- non-empty response shape
- expected runtime outcome
- no public leakage of internal metadata
- no policy or guardrail violation

### Needs Review

The response or runtime outcome completed, but should be reviewed before deeper system expansion.

Signals may include:

- degraded response behavior
- fallback behavior
- retry behavior
- unclear quality signal
- incomplete observability context

### Blocked

The response or runtime outcome should not be treated as acceptable.

Signals may include:

- failed policy decision
- failed guardrail decision
- missing trace identifier
- invalid telemetry payload
- public exposure of internal metadata
- failed runtime validation

## Scoring Rules

The scoring model must remain:

- deterministic
- inspectable
- side-effect free
- internal-only
- independent of model output
- independent of external services

## Review Rules

Scores should help reviewers answer:

- what happened
- where the signal came from
- whether the outcome is acceptable
- whether the outcome needs review
- whether the outcome should be blocked

## Required Guarantees

This scoring model must preserve:

- no public API contract expansion
- no runtime behavior changes
- no telemetry leakage
- no external I/O
- no model calls
- no tool calls
- no hidden mutable state
- fail-closed validation behavior

## Non-Goals

This slice does not introduce:

- scoring code
- automated benchmarks
- model-based judging
- dashboards
- alerting
- external evaluators
- new API response fields

## Exit Criteria

This slice is complete when the repository documents:

- scoring categories
- deterministic scoring rules
- review expectations
- blocked outcome expectations
- explicit non-goals
