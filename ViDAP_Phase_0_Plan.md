# ViDAP Phase 0 Plan - Project Foundation and Delivery Baseline

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.0 |
| Approved | 2026-09-17 |
| Parent | `ViDAP_Roadmap.md` version 1.0 |
| Spine phase | P0 - Project Foundation and Delivery Baseline |
| Product source | `ViDAP_Overview.txt` |
| Created | 2026-09-17 |
| Owner | Central |

---

## 1. Authorization and Boundary

This plan translates approved roadmap Phase 0 into decision work, foundation workstreams, acceptance evidence, and proposed execution-packet boundaries.

Approval of this plan will authorize Central to prepare the first bounded Phase 0 execution packet. It will not by itself authorize repository changes, dependency installation, application scaffolding, or implementation. Each execution packet requires separate approval before execution.

Phase 0 establishes a reproducible project foundation. It does not implement workflow semantics, graph editing, data profiling, model training, experiment behavior, or export functionality.

---

## 2. Plain-English Phase Intent

### What we are building or changing

We will turn the current documentation-only repository into a minimal, reproducible open-source project foundation. That foundation will contain the approved application shape, pinned development environments, a minimal runnable application shell, test and quality entry points, continuous-integration checks, dependency/license controls, contribution documentation, decision records, and a small controlled-fixture policy.

### Why the system needs it

Every later phase depends on contributors and validation workers being able to build and test the same project consistently. Selecting the application boundary now also prevents the visual editor, Python ML runtime, persistence, and export system from becoming accidentally entangled later.

### What real behavior it enables

A contributor will be able to clone the repository, follow documented setup, launch the minimal shell, run all foundation checks, and understand where future UI, workflow, execution, experiment, and export responsibilities belong.

### How we will know it works

An independent validation pass will reproduce setup from a clean environment, execute the documented checks, launch the shell, verify dependency and license reporting, and confirm that no Phase 1+ product semantics were smuggled into the foundation.

---

## 3. Observed Repository and Environment Baseline

The following facts were observed at the start of Phase 0 planning on 2026-09-17. They are not technology selections.

### Repository facts

- Workspace: `C:\Users\seanv\OneDrive\Documents\ViDAP`.
- Git repository: present.
- Current branch: `main`, tracking `origin/main`.
- Remote: `https://github.com/Sean-V-Dev/ViDAP.git`.
- Start-of-planning worktree state: clean.
- Start-of-planning commit: `ed68c32` (`Roadmap`).
- Tracked content: `ViDAP_Overview.txt`, `ViDAP_Phased_Plan_Spine.md`, and `ViDAP_Roadmap.md`.
- No application source, project manifest, lockfile, automated tests, CI configuration, root README, MIT license file, contribution guide, fixture directory, or architecture decision record was present.

### Local tool facts

- Windows PowerShell 5.1 is the active shell.
- Git 2.51.0 for Windows is available.
- Node.js v25.0.0 is available locally.
- npm 11.6.2 is available through `npm.cmd`.
- PowerShell script policy prevents direct execution of `npm.ps1` in the observed shell.
- The Python launcher reports no installed Python runtimes; the discovered `python.exe` is a WindowsApps launcher entry rather than evidence of a usable project runtime.
- No conclusion has been drawn about which locally installed versions should be supported by the project.

### Baseline implications

1. Phase 0 must treat this as a greenfield application repository with approved planning history.
2. Runtime and package-manager versions must be selected and pinned; ambient machine tools cannot serve as the project contract.
3. Setup and task commands must work under the supported Windows shell path or document a deliberate alternative.
4. Generated environments, caches, artifacts, datasets, and secrets must be excluded from Git and kept safe under a synced workspace.
5. Any broader operating-system promise must be explicitly chosen and validated rather than inferred from the current Windows workstation.

---

## 4. Phase Goals and Exclusions

### Goals

P0-G1. Select and record the smallest viable application architecture for a local-first visual frontend and real Python-based data/ML execution.

P0-G2. Establish explicit logical boundaries for UI, workflow/schema, execution, experiment/state, and export code, even where Phase 0 implements only empty or minimal shells.

P0-G3. Establish supported runtime versions, package managers, lockfiles, and setup commands without relying on global mutable state.

P0-G4. Establish real test, formatting, linting, and type-checking entry points appropriate to the selected stack.

P0-G5. Establish continuous integration that exercises the same authoritative checks contributors run locally.

P0-G6. Establish the MIT license, dependency inventory, license-compatibility process, update policy, and basic supply-chain controls.

P0-G7. Establish lightweight contribution, decision-record, documentation, fixture, secret-handling, and generated-artifact conventions.

P0-G8. Deliver a minimal runnable shell proving the selected components can start, communicate only as needed, and be tested together.

P0-G9. Produce sufficient independent evidence for Central to reconcile Phase 0 and open detailed Phase 1 planning.

### Explicit exclusions

Phase 0 does not deliver:

- a functional node graph or node registry;
- workflow schema or typed connections;
- real dataset loading or profiling;
- data transformations, model training, metrics, or experiments;
- notebook or Python export;
- AutoML, agent control, neural-network support, or scientific-data support;
- production deployment, cloud services, authentication, telemetry, analytics, or update services;
- desktop installers unless the approved architecture decision proves an installer is necessary to validate the foundation;
- multiple speculative application shells;
- performance optimization beyond preventing an obviously unusable foundation.

---

## 5. Phase 0 Decision Framework

The first implementation-affecting work is decision work. No scaffolding packet may assume a stack before the relevant decision record is accepted.

### D0.1 - Application shape and process boundary

The decision must compare at least the viable families rather than presuppose one:

- local web application with a browser UI and local Python service;
- packaged desktop shell containing a web UI and local Python service;
- Python-first application/UI approach capable of meeting the graph-editor and separation requirements;
- another bounded option only if it materially improves the approved criteria.

Mandatory criteria:

- direct, testable integration with established Python data/ML libraries;
- a capable interactive node-graph editing path;
- strict separation between visual state and executable semantics;
- local-first operation with no required hosted service;
- deterministic workflow execution and future notebook export compatibility;
- Windows development viability and a documented cross-platform posture;
- automated testing across process and language boundaries;
- packaging and contributor complexity proportional to an open-source playground;
- accessibility and error-presentation feasibility;
- dependency health, licensing, maintenance, and supply-chain exposure.

A small time-boxed feasibility spike may be proposed only where documented evidence cannot resolve a material uncertainty. Spike output is evidence, not production architecture, unless a later packet explicitly adopts it.

### D0.2 - Repository topology and ownership boundaries

The decision must define where the following logical responsibilities live without implementing their later semantics:

- UI/visual graph;
- workflow/schema and shared contracts;
- execution integration;
- experiment/state;
- export;
- shared test fixtures and acceptance assets;
- documentation and decision records.

The topology must make ownership and dependency direction clear. It must not require separate repositories, services, or deployable infrastructure unless the application-shape decision demonstrates a present need.

### D0.3 - Runtime and package management

The decision must select:

- supported Python version and environment/package tool;
- supported JavaScript/TypeScript runtime and package manager if applicable;
- version-pinning files and lockfile policy;
- authoritative local task commands;
- policy for global prerequisites versus repository-managed tooling;
- initial supported development platform and cross-platform verification posture.

Selection is based on project compatibility and maintained releases, not merely the versions installed on the planning workstation.

### D0.4 - Quality and test layers

The decision must define which tools provide:

- formatting;
- linting;
- static/type checking;
- unit testing;
- process/integration smoke testing;
- clean-setup verification;
- dependency and license reporting.

Every tool must have a real Phase 0 target. Empty test suites or ornamental checks do not satisfy the phase.

### D0.5 - CI and branch expectations

The decision must define the checks expected for proposed changes, supported runner environment, cache safety, artifact retention, and the relationship between local and CI task entry points. It must not assume access to paid or organization-only services.

### D0.6 - Dependency, license, and update policy

The decision must define allowed dependency licenses, review of transitive dependencies, lockfile ownership, update cadence, vulnerability-response expectations, and evidence needed before later ML libraries are added. The project remains MIT-licensed.

### D0.7 - Controlled fixture policy

The decision must define fixture provenance, permitted licenses, size bounds, expected-result documentation, sensitive-data prohibition, storage location, and when generated fixtures are preferable. Phase 0 requires only a tiny fixture sufficient to prove the harness; Titanic acquisition is deferred to P4.

---

## 6. Workstreams and Dependencies

| Workstream | Purpose | Depends on | Required outputs |
|---|---|---|---|
| WS0.1 Baseline and decisions | Convert observed facts and open choices into approved records | Approved Phase 0 plan | Baseline record and accepted D0.1-D0.7 decisions |
| WS0.2 Repository governance | Establish the minimal open-source and contribution contract | WS0.1 where stack-specific | MIT license, root guidance, contribution rules, decision-record convention, ignore/line-ending/editor rules |
| WS0.3 Reproducible project scaffold | Create the selected topology and pinned environment | D0.1-D0.3 | Manifests, lockfiles, version pins, directory boundaries, documented setup and task entry points |
| WS0.4 Quality and testing | Make foundation correctness executable | WS0.3 and D0.4 | Format, lint, type, unit, integration/smoke, and clean-setup checks |
| WS0.5 CI and dependency controls | Reproduce authoritative checks and report dependency risk | WS0.3-WS0.4 and D0.5-D0.6 | CI workflow, dependency inventory, license report/check, update and secret-handling rules |
| WS0.6 Fixtures and minimal shell | Prove the selected components work without adding product semantics | WS0.3-WS0.5 and D0.7 | Tiny controlled fixture, minimal application shell, startup/communication smoke test |
| WS0.7 Validation and closeout | Independently reproduce and reconcile the phase | WS0.2-WS0.6 | Validation record, limitations, deferred items, and Central reconciliation |

WS0.2 documentation that is independent of stack choice may proceed alongside decision work only if the execution packets have non-overlapping file ownership and a shared review gate.

---

## 7. Required Phase Deliverables

The exact paths for stack-dependent files are chosen by the approved topology decision. Phase 0 must nevertheless deliver these artifacts or equivalent approved forms:

1. **Architecture decision set:** Application shape, topology, runtimes, package managers, quality layers, CI, dependency/license controls, and fixture policy.
2. **Open-source baseline:** MIT `LICENSE`, project `README`, contribution guidance, and proportionate security/reporting guidance.
3. **Repository hygiene:** Ignore rules, line-ending policy, editor defaults, generated-artifact locations, and secret-handling rules.
4. **Pinned project environments:** Runtime declarations, manifests, lockfiles, and reproducible install/setup instructions.
5. **Logical component shells:** Clear locations and dependency direction for future UI, workflow/schema, execution, experiment/state, and export responsibilities.
6. **Authoritative task entry points:** Setup, format check, lint, type check, test, build, launch, dependency inventory, and license verification as applicable.
7. **Automated test foundation:** At least one meaningful test at each adopted Phase 0 test layer.
8. **Continuous integration:** A clean runner executes the authoritative checks without relying on workstation state.
9. **Dependency evidence:** Direct/transitive dependency inventory and license evidence with failures for disallowed or unknown cases under the accepted policy.
10. **Controlled fixture baseline:** A tiny permitted fixture and documented expected use, with no personal or sensitive data.
11. **Minimal runnable shell:** A recognizable ViDAP shell that proves selected components build, launch, and communicate only as required, while containing no Phase 1+ product claims.
12. **Phase evidence bundle:** Commands, results, environment notes, known limitations, validation findings, and deferrals sufficient for reconciliation.

---

## 8. Proposed Execution-Packet Sequence

These packet definitions are proposals. Approval of this plan does not approve any packet.

### P0-EP01 - Baseline and Architecture Decision

**Objective:** Confirm the repository/environment baseline, evaluate viable application shapes, and accept D0.1-D0.3.

**Outputs:** Controlled baseline record; comparison matrix; application-shape, topology, runtime, and package-management decision records; identified feasibility spikes if genuinely required.

**Acceptance evidence:** Each mandatory criterion is addressed; rejected options and tradeoffs are recorded; no unapproved production scaffold is introduced; downstream packets have a stable boundary and prerequisite list.

### P0-EP02 - Quality, CI, Dependency, and Fixture Decisions

**Objective:** Resolve D0.4-D0.7 before tools and policies are installed into the repository.

**Depends on:** P0-EP01.

**Outputs:** Accepted decisions for quality/test layers, CI, dependency/license/update controls, and fixtures.

**Acceptance evidence:** Every selected check has a Phase 0 purpose, can run locally and in the intended CI environment, and remains proportionate to project risk.

### P0-EP03 - Open-Source and Repository Baseline

**Objective:** Establish the non-application repository contract.

**Depends on:** P0-EP01 and the policy portions of P0-EP02.

**Outputs:** MIT license, root documentation, contribution and reporting guidance, decision-record area, ignore/line-ending/editor rules, and documented generated/local-state locations.

**Acceptance evidence:** A reviewer can identify project purpose, authority documents, setup prerequisites, contribution expectations, license, reporting route, and files that must not enter version control.

### P0-EP04 - Reproducible Project Scaffold

**Objective:** Implement the accepted repository topology and pinned environments without product behavior.

**Depends on:** P0-EP01 through P0-EP03.

**Outputs:** Component directories, manifests, lockfiles, runtime pins, shared task entry points, and minimal setup/build configuration.

**Acceptance evidence:** A clean checkout can install using only documented prerequisites; repeated installs honor lockfiles; component dependency direction matches the accepted decision; no alternate package-manager state is committed.

### P0-EP05 - Quality and Test Harness

**Objective:** Make foundation quality checks executable and meaningful.

**Depends on:** P0-EP04.

**Outputs:** Formatter/linter/type-check/test configuration and meaningful foundation tests at the accepted layers.

**Acceptance evidence:** Authoritative commands succeed on the baseline, intentionally detected violations fail clearly, and tests exercise real foundation behavior rather than empty placeholders.

### P0-EP06 - CI, Dependency, and License Controls

**Objective:** Reproduce local gates in automation and expose dependency/license state.

**Depends on:** P0-EP04 and P0-EP05.

**Outputs:** CI workflow; dependency inventory; license verification; cache rules; documented update and vulnerability-response path.

**Acceptance evidence:** A clean CI-equivalent run executes the same authoritative gates; cache keys include relevant lock state; dependency/license output is reviewable; disallowed or unresolved license cases fail under the accepted policy.

### P0-EP07 - Controlled Fixture and Minimal Runnable Shell

**Objective:** Prove the selected components work together without implementing Phase 1 semantics.

**Depends on:** P0-EP04 through P0-EP06.

**Outputs:** Tiny controlled fixture, recognizable application shell, minimal cross-boundary health/status behavior if the architecture contains multiple processes, and smoke tests.

**Acceptance evidence:** The documented launch path works; the shell identifies itself and reports actionable startup failures; the smoke test uses the accepted boundaries; the fixture has provenance and no sensitive data; no workflow/node/model behavior is claimed.

### P0-EP08 - Fresh-Environment Validation and Reconciliation

**Objective:** Independently determine whether Phase 0 is complete.

**Depends on:** P0-EP03 through P0-EP07.

**Outputs:** Validation report, command/evidence manifest, defect list, limitations, deferrals, and Central reconciliation recommendation.

**Acceptance evidence:** A clean environment reproduces setup, all checks, build, and launch; documentation matches reality; dependency/license evidence is current; the repository contains no secrets or generated local state; P0 exclusions remain intact.

Packets may be split further if an approval unit becomes too broad, but they may not be merged in a way that lets scaffolding precede the architecture decisions or lets the implementer self-accept the completed phase.

---

## 9. Test and Validation Strategy

### Automated foundation checks

The selected stack must provide authoritative commands for the applicable checks:

- formatting conformance;
- linting;
- static/type checking;
- unit tests for configuration and component-shell behavior;
- build/package checks;
- application startup and shutdown smoke tests;
- minimal process-boundary health test if multiple processes are selected;
- dependency inventory and license-policy verification;
- detection of accidentally committed secrets or generated local-state paths, using a proportionate approach.

### Reproducibility checks

- Setup begins from a clean checkout with documented prerequisites only.
- Runtime and package versions resolve from repository declarations.
- Locked installs are used in validation and CI.
- Local and CI entry points invoke the same underlying tasks.
- Tests do not depend on prior caches, OneDrive-only state, user-specific absolute paths, or undeclared environment variables.
- Temporary outputs are isolated and removed or ignored according to policy.

### Independent validation

The validation pass must be performed separately from the implementation claim and must inspect:

- conformity to all accepted decision records;
- fresh setup and launch behavior;
- negative/failure behavior, not just the happy path;
- repository cleanliness after checks run;
- license and dependency evidence;
- documentation accuracy;
- absence of Phase 1+ behavior and unnecessary infrastructure.

---

## 10. Phase Acceptance Criteria

Central may recommend Phase 0 completion only when all of the following are true:

- P0-AC01: D0.1-D0.7 are accepted and represented by durable decision records.
- P0-AC02: The repository contains an MIT license and concise contributor-facing project guidance.
- P0-AC03: Supported runtimes and package managers are explicitly versioned; dependency resolution is locked.
- P0-AC04: A clean checkout can follow documented setup without undocumented global tools or manual file edits.
- P0-AC05: The minimal shell builds and launches through documented commands and exposes actionable startup failure information.
- P0-AC06: UI, workflow/schema, execution, experiment/state, and export responsibilities have explicit locations and dependency direction without implementing future semantics.
- P0-AC07: Formatting, linting, type/static checking, tests, and build checks pass as applicable to the accepted stack.
- P0-AC08: CI or an approved CI-equivalent clean-run validation executes the same authoritative gates.
- P0-AC09: Dependency inventory and license verification are current, reviewable, and compatible with the MIT project policy.
- P0-AC10: The controlled fixture is permitted, documented, small, deterministic where applicable, and free of unnecessary sensitive information.
- P0-AC11: Running setup, tests, and the shell does not dirty the repository with caches, secrets, environments, or build artifacts.
- P0-AC12: Independent validation has no unresolved critical finding and all lesser findings are resolved or explicitly accepted/deferred.
- P0-AC13: Central has reconciled evidence against the spine, roadmap, OV Sections 9, 18, 20-23, and 25-30.

Passing checks on the original workstation alone does not satisfy Phase 0.

---

## 11. Guardrails Specific to Phase 0

1. **Decision before scaffold:** Application and runtime choices require accepted evidence before production structure is created.
2. **No ambient-runtime contract:** Installed Node, npm, Git, or missing Python state does not determine supported project versions.
3. **No system mutation by implication:** Installing system runtimes, changing PowerShell execution policy, adding global packages, containers, or IDE extensions requires explicit packet scope and any necessary user approval.
4. **One authoritative tool per role:** Do not commit competing package managers, formatters, test runners, or task paths without a documented reason.
5. **Lock dependencies:** Reproducibility and CI must use accepted lockfiles rather than floating installs.
6. **No secret material:** Credentials, tokens, local absolute paths, and user data must not enter source, fixtures, logs, snapshots, or evidence.
7. **Synced-workspace safety:** Environments, caches, datasets, databases, build output, and transient artifacts must be isolated and ignored so OneDrive synchronization does not become application state.
8. **No hollow quality gates:** A passing empty test suite or check that skips its intended targets is a failure.
9. **No premature product semantics:** Names and interfaces may reserve logical boundaries, but Phase 0 must not invent workflow, node, execution, experiment, or export contracts owned by later phases.
10. **No deployment theater:** Production hosting, cloud resources, installer pipelines, telemetry, and release automation remain out of scope unless strictly required by an approved Phase 0 acceptance criterion.
11. **Cross-platform honesty:** Only environments actually tested may be claimed as supported; architectural portability is not the same as validated support.
12. **Recoverable changes:** Packets should produce reviewable commits or equivalent bounded diffs and avoid destructive history operations.
13. **Evidence over convention:** A tool or structure is included because it satisfies an approved criterion, not merely because it is common in template repositories.
14. **No independent scope expansion:** Discoveries that affect later phase outcomes return to Central as clarification, dependency change, defect, or scope proposal.

---

## 12. Known Risks and Planned Controls

| Risk | Control in Phase 0 | Escalation condition |
|---|---|---|
| Frontend convenience dictates runtime semantics | D0.1-D0.2 criteria and logical dependency direction | Viable UI option requires workflow or execution truth to live in the frontend |
| Python/JavaScript boundary creates excessive setup or packaging cost | Compare process shapes and permit a bounded feasibility spike | No candidate meets local usability and testing criteria proportionately |
| Local newest tools hide unsupported-version problems | Explicit version support and clean validation | Locked supported versions cannot reproduce required behavior |
| PowerShell policy breaks documented commands | Use compatible entry points or documented shell strategy | Setup requires weakening system policy or undocumented workarounds |
| Synced workspace causes state, cache, or locking problems | Ignore/isolate generated and mutable local state | Required application state cannot be safely separated from the repository |
| CI and local checks diverge | Shared authoritative task entry points | Hosted runner cannot exercise the accepted local workflow |
| Dependency/license tooling reports incomplete information | Direct/transitive inventory validation and unknown-license failure policy | Required dependency cannot be evaluated or conflicts with project licensing |
| Foundation becomes an overbuilt platform | Packet exclusions and P0 acceptance review | A proposed component exists only for unapproved future scope |
| Minimal shell is mistaken for product functionality | Explicit labeling and no workflow claims | Demo implies data-science behavior not actually implemented |

---

## 13. Evidence and Reconciliation Record

Each execution packet must return a compact evidence entry containing:

- packet identifier and approved objective;
- commit or bounded diff reference;
- commands run and their results;
- relevant environment/runtime versions;
- acceptance criteria satisfied;
- tests added or changed;
- dependency/license changes;
- known limitations and unresolved findings;
- deviations from the packet and their approval status;
- independent reviewer conclusion where required.

Phase closeout must consolidate these entries without copying logs into the roadmap. The roadmap should link to accepted evidence and change P0 to `Complete` only after Central reconciliation.

---

## 14. Readiness Review for Phase 0 Execution

Phase 0 is ready for its first execution packet only when:

- this plan is approved;
- P0-EP01 is drafted with bounded outputs and explicit exclusions;
- the decision comparison criteria are accepted;
- any research requiring network access or installation is explicitly identified;
- the packet preserves the current approved planning documents;
- the worker and validator roles are distinct at the acceptance boundary;
- no later-phase product decision is embedded in the packet.

---

## 15. Transition to Phase 1 Planning

Phase 1 planning remains closed until Phase 0 completion evidence is independently validated and reconciled. The Phase 0 closeout must hand Phase 1 at least:

- the accepted application and repository topology;
- supported runtime and tooling contracts;
- the logical ownership boundary for workflow/schema code;
- authoritative quality and CI commands;
- dependency/license rules;
- controlled-fixture conventions;
- known limitations that constrain workflow-format decisions.

Phase 0 may not define the workflow schema on Phase 1's behalf.

---

## 16. Next Action

P0-EP01 through P0-EP06 are complete. D0.1-D0.7, the open-source/repository baseline, reproducible scaffold, quality/test harness, and CI/dependency/license controls are accepted in their respective Central reconciliation records. P0-EP05 version 0.1 was blocked before implementation by a frontend quality-tool peer-compatibility conflict; decision record 0001 selected a maintained peer-compatible TypeScript 6.x line and deferred JSX-a11y, and P0-EP05 version 0.2 was accepted after independent validation. P0-EP06 version 0.4 was accepted after locked local controls, a green user-authorized Windows hosted run, independent validation, and Central reconciliation. P0-EP07 is now ready to draft as a separate bounded packet. Fixtures, shell startup, product implementation, and remote changes remain unauthorized until that packet receives its own explicit approval.
