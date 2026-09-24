# ViDAP P2-EP04 — Run Provenance, Owned Artifacts, Attempt-Local Reuse, and Runtime Diagnostics

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Packet type | Bounded headless run-foundation implementation |
| Parent phase plan | `ViDAP_Phase_2_Plan.md` version 1.5, WS2.4 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.2, P2/checkpoint A2 |
| Prerequisites | P2-EP01 decisions D2.1–D2.8 accepted; P2-EP02 v0.2 and P2-EP03 v0.1 complete and centrally reconciled |
| Authorized worker report | `ViDAP_P2_EP04_Implementation_Report.md` |
| Created | 2026-09-23 |
| Approved | 2026-09-24 by explicit user direction |
| Central reconciliation | `ViDAP_P2_EP04_Validation_and_Reconciliation.md` |
| Completed | 2026-09-24 after independent `Accept` and Central reconciliation |
| Owner | Central |

---

## 1. Authorization Boundary

Central approved this exact packet version on 2026-09-24. That approval
authorized one bounded worker to change only Section 7 paths. The worker
completed the implementation, fresh independent validation returned
`Accept`, and Central accepted it in the reconciliation record above.

The bounded worker may add a synchronous, in-process attempt
layer around the accepted planner/dispatcher: an immutable terminal run record,
one ignored and owned local run directory, visible within-attempt result reuse,
and a sanitized runtime-error envelope. The worker must stop after its report
and handoff to a separate independent validator. Neither worker nor validator
may accept the result for Central.

This packet does **not** approve a product operation, reference fixture,
general data or model artifact, preview retention, cross-run cache, service,
UI/API, or P2-EP05 work. EP03's test-local scalar handlers may be used to
exercise the foundation, but do not become shipped product operations or
Phase 2 exit evidence.

## 2. Plain-English Packet Intent

EP03 can run a valid workflow in a deterministic order, but the result belongs
only to that dispatch call. EP04 makes an *attempt* inspectable: what workflow
and static contracts were used, what resolved inputs and parameters were
involved, what ran or failed, which result was shared inside the attempt, and
which small local files the attempt owns. It also makes failure information
safe and actionable without presenting a failed or partial result as success.

The proof remains deliberately synthetic. EP05 must separately select and
implement the actual small reference operation family and demonstrate it
through this boundary.

## 3. Governing Inputs and Traceability

Worker and validator must read, in authority order:

1. The explicit 2026-09-24 user approval of this exact packet version.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, 25–30.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants 3–8, 11–14,
   17–18 and the worker-completion attestation rule.
4. `ViDAP_Roadmap.md` v4.2, P2 and checkpoint A2, and
   `ViDAP_Phase_2_Plan.md` v1.5, especially D2.4–D2.8, WS2.4, architecture
   boundaries, test strategy, and P2-AC05–P2-AC08.
5. `ViDAP_P2_EP01_Validation_and_Reconciliation.md`, authoritative for
   accepted D2.1–D2.8, including D2.5's metadata-first Central constraint.
6. `ViDAP_P2_EP02.md` v0.2 and its reconciliation, and `ViDAP_P2_EP03.md`
   v0.1 and its reconciliation; inspect their accepted source/tests and the
   current `vidap_execution` API. Do not infer a product operation from EP03
   tests.
7. Applicable accepted Phase 1 validation/document decisions and Phase 0
   runtime, quality, dependency, fixture, and ignored-state controls.
8. `UX refinement.txt` only as consultative later-phase interaction context;
   it does not provide execution inputs or visual-state authority.
9. This packet.

This packet advances OV §§12, 18–19, 21–22A, 25 and Phase 2 WS2.4. It is
not the Phase 2 reference-workflow proof or closeout.

## 4. Required Contracts and Deliberate Limits

### 4.1 Attempt entry, refusals, and immutable record (D2.1, D2.4)

- Provide one narrow synchronous, in-process attempt entry taking the accepted
  canonical document, registry, explicit static bindings, and first-party
  runtime table. It must use `plan_execution` and the EP03 dispatcher rather
  than reimplementing validation, scheduling, or handler selection. No browser
  state, layout, generated code, dynamic import, process, or network is input.
- Preserve Phase 1/EP02 preparation diagnostics and EP03 planning/whole-table
  preflight refusals as **pre-dispatch refusals**, not fabricated terminal
  attempts. A refusal calls no handler and creates no owned run directory.
  If needed, expose EP03's existing whole-table check as a narrow preflight
  callable; do not duplicate it with different rules. After successful
  preflight and before the first handler, allocate a canonical lowercase
  UUIDv4 attempt ID and produce exactly one immutable terminal record,
  including on runtime failure. UUID collisions refuse; never overwrite an
  existing attempt.
- The record uses a fixed first-party format/revision and includes attempt ID;
  workflow ID and semantic digest; contract snapshot reference; plan,
  binding, and runtime-table revisions; ordered node identities/operation
  keys, resolved parameter values and ordered input content references for
  this controlled scalar boundary; explicit seed value or `null` for absence;
  bounded environment fingerprint; UTC start/end timestamps and elapsed
  duration; attempted/completed/failed/blocked/unrelated node status;
  `succeeded` or `failed` outcome; per-output computed/reused events;
  sanitized diagnostics; publication state; and relative owned artifact
  references. A failed attempt may contain completed prior work but cannot
  be labeled successful or expose failed-node partial output as published.
- Phase 2's persisted parameter values are limited to `null`, booleans,
  signed 64-bit integers, and finite IEEE-754 numbers from the controlled
  scalar proof.
  String, collection, path-like, secret-like, arbitrary-object, and real
  dataset/model values are **not** silently serialized into a durable record;
  refuse this attempt before durable write pending a later approved privacy
  policy. This restriction does not change Phase 1 workflow validity.
  Record incoming values by content reference, never raw preview/data values.
- The environment fingerprint is an explicit, bounded allowlist: Python
  implementation/version, operating-system family and architecture, and
  SHA-256 of the two fixed lock authorities when present. Do not store raw
  environment variables, host/user names, absolute paths, process IDs, or
  arbitrary installed-package dumps. A missing required lock authority is a
  refusal, not an invented fingerprint. The caller cannot supply or override
  the fingerprint. Seed is an explicit optional bounded integer; absence is
  distinguishable from zero. Do not imply that EP03 test handlers use seed.
- Terminal record values and their nested collections are deeply immutable;
  later writes, cleanup, and repeated calls do not mutate a returned record.
  Repeated controlled attempts get distinct IDs and recompute; equal
  semantics need not have equal wall-clock timing or ID.

### 4.2 Managed local artifacts (D2.5)

- The only durable root is the existing ignored repository-local
  `.vidap-local/runs/`. Resolve it from the fixed project checkout, **not** a
  caller-provided root, environment variable, workflow field, or current
  directory. The only per-attempt directory name is its validated UUIDv4.
  Approved fixed slots are `record.json` and an optional small
  `proof-output.bin`. EP04 writes the record; tests may exercise the opaque
  proof slot with synthetic bytes. The proof slot is **not** an approved
  product-output format. EP04 does not persist dispatch outputs by default;
  EP05 must separately approve the meaning, slot, and serialization of a real
  managed output.
- Allocate a new per-ID directory without overwrite. Write each slot to a
  fixed same-directory temporary name, validate record UTF-8/JSON and each
  slot's size, then publish atomically. Limit `record.json` to 256 KiB and
  the optional opaque proof slot to 64 KiB. First publish a bounded `pending`
  ownership record before any handler or proof-slot write. Atomically replace
  only this attempt's own pending record with its immutable `succeeded` or
  `failed` terminal record. A pending record is never success; it lists the
  fixed paths the attempt may own so interrupted or failed attempts remain
  inspectable and explicitly removable. No arbitrary filename, absolute
  artifact reference, unbounded recursive store, database, upload, or hidden
  age-based purge.
  Record artifact references are relative to the owned run directory and
  identify only successfully published slots.
- Reject symlink/junction/reparse traversal and paths escaping the resolved
  checkout-owned root; fail closed if safe containment cannot be established.
  Do not read, overwrite, or delete a pre-existing attempt directory. A
  publication failure produces an in-memory failed outcome and explicit
  publication state; a pending, partial, or missing final record is never
  interpreted as a successful run. Roll back any same-attempt unpublished
  proof slot and staging files when safely possible; retain/report an owned
  pending state if cleanup itself fails rather than silently claiming it
  succeeded.
- Provide bounded explicit removal by validated run ID. It may remove only
  fixed, recorded owned slots (including a safely identified pending
  attempt's slots) and its now-empty per-ID directory after
  containment and ownership checks. Unexpected files, links, missing or
  inconsistent ownership metadata, or an unsafe root cause refusal; do not
  recursively erase or touch another run, the checkout, or caller files.
  No background cleanup, automatic expiry, or default preview/intermediate
  persistence is authorized.

### 4.3 Visible attempt-local reuse (D2.3, D2.6)

- Preserve EP03's one computation per node and one source-port result shared
  by its consumers. A fresh result table and reuse ledger exist only for one
  attempt; no global/persistent lookup, cross-attempt hit, or distinct-node
  common-subexpression shortcut is authorized. Expose per-output `computed`
  and per-consumer `reused-within-attempt` events without calling the latter
  a cross-run cache hit. Failed-node outputs have no events or references.
- Associate each shared output with a versioned composite identity containing
  operation key **and** binding revision, resolved parameters, ordered input
  content references (EP03 edge order), workflow semantic digest, explicit
  seed/absence, and environment fingerprint. Include source node/port
  identity separately so equal semantic keys from distinct nodes never
  silently merge their computations. Use a deterministic canonical JSON
  projection with UTF-16 property ordering as accepted in EP02, then SHA-256;
  never hash `repr`, object identity, absolute path, or visual layout.
- EP04 may derive content references only for bounded canonical JSON scalar
  values used in its synthetic tests, or consume an explicit trusted
  content reference. An arbitrary opaque value with no approved reference
  must refuse reuse rather than invent a hash. A changed operation/binding,
  parameter, ordered input reference, semantic digest, seed, or relevant
  environment component changes the key and requires computation. Repeated
  attempts recompute even when keys match. The ledger describes *actual*
  dispatcher consumption, not a fabricated post-hoc claim of saved work.

### 4.4 Runtime diagnostics (D2.7)

- Map EP03 handler failure, malformed output, and missing required output to
  stable structured envelopes with category/code, attempt ID, affected
  operation/node and port where known, terminal outcome, plain-English
  explanation and concrete remedy, plus bounded sanitized technical type,
  message, traceback, and cause-chain fields. Distinguish artifact/publication
  failure from operation failure. Preserve completed/blocked/unrelated status.
- Never persist or return raw exception text, raw traceback paths, environment
  values, credentials, or arbitrary value `repr`. Safe technical fields may
  use stable templates, validated type identifiers, and module/function-only
  frames/cause types when raw exception content is not provably safe. Limit
  frame/cause counts and string lengths; test malicious exception text,
  absolute user paths, and secrets. A narrow EP03 dispatcher change may
  capture only what is needed for this sanitized bridge; do not change its
  schedule, first-failure rule, or public preflight semantics.
- Phase 1 validation diagnostics remain their original distinct refusal
  path, not a runtime envelope with a guessed attempt ID. No UI copy or
  automatic retry/cancellation promise is part of this packet.

## 5. Required Focused Evidence

Tests must use the real accepted preparation, planner, dispatcher, and new
attempt/artifact paths with test-local deterministic scalar handlers. Prove:

1. Successful linear and branched/joined attempts produce complete immutable
   records, correct workflow/contract/revision/seed/environment references,
   real port results in memory, one upstream computation, and truthful
   computed/reused events. Reordering construction and changing only visual
   metadata do not change semantic keys or dispatch meaning.
2. Invalid workflow, binding, malformed graph, and incomplete runtime table
   refuse before any handler or durable run directory; Phase 1 ordered
   diagnostics survive unchanged.
3. A deterministic handler failure and malformed/missing output yield one
   failed attempt with actionable sanitized envelope, completed work and
   blocked/unrelated distinctions, no later handler, and no failed-node
   partial publication. A nested cause and malicious secret/path-bearing
   exception do not leak into returned or persisted diagnostics.
4. Every composite-key component is varied independently; changed conditions
   cannot reuse stale output. Matching values fan out only within one
   attempt. Distinct nodes and repeated attempts still compute separately.
   Opaque outputs without a trusted content reference refuse reuse.
5. Synthetic owned proof-slot writing, size/format refusal, same-root staging,
   atomic pending-to-terminal publication, collision, partial-write failure,
   symlink/reparse or escape refusal, and explicit recorded-only cleanup. An unexpected file in
   a run directory blocks deletion; another run remains untouched. No test
   leaves `.vidap-local` residue that it created.
6. Terminal deep immutability, missing locks, explicit absent-vs-zero seed,
   no raw environment/absolute path, no default output retention, no
   cross-run cache or product operation. The tests do not claim EP05's real
   reference-workflow proof.

If safe Windows ownership/reparse handling, actual reuse observation, or
sanitized technical context cannot be implemented within Section 7 and the
accepted contracts, stop with a requirement-linked blocker for Central. Do
not quietly weaken D2.4–D2.7 or shift proof to the validator.

## 6. Implementation Constraints

Keep the Phase 1 document/contract/validation APIs and accepted EP02
representation/snapshot/digest unchanged. Preserve EP03 deterministic
planning, explicit static runtime table, ordered inputs, exactly-once node
execution, and fail-stop behavior. This packet may extend `dispatch.py` only
for the minimal observed-consumption/sanitized-cause bridge needed above.
It must not create a second executor, direct-to-handler shortcut, or persistent
cache. No new dependency, manifest/lock edit, workflow/CI change, fixture,
route, service, subprocess, UI, data/ML, export, plugin, or remote mutation.

## 7. Exact Authorized Worker Outputs

Only these ten paths may be created or changed by the approved worker:

| Path | Purpose |
|---|---|
| `python/src/vidap_execution/__init__.py` | Narrow truthful attempt API exports, if needed. |
| `python/src/vidap_execution/dispatch.py` | Minimal actual-consumption/sanitized-cause bridge; preserve EP03 behavior. |
| `python/src/vidap_execution/run.py` | In-process attempt entry, immutable provenance record, outcome/publication boundary. |
| `python/src/vidap_execution/artifacts.py` | Fixed owned root/slots, bounded atomic writes, explicit safe removal. |
| `python/src/vidap_execution/reuse.py` | Attempt-local references, composite keys, and visible reuse ledger. |
| `python/src/vidap_execution/diagnostics.py` | Stable sanitized runtime-error envelopes. |
| `python/tests/test_execution_run.py` | End-to-end synthetic attempt/provenance/refusal/failure evidence. |
| `python/tests/test_execution_artifacts.py` | Owned write, failure, containment, and cleanup challenges. |
| `python/tests/test_execution_reuse_diagnostics.py` | Key invalidation, sharing, and sanitization challenges. |
| `ViDAP_P2_EP04_Implementation_Report.md` | Sanitized worker attestation and validator handoff. |

Existing pre-worker changes belong to their owners; record and preserve them.
Generated ignored `.vidap-local/` state is test output only, not a tracked
worker artifact. No edit to the packet, plan, roadmap, other governing record,
existing EP03 tests, or later-packet file is authorized.

## 8. Worker Sequence and Final Attestation

1. Read Section 3. Confirm exact approval, branch/HEAD, staged/unstaged/
   untracked baseline and ownership, no Section 7 collision, and SHA-256 of
   both lock authorities. Inspect accepted source before designing the seam.
2. Reproduce baseline `npm.cmd run setup` and `npm.cmd run check`. If the
   restricted sandbox denies `uv.exe`, use the documented normal Windows
   execution path; do not bypass TLS checks, unlock dependencies, or switch
   interpreters. A real inability to run the required path is a blocker.
3. Implement only Section 7 paths and run focused tests. Any missing policy
   or out-of-scope correction is a named `Blocked` finding, not an invention.
4. On the **final post-change tree**, run in this exact order:
   `npm.cmd run check`; `npm.cmd run coverage`;
   `npm.cmd run deps:inventory`; `npm.cmd run license:check`;
   `npm.cmd run deps:audit`; `git diff --check`.
   If one fails, repair within scope and rerun the entire ordered sequence,
   or stop with a named blocker. Earlier runs never count as final evidence.
5. Confirm both lock hashes are unchanged. Inspect exact worker file scope,
   all owned `.vidap-local/` test state and cleanup, ignored/generated state,
   whitespace/final newlines, sensitive content, and prescribed-port
   listeners or PID/log residue after smoke. Do not delete user-owned files.
6. In one disposable copy outside the repository and OneDrive, with isolated
   npm and uv caches, reproduce locked setup, the focused EP04 suites, and
   `npm.cmd run check`; verify its managed run state and remove only the
   exact bounded copy/cache paths after validating their resolved targets.
   Verify removal. Report outcomes without user-specific absolute paths.
7. Write the Section 7 report and stop. Do not stage, commit, push, validate
   your own work, accept for Central, or start P2-EP05.

## 9. Required Implementation Report

The report must name this packet/governing versions, approval evidence,
baseline and pre-existing ownership, target commit, exact worker scope and
lock hashes. Map each D2.4–D2.7 contract to source and test evidence; state
the record schema/revision and bounds, fixed root/slots, ownership and
partial-write behavior, immutable terminal state, exact key projection and
invalidation, actual reuse events, technical sanitization policy, and every
deliberate refusal. Distinguish tested synthetic handler control from the
still-unapproved EP05 operation family.

Include the complete final ordered attestation; focused test counts;
disposable-copy setup/tests/check and verified cleanup; ignored-state,
artifact-residue, sensitive-content, whitespace, listener, and file-scope
findings. Cite any relevant source or accepted decision precisely. Report a
failed requirement as `Blocked` or `Revise` with requirement-linked owner,
not as complete. Hand off to a fresh independent validator; Central
acceptance remains separate.

## 10. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP04-AC01 | Exact packet approval, governing prerequisites, baseline/ownership, target commit, and both lock authorities are evidenced. |
| EP04-AC02 | Worker delta is confined to ten Section 7 paths; Phase 1, EP02, EP03 planner contracts, dependencies, locks, CI, fixtures, and prohibited scope are unchanged. |
| EP04-AC03 | The attempt entry follows accepted preparation/planning/dispatch once; pre-dispatch refusals preserve original diagnostics and create no owned run. |
| EP04-AC04 | Every begun attempt has a UUIDv4, deep-immutable terminal record with all bounded D2.4 fields, honest outcome and publication state, and no fabricated seed/environment/input data. |
| EP04-AC05 | Controlled scalar-only persisted parameters and input content references are enforced; unsafe or unsupported values fail closed before durable write. |
| EP04-AC06 | Fixed ignored run root, UUID directory, fixed slots, bounded same-root atomic publication, relative references, collision and containment/reparse refusals, and partial-failure behavior are independently demonstrated. |
| EP04-AC07 | Explicit removal touches only verified recorded owned slots and an empty owned directory; unexpected entries/links refuse and other runs remain untouched. |
| EP04-AC08 | Actual within-attempt sharing yields truthful computed/reused events without cross-run or distinct-node hits; opaque unreferenced output refuses reuse. |
| EP04-AC09 | Versioned composite key includes all D2.6 components, uses canonical deterministic encoding, and each component's change forces computation; visual/layout changes do not. |
| EP04-AC10 | Runtime failures return stable affected-operation/port, plain-English/remedy, and bounded sanitized technical envelope; secrets, paths, raw environment, and object representations do not leak. |
| EP04-AC11 | Handler failure, malformed/missing output, and artifact/publication failure preserve completed/failed/blocked/unrelated states and never publish failed-node partial output as success. |
| EP04-AC12 | Synthetic focused tests exercise the actual accepted engine path and artifact lifecycle; no approved product operation or Phase 2 exit proof is falsely claimed. |
| EP04-AC13 | Final ordered post-change attestation and isolated clean-copy proof pass; locks, ignored-state, cleanup, hygiene, and listener checks are compliant. |
| EP04-AC14 | Worker report is complete, sanitized, traceable, and distinguishes previous evidence, its own work, independent validation, and Central acceptance. |
| EP04-AC15 | A fresh independent validator returns `Accept` with no unresolved Critical or High finding after checking criteria, citations/calculations, architecture, artifact safety, and exact Git/file scope. |
| EP04-AC16 | Central explicitly reconciles and accepts P2-EP04 before P2-EP05 is drafted or authorized. |

## 11. Independent Validation Handoff

The independent validator reads Section 3, the completed report, exact
worker delta and current source, then reproduces the relevant final commands
and focused challenges independently, including key calculation, unsafe
artifact paths, partial writes/cleanup, malicious exception sanitization,
pre-dispatch refusal, and no cross-attempt reuse. Recompute stated hashes and
counts; inspect file scope, accepted contracts, managed residue, and no
later-phase behavior. The validator may create only the bounded ignored
build/test/cache and disposable-copy state necessary for these checks and
must verify its cleanup; this is not permission to edit tracked source,
governing files, locks, or the worker report. Do not repair, push, accept for
Central, or begin EP05. Return `Accept`, `Revise`, or `Blocked` with severity,
requirement link, evidence, and owner. `Accept` satisfies EP04-AC15 only;
EP04-AC16 belongs to Central.

## 12. Fresh-Chat Launch Prompts

### Worker

> Execute the approved `ViDAP_P2_EP04.md` as the bounded run-foundation worker. Read every governing input and follow the packet exactly. Complete the full final attestation and clean-copy proof, then stop with `ViDAP_P2_EP04_Implementation_Report.md` and an independent-validation handoff. Do not validate your own work, accept for Central, alter remote state, or begin P2-EP05.

### Independent validator, only after worker handoff

> Act as the independent validator for `ViDAP_P2_EP04.md`. Read the packet, its governing inputs, accepted EP02/EP03 contracts, and `ViDAP_P2_EP04_Implementation_Report.md`. Verify every acceptance criterion, independent reuse-key and artifact-safety challenges, provenance/error sanitization, citations/calculations, architecture boundaries, locks, and Git/file-scope compliance. You may create and clean only bounded ignored/transient verification state required by the packet; do not edit tracked files or the worker report, accept for Central, alter remote state, or begin P2-EP05. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

## 13. Next Action

P2-EP04 v0.1 is complete. Central may draft P2-EP05 under D2.8; that
reference-operation packet requires separate approval before any worker
execution. Phase 2 completion remains closed pending EP05 and EP06 evidence.
