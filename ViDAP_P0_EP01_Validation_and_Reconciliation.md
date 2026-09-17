# ViDAP P0-EP01 Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | P0-EP01 - Baseline and Architecture Decision |
| Status | Accepted by Central |
| Reconciliation date | 2026-09-17 |
| Decision report | `ViDAP_P0_EP01_Decision_Report.md` |
| Governing packet | `ViDAP_P0_EP01.md` version 1.0 |
| Authority | Explicit user direction and Central reconciliation under Spine Section 1 |

---

## 1. Purpose

This record preserves the independent validator's actual findings, resolves the remaining findings, records the user's explicit direction to accept the packet, and states the exact D0.1-D0.3 decisions that later packets may rely on.

The historical validation verdicts are not rewritten as `Accept`. Central accepts the packet after resolving or explicitly disposing of their remaining findings.

---

## 2. Validation History

### Initial validation: Revise

The independent validator confirmed that:

- weighted totals recalculated correctly as A = 4.62, B = 4.04, and C = 3.42;
- Candidate A aligned with the canonical-workflow and local-first boundaries;
- Candidate B was a credible alternative but its additional Rust, Windows tooling, sidecar, and packaging costs supported rejection for the initial architecture;
- the proposed architecture had no identified incompatible mandatory license;
- Git/file-scope evidence showed no scaffold, manifest, lockfile, dependency output, or product code, and the decision report was the sole EP01 execution output.

The validator returned `Revise` with findings V-01 through V-04.

### Revalidation: Blocked

After the execution worker revised the decision report, the validator confirmed V-02 through V-04 were resolved:

- **V-02:** The experiment/state dependency direction was made unambiguous and no longer depended on execution implementation.
- **V-03:** Current primary Qt/PySide Windows-platform evidence was added.
- **V-04:** uv's official Apache-2.0/MIT licensing policy was directly cited.

The validator then returned `Blocked` because:

- **V-01:** the roadmap still described EP01 as drafted/not authorized even though the user had explicitly approved and executed it;
- **V-05:** the report inaccurately described Python 3.13 as remaining in bugfix support through 2029-10 and did not adequately address selecting it immediately before its final regular bugfix release.

No feasibility spike was requested, and no architecture, calculation, scope, or licensing defect remained after V-02 through V-04.

---

## 3. Central Finding Dispositions

### V-01 - Resolved

The user explicitly approved P0-EP01 and directed a bounded worker to execute it. Under the authority order in the approved spine, current explicit user direction outranks stale roadmap status text. The execution itself therefore had valid authority.

The roadmap and packet status are updated as part of this reconciliation. This is an administrative record correction; it does not retroactively broaden the packet or excuse work outside its scope. The worker remained within the packet's single-output boundary.

### V-02 - Resolved and independently confirmed

The corrected dependency rules state that experiment/state may depend on canonical workflow identity and recorded-result abstractions, but not on execution implementation. The independent validator confirmed the correction.

### V-03 - Resolved and independently confirmed

The report added current official Qt/PySide Windows-platform evidence. The independent validator confirmed the correction.

### V-04 - Resolved and independently confirmed

The report added the official uv dual-license policy and both license texts. The independent validator confirmed the correction.

### V-05 - Resolved with a Central amendment

The original lifecycle sentence was wrong. Python 3.13 receives its final regular bugfix release with binary installers on 2026-10-06 and then source-only security releases as needed until approximately 2029-10. Python 3.14 remains in regular bugfix support through 2027-10-05 and security support until approximately 2030-10.

Central amends D0.3 as follows:

- CPython 3.14.x is the default Phase 0 scaffold target.
- P0-EP04 must verify that the exact locked foundation dependencies have compatible Windows distributions before scaffolding.
- If a mandatory foundation dependency lacks Python 3.14 support, P0-EP04 must stop and request an explicit, time-bounded Python 3.13 exception with an upgrade trigger. Silent fallback is prohibited.
- Future phase-specific ML dependencies receive their own compatibility checks when introduced; Phase 0 does not freeze the entire future ML ecosystem today.

This correction is supported by the official Python version-status page, PEP 719, and PEP 745. It changes the runtime default without changing the accepted architecture, topology, package manager, or lockfile strategy.

---

## 4. Revalidation Exception

The packet ordinarily requires a final independent `Accept` result for EP01-AC15. The last independent result was `Blocked` solely on V-01 and V-05 after V-02 through V-04 were confirmed resolved.

The user explicitly directed Central to accept rather than perform another paperwork-only audit cycle. Central records that direction as an approved process exception:

- the original validator verdict remains visible and is not relabeled;
- V-01 is reconciled by the governing authority record;
- V-05 is corrected using current official Python lifecycle evidence and a more conservative compatibility gate;
- no substantive negative finding about the selected application architecture, repository topology, scoring, licensing direction, or execution scope is waived;
- EP01-AC15 is accepted by explicit user/Central exception rather than represented as an independent `Accept` verdict.

This exception applies only to P0-EP01. It does not remove independent validation from later packets.

---

## 5. Accepted Decisions

### D0.1 - Application shape and process boundary: Accepted

ViDAP will begin as a local web application with:

- a TypeScript/React visual UI using React Flow as the initial graph-editor direction;
- a separate local CPython execution host using FastAPI and an ASGI host such as Uvicorn;
- a loopback-only local boundary by default;
- no required hosted service, account, cloud orchestration, or desktop wrapper;
- canonical workflow and execution semantics outside browser layout and UI-only state.

Desktop packaging remains a later evidence-based decision.

### D0.2 - Repository topology and ownership: Accepted

ViDAP will use one repository with explicit ownership areas for:

- the web UI;
- workflow/schema and validation;
- execution integration and local host;
- experiment/state;
- export;
- tests and fixtures;
- documentation and decision records.

The dependency rules in the corrected decision report are authoritative. Phase 0 scaffolding may establish locations and boundaries but must not define Phase 1 workflow semantics or Phase 2 execution contracts.

### D0.3 - Runtime and package-management policy: Accepted with amendment

- Python default: CPython 3.14.x, subject to the P0-EP04 compatibility gate above.
- Python project management: uv, one `pyproject.toml` workspace, and one committed `uv.lock`.
- JavaScript runtime: Node.js 24 LTS.
- JavaScript package management: bundled npm with one committed `package-lock.json`; clean installs use `npm ci`.
- Cross-stack tasks: root JavaScript manifest, using `npm.cmd` on the supported Windows PowerShell path and delegating locked Python tasks through uv.
- Initial platform claim: Windows only until other platforms pass clean-environment validation.
- No competing package managers, global task packages, PowerShell policy changes, containers, installers, or hosted infrastructure are implied.

Exact package versions and full direct/transitive license evidence remain owned by their later approved packets.

---

## 6. Acceptance Decision

Central accepts D0.1 and D0.2 as recommended and D0.3 with the Python 3.14 amendment above.

P0-EP01 is `Complete`. P0-EP02 may now be drafted. This acceptance does not authorize P0-EP02 execution, dependency installation, repository scaffolding, or product implementation.

---

## 7. Evidence Sources for the Central Amendment

- [Python Developer's Guide - Status of Python versions](https://devguide.python.org/versions/), accessed 2026-09-17.
- [PEP 719 - Python 3.13 release schedule](https://peps.python.org/pep-0719/), accessed 2026-09-17.
- [PEP 745 - Python 3.14 release schedule](https://peps.python.org/pep-0745/), accessed 2026-09-17.

These sources support the lifecycle correction only. Dependency compatibility must be verified from the actual locked package set in P0-EP04 and P0-EP06.
