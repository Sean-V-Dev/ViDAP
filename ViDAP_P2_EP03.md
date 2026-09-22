# ViDAP P2-EP03 — Deterministic Planner and Reference Dispatcher

| Field | Value |
|---|---|
| Status | Approved — authorized for bounded worker execution |
| Packet version | 0.1 |
| Packet type | Bounded headless planning and dispatch-control implementation |
| Parent phase plan | `ViDAP_Phase_2_Plan.md` version 1.4, WS2.3 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.1, P2/checkpoint A2 |
| Prerequisites | P2-EP01 D2.1–D2.8 accepted; P2-EP02 v0.2 complete and centrally reconciled |
| Authorized worker report | `ViDAP_P2_EP03_Implementation_Report.md` |
| Created | 2026-09-22 |
| Approved | 2026-09-22 by explicit user direction |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved this exact packet version on 2026-09-22.

Approval authorizes one bounded worker to derive a deterministic plan
from the accepted P2-EP02 representation and implement the in-process,
sequential dispatch control selected by D2.3. Test-local scalar handlers may
exercise the dispatch path. No product operation is registered in this packet.
The worker may change only the Section 7 paths.

The packet does not authorize P2-EP04 run/provenance records, artifact or data
storage, a persistent or cross-run cache, the complete D2.6 reuse key, the
D2.7 user-facing runtime error envelope, D2.8 product reference operations,
fixtures, dependency/lock changes, UI/API/server changes, remote changes, or
P2-EP04 work.

## 2. Plain-English Packet Intent

### What this packet will build

It turns the frozen workflow recipe into a predictable order of nodes. Its
dispatcher then follows that order, passes each computed output to downstream
nodes, and stops cleanly on the first failure. A branch shares the one result
already computed by its upstream node; a join waits for all predecessors.

### Why this is the next step

P2-EP02 established what a valid workflow means to the future engine. EP03
establishes the order and control flow before later packets add durable run
records, artifact ownership, and approved product operations.

### What counts as evidence

Tests must run the actual planner and dispatcher with small test-local scalar
handlers, including a branch, join, reversed construction order, and failure.
The test handlers prove orchestration only. Phase 2 completion still requires
the separately approved real reference operation family in P2-EP05.

## 3. Governing Inputs and Traceability

The worker and independent validator must read:

1. Current explicit user approval of this exact packet version, if given.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 3–8, 11–14,
   17–18, Phase 2, and the worker-completion attestation rule.
4. `ViDAP_Roadmap.md` v4.1, P2 and checkpoint A2.
5. `ViDAP_Phase_2_Plan.md` v1.4, especially D2.1–D2.3, D2.6–D2.8, WS2.3,
   architecture boundaries, test strategy, and P2-AC02–P2-AC04.
6. `ViDAP_P2_EP01_Validation_and_Reconciliation.md`, authoritative for
   D2.1–D2.8; and `ViDAP_P2_EP01_Decision_Report.md` for the accepted D2.3
   scheduling rationale.
7. `ViDAP_P2_EP02.md` v0.2,
   `ViDAP_P2_EP02_Validation_and_Reconciliation.md`, and accepted
   `vidap_execution` source/tests, authoritative for the immutable
   representation, contract snapshot, semantic digest, and static binding
   metadata.
8. The accepted Phase 1 reconciliation records and the applicable Phase 0
   runtime, quality, dependency, and fixture controls.
9. `UX refinement.txt` as consultative Phase 3+ interaction direction only;
   visual placement is never planner input.
10. This packet.

This packet advances OV §§12, 18–19, 21–22A, and 25 through Phase 2 WS2.3.
The phase-level demonstrations and run/provenance requirements remain open
until later approved packets supply their missing evidence.

## 4. Accepted Decisions Applied Here

- **D2.1:** Planning and dispatch control are synchronous and in process.
  There is no service, child process, or cancellation claim for an operation
  already running.
- **D2.2:** The only production preparation path calls P2-EP02's
  `prepare_execution` against a Phase 1-valid document, registry, and
  explicit `BindingMap`. It retains the workflow digest, contract snapshot
  reference, resolved parameters, operation keys, and binding revision.
  Executable handlers live in a separate first-party runtime table; neither
  the document nor `BindingMap` gains a callable or target path.
- **D2.3:** A sorted Kahn topological schedule selects the lexicographically
  smallest currently ready canonical node ID after every completion. Dispatch
  is sequential. An invocation-owned `(source node ID, output port key)`
  result table fans one computation to all consumers. The first handler or
  missing required outgoing value stops further invocation. Completed nodes remain
  visible as completed work within a failed dispatch; transitive unstarted
  descendants are blocked and unrelated unstarted nodes are distinguished.
- **D2.6:** This packet implements only D2.3's within-invocation fan-out. It
  does not claim a content-keyed memoizer, a cache hit/miss policy, reuse across
  invocations, or the complete D2.6 key. P2-EP04 must implement and validate
  those provenance/reuse details before such a claim is made.
- **D2.7:** A small internal structured stop reason records one affected node,
  operation key, and stable code. P2-EP04 owns the full attempt-linked,
  sanitized, user-facing runtime-error envelope and remedy policy. Phase 1
  diagnostics remain a distinct pre-dispatch refusal.
- **D2.8:** Only test-local, deterministic scalar handlers exercise this
  control path. They are not a shipped or approved product operation family,
  fixture, data/model computation, or Phase 2 exit proof.

## 5. Required Planner and Dispatcher Contract

The source may choose final Python names, but the worker report must map them
to these exact behaviors and tests must exercise the real source path.

| Concern | Required behavior |
|---|---|
| Validated entry | A synchronous planning entry takes `WorkflowDocument`, `NodeRegistry`, and explicit `BindingMap`, invokes accepted P2-EP02 preparation once, and propagates its Phase 1 diagnostics/binding refusals unchanged. No public path plans directly from document layout or bypasses validation. |
| Immutable plan | Contains a fixed first-party plan revision, the accepted `ExecutionRepresentation` or its exact immutable references, an ordered node-ID schedule, and immutable dependency/incoming-edge references. It has no run ID, timestamp, result, artifact, seed, environment, cache, UI, or callable. |
| Planning algorithm | Preflight checks that every edge references an existing node, exact duplicate directed edges are rejected, and cycles/self-dependencies refuse. A dynamic lexicographically sorted ready set produces a valid topological order; it must not rely on insertion order or one-time sorting of layers. An empty valid workflow yields an empty plan. |
| Contract boundary | The accepted path relies on Phase 1 for port existence/type/cardinality and on P2-EP02 for contract snapshot provenance. A defensive check of a manually constructed representation may reject dangling/duplicate/cyclic graph structure, but it must not claim to revalidate port contracts from a hash alone. |
| Runtime operation table | An explicit, immutable, separately versioned first-party table maps accepted `(operation key, binding revision)` pairs to trusted in-process handlers. It is constructed in code, never from workflow JSON, UI input, dynamic imports, a plugin, a path, a command, or network discovery. This packet ships no production handler registration; tests may construct test-local scalar handlers. |
| Dispatch preflight | Before the first handler call, ensure the table revision matches the plan and every used operation has exactly one matching handler. Missing, duplicate, or revision-mismatched handlers refuse without partial execution or fallback. P2-EP02 `BindingMap` remains non-executable and unchanged. |
| Input and output flow | Each handler receives frozen/resolved parameters and incoming edge values sorted lexicographically by `(target port key, source node ID, source port key, edge ID)`, with both endpoint identities retained. This preserves multiple incoming edges without inventing new cardinality rules. A handler returns a port-keyed output mapping; every outgoing source port needed by an edge must be present before any of that node's outputs enter the invocation-owned table. One source-port value is shared to every downstream consumer. |
| Failure flow | Catch a handler exception, malformed output mapping, or missing required outgoing value at the dispatch boundary and return one internal structured stop reason with category `execution`, stable code (`handler-failed`, `invalid-handler-output`, or `missing-output`), affected node/operation, and sanitized technical type where applicable; also return completed node IDs, failed node ID, blocked transitive descendants, and other unstarted IDs. Do not call another handler or publish partial outputs from the failed node. Do not expose raw exception text or traceback as a user-facing result. |
| Invocation lifetime | Allocate fresh schedule observation and port-result state per call. No retained global result, persistent cache, output write, run identity, artifact reference, or side-effecting cleanup exists. The dispatcher is an internal control component, not a product run API. |

Any new plan revision must be an explicit stable first-party identifier. A
change to planning meaning cannot silently reuse that revision. Test-only
handlers may perform actual small scalar calculations to prove dispatch, but
must never be registered as shipped product operations.

## 6. Required Implementation and Test Evidence

The worker must prove all of the following with deterministic focused tests:

1. Valid prepared linear, independent-root, branch, and join graphs plan in
   dependency order. A newly ready lower-ID node wins over an older ready
   higher-ID node, proving dynamic sorted-Kahn tie-breaking.
2. Reversing document/node/edge/registry construction order and changing
   labels, layout, or viewport leave the schedule and dispatch trace
   unchanged. The accepted workflow digest and contract snapshot remain
   consistent with P2-EP02.
3. An invalid Phase 1 document refuses before planning with the original
   ordered diagnostics. Missing/unbound static bindings refuse before
   dispatch. Directly challenged malformed representations reject dangling
   references, duplicate exact edges, self-dependency, and cycles.
4. Handler preflight rejects missing, duplicate, or revision-mismatched
   runtime registrations before **any** handler is called. The document
   cannot name or load an executable target.
5. Test-local handlers perform small scalar calculations. A shared upstream
   handler is called exactly once; both branches receive its same output;
   a join receives all predecessors in deterministic edge order. Multiple
   edges to one target port remain distinguishable by endpoint identity.
6. A handler exception stops at the first failed node. Tests distinguish
   completed nodes, the failed node, unstarted dependent descendants, and
   unrelated unstarted nodes; no later handler runs. A missing outgoing
   source-port value or malformed output mapping fails without publishing
   partial output.
7. Two separate dispatch calls allocate separate result tables and invoke
   handlers anew. No cross-call result reuse, cache hit, run ID, artifact, or
   persistent state is claimed. Results/observations are bounded to the call.
8. Static inspection and tests confirm no product operation, Phase 1/EP02
   mutation, dependency/lock change, fixture, file/network/process/UI/API,
   data/ML, export, plugin, or later-packet behavior was introduced.

These tests prove the control path, not the Phase 2 requirement for an
approved real reference operation family; P2-EP05 retains that obligation.

## 7. Exact Authorized Worker Outputs

The worker may create or modify only these six paths:

| Path | Purpose |
|---|---|
| `python/src/vidap_execution/__init__.py` | Update truthful package description and expose only the narrow planning surface, if needed; do not export a product run API. |
| `python/src/vidap_execution/planner.py` | Immutable plan, defensive graph checks, and deterministic planner. |
| `python/src/vidap_execution/dispatch.py` | Separate explicit runtime table and bounded sequential dispatch control. |
| `python/tests/test_execution_planner.py` | Planning determinism and refusal challenges. |
| `python/tests/test_execution_dispatch.py` | Test-local scalar dispatch, branch/join, preflight, and fail-stop challenges. |
| `ViDAP_P2_EP03_Implementation_Report.md` | Sanitized worker evidence and independent-validation handoff. |

The worker must not edit the accepted P2-EP02 representation/bindings or tests,
Phase 1 code/tests, manifests, locks, CI, fixtures, existing documentation, or
governing artifacts. Existing pre-worker dirty paths belong to their owners
and must be separated from this worker's exact six-path scope. Generated
ignored state may be used only for prescribed checks and must be verified or
cleaned as the packet requires.

## 8. Prohibited Scope and Stop Conditions

Do not add shipped product handlers or select D2.8's real reference operation
family. Do not change accepted workflow/contract/validation or P2-EP02
representation/binding semantics. Do not implement a user-facing run entry,
attempt identity, provenance/seed/environment record, durable or default
preview/intermediate output, artifact root, serialization, cleanup interface,
content-keyed or cross-run cache, or the complete D2.7 error envelope. Do not
start a service/process/browser, add a route or UI, download a dependency,
alter locks/CI, create a fixture, use user data or an ML model, export code,
perform remote mutation, or start P2-EP04 or later work.

If the accepted P2-EP02 representation lacks information required to satisfy
this packet without changing its contract, stop with the exact need and a
requirement-linked blocker. Do not silently extend P2-EP02, reconstruct
workflow meaning from visual state, or invent a substitute runtime policy.

## 9. Required Worker Sequence and Final Attestation

1. Read Section 3 and inspect the accepted EP02 reconciliation and current
   source. Record branch, target commit, staged/unstaged/untracked baseline,
   pre-existing work by owner, and both lock hashes. Verify no collision with
   the six Section 7 paths before writing.
2. Run `npm.cmd run setup` and `npm.cmd run check` as baseline checks. If the
   known restricted environment denies `uv`, use the documented normal
   Windows execution path. Do not substitute another interpreter, unlock
   dependencies, or bypass TLS checks.
3. Implement only Section 7 paths and focused tests. The dispatcher must
   preflight every handler before invoking one and keep all output state
   within one call. If a required correction is outside scope, stop `Blocked`.
4. On the final post-change tree, run **in this order**:
   `npm.cmd run check`; `npm.cmd run coverage`;
   `npm.cmd run deps:inventory`; `npm.cmd run license:check`;
   `npm.cmd run deps:audit`; `git diff --check`.
   A failed command requires an in-scope repair and a complete rerun of this
   ordered attestation, or a named blocker. Pre-change results do not count.
5. Verify both lock hashes remain unchanged. Inspect the exact worker file
   list, generated/ignored state, whitespace, new-file final newlines,
   sensitive content, and absence of worker-owned PID/log residue or
   prescribed-port listeners after any smoke run.
6. In one disposable copy outside the repository and OneDrive, with isolated
   npm and uv caches, reproduce locked setup, the focused EP03 suites, and
   `npm.cmd run check`. Remove only the exact bounded copy/cache paths and
   verify their absence. Record outcomes without user-specific absolute paths.
7. Write the authorized report and stop. Do not stage, commit, push, alter
   remote state, validate your own work, accept on Central's behalf, or begin
   P2-EP04.

## 10. Required Implementation Report

`ViDAP_P2_EP03_Implementation_Report.md` must identify packet/governing
versions, baseline and pre-existing changes, target commit, exact six-path
worker scope, lock hashes, and tests. It must map D2.1–D2.3 and the D2.6–D2.8
deferrals to concrete source behavior; explain the sorted-Kahn ready rule,
dependency/edge ordering, runtime table authority, preflight, branch fan-out,
join, failure/blocked/unrelated status, and invocation-owned output lifetime.

Report the complete ordered final attestation, clean-copy setup/focused/full
check and verified cleanup, text/sensitive/ignored-state/listener findings,
and any limitation. The report must say explicitly that test-only scalar
handlers are not approved product operations or Phase 2 exit evidence. It
must hand the result to a fresh independent validator and leave Central
acceptance pending. A failure must be `Blocked` or `Revise` with a precise
requirement-linked finding rather than an implementation-complete claim.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP03-AC01 | Prerequisites and governing decisions are accepted; baseline, pre-existing work, target commit, and lock authorities are accurately recorded. |
| EP03-AC02 | Worker changes are confined to the six Section 7 paths; accepted Phase 1 and P2-EP02 files and all prohibited scopes remain unchanged. |
| EP03-AC03 | The planning entry invokes accepted P2-EP02 preparation once and preserves its original Phase 1 diagnostics and binding refusals. |
| EP03-AC04 | The immutable plan carries stable revision and accepted workflow digest, contract snapshot, binding revision, and deterministic dependency references without run or UI state. |
| EP03-AC05 | Sorted-Kahn planning uses the smallest currently ready node ID; reverse-order/layout challenges produce the same plan and dispatch trace. |
| EP03-AC06 | Defensive graph checks refuse dangling, duplicate-exact, self-dependent, and cyclic representations without silently repairing or claiming port-contract revalidation. |
| EP03-AC07 | The separate first-party runtime table is explicit/versioned; complete handler preflight rejects missing, duplicate, or mismatched registrations before any call, and no workflow field selects executable code. |
| EP03-AC08 | Sequential dispatch computes each node once, fans one source-port result to all consumers, and delivers all join inputs in deterministic endpoint order. |
| EP03-AC09 | The first handler, malformed-output, or required-output failure stops dispatch with one structured internal reason; completed, failed, blocked-descendant, and unrelated unstarted nodes remain distinct, and failed-node partial outputs are not published. |
| EP03-AC10 | Separate calls share no result state or computation; no generalized/cache-keyed reuse or persistent result is claimed. |
| EP03-AC11 | Test-local scalar handlers exercise the actual planner/dispatcher path; no product operation family, fixture, artifact, run record, or later-packet capability is claimed. |
| EP03-AC12 | The complete ordered post-change attestation and isolated clean-copy proof pass; locks and hygiene remain compliant and bounded cleanup is verified. |
| EP03-AC13 | The report accurately maps evidence, decisions, limits, file scope, and pending independent/Central gates without user paths or sensitive content. |
| EP03-AC14 | A fresh independent validator returns `Accept` with no unresolved Critical or High finding. |
| EP03-AC15 | Central separately reconciles and accepts P2-EP03 before P2-EP04 is drafted or authorized. |

## 12. Independent Validation Contract

The validator must read the packet, governing inputs, accepted EP02 source and
reconciliation, the EP03 worker report, and the final changed files. It must
independently challenge dynamic ready-set ordering, reverse construction,
branch/join fan-out, preflight-before-call, malformed graph refusal, first
failure and blocked descendants, missing output, repeated-call isolation,
and the absence of production operations or later-packet behavior. Reproduce
the required attestations and bounded clean-copy/cleanup evidence as permitted;
verify exact file scope, both lock hashes, ignored/generated state, hygiene,
and report calculations/citations.

Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings. Do
not edit files, treat test-local handlers as Phase 2 exit proof, accept for
Central, alter remote state, or begin P2-EP04.

## 13. Fresh-Chat Launch Prompts

### Worker

> Execute the approved `ViDAP_P2_EP03.md` as the bounded planner and dispatcher worker. Read every governing input and follow the packet exactly. Complete the full final attestation and clean-copy proof, then stop with `ViDAP_P2_EP03_Implementation_Report.md` and an independent-validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P2-EP04.

### Independent validator

> Act as the independent validator for `ViDAP_P2_EP03.md`. Read the packet, its governing inputs, accepted EP02 bridge, and `ViDAP_P2_EP03_Implementation_Report.md`. Verify every acceptance criterion, deterministic scheduling/dispatch and failure challenges, citations/calculations, architecture boundaries, locks, and Git/file-scope compliance. Do not modify files, accept for Central, alter remote state, or begin P2-EP04. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

The bounded EP03 worker may execute this approved v0.1 packet and stop with
its implementation report for fresh independent validation. Central
acceptance of the implementation remains a separate later gate.
