# ViDAP P0-EP08 — Fresh-Environment Validation and Reconciliation Evidence

| Field | Value |
|---|---|
| Status | Approved for bounded execution |
| Packet version | 0.1 |
| Parent phase plan | ViDAP_Phase_0_Plan.md version 1.1 |
| Prerequisites | P0-EP01 through P0-EP07 — Complete |
| Prerequisite reconciliations | ViDAP_P0_EP01_Validation_and_Reconciliation.md through ViDAP_P0_EP07_Validation_and_Reconciliation.md |
| Workstream | WS0.7 — Validation and closeout |
| Packet type | Bounded read-only fresh-environment evidence collection |
| Created | 2026-09-19 |
| Approved | 2026-09-19 |
| Owner | Central |

---

## 1. Authorization boundary

Version 0.1 received fresh explicit user approval on 2026-09-19. No approval
of another packet or a later revision carries forward.

After approval, one fresh evidence worker may create only the Section 7 report
in the repository. The worker may inspect the repository read-only; create one
exact temporary clean checkout outside the repository and OneDrive; run the
approved locked commands in that temporary checkout; and remove only the
temporary checkout and its known isolated caches after evidence is recorded.

The worker may not modify product, configuration, dependency, lock, CI,
governance, or remote state; accept Phase 0; commit; push; dispatch CI; open a
browser; install or alter a system/global prerequisite; or begin Phase 1.
This packet gathers closeout evidence. It is not permission to repair a
failure. A failed prerequisite or command is a named blocker for Central.

## 2. Plain-English intent

P0-EP01 through P0-EP07 established and independently validated the pieces of
the Phase 0 foundation. This packet asks a fresh worker to answer one narrower
question: can a clean, isolated Windows checkout reproduce the accepted
foundation, including setup, quality, build, local launch, smoke, and
dependency controls, without relying on the original working directory or
leaving state behind?

The output is evidence and a recommendation for Central. It does not itself
make the Phase 0 completion decision, and it does not add any application
behavior.

## 3. Governing inputs and traceability

The worker and later independent validator must read these sources in order:

1. Current explicit user direction approving this exact packet version.
2. ViDAP_Overview.txt, especially OV Sections 9, 18, 20-23, and 25-30.
3. ViDAP_Phased_Plan_Spine.md version 1.2, especially the authority chain,
   local-first, testing, data-responsibility, completion-attestation, and
   independent-validation rules.
4. ViDAP_Roadmap.md version 1.2, especially Phase 0 and its A0 checkpoint.
5. ViDAP_Phase_0_Plan.md version 1.1, especially WS0.7, Sections 9-11,
   P0-AC01 through P0-AC13, and the Phase 0 exclusions.
6. The accepted P0-EP01 through P0-EP07 reconciliation records, including the
   accepted D0.1-D0.7 decisions and their bounded evidence.
7. Decision Records 0001, 0003, and 0004; docs/dependency-controls.md; the
   current README.md and CONTRIBUTING.md; and the current package/task,
   ignore, and CI configuration.
8. This packet.

This packet advances P0-G9 and P0-AC01 through P0-AC13. It does not decide a
Phase 1 workflow format, node contract, execution semantic, or product scope.

## 4. Preconditions and target baseline

Before any temporary checkout is created, the worker must confirm and record:

1. P0-EP01 through P0-EP07 are marked Complete by their Central reconciliation
   records, with no unresolved Critical or High finding.
2. The current target commit is a committed repository state; its branch,
   full commit identifier, and sanitized remote identity are recorded.
3. The target contains no uncommitted product, manifest, lock, CI,
   configuration, or generated-state change. Pre-existing Central planning or
   reconciliation files outside the target are recorded and preserved.
4. The target retains the accepted Node 24 and uv-managed CPython 3.14
   contracts, sole lock authorities, Windows-only support posture, and
   loopback-only foundation boundary.
5. The last accepted hosted Windows evidence remains applicable. If any
   committed change since the accepted P0-EP07 hosted commit changes source,
   tasks, manifests, locks, CI, or process behavior, stop and return a blocker
   requiring fresh user-authorized hosted evidence.

The worker must not use a moving branch as evidence. It records the exact
target commit before the first setup command and returns a blocker if that
target cannot be cleanly checked out.

## 5. Required fresh-environment evidence

### 5.1 Isolation and safe setup

The worker must create one uniquely named temporary checkout outside both the
repository and OneDrive. It must originate from the recorded committed target,
not copy the current working tree or include uncommitted content. npm and uv
caches used for this proof must be isolated from prior project caches.

Before network-backed setup or audit work, the worker must confirm that no
inherited certificate override or invalid SSL trust setting is active for the
normal Windows uv path. It must not bypass certificate validation, add a
certificate, change a system setting, or substitute a package tool. A trust
failure is a blocker.

### 5.2 Reproduction commands

In that one clean temporary checkout, using the documented Windows command
path, the worker must run and record concise final outcomes for:

1. npm.cmd run setup
2. npm.cmd run check
3. npm.cmd run coverage
4. npm.cmd run deps:inventory
5. npm.cmd run license:check
6. npm.cmd run deps:audit

The aggregate check is the authoritative quality/build/in-process
integration/smoke path and must run with smoke last. The worker must also
exercise npm.cmd run launch in the temporary checkout: wait only for its
documented loopback-ready message, send Ctrl+C only to that worker-started
launch process, and confirm its known child processes exit. No browser may be
opened.

The worker must record Node, npm, uv, and selected CPython versions; both
SHA-256 lock hashes before and after all routine commands; and the direct and
proxied loopback status result only as a bounded observation. It must not
copy logs, environment dumps, or absolute user paths into the report.

### 5.3 Hygiene, documentation, and phase-boundary review

The worker must independently inspect the target and temporary checkout for:

- a clean Git diff and no staged change before/after the proof;
- ignored dependency, environment, cache, build, coverage, PID, and log
  state, with authored fixture content remaining trackable;
- no listener remaining on either prescribed loopback port after smoke and
  controlled launch shutdown;
- current README and CONTRIBUTING instructions matching the observed commands,
  runtime prerequisites, loopback ports, manual-browser rule, and deferrals;
- current dependency inventory, fail-closed license policy, literal Decisions
  0003/0004 treatment, and advisory output; and
- absence of credentials, user data, absolute user paths, generated state, and
  Phase 1 or later behavior.

The worker must map the observed evidence to every P0-AC01 through P0-AC13.
It must separately state the known Phase 0 limitations and deferrals, notably
the absence of workflow/node semantics, datasets, models, experiments, export,
hosting, desktop packaging, and validated non-Windows support.

## 6. Required worker completion attestation

Before reporting implementation evidence complete, the worker must complete
every Section 5 command and review against the final unchanged target. If a
required command fails, it must not call the packet complete or defer the
missed command to independent validation. It must return a named blocker with
the failed command, concise diagnostic, affected P0 acceptance criterion, and
safe Central decision needed.

This is worker-completion attestation only. The worker may not issue an
independent verdict, declare EP08 or Phase 0 accepted, or replace the separate
validator and Central reconciliation.

## 7. Permitted repository output and file scope

The worker may create or modify only this repository file:

| Path | Purpose |
|---|---|
| ViDAP_P0_EP08_Implementation_Report.md | Sanitized fresh-environment evidence, P0 acceptance map, findings, limitations, and independent-validation handoff. |

The report must state that it is evidence only and does not accept EP08 or
Phase 0. It must not contain credentials, user data, absolute user paths, raw
environment values, copied lockfiles, complete command logs, or external
package artifacts.

No other repository path may be created or modified. Temporary files may exist
only in the exact external temporary checkout and its known isolated caches,
and must be removed after evidence collection.

## 8. Prohibited scope

The worker must not:

1. Modify any source, test, fixture, manifest, lock, dependency, task,
   configuration, CI, workflow, ignore, attribute, documentation, decision,
   roadmap, phase plan, reconciliation, security, or license file.
2. Add, remove, upgrade, normalize, resolve, or audit-fix a dependency; alter
   a runtime, global tool, certificate, environment policy, PowerShell policy,
   Git configuration, or repository setting.
3. Start a browser, bind publicly, choose alternate ports, access a cloud
   service other than ordinary locked package retrieval, create a hosted run,
   or manipulate an unrelated process.
4. Stage, commit, push, pull, merge, rebase, tag, dispatch CI, create a pull
   request/release, or change remote state.
5. Repair a finding, create an exception or decision record, alter the target
   commit, accept EP08/Phase 0, or begin Phase 1 planning or work.

## 9. Required execution sequence

After approval, the worker must:

1. Read all governing inputs and record the exact approved packet version,
   target commit, target baseline, pre-existing work, and permitted report path.
2. Verify the prerequisites and hosted-evidence applicability gate in Section
   4 before creating any temporary checkout.
3. Verify the normal Windows Node/npm/uv/CPython and certificate-trust
   posture; record a blocker rather than changing the host if unsuitable.
4. Create the one external clean checkout with isolated npm/uv caches.
5. Capture pre-command lock hashes and run the complete Section 5.2 command
   set, including controlled launch and cleanup observation.
6. Capture post-command lock hashes; perform the Section 5.3 hygiene,
   documentation, dependency/license, phase-boundary, and P0 acceptance review.
7. Remove only the exact temporary checkout and its known caches, then verify
   their absence and that no worker-started listener remains.
8. Create the Section 7 report; run whitespace, link, sensitive-content, and
   exact-file-scope checks; and perform the Section 6 final attestation.
9. Stop for independent validation. Do not make a completion or acceptance
   claim.

## 10. Required worker evidence

ViDAP_P0_EP08_Implementation_Report.md must include:

1. Packet identity, approval, worker role, governing inputs, target commit,
   sanitized remote identity, pre-existing work, and exact repository scope.
2. Prerequisite reconciliation and hosted-evidence applicability results.
3. Fresh-checkout/caching isolation method and confirmation it excluded
   uncommitted workspace content, without exposing absolute paths.
4. Node/npm/uv/CPython facts, certificate-trust result, and pre/post lock
   hashes.
5. Concise results for every Section 5.2 command, including aggregate check,
   coverage, controls, controlled launch, smoke, and cleanup.
6. Documentation, links, ignored-state, sensitive-content, whitespace,
   scope, fixture, dependency/license, and advisory conclusions.
7. A P0-AC01 through P0-AC13 evidence matrix, with each criterion marked
   Pass, Blocked, or Needs-Central-Decision.
8. Known limitations, deferrals, deviations, findings with severity/owner,
   and the exact reason no Phase 1 behavior is present.
9. The final worker-completion attestation and independent-validation handoff.

## 11. Acceptance criteria

P0-EP08 may be accepted only when:

- **EP08-AC01:** Authority, prerequisite reconciliations, target commit,
  hosted-evidence applicability, and worker/report scope are accurately
  recorded.
- **EP08-AC02:** The proof uses one clean external checkout and isolated
  caches; it does not include uncommitted workspace content or mutate the
  target repository.
- **EP08-AC03:** Node 24/npm, uv, CPython 3.14, certificate-trust posture, and
  the Windows-only support claim are accurately verified.
- **EP08-AC04:** Both lock authorities remain byte-identical before and after
  the complete proof.
- **EP08-AC05:** Locked setup succeeds without manual file edits, global
  package use, certificate bypass, or undocumented prerequisite.
- **EP08-AC06:** The aggregate check succeeds with the documented smoke path
  last; coverage and all three dependency-control commands also succeed.
- **EP08-AC07:** Controlled launch proves its documented loopback-ready path
  and known-child Ctrl+C cleanup without opening a browser or leaving a
  listener.
- **EP08-AC08:** The fresh proof leaves no generated dependency, environment,
  cache, build, coverage, PID, log, or temporary-copy residue in the target
  repository or at the exact temporary location.
- **EP08-AC09:** Documentation, tasks, runtime claims, loopback boundary,
  fixture boundary, dependency policy, and explicit deferrals match observed
  behavior.
- **EP08-AC10:** D0.1-D0.7 and P0-EP01 through P0-EP07 evidence are correctly
  reconciled against P0-AC01 through P0-AC13.
- **EP08-AC11:** Dependency inventory, license-policy, and advisory evidence
  are current; unlisted generic licenses remain fail-closed and the literal
  Decisions 0003/0004 dispositions are neither broadened nor altered.
- **EP08-AC12:** The repository remains free of secrets, user data, absolute
  user paths, generated local state, and unauthorized fixture use.
- **EP08-AC13:** The target contains no workflow/node/schema, data, model,
  experiment, export, persistence, hosting, desktop, or other Phase 1+
  behavior.
- **EP08-AC14:** No prohibited local/system/remote action occurs and no
  repository file beyond the Section 7 report is changed.
- **EP08-AC15:** The report is reproducible, sanitized, maps every Phase 0
  acceptance criterion, and clearly distinguishes evidence from acceptance.
- **EP08-AC16:** The worker's final post-change attestation covers every
  required command and evidence item, or returns a named blocker.
- **EP08-AC17:** No unresolved Critical or High finding remains; lesser items
  are resolved or explicitly returned for Central decision.
- **EP08-AC18:** A fresh independent validator accepts the closeout evidence
  without modifying files or accepting for Central.
- **EP08-AC19:** Central explicitly accepts EP08 and reconciles Phase 0 before
  Phase 1 planning begins.

## 12. Independent-validation boundary

Validation occurs in a fresh chat after the worker stops. The validator must
read all governing inputs, every prior reconciliation, the approved packet,
the one Section 7 report, the committed target, and the current Phase 0
artifacts. It must independently reproduce the fresh-checkout proof in its
own isolated location, including setup, check, coverage, dependency controls,
smoke, controlled launch shutdown, lock hashes, hygiene, documentation, and
P0-AC mapping.

The validator must confirm that existing hosted evidence remains applicable or
return Blocked with the required new evidence. It must inspect exact file
scope and prohibit any substitution of worker claims for reproduced evidence.
It must return Accept, Revise, or Blocked with criterion-linked findings,
severity/owner, concise evidence, P0 acceptance conclusion, and an explicit
statement that only Central may accept EP08 and close Phase 0.

The validator must not edit files, repair findings, accept policy changes,
commit, push, dispatch CI, alter remote/system state, or begin Phase 1.

## 13. Fresh-chat handoff prompts

### Execution worker prompt

> Execute freshly approved ViDAP_P0_EP08.md version 0.1 as the bounded Phase 0 closeout evidence worker. Read every governing input and all P0-EP01 through P0-EP07 reconciliations. Modify only ViDAP_P0_EP08_Implementation_Report.md. First prove the exact committed target and prior hosted Windows evidence remain applicable. In one exact clean checkout outside the repository and OneDrive, with isolated npm and uv caches, use the documented Windows path to run setup, check, coverage, dependency inventory, license check, advisory audit, and a controlled launch/Ctrl+C cleanup observation. Verify lock hashes, documentation, hygiene, dependency policy, Phase 0 exclusions, and every P0-AC01 through P0-AC13. Run the entire final post-change attestation before reporting. Do not fix findings, change source/configuration/locks/CI/governance, open a browser, alter system settings, stage/commit/push, self-validate, or begin Phase 1. Return a named blocker if any required condition fails; otherwise stop with the sanitized report for independent validation.

### Independent validator prompt

> Act as the independent validator for freshly approved ViDAP_P0_EP08.md version 0.1. Read every governing input, all accepted P0-EP01 through P0-EP07 reconciliation records, the Section 7 report, the committed target, and all Phase 0 artifacts. In your own isolated fresh checkout, independently reproduce setup, check, coverage, dependency inventory/license/advisory controls, smoke, controlled launch/Ctrl+C cleanup, lock-hash, hygiene, documentation, dependency-policy, and Phase 0 acceptance evidence. Confirm existing hosted Windows evidence remains applicable or return Blocked. Do not edit files, repair findings, accept for Central, alter remote/system state, or begin Phase 1. Return Accept, Revise, or Blocked with criterion-linked findings and an explicit Phase 0 reconciliation recommendation.

## 14. Next action

Version 0.1 is approved for one fresh read-only evidence worker. Independent
validation and Central Phase 0 reconciliation remain separate later gates.
