# ViDAP P0-EP08 v0.2 — Fresh-Environment Evidence Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P0_EP08.md` version 0.2 |
| Role | Bounded fresh-environment evidence worker |
| Evidence outcome | **Blocked** — controlled-launch Ctrl+C cleanup missed its required window |
| Target | `829344140381195bb5b5a4a33cafd3b91719e83b` on `main` |
| Remote identity | GitHub `origin` (sanitized; no remote action taken) |
| Repository output scope | This report only |
| Authority | Current explicit user direction on 2026-09-19 approving this exact packet version |

## Boundary and governing inputs

This is sanitized worker evidence only. It does **not** accept P0-EP08 or Phase 0, provide an independent-validation verdict, or authorize Phase 1.

The worker read the required authority chain: current user direction; `ViDAP_Overview.txt`; `ViDAP_Phased_Plan_Spine.md` version 1.2; `ViDAP_Roadmap.md` version 1.5; `ViDAP_Phase_0_Plan.md` version 1.5; all P0-EP01 through P0-EP07 Central reconciliations; Decision Records 0001, 0003, and 0004; `docs/dependency-controls.md`; `README.md`; `CONTRIBUTING.md`; and the current package, lock, ignore, and CI configuration.

The blocked `ViDAP_P0_EP08_Implementation_Report.md` v0.1 remains unchanged historical evidence. B-EP08-001 is superseded only when a v0.2 proof is complete; this blocked report is not a substitute for completion.

Pre-existing workspace changes were Central planning/reconciliation edits to `ViDAP_P0_EP08.md`, `ViDAP_Phase_0_Plan.md`, and `ViDAP_Roadmap.md`. They were preserved; the proof used only the committed target.

## Prerequisites and target gate

P0-EP01 through P0-EP07 each report `Accepted by Central`; their records show no unresolved Critical or High prerequisite finding. EP07 hosted Windows evidence is for `9a85dca1f7458d779485d1433dbf97f79891cb55`. Intervening committed changes through the target affect only EP07/EP08 evidence and planning records, not source, tasks, manifests, locks, CI, or process behavior. The hosted-evidence applicability gate therefore passed.

The target is a committed detached-checkout baseline. It retains the Windows-only support posture, Node 24/npm and uv-managed CPython 3.14 contracts, both lock authorities, and the loopback-only foundation boundary.

## Fresh isolation, runtime, and locks

One uniquely named clean checkout was created under the system temporary root, outside the repository and OneDrive, using a no-checkout local clone and explicit detached checkout of the target. It excluded uncommitted workspace content. Separate absent temporary npm and uv caches were used. The checkout and both caches were removed after evidence collection; names and locations are intentionally omitted.

No inherited normal-path certificate or trust override was present for Node, npm, or uv. No certificate bypass, package-tool substitution, global install, system change, browser launch, remote action, or audit-directory override was used. `VIDAP_AUDIT_DIR` was absent for `deps:audit`, so its own default bounded system-temporary child was created and removed by the control.

| Fact | Observed value |
|---|---|
| Node | `v24.21.0` |
| npm | `11.19.0` |
| uv | `0.12.16` |
| Selected CPython | `3.14.7` |
| `package-lock.json` SHA-256, pre/post | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` SHA-256, pre/post | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Both lock authorities remained byte-identical through every completed routine command.

## Required command evidence

| Required operation | Result | Observation |
|---|---|---|
| `npm.cmd run setup` | Pass (exit 0) | Locked npm installation and locked uv sync completed. |
| `npm.cmd run check` | Pass (exit 0) | Formatting, linting, type checks, unit tests, build, in-process integration, and smoke completed; smoke is last. |
| `npm.cmd run coverage` | Pass (exit 0) | Locked Vitest V8 and Python coverage paths completed. |
| `npm.cmd run deps:inventory` | Pass (exit 0) | Locked npm and Python graphs were inspected. |
| `npm.cmd run license:check` | Pass (exit 0) | Fail-closed policy passed with literal Decision 0003/0004 treatment. |
| `npm.cmd run deps:audit` | Pass (exit 0) | npm and hash-preserving uv-export/pip-audit scans completed using the default managed temporary child. |
| `npm.cmd run launch` | **Blocked** | Ready message observed; Ctrl+C delivered only to the dedicated worker launch console; process did not exit within 10 seconds. |

Aggregate smoke covers direct and Vite-proxied loopback status. Controlled launch reached its ready message without opening a browser. After the failed window, its worker-owned tree was cleaned and neither prescribed loopback port had a remaining listener. That forced cleanup is not successful Ctrl+C cleanup evidence.

## Hygiene, documentation, policy, and boundary

The fresh target checkout began without staged or unstaged changes. Completed routine commands retained both lock hashes and confined dependency, environment, build, coverage, PID, and log state to ignored or temporary locations. The synthetic EP07 fixture remains trackable while generated/local fixture areas are ignored.

README and contribution instructions match the observed Windows commands, runtime prerequisites, fixed ports, manual-browser rule, smoke order, dependency controls, and Phase 0 deferrals. The current policy remains fail-closed for unlisted licenses and preserves only literal Decision 0003/0004 treatments. The target contains no Phase 1 workflow/node/schema, dataset, model, experiment, export, persistence, hosting, desktop, or validated non-Windows behavior.

Because controlled launch failed its mandatory cleanup condition, the final full hygiene/link/sensitive-content review and completion attestation cannot be asserted as complete evidence. Temporary proof resources were removed and no worker-started listener remained.

## P0 acceptance evidence map

| Criterion | Status | Basis |
|---|---|---|
| P0-AC01 | Pass | Accepted D0.1-D0.7 records were reconciled. |
| P0-AC02 | Pass | Accepted repository baseline remains present. |
| P0-AC03 | Pass | Node 24, npm, uv, CPython 3.14, and locks were observed. |
| P0-AC04 | Pass | Clean detached checkout completed locked setup. |
| P0-AC05 | **Blocked** | Controlled launch did not complete Ctrl+C cleanup in time. |
| P0-AC06 | Pass | Logical boundaries remain declared without future semantics. |
| P0-AC07 | Pass | Aggregate quality/build/integration/smoke and coverage passed. |
| P0-AC08 | Needs-Central-Decision | Hosted evidence is applicable; closeout is blocked by launch cleanup. |
| P0-AC09 | Pass | Inventory, license, and advisory controls passed. |
| P0-AC10 | Pass | Bounded synthetic fixture policy and harness role remain intact. |
| P0-AC11 | Needs-Central-Decision | Routine work was isolated, but final closeout hygiene attestation is incomplete. |
| P0-AC12 | **Blocked** | Independent validation and Central reconciliation remain required. |
| P0-AC13 | Pass | Only the bounded Phase 0 foundation seam is present. |

## Finding and Central decision needed

| ID | Severity | Owner | Criterion | Finding | Safe decision needed |
|---|---|---|---|---|---|
| B-EP08-002 | High | Central | EP08-AC07; P0-AC05 | Dedicated worker launch reached ready state, received Ctrl+C, and did not exit inside the required 10-second window. | Determine whether this is a launch signal/cleanup defect or an evidence-environment limitation; then explicitly authorize a bounded correction or revised evidence method. Do not accept EP08 or Phase 0 on this report. |

An earlier terminal-bridge launch was discarded because the bridge detached its worker process and could not safely deliver Ctrl+C. A later temporary hidden-console start first failed before any child was launched because of command-path quoting, then was repeated with corrected temporary invocation mechanics. None of these temporary observations changed repository files or product behavior.

## Limitations, attestation, and handoff

The target remains a static, input-free, loopback-only Phase 0 seam: it has no workflow/node semantics, datasets, models, experiments, exports, hosting, desktop packaging, or validated non-Windows support. No repair, dependency or configuration change, acceptance, commit, push, CI dispatch, browser use, or Phase 1 work occurred.

**Worker attestation: Blocked.** Setup, aggregate quality, coverage, inventory, license, and advisory commands passed with unchanged locks. The required controlled-launch cleanup did not. Per packet Section 6, the worker does not claim completion or defer that missed condition to independent validation.

**Independent-validation handoff:** Central must first resolve B-EP08-002 and authorize the next bounded action. Do not validate or accept this packet from this report alone. Any later independent validator must use a separate fresh isolated checkout, reproduce all required evidence, inspect exact scope, and state that only Central may accept EP08 and close Phase 0.
