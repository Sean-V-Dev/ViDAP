# ViDAP P3-EP03C — Slice Channel and Workflow Save/Load

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Bounded implementation: local HTTP channel, backend-owned workflow persistence, headless proof |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1, WS3.3 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3/checkpoint A3 |
| Prerequisites | P3-EP01 (D3.2–D3.4, V15, V16, F3 accepted) and P3-EP03B complete |
| Workstream | WS3.3 — Backend slice (third of three packets) |
| Authorized worker report | `ViDAP_P3_EP03C_Implementation_Report.md` |
| Created | 2026-10-02 |
| Approved | 2026-10-02 by explicit user direction |
| Owner | Central |

---

## 1. Authorization Boundary

Approval of this exact version authorizes one bounded worker to change only
the Section 8 paths. All Windows steps run through the user, under the
`CONTRIBUTING.md` workaround.

This packet authorizes:

- the `/api/slice/` endpoints in the existing loopback FastAPI shell;
- workflow and sidecar files under `.vidap-local/workflows/`;
- the three publication tests carried over as observation O3 of the P3-EP03B
  reconciliation;
- headless and live-process evidence.

It does not authorize:

- any UI or web code;
- a new dependency or lock change;
- authentication;
- CORS;
- a background job or status polling;
- a file watcher;
- import or export of workflow files;
- any change to Phase 1 code, the slice operations, run records, or the
  P2-EP05 reference behavior;
- a CI change;
- staging, committing, or pushing;
- starting P3-EP04.

## 2. Plain-English Packet Intent

**What it does.** The browser can now:

- ask the backend which slice nodes exist and what their settings are;
- validate a workflow;
- run a workflow and read back the recorded result and any errors;
- save and reload a workflow and its layout.

When a saved workflow file has been changed by something else, the browser
is told and nothing is silently overwritten.

**Why it is needed.** P3-EP04 (editor) and P3-EP05 (run controls) must use
only what the backend provides: forms come from contracts, verdicts come from
validation, and results come from recorded output. This packet builds that
single channel and proves it without a UI.

**How success is demonstrated.** Tests drive every endpoint in process and
show the following:

- forms match the registry;
- run results equal the recorded slot;
- a saved file is the canonical document;
- reloading and running the saved file gives the same digest and metrics;
- an outside edit is detected and summarized;
- unsafe hosts, origins, content types, sizes, names, and concurrent runs are
  refused.

The user also times real runs through the launched local processes.

## 3. Governing Inputs

The worker and validator must read:

- the explicit approval of this version;
- OV §§18–19 and §22;
- `ViDAP_Phase_3_Plan.md` v1.1 §§5–8;
- `ViDAP_P3_EP01_Decision_Report.md` D3.2–D3.4 (Revision 3) and its
  reconciliation (V15, V16, F3);
- `ViDAP_P3_EP02_Decision_Report.md` and `DESIGN.md` v0.2, for context only:
  the editor's needs from this channel;
- `ViDAP_P3_EP03B.md` and its reconciliation, including O3;
- `ViDAP_P2_EP05.md` §4.2;
- the Phase 1 and Phase 2 sources and the slice module;
- `CONTRIBUTING.md`;
- this packet.

## 4. Approved Channel Contract

### 4.1 Guards for every `/api/slice/` route

Install one `APIRouter` under `/api/slice` in `create_app()`. Every route has
the router-level guards below.

**Central choice.** D3.2 named `TrustedHostMiddleware`. An app-wide
middleware would also change the accepted foundation route `/api/status`,
which the in-process foundation tests call as `testserver`. So the
equivalent host check is a router dependency that applies only to slice
routes. `/api/status` and its tests stay unchanged.

1. **Host.** The `Host` header's name must be `127.0.0.1` or `localhost`.
   Otherwise the response is `400 invalid-host`.
2. **Origin.** The `Origin` header must be absent or exactly
   `http://127.0.0.1:5173` or `http://127.0.0.1:8000`. Otherwise the
   response is `403 origin-refused`.
3. **Content type (POST and PUT).** The request must have
   `Content-Type: application/json`, with an optional
   `charset=utf-8` and nothing else. Otherwise the response is
   `415 unsupported-content-type`.
4. **Body size.** The raw body is read with a 256 KiB cap: a larger body is
   refused as `413 body-too-large` before parsing. It must be UTF-8 JSON;
   otherwise the response is `400 malformed-json`.
5. **No CORS, OpenAPI, or docs.** Install no CORS middleware. OpenAPI and the
   documentation pages stay disabled.

Every error uses one envelope:
`{"error": {"code": "<fixed code>", "message": "<fixed text>"}}`, with an
optional `diagnostics` list where stated. Messages are fixed strings: no
exception text, paths, or input echo.

### 4.2 Contracts, validation, and run

**`GET /api/slice/contracts`** returns `{"contracts": [...]}`, projected from
`SLICE_REGISTRY` only. For each node type it gives:

- `type`, `label`, `description`;
- `inputs` and `outputs`, each with `key`, `nominalType`, `label`,
  `cardinality`, and `required`;
- `parameters`, each with `key`, `kind`, `required`, `label`,
  `description`, `default` (when present), and `constraints`.

The response contains no region data. A drift test compares it field by
field with the registry.

**`POST /api/slice/validate`.** The body is a `vidap.workflow` document.

- If decoding fails, the response is `422 invalid-workflow` with the
  decoder's Phase 1 diagnostic.
- Otherwise the response is `200 {"valid": bool, "diagnostics": [...]}`,
  holding the Phase 1 diagnostics for `SLICE_REGISTRY` unchanged: `code`,
  `severity`, `category`, element kind and reference, `message`, `remedy`,
  and `jsonPointer`.
- Validation never allocates an attempt.

**`POST /api/slice/run`.** The body is a `vidap.workflow` document.

- **Invalid documents.** An undecodable or invalid document gets
  `422 invalid-workflow` with Phase 1 diagnostics, and no attempt is
  allocated. A slice-output refusal (for example, no Evaluate node) or an
  attempt refusal gets `422 run-refused` with fixed text.
- **One run at a time.** A process-level non-blocking lock allows one run at
  a time. A second run while one is in progress gets `409 busy`; it is not
  queued.
- **Synchronous handler.** The handler is a plain `def`, so FastAPI runs it
  in its threadpool.
- **Success response.** The response is
  `200 {"attemptId", "outcome", "semanticDigest", "nodes": [{"nodeId", "operationKey", "status"}], "diagnostics": [<D2.7 runtime envelopes>], "metrics": <object|null>}`.
- **Where `metrics` comes from.** `metrics` comes **only** from the run's
  owned `proof-output.bin`. It is read back after the attempt, parsed, and
  checked to have exactly the `vidap.slice-metrics` 1.0 shape. It is `null`
  unless the outcome succeeded and the record lists the proof slot.
- **Indeterminate publication.** A `PublicationIndeterminate` gets
  `500 publication-indeterminate` with the `attemptId` and no metrics.

V15 applies: the run executes the posted document, not a saved file, and the
response's semantic digest is its identity.

Run records stay under `.vidap-local/runs/` as accepted local state. This
packet adds no automatic deletion; retention is a later decision. Tests remove
their own attempts by recorded ID.

### 4.3 Workflow files (D3.3, D3.4, V15, V16, F3)

**Storage.** Files live in `.vidap-local/workflows/` under the checkout
(the existing ignore rule `/.vidap-local/` covers it):

- the workflow, as `<name>.vidap.json`;
- its sidecar, as `<name>.vidap-view.json`.

**Names.** `<name>` matches `^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$` or is a
single character `[a-z0-9]`. Anything else gets `400 invalid-name`. Callers
never supply a path, separator, or extension.

**Path safety.** The workflows directory and every file in it are checked
for symlinks and reparse points, and for containment within the checkout,
before each read and write. A failure gets `500 storage-refused` with fixed
text.

**Digests.** A workflow's digest is `sha256:<hex>` of its file bytes; the
same rule applies to the sidecar.

**`GET /api/slice/workflows`** returns
`{"workflows": [{"name", "workflowDigest", "hasSidecar"}]}`, sorted by name.
Only files matching the naming rule are listed.

**`GET /api/slice/workflows/{name}`.**

1. Read the bytes (at most 256 KiB). Decode them with `deserialize_document`,
   then validate with `validate_workflow` against `SLICE_REGISTRY`.
2. A malformed, unsupported, or invalid file gets `422 invalid-workflow` with
   Phase 1 diagnostics. It is never repaired.
3. Otherwise the response is
   `200 {"name", "workflow": <canonical document object>, "workflowDigest", "sidecar": <object|null>, "sidecarDigest": <str|null>, "sidecarNotice": <null|"unreadable"|"unsupported">}`.
4. An unreadable or unsupported sidecar is reported in `sidecarNotice`, while
   the workflow still loads.
5. V16 applies: any existing Phase 1 layout metadata is returned unchanged
   and never interpreted.

**`PUT /api/slice/workflows/{name}`.** The body is
`{"workflow": <document>, "sidecar": <object|null>, "baseWorkflowDigest": <str|null>, "baseSidecarDigest": <str|null>}`.

1. The workflow must decode and validate, or the response is
   `422 invalid-workflow`. In Phase 3, save and load both require a valid
   document, so a saved file can always be reloaded.
2. The sidecar, if present, must pass Section 4.4, or the response is
   `422 invalid-sidecar`.
3. **Conflict check (V15).** Under a process-level save lock, compare each
   file's current digest on disk, or its absence, with the matching base
   digest:
   - an existing file needs a base digest equal to its current digest;
   - a missing file needs a `null` base digest.

   Any mismatch in either file refuses the **whole** save with
   `409 conflict`. The response gives the current digests and the change
   summary (Section 4.5) of the disk workflow against the posted workflow.
4. **Writes.** The workflow is written from `serialize_document` output only;
   the sidecar from canonical JSON. Each file goes to an exclusive temporary
   file in the same directory, is synced, and is then moved into place with
   `os.replace`. The workflow is written first, then the sidecar. A `null`
   sidecar leaves any existing sidecar untouched only if `baseSidecarDigest`
   matches it.
5. **Response.** `200 {"name", "workflowDigest", "sidecarDigest"}`.

**`POST /api/slice/workflows/{name}/compare`.** The body is
`{"workflow": <document>, "baseWorkflowDigest": <str|null>, "baseSidecarDigest": <str|null>}`.

- The response is `200 {"changed": bool, "workflowDigest", "sidecarDigest", "summary": <Section 4.5 or null>}`.
- `changed` is true when either current digest differs from its base.
- The summary compares the disk workflow, if any, with the posted one.
- The editor uses this call on focus and before a run. It never diffs
  workflow semantics itself.

### 4.4 Sidecar shape (`vidap.workspace-view` 1.0)

The backend validates shape and bounds only; region meaning stays UI-owned.

```json
{"format": "vidap.workspace-view", "schemaVersion": "1.0",
 "regions": [{"key": "<text>", "width": <number>}],
 "nodes": {"<node UUID>": {"region": "<text>", "x": <number>, "y": <number>}},
 "viewport": {"x": <number>, "y": <number>, "zoom": <number>}}
```

| Field | Rule |
|---|---|
| Fields | Exactly these; no unknown fields. Any other `format` or `schemaVersion` is unsupported. |
| Size | At most 64 KiB serialized. |
| `regions` | At most 32 entries; unique keys of 1–40 characters from `[A-Za-z0-9_-]`; widths 120–4000. |
| `nodes` | At most 500 entries; keys are canonical UUIDs; `region` follows the region-key rule; coordinates are finite and between −100000 and 100000. |
| `viewport` | Zoom between 0.1 and 4. |
| Unknown node IDs | Allowed: the editor drops stale entries itself. |

The sidecar is never accepted by `validate` or `run`. Those bodies are only
documents, and a sidecar posted there is refused by the strict Phase 1
decoder.

### 4.5 Change summary

The summary is computed in Python from the two decoded documents:

```json
{"nodesAdded": [{"nodeId", "type"}], "nodesRemoved": [...],
 "edgesAdded": [{"edgeId", "source", "target"}], "edgesRemoved": [...],
 "parametersChanged": [{"nodeId", "key", "before", "after"}],
 "labelsChanged": [nodeId...], "layoutMetadataChanged": bool}
```

Here "before" is the posted (editor) document and "after" is the disk
document. Entries are sorted deterministically. When the disk file is
missing, the summary is `null` and the response says `"missing": true`.

## 5. Required Real Proof and Negative Challenges

Tests use `httpx.ASGITransport` with `base_url="http://127.0.0.1:8000"`
against `create_app()`. They use the real registry, fixtures, run layer, and
files. No mocked trace or precomputed result counts as proof.

1. **Contracts.** The projection equals `SLICE_REGISTRY` field by field (the
   drift test), and it carries no region data.
2. **Validate.** The success fixture is valid. A type-invalid connection and
   an out-of-range parameter return their Phase 1 codes unchanged. An
   undecodable body returns `422`. No attempt is allocated.
3. **Run.**
   - The success fixture returns the metrics recorded in its slot. These
     equal P3-EP03B's 0.9 envelope and the bytes on disk.
   - The bypass fixture returns `failed`, the Model node's
     `unencoded-category-input` envelope, and `metrics: null`.
   - When metrics publication is forced to fail, the response has no
     metrics.
   - No frontend file is touched. The response's metrics are only those
     parsed from the slot.
4. **Single run.** While one run holds the lock (forced in the test), a
   second request returns `409 busy` and allocates nothing.
5. **Guards.** Each case gets its fixed code, and no attempt or file is
   created:
   - a wrong host (`testserver` and a foreign name);
   - foreign, `null`, and `localhost` origins;
   - a missing or wrong content type;
   - an oversized body;
   - malformed JSON;
   - an invalid name, including `..`, separators, uppercase, and length
     extremes.

   `/api/status` and its tests are unchanged.
6. **Save and load fidelity (P3-AC03).**
   - Save the success fixture with a sidecar. The bytes on disk equal
     `serialize_document` output.
   - Load it again: the workflow and digests are returned.
   - Running the loaded document through the endpoint, and headlessly
     through `run_slice_attempt`, gives the same semantic digest and metrics
     as running the original.
   - Changing only the sidecar leaves the semantic digest, plan, and metrics
     unchanged.
7. **Conflicts and outside edits.**
   - Saving to an existing name with no base digest returns `409` (V15).
   - Saving with a stale workflow digest returns `409`, with a summary that
     names the changed parameter and the added or removed node.
   - Saving with a stale sidecar digest refuses the whole save, leaving both
     files unchanged.
   - A base digest for a file that has since been removed returns `409`.
   - `compare` reports `changed` with the same summary after an outside
     edit, and `changed: false` otherwise.
8. **Load refusals.** These files each return `422` and are never rewritten:
   a malformed file, an unsupported schema version, an invalid workflow, and
   one over the size bound. A malformed or unsupported sidecar loads the
   workflow with `sidecarNotice`. Phase 1 layout metadata round-trips
   unchanged (V16).
9. **Storage safety.** Where the platform allows, a symlinked workflows
   directory or file is refused. Writes leave no temporary file behind, and
   an exclusive temporary file that already exists refuses the write. Files
   outside the naming rule are not listed.
10. **O3 publication tests.** Add three slice tests to
    `python/tests/test_slice_output.py`, mirroring the P2-EP05 §4.2
    challenges:
    - a mismatched read-back after a commit error is indeterminate and the
      attempt is kept;
    - a rollback failure while pending reports `failed-cleanup-incomplete`,
      leaving the pending record in place;
    - a partial proof write is never reported as success.
11. **Latency (D3.2).** With `npm.cmd run launch` running, the user times six
    `POST /api/slice/run` calls of the success fixture directly at
    `127.0.0.1:8000`, and six through the Vite proxy at `127.0.0.1:5173`.
    The first is reported separately as cold. If a typical warm call takes
    more than 2 seconds, stop and report to Central before P3-EP04. Note
    that the harness's `launch` may need the user to stop it afterwards.

## 6. Documentation and Architecture Boundaries

- **`.gitignore`.** Add only a comment naming `.vidap-local/workflows/` (F3).
  The existing `/.vidap-local/` rule already ignores it.
- **`CONTRIBUTING.md`.** Narrow updates:
  - the `.vidap-local/workflows/` local state;
  - the `/api/slice/` local channel, which is loopback-only, unauthenticated,
    and has no CORS.
- **`README.md`.** A narrow current-state update: the slice channel and
  save/load exist, and the editor does not.
- **Prohibited.** No change to:
  - `vidap_workflow`;
  - the slice handlers, metrics, run, artifact, or reference code;
  - fixtures, manifests, locks, CI, or web code.

## 7. Stop Conditions

Stop `Blocked` if:

- an endpoint would need a new dependency, a change to Phase 1 or the slice
  operations, or app-wide middleware that changes `/api/status`;
- metrics could only be shown by a route other than slot readback;
- safe atomic writes cannot be done without weakening the checks;
- warm latency exceeds 2 seconds; or
- a mandatory check cannot be reproduced.

## 8. Exact Authorized Worker Outputs

| Path | Purpose |
|---|---|
| `python/src/vidap_execution/app.py` | Include the slice router; `/api/status` unchanged |
| `python/src/vidap_execution/slice_api.py` | Router, guards, error envelope, contracts, validate, run, workflow endpoints |
| `python/src/vidap_execution/workspace.py` | Workflow and sidecar storage, digests, sidecar shape, change summary |
| `python/tests/test_slice_api.py` | Sections 5.1–5.5 |
| `python/tests/test_slice_workspace.py` | Sections 5.6–5.9 |
| `python/tests/test_slice_output.py` | Section 5.10 additions only; existing tests unchanged |
| `.gitignore` | F3 comment only |
| `CONTRIBUTING.md` | Narrow local-state and channel note |
| `README.md` | Narrow current-state update |
| `ViDAP_P3_EP03C_Implementation_Report.md` | Worker evidence and handoff |

Test state under `.vidap-local/` is cleaned by the tests. No other path may
change.

## 9. Worker Sequence and Final Attestation

1. **Baseline.** Confirm approval. Record branch, `HEAD`, the dirty baseline
   by owner, and both lock hashes. The locks must equal P3-EP03B's.
2. **Implement.** Implement Sections 4 and 5 and Section 6's documentation
   changes.
3. **Attestation.** On the final tree, the user runs, in order:
   1. `npm.cmd run check`
   2. `npm.cmd run coverage`
   3. `npm.cmd run deps:inventory`
   4. `npm.cmd run license:check`
   5. `npm.cmd run deps:audit`
   6. `git --no-pager diff --check`
   7. the lock hashes
   8. `git --no-pager status --porcelain --untracked-files=all` and the
      staged list
   9. the Section 5.11 timing

   Any in-scope repair needs a complete rerun.
4. **Direct checks.** Check exact path scope; that `.vidap-local/` is clean
   after the tests; line endings; whitespace; final newlines; no user paths
   or secrets; and that no listener remains after the timing run.
5. **Stop.** Write the report and stop. Do not stage, commit, push, validate,
   accept, or start P3-EP04.

## 10. Required Implementation Report

The report must cover:

- approval and baseline;
- the endpoint table with request and response shapes, and the guard table
  with codes;
- the host-check choice;
- the storage design, write order, and limits;
- the sidecar rules;
- the change summary;
- evidence for each Section 5 item;
- the O3 tests;
- the latency table;
- the full attestation;
- a validation handoff.

It must contain no user paths or full logs.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP03C-AC01 | Approval, prerequisites, baseline, and ownership are evidenced. |
| EP03C-AC02 | Only Section 8 paths change; locks equal P3-EP03B's; `/api/status` and the slice operations are unchanged. |
| EP03C-AC03 | Contracts come only from `SLICE_REGISTRY` and match it exactly. |
| EP03C-AC04 | Validate and run return Phase 1 diagnostics unchanged and allocate nothing for an invalid document. |
| EP03C-AC05 | Run metrics come only from slot readback; a failed or indeterminate publication returns none. |
| EP03C-AC06 | One run at a time; a concurrent run is refused, not queued. |
| EP03C-AC07 | Host, origin, content type, size, JSON, and name guards refuse with fixed codes and no side effects; no CORS, OpenAPI, or docs. |
| EP03C-AC08 | Saved files are canonical serializer output; save, load, and run fidelity holds; presentation changes cannot change semantics. |
| EP03C-AC09 | Digest conflicts cover workflow and sidecar together; no silent overwrite; backend-built summaries are correct. |
| EP03C-AC10 | Load refuses malformed, unsupported, and invalid files without repair; a bad sidecar degrades with a notice; V16 holds. |
| EP03C-AC11 | Storage refuses unsafe paths and names and writes atomically. |
| EP03C-AC12 | The O3 slice publication tests are added and pass. |
| EP03C-AC13 | Warm endpoint latency is recorded and within 2 seconds, or the packet stopped for Central. |
| EP03C-AC14 | The full final attestation passes on Windows, with hygiene and cleanup checked. |
| EP03C-AC15 | Fresh independent validation returns `Accept`. |
| EP03C-AC16 | Central reconciles before P3-EP04 is drafted. |

## 12. Independent Validation

The validator reads the inputs, the delta, and the report. It drives every
endpoint itself, including:

- every guard with hostile inputs;
- concurrent runs;
- outside edits between load and save;
- stale sidecar digests;
- crafted names and sidecars;
- metrics readback when publication fails.

It recomputes the digests and summaries, and confirms that there is no UI,
CORS, background job, or new dependency. It reproduces the attestation, or
confirms the user-run Windows evidence. It may create and clean only ignored
transient state. It returns `Accept`, `Revise`, or `Blocked`.

## 13. Handoff Prompts

### Worker

> Execute the approved `ViDAP_P3_EP03C.md` v0.1 as the bounded worker. Read every governing input, follow the `CONTRIBUTING.md` workaround for all Windows steps, implement only the Section 8 paths, complete the final attestation including the live latency check, and stop with `ViDAP_P3_EP03C_Implementation_Report.md` and a validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P3-EP04.

### Validator

> Act as the independent validator for `ViDAP_P3_EP03C.md` v0.1. Read the packet, its governing inputs, and the implementation report; verify every acceptance criterion against the actual files and real endpoint behavior, with hostile inputs and concurrency challenges. Do not edit tracked files, accept for Central, or begin P3-EP04. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

P3-EP03C is complete and reconciled in
`ViDAP_P3_EP03C_Validation_and_Reconciliation.md`. WS3.3 is complete;
P3-EP04 (editor core) is ready to draft and needs its own approval.
