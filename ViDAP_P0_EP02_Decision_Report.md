# ViDAP P0-EP02 Decision Report — Quality, CI, Dependency, and Fixture Decisions

| Field | Value |
|---|---|
| Packet | `ViDAP_P0_EP02.md` — Quality, CI, Dependency, and Fixture Decisions |
| Packet status at execution | Approved for execution, version 1.0 |
| Worker authority | Current explicit user direction; packet Section 1; Spine Section 1 authority order |
| Parent | `ViDAP_Phase_0_Plan.md` version 1.0, WS0.1, D0.4–D0.7 |
| Prerequisite | P0-EP01 complete; accepted decisions are in `ViDAP_P0_EP01_Validation_and_Reconciliation.md` |
| Report date / primary-source retrieval date | 2026-09-17 |
| Authorized repository output | This file only |
| Worker status at final revision | Revised after independent findings `V-EP02-001` and `V-EP02-002`; at that time this remained worker policy evidence pending fresh independent validation and Central acceptance. |
| Central disposition | Accepted after independent revalidation returned `Accept`; see `ViDAP_P0_EP02_Validation_and_Reconciliation.md`, 2026-09-17. |

## 1. Scope, inputs, and evidence method

This is a documentation-only decision record. It selects quality roles and policies, but it does not install, execute, configure, or prove any candidate tool. Exact package versions, complete direct/transitive evidence, and executable task implementation remain work for the separately approved implementation packets.

The worker read the current approved governing inputs required by EP02 Section 3:

| Input | Version / status used | Consequence preserved here |
|---|---|---|
| `ViDAP_Overview.txt` | Governing product specification | OV §§9, 18–25, 28, and 30 require real, inspectable computation; quality as delivery; actionable failure; minimal scope; independent review; known-provenance data. |
| `ViDAP_Phased_Plan_Spine.md` | Approved v1.0 | The authority order, Windows-only evidence posture, testing/dependency/data invariants, Phase 0 exit evidence, and no self-acceptance rule apply. |
| `ViDAP_Roadmap.md` | Approved v1.0 | A0 requires proportionate tooling and policy; quality, reproducibility, licensing, security/data responsibility, and accessibility remain cross-cutting tracks. |
| `ViDAP_Phase_0_Plan.md` | Approved v1.0 | D0.4–D0.7, one-tool-per-role, lock discipline, meaningful gates, no secret material, synced-workspace safety, and P0-EP03–EP08 handoffs apply. |
| `ViDAP_P0_EP01_Decision_Report.md` | Historical worker evidence; superseded where reconciliation differs | Supplies the baseline and handoff constraints, but its recommendations are not treated as accepted when the reconciliation says otherwise. |
| `ViDAP_P0_EP01_Validation_and_Reconciliation.md` | Accepted by Central, 2026-09-17 | D0.1–D0.3 are authoritative: local React/React Flow UI; separate local CPython/FastAPI host; one repository; CPython 3.14.x compatibility stop gate; uv; Node 24 LTS/npm; root `npm.cmd` task entry; Windows only. |

External facts below are from official documentation, official repositories, package registries controlled by the publisher, or GitHub documentation. They are evidence for the recommendation, not vendor claims that ViDAP has been installed, tested, secured, or made accessible. License classifications are operational policy, not legal advice; P0-EP06 must review the actual locked graph and notices.

## 2. Execution-time baseline and preconditions

| Precondition / fact | Result |
|---|---|
| Explicit authorization | Met. EP02 says `Approved for execution`; the current user direction expressly authorizes bounded execution. |
| EP01 acceptance state | Met. The reconciliation records P0-EP01 `Complete`, accepts D0.1/D0.2, and accepts D0.3 with the CPython 3.14 amendment. |
| Branch and commit | `main...origin/main` at `bac14c5d5722cee6c16ebfb538646dc815cd1cd2`. |
| Remote | `origin` is the existing GitHub remote. No remote state was inspected beyond its configured URL and no remote state was changed. |
| File inventory before this output | The eight governing/planning/EP01/EP02 documents only. No source tree, manifest, lockfile, dependency directory, test directory, CI workflow, license file, fixture, environment, cache, or build output exists. |
| Pre-existing worktree delta | Tracked modifications: `ViDAP_Phase_0_Plan.md`, `ViDAP_Roadmap.md`. Untracked: `ViDAP_P0_EP01.md`, `ViDAP_P0_EP01_Decision_Report.md`, `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, and the approved `ViDAP_P0_EP02.md`. These are pre-existing planning/promotion inputs, not work by this worker. |
| Output-path conflict before write | None. `ViDAP_P0_EP02_Decision_Report.md` did not exist. |
| Environment posture | EP01's same-day, accepted baseline remains the relevant evidence: Windows host, Windows PowerShell 5.1, Node 25/npm 11 ambiently installed but explicitly non-authoritative, no installed Python, and direct `npm.ps1` blocked while `npm.cmd` is available. This worker did not execute a candidate tool to refresh those observations. |
| Research / execution boundary | Current official-source web research was permitted and used. No candidate quality, testing, CI, dependency, license, vulnerability, or fixture tool was installed or executed. |

The delta from the EP01 reconciliation is the approved EP02 packet and this report only. The repository still satisfies the greenfield premise for later P0 packets.

## 3. Decisions at a glance

| Decision | Recommendation |
|---|---|
| D0.4 quality and test layers | TypeScript `tsc --noEmit`; Prettier; ESLint flat config with `typescript-eslint`, React Hooks, and `jsx-a11y`; Vitest + React Testing Library + jsdom; Ruff; mypy; pytest + AnyIO + HTTPX ASGI transport; direct `coverage.py` and Vitest V8 reports with no P0 threshold; and a repository-owned Node 24 cross-process smoke harness. Full browser E2E is explicitly deferred to P3. |
| D0.5 CI and branches | GitHub Actions on `windows-latest` is the blocking CI lane and executes root `npm.cmd run` tasks. PR, `main` push, manual, and weekly scheduled triggers; read-only permissions; no secrets; lock-keyed caches; pinned third-party actions; and review plus required-check expectations are defined without changing GitHub settings. |
| D0.6 dependencies and updates | `npm ci` and `uv sync --locked` define locked installs. `license-checker-rseidelsohn` plus `pip-licenses` produce license inventories; `npm audit` plus the lock-faithful `uv export --locked` to `pip-audit` requirements-file flow produce advisory evidence. `pip-audit --locked` is prohibited because it does not consume `uv.lock`. Unknown/disallowed licenses fail; high/critical findings require a documented triage before merge. Dependabot is limited to npm and GitHub Actions in P0; uv bot updates are deferred because current upstream UV update issues could create invalid lock diffs. No P0 SBOM is required. |
| D0.7 fixtures | Synthetic/generated-first text fixtures only: UTF-8 `.json`, `.csv`, `.txt`, or `.yaml`; 16 KiB per file and 64 KiB total in root `fixtures/`; metadata, provenance, license, expected properties, and privacy controls are mandatory. P0-EP07 may add one ≤1 KiB synthetic harness fixture, not a product dataset. |

## 4. Current primary-source bibliography

All links were retrieved on 2026-09-17. Sources are grouped so an implementation worker and validator can trace the precise claims without treating a release number observed today as a future pin.

| ID | Primary source | Evidence used |
|---|---|---|
| E01 | [TypeScript compiler options](https://www.typescriptlang.org/docs/handbook/compiler-options) and [`noEmit` TSConfig reference](https://www.typescriptlang.org/tsconfig/#noEmit) | `tsc` reads `tsconfig`; `--noEmit` separates type checking from output generation. |
| E02 | [TypeScript repository and license](https://github.com/microsoft/TypeScript) | TypeScript is Apache-2.0. |
| E03 | [Prettier CLI](https://prettier.io/docs/cli), [install guidance](https://prettier.io/docs/install), and [configuration](https://prettier.io/docs/configuration) | `--check` is a non-writing CI gate; `--write` is separate; project-local configuration is intended; Node 24 is compatible with a data configuration. |
| E04 | [ESLint getting started](https://eslint.org/docs/latest/use/getting-started), [version support](https://eslint.org/version-support/), and [license](https://github.com/eslint/eslint/blob/main/LICENSE) | Current ESLint supports Node `>=24`, uses flat configuration, and is MIT licensed. |
| E05 | [typescript-eslint flat-config guide](https://typescript-eslint.io/getting-started/), [React Hooks ESLint plugin](https://react.dev/reference/eslint-plugin-react-hooks), and [`eslint-plugin-jsx-a11y` license](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/main/LICENSE.md) | TypeScript linting and React Hooks rules have first-party guidance; JSX accessibility rules are an MIT-licensed lint layer, not an accessibility proof. |
| E06 | [Vitest guide](https://vitest.dev/guide/), [Vitest coverage guide](https://vitest.dev/guide/coverage.html), [Vitest license](https://github.com/vitest-dev/vitest/blob/main/LICENSE), and [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) | Vitest requires Node `>=22.12`, supports a project-local installation and V8 coverage; Testing Library exercises rendered DOM behavior. |
| E07 | [Ruff overview](https://docs.astral.sh/ruff/), [formatter](https://docs.astral.sh/ruff/formatter/), [configuration](https://docs.astral.sh/ruff/configuration/), and [license](https://github.com/astral-sh/ruff/blob/main/LICENSE) | Ruff supports Python 3.14, formatting check/fix behavior, import rules, `pyproject.toml`, and an MIT path. |
| E08 | [mypy release notes](https://mypy.readthedocs.io/en/stable/changelog.html) and [mypy license](https://github.com/python/mypy/blob/master/LICENSE) | Current mypy records Python 3.14 support and MIT as its main license, with PSF-licensed bundled portions to be captured by the locked-graph review. |
| E09 | [pytest documentation](https://docs.pytest.org/en/stable/), [strict markers](https://docs.pytest.org/en/stable/how-to/mark.html), [AnyIO pytest testing](https://anyio.readthedocs.io/en/stable/testing.html), and [FastAPI async tests](https://fastapi.tiangolo.com/advanced/async-tests/) | pytest supports Python 3.10+; registered strict markers, AnyIO async fixtures/markers, and HTTPX/ASGI transport support the proposed testing posture. |
| E10 | [coverage.py repository](https://github.com/coveragepy/coveragepy) | Current coverage.py supports Python 3.10–3.15 beta and is Apache-2.0. |
| E11 | [Playwright browser policy](https://playwright.dev/docs/browsers) | Browser binaries are a separate, OS-specific download and may consume hundreds of MB; this supports P0 deferral rather than a silent browser acquisition. |
| E12 | [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners), [billing](https://docs.github.com/en/actions/concepts/billing-and-usage), [dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [secure use](https://docs.github.com/en/actions/reference/security/secure-use), and [artifact retention](https://docs.github.com/en/actions/tutorials/store-and-share-data) | Windows hosted runners, minimum permissions, concurrency, public-repo free usage, lockfile cache keys, full-SHA action pinning, and bounded artifacts are supported policy levers. |
| E13 | [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/), [uv locking/syncing](https://docs.astral.sh/uv/concepts/projects/sync/), and [uv cache policy](https://docs.astral.sh/uv/concepts/cache/) | `uv sync --locked`, full-SHA setup action examples, lock-keyed caching, and `uv cache prune --ci` are documented. |
| E14 | [`npm ci`](https://docs.npmjs.com/cli/v11/commands/npm-ci/) and [`npm audit`](https://docs.npmjs.com/cli/v11/commands/npm-audit/) | `npm ci` validates and does not write package files; audit is advisory evidence and `audit fix` mutates the install graph. |
| E15 | [`license-checker-rseidelsohn` v5.0.1 manifest](https://raw.githubusercontent.com/RSeidelsohn/license-checker-rseidelsohn/v5.0.1/package.json) and [README](https://raw.githubusercontent.com/RSeidelsohn/license-checker-rseidelsohn/v5.0.1/README.md) | The released tool states BSD-3-Clause, Node `>=24`, npm `>=11`, JSON output, unknown detection, license files, and allow/fail controls. |
| E16 | [`pip-licenses` project metadata](https://raw.githubusercontent.com/raimon49/pip-licenses/master/pyproject.toml) and [PyPI documentation](https://pypi.org/project/pip-licenses/) | Current metadata states MIT, Python `>=3.9`, Python 3.14 support, JSON output, license-file and notice-file handling. |
| E17 | [`pip-audit` PyPI page](https://pypi.org/project/pip-audit/) and [project metadata](https://github.com/pypa/pip-audit/blob/main/pyproject.toml) | Current tool supports Python 3.14, requirements-file audits, JSON/CycloneDX output, PyPI/OSV sources, and Apache-2.0 licensing. Its `--locked` project-path mode currently supports only `pyproject.toml` and `pylock.*.toml`, **not** `uv.lock`; a fully pinned, hashed requirements file can instead be audited with `--require-hashes`, and `--disable-pip` prevents pip dependency resolution. |
| E18 | [`uv export` reference](https://docs.astral.sh/uv/reference/cli/#uv-export) and [uv lock-export concepts](https://docs.astral.sh/uv/concepts/projects/export/) | `uv export` exports `uv.lock` to `requirements.txt`; `--locked` prevents re-locking and fails if the lock needs an update. Export includes hashes unless `--no-hashes` is supplied; all extras/groups can be selected, the first-party project can be excluded while retaining its dependencies, and output can be written to a named temporary file. |
| E19 | [Dependabot version updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates), [Dependabot Core](https://github.com/dependabot/dependabot-core), and [current UV issue evidence](https://github.com/dependabot/dependabot-core/issues/15253) | Version/update PRs are available to GitHub repositories; the upstream core supports UV but current UV lock-update defects justify limiting P0 bot scope. |
| E20 | [GitHub Actions workflow commands: environment files](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#setting-an-environment-variable) | A value reaches subsequent workflow steps only when written to `GITHUB_ENV`; a value assigned in one `run` step is otherwise step-local. This policy instead recomputes one fixed child of `RUNNER_TEMP` in every audit, artifact, and cleanup step, avoiding cross-step state. |

## 5. Universal-gate application

`P` means the selection passes the applicable universal gate based on the evidence above; `N/A` means the gate does not apply to a standard-library method or hosted feature. A pass is not permission to bypass the inherited P0-EP04 Python 3.14 exact-wheel stop gate or P0-EP06 full locked-graph review.

| ID | Selected tool or feature (one role) | UG-01 through UG-10 result | Confidence | Implementation-time verifier / constraint |
|---|---|---|---|---|
| Q01 | TypeScript compiler (`tsc`) — UI type check only | P01–P10 | High | P0-EP04 locks a Node 24-compatible release; P0-EP05 proves `--noEmit` produces no output. |
| Q02 | Prettier — UI/document formatting only | P01–P10 | High | P0-EP04 uses local, locked Prettier and data configuration; P0-EP05 proves check does not write and write is opt-in. |
| Q03 | ESLint flat-config ensemble — UI static lint only | P01–P10 | High | P0-EP04 locks ESLint with TypeScript/React/a11y plugins; P0-EP05 proves React Hooks, TS, and a11y diagnostics are clear. |
| Q04 | Vitest + React Testing Library + jsdom — UI unit/component tests only | P01–P10 | High | P0-EP04 locks versions compatible with Node 24; P0-EP05 has at least one real shell/component assertion and deterministic configuration. |
| Q05 | Ruff — Python format, lint, and import ordering only | P01–P10 | High | P0-EP04 verifies an exact CPython 3.14 Windows distribution; P0-EP05 enables targeted import rules and proves check/fix separation. |
| Q06 | mypy — Python type check only | P01–P10 | Medium | P0-EP04 must lock a current Python 3.14-compatible release; P0-EP05 verifies strict initial config against FastAPI typing. The confidence is medium because mypy’s initial 3.14 support notes caveats. |
| Q07 | pytest + AnyIO + HTTPX ASGI transport — Python unit/integration tests only | P01–P10 | High | P0-EP04 verifies exact Windows/Python 3.14 wheels. P0-EP05 registers markers and uses the async fixture rules; no second async runner. |
| Q08 | Vitest V8 coverage + direct `coverage.py` — report only | P01–P10 | High | P0-EP05 configures source-only measurement, no threshold, and ignores generated output. No coverage package is a substitute for meaningful tests. |
| Q09 | Repository-owned Node 24 process harness — cross-process smoke only | P01–P10 | High | P0-EP07 implements it with Node built-ins, no orchestration package. It must start, wait, log, time out, and terminate process trees on all paths. |
| Q10 | GitHub Actions — hosted CI execution only | P01–P06, P08–P10; UG-07 N/A | High | P0-EP06 pins third-party actions by full SHA and validates `windows-latest` execution. It is not a redistributable dependency and never becomes a local-only quality truth. |
| Q11 | `license-checker-rseidelsohn` + `pip-licenses` — lock-installed license inventory only | P01–P10 | Medium | P0-EP06 confirms released versions, actual Windows execution, full notice capture, unknown failure, and the complete transitive graph. The Node scanner’s current release is active but maintainer capacity warrants the medium confidence. |
| Q12 | `npm audit` + `uv.lock`-exported `pip-audit` requirements audit — vulnerability-advisory evidence only | P01–P10 | High | P0-EP06 must run the Section 8 `uv export --locked`/hashed-requirements command and then `pip-audit --require-hashes --disable-pip`; it must never use `pip-audit --locked`, `audit fix`, or a lock-changing command in a check. Every finding receives human triage. |
| Q13 | Dependabot for npm and GitHub Actions only — update PR generation only | P01–P06, P08–P10; UG-07 N/A | High | P0-EP06 restricts PR count/grouping and validates every PR through locked tasks. UV automation is deliberately not selected until upstream lock-diff behavior is re-evaluated. |

### Gate evidence and safety interpretation

All Q01–Q13 are repository-managed, lock-compatible, locally invocable through the inherited root npm entry, and have a distinct pass/fail purpose. Their checks are read-only by default: `tsc --noEmit`, `prettier --check`, `eslint`, `vitest run`, `ruff format --check`, `ruff check`, `mypy`, `pytest`, coverage report, inventory/report commands, and audit/report commands. Fix/write actions are separately named and never included in `check` or CI.

The selected tools produce file/check-specific diagnostics or machine-readable reports. Caches are explicitly non-authoritative and may be bypassed. Browser automation is not selected in P0, so it cannot silently acquire browser binaries. GitHub Actions is selected only for a public/open-source-compatible, Windows-hosted execution lane; it remains provider-neutral because its jobs invoke the same root tasks a contributor runs locally.

## 6. D0.4 — quality and test-layer decisions

### Role decisions and local/CI paths

| Required layer | Decision and non-overlap | Local task / later CI path | Phase 0 target and policy |
|---|---|---|---|
| TypeScript compilation/type checking | **TypeScript `tsc --noEmit`** is the type checker. `tsconfig` owns strict compiler behavior. Emission is separate: the UI build owns output; `typecheck` never emits. | `npm.cmd run typecheck` → same root task in Windows CI. | Catch UI contract, component, and import typing errors without dirtying the tree. P0-EP05 must make strict mode and no generated compiler state the default. |
| Frontend formatting | **Prettier** owns formatting of UI code and selected text/config formats. `format:check` uses `--check`; `format:write` is a deliberate developer repair task. | `npm.cmd run format:check` → CI invokes the identical task. | No ESLint style rules that duplicate Prettier. Project configuration and ignore rules, not user editor settings, are authoritative. |
| Frontend linting | **ESLint flat config** owns static bug, TypeScript, React Hooks, and JSX accessibility rules: `typescript-eslint`, `eslint-plugin-react-hooks`, and `eslint-plugin-jsx-a11y`. | `npm.cmd run lint` / deliberate `lint:fix` → CI runs `lint`, never fix. | `jsx-a11y` is a static safety net, not proof of keyboard or screen-reader acceptance; P3 owns actual graph-editor accessibility evidence. |
| Frontend unit/component tests | **Vitest** is the sole UI runner; React Testing Library runs rendered DOM assertions in **jsdom**. | `npm.cmd run test:unit` delegates UI and Python unit suites; CI uses the same task. | Deterministic `vitest run` only in CI; fake clocks/randomness and mocked network must be restored per test. Test user-visible shell behavior, not React implementation internals. |
| Browser/E2E smoke tests | **Explicitly deferred to P3; Playwright is not selected or acquired in P0.** | No P0 task or CI browser job. | Playwright requires version-coupled browser downloads and can install branded browsers globally. P0 has no graph interaction to justify that surface. P3 must separately choose a browser tool and use a repository-controlled, ignored/cache-isolated browser path; it must not alter a contributor’s browser. |
| Python formatting/linting | **Ruff** owns both roles, preventing Black + isort + Flake8 overlap. `ruff format --check` is format evidence; `ruff check` is lint evidence. Import ordering uses Ruff `I` rules and explicit first-party packages. | Root `format:check` delegates `uv run --locked ruff format --check`; `lint` delegates `uv run --locked ruff check`. Write/fix tasks are separate. | Start with stable Ruff default correctness rules plus `I`, `UP`, `B`, and targeted security/error rules only after P0-EP05 validates their signal. Do not enable preview rules or broad docstring/style doctrine merely to increase gate count. |
| Python type checking | **mypy** owns Python static typing. | Root `typecheck` delegates `uv run --locked mypy`; CI uses the same root task. | Start with `python_version = 3.14`, strict first-party source, explicit package roots, `warn_return_any`, `warn_unused_ignores`, `warn_redundant_casts`, `warn_unused_configs`, `no_implicit_optional`, and no blanket `ignore_missing_imports`. Prefer `py.typed`; lock an approved `types-…` stub where needed. A missing/inaccurate third-party type needs a narrow documented override, stub, or upstream issue—not a global blind spot. |
| Python unit/integration tests | **pytest** owns Python test collection and assertion reporting. **AnyIO** is the async pytest integration; **HTTPX ASGI transport** is the in-process API-client path. | `test:unit` and `test:integration` delegate `uv run --locked pytest` with registered markers. | Register `unit`, `integration`, `smoke`, and `slow` markers and enable strict markers. Default unit task excludes `integration`, `smoke`, and `slow`; CI runs the selected tasks explicitly. Async tests use `pytest.mark.anyio`, one declared `asyncio` backend unless a later packet approves multi-backend coverage. No `pytest-asyncio` is added. |
| Cross-process smoke | **Repository-owned Node 24 harness**, not `concurrently`, `wait-on`, or `start-server-and-test`. | `npm.cmd run test:integration` runs a narrow in-process suite; `npm.cmd run smoke` runs the process harness. CI uses the same `smoke` task. | P0-EP07 owns startup. It starts only declared UI/Python processes on loopback, captures separate logs, waits for a P0-owned readiness signal with a finite 60-second ceiling, fails on early exit or timeout, and terminates the full process trees in `finally`/equivalent on success, failure, cancellation, and Ctrl+C. It creates no API/workflow contract beyond the later-owned health/status behavior. |
| Clean-setup verification | **No extra tool.** A fresh checkout/ephemeral Windows runner performs declared, locked setup and root tasks. | P0-EP08 independently uses `npm ci`, `uv sync --locked`, then root tasks; it must not reuse workstation `node_modules`, `.venv`, or caches as proof. | This proves manifests/locks, not ambient workstation state. The current worktree is never cleaned or reset for this purpose. |
| Coverage | **Vitest V8** and direct **coverage.py** reports are selected, but **no numeric threshold begins in P0**. | Optional `coverage` report task is separate from required `check` until meaningful source and test surfaces exist. | Measure only first-party UI/Python source; exclude generated files, tests, configuration, and type-only declarations. P0’s shell tests are too small for an honest percentage. P0-EP05 must publish the initial report; Central sets any ratcheted threshold after P1 has meaningful semantic behavior. |
| Authoritative root tasks | The stable taxonomy below is selected; exact `package.json` scripts/configuration are deferred. | Every CI job calls a root task via `npm.cmd run <task>` on Windows. | Root npm is the only contributor-facing cross-stack dispatcher; it invokes local binaries and `uv run --locked`, never a global tool, `npx` download, policy change, or second task runner. |

### Root task taxonomy and parity rule

| Category | Stable task name | Required behavior once implemented |
|---|---|---|
| Formatting check / repair | `format:check`, `format:write` | Check is non-mutating; write is opt-in and excluded from CI. |
| Lint / repair | `lint`, `lint:fix` | Check is non-mutating; fix is opt-in and excluded from CI. |
| Type checking | `typecheck` | Runs `tsc --noEmit` and mypy under their locked environments. |
| Unit tests | `test:unit` | Runs deterministic UI and Python unit tests; no network, real clock, user path, or prior cache dependency. |
| Integration tests | `test:integration` | Runs explicitly marked Python/boundary integration checks; it does not start arbitrary background services. |
| Cross-process smoke | `smoke` | Starts/stops only declared local processes and leaves no orphan. |
| Build | `build` | Builds only the Phase 0 shell and writes solely to ignored output. It is not a typecheck substitute. |
| Aggregate | `check` | Ordered aggregate: `format:check` → `lint` → `typecheck` → `test:unit` → `build` → `test:integration` → `smoke`. It fails at the first failed underlying task and does no automatic repair. |
| Dependency/license evidence | `deps:inventory`, `license:check`, `deps:audit` | Produces reviewable reports and enforces unknown/disallowed license policy; no automated update/fix. |

Local/CI parity is semantic, not merely similarly named scripts: each Windows CI job must call these root tasks, using `npm.cmd`, after `npm ci` and `uv sync --locked`. CI may set report/log destinations and time ceilings, but may not substitute a hosted-only scanner, use floating installs, skip a local gate, or run a repair command. Caches are accelerators only; a cache miss must still pass, and scheduled clean runs bypass restored caches at least weekly.

### Comparisons and rejected D0.4 alternatives

| Choice | Credible alternative | Decision reason |
|---|---|---|
| Prettier | Biome as formatter/linter; ESLint formatting rules | Prettier cleanly separates stable formatting from static analysis and has explicit check/write behavior. Biome would overlap the selected lint role and add a native-binary tool before P0 has a measured need. ESLint is not a formatter. |
| ESLint ensemble | Biome-only lint; Prettier-only checks | ESLint has direct TypeScript flat-config guidance and React’s own Hooks plugin; `jsx-a11y` adds a useful static posture. A formatter alone cannot provide semantic linting. |
| Vitest + RTL | Jest + RTL | Vitest is Vite-aligned, requires Node 22.12+ (satisfied by Node 24), and avoids a second bundler/test configuration family. RTL is a helper, not a competing runner. |
| Browser tests deferred | Playwright or WebdriverIO now | Full browser automation is valid later, but P0 lacks visual graph behavior. Playwright’s browser acquisition and cache surface is disproportionate now; deferral avoids an ornamental E2E test. |
| Ruff | Black + isort + Flake8 plugins | Ruff covers format, lint, and imports with project config and distinct check/fix commands. The three-tool route creates overlapping format/import responsibility without a Phase 0 benefit. |
| mypy | Pyright | Both are credible. Mypy is selected because it lives in the locked Python tool chain and has current Python 3.14 evidence; Pyright would add a second Node-hosted Python-analysis path. |
| pytest + AnyIO | `unittest`; pytest + pytest-asyncio | pytest offers fixtures/markers and clear diagnostics; AnyIO supplies the required async plugin without another async runner. |
| Native process harness | `concurrently`, `wait-on`, `start-server-and-test` | A small, explicit Node 24 owner eliminates an orchestration dependency and gives P0-EP07 precise cleanup responsibility. It is deliberately constrained to the P0 shell. |
| No P0 coverage threshold | A 70–90% threshold immediately | Tiny shell code and one foundation test can create a misleading percentage. Reporting first gives a baseline; meaningful thresholding belongs after P1 behavior exists. |

## 7. D0.5 — CI and branch policy

### CI host, runners, triggers, and jobs

GitHub Actions is the selected CI host. It is suitable for the intended public open-source repository because standard hosted runners are free for public repositories; this is not a claim that a private repository has unlimited free Windows minutes. No self-hosted runner, paid service, organization-only control, container, or secret is required. If hosted capacity is unavailable, the authoritative local tasks remain runnable and a Central decision is required before claiming a substitute CI service.

| Topic | Policy for P0-EP06 implementation |
|---|---|
| Blocking runner | `windows-latest`, PowerShell, and `npm.cmd`. This is the only blocking platform because Windows is the sole supported development platform. Image drift is monitored by the weekly run; use a pinned Windows image only if `windows-latest` change evidence justifies it. |
| Additional runner | None in P0. An Ubuntu or macOS advisory lane would not establish supported-platform status and is deferred until its clean-environment validation is approved. |
| Triggers | `pull_request` to `main`; push to `main`; `workflow_dispatch`; and one weekly scheduled clean/cached-bypass run. No `pull_request_target`, release, deployment, or write-triggered workflow. |
| Permissions / secrets | Top-level `permissions: contents: read`; all other permissions absent unless a future documented job needs less-restrictive access. No repository, organization, registry, cloud, browser, or personal secret is consumed. CI logs must mask built-in tokens and never print environment dumps. |
| Job boundaries | `quality-windows` runs the locked setup and `check`; `dependency-license-windows` runs inventory/license/audit evidence; and any artifact upload is a final conditional step. Jobs may run in parallel because no job is an authority for another; `quality-windows` must succeed before a PR is considered green. `fail-fast` applies within a matrix if one is later introduced; P0 has no matrix. |
| Install / parity | Set up the declared Node 24 and uv/managed CPython 3.14 chain using full-SHA-pinned official actions. Run `npm ci`, `uv sync --locked --all-extras --all-groups`, and only root `npm.cmd run` tasks. The locked Python setup must contain the declared `pip-audit` development tool before the audit task starts. No `npx` temporary download, `npm install`, `uv lock`, or tool update occurs in a check. |
| Caches | Cache npm download cache and uv package cache only, never `node_modules`, `.venv`, browser binaries, build output, reports, or a whole workspace. Keys include OS, architecture where exposed, Node major/tool version, uv version, and hashes of the relevant `package-lock.json`, `pyproject.toml`, and `uv.lock`; no broad cross-OS restore. A scheduled clean run has cache disabled; `uv cache prune --ci` may run after evidence capture. |
| Artifacts / logs | Retain failure logs and machine-readable dependency, license, vulnerability, and coverage summaries for 14 days, subject to repository retention limits. The Python-audit JSON is written only under the fixed, bounded path `RUNNER_TEMP\\vidap-pip-audit\\pip-audit.json`, uploaded from that path with an `always()` conditional so a vulnerability exit does not suppress evidence, then removed by a final `always()` cleanup step that recomputes and bounds the same path. No step relies on an environment assignment from an earlier step (E20). Upload no datasets, fixtures beyond the already committed tiny text fixture, secrets, `.venv`, `node_modules`, browser cache, dependency cache, full source checkout, or environment dump. Upload only on failure for diagnostic logs and on success for the small review reports. |
| Concurrency | One group per workflow plus PR branch/ref. Superseded PR runs use `cancel-in-progress: true`; `main`, manual, and scheduled runs are not cancelled. Cancellation still executes the smoke harness cleanup path. |
| Branch expectation | Proposed changes target `main` through a reviewable PR. At least one human review and passing `quality-windows` plus `dependency-license-windows` are the recommended required checks. This report does not mutate branch protection or claim it is enabled. |
| Third-party actions | Permit only actions necessary for checkout, Node setup, uv setup, cache, and small artifact upload. Every reference is a verified full-length commit SHA with a nearby human-readable release comment. A tag, branch, floating SHA, unreviewed reusable workflow, Docker action, or action requesting write permissions is prohibited. Dependabot may propose action-pin updates but never auto-merges them. |

### Exact P0-EP06 CI acceptance evidence

Before CI is accepted, P0-EP06 must retain: (1) the workflow file and all action full-SHA provenance; (2) a Windows hosted-run URL/ID showing declared Node 24, uv, and managed CPython 3.14; (3) proof that `npm ci` and `uv sync --locked` leave both locks unchanged; (4) logs showing identical root tasks locally and in CI; (5) a cache-hit and cache-miss/weekly-clean result; (6) a deliberate failing format/lint/type/test or lock condition with actionable diagnosis; (7) smoke cleanup evidence with no orphan process; (8) artifact path/retention evidence proving prohibited material was not uploaded; (9) dependency/license/audit reports; and (10) a Git status after the checks showing only ignored/transient outputs.

## 8. D0.6 — dependency, license, vulnerability, and update policy

### Lock graph, inventory, and license rules

| Area | Policy |
|---|---|
| Direct dependencies | A direct dependency is an explicit manifest entry. Its PR records name, intended role/owner, phase need, candidate alternatives, license expression/text, maintenance/security evidence, Python 3.14/Windows wheel or Node 24 support as applicable, native/binary/browser impact, and why it belongs in the runtime or dev graph. Product/ML dependencies remain later-phase decisions. |
| Transitive dependencies | A transitive dependency is any resolved package in `package-lock.json` or `uv.lock`. It has no silent approval: P0-EP06 inventories all names, versions, relationships, integrity/source metadata where available, license findings, and notices. A lockfile change is reviewed as a graph change even when the direct manifest diff is small. |
| Install evidence | JavaScript inventory is made after `npm ci`; Python inventory is made after `uv sync --locked`. `npm ci` and `uv sync --locked` are the only normal check/CI installation paths. The graph must be current before reports run. |
| License tools | Node: local locked `license-checker-rseidelsohn` scans installed `node_modules`, emits JSON, includes license file references, treats guessed/unknown as unresolved, and applies a checked-in clarification record only after review. Python: local locked `pip-licenses --from=all --format=json` emits all installed packages; capture license/notice files for every nontrivial notice obligation. Tool output starts review; it does not decide legal compatibility. |
| Allowed without exception | SPDX-identified MIT, BSD-2-Clause, BSD-3-Clause, ISC, Apache-2.0, 0BSD, Zlib, PSF-2.0, and CC0-1.0, provided required copyright/license/NOTICE text is retained. A dual expression is allowed only when the selected branch is clearly one of these. |
| Review-required | MPL-2.0, EPL-2.0, LGPL-2.1-or-later/LGPL-3.0-or-later, CDDL-1.0, Artistic-2.0, Unicode/data licenses, dual/multi-license expressions, platform-binary redistribution terms, licenses with material notices, and any package with generated/native bundled material. Review means no merge until applicable distribution/notice obligations and an explicit permitted branch are recorded. |
| Normally prohibited | GPL-only, AGPL, SSPL, Commons-Clause/BUSL/non-commercial/no-derivatives terms, unlicensed packages, missing/ambiguous/custom license claims, or a package that cannot supply the required source/notice/provenance. This applies to runtime and committed development/CI graphs unless Central approves an exception. |
| Exceptions | Only Central acting on current explicit user direction may grant one. The decision record must name exact package/version and dependency path; direct/transitive role; full license text/expression and source; distribution/notice/copying analysis; alternatives considered; security/maintenance review; responsible owner; expiry/review trigger; and required artifact/notice handling. Legal advice is sought where obligations are uncertain. |
| Notices | P0-EP06 creates a reviewable notice bundle/report for the actual locked graph, but does not treat a package metadata field as the license text. Distribution-facing notices are refreshed on every graph change. |

### Vulnerability policy and triage

`npm audit --json` and a `uv.lock`-exported `pip-audit` requirements audit are the selected scanners. The former queries the configured npm registry; the latter can use PyPI advisory data or OSV. `pip-audit --locked` is expressly **prohibited**: its current locked-project input supports only `pyproject.toml` and `pylock.*.toml`, not `uv.lock` (E17). The Python procedure below is therefore the sole approved path; it does not resolve, install, or rewrite the project graph during the audit. `npm audit fix`, `pip-audit --fix`, floating resolution, and automatic lock rewrites are prohibited from local checks and CI.

#### Python lock-faithful advisory procedure — revised for V-EP02-001 and V-EP02-002

`uv export` is the bridge from the authoritative `uv.lock` to the requirements-file input that `pip-audit` supports. Its `--locked` switch requires an up-to-date lock and prevents a re-lock; requirements export retains hashes unless `--no-hashes` is selected (E18). The audit must include all selected extras and dependency groups, omit only the first-party project while retaining its third-party dependencies, and fail closed if the export cannot satisfy `pip-audit --require-hashes`. There is no fallback to `pip-audit --locked`, a floating resolver, `--no-deps`, or a hand-maintained requirements file.

P0-EP06 must make the root `npm.cmd run deps:audit` task invoke the following PowerShell command body from the repository root after the normal `uv sync --locked --all-extras --all-groups` setup. This report does not create that task or script. `uv export --no-cache` and the temporary `pip-audit` cache prevent persistent cache writes for this audit; `uv run --no-sync` prevents the audit invocation from synchronizing or changing `.venv`. The prior export is the freshness assertion, so `uv run` need not perform another sync.

```powershell
# Local: npm.cmd run deps:audit executes this body.
# CI deliberately ignores VIDAP_AUDIT_DIR and always uses the fixed RUNNER_TEMP child.
if ($env:GITHUB_ACTIONS -eq "true") {
  $runnerTemp = [System.IO.Path]::GetFullPath($env:RUNNER_TEMP)
  $auditDir = Join-Path $runnerTemp "vidap-pip-audit"
} elseif ($env:VIDAP_AUDIT_DIR) {
  $tempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
  if (-not $tempRoot.EndsWith([string][System.IO.Path]::DirectorySeparatorChar)) {
    $tempRoot += [System.IO.Path]::DirectorySeparatorChar
  }
  $auditDir = [System.IO.Path]::GetFullPath($env:VIDAP_AUDIT_DIR)
  $auditName = [System.IO.Path]::GetFileName($auditDir)
  if (-not $auditDir.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
      $auditName -notmatch '^vidap-pip-audit-[0-9a-f]{32}$') {
    throw "VIDAP_AUDIT_DIR must be a new vidap-pip-audit-<32 lowercase hex> child of the system temp directory."
  }
} else {
  $auditDir = Join-Path ([System.IO.Path]::GetTempPath()) ("vidap-pip-audit-" + [guid]::NewGuid().ToString("N"))
}
if (Test-Path -LiteralPath $auditDir) {
  throw "Refusing to reuse or recursively delete a pre-existing audit directory: $auditDir"
}
$requirements = Join-Path $auditDir "uv-lock.requirements.txt"
$httpCache = Join-Path $auditDir "http-cache"
$report = Join-Path $auditDir "pip-audit.json"
New-Item -ItemType Directory -Force -Path $auditDir | Out-Null
$createdAuditDir = $true
$auditExit = 1
try {
  & uv export --locked --no-cache --all-extras --all-groups --no-emit-project --format requirements.txt --output-file $requirements
  if ($LASTEXITCODE -ne 0) { $auditExit = $LASTEXITCODE; exit $auditExit }

  & uv run --no-sync -- pip-audit --requirement $requirements --require-hashes --disable-pip --strict --cache-dir $httpCache --format json --output $report
  $auditExit = $LASTEXITCODE
  if (Test-Path -LiteralPath $report) { Get-Content -LiteralPath $report }
}
finally {
  Remove-Item -LiteralPath $requirements, $httpCache -Recurse -Force -ErrorAction SilentlyContinue
  if ($createdAuditDir -and $env:GITHUB_ACTIONS -ne "true") {
    Remove-Item -LiteralPath $report, $auditDir -Recurse -Force -ErrorAction SilentlyContinue
  }
}
exit $auditExit
```

The temporary requirements file is the complete, hash-preserving export of the selected `uv.lock` graph; it is never committed, uploaded, or reused. `pip-audit --require-hashes --disable-pip --strict` rejects incomplete/unhashed collection, does not invoke pip resolution, and fails on a collection error (E17). A vulnerability result still writes JSON and returns its documented nonzero exit, so the task must preserve that exit after printing/handling the report; it must not suppress or auto-fix it.

For the Windows CI invocation, P0-EP06 must use the same root task and command body. Every relevant step independently recomputes the one allowed path, `Join-Path ([System.IO.Path]::GetFullPath($env:RUNNER_TEMP)) "vidap-pip-audit"`; it does not depend on a step-local `VIDAP_AUDIT_DIR` assignment or use `GITHUB_ENV`. This is deliberate: GitHub documents that a value becomes available to later steps only through `GITHUB_ENV` (E20), while a deterministic child of the runner-controlled temporary root needs no state transfer.

The CI audit step is:

```powershell
npm.cmd run deps:audit
```

The later steps use these exact expressions; their full-SHA action pin remains a P0-EP06 implementation requirement rather than a change made by this report:

```yaml
- name: Upload Python audit evidence
  if: always()
  uses: actions/upload-artifact@<verified-full-commit-sha> # release comment required
  with:
    name: pip-audit-json
    path: ${{ runner.temp }}\vidap-pip-audit\pip-audit.json
    if-no-files-found: ignore

- name: Remove Python audit temporary files
  if: always()
  shell: pwsh
  run: |
    $runnerTemp = [System.IO.Path]::GetFullPath($env:RUNNER_TEMP)
    $auditDir = Join-Path $runnerTemp "vidap-pip-audit"
    if (-not $auditDir.StartsWith($runnerTemp, [System.StringComparison]::OrdinalIgnoreCase) -or
        [System.IO.Path]::GetFileName($auditDir) -ne "vidap-pip-audit") {
      throw "Refusing to clean a path outside the fixed RUNNER_TEMP audit directory."
    }
    if (Test-Path -LiteralPath $auditDir) {
      $item = Get-Item -LiteralPath $auditDir -Force
      if (-not $item.PSIsContainer -or ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        throw "Refusing to recursively delete a non-directory or reparse point."
      }
      Remove-Item -LiteralPath $auditDir -Recurse -Force -ErrorAction Stop
    }
```

Thus local output is printed and deleted in the same task, while CI retains one runner-temporary JSON file only long enough for the existing 14-day review artifact. The local override is normalized, bounded to system temp, name-constrained, and required to be new before any recursive delete; CI does not honor it. Neither the export, cache, nor report is allowed in the checkout, a cache key, or an artifact beyond that JSON evidence.

1. Every finding is recorded with scanner/source, advisory ID/aliases, package/version/dependency path, directness, severity/CVSS if supplied, detected date, fixed versions, and scan coverage/limitations.
2. Triage distinguishes advisory severity from ViDAP risk: reachability in current code, exposure/attack preconditions, local vs shipped execution, sensitive data or credential impact, platform/binary applicability, exploit maturity, and remediation availability all matter. A clean scan is not proof of safety; an alert is not proof of exploitability.
3. A critical finding is acknowledged within one business day and a high finding within five business days. An unresolved reachable critical/high finding blocks merge/release unless a time-bounded Central exception records mitigation and recheck date. Medium/low findings receive a scheduled disposition; a scanner dispute records reproducible evidence and source status, never a silent ignore.
4. If no fixed version exists, remove/replace/isolate the dependency where feasible; otherwise record reachability, compensating controls, upstream issue, owner, expiry, and each rescan. A lockfile must never be hand-edited to pretend a vulnerable transitive version is fixed.

### Updates, Dependabot, and SBOM

- Review direct dependencies and both locks weekly; perform an emergency update as soon as triage requires it. Every update PR includes changelog/release-note review, regenerated locks, inventory/license/audit reports, required root tasks, and a focused compatibility note.
- Configure Dependabot in P0-EP06 for **npm** and **GitHub Actions** weekly, with at most two open PRs per ecosystem. Group only patch/minor development-tool updates within one ecosystem; leave major updates and security updates individually reviewable. No auto-merge, no bypass of required checks/review, no grouping across ecosystems, and no PR is trusted merely because it is bot-authored.
- **Do not configure Dependabot UV updates in P0.** Dependabot Core has UV support, but current upstream reports identify invalid/out-of-date `uv.lock` diffs. Python updates therefore remain a reviewed weekly `uv lock --upgrade` PR under an approved maintenance task until a later packet rechecks the upstream behavior against the exact ViDAP workspace. This is a safety deferral, not a second package manager.
- A Phase 0 SBOM is **deferred**. P0-EP06’s locked direct/transitive inventories, license reports, and audit reports are the smaller robust evidence for a changing foundation. Revisit a standardized SBOM before the first public release, before a later ML/model library is accepted, or when a distribution artifact is introduced—whichever comes first. `pip-audit` CycloneDX output is a candidate, not an automatically adopted standard.
- Before a later ML/model library is accepted, its owning phase must provide exact supported CPython/Windows distributions; direct/transitive license/notice and binary redistribution evidence; vulnerability/SBOM inventory; maintenance/release policy; resource/native accelerator behavior; model/data-license terms; and a documented reason it does not weaken inspectability, reproducibility, or the MIT project policy.

## 9. D0.7 — controlled fixture policy

| Topic | Policy |
|---|---|
| Ownership and preference | Root `fixtures/` is the canonical shared fixture area from accepted D0.2. Prefer synthetic/generated fixtures. Use an external fixture only where a synthetic one cannot test the approved claim, and never let fixtures define production semantics. |
| P0 allowed formats and size | Committed P0 fixtures may only be UTF-8 `.json`, `.csv`, `.txt`, or `.yaml`. Maximum **16 KiB per fixture** and **64 KiB aggregate** under `fixtures/`, including metadata. Archives, executables, media, notebooks, opaque binaries, and unbounded generated output are prohibited. |
| Required metadata | Each fixture’s central-manifest record or adjacent metadata must state: stable ID/version; repository-relative path; byte size; SHA-256 where the asset is externally sourced or generated; purpose and responsible phase; source/provenance URL or `synthetic`; license/terms and retention of required notice; creation method/tool/source revision; generator version and seed if generated; expected properties/results (not merely a snapshot); permitted consumers; data classification/privacy attestation; and reviewer/date. |
| Data prohibition | Never commit personal, health, credential, token, production, proprietary, scraped without clear permission, ambiguous-license, sensitive, or workstation-derived data. The fixture must contain no absolute path, username, network identifier, hidden telemetry, or real-service endpoint. |
| Determinism | A generator is source-controlled, uses a documented fixed seed when randomness exists, has no network/time/environment dependency, and writes a predictable UTF-8 result. Generated files committed as test oracle inputs must be reproducible from that generator; transient generated outputs are regenerated outside `fixtures/` and ignored. |
| Commit versus regenerate | Commit a tiny static/synthetic input when tests need it as reviewed source material. Commit a generator plus a reviewed small output only when the output itself is an assertion oracle. Do not commit caches, downloaded tool output, large derived data, or ephemeral test artifacts. |
| External fixture / binary review | An external asset requires provenance, exact version/URL/date, terms/license review, checksum, size/privacy assessment, expected-result review, and Central acceptance before commit. Binary assets are prohibited in P0; a later binary exception additionally needs malware/security review and explicit storage justification. |
| Mutation/versioning | A fixture change increments metadata version or creates a new ID, updates checksum/expected properties and affected assertions in one reviewable change, and explains why the prior expected result changed. Tests cannot silently bless new output by overwriting snapshots or metadata. |
| Cleanup / ignore | `fixtures/` contains only reviewed committed assets and metadata. Test reports, downloaded data, browser caches, temporary generation folders, environments, and outputs live outside it or in explicitly ignored transient paths. A passing test leaves no untracked fixture artifact. |
| P0-EP07 allowance | EP07 may add **one synthetic, text-only fixture no larger than 1 KiB** to exercise harness/fixture discovery or a documented shell assertion. It must not imply a workflow schema, data loader, model, Titanic support, healthcare support, scientific support, or product data handling. Titanic remains deferred to P4; healthcare and scientific references remain deferred to their roadmap phases. |

## 10. Downstream implementation handoff

| Packet | Exact constraints handed off |
|---|---|
| P0-EP03 — open-source baseline | Document Windows-only support, local `npm.cmd` entry, no global task packages, dependency/license exception path, data/fixture prohibition, ignored mutable state, and the place for decision records. Do not configure tools or create fixtures. |
| P0-EP04 — reproducible scaffold | Create only accepted topology/manifests/locks/version declarations. Lock Node 24 and CPython 3.14-compatible foundation tools; stop rather than silently fall back if any mandatory Windows Python 3.14 wheel is absent. Create the root taxonomy as scripts that call local tools/`uv run --locked`; no second package manager/task runner. |
| P0-EP05 — quality/test harness | Implement Q01–Q08 only. Add meaningful shell/component/configuration tests, strict markers, deterministic test controls, nonmutating check tasks, explicit write/fix tasks, and report-only coverage. Demonstrate negative diagnostics. Do not add browser E2E or product semantics. |
| P0-EP06 — CI/dependency/license controls | Implement Q10–Q13 plus inventory/audit tasks. Use SHA-pinned actions, Windows root-task parity, least privilege, no secrets, safe caches/artifacts, license exceptions/clarifications, reviewable reports, and current advisory scans. Do not enable Dependabot UV updates or auto-merge. |
| P0-EP07 — fixture/minimal shell | Add only the policy-conforming ≤1 KiB synthetic fixture and the Q09 harness. Implement loopback process lifecycle/readiness/log/timeout/cleanup without defining later health, workflow, or API semantics. |
| P0-EP08 — clean validation | In a fresh checkout/ephemeral environment, independently prove locked setup, every root check, CI parity, cache miss, fixture policy, ignored output, and clean repository state. It does not use this worker’s self-assessment as acceptance. |

## 11. Findings and feasibility spikes

| ID | Finding | Status / owner |
|---|---|---|
| F-01 | Exact version pairs, complete transitive licenses/notices, and Windows Python 3.14 wheels are not yet evidenced because no graph may be installed under EP02. | Non-blocking; P0-EP04 stop gate and P0-EP06 inventory/review. |
| F-02 | mypy’s Python 3.14 support is current but had initial caveats. | Non-blocking; P0-EP04 locks current version and P0-EP05 proves the chosen strict configuration on Windows. Failure stops implementation and returns evidence to Central. |
| F-03 | Dependabot UV support exists, but current upstream lockfile-update reports show invalid or stale diffs. | Non-blocking safety limitation; manual reviewed `uv lock --upgrade` maintenance in P0; re-evaluate before enabling an UV bot. |
| F-04 | Browser automation is a legitimate later quality layer but has no Phase 0 target and brings browser acquisition/cache policy. | Non-blocking explicit deferral; P3 owns selection/evidence. |
| F-05 | Accessibility lint cannot prove accessible graph interaction. | Non-blocking; P3 must define keyboard/readability/task acceptance and test it. |

**Feasibility-spike proposal: none.** Documentary evidence resolves all D0.4–D0.7 choices. The remaining uncertainty is appropriately constrained by implementation-time stop gates and does not justify installing or prototyping under this packet.

## 12. EP02 acceptance-criteria documentary self-assessment

This is a worker self-check of report completeness, evidence traceability, and scope. It is not independent validation and does not accept D0.4–D0.7 for Central.

| Criterion | Self-assessment | Evidence / limitation |
|---|---|---|
| EP02-AC01 | Pass (self-assessed) | Sections 1–2 record authorization, exact inputs, baseline, and pre-existing delta without secrets or user-specific paths. |
| EP02-AC02 | Pass | Section 6 selects or explicitly defers every D0.4 role and names owners/rationale. |
| EP02-AC03 | Revised — fresh independent revalidation required | V-EP02-001 is corrected by the lock-faithful export/audit contract, but the supplied audit returned `Revise` on V-EP02-002. Sections 4, 7, and 8 now require a fixed, bounded `RUNNER_TEMP` path across all CI steps and a fail-closed local override; no acceptance is self-claimed. |
| EP02-AC04 | Pass | Section 6 compares credible alternatives; compiler/task-runner non-comparisons are explained as inherited or artificial. |
| EP02-AC05 | Pass | Section 6 gives distinct purposes to formatting, linting, typing, unit, integration/smoke, clean setup, and coverage. |
| EP02-AC06 | Pass | Prettier/ESLint and Ruff each have separated roles and explicit check versus repair behavior; duplicate runners are rejected. |
| EP02-AC07 | Pass | Section 6 establishes root Windows `npm.cmd` categories, locked `uv` delegation, and no global package/policy requirement. |
| EP02-AC08 | Pass | Sections 6–7 require CI to invoke the same underlying root tasks. |
| EP02-AC09 | Revised — fresh independent revalidation required | V-EP02-002 found the prior cleanup cross-step environment assumption invalid. Section 7 and the exact Section 8 CI steps now use the same deterministic `RUNNER_TEMP\\vidap-pip-audit` path for audit, artifact, and cleanup, with no step-state inheritance. |
| EP02-AC10 | Pass | GitHub-hosted public-repository use is evidence-backed; no paid, organization-only, self-hosted, or unsupported-platform premise is used. |
| EP02-AC11 | Pass | Section 8 covers direct/transitive graphs, license categories, exceptions, unknown/custom/multi-license cases, notices, and future ML evidence. |
| EP02-AC12 | Pass | Section 8 separates severity from reachability/exposure/remediation and specifies triage/no-fix handling. |
| EP02-AC13 | Pass | Section 8 sets routine/emergency update rules, locked review, limited bot grouping/rate, and no auto-merge. |
| EP02-AC14 | Pass | Section 9 sets provenance, licenses, privacy, formats, exact size, deterministic generation, metadata, mutation, and transient-output rules. |
| EP02-AC15 | Pass | Section 9 limits P0 to a ≤1 KiB synthetic harness fixture and explicitly excludes all later datasets/domains. |
| EP02-AC16 | Pass | Section 10 assigns specific implementation constraints to P0-EP03 through P0-EP08 without doing their work. |
| EP02-AC17 | Revised — fresh independent revalidation required | E17–E18 cite the corrected `pip-audit`/`uv export` method; E20 cites GitHub Actions environment-file semantics and supports the V-EP02-002 deterministic-path correction. |
| EP02-AC18 | Pass | No tool was installed/executed and no configuration, workflow, fixture, remote setting, scaffold, manifest, lockfile, or product behavior was added. |
| EP02-AC19 | Pass (self-assessed) | Section 13's final read-only Git inspection distinguishes the two pre-existing tracked planning changes and four pre-existing untracked inputs from this sole EP02 worker output. |
| EP02-AC20 | Not met | The supplied independent audit verdict is `Revise` (V-EP02-002), and Central has not accepted D0.4–D0.7. This correction requests fresh validation; it does not convert that verdict to `Accept`. |

## 13. Final file-scope evidence and validation readiness

The original final read-only inspection found `main...origin/main` at `bac14c5d5722cee6c16ebfb538646dc815cd1cd2` with no ahead/behind marker. `git diff --name-status` listed only `M ViDAP_Phase_0_Plan.md` and `M ViDAP_Roadmap.md`, the pre-existing tracked planning-promotion changes. `git ls-files --others --exclude-standard` listed the four pre-existing untracked inputs (`ViDAP_P0_EP01.md`, `ViDAP_P0_EP01_Decision_Report.md`, `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, and `ViDAP_P0_EP02.md`) plus this report, the worker's sole output. The supplied independent audit separately reports that Git/file scope passes and no scaffold, manifest, lock, workflow, fixture, dependency, or build artifact exists. These V-EP02-001/V-EP02-002 corrections change only this report; no new self-validation or file-scope claim is made here.

**Validation readiness:** Ready for a fresh independent validator under EP02 Section 18. The validator must first recheck V-EP02-001 and V-EP02-002: confirm that `pip-audit --locked` is prohibited; `uv export --locked --all-extras --all-groups --no-emit-project --format requirements.txt` is the source of the requirements input; hashes remain required; pip resolution is disabled; the audit, artifact, and cleanup steps each derive exactly `RUNNER_TEMP\\vidap-pip-audit`; and no unvalidated local override can reach a recursive delete. It should then recheck representative high-impact source claims (Node 24/Python 3.14 compatibility, license scanner support, GitHub Actions security/cache policy, Dependabot UV limitation, and Playwright deferral); challenge the frontend, Python typing, CI, dependency/license, and fixture alternatives; verify all D0.4–D0.7 rows and gate results; and return `Accept`, `Revise`, or `Blocked` without accepting on Central’s behalf or beginning a later packet.

## 14. Evidence return to Central

| Required handoff item | Evidence |
|---|---|
| Decision report | `ViDAP_P0_EP02_Decision_Report.md` |
| Current commit / final worktree | `bac14c5d5722cee6c16ebfb538646dc815cd1cd2`; final read-only scope evidence is in Section 13. |
| Read-only work | Governing-input reads; `git status`, `git rev-parse`, `git remote`, output-path check, and `rg --files`; current primary-source research listed in Section 4. |
| Mutation confirmation | No tool install/execution, system/configuration/remote mutation, fixture, scaffold, manifest, lockfile, CI workflow, or product behavior. This report is the only authorized worker output. |
| D0.4–D0.7 summary | Section 3, with detail in Sections 5–10. |
| Worker self-assessment | Section 12; the supplied validator verdict is `Revise`, so AC03/AC09/AC17 require fresh independent revalidation and AC20 is not met pending an `Accept` plus Central acceptance. |
| Blocking / non-blocking / spike | Section 11. No blocking finding or feasibility spike. |
| Independent-validation handoff | Section 13. Execution stops here; no validator report, acceptance, EP03, configuration, or scaffolding is performed. |
