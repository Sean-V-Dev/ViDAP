# ViDAP P3-EP04A — Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP04A.md` v0.1, explicitly approved by the user 2026-10-02 |
| Worker execution | 2026-10-02. Build in Linux shells over the Windows checkout (ViDAP Central session), with every Windows step run by the user under the `CONTRIBUTING.md` workaround. Then handed off to a local Claude Code session on the user's Windows machine, which ran the walkthrough support, the repairs, and the final attestation in Windows PowerShell at the user's direction (Section 12) |
| Revision | 2, 2026-10-03, responding to the independent `Revise` (Section 17) |
| Worker result | Revision 2 complete. Final attestation passed on a complete Windows rerun (Section 12) except `deps:audit`, which reports a newly published advisory in a locked development-tool chain. The lock is unchanged and the packet forbids a lock change (Section 11.1). That item needs Central triage. Ready for re-validation |
| Independent validation | Revision 1 returned `Revise` (R1–R5 blocking; N1–N6 lower severity). Revision 2 awaits re-validation; this report is not a verdict |
| Central decision | Pending |

## 1. Approval and baseline

- Packet v0.1 approved by the user on 2026-10-02 (packet header). Prerequisites: P3-EP02 accepted, with `DESIGN.md` v0.2 accepted in `ViDAP_P3_EP02_Validation_and_Reconciliation.md`. P3-EP03A, P3-EP03B, and P3-EP03C accepted and reconciled.
- Branch `main`, `HEAD` `17652fc`, nothing staged.
- Lock hashes: `package-lock.json` `FB7119F6…82FA`, `python/uv.lock` `8030A7C4…0A25`. Both are unchanged from P3-EP03C and unchanged at the end (Section 12).
- Dirty baseline, by owner:
  - **Accepted, uncommitted P3-EP03A–C work:** the Python slice and channel modules and tests, `fixtures/p3-ep03b/`, the dependency-control script and doc edits, `python/pyproject.toml` and `python/uv.lock`, decision record 0005, and the P3-EP03A–C packets, reports, and reconciliations.
  - **Central records:** `ViDAP_P3_EP04A.md`, plan and roadmap approval edits, `.gitattributes`, and `.gitignore`.
  - **Earlier dirty-baseline edits:** `README.md`, `CONTRIBUTING.md`, and `DESIGN.md` were already dirty. This packet adds only the narrow edits listed in Sections 7 and 13.
- The user commits; no agent staged, committed, or pushed.

## 2. Section 5.2 rendering comparison and choice

| Criterion | (a) One library canvas plus custom layers | (b) A library instance per region | (c) Hand-built DOM and SVG |
|---|---|---|---|
| `DESIGN.md` 2–5, 9 (regions, rails, gutters as first-class layout) | Regions, rails, and gutters become overlays fighting the library's single pan/zoom space | Regions are natural, but each instance has its own viewport, zoom, and focus model to keep in sync | Regions are plain flex columns; rails and gutters are ordinary elements |
| Keyboard parity (G-F7: library arrow-moving off; graph navigation; move mode) | Must disable built-in key handling and re-implement navigation across the canvas | Same, multiplied by five instances; cross-region navigation spans instances | Owned outright: one key handler per node, with no library keys to disable |
| Region-relative positions | Positions are canvas-global; region-relative needs a translation layer that resizing must update | Region-relative by construction | Region-relative by construction (`left = RAIL_WIDTH + x`) |
| "Nothing crosses a gutter" | Library edges are drawn in one SVG over everything, so edges must be suppressed and replaced | Cross-region edges cannot be drawn by any instance, which is the right result | Each region draws only its own wires in its own clipped SVG; cross-region values go through rails |
| Maintainability | Most code fights the library | Five synchronized instances | Smallest surface; no library upgrade risk |

**Choice: (c).** `@xyflow/react` 12.11.6 stays locked and unused. Removing it
is a later dependency decision. No dependency was added. "Nothing crosses a
gutter" is enforced by construction, and tested (Section 8, item 2).

## 3. Section 5.6 accessibility lint evaluation

Primary registry metadata for `eslint-plugin-jsx-a11y-x`:

- latest version 0.2.0, MIT;
- peer `eslint ^9 || ^10`, compatible with the locked 10.10.0;
- published 2026-05-10;
- depends on `axe-core ^4.10.2`, whose current 4.13.0 is **MPL-2.0**. That license is review-required under D0.6.

**Outcome: declined; nothing installed.** `eslint.config.js`, `package.json`,
and the lock are unchanged. The evidence goes to Central for the decision
record 0001 follow-up.

## 4. Module map (`apps/web/src/editor/`)

| Module | Role |
|---|---|
| `api.ts` | The only `/api/slice/` client: types, `ApiError` (fixed envelope: `message`, `code`, and listed extras only), `createSliceClient`, and number-spelling preservation (Section 11.2) |
| `model.ts` | Pure document and contract views: display names, effective values, boundary entries, graph navigation, `withParameter` |
| `layout.ts` | Geometry constants, the sidecar in and out, width and position clamping, push-down, and rail stacking |
| `presentation.ts` | UI-owned presentation only (Section 6) |
| `Editor.tsx` | Shell: top bar, banners, open/save/compare, keyboard, move mode, the live region |
| `Workspace.tsx` | Regions, rails, wires, gutters |
| `NodeView.tsx` | Compact, expanded, and focus node; contract-driven fields; diagnostics |
| `ConfirmDialog.tsx` | Confirmation `alertdialog` |
| `editor.css` | Tokens and styles, light theme only |
| `test-data/recorded.ts`, `test-data/manifest.json` | Recorded backend responses and D0.7 metadata |
| `*.test.ts(x)` | Section 8 |

`main.tsx` renders `<Editor client={createSliceClient()} />`, and
`index.html`'s title is "ViDAP". `foundation-root.tsx` and its test are kept
unchanged as an internal status check. The smoke harness is unchanged.

## 5. Single-source table

| Displayed value | Source | Enforced by |
|---|---|---|
| Node type label, description, ports, port types | `GET /api/slice/contracts` | `contract-source.test.ts` (no copied literals); editor test "builds every setting from the contract" |
| Parameter label, hint, kind, step, min/max, allowed values, default | `GET /api/slice/contracts` | Same; changing the stubbed contract changes the form |
| Parameter values on nodes | The document, falling back to the contract default | `model.test.ts` "takes effective values…" |
| Validation verdicts, messages, remedies, technical detail | `POST /api/slice/validate` | Editor tests: the exact backend message, on the node and in the workspace banner |
| Saved documents, digests, the change summary | Load, save, and compare responses | Editor conflict and compare tests |
| Dataset row and column counts | Not supplied by the backend, so **omitted** | Section 11.3, deviation 3 |
| Evaluate accuracy | Shows "—" until P3-EP05 | Compact node test |

## 6. Presentation map (`presentation.ts`)

- **Region order and names:** DATA, PREPARE, VALIDATE / SPLIT, MODEL, EVALUATE / COMPARE. Unknown types go to UNASSIGNED ("UNASSIGNED · type has no region"), which appears only when it has nodes.
- **Type to region:** `vidap.slice.dataset`→DATA, `.prepare`→PREPARE, `.split`→VALIDATE_SPLIT, `.model`→MODEL, `.evaluate`→EVALUATE_COMPARE.
- **Implementation lines (`DESIGN.md` Section 5):** Controlled CSV; Fill missing · Encode categories; Single holdout; Logistic regression; Accuracy on test rows.
- **Result summary label:** Evaluate shows "Accuracy".
- No parameter, default, range, or validation data lives here.

## 7. `DESIGN.md` changes and proposed clarifications

Changes, each for Central:

1. The status line is set to **Accepted**, as the P3-EP02 reconciliation directed.
2. The N2 dim-fill row is reworded: "text keeps ≥ 4.68:1 (primary text 14.5:1); the dimmed border is about 1.5:1, see Section 9".
3. Section 9's dimmed-border sentence defers the 3:1 question to P3-EP05.

Proposed clarifications, not applied:

- "Double-click" expands a node from anywhere except its form controls and its expanded settings body. The body is excluded so that selecting text cannot collapse the node (Section 10, F4).
- Moving a node never resizes its region; the gutter does that (Section 10, F1).

## 8. Evidence for each Section 6 item

Tests run under Vitest, jsdom, and Testing Library against a stubbed client
that replays the recorded responses. There are 40 editor tests in 5 files
(Section 13 lists them).

| Item | Evidence |
|---|---|
| 1. Contract-driven controls | Editor test "builds every setting from the contract, including changed bounds and labels" (the stubbed contract's label, hint, and bounds change, and the form follows). `contract-source.test.ts` "copies no parameter key, default, or bound…" (a static scan of editor source) |
| 2. Regions and rails | "lays out the slice in its five regions…"; "shows each boundary value once on Outputs and once per consuming port" ("used by 2 nodes", the hover card, no skip-region entry on MODEL); "never draws a wire outside its own region"; `model.test.ts` covers UNASSIGNED and naming with numbering for duplicate types |
| 3. Gutters | "resizes regions by keyboard and buttons without moving any node" (the `separator` value, the bounds, Home); "focuses a gutter when it is pressed…" (pointer). Pointer resizing was also walked by the user |
| 4. Nodes | "lays out…" (compact content and Not run chips); "expands in place, pushes down nodes below, and restores them"; "opens and closes focus mode and returns focus to the node"; "toggles a node by double-click…". **Body scroll:** CSS `overscroll-behavior: contain` on the bounded body, plus wheel `stopPropagation`. jsdom has no layout, so the validator should confirm this in a browser |
| 5. Keyboard | "follows the graph by keyboard and announces where it goes" (Right, Shift+Right, Left, with announcements); `model.test.ts` covers Up/Down neighbours; "moves a node in move mode…" (M, the arrows, Shift, Enter); "keeps the Phase 1 layout metadata…" (Escape ends it); "ends move mode when focus leaves the node"; "orders each region for Tab as Inputs, nodes, then Outputs". There is no library, so there are no library keys to disable |
| 6. Validation feedback | "shows the backend's exact validation message on the node, then clears it"; "shows a problem not tied to a node in the workspace banner"; "does not send text that is not a number" |
| 7. Save, load, conflicts | "moves a node…" (save posts both base digests); "refuses to overwrite…" (409 summary, both actions, reload confirmation, save-as with `null` bases); "checks for outside changes when the window regains focus" (also asserts the clean-state wording and confirmation); "falls back to default placement when the saved layout is unreadable"; "keeps the Phase 1 layout metadata untouched when saving"; "reports a refused load…" |
| 8. Presentation isolation | "moves a node in move mode and saves only the layout": after a move, zoom, expand, and resize, the posted workflow equals the loaded one byte for byte. `api.test.ts` proves byte identity for validate, compare, and save bodies (Section 11.2). Confirmed on Windows: a layout-only save left `capture-example.vidap.json` byte-identical (`DB55A163…` before and after) |
| 9. Contract fixtures | `test-data/recorded.ts` (12 responses captured from the real backend on Windows) and `manifest.json` (D0.7); `contract-source.test.ts` "matches the recorded responses to the channel contract". Capture is described in Section 14 |
| 10. User walkthrough | Section 9 |

## 9. Walkthrough report (Section 6.10, Windows)

`npm.cmd run launch` was started by the local Claude Code session. The user
drove the browser and reported what they saw, with screenshots.
`capture-example` had been saved through the channel by the capture command
(Section 14).

| Step | What the user saw |
|---|---|
| Open | Opened `capture-example` with Open…; five regions, no errors. The look differs from the P3-EP02 prototype (expected: this follows the accepted `DESIGN.md`) |
| Tab to Model, Enter | Model expanded, showing its description, Regularization 1 with its hint, and Advanced (type, node ID). About 26 Tabs from a blank area. The output entry was reached before the node (finding F5) |
| Regularization 0, then back | Amber "Fix before running", "Parameter 'regularization' is below the minimum.", "Use a value within the declared numeric range.", and expandable technical details (constraint violation). Setting it back to 1 cleared it |
| Resize a gutter | −/+, dragging, and arrow keys after Tab all worked. Narrowing stopped before clipping a node, and other regions' nodes stayed put. Clicking the grip did not focus it (F2) |
| Move with M and arrows | Dashed outline; small and Shift steps; ended cleanly with Escape. M after clicking the header did nothing (F2); the outline stayed after clicking away (F3); a node could be dragged past the region's right edge (F1) |
| Save | "Saved" in the top bar. Workflow file byte-identical (`DB55A163…`); the sidecar changed. Discarding an unsaved move by reopening restored the saved position exactly |
| Outside edit | Regularization changed to 0.5 in Notepad |
| Return to window | Amber banner: "capture-example changed outside the editor.", "Model · regularization: yours 1, on disk 0.5", Reload from disk, New name, and Save under new name (disabled until a name is entered). It also said "Your changes have not been saved" with nothing unsaved (F6) |
| Reload | Confirmation, then discard. Regularization showed 0.5; the saved layout was kept |

After the app stopped, there were no listeners on 8000 or 5173. A second walk
after the repairs confirmed F1–F6 (Section 10), and the user restored the
file to its original bytes (`DB55A163…`).

## 10. Repairs after the walkthrough (in scope, user-approved)

| ID | Defect against | Repair | Proof |
|---|---|---|---|
| F1 | `DESIGN.md` §4 ("width … fits its nodes"): drag and move mode clamped only left and top | `layout.clampPosition`: a move stops where the region still fits the node; moving never resizes the region | `layout.test.ts` "keeps a moved node inside its region…"; editor test "…by pointer and by keyboard"; re-walk: drag stops at the Outputs rail, and down still grows the region |
| F2 | §5.5 keyboard parity: header and grip `pointerdown` called `preventDefault`, which blocked focus | Focus the node or grip (`preventScroll`) on pointer-down | Editor tests (header to node focus; grip focus); re-walk: header then M, and grip then arrows, both work |
| F3 | Move mode outline outlived move mode after clicking away | End move mode on focus leaving the node, and announce "Move finished." | "ends move mode when focus leaves the node"; re-walk |
| F4 | §5.4 "Opened by Enter, double-click, or ▸": double-click worked only on the header | Double-click on the node toggles it, except on form controls and the expanded settings body | "toggles a node by double-click…"; re-walk |
| F5 | §6.5 "the Tab order is logical": Outputs rail preceded the nodes in DOM order | The Outputs rail is rendered after the nodes: Inputs, node, Outputs | "orders each region for Tab…"; re-walk |
| F6 | Conflict banner claimed unsaved changes when there were none | Banner sentence only when there are unsaved changes; the reload confirmation (still always shown, §6.7) says "Discard and reload" only when something will be discarded, otherwise "Reload" | Conflict and compare tests assert both wordings; re-walk confirmed the banner wording |

**Test isolation fix.** The repository's Vitest config does not enable
globals, so Testing Library never registered its automatic cleanup. Under
`npm.cmd run check`, every editor test after the first failed with duplicate
elements. The earlier cloud runs had passed, apparently with a different
configuration. `editor.test.tsx` now calls `afterEach(cleanup)` explicitly.
No config change was made.

**A correction made by the worker.** One intermediate F6 version skipped the
reload confirmation when nothing was unsaved, and the user's re-walk saw that
version. It was reverted before the final attestation because §5.7 and §6.7
require the confirmation. The final behavior is in the table and is covered
by the compare test. The user has not re-walked the final reload dialog
wording (Section 15).

## 11. Findings, deviations, and notes for Central

### 11.1 `deps:audit`: newly published advisory (needs Central triage)

`npm audit` reports 11 high advisories, all from one root:
[GHSA-ch52-4w7c-c8xp](https://github.com/advisories/GHSA-ch52-4w7c-c8xp)
in `http-cache-semantics` 4.2.0.

- **Path:** `license-checker-rseidelsohn@5.0.1` › `@npmcli/arborist@9.6.0` › `npm-registry-fetch@19.1.1` › `make-fetch-happen@15.0.6` › `http-cache-semantics@4.2.0`.
- **Scope:** development-only (the license-check tool); nothing in the shipped web bundle or Python runtime.
- **No fix available:** 4.2.0 is the latest published version.
- **npm's suggested fix is unusable:** a semver-major change to `license-checker-rseidelsohn` 4.4.2, which would rewrite the lock.
- **Lock unchanged:** P3-EP03C recorded 0 vulnerabilities on the identical lock (432 packages), so the advisory was published since then. It is not caused by this packet.
- **Python:** "No known vulnerabilities found".

Under `docs/dependency-controls.md`, a high finding needs triage within five
business days, and an unresolved reachable high blocks merge or release
unless Central records a time-bounded mitigation. Reachability is limited to
`license:check` runs. The worker cannot change the lock. **Requested:** a
Central triage or mitigation record, or direction.

### 11.2 Number spelling (EP04A-AC09 / P3-AC08, D3.3)

Browsers parse `1.0` and `1` to the same number, so an unchanged
`"regularization": 1.0` was re-serialized as `1`. That changed the backend's
semantic digest and the workflow identity. `api.ts` now:

- records each loaded number whose spelling differs from the browser's;
- writes the number back with that spelling while the value is unchanged;
- writes user-changed numbers plainly.

`api.test.ts` proves byte identity, and the Windows walkthrough confirmed it
(`DB55A163…` unchanged after a 0 → 1 round trip and save). **Finding for
Central:** the backend does not canonicalize number kinds, so any other
client would hit the same problem.

### 11.3 Deviations (worker-found; not silently decided)

1. The node kicker shows the region label, not a separate category.
2. An expanded node (290 wide) can overlap the Outputs rail sideways and stays on top (z-index). *Corrected in Revision 2 (validator N2):* an expanded Model or Split **fully covers** its own Outputs entry, so the mouse cannot reach that entry's hover card; the keyboard still can. `DESIGN.md` allows sideways overlap; whether to adopt G-F3 (expanding toward open space) is for Central.
3. The Dataset node omits row and column counts because the backend does not supply them (§5.1, N3).
4. The Split node's kicker and title wrap at the default width.
5. After F1, a node stops 16px short of the Outputs rail (the region's right padding) but can sit flush at the left and top. This is a small visual asymmetry, reported by the user.
6. "Saved" is low-prominence light-gray text (user observation; it matches the token use).

### 11.4 Not verified by the worker

- The 1280×720 top-bar wrap and the visual review against `DESIGN.md` §12 are left to the independent validator (EP04A-AC11, AC13). Revision 1 failed the window rule (R3), and Revision 2 repairs it.
- Expanded-body scroll containment in a real browser (Section 8, item 4). The Revision 1 validator confirmed it.

## 12. Final attestation

The local Claude Code session ran these commands on the user's Windows
machine, in Windows PowerShell from the repository root, at the user's
direction, on the final tree. The packet's in-scope repairs required complete
reruns; this is the last complete run, after Revision 2 (2026-10-03).

| Command | Exit | Evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | Prettier clean; ESLint clean; ruff "All checks passed!"; mypy "no issues found in 24 source files"; web 56 passed (8 files); Python unit 151 passed, 1 skipped; build passed; integration 56 passed, 1 skipped; smoke verified |
| `npm.cmd run coverage` | 0 | Web 56 passed, 84.7% statements; Python 207 passed, 2 skipped, 89% total |
| `npm.cmd run deps:inventory` | 0 | Completed (npm 389, Python 63 entries) |
| `npm.cmd run license:check` | 0 | "License policy passed for 438 installed locked packages" |
| `npm.cmd run deps:audit` | **1** | npm 11 high of 432 (Section 11.1); Python "No known vulnerabilities found" |
| `git --no-pager diff --check` | 0 | No output |

**Locks:** unchanged, `FB7119F6…82FA` and `8030A7C4…0A25`.

**Staged list:** empty.

**Status:** 41 entries, identical in membership to the baseline. The only
addition is this report (`??`), which makes 42. The editor directory is
untracked as a whole.

**Listeners:** none on 8000 or 5173 after the walkthroughs.

**Workflow store:** `.vidap-local/workflows/` holds only the capture
workflows. `capture-example` is at its original bytes (`DB55A163…`). The
Revision 2 check workflows were deleted.

**Environment note:** uv prints a harmless warning that the user's Anaconda
`VIRTUAL_ENV` does not match `.venv`, and ignores it.

**Temporary capture tools:** `.vidap-local/ep04a-tools/` was removed before
the final run, because ESLint lints that ignored folder and failed on the
capture converter. The commands are recorded in Section 14.

## 13. Paths changed and test inventory

**Paths.** All are within Section 8:

- `apps/web/src/editor/**` (Revision 2 adds `measure.ts`)
- `apps/web/src/main.tsx`
- `apps/web/index.html`
- `DESIGN.md` (Section 7)
- `README.md` (current-state sentences about the editor workspace)
- `CONTRIBUTING.md` (one editor paragraph: the single-source rule and recorded test data)
- this report

Unchanged: `eslint.config.js`, `package.json`, both locks, `apps/web/src/test/setup.ts`, `foundation-root.*`, Python, fixtures, CI, scripts, and `docs/design/`.

**Editor tests (46 after Revision 2).**

- `api.test.ts` (5): number spellings; unchanged byte identity; changed numbers plain; parity with `JSON.stringify`; "unreachable" only when the backend did not answer (Revision 2).
- `contract-source.test.ts` (2): no copied contract literals; recorded responses match the channel contract.
- `layout.test.ts` (8): sidecar restore; fallback and stale entries; width clamp; position clamp; push-down; push-down by measured height (Revision 2); rail stacking; rail stacking by measured height (Revision 2).
- `model.test.ts` (6): naming; effective values; boundary entries; UNASSIGNED; navigation; `withParameter`.
- `editor.test.tsx` (25): the items in Section 8. Added in Revision 2: the focus-mode Tab trap and hidden wires; a focus-mode edit shown in place; no unsaved state for no-op changes. New after the first walkthrough:
  - position clamp;
  - move mode ending on blur;
  - double-click;
  - gutter focus;
  - Tab order;
  - workspace-banner diagnostic;
  - unreadable-sidecar fallback;
  - clean-state conflict wording.

## 14. Recorded-data capture

`test-data/recorded.ts`: SHA256 `E9EE4660…5B42`, 15,172 bytes, 12 responses,
5 contracts, workflow digest `sha256:db55a163…`. It was captured from the
real backend on the user's Windows machine from the synthetic P3-EP03B
success fixture. The D0.7 metadata is in `test-data/manifest.json`.

Commands as run, with `npm.cmd run launch` running:

```powershell
uv --project python run --locked python .vidap-local\ep04a-tools\capture_slice.py http://127.0.0.1:8000 .vidap-local\ep04a-tools\recorded.json
node .vidap-local\ep04a-tools\gen_recorded.mjs .vidap-local\ep04a-tools\recorded.json apps\web\src\editor\test-data\recorded.ts
npx.cmd prettier --write apps\web\src\editor\test-data\recorded.ts
```

What the capture script does, in order:

1. Removes any earlier `capture-example` and `capture-no-layout` files under `.vidap-local/workflows/`.
2. Records `contracts`, then `validate` for the fixture and for a copy with regularization 0.
3. Saves `capture-example` (with a default sidecar) and `capture-no-layout` (no sidecar).
4. Records `list`, both loads, and a 404 load.
5. Edits the saved `capture-example` regularization to 0.5 on disk and records the 409 save and `compare`.
6. Restores the original bytes and records `compare` unchanged.

The converter wraps the JSON in a typed module.

The first run raised a `ValueError` on its final print only, because of a
relative output path. All 12 responses had been written and the workflow
restored; the print was fixed. Only one digest differs from a cloud
development capture: the temporarily edited file is written with CRLF on
Windows.

**Note for Central.** The capture scripts were temporary, in the ignored
folder, and are no longer in the checkout. The packet did not authorize a
script path. `CONTRIBUTING.md` points to this section for regenerating the
data. A tracked capture tool would need a later packet.

## 15. Open item before validation

The user has not yet re-walked one final behavior: Reload from disk with
nothing unsaved shows a confirmation without "discards" wording and a
"Reload" button (Section 10, the correction). It is covered by the compare
test. The user chose to leave this check to independent validation.

## 16. Independent-validation handoff

> Act as the independent re-validator for `ViDAP_P3_EP04A.md` v0.1, Revision 2. Read the packet, its governing inputs, `DESIGN.md`, and this report, especially Section 17 (the response to the Revision 1 `Revise`), and check the actual delta (Section 13). Confirm R1–R5 and N1, N3, N4, and N6 are repaired in a real browser, including a real 1280×720 window for R3, and that nothing that previously passed has regressed. Run the editor against the real local backend (`npm.cmd run launch`) and drive every state by mouse and keyboard, including a visual review against `DESIGN.md` Section 12 at 100% zoom and at 1280×720 (Section 11.4). Verify that values trace only to contracts and recorded responses, that layout never changes the workflow (including number spelling, Section 11.2), and the conflict flows with outside edits. Assess repairs F1–F6 and the proposed clarifications (Section 7), deviations (Section 11.3), and the `deps:audit` advisory (Section 11.1). Do not edit tracked files, accept for Central, or begin P3-EP04B. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

This worker does not validate its own work or accept anything for Central.

## 17. Response to independent `Revise` (Revision 2)

All repairs are in `apps/web/src/editor/`. jsdom has no layout engine and no
`ResizeObserver`, so R1–R3 were also checked by the user in a real browser on
Windows against the real backend. The check workflows were saved through the
channel and deleted afterwards.

| Item | Revision 2 change | Regression proof |
|---|---|---|
| R1: push-down ignored message height | New `measure.ts` (`useMeasuredHeights`, a `ResizeObserver`). Push-down and region height use each node's **measured** height: any node taller than compact (expanded or showing a message) pushes the nodes below it by its extra height. Unmeasured nodes use nominal heights | `layout.test.ts` "pushes down by measured height…"; user: Model 1 at regularization 0 and collapsed pushes Model 2 below the message, the region grows, and fixing it slides Model 2 back |
| R2: rail entries overlapped | Rail entries are measured, and stacking uses `max(48, measured height + 4)` | `layout.test.ts` "stacks rail entries by their measured heights"; user: two "Train/Test Split.split" entries fully readable |
| R3: page overflowed at 1280×720 | Removed `.editor { min-width: 1280px }`. The editor clips to the window and the top bar wraps; only the workspace scrolls (`min-width/min-height: 0`) | User: a narrowed window never scrolls sideways and the top bar wraps |
| R4: stale field after a focus-mode edit | `ParameterField` follows a document value changed elsewhere, unless its own text already means that value (so typing "0." is kept) | Editor test "shows a value changed in focus mode in the node's own field too"; user |
| R5: Tab left the focus panel | The focus overlay contains Tab and Shift+Tab, cycling the panel's focusable elements | Editor test "keeps Tab inside the focus-mode panel…"; user |
| N1: "could not be reached" for a non-standard 404 | `ApiError` says "could not be reached" only when no response arrived (status 0). Any other non-envelope answer reads "The local ViDAP backend refused the request without an explanation." The backend's text is still never shown | `api.test.ts` "says unreachable only when the backend did not answer" |
| N3: wires visible in focus mode | Wires to and from the lifted node are not drawn while it is lifted | Same editor test as R5 (MODEL's wires go from some to none); user |
| N4: no-op changes marked unsaved | Resize, move (keys and drag), and zoom set the unsaved state only when the value actually changes | Editor test "does not mark the workflow unsaved…"; user |
| N6: Run reason wording | Now exactly "Run arrives in the next step." (§5.3) | Editor test "lays out the slice in its five regions…" |

**Not changed. For Central:**

- **N2:** Section 11.3, deviation 2, is corrected. Whether to adopt G-F3 is for Central.
- **N5:** summary lines wrap to two or three lines (Dataset, Split). `DESIGN.md` §10 says "one summary line". The worker proposes a clarification: one summary *line of content*, which may wrap and is never truncated. That is consistent with the never-truncate rule. Central to decide.
- **N1 channel note:** the backend router answers names containing `/` or `..` with a non-standard 404 body. That is outside this packet.
- **Wires under nodes (user observation in the Revision 2 walk):** when two nodes overlap at the same height, a wire to the farther node runs beneath the nearer one, because wires are drawn below nodes. No routing is specified; a note for P3-EP04B (connections).
