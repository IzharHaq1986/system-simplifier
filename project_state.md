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

## Full Phase Architecture

### Project Goal
Move from pipeline-heavy system building to a simpler AI system architecture built around fewer, stronger components, with models and embeddings treated as infrastructure and with evaluation, guardrails, and observability designed in from the start.

---

## Phase 1 — Current-State Mapping

### Objective
Establish a factual baseline of the current system direction, intended workflows, architectural assumptions, and known reliability gaps before implementation expands.

### Scope
- document intended workflows
- define active planning lens (Architect + SRE)
- identify architectural concerns early
- map reliability concerns
- avoid premature implementation assumptions

### Key Outputs
- Phase 1 lens and audit scope
- workflows and request paths
- happy-path request lifecycle
- failure-path lifecycles
- failure comparison matrix
- initial understanding of gaps in evaluation, guardrails, and observability

### Exit Criteria
- intended workflows are explicitly documented
- request lifecycle is defined end-to-end
- major runtime failure classes are identified
- architecture decisions can move into structured component design

### Out of Scope
- code implementation
- service deployment design
- production scaling decisions
- detailed API specification beyond planning needs

Add or finalize a section with these items only:
active lens
audit scope
intended workflows
happy-path request lifecycle
failure-path lifecycle headings
known gaps:
evaluation
guardrails
observability

---

## Phase 2 — Target Architecture Design

### Objective
Define the target logical architecture of the system using a small number of reusable, high-value components with clear responsibilities and boundaries.

### Scope
- map workflows to components
- classify components as runtime or supporting/control-plane
- define component ownership boundaries
- define interface boundaries
- separate core infrastructure from operational/control concerns

### Key Outputs
- shared component map
- component classification
- ownership model
- input/output boundaries for each core component
- cross-component rules
- architectural separation between runtime path and control-plane

### Exit Criteria
- each major workflow maps to reusable components
- each core component has explicit responsibilities
- component boundaries are clear enough to guide implementation
- architecture is stable enough for minimum build planning

### Out of Scope
- deployment topology
- microservices decomposition
- advanced infra decisions
- performance tuning

---

## Phase 3 — Minimum Build Plan — Completed

### Objective
Define the smallest implementation plan that proves the architecture under normal and failure conditions without overbuilding the system.

### Scope
- identify the minimum runtime path to implement
- define first implementation slice
- define build order
- define what is intentionally deferred
- ensure runtime traceability and basic reliability from the start

### Key Outputs
- minimum build scope
- implementation order
- scope control plan
- first implementation slice
- first code-level implementation target
- minimum success criteria

### Exit Criteria
- minimum build path is clear
- first implementation slice is narrow and testable
- deferred scope is documented
- architecture can move into repository/module planning

### Out of Scope
- full feature set
- evaluation engine maturity
- advanced observability platform
- rich user experience features
- scaling and optimization work

#### Guardrails Layer (Input Control) — Completed
* Input normalization added (whitespace trimming)
* Whitespace-only input rejection enforced
* Request boundary validation strengthened
* Trace ID preserved on rejected requests
* Guardrail behavior covered by automated tests

#### Completed

* Minimum build scope defined
* First implementation slice completed:

  * Input Gateway
  * Request schema
  * Trace ID baseline
* Guardrails slice completed:

  * input normalization
  * whitespace-only rejection
  * deterministic control-character rejection
  * stable validation error contract
* Automated tests added for:

  * health endpoint
  * simplify valid request
  * whitespace normalization
  * schema-level rejection
  * deterministic guardrail rejection
  * trace ID propagation on success and failure
* Repo-level enforcement added:

  * pre-flight checklist
  * pull request template
  * CI repo hygiene check

**Controlled Execution Boundary**

* Typed policy decision model added
* Pure policy evaluator added
* Policy evaluation integrated into `POST /v1/simplify`
* Policy denial returns deterministic `403`
* Policy denial uses stable `policy_denied` error code
* Trace ID preserved on policy denial path
* Guardrails confirmed to run before policy evaluation
* Route tests added for:
  * allow path
  * deny path
  * error contract
  * trace ID propagation
  * boundary ordering

**Execution Decision Boundary**

* Typed execution decision model added
* Pure execution decision builder added
* Execution decision integrated after policy allow
* No model or tool execution introduced
* Public API response contract unchanged
* Unit tests added for execution decision builder
* Route flow now follows:
  * validation
  * guardrails
  * policy decision
  * execution decision
  * success response

**Response Shaping Boundary**

* Explicit response transformation boundary added
* Internal execution result translated into public `SimplifyResponse`
* Internal execution fields prevented from leaking into API response
* Stable success response contract enforced
* Trace ID preserved between response body and `X-Trace-ID` header
* Normalized text length preserved in public response
* Response shaper rejects unexpected internal execution state
* Unit and route-level regression tests added

**Response Policy Validation Boundary**

* Typed response policy decision model added
* Pure response policy evaluator added
* Response policy integrated after response shaping
* Response policy denial returns deterministic `500`
* Stable `response_policy_denied` error code added
* OpenAPI documents response policy denial path
* Trace ID preserved on response policy denial path
* Internal execution field leakage denied before API response
* Unit and route-level regression tests added

**Execution Telemetry Envelope**

- Internal telemetry event model added
- Telemetry event builder added
- Internal no-op telemetry sink added
- Telemetry emitted inside `/v1/simplify`
- Telemetry remains internal-only
- API response contract unchanged
- Regression tests prevent telemetry leakage
- Route-level test verifies telemetry emission

**Evaluation Route Regression**

- Added route-level regression coverage for non-blocking evaluation behavior
- Confirmed evaluation does not change successful API responses
- Confirmed evaluation fields remain internal and are not exposed through the API contract
- Confirmed trace ID consistency between response body and response header

**Execution Adapter Interface**

- Added controlled ExecutionAdapter protocol
- Added execution package exports
- Added adapter contract regression test
- Preserved no-op execution behavior
- No model, tool, network, or external service execution introduced

**Controlled Execution Integration**

- Added controlled execution adapter selector
- Routed /v1/simplify through build_execution_adapter()
- Preserved NoOpExecutionAdapter as active implementation
- Passed validated payload text and trace_id into adapter
- No model, tool, network, or external service execution introduced
- Public API response contract unchanged
- Route-level regression coverage added

**Execution Adapter Mode Coverage**

- Added explicit EXECUTION_ADAPTER_MODE constant
- Current adapter mode locked as no_op
- Exported adapter mode at package level
- Added CI-enforced test coverage for adapter mode
- Confirmed controlled execution remains deterministic

#### Repo-Level Enforcement — Completed

* Pre-flight checklist added:
  * `PRE_FLIGHT_CHECK.md`
* Pull request structure enforcement added:
  * `.github/pull_request_template.md`
  * CI validation for required PR sections
* Pre-flight acknowledgement enforcement added:
  * CI validation for `## Pre-Flight Check`
* Repo hygiene enforcement added:
  * CI fails on tracked `__pycache__`, `.pyc`, or `venv/` artifacts

#### API Contract Hardening — Completed

* Typed success response added:
  * `SimplifyResponse`
* Stable error response added:
  * `ErrorResponse`
* Deterministic guardrail failures now return:
  * machine-readable error code
  * human-readable error message
  * trace-aware response body
* OpenAPI contract updated for `/v1/simplify`:
  * success response documented
  * `422` error response documented
* Test coverage strengthened for:
  * success response shape
  * validation failure shape
  * deterministic guardrail failure shape

### Structured Observability Logging Adapter — Completed

Completed:
- Added internal `LoggingAdapter` for single-line structured JSON logs.
- Added observability hook boundary.
- Added telemetry sink boundary for formatted telemetry.
- Added observability factory for centralized construction.
- Added minimal logging configuration.
- Wired `/v1/simplify` success path to emit structured telemetry.
- Preserved internal telemetry formatter contract.
- Added unit tests for adapter, hook, sink, factory, and logging config.
- Added route-level regression test for telemetry emission.
- Fixed CI Python import path with explicit `PYTHONPATH`.

Validated:
- No telemetry exposed through API responses.
- No external logging dependency introduced.
- No model or tool execution introduced.
- Internal telemetry contract remains isolated.
- CI passed before merge.

---

## Phase 4 — Repository and Module Architecture (Completed ✅)

### Objective
Translate the logical architecture into a clean, minimal repository structure and module layout that preserves boundaries during implementation.

### Scope
- define repository folder structure
- define module boundaries
- define file responsibilities
- define app-layer separation
- define testing structure
- define configuration placement
- define logging and trace propagation structure

### Key Outputs
- repository scaffold
- file/folder architecture
- code-layer responsibilities
- module isolation rules
- initial testing layout
- implementation order by file/module

### Exit Criteria
- repository structure supports the minimum build cleanly
- each module has one clear responsibility
- architecture boundaries survive translation into code structure
- ready to begin actual implementation file by file

### Out of Scope
- adding future-phase folders prematurely
- distributed service layout
- separate repositories
- infrastructure-as-code

### Controlled Execution Evolution (In Progress 🚧)

Completed

1. Execution Mode Validation
- Added fail-closed execution mode validation
- Defined ALLOWED_EXECUTION_MODES
- Allowed only no_op mode
- Rejected unsupported execution modes
- Wired validation into adapter selector
- Exported validation boundary at package level
- Added CI-enforced tests and boundary export audit coverage
- Explicit execution adapter protocol introduced
- No-op adapter aligned with shared execution contract
- Adapter selector contract tests added
- Stub execution adapter scaffold added as internal-only placeholder
- Stub adapter is not exported or selector-wired
- Selector safety test added to prove stub adapter is not selector-reachable
- Execution feature gate added and disabled by default
- Feature gate default behavior covered by test
- Execution adapter selector behavior locked by test
- Selector verified to build only NoOpExecutionAdapter

#### Phase 4 Closure Checklist

- [ ] Execution remains no-op and deterministic
- [ ] Adapter selector fails closed for unsupported modes
- [ ] Feature gate prevents non-no-op execution
- [ ] Stub adapter remains unreachable and not exported
- [ ] Public API contract unchanged
- [ ] Evaluation remains non-blocking and internal
- [ ] Telemetry remains internal-only
- [ ] Observability remains side-effect free
- [ ] CI enforces all architectural boundaries

Current Phase 4 Properties
- Execution mode is explicit
- Adapter selection fails closed
- no_op remains the only active mode
- No model/tool/network execution introduced
- Public API contract remains unchanged
- Adapter contract has a single source of truth
- Stub adapter exists only as unreachable scaffold
- Stub adapter is internal, not exported, and not selector-reachable
- Non-no-op execution remains feature-gated and disabled

---

## Phase 5 — Runtime Reliability and Control Architecture

### Objective

Define the operational behavior of the runtime system under normal, degraded, and failing conditions.

### Scope

- define retry policy
- define fallback policy
- define degraded-response policy
- define boundary-safe failure handling
- define minimum runtime observability behavior

### Key Outputs

- retry rules
- fallback rules
- degraded-response rules
- boundary-safe failure handling model
- request traceability baseline
- logging/event expectations

### Exit Criteria

- failure behavior is explicit
- degraded modes are controlled
- retries and fallbacks are bounded
- architecture can be validated under stress without ambiguity

### Out of Scope

- full incident runbooks
- advanced alerting
- autoscaling behavior
- full SRE platform design

#### Execution Control Alignment (Phase 4 → Phase 5 Bridge)

- Execution remains no-op by default
- Execution feature gate must remain disabled
- All runtime reliability policies must operate without enabling real execution
- Retry, fallback, and degraded-response policies must not introduce side effects
- Any future execution mode must pass through:
  - feature gate
  - adapter selector (fail-closed)
  - policy boundary
  - evaluation (non-blocking)
  - telemetry (internal-only)

#### Retry Policy Definition

- Retries must be bounded
- Retries must never enable real execution
- Retries must not call models, tools, network, or external services
- Retry behavior applies only to explicitly safe internal boundaries
- Retry attempts must preserve the same trace_id
- Retry outcomes must be observable through internal telemetry
- Failed retries must resolve into controlled fallback or degraded response behavior

#### Fallback Policy Definition

- Fallbacks must be explicit and bounded
- Fallbacks must not enable real execution
- Fallbacks must not call models, tools, network, or external services
- Fallback behavior must preserve the same trace_id
- Fallback outcomes must be observable through internal telemetry
- Fallback must produce either a controlled degraded response or a safe failure
- Fallback must not leak internal policy, evaluation, telemetry, or adapter details

---

## Phase 6 — Evaluation, Guardrails, and Observability Expansion

### Objective
Expand the three critical system quality areas identified at project start: evaluation, guardrails, and observability.

### Scope
- define evaluation approach
- define lightweight quality measurement
- define guardrail maturity path
- define observability maturity path
- define what signals must exist before system expansion

### Key Outputs
- evaluation framework plan
- basic scoring and review approach
- guardrail expansion path
- observability maturity plan
- quality visibility goals

### Exit Criteria
- quality is measurable at a basic level
- guardrails are no longer implicit
- observability extends beyond minimal logs
- system is ready for deeper confidence-building work

### Out of Scope
- full benchmark program
- complex dashboards
- advanced policy engines
- large-scale quality automation

---

## Phase 7 — Delivery and Governance Architecture

### Objective
Ensure the repo, PR workflow, CI/CD controls, and governance model support the intended system architecture and reliability goals.

### Scope
- branch protection alignment
- PR workflow discipline
- CI gate definition
- release path planning
- testing expectations
- repository governance alignment

### Key Outputs
- PR-only workflow baseline
- CI expectations
- delivery path
- release safety checks
- governance rules tied to architecture quality

### Exit Criteria
- changes flow through guarded PR path
- basic CI gates exist or are planned
- delivery model supports system safety and reliability
- repo governance matches the architectural intent

### Out of Scope
- advanced deployment automation
- complex multi-environment release orchestration
- enterprise governance overhead

### Governance Milestone — Repo Guardrails Active
Status:
- main branch is protected
- PR-only merge flow enforced
- required status check enabled:
  - Lint, Security, and Tests
- branch must be up to date before merge
- enforcement verified via test PR

Implication:
- CI is now an enforcement layer, not informational
- no unverified code can reach main
- repository governance aligns with system reliability goals

Scope:
- applies to all future changes in this repo
- baseline for expanding CI checks in later phases

Note:
- additional checks (security, container scan, SBOM, etc.) will be added incrementally
- guardrails expansion will follow Phase 3 and Phase 5 progression

---

## Phase 8 — Post-Minimum-Build Expansion

### Objective
Expand the system only after the architecture, reliability baseline, and minimum build are proven.

### Scope
- refine components based on evidence
- add deeper evaluation
- improve observability
- expand retrieval and model capabilities carefully
- revisit deferred items only when justified

### Key Outputs
- evidence-based expansion roadmap
- validated improvement priorities
- controlled feature growth
- architecture refinements grounded in real behavior

### Exit Criteria
- minimum system has been proven
- expansion decisions are evidence-driven
- deferred complexity is added only when justified

### Out of Scope
- speculative capability expansion
- adding features because they seem impressive
- introducing architectural complexity without measured need

---

## Next Focus

* Move from internal execution decision → response shaping or execution result envelope
* Keep execution no-op until model/tool boundary is explicitly designed
* Maintain:
  * deterministic behavior
  * full test coverage
  * CI-enforced workflow
  * no premature model/tool integration

---

## Cross-Phase Rules

### 1. Evidence before expansion
Do not add architectural complexity until current behavior is understood.

### 2. Fewer, stronger components
Prefer shared infrastructure components over many narrow pipelines.

### 3. Runtime path stays simple
Keep the live request path clean, observable, and boundary-safe.

### 4. Control-plane concerns stay separate
Evaluation, observability, and delivery governance should support the runtime path without bloating it.

### 5. No premature distribution
Logical component separation does not imply microservices or distributed deployment.

### 6. Traceability from day one
Every implemented request path must be traceable from entry to result.

### 7. Deferred scope is intentional
Not building something yet is a design decision, not a missing idea.

---

## Phase Progression Model

Phase 1:
- understand and define the system clearly

Phase 2:
- shape the architecture into reusable components

Phase 3:
- define the smallest build that proves the design

Phase 4:
- map architecture into repository/module structure

Phase 5:
- define runtime reliability behavior

Phase 6:
- strengthen evaluation, guardrails, and observability

Phase 7:
- align delivery and governance with system quality

Phase 8:
- expand only after evidence justifies it
