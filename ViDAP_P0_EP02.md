# ViDAP P0-EP02 - Quality, CI, Dependency, and Fixture Decisions

| Field | Value |
|---|---|
| Status | Complete |
| Packet version | 1.0 |
| Execution approved | 2026-09-17 by explicit user direction |
| Completed | 2026-09-17 |
| Decision report | `ViDAP_P0_EP02_Decision_Report.md` |
| Central reconciliation | `ViDAP_P0_EP02_Validation_and_Reconciliation.md` |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisite packet | P0-EP01 - Complete |
| Prerequisite reconciliation | `ViDAP_P0_EP01_Validation_and_Reconciliation.md` |
| Workstream | WS0.1 - Baseline and decisions |
| Decisions covered | D0.4-D0.7 |
| Packet type | Research and decision; documentation-only repository changes |
| Created | 2026-09-17 |
| Owner | Central |

---

## 1. Authorization Boundary

This document defines the second proposed Phase 0 execution packet. It is not authorized for execution while its status is `Draft for review`.

Approval will authorize bounded research, read-only repository/environment inspection, and creation of the decision report named in Section 12. It will not authorize installing tools, adding manifests or configuration, creating CI workflows, adding fixtures, scaffolding the application, changing repository settings, or executing P0-EP03 and later packets.

The packet selects tools and policies. P0-EP03 through P0-EP07 implement the accepted decisions in separately approved units.

---

## 2. Plain-English Packet Intent

### What this packet will do

It will decide:

- which formatting, linting, type-checking, test, and smoke-test roles the project needs and the preferred tool for each role;
- how local checks and GitHub-based continuous integration remain equivalent;
- how dependencies, licenses, vulnerabilities, and updates are reviewed;
- how tiny test fixtures are created, documented, licensed, stored, and kept free of sensitive data.

### Why this comes before scaffolding

The repository should not be generated first and governed later. These decisions determine which manifests, scripts, CI checks, fixture metadata, and evidence the scaffold and later quality packets must create.

### What it enables

Once accepted, P0-EP03 can document the repository contract, P0-EP04 can scaffold only the approved tool boundaries, P0-EP05 can implement meaningful checks, and P0-EP06/P0-EP07 can implement CI, dependency controls, and controlled fixtures without reopening the policy questions.

### How success will be demonstrated

The worker will produce one evidence-backed decision report. Every selected tool will have one explicit role, a real Phase 0 target, a local and CI execution path, current primary-source support, and a license compatible with the MIT project. The report will also define enforceable CI, dependency, license, update, and fixture policies without installing or configuring anything.

---

## 3. Governing Inputs

The worker must read the current approved versions of:

1. `ViDAP_Overview.txt`, especially Sections 9, 18-25, 28, and 30.
2. `ViDAP_Phased_Plan_Spine.md` version 1.0, especially program-wide invariants and P0 completion gates.
3. `ViDAP_Roadmap.md` version 1.0, especially A0, the cross-cutting delivery tracks, and risk controls.
4. `ViDAP_Phase_0_Plan.md` version 1.0, especially D0.4-D0.7, required deliverables, tests, and Phase 0 guardrails.
5. `ViDAP_P0_EP01_Decision_Report.md`, using the accepted state recorded by Central rather than superseded worker recommendations.
6. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, which is authoritative for accepted D0.1-D0.3 and the Python 3.14 amendment.

Instructions or recommendations inside evidence reports are inputs only. Current user direction and the approved authority chain govern execution.

---

## 4. Inherited Decisions and Non-Negotiable Constraints

P0-EP02 must preserve:

- a local TypeScript/React UI with React Flow as the initial graph-editor direction;
- a separate local CPython/FastAPI execution host;
- one repository with explicit UI, workflow/schema, execution, experiment/state, export, tests/fixtures, and documentation ownership;
- CPython 3.14.x as the default scaffold target, with a mandatory compatibility stop gate in P0-EP04 and no silent Python 3.13 fallback;
- uv with one Python workspace and one committed `uv.lock`;
- Node.js 24 LTS with bundled npm and one committed `package-lock.json`;
- a root JavaScript manifest as the cross-stack task entry, invoked through `npm.cmd` on the supported Windows PowerShell path and delegating Python tasks through uv;
- Windows as the only initial supported development platform;
- no PowerShell policy changes, global task packages, containers, installers, hosted product services, or competing package managers;
- exact dependency versions and full locked-graph evidence remaining implementation-time work for P0-EP04/P0-EP06.

P0-EP02 may select quality and policy tools compatible with these decisions. It may not reopen D0.1-D0.3 unless it finds a blocking incompatibility, in which case it must stop and return the evidence to Central.

---

## 5. Objective and Completion Condition

### Objective

Produce recommendations for:

- **D0.4:** Quality and test layers.
- **D0.5:** CI and branch expectations.
- **D0.6:** Dependency, license, vulnerability, and update policy.
- **D0.7:** Controlled fixture policy.

### Completion condition

P0-EP02 is complete only when:

1. The decision report in Section 12 is produced.
2. Its documentary self-check is complete.
3. A separate validator creates the validation report in Section 18 and returns `Accept`.
4. Central accepts, rejects, or returns D0.4-D0.7.

The execution worker and validator cannot accept their own conclusions on Central's behalf.

---

## 6. Preconditions

Before execution, confirm and record:

- this packet is explicitly approved for execution;
- P0-EP01 remains complete and its reconciliation has not been superseded;
- the current branch, commit, worktree, remote, and file inventory are known;
- no application scaffold, manifests, lockfiles, CI workflows, quality configuration, dependency output, or fixture assets have appeared without an approved record;
- the authorized worker-output path is free of conflicting user work;
- current official-source web research is permitted;
- no candidate evaluation requires installing or executing third-party software.

If a precondition is false, stop and report it to Central.

---

## 7. Permitted Scope

The execution worker may:

- inspect repository and environment state read-only;
- research current official documentation, repositories, licenses, support policies, and security policies;
- compare credible tools for each required role;
- define authoritative local task categories and expected CI parity without adding scripts;
- define CI runner, trigger, permission, cache, artifact, and branch-check policies without changing GitHub or repository settings;
- define license categories, exception handling, dependency review, vulnerability triage, and update policies;
- define fixture provenance, privacy, size, metadata, storage, generation, and review rules;
- assign each selected implementation or policy to P0-EP03 through P0-EP07;
- propose a separate bounded feasibility spike only when documentary evidence cannot resolve a blocking decision.

The worker may create or modify only the decision report named in Section 12.

---

## 8. Prohibited Scope

The execution worker must not:

- install or execute candidate quality, test, CI, dependency, license, vulnerability, or fixture tools;
- create or change `package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`, runtime-version files, source directories, test directories, configuration files, or CI workflows;
- add a fixture, dataset, generated file, cache, virtual environment, dependency directory, or build output;
- change GitHub branch protection, Actions settings, Dependabot, secrets, labels, or other remote state;
- modify system configuration, PowerShell policy, global packages, browsers, Python, Node, npm, or uv;
- introduce a second package manager or cross-stack task runner;
- define application APIs, workflow schemas, node contracts, persistence formats, experiment behavior, or export behavior;
- select actual product/ML dependencies owned by later phases;
- treat a vulnerability scanner result as proof of exploitability or a clean result as proof of safety;
- treat automated license classification as final legal advice;
- edit governing artifacts or begin P0-EP03 and later work;
- commit, push, create branches, open pull requests, or mutate external services;
- include secrets, sensitive workstation data, or unrelated user information in the report.

---

## 9. Decision Method

### 9.1 Universal viability gates

Every selected tool or hosted CI feature must satisfy all applicable gates:

| Gate | Requirement |
|---|---|
| UG-01 Runtime compatibility | Credible maintained support for Node 24/npm or Python 3.14/uv as applicable; uncertainty becomes an explicit P0-EP04 stop condition |
| UG-02 Windows viability | Works through documented Windows-compatible commands without changing PowerShell execution policy |
| UG-03 Local/CI parity | The same underlying check can run locally and in CI; CI-only quality truth is prohibited |
| UG-04 Repository management | Configuration and invocation are repository-managed and lockfile-compatible; no global task package is required |
| UG-05 Deterministic role | The tool has one explicit responsibility and produces reproducible pass/fail evidence appropriate to that role |
| UG-06 Maintained primary evidence | Current official documentation, release/support evidence, and repository health are available |
| UG-07 License compatibility | The tool's mandatory path has no identified conflict with the MIT project; uncertainty is surfaced |
| UG-08 Proportionality | Setup and maintenance cost are justified by a current Phase 0 or near-term requirement |
| UG-09 Automation safety | Default automation cannot silently modify source, lockfiles, dependencies, or remote state during a check |
| UG-10 Actionable failure | Failures identify the affected files/check and provide enough detail for a contributor to act |

A failed or unresolved universal gate prevents selection. The worker must not hide a gate failure inside a weighted score.

### 9.2 Comparison rules

For each role where more than one credible choice exists, compare at least two viable candidates using:

- fit to the inherited stack;
- role coverage and overlap;
- Windows/local/CI behavior;
- configuration and maintenance cost;
- speed and contributor feedback;
- ecosystem health and support policy;
- output clarity and machine-readable evidence where useful;
- license and supply-chain surface.

The report need not manufacture a second candidate when an inherited language/compiler or accepted package manager already dictates the role. It must explain why comparison would be artificial.

Selection may use a concise scoring matrix, a structured tradeoff table, or a reasoned role-by-role decision. It must not present preference as evidence.

### 9.3 Evidence confidence

Each selected tool receives `High`, `Medium`, or `Low` confidence and a named implementation-time verification owner. A low-confidence tool cannot be accepted without a blocking spike or an explicit Central exception.

---

## 10. Required D0.4 Decisions - Quality and Test Layers

The report must select or explicitly defer one tool and one task role for each applicable row:

| Layer | Required decision |
|---|---|
| TypeScript compilation/type checking | Compiler/check command, configuration ownership, and whether emission is separate from checking |
| Frontend formatting | Formatter and check-versus-write task separation |
| Frontend linting | Linter, framework-specific coverage, accessibility/static-analysis posture, and overlap with the formatter |
| Frontend unit/component tests | Runner, DOM/component environment, deterministic behavior, and coverage posture |
| Browser/end-to-end smoke tests | Tool or explicit deferral, browser acquisition policy, startup ownership, and Phase 0 target |
| Python formatting/linting | Tool or deliberately separated tools, check/fix separation, and import rules |
| Python type checking | Type checker, strictness starting point, third-party stub policy, and escalation path |
| Python unit/integration tests | Runner, async/API test posture, markers, and deterministic fixture behavior |
| Cross-process smoke testing | Ownership of starting/stopping local processes, readiness checks, timeout/failure behavior, and no orphan process rule |
| Clean-setup verification | How P0-EP08 proves setup from declarations and lockfiles rather than workstation caches |
| Coverage | Whether thresholds begin in Phase 0, what is measured, and why a number is or is not justified |
| Authoritative root tasks | Stable task categories for format-check, lint, typecheck, unit, integration/smoke, build, and aggregate check; exact script implementation is deferred |

Candidate families that normally deserve comparison include:

- integrated frontend formatter/linter versus separate formatter and linter;
- current TypeScript-oriented test runners compatible with the accepted web stack;
- browser automation tools versus explicit Phase 0 browser-test deferral;
- integrated Python formatter/linter versus separate Python tools;
- current Python type checkers;
- standard Python test runners and API test approaches.

The decision must minimize overlapping tools. A tool is not selected merely because it is popular.

---

## 11. Required D0.5-D0.7 Policy Decisions

### 11.1 D0.5 - CI and branch expectations

Define:

- whether GitHub Actions is the selected CI host and how provider-neutral local tasks remain authoritative;
- required Windows runner coverage and any additional non-blocking portability runner;
- pull-request, push-to-main, manual, and scheduled triggers;
- least-privilege permissions and when secrets are prohibited;
- job boundaries, ordering, fail-fast behavior, and required checks;
- lockfile-aware cache keys and conditions where caches are bypassed;
- artifact/log retention and prohibition on uploading datasets, secrets, environments, or dependency directories;
- concurrency/cancellation policy for superseded runs;
- branch expectation and required review/check posture without mutating repository settings;
- third-party action policy, including version or commit pinning and update review;
- the exact evidence P0-EP06 must produce before CI is accepted.

The policy must work for an open-source repository without paid or organization-only services.

### 11.2 D0.6 - Dependency, license, vulnerability, and update policy

Define:

- direct versus transitive dependency inventory responsibilities for npm and uv lock graphs;
- allowed, review-required, and normally prohibited license categories;
- handling of missing, custom, multi-license, platform-binary, notice, and copyleft cases;
- who may grant an exception and what evidence the exception records;
- candidate tools or deterministic methods for dependency and license reports in each ecosystem;
- vulnerability advisory sources and candidate scanners;
- severity, exploitability, reachability, and availability considerations in triage;
- response expectations for critical/high findings and handling of disputed or no-fix findings;
- routine update cadence, emergency updates, and lockfile review expectations;
- automated update-bot posture, grouping, rate limits, and prohibition on unreviewed auto-merge;
- whether a Phase 0 SBOM is required or deferred, with rationale;
- evidence later ML/model libraries must provide before acceptance.

Automated output informs review; it does not replace human license or vulnerability judgment.

### 11.3 D0.7 - Controlled fixture policy

Define:

- synthetic/generated-first versus externally sourced fixture preference;
- allowed Phase 0 formats and an exact size ceiling;
- canonical `fixtures/` ownership consistent with D0.2;
- required metadata for provenance, license/terms, creation method, purpose, expected properties/results, checksum where useful, and responsible phase;
- prohibition on personal, sensitive, credential, production, or ambiguously licensed data;
- deterministic generation and seed policy;
- when generated data is committed versus regenerated;
- review requirements for external fixtures and binary files;
- mutation/versioning rules so a changed fixture cannot silently invalidate expected results;
- cleanup and Git-ignore interaction for transient fixture outputs;
- the tiny Phase 0 fixture P0-EP07 may create without implying Titanic or later domain support.

Titanic remains deferred to P4. Healthcare and scientific reference datasets remain deferred to their roadmap phases.

---

## 12. Authorized Worker Output

The execution worker may create one file:

`ViDAP_P0_EP02_Decision_Report.md`

No other repository file may be created, modified, moved, or deleted by the execution worker.

The report must contain:

1. Packet, input-version, authorization, and evidence metadata.
2. Execution-time repository/environment baseline and delta.
3. Current primary-source bibliography with retrieval dates.
4. UG-01 through UG-10 results for each selected tool or CI feature.
5. Role-by-role D0.4 comparisons and decisions.
6. Authoritative local task taxonomy and local/CI parity rules.
7. D0.5 CI and branch policy.
8. D0.6 dependency, license, vulnerability, and update policy.
9. D0.7 controlled fixture policy.
10. Rejected alternatives and reasons.
11. Exact handoff constraints for P0-EP03 through P0-EP07.
12. Blocking and non-blocking findings with owners.
13. Any separately approvable feasibility-spike proposal.
14. An EP02-AC01 through EP02-AC20 self-assessment.
15. Final read-only Git status and file-scope evidence.
16. A validation-readiness statement.

---

## 13. Research and Evidence Rules

1. Current version support, CI behavior, licenses, security policies, and maintenance status require current primary evidence.
2. Prefer official documentation, official repositories, authoritative license text, and official advisory databases.
3. Record access dates and distinguish external fact from analysis.
4. Research tool behavior without installing or executing it.
5. License conclusions cover the proposed mandatory path and explicitly reserve full locked-graph review for P0-EP06.
6. Do not assume a tool supports Python 3.14 merely because it supports Python 3; verify or mark P0-EP04 compatibility as blocking.
7. Do not infer Windows or PowerShell behavior from POSIX-only examples.
8. Do not rely on vendor marketing for security, accessibility, determinism, or ecosystem-health claims.
9. Do not interpret a scanner's database coverage as complete security coverage.
10. Stop research when every required role and policy has a defensible decision; avoid surveying unrelated tools.

---

## 14. Required Execution Sequence

1. Re-read governing inputs and record exact versions/statuses.
2. Confirm packet authorization, current commit, branch, worktree, remote, file inventory, and output-path availability.
3. Record changes since EP01 reconciliation without altering them.
4. Create the complete role/policy checklist from Sections 10-11.
5. Identify credible candidates and apply UG-01 through UG-10 before selection.
6. Research current primary evidence for compatibility, licensing, maintenance, CI behavior, and security posture.
7. Decide D0.4 tool roles and task taxonomy, eliminating unjustified overlap.
8. Decide D0.5 CI/branch policy while keeping local tasks authoritative.
9. Decide D0.6 dependency/license/vulnerability/update policy.
10. Decide D0.7 fixture policy and Phase 0 bounds.
11. Trace every decision to the packet that implements it.
12. Record blocking questions; propose a separate spike instead of installing or prototyping.
13. Create only `ViDAP_P0_EP02_Decision_Report.md`.
14. Perform the required acceptance-criteria self-assessment and final read-only file-scope check.
15. Stop and hand off to a fresh independent validator.

---

## 15. Feasibility-Spike Rule

Documentary uncertainty becomes a spike proposal only when it changes a required D0.4-D0.7 selection and cannot responsibly be deferred to the implementing packet's compatibility check.

A proposal must state one question, evidence already checked, bounded actions/installations, time or effort bound, observable success/failure, cleanup, license/security implications, and decision consequences. It requires separate approval and cannot be executed under P0-EP02.

---

## 16. Acceptance Criteria

P0-EP02 may be accepted only when:

- **EP02-AC01:** The report accurately records authorization, inputs, baseline, and delta without exposing sensitive information.
- **EP02-AC02:** Every D0.4 role in Section 10 is selected or explicitly deferred with owner and rationale.
- **EP02-AC03:** Every selected tool passes all applicable UG-01 through UG-10 gates with evidence and confidence.
- **EP02-AC04:** Credible alternatives are compared where choice exists; inherited/dictated roles explain why artificial comparison was omitted.
- **EP02-AC05:** Formatting, linting, type checking, unit testing, integration/smoke testing, and clean-setup validation have distinct non-ornamental purposes.
- **EP02-AC06:** The selected toolset avoids unjustified overlapping tools and defines check versus fix/write behavior.
- **EP02-AC07:** Root task categories are stable, cross-stack, Windows-compatible, lock-respecting, and do not require global task packages or policy changes.
- **EP02-AC08:** CI executes the same underlying checks as local tasks and does not create a second source of quality truth.
- **EP02-AC09:** D0.5 covers runners, triggers, permissions, secrets, jobs, caches, artifacts, concurrency, required checks, and action pinning.
- **EP02-AC10:** CI policy requires no paid or organization-only service and makes no unsupported platform claim.
- **EP02-AC11:** D0.6 defines direct/transitive inventory, license categories, exceptions, unknown/custom/multi-license handling, notices, and later ML dependency evidence.
- **EP02-AC12:** Vulnerability policy distinguishes advisory severity from actual project risk and defines triage, response, and no-fix handling.
- **EP02-AC13:** Update policy covers routine/emergency changes, lockfile review, automation limits, and prohibits unreviewed auto-merge.
- **EP02-AC14:** D0.7 defines fixture provenance, licensing, privacy, formats, size ceiling, deterministic generation, metadata, mutation, and transient-output rules.
- **EP02-AC15:** The Phase 0 fixture remains tiny and does not import Titanic, healthcare, scientific, production, personal, or sensitive data.
- **EP02-AC16:** Decisions have specific implementation owners across P0-EP03 through P0-EP07 without performing their work.
- **EP02-AC17:** Current changeable claims cite primary sources with access dates; compatibility uncertainties become explicit stop gates.
- **EP02-AC18:** No tools are installed or executed and no configuration, workflow, fixture, remote setting, scaffold, manifest, lockfile, dependency, or product behavior is introduced.
- **EP02-AC19:** The decision report is the execution worker's only repository change, with final Git evidence distinguishing pre-existing work.
- **EP02-AC20:** Independent validation returns `Accept`, and Central explicitly accepts D0.4-D0.7 before the packet is marked complete.

---

## 17. Stop and Escalation Conditions

Stop and return to Central if:

- a mandatory tool cannot credibly support Python 3.14, Node 24, Windows, or the accepted package managers;
- all credible candidates for a required role fail a universal gate;
- a required tool or service has unresolved license incompatibility or requires a paid/organization-only capability;
- a decision requires changing D0.1-D0.3 rather than merely constraining implementation;
- the choice can be settled only by installation or executable experimentation;
- CI policy would require secrets, write permissions, or remote mutation not justified by a Phase 0 check;
- license policy would silently permit unknown or incompatible mandatory dependencies;
- fixture requirements need real, personal, sensitive, production, or later-phase reference data;
- the authorized output path conflicts with user work;
- more than the one worker-output file is required;
- a product-level tradeoff needs explicit user direction.

Non-blocking limitations must name their owning later packet or phase.

---

## 18. Independent Validation Contract

Independent validation happens in a fresh chat after worker execution and self-checking. The validator must read the governing inputs, this packet, and the worker decision report.

### Validator tasks

The validator must:

1. Recheck representative high-impact compatibility, lifecycle, CI, license, and security-policy citations using current primary sources.
2. Verify every required D0.4 role and D0.5-D0.7 policy field is decided or explicitly deferred.
3. Challenge the most plausible alternative for at least the frontend quality stack, Python quality/type stack, CI approach, dependency/license method, and fixture policy.
4. Confirm every selected tool passes the universal gates and no role overlap is hidden.
5. Confirm Python 3.14 uncertainty is handled as an implementation stop gate rather than assumed compatibility.
6. Verify local/CI task parity, Windows `npm.cmd` viability, lockfile discipline, cache safety, least privilege, and no unsupported platform claim.
7. Review license categories, copyleft/custom/unknown handling, notices, exceptions, vulnerability triage, and automated-update limits.
8. Confirm fixture policy prevents sensitive or ambiguously licensed data and does not pull later validation datasets into Phase 0.
9. Recheck the worker self-assessment and final Git/file-scope evidence.
10. Return `Accept`, `Revise`, or `Blocked` with IDs, severity, affected criteria, evidence, and required correction.

### Authorized validator output

The validator may create one file:

`ViDAP_P0_EP02_Validation_Report.md`

The validator must not modify the worker decision report, packet, governing documents, configuration, remote state, or any other file. If no file write is desired, the validator may return the same structured report in chat for Central to preserve, but a durable validation file is preferred.

The validation report must contain:

- verdict: `Accept`, `Revise`, or `Blocked`;
- inputs and versions reviewed;
- citations rechecked;
- acceptance-criteria result table;
- alternative challenges performed;
- findings with stable IDs and severity;
- Git/file-scope conclusion;
- explicit statement that the validator did not accept D0.4-D0.7 for Central or begin later work.

---

## 19. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute the approved `ViDAP_P0_EP02.md` as the bounded execution worker. Read every governing input listed in the packet and follow its scope exactly. Use current primary sources where required. Create only `ViDAP_P0_EP02_Decision_Report.md`. Perform the packet-required documentary self-check and final read-only Git/file-scope check, but do not independently validate or accept your own work. Do not install or execute candidate tools, change configuration or remote state, create fixtures or scaffolding, or begin P0-EP03. Stop with the evidence and independent-validation handoff required by the packet.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P0_EP02.md`. Read its governing inputs and `ViDAP_P0_EP02_Decision_Report.md`. Follow Section 18 exactly. Use current primary sources to recheck the required evidence. Create only `ViDAP_P0_EP02_Validation_Report.md`, or return the identical structured validation in chat if file creation is not desired. Do not edit the worker report or governing files, accept D0.4-D0.7 on Central's behalf, configure tools or CI, mutate remote state, or begin P0-EP03. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 20. Evidence Return to Central

The execution worker must return:

- decision-report path;
- current commit and final worktree status;
- read-only commands and primary sources used;
- confirmation that no tool was installed/executed and no system/repository/remote mutation occurred;
- D0.4-D0.7 decision summary;
- EP02-AC01 through EP02-AC20 self-assessment;
- blocking/non-blocking findings and spike proposals;
- validation-readiness statement.

The validator must return the Section 18 validation report. Central will preserve the actual verdict, reconcile findings, and explicitly accept or return D0.4-D0.7.

---

## 21. Next Action After Completion

P0-EP02 is complete. Independent validation returned `Accept`, and Central accepted D0.4-D0.7 in `ViDAP_P0_EP02_Validation_and_Reconciliation.md` on 2026-09-17. Central may now draft P0-EP03 as a separate bounded packet. This completion does not authorize P0-EP03 execution, configuration, dependency installation, scaffolding, or application implementation.
