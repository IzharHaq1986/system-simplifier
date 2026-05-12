# Phase 6 Guardrail Maturity Plan

## Objective

Define how guardrails should mature without increasing runtime complexity.

The goal is to make system protection clearer, more inspectable, and easier to validate while preserving deterministic runtime behavior.

## Guardrail Maturity Levels

### Level 1: Basic Input Rejection

Reject clearly invalid input before policy or execution logic runs.

Examples:

- empty input
- whitespace-only input
- malformed request payloads

### Level 2: Policy-Backed Request Control

Route accepted input through explicit policy checks before execution decisions are made.

This keeps authorization and runtime behavior separate.

### Level 3: Trusted and Untrusted Context Separation

Treat user input, tool output, model output, and memory as untrusted unless explicitly validated.

Guardrails should preserve a clear boundary between trusted system state and untrusted runtime content.

### Level 4: High-Risk Action Gating

Require stricter checks before actions that could affect external systems, stored state, credentials, or user-facing outcomes.

High-risk actions should remain gated by explicit policy decisions.

### Level 5: Runtime Monitoring and Review Signals

Guardrail behavior should produce internal signals that help reviewers understand what was blocked, allowed, or escalated.

These signals must remain internal-only and must not expand the public API response.

## Non-Goals

This slice does not introduce:

- new runtime behavior
- new public API fields
- model-based moderation
- external policy engines
- tool execution changes
- memory changes
- network calls
- dashboard work

## Required Guarantees

Guardrail maturity must preserve:

- deterministic behavior
- fail-closed handling
- no telemetry leakage
- no public API contract expansion
- no hidden mutable runtime state
- no external I/O
- clear trusted/untrusted boundaries

## Exit Criteria

This slice is complete when the repository documents:

- guardrail maturity levels
- trusted versus untrusted context boundaries
- high-risk action gating expectations
- internal-only guardrail signal expectations
- explicit non-goals for this phase
