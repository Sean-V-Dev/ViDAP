# ViDAP P0-EP05 - Quality and Test Harness

| Field | Value |
|---|---|
| Status | Complete |
| Packet version | 0.2 |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisite packets | P0-EP01 through P0-EP04 - Complete |
| Prerequisite reconciliations | `ViDAP_P0_EP01_Validation_and_Reconciliation.md`; `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP03_Validation_and_Reconciliation.md`; `ViDAP_P0_EP04_Validation_and_Reconciliation.md` |
| Compatibility decision | `docs/decisions/0001-ep05-frontend-quality-compatibility.md` |
| Central reconciliation | `ViDAP_P0_EP05_Validation_and_Reconciliation.md` |
| Workstream | WS0.4 - Quality and testing |
| Packet type | Bounded local quality, test, and report-only coverage implementation |
| Created | 2026-09-18 |
| Owner | Central |

---

## 1. Authorization Boundary

This is a completed revised execution packet. Version 0.1 was blocked before implementation by B-EP05-001; version 0.2 incorporates Central's accepted compatibility amendment, was approved on 2026-09-18, and completed Central reconciliation on 2026-09-18.

The bounded execution worker created or modified only the Section 7 quality/test artifacts, updated only the two authoritative lockfiles through intentional direct development-dependency changes, ran the accepted local checks, and created the implementation report. Independent validation and Central reconciliation are recorded in `ViDAP_P0_EP05_Validation_and_Reconciliation.md`.

Approval does not authorize CI, dependency/license/audit controls, fixture files, browser automation, process startup, API routes, health endpoints, workflow/schema semantics, data/ML behavior, remote changes, commits, or P0-EP06 through P0-EP08 work. It also does not authorize `eslint-plugin-jsx-a11y`, a substitute accessibility linter, forced peer dependencies, or an unsupported ESLint line.

---

## 2. Plain-English Packet Intent

### What this packet will change

This packet makes the accepted quality decisions executable. It adds project-local formatting, linting, type checking, unit/integration testing, and report-only coverage tools; configures one authoritative root task path; and adds small tests that prove the actual scaffold protections work.

### Why the system needs it

The empty scaffold can build, but it cannot yet prove that accidental formatting drift, unsafe lint patterns, type errors, broken runtime enforcement, or broken local-host wiring will be caught. This packet establishes those checks before CI repeats them and before a minimal runnable shell makes failures harder to isolate.

### What real behavior it enables

Contributors can run a small, documented set of Windows commands to check formatting, lint, types, unit tests, in-process integration tests, build output, and coverage reports. The tests prove the Node 24 guard, the intentionally empty React mount, and a no-route FastAPI ASGI foundation without creating a user-visible application or network service.

### How success will be demonstrated

Every required root check succeeds from a locked setup. Each check has a distinct purpose, does not silently repair files, and produces a clear failure against a temporary deliberate violation. Tests exercise real scaffold behavior. Coverage reports are produced without a percentage threshold. No server starts, no browser opens, no fixture or product data is added, and no future workflow/API behavior is claimed.

---

## 3. Governing Inputs and Traceability

The worker must read these sources in authority order before changing anything:

1. Current explicit user direction approving this exact packet, if given.
2. `ViDAP_Overview.txt`, especially OV §§1, 9, 18-21, 22A, and 25-30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.0, especially Sections 1-3, P0, and Sections 6-7.
4. `ViDAP_Roadmap.md` version 1.0, especially P0 and the quality/dependency delivery tracks.
5. `ViDAP_Phase_0_Plan.md` version 1.0, especially P0-G4, WS0.4, deliverables 6-7, P0-AC07, and Phase 0 guardrails.
6. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, authoritative for the Node 24, CPython 3.14, uv, npm, Windows, topology, and root-task decisions.
7. `ViDAP_P0_EP02_Validation_and_Reconciliation.md`, authoritative for D0.4 and its Q01-Q08 quality decisions, as amended for EP05 by `docs/decisions/0001-ep05-frontend-quality-compatibility.md`.
8. `ViDAP_P0_EP03_Validation_and_Reconciliation.md`, authoritative for repository hygiene, local-state, and contribution policies.
9. `ViDAP_P0_EP04_Validation_and_Reconciliation.md`, authoritative for the accepted scaffold and elevated uv execution-environment note.
10. `docs/decisions/0001-ep05-frontend-quality-compatibility.md`.
11. This approved revised packet.

This packet advances OV §18, OV §§20-21, OV §22A's separation constraints, OV §§25-30, Spine invariants 4, 7, 9, and 11, and Phase 0 WS0.4. It implements Q01-Q08 only; Q09 belongs to P0-EP07 and Q10-Q13 belong to P0-EP06.

---

## 4. Inherited Decisions and Non-Negotiable Constraints

The worker must preserve these accepted constraints:

1. Node 24.x/npm and CPython 3.14.x/uv are the only supported project runtime and package-management paths. The elevated Windows execution path is required when restricted tooling denies the WinGet-installed `uv.exe`.
2. Root `package.json`/`package-lock.json` and `python/pyproject.toml`/`python/uv.lock` remain the only manifest and lock authorities. No requirements export, alternate lockfile, second package manager, global tool, or user-profile dependency is allowed.
3. TypeScript type checking uses `tsc --noEmit` on a maintained TypeScript 6.x version declared compatible with the selected TypeScript-ESLint integration; Prettier owns formatting; ESLint flat config owns TypeScript-aware frontend static lint and React Hooks checks; Vitest plus React Testing Library/jsdom owns frontend tests; Ruff owns Python formatting/lint; mypy owns Python typing; pytest plus AnyIO and HTTPX ASGI transport owns Python unit/integration testing; direct Vitest V8 and coverage.py reports own coverage. JSX-a11y is explicitly deferred under decision record 0001.
4. Formatting/linting check tasks are non-mutating. Explicit format/fix tasks are opt-in and never aggregate into `check`. CI is not created here.
5. Quality rules must have an actual Phase 0 purpose. Do not add rules merely to maximize a score, add a second tool for a role, or use an empty test as evidence.
6. Frontend source remains build plumbing only. The React root must still render no user-visible application content.
7. The only allowed Python behavioral addition is a local `create_app()` factory that returns an un-routed FastAPI application solely for in-process ASGI transport verification. It must not be started, bind a port, expose a route, define a health payload, or establish an API contract.
8. Tests must use constructed values only. No root `fixtures/`, data files, datasets, personal/sensitive data, browser automation, real network calls, or external service dependency is allowed.
9. Python tests use registered strict markers `unit`, `integration`, `smoke`, and `slow`; the project uses the AnyIO pytest integration with the single `asyncio` backend. `pytest-asyncio` is prohibited.
10. Coverage is report-only in P0. No coverage percentage threshold, ratchet, or pass/fail floor may be introduced.
11. `dev`, `launch`, `smoke`, CI, dependency/license/audit, fixture, and release tasks remain absent. P0-EP07 later owns cross-process smoke and a minimal shell.
12. Current direct versions, licenses, maintenance status, Node 24/Python 3.14 support, and Windows compatibility of every added quality dependency must be rechecked from primary sources and reported. The selected TypeScript 6.x and TypeScript-ESLint peer intersection must be declared compatible and maintained; no peer override is allowed. P0-EP06 later owns full transitive license and vulnerability evidence.

---

## 5. Preconditions and Stop Gates

Before changing any file, the worker must confirm and record:

1. This packet is explicitly approved for execution and matches approved version 0.2.
2. P0-EP01 through P0-EP04 remain complete and all reconciliation records are present.
3. The current branch, commit, sanitized remote, pre-existing worktree changes, and existing scaffold paths.
4. Node 24/npm and uv/CPython 3.14 are callable; when default restricted execution denies uv, the worker must retry via the normal/elevated Windows execution path before declaring a project prerequisite failure.
5. Existing `npm.cmd run setup` and `npm.cmd run build` succeed with unchanged locks before the intentional quality dependency change.
6. Current primary sources support every candidate direct quality dependency on Node 24 or Windows CPython 3.14, and each has a license compatible with the accepted D0.6 policy. The exact TypeScript 6.x and TypeScript-ESLint releases must declare a maintained peer-compatible intersection; the current ESLint, official base config, and React Hooks plugin must likewise have a maintained peer-compatible intersection. JSX-a11y is not a candidate in this packet.
7. No existing quality/test/configuration file collides with the Section 7 path set.
8. A worker-created temporary location outside the repository and OneDrive is available for negative-diagnostic and clean-copy verification.
9. A temporary exception to the restricted uv sandbox is usable for required lock/sync/test commands; if it is not, stop with an execution-environment finding rather than substituting Python tooling.

If a necessary package cannot meet the Python 3.14/Windows, license, maintenance, or peer-compatibility gate, if any required check needs product behavior, or if a meaningful test cannot be written within this packet's boundary, stop and return the evidence to Central.

---

## 6. Objective and Completion Condition

### Objective

Implement the accepted Q01-Q08 quality/test layers as local, locked, Windows-compatible root tasks with meaningful foundation assertions and report-only coverage.

### Completion condition

P0-EP05 is complete only when:

1. The worker creates/modifies only the Section 7 path set.
2. EP05-AC01 through EP05-AC34 pass or an unresolved condition is returned to Central.
3. A fresh independent validator returns `Accept` under Section 16.
4. Central reconciles the result and marks P0-EP05 `Complete`.

Passing a command against an empty target, a test that proves no observable scaffold behavior, or a check that repairs source automatically does not satisfy this completion condition.

---

## 7. Authorized Outputs and File Ownership

After approval, the worker may create or modify only these paths:

| Path | Authorized purpose |
|---|---|
| `package.json` | Replace scaffold TypeScript 7.x with the accepted compatible TypeScript 6.x, add accepted JS quality dependencies, and add root quality task scripts |
| `package-lock.json` | Sole updated JavaScript lock after intentional quality dependency changes |
| `python/pyproject.toml` | Add accepted Python quality dependencies/groups and tool configuration |
| `python/uv.lock` | Sole updated Python lock after intentional quality dependency changes |
| `scripts/verify-node-version.mjs` | Refactor only as needed to expose testable Node-major validation while preserving preinstall behavior |
| `scripts/verify-node-version.test.mjs` | Real Vitest coverage of accepted/rejected Node-major logic |
| `.prettierrc.json` | Minimal project Prettier configuration |
| `.prettierignore` | Explicit formatting exclusions for generated/ignored state |
| `eslint.config.js` | Flat ESLint configuration with TypeScript-aware and React Hooks roles; no JSX-a11y plugin or substitute accessibility linter |
| `apps/web/vitest.config.ts` | Vitest/jsdom/coverage configuration for the web area |
| `apps/web/src/foundation-root.tsx` | Explicit no-UI foundation component returning `null` |
| `apps/web/src/foundation-root.test.tsx` | React Testing Library assertion of the intentional empty mount |
| `apps/web/src/test/setup.ts` | Test-only matcher/environment setup |
| `apps/web/src/main.tsx` | Use the explicit foundation root without adding visible behavior |
| `python/src/vidap_execution/app.py` | Un-routed FastAPI application factory for in-process ASGI testing only |
| `python/tests/conftest.py` | AnyIO backend fixture and shared test configuration only |
| `python/tests/test_execution_app.py` | Meaningful in-process ASGI transport/unknown-route integration test |
| `README.md` | Accurate quality-command documentation and remaining Phase 0 deferrals |
| `CONTRIBUTING.md` | Accurate local quality/task and evidence expectations |
| `ViDAP_P0_EP05_Implementation_Report.md` | Worker evidence and validation handoff |

The worker may create only necessary parent directories: `apps/web/src/test/` and `python/tests/`. It may not create any other path.

The worker must not create `.github/`, root `tests/`, root `fixtures/`, browser configuration, CSS/design files, a visual shell, API routes, server/process scripts, health endpoints, dependency/license/audit scripts, `requirements*.txt`, reports committed to the repository, or any later-packet output.

---

## 8. Required Quality and Test Contract

### 8.1 Direct quality dependencies

The worker must use current primary sources to select, lock, and report only the accepted direct development dependencies needed for:

- Prettier;
- ESLint, its official base configuration, TypeScript flat-config integration, and React Hooks plugin;
- Vitest, its V8 coverage provider, jsdom, React Testing Library, and testing-library DOM matchers;
- Ruff;
- mypy;
- pytest;
- AnyIO;
- HTTPX; and
- coverage.py.

The scaffold's TypeScript 7.x direct dependency must be intentionally replaced with an exact current maintained TypeScript 6.x release that is within the selected TypeScript-ESLint peer range. No `eslint-plugin-jsx-a11y`, alternate accessibility linter, Black, isort, Flake8, Pyright, Jest, `pytest-asyncio`, Playwright, Selenium, `concurrently`, `wait-on`, CSS lint tool, or second formatter/linter/test runner is permitted. Version choices must be intentional and current, not copied from ambient caches. Direct package evidence belongs in the implementation report; P0-EP06 owns full graph inventory and advisory/license reports.

### 8.2 Root task contract

`package.json` must expose exactly these new public quality task names in addition to existing `setup` and `build`:

| Task | Required non-overlapping behavior |
|---|---|
| `format:check` | Runs Prettier check for covered JS/TS/JSON/Markdown/configuration text and `uv run --locked ruff format --check` for Python. It writes nothing. |
| `format:write` | Deliberately runs Prettier write and Ruff format repair. It is opt-in and excluded from `check`. |
| `lint` | Runs ESLint static analysis and `uv run --locked ruff check`; it writes nothing. |
| `lint:fix` | Deliberately runs ESLint/Ruff repair paths. It is opt-in and excluded from `check`. |
| `typecheck` | Runs `tsc --noEmit` against the web config and strict mypy against first-party Python source. It writes nothing. |
| `test:unit` | Runs deterministic Vitest unit tests and Python pytest tests marked `unit`; no real network, clock, user path, cache, or process dependency. |
| `test:integration` | Runs Python pytest tests marked `integration` through HTTPX ASGI transport only. It must not start a server or process. |
| `coverage` | Produces Vitest V8 and coverage.py reports for first-party source only, without a threshold or automatic repair. Outputs remain ignored. |
| `check` | Ordered non-mutating aggregate: `format:check` → `lint` → `typecheck` → `test:unit` → `build` → `test:integration`. It stops on the first failure. P0-EP07 may later append `smoke`; EP05 must not create it. |

Each task must use local locked binaries and uv's locked project environment. The implementation may use narrowly named internal npm subcommands only to keep OS shell quoting safe; internal names are not a second task taxonomy. No task may use `npx`, floating install, `npm install`, `uv sync` during a check, `--fix`, `--write`, or an external service unless that task is explicitly `format:write` or `lint:fix`.

### 8.3 Configuration contract

- TypeScript remains strict with `noEmit`; test type coverage must not weaken production compilation settings.
- Prettier configuration must be minimal, project-local, and align with `.editorconfig`; ignore generated dependencies, environments, build output, coverage, caches, and reports without ignoring authored source or documentation.
- ESLint must use flat configuration. It must include TypeScript-aware linting and React Hooks checks with no Prettier style-rule duplication. Rules start with stable correctness/import/React signal; no preview/broad style doctrine or blanket disable is allowed. JSX accessibility linting is deferred by decision record 0001; do not install, configure, or claim it.
- Vitest must use jsdom, deterministic `run` mode for command execution, clear test inclusion, and V8 coverage configured to measure only first-party web source while excluding tests, configuration, and generated output.
- Ruff configuration belongs in `pyproject.toml`, targets Python 3.14, uses formatter plus lint rules for baseline correctness, imports, upgrades, bugbear, and narrowly justified security/error checks. It must not enable preview or broad docstring/style doctrine.
- mypy configuration belongs in `pyproject.toml`, sets Python 3.14, checks first-party Python source strictly, uses explicit package roots, enables `warn_return_any`, `warn_unused_ignores`, `warn_redundant_casts`, `warn_unused_configs`, and `no_implicit_optional`, and must not use global `ignore_missing_imports`.
- pytest configuration belongs in `pyproject.toml`, registers `unit`, `integration`, `smoke`, and `slow`, enables strict markers, defaults to no accidental test discovery outside `python/tests/`, and uses the AnyIO `asyncio` backend only.
- coverage.py configuration belongs in `pyproject.toml`, measures only `python/src`, excludes tests/configuration/generated code, and has no fail-under threshold.

### 8.4 Meaningful foundation tests

The worker must add and demonstrate these minimum tests:

1. Node-major validation accepts a Node 24 version and rejects non-24 majors with the same actionable message used by the preinstall path.
2. React Testing Library renders the explicit `FoundationRoot` and proves that the scaffold intentionally presents no UI content, rather than merely importing an untested file.
3. A marked Python unit test proves that the accepted ownership packages are importable under the configured first-party source path.
4. A marked asynchronous Python integration test creates the un-routed app through `create_app()`, sends a request through HTTPX `ASGITransport`, and proves the application is in-process and has no defined product route by asserting the framework's normal unknown-route response.

The implementation must distinguish the tests' limited foundation claims from a user-facing shell, a health contract, or an API. Tests must use `pytest.mark.anyio`; no loop policy, thread, port, subprocess, real network, test data file, or fixture is permitted.

### 8.5 Negative diagnostic and coverage demonstration

The worker must use a clean worker-created temporary copy outside the repository and OneDrive to demonstrate that representative deliberate violations fail clearly under at least:

- Prettier formatting check;
- ESLint;
- TypeScript `tsc --noEmit`;
- Ruff format or lint;
- mypy; and
- pytest.

The temporary violations must be removed with that exact temporary copy. The live repository must never contain an intentionally failing committed file. The report must show each command, nonzero result, the concise diagnostic category, and cleanup outcome without copying noisy logs or secrets.

The worker must generate one successful report-only coverage run, record the measured source sets and report locations, and explicitly state that no percentage is a P0 threshold or acceptance gate.

---

## 9. Permitted Scope

The worker may:

1. Read governing artifacts, current project files, and current primary sources.
2. Use Node 24/npm and elevated uv/CPython 3.14 to add the approved quality dependencies, regenerate locks intentionally, install locked environments, run checks, and generate ignored reports.
3. Create/modify only the Section 7 files and parent directories.
4. Use exact worker-created temporary directories outside the repository/OneDrive for clean-copy and negative diagnostic proof, then remove only those exact paths.
5. Run local format/lint/type/test/build/coverage commands, package metadata inspection, lock checks, and read-only Git inspection.
6. Return a blocker rather than weakening a check, adding a substitute tool, or broadening into later work.

---

## 10. Prohibited Scope

The worker must not:

1. Create CI workflows, hosted checks, action configuration, dependency/license/audit tooling, Dependabot configuration, or remote policy changes.
2. Create root fixtures, data files, datasets, browser/E2E automation, screenshots, CSS/design work, or a user-visible application shell.
3. Create a `dev`, `launch`, or `smoke` task; start a server/process; bind a port; open a browser; create a health endpoint; or define a browser/Python API message contract.
4. Add workflow/node semantics, typed ports, persistence, experiments, export behavior, data transforms, ML libraries, or product results.
5. Add an alternative package manager, global task tool, second formatter/linter/test runner/type checker, `pytest-asyncio`, container, service, or system-policy workaround.
6. Introduce coverage thresholds, auto-fix behavior into checks/aggregate, suppressed diagnostics, blanket type-ignore behavior, or empty/ornamental test evidence.
7. Change `.gitignore`, `LICENSE`, `SECURITY.md`, decision records, remote settings, branch protection, secrets, staging, commits, pushes, resets, cleans, rebases, or unrelated user files.
8. Write coverage, test, build, cache, environment, lock backup, or temporary evidence into tracked paths.
9. Begin P0-EP06, P0-EP07, P0-EP08, Phase 1, or product implementation.

---

## 11. Required Execution Sequence

After approval, the worker must:

1. Read all governing inputs and the approved packet in full.
2. Record current branch/commit/worktree/remote, accepted scaffold evidence, and existing output-path collision checks.
3. Recheck Node 24/npm, elevated uv/CPython 3.14, existing locked setup/build, and current primary dependency evidence before changing manifests.
4. Stop with a specific blocker if a compatibility, license, environment, output-scope, or meaningful-test gate fails.
5. Select exact direct quality dependency versions and document their roles, current source evidence, licenses, and compatibility.
6. Add only the approved direct dependencies/configuration and intentionally regenerate the two authoritative locks.
7. Implement the root task taxonomy, empty foundation root, Node-major testability, un-routed app factory, and minimum tests within Section 7.
8. Run locked setup, every individual root task, `check`, and `coverage`; prove locks stay unchanged after routine runs.
9. Demonstrate negative diagnostics and clean-copy reproducibility in exact worker-created temporary copies, then remove them.
10. Confirm generated environments, reports, coverage, build output, caches, and temporary state remain ignored and no new tracked residue exists.
11. Update README/CONTRIBUTING only for real task names, usage, and deferrals.
12. Create `ViDAP_P0_EP05_Implementation_Report.md` and perform final `git diff --check`/file-scope evidence.
13. Stop. Do not self-validate, reconcile, update status documents, or begin P0-EP06.

---

## 12. Required Verification and Evidence

The worker must record exact commands and summarized results for:

1. Starting/final Git identity and exact allowed path scope.
2. Node/npm/uv/CPython runtime facts and elevated uv execution distinction, if applicable.
3. Current primary-source package/version/license/maintenance/compatibility evidence for each added direct dependency.
4. Intentional lock-update evidence and routine lock-hash invariance after setup, individual checks, aggregate check, and coverage.
5. Every root task in Section 8.2, including separate check/write/fix boundaries.
6. TypeScript no-emit proof and absence of generated compiler state.
7. ESLint/Prettier/Ruff/mypy/pytest configuration and strict-marker behavior.
8. Meaningful-test proof: Node-major acceptance/rejection, React no-UI mount, Python ownership imports, and in-process ASGI unknown-route behavior.
9. Determinism proof that test commands use no network, port, server, real clock/random dependency, user path, existing cache, or fixture file.
10. Positive and negative ignore checks for dependencies, `.venv`, coverage/report/build output, temporary state, authored source, tests, locks, and documentation.
11. Representative negative diagnostic matrix and cleanup proof from temporary copies.
12. Coverage report output/source inclusion-exclusion evidence and explicit no-threshold statement.
13. README/CONTRIBUTING accuracy, `git diff --check`, scoped sensitive-content scan, and final worker file-scope comparison.

The clean copies are provisional evidence for the uncommitted bounded change, not a substitute for P0-EP08. They must be outside the repository/OneDrive, contain no `.git`, dependencies, environments, caches, reports, generated output, secret, fixture, or user-local state, and be removed by exact path afterward. The worker must never clean/reset/copy over the live repository.

---

## 13. Implementation Report Contract

The worker may create only this evidence file in addition to the Section 7 implementation:

`ViDAP_P0_EP05_Implementation_Report.md`

It must contain:

1. Packet identity, approval/version/date, worker role, and authority read.
2. Starting branch/commit/sanitized remote, pre-existing changes, and output-collision evidence.
3. Exact Section 7 created/modified path list and final scope comparison.
4. Direct quality dependency table with exact version, role, license, primary source/retrieval date, Node/Python/Windows compatibility, and rationale.
5. Manifest/lock authority proof and post-routine-run lock hashes.
6. Root task map, command results, and explicit deferred task names.
7. Configuration summaries proving distinct tool roles and nonmutating check versus opt-in repair behavior.
8. Test inventory and exact limited claims for Node enforcement, no-UI React root, Python package imports, and ASGI unknown-route behavior.
9. Current-worktree/clean-copy/negative-diagnostic/coverage evidence with ignored-output and cleanup results.
10. EP05-AC01 through EP05-AC34 self-assessment, explicitly labeled worker self-assessment.
11. Findings, deviations, exceptions, and blockers; use `None` when absent.
12. Confirmation of no CI, fixture, browser, process startup, product behavior, remote mutation, staging/commit/push, or later-packet work.
13. Independent-validation readiness and handoff.

The report must omit secrets, absolute user paths, cache locations, copied lockfile bodies, and verbose logs.

---

## 14. Acceptance Criteria

P0-EP05 may be accepted only when:

- **EP05-AC01:** Authority, prerequisites, baseline, repository identity, and pre-existing work are accurately recorded.
- **EP05-AC02:** Only Section 7 paths were created or modified by the worker.
- **EP05-AC03:** Every added direct quality dependency, including the replacement TypeScript 6.x, has current primary-source, license, maintenance, Node/Python/Windows compatibility, peer-range, and role evidence.
- **EP05-AC04:** `package-lock.json` and `python/uv.lock` remain the sole authorities and intentional updates are documented.
- **EP05-AC05:** Routine setup/check/build/coverage runs leave both locks unchanged.
- **EP05-AC06:** Prettier is project-local, aligned, nonmutating in check mode, and separate from explicit write mode.
- **EP05-AC07:** ESLint uses flat config with TypeScript-aware and React Hooks roles without Prettier duplication, blanket disables, JSX-a11y, or an alternate accessibility linter.
- **EP05-AC08:** A maintained, peer-compatible TypeScript 6.x line runs `tsc --noEmit` strict checking without generated output.
- **EP05-AC09:** Vitest, React Testing Library, jsdom, and V8 coverage have distinct configured roles and deterministic run behavior.
- **EP05-AC10:** Ruff owns Python format/lint/import ordering without Black/isort/Flake8 overlap or preview/style overreach.
- **EP05-AC11:** mypy checks first-party Python source with the accepted strict settings and no global missing-import blind spot.
- **EP05-AC12:** pytest uses strict registered markers, AnyIO with only the asyncio backend, and no pytest-asyncio.
- **EP05-AC13:** HTTPX ASGI transport proves the limited in-process integration path without a started server or API contract.
- **EP05-AC14:** Direct Vitest V8 and coverage.py reports measure only first-party source and have no percentage threshold.
- **EP05-AC15:** Root tasks have the exact non-overlapping roles in Section 8.2, use locked/local tools, and remain Windows-compatible through `npm.cmd run`.
- **EP05-AC16:** `check` is ordered, nonmutating, fails fast, and excludes future `smoke` until P0-EP07.
- **EP05-AC17:** Format/lint repair is explicit and cannot run as part of normal check/aggregate/CI behavior.
- **EP05-AC18:** The Node 24 guard has meaningful positive and negative unit coverage with actionable diagnostics.
- **EP05-AC19:** The React test proves the intentional no-UI foundation mount without claiming a user-visible shell.
- **EP05-AC20:** Python tests prove package ownership importability and the limited un-routed ASGI behavior with constructed values only.
- **EP05-AC21:** Individual tasks, aggregate check, and build pass from locked setup.
- **EP05-AC22:** Representative temporary deliberate violations fail clearly for format, lint, TypeScript, Ruff, mypy, and pytest, then are cleaned up.
- **EP05-AC23:** Tests and checks are deterministic and require no network, browser, port, service, fixture, dataset, user path, real clock, or prior cache.
- **EP05-AC24:** Current-worktree and clean temporary-copy reproductions pass with isolated dependencies/environments/caches and are cleaned up.
- **EP05-AC25:** Generated dependencies, environments, caches, coverage/reports, build output, and temporary state remain ignored and untracked.
- **EP05-AC26:** README and CONTRIBUTING accurately document quality tasks, prerequisites, no-threshold coverage, and remaining deferrals.
- **EP05-AC27:** Existing license, security, ignore, attribute, editor, decision-record, and local-state policies remain intact.
- **EP05-AC28:** No CI, dependency/license/audit, fixture, browser, process, dev/launch, health/API, workflow, data/ML, product behavior, JSX-a11y, or substitute accessibility linter is introduced.
- **EP05-AC29:** No global/system policy/runtime mutation, remote mutation, staging, commit, push, or unrelated-file modification occurs.
- **EP05-AC30:** Text, configuration, links, sensitive-content scan, and `git diff --check` pass.
- **EP05-AC31:** The implementation report provides reproducible, sanitized evidence and distinguishes pre-existing work from worker changes.
- **EP05-AC32:** No unresolved critical/high compatibility, security, supply-chain, or quality finding remains; lesser findings are resolved or returned to Central.
- **EP05-AC33:** A fresh validator independently verifies the tool evidence, actual check/negative/coverage behavior, test value, scope, and absence of later-packet work.
- **EP05-AC34:** Independent validation returns `Accept`, and Central explicitly accepts the harness before the packet is marked complete or P0-EP06 is drafted.

---

## 15. Stop and Escalation Conditions

Stop, preserve only permitted evidence, and return to Central if:

1. The packet is not explicitly approved or its approved version differs from the execution copy.
2. A prerequisite reconciliation is absent, superseded, or conflicts with the packet.
3. Node 24/npm, elevated uv, or CPython 3.14 cannot perform a required locked operation.
4. A needed quality dependency is incompatible, unmaintained, license-unclear/incompatible, outside a declared peer range, or requires an unapproved substitute.
5. A task needs a global tool, npx download, alternative lock/resolver, system policy change, actual server/browser/network, or a product capability to work.
6. A test cannot make a meaningful assertion without defining a future contract or adding a prohibited fixture/data file.
7. A required configuration/path is outside Section 7 or conflicts with existing user work.
8. A routine task changes a lock, writes tracked output, repairs files unexpectedly, or leaves temporary state behind.
9. A negative-diagnostic or clean-copy proof cannot be safely isolated outside the live repository/OneDrive.
10. Any action would alter remote state, stage/commit/push, or start P0-EP06+ work.

Never weaken a rule, lower the runtime, skip a test, add a blanket ignore, or treat a passing empty check as a solution to a stop condition.

---

## 16. Independent Validation Contract

Validation occurs in a fresh chat after the worker stops. The validator must read every governing input, the approved packet, all Section 7 artifacts, and the implementation report.

### Validator tasks

The validator must independently:

1. Verify approval, prerequisite reconciliations, runtime path, repository identity, and exact worker scope.
2. Recheck primary-source version/license/maintenance/compatibility claims for every added direct dependency.
3. Inspect manifest/lock authority and reproduce locked setup/check/build/coverage with elevated uv where required.
4. Run or inspect every root task, including proof that check versus repair behavior is separate and locks remain unchanged.
5. Challenge TypeScript, Prettier, ESLint, Vitest/RTL/jsdom, Ruff, mypy, pytest/AnyIO/HTTPX, and coverage configurations for role overlap, broad suppressions, or hollow targets.
6. Independently inspect and challenge the meaningful limited tests and their lack of user-facing/API/product claims.
7. Reproduce representative negative diagnostics and clean-copy/ignored-output behavior without touching the live repository.
8. Confirm no browser, fixture, CI, dependency-control, process-startup, product, or P0-EP06/later work was introduced.
9. Re-run file-scope, whitespace, link, and sensitive-content checks without exposing values.
10. Map evidence to EP05-AC01 through EP05-AC34.
11. Return exactly one verdict: `Accept`, `Revise`, or `Blocked`, with criterion-linked findings and severity.

### Authorized validator output

The validator may create only:

`ViDAP_P0_EP05_Validation_Report.md`

Alternatively, the validator may return the identical structured report in chat for Central to preserve. It must not edit implementation, packet, governing files, remote state, or any other file.

The validation report must include verdict, scope, commands/evidence, acceptance-criterion matrix, direct-dependency evidence review, findings with IDs/severity/owner, file-scope conclusion, and an explicit statement that the validator did not accept for Central or begin P0-EP06.

---

## 17. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P0_EP05.md` version 0.2 as the bounded quality/test-harness worker. Read every governing input, including decision record 0001, and follow the packet exactly. Create or modify only the Section 7 artifacts and `ViDAP_P0_EP05_Implementation_Report.md`. Use Node 24/npm and elevated uv-managed CPython 3.14; do not mistake the restricted sandbox's WinGet uv access denial for a project prerequisite failure. Replace the scaffold's TypeScript 7.x with a maintained, declared peer-compatible TypeScript 6.x; implement TypeScript-aware ESLint and React Hooks checks, but do not install JSX-a11y or an accessibility-linter substitute. Implement Q01-Q08 as amended, prove meaningful real foundation checks/tests/negative diagnostics/report-only coverage, and keep all product/process/CI/fixture work out of scope. Do not validate or accept your own work, mutate remote state, or stage/commit/push. Stop with the implementation report and independent-validation handoff.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P0_EP05.md` version 0.2. Read its governing inputs, including decision record 0001, all Section 7 artifacts, and `ViDAP_P0_EP05_Implementation_Report.md`. Follow Section 16 exactly. Independently verify direct dependency evidence, the declared maintained TypeScript 6.x/TypeScript-ESLint peer intersection, ESLint/React Hooks configuration, intentional JSX-a11y deferral, every root task, lock invariance, meaningful tests, negative diagnostics, coverage/no-threshold policy, clean-copy behavior, exact file scope, and absence of P0-EP06/later work. Use elevated uv execution when the restricted sandbox denies the WinGet uv executable. Create only `ViDAP_P0_EP05_Validation_Report.md`, or return the identical structured report in chat. Do not edit implementation or governing files, change remote state, accept for Central, or begin P0-EP06. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 18. Evidence Return to Central

The worker must return:

- implementation-report path;
- starting/final branch, commit, worktree, and sanitized remote evidence;
- exact Section 7 path list;
- direct dependency/version/license/compatibility evidence;
- lock update/invariance, individual-task, aggregate, negative-diagnostic, coverage, and clean-copy results;
- EP05-AC01 through EP05-AC34 self-assessment;
- findings, deviations, exceptions, and blockers; and
- independent-validation readiness.

The validator must return the Section 16 report. Central will preserve the actual verdict, reconcile findings, accept or return the harness, and update packet/roadmap status. Neither worker nor validator may perform Central reconciliation.

---

## 19. Next Action

P0-EP05 is complete. Central may draft P0-EP06 as a separate bounded packet; P0-EP06 execution, CI, fixtures, shell startup, product implementation, and remote changes remain unauthorized unless a new packet is explicitly approved.
