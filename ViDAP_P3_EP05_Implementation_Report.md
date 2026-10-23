# P3-EP05 Implementation Report

Single-chat workflow: planned, implemented, and audited in one session. Sean ran the walkthrough in the browser and approved the results.

## 1. Baseline

- Branch `main`, HEAD `8ff3f85` ("P3-EP04B complete").
- Lock hashes unchanged:
  - `package-lock.json` `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA`
  - `python/uv.lock` `8030A7C44776A9CB0BE51E4528ECC917D10CB0C67790CD76EAEB037960080A25`

## 2. What changed

- `DESIGN.md` v0.4: dimmed-border 3:1 contrast resolved (`--dim-fill` `#EEF0F3` with `--border-strong` `#7A8494`, at least 3.3:1).
- Editor (`apps/web/src/editor/`): Run with gating and a Running state, node status chips, recorded metrics (top bar and Evaluate node, "Last run" when stale), runtime-error presentation on nodes and in banners, and boundary trace from rail entries (`run-trace.editor.test.tsx`).
- Capture tool extended; 24 live `/api/slice/` responses recorded (`p3-ep05-editor-recorded-responses-v3`, sha256 `8095478DD9AA1D9F4E759BD916BFFF54D8881A16B3317B1C167A68D02CC4BACA`, 22,686 bytes).
- `README.md` updated.

## 3. Defect found in the walkthrough and fixed

**Symptom (Sean):** typing in a parameter field (for example Model, Regularization) accepted one digit, then focus left the field.

**Cause:** the focus-mode `NodeView` was given an inline ref callback, `(element) => element?.focus()`. A new function each render makes React re-run it, so every keystroke that re-rendered `Editor` moved focus to the node card.

**Fix:**

- `Editor.tsx`: focus the focus-mode node once, in an effect keyed on `[focusMode]`; stable `registerNode` and `registerFocusedNode` callbacks.
- `measure.ts`: per-key ref callbacks are cached, so nodes are no longer unobserved and re-observed on every render.
- `NodeView.tsx`: typed values update `shown` together with the draft.
- Regression test in `editor.test.tsx`: `document.activeElement` stays on the input across successive edits in focus mode.

Sean re-tested in the browser and confirmed the fix.

## 4. Verification (Windows, run by the agent at Sean's direction)

| Check | Result |
|---|---|
| `npm.cmd run check` | Pass: 11 Vitest files, 89 tests; 151 Python unit passed; build, integration, and smoke passed |
| `npm.cmd run coverage` | Pass: 207 Python passed, 2 skipped; Python total 89% |
| `npm.cmd run deps:inventory` / `license:check` | Pass (438 locked packages) |
| `npm.cmd run deps:audit` | **Exit 1: new findings, see section 5** |
| `git diff --check` | Clean |
| Lock hashes | Unchanged (above) |
| Staged files | None |
| Sean's browser walkthrough | All items pass |

## 5. Items for Sean and Central

1. **New audit findings.** The EP04A reconciliation accepted exit 1 only for GHSA-ch52-4w7c-c8xp (`http-cache-semantics`) with 11 dependents and a clean Python audit. The audit now reports more, with locks unchanged (the advisory database moved). Each is new and must be triaged; none was fixed here, because that would change a lock.
   - npm, besides `http-cache-semantics`: `vite` (high, GHSA-698v-4r3x-3vcv and five more), `source-map-js` (high, GHSA-68fv-2mgg-jv7q), `@vitest/mocker` (moderate, GHSA-qxg6-89mg-rqv8 and GHSA-xp26-3454-mjgp), `ip-address` (moderate, GHSA-rxp7-6hxx-x8q5), plus `vitest` and `@vitest/coverage-v8` through `@vitest/mocker`. The audit reports `vitest` 5.0.5 as a non-major fix for the vitest chain.
   - Python: `certifi` 2026.7.22, PYSEC-2026-4320, fixed in 2026.10.19.
   - Suggested next step: a dependency-update packet, since the policy forbids lock changes here.
2. **Run records.** Five run records from the walkthrough made the Phase 2 test `test_pending_publication_failure_is_in_memory_failure_before_dispatch` fail, because it expects `.vidap-local/runs` to be empty. With Sean's approval I deleted them and the test passed. Run-record retention and test isolation belong to P3-EP06.
3. **Listeners.** Ports 8000 and 5173 are in use by Sean's `npm.cmd run launch`. Stop it for the "no listeners" attestation line.
4. **Uncommitted.** Nothing is staged or committed. Sean commits.
