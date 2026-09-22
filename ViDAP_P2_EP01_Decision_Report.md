# ViDAP P2-EP01 — Execution and Run Foundation Decision Report

| Field | Value |
|---|---|
| Packet | ViDAP_P2_EP01.md version 0.1 |
| Authority | Explicit user direction, 2026-09-21; approved packet |
| Worker disposition | Recommendations only; independent validation and Central acceptance remain required |
| Retrieval date | 2026-09-21 |

## 1. Authority, inputs, and sanitized baseline

Read in order: the explicit approval; ViDAP_Overview.txt; Spine 1.3; Roadmap 3.9; Phase 2 Plan 1.2; P1-EP06 reconciliation; every accepted P1 reconciliation and accepted D1.1–D1.7; UX refinement.txt; accepted Phase 0 topology, Node/npm, uv/CPython, quality, dependency/license, and fixture controls; then this packet. The UX document is a Phase 3+ consultative presentation reference only; its completed-phase assertion has no authority.

Before this report, branch was main at 28c4e0076556. Pre-existing work: ViDAP_Phase_2_Plan.md, ViDAP_Roadmap.md, and the approved untracked packet. The authorized output did not exist and no conflicting report/runtime/policy/fixture path was found. An origin exists; its identity is deliberately omitted.

| Lock | SHA-256 before report |
|---|---|
| package-lock.json | FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA |
| python/uv.lock | AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355 |

Node 24.21.0, npm 11.19.0, and uv 0.12.16 are callable. uv needed the normal Windows retry after restricted-sandbox denial; this is the known environment limitation, not a project failure.

## 2. Current primary evidence

No package, implementation, fixture, operation, process, artifact, download, installation, benchmark, or prototype was selected or performed. Facts below are source-bound; decisions are architectural inferences.

| ID | Primary source, retrieved 2026-09-21 | Fact used |
|---|---|---|
| E1 | [Python 3.14 graphlib](https://docs.python.org/3.14/library/graphlib.html) | Topological order puts predecessors first; ready-node order can vary by insertion order; cycles fail. |
| E2 | [Python 3.14 subprocess](https://docs.python.org/3/library/subprocess.html) | Child processes create startup, return-code, timeout, and exception lifecycle. |
| E3 | [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html) | UUIDs are 128-bit identifiers; version 4 is random/pseudorandom. |
| E4 | [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) | Reliable hashing requires invariant representation; canonical JSON sorts properties but preserves array order. |
| E5 | [NIST FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf) | SHA-256 is a specified integrity digest. |
| E6 | [Python 3.14 os](https://docs.python.org/3.14/library/os.html) | Filesystem operations fail explicitly; environment is process state, not stable implicit input. |
| E7 | [Python 3.14 tempfile](https://docs.python.org/3.14/library/tempfile.html) | Managed temporary file/directory facilities are available. |
| E8 | [Python 3.14 traceback](https://docs.python.org/3.14/library/traceback.html) | Technical failure context can be retained. |

## 3. Gates and scoring

P means the stated candidate can satisfy the gate under its bounded policy; F makes it ineligible regardless of points.

| Gate | Applied test |
|---|---|
| G1 | Only validated Phase 1 canonical workflow determines semantics. |
| G2 | Plan/result ignores layout, insertion, and JSON-member order. |
| G3 | Binding is static and inspectable; no dynamic/untrusted code. |
| G4 | Run, artifact, reuse, and cleanup ownership is auditable. |
| G5 | Invalid/failing work stops with actionable structured information. |
| G6 | Reuse is absent or has semantic key, invalidation, and visibility. |
| G7 | Local Windows design is proportionate; no premature service/database. |
| G8 | No UI, data, ML, comparison, export, or later-phase behavior. |
| G9 | No dependency is silently selected. |

All matrices use scores in this order: alignment 20; determinism 18; provenance 17; failure/cache 15; simplicity 12; test/environment 10; scope/dependency 8. Points equal weight times score divided by five. Each candidate's rationale states why its scores differ; H/M are evidence-and-inference confidence. Totals below were recalculated as a separate arithmetic pass.

### Semantic-content digest rule

The workflow semantic-content digest is SHA-256 (E5) of a deterministic
semantic projection, not a raw document hash and not RFC 8785 alone. The
projection includes only the accepted Phase 1 semantic envelope, node IDs/type
IDs/resolved parameters, and edge IDs/endpoints; it excludes layout, viewport,
labels/display metadata, and all other non-semantic data. Object keys are
recursively ordered using the RFC 8785 property-order rule (E4). Collections
that Phase 1 defines as semantically unordered are sorted by their stable IDs
before serialization; collections whose order is semantically meaningful are
preserved in their accepted order. The projection rejects duplicate IDs/keys,
unknown content, and a missing stable ID rather than choosing an order. Thus
member order, layout, insertion order, and semantically unordered array order
cannot alter the digest, while a real ordered semantic collection can. The
later implementation packet must prove these equivalence and difference cases.

## 4. Recommendations

### D2.1 — Direct in-process bounded invocation seam (M)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Direct in-process module, synchronous invocation | P,P,P,P,P,P,P,P,P | 5,5,4,4,5,5,5 | 93.6 |
| B. Supervised local child process | P,P,P,P,P,P,P,P,P | 4,4,5,5,3,3,4 | 82.0 |
| C. Persistent local worker/service | P,P,P,P,P,P,F,P,P | 3,4,4,4,1,2,2 | 61.6 |

Score rationale/confidence: A earns its high simplicity/test scores because it
uses the accepted local CPython topology while honestly limiting containment
(M). B earns containment/failure points but loses local simplicity and test
fit because E2's lifecycle must be designed and tested (M). C has no
proportionate Phase 2 need for durable worker state and therefore fails G7,
not G8; its scores are retained for comparison only (H).

Recommend A. A future caller invokes one explicit engine entry point and receives one attempt record. Caller owns startup; engine owns attempt-local resources. Cancellation only refuses work not yet started; no claim is made to interrupt an executing in-process operation. Future UI uses the seam but never defines execution meaning. B is a credible later containment option, but E2 shows it adds lifecycle policy before reference proof needs it. C fails G7. Later packets must prove per-attempt cleanup and preserve a replaceable seam.

### D2.2 — Immutable layout-free IR and static dispatch (H)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Immutable IR plus static operation map | P,P,P,P,P,P,P,P,P | 5,5,5,5,4,5,5 | 97.6 |
| B. Direct document interpretation at dispatch | P,P,P,P,P,P,P,P,P | 4,3,3,3,5,4,5 | 74.0 |
| C. Generated-source execution | P,P,F,P,P,P,P,P,P | 2,2,2,2,2,2,2 | 40.0 |

Score rationale/confidence: A maximizes inspectability and semantic fidelity;
its modest simplicity deduction is the explicit conversion boundary (H). B is
simpler but lowers provenance/failure scores by mixing document reading with
dispatch (M). C fails G3 because generated source is an execution authority,
not a static binding (H).

Recommend A. Valid workflow converts once to an immutable plan containing stable node/operation identity, resolved Phase 1 parameters, dependency references, contract/validation snapshot reference, and the Section 3 semantic-content digest. A separately versioned static first-party map binds accepted operation keys; unknown or unbound keys refuse execution. It cannot alter contract meaning or import document-named code. Generated source fails G3.

### D2.3 — Sorted Kahn planning, sequential exactly-once reuse, fail-stop (H)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Stable Kahn schedule, ready set sorted by canonical node ID | P,P,P,P,P,P,P,P,P | 5,5,5,5,4,5,5 | 97.6 |
| B. Document/insertion-order traversal | P,F,P,P,P,P,P,P,P | 2,1,2,2,5,3,5 | 50.4 |
| C. Dependency plan with unspecified ready order | P,F,P,P,P,P,P,P,P | 4,2,4,4,4,4,4 | 72.8 |

Score rationale/confidence: A receives full determinism/provenance credit because
the explicit ID sort closes the E1 insertion-order gap (H). B fails G2 by
making document/insertion order meaningful (H). C also fails G2: a declarative
plan without a tie rule has an unspecified semantic outcome (H).

Recommend A. Input has already passed Phase 1; impossible dependencies refuse rather than repair. Ready nodes are selected lexicographically by stable canonical node ID; E1 specifically prevents reliance on an insertion-sensitive helper. One sequential attempt computes each node once; an attempt-owned port-result table fans it to all consumers. A join awaits every required predecessor. First operation failure ends dispatch, retains completed-not-success evidence, marks unstarted dependents blocked, and records one envelope; no parallel work exists to cancel.

### D2.4 — Immutable minimum run-attempt record (H)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Ephemeral result only | P,P,P,F,P,P,P,P,P | 2,3,1,2,5,3,5 | 54.2 |
| B. Immutable minimal run-attempt record | P,P,P,P,P,P,P,P,P | 5,5,5,5,4,5,5 | 97.6 |
| C. Experiment-history product | P,P,P,P,P,P,F,F,P | 4,4,5,4,1,2,1 | 67.4 |

Score rationale/confidence: A fails G4 because results lack a durable owned
provenance identity (H). B has complete bounded provenance with only a small
local-complexity cost (H). C has strong provenance but fails G7/G8 by building
a Phase 6 product prematurely (H).

Recommend B. Generate UUIDv4 attempt ID (E3); record workflow ID plus the Section 3 semantic-content digest, plan/binding revisions, resolved inputs/parameters, explicit seed or not-supplied, bounded environment fingerprint (runtime/OS/package-lock identifiers, never raw environment values), UTC timing, outcome, reuse events, diagnostics, and owned artifact references. Terminal records are immutable. This records reproduction conditions, not Phase 6 restoration/comparison UX.

### D2.5 — Bounded owned local run directory; no database (M)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. No durable artifact storage | P,P,P,P,P,P,P,P,P | 3,4,2,4,5,5,5 | 75.2 |
| B. Per-run owned local files, fixed names/formats | P,P,P,P,P,P,P,P,P | 5,5,5,5,4,4,5 | 95.6 |
| C. Database/general artifact store | P,P,P,P,P,P,F,F,P | 4,4,5,4,1,2,1 | 67.4 |

Score rationale/confidence: A is simple but lowers provenance/ownership
evidence because no durable artifact can be inspected (M). B is the smallest
choice meeting artifact ownership/partial-failure needs, with bounded local
file-management cost (M). C has provenance value but fails G7/G8 due to a
premature database/general store (H).

Recommend B: one ignored project-local managed root with directory named only by run ID; fixed record/output slots, never caller paths or arbitrary files. Write same-root temporary content, validate/close, then publish named results. Publish failure is failure, never success. Record lists owned paths and partial state. Later explicit removal by run ID deletes only listed owned paths; no hidden age purge, database, upload, or unowned residue. E6/E7 support explicit filesystem failure and managed temporary handling. Exact root, limits, schema, and removal interface stay for a later packet.

### D2.6 — Visible within-attempt memoization only (H)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. No reuse | P,P,P,P,P,P,P,P,P | 4,5,4,5,5,5,5 | 92.6 |
| B. Within-attempt memoization only | P,P,P,P,P,P,P,P,P | 5,5,5,5,5,5,5 | 100.0 |
| C. Persisted cross-run cache | P,P,P,P,P,F,F,F,P | 4,4,5,2,1,2,1 | 61.4 |

Score rationale/confidence: A is maximally safe/simple but loses branch
provenance/efficiency visibility (H). B retains that safety because scope ends
with the attempt and adds transparent shared-upstream reuse (H). C fails G6,
G7, and G8: persistent reuse needs unapproved invalidation/persistence policy
and exceeds the minimal foundation (H).

Recommend B. The D2.3 attempt-owned result table is the only reuse scope, disappears with the attempt, and records computed or reused-within-attempt per output. Key: operation/binding revision, resolved parameters, ordered input content references, the Section 3 semantic-content digest, explicit seed, relevant environment fingerprint. Any changed field computes again. Tests must vary each component and prove no reuse across attempts. No persistent cache artifact or cross-run hit exists.

### D2.7 — Structured runtime-error envelope, separate from validation (H)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Raw exceptions | P,P,P,F,F,P,P,P,P | 1,3,1,1,5,4,5 | 49.2 |
| B. Stable structured runtime-error envelope | P,P,P,P,P,P,P,P,P | 5,5,5,5,4,5,5 | 97.6 |
| C. Phase 1 diagnostics alone | P,P,P,P,F,P,P,P,P | 3,3,3,2,5,4,5 | 67.0 |

Score rationale/confidence: A fails G4/G5 because raw exceptions have no stable
owned or actionable contract (H). B maximizes failure safety with bounded
mapping work (H). C preserves useful validation diagnostics but fails G5 for
lacking attempt/operation runtime context (H).

Recommend B. Every runtime failure carries stable category/code, attempt ID, affected operation/port where known, outcome, plain-English explanation/remedy, and sanitized technical type/message/traceback/cause-chain. It excludes credentials, raw environment values, and arbitrary object representations. A Phase 1 validation diagnostic remains a distinct pre-dispatch refusal, not a runtime failure. E8 supports technical context without raw-exception-only behavior.

### D2.8 — Minimal actual deterministic scalar-proof boundary (M)

| Candidate | G1–G9 | Scores | Total |
|---|---|---|---:|
| A. Mocked/prewritten outcomes | P,P,P,P,F,P,P,P,P | 1,2,1,1,5,5,5 | 47.6 |
| B. Actual pure scalar transforms over controlled values | P,P,P,P,P,P,P,P,P | 5,5,5,5,5,5,5 | 100.0 |
| C. User-data/model workflow | P,P,P,P,P,P,F,F,P | 3,4,4,3,1,2,1 | 57.0 |

Score rationale/confidence: A fails G5 because prewritten outcomes cannot prove
the real error/dispatch path (H). B has complete deterministic, bounded proof
coverage without data/model policy (M). C fails G7/G8 by introducing user
data/model scope and a broad unsupported environment (H).

Recommend B: a later approved packet may propose a tiny family of real deterministic side-effect-free scalar transforms, one controlled deterministic failure, and one deterministic managed-output serialization. This chooses a family boundary, not a fixture, contract, callable, dependency, or artifact format. Evidence must cover linear/branched/joined work, exactly-once sharing, repeatability, publish/partial failure/cleanup, within-attempt reuse, changed-key nonreuse, invalid refusal, and runtime failure. Exact fixture/operations need static binding, Phase 1 contract, and provenance/license/size approval. No user data, preparation, training, evaluation, UI/API, or export is allowed.

## 5. Cross-decision ownership and evidence narrative

| Concern | Owner/boundary | Not owner |
|---|---|---|
| Canonical workflow/validation | Phase 1 schema, registry, diagnostics | UI, planner, runtime repair |
| IR/plan | Phase 2 engine after valid input | layout, creation order, generated code |
| Binding/dispatch | Static first-party runtime map | document, plugins, dynamic imports |
| Run record | Immutable Phase 2 attempt record | Phase 6 history/comparison UX |
| Artifacts | Named per-run owned local directory | General store, fixture, UI success claim |
| Cache | Attempt-owned result table with events | Persisted cross-run cache |
| Diagnostics | Phase 1 validation or Phase 2 runtime envelope | Raw exception-only result |
| UI | Future consumer/presenter | Scheduler or semantic authority |
| Experiment/state | Future lineage/comparison product | Mutable execution source of truth |
| Export | Phase 7 consumer of canonical workflow/IR | Execution mechanism |

Required later evidence: valid linear plan; equivalent branched workflows with reversed layout/creation/collection order producing the same sorted plan and one shared upstream computation; repeated recorded conditions; changed parameter/input/binding/environment producing fresh computation; invalid Phase 1 input refused before dispatch; controlled runtime failure producing blocked downstream state, partial-artifact evidence, and structured envelope. This is a narrative, not fixture, source, or executable sample.

Deferrals are Phase 3+ visual regions/boundaries, UI/API, data/privacy, models, experiment comparison/restoration, export, AutoML, agents, and user-facing behavior. No material documentary uncertainty blocks recommendation; no feasibility spike is proposed.

## 6. Worker self-assessment and handoff

| Acceptance area | Assessment |
|---|---|
| EP01-AC01–AC05 | Met: authority, inputs, baseline, current primary evidence, gates, eight reproducible matrices, fact/inference separation. |
| EP01-AC06–AC11 | Met as recommendations: canonical boundary, static binding, deterministic planning, bounded run/artifact/cache/error policy, minimal proof, ownership separation. |
| EP01-AC12–AC13 | Met pending final scope check: report is sole worker artifact; no source, fixture, dependency, lock, runtime, UI/API, remote, staged, or committed change. |
| EP01-AC14 | Pending final commands, lock, ignored state, and exact-scope evidence. |
| EP01-AC15–AC16 | Not self-accepted. Fresh independent validation and Central acceptance remain required. |

Final attestation passed in packet order, then the complete sequence was rerun successfully against this report: npm.cmd run check (including 51 selected unit tests, three integration tests, and smoke); npm.cmd run coverage (54 Python tests); npm.cmd run deps:inventory; npm.cmd run license:check (431 locked packages); npm.cmd run deps:audit (zero known vulnerabilities); and git diff --check. Both locks retained the Section 1 hashes. Generated ignored state was inspected (18,236 ignored paths); it remains untracked. Final status distinguishes pre-existing changes (ViDAP_Phase_2_Plan.md, ViDAP_Roadmap.md, ViDAP_P2_EP01.md) from this sole worker artifact (ViDAP_P2_EP01_Decision_Report.md). Nothing was staged, committed, pushed, or otherwise changed remotely.

Independent-validator handoff: read all governing inputs and this report; recheck high-impact sources; recalculate tables; independently apply G1–G9; verify no implicit dependency, fixture, data/model, runtime implementation, persistence store, UI/API, or Phase 3+ selection; reproduce complete attestation and hygiene without edits; return Accept, Revise, or Blocked for Central reconciliation.
