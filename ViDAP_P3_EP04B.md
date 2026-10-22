# ViDAP P3-EP04B — Graph Authoring: Add, Remove, Connect, New, and Save As

| Field | Value |
|---|---|
| Status | Complete — accepted and reconciled in `ViDAP_P3_EP04B_Validation_and_Reconciliation.md` (2026-10-21) |
| Packet version | 0.1 |
| Packet type | Bounded implementation (web only, no backend change), with a `DESIGN.md` amendment approved as part of this packet |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1, WS3.4 |
| Parent roadmap | `ViDAP_Roadmap.md`, P3 and checkpoint A3 |
| Prerequisites | P3-EP04A complete (`ViDAP_P3_EP04A_Validation_and_Reconciliation.md`, accepted 2026-10-03) |
| Workstream | WS3.4 — Editor core (second of two packets) |
| Authorized worker report | `ViDAP_P3_EP04B_Implementation_Report.md` |
| Created | 2026-10-03 |
| Approved | 2026-10-03 by explicit user direction |
| Owner | Central |

---

## 1. Purpose

P3-EP04A made the browser an editor for **existing** workflows. P3-EP04B
lets a user **build** one. After this packet, a user can:

- start a new, empty workflow;
- add each slice node to its region;
- connect ports by pointer or keyboard, with typed feedback;
- disconnect and remove;
- validate, save under a name, and reopen.

That covers P3-AC02 up to the point of running, which P3-EP05 adds.

It also closes the items the P3-EP04A reconciliation carried here
(Section 5.6).

## 2. Authorization Boundary

Approval of this exact version authorizes one bounded worker to change only
the Section 8 paths. Windows steps may be run by the local agent at the
user's direction and are recorded as such.

Approval does **not** authorize:

- any Python or backend change, or any `/api/slice/` contract change;
- any new dependency, or any lock change;
- running workflows, results, or trace (P3-EP05);
- composite nodes, reroute points, align/tidy, or Regions / Free canvas views;
- a dark theme or a CI change;
- staging, committing, or pushing;
- starting P3-EP05.

## 3. Plain-English Packet Intent

**What it does.** A user clicks **New**, sees five empty regions, and uses
each region's **+ Add** button to place the slice's nodes. They connect an
output port to an input port by clicking one and then the other, or by
dragging, or entirely by keyboard. While connecting, the editor shows which
ports fit, using the port types from the backend contracts. The backend's
validation stays the authority on whether the workflow is valid. When the
workflow is complete, the user saves it under a name and can reopen it.

**Why it is needed.** Phase 3's main promise (P3-AC02) is that a fresh user
assembles the slice from an empty canvas. Without authoring, the editor can
only change workflows written by code.

**How success is demonstrated.**

- Component tests drive every authoring state against recorded backend responses.
- Tests prove the editor never decides validity itself.
- Tests prove that authoring changes only nodes and edges, and layout changes only the sidecar.
- The user builds the slice from an empty canvas on Windows, saves it, and reopens it.

## 4. Governing Inputs

The worker and validator must read:

- the explicit approval of this version;
- `ViDAP_P3_EP04A.md`, its implementation report, and its reconciliation, especially Section 4 (carried items);
- `DESIGN.md` v0.2 and the amendment in Section 6 of this packet;
- `UX refinement.txt` §§1–11, 18, 20, 23–24;
- `ViDAP_Phase_3_Plan.md` v1.1 §§5–10;
- `ViDAP_P3_EP03C.md` and its reconciliation (the channel contract);
- the Phase 1 validation rules in `python/src/vidap_workflow/validation.py`, **as evidence only**;
- decision records 0001 and 0002;
- `CONTRIBUTING.md`;
- this packet.

## 5. Approved Editor Contract

### 5.1 Facts this packet builds on (verified by Central)

- **IDs.** Workflow, node, and edge IDs must be lowercase UUIDv4 text. The editor creates them with `crypto.randomUUID()`.
- **Validation is complete and specific.** `POST /validate` already reports every connection problem, each with an `elementKind`:
  - type mismatch, reversed direction, unknown port, and dangling node, against the **edge** ID;
  - too many connections into a single input (`cardinality: "one"`) and a missing required input, against the **port** (`nodeId:portKey`);
  - a cycle, against the **workflow**;
  - duplicate edges, against the **edge**.

  The editor never computes any of these verdicts.
- **Contracts carry port metadata.** Each port has `nominalType`, `cardinality`, and `required`.
- **Save and load accept only valid workflows.** The accepted channel decodes through Phase 1 validation, and *any* finding refuses with `422 invalid-workflow` and its diagnostics. An empty workflow is valid and saves; a half-built one does not. This packet does not change that (see Section 10, Central note 1).
- **Names.** Saved names match `[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?`. The backend validates them; the editor shows the backend's message.

### 5.2 New workflow and Save as

- **New.** A **New** button in the top bar opens an empty, unsaved workflow:
  - `format`, `schemaVersion` "1.0", a new `workflowId`, no nodes, no edges;
  - the top bar shows "Untitled" with the unsaved indicator;
  - unsaved changes are confirmed first, as Open does.
- **Save as.** A **Save as…** button opens the same name field the conflict banner uses, in a banner.
  - It saves with `null` bases.
  - For an untitled workflow, **Save** opens Save as.
  - On success, the workflow takes the new name.
  - A name the backend refuses, or one that already exists, shows the backend's message, and the editor still holds the unsaved work.
- **Refused save.** A save refused as `invalid-workflow` keeps the work open and unsaved. It shows the backend's diagnostics in the same structure as validation ("Fix before saving" heading).

### 5.3 Adding and removing nodes

- **+ Add per region.** Each region header gets a **+ Add** button (24×24 or larger), named "Add node to MODEL".
  - It opens a small menu listing the contract types whose presentation region is that region. The labels are the contracts' display labels.
  - The menu is a menu button with arrow-key navigation and Escape.
  - It is shown even when it lists one type, so the choice is explicit.
  - UNASSIGNED has no Add.
- **What is added.**
  - A node with a new ID, the chosen type, and `parameters: {}`. Defaults come from the contract and are never copied in.
  - It is placed at `x = 16`, `y = 16` in an empty region, otherwise 24 px below the bottom of the lowest node in the region (by measured height).
  - Existing nodes never move. The region height grows as usual.
  - Focus moves to the new node, and the live region announces "Added Model 2 to MODEL." Naming and numbering follow `DESIGN.md` §4.
  - Validation is requested.
- **Remove.** On a focused node, the Delete key, or a **Remove node** button in the expanded node's Advanced section, opens a confirmation dialog:
  - "Remove Model 2? Its 2 connections are removed too."
  - Confirming removes the node and every edge touching it.
  - The sidecar entry is dropped at the next save (existing behavior).
  - Focus moves to the nearest node above in the region, or to the region's + Add.
  - The removal is announced, and validation is requested.

### 5.4 Connecting and disconnecting

- **Ports become controls.**
  - Each port is a button with at least a 24×24 hit area, while the glyph stays its current size.
  - It keeps its accessible name: "Output port model, type model".
  - Ports follow their node in the Tab order.
- **Starting.** A click, or Enter/Space, on an **output** port starts connecting:
  - a "Connecting from Model 1.model — choose an input port. Escape cancels." banner with a Cancel button;
  - the source port is marked;
  - every input port whose contract `nominalType` matches is outlined in accent;
  - every other input port is dimmed and shows ✕.

  This is the `DESIGN.md` §4 early feedback, from contracts only.
- **Completing.** A click, or Enter/Space, on a matching **input** port creates the edge with a new ID.
  - If that input's contract `cardinality` is `"one"` and it is already connected, the new edge **replaces** the existing one. The replacement is announced ("Replaced the connection from Model 1.model.").
  - An exact duplicate of an existing edge is not created ("Already connected.").
  - Validation is requested, and connecting ends.
- **Incompatible target.** Choosing a non-matching input creates nothing. The banner says why, using contract labels and types, for example "Evaluate's Split expects split, not model." Connecting continues.
- **Drag.** Pressing on an output port and releasing over an input port does the same as the two clicks. Releasing elsewhere leaves connecting active, as if the output had been clicked.
- **No in-progress wire.** Nothing is drawn between the source and the pointer, so nothing can cross a gutter. The banner, the marks, and the outlines are the feedback.
- **Cancelling.** Escape, the banner's Cancel, or starting from another output cancels or restarts.
- **Disconnecting.** The expanded node gets a **Connections** section. It lists each input port as "Split ← Train/Test Split.split", with a **Disconnect** button, or "not connected". Disconnecting removes that edge, is announced, and requests validation.
- **Keyboard parity (G-F2).** The flow is entirely Tab, Enter or Space, and Escape. Existing graph navigation (arrows on a node) is unchanged.

### 5.5 Showing connection problems (`DESIGN.md` §4)

- **Edge diagnostics.** A diagnostic whose `elementKind` is `edge` and whose reference is an edge ID marks that connection amber:
  - an amber Outputs entry on the producer's rail;
  - an amber Inputs entry, "⚠ not allowed here", on the consumer's rail;
  - short amber dashed local wires to each port;
  - the "Fix before running" message on the consumer node.

  The amber connection still never crosses a gutter.
- **Port diagnostics.** A diagnostic of kind `port` (`nodeId:portKey`), such as a missing required input or too many connections, shows on that node and marks the port amber.
- **Workflow diagnostics.** A diagnostic of kind `workflow`, such as a cycle, shows in the workspace banner, as P3-EP04A already does.
- **Direction.** A connection to an earlier region is drawn like any cross-region value: from the producer's Outputs rail to the consumer's Inputs rail. Whether it is valid is the backend's decision.

### 5.6 Items carried from P3-EP04A (reconciliation §4.2)

| Item | Required here |
|---|---|
| N5: summary lines wrap | Apply the `DESIGN.md` §10 reading in Section 6 of this packet. No code change |
| N2 and G-F3: an expanded node covers its own Outputs entry | **Expand toward open space.** While a node is expanded, if its expanded width would reach past its region's node area into the Outputs rail, display it shifted left by that overflow, but never left of the node area. This is temporary, like push-down: the stored position never changes. A region narrower than the expanded width still overlaps sideways, as before |
| Push-down moved a node that would not have overlapped | Push only by the **overlap actually needed**: a node below moves down just far enough to clear the grown node's displayed bottom plus 24 px, if it would otherwise be covered |
| Wires run beneath overlapping nodes | **Central decision: no change.** Wires stay beneath opaque nodes, so they never draw across node content. Local tangles are handled by the explicit tidy and reroute aids of UX §7, which are not in Phase 3's editor-core scope |
| Capture scripts not tracked | Add a tracked capture tool (Section 5.7) |
| Test cleanup | The worker may move `afterEach(cleanup)` into `apps/web/src/test/setup.ts`, and records whether it did |

### 5.7 Recorded responses and the capture tool

- **The tool.** `scripts/capture-editor-responses.mjs` is a Node script.
  - It uses `globalThis.fetch`; the lint config declares only `console` and `process`, and is not changed.
  - It runs against `npm.cmd run launch` and captures every response the editor tests replay.
  - It writes `apps/web/src/editor/test-data/recorded.ts` directly, formatted by the locked Prettier.
  - It prints the file's SHA-256 and size.
  - It saves only names starting with `capture-` under `.vidap-local/workflows/`, and restores or removes anything it changed.
- **New responses to capture:**
  - `validate` for an empty workflow;
  - `validate` with a missing required input (port kind);
  - `validate` with a type-mismatched edge (edge kind; the posted document is crafted by the script);
  - `validate` with a cycle (workflow kind), if the slice types allow one; otherwise the report says why not;
  - a refused `invalid-workflow` save;
  - a successful save of an empty workflow under a new name;
  - a save-as name conflict;
  - every EP04A response, re-captured.
- **Manifest.** `test-data/manifest.json` gets a new fixture version with the new hash. A test checks that the recorded shapes match the channel contract (extending the EP04A test).

## 6. Approved `DESIGN.md` Amendment (v0.3)

Approval of this packet approves these edits. The worker applies them as
written. Wording changes that the implementation proves necessary are listed
in the report for Central.

1. **Header:** Version 0.3. Add "P3-EP04B amendment (adding, removing, connecting nodes; new and save-as)".
2. **§3, after "Workspace":** "**Adding nodes:** each region header has a **+ Add** menu listing the node types that belong to that region (from the backend contracts and the region map). A new node is placed at the top of an empty region, or below the region's lowest node; existing nodes never move. There is no global node palette or catalog (UX §11)."
3. **§4, Connection feedback, replace the first bullet:** "**Connecting** starts from an output port (click, Enter or Space, or drag). A "Connecting" banner names the source and how to cancel; the source port is marked; every compatible input port is outlined in accent and every other input port is dimmed with ✕. Compatibility in this early feedback comes from the port types in the backend contracts; the backend's validation result is still the authority. Choosing a compatible input creates the connection; a single-connection input that is already connected has its connection replaced, and the replacement is announced. No in-progress line is drawn, so nothing crosses a gutter."
4. **§4, Connection feedback, add:** "**Disconnecting:** the expanded node lists each input port with its source and a Disconnect button."
5. **§5, Expanded, replace the last sentence:** "When it would overlap its region's Outputs rail, it is shown shifted left into open space for as long as it is expanded; its stored position never changes. A region narrower than the expanded node still overlaps sideways."
6. **§5, add:** "**Removing:** Delete on a focused node, or Remove node in its Advanced section, asks for confirmation (naming how many connections go with it), then removes the node and its connections."
7. **§5, Keyboard, add:** "Ports are in the Tab order after their node; Enter or Space on an output port starts connecting, on an input port completes it, and Escape cancels."
8. **§6, add a row:** "Save refused | Amber banner "Fix before saving" with the backend's diagnostics; the work stays open and unsaved."
9. **§9, replace "Connecting by keyboard is designed in P3-EP04, because…":** "Connecting is fully keyboard-operable (Section 5)."
10. **§10, replace the first bullet:** "Show at most one summary line of content per compact node; it may wrap and is never truncated."

## 7. Stop Conditions

Stop `Blocked` and name the requirement, evidence, and owner if:

- authoring would need a backend or contract change;
- the editor would need to decide validity, beyond the §4 type-match early feedback and the §5.4 cardinality replacement;
- a new dependency or lock change would be needed;
- the amendment in Section 6 cannot be implemented as written without a substantive design change;
- a mandatory check cannot be reproduced.

## 8. Exact Authorized Worker Outputs

| Path | Purpose |
|---|---|
| `apps/web/src/editor/**` | Editor source, styles, tests, recorded test data and manifest |
| `apps/web/src/test/setup.ts` | Test setup only (the Section 5.6 cleanup move, optional) |
| `scripts/capture-editor-responses.mjs` | New tracked capture tool (Section 5.7) |
| `DESIGN.md` | Exactly the Section 6 amendment, plus any listed clarification |
| `README.md`, `CONTRIBUTING.md` | Narrow current-state updates (authoring exists; how to regenerate recorded responses) |
| `ViDAP_P3_EP04B_Implementation_Report.md` | Worker evidence and handoff |

Not modified: Python, fixtures, `package.json`, the locks, `eslint.config.js`,
other scripts, CI, `docs/design/`, and the EP04A records.

## 9. Required Proof

Tests use Vitest, jsdom, and Testing Library against recorded responses
(Section 5.7). Any test must fail if the UI decides validity itself.

1. **New and Save as.**
   - New gives an empty, untitled, unsaved workflow with a fresh lowercase UUIDv4 `workflowId`.
   - Save on an untitled workflow opens Save as.
   - Save as posts `null` bases.
   - A refused name and a name conflict show the backend's message and keep the work.
   - A refused `invalid-workflow` save keeps the work and shows its diagnostics.
2. **Add.**
   - Each region's menu lists exactly the contract types mapped to it. Changing the stubbed contracts changes the menu.
   - An added node has a fresh ID and `parameters: {}`, and lands at the specified spot without moving any other node.
   - Focus and the announcement are correct, and naming and numbering are right.
3. **Remove.** The confirmation names the connection count. The node and its edges are removed; focus moves as specified; there is an announcement; and the next save drops its sidecar entry.
4. **Connect.**
   - Click-click, drag, and keyboard each create the same edge.
   - Compatible and incompatible marking comes from contract `nominalType`; changing a stubbed port type changes the marking.
   - An incompatible choice creates nothing and explains why.
   - A single-connection input replaces its edge, with an announcement; an exact duplicate is refused.
   - Escape cancels.
   - No element is drawn across a gutter at any point (extending the EP04A gutter test to the connecting state).
5. **Disconnect.** The Connections section lists inputs from the document; Disconnect removes exactly that edge.
6. **Problems.** Recorded edge-, port-, and workflow-kind diagnostics render as Section 5.5 specifies, with the backend's exact text.
7. **Carried items.**
   - Expand toward open space: the displayed shift, the unchanged stored position, and the narrow-region fallback.
   - The push-down overlap refinement: a tall compact node above a far node does not move it, while a covered node moves just enough.
8. **Isolation.**
   - Authoring changes only `nodes` and `edges`; the posted document keeps every other field and the number spellings.
   - Layout-only changes still post a byte-identical workflow (EP04A tests stay green).
9. **Capture.** The recorded data comes from the tracked tool's run on Windows. Its hash matches the manifest, and the shape test passes.
10. **User walkthrough (Windows, P3-AC02 without Run).** With `npm.cmd run launch` running, the user:
    - clicks New;
    - adds all five slice nodes;
    - connects all five slice connections, including the skip-region Split → Evaluate and the shared Split branch, using the mouse for some and the keyboard alone for at least one;
    - tries one incompatible connection and reads the explanation;
    - sees validation go from problems to valid;
    - tries a Save before it is complete (refused, with the reasons);
    - saves under a new name, reopens it, and removes and re-adds one node.

    The user reports what they saw. The report records it. The saved test workflow is deleted afterwards.

## 10. Central Notes

1. **Saving drafts.** Because the accepted channel saves only valid workflows, a user cannot save an unfinished workflow. This packet makes the refusal clear but does not change it. Draft saving would need a backend decision; Central will raise it at the P3-EP06 closeout if the walkthrough or validation shows it matters.
2. **Cardinality replacement** is editing convenience, not a validity verdict: the backend still validates the result. It is limited to inputs whose contract says `cardinality: "one"`.
3. **`deps:audit`.** Report exit 1 as the known finding accepted in `ViDAP_P3_EP04A_Validation_and_Reconciliation.md` §4.1 if, and only if, the npm findings are exactly that advisory and its 11 dependents and Python is clean. Anything else is new and stops for triage.

## 11. Worker Sequence and Final Attestation

1. **Baseline.** Confirm approval. Record the branch, `HEAD`, the dirty baseline by owner, and both lock hashes.
2. **Capture tool.** Write it, run it against the launched backend, and record the command, hash, and size.
3. **Build.** Implement Sections 5.2–5.6 and the Section 9 tests. Apply the Section 6 amendment.
4. **Walkthrough.** Section 9.10.
5. **Final checks**, on the final tree, in order:
   1. `npm.cmd run check`
   2. `npm.cmd run coverage`
   3. `npm.cmd run deps:inventory`
   4. `npm.cmd run license:check`
   5. `npm.cmd run deps:audit` (Section 10, note 3)
   6. `git --no-pager diff --check`
   7. the lock hashes
   8. the status and staged list
   9. no listeners on 8000 or 5173

   Any in-scope repair requires a complete rerun.
6. **Direct checks:**
   - the exact path scope;
   - the `DESIGN.md` §12 checklist for the authoring states;
   - LF line endings and final newlines;
   - no user paths or secrets;
   - the workflow store restored.
7. **Stop.** Write the report and stop. Do not stage, commit, push, validate, accept, or start P3-EP05.

## 12. Required Implementation Report

The report must cover:

- approval and baseline;
- the capture tool and its run;
- the module changes;
- the single-source table, extended for menus, port marking, and connection problems;
- the `DESIGN.md` amendment as applied, with any clarification;
- the evidence for each Section 9 item;
- the walkthrough;
- deviations;
- the full attestation;
- a validation handoff.

It must contain no user paths and no full logs.

## 13. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP04B-AC01 | Approval, prerequisites, baseline, and ownership are evidenced. |
| EP04B-AC02 | Only Section 8 paths change; there is no backend, contract, Python, fixture, dependency, or lock change. |
| EP04B-AC03 | New and Save as work as Section 5.2 specifies, with `null` bases, backend name checks, and refused saves that keep the work. |
| EP04B-AC04 | Adding offers only the contract types mapped to the region, adds `parameters: {}` with a fresh ID, and never moves an existing node; removal confirms and removes the node's edges. |
| EP04B-AC05 | Connecting works by click, drag, and keyboard alone; typed early feedback comes only from contracts; incompatible choices explain themselves; cardinality replacement and duplicate refusal behave as specified; nothing crosses a gutter. |
| EP04B-AC06 | Disconnecting works from the expanded node and by keyboard. |
| EP04B-AC07 | Edge, port, and workflow diagnostics render as Section 5.5 specifies, with the backend's exact text; the UI decides no verdict. |
| EP04B-AC08 | Authoring changes only nodes and edges; layout still never changes the posted workflow. |
| EP04B-AC09 | The Section 5.6 carried items are implemented or dispositioned as written. |
| EP04B-AC10 | The tracked capture tool reproduces the recorded responses; the manifest matches. |
| EP04B-AC11 | `DESIGN.md` v0.3 contains exactly the Section 6 amendment, plus any listed clarifications. |
| EP04B-AC12 | The full final attestation and the user walkthrough pass on Windows. |
| EP04B-AC13 | Fresh independent validation, including a visual review against `DESIGN.md` §12 at 100% and at 1280×720, returns `Accept`. |
| EP04B-AC14 | Central reconciles before P3-EP05 is drafted. |

## 14. Independent Validation

The validator reads the inputs, the delta, and the report. It runs the
editor against the real backend on its own copy and:

- builds the slice from an empty canvas by mouse and by keyboard;
- tries incompatible connections, replacements, duplicates, removal, a refused save, and name conflicts;
- checks the visuals against `DESIGN.md` §§2–7, 9, and 12 at 100% and at a real 1280×720 window;
- confirms that values and verdicts trace only to contracts and backend responses.

It returns `Accept`, `Revise`, or `Blocked`, without editing tracked files.

## 15. Handoff Prompts

### Worker

> Execute the approved `ViDAP_P3_EP04B.md` v0.1 as the bounded worker. Read every governing input, implement only the Section 8 paths, apply the Section 6 `DESIGN.md` amendment as written, build and run the tracked capture tool, complete the final attestation and the user walkthrough, and stop with `ViDAP_P3_EP04B_Implementation_Report.md` and a validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P3-EP05.

### Validator

> Act as the independent validator for `ViDAP_P3_EP04B.md` v0.1. Read the packet, its governing inputs, `DESIGN.md`, and the implementation report; run the editor against the real local backend and verify every acceptance criterion by mouse and keyboard, including building the slice from an empty canvas and a visual review against `DESIGN.md` §12 at 100% zoom and in a real 1280×720 window. Do not edit tracked files, accept for Central, or begin P3-EP05. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 16. Next Action

The user approved this version on 2026-10-03; obtain worker evidence. After
an independent `Accept` and Central reconciliation, P3-EP05 (run, results,
and trace) is drafted.
