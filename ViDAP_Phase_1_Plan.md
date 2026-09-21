# ViDAP Phase 1 Plan — Canonical Workflow and Node Contract Kernel

| Field | Value |
|---|---|
| Status | Complete — centrally reconciled |
| Version | 2.3 |
| Parent | ViDAP_Roadmap.md version 3.4 |
| Spine phase | Phase 1 — Canonical Workflow and Node Contract Kernel |
| Product source | ViDAP_Overview.txt |
| Prerequisite | Phase 0 complete through P0-EP08 reconciliation |
| Created | 2026-09-19 |
| Approved | 2026-09-20 by explicit user direction |
| Last updated | 2026-09-21 after P1-EP06 acceptance and Phase 1 reconciliation |
| Owner | Central |

---

## 1. Authorization and boundary

This approved plan turns the approved Phase 1 outcome into decision work,
bounded workstreams, acceptance evidence, and proposed execution-packet
boundaries. Its approval authorizes Central to prepare the first Phase 1
execution packet; it does not authorize implementation, dependency changes,
source changes, or a Phase 2 execution engine.

Phase 1 establishes the canonical, UI-independent description of a workflow
and its node contracts. It must not become a visual editor, a data loader, an
ML runtime, a persistence system, an experiment system, or an exporter.

## 2. Plain-English phase intent

### What we are building or changing

We will define the durable structured language that future users, the visual
editor, the execution host, and an exporter will all use to describe the same
workflow. It will say what nodes exist, what they accept and produce, how they
connect, which parameters they carry, and why an invalid workflow is invalid.

### Why the system needs it

Without one canonical workflow representation, the browser layout, Python
runtime, and later notebook export could each invent their own interpretation
of a graph. That would make the application misleading: a graph could look
valid while executing or exporting differently.

### What real behavior it enables

A developer or future user-facing layer will be able to create, inspect,
validate, serialize, deserialize, and programmatically modify a small
workflow without a browser or running ML operation. Later phases can use that
same workflow as their only semantic input.

### How we will know it works

Representative valid, invalid, branched, and versioned workflows will
round-trip deterministically. Invalid connections, missing or invalid
parameters, unknown node types, duplicate identities, cycles, and unsupported
schema versions will return useful structured diagnostics. Changing visual
layout must not change workflow meaning.

## 3. Authority, prerequisites, and handoff

The Phase 1 plan and every child packet must read:

1. Current explicit user direction.
2. ViDAP_Overview.txt, especially OV Sections 3, 5-7, 15-18, 20-23, and
   25-30.
3. ViDAP_Phased_Plan_Spine.md version 1.2, especially Phase 1, the canonical
   workflow invariant, typed contracts, layer separation, and validation
   scaling.
4. ViDAP_Roadmap.md version 3.4, especially P1 and checkpoint A1.
5. ViDAP_Phase_0_Plan.md version 1.9 and
   ViDAP_P0_EP08_Validation_and_Reconciliation.md.
6. The accepted P0 decision/reconciliation records, particularly D0.1-D0.3
   for the local web/Python architecture, repository topology, and runtime
   contracts; D0.4-D0.7 for quality, dependency, fixture, and safety rules.
7. This plan and any later accepted Phase 1 decision records.

Phase 0 hands forward a single repository; apps/web for presentation;
python/src/vidap_workflow as the intended canonical workflow ownership area;
separate execution, experiment, and export ownership areas; Node 24/npm;
uv-managed CPython 3.14; locked dependencies; Windows-only tested support; and
authoritative quality/CI commands. It does not hand forward a workflow schema,
API payload, persistence format, error envelope, execution representation, or
node family implementation.

## 4. Phase outcome and exclusions

### Required outcome

Phase 1 delivers an open, versioned, inspectable, programmatically
manipulable workflow representation with extensible node definitions, typed
ports, parameter contracts, semantic validation, serialization, and
compatibility handling. The canonical representation remains independent of
visual layout and execution order.

### Explicit exclusions

Phase 1 does not deliver:

- a production graph editor, React Flow integration, node palette, forms, or
  user-facing workflow editing experience;
- data loading, profiling, transformations, real ML libraries, model training,
  prediction, metrics, results, or a Python execution engine;
- dependency-derived execution ordering, intermediate execution planning,
  caching, artifact persistence, run records, or experiment comparison;
- notebook/Python generation, import, export parity, or arbitrary
  notebook-to-graph reconstruction;
- database/filesystem workflow persistence beyond the bounded serialized
  workflow values used in tests and controlled fixtures;
- an HTTP workflow API, browser/server contract, public binding, desktop
  packaging, hosting, agent interface, or new autonomous behavior; or
- a universal type system, arbitrary code node, plugin marketplace, or a
  promise that every future node category is implemented now.

## 5. Phase 1 decisions

No implementation packet may assume a decision below until its decision record
is independently validated and accepted by Central.

### D1.1 — Canonical workflow encoding and document envelope

Select the durable workflow encoding and minimum top-level fields. Compare at
least a plain structured JSON document, a schema-backed JSON document, and one
other bounded representation only if it materially improves the criteria.

Required criteria: openness, source-control readability, deterministic
serialization, programmatic manipulation, validation ergonomics, evolution,
safe handling of unknown fields/types, Python fit, and no dependence on UI
coordinates or generated code.

### D1.2 — Identity, graph references, and semantic/layout separation

Define stable workflow, node, port, and edge identity rules; reference
integrity; duplicate handling; and the treatment of optional visual metadata.
The decision must prove that node creation order, serialized member order, and
layout/viewport metadata cannot define semantic execution meaning.

### D1.3 — Practical type and connection compatibility model

Define the initial type vocabulary, input/output port cardinality, compatibility
rules, and whether a type relationship is exact, assignable, or explicitly
adapted. It must reject or clearly flag invalid connections while remaining
small enough to evolve for later table, split, model, prediction, metric, and
artifact families.

### D1.4 — Node parameter and contract model

Define required versus optional parameters, defaults, value shape, allowed
values/ranges, unknown parameters, validation ownership, and the minimum
runtime/export metadata placeholder needed without choosing runtime or export
behavior. A parameter displayed later by UI must have one canonical contract
source and cannot silently be ignored.

### D1.5 — Validation model and actionable diagnostics

Define structural and semantic validation stages; diagnostic identity,
severity, affected workflow element, machine-readable reason, and
plain-English explanation/remedy fields. The decision must distinguish an
invalid workflow from an unsupported future capability and retain technical
detail without making raw exceptions the user-facing contract.

### D1.6 — Schema versioning, migration, and compatibility policy

Define the initial schema version, version detection, supported historical
versions, migration/no-migration behavior, future unknown field/node handling,
and failure behavior. The phase may establish a migration extension point but
must not fabricate a historical migration that has no predecessor.

### D1.7 — Node registration and extension boundary

Define how approved node definitions are registered and discovered, which
parts are canonical data versus implementation references, and how a later
node family extends the registry without changing the workflow core or visual
editor. It must not select a third-party plugin system or dynamically execute
untrusted code.

## 6. Workstreams and proposed packet boundaries

| Workstream | Objective | Depends on | Proposed bounded packets |
|---|---|---|---|
| WS1.1 Decision records | Resolve D1.1-D1.7 with evidence and durable tradeoffs | Phase 0 reconciliation | Complete: P1-EP01 reconciliation accepts D1.1-D1.7 |
| WS1.2 Canonical document kernel | Implement the selected workflow document, identities, edges, and semantic/layout boundary | D1.1-D1.2 | Complete: P1-EP02 accepted document kernel |
| WS1.3 Contracts and registry | Implement selected node definitions, ports, parameter contracts, and registration rules | D1.3-D1.4, WS1.2 | Complete: P1-EP03 accepted contracts and static registry |
| WS1.4 Semantic validation | Implement deterministic structural/semantic validation and diagnostics | D1.5, WS1.2-WS1.3 | Complete: P1-EP04 accepted validation/diagnostics |
| WS1.5 Compatibility proof | Implement selected version handling and controlled fixtures/examples | D1.6-D1.7, WS1.2-WS1.4 | Complete: P1-EP05 accepted compatibility proof |
| WS1.6 Closeout | Independently reproduce Phase 1 evidence and reconcile the outcome | WS1.1-WS1.5 | Complete: P1-EP06 accepted and Phase 1 reconciled |

These are proposed boundaries, not approved packets. Central may split a
packet further if a decision or implementation unit is not independently
testable. Decisions must remain separate from implementation when their
outcome would materially determine the design.

## 7. Required model boundaries

The following direction is mandatory regardless of the selected encoding:

1. The canonical workflow is owned by the workflow/schema layer, not browser
   state, visual coordinates, execution code, or export code.
2. Visual metadata may be preserved as optional non-semantic information, but
   removing or changing it must not change semantic validation or the future
   execution plan.
3. Execution, experiment, and export layers may consume validated workflow
   semantics later; the workflow layer does not import their implementations.
4. The web application may later present contract-derived forms or
   representations, but it cannot be the sole constructor, validator, or
   interpreter of a workflow.
5. A workflow document must be inspectable and constructible without the UI,
   and test fixtures are consumers rather than semantic authorities.
6. A node definition describes contracts and approved metadata; it is not
   permission to execute a library, write arbitrary code, or introduce data
   science behavior in Phase 1.
7. Execution order, run identity, cache policy, artifact ownership, and
   persistence remain owned by Phase 2 decisions.

## 8. Test and validation strategy

Every implementation packet must specify its final worker-completion
attestation commands under the Spine rule. The Phase 1 suite must add
meaningful automated evidence for:

- deterministic create/serialize/deserialize/validate round-trips;
- valid linear and branched examples;
- invalid or missing node/edge references, duplicate identities, cycles,
  incompatible ports, required-input violations, and parameter violations;
- source-order and visual-layout invariance;
- stable diagnostic identifiers, affected-element references, and
  plain-English/actionable diagnostic content;
- schema version detection, supported/unsupported version behavior, and any
  approved migration;
- unknown node/field behavior under the selected compatibility policy;
- registry extension without core-schema modification; and
- programmatic construction/modification without a browser, server, or ML
  execution process.

Tests must not mistake a visual rendering, a mock execution result, or an
empty marker package for semantic validation. Any later frontend or Python
boundary representation must be tested as a consumer of the canonical
workflow, not as a competing authority.

## 9. Phase acceptance criteria

Phase 1 may be recommended complete only when:

- **P1-AC01:** D1.1-D1.7 are accepted and recorded with their alternatives,
  criteria, and consequences.
- **P1-AC02:** The canonical workflow is open, versioned, inspectable,
  deterministic to serialize, and programmatically constructible without UI.
- **P1-AC03:** Stable identities and edges preserve reference integrity;
  duplicate/missing/dangling identities fail usefully.
- **P1-AC04:** Node contracts explicitly define ports, practical types,
  parameter requirements, and validation ownership.
- **P1-AC05:** Invalid type/cardinality connections and invalid parameter/input
  states are rejected or clearly flagged with actionable diagnostics.
- **P1-AC06:** Visual metadata and creation/member order do not change
  canonical workflow semantics, validation outcome, or the future execution
  meaning.
- **P1-AC07:** Valid, invalid, branched, and versioned representative
  workflows round-trip deterministically and retain intended meaning.
- **P1-AC08:** Version handling, unknown fields/nodes, and any migration
  behavior are explicit, tested, and backward-compatible where reasonable.
- **P1-AC09:** The registration/extension boundary permits later node families
  without modifying the workflow core or invoking untrusted code.
- **P1-AC10:** No execution engine, data/ML operation, user-facing graph
  editor, browser/server workflow API, persistence system, export generator,
  or Phase 2+ behavior is introduced.
- **P1-AC11:** Quality, dependency, license, fixture, repository-hygiene, and
  documentation evidence remain current; no unapproved dependency or lock
  change is introduced.
- **P1-AC12:** Independent validation has no unresolved Critical or High
  finding, and Central reconciles the phase against OV Sections 6-7, 16-18,
  21-22A, and 25.

## 10. Phase 1 guardrails

1. **No UI-as-schema shortcut:** React Flow nodes/edges, form state, browser
   storage, and viewport coordinates cannot become canonical workflow truth.
2. **No runtime in the kernel:** A node contract is not a call to FastAPI,
   pandas, scikit-learn, or any model library.
3. **No premature universal ontology:** Start with a small practical type
   vocabulary and explicit extension rules, not every theoretical data-science
   type.
4. **No opaque validation:** A boolean valid/invalid result alone is
   insufficient; diagnostics must identify the affected element and remedy.
5. **No silent compatibility:** Unsupported versions, unknown node types, and
   invalid fields must follow a selected visible policy.
6. **No fake migrations:** Do not invent legacy files or migration behavior
   merely to claim version support.
7. **No fixture drift:** Representative workflows require provenance, purpose,
   expected outcome, and permitted consumer documentation under D0.7.
8. **No dependency convenience:** A schema, graph, validation, or plugin
   dependency requires an explicit license, maintenance, packaging, and
   compatibility decision before addition.
9. **No process dilution:** A worker must run packet-defined final checks and
   report a blocker rather than defer a missed check to validation.
10. **No phase leakage:** Findings about execution ordering, run records,
    caching, frontend interaction, or export return to their owning later
    phase unless the narrow kernel requirement requires a decision now.

## 11. Risks and controls

| Risk | Control | Escalation condition |
|---|---|---|
| Encoding cannot evolve without breakage | Explicit version/unknown-field policy and representative version tests | No candidate can preserve readable source-control documents and safe evolution |
| Type system becomes either arbitrary wires or unusably academic | Small initial vocabulary, explicit compatibility table, extension boundary | Required future families cannot be represented without redefining existing semantics |
| Browser layout becomes semantic truth | Layout-invariance tests and UI-independent constructors | A proposed representation needs UI coordinates or browser state to validate |
| Contracts duplicate across UI/runtime/export | Canonical contract ownership and consumer-only boundaries | A proposed layer independently redefines port/parameter semantics |
| Diagnostics are technically correct but unusable | Required affected element plus plain-English remedy and technical detail | Validator cannot identify a meaningful action from representative failures |
| Registry becomes arbitrary plugin/code execution | Static approved registration model and no dynamic code loading | Extension requires executing untrusted third-party code |
| Phase 1 quietly implements execution | Exact packet scope and tests prohibiting ML/runtime behavior | A packet adds real data processing, dependency ordering, or run results |

## 12. Phase 1 completion and transition

Independent validation must inspect decisions, all implementation packets,
representative workflow fixtures, schema/version behavior, diagnostics,
layout/order invariance, scope, locks/dependencies, hygiene, and the absence
of Phase 2+ behavior. Central then reconciles completion.

Phase 2 planning may open only after that reconciliation. Its starting inputs
will be the accepted canonical workflow, node/port/parameter contracts,
validation and diagnostic model, versioning policy, registry extension
boundary, known limitations, and the explicit statement that execution
semantics remain undecided.

## 13. Next action

P1-EP01 and P1-EP02 are complete. D1.1-D1.7 are accepted in
`ViDAP_P1_EP01_Validation_and_Reconciliation.md`, and the bounded document
kernel is accepted in `ViDAP_P1_EP02_Validation_and_Reconciliation.md`.
P1-EP01 through P1-EP06 are complete. Phase 1 is reconciled in
`ViDAP_P1_EP06_Validation_and_Reconciliation.md`. Central may now draft the
Phase 2 plan — Deterministic Execution and Run Foundations. A Phase 2 plan
would require its own approval before any P2 execution packet is drafted or
implemented.
