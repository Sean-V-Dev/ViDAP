# ViDAP P0-EP08 v0.3 — Final Fresh-Environment Evidence Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P0_EP08.md` version 0.3 |
| Worker role | Bounded fresh-environment evidence worker |
| Evidence outcome | **Blocked** — tracked absolute user path found during required hygiene review |
| Target | `829344140381195bb5b5a4a33cafd3b91719e83b` on `main` |
| Remote identity | GitHub `origin` (sanitized; no remote action taken) |
| Permitted repository output | This report only |
| Authority | Current explicit user direction and approved packet v0.3 |

## Boundary, history, and governing inputs

This is worker evidence only. It does **not** accept EP08 or Phase 0, provide independent validation, or authorize Phase 1.

The worker read the current authority chain: explicit user direction; `ViDAP_Overview.txt`; `ViDAP_Phased_Plan_Spine.md` version 1.2; `ViDAP_Roadmap.md` version 1.7; `ViDAP_Phase_0_Plan.md` version 1.7; all accepted P0-EP01 through P0-EP07 reconciliation records; Decision Records 0001, 0003, and 0004; `docs/dependency-controls.md`; README and contribution guidance; package/task, ignore, lock, and CI configuration; and this packet.

The v0.1 and v0.2 implementation reports were preserved unmodified as blocked historical evidence. B-EP08-001 and B-EP08-002 are superseded only by a complete v0.3 proof; this blocked v0.3 result does not supersede them. Pre-existing workspace changes were the Central EP08/plan/roadmap amendments plus the v0.2 historical report; they were preserved and excluded from the committed target proof.

## Prerequisite and baseline gate

P0-EP01 through P0-EP07 are each `Accepted by Central` with no unresolved Critical or High prerequisite finding. The accepted hosted EP07 Windows evidence is for `9a85dca1f7458d779485d1433dbf97f79891cb55`. Changes through the target affect only EP07/EP08 evidence and planning records, not source, tasks, manifests, locks, CI, or process behavior, so hosted-evidence applicability passed.

The target is a committed detached checkout and retains the Windows-only posture, Node 24/npm and uv-managed CPython 3.14 contracts, sole lock authorities, and loopback-only foundation boundary.

## Isolation, runtime, and lock evidence

One unique clean checkout was created under the system temporary root, outside both the repository and OneDrive, from a no-checkout local clone and explicit detached target checkout. It excluded uncommitted workspace content. New isolated npm and uv caches were used. The checkout and both caches were removed after evidence collection; locations and names are intentionally omitted.

No inherited normal-path certificate/trust override was present for Node, npm, or uv. No certificate bypass, package-tool substitution, global install, system change, browser use, remote action, or `VIDAP_AUDIT_DIR` override occurred. The advisory control used and removed its own default bounded system-temporary child.

| Fact | Observed value |
|---|---|
| Node | `v24.21.0` |
| npm | `11.19.0` |
| uv | `0.12.16` |
| Selected CPython | `3.14.7` |
| `package-lock.json` SHA-256, pre/post | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` SHA-256, pre/post | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Both locks remained byte-identical throughout the completed command sequence.

## Required command and lifecycle evidence

| Operation | Result | Concise observation |
|---|---|---|
| `npm.cmd run setup` | Pass (exit 0) | Locked npm install and locked uv sync completed. |
| `npm.cmd run check` | Pass (exit 0) | Formatting, lint, type checks, tests, build, integration, and smoke completed with smoke last. |
| `npm.cmd run coverage` | Pass (exit 0) | Locked V8 and Python coverage paths completed. |
| `npm.cmd run deps:inventory` | Pass (exit 0) | Locked installed dependency graphs were inspected. |
| `npm.cmd run license:check` | Pass (exit 0) | Fail-closed policy passed with literal Decision 0003/0004 treatment. |
| `npm.cmd run deps:audit` | Pass (exit 0) | npm and hash-preserving uv-export/pip-audit scans completed with the default managed temporary child. |
| Smoke cleanup | Pass | Direct and proxied loopback status completed through smoke; neither prescribed listener remained. |
| Launch lifecycle inspection | Pass | Launch and smoke share child start/readiness sequence; launch prints the documented manual URL/Ctrl+C instruction; SIGINT/SIGTERM are registered; final cleanup targets recorded children only. |

No browser was opened and no hidden, bridged, or detached-console Ctrl+C emulation was attempted.

## Hygiene, documentation, and boundary review

The fresh checkout began clean. After removal of worker-only temporary markers, it had no staged or unstaged change. Dependency, environment, build, coverage, PID, and log state was confined to ignored or external temporary locations. The approved synthetic fixture remains trackable while generated/local fixture areas are ignored. Documentation and task inspection match observed Windows commands, runtime prerequisites, fixed loopback ports, manual-browser direction, smoke behavior, dependency controls, and stated deferrals. The target retains the literal Decision 0003/0004 treatment and no Phase 1 workflow/node/schema, data, model, experiment, export, persistence, hosting, desktop, or validated non-Windows behavior.

The required sensitive-pattern scan passed. The required absolute-user-path scan did not: `ViDAP_Phase_0_Plan.md` line 53 contains a user-specific Windows workspace path. The exact value is deliberately omitted from this report. This violates the packet's required hygiene review and prevents a completion attestation. Temporary proof resources were removed, and no worker-started listener or process remained.

## P0 acceptance evidence map

| Criterion | Status | Basis |
|---|---|---|
| P0-AC01 | Pass | Accepted D0.1-D0.7 records reconciled. |
| P0-AC02 | Pass | Accepted repository baseline remains present. |
| P0-AC03 | Pass | Runtime contracts and locks observed. |
| P0-AC04 | Pass | Fresh detached checkout completed locked setup. |
| P0-AC05 | Pass | Smoke startup/cleanup and launch lifecycle inspection passed. |
| P0-AC06 | Pass | Declared logical boundaries contain no future semantics. |
| P0-AC07 | Pass | Aggregate quality/build/integration/smoke and coverage passed. |
| P0-AC08 | Pass | Hosted evidence remains applicable and clean-run controls passed. |
| P0-AC09 | Pass | Inventory, license, and advisory controls passed. |
| P0-AC10 | Pass | Bounded synthetic fixture policy remains intact. |
| P0-AC11 | **Blocked** | Required tracked-content hygiene scan found an absolute user path. |
| P0-AC12 | **Blocked** | Independent validation and Central reconciliation remain required; hygiene finding is unresolved. |
| P0-AC13 | Pass | Only the bounded Phase 0 foundation seam is present. |

## Finding and Central decision needed

| ID | Severity | Owner | Criterion | Finding | Safe Central decision needed |
|---|---|---|---|---|---|
| B-EP08-003 | High | Central | EP08-AC12; P0-AC11 | A committed Phase 0 governing plan contains a user-specific absolute Windows workspace path. | Decide whether to authorize a bounded governing-document sanitization packet, then require a fresh v0.3 proof after that change. Do not accept EP08 or Phase 0 on this report. |

## Worker attestation and independent-validation handoff

**Worker attestation: Blocked.** Every required command and launch-lifecycle inspection passed with unchanged locks, but the required tracked-content hygiene review found B-EP08-003. Per packet Section 6, the worker does not claim completion and does not defer the failed condition to independent validation.

**Independent-validation handoff:** Central must first resolve B-EP08-003 and authorize the next bounded action. A later independent validator must use a separate fresh checkout, reproduce all v0.3 evidence, inspect exact scope, and state that only Central may accept EP08 and close Phase 0.
