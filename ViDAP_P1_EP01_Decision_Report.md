# ViDAP P1-EP01 Decision Report — Workflow and Compatibility Decisions

| Field | Value |
|---|---|
| Packet | `ViDAP_P1_EP01.md` version 0.1 |
| Worker role | Bounded decision worker; recommendations only |
| Execution authority | Explicit user direction dated 2026-09-20 and packet status `Approved for execution` |
| Authorized repository output | This report only |
| Decision disposition | Recommend D1.1–D1.7 for fresh independent validation and Central reconciliation; **none is accepted by this worker** |
| Research retrieval date | 2026-09-20 |

## 1. Authority, governing inputs, and bounded baseline

The current user direction expressly approves this exact packet.  Under the
authority order in the spine, that direction and the approved packet govern
this bounded report; neither authorizes implementation or Central acceptance.

### Governing inputs read, in required order

1. Current explicit user direction (2026-09-20) approving `ViDAP_P1_EP01.md`
   version 0.1.
2. `ViDAP_Overview.txt` (product source; especially OV §§3, 5–7, 15–18,
   20–23, 25–30).
3. `ViDAP_Phased_Plan_Spine.md` version 1.2 (invariants, Phase 1 outcome,
   Phase 2 exclusion, and completion/independent-review rules).
4. `ViDAP_Roadmap.md` version 2.1 (P1 and checkpoint A1).
5. `ViDAP_Phase_1_Plan.md` version 1.0 (D1.1–D1.7 and §§4–10).
6. `ViDAP_P0_EP08_Validation_and_Reconciliation.md` (P0-EP08 accepted by
   Central; Phase 0 complete).
7. Accepted Phase 0 reconciliation records and decisions: P0-EP01 through
   P0-EP07 reconciliation records, `ViDAP_P0_EP01_Decision_Report.md`, and
   `ViDAP_P0_EP02_Decision_Report.md`.  They establish the local web/Python
   topology; `python/src/vidap_workflow` as the future semantic-owner area;
   Node 24/npm and uv-managed CPython 3.14; the two authoritative locks;
   the root quality task; dependency/license review before any new direct
   dependency; and controlled fixtures as consumers rather than authorities.
8. `ViDAP_P1_EP01.md` version 0.1.

### Baseline before this report

Read-only inspection found branch `main` at commit
`030e9406da205c535605994fb721001f2e4541a7`.  Before this report existed,
the tracked worktree already contained `M ViDAP_Roadmap.md`; the untracked
set already contained `ViDAP_P1_EP01.md` and `ViDAP_Phase_1_Plan.md`.  Those
planning inputs are pre-existing work, not worker output.  The authorized
output path did not exist, and no workflow/schema source, fixture,
decision-record, manifest, or lock conflict was found.

The initial SHA-256 lock evidence was:

| Lock authority | SHA-256 before report |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

This report makes no dependency choice, installation, schema, fixture,
source, test, configuration, process, UI, API, persistence, data/ML, export,
or Phase 2 change.

## 2. Evidence method and primary-source bibliography

Facts below are limited to the cited source behavior.  Recommendations and
scores are architectural inferences made against the governing inputs; they
are not claims that a library implements the proposal.  No candidate library,
standard implementation, prototype, package installation, or benchmark was
run.

| ID | Current primary evidence (retrieved 2026-09-20) | Fact used |
|---|---|---|
| E1 | [IETF RFC 8259 — JSON](https://www.rfc-editor.org/rfc/rfc8259.html) | JSON is a text-based, language-independent structured-data format; object names should be unique and object-member ordering must not be relied on for interoperability. |
| E2 | [JSON Schema 2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core) | A JSON Schema is itself a JSON document describing an instance; instances treat object properties as unordered, and the specification defines standard validation-output forms beyond a boolean flag. |
| E3 | [JSON Schema 2020-12 Validation](https://json-schema.org/draft/2020-12/json-schema-validation) | The vocabulary provides declarative `enum`, numeric bounds, string length/pattern, array cardinality, and uniqueness constraints. |
| E4 | [IETF RFC 9562 — UUIDs](https://www.rfc-editor.org/rfc/rfc9562.html) | UUIDs have a defined 128-bit format and a text `hex-and-dash` representation; version 4 is the standardized random UUID form. |
| E5 | [IETF RFC 6901 — JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html) | JSON Pointer is a defined string syntax for locating a value in a JSON document, including escaping rules. |
| E6 | [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/) | YAML is a distinct human-readable serialization language with its own processing model, so adopting it would materially change parser/serialization policy. |

No cited implementation aid is selected.  Any later JSON Schema validator,
UUID generator, graph helper, or registry framework remains subject to a
separate packet with exact package, maintenance, license, compatibility, and
lock-graph evidence under accepted D0.6.

## 3. Common gates and scoring method

Every candidate was evaluated against G1–G8 before scoring. `P` means the
candidate can meet the gate under its stated bounded policy; `F` means it
fails that gate. A failed candidate is **ineligible for selection regardless
of its weighted score**. Scores remain recorded to make the rejected
alternative comparison reproducible; they do not override gate eligibility.

| Gate | Applied meaning |
|---|---|
| G1 Open inspection | Readable, diffable, UI-independent construction. |
| G2 Deterministic meaning | Layout, creation order, and object-member order cannot determine semantics. |
| G3 Layer separation | No UI, runtime, experiment, or export dependency defines workflow meaning. |
| G4 Safe evolution | Explicit version/unknown handling; no silent loss. |
| G5 Practical validation | Stable affected-element diagnostic and remedy are possible. |
| G6 Declarative extension | Later types can be added without marketplace/dynamic code discovery. |
| G7 Proportion | Small Phase 1 kernel; no universal ontology or engine. |
| G8 License/maintenance posture | No library is assumed selected; a later dependency review remains mandatory. |

For each row, weighted points are `weight × score / 5`; total is out of 100.
Scores 1–5 are aids, not automatic decisions.  `H`, `M`, and `L` denote high,
medium, and low evidence confidence respectively.

| Criterion | Weight |
|---|---:|
| Overview/spine alignment | 20 |
| UI/runtime/export separation | 18 |
| Determinism/source-control usability | 15 |
| Validation/diagnostic clarity | 15 |
| Safe evolution/compatibility | 12 |
| Programmatic Python fit | 10 |
| Practical bounded Phase 1 | 10 |

## 4. D1.1 — Canonical workflow encoding and document envelope

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Plain JSON plus prose-only validation rules | P | P | P | P | P | P | P | P | 5, 5, 5, 3, 3, 5, 5 | 89.2 | H |
| B. JSON document with a supplementary formal JSON Schema validation aid | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 4 | 98.0 | H |
| C. YAML workflow document with documented rules | P | P | P | P | P | P | P | P | 4, 5, 3, 3, 4, 4, 3 | 75.6 | M |

The JSON facts supporting A and B are E1–E3.  E6 supports the factual claim
that YAML introduces a separate serialization/processing policy; its lower
score is an architectural inference about diff and ambiguity discipline, not
a claim that YAML cannot work.

### Recommendation — B, with semantic authority kept out of the schema aid

Adopt an open UTF-8 JSON workflow document.  Its canonical meaning is the
accepted document/contract rules and, later, the small workflow layer—not a
browser, generated code, or validator artifact.  A future JSON Schema 2020-12
artifact may be a **supplementary structural validator aid**, never a second
semantic authority and never a requirement to choose a validator package.

Canonical serialization must use UTF-8; unique JSON object names; a documented
stable indentation/newline policy; lexicographic ordering of object keys where
a serializer controls output; and arrays sorted by their stable ID when their
members are unordered semantically.  Array order therefore is not a semantic
execution order.  On input, a conforming reader must accept valid JSON member
ordering and judge semantics by fields/identities, not text formatting or
member order (E1–E2).

The following is **non-authoritative, non-executable illustrative prose**, not
a schema, fixture, source file, or committed document sample: a document would
carry a format discriminator, a `schemaVersion`, an opaque `workflowId`, a
node collection, an edge collection, and optional explicitly non-semantic
`layout` metadata.  It may later reserve a named `extensions` container; it
does not authorize arbitrary top-level fields.

Extra core fields are invalid rather than ignored.  The only future extension
route is the selected named, versioned extension container in D1.6; an unknown
extension is visibly unsupported, retained only by a caller that can preserve
raw input, and never silently discarded or interpreted.

**Rejected alternatives and limitation.** A would make later structural
diagnostics and testable shape rules needlessly bespoke.  C provides no
material product advantage and adds a second serialization model.  B does not
settle whether a schema aid is written or which validator is used; that is
intentionally deferred to an approved implementation packet.  Confidence is
high for the format choice, medium for the eventual schema-artifact scope
because real node-family shape is deliberately not yet defined.

## 5. D1.2 — Identity, graph references, and semantic/layout separation

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Opaque stable UUID identities and explicit endpoint references | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. Human-derived node names/labels as references | P | P | P | P | P | P | P | P | 3, 4, 4, 3, 3, 4, 4 | 70.6 | H |
| C. Array index or creation-order references | P | F | P | P | P | P | P | P | 2, 2, 2, 3, 2, 4, 4 | 51.0 | H |

E1 establishes why object-member ordering cannot safely carry meaning; E4
establishes a standardized opaque identifier form. Candidate C is ineligible:
its index/creation-order references make order semantic and therefore fail G2.
Scores are the inference that stable opaque identifiers best protect rename,
reorder, and layout changes from altering graph references.

### Recommendation — A

Require stable, opaque lowercase UUIDv4 textual IDs for workflow, node, and
edge identities; each ID is unique within its declared scope.  UUID generation
method is not a Phase 1 dependency selection.  A port has a stable contract
key (for example, a short immutable `portId`) unique inside its node type;
its document reference is the pair `(nodeId, portId)`, so it needs no separate
per-document UUID.

An edge requires its own UUID identity and exactly one directed source endpoint
(`output` port) and target endpoint (`input` port).  Duplicate workflow/node/
edge IDs, a duplicate contract port key, a missing endpoint, a dangling node
reference, a missing port, an input-to-output reversal, or a duplicate exact
source-target edge are invalid.  A future implementation may report all
independent violations, but must not repair them silently.  The initial graph
is acyclic: a directed cycle is semantic invalidity.  This reserves no
execution ordering algorithm; dependency order is expressly Phase 2-owned.

Node labels and display names are mutable presentation fields and never
references.  Optional `layout`/viewport data is isolated under a dedicated
non-semantic top-level member, may reference IDs only, and is excluded from
semantic validation and future execution planning.  Removing, adding,
reordering, or changing it; changing JSON member order; and changing node
creation order cannot change graph meaning.  Layout may not embed alternate
ports, parameters, edges, type assertions, or execution hints.

The following is **non-authoritative and non-executable**: an edge can be
described in prose as “edge ID `e…` joins node `n…` output port `out` to node
`n…` input port `in`.”  It is not a fixture, schema, or executable sample.

**Rejected alternatives and limitation.** Labels are valuable UI annotations
but fail rename stability; indexes/creation order cause unrelated editing to
retarget edges.  The cycle decision is a validation boundary, not a scheduling
or runtime decision.  Confidence is high; nested subgraph identity is a later
node-family/Phase 10 concern and is not designed here.

## 6. D1.3 — Practical types and connection compatibility

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Small nominal port-type vocabulary with exact compatibility and explicit adapters | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. Structural/type-expression matching from the outset | P | P | P | P | P | P | P | P | 4, 5, 3, 4, 5, 4, 2 | 79.0 | M |
| C. Permissive `any`/untyped wires with warnings | P | P | P | P | P | P | P | P | 2, 4, 3, 2, 4, 5, 5 | 67.0 | H |

This comparison is principally architectural inference from OV §7 and the
Phase 1 guardrail against a premature universal ontology.  E2–E3 support the
general feasibility of declaratively constrained values, but do not prescribe
a ViDAP type lattice.

### Recommendation — A

Start with these nominal type tokens only: `table`, `target`, `split`,
`model`, `predictions`, `metrics`, and `artifact`.  They name workflow
artifacts, not Python classes, data structures, ML behavior, or an implied
implementation.  Each port declares exactly one token.  A connection is
compatible only when the source and target tokens are exactly equal.

Inputs declare cardinality `one` or `many`; `one` permits at most one incoming
edge, while `many` permits zero or more.  Outputs may fan out.  Requiredness
is contract data: a required input must have a compatible connection by
semantic validation; optional inputs may have none.  A connection that
violates direction, type, or cardinality is invalid, not a warning-only
success.  Converting between different tokens requires a separately registered
adapter node with its own explicit input/output contract—never a UI cast,
implicit coercion, or generic `any` wire.

Later approved families can add namespaced nominal tokens or accepted,
documented assignability rules.  They must not redefine the meaning of an
existing token or claim that all future values are interchangeable.  There is
no shape, column, model, metric, or runtime type system in this packet.

**Rejected alternatives and limitation.** Structural expressions could later
be useful but require unapproved syntax, variance, and diagnostic rules now.
Permissive wires hide precisely the invalid connections OV §7 requires the
product to flag.  Confidence is high for a nominal kernel and medium for the
seven-token starting set, which must be revisited only by an accepted decision
if an actual future node family proves it insufficient.

## 7. D1.4 — Node parameters and declarative contracts

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Canonical declarative node contract owned by workflow/schema | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. UI-owned form validation/parameter contract | P | P | F | P | P | P | P | P | 2, 1, 3, 3, 3, 4, 4 | 52.8 | H |
| C. Runtime-owned executable contract | P | P | F | P | P | P | P | P | 3, 1, 3, 4, 3, 3, 3 | 55.8 | H |

The selected ownership follows OV §§6, 16, 18–19 and the accepted P0 topology:
the browser, executor, and exporter are consumers. Candidates B and C are
ineligible because UI- or runtime-owned contracts fail G3 layer separation.
E2–E3 demonstrate common declarative constraint primitives, not an
implementation prescription.

### Recommendation — A

A registry-owned node definition is declarative metadata containing a stable
node type ID, display metadata, input/output port contracts, and parameter
contracts.  Each parameter has a stable contract key; declared value kind;
required flag; optional default; and only applicable declarative constraints:
enum membership, numeric inclusive/exclusive range, string length/pattern,
array length/uniqueness, object shape, and nullability.  Constraints apply to
the resolved effective value.  A required parameter without a supplied value
and without a declared default is invalid.  An optional omitted parameter uses
its contract default; a supplied value is never silently replaced.

Workflow node `params` contains key/value overrides, not UI state.  Unknown
parameter keys, duplicate parameter keys, values of the wrong declared kind,
and constraint violations are invalid.  Unknown values are not retained as
harmless decoration.  Defaults are contract-owned, so a UI may render them and
a later runtime/exporter may consume resolved values, but neither can redefine
them.

The minimum non-executing future handoff is the node type ID plus an optional
opaque `operationKey` in the definition.  `operationKey` names a later
approved mapping only; it is not an import path, command, URL, callable,
arbitrary code slot, permission, or runtime/export selection.  No actual
operation keys are created by this report.

The following is **non-authoritative and non-executable**: a parameter might
be described as “`threshold`: numeric, optional, default 0.5, inclusive
range 0 through 1.”  It is neither a node definition nor a schema/fixture.

**Rejected alternatives and limitation.** UI-owned rules would make the UI a
semantic authority, and executable runtime contracts conflate validation with
unapproved behavior and force non-runtime consumers to duplicate rules.
Contract-to-form presentation, runtime dispatch, and export mapping remain
future consumer work.  Confidence is high for ownership and unknown handling;
medium for advanced constraints until real node families exist.

## 8. D1.5 — Validation and actionable diagnostics

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Staged structured diagnostics | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. Boolean result or exception-only validation | P | P | P | P | F | P | P | P | 2, 3, 4, 1, 2, 5, 4 | 56.6 | H |
| C. UI-local error strings plus runtime exceptions | P | P | F | P | F | P | P | P | 2, 1, 3, 2, 2, 4, 4 | 47.4 | H |

The need for plain-English remedy plus preserved technical detail is directly
required by OV §19 and P1-AC05. Candidate B is ineligible because a
boolean/exception-only result fails G5. Candidate C is ineligible because
UI-local strings and runtime exceptions fail G3 and G5. E2 confirms that a
flag-only output conveys less than standardized detailed output; E5 provides a
standard optional location syntax for JSON values. The ViDAP envelope remains
an architectural recommendation, not a JSON Schema output claim.

### Recommendation — A

Validation returns an ordered collection of structured diagnostics; an empty
collection means valid.  It runs in two visible stages:

1. **Structural:** JSON/envelope shape, required fields, identity uniqueness,
   reference existence/direction, duplicate edges, and core/extension-field
   policy.
2. **Semantic:** known registry definition, port/parameter contract,
   type/cardinality/required-input rules, acyclicity, and supported-version
   policy.

Unsupported future capability is neither silently valid nor mislabeled as a
generic malformed document: it receives category `unsupported` with severity
`error`.  Raw parser/runtime exceptions are captured only as technical detail
when safe and never become the stable user contract.

Every diagnostic must have: stable `code` (for example, a namespaced immutable
identifier), `severity` (`error` or `warning`; warnings cannot make an invalid
document valid), category (`structural`, `semantic`, or `unsupported`), an
affected element reference (`workflow`, `node`, `edge`, `port`, `parameter`,
or document field), a plain-English `message`, a plain-English actionable
`remedy`, and optional non-contract `technicalDetail`.  It may include an E5
JSON Pointer `location` when a precise input position exists.  Codes and
categories—not English text or source exception class—are machine-stable.

The following is **non-authoritative and non-executable**: a result could say
“code `VIDAP-SEM-PORT-TYPE-MISMATCH`; affected edge `e…`; message: source and
target types differ; remedy: connect matching ports or add an approved adapter.”
It does not define executable behavior or a committed diagnostic fixture.

**Rejected alternatives and limitation.** Boolean/exception-only outcomes
cannot reliably identify an element and remedy. UI-local strings duplicate
meaning and leave non-UI authors unsupported.  Diagnostic localization and
ordering must later be tested; no UI presentation, HTTP error envelope, or
runtime error model is selected here.  Confidence is high.

## 9. D1.6 — Schema versioning, migration, and compatibility

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Initial strict single-version read with a defined future migration extension point | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. Invent a migration/legacy format at version 1.0 | P | P | P | P | P | P | P | P | 2, 4, 3, 3, 2, 4, 2 | 57.2 | H |
| C. Forward-compatible acceptance of arbitrary unknown fields/nodes | P | P | P | F | P | P | P | P | 3, 3, 3, 2, 5, 5, 4 | 67.8 | H |

E1–E3 establish that JSON/schema do not automatically settle application
compatibility or unknown-field policy. Candidate C is ineligible because
arbitrary unknown-field/node acceptance fails G4 safe evolution. The selected
strict policy is the architectural inference required by packet constraint 8
and the Phase 1 guardrail against silent compatibility.

### Recommendation — A

Use required root fields `format: "vidap.workflow"` and `schemaVersion:
"1.0"`; these literal values are the initial accepted-version discriminator.
The version belongs at the document root, not in UI metadata, a node, a file
extension, or a transport header.  At initial release, only exactly `1.0` is
supported.  Missing, malformed, older, or future versions fail safely with an
`unsupported` diagnostic.  No migration is implemented or implied because no
real predecessor exists.

The compatibility promise is intentionally narrow: a reader implementing
`1.0` preserves and validates all `1.0` core meaning, and rejects meaning it
cannot prove it understands.  A later version may introduce a migration only
with a real predecessor, explicit source/target versions, deterministic
transformation specification, idempotence/round-trip expectations where
applicable, representative evidence, and Central-approved packet scope.

Core unknown fields at root, node, edge, endpoint, port, contract, and
parameter levels are structural invalidity; unknown node types are
`unsupported` semantic invalidity; unknown parameter values/keys are semantic
invalidity; and an unknown version is `unsupported`.  None is ignored,
defaulted, stripped, or reserialized as if accepted.  A future version can
define only an explicit `extensions` container whose entries carry a stable
namespace and extension version.  A `1.0` reader rejects an unknown namespace
or extension version visibly; it need not preserve it when materializing a
validated model.  This is fail-safe, not a false claim of forward compatibility.

The literals above are **non-authoritative and non-executable illustrative
values**, not a schema, source, fixture, or persisted workflow.

**Rejected alternatives and limitation.** B fabricates history and untestable
compatibility. C can silently lose or misinterpret semantic information.
Strictness may initially reject future files more often, but it protects users
until an extension/migration contract is proved.  Confidence is high for the
initial policy; later compatibility breadth is deliberately unresolved.

## 10. D1.7 — Node registration and extension boundary

### Candidates, gates, and weighted comparison

| Candidate | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Weighted scores in criterion order | Total | Confidence |
|---|---|---|---|---|---|---|---|---|---|---:|---|
| A. Static, explicit in-process registration of approved declarative definitions | P | P | P | P | P | P | P | P | 5, 5, 5, 5, 5, 5, 5 | 100.0 | H |
| B. Manifest/directory discovery at startup | P | P | P | P | P | P | P | P | 4, 4, 4, 4, 4, 4, 3 | 78.0 | M |
| C. Dynamic third-party plugin loading to discover node definitions | P | P | P | P | P | F | P | P | 2, 2, 2, 3, 4, 3, 2 | 49.8 | H |

This is an architecture comparison. Candidate C is ineligible because dynamic
third-party discovery executes code and therefore fails G6 declarative
extension. The governing plan requires declarative extension without a plugin
marketplace or dynamic untrusted execution; no external plugin framework is
researched, chosen, installed, or licensed here.

### Recommendation — A

The workflow/schema layer owns an explicit registry assembled from an
allowlisted set of first-party, declarative node definitions.  A definition is
data: stable node type ID, immutable contract version/metadata, ports,
parameters, and optional non-executable `operationKey` from D1.4.  It is not
loaded by executing third-party code, importing a path named by a document,
running a discovery command, contacting a registry, or interpreting a
manifest as permission to execute code.

A registration attempt with an already registered node type ID is a
deterministic error.  A workflow referring to an absent node type is rejected
as `unsupported`; it is never auto-installed, substituted, or treated as a
generic node.  The initial built-in boundary is an explicit list created only
by an approved implementation packet.  Future extension is a separately
approved, static registration contribution that adds declarative definitions
and its tests without changing core document meaning.  A manifest/discovery
route, signed marketplace, sandbox, remote catalog, and dynamic plugin ABI are
all deferred and expressly not selected.

**Rejected alternatives and limitation.** Startup discovery makes provenance,
conflicts, and package boundaries harder to make deterministic before an
actual extension ecosystem exists. Dynamic loading violates the packet’s
no-untrusted-code-discovery rule and broadens security/license review. Static
registration is intentionally less convenient for hypothetical third parties
but proportionate and auditable for Phase 1.  Confidence is high.

## 11. Selected cross-decision contract map

| Concern | Selected owner and contract | Explicit non-owner / deferment |
|---|---|---|
| Document meaning, IDs, nodes, ports, edges | Workflow/schema layer; D1.1–D1.3 JSON semantic document | Browser state, creation/member order, runtime planner, exporter |
| Layout and viewport | Optional isolated non-semantic metadata | Semantic validation and future execution plan |
| Node contracts and parameters | Static registry declarative definitions; D1.4/D1.7 | UI forms, runtime call signatures, arbitrary code |
| Validation and diagnostics | Workflow/schema structural then semantic validation; D1.5 | UI-only messages, HTTP/API envelope, raw exceptions |
| Serialization | Workflow/schema JSON document and stable serialization policy; D1.1 | Browser serialization or generated code |
| Versioning and unknowns | Root version and strict visible policy; D1.6 | Silent coercion, discard, guessed migration |
| Extension | Explicit static approved registry additions; D1.7 | Marketplace, scan/discovery, dynamic plugin execution |
| Execution ordering, run/artifact identity, caching | **Phase 2** | D1.2 does not create an ordering algorithm |
| UI editing/presentation | **Phase 3** consumer of contracts | Canonical validation/meaning |
| Data, profiling, transformations | **Phase 4** | Type token alone does not implement behavior |
| Models/metrics/results | **Phase 5** | Contract token alone does not select a library |
| Experiments | **Phase 6** | Workflow ID is not a run/experiment ID |
| Export | **Phase 7** | `operationKey` is not an export mapping |
| Automation and agent behavior | **Phase 8/post-core decision** | Registry is not a plugin marketplace |
| Nested neural networks | **Phase 10** | No subgraph execution/model semantics in this report |

## 12. Consolidated policies precise enough for later tests

1. A valid initial document has the required core envelope and exact root
   `format`/`schemaVersion` discriminator.  A reader does not derive version
   from filename, UI state, member ordering, or a node.
2. Core JSON objects use unique names.  Semantic collections are identified by
   stable IDs; order in JSON text/arrays and creation order never determine
   semantic or future execution order.
3. Every edge has a unique ID and resolves from a known output port to a known
   input port.  Duplicate/dangling/reversed endpoints, duplicate exact edges,
   incompatible type/cardinality, unmet required input, and directed cycle are
   errors.
4. A node/port/parameter must be known to its static contract.  Unknown node
   type is `unsupported`; unknown core field/parameter is invalid; no unknown
   entity is silently discarded, preserved as accepted semantics, installed,
   or defaulted.
5. Initial type compatibility is exact nominal token equality.  A different
   token requires an approved adapter node contract.
6. Parameter defaults are contract-owned; omitted optional values resolve to
   their declared defaults, while unknown, missing-required, wrong-kind, and
   constraint-violating values are errors.
7. Each error diagnostic has a stable code, severity, category, affected
   element, plain-English message/remedy, and optional technical detail.  An
   optional JSON Pointer is a location aid, not the element’s durable identity.
8. Initial supported version is exactly `1.0`.  Unknown/missing/older/future
   versions visibly fail.  Migration support starts empty and cannot be
   claimed until a real predecessor and an approved migration packet exist.
9. Extensions are allowed only in the expressly versioned extension container
   and only when their namespace/version is known.  Unknown extensions fail
   visibly; they never silently change or disappear from accepted semantics.
10. Registry discovery never executes third-party code.  Built-ins and later
    extensions are explicit, static approved registration inputs.

## 13. Findings, limitations, and feasibility spike disposition

| Finding | Disposition | Owner |
|---|---|---|
| No actual node family exists, so the vocabulary is deliberately nominal and small. | Non-blocking; revisit only through a later accepted decision when a real family demonstrates insufficiency. | Central / owning future phase |
| No predecessor document exists. | Non-blocking; migration registry remains empty, with strict fail-safe version behavior. | P1-EP05 proposal, after approval |
| A JSON Schema artifact and validator are useful aids but no package/artifact is selected. | Non-blocking; direct-dependency evidence and a separate implementation packet are required before adoption. | Central / P1-EP02 proposal |
| Static registration intentionally does not solve third-party extension distribution. | Non-blocking; marketplace/plugin design is deferred, not implied. | Post-core scope proposal |

**Feasibility spike:** none proposed.  Primary standards evidence and governing
constraints are sufficient for these bounded recommendations.  A prototype is
not necessary to decide ownership, fail-safe compatibility, or static
extension boundaries; creating one would exceed this packet.

## 14. Worker self-assessment and final attestation

This is a report-completeness and scope self-check, **not independent
validation** and not Central acceptance. A fresh validator returned `Revise`
for the now-corrected G1–G8 eligibility cells; fresh independent revalidation
remains required before Central consideration.

| Criterion | Worker assessment | Evidence/location |
|---|---|---|
| EP01-AC01 | Pass | §§1 and 14 record authority, inputs, baseline, pre-existing work. |
| EP01-AC02 | Pass | §§4–10 recommend D1.1–D1.7 with alternatives, confidence, and consequences. |
| EP01-AC03–AC04 | Revised; pending fresh independent revalidation | §3 and every decision table now distinguish failed gates/ineligible candidates from scored comparisons. |
| EP01-AC05 | Pass | §2 separates primary-source facts from inference and gives retrieval date. |
| EP01-AC06–AC11 | Pass, pending independent review | §§4–10 specify open JSON, semantic/layout separation, small types/contracts, diagnostics, safe versions, and static registry. |
| EP01-AC12–AC14 | Pass | §§11–13 preserve layer ownership, deferrals, and no dependency selection. |
| EP01-AC15–AC16 | Pass subject to final scope check | Only this report was created/modified by this worker. |
| EP01-AC17 | Pass, pending independent recheck | Required post-report check passed after the required normal-Windows retry and passed again after this gate-eligibility revision; locks, whitespace, and scope are recorded below. |
| EP01-AC18–AC19 | Pending fresh independent validator and Central | This worker cannot self-validate or accept decisions. |

### Final command and scope evidence

Post-report evidence is recorded here only after the required commands run:

| Required evidence | Result |
|---|---|
| `npm.cmd run check` | **Pass** on 2026-09-20 via the normal Windows path, including the required rerun after the gate-eligibility revision. The restricted-sandbox attempt reached JavaScript formatting then stopped at `uv` with `Access is denied`; normal-Windows retries completed all inherited checks successfully. |
| `package-lock.json` and `python/uv.lock` hashes | **Pass** after the gate revision: respectively `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` and `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355`, unchanged from §1. |
| `git diff --check` | **Pass** (exit 0; no output) before the gate revision and after its report-only edit. It is rerun once more after this final attestation update. |
| Final status and exact changed/untracked paths | After the gate-revision scope check: tracked `M ViDAP_Roadmap.md` only; untracked `ViDAP_P1_EP01.md`, this report, and `ViDAP_Phase_1_Plan.md`. The roadmap, packet, and phase plan pre-existed; this report is the sole worker output. |

### Independent-validation handoff

A fresh independent validator must read every governing input and this report,
recheck high-impact primary evidence, recalculate all totals, challenge a
credible rejected alternative for each D1 decision, verify the corrected gate
eligibility and required final attestation, and return exactly `Accept`,
`Revise`, or `Blocked`. No D1 recommendation is accepted until Central
separately reconciles it.
