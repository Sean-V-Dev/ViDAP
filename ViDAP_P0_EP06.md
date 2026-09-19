# ViDAP P0-EP06 - CI, Dependency, and License Controls

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.4 |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisites | P0-EP01 through P0-EP05 - Complete |
| Prerequisite reconciliations | `ViDAP_P0_EP01_Validation_and_Reconciliation.md`; `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP03_Validation_and_Reconciliation.md`; `ViDAP_P0_EP04_Validation_and_Reconciliation.md`; `ViDAP_P0_EP05_Validation_and_Reconciliation.md` |
| Workstream | WS0.5 - CI and dependency controls |
| Packet type | Bounded local controls, repository workflow configuration, and evidence implementation |
| Created | 2026-09-18 |
| Revised | 2026-09-19 after literal scanner-identity correction to Decision Record 0004 |
| Owner | Central |

---

## 1. Authorization Boundary

Version 0.1 stopped correctly at the license gate. Version 0.2 established the
bounded controls, but independent review correctly required its generic Python
metadata claims to remain fail-closed. Decision Record 0004 now provides an
exact, user-authorized Central disposition for those seven locked claims.
The v0.3 worker correctly stopped because three Record 0004 entries used lock
project names rather than the scanner's literal installed-metadata names. This
v0.4 amendment corrects only those three record keys; it adds no name-
normalization rule. Version 0.4 received fresh explicit user approval on
2026-09-19; no approval of an earlier version carried forward.

After approval, one fresh bounded worker may modify only the Section 7 remedial
paths, implement the literal Record 0004 catalog beside the existing Record
0003 catalog, update the related public guidance, run the local controls, and
update the implementation report. This amendment must not alter a manifest,
lock, workflow, Dependabot policy, or any other existing control behavior.
Independent validation and Central reconciliation were completed on
2026-09-19 in `ViDAP_P0_EP06_Validation_and_Reconciliation.md`. P0-EP06 is
`Complete`.

Approval would not authorize repository-settings changes, branch protection, required-check enforcement, Secrets, remote workflow dispatches, commits, pushes, releases, fixtures, a shell, browser automation, server/process startup, APIs, workflow semantics, data/ML behavior, Dependabot UV updates, auto-merge, or P0-EP07 and later work.

---

## 2. Plain-English Packet Intent

### What this packet will change

This packet makes the accepted local quality harness repeatable in GitHub Actions on Windows, and makes the actual locked npm and Python dependency graphs reviewable for inventory, licenses, and current vulnerability advisories. It adds a narrowly configured Dependabot policy for npm and GitHub Actions only.

### What it will not claim

The worker cannot create a GitHub-hosted run because it may not commit, push, or dispatch a workflow. The created workflow is static repository configuration only. Hosted-run evidence is an external gate that the user may supply after normal repository review/commit activity; it is required for P0-EP06 completion but is not a reason for the worker to mutate remote state.

This packet does not create a product, a service, an API, a shell, a fixture, browser testing, a coverage threshold, an SBOM, an automatic update/fix workflow, or legal advice. Scanner output is evidence for human triage, not proof of safety or exploitability.

---

## 3. Governing Inputs and Traceability

The worker and validator must read these sources in authority order:

1. Current explicit user direction approving this exact packet version, if given.
2. `ViDAP_Overview.txt`, especially OV §§9, 18-23, and 25-30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.1, especially invariants 5, 7, 11, 12, and 15.
4. `ViDAP_Roadmap.md` version 1.1, especially Phase 0 and the dependency/licensing track.
5. `ViDAP_Phase_0_Plan.md` version 1.0, especially WS0.5, P0-EP06, P0-AC04, P0-AC08-P0-AC09, and P0-AC11.
6. `ViDAP_P0_EP02_Validation_and_Reconciliation.md` and `ViDAP_P0_EP02_Decision_Report.md`, authoritative for D0.5-D0.6, including the revised lock-faithful Python advisory procedure.
7. `ViDAP_P0_EP03_Validation_and_Reconciliation.md`, authoritative for repository and security-reporting hygiene.
8. `ViDAP_P0_EP04_Validation_and_Reconciliation.md`, authoritative for Windows/Node/uv baseline and the elevated-uv environment distinction.
9. `ViDAP_P0_EP05_Validation_and_Reconciliation.md` and decision record `docs/decisions/0001-ep05-frontend-quality-compatibility.md`, authoritative for the quality task baseline and JSX-a11y deferral.
10. `ViDAP_P0_EP06_License_Graph_Review.md` and accepted decision record `docs/decisions/0003-ep06-locked-license-disposition.md`, authoritative for its existing locked-graph license dispositions only.
11. `ViDAP_P0_EP06_Generic_License_Review.md` and accepted decision record `docs/decisions/0004-ep06-generic-license-metadata-disposition.md`, authoritative only for the seven literal Python package/version/gate-value dispositions recorded there.
12. This packet.

This packet implements D0.5 and D0.6's Q10-Q13 only. Q09, controlled fixtures, shell startup, and cross-process smoke remain P0-EP07; P0-EP08 owns fresh-environment phase validation.

---

## 4. Inherited Decisions and Non-Negotiable Constraints

1. Windows is the only supported platform. `windows-latest`, PowerShell, Node 24/npm, uv-managed CPython 3.14, and root `npm.cmd run` tasks are the CI and contributor paths.
2. `package.json`/`package-lock.json` and `python/pyproject.toml`/`python/uv.lock` remain the only manifest and lock authorities. `npm ci` and `uv sync --locked` are the only normal installation paths.
3. The existing root tasks (`setup`, `format:check`, `lint`, `typecheck`, `test:unit`, `test:integration`, `coverage`, `build`, and `check`) remain authoritative. CI calls them; it must not reimplement, skip, repair, or replace their behavior.
4. CI uses GitHub Actions with pull-request-to-`main`, `main` push, manual, and weekly scheduled triggers; top-level `permissions: contents: read`; no secrets; safe lock-keyed caches; full-commit-SHA-pinned third-party actions with release comments; and cancellation only for superseded PR runs.
5. The only direct control tools introduced here are `license-checker-rseidelsohn` for the locked npm graph and `pip-licenses` plus `pip-audit` for the locked Python graph. Versions, licenses, maintenance, Node 24/Python 3.14/Windows support, and peer compatibility must be rechecked from primary sources before installation.
6. License automation must fail on unknown, missing, ambiguous, custom, prohibited, or unreviewed-review-required licenses. D0.6 governs only as amended by accepted Records `0003` and `0004`; their literal package/version/license-or-gate-value dispositions are pre-existing Central policy, not worker-created exceptions.
7. Advisory controls use `npm audit --json` and the exact D0.6 `uv export --locked --all-extras --all-groups --no-emit-project --format requirements.txt` to hashed requirements followed by `pip-audit --require-hashes --disable-pip --strict`. `pip-audit --locked`, `npm audit fix`, `pip-audit --fix`, floating resolution, hand-maintained requirements files, and lock rewriting are prohibited.
8. CI Python-audit steps independently derive only `RUNNER_TEMP\vidap-pip-audit`; they do not use `GITHUB_ENV`, a carried environment variable, checkout output, a cache key, or a broad deletion target. Local override behavior must be normalized, system-temp-bounded, expected-name constrained, new-only, and fail closed exactly as D0.6 specifies.
9. Dependabot is configured weekly for npm and GitHub Actions only, with no auto-merge, at most two open PRs per ecosystem, patch/minor development-tool grouping only within an ecosystem, and individually reviewable majors/security updates. Dependabot UV updates are prohibited in P0.
10. P0 has no SBOM, unmanaged license exception, ignored permanent report, coverage threshold, browser test, remote setting change, product dependency, or user-visible product behavior. Records `0003` and `0004` are the only current Central license dispositions and do not authorize a distribution notice bundle.
11. The `SSL_CERT_DIR` note in the EP05 reconciliation is a host-environment constraint. Before any network-backed audit/install evidence, the worker must verify that the invoked normal/elevated uv path has usable certificate trust with no invalid-certificate warning. It must stop with a host-environment blocker rather than weaken TLS or alter project/system certificate configuration.

---

## 5. Preconditions and Stop Gates

Before changing a file, the worker must confirm and record:

1. This packet is explicitly approved and matches its approved version.
2. P0-EP01 through P0-EP05 remain complete and their reconciliation records are present.
3. Current branch, commit, sanitized remote, pre-existing worktree changes, and collisions with every Section 7 path.
4. Node 24/npm and elevated uv/CPython 3.14 are callable; the restricted sandbox's known WinGet uv access denial must be retried through the normal Windows path before a project prerequisite failure is claimed.
5. `npm.cmd run setup`, `npm.cmd run check`, `npm.cmd run coverage`, and `npm.cmd run build` succeed with unchanged locks before the intentional control-tool change.
6. The normal/elevated uv path has no invalid `SSL_CERT_DIR` or certificate-trust warning for a harmless primary-source network operation needed by the selected controls. Do not suppress certificate verification or change persistent user/system settings.
7. Current primary sources establish compatible maintained releases for `license-checker-rseidelsohn`, `pip-licenses`, `pip-audit`, and every selected GitHub Action; official action commits and release provenance are available for full-SHA pins.
8. No existing license exception, dependency-policy, workflow, Dependabot, or control-script file conflicts with the Section 7 path set.
9. A worker-created temporary location outside the repository and OneDrive is available for clean-copy and intentional control-failure evidence.

Stop and return evidence to Central if a required direct tool/action is incompatible, unmaintained, license-unclear, cannot be SHA pinned, requires a peer override or global tool, exposes a prohibited license without an existing exception, needs a secret/remote mutation, cannot preserve lock authority, needs an unsafe cleanup, or needs a product capability.

---

## 6. Objective and Completion Condition

### Objective

Implement the accepted Windows CI parity, locked dependency inventory/license/advisory controls, and restricted Dependabot configuration as reviewable, non-product repository controls.

### Completion condition

P0-EP06 is complete only when:

1. The worker creates/modifies only the Section 7 path set.
2. EP06-AC01 through EP06-AC36 pass or an unresolved condition is returned to Central.
3. A fresh independent validator returns `Accept`, including static workflow/cleanup/action-pin review and real control-task evidence.
4. At least one user-authorized hosted Windows workflow run is available for the validator after normal repository review/commit activity; it demonstrates the configured root-task parity and bounded artifact/cleanup behavior without the worker having made remote changes.
5. Central reconciles the result and marks P0-EP06 `Complete`.

---

## 7. Exact Authorized Outputs

Version 0.4 is a remedial amendment. The worker may modify only these existing
paths; it may not create a new path:

| Path | Authorized purpose |
|---|---|
| `scripts/dependency-controls.ps1` | Add only the seven literal Decision Record 0004 catalog entries to the existing fail-closed license control, without changing audit, cleanup, inventory, or workflow behavior. |
| `docs/dependency-controls.md` | Accurately identify Records 0003 and 0004 as the only literal license-disposition catalogs. |
| `README.md` | Update the control-policy reference to include Record 0004 without broadening claims. |
| `CONTRIBUTING.md` | Update the contributor policy reference to include Record 0004 without broadening claims. |
| `ViDAP_P0_EP06_Implementation_Report.md` | Record the remedial worker evidence, exact seven matches, unchanged locks, and hosted-run status. |

The worker may read, but must not modify, the existing workflow, Dependabot
policy, manifests, both locks, decision records, review reports, or any other
file. It must not create a fixture, source/test file, browser configuration,
CSS/design file, application shell, API route, health endpoint, server/process
script, `requirements*.txt`, package/lock alternative, Python
export/requirements authority, SBOM, license exception, branch-policy
configuration, secret, remote setting, or P0-EP07/later output.

---

## 8. Required Control Contract

### 8.1 Root dependency-control tasks

`package.json` must add exactly these public root task names without changing the existing quality-task contract:

| Task | Required behavior |
|---|---|
| `deps:inventory` | Uses only the locked installed npm and uv environments to print reviewable direct/transitive inventory facts; does not resolve, install, write a tracked report, or update a lock. |
| `license:check` | Runs the selected local Node and Python license tools, evaluates the D0.6 categories, produces clear package/path/license diagnostics, and fails closed for unapproved findings. |
| `deps:audit` | Runs `npm audit --json` and the D0.6 lock-faithful Python audit. It preserves scanner nonzero results and does not repair, resolve, or rewrite locks. |

The tasks may dispatch only to the local locked PowerShell control script using a no-profile, process-local Windows invocation. They must not require a persistent PowerShell policy change, `npx`, global installation, a different package manager, or an external service other than the configured official advisory registries.

### 8.2 Control-script safety and output

`scripts/dependency-controls.ps1` must:

- expose a narrow explicit mode for each public task and reject unknown modes/arguments;
- derive inventory and license facts only from `npm ci`/`uv sync --locked` installed graphs and the authoritative locks;
- make the exact D0.6 Python audit sequence the only Python advisory path, preserving hashes, disabling pip resolution, and excluding only the first-party project from export;
- use a newly created, bounded directory for temporary requirements, HTTP cache, and audit JSON; reject pre-existing, reparse-point, non-directory, checkout, OneDrive, or unbounded deletion targets;
- honor `VIDAP_AUDIT_DIR` locally only when it is a newly absent `vidap-pip-audit-<32 lowercase hex>` child of the resolved system temporary directory; ignore it in CI;
- in CI, independently derive `RUNNER_TEMP\vidap-pip-audit` for audit, artifact, and cleanup; write only `pip-audit.json` there for the brief artifact window; and
- print concise sanitized summaries, preserve scanner exit status, and remove local temporary output in `finally`. It must never print environment dumps, secrets, absolute user paths, or copied lockfile bodies.

No cleanup may recursively delete a path unless it first confirms the exact computed bounded directory, existence, directory type, and absence of a reparse point. The live repository is never a cleanup target.

### 8.3 License policy implementation

The implementation must retain D0.6 as amended only by accepted decision
records `docs/decisions/0003-ep06-locked-license-disposition.md` and
`docs/decisions/0004-ep06-generic-license-metadata-disposition.md`; it must
not invent a new policy:

- allow SPDX-identified MIT, BSD-2-Clause, BSD-3-Clause, ISC, Apache-2.0, 0BSD, Zlib, PSF-2.0, and CC0-1.0 when required notices can be retained, plus exact SPDX MIT-0;
- permit only the exact versioned normalization and bounded exception catalogs in Records `0003` and `0004`; each match must emit its package, version, license or gate value, record ID, restricted role, and distribution re-review trigger;
- permit Record `0004` only for its seven literal package/version/gate-value keys. Its generic labels and embedded Apache text must not become a general normalization rule;
- treat a generic BSD label, a generic `MIT License`/Apache/PSFL label, an `A OR B` expression, an `AND` expression, MPL, BlueOak, CC-BY, native/platform material, and data material as unapproved unless that exact package/version/license-or-gate-value is in Record `0003` or `0004`'s catalog;
- fail closed on normally prohibited GPL-only, AGPL, SSPL, Commons-Clause/BUSL/non-commercial/no-derivatives terms, unlicensed packages, and missing/ambiguous/custom claims;
- fail closed as review-required on MPL, EPL, LGPL, CDDL, Artistic, Unicode/data, multi-license, platform-binary, material-notice, or generated/native cases unless the exact Record `0003` or `0004` catalog entry matches; and
- report source/tool limitations and state that automated classification is not legal advice.

The control may not use ranges, prefixes, wildcard matching, or inferred roles
for either record's entries. A changed version, license, gate value, or role; a
new package; or any unlisted finding must fail closed. In particular, the
worker must not parse a future package's license file to normalize its metadata
at runtime. Do not create or edit an exception record, placeholder, or
distribution notice bundle. Notices/reports remain review evidence, not an
SBOM.

### 8.4 CI workflow contract

The workflow must have only:

- `pull_request` to `main`, `push` to `main`, `workflow_dispatch`, and a weekly schedule;
- `permissions: contents: read` and no secret consumption, write token use, `pull_request_target`, deployment/release, self-hosted runner, matrix, container, Docker action, or reusable workflow;
- a `quality-windows` job that uses full-SHA-pinned checkout, Node 24, uv, and cache actions with nearby release comments, runs the root locked setup, then `npm.cmd run check` and `npm.cmd run coverage`;
- a `dependency-license-windows` job that uses the same setup and runs `deps:inventory`, `license:check`, and `deps:audit` through the root tasks; and
- conditional artifact/cleanup steps only for the bounded Python advisory JSON. The upload uses an `always()` condition, has `if-no-files-found: ignore`, retains for 14 days where repository policy permits, and is followed by an `always()` bounded cleanup step.

Cache only npm download and uv package caches. Keys include runner OS, architecture when exposed, Node major/tool version, uv version, and hashes of `package-lock.json`, `pyproject.toml`, and `uv.lock`. Never cache `node_modules`, `.venv`, the workspace, reports, build output, browser binaries, or audit output. The weekly run bypasses restored caches.

Concurrency must cancel superseded pull-request runs only. `main`, manual, and scheduled runs must not be cancelled. Workflow outputs and uploaded material may never include data, fixtures, secrets, environment dumps, dependencies, environments, checkout copies, or browser/cache contents.

### 8.5 Dependabot and documentation contract

Dependabot must have two weekly update entries only: npm and GitHub Actions. Each uses a maximum of two open PRs. Only patch/minor development-tool updates may be grouped within the same ecosystem. Major and security updates stay individually reviewable. No auto-merge, UV ecosystem, Python lock update, grouping across ecosystems, or bot trust bypass is configured.

Documentation must accurately explain the local control commands, CI's parity relationship, allowed/review-required/prohibited license posture, vulnerability triage expectations, weekly/manual update posture, Dependabot restrictions, no-SBOM deferral, no-auto-fix rule, and that the private vulnerability-reporting route in `SECURITY.md` remains the security-report channel.

---

## 9. Permitted Scope

The worker may read governing artifacts and current primary sources; install only the named direct control tools through the authoritative locks; run local setup/quality/control commands; use exact temporary directories outside the repository and OneDrive for clean-copy/negative evidence; inspect Git read-only; and create only Section 7 artifacts.

The worker must return a blocker rather than weakening a license/advisory result, bypassing certificate trust, using an action tag, forcing a peer, suppressing a scanner exit, or broadening into a remote/product capability.

---

## 10. Prohibited Scope

The worker must not:

1. Change GitHub repository settings, required checks, branch protection, Actions settings, secrets, labels, advisories, Dependabot remote state, or any other remote state.
2. Commit, push, dispatch a workflow, open a pull request, merge, create a release, or claim hosted CI evidence without a user-supplied run.
3. Add Dependabot UV updates, auto-merge, a bot bypass, a secret, a write permission, floating action/tag pin, or a third-party action outside the bounded CI roles.
4. Add an SBOM, a license exception, legal advice, lockfile hand editing, audit fix, dependency update, product/ML dependency, fixture, browser test, shell, server/process, API, or product behavior.
5. Change `.gitignore`, `LICENSE`, `SECURITY.md`, runtime pins, existing quality policy, JSX-a11y deferral, decision records, or unrelated user files.
6. Write reports, exports, caches, environments, dependencies, audit output, temporary copies, or credentials into tracked paths.
7. Begin P0-EP07, P0-EP08, Phase 1, or visual-design implementation.

---

## 11. Required Execution Sequence

After approval, the worker must:

1. Read all governing inputs and record baseline branch/commit/worktree/remote/path collisions.
2. Confirm that the pre-existing workflow, Dependabot policy, manifests, and locks are outside this remedial scope; record both lock hashes before and after every command.
3. Recheck normal/elevated uv certificate trust before a network-backed operation; stop if the inherited environment is unsafe.
4. Confirm the seven literal Decision Record 0004 keys against the installed locked metadata and review; stop if any name, version, or gate value differs.
5. Update only the five Section 7 paths. The script change must add exactly the seven literal Record 0004 entries beside the existing Record 0003 catalog; it must not revise the classifier's base rules, cleanup, audit, inventory, cache, or workflow logic.
6. Run setup, every existing quality task, every control task, and prove routine commands do not change locks.
7. Demonstrate in an exact temporary copy that a Record 0004 key passes and that a changed version or gate value, an unknown/prohibited license, and an unlisted generic label fail closed. Never place an intentional failure in the live repository or use live vulnerability data as a fabricated fixture.
8. Re-inspect the existing workflow YAML/action pins and cleanup guards statically; do not edit or dispatch the workflow.
9. Demonstrate clean-copy setup, quality, and control-task behavior with isolated caches where network/advisory evidence is safely available; remove all exact temporary paths.
10. Update `ViDAP_P0_EP06_Implementation_Report.md`, perform final exact-scope/ignore/lock/whitespace/sensitive-content evidence, and stop for independent validation.

---

## 12. Required Worker Evidence

The implementation report must include:

1. Packet identity, approval/version/date, authority read, branch/commit/sanitized remote, pre-existing work, and exact worker scope.
2. Direct tool/action table: version or commit, role, primary source/retrieval date, license, support/peer evidence, action release comment, and rationale.
3. Intentional manifest/lock changes and hash invariance after setup, quality, inventory, license, audit, and build commands.
4. Root task map and actual concise results, including explicit no-fix/no-resolution behavior.
5. License inventory/category results, every Records `0003` and `0004` catalog match and its restricted role/re-review trigger, the exact seven Record 0004 keys, all remaining unapproved findings, notices/limitations, and confirmation that no worker-created exception was needed.
6. npm and Python audit commands/results, scanner limitations, and the exact safe temporary/artifact/cleanup path policy without sensitive values.
7. Workflow trigger, permission, job, cache, artifact, concurrency, action-pin, and Dependabot static evidence.
8. Clean-copy, negative-control, ignored-output, certificate-trust, and cleanup evidence.
9. Documentation accuracy, `git diff --check`, sensitive-content scan, and final scope comparison.
10. EP06-AC01 through EP06-AC36 self-assessment, clearly labeled as worker self-assessment.
11. Hosted-run evidence status, explicitly `Pending user-authorized run` unless the user supplied it without worker remote mutation.

The report must omit secrets, absolute user paths, tokens, full lockfile bodies, environment dumps, and noisy logs.

---

## 13. Acceptance Criteria

P0-EP06 may be accepted only when:

- **EP06-AC01:** Authority, prerequisites, baseline, repository identity, pre-existing work, and output collisions are accurately recorded.
- **EP06-AC02:** Only the five existing Section 7 remedial paths were modified by the worker; no path was created.
- **EP06-AC03:** Every direct control tool and action has current primary-source, license, maintenance, Node/Python/Windows/peer or commit-provenance evidence.
- **EP06-AC04:** `package-lock.json` and `python/uv.lock` remain the sole authorities and remain byte-identical throughout this remedial execution.
- **EP06-AC05:** Existing root quality tasks remain semantically unchanged and CI invokes them through `npm.cmd run` after locked setup.
- **EP06-AC06:** `deps:inventory`, `license:check`, and `deps:audit` have distinct, local, lock-respecting, no-fix roles.
- **EP06-AC07:** Inventory covers actual direct/transitive npm and Python locked graphs without creating a second authority or committed report.
- **EP06-AC08:** License checking implements the D0.6 posture as amended only by Records `0003` and `0004`, matches only their exact literal catalogs, and fails closed for every unknown, changed, unlisted, or unreviewed finding.
- **EP06-AC09:** No worker-created license exception, legal conclusion, or generated distribution notice bundle is fabricated; Records `0003` and `0004` are accurately applied without expansion or generic metadata normalization.
- **EP06-AC10:** `npm audit --json` preserves advisory evidence and nonzero results without `audit fix` or lock mutation.
- **EP06-AC11:** Python advisory input is exported from `uv.lock` with `uv export --locked --all-extras --all-groups --no-emit-project --format requirements.txt`; it retains hashes and excludes only the first-party project.
- **EP06-AC12:** Python audit uses `pip-audit --require-hashes --disable-pip --strict`, never `pip-audit --locked`, resolution, or automatic fix.
- **EP06-AC13:** Local and CI audit temporary paths, artifact handling, and cleanup are bounded, new-only/reparse-safe, deterministic, and independently derived as required by D0.6.
- **EP06-AC14:** Invalid certificate trust is a stop condition; no TLS bypass or persistent environment/system workaround is introduced.
- **EP06-AC15:** CI has only approved triggers, Windows runner, top-level read-only permissions, no secrets, and no write/deployment/reusable/container path.
- **EP06-AC16:** Every third-party action is full-SHA pinned with verified release provenance and a nearby release comment; no floating ref exists.
- **EP06-AC17:** CI cache scope/keys are lock-aware, bounded to download/package caches, and the weekly path bypasses restored caches.
- **EP06-AC18:** CI concurrency cancels superseded PR runs only; main/manual/scheduled runs remain preserved.
- **EP06-AC19:** CI artifacts are limited to the bounded Python audit JSON when available, retained for 14 days where permitted, and exclude prohibited content.
- **EP06-AC20:** Dependabot has only weekly npm and GitHub Actions entries with approved limits/grouping and no UV/auto-merge/bypass configuration.
- **EP06-AC21:** Documentation accurately describes controls, interpretation, triage, updates, Dependabot, SBOM deferral, and no-auto-fix boundaries.
- **EP06-AC22:** Local setup, all quality tasks, all control tasks, and build pass from locked environments; the hosted Windows license job no longer fails for any of the seven exact Record 0004 keys.
- **EP06-AC23:** Representative isolated negative controls fail safely for unsafe audit path, license classification, and preserved advisory failure behavior.
- **EP06-AC24:** Clean-copy reproduction uses isolated state, leaves no residue, and does not rely on cache as proof.
- **EP06-AC25:** Generated dependency, audit, report, cache, coverage, build, and temporary state remain ignored/untracked.
- **EP06-AC26:** No CI-hosted-only quality substitute, global dependency, second package manager, PowerShell policy mutation, network trust bypass, or second authority is introduced.
- **EP06-AC27:** No fixture, browser, shell, process, route, API, workflow/schema, data/ML, product, P0-EP07, or later work is introduced.
- **EP06-AC28:** No remote mutation, staging, commit, push, branch-protection change, secret, or unrelated file modification occurs.
- **EP06-AC29:** Text/YAML/configuration links, whitespace, sensitive-content scan, and `git diff --check` pass.
- **EP06-AC30:** The implementation report is reproducible, sanitized, and distinguishes worker changes, pre-existing changes, and externally pending hosted-run evidence.
- **EP06-AC31:** Current dependency results are correctly described as inventory/advisory evidence, not a safety guarantee or exploitability/legal conclusion.
- **EP06-AC32:** No unresolved critical/high compatibility, security, supply-chain, license, or safety finding remains; lesser findings are resolved or returned to Central.
- **EP06-AC33:** A fresh validator independently checks source claims, actual controls, lock invariance, safe failure/cleanup, static workflow/action/Dependabot content, scope, and absence of later work.
- **EP06-AC34:** A user-authorized hosted `windows-latest` run, created without worker remote mutation, proves root-task parity, bounded artifact behavior, and cleanup; failures have actionable evidence.
- **EP06-AC35:** Independent validation returns `Accept` after hosted-run evidence is available.
- **EP06-AC36:** Central explicitly accepts the controls before P0-EP07 is drafted.

---

## 14. Independent Validation and External-Evidence Boundary

The validator must independently inspect all governing inputs, Section 7 artifacts, direct package/action metadata, both locks, actual local quality/control results, negative-control evidence, cleanup guards, workflow syntax/pins, Dependabot policy, documentation, exact scope, and prohibited-scope absence. It must reproduce safe local controls and use normal/elevated uv only after confirming certificate trust.

The validator must not edit implementation/governing files, dispatch CI, alter GitHub settings, accept for Central, or begin P0-EP07. It may inspect a user-supplied hosted workflow run and its permitted artifact/log evidence. If no hosted run exists, it must return `Blocked` for EP06-AC34/AC35 while retaining the static/local findings; it must not treat a locally passing workflow-like command as hosted proof.

The validation report must return one verdict (`Accept`, `Revise`, or `Blocked`), criterion-linked findings with severity/owner, direct dependency/action evidence, local/hosted command evidence, lock hashes, cleanup/artifact conclusion, file-scope conclusion, and an explicit statement that the validator did not accept for Central or begin P0-EP07.

---

## 15. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute freshly approved `ViDAP_P0_EP06.md` version 0.4 as the bounded remedial license-control worker. Read every governing input, especially D0.5-D0.6, both EP06 license reviews, and accepted decision records `0003` and `0004`. Modify only the five existing Section 7 remedial paths; do not create any file or alter manifests, locks, workflow, Dependabot, or decision records. Preserve root-task authority. Add only the seven exact Record 0004 package/version/gate-value entries beside the existing exact Record 0003 catalog. In particular, use `pip_api`, `pip_audit`, and `tomli_w` as literal scanner names—do not transform names in either direction. Do not add ranges, wildcard matching, inferred roles, generic-label normalization, runtime license-text parsing, policy expansion, a new exception record, or a notice bundle. Re-run complete locked evidence and prove locks stay identical. Stop for every changed, unknown, unlisted, or otherwise unapproved license; do not bypass TLS, force dependencies, suppress findings, dispatch CI, or mutate remote state. Do not self-validate, stage/commit/push, or begin P0-EP07. Hosted-run evidence is user-owned and may remain pending in your report.

### Independent validator prompt

> Act as the independent validator for freshly approved `ViDAP_P0_EP06.md` version 0.4. Read all governing inputs, including both EP06 license reviews and decision records `0003` and `0004`, every Section 7 artifact, and `ViDAP_P0_EP06_Implementation_Report.md`. Independently verify every Record 0004 package/version/gate-value key and its restricted role, with particular attention that `pip_api`, `pip_audit`, and `tomli_w` are literal scanner identities rather than normalized names. Confirm the seven actual locked artifacts remain as reviewed, and prove that changed versions/gate values, generic labels, and all unknown/unlisted/review-required/prohibited findings fail closed. Verify the exact five-path worker scope, lock invariance, root-task parity, actual inventory/license/advisory behavior, D0.6's hashed uv-export/pip-audit procedure, safe temporary/artifact cleanup, existing workflow/Dependabot constraints, negative controls, clean-copy evidence, and absence of P0-EP07/later work. Do not edit files, dispatch CI, alter remote state, accept for Central, or begin P0-EP07. Inspect user-supplied hosted Windows run evidence; return `Blocked` if it is absent or the license job is red. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 16. Next Action

P0-EP06 is complete. The next permitted planning action is to draft P0-EP07;
that separate packet must receive its own explicit approval before any worker
may execute it.
