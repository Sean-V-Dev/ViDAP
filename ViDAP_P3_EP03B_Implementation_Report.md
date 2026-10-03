# ViDAP P3-EP03B — Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03B.md` v0.1, explicitly approved by the user 2026-10-02 |
| Worker execution | 2026-10-02; Linux shells over the Windows checkout. The lock change, setup, and all Windows checks were run by the user under the `CONTRIBUTING.md` workaround |
| Worker result | Implementation complete; final attestation passed (Section 9); ready for independent validation |
| Independent validation | Pending; this report is not a verdict |
| Central decision | Pending; this report does not accept the packet or the fixture bytes |

## 1. Approval and baseline

Before writing, the baseline was:

- branch `main`, `HEAD` `17652fc28eafa0b8e2b5be58c55df9ced0d7afff`, nothing staged;
- `package-lock.json` `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA`;
- `python/uv.lock` `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355`;
- pre-existing Central-owned changes: the modified `ViDAP_P3_EP03A.md`, `ViDAP_Phase_3_Plan.md`, and `ViDAP_Roadmap.md`, plus the untracked `ViDAP_P3_EP03A_Dependency_Review.md`, `ViDAP_P3_EP03A_Validation_and_Reconciliation.md`, `ViDAP_P3_EP03B.md`, and `docs/decisions/0005-p3-slice-numeric-runtime-license-disposition.md`;
- no Section 8 path existed.

**Development environment note.** PyPI is blocked from both worker shells, and
the repository needs CPython 3.14. During development the worker ran the code
and tests against scikit-learn 1.8.0 on CPython 3.11, on a mechanically
back-ported copy outside the repository, with a POSIX stand-in for the
Windows-only artifact layer. That run was development feedback only. All
evidence below comes from the user's Windows runs on the locked environment
(CPython 3.14 and scikit-learn 1.9.1).

## 2. Lock delta (Section 5.1)

The worker edited `python/pyproject.toml`. The user then ran
`uv --directory python lock` (exit 0) and `npm.cmd run setup` (exit 0;
"Resolved 64 packages"). The script compared the locked package lists with
`HEAD`: 57 packages before, 64 after.

| Added | Version |
|---|---|
| cloudpickle | 3.1.2 |
| joblib | 1.6.0 |
| narwhals | 2.26.0 |
| numpy | 2.5.3 |
| scikit-learn | 1.9.1 |
| scipy | 1.18.1 |
| threadpoolctl | 3.7.0 |

No package was changed or removed. The delta is exactly P3-EP03A's Section 4,
and the worker confirmed it separately from the file.

- New `python/uv.lock`: `8030A7C44776A9CB0BE51E4528ECC917D10CB0C67790CD76EAEB037960080A25`.
- `package-lock.json`: unchanged.

The `pyproject.toml` change is exactly the dependency pin
`"scikit-learn==1.9.1"` plus one `[[tool.mypy.overrides]]` for `sklearn` and
`sklearn.*` with `ignore_missing_imports = true`. mypy stays strict
elsewhere and reported "no issues found in 22 source files".

## 3. License catalog (Record 0005)

`scripts/dependency-controls.ps1` gains a separate function,
`Get-Decision0005CatalogEntry`. `Get-LicensePolicyResult` consults it only
after the Record 0003 and 0004 catalogs return nothing.

- The function holds exactly two literal keys:
  - `numpy|2.5.3|BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0`;
  - `scipy|1.18.1|<Appendix A value>`.
- The scipy value is embedded as base64. It is decoded and hashed with
  SHA-256 every time the function runs. Only on an exact match with
  `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E` is the
  value decoded with UTF-8 and the scipy entry added. Otherwise the entry is
  absent and the gate fails closed.
- Keys use the untrimmed gate value, as the existing catalogs do.
- The user's read-only check of the embedded base64 printed
  `bytes=46555 sha256=7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`.
- The role and re-review text follow Record 0005, written in the
  "Re-review on…" form that Record 0004's implementation uses.

The real `license:check` output reported both entries:

- `python allowed numpy@2.5.3 … record=0005 …`
- `python allowed scipy@1.18.1 … record=0005 …`
- "License policy passed for 438 installed locked packages".

That is 431 before plus the 7 new packages. No other change in disposition
was reported.

**Line endings (deviation note).** The packet said to keep the script's CRLF
line endings. The working-tree file actually has LF line endings; Git
converts it on checkout because `.gitattributes` gives `*.ps1` the attribute
`eol=crlf`. The worker kept the existing LF working-tree endings unchanged,
which is what "keep the file's line endings" requires in practice.

## 4. Slice contracts (Section 5.3)

`python/src/vidap_execution/slice.py` adds a separate static family: its own
registry, binding map, and runtime table. Every binding and the map use the
exact revision `vidap.slice.bindings.v1`. The entry point is
`run_slice_attempt(document, *, seed=None)`. `BUILTIN_NODE_REGISTRY` and the
reference family are not changed. `run_slice_attempt` is not re-exported
from `vidap_execution/__init__.py`, so importing the package does not load
scikit-learn. That file is unchanged.

| Node type | Ports (key: nominal type) | Parameters (kind, range, default) | Library mapping |
|---|---|---|---|
| `vidap.slice.dataset` | out `table`: table | none | stdlib `csv`, after a size and SHA-256 check of the fixed fixture |
| `vidap.slice.prepare` | in `table`: table → out `prepared`: table | `missing_fill` (number, −1e6–1e6, 0.0) | `SimpleImputer(strategy="constant", fill_value=missing_fill)`; `OneHotEncoder(categories=[declared list], sparse_output=False, handle_unknown="error")` |
| `vidap.slice.split` | in `table`: table → out `split`: split | `test_fraction` (number, 0.1–0.5, 0.25); `seed` (integer, 0–4294967295, 0) | `train_test_split(row indices, test_size, random_state=seed, stratify=label)` |
| `vidap.slice.model` | in `split`: split → out `model`: model | `regularization` (number, 0.0001–10000, 1.0) | Declared checks, then `LogisticRegression(C=regularization)` with library defaults |
| `vidap.slice.evaluate` | in `model`: model, in `split`: split → out `metrics`: metrics | none | `predict`; `accuracy_score`; counts |

**Deviation note: Prepare's output port key.** The packet's table wrote
Prepare's ports as "`table` → `table`". Phase 1 contracts require port keys
to be unique within a node across inputs and outputs, so the output key is
`prepared`. Its nominal type is still `table`. No Phase 1 change was made.

**Behaviour that applies to every node:**

- **Declared schema.** Tables carry their schema: name, kind
  (numeric, category, target), nullability, and category list. Dataset
  parses strictly by the declared schema. It refuses a header, field count,
  category, target, missing value, or non-finite number that does not match.
- **Values carried between nodes.**
  - Tables, splits, fitted models, and metrics travel as `TrustedValue`s.
  - Each content digest is SHA-256 of canonical JSON. For tables and
    splits it covers the schema and column data. For models it covers the
    implementation, scikit-learn version, `C`, features, classes,
    coefficients, and intercept. For metrics it covers the counts and
    accuracy.
- **Parameter checks.** Handlers re-check parameter keys, numeric kinds,
  and ranges. Booleans are refused as numbers.
- **Inputs and side effects.** Handlers require exactly their declared
  inputs. They hold no global state and make no writes or network calls.
  Only Dataset reads a file, and only the fixed fixture.
- **Randomness.** `seed` is the only randomness. The attempt-level seed is
  recorded but never passed to a handler.

## 5. Output authority and declared failures

**F1, the `vidap.slice-metrics` 1.0 output.**

- `output.py` adds the following:
  - `SliceMetrics`: accuracy (finite float), correct, and test-row counts.
    It refuses invalid counts and any accuracy that is not exactly
    `correct / testRows`.
  - `evaluate_node_id`: exactly one terminal Evaluate node.
  - `metrics_bytes` and `selected_metrics_bytes`.
- The bytes are compact UTF-8 JSON with sorted keys, which for these fixed
  ASCII keys is UTF-16 order.
- `run.py` adds a private `_slice_output` selector beside
  `_reference_output`. Each selector is tied by identity to its own
  registry, bindings, and runtime table. Setting both refuses.
- The slot, the publication sequence, and the commit-point readback and
  indeterminate handling are unchanged and shared with the reference proof.
  Every existing reference test passes unchanged.

**F6, declared failure codes.**

- `diagnostics.py` adds the closed list `DECLARED_FAILURES`, with the
  packet's exact text for `unencoded-category-input` and
  `missing-value-input`. It also adds `DeclaredFailure`, whose constructor
  refuses any other code, and `declared_code`.
- `declared_code` returns a declared code only when the exception's type is
  exactly `DeclaredFailure` and its code is on the list. Otherwise it
  returns `handler-failed`.
- `dispatch.py` uses `declared_code(error)` in place of the fixed
  `handler-failed` at the handler-exception boundary.
- The category stays `execution`, and the technical message stays withheld.

## 6. Fixture

| File | Bytes | SHA-256 |
|---|---:|---|
| `fixtures/p3-ep03b/slice-dataset-v1.csv` | 3,260 | `30EF03B9A552AF2482A87D087B170C777629D72EE4247C3A4F1822570A0FC5FF` |
| `fixtures/p3-ep03b/slice-success-v1.json` | 1,806 | `EC853D200FEDD5B1E3D158B327CA248144EA9F5C18E42465F840DFFE94D408DB` |
| `fixtures/p3-ep03b/slice-bypass-prepare-v1.json` | 1,467 | `FFF38ABA4E35D3C7E11EBD9220327086BB42BB8739B1C3D4133D215C15947307` |
| `fixtures/p3-ep03b/fixture-manifest.json` | 3,937 | `D9C90732DAE2C34E59169F59C0947E4D4144E3CA7E7BA9B0BFD760A8960189D0` |

**The dataset.**

- Rows:
  - 160 rows;
  - `label` = 1 in 74 rows (46%);
  - `feature_b` empty in 13 rows (8%);
  - `segment` takes only the values `north`, `south`, and `east`.
- Generation: `python/tests/slice_fixture_generator.py`, generator version
  1.0, standard-library `random.Random(20261002)`. A test regenerates the
  file and compares it byte for byte.
- Integrity: the manifest records D0.7 metadata, synthetic provenance, MIT
  terms, `synthetic non-sensitive`, the expected results, and a pending
  byte-level review status.
- Size: the fixtures directory totals 23,695 bytes, under 64 KiB.
- Line endings: `.gitattributes` gains `*.csv text eol=lf`.

**Expected results, computed independently in the tests from the CSV with
scikit-learn directly:**

- default parameters: accuracy 0.9, 36 of 40 correct;
- `regularization` 0.0001: accuracy 0.55, 22 of 40 correct.

## 7. Proof (Section 6)

All 23 new tests ran in the user's `check` and `coverage` runs. Unit tests
went from 125 to 148 passing, and coverage from 128 to 151.

| Section 6 item | Evidence |
|---|---|
| 6.1 Success | `test_success_matches_independent_calculation`: outcome succeeded, 5 nodes complete, envelope equals an independent scikit-learn calculation and the manifest; Split's output computed once and consumed by both Model and Evaluate (reuse events) |
| 6.2 Parameter at the call | `test_regularization_reaches_the_library_call`: a spy subclass of `LogisticRegression` records `C` = 1.0, then 0.0001; the recorded accuracy is 0.9 against 0.55, matching the independent calculation |
| 6.3 Repeat and change | Identical runs get new attempt IDs with byte-identical metrics. `seed`, `test_fraction`, and `missing_fill` each change the semantic digest; labels and layout do not. A run with seed 7 matches its independent calculation |
| 6.4 Bypass failure | `test_bypassing_prepare_fails_on_model_with_its_real_cause`: Dataset and Split complete, Model fails with `unencoded-category-input` and its fixed text, Evaluate is blocked, the record is the only artifact. `missing-value-input` is proven at the handler (category is checked first) and through dispatch. A `RuntimeError`, an off-list code, a subclass, and a tampered code all give `handler-failed` without leaking text |
| 6.5 Refusals | A missing Evaluate, duplicated Evaluate, type-invalid connection (`split` into Evaluate's `model` input), and out-of-range `regularization`, `test_fraction`, and `seed` all refuse, and the runs directory is unchanged. In the slice registry no input accepts `metrics`, so a valid non-terminal Evaluate cannot be built; that case is covered by the terminal check in `evaluate_node_id` |
| 6.6 Fixture integrity | Generator reproduction; manifest hashes and sizes; bounds. A changed byte refuses before the CSV is parsed (spy proves `csv.reader` is never called). A tampered fixture fails the Dataset node with `handler-failed` and no metrics |
| 6.7 Publication | A proof-write failure and a terminal-publication failure stay failed or pending; a post-commit error reports the verified success; an unreadable commit raises `PublicationIndeterminate`, leaving the record and proof in place; a failed slice commits no metrics; the generic entry publishes no metrics; authorities are fixed and exclusive |
| 6.8 License gate | Section 3 |
| 6.9 Latency | Section 8 |

## 8. Latency (D3.2 escalation)

The user timed six headless runs of the success fixture on Windows, each
with a fresh attempt that was then removed by its ID:

| Run | Wall time (ms) | Recorded `elapsedMs` | Metrics |
|---|---:|---:|---|
| 0 (cold) | 46 | 39 | 0.9 (36/40) |
| 1 | 37 | 30 | 0.9 (36/40) |
| 2 | 35 | 30 | 0.9 (36/40) |
| 3 | 31 | 25 | 0.9 (36/40) |
| 4 | 34 | 28 | 0.9 (36/40) |
| 5 | 29 | 22 | 0.9 (36/40) |

A typical warm run takes about 30 ms, far below the 2-second escalation
threshold. These timings exclude the one-time scikit-learn import in a fresh
process. Endpoint latency belongs to P3-EP03C.

## 9. Final attestation

The user ran this on the final tree in Windows PowerShell from the repository
root, after every worker change.

| Command | Exit | Evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | "All checks passed!"; mypy "no issues found in 22 source files"; web 10 passed; Python unit 148 passed, 1 skipped, 3 deselected; integration 3 passed |
| `npm.cmd run coverage` | 0 | Web 87.5% of statements; Python 151 passed, 1 skipped, 88% total |
| `npm.cmd run deps:inventory` | 0 | Completed |
| `npm.cmd run license:check` | 0 | Record 0005 matches for numpy and scipy; "License policy passed for 438 installed locked packages" |
| `npm.cmd run deps:audit` | 0 | npm 0 vulnerabilities of 432; Python 64 resolved, "No known vulnerabilities found" |
| `git --no-pager diff --check` | 0 | No whitespace errors |

**Locks.**

- `package-lock.json`: `FB7119F6…82FA`, unchanged.
- `python/uv.lock`: `8030A7C4…0A25`, the Section 2 change.

**Repository state.** Nothing is staged. `git status` shows exactly:

- the Section 8 paths;
- the Section 1 Central-owned files;
- the Central approval edits made before the work started: the
  `ViDAP_P3_EP03B.md` status, and the WS3.3 row and next action in the plan
  and roadmap.

The one Python skip is the host-dependent symlink test that Phase 2 already
accepted.

**Checked directly by the worker:**

- Every changed file has LF line endings, no trailing whitespace, and a
  final newline.
- No user paths or secrets.
- `.vidap-local/runs/` is empty after the tests and the timing run.

No setup, install, or package command ran against the checkout from a Linux
shell. Nothing was staged, committed, or pushed.

## 10. Worker self-assessment

| Criterion | Assessment |
|---|---|
| EP03B-AC01 | Met. |
| EP03B-AC02 | Met: the only worker changes are Section 8 paths; the lock delta equals P3-EP03A exactly. |
| EP03B-AC03 | Met (Section 3). |
| EP03B-AC04 | Met (Section 6). |
| EP03B-AC05 | Met, with the `prepared` port-key note. |
| EP03B-AC06 | Met. |
| EP03B-AC07 | Met. |
| EP03B-AC08 | Met. |
| EP03B-AC09 | Met. |
| EP03B-AC10 | Met: about 30 ms warm. |
| EP03B-AC11 | Met. |
| EP03B-AC12 and EP03B-AC13 | Not self-assessed. |

## 11. Independent-validation handoff

Please read the packet, its governing inputs, and this report, and check the
actual delta. In particular:

1. **Recompute the integrity values.** These cover the fixture and manifest
   hashes, the lock delta against `HEAD`, and the embedded Record 0005
   base64 digest.
2. **Recompute both accuracies.** Recompute 0.9 and 0.55 independently from
   the CSV.
3. **Confirm the library call.** Check that `C` is passed at the
   `LogisticRegression` call and that Prepare learns nothing from the rows.
4. **Challenge the failure paths.** These are the bypass, the declared and
   undeclared failures, the refusal cases, and the publication cases.
5. **Confirm the reference proof is unchanged.** Its bytes and tests must be
   unchanged, and no endpoint, persistence, or UI may have been added.
6. **Assess the two deviation notes.** These are the `prepared` port key and
   the LF line endings of the `.ps1`.
7. **Reproduce or confirm the Windows evidence.**

Return `Accept`, `Revise`, or `Blocked`. This worker does not validate its
own work or accept anything for Central.
