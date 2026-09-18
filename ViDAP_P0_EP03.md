# ViDAP P0-EP03 - Open-Source and Repository Baseline

| Field | Value |
|---|---|
| Status | Complete |
| Packet version | 1.0 |
| Approved | 2026-09-17 by explicit user direction |
| Completed | 2026-09-17 |
| Implementation report | `ViDAP_P0_EP03_Implementation_Report.md` |
| Central reconciliation | `ViDAP_P0_EP03_Validation_and_Reconciliation.md` |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisite packets | P0-EP01 and P0-EP02 - Complete |
| Prerequisite reconciliations | `ViDAP_P0_EP01_Validation_and_Reconciliation.md`; `ViDAP_P0_EP02_Validation_and_Reconciliation.md` |
| Workstream | WS0.2 - Repository governance |
| Packet type | Bounded repository-baseline implementation |
| Created | 2026-09-17 |
| Owner | Central |

---

## 1. Authorization Boundary

This document is a proposed execution packet. Its creation does not authorize execution.

After explicit user approval, one bounded execution worker may create only the repository-governance artifacts listed in Section 7 and the implementation report listed there. Approval will not authorize application code, project manifests, lockfiles, dependencies, workflows, fixtures, runtime installation, remote-repository changes, or P0-EP04 work.

The execution worker may make the approved local file changes and run read-only or non-mutating verification commands. The worker must not accept its own work. A fresh independent validator and Central reconciliation remain required before this packet becomes `Complete`.

---

## 2. Plain-English Packet Intent

### What this packet will change

It will turn the documentation-only repository into a recognizable open-source project at the repository-policy level. A visitor will be able to understand what ViDAP is, its current pre-application status, how contributions are governed, how to report ordinary and security issues, what license applies, where future technical decisions are recorded, and which local/generated files must never be committed.

### Why the system needs it

P0-EP04 will introduce manifests, lockfiles, directories, and setup commands. The repository contract must exist first so those changes land under explicit licensing, contribution, security, line-ending, editor, and local-state rules rather than creating policy accidentally through scaffolding defaults.

### What real behavior it enables

It enables a contributor or later bounded worker to identify the authoritative planning documents, understand the accepted Windows/runtime direction, propose a scoped change, protect secrets and local state, and create a durable decision record without guessing repository conventions.

### How success will be demonstrated

A reviewer can locate and understand every required policy from the repository root; verify the canonical MIT license; follow a real ordinary-issue and sensitive-security reporting route; confirm deterministic text and editor conventions; prove representative secrets, caches, environments, datasets, and generated outputs are ignored; and confirm that manifests, lockfiles, source code, CI, fixtures, and product behavior were not introduced.

---

## 3. Governing Inputs and Traceability

The worker must read these files in authority order before changing anything:

1. Current explicit user direction approving this packet, if given.
2. `ViDAP_Overview.txt`, especially OV §§1, 9, 18, 20-21, and 25-30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.0, especially Sections 1-3, P0, and Sections 6-7.
4. `ViDAP_Roadmap.md` version 1.0, especially P0 and the cross-cutting delivery tracks.
5. `ViDAP_Phase_0_Plan.md` version 1.0, especially P0-G6-P0-G7, WS0.2, required deliverables 2-3, P0-EP03, P0-AC02/P0-AC11, and Phase 0 guardrails.
6. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, authoritative for accepted D0.1-D0.3.
7. `ViDAP_P0_EP02_Validation_and_Reconciliation.md`, authoritative for accepted D0.4-D0.7.
8. This approved packet.

This packet advances:

- OV §1 and §9: an open-source, MIT-licensed project with controlled dependency/licensing expectations;
- OV §20: plain-English planning and contributor-facing meaning;
- OV §21: modularity, reproducibility, minimal hidden state, and avoidance of premature abstraction;
- OV §§25-28: documentation, bounded execution, independent validation, and Central reconciliation;
- OV §§29-30: roadmap alignment and minimal-scope delivery;
- Spine P0: documentation conventions, decision records, repository boundaries, and actionable project conventions; and
- Phase 0 P0-G6-P0-G7, WS0.2, deliverables 2-3, P0-AC02, and the policy portion of P0-AC11.

---

## 4. Inherited Decisions and Constraints

The worker must represent these accepted facts accurately without reopening them:

1. ViDAP is an MIT-licensed, local-first visual data-science project.
2. The selected application direction is a TypeScript/React local web UI and a separate local CPython/FastAPI host.
3. The repository will contain explicit ownership areas for UI, workflow/schema, execution integration, experiment/state, export, tests/fixtures, and documentation/decisions, but those areas are not created by EP03.
4. The Phase 0 default is CPython 3.14.x subject to the P0-EP04 compatibility stop gate; Python project management uses uv.
5. JavaScript uses Node.js 24 LTS and bundled npm.
6. The initial validated platform claim is Windows only. Other platforms may be architecturally plausible but are not supported until validated.
7. The accepted quality, CI, dependency, license, vulnerability, update, and fixture policies are recorded in the EP02 reconciliation. EP03 may summarize and link them but may not implement their tools.
8. The repository is still pre-scaffold. There are no valid setup, build, test, or launch commands yet. Documentation must not invent them or imply a runnable product.
9. Existing root planning and reconciliation documents remain authoritative in their present locations. EP03 does not relocate, rename, or rewrite them.
10. The repository is in a OneDrive-synchronized workspace. Mutable local state, caches, environments, datasets, build output, and secrets must be isolated from tracked content.

If an existing governing artifact conflicts with a lower-authority convention proposed here, stop and return the conflict to Central.

---

## 5. Preconditions and Baseline

Before writing, the worker must confirm and record:

1. This packet is explicitly approved for execution and its status/version reflect that approval.
2. P0-EP01 and P0-EP02 remain `Complete` with their reconciliation files present.
3. The current branch, commit, worktree status, and remote URL without exposing credentials.
4. Every Section 7 output path is absent or, if present, is explicitly identified as a collision before any overwrite.
5. No unrelated worktree change will be modified, staged, reverted, formatted, or incorporated.
6. The public repository identity remains `Sean-V-Dev/ViDAP`, or any changed identity is returned to Central because it affects links and reporting routes.
7. A usable private security-reporting route can be verified without changing remote settings. If GitHub private vulnerability reporting is unavailable and no approved private alternative exists, stop and return the blocker rather than publishing a false or unsafe route.

The observed planning-time baseline on 2026-09-17 was branch `main`, commit `bac14c5d5722cee6c16ebfb538646dc815cd1cd2`, remote `https://github.com/Sean-V-Dev/ViDAP.git`, and no Section 7 implementation output paths present. These facts must be rechecked at execution time and are not assumptions.

---

## 6. Objective and Completion Condition

### Objective

Establish the smallest durable non-application repository contract required before reproducible scaffolding begins.

### Completion condition

P0-EP03 is complete only when:

1. The approved worker creates exactly the authorized baseline artifacts and implementation report.
2. All EP03-AC01 through EP03-AC24 criteria pass or an unresolved item is returned to Central.
3. A separate validator returns `Accept` under Section 16.
4. Central reconciles the evidence and marks the packet `Complete`.

Worker completion, clean Git checks, or attractive documentation alone do not constitute acceptance.

---

## 7. Authorized Outputs and File Ownership

Execution may create only these paths:

| Path | Required purpose |
|---|---|
| `LICENSE` | Canonical MIT license for the ViDAP project |
| `README.md` | Root project identity, status, authority map, prerequisites, scope, and navigation |
| `CONTRIBUTING.md` | Contribution, approval, review, evidence, dependency, data, and repository-safety rules |
| `SECURITY.md` | Supported-version status and ordinary-versus-sensitive reporting routes |
| `.gitignore` | Secret, environment, cache, local-data, build, report, and transient-output exclusions |
| `.gitattributes` | Repository line-ending and text/binary normalization policy |
| `.editorconfig` | Minimal editor-independent text conventions |
| `docs/decisions/README.md` | Decision-record purpose, status model, naming, ownership, and lifecycle |
| `docs/decisions/0000-decision-record-template.md` | Reusable lightweight decision-record template |
| `ViDAP_P0_EP03_Implementation_Report.md` | Execution evidence and validation handoff |

The worker may create parent directory `docs/decisions/` only as needed for its two authorized files. No other file or directory is authorized. In particular, execution must not create `package.json`, `pyproject.toml`, version pins, lockfiles, source/component directories, test directories, fixture content, CI workflows, issue templates, pull-request templates, dependency-bot configuration, generated notices, or application-local-state directories.

The worker must not stage, commit, push, open a pull request, create issues, change repository settings, enable GitHub features, or mutate branch protection or secrets.

---

## 8. Required Content Contract

### 8.1 `LICENSE`

The file must contain the canonical MIT License text without added restrictions. Use:

`Copyright (c) 2026 ViDAP contributors`

Do not insert a guessed personal legal name, organization, dual license, contributor agreement, trademark restriction, warranty promise, dependency license, or custom exception. Dependency licenses remain attributable to their own packages and notices.

### 8.2 `README.md`

The root README must be concise and must include:

1. Project name and a plain-English description aligned with OV §§1-3.
2. A prominent status statement: foundation planning is active, no runnable application exists yet, and setup/build/test/launch commands arrive in later approved packets.
3. The current intended architecture at summary level without claiming implementation.
4. Current prerequisites as planned contracts: Windows, Git, Node.js 24 LTS with npm, CPython 3.14.x subject to compatibility verification, and uv. It must distinguish planned/accepted prerequisites from presently usable setup instructions.
5. A short scope statement and a short list of Phase 0 exclusions sufficient to prevent product overclaiming.
6. An authority/navigation section linking the product specification, spine, roadmap, Phase 0 plan, accepted reconciliation records, contribution guide, security policy, license, and decision-record guide.
7. A contribution entry point and ordinary/security reporting distinction.
8. The MIT license statement and link to `LICENSE`.
9. No badges, screenshots, release/version claims, installation commands, dependency commands, hosted-service claims, or unimplemented feature claims.

The README may link to the repository's GitHub Issues page for ordinary public bugs and proposals. It must not tell users to publish sensitive vulnerability details in an issue.

### 8.3 `CONTRIBUTING.md`

The contribution guide must define:

1. The authority chain from specification through approved packet and validation.
2. The rule that implementation requires an approved bounded packet; ordinary contributors may propose work without pretending it is approved.
3. A small-change path and the escalation categories: defect, clarification, dependency change, and scope proposal.
4. Branch/commit/pull-request expectations without claiming unconfigured enforcement or inventing a mandatory commit syntax.
5. Required change descriptions: what changed, why, user-visible effect, verification performed, files affected, dependency/license impact, data/fixture impact, limitations, and linked authority.
6. Tests and documentation as part of delivery, while acknowledging that executable commands will be added by P0-EP04 through P0-EP06.
7. No secrets, credentials, tokens, personal data, sensitive data, absolute user paths, environments, caches, build output, or transient artifacts in commits.
8. Dependency additions and updates must follow the accepted D0.6 license, vulnerability, lockfile, and review policy; no unreviewed auto-merge.
9. Fixtures must follow D0.7; external or sensitive datasets may not enter through convenience.
10. A link to the decision-record convention and when a durable record is required.
11. A link to `SECURITY.md` and a warning not to disclose vulnerabilities publicly.
12. No CLA, DCO, code-of-conduct promise, release cadence, service-level objective, or maintainer response-time commitment unless separately approved.

### 8.4 `SECURITY.md`

The security policy must:

1. State that there is no released or supported product version yet.
2. Distinguish ordinary bugs/features from security vulnerabilities.
3. Direct ordinary non-sensitive reports to the repository's GitHub Issues page.
4. Direct sensitive reports to a verified private route. The preferred route is GitHub private vulnerability reporting at `https://github.com/Sean-V-Dev/ViDAP/security/advisories/new` if it is available at execution time.
5. Tell reporters not to include exploit details, credentials, personal data, or other sensitive evidence in public issues.
6. Request a concise description, affected area/version or commit, reproduction conditions, impact, and safe contact information.
7. Avoid promises about response or remediation time that have not been approved.

A placeholder such as `TODO`, an unverified email address, or a public-only vulnerability route fails this packet. Enabling private vulnerability reporting is a remote mutation and remains outside scope; if needed, the worker must stop for Central/user direction.

### 8.5 Decision-record area

`docs/decisions/README.md` must define a lightweight record, not a heavyweight governance subsystem. It must cover:

- when a decision record is required: consequential architecture, dependency, compatibility, security, data-governance, or scope choices with meaningful alternatives or lasting consequences;
- when one is not required: routine implementation within an accepted packet;
- immutable numeric identity and descriptive filename after acceptance;
- statuses `Proposed`, `Accepted`, `Superseded`, and `Rejected`;
- Central acceptance ownership and independent evidence where the risk warrants it;
- supersession by linking rather than rewriting history;
- relationship to the governing specification, spine, roadmap, phase plan, execution packet, and validation record; and
- an explicit statement that the existing EP01/EP02 reports and reconciliations remain authoritative and are not migrated by this packet.

`docs/decisions/0000-decision-record-template.md` must contain fields for title, ID, status, date, owners, governing requirements, context, decision, alternatives, consequences/tradeoffs, validation evidence, follow-up owners, and supersession/revisit triggers. Template instructions must be visibly distinguishable from accepted content and contain no fake project decision.

### 8.6 `.gitignore`

The ignore policy must be organized with comments and cover at least:

- environment and secret files, while allowing a deliberately created example template in a later packet;
- Python virtual environments, bytecode, type/lint/test caches, coverage, packaging, and build output;
- Node dependencies, package-manager caches, frontend build/cache output, test coverage, and logs;
- IDE/OS-local metadata not governed by `.editorconfig`;
- local datasets and downloaded data;
- transient reports, temporary directories, and repository-local mutable state;
- project-specific local state under `.vidap-local/`; and
- generated fixture subareas while leaving approved committed fixtures possible.

The file must not ignore authoritative manifests, lockfiles, source, tests, documentation, the root `fixtures/` area wholesale, or the authorized EP03 artifacts. Representative ignore behavior must be tested without creating ignored residue in the workspace.

### 8.7 `.gitattributes`

The line-ending policy must:

- normalize text in Git;
- use LF for ordinary source, configuration, Markdown, JSON, YAML, and shell text;
- permit CRLF for committed Windows-native `.cmd`, `.bat`, and `.ps1` files;
- identify common binary image/archive/font/document formats as binary where useful; and
- avoid language-specific generated-file declarations or export behavior not yet required.

The worker must explain any departure from these defaults. No file may be mass-renormalized under this packet.

### 8.8 `.editorconfig`

The editor policy must be minimal and compatible with the accepted future stack:

- `root = true`;
- UTF-8, final newline, and trailing-whitespace removal by default;
- spaces rather than tabs;
- LF by default, with Windows-native script exceptions aligned to `.gitattributes`;
- two-space indentation for JavaScript/TypeScript, JSON, YAML, CSS, HTML, and Markdown-oriented content where indentation applies;
- four-space indentation for Python and PowerShell; and
- preserved intentional trailing spaces in Markdown.

Do not add IDE-specific settings, formatter duplication, maximum-line-length policy, or code-style rules owned by P0-EP05.

### 8.9 Generated and local-state location contract

The README and/or contribution guide must state:

- `.vidap-local/` is the reserved repository-local home for untracked developer/runtime state when a later packet genuinely needs such state;
- build, test, coverage, environment, package-cache, and downloaded-data paths are untracked and governed by `.gitignore`;
- tracked fixture content is allowed only under the accepted D0.7 policy, while generated/local fixture subareas remain ignored;
- later packets must name new generated or mutable paths and update ignore/documentation rules in the same change; and
- secrets may not be stored in `.vidap-local/` merely because it is ignored; approved secret-handling mechanisms are still required.

This contract reserves safe locations but does not create runtime persistence semantics, databases, datasets, fixture content, or generated directories.

---

## 9. Permitted Scope

The worker may:

1. Read governing documents and current repository/remote metadata.
2. Verify current official MIT and GitHub reporting guidance when necessary.
3. Create the exact Section 7 files and directory parents.
4. Link to the existing GitHub repository, Issues page, and verified private vulnerability-reporting route.
5. Use Git read-only commands and local text-search/check commands.
6. Use temporary paths outside the repository when a verification genuinely requires them, and remove only those exact worker-created temporary paths.
7. Return a blocker instead of publishing misleading guidance.

---

## 10. Prohibited Scope

The worker must not:

1. Create or edit application source, component shells, manifests, lockfiles, runtime pins, task scripts, tests, fixtures, workflows, dependency-bot files, issue templates, or release automation.
2. Install or execute Node, Python, package-manager, formatter, linter, test, build, license, vulnerability, or application tools.
3. Create setup, build, test, launch, dependency, or license commands before their owning packets implement them.
4. Change remote settings, enable features, create issues/PRs/releases, alter branch protection, or add secrets.
5. Stage, commit, push, rebase, reset, clean, or rewrite Git history.
6. Relocate or rewrite the approved specification, spine, roadmap, phase plan, prior packets, decision reports, or reconciliation records.
7. Introduce product semantics, workflow/node contracts, APIs, persistence design, telemetry, hosted services, authentication, deployment, or cross-platform support claims.
8. Add speculative community machinery such as a CLA, DCO, code of conduct, governance board, funding policy, maintainer hierarchy, or release policy.
9. Add third-party content, logos, badges, screenshots, generated legal notices, or dependency inventories.
10. Modify unrelated user work, even to improve consistency or formatting.

---

## 11. Required Execution Sequence

After approval, the worker must:

1. Read every governing input in Section 3 and the approved packet in full.
2. Capture branch, commit, worktree status, remote identity, and output-path collision checks.
3. Stop if authority, prerequisites, repository identity, output ownership, or a private security-reporting route is unresolved.
4. Draft the root README, contribution guide, and security policy against the current pre-scaffold state.
5. Create the canonical MIT license.
6. Create the lightweight decision-record guide and template without moving prior records.
7. Create `.gitignore`, `.gitattributes`, and `.editorconfig` as one coherent local-state/text-policy set.
8. Cross-check every internal link and every statement about current versus future capability.
9. Run the Section 12 verification without installing tools or creating repository residue.
10. Create `ViDAP_P0_EP03_Implementation_Report.md` with exact evidence, limitations, and validator handoff.
11. Perform a final Git/file-scope inspection proving that only Section 7 paths changed during execution.
12. Stop. Do not validate, self-accept, update governing status documents, or begin P0-EP04.

---

## 12. Required Verification and Evidence

Verification is structural and policy-focused because this packet introduces no executable project.

### 12.1 Required checks

The worker must record exact commands and results for:

1. `git status --short --branch`, `git rev-parse HEAD`, and sanitized `git remote -v` at start and finish.
2. Existence and non-empty checks for all Section 7 outputs.
3. A path-scope comparison proving no other worker-created path exists.
4. `git diff --check` for whitespace errors.
5. Internal Markdown link-target checks for every repository-relative link added by EP03.
6. A case-insensitive placeholder scan for `TODO`, `TBD`, `FIXME`, example email domains, and template filler outside the clearly marked decision template instructions.
7. A scan for absolute local paths, credentials, tokens, private keys, and copied sensitive data, reporting the patterns used without printing any discovered secret value.
8. `git check-ignore -v --no-index` or an equivalent non-creating check for representative paths in every required ignore category.
9. Negative ignore checks proving `package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`, representative source/test/docs paths, `fixtures/approved.json`, and all EP03 files are not ignored.
10. `git check-attr` or equivalent checks for representative Markdown, TypeScript, Python, PowerShell, shell, JSON/YAML, and binary paths.
11. Direct comparison of `LICENSE` with the canonical MIT text aside from the approved copyright line.
12. A verification that the ordinary Issues route and the private security-reporting route correspond to the current repository identity, without changing remote state.

### 12.2 Review questions

The report must also answer:

- Does a new visitor know the project is not yet runnable?
- Can a contributor find the authority chain and determine that execution needs an approved packet?
- Can a reporter distinguish public bugs from private vulnerabilities?
- Do ignore rules protect OneDrive-synchronized work without hiding authoritative project files?
- Do `.gitattributes` and `.editorconfig` agree?
- Does the decision convention preserve history without becoming a parallel governance system?
- Did the worker avoid all P0-EP04 and later work?

No new dependency or validation tool may be installed merely to answer these questions.

---

## 13. Implementation Report Contract

The sole execution-evidence file is:

`ViDAP_P0_EP03_Implementation_Report.md`

It must contain:

1. Packet identity, approval/version, date, worker role, and authority read.
2. Starting branch, commit, sanitized remote, and pre-existing worktree changes.
3. Exact created/modified path list mapped to Section 7.
4. Plain-English summary of each artifact and its practical effect.
5. Security-route verification and any limitations.
6. Ignore/attribute/editor policy test matrix with positive and negative cases.
7. Internal-link, placeholder, sensitive-content, whitespace, and license checks.
8. EP03-AC01 through EP03-AC24 self-assessment, explicitly labeled as worker self-assessment.
9. Deviations, findings, blockers, and approved exceptions; use `None` when absent.
10. Confirmation that no tool installation, runtime execution, remote mutation, staging/commit/push, scaffold, manifest, lockfile, workflow, fixture, source, or EP04 work occurred.
11. Final Git/file-scope evidence distinguishing pre-existing changes from worker changes.
12. Independent-validation readiness and exact handoff.

The report may summarize command output; it must not embed secrets, machine-specific absolute user paths, or irrelevant logs.

---

## 14. Acceptance Criteria

P0-EP03 may be accepted only when:

- **EP03-AC01:** Authorization, prerequisites, baseline, repository identity, and pre-existing work are accurately recorded.
- **EP03-AC02:** Only the Section 7 paths were created or modified by the worker.
- **EP03-AC03:** `LICENSE` contains the canonical MIT text and approved copyright line without added terms.
- **EP03-AC04:** The README accurately explains purpose, current non-runnable status, planned architecture, accepted prerequisites, scope, and navigation without overclaiming.
- **EP03-AC05:** README links resolve to the governing and contributor-facing artifacts present in the repository.
- **EP03-AC06:** Contribution guidance preserves the authority/approval model while remaining usable by an ordinary contributor.
- **EP03-AC07:** Contribution guidance covers evidence, tests/docs, dependencies, licenses, data/fixtures, secrets, generated state, and escalation without inventing enforcement.
- **EP03-AC08:** Ordinary issue reporting uses the correct repository route.
- **EP03-AC09:** Sensitive vulnerability reporting uses a verified private route and explicitly prohibits public disclosure of sensitive details.
- **EP03-AC10:** Security guidance makes no unsupported version, response-time, or remediation promise.
- **EP03-AC11:** The decision-record guide is lightweight, defines need/status/ownership/supersession, and does not displace the governing artifact chain.
- **EP03-AC12:** The decision template is complete, reusable, clearly instructional, and contains no fake accepted decision.
- **EP03-AC13:** `.gitignore` covers secrets, environments, caches, local data, build/test output, temporary state, and `.vidap-local/`.
- **EP03-AC14:** `.gitignore` leaves manifests, lockfiles, source, tests, approved fixtures, documentation, and EP03 artifacts trackable.
- **EP03-AC15:** `.gitattributes` defines coherent text normalization, Windows-script exceptions, and binary handling without renormalizing existing files.
- **EP03-AC16:** `.editorconfig` agrees with `.gitattributes` and defers formatter-owned code style to P0-EP05.
- **EP03-AC17:** Generated and mutable local-state locations are documented without creating future persistence semantics or storing secrets.
- **EP03-AC18:** Internal links, whitespace, placeholders, absolute-path, and sensitive-content checks pass.
- **EP03-AC19:** No application source, component shell, manifest, lockfile, runtime pin, test, fixture, CI/dependency-bot file, or product behavior is introduced.
- **EP03-AC20:** No dependency/tool installation, remote mutation, Git staging/commit/push, or unrelated-file modification occurs.
- **EP03-AC21:** The implementation report contains reproducible evidence and distinguishes worker changes from pre-existing work.
- **EP03-AC22:** No unresolved critical or high-severity policy/safety finding remains; lesser findings are resolved or explicitly returned to Central.
- **EP03-AC23:** A fresh validator confirms the packet, governing requirements, file scope, content accuracy, route validity, and verification evidence.
- **EP03-AC24:** Independent validation returns `Accept`, and Central explicitly accepts the baseline before the packet is marked complete or P0-EP04 is drafted.

---

## 15. Stop and Escalation Conditions

Stop without partial publication and return evidence to Central if:

1. This packet is not explicitly approved or its approved content differs from the file being executed.
2. P0-EP01 or P0-EP02 is no longer complete or an accepted decision is in conflict.
3. An authorized output path already exists with content whose ownership is unclear.
4. The repository identity or public issue route has changed.
5. No verified private vulnerability-reporting route is available without remote mutation.
6. The canonical MIT license holder line requires a different legal identity than the approved `ViDAP contributors` wording.
7. A required policy would need a manifest, source file, workflow, remote setting, dependency, or other prohibited output.
8. Ignore rules cannot safely separate local/generated state from tracked future inputs without preempting a later design decision.
9. Verification exposes a credential, sensitive information, or unrelated user data; do not reproduce the value.
10. Any command would overwrite, delete, stage, commit, reset, clean, or otherwise alter unrelated work.
11. The practical solution requires broader community governance or later-phase architecture not approved here.

Classify the return as a defect, clarification, dependency change, or scope proposal where applicable.

---

## 16. Independent Validation Contract

Validation occurs in a fresh chat after the worker stops. The validator must read the governing inputs, this approved packet, every Section 7 artifact, and the implementation report.

### Validator tasks

The validator must independently:

1. Verify approval, prerequisites, current repository identity, and file scope.
2. Check the MIT license text and copyright line.
3. Challenge the README for status, architecture, platform, prerequisite, feature, and setup overclaims.
4. Check contribution guidance against the authority chain, accepted D0.1-D0.7 policies, and Phase 0 exclusions.
5. Verify the ordinary issue route and private vulnerability route without changing remote state.
6. Review decision-record rules for proportionality, traceability, ownership, and preservation of existing records.
7. Independently exercise representative positive and negative `.gitignore` cases.
8. Independently inspect `.gitattributes` and `.editorconfig` consistency and representative attributes.
9. Re-run or independently reproduce link, whitespace, placeholder, absolute-path, sensitive-content, and path-scope checks.
10. Confirm no EP04/later work, remote mutation, tool installation, staging, commit, or push occurred.
11. Map evidence to EP03-AC01 through EP03-AC24.
12. Return exactly one verdict: `Accept`, `Revise`, or `Blocked`, with criterion-linked findings and severity.

### Authorized validator output

The validator may create only:

`ViDAP_P0_EP03_Validation_Report.md`

Alternatively, the validator may return the identical structured report in chat for Central to preserve. It must not edit the implementation, packet, governing files, remote state, or any other file.

The validation report must contain the verdict, scope, commands/evidence, acceptance-criterion matrix, findings with IDs/severity/owner, file-scope conclusion, and an explicit statement that the validator did not accept the packet for Central or begin P0-EP04.

---

## 17. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute the approved `ViDAP_P0_EP03.md` as the bounded implementation worker. Read every governing input and follow the packet exactly. Create only the Section 7 repository-baseline artifacts and `ViDAP_P0_EP03_Implementation_Report.md`. Verify all required policy behavior without installing tools, mutating remote settings, staging or committing, or touching unrelated files. Do not create manifests, lockfiles, source, tests, fixtures, workflows, dependency-bot configuration, or P0-EP04 work. Do not validate or accept your own work. Stop with the implementation report and independent-validation handoff.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P0_EP03.md`. Read its governing inputs, all authorized implementation artifacts, and `ViDAP_P0_EP03_Implementation_Report.md`. Follow Section 16 exactly and independently check every EP03-AC01 through EP03-AC24 criterion, including repository routes, ignore/attribute behavior, file scope, and absence of P0-EP04 work. Create only `ViDAP_P0_EP03_Validation_Report.md`, or return the identical structured report in chat. Do not edit implementation or governing files, change remote state, accept for Central, or begin P0-EP04. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 18. Evidence Return to Central

The worker must return:

- implementation-report path;
- exact authorized file list;
- starting and final branch/commit/worktree evidence;
- security-route result;
- structural/policy verification results;
- EP03-AC01 through EP03-AC24 self-assessment;
- findings, deviations, exceptions, and blockers; and
- independent-validation readiness.

The validator must return the Section 16 report. Central will preserve the actual verdict, reconcile findings, accept or return the baseline, and update packet/roadmap status. Neither worker nor validator may perform Central reconciliation.

---

## 19. Next Action After Completion

P0-EP03 is complete. Independent validation returned `Accept`, and Central accepted the repository baseline in `ViDAP_P0_EP03_Validation_and_Reconciliation.md` on 2026-09-17. Central may now draft P0-EP04 as a separate bounded packet. This completion does not authorize P0-EP04 execution, dependency installation, application scaffolding, or product implementation.
