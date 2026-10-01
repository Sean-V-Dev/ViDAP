# ViDAP Phase 3 Plan — First Visual End-to-End Slice

| Field | Value |
|---|---|
| Status | Draft; awaiting explicit user approval |
| Version | 0.1 |
| Parent | `ViDAP_Roadmap.md` version 4.5 |
| Spine phase | Phase 3 — First Visual End-to-End Slice |
| Product source | `ViDAP_Overview.txt` |
| Interaction-model reference | `UX refinement.txt` (consultative; spine v1.3 holds its approved direction) |
| Prerequisite | Phase 2 complete through P2-EP06 reconciliation (2026-10-01) |
| Created | 2026-10-01 |
| Owner | Central |

---

## 1. Authorization and Boundary

This draft is not approved and authorizes nothing. Once approved, it still is
not an execution packet: it does not authorize source changes, dependencies,
UI, API, persistence, or a Phase 3 worker. Each bounded packet requires its own
explicit Central approval.

Phase 3 proves that a person can build and run one narrow, real workflow
through a visual interface, and that the picture on screen is the same
canonical workflow the engine runs. It may not redefine Phase 1 workflow
meaning, reopen Phase 2 execution semantics without a demonstrated
incompatibility, make the browser the runtime, or take ownership of the
broader data, modeling, experiment, or export policies held by Phases 4–7.

## 2. Plain-English Phase Intent

### What we will build or change

The first real ViDAP screen: a graph editor where a user places a few nodes,
connects them, sets their options, saves and reloads the workflow, presses
run, and sees the result or an understandable error. The canvas uses the
approved interaction direction: left-to-right regions for major
responsibilities (such as Data, Prepare, Model, Evaluate), resizable gutters
between them, named boundary inputs and outputs instead of long wires across
the screen, compact nodes that expand in place, and on-demand tracing of
where a value came from and where it goes.

### Why the system needs it

Phases 1 and 2 built a workflow format and an engine that are only usable
from code. The product promise is visual, and the riskiest visual idea — the
region and boundary model — is new enough that it must be tried on real
workflows before later phases pile more nodes onto it.

### What real behavior it enables

A user without code can assemble a small CSV-to-baseline-result workflow,
fix a connection or setting the editor flags, run it on the real backend,
and read the recorded outcome. The saved file is an ordinary
`vidap.workflow` document that the headless engine and other tools can read.

### How we will know it works

A fresh user completes the reference slice from an empty canvas; the saved
file runs identically headlessly; a parameter changed in the UI measurably
changes the backend computation; a representative failure tells the user
what went wrong and what to do; and an independent visual/UX review against
an approved design system and representative screen set passes.

## 3. Governing Inputs and Handoff

Every Phase 3 packet must read:

1. Current explicit user direction.
2. `ViDAP_Overview.txt`, especially OV §§2–7, 18–22A, 25, and 31.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 1–18, Phase 3,
   the deferred-decision register, and validation scaling.
4. `ViDAP_Roadmap.md` v4.5, especially P3 and checkpoint A3.
5. `UX refinement.txt` as consultative detail behind the spine's approved
   interaction direction; its phase-status statements are not authoritative.
6. `ViDAP_P1_EP06_Validation_and_Reconciliation.md`,
   `ViDAP_P2_EP06_Validation_and_Reconciliation.md`, and the accepted
   decisions D1.1–D1.7 and D2.1–D2.8.
7. `CONTRIBUTING.md`, including "When your shell cannot run the Windows
   commands", which governs how a non-Windows worker obtains the Windows
   attestation without damaging the environment.
8. This plan and later accepted Phase 3 decision records.

### Accepted inputs

Phase 2 hands forward: a strict canonical `vidap.workflow` 1.0 document with
opaque UUID identities and a static contract registry; the seven nominal
types (`table`, `target`, `split`, `model`, `predictions`, `metrics`,
`artifact`); pure validation with plain-English and technical diagnostics; an
immutable layout-independent representation and deterministic plan; a
synchronous in-process invocation seam (D2.1); immutable bounded attempt
records with provenance, outcome, and sanitized diagnostics; visible
attempt-local reuse only; and one fixed checked-integer reference family with
a single scalar proof output.

### Known gaps Phase 3 must decide, not assume

1. **No real data or model operation exists.** The only executable family is
   the scalar reference proof. The spine's CSV-to-baseline slice needs new
   operations, likely new dependencies, and fixture approvals.
2. **No UI/runtime channel exists.** The backend serves only the static
   `/api/status` foundation response; Phase 2 excluded any workflow API.
3. **Presentation state has limited room.** Workflow 1.0 layout metadata holds
   only node positions and a viewport, and the strict reader rejects unknown
   fields and `extensions`. Region membership, region widths, boundary
   presentation, and node expansion state have no accepted home.
4. **Results are scalar-only and attempt-local.** A baseline result needs a
   bounded result representation the UI can display from recorded output.
5. **Browser end-to-end testing and JSX accessibility linting are deferred**
   (Phase 0; decision record 0001).

## 4. Required Outcome and Explicit Exclusions

### Required outcome

A local visual editor that loads node contracts from the backend; lets a user
place, connect, configure, validate, save, reload, and run the approved
narrow workflow; renders semantic regions, resizable gutters, traceable
boundary interfaces, and compact/expanded nodes; shows run status, a recorded
result, and actionable errors; and follows an approved concise design system.

### Explicit exclusions

Phase 3 does not deliver:

- broad node coverage, a general node catalog, or the generic
  Model-node/implementation-selection system (Phase 5);
- general data intake, profiling, type inference, preparation policy, user
  dataset management, or data previews beyond what the slice needs (Phase 4);
- model selection, tuning, evaluation policy, or interpretation wording
  beyond the slice's single baseline result (Phase 5);
- experiment history, branching comparison, restoration, or lineage UX
  (Phase 6);
- notebook/Python export (Phase 7);
- AutoML, agent control, plugins, arbitrary code nodes, hosted or
  multi-user operation, authentication, or a desktop wrapper;
- persistent cross-run caching, background job queues, or parallel execution
  beyond the accepted D2.1 seam unless a Phase 3 decision justifies a narrow
  change with measured need; or
- a silent change to `vidap.workflow` 1.0 semantics. Any schema change follows
  the accepted D1.6 versioning policy as an explicit, approved decision.

## 5. Phase 3 Decisions

No implementation packet may assume a decision below until its decision record
is independently validated and accepted by Central.

### D3.1 — Vertical-slice workflow and minimal operation set

Select the smallest real CSV-to-baseline-result workflow and the operations it
needs (for example: load a bounded CSV, select target/features, split, fit one
baseline estimator, compute one metric). Decide the library, dependency, and
fixture choices under D0.6/D0.7, and the result shape. It must exercise a
shared branch, a cross-region dependency that skips a neighboring region, a
UI-set parameter that measurably changes the backend result, and one
actionable failure. It must state explicitly which Phase 4/5 policies remain
open and must not quietly settle them.

### D3.2 — UI/runtime integration contract

Define how the browser obtains contracts, submits a workflow for validation,
requests a run, and reads status, results, and errors, without computing
execution semantics or recalculating results. Compare proportionate options
(for example: narrow local HTTP endpoints over the existing loopback FastAPI
shell, versus file-based exchange) against D2.1's synchronous seam,
loopback-only exposure, input bounds, error mapping, testability, and Windows
support. Decide how long-running or failed runs are reported within the
accepted lifecycle limits.

### D3.3 — Workflow save/load ownership and location

Decide where a saved workflow lives, who writes it, overwrite and conflict
behavior, and how load reuses Phase 1 deserialization and validation rather
than a UI parser. A saved file must be the same canonical document the
runtime reads.

### D3.4 — Presentation-state ownership and schema impact

Decide where region membership, region widths/gutters, boundary-interface
presentation, node expansion, and similar workspace state live. Compare at
least: derivation from contract metadata plus local UI state; a separate
versioned presentation sidecar; and a D1.6-governed workflow schema revision.
Presentation state may never alter semantic digest, plan, or results. If a
Phase 1 change is chosen, record the demonstrated incompatibility and keep the
change narrow.

### D3.5 — Semantic regions and boundary interfaces

Select the initial region taxonomy for the slice; vertical regions with
left-to-right progression; gutter resize behavior; how a cross-region
dependency renders as a named output and input rather than a persistent long
wire; how the gutter visibly breaks the wire; and the on-demand trace/X-ray
behavior that reveals producers and consumers. Regions are responsibility
zones, not required stages; skipping a region must remain valid.

### D3.6 — Node interaction and local connection behavior

Define compact, expanded, and optional focus states; bounded expansion with
internal scrolling that never pans or zooms the canvas; contract-driven
parameter controls with one canonical contract source; typed port and
connection feedback derived from workflow types and backend validation; and
explicit local layout assistance (align, tidy) instead of continuous
automatic repositioning. Users own spatial arrangement.

### D3.7 — Run controls, result, and error presentation

Define run controls and statuses, how the recorded result is shown, and how
Phase 1 validation diagnostics and Phase 2 runtime errors appear on the
affected node with plain-English explanation, remedy, and expandable
technical detail. Displayed values must come from recorded execution output.

### D3.8 — Visual design system and design/UX support mechanism

Approve a concise design system or equivalent (tokens for type, color,
spacing, and states; node, port, region, gutter, and boundary components;
density rules; light/dark expectations if any) and the maintained mechanism
that keeps it current (for example, a component library, a tokens file, or a
documented reference page). Compare options under dependency/license controls.
Substantial UI packets may not start until this is accepted.

### D3.9 — Accessibility baseline

Set the minimum keyboard operation, focus visibility, contrast, labeling, and
non-color status cues for the editor, and decide whether decision record 0001's
JSX accessibility-lint deferral now ends, since meaningful JSX will exist.

### D3.10 — Representative states and visual/UX validation method

Name the representative screen/state set (for example: empty canvas, valid
slice, invalid connection, validation errors, running, success with result,
runtime failure, trace active, expanded and focused node, narrow and wide
regions, keyboard focus). Choose a proportionate method: automated browser
tests (and any tool such as Playwright, under dependency controls),
screenshot-based state review, a fresh-user walkthrough, and an independent
visual/UX review. Include the UX amendment's prototype questions: can a user
tell where information comes from and goes without persistent long wires,
and does the region system reduce layout effort compared with an
unrestricted canvas?

## 6. Workstreams and Proposed Packet Boundaries

| Workstream | Objective | Depends on | Proposed bounded packets |
|---|---|---|---|
| WS3.1 Slice and integration decisions | Resolve D3.1–D3.4 with evidence | Phase 2 reconciliation | P3-EP01 decision packet |
| WS3.2 Design and interaction decisions | Resolve D3.5–D3.10, including the design system and a throwaway interaction prototype as evidence | WS3.1 (D3.4 at minimum) | P3-EP02 decision and design-system packet |
| WS3.3 Backend slice | Implement the approved slice operations, fixtures, and the D3.2/D3.3 channel, headlessly tested | D3.1–D3.3 | P3-EP03 |
| WS3.4 Editor core | Canvas, regions, gutters, contract-driven nodes, typed connections, validation feedback, save/load | D3.4–D3.9, WS3.3 contracts | P3-EP04 |
| WS3.5 Run, results, and trace | Run controls, status, recorded result and error presentation, boundary trace/X-ray | D3.5–D3.7, WS3.3–WS3.4 | P3-EP05 |
| WS3.6 Closeout | Reproduce Phase 3 evidence, fresh-user walkthrough, independent visual/UX review, reconciliation | WS3.1–WS3.5 | P3-EP06 |

Central may split or merge packets when a decision or dependency needs
separate evidence. The prototype in WS3.2 is design evidence only; it is not
product code and must not be promoted into the product without a packet.

## 7. Required Architecture Boundaries (Checkpoint A3)

1. Node forms derive from backend node contracts; the UI keeps no separate
   copy of parameters, defaults, or ranges.
2. Connection rules come from workflow types and Phase 1 validation; the UI
   may give early feedback but the backend verdict is authoritative.
3. Displayed results come only from recorded execution output; the UI never
   recalculates them.
4. Regions, gutters, and boundary interfaces render canonical dependencies;
   they are not a second graph, hidden global state, or execution input.
5. Layout and presentation changes cannot change semantic digest, plan,
   or results.
6. The runtime channel is local, bounded, input-validated, and loopback-only;
   it adds no authentication, hosting, or public exposure.
7. No dynamic code loading, plugin discovery, or LLM-generated execution.

## 8. Test and Validation Strategy

Every packet names its final worker-completion attestation commands and
requires a complete post-change rerun after any in-scope repair. Workers whose
shell cannot run the Windows commands follow `CONTRIBUTING.md`: they do not
run setup against the checkout from that shell, they hand the user the exact
ordered PowerShell commands, and they record the pasted output as a
user-executed Windows run.

Phase 3 adds evidence for:

- contract-to-form derivation and parameter round trip from UI to the
  backend library call (OV §18);
- typed connection acceptance and rejection matching backend validation;
- save, reload, and headless run of the same file producing the same digest
  and result;
- layout/presentation invariance of semantics and results;
- the representative failure path and error presentation;
- region, gutter, boundary, trace, and node-expansion behavior across the
  representative state set;
- accessibility baseline checks; and
- independent visual/UX review against the approved design system.

Strong validation applies to the UI/runtime contract, parameter propagation,
save/load fidelity, and presentation-state isolation. Standard validation
applies to ordinary node UI; routine to styling alone.

## 9. Phase Acceptance Criteria

Phase 3 may be recommended complete only when:

- **P3-AC01:** D3.1–D3.10 are accepted with alternatives, criteria, and
  consequences recorded.
- **P3-AC02:** A fresh user assembles, validates, saves, reloads, and runs the
  approved slice from an empty canvas using real backend operations.
- **P3-AC03:** The saved file is a canonical workflow that runs headlessly with
  the same semantic digest and result as the UI run.
- **P3-AC04:** A parameter set in the UI is verified at the backend library
  boundary and changes the recorded result as expected.
- **P3-AC05:** Invalid connections and settings are flagged with actionable
  diagnostics; a representative runtime failure shows plain-English
  explanation, remedy, and technical detail on the affected node.
- **P3-AC06:** The slice includes multiple regions, a cross-region dependency
  that skips a neighboring region, and a shared branch; cross-region
  dependencies are traceable on demand without persistent long wires.
- **P3-AC07:** Gutters resize regions without forced repositioning; nodes
  support compact and bounded expanded states with internal scrolling that
  does not move the canvas.
- **P3-AC08:** Presentation state is owned as decided in D3.4 and cannot
  change semantics, plan, or results.
- **P3-AC09:** Independent visual/UX review confirms the approved design
  system, hierarchy, interaction, accessibility baseline, anti-spaghetti
  behavior, and representative states.
- **P3-AC10:** No Phase 4+ policy, broad node catalog, experiment UX, export,
  AutoML, agent control, plugin, hosted, or unapproved runtime behavior is
  introduced.
- **P3-AC11:** Quality, dependency, license, fixture, artifact, hygiene, and
  documentation evidence remains current; every new dependency and fixture
  passed D0.6/D0.7 controls.
- **P3-AC12:** Independent validation has no unresolved Critical or High
  finding, and Central reconciles the phase against OV §§2–7, 18–22A, 25,
  and 31.

## 10. Phase 3 Guardrails

1. **No UI semantics:** the browser edits and presents; it does not validate
   authoritatively, execute, or compute results.
2. **No fake slice:** the slice runs real library operations on real bytes,
   not canned results.
3. **No scope theft:** slice operations stay minimal and leave Phase 4/5
   policy explicitly open.
4. **No hidden dependencies:** boundary interfaces always trace back to
   canonical edges.
5. **No forced layout:** the editor assists layout only through explicit user
   actions.
6. **No design drift:** substantial UI follows the accepted design system.
7. **No dependency convenience:** UI, test, or runtime libraries go through
   existing dependency and license controls.
8. **No environment damage:** non-Windows workers follow the CONTRIBUTING
   workaround and never replace the Windows installations.

## 11. Risks and Controls

| Risk | Control | Escalation condition |
|---|---|---|
| Region/boundary model confuses users | WS3.2 prototype and fresh-user walkthrough with explicit questions | Users cannot tell where a value came from or goes |
| UI duplicates contract or validation logic | Contracts and validation served by backend; drift tests | A form or rule exists only in UI code |
| Slice operations preempt Phase 4/5 policy | D3.1 states open policies; minimal operation set | A packet sets type inference, profiling, model, or metric policy |
| Presentation state leaks into semantics | D3.4 decision; digest invariance tests | Moving or resizing changes digest, plan, or result |
| Runtime channel grows into a general API or service | D3.2 narrow contract; loopback-only | Endpoints beyond the slice or non-local exposure appear |
| Synchronous runs block the UI | D3.2 lifecycle choice with measured slice latency | Slice runtime makes the editor unusable |
| Visual quality treated as polish | D3.8 design system before substantial UI; independent review | UI packets proceed without an accepted design system |

## 12. Completion and Transition

Independent validation must inspect all D3 decisions, the slice operations,
UI/runtime contract, save/load fidelity, presentation-state isolation,
parameter propagation, error presentation, region/boundary/trace behavior,
design-system conformance, accessibility, scope, dependencies, and hygiene.
Central then reconciles the phase.

Phase 4 planning may open only after that reconciliation. Its inputs will be
the accepted editor and runtime channel, slice operation limits, presentation
model, design system, and the explicit statement that data formats, type
inference, profiling, and preparation policy remain undecided.

## 13. Next Action

Review this draft. On explicit user approval, Central records it as approved,
updates the roadmap status, and drafts P3-EP01 (D3.1–D3.4) for separate
approval. No packet or implementation is authorized by this draft.
