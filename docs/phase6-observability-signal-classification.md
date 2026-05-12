# Phase 6 Observability Signal Classification

## Objective

Define how observability signals should be classified before adding more runtime visibility.

The goal is to make operational signals easier to reason about without expanding public API responses or adding runtime side effects.

## Signal Categories

### Runtime Control Signals

Signals that describe deterministic runtime outcomes.

Examples:

- success
- retry
- fallback
- degraded response
- failure

### Policy Boundary Signals

Signals that describe whether a request, response, or runtime action passed policy checks.

These signals must remain internal-only.

### Guardrail Signals

Signals that describe input rejection, trusted/untrusted boundary enforcement, or high-risk action gating.

Guardrail signals should support reviewability without exposing internal decision details publicly.

### Evaluation Signals

Signals that describe quality checks after response shaping.

Evaluation signals must remain deterministic, side-effect free, and non-blocking unless explicitly changed in a later phase.

### Observability Health Signals

Signals that confirm telemetry formatting, sink handling, and observability hooks remain stable.

These signals must not mutate runtime behavior.

## Classification Rules

Each observability signal should define:

- signal category
- source boundary
- allowed audience
- public exposure status
- mutation risk
- failure behavior

## Required Guarantees

Observability signal classification must preserve:

- no public API contract expansion
- no telemetry leakage
- no hidden runtime state mutation
- no external I/O
- no model calls
- no tool calls
- deterministic formatting
- fail-closed validation

## Non-Goals

This slice does not introduce:

- dashboards
- metrics backends
- tracing vendors
- external logging services
- alerting systems
- runtime behavior changes
- new API fields

## Exit Criteria

This slice is complete when the repository documents:

- observability signal categories
- classification rules
- internal-only visibility expectations
- public exposure restrictions
- explicit non-goals
