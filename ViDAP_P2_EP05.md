# ViDAP P2-EP05 — Deterministic Scalar Reference Workflow Proof

| Field | Value |
|---|---|
| Status | Complete — v0.3 independently validated and centrally accepted |
| Packet version | 0.3 |
| Packet type | Bounded headless reference-operation and controlled-fixture implementation |
| Parent phase plan | `ViDAP_Phase_2_Plan.md` version 1.7, WS2.5 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.4, P2/checkpoint A2 |
| Prerequisites | P2-EP01 D2.1–D2.8 accepted; P2-EP02 v0.2, P2-EP03 v0.1, and P2-EP04 v0.1 complete and centrally reconciled |
| Authorized worker report | `ViDAP_P2_EP05_Implementation_Report.md`; existing v0.1 and v0.2 findings must be preserved |
| Created | 2026-09-25 |
| Approved | v0.3 approved 2026-09-25 by explicit user direction |
| Accepted | 2026-09-25 in `ViDAP_P2_EP05_Validation_and_Reconciliation.md` |
| Prior approvals | v0.1 and v0.2 approved 2026-09-25; superseded for execution by v0.3 |
| Revision reason | v0.2 post-commit recovery could report failure while durable success remained, and rewrote an immutable terminal record to pending |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved v0.1 and then v0.2 on 2026-09-25. The v0.1 worker stopped
on incompatible binding revisions. The v0.2 worker implemented the reference
proof, but independent validation found an unresolved High publication defect;
the worker superseded its completion claim in the retained report. The user
separately approved this v0.3 contract correction on 2026-09-25, authorizing
one bounded worker repair under Section 8, followed by a fresh complete worker
attestation and independent validation. Neither the worker nor validator may
accept EP05 for Central.

This packet selects the exact D2.8 reference family, synthetic fixtures, and
managed-output format **for this proof only**. It does not add a general
numeric workflow type, data intake, preview persistence, ML operation,
experiment UI/history, service/API route, export, arbitrary code/plugin,
cross-run cache, or P2-EP06 closeout. Phase 2 remains incomplete until the
later closeout packet is independently validated and centrally reconciled.

## 2. Plain-English Packet Intent

The accepted engine has so far been exercised by handlers defined inside
tests. EP05 adds a tiny set of real, shipped operations that can calculate
with controlled integers. A saved synthetic workflow will genuinely run
through the accepted validation, representation, planner, dispatcher, and
attempt layer; a branch will share one upstream value, a join will combine
both branches, and an approved final value will be published into the one
owned local proof slot. A second workflow will fail deterministically and
show a useful failed-run record without a successful output artifact.

This is a foundation proof of execution, **not** a useful data-science or
modeling workflow and not a UI feature. Its result has no preview or
cross-run data-retention promise.

## 3. Governing Inputs and Traceability

Worker and independent validator must read:

1. The explicit 2026-09-25 approval of this exact v0.3 packet version; the
   v0.1 and v0.2 approvals and blocked worker evidence are historical only.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, 25–30.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 3–8, 11–14,
   17–18 and the worker-completion attestation rule.
4. `ViDAP_Roadmap.md` v4.4, P2/checkpoint A2, and
   `ViDAP_Phase_2_Plan.md` v1.7, especially D2.8, WS2.5, P2-AC03–P2-AC11,
   test strategy, and Phase 3+ exclusions.
5. `ViDAP_P2_EP01_Validation_and_Reconciliation.md`, authoritative for
   D2.1–D2.8, and the accepted P2-EP02, P2-EP03, and P2-EP04 packets,
   reconciliation records, source, tests, and exact limits.
6. Accepted Phase 1 D1.2–D1.7 and the canonical `vidap.workflow`/`1.0`
   document, static registry/contract, compatibility, and diagnostic code.
7. Accepted D0.6 dependency/license policy and D0.7 controlled-fixture
   policy; inspect the existing `fixtures/p1-ep05/fixture-manifest.json` as
   a metadata pattern, **not** as a source of runtime semantics.
8. `UX refinement.txt` as later-phase interaction context only; layout and
   visual regions do not determine this reference computation.
9. This packet.

The packet advances OV §§12, 18–19, 21–22A, 25 and Phase 2 WS2.5. It does
not reconcile the whole phase or open detailed Phase 3 planning.

## 4. Approved Reference Contract

Approval of v0.3 authorizes the following exact first-party reference
design. The worker must not choose substitute operations or silently expand
the Phase 1 type vocabulary.

### 4.1 Static contracts, bindings, and arithmetic

- Create a **separate** immutable `REFERENCE_REGISTRY`; do not alter Phase 1's
  accepted `BUILTIN_NODE_REGISTRY` or any Phase 1 source. The existing nominal
  port token `artifact` is the only carrier for this deliberately opaque
  scalar proof. Here it means an in-memory checked integer value, **not** a
  managed file, a general scalar type, or a claim that all `artifact` ports
  are numeric. Every reference handler enforces the narrower runtime type.
  Any later general numeric type requires a separately accepted Phase 1
  contract decision. No implicit adapter or cross-token connection exists.
- The only node type/operation-key pairs are the same exact keys in this
  table. **Each `StaticBinding.revision`, each matching
  `RuntimeRegistration.binding_revision`, and `BindingMap.revision` must equal
  `vidap.reference.bindings.v1`.** The accepted EP02 preparation
  requires exact equality; do not use a shorter per-operation revision,
  change that check, or introduce revision fallback. The runtime table itself
  uses the accepted EP03 runtime-table revision. Definitions, bindings, and
  handlers are constructed in first-party code, not from fixture text or
  discovery.

| Node type and operation key | Declarative contract | Actual handler behavior |
|---|---|---|
| `vidap.reference.literal` | Required integer `value` parameter; no inputs; one `artifact` output `value` | Emit that exact signed 64-bit integer. |
| `vidap.reference.multiply` | One required `artifact` input `input`; required integer `factor` parameter; one `artifact` output `value` | Multiply the input by `factor`; refuse signed 64-bit overflow. |
| `vidap.reference.add` | Two separately required, cardinality-one `artifact` inputs `left` and `right`; one `artifact` output `value` | Add the two inputs; refuse signed 64-bit overflow. |
| `vidap.reference.emit` | One required, cardinality-one `artifact` input `input`; one `artifact` output `value` | Return the input unchanged; mark the single terminal proof output. The handler performs no file I/O. |

- The `value` and `factor` parameter constraints are inclusive
  `-9223372036854775808` through `9223372036854775807`, with no implicit
  default. All handlers require `type(value) is int` (so booleans refuse),
  exactly the declared incoming ports/cardinalities, and signed 64-bit input
  and output range. They perform pure integer arithmetic only. An overflow
  raises a controlled `OverflowError` at the handler boundary and is recorded
  by the accepted `handler-failed` runtime envelope; no wraparound, clamping,
  floating-point conversion, raw exception message, or retry occurs.
- The first-party entry `run_reference_attempt(document, *, seed=None)`
  supplies this fixed registry, `BindingMap`, and runtime table to EP04's
  `run_attempt` exactly once. It accepts a canonical in-memory
  `WorkflowDocument`, not a path, JSON text, code snippet, callable, or UI
  state. The declared seed is recorded/keyed by EP04; these arithmetic
  handlers do not use randomness. The generic EP04 run entry remains valid
  for its previous callers and retains its default no-output behavior.
- The reference output policy requires **exactly one** `emit` node with no
  outgoing edges. Missing, multiple, or nonterminal emit nodes refuse before
  an attempt ID, handler call, or owned directory. This is a proof-specific
  first-party policy, not an arbitrary document-selected output path or
  general graph-result selection rule.

### 4.2 One versioned managed scalar output

- Extend only the trusted EP04 run-layer seam necessary to select the one
  completed emit node's `value` output *after successful dispatch and before
  terminal record publication*. The selection is determined by the static
  reference operation key and fixed policy above, never by a workflow field
  naming a path, serializer, function, or arbitrary output. Do not duplicate
  Phase 1 validation, replan, redispatch, or let a handler write a file.
- Approve the existing fixed `proof-output.bin` slot for this **single**
  reference format. Its inherited `.bin` name does not make the payload
  arbitrary: it contains exactly compact UTF-8 JSON, no BOM/newline, with
  recursively UTF-16-ordered object keys and the envelope
  `{"format":"vidap.reference-scalar","schemaVersion":"1.0","value":15}`
  for the successful fixture below. The sole value is a signed 64-bit JSON
  integer; no UUID, time, hostname, preview data, or mutable environment
  enters the bytes. Keep EP04's 64 KiB slot limit and fixed ownership root.
- On success, publish the bytes through EP04's owned `write_proof_slot`
  before its atomic terminal record; only then may the successful record list
  `proof-output.bin` alongside `record.json`. Two equal controlled runs have
  identical output bytes, while their attempt IDs/timing and directory names
  differ. The record may identify the relative slot but must not claim
  cross-run cache reuse or default storage of intermediate outputs.
- A missing/wrong-typed emit value, serialization failure, oversized bytes,
  or proof-write failure cannot yield a successful record or a success-looking
  output reference. A terminal *publication-call* error is not by itself proof
  that the atomic replacement failed: the replacement of `record.json` is the
  commit point, and a later error may be only a lost acknowledgement. Under
  EP04's pinned ownership and containment checks, read back the durable state
  before classifying that error:
  - If the exact intended immutable terminal record is present, and every
    referenced fixed slot exists with the exact intended bounded bytes,
    report the committed terminal outcome. For the controlled success proof,
    this is success despite the later acknowledgement error; do not rewrite
    or delete its terminal record or proof.
  - If the expected owned `pending` record remains and no terminal record was
    committed, return a sanitized failed publication outcome only after safe
    same-attempt rollback of unpublished proof/staging slots. If rollback
    fails, report cleanup incomplete while leaving inspectable pending
    ownership; never claim that cleanup occurred.
  - If readback fails, ownership changes, or the record/slot state is neither
    of those two verified cases, surface a distinct sanitized **publication
    indeterminate** error with the validated attempt ID. Do not return an
    `AttemptResult` labeled succeeded or failed, rewrite a terminal record,
    delete any possibly published slot, or retry publication. Leave the owned
    attempt intact for explicit inspection and recorded-ID-only cleanup.
    Indeterminate is not a third durable terminal state.
- A published `succeeded` or `failed` record is immutable. Remove v0.2's
  terminal-to-`pending` restoration path; neither recovery nor tests may use
  it. Preserve EP04's pinned-handle, reparse, atomicity, and recorded-only
  removal rules. An operation failure writes no proof output. This clarification
  changes only EP05's classification of a post-commit acknowledgement error,
  not D2.4's terminal immutability or EP04's generic no-output run behavior.

### 4.3 Controlled input fixtures and their expected meaning

Create exactly two synthetic UTF-8 `vidap.workflow`/`1.0` inputs and one
manifest under `fixtures/p2-ep05/`. The fixtures are reviewed inputs, not
hard-coded operation results. The implementation must compute their outputs
with the shipped handlers.

| Fixture | Fixed graph and independently calculable result |
|---|---|
| `branched-success-v1.json` | Workflow ID `30000000-0000-4000-8000-000000000001`. Node IDs `31000000-0000-4000-8000-000000000001`–`0005`: literal `value=3`; multiply `factor=2`; multiply `factor=3`; add; terminal emit. Connect literal output to both multipliers, their outputs to `left`/`right` of add, and add output to emit. Expected value is `3×2 + 3×3 = 15`; exactly one literal computation, two branch consumptions, one join, five completed nodes, and the exact managed envelope above. |
| `checked-overflow-v1.json` | Workflow ID `30000000-0000-4000-8000-000000000002`. Node IDs `33000000-0000-4000-8000-000000000001`–`0005`: literal `value=9223372036854775807`; literal `value=1`; add; terminal emit; independent literal `value=7`. Connect the first two literals to add `left`/`right`, and add to emit. Dynamic smallest-ready-ID scheduling attempts nodes 1, 2, then 3; add overflows. Nodes 1–2 completed, node 3 failed, emit node 4 blocked, independent node 5 unrelated/unstarted. Outcome `failed`, code `handler-failed`, technical type `OverflowError`, and no proof output. |

The fixture manifest must give each input a stable ID/version, repository-
relative path, exact byte size and SHA-256, synthetic provenance, MIT terms,
manual creation method (or a checked-in deterministic generator with fixed
seed/version if used), expected semantic result/status, permitted consumers
  (`P2-EP05` tests and later Phase 2 validation/closeout only), privacy
  classification, and Central-review status/date. Use `centralReviewer` to
  distinguish Central's approval of this fixed design from still-pending
  byte-level review, `reviewDate` for that packet-approval date, and an
  explicit pending byte-review status. Packet approval pre-approves the
  specified design, **not** unseen fixture bytes; final byte-level acceptance
  belongs to the later independent validation and Central reconciliation.
There is no external source, dataset, person, network ID, credential,
absolute path, or telemetry. Each new fixture and the manifest is below
16 KiB; all files under root `fixtures/` remain below the accepted 64 KiB
aggregate. Changes to bytes/expected properties require a versioned,
reviewable manifest correction, not a silent snapshot rewrite.

## 5. Required Real Proof and Negative Challenges

The focused tests must load the actual fixtures with the accepted strict
deserializer and execute `run_reference_attempt`; a mocked trace or
precomputed result cannot satisfy this packet. Prove at least:

1. The success fixture passes Phase 1 validation, uses the accepted
   representation/contract snapshot, plans and dispatches once, yields the
   independently calculated value 15, records five real computations and
   five actual edge consumptions, publishes only the exact versioned output
   bytes and owned record, and cleans only that run by explicit ID.
   A focused preparation challenge must also prove that the exact approved
   static binding/map/runtime revisions prepare and preflight without
   `binding-revision-mismatch`; a deliberate unequal revision still refuses.
2. A separately constructed linear literal → multiply → emit workflow
   computes `4×5 = 20` through the same first-party path. Reverse node/edge
   collection order and change labels/layout through the fixed reference
   entry: scheduling, semantic digest, value, and managed bytes remain
   invariant where meaning is unchanged. Separately challenge accepted
   preparation/planning with equivalent reversed registry/binding
   construction order; the production entry itself keeps one fixed static
   registry. No visual field enters a key.
3. Repeat an identical controlled run: distinct attempt IDs/record timing,
   the same semantic meaning, real handler recomputation, no cross-run hit,
   and byte-identical scalar output. Change a literal value and separately
   a multiplier factor: the relevant digest/key and computed result change;
   no stale result is returned. EP04's accepted independent component-key
   tests remain evidence for binding/seed/environment changes; do not fake a
   production environment by altering host state.
4. The overflow fixture fails at its real add handler; it preserves completed,
   failed, blocked, and unrelated node statuses, returns the sanitized EP04
   envelope, does not call emit or the unrelated handler, and publishes no
   proof slot. Test `-9223372036854775808`, overflow on multiplication,
   invalid boolean/non-integer handler input, and exact input cardinality.
5. Missing/multiple/nonterminal emit and an invalid or unsupported Phase 1
   workflow refuse before handler/allocation. Neither a fixture field nor a
   caller can choose a serializer, file path, executable target, or output
   slot. Static binding/table mismatch remains a pre-dispatch refusal.
6. Force bounded proof-write and terminal-publication failures after
   successful arithmetic. Distinguish pre-commit failure with verified
   pending ownership, post-commit acknowledgement error with exact terminal
   record/output readback, and unreadable, mismatched, or failed readback
   after a possible commit. The first may return failed after safe rollback;
   the second must report the verified committed outcome; the third must
   raise sanitized publication-indeterminate without a false success/failure
   result or destructive recovery. Inject an error after terminal replacement
   and another during readback; prove the immutable success record and proof
   are not rewritten/deleted. Also force rollback failure while still pending.
   Recorded-ID-only cleanup must preserve another attempt. A pre-existing
   owned slot must not be overwritten. Test the actual EP04 owned-file path,
   including current Windows directory-swap protections, without broad
   deletion.
7. Recompute every fixture's byte size and SHA-256 from exact committed
   bytes; check manifest provenance, license, expected properties, consumers,
   aggregate size, no sensitive/user-path material, and final newlines.
   No generated output or cache is committed under `fixtures/`.

The proof is intentionally narrow. It establishes the selected Phase 2
headless reference path, not a general data, model, experiment, UI, or
export workflow. If the accepted EP04 seam cannot support the managed
output without changing a non-Section 8 path or weakening ownership safety,
stop with a requirement-linked Central blocker instead of adding a second
executor or bypassing the accepted run record.

## 6. Documentation and Architecture Boundaries

Update `README.md` narrowly so its current-state claims no longer say Phase 0
is awaiting validation or that no workflow schema/engine exists. Describe
the accepted Phase 1 kernel and the still-headless, controlled Phase 2
reference proof accurately; `launch` and `/api/status` remain only the
foundation shell, not a workflow API or product UI. Preserve existing setup,
quality, dependency, security, and local-only guidance; add only verified
repository-relative links.

Do not modify Phase 1 code or built-in specimens, P2-EP02 representation,
P2-EP03 planner/dispatcher, P2-EP04 key/error semantics or Windows artifact
safety, manifests/locks/CI, or existing fixtures. Do not add dependencies,
new nominal types, generic operation loading, services, browser workflow
controls, data/ML, persistent cross-run cache, experiment restoration,
export, or Phase 3+ behavior. The output-policy bridge is first-party and
fixed; no user-supplied callback, root path, or arbitrary artifact name.

## 7. Stop Conditions

Stop `Blocked` for a missing accepted prerequisite, a Section 8 collision,
an unsafe or undefined output-publication seam, a fixture/contract mismatch
that would require a Phase 1 revision, a need for an unapproved dependency or
artifact slot, or a non-reproducible mandatory check. Name the requirement,
evidence, and owner. Do not make a broader policy decision inside worker
execution or ask the validator to repair it. The existing v0.1 blocker report
is an authorized prior worker artifact, **not** a Section 8 collision;
preserve its v0.1 and v0.2 blocker/revision history when adding v0.3 evidence.

## 8. Exact Authorized Worker Outputs

Only these twelve paths may be created or modified by the approved worker:

| Path | Purpose |
|---|---|
| `python/src/vidap_execution/__init__.py` | Export only the bounded first-party reference entry, if needed. |
| `python/src/vidap_execution/reference.py` | Separate static registry, bindings, runtime table, pure checked-integer handlers, and reference entry. |
| `python/src/vidap_execution/run.py` | Narrow fixed output-policy bridge between successful dispatch and terminal record. |
| `python/src/vidap_execution/artifacts.py` | Make the existing proof-slot description truthful and, only if necessary, a narrow approved reference-output guard without weakening EP04 safety. |
| `python/src/vidap_execution/output.py` | Versioned deterministic signed-integer JSON serializer and fixed emit selection policy. |
| `python/tests/test_execution_reference.py` | Real operation, graph, ordering, failure, repeat, and refusal proof. |
| `python/tests/test_execution_reference_output.py` | Managed bytes, publish/rollback, ownership, and format challenges. |
| `fixtures/p2-ep05/branched-success-v1.json` | Controlled successful reference workflow. |
| `fixtures/p2-ep05/checked-overflow-v1.json` | Controlled failed reference workflow. |
| `fixtures/p2-ep05/fixture-manifest.json` | Byte-level integrity, terms, privacy, and expected-result metadata. |
| `README.md` | Correct current-state and narrow headless reference description. |
| `ViDAP_P2_EP05_Implementation_Report.md` | Sanitized final worker evidence and independent-validation handoff. |

The worker must record and preserve pre-existing dirty paths by owner. The
existing `ViDAP_P2_EP05_Implementation_Report.md` retains v0.1 and v0.2
history and may be updated only to retain that history and add truthful v0.3
evidence; do not erase or mislabel its prior states. Test
run records/output live only under ignored `.vidap-local/runs/` and must be
explicitly cleaned by validated ID; they are not Section 8 tracked outputs.
No packet, roadmap, phase-plan, reconciliation, existing test/fixture,
manifest, lock, CI, or remote edit is authorized.

## 9. Worker Sequence and Final Attestation

1. Read Section 3 and confirm explicit approval of v0.3. Record
   branch, HEAD, staged/unstaged/untracked baseline, ownership, Section 8
   collisions apart from the authorized prior blocker report, and both lock
   hashes before writing. Inspect the actual EP04
   publication path; do not infer that the test-only proof slot already has
   approved product semantics.
2. Run baseline `npm.cmd run setup` and `npm.cmd run check`. If a restricted
   sandbox denies `uv.exe`, use the documented normal Windows path; do not
   bypass TLS, choose another interpreter, or alter either lock.
3. First verify the corrected exact binding equality against accepted EP02
   preparation and EP03 preflight. Remove the v0.2 terminal-to-pending
   restoration path and implement the Section 4.2 commit-point/readback
   contract without changing generic EP04 behavior. Implement only Section 8
   and focused real-operation tests. Generate the
   two fixture byte hashes/sizes from the finished files and record them in
   the manifest. If a required repair is outside scope, stop `Blocked`.
4. On the **final post-change tree**, run in this exact order:
   `npm.cmd run check`; `npm.cmd run coverage`;
   `npm.cmd run deps:inventory`; `npm.cmd run license:check`;
   `npm.cmd run deps:audit`; `git diff --check`.
   If any fails, repair within scope and rerun the entire ordered sequence,
   or return a named blocker. Pre-change/partial passes do not count.
5. Recheck both lock hashes, twelve-path worker scope, fixture integrity and
   aggregate size, `README.md` links/claims, ignored generated state,
   managed-run cleanup, whitespace/final newlines, sensitive/user-path
   patterns, and prescribed-port listener/PID/log residue after smoke.
   Never broadly delete `.vidap-local`, user data, or another attempt.
6. In one disposable copy outside the repository and OneDrive, with isolated
   npm/uv caches, reproduce locked setup, the focused EP05 suites, fixture
   hashes/expected outcomes, and `npm.cmd run check`. Validate resolved
   exact copy/cache targets before bounded removal and verify absence.
   Report outcomes without user-specific absolute paths.
7. Write the Section 8 report and stop. Do not stage, commit, push, alter
   remote state, validate your own work, accept for Central, or start EP06.

## 10. Required Implementation Report

The report must preserve the v0.1 blocked history, v0.2 approval and failed
validation, and document the separate v0.3 approval, packet/governing
versions, baseline,
pre-existing work, target commit, twelve-path scope, lock hashes, fixture
sizes/digests and total, and the concrete source mapping for every selected
contract and operation. It must distinguish Phase 1 `artifact` token usage
from actual checked-integer semantics; explain the fixed first-party output
policy, exact serialized bytes/revision, owned publication/rollback,
commit-point readback and indeterminate failure classification, and
reference-only limits.

Report each required real workflow's calculated values, schedule, actual
handler calls, reuse events, record outcome, output bytes/digest or absence,
and cleanup. Include invalid/overflow, changed-input/parameter, repeated
attempt, and pre-commit, post-commit, and indeterminate publication
challenges. Include the complete final
ordered attestation and isolated-copy proof, with verified cleanup and
hygiene. A failure is `Blocked` or `Revise` with a requirement-linked finding,
not an implementation-complete claim. Request fresh independent validation;
leave Central acceptance and Phase 2 closeout pending.

## 11. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP05-AC01 | Exact v0.3 packet approval, accepted prerequisite chain, v0.1 and v0.2 blocker/revision disposition, baseline/ownership, target commit, and lock authorities are evidenced. |
| EP05-AC02 | Worker delta is confined to twelve Section 8 paths; inherited Phase 1–P2-EP04 boundaries and prohibited scopes remain unchanged. |
| EP05-AC03 | A separate explicit registry/binding/runtime table provides exactly four approved first-party operations; every per-operation and map revision is the same exact approved value and passes accepted preparation/preflight, while a mismatch refuses. No dynamic or document-selected handler exists. |
| EP05-AC04 | Declarative ports use only existing `artifact` nominal token; handlers independently enforce exact signed 64-bit integer/cardinality semantics without implying a general numeric type. |
| EP05-AC05 | The real literal, multiply, add, and emit handlers produce independently calculated values, refuse bool/invalid input and overflow, and have no side effect or hidden state. |
| EP05-AC06 | The reference entry uses accepted validation, representation, plan, dispatch, and attempt path once; emit selection is single, terminal, fixed, and refused before allocation when invalid. |
| EP05-AC07 | The success fixture executes its real branch/join to value 15 with one upstream computation and actual reuse events; a linear workflow computes 20; construction/layout changes preserve meaning. |
| EP05-AC08 | Repeated attempts recompute and produce equal reference bytes with distinct attempt IDs; changed literal/factor yields changed semantic key/result and no cross-run hit. |
| EP05-AC09 | The controlled overflow fixture records correct completed/failed/blocked/unrelated status, sanitized affected-node failure, and no managed output. |
| EP05-AC10 | The selected versioned serializer produces exact bounded UTF-8 JSON in the inherited fixed slot, with no timestamp, UUID, environment, preview, or arbitrary bytes. |
| EP05-AC11 | Proof-write/pre-commit failure cannot appear successful; post-commit acknowledgement errors report only an exactly verified durable outcome; unresolved commit state raises sanitized publication-indeterminate without a false success/failure result, terminal rewrite, unsafe deletion, or retry. Pending rollback, cross-attempt isolation, and recorded-only cleanup preserve EP04 artifact safety and terminal immutability. |
| EP05-AC12 | Both fixture bytes and manifest satisfy accepted D0.7 metadata, synthetic provenance, MIT terms, privacy, byte-hash/size, expected properties, permitted consumers, per-file and aggregate bounds; the manifest distinguishes packet-design review from Central's later byte-level acceptance. |
| EP05-AC13 | README current-state claims and links are accurate without describing a workflow API, product UI, data/ML, export, or general artifact retention. |
| EP05-AC14 | Complete final post-change ordered attestation, focused suites, disposable clean-copy proof, unchanged locks, exact file scope, hygiene, managed-run cleanup, and listener checks pass. |
| EP05-AC15 | Worker report is complete, sanitized, calculation/fixture-traceable, and leaves validation and Central acceptance pending. |
| EP05-AC16 | Fresh independent validation returns `Accept` without unresolved Critical or High findings after checking actual operation results, fixture bytes, artifact safety, architecture, calculations, and Git scope. |
| EP05-AC17 | Central separately reviews the exact fixture bytes and reconciliation evidence, then accepts P2-EP05 before drafting or authorizing P2-EP06. |

## 12. Independent Validation Handoff

The fresh validator must read Section 3, exact worker delta, report, source,
fixtures, and README. Independently calculate 15, 20, overflow and expected
statuses; recompute fixture byte sizes, SHA-256 and total, managed output
bytes/digest, both lock hashes, and selected reuse keys. Challenge true
first-party dispatch rather than trusting test traces; attempt malformed
and reordered graphs, missing/multiple emit, changed semantic inputs,
failure, and all three Section 4.2 publication/readback cases, including
injected post-commit readback failure. Confirm no Phase 1/P2-EP02–EP04
contract erosion or later-phase capability. Reproduce relevant final checks
and bounded clean-copy proof. The validator may create and clean only
necessary ignored/transient test state; do not edit tracked files, repair
the worker output, push, accept for Central, or begin EP06. Return `Accept`,
`Revise`, or `Blocked` with severity, requirement, evidence, and owner.
`Accept` satisfies EP05-AC16 only; Central owns EP05-AC17.

## 13. Fresh-Chat Launch Prompts

### Worker

> Execute the approved `ViDAP_P2_EP05.md` v0.3 as the bounded scalar-reference repair worker. Read every governing input, preserve the historical v0.1 and v0.2 findings in `ViDAP_P2_EP05_Implementation_Report.md`, and follow the corrected publication contract exactly. Complete the full final attestation and clean-copy proof, then stop with the updated report and an independent-validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P2-EP06.

### Independent validator, only after worker handoff

> Act as the independent validator for `ViDAP_P2_EP05.md` v0.3. Read the packet, its governing inputs, accepted EP04 run/artifact contract, and revised `ViDAP_P2_EP05_Implementation_Report.md`. Verify the commit-point/readback distinction, immutable terminal behavior, all acceptance criteria, actual reference calculations and error behavior, fixture/managed-output bytes and hashes, architecture boundaries, locks, and Git/file-scope compliance. Independently fault-inject post-commit acknowledgement and readback failures. You may create and clean only bounded ignored/transient verification state; do not edit tracked files, accept for Central, alter remote state, or begin P2-EP06. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 14. Next Action

P2-EP05 v0.1 and v0.2 remain historical blocked/revised attempts. The v0.3
repair passed independent validation, and Central accepted the exact fixture
bytes and bounded implementation in
`ViDAP_P2_EP05_Validation_and_Reconciliation.md`. EP05-AC17 is satisfied.
P2-EP06 is ready to draft but not approved or authorized for execution;
Phase 2 completion remains closed pending its separate closeout.
