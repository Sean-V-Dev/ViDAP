# ViDAP P0-EP04 - Reproducible Project Scaffold

| Field | Value |
|---|---|
| Status | Complete |
| Packet version | 1.0 |
| Approved | 2026-09-17 by explicit user direction |
| Completed | 2026-09-18 |
| Implementation report | `ViDAP_P0_EP04_Implementation_Report.md` |
| Central reconciliation | `ViDAP_P0_EP04_Validation_and_Reconciliation.md` |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisite packets | P0-EP01 through P0-EP03 - Complete |
| Prerequisite reconciliations | `ViDAP_P0_EP01_Validation_and_Reconciliation.md`; `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP03_Validation_and_Reconciliation.md` |
| Workstream | WS0.3 - Reproducible project scaffold |
| Packet type | Bounded local scaffold, dependency-lock, and build-configuration implementation |
| Created | 2026-09-17 |
| Owner | Central |

---

## 1. Authorization Boundary

This is a proposed execution packet. Drafting it does not authorize execution.

After explicit user approval, one bounded execution worker may create only the Section 7 scaffold artifacts, modify only the Section 7 documentation/policy files, install the exact repository dependencies into ignored locations as necessary to create and verify committed locks, and create the implementation report. The worker must not accept its own work. Independent validation and Central reconciliation remain required before P0-EP04 is `Complete`.

Approval does not authorize product behavior, workflow/schema semantics, APIs, datasets, fixtures, CI, dependency automation, tests, quality configuration, remote changes, commits, or P0-EP05 through P0-EP08 work.

---

## 2. Plain-English Packet Intent

### What this packet will change

This packet turns the accepted repository shape into a reproducible technical skeleton. It adds the locked JavaScript and Python project definitions, exact runtime declarations, empty ownership packages, a buildable but intentionally non-functional web entry point, and the smallest root commands needed to install the locked dependencies and build that entry point.

### Why the system needs it

Later packets need one repeatable foundation rather than each introducing its own package manager, runtime assumption, source location, or task convention. Locking the initial React/React Flow/Vite and FastAPI/Uvicorn graphs now also makes the Python 3.14-on-Windows compatibility decision real before quality tooling, CI, fixtures, or product behavior depend on it.

### What real behavior it enables

Contributors will be able to use documented Windows prerequisites to install the exact locked dependency graphs and build the intentionally empty web foundation. The repository will visibly reserve the UI, workflow, execution, experiment/state, export, test, fixture, and documentation ownership areas without pretending that those later systems exist yet.

### How success will be demonstrated

Using Node 24 LTS, uv, and a uv-managed CPython 3.14.x runtime, a fresh temporary copy can run the documented root setup command followed by the root build command. Both lockfiles remain unchanged by routine setup/build, all generated state is ignored, and no application capability beyond an empty build entry point is claimed or started.

---

## 3. Governing Inputs and Traceability

The worker must read these sources in authority order before changing anything:

1. Current explicit user direction approving this exact packet, if given.
2. `ViDAP_Overview.txt`, especially OV §§1, 9, 18, 20-22A, and 25-30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.0, especially Sections 1-3, P0, and Sections 6-7.
4. `ViDAP_Roadmap.md` version 1.0, especially P0 and its delivery tracks.
5. `ViDAP_Phase_0_Plan.md` version 1.0, especially P0-G1-P0-G7, WS0.3, deliverables 4-6, P0-AC03-P0-AC06/P0-AC11, P0-EP04, and Phase 0 guardrails.
6. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, authoritative for D0.1-D0.3 and the Python 3.14 amendment.
7. `ViDAP_P0_EP02_Validation_and_Reconciliation.md`, authoritative for D0.4-D0.7.
8. `ViDAP_P0_EP03_Validation_and_Reconciliation.md`, authoritative for repository governance and local-state rules.
9. This approved packet.

This packet advances:

- OV §§1 and 9: local-first real-library direction and MIT-compatible dependency control;
- OV §18: a later-testable foundation without pretending tests already exist;
- OV §§20-21: plain-English, modular, reproducible, minimal-hidden-state engineering;
- OV §22 and §22A: separation of browser/UI from local Python ownership without defining future contracts;
- OV §§25-30: bounded delivery, independent review, roadmap alignment, and minimal scope;
- Spine P0: selected application shape, development setup, quality entry-point foundation, and minimal component boundaries; and
- Phase 0 WS0.3 and required deliverables 4-6.

---

## 4. Inherited Decisions and Non-Negotiable Constraints

The worker must implement these accepted decisions exactly and must stop rather than silently substitute an alternative:

1. ViDAP is one MIT-licensed repository with `apps/web/` for the TypeScript/React UI and `python/` for the CPython workspace.
2. Python ownership directories are `python/src/vidap_workflow/`, `python/src/vidap_execution/`, `python/src/vidap_experiments/`, and `python/src/vidap_export/`. They reserve ownership only; they must not define workflow, execution, persistence, experiment, export, or API semantics.
3. Cross-component tests will later live under root `tests/` and Python tests under `python/tests/`; controlled shared fixtures will later live at root `fixtures/`. EP04 must not create tests or fixtures.
4. The web direction is TypeScript, React, React Flow, and Vite. The local Python direction is FastAPI with Uvicorn. The browser and Python host communicate only through a later-defined loopback boundary; EP04 must not create that boundary or start processes.
5. The Python target is CPython 3.14.x. If a mandatory direct foundation dependency lacks a compatible Windows Python 3.14 distribution, stop and return evidence for an explicit, time-bounded Python 3.13 exception. Silent fallback is prohibited.
6. Python uses one `python/pyproject.toml` and one committed `python/uv.lock`; uv is the only Python project/package tool. No `requirements*.txt`, Poetry lockfile, Conda environment, Pipenv, or competing resolver output is permitted.
7. JavaScript uses Node.js 24 LTS, bundled npm, one root `package.json`, and one committed root `package-lock.json`. No pnpm, Yarn, Bun, alternate JavaScript lockfile, or global JavaScript task package is permitted.
8. The supported development path is Windows PowerShell using `npm.cmd run <task>`. Direct `npm.ps1` use must not require a PowerShell execution-policy change. macOS/Linux remain unvalidated and must not be claimed as supported.
9. Root npm scripts are the only contributor-facing cross-stack task entry. They may invoke local binaries and `uv run --locked` or `uv --directory python ...`; they may not use `npx` downloads, a second task runner, a user-specific profile, or a global package.
10. P0-EP04 may establish only `setup`, `build`, and any narrowly necessary internal build/setup scripts. `dev`, `launch`, `check`, quality, test, audit, CI, and process-smoke tasks remain owned by later packets.
11. The EP03 ignore, attribute, editor, contribution, security, and decision-record policies remain authoritative. OneDrive-synchronized mutable state must remain ignored and no ignored location becomes an approved secret store.
12. Exact direct versions, licenses, source links, and compatibility evidence must be current primary-source evidence gathered at execution time and preserved in the implementation report. P0-EP06 later performs the full direct/transitive inventory, license verification, and advisory evidence.

---

## 5. Preconditions and Stop Gates

Before writing any scaffold artifact, the worker must confirm and record:

1. This packet is explicitly approved for execution and matches the approved version.
2. P0-EP01 through P0-EP03 remain complete and their reconciliation records are present.
3. Current branch, commit, sanitized remote URL, and all pre-existing worktree changes.
4. The current repository still has the accepted EP03 baseline and no conflicting manifest, lockfile, runtime declaration, source tree, test tree, or scaffold output.
5. Node 24 LTS with bundled npm is installed and callable via `node` and `npm.cmd`; the observed Node 25 workstation runtime is not acceptable.
6. uv is installed through an approved bootstrap path and callable without a PowerShell policy change.
7. uv can select/provision a CPython 3.14.x interpreter suitable for the intended project environment.
8. Current official primary sources support the direct foundation dependency versions selected for React, React DOM, React Flow, Vite, TypeScript, the Vite React integration, FastAPI, and Uvicorn.
9. Every selected direct dependency has a compatible permissive license under accepted D0.6 policy, current maintenance evidence, and a Windows/Python 3.14 compatibility basis where applicable.
10. Network access is sufficient to resolve/install the selected locked graphs. If it is not, stop with the exact failed operation rather than fabricating locks.
11. A temporary directory outside the repository is available for clean-copy verification. It must be an exact worker-created path and may be removed only after successful or failed verification.

The worker may use uv to provision the selected CPython interpreter as part of the approved repository setup. It must not install or alter system Node, PowerShell policy, global npm packages, containers, IDE extensions, or remote repository settings. If Node 24 or uv is absent, stop and return the prerequisite rather than altering the system.

---

## 6. Objective and Completion Condition

### Objective

Create the smallest locked, Windows-oriented scaffold that preserves the accepted UI/Python topology and proves reproducible dependency setup and web build without introducing product semantics.

### Completion condition

P0-EP04 is complete only when:

1. The worker creates only the authorized Section 7 paths and modifies only the authorized existing files.
2. EP04-AC01 through EP04-AC31 pass or an unresolved condition is returned to Central.
3. A fresh independent validator returns `Accept` under Section 16.
4. Central reconciles the result and marks P0-EP04 `Complete`.

Successful installation or a successful build is necessary evidence, not acceptance.

---

## 7. Authorized Outputs and File Ownership

After approval, the worker may create or modify only these paths:

| Path | Authorized purpose |
|---|---|
| `.nvmrc` | Exact Node 24.x runtime pin selected at execution time |
| `package.json` | Root JavaScript manifest, engines constraint, and approved root setup/build scripts |
| `package-lock.json` | Sole committed JavaScript dependency lock |
| `scripts/verify-node-version.mjs` | Local preinstall/runtime-major enforcement with clear Windows-friendly diagnostics |
| `apps/web/index.html` | Vite build document only; no product copy or workflow UI |
| `apps/web/vite.config.ts` | Minimal Vite configuration rooted at `apps/web/` with ignored build output |
| `apps/web/tsconfig.json` | Strict TypeScript build configuration only; P0-EP05 owns quality policy expansion |
| `apps/web/src/main.tsx` | Minimal React build entry that renders no product UI or semantics |
| `python/.python-version` | Exact CPython 3.14.x pin selected at execution time |
| `python/pyproject.toml` | Sole Python project metadata and direct foundation dependency declaration |
| `python/uv.lock` | Sole committed Python dependency lock |
| `python/src/vidap_workflow/__init__.py` | Empty ownership package marker with no semantic contract |
| `python/src/vidap_execution/__init__.py` | Empty ownership package marker with no host/API behavior |
| `python/src/vidap_experiments/__init__.py` | Empty ownership package marker with no persistence behavior |
| `python/src/vidap_export/__init__.py` | Empty ownership package marker with no export behavior |
| `README.md` | Accurate post-scaffold prerequisites, setup/build instructions, and status update |
| `CONTRIBUTING.md` | Accurate post-scaffold contributor commands and constraints update |
| `.gitattributes` | Minimal explicit LF treatment for new TOML/lock configuration if needed for policy alignment |
| `.editorconfig` | Minimal TOML/lock indentation treatment if needed for policy alignment |
| `ViDAP_P0_EP04_Implementation_Report.md` | Worker evidence, compatibility results, and validation handoff |

The worker may create only necessary parent directories: `scripts/`, `apps/web/src/`, `python/src/`, and the four named Python package directories. No other path is authorized.

The worker must not create `apps/web/package.json`, an npm workspace, a second lockfile, `requirements*.txt`, a Python `.venv` in a tracked location, `python/tests/`, root `tests/`, root `fixtures/`, source files beyond those listed, CSS, API routes, process-launch scripts, CI workflows, quality/test configuration, dependency-bot files, generated reports, databases, data directories, or local-state directories.

---

## 8. Required Scaffold Contract

### 8.1 Runtime declarations and locks

The worker must select the latest compatible patch releases within the accepted Node 24 and CPython 3.14 families using current primary sources, then commit:

- `.nvmrc` with the exact Node 24 patch;
- `package.json` `engines.node` limited to the Node 24 major line and a local enforcement path that rejects other majors before package installation;
- `python/.python-version` with the exact CPython 3.14 patch;
- `python/pyproject.toml` `requires-python` limited to `>=3.14,<3.15`; and
- exactly one `package-lock.json` and one `python/uv.lock` generated from those manifests.

The root JavaScript manifest must be marked private while the repository remains unpublished as a package. Neither manifest may introduce a publish, release, container, deployment, telemetry, or global-install configuration.

Routine setup must leave both locks unchanged. A lock difference after a routine setup/build is a failure unless the worker has intentionally changed a direct dependency and records the reason before regenerating the relevant lock.

### 8.2 Direct dependency boundary

The JavaScript lock may contain only the current direct foundation choices necessary for the accepted web direction:

- React and React DOM;
- React Flow's current maintained React package;
- Vite, TypeScript, and the minimal Vite/React integration and type packages required to build the empty TypeScript entry point.

The Python lock may contain only FastAPI, Uvicorn, and their necessary direct build/runtime support. No data, ML, database, HTTP-client, task-runner, test, lint, formatting, type-checking, browser-automation, vulnerability, license-inventory, or CI dependency may be added under EP04.

The worker must use current official project/package sources for exact names, versions, support windows, installation guidance, and license claims. It must record the exact direct dependencies, versions, retrieval dates, license evidence, and rationale in the implementation report. Full transitive license/advisory proof remains P0-EP06 work.

### 8.3 JavaScript scaffold and root tasks

`package.json` may expose only these public task names:

| Task | Required behavior |
|---|---|
| `setup` | Performs locked JavaScript installation and locked Python synchronization through the accepted root/npm and uv paths. It must fail clearly on missing Node 24 or uv, not repair runtimes, and not write a lockfile. |
| `build` | Builds the empty web entry point only to an ignored output directory. It must not start a server, invoke Python, create a fixture, or stand in for later type/quality/test checks. |

An internal `preinstall` hook and a narrowly named build subcommand are allowed only when necessary to make `setup`/`build` deterministic. They are implementation details, not contributor-facing task taxonomy expansion. `dev`, `launch`, `check`, `format:*`, `lint*`, `typecheck`, `test:*`, `smoke`, `deps:*`, and `license:*` must be absent; later packets own them.

`scripts/verify-node-version.mjs` must use only Node standard capabilities, report the actual and required major family, and exit nonzero before installation when Node is not 24.x. It must not download Node, edit system state, or depend on a user shell profile.

`apps/web/src/main.tsx` may mount an empty React root only as strictly required for a Vite/React production build. It must not display a branded shell, node canvas, controls, navigation, status, data, error, workflow, model, or API behavior. `apps/web/index.html` must likewise be generic build plumbing rather than a product page.

### 8.4 Python workspace and ownership markers

`python/pyproject.toml` must represent one uv-managed project and must retain the four accepted ownership packages beneath `python/src/`. It may use package-disabled/project configuration when appropriate to prevent premature distribution behavior; it must not add a build/publish configuration unless strictly needed by uv and documented.

Each `__init__.py` may contain at most a short ownership docstring. It must not expose a workflow type, FastAPI application, endpoint, startup code, database, storage layout, result type, experiment type, exporter, or third-party ML call.

FastAPI and Uvicorn are locked as the accepted future local-host foundation but are not started, configured with routes, or used to define a health/API contract in EP04. P0-EP07 owns startup proof and P1/P2/P3 own later semantic and boundary contracts.

### 8.5 Documentation and repository-policy alignment

The worker must update README and CONTRIBUTING so they accurately state:

1. Windows is the only currently supported development environment.
2. Node 24 LTS with npm and uv are prerequisites; CPython 3.14 is selected/provisioned through uv and pinned in the Python workspace.
3. The authoritative Windows commands are `npm.cmd run setup` and `npm.cmd run build`.
4. Setup installs only the committed locks and build creates only ignored output.
5. There is still no `dev`/`launch` command, application shell, workflow, API, dataset, model, test suite, CI workflow, or cross-platform support claim.
6. Lockfiles are committed authority and must not be casually regenerated or replaced.

The worker must modify `.gitattributes` and `.editorconfig` only as necessary for coherent committed TOML/lock text treatment. It must not weaken the EP03 ignore, secret, local-state, license, contribution, or security policies.

---

## 9. Permitted Scope

The worker may:

1. Read governing documents, current repository state, and current official primary sources.
2. Use network access to resolve the selected direct package graphs and retrieve primary documentation/license evidence.
3. Use Node 24/npm and uv/CPython 3.14 to create committed locks and ignored environments/dependencies/output necessary for verification.
4. Create the exact Section 7 files and update only the Section 7 existing files.
5. Run `npm.cmd run setup`, `npm.cmd run build`, lock inspection, package metadata inspection, and read-only Git checks.
6. Create a bounded temporary clean-copy directory outside the repository for verification, then remove only that exact worker-created directory.
7. Stop with concrete evidence if a compatibility, license, source, or scope gate fails.

---

## 10. Prohibited Scope

The worker must not:

1. Use Node 25 or any non-Node-24 runtime as the supported scaffold result.
2. Install Node, uv, global npm packages, global Python packages, containers, IDE extensions, or change PowerShell execution policy.
3. Add a second package manager, lockfile, manifest, requirements export, workspace manager, task runner, or shell-profile dependency.
4. Create user-visible UI, React Flow graph behavior, workflow schema, typed ports, API route, process coordination, health endpoint, persistence, run/experiment behavior, exporter, data/ML behavior, fixture, test, or CSS/design system.
5. Create a `dev` or `launch` command, start a server, open a browser, bind a port, or define a browser/Python message format.
6. Add quality, formatting, lint, typing, test, coverage, license, audit, CI, browser, dependency-bot, release, or deployment configuration.
7. Add non-foundation direct packages, including scikit-learn or any other ML/data library.
8. Change remote settings, enable GitHub features, create issues/PRs/releases, modify branch protection, or add secrets.
9. Stage, commit, push, reset, clean, rebase, or change unrelated user work.
10. Relocate or rewrite governing documents, accepted reconciliations, or EP03 baseline policy except the specifically authorized README/CONTRIBUTING and text-policy alignment edits.

---

## 11. Required Execution Sequence

After approval, the worker must:

1. Read every governing input and this packet in full.
2. Capture pre-existing branch, commit, worktree, remote, file-inventory, and Node/uv/Python facts.
3. Verify Node 24, uv, CPython 3.14 provisioning, direct-package primary evidence, direct-license compatibility, and output-path ownership before writing scaffold files.
4. Stop immediately with a compatibility report if the Python 3.14 gate or another Section 5 precondition fails.
5. Select exact direct foundation dependency versions and document why each is necessary now.
6. Create the exact runtime declarations and manifests.
7. Resolve and commit only the two authoritative lockfiles.
8. Create only the empty web build entry and empty Python ownership package markers.
9. Add the root setup/build entry points and runtime-major enforcement.
10. Update README/CONTRIBUTING and text-policy files only as required by the actual scaffold.
11. Run locked setup and build in the current worktree, confirm generated state is ignored, and confirm routine execution does not change either lock.
12. Create a clean temporary copy outside the repository, repeat documented setup and build there using no pre-existing `node_modules`, `.venv`, or build output, and delete only that temporary copy afterward.
13. Run all Section 12 checks and create `ViDAP_P0_EP04_Implementation_Report.md`.
14. Perform final Git/file-scope evidence showing only authorized paths changed during this packet.
15. Stop. Do not create tests, validate, self-accept, update governing status documents, or begin P0-EP05.

---

## 12. Required Verification and Evidence

### 12.1 Required checks

The worker must record exact commands and summarized results for:

1. Starting/final `git status --short --branch`, `git rev-parse HEAD`, and sanitized `git remote -v`.
2. Node/npm/uv/CPython version checks, including proof that Node 24—not ambient Node 25—performed package installation and build.
3. Direct dependency source, version, license, maintenance, and Python 3.14 Windows compatibility evidence.
4. `npm.cmd ci` or the corresponding locked operation, `uv --directory python sync --locked`, and proof neither lock changed after routine setup.
5. `npm.cmd run setup` and `npm.cmd run build` from the documented Windows path.
6. Inspection that build output, `node_modules`, uv environments/caches, and temporary reports are ignored and no generated residue is tracked.
7. Node-major rejection behavior from the local enforcement script, using an inspection or safe controlled invocation that does not require changing the system Node runtime.
8. Validation that manifest engines/runtime pins constrain exactly Node 24 and Python 3.14 families.
9. Source inventory proving only the listed empty entry/package markers exist and contain no prohibited behavior.
10. Negative searches for `dev`, `launch`, routes, `FastAPI(`, `uvicorn.run`, React Flow rendering, workflow/node/model/data terms in scaffold source, test/configuration files, alternate lockfiles, requirements files, and second package managers.
11. README/CONTRIBUTING instruction/link accuracy and no unsupported capability/platform claim.
12. A clean temporary-copy setup/build run that begins without repository-generated dependencies, environments, caches, or build output.
13. `git diff --check` and final exact file-scope comparison.

### 12.2 Clean-copy rules

The clean copy is provisional evidence for this uncommitted bounded change, not a substitute for P0-EP08's clean-checkout validation. It must:

- be outside the repository and OneDrive workspace;
- contain the current intended files but no `.git`, `node_modules`, `.venv`, package caches, build output, reports, datasets, secrets, or user-local state;
- use the documented Node 24/npm and uv commands only;
- leave locks unchanged;
- capture only sanitized results; and
- be removed at the end by exact path, whether verification passes or fails.

The worker must never clean, reset, delete, or copy over the live working repository to simulate a fresh environment.

---

## 13. Implementation Report Contract

The worker may create only this evidence file in addition to the scaffold:

`ViDAP_P0_EP04_Implementation_Report.md`

It must contain:

1. Packet identity, approval/version, date, worker role, and governing authority read.
2. Starting branch, commit, sanitized remote, pre-existing changes, and output collision evidence.
3. Exact Section 7 created/modified path list and final scope comparison.
4. Exact Node, npm, uv, and CPython versions used, with machine-readable pin locations.
5. Direct dependency table: package, exact version, role, current primary source, retrieval date, direct license evidence, compatibility basis, and why it is needed before P0-EP05.
6. Manifest/lock authority explanation and proof that no alternate resolver/package-manager state was committed.
7. Root task table with actual setup/build behavior and explicit deferred task names.
8. Empty-source ownership inventory and proof of absence of UI/API/workflow/data/product behavior.
9. Current-worktree and clean-temporary-copy setup/build evidence, lock immutability result, ignored-output result, and temporary-path cleanup result.
10. Documentation/policy updates and accurate remaining limitations.
11. EP04-AC01 through EP04-AC31 self-assessment, explicitly labeled as worker self-assessment.
12. Findings, compatibility failures, deviations, and exceptions; use `None` when absent.
13. Confirmation of no remote mutation, runtime/system mutation outside uv-managed project provisioning, staging/commit/push, later-packet work, or unrelated-file changes.
14. Independent-validation readiness and exact handoff.

The report must not contain secrets, absolute user paths, package-cache paths, copied lockfile bodies, or noisy logs.

---

## 14. Acceptance Criteria

P0-EP04 may be accepted only when:

- **EP04-AC01:** Authority, prerequisites, baseline, repository identity, and pre-existing work are accurately recorded.
- **EP04-AC02:** Only Section 7 paths were created or modified by the worker.
- **EP04-AC03:** Node 24.x is selected, machine-readably pinned, enforced before installation, and used for setup/build; Node 25 is not treated as supported.
- **EP04-AC04:** CPython 3.14.x is selected, machine-readably pinned, constrained in project metadata, and used through uv for locked setup.
- **EP04-AC05:** A missing required Windows Python 3.14 dependency distribution causes a documented stop rather than a silent Python fallback.
- **EP04-AC06:** Root `package.json` and root `package-lock.json` are the sole JavaScript manifest/lock authority.
- **EP04-AC07:** `python/pyproject.toml` and `python/uv.lock` are the sole Python project/lock authority.
- **EP04-AC08:** No alternative package manager, resolver, lockfile, requirements export, global task package, or user-profile dependency is introduced.
- **EP04-AC09:** Direct JavaScript dependencies are limited to the accepted web-build foundation and are current, necessary, direct-license-compatible choices.
- **EP04-AC10:** Direct Python dependencies are limited to FastAPI/Uvicorn foundation needs and are current, necessary, direct-license-compatible choices.
- **EP04-AC11:** Exact direct dependency/version/license/compatibility evidence is preserved for later P0-EP06 review.
- **EP04-AC12:** The accepted `apps/web/` and `python/src/vidap_*` ownership areas exist without defining future semantics.
- **EP04-AC13:** The web entry point is build plumbing only and contains no user-visible shell, graph, product flow, or API interaction.
- **EP04-AC14:** Python ownership packages contain no host, route, startup, persistence, workflow, experiment, export, or ML behavior.
- **EP04-AC15:** Root task entry is Windows-compatible through `npm.cmd run`, uses only locked/local tools, and provides only setup/build behavior.
- **EP04-AC16:** `dev`, `launch`, check, quality, test, CI, dependency/license, and process-smoke tasks are absent and explicitly deferred.
- **EP04-AC17:** Documented setup succeeds in the current worktree using committed locks and leaves locks unchanged.
- **EP04-AC18:** Documented build succeeds and writes only ignored output without starting a service or invoking Python.
- **EP04-AC19:** A clean temporary copy independently reproduces locked setup and build without reused project dependencies, environments, caches, or output.
- **EP04-AC20:** Generated dependencies, environments, caches, build output, and temporary verification state are ignored and do not dirty the repository.
- **EP04-AC21:** README and CONTRIBUTING accurately describe the Windows commands, pins, locks, current pre-shell state, and remaining deferrals.
- **EP04-AC22:** Existing EP03 security, license, secret, local-state, decision-record, ignore, attribute, and editor policies remain intact or are minimally aligned without weakening them.
- **EP04-AC23:** No PowerShell-policy change, global package/system-runtime installation, remote mutation, staging, commit, push, or unrelated-file modification occurs.
- **EP04-AC24:** No test, quality, CI, fixture, dependency-audit, browser, release, deployment, or dependency-bot configuration is introduced.
- **EP04-AC25:** No workflow schema, API, process startup, health endpoint, persistence, experiment, exporter, dataset, model, or other product behavior is introduced.
- **EP04-AC26:** All text files comply with the accepted attribute/editor policy and `git diff --check` passes.
- **EP04-AC27:** The implementation report provides reproducible, sanitized evidence and distinguishes pre-existing work from worker changes.
- **EP04-AC28:** No unresolved critical or high-severity compatibility, license, supply-chain, or safety finding remains; lesser findings are resolved or returned to Central.
- **EP04-AC29:** A fresh validator independently verifies source claims, runtime/lock behavior, build evidence, clean-copy evidence, file scope, and absence of later-packet work.
- **EP04-AC30:** Independent validation returns `Accept` without the validator accepting for Central.
- **EP04-AC31:** Central explicitly accepts the scaffold before the packet is marked complete or P0-EP05 is drafted.

---

## 15. Stop and Escalation Conditions

Stop, preserve only permitted evidence, and return to Central if:

1. The packet is not explicitly approved or its approved version differs from the execution copy.
2. A prerequisite reconciliation is missing, superseded, or conflicts with this packet.
3. Node 24/npm or uv is absent, unusable, or requires a system/policy mutation to work.
4. CPython 3.14 cannot be provisioned/selected or a mandatory direct Python foundation dependency lacks a compatible Windows distribution.
5. A selected direct dependency is unmaintained, has an incompatible/unclear license, needs an unjustified extra package, or cannot be locked reproducibly.
6. Lock generation requires an alternate package manager, floating resolver output, global tool, user profile, or secret.
7. A buildable web scaffold would require user-visible shell/product code beyond the expressly empty entry point.
8. A needed source/path is not in Section 7, conflicts with existing user work, or would redefine later ownership semantics.
9. Setup/build changes a lock unexpectedly, writes tracked generated state, or cannot be repeated in the clean temporary copy.
10. The existing Windows/OneDrive/local-state rules cannot be preserved.
11. A command would mutate remote state, stage/commit/push, reset/clean/delete unrelated work, or broaden into P0-EP05+.

Classify the return as a defect, clarification, dependency change, or scope proposal where applicable. Never silently downgrade the runtime, remove a gate, or omit a lock to finish the packet.

---

## 16. Independent Validation Contract

Validation occurs in a fresh chat after the worker stops. The validator must read every governing input, the approved packet, all Section 7 artifacts, and the implementation report.

### Validator tasks

The validator must independently:

1. Verify approval, prerequisite reconciliations, current repository identity, and exact worker file scope.
2. Recheck primary-source support, maintenance, direct-license, and compatibility claims for all direct dependencies.
3. Confirm Node 24 and CPython 3.14 pins/constraints, runtime enforcement, and the absence of silent fallback.
4. Inspect both manifests and locks for sole-authority discipline, expected direct dependencies, and absence of prohibited additions.
5. Reproduce or inspect locked setup/build from the documented Windows path and a bounded clean temporary copy, without reusing project dependencies or accepting a cache hit as proof.
6. Verify routine setup/build leave locks unchanged and generated state ignored.
7. Inspect every source/configuration file for empty ownership/build plumbing only, absence of product semantics, and preservation of the approved dependency direction.
8. Check README/CONTRIBUTING accuracy and existing policy-file preservation.
9. Confirm no dev/launch/quality/test/CI/dependency-control/fixture/process-startup work was smuggled into the scaffold.
10. Re-run whitespace, file-scope, and sensitive-content checks without exposing sensitive values.
11. Map evidence to EP04-AC01 through EP04-AC31.
12. Return exactly one verdict: `Accept`, `Revise`, or `Blocked`, with criterion-linked findings and severity.

### Authorized validator output

The validator may create only:

`ViDAP_P0_EP04_Validation_Report.md`

Alternatively, the validator may return the identical structured report in chat for Central to preserve. It must not edit the scaffold, packet, governing files, remote state, or any other file.

The validation report must include verdict, scope, commands/evidence, acceptance-criterion matrix, direct-dependency evidence review, findings with IDs/severity/owner, file-scope conclusion, and an explicit statement that the validator did not accept for Central or begin P0-EP05.

---

## 17. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P0_EP04.md` as the bounded scaffold worker. Read every governing input and follow the packet exactly. Create only the Section 7 artifacts and `ViDAP_P0_EP04_Implementation_Report.md`. Use only Node 24/npm and uv-managed CPython 3.14 with current primary-source evidence; stop rather than silently downgrade a runtime or introduce another package manager. Prove locked setup and build in the worktree and a bounded clean temporary copy. Do not create product behavior, dev/launch tasks, tests, quality/CI/dependency controls, fixtures, APIs, or P0-EP05 work. Do not validate or accept your own work, mutate remote state, or stage/commit/push. Stop with the implementation report and independent-validation handoff.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P0_EP04.md`. Read its governing inputs, all Section 7 artifacts, and `ViDAP_P0_EP04_Implementation_Report.md`. Follow Section 16 exactly. Independently verify direct dependency evidence, Node 24/Python 3.14 runtime and lock behavior, current/clean-copy setup-build proof, policy preservation, exact file scope, and absence of P0-EP05/later work. Create only `ViDAP_P0_EP04_Validation_Report.md`, or return the identical structured report in chat. Do not edit implementation or governing files, change remote state, accept for Central, or begin P0-EP05. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 18. Evidence Return to Central

The worker must return:

- implementation-report path;
- starting/final branch, commit, worktree, and sanitized remote evidence;
- exact Section 7 path list;
- direct dependency/version/license/compatibility evidence;
- runtime and lockfile evidence;
- current-worktree and clean-copy setup/build results;
- EP04-AC01 through EP04-AC31 self-assessment;
- findings, deviations, exceptions, and blockers; and
- independent-validation readiness.

The validator must return the Section 16 report. Central will preserve the actual verdict, reconcile findings, accept or return the scaffold, and update packet/roadmap status. Neither worker nor validator may perform Central reconciliation.

---

## 19. Next Action After Completion

P0-EP04 is complete. Independent validation returned `Accept`, and Central accepted the reproducible scaffold in `ViDAP_P0_EP04_Validation_and_Reconciliation.md` on 2026-09-18. Central may now draft P0-EP05 as a separate bounded packet. This completion does not authorize P0-EP05 execution, quality/test configuration, CI, fixtures, shell startup, or product implementation.
