# ViDAP P1-EP05 — Versioning and Representative Workflows

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Bounded compatibility behavior and controlled-fixture implementation |
| Parent phase plan at authorization | `ViDAP_Phase_1_Plan.md` version 1.9 |
| Prerequisites | P1-EP01 through P1-EP04 complete |
| Prerequisite reconciliations | `ViDAP_P1_EP01_Validation_and_Reconciliation.md`; `ViDAP_P1_EP02_Validation_and_Reconciliation.md`; `ViDAP_P1_EP03_Validation_and_Reconciliation.md`; `ViDAP_P1_EP04_Validation_and_Reconciliation.md` |
| Workstream | WS1.5 — Compatibility proof |
| Authorized worker report | `ViDAP_P1_EP05_Implementation_Report.md` |
| Created | 2026-09-21 |
| Approved | 2026-09-21 by explicit user direction |
| Completed | 2026-09-21 by explicit Central acceptance |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved this exact version on 2026-09-21. That approval authorizes one
fresh worker to make the accepted strict version/unknown-content policy visible
through the workflow validation boundary and to add only the small, controlled
representative fixtures named in Section 7. The worker may modify only those
paths.

This packet does not authorize a migration, a second supported schema version,
a forward-compatible reader, a new canonical document field, arbitrary
extension preservation, node-contract changes, UI/API behavior, persistence,
process launch, execution planning/caching, data/ML operations, export,
plugin discovery, dependencies/locks, CI changes, remote mutation, or P1-EP06
work.

## 2. Plain-English Packet Intent

### What this packet will build

It makes the project’s compatibility promise explicit and testable: version
`1.0` is the only supported workflow version; malformed, older, future, or
unknown-content documents visibly fail; and representative valid, invalid,
branched, and versioned workflow documents prove the behavior without a UI or
runner.

### Why this is needed

Without actual examples and a stable diagnostic route for text input, the
project could claim a safe format while silently accepting, dropping, or
misreading a future document. The fixtures make the chosen strict policy
reviewable in source control before real workflow persistence or export exist.

### What it does not imply

No migration is implemented, promised, or simulated. Fixtures are test
consumers, not semantic authorities or product datasets. The packet does not
make workflows durable application state, nor does it add a browser/API file
upload or a user-facing import feature.

## 3. Governing Inputs

The worker and validator must read:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§6–7, 16, 18–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially invariants 3–4,
   10–13 and Phase 1/Phase 2 boundaries.
4. `ViDAP_Roadmap.md` version 3.0, especially P1 and its next action.
5. `ViDAP_Phase_1_Plan.md` version 1.9, especially D1.6, WS1.5, the
   fixture guardrail, and P1-AC07 through P1-AC11.
6. `ViDAP_P1_EP01_Validation_and_Reconciliation.md`, authoritative for
   accepted D1.1, D1.5, D1.6, and D1.7.
7. `ViDAP_P1_EP02_Validation_and_Reconciliation.md`,
   `ViDAP_P1_EP03_Validation_and_Reconciliation.md`, and
   `ViDAP_P1_EP04_Validation_and_Reconciliation.md`, authoritative for the
   accepted document, contract, registry, validation, and diagnostic layers.
8. Accepted D0.7 controlled-fixture policy and its Phase 0 reconciliation.
9. This packet.

## 4. Inherited Compatibility and Fixture Contract

The implementation must preserve these accepted decisions:

1. The sole initial supported envelope is root
   `format: "vidap.workflow"` and `schemaVersion: "1.0"`.
2. Missing, malformed, older, and future versions fail visibly as
   `unsupported`. They are not defaulted, upgraded, stripped, or treated as
   valid.
3. Unknown core fields are structural errors; unknown node types are
   unsupported; unknown parameter keys/values remain semantic errors. Nothing
   unknown is silently discarded or reserialized as accepted meaning.
4. There is no migration because no predecessor document exists. Do not create
   a fake `0.x` fixture, a migration table, an upgrade function, or a
   compatibility claim beyond strict `1.0`.
5. A future extension container may be defined only by an approved future
   version. A `1.0` reader visibly rejects an extension field, namespace, or
   version it does not understand.
6. Text-input validation returns the accepted immutable diagnostic collection,
   not a raw parser exception, bare boolean, UI/API response, or file I/O
   result. Decode/parser detail is optional technical detail only.
7. Representative fixtures are UTF-8 synthetic JSON, each below 16 KiB, with
   a total below 64 KiB. They contain no personal, sensitive, credential,
   path, network, telemetry, proprietary, or dataset content.
8. The fixture manifest is metadata only. It declares ID/version,
   repository-relative path, byte size, SHA-256, synthetic provenance, MIT
   terms, creation method, expected result, permitted consumers, privacy
   attestation, Central reviewer, and review date. Fixtures do not define
   product semantics over the accepted source contracts.

## 5. Required Implementation

### 5.1 Text compatibility boundary

Add a small pure public validation entry point that accepts JSON text and a
static `NodeRegistry`, returning the same ordered immutable diagnostics used
for an in-memory `WorkflowDocument`.

It must convert decode/envelope failures to stable diagnostics with:

- a structural category for malformed JSON, non-object root, missing/invalid
  core envelope shape, duplicate object names, and unknown core fields; and
- an unsupported category for a missing, malformed, older, or future format/
  schema version and for a `1.0` extension field/namespace/version that is
  not understood.

The source decoder may retain a narrow internal exception, but callers of the
new validation entry point must receive diagnostics with stable code, category,
affected document field, plain-English message/remedy, and safe optional
technical detail. The boundary must not read a path, write a file, mutate the
document, repair content, preserve unknown content, launch a process, access a
network, or add an HTTP/UI representation.

### 5.2 Strict no-migration policy

Make the accepted `1.0` behavior explicit in code/tests:

- only exact `format` and `schemaVersion` values are accepted;
- missing/malformed/older/future versions return an unsupported diagnostic;
- no migration registry, version alias, fallback, transform, or history is
  created; and
- unknown core fields and extension content cannot be silently retained,
  defaulted, or serialized back as valid `1.0` meaning.

Do not add another supported version or change the canonical document model.

### 5.3 Controlled representative fixtures

Create exactly these UTF-8 JSON fixtures and one metadata manifest:

| Path | Required purpose and expected outcome |
|---|---|
| `fixtures/p1-ep05/valid-branched-v1.json` | Valid `1.0` branched specimen using only the two non-operational contract specimens; decodes, validates with no diagnostics, and round-trips deterministically. |
| `fixtures/p1-ep05/invalid-unknown-node-v1.json` | Valid `1.0` envelope containing an unregistered node type; validates with the stable unsupported-node diagnostic. |
| `fixtures/p1-ep05/invalid-unknown-core-field-v1.json` | `1.0` text with an extra core field; returns a stable structural unknown-core-field diagnostic and is not silently preserved. |
| `fixtures/p1-ep05/unsupported-schema-version-v2.json` | Correctly shaped future-version text; returns a stable unsupported-version diagnostic without migration. |
| `fixtures/p1-ep05/fixture-manifest.json` | D0.7 metadata for the four fixtures, including exact final byte size and SHA-256. |

The valid specimen must actually branch from one source output to two sink
inputs while satisfying all required sink inputs through declared non-
operational contracts. It may not add a real data/ML node, operation key, UI
metadata, execution hint, or user data.

Fixture files are read only by P1-EP05 tests and later Phase 1 validation/
closeout evidence. They must not be served, treated as application input,
loaded automatically by the registry, or consumed by the Phase 0 shell.

### 5.4 Tests

Add tests that:

1. verify fixture-manifest identity, provenance, size, SHA-256, terms,
   permitted consumers, and expected-result metadata against the exact fixture
   bytes;
2. prove valid branched `1.0` fixture decode, no diagnostics, full/semantic
   deterministic round trip, and invariance under JSON object-member order;
3. prove the unknown-node, unknown-core-field, and future-version fixtures
   yield the expected stable diagnostics;
4. independently exercise missing, malformed, and older version values;
5. confirm no migration, unknown-content preservation, document mutation,
   file-writing, UI/API, execution, data/ML, export, plugin, or process
   behavior is present; and
6. retain all P1-EP02 through P1-EP04 behavior and test boundaries.

## 6. Preconditions and Stop Gates

Before modifying a file, the worker must confirm and record:

1. This exact packet has explicit execution approval.
2. P1-EP01 through P1-EP04 are complete and their reconciliation records are
   present and unsuperseded.
3. Current branch, commit, sanitized remote identity, worktree state,
   pre-existing work, output collisions, both lock hashes, and the existing
   fixture inventory/aggregate size.
4. Node 24/npm and normal Windows uv-managed CPython 3.14 are callable. A
   restricted `uv.exe` denial must be retried through the normal Windows
   path before a project prerequisite failure is reported.
5. Inherited locked setup and aggregate check pass before the worker change.
6. The proposed fixture paths are absent and do not collide with user work.
7. A new bounded temporary location outside the repository and OneDrive is
   available for clean-copy proof and safe removal.

Stop with a blocker if strict `1.0` compatibility cannot be preserved, a
fixture needs data/ambiguous terms/external content, a hash/size/provenance
fact cannot be reproduced, an exact output path collides, or any required
change would add a migration, a source-of-truth conflict, a dependency,
product behavior, or output beyond Section 7.

## 7. Exact Authorized Repository Outputs

The worker may create or modify only:

| Path | Authorized purpose |
|---|---|
| `python/src/vidap_workflow/serialization.py` | Stable internal decode categorization needed for the strict text boundary only. |
| `python/src/vidap_workflow/validation.py` | Pure text-to-diagnostic validation entry point only. |
| `python/src/vidap_workflow/__init__.py` | Deliberate public export for the text validation entry point only. |
| `python/tests/test_workflow_compatibility.py` | Fixture/strict-version/unknown-content tests only. |
| `fixtures/p1-ep05/valid-branched-v1.json` | Controlled valid representative fixture. |
| `fixtures/p1-ep05/invalid-unknown-node-v1.json` | Controlled invalid representative fixture. |
| `fixtures/p1-ep05/invalid-unknown-core-field-v1.json` | Controlled invalid representative fixture. |
| `fixtures/p1-ep05/unsupported-schema-version-v2.json` | Controlled versioned representative fixture. |
| `fixtures/p1-ep05/fixture-manifest.json` | Required fixture provenance and integrity metadata. |
| `ViDAP_P1_EP05_Implementation_Report.md` | Sanitized worker evidence and self-attestation. |

No other path may be created, modified, moved, staged, committed, or deleted.
Do not alter document/contract/registry/diagnostic source, existing tests,
manifests, locks, configuration, CI, web code, execution/experiment/export
packages, governing documents, or prior decision/reconciliation records.

## 8. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read all governing inputs and record baseline/pre-existing work, fixture
   inventory, output collisions, and lock hashes.
2. Run `npm.cmd run setup` and `npm.cmd run check` against the inherited
   baseline. Stop if either fails before the worker change.
3. Implement only Section 7. Generate fixture hashes/sizes from their exact
   final bytes and verify manifest values before proceeding.
4. Run focused compatibility tests while implementing. Then run the complete
   final attestation in this order:
   - `npm.cmd run check`;
   - `npm.cmd run coverage`;
   - `npm.cmd run deps:inventory`;
   - `npm.cmd run license:check`;
   - `npm.cmd run deps:audit`; and
   - `git diff --check`.
5. If a final check finds a worker-caused issue, fix it only within Section 7
   and rerun the *entire* sequence from the first command. Do not report
   completion unless every required command passes. Stop with evidence if a
   failure is unrelated or needs broader authority.
6. Confirm both locks are byte-identical; recheck fixture size/hash/manifest
   metadata; inspect exact scope, aggregate fixture size, ignored state, text
   policy, sensitive-content scan, and absence of listener/log/cache/
   environment/temporary-copy residue.
7. In a new clean copy outside the repository and OneDrive, run locked setup,
   focused compatibility tests, and `npm.cmd run check`; confirm fixture
   metadata/integrity and safely remove only the exact bounded temporary copy
   and caches.
8. Write the implementation report and stop for independent validation. Do
   not self-validate, stage, commit, push, alter remote state, or begin
   P1-EP06.

## 9. Required Worker Evidence

The report must contain:

1. Packet/version/approval, governing inputs, baseline, sanitized remote,
   pre-existing work, fixture inventory, exact scope, and collision evidence.
2. Before/after lock hashes and confirmation that no dependencies/manifests/
   locks/configuration/CI/runtime policy changed.
3. A requirement-to-path/test mapping for Sections 4–5.
4. A strict compatibility table covering supported, missing, malformed, older,
   future, unknown-core-field, unknown-extension, and unknown-node behavior.
5. Fixture manifest, size/hash/provenance/terms/privacy/consumer evidence and
   explicit confirmation that fixtures are non-product test consumers.
6. Focused-test and complete final-attestation results, including any repair/
   rerun loop.
7. Clean-copy proof and bounded cleanup evidence.
8. Scope, hygiene, sensitive-content, ignored-state, listener, and final Git
   evidence.
9. Criterion-by-criterion worker self-assessment clearly labeled as not
   independent validation or Central acceptance.

## 10. Acceptance Criteria

P1-EP05 may be accepted only when:

- **EP05-AC01:** Authority, prerequisites, baseline, fixture inventory,
  pre-existing work, locks, and exact scope are accurately recorded.
- **EP05-AC02:** Only the ten Section 7 paths are created/modified by the
  worker; no unauthorized/generated residue remains.
- **EP05-AC03:** The text compatibility boundary returns stable actionable
  diagnostics rather than raw decode exceptions or a bare boolean.
- **EP05-AC04:** Exact `vidap.workflow`/`1.0` is the sole supported
  envelope; missing/malformed/older/future versions visibly fail as
  unsupported with no fallback or migration.
- **EP05-AC05:** Unknown core/extension content visibly fails as structural
  or unsupported as appropriate; it is never silently retained, defaulted,
  stripped, or reserialized as accepted meaning.
- **EP05-AC06:** The valid branched fixture is valid, deterministic,
  UI-independent, and uses no product operation or execution hint.
- **EP05-AC07:** Invalid, unknown-node, unknown-core-field, and future-version
  fixtures produce the declared stable outcomes.
- **EP05-AC08:** Every new fixture is synthetic UTF-8 JSON, individually
  below 16 KiB and collectively below 64 KiB; its manifest has complete,
  correct provenance/integrity/purpose/consumer/privacy metadata.
- **EP05-AC09:** Fixtures are consumed only by P1-EP05 tests and later Phase
  1 validation/closeout evidence, never automatically loaded, served, or
  treated as product data/state.
- **EP05-AC10:** No migration, second version, schema artifact, dependency,
  UI/API, persistence, execution, data/ML, export, plugin/discovery, or Phase
  2 behavior is introduced.
- **EP05-AC11:** Tests preserve all P1-EP02 through P1-EP04 guarantees and
  cover strict versions, unknown content, manifest integrity, valid/invalid/
  branched behavior, and deterministic round trips.
- **EP05-AC12:** Baseline setup and complete post-change final attestation,
  including quality, coverage, inventory, license, advisory, clean-copy,
  lock, fixture, and hygiene checks, pass after any worker-caused repair.
- **EP05-AC13:** Locks remain byte-identical; no dependency, manifest,
  configuration, CI, package-manager, or runtime policy changes occur.
- **EP05-AC14:** Clean-copy evidence/cleanup is bounded and leaves no residue.
- **EP05-AC15:** The report is accurate, sanitized, and distinguishes worker
  evidence, pre-existing work, self-attestation, and independent validation.
- **EP05-AC16:** A fresh independent validator returns `Accept` with no
  unresolved Critical or High finding.
- **EP05-AC17:** Central explicitly accepts P1-EP05 before P1-EP06 is drafted.

## 11. Independent Validation Contract

A fresh independent validator must:

1. Read all governing inputs, prerequisite reconciliations, this packet,
   every Section 7 artifact, and the worker report.
2. Independently challenge text decode/version/unknown-content outcomes,
   stable code/category/actionability, no-migration behavior, fixture bytes/
   hashes/sizes/manifest metadata, and permitted-consumer boundaries.
3. Verify valid, invalid, branched, and versioned fixture behavior, including
   deterministic full/semantic round trips and layout/member-order invariance.
4. Reproduce the full final attestation, lock invariance, clean-copy proof,
   fixture integrity, cleanup, hygiene, and exact scope.
5. Confirm no P1-EP06/Phase 2 or prohibited product behavior entered.
6. Return exactly `Accept`, `Revise`, or `Blocked` with criterion-linked
   findings and owners.

The validator may not edit files, accept for Central, alter remote state, or
begin P1-EP06.

## 12. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P1_EP05.md` version 0.1 as the bounded compatibility-and-fixture worker. Read every governing input and all P1 reconciliations, then follow the packet exactly. Modify only the ten Section 7 paths. Implement only the pure strict text-to-diagnostic compatibility boundary and the four named synthetic representative workflow fixtures plus their integrity manifest. Preserve exact `1.0` support: do not add a migration, a second version, fallback, unknown-content preservation, dependencies, schemas, UI/API/process behavior, persistence, execution, data/ML, export, plugin/discovery, CI, or remote changes. Verify all fixture metadata against final bytes. Run the full final attestation; if it finds a worker-caused issue, fix it only within scope and rerun the complete sequence until it passes. Stop with the implementation report and independent-validation handoff; do not self-validate, accept for Central, stage/commit/push, or begin P1-EP06.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P1_EP05.md` version 0.1. Read all governing inputs, all prerequisite reconciliations, every Section 7 artifact, and `ViDAP_P1_EP05_Implementation_Report.md`. Follow Section 11 exactly. Independently challenge strict text decoding/version/unknown-content behavior, diagnostic stability/actionability, no-migration enforcement, fixture hashes/sizes/manifest metadata, permitted-consumer limits, valid/invalid/branched/versioned fixture results, deterministic round trips, and layout/member-order invariance. Reproduce full attestation, unchanged locks, clean-copy proof, fixture integrity, cleanup, hygiene, and exact scope. Confirm no UI/API, execution, persistence, data/ML, export, plugin/discovery, P1-EP06, or Phase 2 behavior entered. Do not edit files, accept for Central, change remote state, or begin P1-EP06. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

## 13. Next Action

P1-EP05 is complete. Its independent `Accept` and Central acceptance are
recorded in `ViDAP_P1_EP05_Validation_and_Reconciliation.md`. Central may now
draft P1-EP06 — Phase 1 closeout and reconciliation; that packet needs its own
approval before any worker begins it.
