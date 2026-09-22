# ViDAP P2-EP01 — Decision Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P2_EP01.md` version 0.1 |
| Worker report | `ViDAP_P2_EP01_Decision_Report.md` |
| Independent-validation verdict | Accept |
| Central decision | D2.1–D2.8 accepted |
| Reconciliation date | 2026-09-21 |
| Owner | Central |

---

## 1. Purpose and authority

This record preserves the independently validated result of P2-EP01 and
records Central's explicit acceptance of the execution/run-foundation
decisions. The worker made recommendations only; independent validation
returned `Accept`; Central makes the decisions recorded here.

This reconciliation accepts architecture decisions, not an engine. It does not
create runtime source/tests, operations, fixtures, data, dependencies, locks,
subprocesses, artifact files, persistence, UI/API, remote changes, or P2-EP02
work.

## 2. Independent-validation result

The independent validator returned `Accept` after confirming:

- corrected weighted totals, D2.1's persistent-service rejection at G7,
  candidate rationales/confidence, and the Phase-1-aligned semantic digest;
- full fidelity to Phase 1, Phase 2, UX, dependency, and later-phase
  boundaries;
- full final attestation, unchanged lock hashes, clean whitespace, no staged
  files, and the decision report as the sole worker artifact; and
- no unresolved finding.

These findings satisfy P2-EP01 acceptance criteria EP01-AC01 through
EP01-AC15. The worker report's pending-validation wording is historical; the
subsequent independent `Accept` resolves that condition.

## 3. Accepted decisions

### D2.1 — Direct in-process bounded invocation seam

The initial engine is one explicit synchronous in-process entry seam. The
caller owns startup; the engine owns attempt-local resources and returns one
attempt record. It may refuse work before it begins but does not claim to
interrupt an already executing operation. A supervised child process remains a
future containment option; a persistent worker/service is rejected for this
foundation as disproportionate local state.

### D2.2 — Immutable layout-free execution representation and static dispatch

After successful Phase 1 validation, the engine converts canonical semantics
once into an immutable execution representation. It contains stable
node/operation identity, resolved parameters, dependency references, a
contract/validation snapshot reference, and a semantic-content digest. The
digest is SHA-256 of a deterministic semantic projection: non-semantic layout,
viewport, labels, display metadata, and semantically unordered collection
order cannot affect it.

Runtime dispatch uses a separately versioned static first-party operation map.
Unknown or unbound operations refuse execution; the map cannot change workflow
meaning, dynamically import code, or use generated source as an authority.

### D2.3 — Sorted Kahn planning, attempt-local sharing, and fail-stop flow

The engine derives a stable topological schedule with ready nodes ordered
lexicographically by canonical node ID. It executes sequentially. An
attempt-owned port-result table computes a shared upstream result once and
fans it to all consumers; joins await every required predecessor. Invalid
dependencies refuse rather than repair. The first operation failure ends
dispatch, preserves completed-but-not-success evidence, marks unstarted
dependents blocked, and records one structured envelope.

### D2.4 — Immutable minimum run-attempt record

Each attempt receives a UUIDv4 identity and records workflow identity plus
semantic digest, plan/binding revisions, resolved inputs/parameters, explicit
seed or its absence, bounded environment fingerprint, timing, outcome,
attempt-local reuse events, diagnostics, and owned artifact references.
Terminal records are immutable. This is a bounded reproducibility record, not
the Phase 6 history, restoration, or comparison product.

### D2.5 — Metadata-first, bounded owned local artifacts

Phase 2 uses one ignored project-local managed directory per run ID with fixed
owned record/output slots, same-root temporary writes, explicit publish/failure
state, and removal only by recorded owned paths. There is no database, general
artifact store, upload, caller-selected path, hidden age purge, or unowned
residue.

**Central constraint:** Phase 2 is metadata-first. It may retain the bounded
run record and explicitly selected small proof artifacts, but it does not
authorize default persistence of preview data, intermediate data, or
cross-run-cached output. Phase 4/5 planning must separately decide what real
data/model artifacts may persist, their retention, and their privacy rules.

### D2.6 — Visible attempt-local shared-result table only

The selected reuse mechanism is an attempt-local shared-result table, not a
cross-run cache. It disappears with the attempt and records each output as
computed or reused within that attempt. Its key includes operation/binding
revision, resolved parameters, ordered input content references, semantic
digest, explicit seed, and relevant environment fingerprint. A change to any
component requires fresh computation. No persistent cache artifact or
cross-run hit exists.

### D2.7 — Structured runtime-error envelope

Runtime failure returns a stable structured envelope containing category/code,
attempt ID, affected operation/port where known, outcome, plain-English
explanation/remedy, and sanitized technical type/message/traceback/cause
chain. It excludes credentials, raw environment values, and arbitrary object
representations. Phase 1 validation diagnostics remain a distinct
pre-dispatch refusal, not a runtime failure.

### D2.8 — Minimal actual deterministic scalar-proof boundary

A later approved packet may introduce a tiny family of actual deterministic,
side-effect-free scalar transforms, one controlled deterministic failure, and
one deterministic managed-output serialization. This is a family boundary,
not approval of a fixture, operation, callable, dependency, artifact format,
user data, preparation, training, evaluation, UI/API, or export behavior.
The later packet must provide explicit static bindings and controlled-fixture
provenance, license, size, and privacy evidence.

## 4. Accepted limitations and next boundary

The following remain deliberately deferred: a child-process implementation;
parallel execution; persistent cross-run caching; user datasets and preview
data retention; data preparation; models; experiment comparison/restoration;
UI/API interaction and semantic regions; export; AutoML; agents; plugins; and
distributed/cloud behavior.

Central accepts D2.1 through D2.8 as independently validated. P2-EP01 is
`Complete`; EP01-AC16 is satisfied. Central may now draft P2-EP02 — execution
representation and contract bridge. It must implement only D2.1–D2.2 and their
necessary tests, without selecting an operation, planner/dispatcher, artifact
write, cache, or Phase 3+ behavior. It requires separate approval before
execution.
