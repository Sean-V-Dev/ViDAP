# ViDAP P3-EP02 — Design System, Interaction Decisions, and Prototype Evidence

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Research, design, and decision; documentation and throwaway design-evidence only |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3/checkpoint A3 |
| Prerequisite | P3-EP01 complete (D3.1–D3.4 accepted 2026-10-01) |
| Workstream | WS3.2 — Design and interaction decisions |
| Decisions covered | D3.5 through D3.10 |
| Authorized worker outputs | Section 9 (decision report, `DESIGN.md`, one self-contained prototype, bounded state screenshots) |
| Central reconciliation | `ViDAP_P3_EP02_Validation_and_Reconciliation.md` (Central only) |
| Created | 2026-10-01 |
| Approved | 2026-10-01 by explicit user direction |
| Completed | 2026-10-02 by explicit Central acceptance |
| Owner | Central |

---

## 1. Authorization Boundary

The user explicitly approved this exact version on 2026-10-01. One bounded
worker may inspect the repository, research current
primary sources, write the design system and decision report, build one
throwaway prototype, capture its representative states, and run a short
walkthrough with the user. Approval does not authorize product source or
tests, dependencies, locks, endpoints, persistence, schema changes, CI,
remote changes, or P3-EP03 work.

The prototype is design evidence only. It is not product code: it is never
imported, built, served by the product, or promoted into `apps/web/`
without a later approved packet.

The worker recommends decisions and a proposed design system. A fresh
independent validator checks them. Only Central may accept D3.5–D3.10 and
the design system.

## 2. Plain-English Packet Intent

### What this packet does

It decides how the Phase 3 editor will look and behave before anyone builds
it: how regions, gutters, and boundary inputs and outputs work; how nodes
expand and get edited; how runs, results, and errors appear; what the
visual design system is; what the accessibility baseline is; and how visual
quality will be checked. It tests the riskiest idea, the region and
boundary model, with a clickable throwaway prototype before any product
code exists.

### Why this comes before implementation

`UX refinement.txt` describes an interaction model that differs from
ordinary node editors. If the editor were built first, a convenient library
default (long wires, a side inspector, a free-form canvas) could quietly
replace that model. Decision record 0002 also requires an approved design
system before substantial UI work.

### What it enables

Accepted decisions and an accepted `DESIGN.md` let P3-EP04 (editor core) and
P3-EP05 (run, results, trace) build against fixed, reviewable visual and
interaction rules, and give the final Phase 3 review a reference to check
against.

### How success is demonstrated

The report compares credible options against gates and weighted criteria,
traces every choice to `UX refinement.txt`, and backs the region/boundary
model with prototype evidence that answers the UX §23 questions and the
§24 north-star test. `DESIGN.md` covers every topic decision record 0002
requires.

## 3. Governing Inputs and Authority

The worker and validator must read these in order:

1. The explicit user approval of this exact packet version.
2. `ViDAP_Overview.txt`, especially OV §§2–7, 13, 19–22A, 25, and 31.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 1–18 (notably
   16 and 18), Phase 3, and validation scaling.
4. `ViDAP_Roadmap.md` v4.6, P3 and checkpoint A3.
5. `ViDAP_Phase_3_Plan.md` v1.1, especially D3.5–D3.10, Sections 7–11.
6. `UX refinement.txt`: by explicit user direction on 2026-10-01, the basis
   for these decisions. Each recommendation cites the sections it serves and
   records any deviation with a rationale. Its phase-status statements are
   not authoritative.
7. `docs/decisions/0002-visual-design-and-ux-quality.md`: the required scope
   of the design artifact (tentatively `DESIGN.md`), the requirement to
   select a maintained design/UX support mechanism, and the visual evidence
   expectations.
8. `docs/decisions/0001-ep05-frontend-quality-compatibility.md`: the JSX
   accessibility-lint deferral D3.9 must revisit.
9. `ViDAP_P3_EP01_Validation_and_Reconciliation.md` and the accepted
   D3.1–D3.4 in `ViDAP_P3_EP01_Decision_Report.md`, including the five-node
   slice, the `/api/slice/` contract, save/load conflict behavior, the
   presentation sidecar, F1, F6, and the V15/V16 clarifications.
10. `ViDAP_P2_EP06_Validation_and_Reconciliation.md` and accepted D2.1–D2.8,
    especially D2.4 run statuses, D2.6 visible reuse, and D2.7 errors.
11. Current `apps/web/`, `package.json` (including the existing
    `@xyflow/react` dependency), `eslint.config.js`, `CONTRIBUTING.md`,
    `README.md`, and dependency-control documentation.
12. This packet.

Higher-authority artifacts prevail. None of these inputs authorize
implementation beyond this packet.

## 4. Objective and Completion Condition

### Objective

Produce evidence-backed recommendations for:

- **D3.5:** semantic regions and boundary interfaces;
- **D3.6:** node interaction and local connection behavior;
- **D3.7:** run controls, result, and error presentation;
- **D3.8:** the visual design system and design/UX support mechanism;
- **D3.9:** the accessibility baseline; and
- **D3.10:** representative states and the visual/UX validation method;

plus a proposed `DESIGN.md` and prototype evidence for the region/boundary
model.

### Completion condition

P3-EP02 is complete only when the Section 9 outputs exist and pass the
worker's final attestation; a fresh independent validator returns `Accept`;
no dependency, product code, schema change, or Phase 4+ policy is hidden in
a recommendation; and Central separately accepts, rejects, or returns each
decision and the design system in a reconciliation record.

## 5. Preconditions and Stop Gates

Before writing, the worker must record: this packet's approval; P3-EP01
complete; branch, `HEAD`, staged/unstaged/untracked state and owners of
pre-existing paths; no collision with any Section 9 path; both lock hashes;
and how the final attestation will run (directly on Windows, or through the
`CONTRIBUTING.md` workaround).

Stop with a `Blocked` report if a responsible recommendation would require
installing a dependency, changing product code or the accepted D3.1–D3.4
boundaries, settling a Phase 4+ policy, or evidence that primary sources and
the prototype cannot supply. If the prototype shows the region/boundary
model failing its UX §23 questions, that is a valid finding, not a stop:
record it and recommend the revision UX §23 allows, presentation-only and
without changing the canonical workflow.

## 6. Non-Negotiable Decision Constraints

1. Regions, gutters, and boundary interfaces are presentation over canonical
   edges. They never become a second graph, hidden global state, or
   execution input; every boundary value traces to its canonical producer
   and consumers.
2. The UI never validates authoritatively, executes, or computes results.
   Forms come only from backend contracts; displayed results only from
   recorded output (A3, accepted D3.2).
3. Visible nodes are responsibility-level; no per-implementation node
   catalog; no permanent side inspector as the primary configuration model
   unless the prototype shows in-place expansion fails (UX §§1, 8–11).
4. Users own spatial arrangement; layout assistance is explicit only
   (UX §§3, 6, 20).
5. Accepted D3.1–D3.4 and the V15/V16 clarifications are inputs, not open
   questions. A conflict is reported to Central, not resolved here.
6. Recommended libraries or tools are candidates only; selection and
   installation require a later approved packet with D0.6 evidence. The
   existing `@xyflow/react` dependency may be assessed for fit, not
   upgraded or reconfigured.
7. The design system follows decision record 0002: intentional,
   information-dense, readable analytical workspace, not decoration; graph
   visually dominant; glance-to-investigate-to-verify.
8. Phase 4–6 presentation (data summaries, model results, experiment
   history) is not designed here beyond leaving room for it.
9. The report is a design and architecture decision, not legal advice.

## 7. Required Decision Analysis

Apply every gate before scoring; a candidate that fails a gate is
ineligible.

| Gate | Required result |
|---|---|
| G1 — Canonical traceability | Every rendered dependency maps to canonical edges and can be revealed on demand. |
| G2 — Backend authority | UI presents contracts, validation, and results from the backend only. |
| G3 — Accepted-decision continuity | Consistent with D3.1–D3.4, F1, F6, and V15/V16. |
| G4 — UX basis | Follows `UX refinement.txt` or records a justified deviation. |
| G5 — Accessibility | Meets the D3.9 baseline, including keyboard operation and non-color cues. |
| G6 — Phase boundary | No Phase 4+ presentation or policy is designed or settled. |
| G7 — Dependency posture | No dependency selected or installed; candidates carry evidence. |
| G8 — Proportionality and testability | Fits Windows, the existing stack, and proportionate automated and visual checks. |

Scores use 1–5 with rationale and confidence; weighted points are
`weight × score / 5`, with reproducible totals and an explanation if a
recommendation differs from the numerical leader.

| Criterion | Weight |
|---|---:|
| UX-refinement alignment | 22 |
| At-a-glance intelligibility and orientation | 16 |
| Interaction quality and anti-spaghetti effect | 14 |
| Canonical fidelity and backend authority | 14 |
| Accessibility | 12 |
| Maintainability and testability | 12 |
| Dependency and maintenance posture | 10 |
| **Total** | **100** |

### D3.5 — Semantic regions and boundary interfaces

Compare at minimum: (A) vertical regions with resizable gutters, boundary
rails, name-matched boundary outputs and inputs, and on-demand trace/X-ray;
(B) regions with ordinary long wires routed through gutters; and (C) an
unrestricted canvas with optional grouping frames. Specify: the slice's
region names and order; gutter drag behavior and limits; boundary rail
layout; how a boundary value is named and matched by semantic identity, not
vertical alignment (UX §4.4); how the gutter visibly breaks the wire
(UX §4.5); producer/consumer reveal on hover, selection, and keyboard
focus (UX §5); trace/X-ray behavior (dim unrelated, reveal real path,
exit); how the three complexity forms are handled (UX §7); and the
"Unassigned" region from D3.4.

### D3.6 — Node interaction and local connection behavior

Compare at minimum: (A) compact, in-place expanded with bounded internal
scrolling, and optional focus mode, no permanent inspector; (B) compact
nodes plus a persistent side inspector; (C) modal editing dialogs. Specify
what the compact state shows for each slice node; expansion trigger and
maximum size; internal scrolling that never pans or zooms the canvas; clear
separation of scroll, drag, control editing, pan, and zoom (UX §9.3);
contract-driven control mapping by parameter kind (bool, int, float, with
bounds) from D1.4 contracts; typed port and connection feedback; local
reroute, highlight, dim, align, and tidy as explicit actions; and how the
generic Model node shows its fixed implementation (UX §11).

### D3.7 — Run controls, result, and error presentation

Compare at minimum: (A) a persistent run control with per-node status, the
primary result kept visible near the canvas, and errors shown on the
affected node with expandable technical detail; (B) a separate results
panel or page; (C) transient notifications. Specify statuses (D2.4
completed/failed/blocked/unrelated, plus not-run and running), how
visible reuse (D2.6) is shown if at all, how Phase 1 validation diagnostics
differ visually from runtime errors (D2.7, F6), how the slice metrics (F1)
stay visible while editing (UX §15) without designing Phase 5 result views,
how a conflict from D3.3 is shown, and the busy state from D3.2's
single-run limit.

### D3.8 — Visual design system and design/UX support mechanism

Compare at minimum, for the styling mechanism: (A) project-owned design
tokens (for example CSS custom properties) and hand-built components on the
existing stack; (B) adopting a component library; (C) a utility-CSS
framework. Compare, for the decision record 0002 support mechanism, at
least two current maintained options (for example a design-review skill or
plugin, a written review checklist with a review workflow, or a
component-catalog tool), with primary-source maintenance and license
evidence. Decide light/dark expectations, minimum window size, and density
targets. Produce the proposed `DESIGN.md` (Section 9).

### D3.9 — Accessibility baseline

Set measurable targets: a WCAG 2.2 conformance level for contrast, focus
visibility, and keyboard operation; how every canvas action (select, move,
connect, expand, trace, resize gutter, run) is reachable by keyboard;
labeling for nodes, ports, and boundary values; non-color status cues; and
reduced-motion behavior. Recheck, from primary package metadata, whether
the JSX accessibility-lint deferral in decision record 0001 can now end with
a maintained, peer-compatible package for the current ESLint and
TypeScript-ESLint versions; recommend ending, extending, or replacing the
deferral without installing anything.

### D3.10 — Representative states and the visual/UX validation method

Name the representative state set, covering at least: empty canvas; valid
slice; invalid connection; validation errors; running; success with metrics;
runtime failure on the Model node (F6 message); trace active; expanded node
with internal scroll; focus mode; narrow and wide regions; keyboard focus
visible; save conflict; busy. Choose the method for later packets:
automated browser tests and tooling candidates (for example Playwright)
with D0.6 evidence still to be collected, screenshot review against
`DESIGN.md`, keyboard and contrast checks, a fresh-user walkthrough, and
independent visual/UX review. Define the walkthrough tasks and questions
P3-EP06 will reuse.

## 8. Prototype Evidence Rules

1. **One self-contained file.** The prototype is a single HTML file with
   inline CSS and JavaScript, no external scripts, fonts, network requests,
   build step, package, or dependency. It opens directly in a current
   desktop browser.
2. **Illustrative data only.** It contains no backend calls and no real
   computation. Every displayed value is visibly labeled as illustrative.
   It must not present itself as the product or as run evidence.
3. **Required content (UX §23):** multiple regions; several connected nodes
   inside at least one region (V12/F5); the D3.1 slice's Split → Evaluate
   skip-region dependency; one output consumed by several later nodes; an
   illustrative branched model comparison; resizable gutters; compact and
   expanded nodes with internal scroll; boundary hover and trace/X-ray; and
   a toggle that shows the same graph as an unrestricted canvas with
   ordinary long wires, for comparison.
4. **Accessibility in the prototype:** keyboard reach for trace, expand, and
   gutter resize is demonstrated, so D3.9 is tested, not only stated.
5. **Screenshots.** The worker captures the D3.10 states the prototype can
   show, using any browser outside the repository. No repository
   dependency, script, or configuration is added for this.
6. **Walkthrough.** The worker writes a short task script (for example:
   find where Evaluate's input came from; list every consumer of Split;
   resize PREPARE without moving nodes elsewhere; expand Model and change a
   value; switch to the free canvas and repeat the first task). The user
   performs it and answers the UX §23 questions and the UX §24 north-star
   test. The worker records the answers verbatim in summary form, with the
   limitation that the user authored the UX direction and is not a fresh
   user. P3-EP06 performs the fresh-user walkthrough on the real editor.

## 9. Exact Authorized Outputs

The worker may create or modify only:

| Path | Purpose |
|---|---|
| `ViDAP_P3_EP02_Decision_Report.md` | D3.5–D3.10 analysis, recommendations, prototype findings, walkthrough record, attestation |
| `DESIGN.md` | Proposed concise ViDAP design system covering every decision record 0002 topic; marked proposed until Central accepts it |
| `docs/design/p3-ep02-prototype/index.html` | The single self-contained throwaway prototype |
| `docs/design/p3-ep02-prototype/states/*.png` | At most 16 representative-state screenshots, each at most 500 KiB |

No other repository path may be added, modified, moved, staged, committed,
or deleted. Outputs must not contain absolute user paths, credentials, raw
environment values, copied lockfiles, full command logs, or third-party
copyrighted design assets.

The report must contain: approval, versions, baseline, and pre-existing
ownership; a primary-source bibliography with retrieval dates; G1–G8 and
weighted comparisons for every decision; recommendations with rejected
alternatives, confidence, limitations, and consequences for P3-EP03–EP06;
a UX trace table with any deviations; prototype findings against UX §23 and
§24, with the walkthrough record and its limitation; candidate tools and
dependencies with the evidence a later step must collect; findings for
Central; and the worker self-assessment and final attestation.

## 10. Required Execution Sequence and Final Attestation

1. Read every governing input; record versions and the Section 5 baseline.
2. Research current primary sources (WCAG 2.2, `@xyflow/react`
   documentation for keyboard and accessibility support, candidate design
   support mechanisms, JSX accessibility-lint package metadata, candidate
   browser-testing tools).
3. Draft recommendations and `DESIGN.md`; build the prototype; capture
   states; hand the user the walkthrough script and record the result.
4. Re-read all outputs against Sections 4 and 6–9.
5. Run, in order: `npm.cmd run check`, `npm.cmd run coverage`,
   `npm.cmd run deps:inventory`, `npm.cmd run license:check`,
   `npm.cmd run deps:audit`, and `git diff --check`, then lock hashes and
   `git status --porcelain`. A worker whose shell cannot run these follows
   `CONTRIBUTING.md`: hand the user the exact ordered list (the summary-line
   loop used for P3-EP01 is acceptable) and record the pasted output as a
   user-executed Windows run, claiming only what it shows. Because the
   outputs are untracked, also inspect each directly: no trailing whitespace
   and a final newline in text files; no user paths or secrets; the
   prototype contains no external URL, network call, or script source; the
   screenshot count and sizes are within Section 9 limits.
6. If an authorized output causes a failure, repair only that output and
   rerun the full sequence; otherwise stop with a named blocker.
7. Confirm locks unchanged and the Section 9 paths are the only worker
   changes. Stop for independent validation; do not self-validate, stage,
   commit, push, or begin P3-EP03.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP02-AC01 | Approval, prerequisites, versions, baseline, ownership, and locks are accurately recorded without sensitive data. |
| EP02-AC02 | D3.5–D3.10 each have a recommendation, alternatives, G1–G8 results, reproducible weighted totals, confidence, limitations, and consequences. |
| EP02-AC03 | Changeable claims cite primary sources with retrieval dates; inference is labeled. |
| EP02-AC04 | Every recommendation traces to `UX refinement.txt` sections, and every deviation has a rationale. |
| EP02-AC05 | D3.5 keeps all rendered dependencies canonical and traceable, matches boundary values by identity, breaks wires visibly at gutters, and keeps layout assistance explicit. |
| EP02-AC06 | D3.6 and D3.7 keep forms contract-driven and results backend-recorded, avoid a primary side inspector unless prototype evidence justifies one, separate input gestures, and keep the primary result visible. |
| EP02-AC07 | `DESIGN.md` covers every decision record 0002 topic, selects a maintained design/UX support mechanism with evidence, and stays proportionate and information-dense. |
| EP02-AC08 | D3.9 sets measurable accessibility targets demonstrated in the prototype and gives an evidence-based recommendation on the decision record 0001 deferral. |
| EP02-AC09 | D3.10 names the representative states and a proportionate validation method, including walkthrough tasks reusable in P3-EP06. |
| EP02-AC10 | The prototype meets Section 8, answers UX §23 and §24 with recorded evidence and stated limitations, and is not presented as product or run evidence. |
| EP02-AC11 | No dependency, lock, product source or test, endpoint, persistence, schema, CI, or remote change occurs; only Section 9 paths change. |
| EP02-AC12 | The complete final attestation passes (directly or as a recorded user-executed Windows run); locks unchanged; output hygiene verified. |
| EP02-AC13 | A fresh independent validator returns `Accept`, including an independent look at the prototype and screenshots against `DESIGN.md`. |
| EP02-AC14 | Central explicitly accepts D3.5–D3.10 and `DESIGN.md` before this packet is complete or substantial UI packets are approved. |

## 12. Independent Validation Contract

A fresh validator must read every governing input, this packet, and all
Section 9 outputs; open the prototype and check it against Section 8 and
`DESIGN.md`; recheck high-impact sources; recalculate totals and apply
G1–G8 independently; challenge each recommendation for hidden
dependencies, UI authority, Phase 4+ design, or unjustified departure from
`UX refinement.txt`; check `DESIGN.md` against decision record 0002;
reproduce the Section 10 attestation (directly or through the
`CONTRIBUTING.md` workaround); verify scope and hygiene; and return
`Accept`, `Revise`, or `Blocked` with criterion-linked findings and a Central
recommendation. The validator may not edit files, accept for Central, write
the reconciliation, or begin P3-EP03.

## 13. Fresh-Chat Handoff Prompts

### Execution worker

> Execute approved `ViDAP_P3_EP02.md` v0.1 as the bounded design and interaction decision worker. Read every governing input, especially `UX refinement.txt` (the decision basis), decision records 0001 and 0002, and the accepted P3-EP01 reconciliation. Create or modify only the Section 9 paths: the decision report, a proposed `DESIGN.md`, one self-contained throwaway prototype, and at most 16 state screenshots. Recommend D3.5–D3.10 with the Section 7 gates and weights, build the prototype per Section 8, and run the walkthrough with the user. Do not install or select dependencies, change product code, or design Phase 4+ presentation. Run the Section 10 attestation, using the `CONTRIBUTING.md` Windows workaround if needed. Stop with the outputs and a validation handoff; do not self-validate, accept for Central, stage/commit/push, or begin P3-EP03.

### Independent validator

> Act as the independent validator for approved `ViDAP_P3_EP02.md` v0.1. Read every governing input and all Section 9 outputs, open the prototype, and follow Section 12: recheck sources, recalculate totals, apply G1–G8, check `DESIGN.md` against decision record 0002, and challenge D3.5–D3.10 against `UX refinement.txt`. Reproduce the Section 10 attestation (using the `CONTRIBUTING.md` workaround if needed) with lock, scope, and hygiene checks. Do not edit files, accept for Central, write reconciliation, or begin P3-EP03. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and a Central recommendation.

## 14. Next Action

P3-EP02 is complete. The independent `Accept` and Central acceptance of
D3.5–D3.10 and `DESIGN.md` v0.2 are recorded in
`ViDAP_P3_EP02_Validation_and_Reconciliation.md`. P3-EP03 is ready to draft.
