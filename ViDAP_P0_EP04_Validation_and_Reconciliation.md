# ViDAP P0-EP04 Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | P0-EP04 - Reproducible Project Scaffold |
| Status | Accepted by Central |
| Reconciliation date | 2026-09-18 |
| Implementation report | `ViDAP_P0_EP04_Implementation_Report.md` |
| Governing packet | `ViDAP_P0_EP04.md` version 1.0 |
| Independent verdict | `Accept`, returned in chat on 2026-09-18 |
| Authority | Explicit user direction and Central reconciliation under Spine Section 1 |

---

## 1. Purpose

This record preserves the independent validator's final `Accept` verdict, dispositions its informational environment note, and records Central's acceptance of the P0-EP04 reproducible scaffold.

The validator returned its structured report in chat, as permitted by P0-EP04 Section 16. This file is Central's durable preservation of that result rather than a validator-authored report.

This reconciliation accepts only the locked project scaffold. It does not authorize P0-EP05 execution, quality/test configuration, CI, fixtures, process startup, APIs, workflow semantics, data/ML functionality, or product behavior.

---

## 2. Independent Validation Result

The independent validator returned `Accept` and concluded that:

- EP04-AC01 through EP04-AC30 pass; EP04-AC31 required only Central acceptance;
- exactly the 20 paths authorized by packet Section 7 were changed or created;
- Node 24.21.0 and CPython 3.14.7 are correctly pinned and constrained, with Node-major enforcement before installation;
- `package-lock.json` and `python/uv.lock` are the sole lock authorities and remained hash-identical across repeated setup/build runs;
- the documented Windows `npm.cmd run setup` and `npm.cmd run build` commands passed both in the worktree and in a fresh temporary copy outside the repository and OneDrive, using fresh npm and uv caches;
- generated dependencies, the Python environment, and web build output remained ignored, and the temporary verification copy/caches were removed;
- the web entry mounts `null`, the Python ownership markers are empty, and no workflow, API, service startup, persistence, UI shell, or later-packet behavior exists;
- the direct dependency evidence is current and license-compatible for the accepted foundation, while the exact lock contents and implementation report remain the authoritative package evidence;
- the reproduced dependency counts agree with worker evidence: 44 npm packages and 14 Python packages resolved;
- `git diff --check`, text/attribute policy checks, and scoped sensitive-content checks passed; and
- no open `Revise` or `Blocked` finding remains.

The validator did not modify files, accept the scaffold for Central, or begin P0-EP05.

---

## 3. Informational Finding Disposition

### I-EP04-001 - Closed as an execution-environment note

The restricted validation sandbox denies direct execution of the WinGet-installed `uv.exe`. The normal elevated Windows execution path successfully ran uv 0.12.16, selected CPython 3.14.7, and completed both worktree and clean-copy reproductions.

This is not a project scaffold, runtime-selection, dependency, lockfile, or user-machine prerequisite defect. It requires no scaffold correction and does not authorize a second Python/package tool. Future bounded workers that need uv must use the normal/elevated Windows execution path when the restricted sandbox produces this specific access-denied result, then record the distinction in their evidence.

---

## 4. Accepted Scaffold Baseline

Central accepts the following EP04 baseline:

| Area | Accepted role |
|---|---|
| `.nvmrc`, `package.json`, `package-lock.json`, and `scripts/verify-node-version.mjs` | Node 24-pinned root npm authority, lock discipline, and preinstall major-version enforcement |
| `apps/web/` build files | Empty TypeScript/React build plumbing only; no visible application shell or semantic behavior |
| `python/.python-version`, `python/pyproject.toml`, and `python/uv.lock` | CPython 3.14-pinned uv project authority and lock discipline |
| `python/src/vidap_*` markers | Reserved workflow, execution, experiment/state, and export ownership without implementations or contracts |
| `README.md` and `CONTRIBUTING.md` | Accurate Windows setup/build instructions and remaining Phase 0 deferrals |
| `.gitattributes` and `.editorconfig` | Aligned TOML/lock text conventions without weakening repository policy |
| `ViDAP_P0_EP04_Implementation_Report.md` | Bounded implementation evidence and validation handoff |

The authoritative root commands are `npm.cmd run setup` and `npm.cmd run build`. They establish only locked setup and an ignored empty web build; they do not constitute `dev`, `launch`, quality, test, CI, API, or product commands.

---

## 5. Acceptance Decision

Central accepts the P0-EP04 reproducible scaffold as independently validated. EP04-AC31 is satisfied, and P0-EP04 is `Complete`.

P0-EP05 may now be drafted as a separate bounded packet for the quality and test harness. This acceptance does not create or approve that packet and does not authorize its execution, CI, fixture creation, process startup, or product implementation.

---

## 6. Validation Sources Preserved from the Returned Report

- [Node.js release index](https://nodejs.org/dist/index.json)
- [uv Python support policy](https://docs.astral.sh/uv/reference/policies/python/)
- [FastAPI 0.141.1 package metadata](https://pypi.org/pypi/fastapi/0.141.1/json)
- [Uvicorn 0.53.0 package metadata](https://pypi.org/pypi/uvicorn/0.53.0/json)

These links preserve the sources cited by the independent validator. The validator's `Accept` result, not this Central record, supplies the independent-validation conclusion.
