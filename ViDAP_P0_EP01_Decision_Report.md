# ViDAP P0-EP01 Decision Report — Baseline and Architecture Decision

| Field | Value |
|---|---|
| Packet | P0-EP01 — Baseline and Architecture Decision |
| Packet status at execution | Approved for execution |
| Execution date | 2026-09-17 |
| Worker role | Bounded execution worker; recommendation only |
| Governing inputs read | `ViDAP_Overview.txt`; `ViDAP_Phased_Plan_Spine.md` v1.0; `ViDAP_Roadmap.md` v1.0; `ViDAP_Phase_0_Plan.md` v1.0; `ViDAP_P0_EP01.md` v0.1 |
| Authorized output | This file only |
| Decision disposition | Recommend D0.1–D0.3 for independent validation and Central reconciliation; not accepted by this worker |
| Central disposition | Accepted with the Python-runtime amendment recorded in `ViDAP_P0_EP01_Validation_and_Reconciliation.md` on 2026-09-17 |

## 1. Scope, evidence, and interpretation

This report applies the approved P0-EP01 decision method to D0.1–D0.3 only. It does not create an application, package manifest, lockfile, environment, test, workflow schema, API contract, or product behavior. “Recommendation” and “analysis” below are worker inferences from the governing inputs and cited evidence, not claims by a framework vendor.

The governing requirements most consequential to these decisions are OV §§2–3, 6–7, 9, 15–23, 25–28, and 30–31; the spine’s canonical-workflow, logical-layer-separation, local/proportional-architecture, testability, licensing, and no-runtime-LLM invariants; Roadmap checkpoints A0–A3; and the Phase 0 exclusions. In particular, the browser/editor cannot become the executable source of truth: a structured workflow and later intermediate representation must independently drive execution and export.

### Evidence method and limits

- Current external facts were researched from official documentation, official repositories, and authoritative license texts on 2026-09-17. Source IDs in this report are primary-source bibliography entries in Section 4.
- Framework versions are observations, not pinned selections. Exact compatible releases and their complete transitive dependency evidence remain a P0-EP04/P0-EP06 task after the applicable later decisions are accepted.
- The candidate evaluations are architectural. They do not claim that the selected candidate has been installed, started, benchmarked, packaged, or accessibility-tested.
- Current workstation tools describe the baseline only. They do not define project support.

## 2. Confirmed baseline and planning-state delta

### Packet authorization and input status

- **Execution-approval basis:** execution proceeded under the current explicit user direction, “Execute the approved `ViDAP_P0_EP01.md` as the bounded execution worker,” together with the packet’s `Status: Approved for execution`. Under Spine §1, current explicit user direction outranks the roadmap. The packet limits that authority to research, read-only inspection, and this one report.
- `ViDAP_Phase_0_Plan.md` is `Approved`, version 1.0, dated 2026-09-17. No superseding Phase 0 plan was found in the repository inventory.
- **Authorization discrepancy recorded at worker handoff:** the approved Roadmap v1.0 described Phase 0 as having P0-EP01 “drafted for review” and its program-state table said execution packets were “Not authorized.” Those statements conflicted with the packet status and current user direction above. Central subsequently reconciled the record under the spine's authority order; see `ViDAP_P0_EP01_Validation_and_Reconciliation.md`.
- The report path was absent before execution, so it did not conflict with pre-existing user work.

### Repository baseline at execution

| Item | Observed state |
|---|---|
| Repository / branch | Git repository; `main` tracking `origin/main` |
| Current commit | `bac14c5d5722cee6c16ebfb538646dc815cd1cd2` |
| Remote | `origin` is the repository remote recorded in the Phase 0 planning baseline; no remote change was made |
| Worktree before this output | Modified: `ViDAP_Phase_0_Plan.md`, `ViDAP_Roadmap.md`; untracked: approved `ViDAP_P0_EP01.md` |
| Planning baseline recorded in Phase 0 plan | Clean worktree at `ed68c32` with only the overview, spine, and roadmap tracked |
| Delta from planning baseline | The Phase 0 plan was promoted from draft v0.1 to approved v1.0; the roadmap was updated to say the plan is approved and EP01 drafted; EP01 is the approved untracked packet. These are planning/authorization changes, not scaffold work, and were not changed by this worker. |
| Current file inventory before output | The five governing/planning files only; no source tree, manifest, lockfile, test suite, CI config, license, README, fixture directory, or application build output found. |

### Environment baseline at execution

| Item | Observed state and consequence |
|---|---|
| Host posture | Windows development host; only Windows viability can be discussed from direct observation. No cross-platform support is claimed. |
| Shell | Windows PowerShell 5.1. The Phase 0 baseline records that direct `npm.ps1` invocation was blocked by policy; `npm.cmd` is available. Later tasks must not require an execution-policy change. |
| Git | 2.51.0 for Windows is available. |
| Node/npm | Node `v25.0.0` and `npm.cmd` `11.6.2` are installed. Node’s official release page lists v25 as EOL, so this ambient runtime is expressly not a support target [E02]. |
| Python | The Python launcher reports no installed runtime. This is a baseline fact only, not a reason to weaken the runtime policy or install anything in this packet. |
| Mutation record | No dependency, system, runtime, package-manager, configuration, scaffold, service, or remote mutation was made. |

The absence of project state and the recorded planning changes do not block the packet. They match the approved greenfield P0 baseline and leave the authorized output path uncontested.

## 3. Candidate definitions

The following concrete combinations are representatives used to evaluate the required architectural families. They are not generated projects or accepted dependency manifests.

| Candidate | Architectural family and representative combination | Why it is a bounded candidate |
|---|---|---|
| A | **Local web application:** TypeScript/React visual UI using React Flow; a separate local CPython service using FastAPI and an ASGI host such as Uvicorn. Browser UI and Python host communicate only on the local machine. React Flow supplies interactive nodes, edges, custom nodes/handles, selection, panning, and zooming [E03–E05]; FastAPI is MIT-licensed [E06]. | Directly represents the required visual-first UI plus real Python execution while keeping future desktop packaging optional. |
| B | **Packaged desktop shell with web UI:** the Candidate A UI and local Python execution host packaged/coordinated by Tauri 2 and a Rust host. Tauri can package external binaries as target-specific sidecars [E12]. | A credible local desktop route, but it adds a third runtime and early binary-distribution responsibility. |
| C | **Python-first UI/application:** CPython application with PySide6/Qt and a bespoke graph editor built on Qt Graphics View; Python directly hosts the UI and later execution components. Qt Graphics View supports custom interactive 2D items, keyboard/mouse events, dragging, selection, and zooming [E14]. | Meets the family requirement without assuming an unreviewed third-party Python node-editor library. |
| D | **No additional candidate.** | No evidence-backed alternative addresses a material weakness of A without adding an unapproved hosted platform, proprietary runtime, or another early packaging layer. Adding one would broaden the survey without changing D0.1–D0.3. |

## 4. Primary-source bibliography

All sources retrieved 2026-09-17. License conclusions concern direct candidate components only; they are not a substitute for the later full direct/transitive inventory required by D0.6.

| ID | Primary source | Evidence used |
|---|---|---|
| E01 | [Python Developer’s Guide — Status of Python versions](https://devguide.python.org/versions/) and [PEP 719 — Python 3.13 release schedule](https://peps.python.org/pep-0719/) | CPython 3.13 receives its final regular bugfix release with binary installers on 2026-10-06, then source-only security fixes as needed until approximately 2029-10. The earlier statement that bugfix support continued through 2029-10 was incorrect. |
| E02 | [Node.js — Releases](https://nodejs.org/en/about/previous-releases) | v24 is LTS; v25 is EOL; production applications should use an Active or Maintenance LTS line. |
| E03 | [React Flow — official overview](https://reactflow.dev/) | React Flow is MIT-licensed and provides node-based-editor primitives including drag, zoom, pan, selection, and elements. |
| E04 | [React Flow — terms and definitions](https://reactflow.dev/learn/concepts/terms-and-definitions) | Custom nodes and multiple handles/ports are supported. |
| E05 | [React Flow — Node API](https://reactflow.dev/api-reference/types/node) | Node UI has layout/presentation properties and ARIA-related fields; this supports, but does not itself enforce, UI/semantic separation. |
| E06 | [FastAPI — official license statement](https://fastapi.tiangolo.com/) | FastAPI is MIT-licensed. |
| E07 | [scikit-learn — installation guide](https://scikit-learn.org/stable/install.html) | Current stable documentation supports Python 3.10 or newer for scikit-learn 1.7+ and recommends isolated environments; it is evidence that CPython 3.13 remains a credible route to real Python ML libraries, not a decision to add scikit-learn now. |
| E08 | [uv — project guide](https://docs.astral.sh/uv/guides/projects/) | `pyproject.toml` project management, `uv.lock`, exact resolved versions, and locked execution behavior. |
| E09 | [uv — locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | `--locked` fails rather than updates an out-of-date/missing lockfile; exact sync behavior. |
| E10 | [uv — official overview](https://docs.astral.sh/uv/), [uv license policy](https://docs.astral.sh/uv/reference/policies/license/), [uv Apache-2.0 license](https://github.com/astral-sh/uv/blob/main/LICENSE-APACHE), and [uv MIT license](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT) | uv manages Python versions/projects, supports Windows, and is licensed at the recipient’s option under Apache-2.0 or MIT. |
| E11 | [npm — package-lock.json](https://docs.npmjs.com/cli/install/) and [npm ci](https://docs.npmjs.com/cli/commands/npm-ci/) | `package-lock.json` records exact resolution; `npm ci` requires it, fails when it disagrees with the manifest, and does not write project files. |
| E12 | [Tauri — embedding external binaries](https://v2.tauri.app/fr/develop/sidecar/) | Python services can be bundled as sidecars, but each supported target needs appropriately named binaries and explicit spawn/execute permission. |
| E13 | [Tauri — prerequisites](https://v2.tauri.app/start/prerequisites/) and [Tauri architecture/license](https://github.com/tauri-apps/tauri/blob/dev/ARCHITECTURE.md) | Windows development requires Rust and Microsoft C++ Build Tools (and uses WebView2); Tauri is MIT or Apache-2.0. |
| E14 | [Qt Graphics View Framework](https://doc.qt.io/qt-6/graphicsview.html) | Interactive 2D scene/view primitives, events, selection, drag/drop, and zoom. |
| E15 | [Qt for Python](https://doc.qt.io/qtforpython-6) and [Qt for Python license notes](https://doc.qt.io/qtforpython-6/licenses.html) | PySide6 is offered under LGPLv3/GPLv3/commercial terms and has third-party notices; its use requires distribution-license diligence. |
| E16 | [React license](https://github.com/react/react/blob/main/LICENSE), [xyflow license](https://github.com/xyflow/xyflow/blob/main/LICENSE), and [Vite license](https://github.com/vitejs/vite/blob/main/LICENSE) | Representative Candidate A direct frontend components are MIT-licensed. |
| E17 | [Uvicorn license](https://github.com/Kludex/uvicorn/blob/main/LICENSE.md), [scikit-learn license](https://github.com/scikit-learn/scikit-learn/blob/main/COPYING), and [Python license](https://docs.python.org/3.13/license.html) | Representative Python host/runtime/likely future baseline ML-library licenses are permissive (BSD/PSF/MIT compatible), subject to later component-by-component review. |
| E18 | [Qt — supported platforms](https://doc.qt.io/qtforpython-6/overviews/qtdoc-supported-platforms.html) | Current Qt 6.11 documentation lists Windows 10, Windows 11, and Windows on ARM desktop configurations as supported. This establishes Qt/PySide platform availability, not a tested ViDAP support claim. |
| E19 | [PEP 745 — Python 3.14 release schedule](https://peps.python.org/pep-0745/) | CPython 3.14 is in regular bugfix support with binary installers through 2027-10-05 and source-only security fixes as needed until approximately 2030-10. |

## 5. Hard viability gates

The statuses in this section are architectural analysis using the evidence above. “Pass with constraint” still meets the gate; the stated constraint must be carried forward. No unresolved hard gate remains.

| Gate | A — local web + local Python | B — Tauri desktop + local Python | C — PySide6/Qt Python-first |
|---|---|---|---|
| HG-01 Real Python ML path | **Pass / High.** Python host invokes supported data/ML libraries directly; current scikit-learn documentation supports current Python 3.10+ use [E07]. | **Pass / High.** Same Python host path; desktop host does not replace it. | **Pass / High.** Python UI can call libraries directly; separation is still an internal design obligation. |
| HG-02 Canonical separation | **Pass / High.** UI state is separate from the local service; topology explicitly prohibits UI-owned execution semantics. | **Pass / High.** Same canonical boundary can be retained, though Tauri adds a host bridge. | **Pass / Medium.** Feasible only if the Qt scene is treated as presentation and a separate workflow component remains canonical. |
| HG-03 Local-first operation | **Pass / High.** Browser and loopback Python host operate locally with no account or hosted service. | **Pass / High.** A packaged app can operate locally. | **Pass / High.** Single local native application. |
| HG-04 Graph-editor feasibility | **Pass / High.** React Flow offers node/edge interaction, custom nodes, and handles [E03–E05]. | **Pass / High.** Reuses the same React Flow capability. | **Pass / Medium.** Qt Graphics View has credible low-level interactive graph primitives [E14], but typed ports/editor behavior must be designed and built. |
| HG-05 Deterministic execution/export path | **Pass / High.** A service boundary reinforces a shared canonical workflow consumed independently by later runtime and exporter. | **Pass / High.** Same Python canonical path is possible; packaging is orthogonal. | **Pass / Medium.** Feasible by internal separation, but direct UI/runtime proximity makes boundary discipline more important. |
| HG-06 Testable boundary | **Pass / High.** UI, workflow, and service can have separate unit tests plus integration tests at the local boundary. | **Pass / Medium.** Adds Tauri/Rust/sidecar integration paths and target-specific packaging tests. | **Pass / Medium.** Components can be tested separately, but native UI testing and the lack of a natural process boundary increase custom test design. |
| HG-07 License compatibility | **Pass / High.** Representative mandatory components are MIT/BSD/PSF/Apache-compatible [E06, E10, E16–E17]. Later transitive review remains mandatory. | **Pass / High.** Tauri is MIT/Apache-2.0 [E13]; same later review applies. | **Pass with constraint / Medium.** LGPLv3 is not a known incompatibility with an MIT-owned project, but distribution/relinking/notices and used third-party components must be assessed [E15]. GPL-only use is not approved. |
| HG-08 Windows viability | **Pass / High.** Current Windows browser/Node/Git baseline and local Python route are viable without policy changes; project commands use `npm.cmd` where PowerShell shims are blocked. | **Pass with constraint / High.** Tauri documents Windows C++ Build Tools, WebView2, and Rust prerequisites [E13]; installation is viable but materially heavier and must not weaken policy. | **Pass / Medium.** Qt’s current supported-platform documentation lists Windows desktop configurations [E18]. No PySide package was installed, so this is platform availability evidence rather than a tested ViDAP support claim. |
| HG-09 Proportional operations | **Pass / High.** Two local processes only; no hosting, deployment, or enterprise control plane. | **Pass / Medium.** Still local, but introduces Rust, sidecar, target binary, signing/installer concerns prematurely. | **Pass / High.** One local runtime, though custom-editor cost is disproportionate compared with A. |
| HG-10 Inspectable failure path | **Pass / High.** Structured service diagnostics can preserve technical detail while the UI renders plain-language actions. | **Pass / Medium.** Same is possible, but failures cross UI, Rust host, sidecar, and Python layers. | **Pass / Medium.** Possible within Python, but needs deliberate cross-layer error envelopes rather than raw exceptions. |

## 6. Weighted comparison

Scores use the packet’s 1–5 scale. Totals are weighted sums divided by 100. The tables following the summary provide the required rationale, confidence, mitigation for scores below 3, and the phase in which each limitation matters.

| Candidate | Weighted total / 5 | Rank | Eligibility |
|---|---:|---:|---|
| A — local web + local Python | **4.62** | 1 | All hard gates pass |
| B — desktop shell + local Python | **4.04** | 2 | All hard gates pass |
| C — Python-first native UI | **3.42** | 3 | All hard gates pass; licensing constraint applies |

### A. Local web application with local Python host

| Criterion (weight) | Score | Rationale and evidence | Confidence | Mitigation if below 3 | Affected phase |
|---|---:|---|---|---|---|
| C-01 Python data/ML and notebook alignment (15) | 5 | Dedicated CPython host aligns directly with established Python libraries and a later Python/notebook exporter [E07]. | High | — | P2, P5, P7 |
| C-02 Canonical architecture and replaceable UI (15) | 5 | Process boundary makes it natural for the UI to edit/present a workflow while execution/export consume canonical semantics. This is an architectural inference, not an API claim. | High | — | P1–P3, P7 |
| C-03 Interactive graph editor (12) | 5 | React Flow explicitly provides the graph interactions, custom nodes, and handles needed for a credible typed-port UI route [E03–E05]. | High | — | P3 |
| C-04 Local user experience (10) | 4 | Browser + local host is simple for development but needs clear startup/health/recovery behavior. | Medium | — | P0, P3 |
| C-05 Testing and debugging (10) | 5 | Independent UI/service tests and local boundary integration tests map directly to the intended layers. | High | — | P0, P1–P3 |
| C-06 Packaging and reproducibility (10) | 4 | Two managed dependency graphs and a browser launch need coordination, but standard lockfile mechanisms exist [E08–E11]. | High | — | P0, P7 |
| C-07 Maintainability and contributor accessibility (10) | 5 | TypeScript web development plus ordinary CPython data/ML tooling use well-documented, independently replaceable components. | Medium | — | P0 onward |
| C-08 Dependency, licensing, and supply-chain exposure (8) | 4 | Direct candidates are permissive [E06, E10, E16–E17], but two ecosystems require the later complete inventory. | High | — | P0, P5, P8, P10 |
| C-09 Accessibility and actionable errors (5) | 4 | React Flow exposes ARIA-related node fields [E05]; accessible graph interaction and plain-language/technical errors still require product validation. | Medium | — | P3 onward |
| C-10 Cross-platform posture (5) | 4 | Browser/Node/Python architecture is portable in principle, but only Windows is an initial development claim. | Medium | — | P0, validation after P0 |

### B. Packaged desktop shell with web UI and local Python sidecar

| Criterion (weight) | Score | Rationale and evidence | Confidence | Mitigation if below 3 | Affected phase |
|---|---:|---|---|---|---|
| C-01 Python data/ML and notebook alignment (15) | 5 | Retains the same direct CPython host path as A. | High | — | P2, P5, P7 |
| C-02 Canonical architecture and replaceable UI (15) | 5 | A service-side canonical workflow remains feasible; the shell is not a semantic owner. | Medium | — | P1–P3, P7 |
| C-03 Interactive graph editor (12) | 5 | Reuses React Flow’s documented capabilities [E03–E05]. | High | — | P3 |
| C-04 Local user experience (10) | 4 | Desktop installation can be convenient, but first-run, sidecar, and recovery complexity are added. | Medium | — | P0, future packaging decision |
| C-05 Testing and debugging (10) | 4 | UI/Python tests remain possible; Rust host, permissions, sidecar lifecycle, and target artifacts add integration surfaces [E12]. | High | — | P0, P3, future packaging |
| C-06 Packaging and reproducibility (10) | 2 | Tauri requires Rust and Windows C++ Build Tools [E13]; sidecars must be target-specific [E12]. | High | Defer desktop packaging until a later approved decision after the browser-host architecture is proven. | P0 and later packaging scope |
| C-07 Maintainability and contributor accessibility (10) | 3 | Adds Rust/Tauri expertise and third ecosystem while no current requirement calls for installers. | High | — | P0 onward |
| C-08 Dependency, licensing, and supply-chain exposure (8) | 3 | Tauri’s direct license is permissive [E13], but the Rust/plugin/sidecar surface adds review work. | High | — | P0, P0-EP06, future packaging |
| C-09 Accessibility and actionable errors (5) | 4 | Web UI can retain browser accessibility; errors need to cross the added host/sidecar boundary. | Medium | — | P3 onward |
| C-10 Cross-platform posture (5) | 4 | Tauri targets major desktop platforms [E13], yet target-native sidecars and prerequisites make support validation per platform mandatory. | High | — | Future packaging validation |

### C. Python-first PySide6/Qt application

| Criterion (weight) | Score | Rationale and evidence | Confidence | Mitigation if below 3 | Affected phase |
|---|---:|---|---|---|---|
| C-01 Python data/ML and notebook alignment (15) | 5 | Python UI and execution have direct access to established libraries. | High | — | P2, P5, P7 |
| C-02 Canonical architecture and replaceable UI (15) | 4 | A separate workflow component can be maintained, but no process/language boundary prevents accidental coupling. | Medium | — | P1–P3, P7 |
| C-03 Interactive graph editor (12) | 3 | Qt has credible scene/item interaction [E14], but typed-port editing, custom components, and related UX must be authored rather than supplied by a dedicated node-editor library. | High | — | P3 |
| C-04 Local user experience (10) | 4 | Native local application has no browser/service coordination, but installer/distribution behavior is untested. | Medium | — | P0, later packaging |
| C-05 Testing and debugging (10) | 3 | Core Python can be tested directly; native interactive UI behavior needs a custom test approach. | Medium | — | P0, P3 |
| C-06 Packaging and reproducibility (10) | 2 | Native Qt/Python distribution and Qt runtime handling are more complex than a development browser plus local host. | Medium | Defer any native-distribution commitment; require a separately approved packaging feasibility decision if this candidate is reconsidered. | P0 and future packaging |
| C-07 Maintainability and contributor accessibility (10) | 3 | One language helps, but specialized Qt graph-editor work narrows contributor familiarity relative to web graph tooling. | Medium | — | P0 onward |
| C-08 Dependency, licensing, and supply-chain exposure (8) | 2 | Qt for Python’s LGPLv3/GPLv3/commercial terms and third-party notices require careful distribution compliance [E15]. | High | Use only an explicitly reviewed LGPL-compliant path, document notices/relinking obligations, and reject GPL-only/commercial assumptions; otherwise do not adopt. | P0-EP02/EP06 and future distribution |
| C-09 Accessibility and actionable errors (5) | 3 | Native controls can be accessible, but the custom canvas and error patterns need deliberate validation. | Low | — | P3 onward |
| C-10 Cross-platform posture (5) | 4 | Qt documents maintained Windows, macOS, and Linux desktop platforms [E18], but project support cannot be asserted until each target is validated. | Medium | — | Post-P0 validation |

## 7. D0.1 recommendation — application shape and process boundary

### Decision recommendation

Adopt **Candidate A: a local web application with a TypeScript browser UI and a separate local CPython execution host**. The initial UI route is React plus React Flow; the Python host route is FastAPI under an ASGI server such as Uvicorn. These are the selected initial framework directions, subject to exact-version, license, and dependency review during the authorized scaffold/dependency-control packets.

In plain language: the browser supplies the visual workbench, including the node canvas. Python supplies the genuine data-science engine. They run locally on the user’s computer; neither requires a hosted ViDAP service or account.

### Required conceptual boundary

```text
Browser UI / visual layout
        -> local boundary (loopback only)
Structured workflow and validation (canonical; P1-owned detail)
        -> semantic execution representation (P2-owned detail)
Python execution host -> established Python data/ML libraries
        -> recorded results/artifacts -> UI presentation

The same canonical workflow / representation -> later Python/Jupyter exporter
```

- The UI owns interaction, visual layout, transient view state, node configuration presentation, and result/error presentation. It does **not** own executable graph semantics, determine dependency order, invoke ML libraries, calculate authoritative results, or generate arbitrary Python as the normal execution path.
- The future workflow/schema layer owns the semantic workflow, contracts, validation, and versioning. Its exact encoding, type system, and API payloads are expressly deferred to P1; this decision does not invent them.
- The Python host owns translation from validated semantics into direct calls to approved libraries, execution diagnostics, and later artifact references. It must bind locally by default; a network-accessible service, hosting, account, cloud orchestration, or remote data plane is out of scope.
- The exporter is a later, independent canonical-workflow consumer. Notebook/code export may never treat browser layout or a frontend recalculation as its semantic input.
- Development startup may coordinate two local processes. P0-EP04 must supply a small, documented, recoverable task path; P0-EP07 may prove only the approved minimal health/communication boundary. It must not create workflow or model behavior.
- Structured error information must preserve the operation, technical diagnostic, and a display-safe plain-language cause/remedy across the local boundary. Exact error envelopes are a later P2/P3 decision.

This choice directly protects Roadmap A1–A3 and OV §22A. It also leaves desktop packaging optional: a later approved decision can wrap the proven web UI and local engine if a real distribution requirement emerges. It is not a commitment to a desktop installer now.

## 8. D0.2 recommendation — repository topology and dependency direction

### Decision recommendation

Adopt **one repository with a web application area and one Python workspace, divided into explicit logical ownership areas**. It does not require separate repositories, deployed services, containers, or a microservice platform. The following is the approved target topology for P0-EP04 to scaffold; none of these paths are created by this packet.

```text
apps/web/                  TypeScript UI and visual graph presentation
python/
  src/vidap_workflow/      canonical workflow/schema and validation ownership
  src/vidap_execution/     execution integration and local host ownership
  src/vidap_experiments/   run/experiment state ownership
  src/vidap_export/        external-artifact generation ownership
  tests/                   Python/component and boundary tests
tests/                     cross-component acceptance assets and tests
fixtures/                  controlled, permitted shared fixture assets
docs/                      contributor documentation and decision records
```

Path names may be adapted only if P0-EP04 preserves the same ownership and dependency rules. These are boundaries, not Phase 1+ schemas, interfaces, persistence designs, or implementation stubs.

### Permitted dependency direction

```text
Compile-time production dependencies (arrow means “depends on”):

vidap_execution   ------> vidap_workflow
vidap_export      ------> vidap_workflow
vidap_experiments ------> vidap_workflow
vidap_experiments ------> recorded-result abstraction

apps/web ------> local boundary/client representations only
apps/web -/-> Python component implementation imports

Runtime result exchange is not a compile-time dependency arrow:
vidap_execution produces recorded results through the boundary-defined abstraction;
vidap_experiments records those results without importing vidap_execution.

tests/fixtures -> may exercise the above; production components do not depend on tests/fixtures
docs -> no runtime dependencies
```

Rules carried to P0-EP04 and later phases:

1. `vidap_workflow` has no dependency on UI, execution, experiment storage, or exporter implementation. It is the canonical semantic owner once P1 defines it.
2. `vidap_execution` depends on validated workflow contracts and approved third-party data/ML libraries. It must not import browser/UI implementation.
3. `vidap_export` consumes canonical workflow/representation and the approved result/artifact references it needs; it must not export from UI layout, UI-only state, or execution internals.
4. `vidap_experiments` owns durable run/experiment metadata and artifact references. It may depend on canonical workflow identities and recorded-result abstractions, but must not depend on the UI for authoritative state or on the `vidap_execution` implementation.
5. `apps/web` may contain non-authoritative view-model or generated/read-only contract representations. A UX precheck cannot be the only semantic validation, and a UI duplicate may not independently define execution behavior.
6. The local boundary is the only allowed production coupling between web UI and Python engine. Direct filesystem/database shortcuts from UI to execution/experiment ownership are prohibited.
7. Tests and fixtures are consumers, not semantic authorities. Documentation records decisions but has no runtime dependency role.

This topology establishes all five required logical layers while preserving the Phase 0 rule against defining workflow contracts or persistence formats early. The exact canonical file encoding, generated bindings (if any), and semantic validation implementation remain P1 decisions.

## 9. D0.3 recommendation — runtime, package, lock, task, and platform policy

### Decision recommendation

| Topic | Policy recommended for acceptance |
|---|---|
| Python runtime | **CPython 3.14.x is the default scaffold target**, with the latest compatible patch pinned at scaffold time. Python 3.14 remains in regular bugfix support with binary installers through 2027-10 and security support through approximately 2030-10 [E19]. P0-EP04 must verify compatible Windows distributions for the exact locked foundation dependencies before scaffolding. If a mandatory foundation dependency lacks Python 3.14 support, P0-EP04 must stop and request an explicit, time-bounded Python 3.13 exception; it may not silently fall back. Do not use the absent workstation Python state as a contract. |
| Python project/package tool | **uv** with a root `python/pyproject.toml` workspace and one committed `python/uv.lock`. uv supports Windows, manages Python/projects, and its universal lock records exact resolutions [E08–E10]. Environment creation is deferred to P0-EP04. |
| JavaScript runtime | **Node.js 24.x LTS**, latest compatible patch pinned at scaffold time. Node’s release policy says to use an Active or Maintenance LTS line; the observed Node 25 is EOL [E02]. |
| JavaScript package tool | **npm bundled with the selected Node 24 release**, with the root application manifest and one committed `package-lock.json`. Use `npm ci` for clean/CI installs because it validates the lock and does not write package files [E11]. No pnpm, Yarn, Bun, or alternative JS lockfile is permitted. |
| Version declarations | P0-EP04 must add machine-readable declarations for the selected Python and Node families and record exact bootstrap/tool versions in contributor setup documentation. The declaration must fail or warn clearly on an unsupported major version; exact file syntax is a scaffold implementation detail. |
| Python lock policy | `pyproject.toml` states broad supported constraints; `uv.lock` is the sole generated Python dependency resolution and is committed. Routine setup/checks use `uv sync --locked`/`uv run --locked`; lock changes are intentional dependency changes, never incidental task output [E08–E09]. Do not commit `requirements*.txt`, Poetry lockfiles, Conda environments, or multiple resolver outputs as competing sources of truth. |
| JavaScript lock policy | `package.json` expresses ranges/metadata; root `package-lock.json` is committed and is the sole JS resolution. Routine setup/checks/CI use `npm ci`; lock changes require an explicit dependency change. Do not commit a second JS lockfile [E11]. |
| Task entry strategy | The root JavaScript manifest is the sole cross-stack task entry. On the current supported PowerShell path, contributors invoke it as `npm.cmd run <task>`; ordinary POSIX use may use `npm run <task>`. Root tasks delegate to the pinned Python project through `uv`; no developer-facing task depends on a global package or a user-specific shell profile. P0-EP04 establishes `setup`, `dev`, `build`, and `launch` only as allowed by its packet; P0-EP02/P0-EP05 define the quality/check task names and behavior. |
| Global prerequisites | Only Git, Node 24 LTS with bundled npm, a modern supported browser, and an approved installation of uv are global/bootstrap prerequisites. CPython 3.14 is provisioned/selected through the accepted Python tooling rather than inferred from a user’s ambient Python. No global `npm` packages, `npx`-installed task tools, `uv tool install` task tools, virtual environments, or system-policy changes may be required. Bootstrap installation must use a security-approved path and never changes PowerShell execution policy. |
| Platform posture | Windows is the **only initial supported development platform**. The architecture is portable in principle, but macOS/Linux are not yet supported claims and require clean-environment validation before being documented as supported. No installer, signing, container, or desktop-package commitment is made. |
| Synced-workspace posture | P0-EP03/P0-EP04 must ignore/isolate environments, `node_modules`, caches, build output, datasets, databases, and secrets so OneDrive does not become application state. This decision does not choose an experiment/persistence location. |

The current Node 25 installation and absent Python are deliberately non-authoritative. The selected policy favors an LTS Node line and the current stable Python bugfix line whose project dependencies are verified and fully locked, rather than trying to reproduce this particular workstation.

## 10. License and supply-chain decision implications

The recommended direct architecture components have permissive primary licenses: React, React Flow, Vite, FastAPI, uv, and the likely Uvicorn/scikit-learn baseline paths are MIT, dual MIT/Apache, BSD, or PSF-licensed [E06, E10, E16–E17]. This supports an MIT-owned project but is **not** a blanket approval for every transitive package or any future ML framework.

Required carry-forward constraints:

- P0-EP02 must decide the allowed-license policy, unknown-license failure policy, update cadence, and vulnerability response. This report does not preempt D0.4–D0.7.
- P0-EP04 must capture direct package choices in the two selected lockfiles, not add ML/model-family dependencies beyond the approved Phase 0 shell need.
- P0-EP06 must produce the direct/transitive inventory and license evidence for the actual locked graphs, including notices and platform binaries.
- Any later addition such as XGBoost, CatBoost, LightGBM, PyTorch, Optuna, or AutoML remains a separate phase-appropriate license/maintenance/packaging decision. None is selected or installed here.

## 11. Rejected alternatives and material tradeoffs

### Rejected as the initial D0.1 choice: Candidate B — desktop shell

Candidate B passes every hard gate. It is not selected because its benefit—early installer/native window distribution—does not satisfy a present product requirement. Tauri’s documented Windows prerequisites add Rust, Microsoft C++ Build Tools, and WebView2; a Python sidecar needs target-specific binary handling and explicit process permissions [E12–E13]. That early complexity weakens the proportional-operations and reproducible-foundation objectives without improving canonical semantics or graph-editor feasibility over Candidate A.

The tradeoff is deliberate: Candidate A initially launches in a browser and needs local process coordination. It avoids committing the project to a desktop-package lifecycle before a useful canonical workflow and visual slice exist. Desktop packaging remains a future evidence-backed option, not a rejected product possibility.

### Rejected as the initial D0.1 choice: Candidate C — Python-first native UI

Candidate C passes every hard gate but ranks lower. Qt Graphics View makes an interactive canvas credible [E14]; nevertheless, it requires more bespoke graph-editor functionality than React Flow. The absence of a natural process boundary also puts more burden on code organization to prevent UI state from becoming execution truth. Qt for Python’s LGPLv3/GPLv3/commercial terms and third-party notices introduce a distribution-compliance burden [E15].

The tradeoff is that Candidate C would simplify language count. It does not, however, outweigh the web graph-editor maturity, independent boundary testing, and future browser UI accessibility path of Candidate A.

### Rejected: extra Candidate D

No Candidate D was added. A hosted/SaaS visual environment fails local-first and proportional-operations requirements; an alternate desktop wrapper repeats Candidate B’s premature packaging cost; and a novel graph framework alone would not improve the mandated separation between visual representation, canonical workflow, execution, experiments, and export.

## 12. Handoff constraints for subsequent approved packets

### P0-EP02 — Quality, CI, dependency, and fixture decisions

- Select tools that work with CPython 3.14/uv and Node 24/npm without adding a competing task runner or package manager.
- Define the actual quality, integration, license, and fixture policies; do not treat this report’s permissive-license observations as a completed inventory.
- Ensure planned cross-boundary tests can independently exercise the browser UI, canonical workflow, and Python host without defining Phase 1 schema or Phase 2 execution behavior.
- Retain Windows `npm.cmd` task viability and forbid a PowerShell execution-policy workaround.

### P0-EP03 — open-source and repository baseline

- Document the one-repository/topology decision, Windows-only initial support statement, supported global prerequisites, and the fact that desktop packaging is deferred.
- Establish ignore and local-state rules for the OneDrive-synced workspace without creating runtime persistence semantics.
- Establish a decision-record home that can later link/migrate this accepted report without changing its meaning.

### P0-EP04 — reproducible scaffold

- Scaffold only the Section 8 ownership areas and two selected dependency graphs; add no Phase 1 workflow/schema, model, dataset, experiment, or exporter behavior.
- Create the accepted version declarations, `python/pyproject.toml`, `python/uv.lock`, root JS manifest, and root `package-lock.json`; do not create competing manifests/lockfiles.
- Provide root `npm.cmd run` task entry on Windows and lock-respecting delegated uv tasks. Exact framework versions must be researched and locked at that time, with license and compatibility evidence retained for review.
- Use a local-only browser/Python boundary and a recoverable two-process startup path; leave health payload, workflow payloads, and error-envelope formats to their owning later decisions.

## 13. Unresolved questions and feasibility spikes

| Finding | Status | Owner / required handling |
|---|---|---|
| Exact compatible React/React Flow/Vite/FastAPI/Uvicorn/uv release set and full transitive licenses | Non-blocking | P0-EP04 chooses and locks only foundation dependencies; P0-EP06 independently inventories and checks them. |
| Exact Windows local-process startup/recovery implementation | Non-blocking | P0-EP04/P0-EP07, constrained by the local-only boundary and `npm.cmd` task entry. No API or health contract is decided here. |
| Accessible typed-graph interaction acceptance evidence | Non-blocking | P3 plan; React Flow’s accessibility-related fields support a route but do not prove ViDAP accessibility [E05]. |
| macOS/Linux support | Non-blocking | No support claim until clean-environment validation; later scope/validation owner. |
| Desktop packaging need | Non-blocking | Defer until a demonstrated user/distribution need and a separately approved decision. |
| Authorization-record conflict (V-01) | **Resolved by Central on 2026-09-17** | The current explicit user approval authorized execution under the spine’s authority order. Central reconciled the stale roadmap state and recorded the disposition in `ViDAP_P0_EP01_Validation_and_Reconciliation.md`. |
| Python lifecycle statement and selection (V-05) | **Resolved by Central on 2026-09-17** | E01 now states the correct Python 3.13 lifecycle. D0.3 is amended to target Python 3.14 by default, with an explicit compatibility gate and no silent fallback. |

**Feasibility spike proposal:** None. Documentary evidence resolves the D0.1–D0.3 choice without installation or execution. No material uncertainty changes the local-web/Python recommendation, so a spike would be premature.

## 14. Acceptance-criteria handoff and independent-validation request

Documentary self-checking is required for this packet and has been performed below. It is limited to checking this report, its recorded evidence, arithmetic, stated scope, and the Git file-scope evidence. It is not independent validation and cannot accept D0.1-D0.3 or the packet. AC15 remains for the independent validator, and AC16 remains for Central.

### Independent-validation outcome recorded

An independent validator returned **Revise** and did not accept D0.1-D0.3 or start P0-EP02. The findings were:

- **V-01 (major):** reconcile the packet/roadmap execution-authorization conflict under Spine §1.
- **V-02 (major):** make the experiment/state dependency rule unambiguous and remove the diagram’s apparent dependency on execution implementation.
- **V-03 (major):** add primary Windows-platform evidence, or reduce Candidate C’s HG-08 conclusion/confidence.
- **V-04 (minor):** directly trace uv’s Apache-2.0 licensing as well as MIT.

Sections 2, 4–6, 8, 13, and this section contain the worker’s documentary responses to V-01–V-04. A subsequent revalidation confirmed V-02 through V-04 resolved and returned `Blocked` on V-01 plus the newly identified Python-lifecycle finding V-05. Central later resolved V-01 and V-05 and accepted the packet through the documented user-directed process exception in `ViDAP_P0_EP01_Validation_and_Reconciliation.md`. The historical validator outcomes remain `Revise` and `Blocked`; they are not relabeled as `Accept`.

### EP01 acceptance-criteria self-assessment

| Criterion | Self-assessment status | Evidence and limitation |
|---|---|---|
| EP01-AC01 | **Pass (self-assessed)** | Section 2 records the execution-time repository, planning delta, and tool baseline without absolute user paths, credentials, or other unrelated machine information. |
| EP01-AC02 | **Pass (self-assessed)** | Section 3 defines and evaluates Candidates A, B, and C; it documents why no Candidate D was added. |
| EP01-AC03 | **Pass (self-assessed)** | Section 5 applies HG-01 through HG-10 to each candidate before the weighted comparison. |
| EP01-AC04 | **Pass (self-assessed)** | Section 6 gives every eligible candidate a C-01 through C-10 score, rationale, confidence, mitigation for scores below 3, and affected phase. |
| EP01-AC05 | **Pass (self-assessed)** | Section 4 records current primary sources, direct links, retrieval date, and the external facts used in conclusions, including the new Qt Windows-platform evidence (E18). |
| EP01-AC06 | **Pass (self-assessed)** | Sections 4 and 10 identify licenses for the representative mandatory candidate components and reserve direct/transitive inventory review for the packet that owns it. |
| EP01-AC07 | **Pass (self-assessed)** | Section 7 defines a local-only application/process boundary and explicitly separates UI state from canonical execution semantics. |
| EP01-AC08 | **Pass (self-assessed)** | Section 8 assigns UI, workflow/schema, execution, experiment/state, export, tests/fixtures, and documentation responsibilities with unambiguous permitted dependency direction: experiment/state depends on workflow and recorded-result abstractions, not execution implementation. |
| EP01-AC09 | **Pass (self-assessed)** | Section 9 selects maintained runtime families, package managers, lockfile policy, root task entry, Windows posture, and global-prerequisite constraints. |
| EP01-AC10 | **Pass (self-assessed)** | Sections 6, 10, 11, and 13 state tradeoffs, lower-confidence evidence, mitigations, and reasons for rejecting the viable alternatives. |
| EP01-AC11 | **Pass (self-assessed)** | Section 12 supplies packet-specific constraints for P0-EP02, P0-EP03, and P0-EP04 without implementing them. |
| EP01-AC12 | **Pass (self-assessed; Git evidence recorded in Section 15)** | No install, dependency, system configuration, scaffold, manifest, lockfile, or product behavior was introduced; final Git inspection is the scope evidence. |
| EP01-AC13 | **Pass (self-assessed; Git evidence recorded in Section 15)** | The final Git inspection distinguishes the pre-existing planning changes from the sole EP01 output, this report. |
| EP01-AC14 | **Pass (self-assessed)** | Section 13 identifies no blocking architectural uncertainty requiring a feasibility spike; the documented non-blockers do not prevent a responsible D0.1-D0.3 recommendation. V-01 is separately recorded as a Central-owned authorization/acceptance blocker, not a documentary-evidence spike question. |
| EP01-AC15 | **Accepted by recorded user/Central process exception; no independent `Accept` verdict** | Independent review validated the substantive architecture, arithmetic, licensing direction, corrected dependency direction, Qt evidence, uv license evidence, and file scope. Its final `Blocked` result concerned V-01 and V-05, which Central resolved. The user explicitly directed acceptance without another paperwork-only audit cycle; the exception is recorded without rewriting the historical verdict. |
| EP01-AC16 | **Pass — Central accepted on 2026-09-17** | Central accepted D0.1 and D0.2 and accepted D0.3 with the Python 3.14 amendment in `ViDAP_P0_EP01_Validation_and_Reconciliation.md`. |

### Self-check results

- **Weighted arithmetic:** The recorded weighted totals are A = 4.62, B = 4.04, and C = 3.42. The independent validator must recalculate them rather than relying on this worker's calculation.
- **Scope check:** This report remains the sole EP01 repository output. The final read-only Git inspection and its exact worktree record are included in Section 15.
- **Acceptance boundary:** The worker self-assessment supplied evidence only. Independent outcomes remained `Revise` and `Blocked`; Central's later acceptance and the explicit process exception are recorded separately and do not rewrite those outcomes.

The independent validator should:

1. Confirm Central has reconciled the P0-EP01 authorization conflict recorded in Section 2/13, applying Spine §1 authority rather than silently treating the roadmap statement as resolved.
2. Recheck representative high-impact sources and every license assertion in Section 4/10, including the Python 3.13 and Node 24 lifecycle conclusions, Qt Windows-platform evidence (E18), and uv’s Apache-2.0/MIT policy (E10).
3. Recalculate the Section 6 totals from the listed scores: A = 4.62, B = 4.04, C = 3.42.
4. Verify that every HG-01 through HG-10 result is consistently applied before scoring, and challenge Candidate B as the most plausible alternative.
5. Confirm Section 8’s topology retains UI, workflow/schema, execution, experiment/state, and export boundaries without prematurely defining Phase 1/2 contracts; specifically verify that experiment/state has no dependency on execution implementation.
6. Confirm Section 9’s policy is based on maintained releases rather than the observed Node 25/no-Python workstation state, and that it does not require a PowerShell policy change.
7. Inspect the final Git change set for the Section 11 one-file constraint, prohibited dependencies/manifests/scaffolds, and any user-work conflict.
8. Return `Accept`, `Revise`, or `Blocked` with packet/requirement-linked findings. Central alone then accepts, rejects, or returns D0.1–D0.3.

## 15. Evidence return to Central

| Required handoff item | Evidence |
|---|---|
| Report path | `ViDAP_P0_EP01_Decision_Report.md` |
| Current commit at execution | `bac14c5d5722cee6c16ebfb538646dc815cd1cd2` |
| Read-only commands used | Governing-document reads; Git branch/status/commit/remote/file inventory/diff inspection; output-path check; tool/version checks for Node, npm, Python launcher, Git, and PowerShell. |
| Research sources used | Official Python, Node, React Flow, FastAPI, scikit-learn, uv, npm, Tauri, Qt, and official-repository license sources listed in Section 4. |
| Install/system mutation | None. No package, runtime, configuration, execution policy, scaffold, project, service, or remote mutation was performed. |
| Worker self-assessment | Completed in Section 14. AC15 has an independent `Revise` outcome and requires revalidation; AC16 remains pending Central acceptance. |
| Final worktree state | Read-only post-write inspection found `main...origin/main` with: `M ViDAP_Phase_0_Plan.md` and `M ViDAP_Roadmap.md` (**pre-existing planning-promotion changes**); `?? ViDAP_P0_EP01.md` (**pre-existing approved packet input**); and `?? ViDAP_P0_EP01_Decision_Report.md` (**the sole EP01 execution output**). `git diff --name-status` lists only the two pre-existing tracked planning changes; `git ls-files --others --exclude-standard` lists the approved packet and this report. `git diff --check` reported no whitespace errors (only existing LF/CRLF notices). The untracked report diff was inspected with `git diff --no-index --stat`. |
| Blocking findings at worker handoff | V-01 was pending Central reconciliation; the later validator also identified V-05. Both are resolved in `ViDAP_P0_EP01_Validation_and_Reconciliation.md`. No blocking finding remains for the accepted packet. |
| Non-blocking findings | Exact dependency set/transitive licenses, startup detail, accessibility evidence, non-Windows validation, and future desktop need are carried forward in Section 13. |
| Spike proposal | None. |
| Validation readiness at worker handoff | Revalidation was required. Revalidation later confirmed V-02–V-04 and returned `Blocked` on V-01/V-05. The user then directed Central acceptance after those two findings were resolved; see the reconciliation record. |

Worker execution ended with this evidence and validation handoff. Central reconciliation is now complete. P0-EP02 may be drafted but remains unauthorized for execution.
