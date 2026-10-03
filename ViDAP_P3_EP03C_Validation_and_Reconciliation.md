# ViDAP P3-EP03C — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03C.md` version 0.1, approved 2026-10-02 |
| Worker report | `ViDAP_P3_EP03C_Implementation_Report.md` (Revision 2) |
| Report SHA-256 at reconciliation | `2DA295CC30EABEA9CF453953CB5646A797D61CBC5A3D746E44A584312794AA42` |
| Independent-validation verdict | Accept on Revision 2, after one `Revise` (R1 blocking, R2 recommended); no unresolved finding |
| Central decision | P3-EP03C accepted; EP03C-AC16 satisfied; WS3.3 (backend slice) complete |
| Baseline HEAD | `17652fc28eafa0b8e2b5be58c55df9ced0d7afff` on `main` |
| Reconciliation date | 2026-10-02 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied both verdicts:

- **Revision 1:** `Revise`, after the validator attacked every endpoint.
- **Revision 2:** `Accept`.

The validator re-checked the revised tree on its own copy (Python 3.13, the
locked numeric packages, and a POSIX stand-in for the Windows-only run
folders). Any unhandled exception was made to fail the harness.

**Earlier findings, re-checked:**

- **R1 (crafted inputs returned a bare 500):** fixed. Every R1 input now
  returns its fixed envelope, and a hostile sidecar on disk now loads with
  `sidecarNotice` (AC10).
- **R2 (partial save after a refusal):** fixed. A leftover temporary file
  refuses the whole save, with both files unchanged.
- **Observation 1 (`compare` and `save` read an oversized file):** now
  refused with `413`.
- **Observation 3 (Windows device names):** refused, while look-alike names
  are still allowed.

**Regression checks.** All 84 slice and app tests passed. The validator
re-ran its own probes with unchanged results:

- the guards;
- five concurrent runs;
- metrics readback, including the tampered-slot case;
- the bypass failure;
- the indeterminate publication case;
- change summaries checked against its own computation;
- stale-sidecar refusals;
- save, load, and run fidelity.

**Scope and state.**

- The three changed files and the report match their hashes.
- Every other changed file, both locks, and all four fixtures are
  byte-identical to the Revision 1 tree.
- The run path is untouched.
- The tree has 38 status entries and nothing staged; `diff --check` is clean;
  there is no `.git/index.lock`.
- `.vidap-local/` holds only an empty `runs/`.

This satisfies EP03C-AC01–EP03C-AC15.

## 2. Central evidence check

Central confirmed the following before writing this record. Central did not
rerun the attestation.

- **Repository state:** `HEAD` is unchanged; there are 38 status entries and
  nothing is staged.
- **Lock files:** `package-lock.json` is `FB7119F6…82FA` and
  `python/uv.lock` is `8030A7C4…0A25`, matching P3-EP03B.
- **Report:** its hash is in the table above.
- **Accepted source files:**

| File | SHA-256 |
|---|---|
| `python/src/vidap_execution/app.py` | `9AFF3BB74BADDDD349B18A547F0494E58BD8D3590179065E9ECD0236F02F6970` |
| `python/src/vidap_execution/slice_api.py` | `40D30B24D5E4B17F04D4FAAFB3167EF2BD5C7A82ABAEE25C0810C1CEA1E12C32` |
| `python/src/vidap_execution/workspace.py` | `4F023E589BAF5E118462F261D180995F56511A832CC95CEF724E17912D10805E` |
| `python/tests/test_slice_api.py` | `8D7F54FC42B310B5AD5F576FC9B46BDB932FA7552D4B324A4412ABDAC86A4BF5` |
| `python/tests/test_slice_workspace.py` | `D07D5EBB503E80AF79EB8D1D096894997F9E011045A0A07EB85353B5D223297B` |
| `python/tests/test_slice_output.py` | `FC713F2D889D36580A48B637AECBCDF07B50A1DFD13D00946D4FDF8D13F6B39B` |

- **Windows evidence:** the user's Revision 2 run is in report Section 8. It
  shows `check` and `coverage` passing (207 Python tests, 2 skips), all
  controls clean, and warm latency of about 36 ms through both addresses.

## 3. Accepted

- **The `/api/slice/` channel** in the loopback shell:
  - Routes: contracts, validate, run, list, load, save, compare.
  - Guards: host, origin, content type, size, and strict JSON.
  - Errors: one fixed envelope.
  - Absent: CORS, OpenAPI, and docs.
- **Host check scope.** The router-level host check applies to slice routes
  only (packet §4.1), so `/api/status` is unchanged.
- **Recorded results only.** Run metrics come only from exact readback of
  the owned slot. A failed, tampered, or indeterminate publication returns no
  metrics.
- **One run at a time.** A concurrent run is refused with `409 busy`; it is
  not queued.
- **Backend-owned files** under `.vidap-local/workflows/`:
  - saved bytes are canonical serializer output;
  - every save is checked against the base digests of both files;
  - change summaries are built by the backend;
  - writes are atomic and are refused as a whole;
  - a bad sidecar degrades to a notice;
  - V15 and V16 hold.
- **Two error codes added beyond the packet's list:**
  - `413 workflow-too-large`, for an oversized saved file on load, compare,
    and save;
  - `500 metrics-readback-failed`.
- **The three O3 slice publication tests** carried from P3-EP03B.
- **Endpoint latency:** about 36 ms warm, directly and through the Vite
  proxy. The D3.2 2-second escalation does not fire, so the synchronous
  channel stands for P3-EP05.

## 4. Observations dispositioned

| Item | Central disposition |
|---|---|
| A malformed body on `validate`/`run` returns `422 invalid-workflow`, not `400 malformed-json` | **Central reading recorded.** Packet §4.1's `malformed-json` applies to the bodies the channel parses itself: the save and compare wrappers, and invalid UTF-8. The document bodies of `validate` and `run` go straight to the strict Phase 1 decoder, and a decode failure returns `422 invalid-workflow` with that finding, as §§4.2 and 5.2 state. The packet is not edited. |
| One symlinked sidecar makes `GET /workflows` return `500` | Accepted. It fails safe, and a per-entry notice can come later if needed. |
| The `.gitignore` comment also names `runs/` | Accepted; it is accurate and only a comment. |
| An existing Phase 2 test failed once on Windows (`test_write_and_terminal_failure_are_bounded`) | **Carried to P3-EP06.** It passed 15 isolated repeats and every later run. The likely cause is a transient lock on the OneDrive-synced checkout. P3-EP06 should watch for it and, if it recurs, investigate a retry or a non-synced run location. |
| The Windows symlink and reparse-point refusal is checked by inspection only (tests skip there; Linux exercised it) | **Carried to P3-EP06**, for a Windows check where symlink creation is permitted (for example, Developer Mode). |
| Run records accumulate under `.vidap-local/runs/` | As accepted in the packet: retention is a later decision. P3-EP05 should note it when the editor starts creating runs. |

## 5. Central decision and next boundary

Central accepts P3-EP03C v0.1, and EP03C-AC16 is satisfied. **WS3.3 is
complete.** Through one guarded local channel, the backend slice can:

- describe its operations;
- validate a workflow;
- run it and return recorded results with plain-English failures;
- save and reload workflows safely.

P3-EP04 (editor core, WS3.4) is now ready to draft. It needs its own approval
before any work. It must carry:

- these accepted channel contracts;
- D3.4–D3.9 and `DESIGN.md` v0.2;
- the design items carried from P3-EP02: the jsx-a11y-x evaluation, keyboard
  connecting, React Flow arrow-key node moving, Decision Record 0002 as an
  input, N2–N5, and the `DESIGN.md` status update.

Nothing in this record changes a source file, lock, or remote state, and
nothing was staged, committed, or pushed.
