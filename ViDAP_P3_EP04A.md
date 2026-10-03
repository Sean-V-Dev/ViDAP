# ViDAP P3-EP04A — Editor Workspace: Regions, Nodes, Layout, and Save/Load

| Field | Value |
|---|---|
| Status | Complete — accepted by Central 2026-10-03 (`ViDAP_P3_EP04A_Validation_and_Reconciliation.md`) |
| Packet version | 0.1 |
| Packet type | Bounded implementation: the first product UI (web only), no backend change |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1, WS3.4 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3/checkpoint A3 |
| Prerequisites | P3-EP02 complete (D3.4–D3.10, `DESIGN.md` v0.2 accepted); WS3.3 complete (P3-EP03A, P3-EP03B, P3-EP03C) |
| Workstream | WS3.4 — Editor core (first of two packets) |
| Authorized worker report | `ViDAP_P3_EP04A_Implementation_Report.md` |
| Created | 2026-10-02 |
| Approved | 2026-10-02 by explicit user direction |
| Owner | Central |

---

## 1. Why WS3.4 is split

WS3.4 covers the whole editor core: the canvas, regions, gutters,
contract-driven nodes, typed connections, validation feedback, and
save/load. That is too much for one validation cycle. There is also a design
gap: `DESIGN.md` does not say how a user **adds a node** to the canvas, and
P3-AC02 needs that to assemble the slice from an empty canvas. Central
therefore splits WS3.4 into two packets:

- **P3-EP04A (this packet): the editor workspace.** It covers:
  - the visual system and app shell;
  - regions, gutters, and boundary rails;
  - compact, expanded, and focused nodes, with contract-driven parameter
    controls;
  - keyboard navigation and move mode;
  - the `vidap.workspace-view` sidecar;
  - opening, validating, and saving an existing workflow, with conflict
    handling.
- **P3-EP04B (later): graph authoring.** It covers:
  - adding and removing nodes, including the `DESIGN.md` amendment that
    designs it;
  - connecting by pointer and by keyboard (G-F2);
  - connection feedback;
  - invalid and right-to-left connections on rails;
  - new and save-as workflows.

P3-EP05 (run, results, trace) and P3-EP06 (closeout) are unchanged.

## 2. Authorization Boundary

Approval of this exact version authorizes one bounded worker to change only
the Section 8 paths. All Windows steps run through the user, following the
`CONTRIBUTING.md` workaround.

Approval does **not** authorize:

- any Python or backend change, or any change to the `/api/slice/` contract;
- any new runtime dependency;
- a lock change, except the one conditional development dependency in
  Section 5.6;
- adding, removing, or connecting nodes;
- running workflows, or trace or X-ray views;
- browser end-to-end tests with a new tool;
- a dark theme or a CI change;
- staging, committing, or pushing;
- starting P3-EP04B.

## 3. Plain-English Packet Intent

**What it does.** The browser stops showing the Phase 0 placeholder and
becomes the ViDAP editor. The user can:

- open a saved slice workflow and see it laid out in its five regions;
- read each node at a glance and expand it to change its settings;
- see backend validation problems on the node;
- resize regions and move nodes, by mouse or by keyboard;
- save the result.

If the file changed outside the editor, the editor says so and never
overwrites it silently.

**Why it is needed.** This is the first time the design system becomes real
UI. Building the workspace before authoring keeps each review focused: this
packet proves the layout, nodes, accessibility, and persistence; P3-EP04B
proves how a graph is built.

**How success is demonstrated.**

- Component tests drive the editor through the representative states it
  owns.
- Tests prove every form and value comes only from the backend contract or
  the document.
- Tests prove layout changes never change the workflow's meaning.
- The user does a short walkthrough on Windows and confirms what they saw.

## 4. Governing Inputs

The worker and validator must read:

- the explicit approval of this version;
- `UX refinement.txt` §§1–10, 18, 20, 23–24;
- OV §§18–22A;
- `ViDAP_Phase_3_Plan.md` v1.1 §§5–8;
- **`DESIGN.md` v0.2**, Sections 2–7 and 9–12;
- `ViDAP_P3_EP02_Decision_Report.md` and its reconciliation, including:
  - D3.4–D3.10;
  - G-F1–G-F9;
  - N2–N5;
  - the results-dock reservation;
- `ViDAP_P3_EP01_Decision_Report.md`: D3.3, D3.4, V15, and V16;
- `ViDAP_P3_EP03C.md` and its reconciliation: the accepted channel contract;
- decision records 0001 and 0002;
- `docs/design/p3-ep02-prototype/`, as **evidence only**: never copied into
  the product;
- `CONTRIBUTING.md`;
- this packet.

**Central note (G-F6).** Decision record 0002 governs visual quality for
every Phase 3 UI packet. It is a governing input here; the next amendment to
the Phase 3 plan will list it formally.

## 5. Approved Editor Contract

### 5.1 Structure and data authority

- **Module layout.** The editor lives under `apps/web/src/editor/`, with
  small modules:
  - the API client;
  - the document model;
  - layout and the sidecar;
  - the presentation map;
  - components;
  - styles.

  `main.tsx` renders the editor in place of `FoundationRoot`. The foundation
  status component and its test may stay as an internal status check, or be
  removed only if `npm.cmd run smoke` does not depend on its text. Either
  way, the smoke harness itself is unchanged.
- **API client.** One client calls only the accepted `/api/slice/` endpoints
  and `/api/status`, with `Content-Type: application/json`. It treats every
  error as the fixed backend envelope: it shows the envelope's fixed
  `message`, and reads only its `code` and listed extra fields. It never
  parses or displays any other text.
- **Single sources (A3).** Each kind of value has exactly one source:

  | Value | Source |
  |---|---|
  | Node labels, descriptions, ports, port types | `GET /api/slice/contracts` |
  | Parameter kinds, defaults, bounds | `GET /api/slice/contracts` |
  | Validation verdicts | `POST /api/slice/validate` |
  | Saved documents | the backend |

  The UI copies no defaults, ranges, or validation rules into code; tests
  enforce this (Section 6).
- **UI-owned presentation.** One presentation module holds:
  - the map from node type to region (D3.4);
  - the region order and names;
  - the implementation-line text from `DESIGN.md` Section 5.

  It holds no parameter, default, or validation data. Unknown types fall into
  the UNASSIGNED region.
- **Values shown on nodes (N3).** Summary lines show only:
  - parameter values from the document, falling back to the contract
    default;
  - text from the contract description.

  The Dataset row and column counts are **not** in the contract, so they are
  omitted in this packet rather than hard-coded; the Dataset summary uses
  its contract description. Evaluate's accuracy shows "—" until P3-EP05.
  Nothing shows a value the backend did not supply.
- **Document handling (V16).**
  - The workflow document is kept as received.
  - Edits change only parameter values and node labels, and never remove
    other content.
  - Phase 1 `layout` metadata is round-tripped unchanged and never displayed
    (V16).
  - The sidecar is the only source of positions.

### 5.2 Rendering approach and the graph library

`@xyflow/react` 12.11.6 is already locked but unused. The worker must
compare three approaches:

- (a) one graph-library canvas with custom region, rail, and gutter layers;
- (b) a graph-library instance per region;
- (c) hand-built DOM and SVG, as in the prototype.

Each is judged against:

- `DESIGN.md` Sections 2–5 and 9;
- keyboard parity, including **turning off** the library's own arrow-key
  node moving in favour of graph navigation and move mode (G-F7);
- region-relative positions;
- "nothing crosses a gutter";
- maintainability.

The worker records a short comparison and builds the choice. No new
dependency is allowed. If (c) is chosen, `@xyflow/react` stays locked and
unused; removing it is a later dependency decision, not part of this packet.

### 5.3 Workspace (`DESIGN.md` Sections 2–4)

- **Tokens and top bar.**
  - Tokens are CSS custom properties exactly as in Section 2, light theme
    only.
  - The top bar holds the product name, the open workflow name with a
    saved/unsaved indicator, Open, Save, and the zoom control (100% default;
    85% and 70% as an overview).
  - A Run button is shown **disabled** with the reason "Run arrives in the
    next step"; P3-EP05 enables it.
  - At 1280×720 the top bar wraps rather than overflowing.
- **Regions.**
  - Five regions in order: DATA, PREPARE, VALIDATE / SPLIT, MODEL,
    EVALUATE / COMPARE.
  - Each region shows a header with its name and node count, an Inputs rail,
    and an Outputs rail.
  - The UNASSIGNED region appears only when it has nodes.
  - The empty canvas keeps all regions visible, with one hint in DATA.
- **Gutters.**
  - A gutter resizes the region to its left: by pointer drag, by arrow keys
    (Shift for larger steps), or by − and + buttons.
  - Each gutter has the `separator` role with its current value.
  - Width runs from "fits its nodes" to 900.
  - Resizing never moves nodes, because positions are region-relative.
- **Rails.**
  - Values are named `Name.port`, matched only by canonical node ID and port
    key.
  - There is one Outputs entry per value, level with its port, reading
    "used by N nodes". There is one Inputs entry per consuming port, level
    with its port, reading "from REGION".
  - Overlapping entries stack, and text wraps; it is never truncated.
  - On hover or keyboard focus, a value shows a card listing its producer and
    consumers.
  - Within a region, wires are short. **Nothing crosses a gutter.**
- **Results band.** The empty band below the regions stays reserved for the
  future results dock: no permanent UI is placed there.

### 5.4 Nodes (`DESIGN.md` Section 5)

- **Compact view.** Each node shows:
  - the kicker, title, implementation line, one summary line, and a "– Not
    run" chip;
  - ports on its edges, marked with type glyphs and given accessible names.
- **Expanded view.**
  - Opened by Enter, double-click, or the ▸ button.
  - The width is 290 and the body is bounded, with internal scroll that
    never pans or zooms the canvas.
  - Nodes directly below in the same region slide down while it is
    expanded, and slide back when it collapses. Stored positions never
    change.
  - Expanding toward open space (G-F3) is optional and is recorded if
    implemented.
- **Focus mode.** F or ⤢ opens a centered panel over a dimmed canvas.
  Escape or clicking the dimmed area closes it, and focus returns to the
  node.
- **Parameter controls.** Controls come **only** from D1.4 contract fields,
  mapped as in Section 5:
  - integer: step 1;
  - number: no step;
  - bounds from `minimum` and `maximum`;
  - labels and hints from the contract display fields.

  Changing a value updates the in-memory document, marks the workflow
  unsaved, and requests validation after a short pause. A value outside the
  bounds is still sent: the backend's verdict decides.
- **Validation feedback.** Diagnostics from `validate` appear on the
  affected node in the `DESIGN.md` Section 6 structure: an amber "Fix before
  running" label, the backend message, the remedy, and collapsed technical
  detail. The text is exactly what the backend returned. A problem not tied
  to a node appears in a workspace banner.
- **Input separation.** Each gesture does exactly one thing:
  - drag moves a node by its header only;
  - the body is for editing;
  - the wheel scrolls inside the body;
  - workspace scrollbars pan;
  - the zoom control zooms.

### 5.5 Keyboard, focus, and announcements (`DESIGN.md` Sections 5 and 9)

- **Tab order.** Tab reaches the top bar, nodes, rail values, gutters, and
  controls.
- **Graph navigation (on a node).**
  - Right goes to the first downstream node, nearest region first, and
    announces the count.
  - Shift+Right goes to the next downstream node.
  - Left goes to the node that feeds this one.
  - Up and Down move within a region.
- **Node actions.** Enter expands, F opens focus mode, and M enters move
  mode: arrows move the node (Shift for larger steps), and Enter or Escape
  ends it.
- **Library keys.** The graph library's own arrow-key moving, if a library
  is used, is disabled.
- **Focus visibility.** Focus is always visible as a 2-pixel accent ring
  with a 2-pixel offset, and is never fully hidden.
- **Live region.** One polite live region announces:
  - navigation counts;
  - validation changes;
  - save results;
  - conflicts.
- **Targets and motion.** Every target is at least 24×24 at 100% zoom.
  Motion is disabled under reduced-motion preferences.

### 5.6 Accessibility lint (G-F1, N5)

The worker rechecks `eslint-plugin-jsx-a11y-x` against **primary registry
metadata** before any install:

- the latest version;
- the ESLint 10 peer range, against the locked `eslint` 10.10.0;
- the license;
- maintenance;
- its transitive packages.

- **If it passes,** the worker gives the user the Windows commands to add it
  as an exact-pinned development dependency. The user's
  `deps:inventory`/`license:check`/`deps:audit` run must pass. The
  recommended rules are enabled for `apps/web/src`, and any findings in this
  packet's code are fixed.
- **If it does not pass,** for any reason (a peer mismatch, a license that
  needs review, or an inactive project), nothing is installed, and the
  report records the evidence for Central's decision record 0001 follow-up.
  Either outcome is acceptable. Forcing peers or using another linter is
  not.

### 5.7 Open, save, sidecar, and conflicts (D3.3, D3.4, V15)

- **Open.** Open lists `GET /api/slice/workflows` and loads one. A refused
  load shows its backend message and diagnostics, and the current workspace
  is unchanged.
- **Sidecar.**
  - A loaded sidecar sets region widths, node positions, and the viewport.
  - With no sidecar, or a `sidecarNotice`, the editor uses deterministic
    default placement and says so in a banner.
  - Entries for unknown node IDs are ignored and dropped at the next save.
- **Save.** Save sends the document, the sidecar, and **both base digests**
  from the last load or save.
- **Conflict.** A `409 conflict` shows the amber conflict banner with the
  backend's change summary, rendered as plain text from its fields, and
  two actions:
  - **Reload from disk:** this discards local changes after a confirmation
    dialog.
  - **Save under a new name:** a name field validated by the backend, saved
    with `null` bases.
- **Compare.** When the window regains focus, the editor calls `compare` and
  shows the same banner if the files changed.
- **Unsaved changes.** The unsaved indicator and the browser's leave-page
  prompt protect unsaved edits.
- **Presentation isolation (P3-AC08).** Moving, resizing, expanding, and
  zooming change only the sidecar. Tests prove the posted workflow document
  is byte-identical before and after.

## 6. Required Proof

The tests use Vitest, jsdom, and Testing Library, all already locked. They
work against a stubbed client that returns **recorded responses captured
from the real backend contract**. Any test must fail if the UI computes a
default, range, or validation verdict itself.

1. **Contract-driven controls.**
   - Change a recorded contract's default, bounds, or label in the stub, and
     the form follows it.
   - No parameter metadata literal appears in the editor source (a static
     check over the source).
2. **Regions and rails.**
   - The five-region slice renders every node in its region.
   - Split's value appears once on VALIDATE / SPLIT's Outputs rail ("used by
     2 nodes") and once on each consuming port's Inputs rail.
   - The skip-region value never produces a wire element across a gutter.
   - The UNASSIGNED region appears only for an unknown type.
   - Names follow `DESIGN.md` naming, including numbering for duplicate
     types.
3. **Gutters.** Resizing by pointer, keyboard, and buttons changes the
   region width within its bounds, does not change any node's stored
   position, and is reflected in the `separator` value.
4. **Nodes.**
   - Compact content matches Section 5.4.
   - Expanded nodes push down the nodes below in the same region and
     restore them on collapse; stored positions are unchanged.
   - Focus mode opens and closes and returns focus.
   - The body scroll does not change the workspace scroll.
5. **Keyboard.** Right, Shift+Right, Left, Up, and Down follow the graph as
   specified, with the correct live announcements. Move mode moves a node
   and ends on Enter or Escape. The library's arrow-key moving is disabled.
   Every control has an accessible name, and the Tab order is logical.
6. **Validation feedback.** An out-of-range `regularization` produces the
   backend diagnostic on Model, exactly as recorded. Fixing it clears the
   message. A diagnostic not tied to a node shows in the banner.
7. **Save, load, and conflicts.**
   - Save posts both base digests.
   - A recorded `409` shows the summary and both actions.
   - Reload asks for confirmation.
   - Save under a new name uses `null` bases.
   - `compare` runs when the window regains focus.
   - A load with a sidecar notice falls back to default placement.
   - Phase 1 layout metadata round-trips unchanged.
8. **Presentation isolation.** After moving, resizing, expanding, and
   zooming, the posted workflow is identical to the loaded one.
9. **Contract fixtures.** The recorded backend responses used by the stub
   are captured from the real backend: the user runs a worker-provided
   command against `npm.cmd run launch`. They are committed under
   `apps/web/src/editor/test-data/` (D0.7 metadata in a small manifest),
   and a test checks that their shape matches the channel contract.
10. **User walkthrough (Windows).** With `npm.cmd run launch` running and
    the success fixture saved through the channel (a worker-provided
    command), the user:
    - opens the workflow;
    - Tabs to Model and expands it;
    - sets `regularization` to 0, sees the amber message, and sets it back;
    - resizes a gutter;
    - moves a node with M and the arrows;
    - saves;
    - edits the saved file outside the editor;
    - returns to the window and sees the conflict banner;
    - reloads.

    The user reports what they saw and may attach screenshots. This is
    walkthrough evidence, not the P3-EP06 fresh-user test.

## 7. Stop Conditions

Stop `Blocked` and name the requirement, evidence, and owner if:

- the editor would need a backend or contract change;
- it would need a new runtime dependency;
- it would need to compute a default, range, or validation verdict in the
  UI;
- Section 5.2 shows that no approach can meet "nothing crosses a gutter"
  with keyboard parity;
- a mandatory check cannot be reproduced.

## 8. Exact Authorized Worker Outputs

| Path | Purpose |
|---|---|
| `apps/web/src/main.tsx` | Render the editor |
| `apps/web/index.html` | Title only |
| `apps/web/src/foundation-root.tsx`, `apps/web/src/foundation-root.test.tsx` | Keep, adjust, or remove (Section 5.1) |
| `apps/web/src/editor/**` | Editor source, styles, tests, recorded test data and its manifest |
| `apps/web/src/test/setup.ts` | Test setup additions only, if needed |
| `eslint.config.js` | Only to enable jsx-a11y-x rules (Section 5.6) |
| `package.json`, `package-lock.json` | Only the Section 5.6 dev dependency, if adopted; changed by the user's Windows commands |
| `DESIGN.md` | Status line to Accepted (per the P3-EP02 reconciliation), the N2 wording fix, and **only** clarifications the implementation proves necessary, each listed in the report for Central |
| `README.md`, `CONTRIBUTING.md` | Narrow current-state updates |
| `ViDAP_P3_EP04A_Implementation_Report.md` | Worker evidence and handoff |

The prototype under `docs/design/` is not modified. Neither are Python
files, fixtures, CI, scripts, or `python/uv.lock`.

## 9. Worker Sequence and Final Attestation

1. **Baseline.** Confirm approval. Record the branch, `HEAD`, the dirty
   baseline by owner, and both lock hashes.
2. **Section 5.2 comparison.** Write the comparison, then build the chosen
   approach.
3. **Lint (Section 5.6).** Run the registry check. If the plugin passes,
   give the user the install commands and record the lock delta.
4. **Build.** Implement Sections 5.1–5.7 and the Section 6 tests. Capture
   the recorded responses with the user's run.
5. **Final checks.** On the final tree the user runs, in order:
   1. `npm.cmd run check`
   2. `npm.cmd run coverage`
   3. `npm.cmd run deps:inventory`
   4. `npm.cmd run license:check`
   5. `npm.cmd run deps:audit`
   6. `git --no-pager diff --check`
   7. the lock hashes
   8. the status and staged list
   9. the Section 6.10 walkthrough

   Any in-scope repair requires a complete rerun.
6. **Direct checks.** Check:
   - the exact path scope;
   - the `DESIGN.md` Section 12 checklist against the states this packet
     touches;
   - line endings, whitespace, and final newlines;
   - that there are no user paths or secrets;
   - that no listener remains after the walkthrough.
7. **Stop.** Write the report and stop. Do not stage, commit, push,
   validate, accept, or start P3-EP04B.

## 10. Required Implementation Report

The report must cover:

- approval and baseline;
- the Section 5.2 comparison and choice;
- the lint evaluation and outcome;
- the module map;
- the single-source table, showing where each displayed value comes from;
- the presentation map;
- `DESIGN.md` changes and any proposed clarifications;
- the evidence for each Section 6 item;
- the walkthrough report;
- the full attestation;
- a validation handoff.

It must contain no user paths and no full logs.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP04A-AC01 | Approval, prerequisites, baseline, and ownership are evidenced. |
| EP04A-AC02 | Only Section 8 paths change; there is no backend, contract, Python, or fixture change; any lock change is exactly the Section 5.6 dependency. |
| EP04A-AC03 | Every displayed contract value and form control comes from `GET contracts`; every verdict comes from `validate`; no defaults, ranges, or rules are copied into the UI. |
| EP04A-AC04 | Regions, rails, naming, gutters, and the UNASSIGNED region match `DESIGN.md` Sections 3–4; nothing crosses a gutter. |
| EP04A-AC05 | Compact, expanded (with push-down), and focus states match Section 5; input separation holds. |
| EP04A-AC06 | Keyboard parity: navigation, move mode, expand, focus, gutters, save, and open; visible focus; live announcements; the library's arrow-key moving is disabled. |
| EP04A-AC07 | Validation diagnostics appear on the node with the backend's exact text and the Section 6 structure. |
| EP04A-AC08 | Save and load use both base digests; conflicts show the backend summary and both actions; nothing is silently overwritten; sidecar degradation works; V16 holds. |
| EP04A-AC09 | Layout and presentation changes never change the posted workflow (P3-AC08). |
| EP04A-AC10 | The jsx-a11y-x evaluation is recorded and either adopted cleanly through D0.6 or declined with evidence. |
| EP04A-AC11 | The top bar and workspace meet the 1280×720 and 100%-zoom rules; the results band stays empty. |
| EP04A-AC12 | The full final attestation and the user walkthrough pass on Windows. |
| EP04A-AC13 | Fresh independent validation, including a visual review against `DESIGN.md` Section 12, returns `Accept`. |
| EP04A-AC14 | Central reconciles before P3-EP04B is drafted. |

## 12. Independent Validation

The validator reads the inputs, the delta, and the report. It runs the
editor against the real backend on its own copy and drives every state
above by mouse and keyboard. It checks:

- the visuals against `DESIGN.md` Sections 2–7, 9, and 12, at 100% zoom and
  at 1280×720;
- that values trace to contracts and recorded responses only;
- that layout never changes the document;
- the conflict flows, using outside edits.

It returns `Accept`, `Revise`, or `Blocked`, without editing tracked files.

## 13. Handoff Prompts

### Worker

> Execute the approved `ViDAP_P3_EP04A.md` v0.1 as the bounded worker. Read every governing input including `DESIGN.md`, follow the `CONTRIBUTING.md` workaround for all Windows steps, implement only the Section 8 paths, complete the final attestation and the user walkthrough, and stop with `ViDAP_P3_EP04A_Implementation_Report.md` and a validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P3-EP04B.

### Validator

> Act as the independent validator for `ViDAP_P3_EP04A.md` v0.1. Read the packet, its governing inputs, `DESIGN.md`, and the implementation report; run the editor against the real local backend and verify every acceptance criterion by mouse and keyboard, including a visual review against `DESIGN.md` Section 12. Do not edit tracked files, accept for Central, or begin P3-EP04B. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

The user approved this version on 2026-10-02; obtain worker evidence. After an independent
`Accept` and Central reconciliation, draft P3-EP04B (graph authoring).
