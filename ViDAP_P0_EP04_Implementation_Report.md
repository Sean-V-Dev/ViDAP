# ViDAP P0-EP04 Implementation Report

| Field | Value |
|---|---|
| Packet | P0-EP04 - Reproducible Project Scaffold |
| Packet version | 1.0 |
| Approval | Explicit user direction; packet status `Approved for execution` |
| Date | 2026-09-18 |
| Worker role | Bounded scaffold worker |
| Outcome | Scaffold implemented; independent validation pending |
| Stop classification | None; worker execution complete, not accepted |
| Central disposition | Accepted after independent validation returned `Accept`; see `ViDAP_P0_EP04_Validation_and_Reconciliation.md`, 2026-09-18. |

---

## 1. Governing Authority Read

The worker read the current explicit user direction and, in the packet's
authority order:

1. `ViDAP_Overview.txt`;
2. `ViDAP_Phased_Plan_Spine.md` version 1.0;
3. `ViDAP_Roadmap.md` version 1.0;
4. `ViDAP_Phase_0_Plan.md` version 1.0;
5. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`;
6. `ViDAP_P0_EP02_Validation_and_Reconciliation.md`;
7. `ViDAP_P0_EP03_Validation_and_Reconciliation.md`; and
8. `ViDAP_P0_EP04.md` version 1.0.

The prerequisite reconciliations are present and state that P0-EP01 through
P0-EP03 are complete. The EP01 Python amendment makes CPython 3.14.x
mandatory for this scaffold unless an explicit exception is approved.

## 2. Baseline and Collision Evidence

Starting branch and commit:

```text
## main...origin/main
7c5dd943bda68018d09c0bcb22f345e785a15a91
```

Sanitized remote:

```text
origin  https://github.com/Sean-V-Dev/ViDAP.git (fetch)
origin  https://github.com/Sean-V-Dev/ViDAP.git (push)
```

Pre-existing worktree changes (not worker changes) were:

```text
M  README.md
M  ViDAP_P0_EP03.md
M  ViDAP_P0_EP03_Implementation_Report.md
M  ViDAP_Phase_0_Plan.md
M  ViDAP_Roadmap.md
?? .editorconfig
?? .gitattributes
?? .gitignore
?? CONTRIBUTING.md
?? LICENSE
?? SECURITY.md
?? ViDAP_P0_EP03_Validation_and_Reconciliation.md
?? ViDAP_P0_EP04.md
?? docs/
```

The accepted EP03 policy baseline is present. No pre-existing Section 7
scaffold artifact, alternate JavaScript/Python lockfile, requirements export,
or source-tree collision was found. The pre-existing changes were preserved.

## 3. Required Runtime Gate Result

Commands executed before any scaffold write:

```text
node --version
npm.cmd --version
uv --version
uv python list --only-installed
```

Observed results:

```text
node: v25.0.0
npm.cmd: 11.6.2
uv: not found / not callable
```

`Get-Command` confirms only the Node 25 installation and its bundled
`npm.cmd`; no `uv` command is available. This fails EP04 Section 5
preconditions 5 and 6. Consequently, the worker could neither prove Node 24
use nor select/provision CPython 3.14 through uv (precondition 7).

Per Sections 5, 11, and 15, the worker stopped rather than installing Node,
installing uv, changing PowerShell policy, using Node 25 as a substitute, or
introducing any alternate package manager. No dependency version was selected
and no primary-source dependency, license, maintenance, or Python 3.14
compatibility evidence was gathered: those steps are downstream of the failed
mandatory runtime gate.

## 4. File Scope and Changes

No Section 7 scaffold artifact was created or modified. No README,
CONTRIBUTING, `.gitattributes`, or `.editorconfig` change was made by this
worker.

The sole worker-created path is this permitted report:

```text
ViDAP_P0_EP04_Implementation_Report.md
```

No manifests, runtime pins, lockfiles, dependencies, environments, build
outputs, temporary clean copies, caches, source files, tests, fixtures, CI
files, or product behavior were created. No remote mutation, staging, commit,
push, reset, clean, or system/runtime mutation occurred.

## 5. Tasks, Locks, and Verification

`setup` and `build` were not created or run. `npm.cmd ci`, uv synchronization,
lock immutability checks, build-output ignore checks, Node-major negative
checks, and clean-temporary-copy verification were not applicable after the
mandatory gate failed. No temporary path was created.

There are no direct dependencies or lockfiles to inventory. This report does
not claim a reproducible scaffold, build, clean-copy result, or acceptance.

## 6. Worker Self-Assessment Against EP04 Acceptance Criteria

This is a worker self-assessment only; it is not validation or Central
acceptance.

| Criteria | Status | Basis |
|---|---|---|
| EP04-AC01 | Partial | Authority, prerequisite presence, repository identity, and pre-existing work recorded; runtime prerequisites fail. |
| EP04-AC02 | Pass | No unauthorized scaffold path was changed; only this authorized report was created. |
| EP04-AC03 to EP04-AC31 | Blocked / not assessed | The mandatory Node 24 and uv prerequisites were unavailable, so scaffold implementation and its required verification could not begin. |

## 7. Findings and Required Return

| ID | Severity | Classification | Finding | Owner / required action |
|---|---|---|---|---|
| EP04-BLOCK-001 | High | Prerequisite | Node `v25.0.0` is installed; Node 24 LTS is not callable. | Provide a callable Node 24 LTS installation without treating Node 25 as supported. |
| EP04-BLOCK-002 | High | Prerequisite | `uv` is absent from the command path. | Provide an approved, callable uv bootstrap; do not ask this packet worker to install it. |

No deviations, compatibility exceptions, dependency substitutions, license
findings, supply-chain findings, or secret exposure occurred.

## 8. Independent-Validation Handoff

The scaffold is **not ready for independent acceptance validation** because
Sections 5 and 15 required the worker to stop before implementation. A later
fresh worker may resume P0-EP04 only after Node 24/npm and uv are callable in
the supported Windows PowerShell path. That worker must re-check all
preconditions, gather then-current primary-source dependency evidence, and
perform the packet's worktree and clean-copy verification. No P0-EP05 work was
started.

## 9. Resume Attempt - 2026-09-18

The user directed the worker to resume after reporting that the Node and uv
problem had been resolved. The worker rechecked the mandatory Section 5 gates
before any scaffold write.

Current repository baseline:

```text
## main...origin/main
0acaf827810b483eed0003d4aef7ecd82dd69d86
```

The worktree was clean before this report update. Node is now compliant:

```text
node: v24.21.0
npm.cmd: 11.19.0
```

However, the resolved `uv` command points to an installed executable but fails
before it can run:

```text
uv --version
Program 'uv.exe' failed to run: Access is denied.
```

The same failure occurs for `uv python list --only-installed`. Command
discovery identifies the executable as a WinGet-installed `uv.exe`; the worker
does not record its local path because evidence must not contain absolute user
paths. This still fails Section 5 precondition 6 and prevents checking
precondition 7. Node 24 resolves EP04-BLOCK-001. The replacement finding is:

| ID | Severity | Classification | Finding | Owner / required action |
|---|---|---|---|---|
| EP04-BLOCK-003 | High | Prerequisite | `uv.exe` is discoverable but not executable: Windows returns `Access is denied`. | Restore an approved callable uv installation or its execution permission; do not bypass the failure with another Python/package tool. |

No scaffold artifacts, dependencies, locks, temporary copies, system changes,
or later-packet work were created during the resume attempt. Independent
validation remains unavailable until uv executes successfully.

## 10. Final Elevated Execution - 2026-09-18

### Elevated prerequisite determination

The current explicit user direction established that the restricted execution
sandbox can deny access to the WinGet-installed `uv.exe` even though the
normal non-Conda Windows PowerShell environment is valid. Per that direction,
the worker re-ran the required uv commands with elevated/unsandboxed execution
before treating the sandbox result as a blocker.

```text
uv --version
uv 0.12.16 (761ff1379 2026-09-17 x86_64-pc-windows-msvc)

uv python list --only-installed
cpython-3.14.7-windows-x86_64-none (Windows system installation)

uv python find 3.14
CPython 3.14.7 selected successfully
```

The elevated `uv --directory python lock --python 3.14.7` command selected
CPython 3.14.7 and resolved the project lock. Therefore the restricted-sandbox
`Access is denied` observation in Section 9 is superseded as an EP04 blocker;
it is not evidence of a prerequisite failure in the supported environment.
No uv was reinstalled or substituted.

### Starting state and output collision review

At the beginning of this resumed execution, the repository was on `main` at
`0acaf827810b483eed0003d4aef7ecd82dd69d86`, tracking `origin/main`. The
sanitized remote was `origin https://github.com/Sean-V-Dev/ViDAP.git` for both
fetch and push. The only
pre-existing worktree change was this report, containing the historical blocked
attempt evidence above. No manifest, lockfile, runtime declaration, source
tree, test tree, or generated scaffold output existed. That pre-existing report
content is retained as historical evidence; this section records the final
resumed execution.

### Authorized paths created or modified

Created:

- `.nvmrc`
- `package.json`
- `package-lock.json`
- `scripts/verify-node-version.mjs`
- `apps/web/index.html`
- `apps/web/vite.config.ts`
- `apps/web/tsconfig.json`
- `apps/web/src/main.tsx`
- `python/.python-version`
- `python/pyproject.toml`
- `python/uv.lock`
- the four authorized empty `python/src/vidap_*/__init__.py` markers

Modified:

- `README.md`
- `CONTRIBUTING.md`
- `.gitattributes`
- `.editorconfig`
- this implementation report

The final Git comparison names only those authorized paths. `node_modules/`,
`python/.venv/`, and `apps/web/dist/` remain ignored and untracked.
The final branch and commit remain `main` and
`0acaf827810b483eed0003d4aef7ecd82dd69d86`; nothing is staged, committed,
or pushed.

### Runtime declarations and direct dependency evidence

The exact runtime pins are `.nvmrc` `24.21.0` and
`python/.python-version` `3.14.7`. `package.json` limits Node to `>=24 <25`;
`python/pyproject.toml` limits Python to `>=3.14,<3.15`.

Node's official release index identified `v24.21.0` (Krypton LTS, released
2026-09-07) with bundled npm `11.19.0`. The worker used Node `v24.21.0` and
npm `11.19.0` for lock generation, `npm.cmd run setup`, and
`npm.cmd run build`. The local verification script inspects Node's actual major
version and exits nonzero unless it is 24; source inspection confirms the
rejecting branch reports the actual version and Windows-friendly remediation.

Python's official 3.14.7 release page and uv's Python support policy were
retrieved on 2026-09-18. uv documents Tier 1 support for CPython 3.14 and
Windows discovery/selection. The exact elevated lock/sync commands selected
CPython 3.14.7 and created the project environment successfully.

| Package | Exact version | Role before P0-EP05 | Primary source retrieved 2026-09-18 | License evidence | Compatibility/maintenance basis |
|---|---:|---|---|---|---|
| `react` | 19.3.0 | Empty root runtime | npm registry metadata; `react/react` | MIT | Current registry release; pairs with React DOM 19.3.0 |
| `react-dom` | 19.3.0 | React DOM root mount | npm registry metadata; `react/react` | MIT | Current registry release; peer requires React 19.3.0 |
| `@xyflow/react` | 12.11.6 | Accepted future graph-editor foundation, unused by the empty entry | npm registry metadata; `xyflow/xyflow` | MIT | Current maintained React Flow package; peers accept React 19 |
| `vite` | 8.3.0 | Web production build | npm registry metadata; `vitejs/vite` | MIT | Current registry release; declares Node `^20.19.0 || >=22.12.0`, satisfied by Node 24 |
| `typescript` | 7.0.2 | TypeScript source/configuration | npm registry metadata; `microsoft/TypeScript` | Apache-2.0 | Current registry release; Node >=16.20.0, satisfied by Node 24 |
| `@vitejs/plugin-react` | 6.1.1 | Minimal Vite React integration | npm registry metadata; `vitejs/vite-plugin-react` | MIT | Current registry release; peer requires Vite 8 |
| `@types/react` | 19.3.0 | React TypeScript declarations | npm registry metadata; `DefinitelyTyped/DefinitelyTyped` | MIT | Current registry release; matches React 19.3.0 |
| `@types/react-dom` | 19.3.0 | React DOM TypeScript declarations | npm registry metadata; `DefinitelyTyped/DefinitelyTyped` | MIT | Current registry release; peer requires `@types/react` 19.3.0 |
| `fastapi` | 0.141.1 | Accepted future local-host foundation, not started | `https://pypi.org/pypi/fastapi/json` | MIT (`license_expression`) | PyPI metadata declares Python >=3.10, OS-independent, and Python 3.14 classifier; locked/synced on Windows CPython 3.14.7 |
| `uvicorn` | 0.53.0 | Accepted future ASGI host foundation, not started | `https://pypi.org/pypi/uvicorn/json` | BSD-3-Clause (`license_expression`) | PyPI metadata declares Python >=3.10, OS-independent, and Python 3.14 classifier; locked/synced on Windows CPython 3.14.7 |

The npm metadata was read directly through the official npm registry at
execution time. FastAPI and Uvicorn metadata was read directly from PyPI at
execution time. All direct licenses are permitted under accepted D0.6 policy.
Current registry/PyPI releases and successful lock resolution provide the
maintenance basis for this bounded foundation; P0-EP06 remains responsible for
full direct/transitive inventory, license, and advisory review.

Primary-source links used for the runtime/dependency evidence:

- `https://nodejs.org/dist/index.json`
- `https://www.python.org/downloads/release/python-3147/`
- `https://docs.astral.sh/uv/reference/policies/python/`
- `https://registry.npmjs.org/react/19.3.0`
- `https://registry.npmjs.org/react-dom/19.3.0`
- `https://registry.npmjs.org/@xyflow%2freact/12.11.6`
- `https://registry.npmjs.org/vite/8.3.0`
- `https://registry.npmjs.org/typescript/7.0.2`
- `https://registry.npmjs.org/@vitejs%2fplugin-react/6.1.1`
- `https://registry.npmjs.org/@types%2freact/19.3.0`
- `https://registry.npmjs.org/@types%2freact-dom/19.3.0`
- `https://pypi.org/pypi/fastapi/json`
- `https://pypi.org/pypi/uvicorn/json`

### Lock authority and tasks

The root `package.json` and `package-lock.json` are the sole JavaScript
manifest/lock pair. `python/pyproject.toml` and `python/uv.lock` are the sole
Python project/lock pair. No workspace, alternate package manager, alternate
lock, requirements export, or global task package was created. The Python
project is package-disabled so its ownership markers do not establish a
premature distribution contract.

| Public task | Actual behavior |
|---|---|
| `npm.cmd run setup` | Verifies Node 24, executes `npm.cmd ci`, then executes `uv --directory python sync --locked`. It does not repair a runtime or write a lock. |
| `npm.cmd run build` | Verifies Node 24, then runs the local Vite build for `apps/web/` into ignored `apps/web/dist/`. It does not start a server or invoke Python. |

`preinstall` is the permitted internal Node-major enforcement hook. No `dev`,
`launch`, quality, test, audit, CI, dependency-control, or process-smoke task
exists.

### Ownership/source and policy result

The web source mounts `null` into the empty root. It contains no visible shell,
React Flow rendering, controls, workflow behavior, data, model, or API logic.
The four Python ownership-marker files are empty and contain no host, route,
startup, persistence, workflow, experiment, export, or ML behavior. FastAPI
and Uvicorn are only locked dependencies; no Python process was started.

README and CONTRIBUTING now state the Windows-only prerequisites and the
authoritative `npm.cmd run setup` / `npm.cmd run build` commands, explain lock
authority and ignored output, and explicitly defer a shell, `dev`/`launch`,
workflow/API/data/model behavior, tests, CI, and cross-platform support.
`.gitattributes` and `.editorconfig` add only LF/indentation treatment for
TOML and lock text; the accepted EP03 policies are otherwise unchanged.

### Reproducibility evidence

In the current worktree, the following completed successfully with Node 24,
npm 11.19.0, uv 0.12.16, and CPython 3.14.7:

```text
npm.cmd run setup
npm.cmd run build
```

`npm.cmd ci` added 44 locked JavaScript packages. `uv --directory python sync
--locked` resolved the 14-package locked Python graph and installed the 13
non-project packages. Routine setup and build left both lock hashes unchanged.
`git check-ignore -v` confirmed the Node dependencies, Python environment, and
web output are ignored.

A worker-created fresh temporary copy outside the repository and OneDrive
contained only the intended scaffold/policy files, no `.git`, report,
dependencies, environment, build output, or pre-existing npm/uv cache. It ran
the same two documented commands with fresh temporary npm and uv cache
directories. Setup and build succeeded, both locks remained unchanged, and the
copy produced its own `node_modules`, `python/.venv`, and web build output.
The exact worker-created temporary directory was removed after success. An
earlier temporary-copy command was rejected before directory creation because
Windows PowerShell does not support the attempted `New-Item -LiteralPath`
parameter; its guarded cleanup confirmed no temporary path remained. The
subsequent successful run is the clean-copy evidence.

### Worker self-assessment against EP04 acceptance criteria

This is worker evidence only, not independent validation, acceptance, or
Central reconciliation.

| Criterion | Worker self-assessment |
|---|---|
| EP04-AC01 | Pass — authority, prerequisites, current baseline, and pre-existing report change recorded. |
| EP04-AC02 | Pass — final changed/created path list is limited to Section 7. |
| EP04-AC03 | Pass — Node 24.21.0 pin, engine, enforcement, and observed use recorded. |
| EP04-AC04 | Pass — CPython 3.14.7 pin/constraint and uv selection recorded. |
| EP04-AC05 | Pass — elevated Python 3.14 lock/sync succeeds; no fallback occurred. |
| EP04-AC06 | Pass — one root npm manifest and lock. |
| EP04-AC07 | Pass — one uv project manifest and lock. |
| EP04-AC08 | Pass — no alternate resolver/package-manager state committed. |
| EP04-AC09 | Pass — accepted JavaScript foundation only, with current evidence. |
| EP04-AC10 | Pass — FastAPI/Uvicorn foundation only, with current evidence. |
| EP04-AC11 | Pass — exact direct package evidence recorded above. |
| EP04-AC12 | Pass — accepted web/Python ownership areas exist without semantics. |
| EP04-AC13 | Pass — empty web build plumbing only. |
| EP04-AC14 | Pass — empty Python markers only. |
| EP04-AC15 | Pass — Windows `npm.cmd run` setup/build use locked local tools. |
| EP04-AC16 | Pass — deferred task names are absent and documented. |
| EP04-AC17 | Pass — current-worktree locked setup succeeded without lock change. |
| EP04-AC18 | Pass — build succeeded into ignored output without service/Python invocation. |
| EP04-AC19 | Pass — fresh temporary-copy setup/build succeeded with fresh caches. |
| EP04-AC20 | Pass — generated state is ignored and temporary copy was cleaned. |
| EP04-AC21 | Pass — README/CONTRIBUTING match the bounded scaffold. |
| EP04-AC22 | Pass — EP03 policy baseline retained; only TOML/lock alignment added. |
| EP04-AC23 | Pass — no policy/system runtime/global package/remote/staging/commit/push mutation. |
| EP04-AC24 | Pass — no test, quality, CI, fixture, audit, browser, release, or bot configuration. |
| EP04-AC25 | Pass — no workflow schema, API, startup, persistence, dataset, model, or product behavior. |
| EP04-AC26 | Pass — `git diff --check` succeeded and text-policy coverage is present. |
| EP04-AC27 | Pass — this report is sanitized, reproducible, and distinguishes prior evidence. |
| EP04-AC28 | Pass — no unresolved critical/high compatibility, license, supply-chain, or safety finding observed. |
| EP04-AC29 | Pending — requires the fresh independent validator. |
| EP04-AC30 | Pending — requires an independent `Accept` verdict. |
| EP04-AC31 | Pending — requires Central acceptance. |

### Findings, deviations, and handoff

No unresolved compatibility failure, dependency change, license exception,
scope deviation, sensitive content, remote mutation, runtime/system mutation
outside uv project-environment provisioning, staging, commit, push,
unrelated-file modification, P0-EP05 work, or product behavior occurred.

The scaffold is ready for independent validation under packet Section 16. The
validator must independently re-read the governing inputs, inspect all
authorized artifacts and this report, re-check the direct-package evidence and
elevated uv behavior, reproduce the locked current/clean-copy setup and build,
and return exactly `Accept`, `Revise`, or `Blocked`. The validator must not
accept for Central or begin P0-EP05.
