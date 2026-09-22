# ViDAP P2-EP01 — Execution and Run Foundation Decisions

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Research and decision; documentation-only repository change |
| Parent phase plan at authorization | `ViDAP_Phase_2_Plan.md` version 1.2 |
| Prerequisite | Phase 1 complete through P1-EP06 reconciliation |
| Workstream | WS2.1 — Decisions |
| Decisions covered | D2.1 through D2.8 |
| Authorized worker output | `ViDAP_P2_EP01_Decision_Report.md` |
| Central reconciliation | `ViDAP_P2_EP01_Validation_and_Reconciliation.md` |
| Created | 2026-09-21 |
| Approved | 2026-09-21 by explicit user direction |
| Completed | 2026-09-21 by explicit Central acceptance |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved this exact version on 2026-09-21. That approval authorizes one
bounded worker to inspect the repository and research current primary sources,
then create only the decision report named above. It does not authorize
execution source/tests, reference operations, fixtures, data, dependencies,
locks, subprocesses, local services, artifact files, persistence, UI/API work,
remote changes, or P2-EP02 work.

The worker recommends decisions. A fresh independent validator checks the
report. Only Central may accept D2.1 through D2.8.

## 2. Plain-English Packet Intent

### What this packet does

It decides the rules the future engine must follow before anyone builds it:
where execution lives, how a validated workflow becomes an execution plan, how
the plan runs deterministically, what a run remembers, who owns artifacts,
when cache reuse is valid, how failure is described, and what the smallest
real reference proof may be.

### Why this comes before implementation

If source code is written first, process behavior, temporary files, or a test
fixture can become the accidental definition of a run. That would risk stale
results, invisible failures, and an engine shaped around a browser or one
future model library.

### What it enables

Accepted decisions give P2-EP02 through P2-EP05 fixed, testable boundaries for
a headless deterministic engine and its minimal run record. They do not create
that engine, any operation, or a user-facing feature.

### How success is demonstrated

The sole decision report compares credible alternatives, applies explicit
gates and weighted criteria, cites current primary evidence, recommends a
bounded D2.1–D2.8 set, identifies limitations and Phase 3+ deferrals, and
leaves the repository free of runtime implementation.

## 3. Governing Inputs and Authority

The worker and validator must read these in order:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.3, especially invariants 1–18,
   Phase 2, execution-isolation/artifact-persistence decisions, and strong
   validation scaling.
4. `ViDAP_Roadmap.md` version 3.9, especially P2 and checkpoint A2.
5. `ViDAP_Phase_2_Plan.md` version 1.2, especially D2.1–D2.8, Sections 4,
   7–11, and P2 acceptance criteria.
6. `ViDAP_P1_EP06_Validation_and_Reconciliation.md`, authoritative for Phase
   1 completion and the Phase 2 planning gate.
7. Every accepted P1 reconciliation record and its decisions D1.1–D1.7,
   especially canonical workflow ownership, static contracts/registry,
   validation/diagnostics, strict compatibility, and controlled fixtures.
8. `UX refinement.txt` as a consultative visual-direction reference only. Its
   completed-phase claims are non-authoritative; it cannot make UI behavior or
   speculative cache optimization a Phase 2 requirement.
9. Accepted Phase 0 controls for the local web/Python topology, Node 24/npm,
   uv-managed CPython 3.14, quality/CI, dependency/license policy, and
   controlled fixture policy.
10. This packet.

The overview and approved spine prevail if a lower-level artifact is unclear.
None of these inputs authorize implementation beyond this packet.

## 4. Objective and Completion Condition

### Objective

Produce evidence-backed recommendations for:

- **D2.1:** execution isolation and local lifecycle;
- **D2.2:** intermediate execution representation and runtime binding;
- **D2.3:** deterministic planning, shared-upstream work, and failure flow;
- **D2.4:** run identity, provenance, and reproducibility record;
- **D2.5:** artifact ownership, local persistence, and cleanup;
- **D2.6:** cache keys, invalidation, and visibility;
- **D2.7:** runtime error envelope and diagnostics bridge; and
- **D2.8:** reference operation and acceptance-workflow boundary.

### Completion condition

P2-EP01 is complete only when:

1. The authorized decision report exists and passes the worker's required
   self-check.
2. A fresh independent validator returns `Accept`.
3. No material uncertainty, policy conflict, license issue, unbounded
   persistence choice, or implementation dependency is hidden in a
   recommendation.
4. Central separately accepts, rejects, or returns each D2 decision for
   revision in a reconciliation record.

## 5. Preconditions and Stop Gates

Before writing the report, the worker must confirm and record:

1. This exact packet version has explicit execution approval.
2. The Phase 2 plan remains approved and P1-EP06 remains complete.
3. The current branch, commit, sanitized remote identity, worktree state, and
   pre-existing changed/untracked files are known.
4. No existing runtime, decision report, artifact policy, fixture, or other
   file conflicts with the one output path in Section 9.
5. Existing Node 24/npm and uv-managed CPython 3.14 paths are callable enough
   for the final attestation; a known restricted-sandbox `uv.exe` access
   limitation must be retried through the normal Windows path before reporting
   a project failure.
6. Research can rely on primary sources: relevant language/platform
   documentation, standards, official project documentation, official
   registries, or authoritative license text.

Stop and return a `Blocked` report if a required choice needs an unapproved
dependency, cannot preserve a Phase 1 or spine invariant, needs a prototype to
avoid a material product decision, depends on user data/model behavior, or
cannot be supported by sufficiently reliable documentary evidence.

## 6. Non-Negotiable Decision Constraints

Every recommendation must preserve all of the following:

1. Only a workflow that passes the accepted Phase 1 validation boundary enters
   planning or execution. The engine does not repair, default, or reinterpret
   invalid input.
2. Execution plan/order derives from canonical dependencies, never browser
   state, region placement, node creation order, JSON member order, generated
   source, or an LLM.
3. Runtime operation bindings are explicit, static, inspectable, and limited
   to the selected reference scope. No dynamic imports, arbitrary code nodes,
   plugin discovery, or untrusted code execution is allowed.
4. Branching reuses a shared upstream result exactly as selected inside one
   run. It cannot silently duplicate work or make result ownership ambiguous.
5. Every reuse/cache decision is visible and safe. A changed workflow,
   parameter, input, or relevant environment condition cannot silently return
   a stale result.
6. A run record distinguishes identity, attempt, outcome, diagnostics, and
   owned artifact references. It contains enough provenance for the selected
   reproduction claim without promising Phase 6 comparison UX.
7. Artifact/persistence policy is local, minimal, owned, inspectable,
   removable, and explicit about partial failure. It cannot grow into a
   database, general storage system, or hidden durable state by convenience.
8. Runtime errors provide a stable affected operation/run, category,
   plain-English explanation/remedy, and retained technical detail. A raw
   exception alone is not an acceptable result.
9. The reference proof performs selected real deterministic computation; it
   cannot merely return fabricated or prewritten outcomes. It must not claim
   user-data, data-preparation, model-training, evaluation, UI, or export
   capability owned by later phases.
10. The visual-interaction amendment is a Phase 3+ presentation direction.
    It does not change Phase 1 semantics or require a speculative UI cache,
    region state, browser interface, or visual implementation in Phase 2.
11. The report is an architecture decision, not legal advice. Any prospective
    external library must receive current maintenance, license, compatibility,
    package-boundary, and lock-graph evidence in a later approved dependency
    packet before selection or installation.

## 7. Required Decision Analysis

Apply every gate before recommending a candidate. A candidate that fails a
gate is ineligible regardless of score.

| Gate | Required result |
|---|---|
| G1 — Canonical-input fidelity | Only validated canonical workflow semantics determine planning/execution. |
| G2 — Deterministic plan | Ordering, branches, and result identity are independent of layout and insertion order. |
| G3 — Explicit runtime boundary | Runtime bindings are static and inspectable; no dynamic/untrusted code path exists. |
| G4 — Provenance and ownership | Run, artifact, cache, and cleanup ownership are explicit and auditable. |
| G5 — Failure safety | Invalid graphs and runtime failure stop predictably with actionable structured information. |
| G6 — Cache correctness | Reuse is absent or has testable semantic keys, invalidation, and visibility. |
| G7 — Local proportionality | The choice fits supported local Windows execution without a premature service, database, or distributed system. |
| G8 — Phase boundary | The choice does not add UI, user data, ML modeling, comparison, export, or later-phase behavior. |
| G9 — Dependency posture | No external implementation is assumed selectable without a later direct-dependency decision. |

For every D2 decision, compare at least two credible choices using this common
matrix. Scores use 1–5 with a rationale and evidence-confidence label; they
are an aid to reasoning rather than an automatic decision.

| Criterion | Weight |
|---|---:|
| Overview and spine alignment | 20 |
| Determinism and semantic fidelity | 18 |
| Reproducibility, provenance, and inspectability | 17 |
| Failure and cache safety | 15 |
| Local simplicity and containment | 12 |
| Testability and supported-environment fit | 10 |
| Bounded scope and dependency posture | 8 |
| **Total** | **100** |

Weighted points are `weight × score / 5`. The report must show reproducible
totals, gate outcomes, evidence confidence, and an explanation if the
recommendation differs from the numerical leader.

### D2.1 — Execution isolation and local lifecycle

Compare at minimum a direct in-process execution module, a supervised bounded
local child-process model, and a persistent local service/worker model.
Recommend lifecycle ownership, startup/termination, cancellation boundary,
failure containment, and the future caller seam. Reject any approach that
needs a UI, network service, or broader process architecture without evidence.

### D2.2 — Intermediate representation and runtime binding

Compare direct interpretation of the document, a separate immutable
layout-independent execution representation, and generated-source execution.
Specify whether the selected plan carries operation identity, resolved
parameters, dependency references, and validation snapshot/reference; how it
relates to Phase 1 contract declarations; and how explicit runtime bindings
are registered without changing canonical workflow meaning.

### D2.3 — Deterministic planning, shared upstream work, and failure flow

Compare at minimum stable topological scheduling, insertion-order traversal,
and any credible declarative/dependency-plan alternative. Specify deterministic
tie-breaking, branch/join behavior, exactly-once within-run reuse, invalid
graph refusal, first/aggregate failure policy, cancellation limit, and result
ownership. Do not implement a planner.

### D2.4 — Run identity, provenance, and reproducibility record

Compare an ephemeral result-only approach, an immutable minimal run record,
and an experiment-history model. Specify the selected run ID, workflow/content
reference, operation/parameter inputs, seed/environment metadata, timing
policy, outcome, diagnostic, and artifact-reference fields. Keep comparison,
restoration, and user-visible history in Phase 6.

### D2.5 — Artifact ownership, local persistence, and cleanup

Compare no durable artifact storage, bounded owned local files, and a database
or general artifact-store approach. Specify selected ownership, path/format
concept, write/commit boundary, retention/removal, partial failure, and how a
later phase can consume references without treating them as success evidence.
Do not create directories, files, a database, or an artifact format.

### D2.6 — Cache keys, invalidation, and visibility

Compare no cross-run reuse, selected within-run memoization, and persisted
cross-run caching. Specify the selected cache scope; semantic key inputs;
invalidators; hit/miss representation; relationship to owned artifacts; and
tests that prove stale output cannot be returned. A no-reuse policy remains a
valid selection.

### D2.7 — Runtime error envelope and diagnostics bridge

Compare raw exceptions, a new structured run-error envelope, and direct reuse
of Phase 1 diagnostics without runtime context. Specify stable category/code,
affected run/operation, user-oriented explanation/remedy, technical detail,
cause-chain handling, and how pre-execution validation diagnostics remain
distinct from execution failures.

### D2.8 — Reference operation and acceptance-workflow boundary

Compare a mocked/prewritten-result proof, a small actual deterministic
reference operation family over synthetic controlled values, and a real
user-data/model workflow. Select the smallest actual operation family and
controlled inputs that exercise plan order, branch reuse, result/artifact
handling, repeatability, cache choice, and failure. Specify the evidence
needed before any fixture/dependency is proposed. Do not create or select the
fixture, operation, dependency, or artifact in this packet.

## 8. Research and Evidence Rules

1. Check changeable facts at execution time. Cite primary sources with
   retrieval dates.
2. Separate source facts from architectural inferences.
3. Do not install, download, clone, run, or benchmark a candidate library or
   platform implementation. Documentary research is sufficient here.
4. Do not use a blog, AI output, or secondary comparison as the sole support
   for a technical claim where a primary source exists.
5. Treat standards/docs as evidence about defined behavior, not proof a
   particular implementation will satisfy ViDAP's selected design.
6. Record uncertainty and its owner. A material question that needs a
   prototype becomes a separately proposed, unexecuted spike using Section
   11's template.
7. Do not copy large text from any source. Summarize and use brief quotations
   only where exact language matters.

## 9. Exact Authorized Output

The worker may create or modify only:

`ViDAP_P2_EP01_Decision_Report.md`

The report must contain:

1. Packet metadata; authorization; governing-input versions; and a sanitized
   repository baseline.
2. A current primary-source bibliography with retrieval dates.
3. Gates G1–G9 and weighted comparison evidence for every D2 decision.
4. A clear recommended D2.1–D2.8 decision set, rejected alternatives,
   confidence, limitations, and downstream consequences.
5. One cross-decision ownership map covering canonical workflow input,
   execution representation/plan, runtime binding/dispatch, run record,
   artifacts, cache, diagnostics, UI, experiment/state, and export.
6. A precise narrative of the proposed valid, branched, repeated, stale-cache,
   invalid, and runtime-failure evidence cases. It is not a fixture, source,
   executable sample, or selected operation.
7. Explicit Phase 3+ deferrals, including visual regions/boundaries, data,
   models, experiment comparison, export, AutoML, agents, and UI/API behavior.
8. Blocking/non-blocking findings and any separately proposed feasibility
   spike using Section 11's template.
9. Worker self-assessment against Section 12 plus final command, lock, and
   exact-scope evidence.

No other tracked repository path may be added, modified, moved, staged,
committed, or deleted. The report must not contain absolute user paths,
credentials, raw environment values, copied lockfiles, or full command logs.

## 10. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read every governing input and record its version; preserve all pre-existing
   work.
2. Record baseline branch, commit, worktree state, output-path collision check,
   and lock hashes.
3. Gather current primary evidence, apply G1–G9, and compare every D2 choice
   using the Section 7 matrix. Record facts, inferences, confidence, rejected
   alternatives, and unresolved questions.
4. Draft only the decision report. Keep proposed records, operations, and
   evidence cases non-authoritative and non-executable.
5. Re-read the report against Sections 4, 6–9, and 12.
6. Run, in order, `npm.cmd run check`, `npm.cmd run coverage`,
   `npm.cmd run deps:inventory`, `npm.cmd run license:check`,
   `npm.cmd run deps:audit`, and `git diff --check`. If an authorized report
   issue caused a failure, repair only that report and rerun the full sequence;
   otherwise stop with a named blocker.
7. Confirm both lock hashes are unchanged; inspect generated ignored state,
   final Git status, and exact changed/untracked path set. The report must be
   the only worker repository artifact.
8. Record final self-assessment and stop for independent validation. Do not
   self-validate, stage, commit, push, or begin P2-EP02.

## 11. Feasibility-Spike Proposal Template

If documentary evidence cannot settle a material D2 decision, the report may
propose—but may not execute—a separate spike containing:

- one precise question and why it affects the decision;
- sources checked and remaining uncertainty;
- hypothesis and bounded actions;
- exact files, commands, dependencies, processes, or artifact paths requested;
- time/effort limit, success/failure signals, cleanup, and lock/scope proof;
- license/security/data implications; and
- the effect of each outcome on D2 and the next packet.

The worker returns `Blocked` when the unresolved question prevents a
responsible recommendation.

## 12. Acceptance Criteria

P2-EP01 may be accepted only when:

- **EP01-AC01:** Authority, Phase 1 prerequisite, governing versions,
  baseline, and pre-existing work are accurately recorded without sensitive or
  user-specific information.
- **EP01-AC02:** D2.1–D2.8 each have a recommended decision, alternatives,
  evidence confidence, limitations, and downstream consequences.
- **EP01-AC03:** Gates G1–G9 are applied consistently before scoring.
- **EP01-AC04:** Every D2 comparison uses the full weighted criteria with
  reproducible totals and stated rationale.
- **EP01-AC05:** Current/changeable claims use primary sources with retrieval
  dates, and the report labels inference separately from source facts.
- **EP01-AC06:** D2.1–D2.3 preserve validated canonical input, an explicit
  layout-independent runtime boundary, deterministic dependency planning,
  predictable branch/failure behavior, and no dynamic/untrusted code.
- **EP01-AC07:** D2.4–D2.5 define bounded inspectable run provenance and
  artifact ownership/cleanup without a comparison product, database, or
  unowned persistent state.
- **EP01-AC08:** D2.6 makes cache reuse absent or visibly safe, with semantic
  keys, invalidation, and stale-result proof requirements.
- **EP01-AC09:** D2.7 distinguishes pre-execution validation from runtime
  failure and requires stable actionable/technical error information.
- **EP01-AC10:** D2.8 requires a real, minimal deterministic reference proof
  without selecting data, models, fixtures, dependencies, UI, or later-phase
  behavior prematurely.
- **EP01-AC11:** The cross-decision ownership map keeps workflow/schema,
  execution, experiment/state, UI, and export responsibilities separate and
  preserves the visual-interaction amendment as future presentation work.
- **EP01-AC12:** Dependencies, locks, source, tests, fixtures, configuration,
  CI, processes, artifact files, persistence, UI/API, data/ML, export, remote
  state, and product behavior remain unchanged.
- **EP01-AC13:** The decision report is the worker's only repository change.
- **EP01-AC14:** Complete final attestation passes after report completion;
  locks remain unchanged; `git diff --check` passes; and scope evidence
  distinguishes worker output from pre-existing work.
- **EP01-AC15:** A fresh independent validator finds the analysis
  reproducible, internally consistent, and aligned with the overview, spine,
  roadmap, Phase 2 plan, Phase 1 reconciliation, and UX boundary.
- **EP01-AC16:** Central explicitly accepts D2.1–D2.8 before this packet is
  marked complete or a P2 implementation packet is drafted.

## 13. Independent Validation Contract

The validator must use a fresh chat and must:

1. Read every governing input, this packet, and the worker decision report.
2. Recheck high-impact primary sources and current claims that could materially
   change a recommendation.
3. Recalculate every comparison total; apply G1–G9 independently; challenge
   rejected alternatives, confidence, deferrals, and decision consistency.
4. Verify no decision silently selects a dependency, fixture, data/model
   policy, runtime implementation, artifact store, UI/API, or Phase 3+ work.
5. Independently run the full Section 10 attestation, recheck locks, exact
   scope, generated-state/hygiene evidence, and report sanitization. It may
   create only ignored state needed by those commands; it may not edit tracked
   files or repair a finding.
6. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and
   a Central-reconciliation recommendation.

The validator may not edit files, accept D2 decisions for Central, alter remote
state, create a reconciliation record, or begin P2-EP02.

## 14. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P2_EP01.md` version 0.1 as the bounded execution-and-run-foundation decision worker. Read every governing input, especially the accepted Phase 1 reconciliation, the approved Phase 2 plan, and the UX boundary. Create or modify only `ViDAP_P2_EP01_Decision_Report.md`. Research only current primary sources and recommend D2.1–D2.8 through the packet's gates and weighted comparisons. Preserve validated canonical workflow input, deterministic planning, explicit runtime bindings, run/artifact/cache ownership, actionable runtime errors, and a minimal real reference-proof boundary. Do not select/install dependencies, create fixtures, source, tests, artifact files, processes, UI/API, persistence, data/ML, export, or Phase 3+ work. Run the complete Section 10 final attestation; if an authorized report issue caused a failure, repair only that report and rerun the full sequence. Stop with the report and independent-validation handoff; do not self-validate, accept for Central, stage/commit/push, alter remote state, or begin P2-EP02.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P2_EP01.md` version 0.1. Read every governing input and `ViDAP_P2_EP01_Decision_Report.md`. Follow Section 13 exactly. Recheck current primary sources, recalculate every weighted total, apply G1–G9 independently, and challenge all D2.1–D2.8 recommendations, alternatives, confidence, deferrals, dependency posture, provenance/artifact/cache claims, runtime-error boundary, and UX scope boundary. Reproduce the complete Section 10 attestation with unchanged locks and exact-scope/hygiene evidence. Do not edit files, accept D2 decisions for Central, alter remote state, create a reconciliation record, or begin P2-EP02. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and a Central-reconciliation recommendation.

## 15. Next Action

P2-EP01 is complete. Its independent `Accept` and Central acceptance of
D2.1–D2.8 are recorded in `ViDAP_P2_EP01_Validation_and_Reconciliation.md`.
Central may now draft P2-EP02 — execution representation and contract bridge.
That packet requires separate approval before execution.
