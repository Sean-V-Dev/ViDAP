# ViDAP P3-EP03B — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03B.md` version 0.1, approved 2026-10-02 |
| Worker report | `ViDAP_P3_EP03B_Implementation_Report.md` |
| Report SHA-256 at reconciliation | `21BDD6C63897F5439DB77426163B16ECB7F78C9E00298144CA97A9F21B62D1FD` |
| Independent-validation verdict | Accept, first round; three non-blocking observations |
| Central decision | P3-EP03B accepted; fixture bytes accepted; EP03B-AC13 satisfied |
| Baseline HEAD | `17652fc28eafa0b8e2b5be58c55df9ced0d7afff` on `main` |
| Reconciliation date | 2026-10-02 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied the independent `Accept`. The validator checked the actual
delta against `HEAD`, outside the checkout, on a copy running the locked
scikit-learn 1.9.1, numpy 2.5.3, and scipy 1.18.1. The only change in that
copy was the syntax back-port for its older Python, plus a POSIX stand-in for
the Windows-only run-folder layer.

What the validator recomputed:

- the fixture and manifest hashes;
- the lock delta: exactly the seven P3-EP03A packages, with nothing removed or
  re-versioned;
- the embedded Record 0005 value (46,555 bytes, Appendix A digest) and the
  numpy key.

The validator also confirmed that the gate:

- checks the digest before the scipy entry exists;
- consults the new catalog only after Records 0003 and 0004.

The validator calculated five cases independently from the CSV, and each
matched the recorded bytes:

| Case | Accuracy |
|---|---|
| Defaults | 0.9 |
| `regularization` 0.0001 | 0.55 |
| `seed` 7 | 0.85 |
| `test_fraction` 0.5 | 0.85 |
| `missing_fill` 5.0 | 0.875 |

The validator also confirmed, through its own challenges:

- the exact `C` value reaches `LogisticRegression`;
- Prepare learns nothing from the rows;
- shared reuse of Split's output;
- the bypass failure;
- the declared and undeclared failure mapping;
- the refusals before allocation;
- the fail-closed check on a tampered fixture;
- two extra publication cases (mismatched read-back and rollback failure).

Windows-specific behavior rests on the user's Windows run, recorded in
Section 9 of the report.

**Validator-side incident.** A `git status` left an empty `.git/index.lock`.
The validator removed it with the user's permission, along with its own
temporary files. Central confirmed that the lock file is absent,
`.vidap-local/runs/` is empty, and the working tree has the same 29 entries
as before validation.

This satisfies EP03B-AC01–EP03B-AC12.

## 2. Central evidence check

Central confirmed the following before writing this record. Central did not
rerun the attestation.

- **Repository state:** `HEAD` is unchanged and nothing is staged.
- **Locks:**
  - `package-lock.json`: `FB7119F6…82FA`, unchanged.
  - `python/uv.lock`: `8030A7C4…0A25`, the accepted lock change.
- **Worker report:** its hash, in the table above.
- **Accepted fixture bytes:**

| File | SHA-256 |
|---|---|
| `fixtures/p3-ep03b/slice-dataset-v1.csv` | `30EF03B9A552AF2482A87D087B170C777629D72EE4247C3A4F1822570A0FC5FF` |
| `fixtures/p3-ep03b/slice-success-v1.json` | `EC853D200FEDD5B1E3D158B327CA248144EA9F5C18E42465F840DFFE94D408DB` |
| `fixtures/p3-ep03b/slice-bypass-prepare-v1.json` | `FFF38ABA4E35D3C7E11EBD9220327086BB42BB8739B1C3D4133D215C15947307` |
| `fixtures/p3-ep03b/fixture-manifest.json` | `D9C90732DAE2C34E59169F59C0947E4D4144E3CA7E7BA9B0BFD760A8960189D0` |

The manifest's `byteReviewStatus` still reads "pending". As with P2-EP05,
this record is the byte-level acceptance, and the manifest is not edited.

## 3. Accepted

- **The slice dependency:** `scikit-learn==1.9.1` and its seven-package lock
  delta, governed by Decision Record 0005.
- **The Record 0005 gate catalog**, as implemented.
- **The five slice operations and contracts.** This includes Prepare's
  `prepared` output port key, which is needed because Phase 1 requires port
  keys to be unique within a node. Its nominal type is still `table`.
- **The `vidap.slice-metrics` 1.0 output authority (F1)** and the closed
  declared failure list (F6), exactly as implemented.
- **The controlled fixture bytes** listed in Section 2.
- **Headless latency:** about 30 ms per warm run on Windows. The D3.2
  2-second escalation does not fire.

## 4. Observations dispositioned

| Item | Central disposition |
|---|---|
| O1: the gate's role and re-review strings are worded slightly differently from Record 0005 | Accepted as is. The meaning is identical, and the "Re-review on…" form follows the implementation precedent of Record 0004. Any later edit to these strings must keep that meaning. |
| O2: the report says Git converts the `.ps1` on checkout | Superseded here. The working copy has LF line endings. Git applies the `.ps1` `eol=crlf` attribute only when it writes the file on a fresh checkout. Keeping the LF working copy was correct. The validated report is not edited. |
| O3: three P2-EP05 §4.2 publication challenges were not repeated as slice tests (mismatched read-back, rollback failure, partial proof write) | The publication code is shared with the reference proof, and the validator ran the first two by hand for the slice. **Carried to P3-EP03C:** it must add these three as slice tests. |

## 5. Central decision and next boundary

Central accepts P3-EP03B v0.1, and EP03B-AC13 is satisfied. The slice now runs
headlessly; it has no endpoint, persistence, or UI yet.

P3-EP03C is now ready to draft. Its scope is:

- the `/api/slice/` channel (D3.2), with its host, origin, content-type,
  size, and single-run limits;
- workflow and sidecar save/load under `.vidap-local/workflows/` (D3.3, D3.4,
  F3, V15, V16);
- endpoint latency evidence;
- the O3 tests.

P3-EP03C needs its own approval before any work. Nothing in this record
changes a lock, manifest, or source file, or stages, commits, or pushes.
