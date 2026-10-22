# ViDAP — Phase 3 Execution Packet P3-EP04B Validation and Central Reconciliation Record

- **Packet ID:** `P3-EP04B`
- **Packet Title:** Graph Authoring: Add, Remove, Connect, New, and Save As (`WS3.4`, Part B)
- **Phase:** Phase 3 (`P3`) — Vertical Slice & Usable MVP
- **Workstream:** `WS3.4` — Visual editor workspace (Part B of 2)
- **Outcome:** **`Accept`**
- **Date:** 2026-10-21
- **Baseline `HEAD`:** `17b7c736dce497c89c30387535a0b3de1d91cd04` (`17b7c73` — `P3-EP03 and 04 done`)
- **Primary evidence:** `ViDAP_P3_EP04B_Implementation_Report.md`

---

## 1. Validation Summary

1. **Verdict:** **`Accept`**.
2. **Evidence basis:** Direct codebase inspection of all created and modified files in `apps/web/src/editor/**`, `apps/web/src/test/setup.ts`, `scripts/capture-editor-responses.mjs`, `DESIGN.md` (`v0.3`), `README.md`, and `CONTRIBUTING.md`; full Windows execution of `npm.cmd run check`, `npm.cmd run coverage`, `npm.cmd run deps:inventory`, `npm.cmd run license:check`, `npm.cmd run deps:audit`, and `git --no-pager diff --check`; and live Windows `npm.cmd run launch` walkthrough (`a`–`m`).
3. **Scope and authority checks:**
   - All changed and new files are within `P3-EP04B` Section 8 authorized paths (plus Central's packet/plan/reconciliation records).
   - No backend Python files (`python/**`), Phase 1/2 contracts, or lockfiles (`package-lock.json`, `python/uv.lock`) were modified.
   - `DESIGN.md` `v0.3` matches the pre-approved Section 6 amendment (`items 1–10`) verbatim.
   - All 71 editor unit/integration tests across 7 test files (`81` web tests across 10 files total) pass, and web coverage is `87.1%` statements (`87.01%` in `apps/web/src/editor`).

---

## 2. Acceptance Criteria Verification (`EP04B-AC01` through `EP04B-AC14`)

| Criterion | Status | Evidence |
|---|---|---|
| `EP04B-AC01` — Contract-driven `+ Add` menu in each spatial region header (`Data`, `Model`, `Evaluation`) | **Satisfied** | `AddMenu.tsx`, `Workspace.tsx`, `contract-source.test.ts`, `authoring.editor.test.tsx`. |
| `EP04B-AC02` — Adding a node creates deterministic IDs (`dataset`, `dataset-2`, ...), materializes defaults, places on grid without overlap, marks dirty, and calls `/api/slice/validate` | **Satisfied** | `authoring.ts` (`nextNodeId`, `addNodeToWorkflow`), `authoring.test.ts`, `authoring.editor.test.tsx`. |
| `EP04B-AC03` — Removing a node requires confirmation (naming incident edge count when `> 0`), deletes node + incident edges + sidecar position, and revalidates | **Satisfied** | `authoring.ts` (`removeNodeFromWorkflow`), `Editor.tsx`, `authoring.test.ts`, `authoring.editor.test.tsx`. |
| `EP04B-AC04` — Connect output port to input port by click-then-click, pointer drag, and keyboard (`Enter`/`Space` + `Escape`) | **Satisfied** | `Workspace.tsx`, `NodeView.tsx`, `Editor.tsx`, `authoring.editor.test.tsx`. |
| `EP04B-AC05` — Contract-derived compatibility preview (`nominalType` match, no self-loop), non-color incompatible refusal, and backend `/api/slice/validate` authority | **Satisfied** | `authoring.ts` (`evaluateConnectionCandidate`), `NodeView.tsx` (`data-port-state`), `authoring.test.ts`, `authoring.editor.test.tsx`. |
| `EP04B-AC06` — `cardinality: "one"` replaces existing incoming edge on `(targetNodeId, targetPortKey)` without disturbing other ports; duplicate identical edges refused | **Satisfied** | `authoring.ts` (`connectPorts`), `authoring.test.ts`, `authoring.editor.test.tsx`. |
| `EP04B-AC07` — Expanded node `Connections` section lists incoming/outgoing edges with `Disconnect` action that removes the edge and revalidates | **Satisfied** | `NodeView.tsx`, `authoring.ts` (`disconnectEdge`), `authoring.editor.test.tsx`. |
| `EP04B-AC08` — Non-input diagnostics (`edge`, `workflow`, and non-input `port` diagnostics) render visibly in the workspace diagnostic banner (`role="status"`) | **Satisfied** | `authoring.ts` (`diagnosticsNotOnNodeInputs`), `Editor.tsx`, `authoring.editor.test.tsx`. |
| `EP04B-AC09` — `New` action with unsaved-changes confirmation and `Save as` flow with client-side `^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$` validation, `PUT /api/slice/workflows/{name}`, list refresh, and `409 conflict` handling | **Satisfied** | `authoring.ts` (`createEmptyWorkflow`, `validateWorkflowName`), `Editor.tsx`, `authoring.editor.test.tsx`. |
| `EP04B-AC10` — Expanded node shifts left inside its region when default right expansion would overflow region bounds or overlap a node to the right (`C1`), and lower nodes push down only by actual vertical overlap + `16px` (`C2`) | **Satisfied** | `layout.ts` (`resolveExpandedX`, `applyExpandedPushDown`), `layout.test.ts`. |
| `EP04B-AC11` — Tracked capture script `scripts/capture-editor-responses.mjs` (`C4`) and matching `recorded.ts` + `manifest.json` (`p3-ep04b-editor-recorded-responses-v2`) | **Satisfied** | `scripts/capture-editor-responses.mjs`, `apps/web/src/editor/test-data/recorded.ts` (`18,496` bytes, SHA-256 `126D8C13301A5D616315F52182585FCA6935EB6E6FAA3D6541D264A5616391CD`), `apps/web/src/editor/test-data/manifest.json`. |
| `EP04B-AC12` — `DESIGN.md` updated to `v0.3` matching Section 6 items 1–10 and satisfied by `DESIGN.md` §12 self-check | **Satisfied** | `DESIGN.md` (`4DEEDCC851436D0FA7C495F9132B73AEEA85055C4C9BEC6F511560A764084171`). |
| `EP04B-AC13` — Manual Windows `npm.cmd run launch` walkthrough (`a`–`m`) completed and temporary workflow removed | **Satisfied** | `ViDAP_P3_EP04B_Implementation_Report.md` §6 and §9. |
| `EP04B-AC14` — Full attestation passes with unchanged lockfiles and clean `git --no-pager diff --check` | **Satisfied** | `ViDAP_P3_EP04B_Implementation_Report.md` §7 and §8. |

---

## 3. File Inventory and SHA-256 Hashes

| Path | SHA-256 |
|---|---|
| `apps/web/src/editor/AddMenu.tsx` | `0B8FA9FD8C53890A0E43280297F9AE5BB6142D13270A6DFFAE90CC5C331203F5` |
| `apps/web/src/editor/ConfirmDialog.tsx` | `A1A304FAC12F593FFCB78B2B5C5F64BA9CD6E5777ED68F19E4CA52A3C021F5D5` |
| `apps/web/src/editor/Editor.tsx` | `382B5DD788F5DF1795134D4FC659C01653D0C31E10D7AD29896610650788B281` |
| `apps/web/src/editor/NodeView.tsx` | `67ACB6159CD4EBF8B7C938013A3747E68BFDBB7F8708742D4B0EC75A26BC577F` |
| `apps/web/src/editor/Workspace.tsx` | `82E1D009B24E78825BD9603C490E4B38AE10FB0E3F95BE37030F47611A217C79` |
| `apps/web/src/editor/api.test.ts` | `D30386ADF7D866A8173516FB1DD7F58F152B487DC0F7148C65570E5A66256209` |
| `apps/web/src/editor/api.ts` | `D1902A4D864FB3E09211B0355E1564FBFF6358607B38B93750B702C693684E97` |
| `apps/web/src/editor/authoring.editor.test.tsx` | `90181E82BB4CD90E6A764FE7AD18C148633251881F2BE14821359AE9F71B73C2` |
| `apps/web/src/editor/authoring.test.ts` | `489DE5BB4A4DD1D31FC85F9C093197BF3397B231A65A20388686E6C72904F5AF` |
| `apps/web/src/editor/authoring.ts` | `99B0BC87ABFF14943C492020C5B1BD993AF6D9AD29846549F21BF0504E3A4372` |
| `apps/web/src/editor/contract-source.test.ts` | `BFA181CD67F4876DB6CC42244E8FE10C39F0A66476D1BB18CC03AA86198C91DA` |
| `apps/web/src/editor/editor.css` | `6F16DA1974CC6FDAFCCBEC2F44F63FBA7662285A9DC16287888708C2AF70FC77` |
| `apps/web/src/editor/editor.test.tsx` | `EBDE74F358F7531A377965346A8AA6D5748486A5370B4162DFAA03B95F7085BC` |
| `apps/web/src/editor/layout.test.ts` | `55D2FA3EFEB9533748C402C21A4B4A8ED3E5A98D23864076213CFE66987E0FBD` |
| `apps/web/src/editor/layout.ts` | `FD75E24515B40C5C9EA830B107E144E943CDEE557E83EAF0DD3CC78D01132345` |
| `apps/web/src/editor/measure.ts` | `6C475DAF21688A474AB5BBF48DBE2A4FE01A7718AA44D2D5B809CAF07129A7F0` |
| `apps/web/src/editor/model.test.ts` | `53115529A43EDF447A06191F3769747BC5C0568519E598623947F4A9391C09CB` |
| `apps/web/src/editor/model.ts` | `FFBFEB6E604029AAA83EB3CD30961090832250AB9A1950B4A52F732DD46E538A` |
| `apps/web/src/editor/presentation.ts` | `B68F70922D741297B89AE3D3E6C9B0C6F32210CAE133FF4090C15A7712AC7A1E` |
| `apps/web/src/editor/test-data/manifest.json` | `5B82EBFDA971C0A95D67CF10563352BC08211F1D8DD29DD9DF93EC15B11E2610` |
| `apps/web/src/editor/test-data/recorded.ts` | `126D8C13301A5D616315F52182585FCA6935EB6E6FAA3D6541D264A5616391CD` |
| `apps/web/src/editor/test-support.tsx` | `B5902121BA05A59215BE3EFED7D398712894CC34A6AB2D8AA8AA7B568F70EB4F` |
| `apps/web/src/editor/vite-env.d.ts` | `65996936FBB042915F7B74A200FCDDE7E410F32A669B1AB9597CFAA4B0FADDB5` |
| `apps/web/src/test/setup.ts` | `A9028FD5A779665659FF489773B267543B48A6C82FAC14B1FC11259657414C01` |
| `scripts/capture-editor-responses.mjs` | `30A91DB096D45B450F6383F7BFBCED5670F07CD3A6D2FA2FDD4A7E000AE9098A` |
| `DESIGN.md` | `4DEEDCC851436D0FA7C495F9132B73AEEA85055C4C9BEC6F511560A764084171` |
| `README.md` | `9D26CBB4D135E4E3A7F812F68B274BCB0B459775D276E0ED08620D38C5D85CE2` |
| `CONTRIBUTING.md` | `B69F526D085EE3757614A69EE62077A3499334486EC6FD16CB5755F8C378DC03` |
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `8030A7C44776A9CB0BE51E4528ECC917D10CB0C67790CD76EAEB037960080A25` |

---

## 4. Central Reconciliation Notes & Next Packet (`P3-EP05`)

1. **`WS3.4` (`P3-EP04A` + `P3-EP04B`) is now complete.** Both parts of the visual editor workspace workstream are accepted and reconciled.
2. **Carry-forward items for `P3-EP05` (`WS3.5` — Run, results, and trace):**
   - Trigger `POST /api/slice/run` from the top bar `Run` control (enabled only when the workflow is valid and no run is in progress) and handle `409 busy` with a clear non-destructive banner.
   - Render per-node execution states (`Running`, `Completed`, `Failed`, `Blocked`, `Unrelated`) from the `/api/slice/run` response (`nodes[].status`).
   - Render the primary result (`Accuracy` formatted as percentage + `correct / testRows`) in the top application bar and on `Evaluate`'s compact summary line, sourced exclusively from `metrics` in `/api/slice/run` (which reads back `proof-output.bin`). Clear or mark stale when edits change the workflow after a run.
   - Present runtime failures (`outcome: "failed"`, `diagnostics[]`) directly on the affected node (`Run failed` badge, plain-language `explanation` and `remedy`, and collapsed `Technical details` toggle) or in the workspace banner when `nodeId` is `null`.
   - Implement Boundary Value Trace / X-Ray mode (`DESIGN.md` §9): clicking or pressing `Enter`/`Space` on a boundary rail entry highlights the producer node, consumer nodes, and matching rail entries in `--accent`, dims unrelated nodes/rails (`opacity: 0.45`), draws dashed `2px` `--accent` cross-region trace lines, shows the top-bar `Tracing: <Boundary value> — Esc to exit` banner, and resolves the dimmed-border 3:1 contrast check (`DESIGN.md` §9).
3. **Carry-forward items for `P3-EP06` (`WS3.6` — Closeout):**
   - Draft saving decision (`P3-EP04B` Central note 1), intermittent Phase 2 test check, Windows symlink check, `1280×720` secondary viewport walk, and lockfile advisory review (`http-cache-semantics`, `source-map-js`, `vite`, `certifi`).
