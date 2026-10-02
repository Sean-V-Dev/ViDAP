# ViDAP P3-EP02 — Design System, Interaction Decisions, and Prototype Evidence Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP02.md` v0.1, explicitly approved by the user 2026-10-01 |
| Worker execution | 2026-10-01; Linux shell over the Windows checkout, cloud browser for screenshots, user-executed Windows attestation per `CONTRIBUTING.md` |
| Worker result | Revision 2 after an independent `Revise` (V1–V6, L1–L9; Section 12): `DESIGN.md` v0.2, revised prototype and 16 screenshots; Revision 2 attestation in Section 10 |
| Independent validation | Pending; this report is not a verdict |
| Central acceptance of D3.5–D3.10 and `DESIGN.md` | Pending |

## 1. Authority, inputs, and sanitized baseline

Governing inputs read: the user's 2026-10-01 approval of this exact packet;
`ViDAP_Overview.txt`; Spine v1.3; Roadmap v4.6; Phase 3 plan v1.1;
`UX refinement.txt` (the decision basis by user direction); decision records
0001 and 0002; the P3-EP01 reconciliation and decision report (D3.1–D3.4,
F1, F6, V15/V16); the P2-EP06 reconciliation and D2.1–D2.8; current
`apps/web/`, `package.json`, `eslint.config.js`, `CONTRIBUTING.md`,
`README.md`, and the dependency-control documentation.

Baseline before writing: branch `main`, `HEAD`
`678f1986cce18286c3b9ba9479ae0b919c8a3184`, no staged path. Pre-existing
Central-owned changes: modified `ViDAP_Phase_3_Plan.md` and
`ViDAP_Roadmap.md`; untracked `ViDAP_P3_EP01.md`,
`ViDAP_P3_EP01_Decision_Report.md`,
`ViDAP_P3_EP01_Validation_and_Reconciliation.md`, and `ViDAP_P3_EP02.md`.
None of the Section 9 paths existed. Installed versions read from the
checkout: `@xyflow/react` 12.11.6, ESLint 10.10.0, TypeScript-ESLint 8.70.0.

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Attestation route: the `CONTRIBUTING.md` workaround (user-executed Windows
run). Screenshots were taken with a headless browser in the worker's cloud
workspace, outside the repository; no repository dependency, script, or
configuration was added.

## 2. Primary sources (retrieved 2026-10-01)

| ID | Source | Fact used |
|---|---|---|
| S1 | w3.org/TR/WCAG22 (W3C Recommendation, 12 Dec 2024) | 1.4.3 Contrast Minimum AA 4.5:1; 1.4.11 Non-text Contrast AA 3:1; 2.1.1 Keyboard A; 2.4.7 Focus Visible AA; 2.4.11 Focus Not Obscured (Minimum) AA; 2.5.7 Dragging Movements AA (alternative to dragging); 2.5.8 Target Size (Minimum) AA; 1.4.1 Use of Color A; 2.3.3 Animation from Interactions AAA |
| S2 | w3.org/WAI/WCAG22/Understanding/target-size-minimum | 2.5.8 sets a 24 by 24 CSS pixel minimum (title and summary seen in search results; full page not fetched) |
| S3 | reactflow.dev accessibility guide (updated 31 Aug 2026) | Nodes and edges focusable with Tab; Enter/Space select; Escape clears; arrow keys move selected nodes; `ariaLabelConfig`; assertive live region; `disableKeyboardA11y`. The guide does not describe connecting nodes by keyboard |
| S4 | github.com/jsx-eslint/eslint-plugin-jsx-a11y `package.json` | Version 6.10.2, MIT, ESLint peer range `^3` through `^9`; ESLint 10 is not declared |
| S5 | playwright.dev release notes; github.com/microsoft/playwright | Latest 1.63; Apache-2.0; Chromium, Firefox, and WebKit on Windows; `toMatchAriaSnapshot`, screenshot comparisons |
| S6 | github.com/dequelabs/axe-core | MPL-2.0; tests WCAG 2.0–2.2 A/AA/AAA; finds on average about 57% of issues automatically; flags items needing manual review |
| S7 | anthropics/claude-code `plugins/frontend-design` README | An AI skill that generates frontends with "bold aesthetic choices" and distinctive visuals |
| S8 | anthropics/claude-code `LICENSE.md` | "All rights reserved. Use is subject to Anthropic's Commercial Terms of Service": not an open-source license, so review-required under D0.6 if ever adopted as a dependency |
| S9 | github.com/storybookjs/storybook | MIT; supports React and Vite (latest version not shown on the page; recheck in the registry) |
| S10 | github.com/jsx-eslint/eslint-plugin-jsx-a11y issue #1075 | ESLint 10 support is open; the maintainer intends to support it but gave no date; related pull requests are unmerged |
| S11 | github.com/es-tooling/eslint-plugin-jsx-a11y-x; upleveled/eslint-config-upleveled PR #707 | jsx-a11y-x is MIT, maintained by es-tooling; the PR reports its peer range as ESLint `^9 || ^10` (secondary report; recheck in the registry) |

The npm registry metadata endpoints were blocked from both worker shells, so
package facts come from the projects' own repositories and documentation.
The validator independently confirmed S3 against the installed
`@xyflow/react` 12.11.6 source and reported that the jsx-a11y repository has
had no commits since January 2026; the worker could not fetch the commit
history (blocked by the site), so that date is recorded as the validator's
observation.
Version, peer, and license facts must be rechecked from the registry in the
later dependency step. Everything in Sections 4–9 not labeled S1–S7 is
design inference or prototype observation.

## 3. Gates and scoring

Gates G1–G8 are the packet's Section 7 gates. Scores use the packet weights
in this order: UX-refinement alignment 22, at-a-glance intelligibility 16,
interaction quality 14, canonical fidelity 14, accessibility 12,
maintainability/testability 12, dependency posture 10. Weighted points are
`weight × score / 5`; totals were recomputed by script.

## 4. Recommendations

Gate results are shown per candidate. A G4 failure means the candidate
contradicts an explicit `UX refinement.txt` requirement, not merely a
preference. Each matrix is followed by the per-criterion reasoning in the
order UX, glance, interaction, fidelity, accessibility, maintainability,
dependency.

### D3.5 — Vertical regions with boundary rails, identity-matched values, on-demand trace, and rail-based connection feedback (H)

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. Regions, gutters, boundary rails, identity matching, trace/X-ray | all P | 5,5,5,5,4,4,5 | 95.2 |
| B. Regions with ordinary long wires through gutters | G4 F (UX §4.5) | 2,3,2,5,4,4,5 | 67.2 |
| C. Unrestricted canvas with optional grouping frames | G4 F (UX §§4, 20) | 1,2,2,5,4,5,5 | 62.0 |

Reasoning. A: fully matches UX §§2–5; the walkthrough read it at a glance;
rails remove gutter-crossing wires; canonical edges are unchanged; trace and
rails are keyboard-reachable but add focus targets (4); custom rendering
beside the graph library is more code (4); no dependency. B and C keep
fidelity and libraries but reintroduce long wires, which the walkthrough
found harder to read (screenshot 07).

Behavior is specified in `DESIGN.md` Section 4: the slice regions; a far-right
UNASSIGNED region shown only when needed; Inputs and Outputs rails;
`Name.port` values whose names come from the node label or type label with
an ordinal, matched by canonical node ID and port key; one Outputs entry per
value and one Inputs entry per consuming port, each level with its port;
hover/focus card; trace that de-emphasizes without losing text contrast;
gutter widths from "fits its nodes" to 900; and **connection feedback** (V1):
compatible ports outlined and incompatible ports marked ✕ while connecting
(screenshot 13); an invalid existing connection shown as amber entries on
both rails with short amber wires, never a wire across a gutter
(screenshot 11); right-to-left dependencies drawn the same way, with
validity decided by workflow validation.

### D3.6 — Compact nodes that expand in place, with an optional focus mode and no permanent inspector (H)

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. Compact → in-place expanded (bounded, internal scroll, push-down) → optional focus mode | all P | 5,5,4,5,4,4,5 | 92.4 |
| B. Compact nodes plus a persistent side inspector | all P (UX §10 allows a validated sidebar later) | 2,4,4,5,4,4,5 | 76.0 |
| C. Modal editing dialogs | G4 F (UX §9.4 prefers the node over a separate screen) | 1,2,2,5,3,4,5 | 57.2 |

Reasoning. A follows UX §§9–10 and kept spatial context in the walkthrough;
editing in place interacts with neighbors, mitigated by push-down (4);
contract-driven; keyboard expand and focus demonstrated; bounded layout
logic (4). B separates editing from the node (UX 2) but is otherwise sound.
C breaks orientation and is harder to make accessible.

`DESIGN.md` Section 5 now gives the compact content for each slice node and
derives controls **only from existing D1.4 contract fields** (V2): boolean →
checkbox, `allowedValues` → select, integer → step 1, number → no step
restriction, `minimum`/`maximum` → bounds, `nullable` → a "None" choice,
fixed values → read-only text. No step or other new contract field is
needed. Keyboard: arrows navigate the graph (Right to the first downstream
node and Shift+Right to the next, Left upstream, Up/Down within a region), M
enters move mode, and ports have accessible names (screenshot 15).

### D3.7 — Persistent run control, primary result in the top bar, errors on the node (H)

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. Run control and primary result in the top bar; per-node status; errors on the affected node | all P | 5,5,4,5,4,4,5 | 92.4 |
| B. Separate results panel or page | G4 F (UX §15) | 2,2,3,5,4,4,5 | 66.8 |
| C. Transient notifications | G4 F (UX §15), G5 F (messages vanish) | 1,2,2,4,2,4,5 | 52.0 |

Reasoning. A keeps change and consequence together (UX §15), shows every
status with icon and words, and needs no dependency. B moves the result
away from the canvas; C loses failures.

Statuses follow D2.4 plus not-run and running (`DESIGN.md` Section 6), with
"Unrelated" shortened so it fits and a tooltip that explains it. Runtime
errors use **only the fixed text for the failure code** (V3): for example
"A text column reached the model without encoding", with no column name or
exception content, as accepted F6 requires. Phase 1 validation problems are
amber "Fix before running". The save conflict, busy (shown during a run,
screenshot 08), and the primary result follow D3.2/D3.3/F1. Attempt-local
reuse (D2.6) is not shown in Phase 3 (L2).

### D3.8 — Project-owned tokens and components; `DESIGN.md` with a review loop as the support mechanism (M)

Styling mechanism:

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. Project-owned CSS custom-property tokens and hand-built components on the existing stack | all P | 5,4,4,5,4,4,5 | 89.2 |
| B. Adopt a component library | all P | 3,4,4,5,5,3,2 | 74.4 |
| C. Adopt a utility-CSS framework | all P | 3,4,4,5,4,3,2 | 72.0 |

Reasoning. A fits the editor's specific vocabulary (regions, rails,
gutters) that libraries do not provide, with no new dependency; B's
accessible primitives score higher on accessibility but add a dependency
and a second visual language; C adds a build-time dependency for little
editor-specific benefit.

Support mechanism (decision record 0002):

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| i. `DESIGN.md` as sole authority, with a state-capture and checklist review loop plus independent review | all P | 5,4,4,5,4,4,5 | 89.2 |
| ii. The frontend-design AI skill (S7) as the design authority | all P | 2,3,3,5,3,3,4 | 63.2 |
| iii. A component catalog, Storybook (S9) | all P | 3,4,4,5,4,4,2 | 74.4 |

Reasoning (V6). i keeps one authority inside the repository and matches
decision record 0002's review requirement. ii aims at "bold aesthetic
choices" (S7), which conflicts with decision record 0002's quiet,
information-dense direction, and its repository license is "All rights
reserved" under commercial terms (S8), so it is review-required under D0.6
and suitable at most as an optional draft aid. iii is MIT (S9) and useful
once there are many components, but it is a sizable development dependency
Phase 3 does not need yet; `DESIGN.md` Section 11 records it as a reasonable
later addition through the dependency controls.

Light theme only in Phase 3, with role-named tokens; default zoom 100%;
minimum window 1280×720 with a wrapping top bar and horizontal scrolling.

### D3.9 — WCAG 2.2 Level AA at the default zoom, full keyboard parity, and an extended lint deferral (H)

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. WCAG 2.2 AA; keyboard parity for every canvas action; extend decision record 0001 with compensating checks | all P | 5,4,4,5,5,4,5 | 91.6 |
| B. WCAG 2.2 Level A only | G5 F (no contrast, focus, or target minimums) | 3,4,4,5,2,5,5 | 78.0 |
| C. WCAG 2.2 AAA | all P | 3,3,3,5,5,2,5 | 72.0 |

Reasoning. A matches decision record 0002 and is measurable; B omits AA
criteria the editor needs; C's AAA contrast and motion rules would constrain
the dense graph more than the benefit warrants for Phase 3.

Revision 2 makes the prototype meet the targets **at the default zoom of
100%** (V4). Measured headlessly: smallest button 24×24, gutter hit area
24 wide, smallest text 10 pixels, no truncated rail text, and no top-bar
overflow at 1280×720 (screenshot 16). The 85% and 70% zooms remain an
explicit overview where minimums are not guaranteed; nothing requires them.
Dimming during trace no longer uses transparency: unrelated items get a grey
fill and lighter border while text keeps at least 6.9:1 (L5). Connecting by
keyboard is still for P3-EP04 (S3).

**Decision record 0001 (G-F1, L7):** `eslint-plugin-jsx-a11y` 6.10.2 still
declares ESLint only up to 9 (S4), its ESLint 10 issue is open with no date
(S10), and the validator observed no repository commits since January 2026.
A replacement exists: `eslint-plugin-jsx-a11y-x` (MIT, es-tooling), reported
to support ESLint 9 and 10 (S11). Recommendation: extend the deferral now,
and name jsx-a11y-x as the candidate to evaluate, with registry-verified
peer, license, and maintenance evidence, in the packet that adds the
editor's first substantial JSX (P3-EP04). Compensating checks until then:
accessibility-tree assertions in browser tests (S5), optionally axe-core
(S6, MPL-2.0, review-required), and manual keyboard and contrast checks
against `DESIGN.md`.

### D3.10 — Representative states and a layered validation method (M)

| Candidate | Gates | Scores | Total |
|---|---|---|---:|
| A. Browser tests capturing named states, keyboard and contrast checks, a walkthrough, and independent visual review | all P | 5,5,4,5,5,4,4 | 92.8 |
| B. Unit tests only | G4 F (UX §23 needs a prototype test), G5 F | 1,2,2,5,2,5,5 | 57.2 |
| C. Manual review only | all P | 3,4,3,5,3,2,5 | 70.4 |

Reasoning. A covers what users see and decision record 0002's evidence
list; it needs a browser-test dependency later (4). B cannot see layout or
interaction; C is not repeatable.

**Representative state set** (prototype screenshot numbers): empty canvas
[14]; valid slice not run [01]; boundary hover [02]; trace active [03];
expanded node with push-down and internal scroll [04]; focus mode [05];
resized regions [06]; free-canvas comparison [07, prototype only]; running
with a busy notice [08]; success with metrics [09]; runtime failure on
Model [10]; validation error shown on rails [11]; save conflict [12];
connecting with port feedback [13]; keyboard navigation and move mode [15];
minimum window 1280×720 [16]. P3-EP04/EP05 add: invalid parameter value,
connecting by keyboard, and the UNASSIGNED region.

**Method for later packets:** browser tests that drive the real editor into
each state, with screenshot capture and accessibility-tree assertions
(Playwright is the leading candidate, S5; its D0.6 evidence is collected in
the packet that adds it); keyboard and contrast checks against `DESIGN.md`
Sections 2 and 9 at 100% zoom and at 1280×720; the Section 12 checklist; a
fresh-user walkthrough in P3-EP06 using the exact script in Section 8; and
independent visual review of the captured states.

## 5. Consequences for later packets

| Packet | Consequence |
|---|---|
| P3-EP03 (backend slice) | No change from P3-EP01. Contracts use only existing D1.4 fields (label, description, kind, minimum, maximum, allowedValues, nullable); runtime failure messages are fixed text per F6 code. |
| P3-EP04 (editor core) | Implements tokens and `DESIGN.md` Sections 3–7 and 9; decides how rails and gutters coexist with `@xyflow/react`; turns off the library's arrow-key node moving in favor of graph navigation and move mode (G-F7); designs keyboard connecting; implements connection feedback and rail-based invalid connections; evaluates jsx-a11y-x (G-F1). |
| P3-EP05 (run, results, trace) | Implements Section 6 states, the primary result in the top bar, fixed-text node errors, and trace with contrast-safe dimming. |
| Packet adding browser tests | Brings Playwright and any accessibility-check library through D0.6. |
| P3-EP06 (closeout) | Fresh-user walkthrough with the Section 8 script, including a check of the W1–W5 revisions; independent visual review against `DESIGN.md` Section 12. |

## 6. Findings for Central

| ID | Severity | Finding | Owner |
|---|---|---|---|
| G-F1 | Non-blocking | Extend decision record 0001's JSX accessibility-lint deferral; evaluate jsx-a11y-x in P3-EP04 (D3.9). | Central |
| G-F2 | Non-blocking | Keyboard connecting is not covered by the graph library's documented keyboard support (S3); P3-EP04 designs it. | P3-EP04 |
| G-F3 | Non-blocking | Expanded nodes push nodes below them but can still overlap a neighboring rail sideways; opening toward open space is a P3-EP04 option. | P3-EP04 |
| G-F4 | Non-blocking | At 100% zoom the nine-node prototype is wider than a 1920 screen; horizontal scrolling and the overview zooms handle it, and larger workflows will need collapse and composite tools sooner. | P3-EP04 / later phases |
| G-F5 | Non-blocking | Package metadata could not be read from the npm registry; versions, peers, and licenses must be rechecked there before any install. | Dependency steps |
| G-F6 | Info | The Phase 3 plan's input list does not name decision record 0002, although this packet relies on it. | Central |
| G-F7 | Non-blocking | The graph library moves selected nodes with arrow keys by default (S3); P3-EP04 must turn that off and keep move mode. | P3-EP04 |
| G-F8 | Info | Fixed error text cannot name the offending column. Naming it would need a separate Central decision to allow bounded, sanitized parameters in failure text. | Central |
| G-F9 | Info | The 85% and 70% overview zooms can fall below the size and text minimums; they are optional and nothing depends on them. | Central / P3-EP04 |

## 7. Prototype evidence and UX trace

The prototype (`docs/design/p3-ep02-prototype/index.html`, Revision 2) is
one self-contained file: inline CSS and JavaScript, no external script,
font, or network request (a headless run recorded zero external requests
and zero console errors; the only URL-like string is the SVG namespace
identifier). All values are labeled illustrative, and a top badge says it is
not the product. It contains the five slice nodes plus four labeled extras.
Two biases are stated on the page itself (L4, L5): Family size sits between
Prepare Data and Split, where the slice connects them directly; and the free
canvas reuses the region layout's positions instead of a hand-arranged free
layout, which may favor regions.

| UX section | Where it is applied | Deviation |
|---|---|---|
| §§1, 8 responsibility and composite nodes | Node kickers; Prepare Data lists its inner steps | None |
| §2 vertical regions, left to right | Workspace layout; UNASSIGNED at far right | None |
| §3 resizable gutters, user-owned layout | Gutters; region-relative positions; temporary push-down | Push-down is temporary and reverts (walkthrough W4) |
| §4 boundary rails, identity matching, broken wire | Rails; invalid connections also on rails | §4.2's single fan-out entry is replaced by one entry per consuming port (walkthrough W2) |
| §5 inspectable boundaries, X-ray | Hover/focus card; trace | None |
| §§6–7 local wiring, three complexity forms | Local wires; `DESIGN.md` Section 4 | Reroute points and tidy are specified, not prototyped |
| §9 compact, expanded, bounded scroll, focus | Nodes | Sideways overlap remains (G-F3) |
| §10 no permanent inspector | No inspector | None |
| §11 generic Model responsibility | Model kicker plus implementation line | None |
| §15 visible results | Primary result in top bar | None |
| §16 preview labeling | Amber "illustrative" labels | None |
| §18 human and agent edits | Save-conflict banner (D3.3) | None |
| §§23–24 prototype questions, north-star | Section 8 walkthrough | See Section 8 |

## 8. Walkthrough

### Script (reusable in P3-EP06)

The prototype or editor opens on the valid slice. The participant reads
each task, does it, and says what they see.

| # | Task (exact wording) | Checks |
|---|---|---|
| 1 | "Without hovering anything, say where the data enters, what happens to it, which model approach is used, where the branches are, and what the outcome would be." | UX §24 north-star |
| 2 | "Find where Evaluate (A)'s `split` input comes from." (In the revised prototype and the editor: "Evaluate 1".) | UX §23 Q1 |
| 3 | "List every node that uses the Split output." | UX §23 Q1 |
| 4 | "Make PREPARE wider by dragging its right-hand gutter. Did any node in another region move?" | UX §3 |
| 5 | "Expand the logistic-regression Model, scroll its settings, change Regularization, then open it in focus mode (⤢ or F) and close it." | UX §9 |
| 6 | "Switch to 'Free canvas (comparison)' and repeat task 2." | UX §23 Q2 |
| 7 | "Set 'Illustrative state' to 'Runtime failure on Model'. What went wrong and what should you do?" | OV §19; D3.7 |
| 8 | "Keyboard only: trace the Split output and exit the trace. Tab to a rail value, press Enter, then Escape." | D3.9 |

| Question (exact wording) | Maps to |
|---|---|
| A. "Could you tell where information came from and goes without long wires?" | UX §23 question 1 |
| B. "Did the region view take less effort to read than the free canvas?" | UX §23 question 2 |
| C. "Anything confusing, missing or wrong?" | Open findings |

In P3-EP06, task 7 uses the editor's real failure path instead of the
illustrative state selector.

### Results (first prototype version)

The user performed the script on 2026-10-01, deliberately reading it as if
they had not helped design it. They wrote the UX direction, so this is not
a fresh-user test.

- **Task 1:** Correctly read the whole flow without hovering: data enters in
  DATA from a controlled CSV, goes to PREPARE (fill missing, then family
  size), then to VALIDATE / SPLIT, then to two models, two Evaluates, and a
  side-by-side Compare.
- **Tasks 2–3:** Answered, but the lines into the Evaluates were "a bit
  messed up" because one shared `split` input fanned out to two nodes.
- **Task 4:** Widening a region did not move other nodes.
- **Task 5:** Read the Model's settings correctly.
- **Task 6:** Found the Split connection, but the wire stretched across the
  screen and "makes you drag your gaze along that line"; not readable at a
  glance.
- **Task 7:** Identified an unencoded text column, but "Run failed" and the
  cause blended together.
- **Task 8:** "Didn't really work too great."
- **A:** Definitely preferred the gutters version.
- **B:** Yes, "by a lot". The user also suggested, as a hypothesis, that a
  vision-capable model might read regions more easily than wires; recorded
  as their observation, not tested.
- **C:** Covered by W1–W5.

| ID | Finding | Change |
|---|---|---|
| W1 | "to 1 region" is unclear; a bare `table` label would be ambiguous with several sources | `Name.port` values; outputs say "used by N nodes"; inputs say "from REGION" |
| W2 | One shared input fanning out tangled the lines | One Inputs entry per consuming port, level with that port |
| W3 | "Run failed" and the cause blend | Small "Run failed" label, then the cause as the bold headline |
| W4 | Expanding covered the node below | Temporary push-down that reverts |
| W5 | Keyboard was awkward; arrows should follow the graph | Graph navigation with arrows; M for move mode |

**Re-walk (L8):** the revised prototype has not been re-walked by the user.
It is carried explicitly to P3-EP06, whose fresh-user walkthrough uses this
script on the real editor and checks W1–W5. Recorded answers to UX §23 and
§24 above apply to the first version.

## 9. Worker self-assessment

| Criterion | Assessment |
|---|---|
| EP02-AC01 | Met. |
| EP02-AC02–AC04 | Met: per-candidate gate results with reasons, recomputed totals, per-criterion reasoning, primary sources, and a UX trace with deviations. |
| EP02-AC05 | Met: rails, identity matching by canonical ID and port, and connection feedback that never crosses a gutter. |
| EP02-AC06 | Met: controls from existing D1.4 fields only; fixed error text; no inspector; input separation; visible result. |
| EP02-AC07 | Met as a proposal: `DESIGN.md` v0.2 covers every decision record 0002 topic, now including explicit information hierarchy and control states; support mechanism chosen with license evidence for both alternatives. |
| EP02-AC08 | Met: measured AA targets at 100% and 1280×720; replacement lint candidate named. |
| EP02-AC09 | Met: exact script and questions mapped to UX sections. |
| EP02-AC10 | Met, with the re-walk carried to P3-EP06. |
| EP02-AC11–AC12 | See Section 10. |
| EP02-AC13–AC14 | Not self-assessed. |

## 10. Final attestation and scope

### Revision 1 (historical)

The first user-executed run passed `check`, `coverage`,
`deps:inventory`, `license:check`, and `deps:audit`; `git diff --check`
printed only line-ending warnings, but Git's pager cut off its exit code and
the following lines. The validator's own run of the same block was not
returned before its verdict. Both are superseded by the Revision 2 run.

### Revision 2

PENDING: the user-executed Windows run of the full sequence, using
`git --no-pager diff --check`, recorded exactly as the output shows.

## 11. Independent-validation handoff

PENDING completion of Section 10.

## 12. Response to the independent `Revise`

| Finding | Change |
|---|---|
| V1 (Medium) | `DESIGN.md` Section 4 adds connection feedback: compatible and incompatible port marking while connecting, refusal on drop, invalid connections on both rails in amber, and right-to-left dependencies via rails. The prototype shows both (screenshots 11 and 13); no wire crosses a gutter. |
| V2 (Medium) | Controls come only from existing D1.4 fields; integers step by 1 and numbers have no step restriction. No contract extension. |
| V3 (Medium) | Failure messages use only fixed text per F6 code; the column name was removed. Naming it is G-F8 for Central. |
| V4 (Medium) | Default zoom is 100%; gutters are 24 wide; rail text wraps; the top bar wraps at 1280×720 (screenshot 16). Measured: 24-pixel minimum targets, 10-pixel minimum text, no truncation, no overflow. Overview zooms are G-F9. |
| V5 (Medium) | Section 8 records the exact script and questions, mapped to UX sections. |
| V6 (Medium) | S8 records the frontend-design skill's license; the catalog option is Storybook (S9, MIT). |
| L1 | Per-candidate gate reasons and per-criterion reasoning added; D3.6 option C now fails G4 (UX §9.4), consistent with D3.5 and D3.7. Totals unchanged. |
| L2 | Reuse is "not shown in Phase 3". |
| L3 | UNASSIGNED placement and look, gutter maximum (900), and compact content per slice node are in `DESIGN.md`. |
| L4 | Rails are 96 in both; advanced booleans are checkboxes and enums are selects; "Unrelated" chips fit; the Family-size insertion is stated on the page. |
| L5 | Ports have accessible names; Shift+Right reaches every downstream node; trace dimming keeps contrast; the free-canvas bias is stated. |
| L6 | Naming rule and matching by canonical node ID and port key are in `DESIGN.md`; the prototype follows it (Model 1, Evaluate 1). |
| L7 | Replacement candidate jsx-a11y-x (S11) and the plugin's stalled ESLint 10 support (S10) are recorded. |
| L8 | Re-walk carried explicitly to P3-EP06. |
| L9 | `DESIGN.md` adds an information-hierarchy order and control states. |

No recommendation changed direction and no weighted total changed.
