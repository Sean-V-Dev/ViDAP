# ViDAP P2-EP06 — Phase 2 Evidence Closeout and Reconciliation Handoff

| Field | Value |
|---|---|
| Status | Complete — independently validated and centrally accepted; Phase 2 reconciled |
| Packet version | 0.1 |
| Packet type | Bounded Phase 2 evidence reproduction and reconciliation handoff |
| Parent phase plan at authorization | `ViDAP_Phase_2_Plan.md` version 1.7, WS2.6 and P2-AC01–P2-AC12 |
| Parent roadmap at authorization | `ViDAP_Roadmap.md` version 4.4, P2/checkpoint A2 |
| Prerequisites | P2-EP01 through P2-EP05 independently validated and centrally reconciled |
| Authorized worker report | `ViDAP_P2_EP06_Implementation_Report.md` |
| Created | 2026-09-25 |
| Approved | 2026-09-25 by explicit user direction |
| Completed | 2026-10-01 in `ViDAP_P2_EP06_Validation_and_Reconciliation.md` |
| Owner | Central |

---

## 1. Authorization Boundary

The user explicitly approved this exact v0.1 packet on 2026-09-25,
authorizing one fresh closeout worker run. The worker may create or modify
only the Section 7 report. The
worker must not repair implementation, change a fixture or governing record,
accept Phase 2, or begin Phase 3 planning. A separate independent validator
then checks the report and current behavior. Only Central may reconcile
P2-AC12 and mark Phase 2 complete.

Existing quality commands may create ignored build, environment, coverage,
cache, and test-run state. The worker may create one bounded disposable copy
and isolated caches outside the repository and OneDrive. It must validate
their exact resolved targets before cleanup, remove only what it created, and
verify their absence. It may remove test attempts only by validated attempt
ID under the accepted recorded-ownership contract. No broad deletion of
`.vidap-local`, user data, or another attempt is authorized.

## 2. Plain-English Packet Intent

This is the whole-phase evidence check, not another feature packet. It asks
whether the accepted decisions and EP02–EP05 implementation together prove
the Phase 2 promise: a validated workflow runs headlessly in dependency
order, real reference operations produce the expected result, branch sharing
and failure are predictable, run evidence is inspectable, and owned output
cannot be mistaken for a successful result after an uncertain publication.

The worker must distinguish that proof from the product capabilities still
deferred. Phase 2 supplies an engine foundation and one deliberately small
scalar reference family; it does not supply a visual editor, workflow HTTP
API, user data pipeline, model training, experiment comparison UI, notebook
export, or persistent cross-run cache.

## 3. Governing Inputs and Traceability

Worker and validator must read:

1. The explicit 2026-09-25 user approval of this exact v0.1 packet version.
2. `ViDAP_Overview.txt`, especially OV §§12, 16–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` v1.3, especially invariants, Phase 2 exit
   evidence, worker-completion attestation, readiness/completion gates, and
   the Phase 3 boundary.
4. `ViDAP_Roadmap.md` v4.4, P2/checkpoint A2 and P3 entry gate, and
   `ViDAP_Phase_2_Plan.md` v1.7, especially D2.1–D2.8, WS2.1–WS2.6,
   architecture boundaries, P2-AC01–P2-AC12, and completion/transition.
5. `ViDAP_P1_EP06_Validation_and_Reconciliation.md` and the accepted Phase 1
   canonical workflow/contract/validation limits.
6. Every P2-EP01 through P2-EP05 packet, worker report, and
   validation/reconciliation record. Reconciliation records govern accepted
   outcomes; historical v0.1/v0.2 EP05 blockers and earlier worker handoff
   claims do not override the accepted v0.3 result.
7. Current execution source/tests; both controlled fixture families and their
   manifests; package tasks, lock authorities, dependency/license/audit
   controls, CI configuration, ignore/attribute policy, and README.
8. This packet.

The packet advances OV §§12, 18–19, 21–22A, and 25 by closing the accepted
Phase 2 proof. It does not select Phase 3 UI/design, Phase 4 data ownership,
Phase 5 modeling, Phase 6 experiment UX, or Phase 7 export policy.

## 4. Whole-Phase Reconciliation Contract

The worker must make no new architecture or policy choice. Its report must
trace each P2-AC01–P2-AC12 to accepted decisions, current implementation,
direct reproduction, and any limitation:

1. D2.1–D2.8 are accepted in P2-EP01. The initial engine is a bounded
   synchronous in-process entry, not a persistent service; validated
   canonical meaning is converted once to an immutable layout-independent
   representation with a contract snapshot reference and semantic digest.
2. Accepted static bindings and the deterministic smallest-ready-ID planner
   dispatch only known first-party handlers. Shared upstream values are
   computed once per attempt and fanned to branches; failures stop safely and
   distinguish completed, failed, blocked, and unrelated nodes. Creation
   order and visual layout are not runtime inputs.
3. Attempts retain immutable terminal records with bounded provenance,
   explicit seed or absence, environment fingerprint, node/reuse events,
   outcome, sanitized diagnostics, and relative owned artifact references.
   The only approved durable result beyond metadata is the exact bounded
   reference-scalar proof in the fixed slot. There is no default preview or
   intermediate retention and no persistent cross-run cache.
4. A proof write or pre-commit terminal failure cannot look successful. A
   post-commit acknowledgement error may return success only after exact
   durable record/output readback. Unverifiable publication raises sanitized
   `PublicationIndeterminate` without a false terminal result, retry,
   terminal rewrite, or unsafe deletion. Explicit cleanup remains bounded
   to validated recorded ownership.
5. The actual EP05 branch/join fixture computes `3×2 + 3×3 = 15` through
   the shipped handlers, with one upstream computation, five edge
   consumptions, and the approved 68-byte scalar envelope. The overflow
   fixture fails at maximum signed 64-bit integer plus 1; emit is blocked,
   independent work is unrelated, and no proof output is published. Repeat,
   changed-input/parameter, invalid-workflow, and layout/order cases show
   deterministic semantics and visible attempt-local reuse/invalidation.
6. No visual workflow editor or run controls, workflow API, user dataset,
   profiling/preparation, model training/evaluation, experiment comparison,
   notebook/Python export, plugin/arbitrary code loading, distributed/cloud
   execution, or other Phase 3+ capability is claimed or introduced.

The report must preserve the difference between accepted historical evidence
and evidence reproduced on the current target. It must explicitly mark
P2-AC12 **pending independent validation and Central reconciliation**; a
worker cannot declare the phase complete.

## 5. Required Worker Evidence and Final Checks

1. Before writing, record branch, `HEAD`, staged/unstaged/untracked baseline,
   ownership of pre-existing paths, exact lock hashes, current task/CI
   identity, and the P2 packet/reconciliation chain. The target is the
   current working-tree snapshot, including accepted but not-yet-committed
   EP05 files; a commit-only checkout or previously validated snapshot cannot
   substitute for it. Do not classify pre-existing EP05 or Central planning
   changes as EP06 worker output.
2. Build a P2-AC01–P2-AC12 traceability matrix. For each criterion cite the
   governing decision and accepted packet/reconciliation, relevant current
   source/test/fixture evidence, current reproduction, result, and limitation.
   A missing link is a named blocker, not an inferred pass.
3. Inspect the public Phase 2 entry, representation/snapshot, planner,
   dispatch, run/reuse/diagnostics, owned artifacts, reference handlers, and
   output serializer. Challenge real valid/invalid and reordered workflows,
   branch/join and overflow behavior, changed semantic input/parameter,
   repeat-run identity and bytes, bounded provenance, and publication
   pre-commit/post-commit/indeterminate handling. Use existing controlled
   tests or bounded transient probes; do not edit tracked files or fabricate
   a result from fixture expectations. Verify exact EP05 fixture bytes and
   manifest against their Central byte-level reconciliation.
4. Run locked `npm.cmd run setup`, then on the final current target run this
   full attestation in order: `npm.cmd run check`;
   `npm.cmd run coverage`; `npm.cmd run deps:inventory`;
   `npm.cmd run license:check`; `npm.cmd run deps:audit`;
   `git diff --check`. Record each result, lock hashes before/after, and the
   actual test counts/skips. If any check fails, stop with a requirement-
   linked blocker; this evidence-only packet does not authorize repair.
   The documented normal Windows execution path may be used if a restricted
   sandbox denies `uv.exe`; do not bypass TLS, change interpreter/dependency
   policy, or claim a failed restricted run is a pass. This documentation-only
   closeout does not require a new hosted CI run or authorize a push.
5. In one clean disposable copy outside the checkout and OneDrive, include
   the exact current relevant source, tests, fixtures, manifests, package
   files, locks, and configuration from the target working tree, including
   accepted untracked EP05 paths. Use isolated npm/uv caches. Run locked
   setup, the focused Phase 2 Python execution suites with
   `uv --directory python run --locked pytest tests/test_execution_representation.py tests/test_execution_planner.py tests/test_execution_dispatch.py tests/test_execution_run.py tests/test_execution_artifacts.py tests/test_execution_reuse_diagnostics.py tests/test_execution_app.py tests/test_execution_reference.py tests/test_execution_reference_output.py`,
   fixture-integrity checks, and `npm.cmd run check`. Record the copy's
   source-snapshot identity and results. Validate the resolved exact copy
   and cache paths are inside the designated temporary root before removal;
   remove only those paths and verify absence. Do not use a repository or
   OneDrive path as the temporary root.
6. Verify both locks unchanged; EP05/P1 fixture sizes and hashes; generated
   state ignored; no unowned `.vidap-local` attempt, prescribed-port listener,
   harness PID/log residue, sensitive/user-path leakage, broken README link,
   alternate lock, dependency drift, unauthorized file, or later-phase
   behavior. Clean only attempts and temporary state created by this worker
   under their approved ownership rules.
7. Write only the Section 7 report, then recheck its text hygiene and final
   Git scope. `git diff --check` does not cover an untracked report, so inspect
   that report directly for whitespace, final newline, user paths, and
   sensitive content. Stop. Do not stage, commit, push,
   dispatch hosted CI, self-validate, create the Central reconciliation, or
   begin Phase 3 planning.

## 6. Worker Completion Attestation and Stop Conditions

The report may request independent validation only after all Section 5
checks pass against the final target and exact copied snapshot. It must name
the full command sequence and its outcomes, focused tests and direct
challenges, before/after lock hashes, fixture integrity, ignored-state and
listener checks, temporary-copy/cache cleanup, and the sole-report scope.
This is worker evidence, never an independent verdict or Central acceptance.

Stop `Blocked` or `Revise` with requirement, evidence, and owner if a
prerequisite is missing, the current working tree cannot be faithfully
copied, a required check/challenge fails, an accepted contract conflicts with
current behavior, a cleanup target cannot be proved safe, or a finding needs
any source/fixture/dependency/governing repair. Do not broaden the packet or
ask the validator to finish worker checks. A later repair requires separate
Central authorization and a fresh final attestation.

## 7. Exact Authorized Repository Output

| Path | Purpose |
|---|---|
| `ViDAP_P2_EP06_Implementation_Report.md` | Sanitized whole-phase traceability, reproduction, limitations, scope, and independent-validation handoff. |

No other tracked or untracked repository file may be created, modified,
moved, staged, committed, or deleted by the worker. Expected ignored command
output is temporary, not an authorized product change. The report must not
contain user-specific absolute paths, credentials, raw environment values,
full lockfiles, or copied command logs. Preserve pre-existing dirty/untracked
paths by owner, including the EP05 worker artifacts and Central planning and
reconciliation documents.

## 8. Explicit Prohibited Scope

No implementation, tests, fixtures, manifests, README, packet, phase plan,
roadmap, spine, decision record, lock, dependency, CI, workflow, API, UI,
data/model, export, or remote change is authorized. Do not start a persistent
application/service except the existing bounded quality/smoke check. Do not
make a new D2 decision, reinterpret Phase 1 schema, weaken terminal
immutability, change accepted EP05 output bytes, remove another attempt, or
begin P3 planning/implementation. The worker and validator may not accept
P2-EP06 or Phase 2 on Central's behalf.

## 9. Required Worker Report

The report must include: exact packet approval/version and authority chain;
baseline/target snapshot and pre-existing ownership; a P2-AC01–P2-AC12
matrix with source/test/reconciliation citations and direct evidence; D2.1–
D2.8 map and accepted limits; actual reference calculations, fixture and
managed-output hashes, run/provenance/reuse/artifact/error behavior; negative
and publication-fault evidence; all final commands and clean-copy/cleanup
results; lock/scope/hygiene/ignored-state/listener findings; explicit Phase 3
handoff inputs and still-open UI/data/model/export choices; and a worker
self-assessment that leaves independent validation and Central P2-AC12
reconciliation pending. Avoid copied command logs or user-specific paths.

## 10. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP06-AC01 | Exact packet approval, accepted EP01–EP05 prerequisites, target working-tree snapshot, pre-existing ownership, sole-report scope, and both lock authorities are accurately evidenced. |
| EP06-AC02 | D2.1–D2.8, their alternatives/constraints, and EP01–EP05 reconciliations are faithfully traced without new policy or silent scope expansion. |
| EP06-AC03 | Current direct evidence supports P2-AC02–P2-AC04: strict Phase 1 handoff, layout-independent representation, static bindings, deterministic real dispatch, branch sharing, and predictable refusal/failure. |
| EP06-AC04 | Current direct evidence supports P2-AC05–P2-AC08: bounded immutable run provenance, exact owned scalar output, visible attempt-local reuse/invalidation, sanitized runtime errors, safe publication classification, and recorded-only cleanup. |
| EP06-AC05 | Current direct evidence supports P2-AC09: accepted fixture bytes and real values/statuses, repeat and changed-semantic behavior, invalid graph and publication-fault challenges; no fabricated execution proof. |
| EP06-AC06 | P2-AC10 exclusions and A2 separation hold: no unapproved Phase 3+ product behavior, service, untrusted code loading, broad data/model persistence, cross-run cache, or UI authority. |
| EP06-AC07 | P2-AC11 controls remain current: quality, coverage, dependency/license/advisory, fixtures, owned artifacts, documentation, locks, hygiene, and generated-state policy. |
| EP06-AC08 | Locked setup, complete final attestation, direct/focused challenges, and faithful disposable-copy proof pass with unchanged locks, verified bounded cleanup, and honest skips/limitations. |
| EP06-AC09 | The worker changes only the Section 7 report and makes no unauthorized repository, system, remote, or later-phase change. |
| EP06-AC10 | The report is sanitized, reproducible, criterion-linked, accurate about historical versus current evidence, and does not claim independent validation or Central acceptance. |
| EP06-AC11 | Fresh independent validation returns `Accept` with no unresolved Critical or High finding and recommends whether P2-AC12 is ready for Central reconciliation. |
| EP06-AC12 | Central separately accepts P2-EP06 and reconciles P2-AC01–P2-AC12 before marking Phase 2 complete or opening detailed Phase 3 planning. |

## 11. Independent Validation Contract

A fresh independent validator must read Section 3, the worker report, actual
target snapshot, source/tests/fixtures, and acceptance criteria. It must
independently verify P2-AC01–P2-AC12 traceability and D2.1–D2.8 fidelity;
challenge real workflow execution, semantic/layout invariance, run/reuse
provenance, branch/failure statuses, owned output bytes, and all three
publication/readback classifications, including an injected post-commit
readback failure. It must recompute fixture and output bytes/hashes and lock
hashes, inspect the absence of prohibited/later-phase behavior, reproduce
the complete final attestation and a separate bounded clean-copy proof, and
verify cleanup and file scope. It may create only ignored/transient test
state and its own bounded temporary copy/cache, with exact-target cleanup.
It may not modify tracked files, repair defects, alter remote state, accept
for Central, write a reconciliation record, or begin Phase 3 planning.

Return `Accept`, `Revise`, or `Blocked` with requirement-linked severity,
evidence, owner, and an explicit recommendation on Central's P2-AC12
reconciliation. A validator `Accept` satisfies EP06-AC11 only; Central owns
EP06-AC12 and the Phase 2 completion decision.

## 12. Fresh-Chat Launch Prompts

### Worker

> Execute approved `ViDAP_P2_EP06.md` v0.1 as the bounded Phase 2 closeout-evidence worker. Read every governing input and accepted P2-EP01–EP05 packet, report, and reconciliation. Follow the packet exactly; create or modify only `ViDAP_P2_EP06_Implementation_Report.md`. Trace P2-AC01–P2-AC12 to accepted decisions and current direct evidence, including real reference runs and uncertain-publication safety. Run the complete final attestation and one faithful disposable-copy proof, including accepted untracked EP05 files, with bounded cleanup. Stop with a sanitized report and independent-validation handoff, or a named blocker. Do not repair source or fixtures, self-validate, accept for Central, stage/commit/push, alter remote state, or begin Phase 3 planning.

### Independent validator — only after worker handoff

> Act as the independent validator for approved `ViDAP_P2_EP06.md` v0.1. Read all governing inputs, accepted P2-EP01–EP05 evidence, and `ViDAP_P2_EP06_Implementation_Report.md`. Independently check every P2-AC and EP06-AC criterion, decision and architecture fidelity, actual reference computations, fixture/output hashes, publication/cleanup fault behavior, exclusions, locks, and Git/file scope. Reproduce the required final commands and a separate bounded clean-copy proof with verified cleanup. Do not repair tracked files, accept for Central, change remote state, write reconciliation, or begin Phase 3 planning. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings and a clear P2-AC12 recommendation.

## 13. Next Action

P2-EP06 v0.1 is complete. The independent Accept and Central reconciliation
of P2-AC01–P2-AC12 are recorded in
`ViDAP_P2_EP06_Validation_and_Reconciliation.md`. Phase 2 is complete and
detailed Phase 3 planning is ready to draft. Phase 3 execution requires its
own approved plan and bounded packets.
