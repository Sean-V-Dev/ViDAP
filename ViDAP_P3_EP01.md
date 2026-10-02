# ViDAP P3-EP01 — Vertical-Slice and Integration Decisions

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Research and decision; documentation-only repository change |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3/checkpoint A3 |
| Prerequisite | Phase 2 complete through P2-EP06 reconciliation |
| Workstream | WS3.1 — Slice and integration decisions |
| Decisions covered | D3.1 through D3.4 |
| Authorized worker output | `ViDAP_P3_EP01_Decision_Report.md` |
| Central reconciliation | `ViDAP_P3_EP01_Validation_and_Reconciliation.md` (Central only) |
| Created | 2026-10-01 |
| Approved | 2026-10-01 by explicit user direction |
| Completed | 2026-10-01 by explicit Central acceptance |
| Owner | Central |

---

## 1. Authorization Boundary

The user explicitly approved this exact version on 2026-10-01. One bounded
worker may inspect the repository and research current
primary sources, then create only the decision report named above. Approval
does not authorize source or tests, operations, fixtures, data, dependencies,
locks, prototypes, local services, endpoints, persistence, UI work, schema
changes, remote changes, or P3-EP02 work.

The worker recommends decisions. A fresh independent validator checks the
report. Only Central may accept D3.1 through D3.4.

## 2. Plain-English Packet Intent

### What this packet does

It settles four questions before anyone writes Phase 3 code: what the one
small real workflow will be and which operations it needs; how the browser
talks to the engine without becoming the engine; where a saved workflow
lives; and where visual workspace details such as regions and expanded nodes
are stored.

### Why this comes before implementation

Each of these choices is easy to make by accident in code. A convenient
endpoint can turn into a general API, a CSV loader can quietly set Phase 4's
data policy, a model node can set Phase 5's model policy, and a region width
stored in the wrong place can change what a workflow means or break the
strict Phase 1 reader.

### What it enables

Accepted D3.1–D3.4 give the design packet (P3-EP02), the backend slice
(P3-EP03), and the editor (P3-EP04) fixed, testable boundaries. They create
no operation, endpoint, file, or screen.

### How success is demonstrated

The sole decision report compares credible alternatives against explicit
gates and weighted criteria, cites current primary sources, recommends a
bounded D3.1–D3.4 set, names exactly which Phase 4/5 policies stay open, and
leaves the repository free of implementation.

## 3. Governing Inputs and Authority

The worker and validator must read these in order:

1. The explicit user approval of this exact packet version.
2. `ViDAP_Overview.txt`, especially OV §§2–7, 16, 18–22A, 25, and 30–31.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 1–18, Phase 3,
   Phases 4–5 boundaries, and the deferred-decision register.
4. `ViDAP_Roadmap.md` v4.6, especially P3, checkpoint A3, and P4/P5 decisions.
5. `ViDAP_Phase_3_Plan.md` v1.1, especially Sections 3–5, 7–11, and
   D3.1–D3.4.
6. `ViDAP_P2_EP06_Validation_and_Reconciliation.md` and the accepted D2.1–D2.8
   in `ViDAP_P2_EP01_Decision_Report.md` and its reconciliation, with
   particular attention to D2.1 (in-process seam), D2.4–D2.5 (run record and
   owned artifacts), D2.7 (error envelope), and D2.8 (reference boundary).
7. `ViDAP_P1_EP06_Validation_and_Reconciliation.md` and accepted D1.1–D1.7,
   especially D1.2 (semantic/layout separation), D1.3 (nominal types), D1.4
   (parameters), D1.5 (diagnostics), and D1.6 (versioning and migration).
8. Current source: `python/src/vidap_workflow/` (document, layout metadata,
   strict reader), `python/src/vidap_execution/` (seam, run, artifacts,
   reference), the loopback FastAPI shell and process harness, `apps/web/`,
   `package.json`, `python/pyproject.toml`, both locks, dependency-control
   documentation, decision records 0001–0004, `.gitignore`, `README.md`, and
   `CONTRIBUTING.md`.
9. `UX refinement.txt`, by explicit user direction on 2026-10-01, is the basis
   for these decisions. Each recommendation cites the UX sections it serves
   and records any deviation with a rationale. Its phase-status statements
   are not authoritative, and it does not move Phase 4+ behavior into this
   packet.
10. This packet.

Higher-authority artifacts prevail. None of these inputs authorize
implementation beyond this packet.

## 4. Objective and Completion Condition

### Objective

Produce evidence-backed recommendations for:

- **D3.1:** the vertical-slice workflow and minimal operation set;
- **D3.2:** the UI/runtime integration contract;
- **D3.3:** workflow save/load ownership and location; and
- **D3.4:** presentation-state ownership and schema impact.

### Completion condition

P3-EP01 is complete only when:

1. The authorized decision report exists and passes the worker's required
   self-check and final attestation.
2. A fresh independent validator returns `Accept`.
3. No material uncertainty, policy conflict, license issue, schema change, or
   later-phase policy is hidden inside a recommendation.
4. Central separately accepts, rejects, or returns each D3 decision for
   revision in a reconciliation record.

## 5. Preconditions and Stop Gates

Before writing the report, the worker must confirm and record:

1. This exact packet version has explicit approval.
2. The Phase 3 plan v1.1 is approved and Phase 2 is complete.
3. Branch, `HEAD`, sanitized remote identity, staged/unstaged/untracked
   state, and owners of pre-existing paths.
4. No file collides with the Section 9 output path.
5. Both lock hashes.
6. How the final attestation will run: directly in Windows PowerShell, or,
   if the worker's shell cannot run the Windows commands, through the
   `CONTRIBUTING.md` workaround (user-executed Windows run).

Stop with a `Blocked` report if a responsible recommendation would require an
unapproved prototype, a choice that cannot preserve a Phase 1/2 or spine
invariant, a Phase 4/5 policy decision, or evidence that primary sources
cannot supply.

## 6. Non-Negotiable Decision Constraints

Every recommendation must preserve all of the following:

1. The canonical `vidap.workflow` document remains the single source of
   workflow meaning. The UI edits it; it never becomes a second graph.
2. Only a workflow that passes Phase 1 validation is planned or run. The
   backend's verdict is authoritative; UI checks are early feedback only.
3. The browser does not execute workflow semantics, recompute results, or hold
   a private copy of contracts, parameters, defaults, or ranges.
4. Execution reuses the accepted D2.1 in-process seam, D2.2 static bindings,
   D2.3 planning, D2.4 run record, D2.5 owned artifacts, D2.6 attempt-local
   reuse, and D2.7 errors. Any narrow change to one of them must be named,
   justified by a demonstrated slice need, and kept out of the recommendation
   until Central accepts it.
5. Layout and presentation state never alter semantic digest, plan, or result.
6. Slice operations call established libraries (invariant 1), stay minimal,
   and leave data-format, type-inference, profiling, preparation, model-family,
   split, metric, and interpretation policy explicitly open for Phases 4–5.
7. Any runtime channel is loopback-only, bounded, input-validated, and adds
   no authentication, hosting, public exposure, job service, or general API.
8. No dynamic code loading, plugin discovery, or LLM-generated execution.
9. Any prospective library is a candidate only. Its selection and
   installation require a later approved packet with D0.6 maintenance,
   license, vulnerability, and lock evidence. Any fixture is a proposal only,
   governed by D0.7.
10. Recommendations follow `UX refinement.txt`: responsibility-level and
    composite nodes rather than one node per library call; no
    implementation-named model node types; regions and boundary interfaces as
    presentation over canonical dependencies; and the canonical workflow as
    the shared source of truth for humans and future agents.
11. The report is an architecture decision, not legal advice.

## 7. Required Decision Analysis

Apply every gate before scoring. A candidate that fails a gate is ineligible.

| Gate | Required result |
|---|---|
| G1 — Canonical fidelity | The saved, displayed, and executed workflow are the same canonical document. |
| G2 — Backend authority | Validation, execution, and results come from the backend; the UI only edits and presents. |
| G3 — Phase 2 continuity | Accepted D2 behavior is reused or any narrow change is explicitly named and justified. |
| G4 — Presentation isolation | Presentation state cannot change semantic digest, plan, or result. |
| G5 — Real computation | Slice operations run established library code on real bytes; no canned results. |
| G6 — Phase boundary | No Phase 4/5 policy, broad node catalog, experiment UX, export, or agent capability is settled. |
| G7 — Local proportionality | Loopback-only, synchronous-seam-compatible, no service, database, auth, or hosting. |
| G8 — Dependency and fixture posture | Libraries and fixtures are candidates with evidence, not selections. |
| G9 — Windows support and testability | Fits the supported Windows environment and existing quality tasks. |
| G10 — UX basis | Follows `UX refinement.txt` or records a justified deviation; does not foreclose its later-phase direction. |

For every D3 decision, compare at least the options listed below using this
matrix. Scores use 1–5 with a rationale and evidence-confidence label; they
aid reasoning and do not decide automatically.

| Criterion | Weight |
|---|---:|
| Overview, spine, and Phase 3 plan alignment | 20 |
| Canonical fidelity and backend authority | 18 |
| Phase-boundary discipline (no Phase 4+ policy) | 15 |
| User value for the visual slice | 14 |
| Failure, error, and data safety | 12 |
| Local simplicity and testability on Windows | 13 |
| Dependency and maintenance posture | 8 |
| **Total** | **100** |

Weighted points are `weight × score / 5`. Show reproducible totals, gate
outcomes, confidence, and an explanation if a recommendation differs from
the numerical leader.

### D3.1 — Vertical-slice workflow and minimal operation set

Compare at minimum: (A) a tiny controlled synthetic CSV, a load step, target
and feature selection, a split, one established baseline estimator, and one
metric through a mature library; (B) a standard-library-only path with a
hand-written baseline; and (C) extending only the existing scalar reference
family without CSV. Specify the workflow shape and operations, candidate
libraries, how the CSV enters (a controlled fixture selected by identity
versus a user-chosen file) and what that leaves open for Phase 4, the nominal
types used at each port, and the result representation and its fit with
D2.4/D2.5 owned output.

The recommended slice must include: multiple regions, a cross-region
dependency that skips a neighboring region, one output consumed by more than
one later node (shared branch), a UI-settable parameter whose change
measurably changes the recorded result, and one representative actionable
failure (for example, OV §19's unencoded-categorical case). Name every
Phase 4/5 policy the slice deliberately does not decide.

Visible nodes must be responsibility-level (UX §§1, 8): for example Data,
Prepare, Split, Model, Evaluate, with routine library steps inside a
composite node that remains real and inspectable, not one node per library
call. The model step must be a model responsibility with one fixed
implementation, not an implementation-named node type, so Phase 5's generic
Model node and implementation selection (UX §§11–13) stay open. State the
proposed regions and which UX §2 candidates the slice uses.

### D3.2 — UI/runtime integration contract

Compare at minimum: (A) narrow loopback HTTP JSON endpoints in the existing
FastAPI shell calling the in-process seam synchronously; (B) the same with a
bounded background attempt and status polling; (C) a file- or command-based
exchange; and (D) browser-side execution (expected to fail G2, recorded for
completeness). Specify the minimum operations (publish contracts, validate,
run, read status/result/error), request and response bounds, how Phase 1
diagnostics and D2.7 errors map to responses, loopback and origin/Host
protections appropriate to a local tool, behavior when a run is slow or
fails, and the tests that prove the UI cannot obtain a result the backend did
not record. Do not design endpoints beyond the slice.

### D3.3 — Workflow save/load ownership and location

Compare at minimum: (A) backend-written files in an owned local workspace
location; (B) browser download/upload or file-system-access APIs; and (C) a
hybrid. Specify who writes, where, naming, overwrite and conflict behavior,
how load reuses the Phase 1 reader and validation rather than a UI parser,
how an invalid or future-version file is refused, ignore/ownership rules for
any local path, and how the saved bytes are proven identical to what the
runtime reads. Because the file is shared with other tools and future agents
(UX §18), specify how the editor detects a change made outside it, shows
what changed, and avoids silently overwriting it.

### D3.4 — Presentation-state ownership and schema impact

Compare at minimum: (A) derivation from contract metadata plus local UI
state; (B) a separate versioned presentation sidecar file; and (C) a
D1.6-governed `vidap.workflow` schema revision extending layout metadata.
Cover region membership, region widths/gutters, boundary-interface
presentation, node expansion, and viewport. State what persists across
save/reload, what is per-session only, how missing or stale presentation
state degrades safely, and the digest-invariance tests. If (C) or any Phase 1
change is recommended, record the demonstrated incompatibility with the
current strict reader and keep the change narrow; the change itself requires
a later approved packet.

## 8. Research and Evidence Rules

1. Check changeable facts (library versions, maintenance, licenses, security
   guidance, browser API support) at execution time; cite primary sources
   with retrieval dates.
2. Separate source facts from architectural inference.
3. Do not install, download, clone, run, or benchmark a candidate library.
   Documentary research is sufficient here.
4. Do not rely on blogs, AI output, or secondary comparisons where a primary
   source exists.
5. Record uncertainty and its owner. A question that needs a prototype
   becomes a proposed, unexecuted spike using Section 11.
6. Quote sparingly; summarize instead of copying.

## 9. Exact Authorized Output

The worker may create or modify only:

`ViDAP_P3_EP01_Decision_Report.md`

The report must contain:

1. Packet metadata, approval, governing-input versions, and a sanitized
   baseline with pre-existing path ownership.
2. A primary-source bibliography with retrieval dates.
3. Gates G1–G10 and weighted comparisons for every D3 decision.
4. A recommended D3.1–D3.4 set with rejected alternatives, confidence,
   limitations, and downstream consequences for P3-EP02 through P3-EP05,
   each traced to the `UX refinement.txt` sections it serves, with any
   deviation and its rationale.
5. A slice narrative (non-executable): the proposed workflow, its regions,
   the skip-region dependency, the shared branch, the UI-parameter effect,
   and the failure case.
6. An explicit list of Phase 4/5 policies left open, and any narrow Phase 1/2
   change proposed for later approval.
7. Candidate dependency and fixture proposals with the evidence a later
   dependency/fixture step must collect.
8. Blocking and non-blocking findings and any proposed spike.
9. Worker self-assessment against Section 12, final command outcomes, lock
   hashes, and exact-scope evidence.

No other repository path may be added, modified, moved, staged, committed, or
deleted. The report must not contain absolute user paths, credentials, raw
environment values, copied lockfiles, or full command logs.

## 10. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read every governing input and record its version; preserve all
   pre-existing work.
2. Record the Section 5 baseline.
3. Gather current primary evidence, apply G1–G10, and compare every D3 option
   with the Section 7 matrix.
4. Draft only the decision report; keep proposals non-executable.
5. Re-read the report against Sections 4, 6–9, and 12.
6. Run, in order: `npm.cmd run check`, `npm.cmd run coverage`,
   `npm.cmd run deps:inventory`, `npm.cmd run license:check`,
   `npm.cmd run deps:audit`, and `git diff --check`. A worker whose shell
   cannot run these follows `CONTRIBUTING.md` ("When your shell cannot run
   the Windows commands"): give the user this exact ordered list, record the
   pasted output as a user-executed Windows run, and claim only what it shows.
   `git diff --check` does not cover the untracked report, so also inspect
   the report directly for trailing whitespace, final newline, user paths,
   and sensitive content. If an authorized report issue causes a failure,
   repair only the report and rerun the full sequence; otherwise stop with a
   named blocker.
7. Confirm lock hashes are unchanged and the report is the only worker
   repository change.
8. Record the self-assessment and stop for independent validation. Do not
   self-validate, stage, commit, push, or begin P3-EP02.

## 11. Feasibility-Spike Proposal Template

If documentary evidence cannot settle a material D3 decision, the report may
propose, but not execute, a spike stating: the question and why it matters;
sources checked; hypothesis and bounded actions; exact files, commands,
dependencies, processes, or paths requested; effort limit, success and
failure signals, cleanup, and lock/scope proof; license, security, and data
implications; and how each outcome changes D3 and the next packet. Return
`Blocked` if the open question prevents a responsible recommendation.

## 12. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP01-AC01 | Approval, prerequisites, governing versions, baseline, and pre-existing ownership are accurately recorded without sensitive or user-specific data. |
| EP01-AC02 | D3.1–D3.4 each have a recommendation, alternatives, confidence, limitations, and downstream consequences. |
| EP01-AC03 | Gates G1–G10 are applied before scoring; every comparison uses the full weighted matrix with reproducible totals. |
| EP01-AC04 | Changeable claims cite primary sources with retrieval dates; inference is labeled separately. |
| EP01-AC05 | D3.1 selects a real, minimal slice of responsibility-level nodes meeting every Section 7 inclusion, keeps the model step implementation-neutral in shape, names its candidate libraries and fixture without selecting them, and lists the Phase 4/5 policies left open. |
| EP01-AC06 | D3.2 keeps the backend authoritative, reuses the D2 seam and error envelope, stays loopback-only and slice-bounded, and specifies proof that the UI cannot show an unrecorded result. |
| EP01-AC07 | D3.3 makes the saved file the canonical document read by the runtime, reuses the Phase 1 reader, defines overwrite, refusal, and ownership behavior, and never silently overwrites an external change. |
| EP01-AC08 | D3.4 isolates presentation state from semantics with testable digest invariance; any Phase 1 change is a named, narrow, separately approved proposal. |
| EP01-AC09 | No source, test, fixture, dependency, lock, prototype, process, endpoint, persistence, UI, schema, CI, or remote change occurs; the report is the only worker change. |
| EP01-AC10 | The complete final attestation passes (directly or as a recorded user-executed Windows run); locks are unchanged; report hygiene is verified. |
| EP01-AC11 | A fresh independent validator finds the analysis reproducible and aligned with the overview, spine, roadmap, Phase 3 plan, and accepted Phase 1/2 decisions, and returns `Accept`. |
| EP01-AC12 | Central explicitly accepts D3.1–D3.4 before this packet is complete or P3-EP03 is drafted. |

## 13. Independent Validation Contract

A fresh validator must read every governing input, this packet, and the
report; recheck high-impact primary sources; recalculate every total and
apply G1–G10 independently; challenge each recommendation for hidden Phase 4/5
policy, UI authority, schema change, dependency selection, service growth,
or unjustified departure from `UX refinement.txt`;
reproduce the Section 10 attestation (directly or through the
`CONTRIBUTING.md` workaround); verify locks, scope, and report hygiene; and
return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and a
Central recommendation. The validator may not edit files, accept for Central,
write the reconciliation, alter remote state, or begin P3-EP02.

## 14. Fresh-Chat Handoff Prompts

### Execution worker

> Execute approved `ViDAP_P3_EP01.md` v0.1 as the bounded vertical-slice and integration decision worker. Read every governing input, especially the approved Phase 3 plan, the Phase 2 reconciliation and accepted D2/D1 decisions, and current source. Create or modify only `ViDAP_P3_EP01_Decision_Report.md`. Using current primary sources, the Section 7 gates and weighted matrix, recommend D3.1–D3.4: the minimal real CSV-to-baseline slice, the UI/runtime contract, save/load ownership, and presentation-state ownership. Keep the backend authoritative and leave Phase 4/5 policy open. Do not select or install dependencies, create fixtures, source, tests, prototypes, endpoints, persistence, UI, or schema changes. Run the complete Section 10 attestation, using the `CONTRIBUTING.md` Windows workaround if your shell cannot run it. Stop with the report and validation handoff; do not self-validate, accept for Central, stage/commit/push, or begin P3-EP02.

### Independent validator

> Act as the independent validator for approved `ViDAP_P3_EP01.md` v0.1. Read every governing input and `ViDAP_P3_EP01_Decision_Report.md`. Follow Section 13: recheck primary sources, recalculate totals, apply G1–G10, and challenge D3.1–D3.4 for hidden Phase 4/5 policy, UI authority, schema change, dependency selection, or service growth. Reproduce the Section 10 attestation (using the `CONTRIBUTING.md` workaround if needed) with lock, scope, and hygiene checks. Do not edit files, accept for Central, write reconciliation, or begin P3-EP02. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and a Central recommendation.

## 15. Next Action

P3-EP01 is complete. The independent `Accept` and Central acceptance of
D3.1–D3.4, with F1 and F6 accepted as narrow Phase 2 extensions and F2 kept
as a P3-EP03 gate, are recorded in
`ViDAP_P3_EP01_Validation_and_Reconciliation.md`. P3-EP02 is ready to draft.
