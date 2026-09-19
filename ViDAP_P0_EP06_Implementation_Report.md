# ViDAP P0-EP06 Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P0_EP06.md` — CI, Dependency, and License Controls |
| Packet version | 0.4 |
| Worker role | Bounded scaffold worker |
| Execution date | 2026-09-19 |
| Approval | Fresh explicit user direction after the amended packet, both license reviews, and accepted records `0003` and `0004` were rechecked |
| Hosted workflow evidence | **Pending user-authorized run**; this worker did not dispatch or mutate remote state |
| Remedial result | The seven literal Record `0004` scanner keys now pass; changed, generic, unknown, and unlisted claims remain fail-closed |

## 1. Authority, baseline, and bounded scope

The worker read the complete Section 3 governing chain, including the product overview, spine, roadmap, Phase 0 plan, EP02 decision/reconciliation, EP03–EP05 reconciliations, accepted records `0001`, `0003`, and `0004`, the EP06 v0.4 packet, `ViDAP_P0_EP06_License_Graph_Review.md`, and `ViDAP_P0_EP06_Generic_License_Review.md`. Records `0003` and `0004` are Central-owned accepted policy decisions; the reviews provide the evidence they govern.

Baseline was `main` at `befb3dd7b67401ca931aee29f23b97b69ea93685` with a configured sanitized GitHub `origin`. Existing Phase 0 planning, scaffold, and quality-harness changes predated this worker and were preserved. No files were staged, committed, pushed, dispatched, or changed remotely.

The earlier EP06 scaffold changed the broader original Section 7 set. This v0.4 remedial execution changed only the five approved existing paths: `scripts/dependency-controls.ps1`, `docs/dependency-controls.md`, `README.md`, `CONTRIBUTING.md`, and this report. It did not alter manifests, either lock, workflow, Dependabot, decision records, fixtures, product behavior, API, process, shell, P0-EP07, or later-phase work.

## 2. Direct controls and action provenance

| Item | Locked selection | Evidence and role |
|---|---|---|
| Node license inventory | `license-checker-rseidelsohn@5.0.1` | BSD-3-Clause; npm primary metadata retrieved 2026-09-18; supports Node `>=24` and npm `>=11`. |
| Python license inventory | `pip-licenses==5.5.5` | MIT; PyPI primary metadata retrieved 2026-09-18; JSON output and Python 3.14 support. |
| Python advisory scanner | `pip-audit==2.10.1` | Apache-2.0; PyPI primary metadata retrieved 2026-09-18; Python `>=3.10` and Python 3.14 support. |
| Checkout | `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` | Official `v7.0.1` full commit; nearby workflow comment. |
| Node setup | `actions/setup-node@820762786026740c76f36085b0efc47a31fe5020` | Official `v7.0.0` full commit; nearby workflow comment. |
| uv setup | `astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9` | Official `v9.0.0` full commit; nearby workflow comment. |
| Cache | `actions/cache@a7833574556fa59680c1b7cb190c1735db73ebf0` | Official `v5.0.0` full commit; nearby workflow comment. |
| Audit artifact | `actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | Official `v7.0.1` full commit; nearby workflow comment. |

The normal Windows uv path was rechecked before network-backed work: uv `0.12.16` with CPython `3.14.7` resolved the locked graph without a certificate-trust warning. No TLS bypass or persistent environment workaround was introduced.

## 3. Implemented controls

- Added exact root tasks `deps:inventory`, `license:check`, and `deps:audit`. They call only the local no-profile PowerShell control script.
- Added the named direct tools through the authoritative npm and uv locks; no peer override, global tool, alternate package manager, hand-edited lock, or automatic fix was used.
- The audit flow uses `npm audit --json` and the required locked uv export with `--all-extras --all-groups --no-emit-project`, followed by `pip-audit --require-hashes --disable-pip --strict`. It neither resolves nor fixes dependencies.
- The license classifier applies D0.6 and only the literal record-`0003` and record-`0004` catalogs. Base allows are exact SPDX strings only; generic aliases, full-text claims, prefixes, and fallback-to-later Python fields do not authorize a package. It has no ranges, prefixes, wildcards, name normalization, inferred roles, or runtime license-text parsing. It emits the record ID, restricted role, and re-review trigger for each catalog match.
- The audit temporary root must itself be an existing non-reparse directory outside the checkout and OneDrive before a bounded child can be created or cleaned.
- Added Windows CI parity, a weekly clean-cache path, bounded cache/artifact handling, and weekly npm/GitHub-Actions-only Dependabot configuration.
- After GitHub rejected the initial workflow before runner allocation, moved the two `runner.temp` cache variables from job-level `env` to their individual cache/setup steps. The cache directories, keys, actions, and all artifact/cleanup boundaries are unchanged.
- Updated public contributor guidance for the controls, literal exception boundary, no-auto-fix/no-SBOM posture, triage, updates, and `SECURITY.md`.

## 4. Locks and command evidence

| Point | `package-lock.json` SHA-256 | `python/uv.lock` SHA-256 | Result |
|---|---|---|---|
| Pre-control baseline | `6ECCE2541E202A17A55A072B9EC4C6689F86D9293114B856A90882F9C98EFA3C` | `449A4027D168A3823585D8D6A96B0AF2A1B68AAF0EB2B616A8976E1D7E19C293` | Pre-existing accepted EP05 graph. |
| Intentional direct-tool update | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` | Only the permitted direct control tools were added. |
| After setup, quality, coverage, build, inventory, license, and audit | Same | Same | Routine commands did not rewrite either authority. |

After the v0.4 amendment, `npm.cmd run setup`, `check`, `coverage`, `build`, `deps:inventory`, `license:check`, and `deps:audit` completed successfully from the locked environment. The same complete set succeeded in a fresh system-temporary clean copy with separate npm and uv caches. Inventory prints actual direct/transitive npm and installed Python facts without writing a second authority. npm audit reported zero vulnerabilities; pip-audit reported no known vulnerabilities. Those results are scanner evidence, not a safety guarantee or exploitability conclusion.

## 5. Exact record-0003 license evidence

The pre-correction installed graph passed for 431 packages. The following are the complete literal catalog matches; each entry records the limited current use and its re-review trigger.

| Exact match(es) | Restricted role | Re-review trigger |
|---|---|---|
| `@csstools/color-helpers@6.1.1`, `MIT-0` | Test-only DOM/CSS-color emulation support. | Before distributing package/data, or any version, license, or role change. |
| `@csstools/css-syntax-patches-for-csstree@1.1.14`, `MIT-0` | Test-only DOM CSS-parser compatibility data. | Before distributing package/data, or any version, license, or role change. |
| `lightningcss@1.33.0`, `MPL-2.0`; `lightningcss-win32-x64-msvc@1.33.0`, `MPL-2.0` | Unchanged Vite build-only CSS-processing capability; current scaffold has no CSS processing or output. | Before CSS processing, desktop/installer delivery, packaged node modules, or distribution containing code/native binary. |
| `chownr@3.0.0`; `common-ancestor-path@2.0.0`; `glob@13.0.6`; `isexe@4.0.0`; `lru-cache@11.5.2`; `minimatch@10.2.6`; `minipass@7.1.3`; `minipass-flush@1.0.7`; `path-scurry@2.0.2`; `tar@7.5.22`; `yallist@5.0.0` — all `BlueOak-1.0.0` | Current development, test, quality, or local dependency-control tooling only. | Before code distribution; Central must record license-text/link treatment. |
| `caniuse-lite@1.0.30001810`, `CC-BY-4.0` | Development-only browser-compatibility data. | Before distributing the data. |
| `spdx-exceptions@2.5.0`, `CC-BY-3.0` | Local dependency-control tooling. | Before distributing the data; Central must review attribution treatment. |
| `spdx-ranges@2.1.1`, `(MIT AND CC-BY-3.0)` | Local dependency-control tooling. | Before distributing data/code; retain both license components. |
| `certifi@2026.7.22`, `MPL-2.0` | Development/integration HTTP-advisory CA bundle only; not imported/output by the application. | If a Python environment, runtime, or certificate bundle is distributed. |
| `colorama@0.4.6`, `BSD License` | Development/test quality tooling; record `0003` verifies the locked artifact as BSD-3-Clause. | Before distribution, or any version, license, or role change. |
| `packaging@26.3`, `Apache-2.0 OR BSD-2-Clause` | Development/test quality tooling; record `0003` verifies both permitted branches. | Before distribution, or any version, license, or role change. |
| `pathspec@1.1.1`, `Mozilla Public License 2.0 (MPL 2.0)` | Development-only mypy path-pattern support. | Before distribution, or any version, license, or role change. |

This worker created no license exception or legal conclusion. Record `0003` already existed as the accepted Central decision; any changed, unknown, unlisted, ambiguous, or otherwise unapproved finding remains fail-closed. Required notices and distribution obligations remain future Central review work.

### Record-0004 remedial license evidence

The post-validation correction remains fail-closed: only exact SPDX base
strings or an exact record-`0003`/`0004` key may pass. Record `0004` supplies
the following seven literal package/version/gate-value dispositions. The
scanner names are deliberately literal: `pip_api`, `pip_audit`, and `tomli_w`
are neither hyphenated nor normalized.

| Exact match | Restricted role | Re-review trigger |
|---|---|---|
| `defusedxml@0.7.1`, `PSFL` | Transitive defensive XML handling in pip-audit CycloneDX support. | Any version, gate value, role, modification, vendoring, or distribution change; retain the license text/notices. |
| `markdown-it-py@4.2.0`, `MIT License` | Transitive markdown renderer supporting pip-audit output. | Any version, gate value, role, modification, vendoring, or distribution change; retain license/copyright. |
| `mdurl@0.1.2`, `MIT License` | Transitive URL parsing supporting markdown-it-py. | Any version, gate value, role, modification, vendoring, or distribution change; retain license/copyright. |
| `pip_api@0.0.35`, reviewed full Apache 2.0 metadata value (SHA-256 `DCB058E1702F3BB0DC7C1E0C7DF595E5C04AD727187FFA8FF0A39E4C5A0519FE`) | Transitive pip-environment access within pip-audit. | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and applicable NOTICE. |
| `pip_audit@2.10.1`, `Apache Software License` | Direct development-only dependency audit in CI. | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and applicable NOTICE. |
| `sortedcontainers@2.4.0`, `Apache 2.0` | Transitive sorted-collection support in pip-audit. | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and applicable NOTICE. |
| `tomli_w@1.2.0`, `MIT License` | Transitive TOML-writing support in pip-audit. | Any version, gate value, role, modification, vendoring, or distribution change; retain license/copyright. |

The full `pip_api` value is stored as the reviewed literal gate value and is
compared as a value; the worker added no parser or normalization path. Live
`license:check` passed with all seven record-`0004` matches. In the isolated
copy, changing `markdown-it-py` to `4.2.1`, changing an unlisted npm `MIT`
claim to `MIT License`, and changing it to `UNLICENSED` each produced a
nonzero fail-closed result. Thus the seven decisions do not authorize changed,
generic, unknown, or unlisted claims.

## 6. Safety, temporary paths, negative controls, and clean copy

Local audit output is created only as a new randomly named child of the resolved system temporary directory. A local override must be a new exact `vidap-pip-audit-<32 lowercase hex>` child; CI ignores that override and uses a fixed `RUNNER_TEMP` child. Creation and cleanup verify parent containment, exact child name, directory type, and no reparse point. CI uploads only the bounded Python advisory JSON (when present) for 14 days, then performs its own bounded cleanup.

- An unsafe local audit override was rejected before creation or cleanup.
- A process-level temporary-root override pointing into the checkout/OneDrive
  was rejected before audit creation or cleanup; a normal system-temporary
  audit still completed and removed its bounded child.
- In a new isolated system-temporary clean copy with separate npm/uv caches, setup, quality, inventory, license, and audit controls reproduced successfully.
- In that copy only, changed `markdown-it-py@4.2.1`, an unlisted `MIT License` claim, and `UNLICENSED` each caused the license task to fail closed with a nonzero exit.
- The clean copy and separate caches were reparse-checked and removed. No temporary evidence was written to tracked paths or left as repository residue.

## 7. Static CI, Dependabot, documentation, and scope evidence

Static worker inspection found a two-job `windows-latest` workflow with the approved PR/main/manual/weekly triggers, top-level `contents: read`, no secrets/write/deployment/container/reusable path, and PR-only cancellation. The original hosted parse failure was corrected by moving `runner.temp` references out of job-level `env`; those references now occur only in cache/setup or artifact steps after runner allocation. Every action is full-SHA pinned with an adjacent release comment. Only npm download and uv package caches are keyed by OS, architecture, Node/uv versions, and all three authority files; the scheduled run bypasses restore. The artifact is restricted to the temporary Python advisory JSON, uses `always()` with `if-no-files-found: ignore`, and has 14-day retention plus bounded cleanup.

Dependabot has exactly weekly npm and GitHub Actions entries, each limited to two open pull requests and patch/minor development grouping within its ecosystem. It has no UV entry, auto-merge, bypass, or cross-ecosystem group.

`git diff --check` passed. The v0.4 scope comparison found only its five authorized worker paths; the amended packet, generic-license review, and record `0004` were pre-existing Central inputs and were untouched. The repository also has 93 pre-existing tracked `node-compile-cache/` files. That generated state is outside the five-path authority and remains a Central/repository-maintainer remediation item, not a worker change. No additional generated build, coverage, environment, cache, audit, or temporary-copy residue was created.

## 8. Worker self-assessment — not independent validation

| Criteria | Worker evidence status |
|---|---|
| AC01–AC04 | Implemented and evidenced: authority/baseline/scope recorded; direct-tool provenance and lock invariance recorded. |
| AC05–AC14 | Implemented and locally exercised: unchanged root tasks, distinct locked controls, installed-graph inventory, exact record-`0003` and `0004` catalogs, and fail-closed audit/license/temporary/certificate safeguards. **AC08 passes only for the exact reviewed keys and fails closed otherwise.** |
| AC15–AC21 | Implemented with worker static evidence: approved Windows workflow, pins, caches, concurrency, artifact boundary, Dependabot, and documentation. |
| AC22–AC25 | Setup, quality, coverage, build, inventory, license, and audit pass; safe negative controls and clean copy pass. **AC25 remains blocked for Central/repository maintainer by the 93 pre-existing tracked `node-compile-cache/` files, which v0.4 does not authorize this worker to remove.** |
| AC26–AC32 | Implemented/evidenced within scope: no substitute authority/global tool/TLS bypass/later work/remote mutation; whitespace and scope checks pass; scanner limitations are stated. The record-`0004` disposition resolves the prior local license-policy block; cache-state acceptance remains outside worker authority. |
| AC33 | **Pending independent validator.** |
| AC34–AC35 | **Pending user-owned green hosted Windows v0.4 run and independent verdict.** The earlier supplied hosted run parsed and created jobs but its license job was red before record `0004`; it is not v0.4 pass evidence. |
| AC36 | **Central-owned and pending.** |

## 9. Independent-validation handoff

An independent validator must inspect every governing input and Section 7 artifact; verify every literal record-`0003` and record-`0004` match, including the full reviewed `pip_api` gate value and literal underscore scanner names; reproduce safe local controls after certificate-trust verification; and inspect lock hashes, cleanup guards, action provenance, workflow/Dependabot constraints, scope, and the absence of later work. The validator must not edit files, dispatch CI, alter remote state, accept for Central, or begin P0-EP07.

The independent handoff must retain two separate blockers: Central/repository-maintainer disposition of the 93 pre-existing tracked `node-compile-cache/` files, and user-owned green hosted Windows v0.4 evidence. Until the latter is supplied, the validator must return `Blocked` for AC34/AC35 while preserving separate local/static findings.
