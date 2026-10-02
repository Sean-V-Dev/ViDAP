# ViDAP P3-EP01 — Vertical-Slice and Integration Decision Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP01.md` v0.1, explicitly approved by the user 2026-10-01 |
| Worker execution | 2026-10-01; Linux shell over the Windows checkout, with a user-executed Windows attestation per `CONTRIBUTING.md` |
| Worker result | Revision 3 after a second independent `Revise` (V13–V14, Section 11); user-executed Windows attestation passed; ready for re-validation |
| Independent validation | Pending; this report is not a verdict |
| Central acceptance of D3.1–D3.4 | Pending |

## 1. Authority, inputs, and sanitized baseline

Governing inputs read: the user's 2026-10-01 approval of this exact packet;
`ViDAP_Overview.txt`; Spine v1.3; Roadmap v4.6; Phase 3 plan v1.1;
`UX refinement.txt` (the decision basis by user direction, 2026-10-01);
the P2-EP06 and P1-EP06 reconciliations; the P2-EP01 decision report (D2.1–
D2.8); the Phase 1 plan's D1.1–D1.7; and current source in
`python/src/vidap_workflow/`, `python/src/vidap_execution/`, the FastAPI
shell, the process harness, `apps/web/`, `package.json`,
`python/pyproject.toml`, `docs/dependency-controls.md`, `.gitignore`,
`README.md`, and `CONTRIBUTING.md`.

Baseline before writing: branch `main`, `HEAD`
`678f1986cce18286c3b9ba9479ae0b919c8a3184`, remote
`github.com/Sean-V-Dev/ViDAP`, no staged path. Pre-existing Central-owned
changes: modified `ViDAP_Phase_3_Plan.md` and `ViDAP_Roadmap.md`; untracked
`ViDAP_P3_EP01.md`. The output path did not exist. Locks:

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Attestation route: this worker's shell is Linux and cannot run the Windows
commands, so Section 10 step 6 uses the `CONTRIBUTING.md` workaround. No
setup, install, or package task was run from the Linux shell.

## 2. Current evidence

### Source facts from the repository (read 2026-10-01)

- **R1.** `run_attempt` refuses any resolved parameter that is not `None`, a
  boolean, a signed 64-bit integer, or a finite float ("controlled scalar
  policy"). String parameters are refused before allocation.
- **R2.** `reuse.TrustedValue` lets a first-party handler pass an opaque
  in-memory value with a handler-supplied SHA-256 content reference, so
  tables and fitted models can flow through dispatch and visible reuse
  without changing D2.6.
- **R3.** The only durable output is one bounded proof slot, gated to fixed
  first-party authorities; its envelope (`vidap.reference-scalar` 1.0)
  carries one integer.
- **R4.** `DisplayMetadata` on node, port, and parameter contracts holds only
  `label` and `description`. No contract field names a region.
- **R5.** Workflow 1.0 `LayoutMetadata` holds node positions and a viewport;
  the strict reader rejects unknown fields and `extensions`. Layout is
  excluded from the semantic projection and digest.
- **R6.** The FastAPI shell exposes only `GET /api/status`, with OpenAPI and
  docs disabled. The harness binds Python and Vite to `127.0.0.1` on fixed
  ports; Vite proxies `/api` to the Python host.
- **R7.** `.vidap-local/` is ignored and reserved for packet-named local
  state; runs already live under `.vidap-local/runs/`.
- **R8.** Nominal types available: `table`, `target`, `split`, `model`,
  `predictions`, `metrics`, `artifact`.
- **R9.** D0.6 automatically allows MIT, MIT-0, BSD-2/3-Clause, ISC,
  Apache-2.0, 0BSD, Zlib, PSF-2.0, and CC0-1.0; others are review-required.

### Primary external sources (retrieved 2026-10-01)

| ID | Source | Fact used |
|---|---|---|
| E1 | pypi.org/project/scikit-learn | 1.9.1 (2026-09-10), BSD-3-Clause, Python ≥3.11, CPython 3.14 classifier; requires NumPy, SciPy, Narwhals, joblib, threadpoolctl; a `cp314-win_amd64` wheel is published |
| E2 | scikit-learn.org API reference (1.9.1) | `train_test_split`, `OneHotEncoder`, `SimpleImputer`, `ColumnTransformer`, `Pipeline`, `LogisticRegression`, `accuracy_score`, `DummyClassifier` exist in their documented modules |
| E3 | scikit-learn `LogisticRegression` page | `C` defaults to 1.0 and is the inverse regularization strength; default solver `lbfgs` |
| E4 | pypi.org/project/numpy | 2.5.3 (2026-09-06); license expression BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0; 3.14 classifier |
| E5 | pypi.org/project/scipy | 1.18.1 (2026-08-21); BSD license classifier; 3.14 classifier |
| E6 | github.com/scipy/scipy/issues/7093 | SciPy wheels have bundled a gfortran runtime under GPLv3 with the GCC runtime exception, documented inside the wheel |
| E7 | pypi.org/project/narwhals | 2.26.0, MIT, zero required dependencies, 3.14 classifier |
| E8 | pypi.org/project/pandas | 3.0.6 (2026-09-17), BSD-3-Clause; requires NumPy, python-dateutil, tzdata on Windows |
| E9 | docs.python.org/3.14 `csv` | `csv.reader` returns every field as a string with no type conversion unless `QUOTE_NONNUMERIC` is set |
| E10 | fastapi.tiangolo.com/async | A plain `def` path operation runs in an external threadpool rather than blocking the server |
| E11 | starlette.io/middleware | `TrustedHostMiddleware` rejects requests whose `Host` is not allowed with HTTP 400; CORS is not permitted unless `CORSMiddleware` is configured |
| E12 | MDN CORS guide | Only three content types avoid preflight; `application/json` triggers a preflight |
| E13 | MDN `showSaveFilePicker` | Experimental, not Baseline, secure-context only, needs user activation |

Facts above are labeled E/R. Everything in Sections 4–6 that is not a cited
fact is architectural inference.

## 3. Gates and scoring

Gates G1–G10 are the packet's Section 7 gates. Scores use the packet weights
in this order: plan alignment 20, canonical fidelity 18, phase boundary 15,
user value 14, safety 12, simplicity/testability 13, dependency posture 8.
Weighted points are `weight × score / 5`. Totals were recomputed by script.

## 4. Recommendations

### D3.1 — Five responsibility nodes over a controlled synthetic CSV, with scikit-learn as the sole candidate library (M)

| Candidate | G1–G10 | Scores | Total |
|---|---|---|---:|
| A1. Responsibility nodes; stdlib `csv` load; scikit-learn for prepare, split, model, metric | all P | 5,5,5,4,4,4,3 | 89.0 |
| A2. As A1, plus pandas for the table | all P | 5,5,3,5,4,4,2 | 84.2 |
| B. Standard library only, hand-written baseline | G5 F | 2,5,5,2,3,5,5 | 74.8 |
| C. Existing scalar family only, no CSV | all P | 1,5,5,1,4,5,5 | 70.4 |

Rationale: B fails G5 and invariant 1 because a hand-written baseline is not
an established implementation (H). C is real but does not deliver the
spine's CSV-to-baseline slice (H). A2 is more convenient, but choosing a
dataframe library is a substantial piece of Phase 4's data-intake decision;
A1 keeps it open at the cost of a slightly lower user-value score (M). A1
leads numerically and is recommended.

**Fixed schema, no inference (V1).** The controlled fixture declares, as
constants in its contract and manifest: every column name, its type
(numeric or category), its role (feature or target), the target column, and
the exact category list for the category column. The Dataset node parses
each field by that declared schema and refuses a file that does not match
it. Nothing about column types or roles is inferred from the data; type
inference stays a Phase 4 policy.

**No learned preparation, so no leakage (V2).** Prepare runs before Split,
so anything Prepare learned from the rows would leak test rows into
training. To avoid that, Prepare's steps learn nothing from the data: the
fill value is the user's `missing_fill` parameter, and the one-hot
categories are the fixture's declared list. Scaling is left out of the
slice for the same reason. This order is a property of this fixed slice
only. It sets no precedent for where preparation sits relative to splitting;
leakage-aware boundaries remain Phase 5 policy.

**The slice (non-executable narrative).** Five visible nodes, one per region,
using the UX §2 candidate regions DATA, PREPARE, VALIDATE / SPLIT, MODEL,
and EVALUATE / COMPARE. Final region names and styling belong to D3.5.

| Region | Node (responsibility) | Inside the node | In → out | UI parameters |
|---|---|---|---|---|
| DATA | Dataset | Load one controlled synthetic CSV, chosen by fixture identity, with stdlib `csv` (E9), converting each column by its **declared** schema | — → `table` | none |
| PREPARE | Prepare Data (composite) | Fill missing numbers with a constant (`SimpleImputer`, constant strategy) and one-hot encode the category column against its **declared** category list (`OneHotEncoder` with fixed categories); keep the declared target. Nothing is learned from the rows | `table` → `table` | `missing_fill` (float) |
| VALIDATE / SPLIT | Train/Test Split | `train_test_split` (E2) | `table` → `split` | `test_fraction` (float), `seed` (int) |
| MODEL | Model | One fixed implementation, logistic regression (E2, E3) | `split` → `model` | `regularization` (float, maps to `C`) |
| EVALUATE / COMPARE | Evaluate | Predict on the test part; `accuracy_score` (E2) | `model` + `split` → `metrics` | none |

- **Shared branch:** the Split node's `split` output is consumed by both
  Model and Evaluate.
- **Skip-region dependency:** Split → Evaluate crosses the MODEL region
  without entering it. With UX §4 boundary interfaces it renders as a named
  `split` output on the VALIDATE / SPLIT boundary and a matching input on
  the EVALUATE boundary, with no wire across MODEL.
- **UI parameter with measurable effect:** `regularization` reaches
  `LogisticRegression(C=…)`. P3-EP03 must design the fixture so that a
  very small value (strong regularization) produces a different recorded
  accuracy from the default, and must assert the value at the library call
  (OV §18).
- **Actionable failure (OV §19):** connecting Dataset directly to Split,
  bypassing Prepare, is type-valid. The model then receives an unencoded
  category column. Before calling the library, the Model handler checks its
  input deterministically against the declared schema it carries: first for
  any category (text) column, then for any missing value (V5). Each check
  raises its own runtime error, so the D2.7 envelope on the Model node
  always names the real cause in plain English (an unencoded category
  column, or missing values) and suggests routing the data through Prepare
  Data, with the technical detail available. The library's own error is
  never the diagnosis.
  **This needs a named narrow Phase 2 change (V13, F6).** Today every
  handler exception maps to the single generic `handler-failed` text, and
  the exception message is deliberately withheld (`diagnostics.py`). To
  show these specific messages, a first-party handler must be able to raise
  a declared failure that carries a fixed code from a closed, static list
  (for example `unencoded-category-input` and `missing-value-input`), each
  with fixed explanation and remedy text defined beside the handler. The
  diagnostics bridge maps that code to its fixed text. Exception messages
  stay withheld, the category stays `execution`, and any other exception
  still maps to `handler-failed`. This is a D2.7 extension that Central must
  accept before P3-EP03 implements it. A second, pre-run case is a type-invalid
  connection (for example, `metrics` into Model), refused by Phase 1
  validation.
- **Responsibility shape (UX §§1, 8, 11–13):** Prepare is a composite whose
  steps stay real and inspectable. The Model node's type is a generic model
  responsibility (for example `vidap.slice.model`) with one fixed
  implementation stated in its contract description, not an
  implementation-named type. This keeps the door open for Phase 5 to add
  implementation selection to the same responsibility, but it does not
  guarantee it (V14): node contracts have no revision field today, so adding
  a selector would change an existing type's contract. Whether Phase 5 does
  that as an optional parameter on the same type, defaulting to the slice's
  implementation so saved workflows still load, or as a new type with a
  D1.6 migration, is a Phase 5 decision. The slice only avoids a name that
  would force a rename.
- **Seeds (V6):** the Split node's `seed` parameter is the only seed that
  affects the slice; it controls `train_test_split` and is part of the
  workflow's semantic content and the attempt's recorded resolved
  parameters. Logistic regression with the default `lbfgs` solver (E3) uses
  no randomness here. The D2.4 attempt-level seed is recorded as not
  supplied for slice runs; if a later caller supplies one, it does not
  override the node parameter, and both are recorded.
- **Fits Phase 2 without policy changes:** every UI parameter is a bool,
  int, or float, so R1's scalar policy holds and no string parameter is
  needed. Tables, splits, and fitted models travel as `TrustedValue`s with
  handler-computed content digests (R2), so D2.6 visible reuse still works.
  The target column is fixed by the controlled fixture, not chosen in the
  UI.

**Result representation.** The recorded result is a small metrics envelope
(accuracy as a float, plus test-row and correct counts as integers) written
to the existing bounded proof slot under a new fixed first-party output
authority (for example `vidap.slice-metrics` 1.0). This is a **named narrow
Phase 2 extension** (R3): a second fixed output authority beside the
reference scalar, under the same D2.5 ownership, readback, and
publication-classification rules. It needs Central acceptance and is
implemented only in P3-EP03.

**Candidate dependency (not selected).** scikit-learn (E1), which pulls in
NumPy, SciPy, Narwhals, joblib, and threadpoolctl. The later dependency step
must collect: exact versions and lock delta; CPython 3.14 Windows wheels for
every package; license expressions, including NumPy's compound expression
(E4, all in the D0.6 allowed set); and **the bundled native libraries inside
every compiled wheel (NumPy, SciPy, and scikit-learn), including SciPy's
GCC-runtime-exception code (E6), which are expected to be review-required**
under D0.6/0003/0004 (V10);
maintenance and advisory evidence; and install size. pandas (E8) is
recorded as a Phase 4 candidate, not proposed here.

**Candidate fixture (not created).** One synthetic CSV, at most 16 KiB, about
100–200 rows: a binary target, two numeric features (one with deliberate
missing values), and one text category, created by a documented
deterministic method. MIT terms, `synthetic non-sensitive`, and a manifest
entry under D0.7, the same as P2-EP05.

**Phase 4/5 policies deliberately left open:** initial task types (the
slice happens to be binary classification, which sets no precedent);
supported file formats and size limits; user-chosen files and dataset
management; type inference and column-role detection;
profiling and data-quality messages; which preparation operations exist and
their options, including learned transforms such as scaling; leakage-aware
ordering of preparation and splitting; dataframe library choice; target
selection; split strategy
beyond one holdout; model families, implementation selection, and curated or
introspected parameter presentation; metric policy and interpretation
wording; prediction output.

### D3.2 — Narrow synchronous loopback JSON endpoints in the existing FastAPI shell (H)

| Candidate | G1–G10 | Scores | Total |
|---|---|---|---:|
| A. Synchronous loopback JSON endpoints in the existing shell | all P | 5,5,5,4,4,5,5 | 94.8 |
| B. As A, with a background attempt and status polling | all P | 4,5,4,5,4,3,5 | 85.4 |
| C. File- or command-based exchange | all P | 2,4,5,2,3,3,5 | 66.0 |
| D. Browser-side execution | G2, G5, G7 F | 1,1,3,3,2,2,1 | 36.6 |

Rationale: A reuses the accepted D2.1 seam directly. A plain `def` endpoint
runs in FastAPI's threadpool (E10), so the server stays responsive while a
short run executes (H). B adds a job lifecycle that D2.1 deliberately
deferred and that a sub-second slice does not need (M). C makes the browser
depend on files with no clear status channel (M). D makes the browser the
runtime and fails G2 (H).

**Minimum operations, all under `/api/slice/`:**

1. `GET contracts`: the registered slice node contracts (types, ports,
   parameters, labels, descriptions), projected from the static registry.
   This is the UI's only source for forms (A3).
2. `POST validate`: a document body returns Phase 1 diagnostics unchanged
   (code, severity, element, plain-English explanation, remedy).
3. `POST run`: a document body runs one attempt and returns the attempt ID,
   outcome, per-node statuses, semantic digest, D2.7 runtime diagnostics,
   and the recorded metrics read back from the owned slot. Invalid
   documents are refused with Phase 1 diagnostics and never allocate an
   attempt.
4. The save/load operations in D3.3.

**Bounds and protections:** loopback binding stays as today (R6);
`TrustedHostMiddleware` limited to the loopback host names (E11); no
`CORSMiddleware` is installed, so the server sends no CORS permission headers
(an inference from E11, which says cross-origin access must be explicitly
enabled); POST endpoints require `Content-Type: application/json`, which
forces a browser preflight for any cross-origin attempt (E12); POST
endpoints also accept `Origin` only when it is absent (non-browser local
tools and tests) or exactly `http://127.0.0.1:5173` (the Vite host) or
`http://127.0.0.1:8000` (the Python host), and refuse anything else (V7); body
size capped (for example 256 KiB); one run at a time behind a process-level
lock, with a second request refused as busy rather than queued; OpenAPI and
docs stay disabled. No authentication is added, because the surface is
local-only.

**Latency escalation (V7):** P3-EP03 must measure the slice run time on the
supported Windows environment. If a typical run exceeds 2 seconds, or the
editor is observably unresponsive while a run is in progress, P3-EP03 stops
and Central revisits option B (background attempt with status polling)
before P3-EP05 builds the run controls.

**Proof that the UI cannot show an unrecorded result:** the run response's
metrics come only from readback of the owned slot. Tests must show that a
run whose publication fails or is indeterminate returns no metrics, and
that frontend code never derives a metric. A contract-drift test compares
`GET contracts` with the Python registry.

### D3.3 — Backend-owned workflow files with digest-based conflict detection (M)

| Candidate | G1–G10 | Scores | Total |
|---|---|---|---:|
| A. Backend-owned files in an ignored local workspace | all P | 5,5,5,4,5,4,5 | 94.6 |
| B1. Browser download/upload | G10 F | 3,3,5,3,2,5,5 | 72.0 |
| B2. Browser file-system-access API | all P | 3,4,5,4,3,2,5 | 73.0 |
| C. Hybrid of A plus browser import/export | all P | 4,5,5,5,4,3,5 | 88.4 |

Rationale: B1 cannot detect a file changed by another tool, so it fails the
UX §18 requirement (G10) and cannot overwrite in place (H). B2 is
experimental, not Baseline, and needs user activation (E13) (H). C is
useful, but it is extra scope for the first slice (M). A is recommended,
with import/export of copies deferred to a later packet if needed.

**Behavior:**

- **Location:** `.vidap-local/workflows/` under the ignored, reserved local
  root (R7). This packet names that need; P3-EP03 must update the ignore and
  documentation rules, as `CONTRIBUTING.md` requires for new local paths.
- **Naming:** a validated slug plus a fixed `.vidap.json` extension. No path
  separators, absolute paths, or caller-chosen directories.
- **Writing:** the backend writes only `serialize_document` output (the
  canonical Phase 1 serializer), so the saved bytes are the canonical
  document. Writes go to a temporary file in the same directory and are
  then replaced atomically.
- **Loading:** `deserialize_document`, then `validate_workflow`. A malformed,
  unsupported-version, or invalid file is refused with its Phase 1
  diagnostic and is never repaired.
- **External changes (UX §18):** every load returns the file's SHA-256, and
  every save sends the digest it was based on. If the file on disk differs,
  the save is refused as a conflict. The editor also re-checks the digest
  when the window regains focus and before a run. When it differs, the
  editor shows that the file changed outside it, with a semantic summary
  (nodes and edges added or removed, parameters changed), and offers to
  reload or save under a new name. It never silently overwrites. No
  file-watcher dependency is needed.
- **Who builds the change summary (V8):** the backend. A conflict response
  (and a dedicated compare call used on focus) returns the summary computed
  by comparing the two canonical documents on the Python side. The editor
  only displays it and never diffs workflow semantics itself.
- **Sidecar conflicts (V8):** the D3.4 sidecar gets the same base-digest
  check. One save request carries the workflow and its sidecar, each with
  the digest it was based on. If either file on disk differs, the whole save
  is refused as a conflict, so the two files are never left from different
  editing sessions.
- **Fidelity proof:** a test saves, reads the file from disk, deserializes
  it, and compares the semantic digest with the UI run's response; running
  the saved file headlessly must produce the same digest and metrics
  (P3-AC03).

### D3.4 — A versioned presentation sidecar, with region membership derived from node type (M)

| Candidate | G1–G10 | Scores | Total |
|---|---|---|---:|
| A. Derived membership plus per-session UI state only | G10 F | 3,4,5,2,4,5,5 | 77.6 |
| B. Versioned presentation sidecar plus derived membership | all P | 5,5,5,5,4,4,5 | 95.0 |
| C. `vidap.workflow` schema revision extending layout | all P | 3,5,4,5,4,2,5 | 78.8 |

Rationale: A loses region widths and node positions on every reload, but UX
§3 makes region width user-owned workspace state, which this report reads
as state that survives a reload (G10 F). The validator noted this reading
is generous; if A passed G10 instead, B would still lead on score (M). C is a real
option, since R5 shows the strict reader cannot carry this state today
(H), but it brings D1.6 migration work and reopens Phase 1, which UX §22
asks to avoid when an alternative exists (M). B keeps Phase 1 untouched and
the semantics clean.

**Ownership:**

- **Region membership** is derived, not stored. The frontend keeps a small
  presentation map from node type to region. Unknown types fall into a
  visible "Unassigned" region. This is UI-owned presentation, not contract
  data, so it adds nothing to the Phase 1 contract (R4) and copies no
  parameter or validation data.
- **Persisted in the sidecar** (`<name>.vidap-view.json`, format
  `vidap.workspace-view` 1.0, saved next to the workflow by the same
  backend endpoint): region widths and order, each node's position relative
  to its region (so moving a gutter does not displace nodes), and the
  viewport. Content is size-capped and shape-validated by the backend.
- **Why not the Phase 1 layout fields (V9):** Phase 1 layout stores absolute
  canvas coordinates. Region-relative positions would change what those
  numbers mean to any other reader of the workflow file, and a gutter move
  would otherwise have to rewrite every position to its right. The viewport
  goes in the sidecar too, so all editor presentation has one owner.
- **Per-session only:** expanded or focused node, active trace or X-ray,
  hover, and selection.
- **The workflow document's own layout metadata** is not created or edited
  by the region editor. If a loaded document already has it, it is
  round-tripped unchanged, so no external content is dropped silently.
- **Which position wins (V9):** the sidecar is the only position source the
  region editor uses. Phase 1 layout positions are never displayed or
  merged; when there is no sidecar, the editor uses deterministic default
  placement, not the Phase 1 layout.
- **Safe degradation:** a missing sidecar produces deterministic default
  placement within derived regions; entries for node IDs that no longer
  exist are ignored and dropped on the next save; new nodes get default
  placement; an unreadable or unsupported sidecar is set aside with a
  notice, and the workflow itself still loads.
- **Isolation tests:** the run and validate endpoints accept only the
  workflow document and refuse sidecar content. Changing widths, positions,
  or expansion leaves the semantic digest, plan, and metrics unchanged.

No Phase 1 change is proposed. If later phases need presentation state
inside the workflow file, that is a separate D1.6 proposal.

## 5. Downstream consequences

| Packet | Consequence |
|---|---|
| P3-EP02 (design and interaction) | With one node per region, the slice never shows a wire within a region, so the P3-EP02 prototype must add at least one region with several connected nodes (UX §§6, 23) (V12). Designs for the five-region slice: boundary rails, name-matched boundary values, producer/consumer reveal, the gutter break, compact and expanded node states for these node types, the visible metrics result, the conflict notice, and the Unassigned region. It cannot assume a side inspector or per-implementation nodes. |
| P3-EP03 (backend slice) | Adds the scikit-learn dependency only after full D0.6 evidence, including SciPy's bundled-license review; the D0.7 fixture; five contracts and static bindings; `TrustedValue` digests; the slice metrics output authority (a named narrow D2 extension); the declared handler failure codes (F6, if accepted); the `/api/slice/` endpoints with host, origin, content-type, size, and single-run limits; workflow and sidecar save/load under `.vidap-local/workflows/`, with ignore and doc updates; and headless tests including parameter-at-library-boundary and the unencoded-text failure mapping. |
| P3-EP04 (editor core) | Forms come only from `GET contracts`; the region map; sidecar ownership; digest-based conflict handling. |
| P3-EP05 (run, results, trace) | Displays only metrics read back from the run response; shows D2.7 errors on the affected node; implements the trace and X-ray. |

## 6. Findings, open policies, and spikes

| ID | Severity | Finding | Owner |
|---|---|---|---|
| F1 | Non-blocking | The slice needs a second fixed output authority (metrics envelope) beside the scalar reference proof. This is a named narrow D2.5/D2.8 extension for Central to accept or reject. | Central |
| F2 | Non-blocking | Compiled wheels (NumPy, SciPy, scikit-learn) bundle native libraries; SciPy has historically bundled GCC-runtime-exception code (E6). All are expected to need review under D0.6 before scikit-learn can be installed. If they are not accepted, D3.1 needs revisiting. | Central / P3-EP03 dependency step |
| F3 | Non-blocking | `.vidap-local/workflows/` is a new local path that P3-EP03 must name in the ignore rules and documentation. | P3-EP03 |
| F4 | Non-blocking | Region membership is fixed by node type for the slice; moving a node to a different region is not supported yet. | P3-EP02 / later phases |
| F5 | Non-blocking | The slice has no intra-region wire; the P3-EP02 prototype must cover local wiring (V12). | P3-EP02 |
| F6 | Non-blocking | The specific Model-node failure messages need declared first-party failure codes with fixed text, a named narrow D2.7 extension (V13). Without it, the failure would show only the generic `handler-failed` message and the OV §19 example would not be met. | Central |

The Phase 4/5 policies left open are listed under D3.1. No Phase 1 change is
proposed. No feasibility spike is needed: the remaining uncertainty (the
exact fixture values that make `regularization` change accuracy, and the
exact library error text) is implementation evidence for P3-EP03, not a
decision question.

## 7. UX basis trace

| Recommendation | `UX refinement.txt` sections | Deviation |
|---|---|---|
| D3.1 responsibility and composite nodes, generic Model | §§1, 8, 11–14 | None |
| D3.1 regions, skip-region dependency, shared branch | §§2, 4, 23 | None; final region names left to D3.5 |
| D3.2 backend-authoritative channel | §18 (canonical workflow as shared truth) | None |
| D3.3 external-change detection | §18 | Detection on focus and before save or run, not live push; justified by no new dependency and the slice's single local user |
| D3.4 user-owned region widths, positions that don't move | §§3, 6, 20 | None |
| D3.4 no Phase 1 reopening | §22 | None |
| Visible metrics result kept with the canvas | §15 | Design is P3-EP02's |

## 8. Worker self-assessment

| Criterion | Assessment |
|---|---|
| EP01-AC01 | Met: approval, versions, baseline, ownership, and locks recorded without user paths. |
| EP01-AC02–AC04 | Met: four recommendations with alternatives, G1–G10, recomputed totals, confidence, consequences, cited sources, and labeled inference. |
| EP01-AC05 | Met as a recommendation: real minimal slice of responsibility nodes, generic Model shape, candidates only, open policies listed. |
| EP01-AC06 | Met as a recommendation: backend-authoritative, D2 seam reused, loopback-bounded, readback-only metrics. |
| EP01-AC07 | Met as a recommendation: canonical serializer, Phase 1 reader, conflict refusal, no silent overwrite. |
| EP01-AC08 | Met as a recommendation: sidecar isolation with digest-invariance tests; no Phase 1 change. |
| EP01-AC09 | Met: the report is the only worker change; locks unchanged. |
| EP01-AC10 | Met: the Revision 3 user-executed Windows run passed every step with captured counts; locks unchanged; report hygiene verified (Section 9). |
| EP01-AC11–AC12 | Not self-assessed; independent validation and Central acceptance remain required. |

## 9. Final attestation and scope

### Revision 1 run (historical)

The user ran the full Section 10 sequence on 2026-10-01 against the first
version of this report. The pasted output showed zero audit findings, a
clean `git diff --check`, unchanged lock hashes, and the report as the only
worker change. The results of `check`, `coverage`, `deps:inventory`, and
`license:check` were **not evidenced in that worker run**: the output was
not pasted, and the earlier version of this section wrongly claimed them on
the user's statement (V4). The independent validator then reproduced the
whole sequence and recorded: `check` passed (mypy 21 files; web 10/10;
Python unit 125 passed, 1 skipped; build, 3 integration tests, smoke);
`coverage` passed (web 10; Python 128 passed, 1 skipped; Python 88%, web
87.5% of statements); `deps:inventory` completed; `license:check` passed for
431 locked packages; `deps:audit` found 0 vulnerabilities; `git diff
--check` clean; locks unchanged. Those are the validator's results, not
this worker's.

### Revision 2 run (historical)

The user ran the full Section 10 sequence in Windows PowerShell from the
repository root on 2026-10-01, against this revised report, in packet order,
and pasted the captured summary lines. This is a user-executed Windows run
under the `CONTRIBUTING.md` workaround. Results exactly as the output shows:

| Command | Exit | Captured evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | Formatting "All checks passed!"; mypy "no issues found in 21 source files"; web tests 3 files, 10 passed; Python unit 125 passed, 1 skipped, 3 deselected; Python integration 3 passed, 126 deselected |
| `npm.cmd run coverage` | 0 | Web tests 10 passed; web coverage 87.5% statements, 85.71% branches, 83.33% functions, 87.5% lines; Python 128 passed, 1 skipped; Python total coverage 88% |
| `npm.cmd run deps:inventory` | 0 | Completed; inventory lines printed |
| `npm.cmd run license:check` | 0 | "License policy passed for 431 installed locked packages" |
| `npm.cmd run deps:audit` | 0 | npm: 0 vulnerabilities of 432 dependencies; Python: 57 packages resolved, "No known vulnerabilities found" |
| `git diff --check` | 0 | No output |

Both lock hashes match the Section 1 baseline. `git status --porcelain`
shows modified `ViDAP_Phase_3_Plan.md` and `ViDAP_Roadmap.md` and untracked
`ViDAP_P3_EP01.md` (all Central-owned and pre-existing) plus this report;
nothing is staged. The summary filter did not print the build or smoke
lines individually; `check` runs them in sequence and exited 0. The one
Python skip is the host-dependent symlink test Phase 2 already accepted.

Report hygiene was checked directly after this revision: no trailing
whitespace, final newline present, no user paths, credentials, or raw
environment values. No setup, install, or package task ran from the Linux
shell. Nothing was staged, committed, or pushed, and no P3-EP02 work began.

### Revision 3 run

The user ran the full Section 10 sequence in Windows PowerShell from the
repository root on 2026-10-01, against Revision 3, in packet order, and
pasted the captured summary lines (user-executed Windows run under the
`CONTRIBUTING.md` workaround). Results exactly as the output shows:

| Command | Exit | Captured evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | Formatting "All checks passed!"; mypy "no issues found in 21 source files"; web tests 3 files, 10 passed; Python unit 125 passed, 1 skipped, 3 deselected; Python integration 3 passed, 126 deselected |
| `npm.cmd run coverage` | 0 | Web tests 10 passed; web coverage 87.5% statements, 85.71% branches, 83.33% functions, 87.5% lines; Python 128 passed, 1 skipped; Python total coverage 88% |
| `npm.cmd run deps:inventory` | 0 | Completed; inventory lines printed |
| `npm.cmd run license:check` | 0 | "License policy passed for 431 installed locked packages" |
| `npm.cmd run deps:audit` | 0 | npm: 0 vulnerabilities of 432 dependencies; Python: 57 packages resolved, "No known vulnerabilities found" |
| `git diff --check` | 0 | No output |

Both lock hashes match the Section 1 baseline. `git status --porcelain`
shows modified `ViDAP_Phase_3_Plan.md` and `ViDAP_Roadmap.md`, untracked
`ViDAP_P3_EP01.md` (all Central-owned and pre-existing), and this report;
nothing is staged. `check` runs build and smoke in its chain and exited 0;
their lines were not printed by the summary filter. The one Python skip is
the host-dependent symlink test Phase 2 already accepted.

Report hygiene was checked directly after Revision 3: no trailing
whitespace, final newline present, no user paths, credentials, or raw
environment values. No setup, install, or package task ran from the Linux
shell. Nothing was staged, committed, or pushed, and no P3-EP02 work began.

## 10. Independent-validation handoff

Please independently check this Revision 3 against the governing inputs and
the prior findings V1–V14: confirm each Section 11 change resolves its
finding without introducing hidden Phase 4/5 policy, UI authority, schema
change, dependency selection, or service growth; confirm no weighted total
changed; recheck the Section 9 Revision 2 evidence by reproducing the
Section 10 sequence with captured counts; confirm locks and scope; and
return `Accept`, `Revise`, or `Blocked` with criterion-linked findings and a
Central recommendation, including on F1 (metrics output authority), F2
(bundled-license review), and F6 (declared handler failure codes). This worker does not validate or accept its own
work.

## 11. Response to the independent `Revise`

| Finding | Change in this revision |
|---|---|
| V1 (Medium) | D3.1 now fixes column names, types, roles, target, and category list as declared fixture constants; the Dataset node parses by that schema and refuses mismatches; type inference and column-role detection are listed as open. |
| V2 (Medium) | Prepare now learns nothing from the rows: a constant fill value (the `missing_fill` parameter) and fixed declared categories; scaling removed. The slice order is stated to set no precedent, and leakage-aware ordering is listed as open Phase 5 policy. |
| V3 (Low) | Initial task types added to the open-policy list. |
| V4 (Low) | Section 9 now separates what the worker run evidenced from the validator's reproduction, and a fresh worker run with captured counts is required for this revision. |
| V5 (Low) | The Model handler checks its input against the declared schema in a fixed order (category columns, then missing values), each with its own plain-English error. |
| V6 (Low) | The Split `seed` parameter governs; the attempt-level seed is recorded as not supplied, does not override the node seed, and both are recorded. |
| V7 (Low) | Allowed `Origin` values named; a 2-second / unresponsive-editor latency escalation added for P3-EP03. E11's CORS statement relabeled as inference. |
| V8 (Low) | Sidecar uses the same base-digest conflict check in one combined save; the backend builds the change summary. |
| V9 (Low) | Reason for keeping positions out of Phase 1 layout given; the sidecar is the only position source and wins. |
| V10 (Info) | Bundled-license review extended to every compiled wheel. |
| V11 (Info) | D3.4 option A gate judgment explained; outcome unchanged. Other gate results remain as shown in each table. |
| V12 (Info) | Recorded as F5 and in the P3-EP02 consequences. |

No recommendation changed direction, and no weighted total changed: the
revisions tighten D3.1's wording and add detail to D3.2–D3.4 within the
same options.

### Revision 3 (second `Revise`)

| Finding | Change in this revision |
|---|---|
| V13 (Medium) | The Model-node failure messages now name the Phase 2 change they need: declared first-party failure codes with fixed text, mapped by the diagnostics bridge, with exception messages still withheld. Recorded as F6 for Central and added to P3-EP03's consequences. |
| V14 (Low) | The "without renaming or rewiring" claim is withdrawn. The report now says the generic Model shape keeps the option open, that contracts have no revision field, and that how Phase 5 adds selection is a Phase 5 decision. |
| V15, V16 (Info) | Not received in detail by this worker; the validator's summary describes them as clarifications only. No change made. |

No weighted total or recommendation direction changed.
