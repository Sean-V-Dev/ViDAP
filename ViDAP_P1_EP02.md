# ViDAP P1-EP02 — Workflow Model and Serialization

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Execution approved | 2026-09-20 by explicit user direction |
| Completed | 2026-09-20 |
| Packet type | Bounded Python workflow-kernel implementation |
| Parent phase plan | `ViDAP_Phase_1_Plan.md` version 1.2 |
| Prerequisite | P1-EP01 complete; D1.1–D1.7 accepted |
| Prerequisite reconciliation | `ViDAP_P1_EP01_Validation_and_Reconciliation.md` |
| Workstream | WS1.2 — Canonical document kernel |
| Authorized worker report | `ViDAP_P1_EP02_Implementation_Report.md` |
| Central reconciliation | `ViDAP_P1_EP02_Validation_and_Reconciliation.md` |
| Created | 2026-09-20 |
| Owner | Central |

---

## 1. Authorization Boundary

This approved packet authorizes one bounded worker to implement the accepted
canonical workflow document, identity/reference value objects, deterministic
serialization/deserialization, and isolation of optional layout metadata. The
worker may modify only the Section 7 paths.

This packet does not authorize node contracts or registry implementation,
port-type/cardinality validation, parameter validation, structured diagnostic
implementation, migration behavior, fixture files, UI/editor work, API
binding, persistence, process launch, execution planning, caching, data/ML
operations, export, dynamic extension loading, dependency changes, lockfile
changes, CI changes, remote mutation, or P1-EP03 and later work.

## 2. Plain-English Packet Intent

### What this packet will build

It creates the small Python-owned in-memory form of a workflow document and
the reliable way to turn that form into readable JSON and back. It gives
workflows stable IDs, explicit directed edges, and an optional place for visual
layout that cannot affect semantic workflow meaning.

### Why this is limited

The product needs one workflow language before a UI, runner, or exporter can
consume it. But this packet must not decide whether a node is valid, connect
real data-science operations, or determine the order in which anything runs.
Those concerns belong to later P1 and P2 packets.

### How success will be demonstrated

Python tests will construct valid minimal and branched documents without a
browser, serialize them deterministically, deserialize them, and prove that
layout, collection order, and construction order do not change the semantic
document representation. Tests will also demonstrate safe rejection of
malformed JSON/envelope input without claiming the richer diagnostic contract
reserved for P1-EP04.

## 3. Governing Inputs

The worker and validator must read these sources in authority order:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§6–7, 16, 18–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially invariants 3–4,
   10–13 and Phase 1/Phase 2 boundaries.
4. `ViDAP_Roadmap.md` version 2.3, especially P1, checkpoint A1, and the
   current next action.
5. `ViDAP_Phase_1_Plan.md` version 1.2, especially WS1.2, Sections 4,
   7–10, and P1-AC01 through P1-AC12.
6. `ViDAP_P1_EP01.md` version 0.1 and
   `ViDAP_P1_EP01_Validation_and_Reconciliation.md`, authoritative for
   accepted D1.1–D1.7.
7. Accepted Phase 0 reconciliation records, especially the Python workspace,
   Node 24/npm plus uv-managed CPython 3.14, quality/test, dependency/license,
   fixture, and hygiene decisions.
8. This packet.

The P1-EP01 reconciliation is authoritative for the selected D1 decisions.
This packet implements only the D1.1–D1.2 subset while preserving D1.3–D1.7
as constraints for later packets.

## 4. Inherited Decisions and Implementation Contract

The implementation must faithfully preserve:

1. A workflow is an open UTF-8 JSON document with root
   `format: "vidap.workflow"` and `schemaVersion: "1.0"`.
2. Semantic document collections are identified by stable opaque lowercase
   UUIDv4 text. The worker must not introduce sequential IDs, labels, array
   indexes, creation order, or UI state as identity/reference authority.
3. Nodes and edges have independent IDs. An edge has one directed output
   endpoint and one directed input endpoint. A port reference is the pair of
   node ID and immutable contract port key.
4. Layout/viewport metadata is optional, explicitly non-semantic, and may not
   become an alternate store for edges, ports, parameters, types, validation,
   or execution hints.
5. Canonical full-document serialization is readable and deterministic when a
   serializer controls output. Semantic serialization excludes layout and is
   invariant under layout changes, construction order, collection order, and
   JSON object-member order.
6. A JSON Schema may later be a supplementary validation aid; do not create a
   schema artifact or select/install a validator package here.
7. Exact nominal types, cardinality, required inputs, parameter/default rules,
   registry lookup, detailed diagnostics, unknown-node handling, and
   migration/extension behavior are not implemented in this packet. The model
   must leave room for their later declarative implementation without
   inventing their validation behavior now.
8. Parsing may reject malformed JSON or an invalid basic envelope through a
   narrow decode exception. It must not expose this as the Phase 1 structured
   diagnostic contract, attempt repair, silently discard content, or perform
   semantic graph validation.
9. No method may calculate dependency order, execute a node, invoke a Python
   data/ML library, write a workflow to disk, open a network connection, or
   use a browser/API/process boundary.

## 5. Preconditions and Stop Gates

Before modifying a file, the worker must confirm and record:

1. This exact packet version has explicit execution approval.
2. P1-EP01 is complete and its reconciliation remains present and
   unsuperseded.
3. Current branch, commit, sanitized remote identity, worktree state,
   pre-existing changes, output-path collisions, and both lock hashes.
4. Node 24/npm and normal Windows uv-managed CPython 3.14 are callable. If
   restricted execution cannot call `uv.exe`, retry through the normal
   Windows path before reporting a project prerequisite failure.
5. The existing locked setup and aggregate check pass before the worker's
   change, with unchanged locks.
6. The Section 7 paths are free of conflicting user work.
7. A new, bounded temporary location outside the repository and OneDrive is
   available for clean-copy evidence and can be removed safely.

Stop and report a blocker if a needed change would require a dependency,
manifest/lock update, fixture, schema artifact, UI/API/process behavior,
semantic validation, migration, registry implementation, unsafe cleanup, or
any output beyond Section 7. Do not solve a stop condition by expanding the
packet.

## 6. Required Implementation

### 6.1 Python ownership and public surface

Implement the kernel only under `python/src/vidap_workflow/`. Its public
surface may expose:

- immutable value objects for a workflow document, node, edge, endpoint, and
  optional non-semantic layout metadata;
- explicit constructors or narrowly scoped factory functions for valid
  well-formed values;
- deterministic full-document JSON serialization;
- deterministic semantic-only JSON serialization; and
- JSON deserialization for the selected `vidap.workflow`/`1.0` envelope.

Use only Python 3.14 standard-library functionality already available through
the accepted runtime. Do not add a direct dependency or write a custom general
JSON/schema/UUID/graph framework.

The root `vidap_workflow` public exports must be deliberate and small. It
must not import `vidap_execution`, `vidap_experiments`, `vidap_export`,
FastAPI, Uvicorn, or web code.

### 6.2 Document and reference representation

The document must represent:

- root `format`, `schemaVersion`, and `workflowId`;
- a semantic node collection, where a node has its stable ID, node type ID,
  optional display label, and a preserved parameter-value mapping;
- a semantic edge collection, where each edge has its stable ID and explicit
  source/target endpoint values; and
- optional layout/viewport metadata stored separately from semantic node/edge
  content.

Document/node/edge IDs must use lowercase UUIDv4 text. Node-type and port keys
are non-empty stable strings; no label, object position, or object-member
ordering is a reference. A model constructor may enforce its own local value
shape and ID format, but it must not claim that semantic graph validity,
registry membership, type compatibility, cardinality, required inputs, or
parameter constraints have been checked.

### 6.3 Serialization and decode boundary

The serializer must:

- emit UTF-8 JSON text with a documented stable indentation/newline policy;
- use stable lexicographic object-key ordering;
- serialize nodes and edges by stable ID, not insertion/construction order;
- retain optional layout only in full-document output;
- emit semantic-only output without layout/viewport metadata; and
- avoid timestamps, random values, environment data, source paths, and
  generated execution information.

The decoder must accept legal JSON object-member order and reconstruct the
same canonical document representation. It must reject invalid JSON, non-object
root values, missing/incorrect `format` or `schemaVersion`, and malformed
basic value shapes without silent repair. Its narrow exception is a local
decode-boundary signal only. P1-EP04 owns stable diagnostic codes, severities,
affected-element references, remedies, aggregation, and structural/semantic
validation behavior.

### 6.4 Required tests

Use only inline, synthetic test values. Do not add a controlled fixture file.
The tests must prove:

1. A minimal document can be constructed, serialized, deserialized, and
   serialized identically.
2. A branched document round-trips without changing IDs, endpoints, node
   types, labels, parameter values, or edge identity.
3. Equivalent documents built with different construction/collection order
   produce identical semantic JSON and stable full JSON.
4. Changing only layout/viewport metadata changes neither semantic JSON nor
   semantic document equality.
5. Reordered JSON object members decode to the same canonical representation.
6. Bad JSON and invalid basic envelopes fail through the narrow decode
   boundary without a browser, server, or process.
7. Public imports do not transitively import execution, experiment, export,
   FastAPI, Uvicorn, or web code.
8. No test claims type/cardinality/parameter/registry/cycle validation,
   diagnostics, migration, extension, execution order, or real operation
   behavior.

## 7. Exact Authorized Repository Outputs

The worker may create or modify only:

| Path | Authorized purpose |
|---|---|
| `python/src/vidap_workflow/__init__.py` | Deliberate small public kernel exports only. |
| `python/src/vidap_workflow/document.py` | Immutable document/identity/edge/endpoint/layout values and deterministic conversion helpers. |
| `python/src/vidap_workflow/serialization.py` | Full and semantic JSON encode/decode boundary only. |
| `python/tests/test_workflow_document.py` | Inline synthetic unit tests required by Section 6.4. |
| `ViDAP_P1_EP02_Implementation_Report.md` | Sanitized worker evidence and self-attestation. |

The worker may not alter any other path. In particular it must not edit
`pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json`,
existing test/configuration files, the web application, execution/experiment/
export packages, CI, fixtures, decision/reconciliation records, or governing
documents.

## 8. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read every governing input and record baseline branch/commit/worktree,
   output collisions, and lock hashes.
2. Run `npm.cmd run setup` and `npm.cmd run check` against the inherited
   baseline. Stop if they fail before the worker change.
3. Implement only the five Section 7 paths and keep all model examples/test
   data inline and synthetic.
4. Run focused Python tests while implementing, then run the complete final
   attestation in this order:
   - `npm.cmd run check`;
   - `npm.cmd run coverage`;
   - `npm.cmd run deps:inventory`;
   - `npm.cmd run license:check`;
   - `npm.cmd run deps:audit`; and
   - `git diff --check`.
5. If a final command finds an issue caused by the worker's authorized change,
   fix it and rerun the entire final-attestation sequence from the first
   command. The worker may not report completion until the whole sequence
   passes. If a failure is unrelated or cannot be fixed within Section 7,
   stop with a blocker and evidence.
6. Confirm both lock hashes remain byte-identical, inspect exact
   changed/untracked scope and ignored generated state, perform a
   sensitive-content scan, and confirm no listeners, logs, caches, temporary
   copies, or environments remain.
7. In a newly created clean copy outside the repository and OneDrive, run
   locked setup and the focused workflow tests plus `npm.cmd run check`;
   confirm the same deterministic results, then remove only that exact bounded
   temporary copy and its task-specific temporary caches.
8. Write the implementation report with final evidence and stop for
   independent validation. Do not self-validate, stage, commit, push, or begin
   P1-EP03.

## 9. Required Worker Evidence

The implementation report must include:

1. Packet/version/approval metadata, governing inputs, baseline commit,
   sanitized remote, pre-existing work, output collisions, and exact scope.
2. Before/after lock hashes and the statement that no dependency or lock
   authority changed.
3. A mapping from every Section 6 requirement and every test to the exact
   implemented path.
4. A plain-English account of the public API, document shape, identity
   boundaries, full versus semantic serialization, decode boundary, and what
   is deliberately not validated.
5. Focused and complete final-attestation command outcomes, including the
   required rerun loop when applicable.
6. Clean-copy setup/test/check evidence, bounded temporary-path/cleanup
   evidence, and no-listener conclusion.
7. Determinism/layout/order evidence and the absence of UI, execution,
   process, data/ML, export, persistence, migration, registry, and dynamic
   plugin behavior.
8. Exact file-scope, whitespace, sensitive-content, ignored-state, and final
   Git-status evidence.
9. A criterion-by-criterion worker self-assessment that clearly states it is
   not independent validation or Central acceptance.

The report must not contain secrets, absolute user paths, copied lockfile
bodies, environment dumps, or excessive command logs.

## 10. Acceptance Criteria

P1-EP02 may be accepted only when:

- **EP02-AC01:** Authority, accepted D1 decisions, prerequisites, baseline,
  pre-existing work, and exact file scope are correctly recorded.
- **EP02-AC02:** Only the five Section 7 paths are created or modified by the
  worker; no unauthorized file or generated state remains.
- **EP02-AC03:** The public Python workflow surface is small, deliberate, and
  imports no web, execution, experiment, export, FastAPI, or Uvicorn code.
- **EP02-AC04:** Document, node, edge, and endpoint identities use the
  accepted UUIDv4/reference rules; labels, indexes, and creation order are
  not identity authority.
- **EP02-AC05:** Full-document JSON is UTF-8, readable, deterministic, and
  contains the exact initial root discriminator/version.
- **EP02-AC06:** Semantic serialization excludes layout/viewport metadata and
  is invariant under layout, collection order, construction order, and JSON
  object-member order.
- **EP02-AC07:** Minimal and branched documents round-trip deterministically
  with semantic fields preserved.
- **EP02-AC08:** The decoder rejects malformed JSON and invalid basic envelope
  shapes without repair or silent content loss, while not claiming P1-EP04
  structured diagnostics.
- **EP02-AC09:** No schema artifact/validator package, node contract,
  registry, port type/cardinality validation, parameter validation,
  diagnostics, migration, extension, execution ordering, run/artifact state,
  persistence, UI/API, data/ML, export, or dynamic loading is introduced.
- **EP02-AC10:** Tests are inline, synthetic, deterministic, and prove the
  Section 6.4 behavior without a fixture, browser, server, network, or
  process.
- **EP02-AC11:** `npm.cmd run setup`, final `npm.cmd run check`,
  `coverage`, inventory, license, advisory, and clean-copy checks pass;
  failures caused by the worker are fixed and the full attestation rerun.
- **EP02-AC12:** Both lock authorities remain byte-identical; no dependency,
  manifest, alternate lock, package manager, global prerequisite, or runtime
  policy changes.
- **EP02-AC13:** Clean-copy evidence is outside the repository and OneDrive,
  is safely removed, and does not rely on prior generated state.
- **EP02-AC14:** No listener, cache, environment, report, temporary copy,
  sensitive content, or generated output remains tracked or unignored.
- **EP02-AC15:** Whitespace, text policy, sensitive-content scan, and
  `git diff --check` pass.
- **EP02-AC16:** The report accurately distinguishes worker implementation,
  pre-existing work, final self-attestation, and independent-validation
  status.
- **EP02-AC17:** A fresh independent validator independently reproduces
  bounded behavior and returns `Accept` without unresolved Critical or High
  finding.
- **EP02-AC18:** Central explicitly accepts P1-EP02 before P1-EP03 is drafted.

## 11. Independent Validation Contract

A fresh independent validator must:

1. Read all governing inputs, D1 acceptance, this packet, all Section 7
   artifacts, and the implementation report.
2. Inspect the document model, serialization boundary, public imports, tests,
   deterministic ordering, semantic/layout separation, and absence of
   validation/runtime/UI behavior.
3. Independently run the full final attestation and confirm lock invariance.
4. Reproduce a clean-copy setup plus focused workflow tests/check through a
   bounded temporary path, then verify cleanup.
5. Challenge at least one layout/order-invariance case and one malformed
   envelope/decode case.
6. Verify exact file scope, no hidden fixture/schema/dependency/configuration
   change, whitespace, sensitive-content hygiene, and absence of P1-EP03+
   work.
7. Return exactly `Accept`, `Revise`, or `Blocked` with
   criterion-linked findings and owners.

The validator may not edit files, accept implementation for Central, alter
remote state, or begin P1-EP03.

## 12. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P1_EP02.md` version 0.1 as the bounded workflow-model worker. Read every governing input, especially the accepted D1.1–D1.7 reconciliation, and follow the packet exactly. Modify only the five Section 7 paths. Implement only immutable Python workflow document/identity/edge/endpoint/layout values and deterministic full versus semantic JSON serialization/deserialization. Use only Python 3.14 standard-library functionality. Do not add dependencies, locks, fixtures, schemas, node contracts, registries, validation diagnostics, migration, UI/API/process behavior, execution ordering, persistence, data/ML, export, dynamic plugins, CI, or remote changes. Keep test data inline and synthetic. Run the required complete final attestation; if it finds a worker-caused issue, fix it and rerun the entire sequence until it passes. Stop with the implementation report and independent-validation handoff; do not self-validate, accept on Central's behalf, stage/commit/push, or begin P1-EP03.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P1_EP02.md` version 0.1. Read all governing inputs, the D1 reconciliation, every Section 7 artifact, and `ViDAP_P1_EP02_Implementation_Report.md`. Follow Section 11 exactly. Independently verify immutable Python workflow ownership, UUID/reference rules, deterministic full and semantic JSON behavior, layout/order invariance, basic safe decode rejection, small public imports, inline synthetic tests, and the deliberate absence of contracts/registry/diagnostics/migration/execution/UI/API/persistence/data/ML/export behavior. Reproduce the complete final attestation, unchanged locks, clean-copy evidence, cleanup, hygiene, and exact file scope. Do not edit files, accept on Central's behalf, mutate remote state, or begin P1-EP03. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

## 13. Next Action

P1-EP02 is complete. Independent validation returned `Accept`, and Central
accepted the result in `ViDAP_P1_EP02_Validation_and_Reconciliation.md` on
2026-09-20. Central may now draft P1-EP03 as a separate bounded packet. This
completion does not authorize P1-EP03 execution or later implementation.
