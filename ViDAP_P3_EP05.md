# ViDAP P3-EP05 — Run, Results, Error Presentation, and Boundary Trace

| Field | Value |
|---|---|
| Status | Drafted for review and execution in single-chat workflow |
| Packet version | 0.1 |
| Packet type | Bounded implementation (web + capture script + `DESIGN.md` §9 contrast resolution; no Python runtime changes) |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1, WS3.5 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3 and checkpoint A3 |
| Prerequisites | `P3-EP04B` complete (`ViDAP_P3_EP04B_Validation_and_Reconciliation.md`, accepted 2026-10-21) |
| Workstream | `WS3.5` — Run, results, and trace |
| Authorized worker report | `ViDAP_P3_EP05_Implementation_Report.md` |
| Created | 2026-10-21 |
| Owner | Central |

---

## 1. Purpose

`P3-EP04A` and `P3-EP04B` built the visual editor workspace and full graph authoring (`New`, `Save`, `Save as`, `+ Add`, remove, connect, disconnect, and live validation). `P3-EP05` completes the interactive Phase 3 loop (`WS3.5`):

1. **Run controls and per-node execution statuses:** Run a valid workflow against `POST /api/slice/run`, surface in-flight `Running` state, handle the single-run `409 busy` refusal with a non-destructive retry banner, and render recorded per-node statuses (`Completed`, `Failed`, `Blocked`, `Unrelated`).
2. **Recorded result presentation:** Display the recorded accuracy result (`Accuracy: 87.5% (28 / 32 test rows)`) in the top application bar and on `Evaluate`'s compact summary line, sourced exclusively from `metrics` in `/api/slice/run` (read back from `proof-output.bin`). Keep the last recorded result visible with a `Last run` indicator when subsequent edits are made so the user can compare before and after runs (`UX refinement.txt` §15, `D3.7`).
3. **Runtime failure presentation:** Render Phase 2/3 sanitized runtime diagnostics (`outcome: "failed"`, `diagnostics[]`) directly on the affected node with a `Run failed` badge, plain-language **Why it failed** (`explanation`) and **How to fix** (`remedy`), and a collapsed **`Technical details`** disclosure (`code`, `attemptId`, `operationKey`, `technical.type`, `technical.message`, `technical.traceback`, `technical.causes`).
4. **Boundary value Trace / X-Ray mode:** Clicking or pressing `Enter`/`Space` on any boundary rail entry enters **Trace Mode** (`DESIGN.md` §§8–9), highlighting the producer node, consumer nodes across regions, and matching boundary rail entries in `--accent`, dimming unrelated nodes/rails while preserving `>= 3:1` non-text border contrast (`DESIGN.md` §9 open item), drawing temporary dashed `2px` `--accent` cross-region trace lines, and showing a top-bar trace banner (`Tracing: <Producer> · <Port> — Esc to exit`).

---

## 2. Governing Inputs

1. `ViDAP_Overview.txt` §§2–7, 18–22A, 25, 31.
2. `UX refinement.txt` §§6–16, 22, 24.
3. `ViDAP_Phased_Plan_Spine.md` v1.3 and `ViDAP_Roadmap.md` v4.6.
4. `ViDAP_Phase_3_Plan.md` v1.1 (`WS3.5`, `D3.5`–`D3.10`, `P3-AC02`–`P3-AC08`).
5. `ViDAP_P3_EP01_Validation_and_Reconciliation.md` (`D3.1`–`D3.4`) and `ViDAP_P3_EP02_Validation_and_Reconciliation.md` (`D3.5`–`D3.10`).
6. `ViDAP_P3_EP03C_Validation_and_Reconciliation.md`, `ViDAP_P3_EP04A_Validation_and_Reconciliation.md`, and `ViDAP_P3_EP04B_Validation_and_Reconciliation.md`.
7. `DESIGN.md` v0.3 (`§§4, 5, 7, 8, 9, 10, 12`).

---

## 3. Scope and Non-Goals

### 3.1 In scope

- **API client (`apps/web/src/editor/api.ts`, `model.ts`):**
  - Typed `runWorkflow(workflow: WorkflowDocument, rawNumbers?: ReadonlyMap<string, string>)` calling `POST /api/slice/run` with canonical serialized workflow JSON.
  - Typed response models (`SliceRunResponse`, `SliceRunNode`, `SliceRuntimeDiagnostic`, `SliceMetricsPayload`) and error handling (`409 busy`, `422 invalid-workflow` / `run-refused`, `500` storage/readback errors).
- **Run lifecycle & status presentation (`Editor.tsx`, `Workspace.tsx`, `NodeView.tsx`, `presentation.ts`):**
  - Top bar `Run` primary button (`--accent`), enabled when the workflow has no validation diagnostics (`valid === true` and `nodes.length > 0`) and no run is currently in flight; disabled with clear reason otherwise.
  - While a run is in flight: `Run` button shows `Running...` and is disabled; top-bar run status shows `Running...`; nodes show `Running` status badge.
  - When a run completes (`outcome === "succeeded"`):
    - Top bar right cluster shows the recorded primary result chip (`Accuracy: 87.5% (28 / 32 test rows)`) and `Completed` run state.
    - `Evaluate` node compact summary shows `Accuracy: 87.5% (28 / 32)` (and expanded `Evaluate` node shows the recorded result breakdown: accuracy percentage, `correct` count, `testRows` count, `attemptId`, and `semanticDigest`).
    - Each node in `nodes[]` shows its recorded execution status chip (`Completed`, `Failed`, `Blocked`, `Unrelated`).
  - When the user edits the workflow after a run (parameter change, node add/remove, edge connect/disconnect):
    - Per-node run statuses reset to normal validation readiness (`Ready` / `N issues`) so stale per-node statuses are not confused with current graph state.
    - The last recorded primary result remains visible in the top bar and on `Evaluate` labeled `Last run: 87.5% (28 / 32 test rows)` (`Last run: 87.5% (28 / 32)` on `Evaluate`) until the next run completes or `New` / `Open` loads a different workflow (`UX refinement.txt` §15, `D3.7`).
  - When `POST /api/slice/run` returns HTTP `409` (`code: "busy"`):
    - Render a non-destructive busy banner (`"Another run is in progress."`) with a **`Retry`** button that re-invokes `runWorkflow`; preserve all canvas and parameter state.
- **Runtime error presentation (`NodeView.tsx`, `Editor.tsx`):**
  - When `outcome === "failed"`:
    - Per-node statuses from `nodes[]` (`Completed`, `Failed`, `Blocked`, `Unrelated`) render on each node; the failed node shows `Run failed` (`--status-failed` `#dc2626` / `#fef2f2` / `#fca5a5`).
    - Automatically expand the failed node (if not already expanded) so the user immediately sees the explanation and remedy without hunting.
    - On the affected node (`diagnostic.nodeId === node.id`), render a dedicated runtime failure card containing:
      - Plain-language **Why it failed:** `diagnostic.explanation`
      - Plain-language **How to fix:** `diagnostic.remedy`
      - Collapsed **`Technical details`** disclosure (`<details>`) displaying `code`, `attemptId`, `operationKey`, `portKey` (if any), `technical.type`, `technical.message`, `technical.traceback`, and `technical.causes` in `--font-mono`.
    - Any runtime diagnostic with `nodeId === null` (such as `publication-failed`) renders in the workspace diagnostic banner.
- **Boundary value Trace / X-Ray mode (`Workspace.tsx`, `NodeView.tsx`, `Editor.tsx`, `layout.ts`, `editor.css`):**
  - Make each boundary rail entry (`Exported` on right rail, `Imported` on left rail) an interactive `<button type="button">` with `aria-pressed={isActiveTrace}` and keyboard focus ring.
  - Activating a boundary rail entry enters **Trace Mode** for `{ sourceNodeId, sourcePortKey }`:
    - Top bar / workspace trace banner: `Tracing: <SourceNodeLabel> · <PortLabel> — Esc to exit` with an **`Exit trace`** button.
    - Producer node, all consumer nodes across regions, and all boundary rail entries matching `(sourceNodeId, sourcePortKey)` get `data-trace-state="highlighted"` (`2px solid var(--accent)`, `--accent-subtle` header/tint).
    - Unrelated nodes and boundary rail entries get `data-trace-state="dimmed"`. To satisfy the **3:1 non-text border contrast requirement** (`DESIGN.md` §9), dimmed nodes use explicit muted surface/text styling with a `#64748b` (`--border-strong`, `4.46:1` against `#f8fafc`) border rather than whole-card `opacity: 0.45` that would wash the border below `3:1`.
    - Temporary cross-region SVG trace curves (`2px` dashed `--accent`, `stroke-dasharray: 6 4`, `pointer-events: none`) connect the producer node's output port to every cross-region consumer node's input port across the workspace SVG layer.
    - Pressing `Escape`, clicking **`Exit trace`**, clicking the same boundary rail entry again, or switching/clearing workflows exits Trace Mode.
- **Recorded-response capture (`scripts/capture-editor-responses.mjs`, `apps/web/src/editor/test-data/recorded.ts`, `manifest.json`):**
  - Extend `scripts/capture-editor-responses.mjs` to capture real `/api/slice/run` responses from the live backend:
    1. Successful run of `capture-example` (`outcome: "succeeded"`, `metrics` with `accuracy`, `correct`, `testRows`).
    2. Successful run of `capture-example` with modified parameter (`regularization: 0.01` or `test_fraction: 0.5`) proving parameter propagation changes the backend result (`P3-AC04`).
    3. Failed run of a valid slice workflow where `Dataset.table` is wired directly to `Train/Test Split.table` (bypassing `Prepare Data`), producing `outcome: "failed"`, `code: "unencoded-category-input"`, `Dataset` and `Train/Test Split` `completed`, `Model` `failed`, and `Evaluate` `blocked` (`P3-AC05`).
  - Clean up any attempt directories created in `.vidap-local/runs/` during capture so `.vidap-local/runs/` is not left dirty.

### 3.2 Out of scope (non-goals)

- No changes to `python/**`, `package-lock.json`, or `python/uv.lock`.
- No client-side metric calculation or synthetic run results; every displayed metric comes from `/api/slice/run`.
- No multi-run comparison table or experiment history UI (belongs to Phase 6).
- No draft-saving of invalid workflows (deferred to `P3-EP06` per `P3-EP04B` Central note 1).

---

## 4. `DESIGN.md` Amendment (`v0.4` — §9 Dimmed Border Contrast Resolution)

In `DESIGN.md` §9 (`Trace / X-Ray Mode`), replace:

> - **Unrelated nodes and rails:** Dim to `opacity: 0.45` (maintaining legible text if inspected, while clearly receding visually). Ensure dimmed node borders retain at least a 3:1 contrast ratio against the region background, or verify during `P3-EP05` implementation.

with:

> - **Unrelated nodes and rails:** Receive `data-trace-state="dimmed"`, muting interior text/chrome while keeping a `1px solid var(--border-strong)` (`#64748b`) node border (`4.46:1` contrast ratio against `--bg-region` `#f8fafc`, satisfying the 3:1 non-text contrast floor) and `opacity: 0.55` on unrelated wires.

And update `DESIGN.md` header version to `0.4 (Phase 3 P3-EP05 run, results, and trace amendment — 2026-10-21)`.

---

## 5. Authorized File Scope

- `apps/web/src/editor/**`
- `scripts/capture-editor-responses.mjs`
- `DESIGN.md`
- `README.md`
- `ViDAP_P3_EP05.md`
- `ViDAP_P3_EP05_Implementation_Report.md`
- `ViDAP_P3_EP05_Validation_and_Reconciliation.md`
- `ViDAP_Phase_3_Plan.md`
- `ViDAP_Roadmap.md`

---

## 6. Proof Items and Acceptance Criteria (`EP05-AC01` through `EP05-AC10`)

1. **`EP05-AC01` — Run control gating and in-flight state:** `Run` is enabled when the workflow is valid and idle, disabled when invalid or while a run is in flight, and shows `Running...` during execution.
2. **`EP05-AC02` — Recorded result display and no UI recalculation:** Running `capture-example` displays the exact `accuracy`, `correct`, and `testRows` from `/api/slice/run` (`proof-output.bin`) in the top bar and on `Evaluate`'s compact summary line and expanded view.
3. **`EP05-AC03` — Parameter change alters recorded result (`P3-AC04`) and `Last run` retention (`UX §15`):** Editing a parameter after a successful run marks the displayed result as `Last run` while editing, and running again updates the displayed result to the new recorded backend metrics.
4. **`EP05-AC04` — Per-node execution statuses:** Recorded node statuses (`completed`, `failed`, `blocked`, `unrelated`) from `/api/slice/run` render as non-color-only text badges (`Completed`, `Run failed`, `Blocked`, `Unrelated`) on the corresponding nodes.
5. **`EP05-AC05` — Runtime failure presentation on affected node (`P3-AC05`):** Running the valid-but-unprepared workflow (`Dataset.table -> Train/Test Split.table`) surfaces `unencoded-category-input` directly on `Model` (`Run failed` badge, plain-language `explanation` and `remedy`, and collapsed `Technical details` toggle) and marks `Evaluate` as `Blocked`.
6. **`EP05-AC06` — Single-run `409 busy` handling:** When `/api/slice/run` returns HTTP `409` (`code: "busy"`), the editor displays `"Another run is in progress."` with a working `Retry` button and preserves all workspace state.
7. **`EP05-AC07` — Boundary value Trace / X-Ray mode (`P3-AC06`, `DESIGN.md` §§8–9):** Clicking or pressing `Enter`/`Space` on a boundary rail entry highlights producer node, consumer nodes across regions (including `Train/Test Split · Split` consumed in both `Model` and `Evaluation`), and matching boundary rail entries, dims unrelated nodes while keeping `>= 3:1` border contrast, renders dashed `--accent` cross-region trace lines, shows the `Tracing: ... — Esc to exit` banner, and exits on `Escape` or `Exit trace`.
8. **`EP05-AC08` — Recorded responses and clean `.vidap-local/` state:** `scripts/capture-editor-responses.mjs` captures the `/api/slice/run` fixtures from the live backend, `manifest.json` matches `recorded.ts`, and `.vidap-local/runs/` has no leftover capture directories.
9. **`EP05-AC09` — Manual Windows `npm.cmd run launch` walkthrough:** User walkthrough verifies running `capture-example`, changing a parameter and re-running, triggering the runtime failure (`Dataset -> Train/Test Split`) and inspecting the remedy/technical details, and activating/exiting Boundary Trace mode.
10. **`EP05-AC10` — Full attestation:** `npm.cmd run check`, `npm.cmd run coverage`, `npm.cmd run deps:inventory`, `npm.cmd run license:check`, `git --no-pager diff --check`, and unchanged lockfile hashes pass.
