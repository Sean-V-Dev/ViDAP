# ViDAP P0-EP08 Implementation Report — Blocked Evidence Handoff

| Field | Value |
|---|---|
| Packet | P0-EP08 — Fresh-Environment Validation and Reconciliation Evidence |
| Packet version | 0.1 |
| Approval | Current explicit user direction, 2026-09-19 |
| Worker role | Bounded fresh-environment evidence worker |
| Report status | **Blocked — incomplete evidence; not an EP08 or Phase 0 acceptance** |
| Target commit | `9a85dca1f7458d779485d1433dbf97f79891cb55` |
| Target branch | `main` at `origin/main` |
| Sanitized remote identity | `github.com/Sean-V-Dev/ViDAP` |
| Permitted repository scope | This report only |

## 1. Authority, governing inputs, and target baseline

This worker acted only under the current explicit approval for P0-EP08 version 0.1. It read the specified governing inputs in packet order: the current direction; applicable Overview sections; Spine version 1.2; Roadmap version 1.2; Phase 0 Plan version 1.1; accepted P0-EP01 through P0-EP07 reconciliations; Decisions 0001, 0003, and 0004; dependency controls; current README and CONTRIBUTING guidance; and the package, task, ignore, and CI configuration.

P0-EP01 through P0-EP07 are each recorded Complete by Central, with no unresolved Critical or High finding. The target is the committed hosted-evidence commit from the P0-EP07 reconciliation, `9a85dca1f7458d779485d1433dbf97f79891cb55`. The accepted hosted Windows run remains applicable because no committed source, task, manifest, lock, CI, or process change exists after it.

Before this work, the target workspace contained Central-owned uncommitted planning/reconciliation material outside the target: modifications to the EP07 packet, Phase 0 Plan, Spine, and Roadmap; plus untracked EP07 reconciliation and this approved EP08 packet. No uncommitted product, manifest, lock, CI, configuration, or generated-state change was present. Those files were preserved and excluded from the proof.

The inspected target retains the accepted Windows-only, local-first foundation: Node 24 with npm and `package-lock.json`; uv-managed CPython 3.14 with `python/uv.lock`; loopback-only ports 8000 and 5173; and no alternate lock or package authority.

## 2. Isolation and environment facts

One uniquely named clean Git clone was created in a non-OneDrive temporary location from the recorded committed target. It was not copied from the working tree, resolved exactly to the target commit, and was clean before proof work. New npm and uv caches were isolated beside that clone. The clone, both caches, and the attempted audit directory were removed after evidence collection; their absence was confirmed. No worker-started listener remained on either prescribed port.

Before setup, the certificate-override variables relevant to the documented Windows npm/uv path were all absent, including SSL certificate file/directory, requests/curl bundle, Node extra-CA, npm CA-file, uv TLS, and uv insecure-host overrides. No trust bypass, certificate change, system change, or substitute tool was used.

| Fact | Observed result |
|---|---|
| Node | `v24.21.0` |
| npm | `11.19.0` |
| uv | `0.12.16` |
| Selected CPython | `3.14.7` |
| `package-lock.json` SHA-256, before and after routine commands | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` SHA-256, before and after routine commands | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

## 3. Required-command evidence

| Required command or observation | Result | Concise evidence |
|---|---|---|
| `npm.cmd run setup` | Pass | Locked npm installation and `uv sync --locked` completed using isolated caches; uv selected CPython 3.14.7. |
| `npm.cmd run check` | Pass | Authoritative ordered aggregate completed; its declared final task is the cross-process smoke path. |
| `npm.cmd run coverage` | Pass | V8 and Python coverage paths completed; generated reports remained ignored. |
| `npm.cmd run deps:inventory` | Pass | Current direct/transitive installed npm and Python graph was printed without resolution or lock mutation. |
| `npm.cmd run license:check` | Pass | Locked fail-closed control completed using literal Decisions 0003/0004 treatment. |
| `npm.cmd run deps:audit` | **Blocked** | See Section 4. |
| `npm.cmd run launch`, ready message, Ctrl+C, child cleanup | Not run | Prohibited after the required advisory-control failure. No browser was opened. |
| Direct/proxied loopback observation | Not newly collected | Aggregate smoke completed, but the separate controlled-launch observation was not authorized after the blocker. |

The temporary checkout was clean after the completed commands, with generated dependency, environment, build, and coverage state ignored. Both authoritative locks remained byte-identical. Documentation and inspected task definitions agree on Windows-only support, Node 24/uv/CPython 3.14, fixed loopback ports, manual browser opening only, smoke-last aggregate behavior, and Phase 0 deferrals. The fixture boundary is retained: the sole synthetic status fixture is limited to the harness/tests and is not served as data.

## 4. Named blocker

**B-EP08-001 — `npm.cmd run deps:audit` did not run with a conforming local audit temporary directory.** Severity: High. Owner: Central / fresh evidence worker.

The worker supplied an isolated audit-directory override beneath the fresh proof's non-OneDrive temporary root. The documented control requires any local override to be a newly absent, specifically named child of the resolved **system** temporary root. It fail-closed before advisory retrieval with the concise diagnostic: `Refusing an audit path outside the expected temporary-directory child.` No package, lock, repository, or system state was changed by this failure.

Per packet Sections 1 and 6, the worker did not retry the command with a different value, did not complete the launch observation, and does not call the evidence complete. A safe Central decision is required: authorize a new fresh P0-EP08 evidence-worker run that repeats the whole proof from a new clean external checkout and uses only a documented conforming system-temporary audit directory (or no override). It must not reuse this worker's partial results as a substitute for the required full proof.

Affected criteria: P0-AC09; EP08-AC06, EP08-AC16, and the independent-validation prerequisite. No determination is made about current advisory findings because advisory tools did not run.

## 5. Phase 0 acceptance map

| Criterion | Worker evidence state |
|---|---|
| P0-AC01 | Pass — D0.1-D0.7 remain accepted in the reconciliations. |
| P0-AC02 | Pass — MIT and contributor-facing guidance remain present. |
| P0-AC03 | Pass — pinned Node 24 and CPython 3.14 contracts; both locks unchanged. |
| P0-AC04 | Pass — fresh locked setup completed without manual edits or global packages. |
| P0-AC05 | Blocked — separate controlled launch/cleanup observation was not run after B-EP08-001. |
| P0-AC06 | Pass — inspected ownership boundaries remain markers/seams, not future semantics. |
| P0-AC07 | Pass — fresh aggregate check and coverage completed. |
| P0-AC08 | Pass — accepted hosted Windows evidence applies to the unchanged target. |
| P0-AC09 | Blocked — inventory and license evidence passed, but advisory evidence did not run. |
| P0-AC10 | Pass — the single synthetic, bounded, documented fixture remains confined to harness/tests. |
| P0-AC11 | Pass — temporary checkout was clean and all named temporary proof paths were removed. |
| P0-AC12 | Blocked — fresh independent validation cannot begin from incomplete worker evidence. |
| P0-AC13 | Needs-Central-Decision — Central reconciliation remains a later gate. |

## 6. Limitations, exclusions, and handoff

Phase 0 remains intentionally limited. The target contains no workflow/node or schema semantics, datasets/data loading, models, experiments, export, persistence, hosting, desktop packaging, or validated non-Windows support. The static loopback status seam is not a product or general API contract. Browser end-to-end testing and JSX accessibility linting remain deferred as previously recorded.

This report is evidence only. It does **not** accept P0-EP08 or Phase 0, replace independent validation, issue an independent verdict, or authorize P0-EP09/Phase 1 work.

## 7. Worker completion attestation and independent-validation handoff

I attest that I preserved the target repository, changed no repository file other than this report, used one isolated external checkout and isolated caches, did not open a browser or alter local/system/remote settings, and removed only the known isolated proof paths. However, I cannot attest worker completion because the required `deps:audit` command failed its documented temporary-directory guard and the required controlled-launch observation was therefore not performed.

**Independent-validation handoff: Blocked.** A fresh independent validator must not accept or reproduce partial evidence from this report. After Central authorizes a new complete fresh-worker proof, the validator must independently read all governing inputs and reproduce the entire packet in its own isolated location before issuing Accept, Revise, or Blocked for Central.
