# ViDAP P2-EP02 — Execution Representation and Contract Bridge

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.2 |
| Packet type | Bounded immutable execution-representation implementation |
| Parent phase plan | `ViDAP_Phase_2_Plan.md` version 1.4 |
| Prerequisites | P2-EP01 complete; D2.1–D2.8 accepted |
| Prerequisite reconciliation | `ViDAP_P2_EP01_Validation_and_Reconciliation.md` |
| Workstream | WS2.2 — Execution representation |
| Authorized worker report | `ViDAP_P2_EP02_Implementation_Report.md` |
| Created | 2026-09-22 |
| Prior approval | Version 0.1 approved 2026-09-22; superseded by version 0.2 |
| Approved | Version 0.2 approved 2026-09-22 by explicit user direction |
| Central reconciliation | `ViDAP_P2_EP02_Validation_and_Reconciliation.md` |
| Completed | 2026-09-22 after independent `Accept` and Central reconciliation |
| Revision reason | Independent `Revise`: missing D2.2 contract/validation snapshot reference; digest property-order clarification |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved v0.1 on 2026-09-22. Independent validation found two High
issues. The worker repaired the digest property ordering within the
authorized scope and stopped at the omitted snapshot decision. This v0.2
clarified that decision and Central approved the revised version on
2026-09-22. The worker completed v0.2, independent validation returned
`Accept`, and Central accepted it in the reconciliation record above.

Approval of v0.2 authorizes the same bounded worker to finish the
immutable, layout-free representation and static binding metadata within
Section 7, then repeat all required evidence and seek fresh validation.

Approval does not authorize operation code or invocation, scheduling/topological
planning, dispatch, run records/IDs, artifacts, persistence, cache behavior,
runtime-error envelopes, data, models, fixtures, dependencies/locks, UI/API,
subprocesses/services, remote changes, or P2-EP03 work.

## 2. Plain-English Packet Intent

### What this packet will build

It creates the checked handoff between a valid workflow and the future engine:
a frozen execution recipe containing node identity/type, selected operation
key, resolved parameters, directed edge endpoints, binding revision, a
deterministic workflow-semantic digest, and a reference to the Phase 1
contract/validation snapshot used for preparation.

### Why the system needs it

The future engine must not reinterpret a workflow differently on each run or
consult visual layout. This boundary makes the engine input stable and
inspectable without treating the workflow document, registry, or generated
Python as a runtime implementation.

### What it enables

Later packets can derive a dependency schedule, invoke approved static
operations, and record runs from one frozen representation. This packet stops
before all of those actions.

### How we will know it works

Focused tests will prove that valid test-only declarative workflows with
explicit static bindings become immutable representations; display/order
changes do not alter their digest; invalid/unbound cases refuse before
dispatch; and no operation, schedule, process, file, artifact, cache, or UI
behavior exists.

## 3. Governing Inputs

The worker and validator must read:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§16, 18–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.3, especially invariants 3–8,
   11–14, 17–18, Phase 2, and strong validation scaling.
4. `ViDAP_Roadmap.md` version 4.1, especially P2 and checkpoint A2.
5. `ViDAP_Phase_2_Plan.md` version 1.4, especially D2.1–D2.2, Sections 7–10,
   and P2-AC02 through P2-AC04.
6. `ViDAP_P2_EP01_Validation_and_Reconciliation.md`, authoritative for the
   direct in-process seam, immutable representation, semantic digest, static
   binding map, and metadata-first/no-cross-run-cache limits.
7. All Phase 1 reconciliation records, especially the canonical document,
   static registry, validation/diagnostics, and strict compatibility boundary.
8. Accepted Phase 0 topology, runtime, quality, dependency, and fixture
   controls.
9. `UX refinement.txt` as Phase 3+ consultative direction only. Region state,
   visual layout, and interactive caching are not Phase 2 semantics.
10. This packet.
11. The existing `ViDAP_P2_EP02_Implementation_Report.md` as historical worker
    evidence, not as authority to replace v0.2 requirements.

## 4. Accepted Decisions Implemented Here

This packet implements only:

1. **D2.1:** one importable synchronous in-process preparation seam. It has no
   process lifecycle, cancellation, service, or operation invocation.
2. **D2.2:** an immutable representation produced only after Phase 1
   validation, a workflow-semantic digest, a contract/validation snapshot
   reference, and a static first-party binding map with explicit binding
   revision. Unknown/missing/unbound operation keys refuse preparation.

The digest is SHA-256 of a deterministic semantic projection containing the
accepted `vidap.workflow`/`1.0` envelope, workflow/node/edge IDs, node type
IDs, parameters, and directed endpoints. It excludes labels, layout, viewport,
JSON member order, construction/collection order, and other display metadata.
Semantically unordered collections are ordered by stable ID before encoding.
Invalid/unknown content or missing/duplicate stable ID refuses preparation
rather than receiving a chosen order.

Encode the workflow-semantic projection as compact UTF-8 JSON with object keys
recursively sorted by the RFC 8785 **UTF-16 code-unit property-order rule**.
Do not use Python's default Unicode code-point `sort_keys=True` order as a
substitute. Preserve the order of arrays whose order is semantically
meaningful. This is the accepted property-order rule, not a claim that the
entire encoder implements every RFC 8785 canonicalization rule.

The separate `contract_snapshot_ref` is a lowercase SHA-256 hex reference to
the exact declarative Phase 1 contracts used for this preparation. Derive it
only after successful Phase 1 validation from a deterministic, immutable
projection containing:

- a fixed validation-policy identifier `vidap.workflow-validation/1.0` and
  the accepted `vidap.workflow`/`1.0` format/schema envelope;
- each distinct node type **used by this workflow**, sorted by type ID, with
  its type ID and optional `operation_key` (distinguishing absence from text);
- every declared input and output port of those types, sorted by port key,
  including key, direction, nominal type, and input cardinality/requiredness;
- every declared parameter, sorted by key, including key, value kind,
  requiredness, whether a default is present, its JSON value when present,
  and the complete declarative constraints mapping and values.

Exclude display labels/descriptions, registry insertion order, unused node
definitions, document layout, and any runtime binding implementation. Preserve
JSON array order inside default/constraint values unless Phase 1 explicitly
defines an array as unordered. Sort all object properties recursively by the
same RFC 8785 UTF-16 rule, encode compact UTF-8 JSON, and hash those bytes with
SHA-256. The reference is a fingerprint, not a copy of the contracts or a
runtime authority; preparation still calls the existing Phase 1 validator.
The policy identifier names the currently accepted validation semantics; it
must be revised under a separately approved change when those semantics
change. Do not derive it from Python source bytes, paths, timestamps, or
diagnostic wording.

Keep `semantic_digest` as the workflow-only digest defined above. A changed
contract can leave that digest identical while changing `contract_snapshot_ref`
and therefore the representation. The reference is neither a cache key nor an
authorization to reuse results. Future execution must retain the reference
with its plan/run provenance and must not treat identical workflow digests
under different contract snapshots as the same validated execution input.

The representation may carry binding revision and operation keys. It may not
carry a callable, import path, command, URL, runtime result, cache key/event,
run ID, artifact path, seed, environment fingerprint, scheduling rank, or
runtime-error envelope.

## 5. Required Public Contract

The new `vidap_execution` package must expose this minimum Python-only surface.
Final names may differ only when the report maps them to this contract and
tests prove equivalent behavior.

| Concern | Required behavior |
|---|---|
| Static binding metadata | Immutable value mapping one non-empty operation key to a non-empty binding revision. It has no callable, import/module path, command, URL, or executable behavior. Duplicate keys reject deterministically. |
| Binding collection | Immutable explicit lookup only. No discovery, plugin, network, filesystem, environment, or document-driven loading. |
| Execution representation | Frozen values represent format/schema version, workflow ID, semantic digest, `contract_snapshot_ref`, binding revision, nodes, and directed edges. Collections are deterministically ID-stable but are not a schedule. |
| Node representation | Frozen node with node ID, type ID, operation key, binding revision, and resolved canonical parameters only. No result, callable, cache/event, run, artifact, or UI field. |
| Preparation seam | One synchronous function accepts `WorkflowDocument`, `NodeRegistry`, and explicit bindings; runs Phase 1 validation first; then constructs the representation only when every node has registered non-empty operation metadata and a matching static binding. |
| Preparation refusal | Invalid workflow preserves Phase 1 diagnostic evidence. Missing/unbound/mismatched binding refuses deterministically through a narrow preparation failure/value. It is not a D2.7 runtime-error envelope and no dispatcher starts. |
| Semantic projection/digest | A pure deterministic helper may be exposed for inspection/tests. It may not mutate input, read files, or claim to be a persisted workflow format. |
| Contract/validation snapshot reference | A required immutable lowercase SHA-256 hex value derived after validation from only the Section 4 policy identifier, accepted envelope, and complete relevant declarative node contracts. No display metadata, unused registry entries, source-code hash, external lookup, or separate registry revision is substituted for it. |

Existing non-operational Phase 1 specimens have no operation key and must
refuse preparation. Do not modify the Phase 1 registry to make them executable.
Tests may define small test-only declarative definitions with explicit operation
keys and matching non-callable binding metadata; they prove the bridge only.

## 6. Required Implementation and Test Evidence

The worker must prove:

1. Valid test-only declarative definitions with matching static bindings produce
   an immutable deterministic representation.
2. Equivalent member, node/edge collection, construction, label, and
   layout/viewport changes preserve semantic projection/digest, snapshot
   reference, and representation meaning.
3. A changed node type, parameter, directed endpoint, operation key, binding
   revision, workflow identity, or semantic member changes the representation,
   appropriate digest/reference, or refuses deterministically as appropriate.
4. Invalid Phase 1 workflows refuse before construction and retain ordered
   Phase 1 diagnostics without a runtime remapping.
5. Missing operation metadata, unbound key, duplicate binding key, and binding
   revision mismatch refuse without fallback, dynamic import, or
   document-selected executable behavior.
6. Binding/representation values are immutable; input-mapping mutation cannot
   alter an already constructed representation.
7. Static inspection and focused tests prove no callable/import/path/command/
   URL, schedule, result, run, artifact, cache, environment, seed, filesystem,
   subprocess, network, UI/API, data/ML, or export behavior entered.
8. For the **same valid document**, changing a used type's output-port nominal
   type (while keeping the workflow valid) changes `contract_snapshot_ref` and
   representation equality; the workflow-only semantic digest remains equal.
   Changes to used input-port cardinality/requiredness and parameter kind,
   default, or constraints likewise change the reference when valid. Changing
   only display metadata, declaration/registry order, or an unused definition
   does not. An omitted default differs from an explicit null default.
   Independent expected hashes must be reproducible from the stated
   projection. A non-ASCII object-key challenge must confirm UTF-16 property
   ordering for both digest and snapshot, including a supplementary-plane key
   versus a BMP key whose Python code-point order differs.

## 7. Exact Authorized Output and Scope

The worker may create or modify only:

| Path | Purpose |
|---|---|
| `python/src/vidap_execution/__init__.py` | Narrow explicit public execution-representation exports. |
| `python/src/vidap_execution/bindings.py` | Immutable static non-executable binding metadata and collection. |
| `python/src/vidap_execution/representation.py` | Immutable representation, semantic projection/digest, and preparation seam. |
| `python/tests/test_execution_representation.py` | Focused deterministic bridge and boundary tests. |
| `ViDAP_P2_EP02_Implementation_Report.md` | Sanitized worker evidence and self-attestation. |

No other tracked repository path may be created, modified, moved, staged,
committed, or deleted. Do not modify `vidap_workflow`, its registry/contracts,
existing tests, manifests, locks, CI, package configuration, fixtures, docs,
or governing files. Ignored generated state is permitted only for required
checks and must be cleaned or verified as ignored state as applicable.

## 8. Prohibited Scope

The worker must not implement or invoke an operation; add a callable to a
binding; create a graph schedule; execute a graph; assign a run ID; write an
artifact, record, cache, data, or temporary output; create a persistent
directory/format; implement runtime errors; add a fixture/dependency; change
Phase 1 semantics; add a service/process/network/UI/API/browser/data/ML/export/
plugin/agent/Phase 3+ behavior; alter remote state; stage/commit/push;
self-validate; accept for Central; or begin P2-EP03.

## 9. Required Worker Procedure

1. Read every governing input and the existing worker report. Record the
   target commit, branch, worktree state, v0.1 worker output versus pre-existing
   changes, and both lock hashes before resuming. Do not treat v0.1's partial
   evidence as satisfying the v0.2 final proof.
2. Run `npm.cmd run setup` and `npm.cmd run check` before implementation. If
   the restricted environment prevents the approved Windows `uv` path from
   running, use the documented normal Windows retry; do not substitute a
   different interpreter or unlock dependencies.
3. Implement only the Section 7 bridge and its focused tests. Keep every
   binding declarative and every representation value immutable.
4. Before reporting success, run this complete ordered attestation:
   `npm.cmd run check`; `npm.cmd run coverage`; `npm.cmd run deps:inventory`;
   `npm.cmd run license:check`; `npm.cmd run deps:audit`; and `git diff --check`.
   If an in-scope repair is needed, repeat the complete attestation. If a
   required command cannot pass or a required repair is out of scope, stop
   `Blocked` with evidence.
5. Verify both lock authorities are unchanged; inspect the exact changed-file
   list, ignored/generated state, text hygiene, sensitive-content scan, and
   absence of prescribed-port listeners or worker residue.
6. In one disposable copy outside both the repository and OneDrive, using an
   isolated cache, reproduce locked setup, the focused suite, and
   `npm.cmd run check`. Remove the exact temporary copy and cache, then verify
   they are absent. Do not record user-specific absolute paths in repository
   evidence.
7. Write the authorized report and stop. Do not stage, commit, push, alter a
   remote, independently validate, accept for Central, or begin P2-EP03.

## 10. Required Worker Report

`ViDAP_P2_EP02_Implementation_Report.md` must state the packet version,
governing versions, baseline/lock evidence, exact worker file scope, and any
pre-existing changes separated from worker output. It must map each D2.1–D2.8
boundary used here to the implemented contract, explain the semantic-digest
projection and its exclusions, and record static-binding, validation,
determinism, rejection, and immutability evidence. It must explain the separate
contract/validation snapshot projection, its policy identifier, derivation,
exclusions, reference hash, and its relationship to representation equality
and the workflow digest. It must distinguish the v0.1 evidence and digest
repair from the new v0.2 snapshot implementation and final proof.

It must include the complete final-attestation results, clean-copy/cleanup
evidence without user paths, hygiene and residue results, exclusions confirmed,
and an explicit independent-validation handoff. It must identify any failure as
`Blocked` or `Revise`, with requirement-linked evidence.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP02-AC01 | Governing inputs, P2-EP01 decisions including the D2.2 snapshot reference, baseline, locks, and worker scope are accurately recorded. |
| EP02-AC02 | Only the five Section 7 paths changed, with no prohibited or unrelated residue. |
| EP02-AC03 | Preparation accepts only Phase 1-valid documents plus explicit static bindings, records the relevant contract/validation snapshot reference, and has no dynamic discovery or executable selection. |
| EP02-AC04 | Bindings and representations contain no callable, import/path/command/URL, run/result/artifact/cache/environment/seed, or other prohibited field or behavior. |
| EP02-AC05 | The workflow digest follows the accepted RFC 8785 UTF-16 property order; it is deterministic, layout-free, member-order invariant, and changes for every specified workflow-semantic difference. The separate snapshot reference follows the exact Section 4 contract projection, changes for relevant contract/validation changes, and ignores display/order/unused-definition changes. |
| EP02-AC06 | Phase 1 validation diagnostics remain authoritative; binding failures are narrow preparation refusals, not runtime errors or fallbacks. |
| EP02-AC07 | Binding collection, metadata, snapshot reference, and representation values are immutable, static, and deterministic. |
| EP02-AC08 | Existing Phase 1 built-ins remain non-operational; only test-local declarative definitions can demonstrate success. |
| EP02-AC09 | No operation, schedule, dispatch, run, artifact, persistence, cache, runtime error, fixture, dependency, UI/API, process, network, data/ML, export, or later-phase behavior exists. |
| EP02-AC10 | The complete ordered local attestation and bounded clean-copy proof pass with unchanged locks and verified cleanup. |
| EP02-AC11 | The implementation report accurately distinguishes v0.1 evidence from v0.2 proof, explains both hashes and the snapshot contract, is sanitized and complete, and leaves validation and acceptance to their proper owners. |
| EP02-AC12 | A fresh independent validator returns `Accept` with no unresolved Critical or High finding. |
| EP02-AC13 | Central explicitly accepts this packet before P2-EP03 is drafted or authorized. |

## 12. Independent Validation Contract

The validator must read this packet, every governing input, and the worker
report; independently inspect the target and exact file scope; reproduce the
focused contract challenges and required attestations as permitted; recalculate
the semantic digest and contract snapshot reference from independent
projections, including the port-type-change and non-ASCII key challenges;
verify locks, hygiene, ignored state, clean-copy evidence, and all exclusions.
It must return `Accept`, `Revise`, or `Blocked`
with requirement-linked findings. It must not modify files, accept the bridge
for Central, alter remote state, or begin P2-EP03.

## 13. Fresh-Chat Prompts

### Worker

> Resume the approved `ViDAP_P2_EP02.md` v0.2 as the bounded implementation worker. Read every governing input and the existing worker report. Implement the clarified contract/validation snapshot reference within Section 7, preserve the repaired digest ordering, and rerun the complete required evidence. Update `ViDAP_P2_EP02_Implementation_Report.md` and stop with an independent-validation handoff; do not validate your own work, accept for Central, or begin P2-EP03.

### Independent validator

> Act as the independent validator for `ViDAP_P2_EP02.md`. Read the packet, its governing inputs, and `ViDAP_P2_EP02_Implementation_Report.md`. Follow the packet’s independent-validation instructions exactly. Verify every acceptance criterion, citations, calculations, architecture boundaries, and Git/file-scope compliance. Do not modify files, accept for Central, alter remote state, or begin P2-EP03. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

P2-EP02 is complete. Central may draft P2-EP03 under WS2.3; that packet
requires separate approval before any worker executes it.
