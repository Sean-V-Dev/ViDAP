# ViDAP P1-EP01 — Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P1_EP01.md` version 0.1 |
| Worker report | `ViDAP_P1_EP01_Decision_Report.md` |
| Independent-validation verdict | Accept |
| Central decision | D1.1–D1.7 accepted |
| Reconciliation date | 2026-09-20 |
| Owner | Central |

---

## 1. Purpose and authority

This record preserves the independently validated result of P1-EP01 and
records Central's explicit acceptance of its workflow and compatibility
decisions. The worker made recommendations only; the independent validator
returned `Accept`; Central made the decisions recorded here.

This reconciliation accepts architecture decisions, not an implementation.
It does not create a workflow model, schema artifact, source code, test,
fixture, dependency, lockfile change, UI, API, process, persistence, data/ML
behavior, execution engine, export, remote change, or Phase 2 work.

## 2. Independent-validation result

The independent validator confirmed:

- gate failures are marked and treated as ineligible;
- every weighted total remains correct;
- the required post-report quality check passed;
- `package-lock.json` and `python/uv.lock` remained unchanged;
- `git diff --check` passed; and
- the final scope contains no implementation or Phase 2+ work.

This satisfies P1-EP01 acceptance criterion EP01-AC18. The worker report's
earlier statement that fresh independent validation remained pending is a
historical worker-state statement; the later `Accept` verdict resolves that
pending condition.

## 3. Accepted decisions

### D1.1 — Canonical workflow encoding and document envelope

ViDAP workflows use an open UTF-8 JSON document. The canonical authority is
the workflow/schema contract and its later small kernel, not the browser,
generated code, or a validator artifact. A JSON Schema 2020-12 artifact may
later be a supplementary structural-validation aid, never a competing
semantic authority or an implied package selection.

Canonical serialization uses a documented stable indentation/newline policy,
unique object names, lexicographic object-key ordering when a serializer
controls output, and stable-ID sorting for semantically unordered arrays.
Readers judge meaning by fields and identities, not textual formatting or
member/array order. Extra core fields are invalid. A future named extension
container is governed by D1.6.

### D1.2 — Identity, references, and semantic/layout separation

Workflow, node, and edge identities are stable opaque lowercase UUIDv4 text.
Port identity is an immutable contract key unique within its node type; an
endpoint is the pair of node ID and port key. Edges have their own identity
and directed output-to-input endpoints.

Duplicate, dangling, missing, reversed, or duplicate-exact endpoints are
invalid. The initial graph is acyclic. Labels are mutable presentation, never
references. Optional layout/viewport data is isolated as non-semantic metadata
and cannot contain alternate semantics, ports, edges, types, parameters, or
execution hints. Execution ordering remains a Phase 2 decision.

### D1.3 — Practical types and connection compatibility

The initial nominal port-type vocabulary is `table`, `target`, `split`,
`model`, `predictions`, `metrics`, and `artifact`. These are workflow
artifact names, not Python classes or implemented data/ML behavior.

Each port declares one token. Connections require exact token equality.
Inputs declare `one` or `many` cardinality; requiredness is contract data.
Different-token conversion requires an explicitly registered adapter node,
never implicit casting or an `any` wire. Later expansion requires an
accepted decision and must not redefine existing tokens.

### D1.4 — Node parameter and contract model

The workflow/schema layer owns declarative node definitions: stable node-type
ID, display metadata, port contracts, parameter contracts, and optional
non-executing `operationKey` metadata. Parameter contracts define stable
key, value kind, requiredness, optional default, and applicable declarative
constraints.

Workflow nodes carry parameter overrides, not UI state. Unknown parameters,
wrong kinds, and constraint violations are invalid. Omitted optional
parameters resolve to contract-owned defaults; supplied values are not
silently replaced. `operationKey` is not a callable, import path, command,
URL, permission, or runtime/export mapping.

### D1.5 — Validation and actionable diagnostics

Validation returns an ordered collection of structured diagnostics; no
diagnostics means valid. Structural validation precedes semantic validation.
Unsupported capability is visibly identified as `unsupported`, rather than
treated as valid or confused with malformed input.

Each diagnostic has a stable code, severity, category, affected-element
reference, plain-English message, plain-English remedy, and optional
non-contract technical detail. JSON Pointer may be an optional location aid.
Raw exceptions are not the stable user-facing contract.

### D1.6 — Versioning, migration, and compatibility

The initial envelope requires root `format: "vidap.workflow"` and
`schemaVersion: "1.0"`. Only exactly version `1.0` is supported initially.
Missing, malformed, older, or future versions fail visibly as unsupported.
There is no migration until a real predecessor, an explicit transformation,
representative evidence, and a separately approved packet exist.

Unknown core fields are structural errors; unknown node types are unsupported;
unknown parameter keys/values are semantic errors. Nothing unknown is
silently ignored, defaulted, stripped, or reserialized as accepted meaning.
Future extensions are allowed only in an explicit, versioned extension
container. Unknown namespace or extension versions fail visibly.

### D1.7 — Node registration and extension boundary

The workflow/schema layer uses an explicit static registry of approved
first-party declarative node definitions. Duplicate node-type registration is
a deterministic error. A missing node type is unsupported; it is not
auto-installed, substituted, or treated as generic.

Registry discovery must not execute third-party code, import a document-named
path, run a discovery command, contact a registry, or interpret a manifest as
permission to execute code. Future extension requires separately approved
static registration and tests. A marketplace, dynamic plugin ABI, remote
catalog, and dynamic plugin loading remain deferred.

## 4. Accepted limitations and deferrals

The following are intentionally not selected or implemented:

- a committed JSON Schema artifact or validator package;
- a universal/structural type system, shape system, or generic `any` wire;
- node-family operations, runtime calls, execution ordering, run identity,
  caching, artifacts, or persistence;
- UI rendering, forms, an HTTP/API error envelope, or browser storage;
- import/export generation and mapping;
- a migration implementation, forward-compatible acceptance of unknown
  meaning, a marketplace, or dynamic plugin loading.

These are not gaps in the decision. They remain bounded work for their owning
future packet or phase.

## 5. Central acceptance

Central accepts D1.1 through D1.7 as independently validated. P1-EP01 is
`Complete`; EP01-AC19 is satisfied.

Central may now draft P1-EP02 — Workflow Model and Serialization as a
separate bounded implementation packet. That draft, and any later explicit
approval, must remain faithful to the decisions above. This acceptance does
not itself authorize P1-EP02 execution or any implementation.
