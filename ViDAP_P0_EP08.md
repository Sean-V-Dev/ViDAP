# ViDAP P0-EP08 — Documentation-Only Delta Closeout

| Field | Value |
|---|---|
| Status | Approved for bounded execution |
| Packet version | 0.4 |
| Parent phase plan | ViDAP_Phase_0_Plan.md version 1.8 |
| Prerequisites | P0-EP01 through P0-EP07 — Complete |
| Prior EP08 evidence | Versions 0.1-0.3 retained as historical evidence; no acceptance |
| Workstream | WS0.7 — Validation and closeout |
| Packet type | Bounded read-only committed-snapshot delta review |
| Created | 2026-09-19 |
| Revised | 2026-09-19 |
| Approved | 2026-09-19, explicit user pre-approval for this documentation-only amendment |
| Owner | Central |

---

## 1. Authorization boundary

Versions 0.1 through 0.3 collected evidence against earlier committed
snapshots. The final v0.3 proof passed setup, check, coverage, inventory,
license, advisory, smoke cleanup, and launch-lifecycle inspection with
unchanged locks, but was blocked only because its committed target retained a
historical absolute user path in a governing document.

The subsequent committed snapshot removes that path and changes only EP08
evidence/governance documents. Current explicit user direction approves this
v0.4 documentation-only delta review without another approval prompt.

One fresh worker may create only the Section 7 delta report. It may inspect Git
and files read-only and run only the non-mutating document/provenance checks
named here. It may not install dependencies, run application processes, alter
source/configuration/locks/CI/governance, repair any finding, stage, commit,
push, dispatch CI, or begin Phase 1.

## 2. Plain-English intent

The runnable foundation has already passed its full fresh-environment proof.
This packet does not retest unchanged program behavior. It answers the smaller
question created by the documentation correction: does the new committed
snapshot differ from the tested snapshot only in allowed planning/evidence
files, and does it now pass the documentation hygiene checks that previously
blocked closeout?

This is a risk-proportionate evidence bridge, not a waiver of independent
validation or Central Phase 0 reconciliation.

## 3. Governing inputs and traceability

The worker and independent validator must read:

1. Current explicit user direction approving this exact version.
2. ViDAP_Overview.txt, especially OV Sections 9, 18, 20-23, and 25-30.
3. ViDAP_Phased_Plan_Spine.md version 1.2.
4. ViDAP_Roadmap.md version 1.8 and ViDAP_Phase_0_Plan.md version 1.8.
5. All accepted P0-EP01 through P0-EP07 reconciliation records.
6. The blocked EP08 v0.1, v0.2, and v0.3 reports, especially their successful
   functional evidence and named documentation-only findings.
7. The current README, CONTRIBUTING, dependency-control policy, package/task,
   lock, ignore, and CI artifacts.
8. This packet.

This packet advances P0-G9 and the documentation/hygiene portion of P0-AC11
and P0-AC12. It does not authorize product implementation or change the Phase
0 outcome.

## 4. Exact committed-snapshot gate

The worker must identify:

- the prior tested snapshot 829344140381195bb5b5a4a33cafd3b91719e83b;
- the documentation-correction baseline d20fb28dc9792664e21c3373d69fa92ff2c83d6b;
- the current committed target, which must be a descendant of the correction
  baseline; and
- the sanitized remote identity and branch relationship.

The complete committed delta from the prior tested snapshot through the target
may affect only these paths:

- ViDAP_P0_EP08.md;
- ViDAP_P0_EP08_Implementation_Report.md;
- ViDAP_P0_EP08_Rerun_Implementation_Report.md;
- ViDAP_P0_EP08_Final_Implementation_Report.md;
- ViDAP_P0_EP08_Delta_Closure_Report.md;
- ViDAP_Phase_0_Plan.md; and
- ViDAP_Roadmap.md.

Any change to source, test, fixture, package/task, manifest, lock, runtime
pin, CI, ignore/attribute, dependency-control, decision, security, license,
or contributor/product documentation is a blocker. No new hosted run is
required unless such a behavior-affecting change is found.

## 5. Required delta evidence

The worker must perform and record:

1. Exact Git ancestry and name-status comparison from the prior tested snapshot
   to the committed target, proving the Section 4 path limit.
2. Exact comparison of package.json, package-lock.json, python/uv.lock,
   runtime pins, root task definitions, CI/Dependabot, source, tests, fixture,
   and process-harness paths between the prior tested snapshot and target,
   proving they are unchanged.
3. Current SHA-256 hashes of both lock authorities matching the successful
   v0.3 report values.
4. A tracked-content scan for absolute user paths, credentials, private keys,
   and generated/local state. The previously found Phase 0 plan path must be
   absent.
5. Markdown link and whitespace checks for the changed documentation/evidence
   files; a review that packet/plan/roadmap status and version references agree;
   and a check that all historical EP08 reports remain preserved.
6. A clean worktree and exact-file-scope check before and after the review.

The worker must not rerun setup, check, coverage, dependency controls, smoke,
or launch. Their successful v0.3 evidence remains applicable only because
this packet requires proof that all behavior-affecting paths are unchanged.

## 6. Required worker completion attestation

Before reporting completion, the worker must complete every Section 5 item
against the final committed target. If any item fails, it must return a named
blocker and must not reuse earlier evidence to claim completion.

This attestation is evidence only. The worker cannot issue an independent
verdict, accept EP08 or Phase 0, or replace independent validation and Central
reconciliation.

## 7. Permitted repository output and scope

The worker may create or modify only:

| Path | Purpose |
|---|---|
| ViDAP_P0_EP08_Delta_Closure_Report.md | Sanitized committed-delta, hygiene, provenance, and attestation evidence for independent validation. |

All earlier EP08 reports are immutable historical records. The new report must
not contain absolute user paths, credentials, raw environment values, copied
lockfiles, or full command logs.

## 8. Prohibited scope

The worker must not modify any existing repository file; create any artifact
outside Section 7; run package installation, application, process, browser, or
network tasks; alter local/system/remote state; repair findings; stage, commit,
push, dispatch CI, or create a release/PR; accept EP08/Phase 0; or begin
Phase 1.

## 9. Required execution sequence

1. Read the governing inputs and preserve all pre-existing work.
2. Verify the exact committed-snapshot gate before doing any other review.
3. Perform every Section 5 delta, hash, hygiene, link, whitespace, status,
   and historical-report check.
4. Create the Section 7 report, then repeat the exact-file-scope and
   whitespace checks.
5. Record the final worker-completion attestation and stop for independent
   validation.

## 10. Acceptance criteria

P0-EP08 v0.4 may be accepted only when:

- **EP08-AC01:** The prior tested snapshot, correction baseline, final target,
  ancestry, branch, remote identity, and authority chain are accurate.
- **EP08-AC02:** The complete committed delta is limited exactly to Section 4
  documentation/evidence paths.
- **EP08-AC03:** Every behavior-affecting source, task, manifest, lock,
  runtime, CI, test, fixture, and process-harness path is unchanged from the
  prior tested snapshot.
- **EP08-AC04:** Both current lock hashes match the accepted v0.3 values.
- **EP08-AC05:** The prior v0.3 successful functional evidence remains
  applicable, while its blocked hygiene finding is explicitly resolved only by
  the current target.
- **EP08-AC06:** The current tracked content has no user-specific absolute
  path, credential, private-key, or generated/local-state finding; the former
  Phase 0 plan path is absent.
- **EP08-AC07:** Changed documentation/evidence links, whitespace, status,
  version references, and historical-record preservation pass review.
- **EP08-AC08:** No prohibited local, repository, system, remote, or later
  phase action occurs; only the Section 7 report is changed.
- **EP08-AC09:** The report is reproducible, sanitized, and clearly
  distinguishes the prior full proof from the current delta review.
- **EP08-AC10:** Final worker-completion attestation covers every required
  delta item with no unresolved Critical or High finding.
- **EP08-AC11:** A fresh independent validator accepts the delta evidence and
  confirms the full functional evidence remains applicable.
- **EP08-AC12:** Central explicitly accepts EP08 and reconciles Phase 0 before
  Phase 1 planning begins.

## 11. Independent-validation boundary

Validation occurs in a fresh chat after the worker stops. The validator must
independently calculate the committed delta, verify all Section 5 hygiene and
provenance evidence, compare behavior-affecting paths and lock hashes to the
prior tested snapshot, and inspect every EP08 report. It must accept the prior
functional proof only if the delta proves that all behavior-affecting paths are
unchanged.

The validator does not need to repeat setup, quality, coverage, audit, smoke,
or launch when that condition holds. It must return Blocked if the target delta
contains any behavior-affecting path, if the earlier proof is not applicable,
or if a current hygiene check fails.

The validator must not edit files, repair findings, accept for Central, alter
remote/system state, or begin Phase 1.

## 12. Fresh-chat handoff prompts

### Execution worker prompt

> Execute approved ViDAP_P0_EP08.md version 0.4 as the bounded documentation-only delta-closeout worker. Read all governing inputs and preserve the three blocked EP08 reports. Modify only ViDAP_P0_EP08_Delta_Closure_Report.md. Prove the committed target descends from d20fb28 and that the complete delta since 8293441 changes only the allowed Section 4 evidence/governance paths. Prove all source, tasks, manifests, locks, runtime pins, CI, tests, fixture, and process-harness paths are unchanged; compare both current lock hashes to the v0.3 evidence; scan tracked content for absolute user paths, credentials, private keys, and generated/local state; verify links, whitespace, status/version consistency, and historical-report preservation. Do not run setup, tests, audit, smoke, launch, or any process. Do not change existing files, stage/commit/push, self-validate, or begin Phase 1. Return a named blocker on any failed condition; otherwise stop with the sanitized report for independent validation.

### Independent validator prompt

> Act as the independent validator for approved ViDAP_P0_EP08.md version 0.4. Read all governing inputs, the three prior EP08 reports, the delta report, and all Phase 0 artifacts. Independently calculate the committed delta since 8293441, verify its path boundary, compare all behavior-affecting paths and lock hashes, reproduce the hygiene/link/whitespace/status checks, and verify the old absolute path is absent. Accept the prior v0.3 full functional proof only if the delta establishes that it remains applicable; otherwise return Blocked. Do not rerun setup, tests, audit, smoke, or launch unless a behavior-affecting difference is found. Do not edit files, accept for Central, alter remote/system state, or begin Phase 1. Return Accept, Revise, or Blocked with criterion-linked findings and a Phase 0 reconciliation recommendation.

## 13. Next action

Version 0.4 is approved for one documentation-only delta-closeout worker.
Independent validation and Central Phase 0 reconciliation remain separate later
gates.
