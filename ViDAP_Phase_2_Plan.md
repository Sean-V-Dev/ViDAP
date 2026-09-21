# ViDAP Phase 2 Plan — Deterministic Execution and Run Foundations

| Field | Value |
|---|---|
| Status | Draft — approval required |
| Version | 0.1 |
| Parent | `ViDAP_Roadmap.md` version 3.5 |
| Spine phase | Phase 2 — Deterministic Execution and Run Foundations |
| Product source | `ViDAP_Overview.txt` |
| Prerequisite | Phase 1 complete through P1-EP06 reconciliation |
| Created | 2026-09-21 |
| Owner | Central |

---

## 1. Authorization and Boundary

This is a draft phase plan. It is not an execution packet and does not
authorize source changes, dependencies, runtime behavior, persistence, or a
Phase 2 worker. Its approval would authorize Central only to prepare the first
bounded Phase 2 decision packet.

Phase 2 turns a validated, UI-independent workflow description into a
deterministic headless execution foundation. It owns runtime planning and the
small run record needed to make that execution inspectable and reproducible.
It must preserve the Phase 1 canonical workflow as input; it cannot redefine
workflow meaning, make the browser the runtime, or use generated arbitrary
code or an LLM for normal execution.

## 2. Plain-English Phase Intent

### What we will build or change

We will add the dependable middle layer between “this workflow is valid” and
“this workflow actually ran.” It will turn a validated graph into a clear
order of operations, run a deliberately small approved operation set, and
retain an inspectable record of what happened.

### Why the system needs it

A graph that only validates is still a diagram. The system needs a single
engine that follows graph dependencies rather than visual placement, tells us
which operation failed and why, and avoids accidentally treating an old result
as a new one.

### What real behavior it enables

A developer can run a small branched workflow headlessly, receive a structured
run result and artifact references, repeat the run under the same recorded
conditions, and see predictable failure for invalid graphs or runtime errors.
The UI and real data-science workflows remain later consumers of this engine.

### How we will know it works

Representative headless workflows will execute in dependency order regardless
of creation or layout order. Branches will share one upstream result; changed
workflow/input/parameter conditions cannot silently reuse a stale cache; and
both successful and failed runs will leave actionable, technical evidence.

## 3. Governing Inputs and Handoff

Every Phase 2 packet must read:

1. Current explicit user direction.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially invariants 1–14,
   Phase 2, execution-isolation/artifact-persistence decision requirements,
   and strong validation scaling.
4. `ViDAP_Roadmap.md` version 3.5, especially P2 and checkpoint A2.
5. `ViDAP_Phase_1_Plan.md` version 2.3 and
   `ViDAP_P1_EP06_Validation_and_Reconciliation.md`.
6. The accepted P1 reconciliation records and their decisions D1.1–D1.7.
7. This plan and later accepted Phase 2 decision records.

Phase 1 hands forward an open, strict `vidap.workflow` version `1.0` document;
stable identities/endpoints; static immutable contracts and registry; nominal
types; pure validation and diagnostics; and controlled fixture evidence. It
does **not** hand forward execution semantics, an intermediate representation,
runtime node implementations, scheduling, run identity, seed/environment
capture, cache policy, artifact ownership, persistence, cancellation, or
runtime-failure behavior. Phase 2 must decide those explicitly before assuming
them in implementation.

## 4. Required Outcome and Explicit Exclusions

### Required outcome

Phase 2 delivers a deterministic, headless engine that accepts only a
validated canonical workflow, derives dependency order, dispatches a small
approved reference operation set, and returns an inspectable run record with
result/artifact references and actionable failure information. Branching must
reuse a shared upstream computation within a run. Cache reuse, if selected,
must be explicit and correct rather than an invisible optimization.

### Explicit exclusions

Phase 2 does not deliver:

- a graph editor, browser/server workflow API, web-run controls, result UI, or
  any Phase 3 visual integration;
- general data intake, profiling, preparation, user datasets, or the Phase 4
  data ownership/provenance policy;
- real supervised-model selection/training/evaluation, model results, or the
  Phase 5 modeling policy;
- full experiment history/comparison UX, branching comparison, or the Phase 6
  experimentation product;
- notebook/Python export or parity claims, which belong to Phase 7;
- AutoML, advanced models, neural networks, plugins, arbitrary Python/code
  nodes, distributed/cloud execution, production serving, or enterprise MLOps;
- a migration, new workflow schema version, or redefinition of Phase 1
  document/contract/validation semantics; or
- an unbounded artifact store. Any selected local run/artifact persistence must
  be minimal, explicit, inspectable, owned, and removable.

## 5. Phase 2 Decisions

No implementation packet may assume a decision below until its decision record
is independently validated and accepted by Central.

### D2.1 — Execution isolation and local lifecycle

Select the local execution boundary: process/module isolation, lifecycle,
resource/failure containment, cancellation limits, and how a future UI calls
it without becoming the authority. Compare proportionate options using local
simplicity, reproducibility, failure containment, inspectability, Windows
support, testing, and no premature service architecture.

### D2.2 — Intermediate execution representation and runtime binding

Define the layout-independent representation derived from a validated workflow,
the allowed runtime binding on a node contract, and the boundary between
declarative Phase 1 contracts and executable implementations. It must preserve
stable workflow meaning and forbid dynamic/untrusted code loading.

### D2.3 — Deterministic planning, shared upstream work, and failure flow

Define dependency-derived ordering, deterministic tie-breaking, branch/join
rules, within-run result ownership, invalid-graph refusal, failure propagation,
and bounded cancellation behavior. Creation order and visual coordinates may
not influence the result.

### D2.4 — Run identity, provenance, and reproducibility record

Define the minimum inspectable run record: workflow identity/content reference,
operation/parameter inputs, runtime/package/environment-relevant metadata,
seed policy, timestamps where appropriate, outcome, diagnostics, and artifact
references. It must distinguish an attempt from its results without promising
the later Phase 6 comparison experience.

### D2.5 — Artifact ownership, local persistence, and cleanup

Decide which run outputs and metadata are durable, their local ownership and
format, retention/removal rules, atomicity, partial-failure handling, and how
the project avoids orphaned or silently overwritten artifacts. Compare no
durable storage, bounded local files, and another proportionate option; do not
introduce a database or broad artifact store by convenience.

### D2.6 — Cache keys, invalidation, and visibility

Decide whether the initial engine reuses any result, which semantic inputs form
the cache key, how a changed workflow/parameter/input/environment invalidates
it, how users and tests can distinguish a cache hit, and how stale results are
prevented. A deliberate no-reuse initial policy is a valid alternative.

### D2.7 — Runtime error envelope and diagnostics bridge

Define how execution failures become stable structured results: affected
operation/run, category, plain-English explanation/remedy, technical detail,
and preservation of the original diagnostic context. It must not expose only a
raw Python exception or fabricate a user-facing UI policy.

### D2.8 — Reference operation and acceptance-workflow boundary

Select the smallest real deterministic operation family and synthetic
controlled inputs needed to prove the engine. It must exercise ordering,
branching, output/artifact handling, failure, and cache behavior without
silently taking ownership of Phase 4 data intake or Phase 5 model behavior.
Any new dependency, fixture, or artifact requires the existing license,
maintenance, provenance, privacy, size, and package-control decisions.

## 6. Workstreams and Proposed Packet Boundaries

| Workstream | Objective | Depends on | Proposed bounded packets |
|---|---|---|---|
| WS2.1 Decisions | Resolve D2.1–D2.8 with evidence and durable tradeoffs | P1 reconciliation | P2-EP01 — execution/run foundation decisions |
| WS2.2 Execution representation | Implement the selected layout-independent plan and runtime binding boundary | D2.1–D2.2 | P2-EP02 — execution representation and contract bridge |
| WS2.3 Planner and dispatcher | Implement deterministic dependency planning, dispatch, branching, and failure flow | D2.2–D2.3, WS2.2 | P2-EP03 — deterministic planner and reference dispatcher |
| WS2.4 Runs, artifacts, and cache | Implement selected run record, artifact ownership, error envelope, and explicit cache rules | D2.4–D2.7, WS2.3 | P2-EP04 — run provenance, artifacts, cache, and runtime diagnostics |
| WS2.5 Reference proof | Prove deterministic successful/failed/branched runs and cache correctness through controlled workflows | D2.8, WS2.2–WS2.4 | P2-EP05 — headless reference-workflow evidence |
| WS2.6 Closeout | Independently reproduce Phase 2 evidence and reconcile the outcome | WS2.1–WS2.5 | P2-EP06 — validation and reconciliation evidence |

These are proposed packet boundaries, not approved packets. Central may split a
packet further when a decision, persistence choice, or operation family needs
separate independent evidence.

## 7. Required Architecture Boundaries

1. Only a workflow that passed Phase 1 validation can enter planning/execution;
   the executor does not repair, default, or reinterpret an invalid document.
2. The intermediate representation and execution plan derive from canonical
   workflow semantics, never browser state, visual coordinates, creation order,
   or generated source code.
3. Runtime dispatch uses only the accepted explicit operation bindings; no
   dynamic imports, arbitrary code, plugin discovery, or LLM-generated source.
4. A run record is an execution/experiment-state concern. It references the
   workflow and owned artifacts without turning the UI or fixture material into
   a source of truth.
5. Cache behavior is either absent or visible, keyed by semantic inputs, and
   invalidated correctly. It cannot hide a changed input, parameter, workflow,
   or relevant environment condition.
6. Artifact writes are owned, bounded, and auditable. Partial failures and
   cleanup must not leave a result that looks successful.
7. Runtime failures retain technical context while providing an actionable
   structured explanation. They do not become unhandled exceptions or silent
   missing results.
8. The frontend remains a later consumer. It may neither compute execution
   semantics nor independently recalculate results.

## 8. Test and Validation Strategy

Every implementation packet must name its final worker-completion attestation
commands and require the complete post-change rerun after an in-scope repair.
Phase 2 adds meaningful automated evidence for:

- deterministic layout/creation-order-independent planning and dispatch;
- valid linear, branched, joined, failed, and invalid-workflow behavior;
- exactly-once shared-upstream work inside a run;
- stable run identity, provenance, seed/environment metadata, result, and
  artifact references appropriate to the selected policy;
- deterministic repeat runs where the selected operation/input permits it;
- changed workflow/input/parameter/relevant-environment cache invalidation and
  observable cache/no-cache behavior;
- owned artifact write, partial-failure, cleanup, and stale-artifact cases;
- plain-English plus technical runtime error envelopes; and
- headless operation with no UI, browser, HTTP workflow API, external dataset,
  ML model, export, or later-phase behavior.

Execution ordering, caching, provenance, and failure behavior require strong
independent validation. Tests cannot treat mock order traces, fabricated run
records, or empty marker packages as proof that the selected runtime path
actually executed the approved reference operations.

## 9. Phase Acceptance Criteria

Phase 2 may be recommended complete only when:

- **P2-AC01:** D2.1–D2.8 are accepted with alternatives, criteria, and
  consequences recorded.
- **P2-AC02:** A valid Phase 1 workflow becomes a layout-independent
  intermediate representation and deterministic execution plan; invalid input
  is refused with actionable information.
- **P2-AC03:** Explicit approved runtime bindings execute a small real
  reference operation family headlessly without dynamic/untrusted code or an
  LLM dependency.
- **P2-AC04:** Creation order and visual position do not alter execution;
  branches share upstream computation exactly as selected and failures behave
  predictably.
- **P2-AC05:** Each run records sufficient inspectable provenance, relevant
  inputs/parameters, environment/seed information, outcome, diagnostics, and
  artifact references for the selected reproduction claim.
- **P2-AC06:** Artifact ownership, persistence, partial-failure handling, and
  cleanup are explicit, bounded, and reproducibly tested.
- **P2-AC07:** Cache behavior is absent or visibly correct: changed semantic
  inputs cannot receive stale output, and cache state is independently tested.
- **P2-AC08:** Runtime errors retain actionable plain-English and technical
  detail without silent failure or raw-exception-only behavior.
- **P2-AC09:** Deterministic reference workflows, repeated runs, invalid
  graphs, branch/failure paths, and cache cases have independent acceptance
  evidence.
- **P2-AC10:** No user-facing editor/API, broad data handling, modeling,
  comparison UX, export, plugins, distributed/cloud execution, or Phase 3+
  behavior is introduced.
- **P2-AC11:** Quality, dependency, license, fixture, artifact, hygiene, and
  documentation evidence remains current; no unapproved dependency or lock
  change is introduced.
- **P2-AC12:** Independent validation has no unresolved Critical or High
  finding, and Central reconciles the phase against OV §§12, 16–19, 21–23, and
  25.

## 10. Phase 2 Guardrails

1. **No UI runtime shortcut:** browser state, graph layout, and generated code
   cannot execute a workflow or become run provenance.
2. **No fake runtime proof:** reference operations must perform the approved
   real computation, not merely emit predetermined test results.
3. **No hidden cache:** no reuse occurs unless the selected cache policy makes
   the key, hit/miss, invalidation, and result ownership testable.
4. **No mutable-history ambiguity:** run identity, attempt outcome, artifact
   references, and partial failures remain distinguishable.
5. **No incidental persistence:** every durable local file has an owner,
   format, retention/cleanup rule, and failure behavior.
6. **No scope theft:** data ownership/profiling, model behavior, experiment
   comparison, UI, and export return to Phases 3–7 unless this plan explicitly
   names a minimal execution-foundation dependency.
7. **No dependency convenience:** a runtime, persistence, or testing dependency
   requires an explicit D2 decision and existing dependency/license controls.
8. **No process dilution:** workers run packet-defined post-change checks and
   repair only in scope or return a named blocker; validation does not replace
   the worker attestation.

## 11. Risks and Controls

| Risk | Control | Escalation condition |
|---|---|---|
| Planner accidentally adopts visual or insertion order | Canonical dependency graph, deterministic tie-breaker, reversal tests | Equivalent workflows produce differing plans/results |
| Cache returns misleading stale output | Explicit keys, hit/miss evidence, semantic invalidation tests | Changed semantic input can reuse a prior result |
| Run records omit necessary provenance | Minimum provenance contract and repeat-run tests | Reproduction claim cannot identify relevant workflow/input/environment/seed |
| Artifacts survive failed work ambiguously | Owned temporary/final paths, atomicity/cleanup policy, failure tests | Failed run leaves output presented as successful |
| Runtime errors lose useful context | Structured envelope with plain-English and technical fields | Failure is raw exception-only, silent, or lacks affected operation |
| Reference proof expands into data/ML product scope | Bounded D2.8 operation decision and fixture controls | A packet introduces user data, training, or Phase 4/5 policy |
| Isolation grows into unnecessary services | Compare local proportionate options before implementation | Proposal adds persistent service/distributed architecture without need |

## 12. Completion and Transition

Independent validation must inspect all D2 decisions, intermediate
representation, planner, dispatcher, run and artifact behavior, provenance,
cache correctness, runtime errors, controlled reference workflows, scope,
locks/dependencies, hygiene, and the absence of Phase 3+ behavior. Central
then reconciles the phase.

Phase 3 planning may open only after that reconciliation. Its starting inputs
will be the accepted runtime invocation and result boundary, run/provenance and
artifact policy, cache semantics, error envelope, reference operation limits,
and the explicit statement that visual design, UI interaction, data ownership,
and modeling policy remain undecided.

## 13. Next Action

This Phase 2 plan is a draft. It needs Central's explicit approval before a
fresh P2-EP01 decision packet may be drafted. Approval of this plan would not
authorize P2-EP01 execution or any Phase 2 implementation.
