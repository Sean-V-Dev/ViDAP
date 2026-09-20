# ViDAP P1-EP01 — Workflow and Compatibility Decisions

| Field | Value |
|---|---|
| Status | Approved for execution |
| Packet version | 0.1 |
| Execution approved | 2026-09-20 by explicit user direction |
| Packet type | Research and decision; documentation-only repository change |
| Parent phase plan | `ViDAP_Phase_1_Plan.md` version 1.0 |
| Prerequisite | Phase 0 complete through P0-EP08 reconciliation |
| Workstream | WS1.1 — Decision records |
| Decisions covered | D1.1 through D1.7 |
| Authorized worker output | `ViDAP_P1_EP01_Decision_Report.md` |
| Created | 2026-09-20 |
| Owner | Central |

---

## 1. Authorization Boundary

This approved packet authorizes one bounded worker to inspect the repository
and research current primary sources, then create only the decision report
named above. It does not authorize workflow source code, tests, controlled
fixtures, schema files, dependencies, lockfile changes, UI work, API work,
local process launches, data/ML behavior, persistence, export, or Phase 2
work.

The worker recommends decisions. A fresh independent validator checks the
report. Only Central may accept D1.1 through D1.7.

## 2. Plain-English Packet Intent

### What this packet does

It selects the rules for the durable language that will describe a ViDAP
workflow before anyone writes that workflow model. The decisions cover the
document shape, identities and references, the first practical port types,
parameter contracts, diagnostics, version handling, and the safe boundary for
adding later node families.

### Why this comes before implementation

If source code is written first, a Python data structure, browser graph
library, or future executor can become the accidental definition of a
workflow. That would undermine the product requirement that UI, execution,
and export share one inspectable, versioned representation.

### What it enables

An accepted decision set gives P1-EP02 through P1-EP05 fixed, testable
constraints for implementing a UI-independent kernel. It does not create that
kernel itself.

### How success is demonstrated

The sole report compares credible alternatives, applies explicit gates and
criteria, cites current primary evidence, makes bounded recommendations for
D1.1 through D1.7, records rejected alternatives and limitations, and leaves
the repository free of product implementation.

## 3. Governing Inputs and Authority

The worker and validator must read these in this order:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§3, 5–7, 15–18, 20–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially its invariants,
   Phase 1 outcome, Phase 2 exclusion, and P1 exit evidence.
4. `ViDAP_Roadmap.md` version 2.1, especially P1 and checkpoint A1.
5. `ViDAP_Phase_1_Plan.md` version 1.0, especially D1.1–D1.7, Sections
   4–10, and P1 acceptance criteria.
6. `ViDAP_P0_EP08_Validation_and_Reconciliation.md`, which establishes
   Phase 0 completion and the permitted Phase 1 planning gate.
7. Accepted Phase 0 reconciliation records and decisions, particularly the
   local web/Python topology; Node 24/npm and uv-managed CPython 3.14
   baseline; authoritative quality controls; dependency/license policy; and
   controlled-fixture rules.
8. This packet.

The product overview and approved spine prevail if a lower-level artifact is
unclear. None of these inputs authorize implementation beyond this packet.

## 4. Objective and Completion Condition

### Objective

Produce evidence-backed recommendations for:

- **D1.1:** canonical workflow encoding and document envelope;
- **D1.2:** identity, graph references, and semantic/layout separation;
- **D1.3:** practical type and connection-compatibility model;
- **D1.4:** node parameter and contract model;
- **D1.5:** validation model and actionable diagnostics;
- **D1.6:** schema versioning, migration, and compatibility policy; and
- **D1.7:** node registration and extension boundary.

### Completion condition

P1-EP01 is complete only when:

1. The authorized decision report exists and passes the worker's required
   self-check.
2. A fresh independent validator returns `Accept`.
3. No material uncertainty, policy conflict, license issue, or unbounded
   implementation dependency is hidden in the recommendation.
4. Central separately accepts, rejects, or returns each D1 decision for
   revision in a reconciliation record.

## 5. Preconditions and Stop Gates

Before writing the report, the worker must confirm and record:

1. This exact packet version has explicit execution approval.
2. The Phase 1 plan remains approved and P0-EP08 remains complete.
3. The current branch, commit, sanitized remote identity, worktree state, and
   any pre-existing changed or untracked files are known.
4. No existing workflow/schema source, fixture, decision report, or other
   file conflicts with the one output path in Section 9.
5. Existing Node 24/npm and uv-managed CPython 3.14 paths are callable enough
   to run the inherited final attestation; a known restricted-sandbox
   `uv.exe` access limitation must be retried through the normal Windows
   path before reporting a project failure.
6. Research can rely on primary sources: relevant standards/specifications,
   official project documentation, official registries, or authoritative
   license text.

Stop and return a `Blocked` report if a required choice needs an unapproved
dependency, cannot be reconciled with an overview/spine invariant, depends on
running a prototype, requires a material user-product choice, or cannot be
supported by sufficiently reliable documentary evidence.

## 6. Non-Negotiable Decision Constraints

Every recommendation must preserve all of the following:

1. The canonical workflow is an open, versioned, source-control-readable,
   programmatically manipulable structured document.
2. Browser state, visual coordinates, viewport data, serialized member order,
   and node creation order cannot define workflow semantics or future
   execution order.
3. The workflow/schema layer owns workflow meaning, nodes, ports, edges,
   validation, and serialization. UI, execution, experiment/state, and export
   are separate consumers.
4. The first type system must be practical and deliberately small. It must
   leave an explicit extension path for later tabular data, split, model,
   prediction, metric, and artifact families without pretending they are
   already implemented.
5. A node contract is declarative metadata. It is not a permission to import
   an ML library, execute arbitrary code, dynamically load a plugin, write a
   file, or call a server.
6. Diagnostics must distinguish structural invalidity, semantic invalidity,
   and unsupported future capability. They need stable machine-readable
   identity plus a plain-English remedy.
7. Version behavior must be visible and fail safely. Do not invent a legacy
   document or a migration merely to claim compatibility.
8. Unknown fields, nodes, versions, and parameter values follow an explicit
   selected policy; none may be silently discarded.
9. No recommendation may make UI behavior, an HTTP API, persistence,
   execution planning, caching, run records, exports, agents, or data/ML
   libraries a Phase 1 requirement.
10. The report is an architecture decision, not legal advice. Any prospective
    external library must have current maintenance, license, compatibility,
    and package-boundary evidence before a later implementation packet may
    select it.

## 7. Required Decision Analysis

The worker must use the following gates before recommending any candidate.
Failure of a gate makes that candidate ineligible regardless of any score.

| Gate | Required result |
|---|---|
| G1 — Open inspection | Documents can be read, diffed, and constructed without a browser or proprietary service. |
| G2 — Deterministic meaning | Semantics are independent of layout, creation order, and member order. |
| G3 — Layer separation | The proposed representation does not import or depend on UI, runtime, experiment, or export behavior. |
| G4 — Safe evolution | Version, unknown-element, and compatibility behavior can be explicit and fail safely. |
| G5 — Practical validation | Structural and semantic errors can identify the affected element and offer a stable actionable diagnostic. |
| G6 — Extensibility without code loading | Later node families can register declaratively without a marketplace or dynamic untrusted execution. |
| G7 — Implementation proportion | The decision can be implemented with a small Phase 1 kernel, without a universal ontology or Phase 2 engine. |
| G8 — License and maintenance posture | Any cited implementation aid is not assumed selectable without later direct-dependency evidence. |

For each D1 decision, compare at least two credible choices using the common
criteria below. A choice can be inherited or deferred only with a specific
reason.

| Criterion | Weight |
|---|---:|
| Alignment with the overview and spine | 20 |
| UI/runtime/export separation | 18 |
| Determinism and source-control usability | 15 |
| Validation and diagnostic clarity | 15 |
| Safe evolution and compatibility | 12 |
| Programmatic Python fit | 10 |
| Practical, bounded Phase 1 implementation | 10 |
| **Total** | **100** |

Scores use 1–5, include a rationale and evidence-confidence label, and are an
aid to reasoning rather than an automatic decision. The report must explain
any recommendation that differs from the numerical leader.

### D1.1 — Encoding and envelope

Compare at minimum:

- a plain JSON workflow document with documented validation;
- JSON with a formal schema artifact as a normative or supplementary
  contract; and
- one other bounded structured-document approach only if it materially changes
  the decision.

Specify candidate top-level fields, canonical serialization expectations,
whether a schema artifact is itself canonical or only a validator aid, and the
policy for extra fields. Do not create a schema file.

### D1.2 — Identity, references, and layout

Compare stable opaque IDs with at least one human-derived alternative. Define
workflow/node/port/edge identities, duplicate and dangling-reference behavior,
edge direction, whether edge identity is required, and how optional layout is
isolated from semantics. The decision must state that execution order remains
for Phase 2.

### D1.3 — Types and connection compatibility

Compare a minimal nominal vocabulary, a structural/type-expression approach,
and one permissive alternative if it is credible. Select the smallest
initial vocabulary, port cardinality rules, compatibility relation, and
explicit-adapter policy. Explain how later data/model families can extend it
without treating all values as interchangeable.

### D1.4 — Parameters and contracts

Compare a declarative contract with UI-owned validation and a runtime-owned
contract as rejected alternatives. Define parameter identity, requiredness,
defaults, shape/range/enum constraints, unknown parameter behavior, and the
minimum non-executing metadata a future runtime/exporter may need.

### D1.5 — Validation and diagnostics

Compare boolean/exception-only reporting with a structured diagnostic model.
Specify structural versus semantic stages, stable diagnostic code, severity,
affected element reference, plain-English message/remedy, and technical
detail. No raw exception becomes a user contract.

### D1.6 — Versions and migration

Compare strict-single-version rejection, explicit migration, and any
forward-compatible extension policy. Specify the initial version, version
location, future-version/unknown-field/node response, compatibility promise,
and the rule that no migration is implemented until a real predecessor exists.

### D1.7 — Registration and extension

Compare static in-process registration, manifest/discovery approaches, and
dynamic plugin loading. Specify the selected registry ownership, duplicate
node-type behavior, built-in versus future extension boundary, and prohibition
on executing third-party code simply to discover a node definition.

## 8. Research and Evidence Rules

1. Check changeable facts at execution time. Cite primary sources with
   retrieval dates.
2. Separate facts from architectural inferences.
3. Do not install, download, clone, run, or benchmark a candidate library or
   standard implementation. Documentary research is sufficient here.
4. Do not use a blog, AI output, or a secondary comparison as the sole support
   for a technical claim where a primary source exists.
5. Treat standards as evidence about their defined behavior, not proof that a
   particular library implements them correctly.
6. Record uncertainty and its owner. A choice that needs a prototype becomes a
   separately proposed, unexecuted spike rather than expanding this packet.
7. Do not copy large text from any source. Summarize in the report and use
   only brief quotations where exact wording matters.

## 9. Exact Authorized Output

The worker may create or modify only:

`ViDAP_P1_EP01_Decision_Report.md`

The report must contain:

1. Packet metadata; authorization; governing-input versions; and a sanitized
   repository baseline.
2. A current primary-source bibliography with retrieval dates.
3. Gates G1–G8 and the weighted comparison evidence for every D1 decision.
4. A clear recommended decision for D1.1 through D1.7, including rejected
   alternatives, confidence, limitations, and downstream consequences.
5. A single cross-decision contract map showing which layer owns document
   meaning, layout metadata, contracts, validation, serialization,
   versioning, registry extension, and deferred execution concerns.
6. The proposed minimum canonical document fields and illustrative values in
   prose or non-authoritative pseudocode only. It must not be a committed
   schema, fixture, source file, or executable sample.
7. The selected unknown-field/node/version policy and diagnostic envelope in
   precise enough language for later packets to test.
8. A table of explicit Phase 2+ deferrals and their owning phase.
9. Blocking and non-blocking findings, plus any separately proposed
   feasibility spike using Section 11's template.
10. The worker's self-assessment against Section 12 and final command/scope
    evidence.

No other file may be added, modified, moved, staged, committed, or deleted.

## 10. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read every governing input and record their versions.
2. Record the baseline branch, commit, worktree state, output-path collision
   check, and lock hashes. Identify pre-existing changes without overwriting
   them.
3. Gather current primary evidence and apply G1–G8.
4. Compare each D1 choice using the Section 7 matrix. Record facts,
   inferences, confidence, and rejected alternatives.
5. Draft only the decision report, keeping proposed document examples
   explicitly non-authoritative and non-executable.
6. Re-read the report against every requirement in Sections 4, 6–9, and 12.
7. Run `npm.cmd run check` after the report is complete. If it fails, fix
   only an authorized report issue if one caused the failure, then rerun it.
   Otherwise stop and report the unrelated blocker; do not claim completion.
8. Confirm both lock hashes are unchanged; run `git diff --check`; inspect
   final Git status and the exact changed/untracked path set.
9. Record the command results and final self-assessment in the report, then
   stop for independent validation.

The worker must not self-validate, stage, commit, push, or start P1-EP02.

## 11. Feasibility-Spike Proposal Template

If documentary evidence cannot settle a material D1 decision, the report may
propose—but may not execute—a separate spike with:

- one precise question and why it affects the decision;
- sources checked and remaining uncertainty;
- hypothesis and bounded actions;
- exact files, commands, dependencies, or processes requested;
- time/effort limit, success/failure signals, cleanup, and lock/scope proof;
- license/security implications; and
- the effect of each outcome on D1 and the next packet.

The worker returns `Blocked` when the unresolved question prevents a
responsible recommendation.

## 12. Acceptance Criteria

P1-EP01 may be accepted only when:

- **EP01-AC01:** Authority, prerequisite completion, governing versions,
  baseline, and pre-existing work are accurately recorded without sensitive or
  user-specific information.
- **EP01-AC02:** D1.1–D1.7 are each addressed with a recommended decision,
  alternatives, evidence confidence, and consequences.
- **EP01-AC03:** All G1–G8 gates are applied consistently before scoring.
- **EP01-AC04:** Each D1 comparison uses the full weighted criteria, with
  reproducible totals and stated rationale.
- **EP01-AC05:** Current changeable claims use primary sources with retrieval
  dates, and the report labels inference separately from source facts.
- **EP01-AC06:** D1.1 selects an open, readable, deterministic,
  programmatically usable document envelope without making a browser or
  generated code authoritative.
- **EP01-AC07:** D1.2 protects semantic meaning from layout, member order,
  and creation order, and keeps execution order deferred to Phase 2.
- **EP01-AC08:** D1.3 and D1.4 select a small declarative, extensible
  contract/type model that rejects or flags invalid connections and parameters
  without implementing data/ML behavior.
- **EP01-AC09:** D1.5 specifies stable structured diagnostics with affected
  element, plain-English remedy, and technical detail.
- **EP01-AC10:** D1.6 makes version, migration, unknown-field/node, and
  forward-compatibility behavior explicit without fabricating legacy support.
- **EP01-AC11:** D1.7 preserves static, declarative extension without dynamic
  untrusted code loading or a plugin marketplace.
- **EP01-AC12:** The cross-decision contract map retains clear UI,
  workflow/schema, execution, experiment/state, and export ownership.
- **EP01-AC13:** Phase 2 execution, persistence, API, UI editor, data/ML,
  experiments, export, and autonomous behavior remain explicitly deferred.
- **EP01-AC14:** Any external library or schema aid is treated as a later
  dependency decision, not selected or installed by this report.
- **EP01-AC15:** No source, test, fixture, manifest, lock, dependency,
  configuration, workflow, process, remote state, or product behavior changes.
- **EP01-AC16:** The decision report is the worker's only repository change.
- **EP01-AC17:** `npm.cmd run check` passes after report completion; both
  lock hashes remain unchanged; `git diff --check` passes; and final scope
  evidence distinguishes worker output from pre-existing work.
- **EP01-AC18:** A fresh independent validator finds the analysis
  reproducible, internally consistent, and aligned with the overview, spine,
  roadmap, and Phase 1 plan.
- **EP01-AC19:** Central explicitly accepts D1.1–D1.7 before this packet is
  marked complete or a P1 implementation packet is drafted.

## 13. Independent Validation Contract

The validator must use a fresh chat and must:

1. Read every governing input, this packet, and the worker decision report.
2. Recheck high-impact primary sources and all claims that are current or
   could materially change the recommendation.
3. Recalculate every comparison total and verify gates are consistently
   applied.
4. Challenge at least one credible rejected alternative for every D1 decision.
5. Confirm the proposed document, identity, type, parameter, diagnostic,
   compatibility, and registry rules preserve the mandatory boundaries.
6. Confirm no decision silently chooses a new dependency, runtime, UI
   library, executor, persistence mechanism, API, or export approach.
7. Verify `npm.cmd run check`, unchanged locks, `git diff --check`, final
   file scope, and absence of product/Phase 2 work.
8. Return exactly one verdict: `Accept`, `Revise`, or `Blocked`, with
   criterion-linked findings and named owner.

The validator must not modify any file, accept D1.1–D1.7 for Central, alter
remote state, or begin P1-EP02.

## 14. Evidence Return to Central

The worker must return:

- the path to `ViDAP_P1_EP01_Decision_Report.md`;
- current commit and sanitized final worktree status;
- the research sources and read-only commands used;
- final `npm.cmd run check`, lock-hash, and whitespace/scope results;
- a criterion-by-criterion worker self-assessment;
- blockers, non-blocking limitations, and any spike proposal; and
- an independent-validation handoff stating that no decision is accepted yet.

## 15. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P1_EP01.md` version 0.1 as a bounded Phase 1 decision worker. Read all governing inputs and follow the packet exactly. Research and recommend D1.1 through D1.7, but create or modify only `ViDAP_P1_EP01_Decision_Report.md`. Do not write schema, source, tests, fixtures, manifests, locks, configuration, or decision-record files; do not install or execute candidate tools; do not launch processes; and do not perform UI, API, persistence, data/ML, export, or Phase 2 work. Every proposed example must be explicitly non-authoritative and non-executable. Apply G1–G8, compare credible alternatives for each decision, cite current primary evidence, and return a bounded spike proposal if evidence is insufficient. Before reporting completion, run `npm.cmd run check`, confirm locks are unchanged, run `git diff --check`, and record exact scope evidence. If a final check fails, resolve only an authorized report-caused issue and rerun; otherwise stop with a blocker. Do not self-validate, accept decisions for Central, stage, commit, push, change remote state, or begin P1-EP02.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P1_EP01.md` version 0.1. Read all governing inputs, the packet, and `ViDAP_P1_EP01_Decision_Report.md`. Recheck high-impact current primary sources, recalculate every weighted comparison, test G1–G8 consistency, and challenge a credible rejected alternative for each D1 decision. Verify that the recommended document/identity/type/parameter/diagnostic/version/registry decisions preserve canonical workflow ownership, semantic/layout separation, safe evolution, declarative extension, and Phase 2 deferrals. Verify the required post-report `npm.cmd run check`, unchanged lock hashes, `git diff --check`, final file scope, and absence of any implementation or later-phase work. Do not edit files, install tools, change remote state, accept D1 decisions for Central, or begin P1-EP02. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and owners.

## 16. Next Action

P1-EP01 is approved for bounded execution. A fresh worker may create only the
decision report. Its completion still requires independent validation and
Central acceptance of D1.1–D1.7; neither outcome authorizes workflow-model
implementation.
