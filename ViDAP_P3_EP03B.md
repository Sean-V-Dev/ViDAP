# ViDAP P3-EP03B — Slice Dependency, Operations, and Headless Run

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Bounded implementation: one runtime dependency, five first-party operations, two narrow Phase 2 extensions, controlled fixture, headless proof |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1, WS3.3 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3/checkpoint A3 |
| Prerequisites | P3-EP01 (D3.1–D3.4, F1, F6 accepted), P3-EP02, and P3-EP03A complete; Decision Record 0005 accepted 2026-10-02 |
| Workstream | WS3.3 — Backend slice (second of three packets) |
| Authorized worker report | `ViDAP_P3_EP03B_Implementation_Report.md` |
| Created | 2026-10-02 |
| Approved | 2026-10-02 by explicit user direction |
| Owner | Central |

---

## 1. Why WS3.3 has a third packet

WS3.3 was split into EP03A (license review) and EP03B (implementation).
The implementation itself has two separable halves with different risks:
the slice's operations and their dependency, and the browser-facing channel
and persistence. Central splits them so each gets focused validation:

- **P3-EP03B (this packet):** add scikit-learn under Record 0005, the
  controlled fixture, the five slice operations, the F1 metrics output and
  the F6 declared failure codes, all proven headlessly through the accepted
  Phase 2 attempt path.
- **P3-EP03C (later):** the `/api/slice/` endpoints (D3.2), workflow and
  sidecar save/load under `.vidap-local/workflows/` (D3.3, D3.4, F3, V15,
  V16), and endpoint latency evidence.

Later packet numbers (EP04, EP05, EP06) are unchanged.

## 2. Authorization Boundary

Approval of this exact version authorizes one bounded worker to change only
the Section 8 paths. The lock change is made by the user on Windows, through
commands the worker supplies under the `CONTRIBUTING.md` workaround; the
worker never runs `uv`, `npm ci`, or setup against the checkout from a
non-Windows shell.

It does not authorize any HTTP endpoint, file persistence of workflows,
sidecar, UI code, other dependency, change to Phase 1 code, change to the
P2-EP05 reference behavior, CI change, staging, commit, push, or the start of
P3-EP03C.

## 3. Plain-English Packet Intent

### What this packet does

It makes the first real machine-learning workflow run headlessly: a small
synthetic CSV is loaded, prepared, split, used to train a logistic
regression model, and evaluated, with the accuracy recorded by the existing
attempt layer.

### Why it is needed

Every later Phase 3 packet (channel, editor, run controls) displays or
drives these operations. Proving them headlessly first keeps the editor
honest: it can only show what the backend computed and recorded.

### How success is demonstrated

Running the controlled success workflow produces a recorded accuracy that
an independent calculation reproduces; changing `regularization` changes
the recorded accuracy; bypassing Prepare Data fails on the Model node with
a plain-English cause and remedy; and the license gate passes on the real
install because Record 0005's literal entries match.

## 4. Governing Inputs

The worker and validator must read: the explicit approval of this version;
`ViDAP_Overview.txt` OV §§18–19; `ViDAP_Phase_3_Plan.md` v1.1 §§5–8;
`ViDAP_P3_EP01_Decision_Report.md` D3.1 (Revision 3) and
`ViDAP_P3_EP01_Validation_and_Reconciliation.md` (D3.1, F1, F6);
`ViDAP_P3_EP03A_Dependency_Review.md` (Revision 2, including Appendix A) and
its reconciliation; Decision Records 0003, 0004, and 0005; accepted D0.6 and
D0.7; `ViDAP_P2_EP05.md` and its reconciliation (the reference output and
publication contract this packet extends); the Phase 2 execution sources;
`docs/dependency-controls.md`; `CONTRIBUTING.md`; and this packet.

## 5. Approved Slice Contract

### 5.1 Dependency and license catalog

- Add exactly `"scikit-learn==1.9.1"` to `[project].dependencies` in
  `python/pyproject.toml`. Add only one `[[tool.mypy.overrides]]` entry,
  for `sklearn` and `sklearn.*`, with `ignore_missing_imports = true`,
  because scikit-learn ships no type information. Keep mypy strict
  everywhere else.
- The user runs `uv --directory python lock` and `npm.cmd run setup` on
  Windows. The lock delta must be exactly the seven packages and versions
  in the P3-EP03A review Section 4, with no existing locked package changed
  or removed. **Any difference is a stop gate**: Record 0005 is
  version-exact.
- In `scripts/dependency-controls.ps1`, add a separate literal catalog
  function for Record 0005, consulted after Records 0003 and 0004, with
  exactly two keys: `numpy|2.5.3|<the 50-character expression>` and
  `scipy|1.18.1|<the Appendix A value>`. Embed scipy's value as base64
  decoded with UTF-8, as Record 0004 does for `pip_api`, and **verify its
  SHA-256 at load** against
  `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`. On a
  mismatch, the catalog must not match and the gate fails closed. Report
  record `0005`, the role, and the re-review trigger exactly as the record
  states. Keep the file's CRLF line endings. Nothing else in the script
  changes.

### 5.2 Controlled fixture

Under `fixtures/p3-ep03b/`:

- `slice-dataset-v1.csv`: UTF-8, LF line endings, at most 16 KiB, 120–200
  rows. Columns in this order:
  - `feature_a`: numeric, no missing values;
  - `feature_b`: numeric, with at least 5% deliberately empty cells;
  - `segment`: category, values exactly `north`, `south`, `east`;
  - `label`: binary target, `0`/`1`, both classes at least 30% of rows.
- A deterministic standard-library generator with a fixed seed and version
  at `python/tests/slice_fixture_generator.py`. A test regenerates the bytes
  and compares them with the committed file.
- `slice-success-v1.json`: a `vidap.workflow` 1.0 document with the five
  slice nodes wired as D3.1 states, at default parameters.
- `slice-bypass-prepare-v1.json`: the same, but Dataset feeds Split
  directly, without Prepare Data.
- `fixture-manifest.json`, in the P2-EP05 style: ID and version, relative
  path, byte size, SHA-256, synthetic provenance, MIT terms, generation
  method, expected results, permitted consumers (P3 packets and their
  validation), privacy classification `synthetic non-sensitive`, and a
  pending byte-level review status.

Add `*.csv text eol=lf` to `.gitattributes` so Windows checkouts keep the
hashed bytes. The fixture design must make a very small `regularization`
(for example `0.0001`) record a different accuracy from the default; the
worker tunes the generator, not the handlers, to achieve that.

### 5.3 The five operations

A new first-party module provides a separate static registry, binding map,
and runtime table (one exact binding revision, `vidap.slice.bindings.v1`,
used for every binding and the map), and the entry
`run_slice_attempt(document, *, seed=None)`. It does not alter
`BUILTIN_NODE_REGISTRY` or the reference family.

| Node type | Ports | Parameters (kind, constraints, default) | Handler |
|---|---|---|---|
| `vidap.slice.dataset` | out `table` | none | Read the one fixed fixture file through a first-party path constant; verify its SHA-256 against a constant before parsing; parse with stdlib `csv` by the **declared** schema (refuse any mismatch); emit a table carrying its declared schema |
| `vidap.slice.prepare` | in `table` → out `table` | `missing_fill` (number, −1e6–1e6, default 0.0) | Fill missing numerics with the constant (`SimpleImputer`, constant strategy); one-hot encode `segment` against the declared category list (`OneHotEncoder` with fixed categories); keep `label`. Learns nothing from the rows |
| `vidap.slice.split` | in `table` → out `split` | `test_fraction` (number, 0.1–0.5, default 0.25); `seed` (integer, 0–4294967295, default 0) | `train_test_split` with `random_state=seed`, stratified on `label` |
| `vidap.slice.model` | in `split` → out `model` | `regularization` (number, 0.0001–10000, default 1.0) | Check the input against its declared schema: first any category column, then any missing value (each a declared failure, Section 5.5); then fit `LogisticRegression(C=regularization)` with the default solver. Its contract description names the fixed implementation; its type stays a generic model responsibility |
| `vidap.slice.evaluate` | in `model`, in `split` → out `metrics` | none | Predict on the test part; `accuracy_score`; emit accuracy (float), test-row count, and correct count (integers) |

- Tables, splits, and fitted models travel as `TrustedValue`s. Each
  handler computes its content digest from canonical bytes of the value:
  for tables and splits, the schema plus column data; for the model, the
  implementation identity, scikit-learn version, classes, coefficients,
  and intercept. Equal meaning gives equal digests on one machine.
- Handlers have no hidden state, global configuration, network, or file
  writes. Only Dataset reads a file, and only the fixed fixture.
- `seed` is the only randomness; the attempt-level seed is recorded but
  never overrides it (D3.1 V6).

### 5.4 Metrics output authority (F1)

Add the fixed first-party output authority `vidap.slice-metrics` 1.0
beside the reference scalar, in the same bounded slot, under the same
ownership, atomic publication, readback, commit-point, and indeterminate
rules as P2-EP05 §4.2. The output policy requires exactly one terminal
Evaluate node; anything else refuses before allocation. The bytes are
compact UTF-8 JSON with UTF-16-ordered keys:
`{"accuracy":<float>,"correct":<int>,"format":"vidap.slice-metrics","schemaVersion":"1.0","testRows":<int>}`.
`accuracy` must equal `correct / testRows` and be finite. No timestamp, ID,
path, or environment value enters the bytes.

`run.py` may replace the private reference flag with a closed, private
selection of fixed authorities (reference or slice-metrics), each tied by
identity to its own registry, bindings, and runtime table. The reference
proof's behavior and bytes must not change.

### 5.5 Declared failure codes (F6)

Add a closed static list of first-party declared failures with fixed text:

| Code | Explanation | Remedy |
|---|---|---|
| `unencoded-category-input` | The model received a category column that has not been converted to numbers. | Route the data through Prepare Data before the model. |
| `missing-value-input` | The model received rows with missing values. | Route the data through Prepare Data, which fills missing values, before the model. |

A handler raises a dedicated exception type carrying only one of these
codes. Dispatch maps it to that code's fixed text, with category
`execution`; the technical context keeps its withheld-message behavior.
Any other exception, including an unknown code, still maps to
`handler-failed`. A code is never taken from exception text or data.

## 6. Required Real Proof and Negative Challenges

Tests load the real fixtures through the strict deserializer and run
`run_slice_attempt`; mocked traces or precomputed results do not count.
Prove at least:

1. **Success:** the success fixture validates, plans, and runs once. The
   recorded envelope matches an independent calculation in the test (built
   directly from the CSV with scikit-learn, not through the handlers). Five
   nodes complete. Split's output is consumed by both Model and Evaluate,
   with a visible reuse event.
2. **Parameter at the library call:** `regularization` reaches
   `LogisticRegression` as `C` exactly (asserted at the call). A value of
   `0.0001` records a different accuracy from the default.
3. **Repeat and change:** an identical run recomputes with a new attempt
   ID and byte-identical metrics. Changing `seed`, `test_fraction`, or
   `missing_fill` changes the semantic digest; layout or label changes do
   not.
4. **Bypass failure:** the bypass fixture fails at the Model node with
   `unencoded-category-input` and its fixed text. Upstream nodes complete,
   Evaluate is blocked, and no metrics are published. A directly built
   table with missing values and no category column fails with
   `missing-value-input`. An unexpected handler exception still yields
   `handler-failed`.
5. **Refusals before allocation:** a missing, duplicated, or non-terminal
   Evaluate; a type-invalid connection (for example `metrics` into Model);
   and an out-of-range parameter all refuse with no attempt allocated.
6. **Fixture integrity:** a changed fixture byte makes Dataset fail closed
   before parsing. The generator reproduces the committed bytes. The
   manifest's sizes and hashes match the files, and all files under
   `fixtures/` stay under the 64 KiB aggregate.
7. **Publication:** the P2-EP05 §4.2 pre-commit, post-commit, and
   indeterminate challenges, repeated for the slice-metrics authority.
   Existing reference-output tests pass unchanged.
8. **License gate:** with the real install, `license:check` passes. The
   report records the Record 0005 matches from the gate's output. A
   user-run, read-only PowerShell check confirms that the embedded base64
   decodes to the Appendix A SHA-256.
9. **Latency (D3.2 escalation):** the user times five headless runs of the
   success fixture on Windows (first run reported separately as cold). If
   a typical warm run exceeds 2 seconds, stop and report to Central before
   P3-EP03C.

## 7. Stop Conditions

Stop `Blocked` and name the requirement, evidence, and owner if:

- the lock delta differs from P3-EP03A;
- `license:check` fails for any reason other than an error in this
  packet's own catalog code;
- the Phase 2 seams cannot carry the F1 authority or F6 codes without
  weakening ownership, publication, or diagnostics rules;
- the fixture cannot be tuned so that `regularization` changes accuracy;
- a Phase 1 change would be needed;
- the warm-run latency exceeds 2 seconds; or
- a mandatory check cannot be reproduced.

## 8. Exact Authorized Worker Outputs

Only these paths may be created or modified:

| Path | Purpose |
|---|---|
| `python/pyproject.toml` | The one dependency and the one mypy override |
| `python/uv.lock` | Regenerated by the user on Windows only |
| `scripts/dependency-controls.ps1` | Record 0005 literal catalog |
| `docs/dependency-controls.md` | Link and describe Record 0005 beside 0003/0004 |
| `.gitattributes` | `*.csv text eol=lf` |
| `python/src/vidap_execution/slice.py` | Registry, bindings, runtime table, handlers, value types, `run_slice_attempt` |
| `python/src/vidap_execution/output.py` | Slice-metrics selection and bytes |
| `python/src/vidap_execution/run.py` | Closed private selection of fixed output authorities |
| `python/src/vidap_execution/diagnostics.py` | F6 declared failure codes and text |
| `python/src/vidap_execution/dispatch.py` | Map a declared failure to its code |
| `python/src/vidap_execution/__init__.py` | Export `run_slice_attempt` if needed |
| `python/tests/test_slice_operations.py` | Sections 6.1–6.3, 6.5 |
| `python/tests/test_slice_failures.py` | Section 6.4 |
| `python/tests/test_slice_output.py` | Section 6.7 |
| `python/tests/test_slice_fixture.py` | Section 6.6 |
| `python/tests/slice_fixture_generator.py` | Deterministic fixture generator |
| `fixtures/p3-ep03b/slice-dataset-v1.csv` | Controlled dataset |
| `fixtures/p3-ep03b/slice-success-v1.json` | Success workflow |
| `fixtures/p3-ep03b/slice-bypass-prepare-v1.json` | Failure workflow |
| `fixtures/p3-ep03b/fixture-manifest.json` | D0.7 metadata |
| `README.md` | Narrow current-state update: headless slice exists; no endpoint or UI yet |
| `CONTRIBUTING.md` | Narrow update to the fixture rule and Record 0005 link |
| `ViDAP_P3_EP03B_Implementation_Report.md` | Worker evidence and handoff |

Run records live only under ignored `.vidap-local/runs/` and are cleaned by
recorded ID. No packet, plan, roadmap, decision record, reconciliation,
existing fixture or test, CI, or remote edit is authorized.

## 9. Worker Sequence and Final Attestation

1. Confirm approval; record branch, `HEAD`, the dirty baseline by owner,
   and both lock hashes.
2. Edit `pyproject.toml`; give the user the Windows commands for
   `uv --directory python lock` and `npm.cmd run setup`; record the lock
   delta from the user's output and compare it with P3-EP03A.
3. Implement Sections 5.1–5.5 and the tests. Generate the fixture and
   record its hashes in the manifest.
4. On the final tree, the user runs in order: `npm.cmd run check`,
   `npm.cmd run coverage`, `npm.cmd run deps:inventory`,
   `npm.cmd run license:check`, `npm.cmd run deps:audit`,
   `git --no-pager diff --check`; then the lock hashes,
   `git --no-pager status --porcelain --untracked-files=all`, and the
   staged list; then the Section 6.8 base64 check and the Section 6.9
   timing. Any in-scope repair requires a complete rerun.
5. Check directly: exact path scope; fixture integrity; whitespace, final
   newlines, and line endings (CRLF for the `.ps1`, LF elsewhere); no user
   paths or secrets; run-record cleanup.
6. Write the report and stop. Do not stage, commit, push, validate your own
   work, accept for Central, or start P3-EP03C.

## 10. Required Implementation Report

The report must cover:

- approval, baseline, and lock hashes before and after;
- the lock delta against P3-EP03A;
- the catalog change and gate output;
- each contract, with its source mapping;
- the fixture design, generator, and hashes;
- the independent calculation and recorded envelopes for the success and
  low-regularization runs;
- the bypass failure;
- the publication challenges;
- the latency table;
- the full attestation; and
- a validation handoff.

Use no user paths and no full command logs.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP03B-AC01 | Approval, prerequisites, baseline, and ownership are evidenced. |
| EP03B-AC02 | Only Section 8 paths change; the lock delta equals P3-EP03A exactly. |
| EP03B-AC03 | Record 0005's catalog is literal, verified by SHA-256, consulted after 0003/0004, and `license:check` passes on the real install. |
| EP03B-AC04 | The fixture satisfies D0.7, is reproducible from its generator, and keeps its bytes on Windows checkout. |
| EP03B-AC05 | Five static contracts and handlers match Section 5.3; no dynamic loading; the reference family is unchanged. |
| EP03B-AC06 | The success run's recorded metrics match an independent calculation; the shared branch reuses Split's output. |
| EP03B-AC07 | `regularization` reaches `C` exactly and measurably changes recorded accuracy. |
| EP03B-AC08 | The bypass path fails on Model with `unencoded-category-input`; `missing-value-input` and the `handler-failed` fallback are proven. |
| EP03B-AC09 | The slice-metrics authority meets every P2-EP05 §4.2 publication rule; the reference bytes are unchanged. |
| EP03B-AC10 | The warm-run latency is recorded and within 2 seconds, or the packet stopped for Central. |
| EP03B-AC11 | The full final attestation passes on Windows, with hygiene and cleanup checked. |
| EP03B-AC12 | Fresh independent validation returns `Accept`. |
| EP03B-AC13 | Central reconciles the packet and accepts the fixture bytes before P3-EP03C is drafted. |

## 12. Independent Validation

The validator reads the inputs, the worker delta, and the report. The
validator must:

- recompute the fixture hashes, the lock delta, and the Record 0005 digest;
- compute the expected accuracies independently from the CSV;
- check that `C` is passed at the library call;
- challenge the bypass, refusal, and publication cases;
- confirm that the reference behavior is unchanged and that no endpoint,
  persistence, or UI was added; and
- reproduce the attestation, or confirm the user-run Windows evidence.

The validator may create and clean only ignored transient state. It
returns `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 13. Handoff Prompts

### Worker

> Execute the approved `ViDAP_P3_EP03B.md` v0.1 as the bounded worker. Read every governing input, follow the `CONTRIBUTING.md` workaround for all Windows steps (including the lock change), implement only the Section 8 paths, complete the final attestation, and stop with `ViDAP_P3_EP03B_Implementation_Report.md` and a validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P3-EP03C.

### Validator

> Act as the independent validator for `ViDAP_P3_EP03B.md` v0.1. Read the packet, its governing inputs, and the implementation report; verify every acceptance criterion against the actual files, fixture bytes, lock, gate output, and real runs, with independent calculations. Do not edit tracked files, accept for Central, or begin P3-EP03C. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

P3-EP03B is complete and reconciled in
`ViDAP_P3_EP03B_Validation_and_Reconciliation.md`. P3-EP03C (channel and
persistence) is ready to draft and needs its own approval.
