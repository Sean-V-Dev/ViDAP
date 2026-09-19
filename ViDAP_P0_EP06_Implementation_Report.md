# ViDAP P0-EP06 Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P0_EP06.md` — CI, Dependency, and License Controls |
| Packet version | 0.2 |
| Worker role | Bounded scaffold worker |
| Execution date | 2026-09-18 |
| Approval | Fresh user direction to proceed after the packet, graph review, and accepted record `0003` were rechecked |
| Hosted workflow evidence | **Pending user-authorized run**; this worker did not dispatch or mutate remote state |
| Post-validation correction | 2026-09-18: tightened after independent validator P1 findings; current live license result is intentionally fail-closed pending Central disposition |

## 1. Authority, baseline, and bounded scope

The worker read the complete Section 3 governing chain, including the product overview, spine, roadmap, Phase 0 plan, EP02 decision/reconciliation, EP03–EP05 reconciliations, accepted records `0001` and `0003`, the EP06 v0.2 packet, and `ViDAP_P0_EP06_License_Graph_Review.md`. The latter two artifacts were added to the packet after the earlier v0.1 fail-closed stop; record `0003` is the Central-owned, accepted policy amendment applied here.

Baseline was `main` at `befb3dd7b67401ca931aee29f23b97b69ea93685` with a configured sanitized GitHub `origin`. Existing Phase 0 planning, scaffold, and quality-harness changes predated this worker and were preserved. No files were staged, committed, pushed, dispatched, or changed remotely.

Worker changes are limited to packet Section 7: `.github/workflows/ci.yml`, `.github/dependabot.yml`, `package.json`, `package-lock.json`, `python/pyproject.toml`, `python/uv.lock`, `scripts/dependency-controls.ps1`, `docs/dependency-controls.md`, `README.md`, `CONTRIBUTING.md`, and this report. No fixture, product behavior, API, process, shell, P0-EP07, or later-phase work was added.

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
- The license classifier applies D0.6 and only the literal record-`0003` catalog. Base allows are exact SPDX strings only; generic aliases, full-text claims, prefixes, and fallback-to-later Python fields do not authorize a package. It has no ranges, prefixes, wildcards, or inferred roles. It emits the record ID, restricted role, and re-review trigger for each catalog match.
- The audit temporary root must itself be an existing non-reparse directory outside the checkout and OneDrive before a bounded child can be created or cleaned.
- Added Windows CI parity, a weekly clean-cache path, bounded cache/artifact handling, and weekly npm/GitHub-Actions-only Dependabot configuration.
- Updated public contributor guidance for the controls, literal exception boundary, no-auto-fix/no-SBOM posture, triage, updates, and `SECURITY.md`.

## 4. Locks and command evidence

| Point | `package-lock.json` SHA-256 | `python/uv.lock` SHA-256 | Result |
|---|---|---|---|
| Pre-control baseline | `6ECCE2541E202A17A55A072B9EC4C6689F86D9293114B856A90882F9C98EFA3C` | `449A4027D168A3823585D8D6A96B0AF2A1B68AAF0EB2B616A8976E1D7E19C293` | Pre-existing accepted EP05 graph. |
| Intentional direct-tool update | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` | Only the permitted direct control tools were added. |
| After setup, quality, coverage, build, inventory, license, and audit | Same | Same | Routine commands did not rewrite either authority. |

Before the post-validation correction, `npm.cmd run setup`, `check`, `coverage`, `build`, `deps:inventory`, `license:check`, and `deps:audit` completed successfully from the locked environment. The hardened `deps:audit` remains successful, while the hardened `license:check` now intentionally fails as described below. Inventory prints actual direct/transitive npm and installed Python facts without writing a second authority. npm audit reported zero vulnerabilities; pip-audit reported no known vulnerabilities. Those results are scanner evidence, not a safety guarantee or exploitability conclusion.

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

### Post-validation fail-closed result

The validator correctly identified that generic labels and prefix matching were
too permissive. The corrected policy now accepts only exact SPDX base strings
or literal record-`0003` entries and selects Python declaration fields in a
fixed priority order without seeking a later allowed alternative. The current
locked graph consequently has these unapproved metadata-only claims:

- `defusedxml@0.7.1` — `PSFL`;
- `markdown-it-py@4.2.0`, `mdurl@0.1.2`, and `tomli_w@1.2.0` — `MIT License`;
- `pip_api@0.0.35` — embedded Apache 2.0 full text;
- `pip_audit@2.10.1` — `Apache Software License`; and
- `sortedcontainers@2.4.0` — `Apache 2.0`.

`license:check` exits nonzero for these entries. They are not silently
normalized because record `0003` does not authorize them. Central must either
record an exact disposition or choose another approved approach before the
license task can pass.

## 6. Safety, temporary paths, negative controls, and clean copy

Local audit output is created only as a new randomly named child of the resolved system temporary directory. A local override must be a new exact `vidap-pip-audit-<32 lowercase hex>` child; CI ignores that override and uses a fixed `RUNNER_TEMP` child. Creation and cleanup verify parent containment, exact child name, directory type, and no reparse point. CI uploads only the bounded Python advisory JSON (when present) for 14 days, then performs its own bounded cleanup.

- An unsafe local audit override was rejected before creation or cleanup.
- A process-level temporary-root override pointing into the checkout/OneDrive
  was rejected before audit creation or cleanup; a normal system-temporary
  audit still completed and removed its bounded child.
- In a new isolated system-temporary clean copy with separate npm/uv caches, setup, quality, inventory, license, and audit controls reproduced successfully.
- In that copy only, changing `caniuse-lite` metadata to `UNLICENSED` caused the license task to fail closed with a nonzero exit.
- In that copy only, a temporary mock `npm audit` result returned nonzero; the script retained the nonzero result after the locked Python scan and performed no fix, resolution, or live-lock mutation.
- The clean copy, mock directory, separate caches, and audit children were reparse-checked and removed. No temporary evidence was written to tracked paths or left as repository residue.

## 7. Static CI, Dependabot, documentation, and scope evidence

Static worker inspection found a two-job `windows-latest` workflow with the approved PR/main/manual/weekly triggers, top-level `contents: read`, no secrets/write/deployment/container/reusable path, and PR-only cancellation. Every action is full-SHA pinned with an adjacent release comment. Only npm download and uv package caches are keyed by OS, architecture, Node/uv versions, and all three authority files; the scheduled run bypasses restore. The artifact is restricted to the temporary Python advisory JSON, uses `always()` with `if-no-files-found: ignore`, and has 14-day retention plus bounded cleanup.

Dependabot has exactly weekly npm and GitHub Actions entries, each limited to two open pull requests and patch/minor development grouping within its ecosystem. It has no UV entry, auto-merge, bypass, or cross-ecosystem group.

`git diff --check` passed. The final scope comparison found only the authorized worker paths above; other existing modified/untracked Phase 0 files remain pre-existing and untouched by this worker. Generated build, coverage, environment, cache, audit, and temporary-copy state remained ignored/untracked.

## 8. Worker self-assessment — not independent validation

| Criteria | Worker evidence status |
|---|---|
| AC01–AC04 | Implemented and evidenced: authority/baseline/scope recorded; direct-tool provenance and lock invariance recorded. |
| AC05–AC14 | Implemented and locally exercised: unchanged root tasks, distinct locked controls, installed-graph inventory, exact record-`0003` catalog, fail-closed audit/license/temporary/certificate safeguards. **AC08 now correctly fails closed for the unapproved claims listed above.** |
| AC15–AC21 | Implemented with worker static evidence: approved Windows workflow, pins, caches, concurrency, artifact boundary, Dependabot, and documentation. |
| AC22–AC25 | Setup, quality, coverage, build, inventory, and audit pass; safe negative controls and clean copy pass; temporary/generated state removed or ignored. **AC22 is blocked because the corrected license task must fail closed until Central disposes of the seven unapproved entries.** |
| AC26–AC32 | Implemented/evidenced within scope: no substitute authority/global tool/TLS bypass/later work/remote mutation; whitespace and scope checks pass; scanner limitations are stated. **AC32 is blocked by the unresolved license-policy disposition.** |
| AC33 | **Pending independent validator.** |
| AC34–AC35 | **Pending user-authorized hosted Windows run; blocked until that evidence and independent verdict exist.** |
| AC36 | **Central-owned and pending.** |

## 9. Independent-validation handoff

An independent validator must inspect every governing input and Section 7 artifact; verify every literal record-`0003` match and negative case; reproduce safe local controls after certificate-trust verification; inspect lock hashes, cleanup guards, action provenance, workflow/Dependabot constraints, scope, and the absence of later work. The validator must not edit files, dispatch CI, alter remote state, accept for Central, or begin P0-EP07.

Central must first decide the exact disposition for the seven unapproved
metadata-only claims above. A commit/push or hosted run cannot substitute for
that policy decision.

Hosted evidence remains **Pending user-authorized run**. Until the user supplies a `windows-latest` run, the validator must return `Blocked` for AC34/AC35 while preserving its separate local/static findings.
