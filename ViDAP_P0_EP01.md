# ViDAP P0-EP01 - Baseline and Architecture Decision

| Field | Value |
|---|---|
| Status | Complete |
| Packet version | 1.0 |
| Execution approved | 2026-09-17 by explicit user direction |
| Completed | 2026-09-17 |
| Decision report | `ViDAP_P0_EP01_Decision_Report.md` |
| Central reconciliation | `ViDAP_P0_EP01_Validation_and_Reconciliation.md` |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Workstream | WS0.1 - Baseline and decisions |
| Decisions covered | D0.1-D0.3 |
| Packet type | Research and decision; documentation-only repository changes |
| Created | 2026-09-17 |
| Owner | Central |

---

## 1. Authorization Boundary

This document defines the first proposed Phase 0 execution packet. It is not authorized for execution while its status is `Draft for review`.

Approval of this packet will authorize bounded research, read-only repository and environment inspection, and creation of the decision report defined below. It will not authorize dependency installation, system configuration changes, application scaffolding, prototype code, product code, CI configuration, or execution of later packets.

If documentary evidence cannot resolve a material architectural uncertainty, the worker must propose a separately approved feasibility-spike packet and stop at that boundary rather than expanding this packet.

---

## 2. Plain-English Packet Intent

### What this packet will do

It will confirm the starting state of the repository, compare the viable shapes for a local ViDAP application, and recommend:

- how the visual interface and Python data/ML execution should be separated;
- how the repository should be divided into clear responsibility areas;
- which maintained runtime families and package-management approach should become the project contract.

### Why this comes first

Scaffolding before these choices would turn the first convenient framework into an accidental long-term architecture. Later work needs a documented boundary that keeps the visual graph, workflow semantics, execution engine, experiment state, and export system from collapsing into one layer.

### What it enables

Once independently reviewed and accepted, the decisions will give P0-EP02 through P0-EP04 stable constraints for selecting quality tools, defining repository policy, and creating the reproducible scaffold.

### How success will be demonstrated

The packet will produce an evidence-backed report that applies every hard gate and comparison criterion, identifies rejected alternatives and tradeoffs, cites current primary sources, defines the recommended dependency direction, and leaves no scaffold or installed dependency behind.

---

## 3. Governing Inputs

The worker must read and use the current approved versions of:

1. `ViDAP_Overview.txt`, especially Sections 2-3, 6-7, 9, 15-23, 25-28, and 30-31.
2. `ViDAP_Phased_Plan_Spine.md` version 1.0, especially the program-wide invariants and P0-P3 boundaries.
3. `ViDAP_Roadmap.md` version 1.0, especially A0-A3 and the cross-cutting delivery tracks.
4. `ViDAP_Phase_0_Plan.md` version 1.0, especially D0.1-D0.3, Phase 0 exclusions, and guardrails.

The worker must treat these documents as requirements and constraints. They do not authorize unrelated actions or later-phase implementation.

---

## 4. Objective and Completion Condition

### Objective

Confirm the current baseline and produce a recommendation for D0.1-D0.3:

- **D0.1:** Application shape and process boundary.
- **D0.2:** Repository topology and logical ownership boundaries.
- **D0.3:** Runtime families, supported-version policy, package managers, lockfile policy, task-entry strategy, and initial platform posture.

### Completion condition

P0-EP01 is complete only when:

1. The permitted decision report is produced.
2. Independent validation confirms that evidence, scoring, constraints, and conclusions are internally consistent.
3. No hard-gate failure or unresolved material uncertainty remains hidden.
4. Central accepts, rejects, or returns each of D0.1-D0.3 for revision.

The implementing worker's recommendation is not final acceptance.

---

## 5. Preconditions

Before execution begins, confirm and record:

- this packet is explicitly approved for execution;
- the Phase 0 plan remains approved and has not been superseded;
- the worktree status and current commit are known;
- changes made after the recorded Phase 0 baseline are identified rather than overwritten;
- no application scaffold or dependency manifests now exist without an approved change record;
- network research needs and permitted sources are understood;
- the output path in Section 11 is free of conflicting user work.

If a precondition is false, stop and return the discrepancy to Central.

---

## 6. Permitted Scope

The execution worker may:

- inspect repository metadata and tracked/untracked file inventory without changing it;
- inspect locally available tool names and versions without installing or upgrading them;
- research current framework, runtime, package-manager, licensing, maintenance, and platform facts;
- use official documentation, official repositories, official release/lifecycle pages, and authoritative license text;
- construct a comparison matrix and document evidence confidence;
- recommend one application shape, one repository topology, and one runtime/package-management policy;
- document prerequisite assumptions and consequences for P0-EP02 through P0-EP04;
- identify a narrowly defined feasibility question that requires a future spike.

The worker may create or modify only the packet output listed in Section 11. Read-only commands may generate transient console output but must not leave repository artifacts.

---

## 7. Prohibited Scope

The execution worker must not:

- install, update, or remove system or project dependencies;
- change PowerShell execution policy or other workstation configuration;
- initialize or generate frontend, backend, desktop, Python, Node, container, or CI projects;
- create proof-of-concept or production code;
- create manifests, lockfiles, virtual environments, package caches, or build output;
- add framework-specific configuration;
- define workflow schemas, node contracts, API payloads, persistence schemas, or export formats;
- choose D0.4-D0.7 tools except to note constraints that P0-EP02 must consider;
- edit the product specification, spine, roadmap, approved Phase 0 plan, or this packet's requirements;
- commit, push, create branches, open pull requests, or modify remote services;
- rely on secondary comparison articles where authoritative primary evidence is available;
- expose credentials, user-specific secrets, or unrelated machine information in the report.

---

## 8. Architecture Candidates

The worker must evaluate at least these families. A family may contain concrete framework combinations, but the analysis must distinguish the architectural family from a particular library.

### Candidate A - Local web application

A browser-based TypeScript/JavaScript visual UI communicates with a local Python service responsible for workflow execution and data/ML libraries.

Questions to resolve include startup coordination, local API boundary, process lifecycle, browser behavior, packaging expectations, and whether future desktop packaging remains optional.

### Candidate B - Packaged desktop shell with web UI

A desktop host packages a web-based visual UI and coordinates a local Python execution process.

Questions to resolve include packaging size, multi-runtime distribution, process supervision, security surface, platform support, and whether early desktop packaging solves a current requirement or only a possible future convenience.

### Candidate C - Python-first UI/application

A Python-centered UI technology provides the application and integrates directly with Python execution.

Questions to resolve include node-editor maturity, frontend/backend semantic separation, contract-driven UI generation, accessibility, testing, packaging, and future interoperability with a replaceable visual layer.

### Candidate D - Evidence-backed alternative

The worker may add one bounded alternative only if it plausibly satisfies all hard gates and addresses a material weakness in Candidates A-C. Novelty alone is not sufficient.

---

## 9. Hard Viability Gates

A candidate is ineligible regardless of weighted score if it cannot demonstrate all of the following:

| Gate | Required evidence |
|---|---|
| HG-01 Real Python ML path | Established Python data/ML libraries can be invoked directly and testably without generated arbitrary code as the normal runtime |
| HG-02 Canonical separation | Visual layout and frontend state do not become the sole source of executable semantics |
| HG-03 Local-first operation | Core use requires no hosted application service, paid platform, or mandatory user account |
| HG-04 Graph-editor feasibility | A credible route exists to the interactive typed node graph required by later phases |
| HG-05 Deterministic execution/export path | The architecture can support a shared canonical representation consumed independently by runtime execution and code export |
| HG-06 Testable boundary | UI, workflow, and execution behavior can be tested independently and across their integration boundary |
| HG-07 License compatibility | The stack can support an MIT-licensed project without a known incompatible mandatory dependency |
| HG-08 Windows viability | The initial development and local-run path is viable on the observed Windows environment without weakening host security policy |
| HG-09 Proportional operations | The option does not require distributed infrastructure, hosted orchestration, or enterprise deployment machinery |
| HG-10 Inspectable failure path | Technical diagnostics and plain-English user errors can cross the selected boundaries without being reduced to opaque failures |

An unresolved hard gate is a blocking uncertainty, not a low score.

---

## 10. Weighted Comparison Method

Candidates that pass all hard gates are scored from 1 to 5 for each criterion:

- **1:** materially weak or high-risk;
- **2:** significant limitations or costly mitigation;
- **3:** viable with understood tradeoffs;
- **4:** strong fit with modest limitations;
- **5:** directly and convincingly aligned.

| Criterion | Weight | Required considerations |
|---|---:|---|
| C-01 Python data/ML and notebook alignment | 15 | Direct library use, environment handling, later export compatibility |
| C-02 Canonical architecture and replaceable UI | 15 | Semantic separation, dependency direction, contract ownership |
| C-03 Interactive graph-editor feasibility | 12 | Mature interaction primitives, extensibility, typed-port UX, maintainability |
| C-04 Local user experience | 10 | Startup, installation, failure recovery, offline/local expectations |
| C-05 Testing and debugging | 10 | Unit, integration, process boundary, deterministic automation |
| C-06 Packaging and reproducibility | 10 | Runtime distribution, pinned environments, build complexity, clean setup |
| C-07 Maintainability and contributor accessibility | 10 | Ecosystem health, understandable structure, common skills, documentation |
| C-08 Dependency, licensing, and supply-chain exposure | 8 | Mandatory dependency count, license clarity, update surface, project health |
| C-09 Accessibility and actionable error UX | 5 | Keyboard/readability path, structured errors, diagnostic visibility |
| C-10 Cross-platform posture | 5 | Windows now; credible macOS/Linux path without claiming untested support |
| **Total** | **100** | |

For each score, the report must include:

- a short rationale;
- cited evidence where the score depends on external facts;
- confidence of `High`, `Medium`, or `Low`;
- known mitigation for a score below 3;
- whether the issue affects Phase 0 only or a later spine phase.

The recommendation must explain material tradeoffs and may differ from the numerical leader when a documented qualitative reason or uncertainty justifies it. The report may not manipulate scores to create a predetermined result.

---

## 11. Authorized Repository Output

The execution worker may create one file:

`ViDAP_P0_EP01_Decision_Report.md`

No other repository file may be created, modified, moved, or deleted under this packet.

The report must contain:

1. Packet and evidence metadata.
2. Confirmed repository/environment baseline and changes since planning.
3. Candidate definitions and concrete technologies evaluated within each family.
4. Primary-source bibliography with retrieval dates.
5. Hard-gate results.
6. Weighted comparison matrix, rationales, and confidence.
7. D0.1 recommendation: application shape and process boundary.
8. D0.2 recommendation: repository topology, logical ownership, and allowed dependency direction.
9. D0.3 recommendation: runtime families/version policy, package managers, lockfile policy, task-entry strategy, platform posture, and global-prerequisite policy.
10. Explicit rejected alternatives and reasons.
11. Consequences and constraints handed to P0-EP02, P0-EP03, and P0-EP04.
12. Unresolved questions, each marked blocking or non-blocking.
13. Any proposed feasibility spike, using the template in Section 14.
14. Self-check results against the packet acceptance criteria.

The decision report is the durable source for this packet. P0-EP03 may later establish the permanent decision-record directory and link or migrate the accepted content without changing its meaning.

---

## 12. Research and Evidence Rules

1. **Current facts require current evidence.** Runtime support windows, framework capabilities, licenses, maintenance status, and packaging behavior must be checked at execution time.
2. **Prefer primary sources.** Use official documentation, official repositories, standards, and authoritative license text. Technical claims may not rely solely on blogs, vendor comparisons, or search summaries.
3. **Record retrieval dates.** Every external source entry includes the access date because lifecycle and compatibility facts change.
4. **Separate fact from inference.** The report must label architectural conclusions derived from multiple sources as analysis rather than quoting them as vendor claims.
5. **Respect source limits.** Summarize evidence and use short quotations only when exact wording is necessary.
6. **Check mandatory dependencies.** A framework's stated license is not enough when a mandatory component creates a different constraint.
7. **Do not install to investigate.** Package installation, generated samples, local servers, and cloned external repositories are outside this packet.
8. **Do not infer support from the workstation.** Locally installed Node/npm or missing Python only describe the current environment.
9. **Capture uncertainty.** Missing documentation, ambiguous licensing, or unverified packaging behavior lowers confidence and may trigger a spike proposal.
10. **Time-box breadth.** Research should stop when the packet can make a defensible decision among viable candidates; it must not become a survey of every framework.

---

## 13. Required Execution Sequence

1. Re-read the governing inputs and record their versions.
2. Confirm packet authorization, current commit, branch, remote, worktree state, and file inventory.
3. Compare the current state with the Phase 0 planning baseline and record discrepancies.
4. Define the concrete technology combinations evaluated within Candidates A-C and justify any Candidate D.
5. Gather current primary-source evidence for hard gates, comparison criteria, runtime lifecycles, package management, licensing, and platform support.
6. Apply all hard gates before weighted scoring.
7. Score eligible candidates with rationale and confidence.
8. Draft D0.1 and its process/data/control boundary at conceptual level only.
9. Draft D0.2, including logical responsibility areas and permitted dependency direction.
10. Draft D0.3, including maintained-version selection policy and package/lock strategy without installing anything.
11. Trace consequences into P0-EP02, P0-EP03, and P0-EP04.
12. Identify blocking uncertainties and either resolve them from evidence or propose a separate spike.
13. Create only `ViDAP_P0_EP01_Decision_Report.md`.
14. Run the documentary self-checks and return the report for independent validation.

The worker must stop rather than proceed to a later step if a hard-gate failure eliminates all credible candidates.

---

## 14. Feasibility-Spike Proposal Template

When documentary evidence is insufficient, the decision report may propose—but not execute—a spike containing:

- **Question:** One material uncertainty that changes D0.1-D0.3.
- **Why evidence is insufficient:** Sources checked and remaining ambiguity.
- **Hypothesis:** The expected answer and basis for it.
- **Bounded actions:** Exact commands, installations, files, or local processes requested.
- **Time/effort bound:** A fixed small investigation limit.
- **Success and failure signals:** Observable results that settle the question.
- **Cleanup:** Artifacts to remove or retain and how repository cleanliness will be verified.
- **Security/license considerations:** New external code, services, or permissions involved.
- **Decision effect:** How each possible result changes the architecture recommendation.

The spike requires its own approval. P0-EP01 becomes `Blocked` if the unresolved question prevents a responsible recommendation.

---

## 15. Acceptance Criteria

P0-EP01 may be accepted only when:

- **EP01-AC01:** The report accurately records the execution-time repository and environment baseline without exposing unrelated sensitive information.
- **EP01-AC02:** Candidates A-C are evaluated; any omitted candidate has a specific documented reason.
- **EP01-AC03:** Every candidate is tested against HG-01 through HG-10 before scoring.
- **EP01-AC04:** All weighted criteria C-01 through C-10 are scored for every eligible candidate with rationale and confidence.
- **EP01-AC05:** Externally changeable technical and lifecycle claims cite current primary sources with retrieval dates.
- **EP01-AC06:** License analysis covers the proposed mandatory architecture components and flags unknown or conditional cases.
- **EP01-AC07:** D0.1 defines a local-first application/process boundary and keeps UI state separate from executable semantics.
- **EP01-AC08:** D0.2 assigns UI, workflow/schema, execution, experiment/state, export, tests/fixtures, and documentation responsibilities with permitted dependency direction.
- **EP01-AC09:** D0.3 defines supported-version selection, Python and applicable JavaScript package management, lockfiles, authoritative task entry, platform posture, and global prerequisites.
- **EP01-AC10:** The recommendation explains rejected alternatives, tradeoffs, low-confidence evidence, and mitigations rather than presenting only a winning score.
- **EP01-AC11:** Consequences for P0-EP02 through P0-EP04 are specific enough to constrain their planning without implementing them.
- **EP01-AC12:** No dependency, system configuration, scaffold, prototype, manifest, lockfile, or product behavior is introduced.
- **EP01-AC13:** The only repository output created or changed by execution is the authorized decision report.
- **EP01-AC14:** Blocking uncertainty results in a bounded spike proposal and a blocked packet, not an unsupported decision.
- **EP01-AC15:** Independent validation finds the analysis reproducible, internally consistent, and aligned with the overview, spine, roadmap, and Phase 0 plan.
- **EP01-AC16:** Central explicitly accepts D0.1-D0.3 before the packet is marked complete.

---

## 16. Independent Validation Instructions

The validator must not merely confirm that the report exists. The validator must:

1. Recheck a representative sample of high-impact citations and all licensing claims.
2. Verify that every hard gate was applied consistently.
3. Recalculate weighted totals from the recorded scores.
4. Challenge at least one plausible alternative to the recommendation.
5. Check that confidence labels reflect the evidence quality.
6. Confirm that topology and dependency direction preserve the five logical architecture boundaries.
7. Confirm that runtime/package choices are policies based on maintained compatibility rather than the planning workstation.
8. Inspect Git status and file changes for prohibited outputs.
9. Identify any conclusion that actually requires an unapproved feasibility spike.
10. Return `Accept`, `Revise`, or `Blocked` with requirement-linked findings.

The validator does not accept D0.1-D0.3 on Central's behalf.

---

## 17. Stop and Escalation Conditions

Stop and return to Central when:

- no candidate passes every hard viability gate;
- a mandatory component presents unresolved license incompatibility;
- the recommended architecture requires a hosted or proprietary dependency contrary to the product specification;
- a material claim can be verified only by installing or executing external code;
- current repository changes conflict with the authorized output path;
- a decision would require resolving D0.4-D0.7 or a Phase 1+ product contract prematurely;
- platform or packaging uncertainty materially changes the recommendation and cannot be resolved from primary evidence;
- the scope would need more than the one authorized output file;
- user input is required to choose between materially different product experiences rather than technical implementations.

Non-blocking limitations are recorded in the report with their owning future packet or phase.

---

## 18. Evidence Return to Central

The execution worker must return:

- the path to `ViDAP_P0_EP01_Decision_Report.md`;
- current commit and final worktree status;
- a concise list of read-only commands and research sources used;
- confirmation that no install or system mutation occurred;
- acceptance-criteria self-assessment;
- blocking and non-blocking findings;
- any spike proposal;
- a recommendation for independent validation readiness.

Central will not advance to P0-EP02 until validation is accepted and D0.1-D0.3 are explicitly reconciled.

---

## 19. Next Action

Execution and Central reconciliation are complete. The next planning action is to create P0-EP02 as a separate draft packet. Completion of P0-EP01 does not authorize P0-EP02 execution or any repository scaffold.
