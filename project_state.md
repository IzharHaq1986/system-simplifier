# Project: System Simplifier

## Current Direction
- Shift from pipeline-heavy design to reusable system architecture
- Reduce component sprawl and consolidate into fewer high-value services
- Treat models and embeddings as infrastructure
- Prioritize evaluation, guardrails, and observability

## Problem Statement
Current AI systems rely on fragmented pipelines that are:
- Hard to maintain
- Difficult to measure
- Prone to silent failures

## Objective
Build a simplified AI system architecture with:
- Fewer, stronger components
- Clear interfaces
- Built-in evaluation and monitoring

## Core Pillars
1. System simplification
2. Shared infrastructure (models + embeddings)
3. Evaluation framework
4. Guardrails
5. Observability

## Initial Workstreams
1. Architecture audit
2. Target system design
3. Evaluation setup
4. Guardrails definition
5. Observability foundation

## Immediate Next Step
Document current-state architecture:
- existing pipelines
- duplicated logic
- model usage
- embedding usage
- monitoring gaps
- guardrail gaps

## Success Signals
- Reduced system complexity
- Measurable output quality
- Faster iteration cycles
- Lower regression risk
- Improved reliability

## Phase 1 — Lens & Audit Scope

### Active Lens
Primary: Staff / Principal Architect  
Secondary: SRE / Operations Engineer

### Lens Application

#### Architect Lens Focus
- Define system boundaries
- Identify duplicated or overlapping components
- Evaluate ownership and responsibilities
- Assess interface clarity between components
- Highlight unnecessary pipeline complexity

#### SRE Lens Focus
- Identify what is currently observable vs invisible
- Assess logging, metrics, and tracing coverage
- Detect failure points with poor visibility
- Identify gaps in evaluation and monitoring
- Highlight areas with high operational risk

---

## Phase 1 — Current-State Mapping

### Goal
Establish a factual baseline of the current AI system before proposing simplification.

### Audit Areas
1. Existing pipelines and workflows
2. Duplicated components or logic
3. Model usage and routing
4. Embedding usage and ownership
5. Evaluation gaps
6. Guardrail gaps
7. Observability gaps
8. Top pain points

### Current Findings
- Existing pipelines: TBD
- Duplicated logic: TBD
- Model usage: TBD
- Embedding usage: TBD
- Evaluation gaps: TBD
- Guardrail gaps: TBD
- Observability gaps: TBD
- Top pain points: TBD

### Exit Criteria
- Current system inventory documented
- Major duplication identified
- Critical gaps clearly visible
- Ready for Phase 2 target architecture design

### Audit Scope

#### 1. Pipelines & Workflows
- What pipelines currently exist?
- What problems do they solve?
- Where is duplication present?

#### 2. Models & Embeddings
- How are models accessed and used?
- How are embeddings generated, stored, and versioned?
- Are these treated as shared infrastructure or app-level logic?

#### 3. Component Boundaries
- What are the main system components?
- Are responsibilities clearly separated?
- Where are boundaries unclear or leaking?

#### 4. Evaluation
- Are there defined evaluation datasets?
- Is regression testing in place?
- Can output quality be measured consistently?

#### 5. Guardrails
- Are there input/output validation mechanisms?
- Are policy checks centralized or scattered?
- What failure modes are unhandled?

#### 6. Observability
- What logs, metrics, or traces exist?
- Can failures be diagnosed quickly?
- Are latency, cost, and quality tracked?

#### 7. Pain Points
- What are the top recurring issues?
- Where do failures go unnoticed?
- What is hardest to debug or maintain?

---

### Operating Rule (Phase 1)
- No redesign decisions without evidence
- No new components introduced
- Document first, simplify later

---

### Exit Criteria
- Clear inventory of current system
- Duplication and boundary issues identified
- Observability and evaluation gaps visible
- Ready for Phase 2 (Target Architecture Design)
