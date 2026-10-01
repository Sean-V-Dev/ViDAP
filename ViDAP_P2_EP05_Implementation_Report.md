# ViDAP P2-EP05 — Bounded Worker Blocker Report

> Historical v0.1 record. The separately approved v0.2 result follows below.

| Field | Result |
|---|---|
| Packet | `ViDAP_P2_EP05.md` v0.1, explicitly approved 2026-09-25 |
| Governing phase/roadmap | Phase 2 plan v1.7; roadmap v4.4; Spine v1.3 |
| Status | **Blocked before implementation** |
| Worker baseline/target commit | `f2d2b9526888b92094140f36aa191fdb2b8b927e` on `main` |
| Independent validation | Not requested as an implementation-complete handoff |

## Baseline and ownership

Before writing, no files were staged. The pre-existing Central-owned worktree
changes were `ViDAP_Phase_2_Plan.md` and `ViDAP_Roadmap.md`; the approved
`ViDAP_P2_EP05.md` packet was untracked. All were preserved. No Section 8
collision existed. `npm.cmd run setup` passed. The restricted baseline
`npm.cmd run check` stopped at the documented `uv.exe` access denial; its
normal Windows retry passed formatting, lint, typecheck, unit tests (109
passed, one skipped), build, integration tests (three passed), and smoke.
Smoke verified the direct and proxied loopback foundation status.

The lock authorities before and after the investigation are unchanged:

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

## Blocking finding — binding revision contract

Packet §4.1 requires **every static binding registration revision `v1`** and
the **`BindingMap` revision `vidap.reference.bindings.v1`**. The accepted
P2-EP02 preparation contract in
`python/src/vidap_execution/representation.py` lines 338–342 refuses any
node whose `StaticBinding.revision` differs from `BindingMap.revision`, with
`binding-revision-mismatch`. Thus the exact packet-specified binding table
cannot prepare a valid reference workflow. No handler or output-publication
work can produce an accepted run under those simultaneous requirements.

Choosing either revision as a substitute would violate the approved packet.
Changing the accepted representation check is outside the twelve authorized
paths and would revise the P2-EP02 contract. Packet §7 explicitly requires a
`Blocked` stop for a Section 8 collision or a fixture/contract mismatch
requiring a previously accepted contract revision. **Owner: Central.** Central
must resolve and approve the binding-version requirement before bounded
worker execution can resume.

Two initial source files under authorized paths were created during the
seam investigation, then removed after discovering this contradiction. No
implementation source, fixture, README, or governing document remains changed
by the worker. This blocker report is the only worker-created path. No
managed-run directory remains. There was no stage, commit, push, dependency
install beyond locked setup, lock edit, remote change, or EP06 work.

## Attestation and handoff

The final post-change ordered attestation, focused operation suites, fixture
integrity proof, and isolated-copy proof were not run: there is no viable
packet-compliant implementation to attest. This report makes no completion
or independent-validation claim. Once Central resolves the revision conflict
in a newly approved packet, a worker should start from a fresh baseline and
perform the full packet sequence. Independent validation and Central
acceptance remain pending.

---

# P2-EP05 v0.2 — Bounded Worker Implementation Report

| Field | Evidence |
|---|---|
| Authorization/status | `ViDAP_P2_EP05.md` v0.2 explicitly approved 2026-09-25; **Blocked after second independent `Revise`**; prior implementation and checks are historical evidence, not a completion claim |
| Governing versions | Overview; Spine v1.3; roadmap v4.4; Phase 2 plan v1.7; accepted D2.1–D2.8, P2-EP02 v0.2, P2-EP03 v0.1, P2-EP04 v0.1; accepted Phase 1 and D0.6/D0.7 |
| Baseline and target | `main` at `f2d2b9526888b92094140f36aa191fdb2b8b927e` |

## Baseline, ownership, and exact scope

Before v0.2 writing, no path was staged. Central already owned modified
`ViDAP_Phase_2_Plan.md` and `ViDAP_Roadmap.md` and the untracked approved
`ViDAP_P2_EP05.md`. This untracked report held only the historical v0.1
blocker above; it was the authorized exception to the Section 8 collision
gate. No other Section 8 collision existed. Baseline locked setup passed.
The first restricted baseline check stopped on the documented `uv.exe` access
denial; its normal Windows retry passed formatting, lint, types, 109 Python
unit tests with one host-dependent skip, build, three integration tests, and
smoke. The v0.1 revision contradiction is resolved by v0.2's exact equality.

The worker changed only the twelve Section 8 paths: `README.md`, this report,
`python/src/vidap_execution/{__init__.py,reference.py,run.py,artifacts.py,output.py}`,
two `python/tests/test_execution_reference*.py` files, and three
`fixtures/p2-ep05/` files. The pre-existing Central changes were preserved.
No governing, Phase 1, EP02/EP03, dependency, lock, CI, service, UI, existing
fixture, or remote state changed. No stage, commit, push, or EP06 work occurred.

| Lock | Unchanged baseline/final SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

## Contract and source mapping

`reference.py` supplies a separate immutable `REFERENCE_REGISTRY`, fixed
`BindingMap`, runtime table, and exactly four first-party handlers. Literal
requires integer `value`, has no input, and emits it. Multiply requires one
`input` and integer `factor`, then checks its product. Add requires exactly
one `left` and one `right`, then checks their sum. Emit requires one `input`,
returns it unchanged, and does no I/O. All use the exact matching
`vidap.reference.*` node type and operation key, required `artifact` ports,
and `vidap.reference.bindings.v1` for every static binding, runtime
registration, and binding map. The runtime table keeps accepted
`vidap.runtime-table/1.0`. Accepted preparation/preflight pass; an unequal
binding or runtime registration refuses. The Phase 1 `artifact` token is an
opaque carrier only; each handler separately checks exact port cardinality,
`type(value) is int` (excluding bool), and inclusive signed 64-bit range.
Overflow raises `OverflowError` at the accepted handler boundary.

`run_reference_attempt` calls accepted `run_attempt` once with those fixed
authorities. The narrow `run.py` bridge refuses reference publication unless
the supplied registry, binding map, and runtime table are those exact
first-party objects; its `output.py` policy uses the static emit key
to demand exactly one terminal emit before attempt allocation. It selects
that node's `value` only after successful dispatch. `output.py` produces
compact, BOM-free, newline-free UTF-8 JSON with fixed UTF-16-ordered keys.
Exact successful bytes are
`{"format":"vidap.reference-scalar","schemaVersion":"1.0","value":15}`;
SHA-256 is
`53B600435D2936FA8D06EB0DB22E176676ABB8D75070B426AE909A91C9F6F2D6`.
The inherited 64 KiB `proof-output.bin` slot is written under EP04 pending
ownership before atomic terminal publication. Only a successful record may
reference it alongside `record.json`. The generic EP04 entry retains its
default no-output behavior. Operation failure writes no proof. Missing/wrong
emit value, serialization/write failure, or terminal-publication failure is
sanitized as `publication-failed`, cannot return success, and rolls back only
this attempt's unpublished slots where safe. If a terminal record reaches disk
before publication raises, the reference-only recovery rewrites that same
pinned attempt to metadata-only pending ownership before deleting the proof.
Even if proof cleanup then fails, the durable record has no success state or
output reference; explicit ID-based removal can inspect and clean it. No
workflow field or caller selects a path, serializer, slot, or executable.
There is no general numeric type, data intake, preview, cross-run cache,
workflow API, UI, export, or intermediate retention.

## Fixture bytes and real results

| New fixture file | Bytes | SHA-256 |
|---|---:|---|
| `branched-success-v1.json` | 1,780 | `F2079F1A4BDADB073792BD19A26B43F2D5F7A8F5B81781715D180B95B78687D1` |
| `checked-overflow-v1.json` | 1,362 | `06F04CFF6D8F2642AADF28784C96AEF04DE4E41EAAD005F2079D6EEA695E7ED1` |
| `fixture-manifest.json` | 2,275 | `75B6584102E96E25DB9036445C91CFC16989D07502015596A98134A12870F49B` |

The new set totals 5,417 bytes; all root `fixtures/` files total 13,225
bytes. Each new file is below 16 KiB, has a final newline, and is synthetic
UTF-8 material. The manifest records manual creation, MIT terms, expected
properties, limited consumers, explicit `synthetic non-sensitive` privacy
classification and attestation, byte hashes/sizes, and Central's
fixed-design approval date. Its byte-level review status remains pending
independent validation and Central reconciliation.

The strict deserializer loaded both actual fixture files. Branched success
scheduled and called literal 1, multiply 2, multiply 3, add 4, emit 5.
It calculated `3×2 + 3×3 = 15`: five completed nodes, five `computed`
events, and five actual edge-consumption `reused-within-attempt` events.
The literal computed once and fed both branches. Semantic digest:
`c3f29ed610cde6875c6c6ed7c3c69b93945290798356eafc8c11576957f4c3f0`.
Its terminal record succeeded with only `record.json` and the exact proof
bytes. The attempt was explicitly cleaned by validated ID. The separate
linear workflow computed `4×5=20`; reversed node/edge collections and
label/layout edits preserved schedule, digest, value, and output bytes.
Reversed registry/binding construction prepared and preflighted identically.

Overflow scheduled/attempted literals 1 and 2, then add 3. The add raised
on `9223372036854775807 + 1`; emit 4 was blocked and independent literal 5
unrelated/unstarted. The record has two completed, one failed, one blocked,
one unrelated; outcome `failed`, code `handler-failed`, technical type
`OverflowError`, and no proof slot. Semantic digest:
`0eb20af691842c2de3343ed08fdda5a1babcae6b68eb1cf5bbcd0235499b88bf`.
It too was removed by validated ID. Focused challenges cover signed minimum,
multiply overflow, bool/non-integer and cardinality refusal, missing/multiple/
nonterminal emit, malformed/unsupported fields, changed literal/factor,
repeats, and unequal revisions. Repeated runs get distinct attempt IDs/times,
recompute real handlers, keep equal semantic keys and bytes, and record no
cross-run hit. Changed semantic inputs yield changed digest and result.
Forced proof-write, partial-write, pre-write terminal failure, post-write
terminal failure, and post-write cleanup failure remain failed, roll back
same-attempt proof when possible, preserve inspectable pending ownership
without a success-looking output reference, and preserve another run.
Existing EP04 Windows directory-swap/recorded-only cleanup tests passed;
one symlink-creation challenge remained host-dependent and skipped.

## Final attestation, clean copy, and hygiene

The first post-repair `check` attempt stopped on an intermittent `OSError`
while an existing run test removed its owned directory. That exact test
passed alone; the complete `check` then passed. The stopped attempt is not
counted as final evidence. The following complete ordered sequence passed.

On the final implementation tree, required checks passed in order:
`npm.cmd run check` (122 Python unit tests passed, one host-dependent skip,
three integration tests, build, smoke, formatting/lint/types);
`npm.cmd run coverage` (125 Python tests passed, one skipped; 88% aggregate
Python coverage); `npm.cmd run deps:inventory`; `npm.cmd run license:check`
(431 locked installed packages classified); `npm.cmd run deps:audit` (zero
reported npm/Python vulnerabilities); `git diff --check` (clean). Both
focused EP05 suites passed all 13 tests. Locks are unchanged; fixture bytes,
aggregate, final newlines, and manifest integrity match the table. Only the
twelve worker paths changed alongside separately owned baseline paths.
Generated build, coverage, environment, and run state are ignored. No managed
attempt remains, no prescribed-port listener or PID/log residue was found
after smoke, and verified README links are repository-relative. New
source/fixtures contain no user-specific path or sensitive value.

In a disposable copy outside the repository and OneDrive with isolated npm
and uv caches, locked setup passed, all 13 focused EP05 tests passed, both
fixture hashes/sizes and expected outcomes were checked, and full
`npm.cmd run check` passed. The copy contained 148 current source files.
The exact copy/cache target was verified as a child of the system temporary
directory before bounded removal; absence was verified afterward.

## Response to independent `Revise`

The validator identified a High EP05-AC11/AC16 case where a terminal write
succeeded on disk and then raised, leaving a success record while the caller
returned failure. The reference-only `restore_reference_pending` repair above
and real owned-file fault tests address that case, including a second failure
while removing proof bytes. The validator also identified a Medium EP05-AC12
missing privacy classification. Both manifest entries now declare
`synthetic non-sensitive`; their new manifest size and digest are recorded
above. These are worker repairs, not independent acceptance.

## Independent-validation handoff

Please independently inspect the exact v0.2 packet and governing inputs,
this twelve-path delta, real code/fixtures, and this report. Recalculate 15,
20, overflow/status, reuse keys, fixture and output hashes, ownership failures,
locks, scope, and clean-copy proof; return `Accept`, `Revise`, or `Blocked`
with severity, requirement, evidence, and owner. This worker does not
independently validate or accept its own result. Central byte-level fixture
review, P2-EP05 acceptance, EP06, and Phase 2 closeout remain pending.

## Superseding blocker after second independent `Revise`

**Status: Blocked. Owner: Central for the contract decision; worker for any
subsequently authorized repair.** The second independent validator reproduced
EP05-AC02/AC11/AC16 failure by making terminal publication write the success
record and then raise, followed by a failure while restoring `record.json`.
`run.py` returned `failed-cleanup-incomplete`, but the durable record still
said `succeeded` and referenced `proof-output.bin`. The validator removed the
generated attempt by validated ID. The first repair's test covered failure
while deleting proof after metadata restoration; it did not cover failure of
the metadata restoration itself. Its claim above that post-publication
failure cannot leave a success-looking record is therefore superseded.

The added `restore_reference_pending` also changes an already published
terminal record back to `pending`. Accepted D2.4 and P2-EP04 require terminal
records to be immutable and allow only pending-to-terminal replacement.
Changing that rule is outside P2-EP05 authority. Conversely, if the terminal
write has committed and a later error prevents reliable readback, the worker
cannot truthfully classify the durable attempt as failed while guaranteeing
that no successful record exists. The packet's publication requirement and
the accepted immutable-terminal contract need Central resolution before
another implementation decision. No further source, fixture, dependency,
lock, or governing change was made in response to this second verdict.

The previous Medium EP05-AC12 finding is resolved: both manifest entries
explicitly classify privacy. The validator reported that calculations,
fixtures, managed bytes, locks, scope, focused tests, ordered checks,
disposable-copy proof, cleanup, and listener checks passed. Those passes do
not resolve this High contract blocker. The earlier independent-validation
handoff and implementation-complete language above are historical and must
not be used as an acceptance request. Central must resolve the uncertain
post-commit publication contract in a newly approved correction before the
worker can safely revise and reattest. P2-EP05 acceptance and EP06 remain
closed.

---

# P2-EP05 v0.3 — Bounded Publication Repair and Worker Handoff

| Field | Evidence |
|---|---|
| Authorization/status | `ViDAP_P2_EP05.md` v0.3 explicitly approved 2026-09-25; bounded repair implemented and locally attested; fresh independent validation pending |
| Governing versions | Overview; Spine v1.3; roadmap v4.4; Phase 2 plan v1.7; accepted D2.1–D2.8, P2-EP02 v0.2, P2-EP03 v0.1, P2-EP04 v0.1, Phase 1 D1.2–D1.7, and D0.6/D0.7 |
| Baseline/target | `main` at `f2d2b9526888b92094140f36aa191fdb2b8b927e`; no staged paths |
| Historical disposition | The v0.1 binding blocker and both v0.2 independent `Revise` findings remain above; their earlier completion and handoff claims are superseded |

## Ownership and exact scope

Before v0.3 writing, the two modified planning paths and untracked approved
packet were Central-owned. The twelve Section 8 paths contained the v0.2
worker implementation and report; the retained report was the packet's
authorized historical exception. Locked baseline `npm.cmd run setup` and
`npm.cmd run check` passed. This repair changed only `run.py`, `artifacts.py`,
the focused reference-output test, and this report, all within the same twelve
authorized worker paths. The other worker paths preserve the v0.2 reference
proof. No Phase 1, EP02/EP03, generic EP04 key/error or Windows safety source,
dependency, lock, CI, service, UI, existing fixture, governing plan, remote,
or EP06 work was changed. Nothing was staged, committed, or pushed.

| Lock authority | Baseline and final SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

## Reference and publication contract

The unchanged first-party `reference.py` registry has exactly literal,
multiply, add, and emit operations with matching
`vidap.reference.bindings.v1` static/map/runtime binding revisions and the
accepted runtime-table revision. Phase 1's nominal `artifact` port token is
only an opaque carrier here; the four pure handlers separately check exact
input cardinality, `type(value) is int`, and signed 64-bit bounds. Literal
returns the declared integer, multiply checks its product, add checks its
sum, and emit returns its input without I/O. The fixed reference entry calls
accepted validation, representation, planning, preflight, dispatch, and the
EP04 attempt layer once. Exactly one terminal emit is required before
allocation. No document or caller chooses code, a serializer, output path, or
slot. Generic `run_attempt` retains its default no-output behavior.

`output.py` still selects the completed emit's value and emits the exact
compact UTF-8, UTF-16-key-ordered `vidap.reference-scalar`/`1.0` envelope.
For value 15, the 68 bytes are
`{"format":"vidap.reference-scalar","schemaVersion":"1.0","value":15}`;
SHA-256 is
`53B600435D2936FA8D06EB0DB22E176676ABB8D75070B426AE909A91C9F6F2D6`.
They enter only the inherited bounded `proof-output.bin` owned slot before
the immutable terminal record. No intermediate output, preview, or cross-run
cache is stored.

The v0.2 `restore_reference_pending` terminal rewrite is removed.
`artifacts.py` now supplies a read-only, pinned, reparse-checked inspection
of the exact canonical record bytes and the exact bounded proof bytes. If
terminal publication raises after commit, `run.py` returns the verified
immutable terminal outcome, successful or failed, without rewriting or
deleting either slot. If readback instead verifies the original pending
record and expected proof, it rolls back only this attempt's unpublished
slots and returns a sanitized publication failure. A rollback error is
reported as cleanup incomplete with pending ownership intact. If readback
fails or either fixed slot differs, `PublicationIndeterminate` raises with
only the validated attempt ID; it returns no success/failure `AttemptResult`,
does not retry or alter the owned attempt, and leaves recorded-ID-only
inspection/removal available. It is not a durable terminal state.

## Real workflows and negative challenges

The strict deserializer reads the two unchanged synthetic fixtures. The
branched graph schedules literal 1, multiplies 2 and 3, add 4, emit 5;
`3×2 + 3×3 = 15`. Five real handlers complete and five edge consumptions
reuse produced values, with the literal computed once. The successful owned
directory contains only `record.json` and the 68-byte proof above; its
semantic digest is
`c3f29ed610cde6875c6c6ed7c3c69b93945290798356eafc8c11576957f4c3f0`.
The separate linear graph computes `4×5 = 20`; reversed construction and
layout/label changes preserve semantic meaning and bytes. Repeated runs have
distinct attempt IDs and timing but recompute the handlers and yield equal
bytes. Changed literal or factor changes the digest/key and result, with no
cross-run hit. The overflow graph attempts literal 1, literal 2, add 3;
`9223372036854775807 + 1` raises `OverflowError`. Emit 4 is blocked,
independent literal 5 unrelated, outcome `failed`, code `handler-failed`,
and no proof slot; its semantic digest is
`0eb20af691842c2de3343ed08fdda5a1babcae6b68eb1cf5bbcd0235499b88bf`.
The retained v0.2 focused tests also cover signed minimum, multiply overflow,
bool and non-integer refusal, cardinality, invalid/reordered graphs, unequal
revisions, changed semantics, and owned-slot overwrite refusal.

The v0.3 focused tests force proof-write failure, pre-commit terminal error,
post-commit acknowledgement error for both successful and failed arithmetic,
readback I/O error, mismatched proof readback, and rollback failure while
still pending. They verify immutable committed slots, sanitized indeterminate
errors without private text, pending ownership and cleanup-incomplete
reporting, preservation of another attempt, and validated-ID cleanup. EP04's
existing Windows directory-swap and recorded-only cleanup tests passed; the
one host-dependent live-symlink test remained skipped.

| New fixture | Bytes | SHA-256 |
|---|---:|---|
| `branched-success-v1.json` | 1,780 | `F2079F1A4BDADB073792BD19A26B43F2D5F7A8F5B81781715D180B95B78687D1` |
| `checked-overflow-v1.json` | 1,362 | `06F04CFF6D8F2642AADF28784C96AEF04DE4E41EAAD005F2079D6EEA695E7ED1` |
| `fixture-manifest.json` | 2,275 | `75B6584102E96E25DB9036445C91CFC16989D07502015596A98134A12870F49B` |

The new fixture set totals 5,417 bytes; all root fixtures total 13,225 bytes.
Each new file is UTF-8 with a final newline and below 16 KiB. The manifest
records synthetic manual provenance, MIT terms, expected results, permitted
consumers, explicit `synthetic non-sensitive` classification, privacy
attestation, integrity metadata, and Central's design-approval date while
leaving byte-level review pending.

## Final attestation and clean-copy proof

On the final source tree, the required ordered sequence passed:
`npm.cmd run check` (125 Python unit tests passed, one host-dependent skip,
three integration tests, build, smoke, formatting/lint/types);
`npm.cmd run coverage` (128 Python tests passed, one skipped; 88% aggregate
Python coverage); `npm.cmd run deps:inventory`; `npm.cmd run license:check`
(431 locked installed packages classified); `npm.cmd run deps:audit` (zero
reported npm/Python vulnerabilities); and `git diff --check` (clean). All
16 focused EP05 tests passed. Lock hashes match the table, fixture
hashes/sizes and final newlines match, and the twelve-path worker scope is
unchanged alongside separately owned Central planning paths. Generated state
is ignored, no managed attempt remains, and no prescribed-port listener or
root PID/log residue remains after smoke. README links and current-state
claims remain valid; new source and fixtures contain no user-specific path or
sensitive value.

A disposable copy outside the repository and OneDrive, with separate npm and
uv caches, passed locked setup, all 16 focused EP05 tests, fixture byte
hash/size and expected-outcome checks, and full `npm.cmd run check`. The copy
contained 150 current tracked/untracked repository paths. The exact copy and
cache targets were verified within the system temporary directory before
bounded removal; both were verified absent afterward.

## Independent-validation handoff

This is worker evidence, not independent validation or Central acceptance.
Please independently inspect v0.3's commit-point classification, exact
readback and immutable terminal behavior, including post-commit error,
readback failure, and pending rollback failure, along with the retained
reference calculations, fixtures, keys, scope, locks, and final checks.
Central byte-level fixture review, EP05 acceptance, EP06, and Phase 2
closeout remain pending.
