# ViDAP P3-EP03C — Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03C.md` v0.1, explicitly approved by the user 2026-10-02 |
| Worker execution | 2026-10-02; Linux shells over the Windows checkout; every Windows step run by the user under the `CONTRIBUTING.md` workaround |
| Revision | 2, 2026-10-02, responding to the independent `Revise` (Section 11) |
| Worker result | Revision 2 complete; final attestation passed on a complete Windows rerun after the revision (Section 8); ready for re-validation |
| Independent validation | Revision 1 returned `Revise` (R1 blocking, R2 recommended); Revision 2 awaits re-validation; this report is not a verdict |
| Central decision | Pending |

## 1. Approval and baseline

The baseline was recorded before writing:

- Branch `main`, `HEAD` `17652fc28eafa0b8e2b5be58c55df9ced0d7afff`, nothing staged.
- Lock hashes equal P3-EP03B's: `package-lock.json` `FB7119F6…82FA`, `python/uv.lock` `8030A7C4…0A25`.
- The working tree had 31 entries: the accepted, uncommitted P3-EP03A and P3-EP03B work, the Central records, the P3-EP03C packet, and the Central approval edits to the packet, plan, and roadmap.
- None of `slice_api.py`, `workspace.py`, `test_slice_api.py`, or `test_slice_workspace.py` existed.

**Development environment note.** PyPI is blocked from the worker shells, and
the cloud shell has no FastAPI. For development only, the worker copied the
pure-Python `fastapi` 0.141.1 and `starlette` 1.6.0 packages (with two small
pure-Python helpers) out of the existing locked Windows environment. It did so
through one temporary archive in the ignored `.vidap-local/` folder, which was
removed right after copying. The development copy otherwise matched P3-EP03B.
Nothing was installed or changed in the checkout's environment. All evidence
below comes from the user's Windows runs.

## 2. Channel (Section 4.1–4.2)

`slice_api.py` provides one `APIRouter` at `/api/slice`, carrying a
router-level `guard` dependency. `app.py` calls `install(app)`, which adds
the router and a handler for its own `SliceError` only. `/api/status` and the
FastAPI settings are unchanged, so OpenAPI and docs stay disabled and no CORS
middleware is installed. The router-level host check is the Central choice
recorded in packet §4.1.

| Guard | Rule | Refusal |
|---|---|---|
| Host | Host header's name is `127.0.0.1` or `localhost` (port ignored) | `400 invalid-host` |
| Origin | absent, or exactly `http://127.0.0.1:5173` / `http://127.0.0.1:8000` | `403 origin-refused` |
| Content type (POST/PUT) | `application/json`, optionally `; charset=utf-8`, case-insensitive | `415 unsupported-content-type` |
| Size | `Content-Length` and the streamed byte count are both capped at 256 KiB | `413 body-too-large` |
| Encoding and JSON | UTF-8; for wrapper bodies, JSON with no duplicate names and no `NaN`/`Infinity` | `400 malformed-json` |

Every error uses the same envelope: `{"error": {"code", "message"}}`, plus
listed extras such as `diagnostics`, `attemptId`, or conflict fields. Each
message is a fixed string. The test suite checks that input is never echoed.

| Endpoint | Request | Success response |
|---|---|---|
| `GET /contracts` | — | `{"contracts": [{type, label, description, inputs[], outputs[], parameters[]}]}` from `SLICE_REGISTRY` only |
| `POST /validate` | workflow text | `{"valid", "diagnostics": [{code, severity, category, elementKind, elementReference, message, remedy, jsonPointer}]}`; an undecodable document → `422 invalid-workflow` with the decoder's Phase 1 finding |
| `POST /run` | workflow text | `{"attemptId", "outcome", "semanticDigest", "nodes": [{nodeId, operationKey, status}], "diagnostics": [D2.7 envelopes], "metrics"}` |
| `GET /workflows` | — | `{"workflows": [{name, workflowDigest, hasSidecar}]}` |
| `GET /workflows/{name}` | — | `{"name", "workflow", "workflowDigest", "sidecar", "sidecarDigest", "sidecarNotice"}` |
| `PUT /workflows/{name}` | `{"workflow", "sidecar", "baseWorkflowDigest", "baseSidecarDigest"}` (exact fields) | `{"name", "workflowDigest", "sidecarDigest"}` |
| `POST /workflows/{name}/compare` | `{"workflow", "baseWorkflowDigest", "baseSidecarDigest"}` (exact fields) | `{"changed", "missing", "workflowDigest", "sidecarDigest", "summary"}` |

**Run endpoint.**

- **Before running.** The document is decoded and validated first. Any
  finding returns `422 invalid-workflow`, and no attempt is allocated. A
  refusal before allocation (for example, no Evaluate node) returns
  `422 run-refused`.
- **One run at a time.** A process-level non-blocking lock is held only
  around `run_slice_attempt`. A second run gets `409 busy` and is not queued.
- **Recorded result.** `metrics` comes only from the attempt's
  `proof-output.bin`, and only when the outcome succeeded and the record lists
  the slot. The bytes must:
  - parse with the five exact fields;
  - rebuild through `SliceMetrics`;
  - serialize back to identical bytes.

  Otherwise the response is `500 metrics-readback-failed`, carrying the
  attempt ID and no metrics.
- **Unverifiable record.** `PublicationIndeterminate` returns
  `500 publication-indeterminate` with the attempt ID.

`metrics-readback-failed` is the one code not named in the packet. It covers a
recorded slot that cannot be read back exactly, a case the packet requires to
return no metrics.

## 3. Workflow files (Section 4.3–4.5)

`workspace.py` implements the storage.

- **Location.** The fixed directory `.vidap-local/workflows/`. Each path
  segment and file is checked for symlinks and reparse points, and the
  resolved path must stay inside the checkout.
- **Names.** Workflow names must match `^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$`.
  Files are `<name>.vidap.json` and `<name>.vidap-view.json`.
- **Digests.** `sha256:<hex>` of the file bytes.
- **Load.**
  - A workflow file over 256 KiB returns `413 workflow-too-large`.
  - Otherwise the strict Phase 1 path decodes and validates it. Undecodable
    UTF-8 receives the Phase 1 malformed-text finding. Any finding returns
    `422 invalid-workflow`, and the file is never rewritten.
  - The workflow is returned as canonical serializer output, with any
    Phase 1 layout returned unchanged (V16).
  - A malformed, oversized, or unsupported sidecar is reported in
    `sidecarNotice` (`unreadable` or `unsupported`), with its digest. The
    workflow still loads.
- **Save.** The workflow must decode and validate, and the sidecar must pass
  the §4.4 shape check. Then, under a process-level save lock:
  - Each file's current digest, or `null` if absent, is compared with its
    base. Any mismatch refuses the whole save with `409 conflict`, returning
    the current digests, `missing`, and the summary (V15).
  - The workflow bytes are exactly `serialize_document` output. The sidecar
    is sorted, indented JSON with a final newline.
  - Each file is written to an exclusive `<file>.tmp`, synced, and moved into
    place with `os.replace`: the workflow first, then the sidecar. A
    pre-existing temporary file refuses the write. A `null` sidecar leaves an
    existing sidecar untouched, and only when its base digest matches.
- **Compare.** Compare is read-only. Its summary compares the disk workflow
  with the posted one, and is `null` when nothing changed or the file is
  missing.
- **Sidecar shape (§4.4).**
  - The keys must be exactly the five listed ones.
  - Regions: at most 32 entries, unique keys of 1–40 characters from
    `[A-Za-z0-9_-]`, and widths from 120 to 4000.
  - Nodes: at most 500 entries, keyed by canonical UUID, each with a region
    key and coordinates in ±100000.
  - Viewport zoom: from 0.1 to 4.
  - Booleans are refused as numbers. The serialized sidecar must be at most
    64 KiB.
- **Change summary (§4.5).** The summary records:
  - nodes added or removed, with their types;
  - edges added or removed, with their endpoints;
  - parameters changed, with before (posted) and after (disk) values;
  - labels changed;
  - whether the layout metadata changed.

  Each list is sorted. If the disk file cannot be decoded, the summary
  becomes `{"diskUnreadable": true}`.

**Deviation note.** The packet listed four load refusals as `422`. An
oversized file is refused before decoding with its own code,
`413 workflow-too-large`, consistent with the request-size code. The three
decodable-failure cases, plus undecodable UTF-8, return `422` as specified.

## 4. Proof (Section 5)

The tests drive `create_app()` through `httpx.ASGITransport` at
`http://127.0.0.1:8000`, using the real registry, fixtures, run layer, and
files. Save and load tests point the workspace at a temporary directory, so
they never touch the user's real saved workflows. Run records go to
`.vidap-local/runs/` and are removed by recorded ID.

| Item | Tests and evidence |
|---|---|
| 5.1 Contracts | Field-by-field drift test against `SLICE_REGISTRY`; the response contains no region data |
| 5.2 Validate | Success is valid. A constraint violation and a wrong-port connection return Phase 1 codes. An undecodable document returns `422`. No attempt is allocated |
| 5.3 Run | Success metrics equal the independent calculation and the slot bytes; the digest equals the plan's. The bypass returns `unencoded-category-input` on the Model node with `metrics: null`. A proof-write failure returns no metrics. A non-canonical slot returns `500 metrics-readback-failed` with no metrics. Indeterminate publication returns `500` with the attempt ID. Invalid and refused runs allocate nothing |
| 5.4 Single run | With the lock held, `409 busy` and no allocation |
| 5.5 Guards | Foreign hosts (`testserver`, `evil.example`, `127.0.0.2`, `localhost.evil`) are refused while `/api/status` still answers. Five foreign origins are refused with no CORS header (a preflight gets none either); `localhost` and both allowed origins are accepted. Four bad content types are refused; a mixed-case charset is accepted. An oversized body is refused, whether declared or streamed. Invalid UTF-8, a truncated document, `NaN`, and duplicate names are refused. Input is never echoed, and docs and OpenAPI return 404 |
| 5.6 Fidelity | The saved bytes equal `serialize_document` output. Load returns matching digests. An endpoint run of the loaded document, and a headless run of the disk file, give the same semantic digest and metrics as the original. A sidecar-only resave keeps the workflow digest and the plan digest |
| 5.7 Conflicts | A save with no base digest returns 409. A stale base digest returns 409, with a summary naming the removed Evaluate node, both removed edges, and `regularization` 2.0 → 0.5. A stale sidecar refuses the whole save, leaving both files unchanged. `compare` returns the same summary, or `changed: false`. A removed file returns 409 with `missing` |
| 5.8 Load refusals | Malformed, unsupported-version, unknown-type, and undecodable files return `422` and are never rewritten. Oversized returns `413`; absent returns `404`. Four bad sidecars degrade to a notice. Phase 1 layout metadata round-trips unchanged (V16) |
| 5.9 Storage | Stray names are not listed. A pre-existing temporary file refuses the write and leaves the disk file unchanged. A symlinked file and a symlinked directory are refused; this part is skipped on Windows when symlinks are not permitted (the run shows that skip) and was exercised in development. Ten malformed sidecars return `422 invalid-sidecar`. Seven bad names return `400 invalid-name`; an encoded separator never matches a route (`404`). Exact fields and digest formats are required |
| 5.10 O3 | Added to `test_slice_output.py`: mismatched read-back is indeterminate, and the record and proof are kept; a rollback failure reports `failed-cleanup-incomplete`, leaving the pending record in place; a partial proof write is reported as failed, with only `record.json`. The existing tests are unchanged apart from one import line widened to include `ArtifactRefusal` |

## 5. Latency (Section 5.11)

With `npm.cmd run launch` running on Windows, the user posted the success
fixture six times to each address:

| Address | Cold (ms) | Warm runs (ms) | Result |
|---|---:|---|---|
| `127.0.0.1:8000` direct | 222 | 31, 37, 35, 37, 38 | 0.9 (36/40) every run |
| `127.0.0.1:5173` (Vite proxy) | 41 | 36, 35, 36, 40, 36 | 0.9 (36/40) every run |

Warm calls take about 36 ms through either address, far below the 2-second
escalation. The cold direct call includes first-request warm-up. A request
with a foreign `Origin` returned HTTP 403 through the live server. Afterwards:

- all 12 attempts were removed by recorded ID ("removed 12");
- after the user stopped `launch`, no listener remained on ports 8000 or 5173;
- `.vidap-local/` holds only an empty `runs/`.

## 6. Paths changed

| Path | SHA-256 |
|---|---|
| `python/src/vidap_execution/app.py` | `9AFF3BB74BADDDD349B18A547F0494E58BD8D3590179065E9ECD0236F02F6970` |
| `python/src/vidap_execution/slice_api.py` (new) | `40D30B24D5E4B17F04D4FAAFB3167EF2BD5C7A82ABAEE25C0810C1CEA1E12C32` (Revision 2) |
| `python/src/vidap_execution/workspace.py` (new) | `4F023E589BAF5E118462F261D180995F56511A832CC95CEF724E17912D10805E` (Revision 2) |
| `python/tests/test_slice_api.py` (new) | `8D7F54FC42B310B5AD5F576FC9B46BDB932FA7552D4B324A4412ABDAC86A4BF5` |
| `python/tests/test_slice_workspace.py` (new) | `D07D5EBB503E80AF79EB8D1D096894997F9E011045A0A07EB85353B5D223297B` (Revision 2) |
| `python/tests/test_slice_output.py` | `FC713F2D889D36580A48B637AECBCDF07B50A1DFD13D00946D4FDF8D13F6B39B` |

The other changed paths:

- `.gitignore`: a comment naming `.vidap-local/runs/` and `.vidap-local/workflows/`; the rule itself is unchanged.
- `CONTRIBUTING.md`: the channel's properties and the named local-state uses.
- `README.md`: the current-state line.

The P3-EP03B source files were confirmed byte-identical, by hash, before and
after this work. No Phase 1 code, slice operation, run, or artifact file;
fixture; lock; script; CI; or web file changed.

## 7. Deviations and notes for the validator

1. **`413 workflow-too-large` on load** (Section 3).
2. **`500 metrics-readback-failed`**, a new fixed code (Section 2).
3. **One intermittent failure in an existing Phase 2 test.**
   - What happened: in the user's first attestation run,
     `test_write_and_terminal_failure_are_bounded` failed once during
     `npm.cmd run check`. A record that should have been terminal still read
     as pending.
   - Rerun evidence: the same test passed in that run's `coverage` step, in
     15 consecutive isolated repeats (0 failures), and in a complete
     attestation rerun.
   - Code impact: EP03C does not touch that test or any code it uses.
   - Likely cause (unconfirmed): a transient Windows lock, for example the
     checkout's OneDrive sync or antivirus briefly holding `record.json`
     during the atomic replace.
   - Recommendation: Central may want to note it for P3-EP06.
4. **Symlink refusal coverage on Windows.** The storage test's symlink part
   is skipped where Windows denies symlink creation. On Windows that leaves
   the reparse-point check exercised only by code inspection.

## 8. Final attestation

**Revision 1.** The user's first ordered run had one failure (Section 7.3),
so the user ran the complete sequence again on the unchanged tree. Every
step passed: unit 151 passed and 1 skipped, integration 49 passed and 1
skipped, and coverage 200 passed and 2 skipped at 89%.

**Revision 2.** Revision 2 changed `slice_api.py`, `workspace.py`, and
`test_slice_workspace.py`, so the user ran the complete sequence again on
the final tree, in Windows PowerShell from the repository root:

| Command | Exit | Evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | "All checks passed!"; mypy "no issues found in 24 source files"; web 10 passed; Python unit 151 passed, 1 skipped; integration 56 passed, 1 skipped |
| `npm.cmd run coverage` | 0 | Web 87.5% of statements; Python 207 passed, 2 skipped, 89% total |
| `npm.cmd run deps:inventory` | 0 | Completed |
| `npm.cmd run license:check` | 0 | "License policy passed for 438 installed locked packages" |
| `npm.cmd run deps:audit` | 0 | npm 0 vulnerabilities of 432; Python "No known vulnerabilities found" |
| `git --no-pager diff --check` | 0 | No output |

**Locks.** Unchanged: `FB7119F6…82FA` and `8030A7C4…0A25`.

**Repository state.** Nothing is staged. `git status` shows 38 entries: the
Revision 1 set, unchanged in membership. `.vidap-local/` holds only an empty
`runs/`.

**Skips.** Two:

- the host-dependent symlink test Phase 2 already accepted;
- the new storage test's symlink part (Section 7.4).

**Latency.** The Section 5 latency evidence stands. Revision 2 did not
change the run path: the run endpoint, the run lock, metrics readback, and
the slice operations are untouched.

**Checked directly.** LF line endings, no trailing whitespace, final
newlines, and no user paths or secrets. Before writing back, the worker
confirmed that the three changed files were the only ones differing from
the repository; every other Python source and test file was identical by
hash. Nothing was staged, committed, or pushed.

## 9. Worker self-assessment

| Criterion | Assessment |
|---|---|
| EP03C-AC01 | Met. |
| EP03C-AC02 | Met. |
| EP03C-AC03 | Met. |
| EP03C-AC04 | Met. |
| EP03C-AC05 | Met. |
| EP03C-AC06 | Met. |
| EP03C-AC07 | Met (Revision 2 closes R1). |
| EP03C-AC08 | Met. |
| EP03C-AC09 | Met. |
| EP03C-AC10 | Met, with the `413` note (Revision 2: a hostile sidecar on disk degrades to a notice). |
| EP03C-AC11 | Met; the Windows symlink case is by inspection. |
| EP03C-AC12 | Met. |
| EP03C-AC13 | Met: about 36 ms warm. |
| EP03C-AC14 | Met on the complete Revision 2 rerun. |
| EP03C-AC15–AC16 | Not self-assessed. |

## 10. Independent-validation handoff

Please read the packet, its inputs, and this report, and check the actual
delta. Drive every endpoint with hostile inputs, including:

- hosts, origins, content types, chunked oversized bodies, and duplicate
  JSON names;
- names and path-encoding tricks;
- crafted sidecars;
- concurrent runs;
- outside edits between load and save;
- stale sidecar digests;
- metrics readback when publication fails or is tampered with.

Recompute digests and summaries independently. Assess the deviations and
notes in Section 7, especially whether the intermittent Phase 2 test failure
needs action. Confirm there is no UI, CORS, background job, or new
dependency. Return `Accept`, `Revise`, or `Blocked`. This worker does not
validate its own work or accept anything for Central.

## 11. Response to independent `Revise`

| Item | Revision 2 change | Regression proof |
|---|---|---|
| R1: deeply nested JSON in `PUT` or `compare` | `_parse` treats `RecursionError` as `400 malformed-json` | `test_crafted_bodies_keep_the_error_envelope`: deep wrapper and deep sidecar bodies, for both `PUT` and `compare` |
| R1: `1e400` in a posted workflow | `_parse` refuses any float that overflows to infinity (`parse_float`), giving `400 malformed-json`; `_nested_document` also wraps re-encoding errors | Same test, "overflowing float in workflow" |
| R1: 400-digit integer as a sidecar number | `_number` compares integers exactly against the bounds before converting, so `OverflowError` cannot occur; float inputs are still checked for finiteness | Same test: ±10^400, 2^63, and ±100001 give `422 invalid-sidecar`, and no file is written |
| R1 / AC10: hostile sidecar already on disk | Load treats `RecursionError` like other unreadable sidecars: the workflow still loads with `sidecarNotice: "unreadable"` | `test_crafted_files_on_disk_still_load_or_refuse_cleanly`: a huge-integer sidecar, a deep array, and a deep object each load with the notice; deep workflow files return `422` and are never rewritten |
| R2: partial save with a stale sidecar temporary file | Before writing anything, `save` checks both temporary files (the workflow's, and the sidecar's when one will be written). A leftover refuses the whole save with both files unchanged | `test_a_stale_sidecar_temporary_refuses_the_whole_save`: refused with the workflow, sidecar, and leftover unchanged; succeeds once the leftover is removed |
| Observation 1: oversized file on `compare` | `compare` and `save` now read the disk workflow with the same size bound as `load`, and refuse with `413 workflow-too-large`. Before this, both read it without a bound, and `compare` returned `200` | The on-disk test covers both `compare` and `save` |
| Observation 3: Windows device names | `check_name` refuses `con`, `prn`, `aux`, `nul`, `com1`–`com9`, and `lpt1`–`lpt9` | `test_invalid_names_are_refused` adds `con`, `nul`, `com1`, `lpt9` |
| Also | Sidecar digests are computed in 64 KiB chunks rather than reading the whole file into memory | Covered by the existing load, compare, and conflict tests |

**Left unchanged**, for Central:

- **Observation 2:** a malformed body on `validate`/`run` returns `422 invalid-workflow`, following packet §§4.2 and 5.2.
- **Observation 4:** one symlinked sidecar makes the listing return `500 storage-refused`; this fails safe.
- **Observation 5:** the `.gitignore` comment.
- **Observation 6:** the intermittent Phase 2 test.

The test count rose from 200 to 207 in the full Python run.
