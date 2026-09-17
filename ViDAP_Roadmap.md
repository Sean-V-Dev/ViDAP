# ViDAP Implementation Roadmap

**Status:** Draft for review  
**Version:** 0.1  
**Parent:** `ViDAP_Phased_Plan_Spine.md` version 1.0  
**Product source:** `ViDAP_Overview.txt`  
**Created:** 2026-09-17  
**Owner:** Central  

---

## 1. Purpose and Limits

This roadmap communicates how the approved ViDAP spine advances from project foundation to validated product capabilities. It records milestone order, dependencies, visible demonstrations, architectural checkpoints, validation targets, major decisions, deferrals, and current status.

This roadmap does not:

- replace the product specification or the approved spine;
- define file-level implementation work;
- authorize execution;
- select technologies whose decisions belong to a phase plan;
- promise dates without an evidence-based delivery baseline;
- make later phases prerequisites for demonstrating earlier useful outcomes.

Detailed work is planned one phase at a time. Roadmap changes may clarify sequencing and status, but changes to an approved phase outcome or boundary require a spine change under the approved change-control process.

---

## 2. Current Program State

| Artifact or scope | Status | Evidence or next gate |
|---|---|---|
| Product specification | Governing source | `ViDAP_Overview.txt` |
| Phased Plan Spine | Approved | Version 1.0, approved 2026-09-17 |
| Roadmap | Draft for review | Approval required before Phase 0 planning |
| Phase 0 | Not planned | Blocked on roadmap approval |
| Phases 1-11 | Sequenced only | Remain at roadmap resolution until predecessor reconciliation |
| Execution packets | Not authorized | Require an approved phase plan and separate packet approval |
| Product implementation | Not started | No implementation is authorized by this roadmap |

No percentage-complete values are used. A phase moves state only when its named gate and evidence support the change.

---

## 3. Dependency Model

The default critical path is sequential:

```text
P0 Foundation
  -> P1 Workflow and Contracts
  -> P2 Execution and Runs
  -> P3 Visual Vertical Slice
  -> P4 Data Understanding and Preparation
  -> P5 Baseline Modeling and Evaluation
  -> P6 Experiments and Comparison
  -> P7 Export and Interoperability
  -> P8 Inspectable Automation
  -> P9 Real-World Tabular Validation
  -> P10 Bounded Neural Networks
  -> P11 Scientific Extension Validation
```

This order protects the canonical workflow and deterministic runtime from being shaped around UI convenience, a single model family, or one validation dataset.

Parallel work is allowed only inside an approved phase plan when workstreams have explicit interfaces, separate ownership, compatible file scope, and a shared integration gate. Later phases may receive research or decision preparation when useful, but not detailed implementation planning or execution that assumes unvalidated earlier architecture.

---

## 4. Capability Horizons

These are evidence-based product horizons, not release names or calendar commitments.

| Horizon | Completed phases | Capability reached | Principal proof |
|---|---:|---|---|
| H0 - Foundation Ready | P0 | Contributors can reproduce, build, test, and launch the project shell | Clean-environment setup and CI-equivalent checks |
| H1 - Executable Architecture | P1-P2 | Versioned workflows validate and execute independently of the UI | Deterministic branched headless workflow |
| H2 - Visual Interaction | P3 | A user can build and run a narrow real workflow visually | Saved visual graph and backend execution agree |
| H3 - Useful Baseline Product | P4-P5 | A user can understand data, prepare it, train a real baseline, and interpret results | Titanic reference workflow |
| H4 - Core Experimentation Product | P6-P7 | A user can compare durable experiments and export conventional artifacts | Branch comparison plus independently executable export |
| H5 - Advanced Tabular Product | P8 | Stronger models and optimization remain inspectable and editable | Automated baseline materialized as an editable workflow |
| H6 - Real-World Robustness | P9 | The product survives materially more complex tabular/domain conditions | Approved healthcare scenario |
| H7 - Neural-Network Depth | P10 | A bounded feed-forward network can be visually defined and genuinely trained | Validated nested network workflow |
| H8 - Scientific Generality Assessed | P11 | Claims about non-tabular scientific extensibility have bounded evidence | Approved scientific scenario or validated limitation report |

H3 is the first target that demonstrates the core product promise end to end. H4 is the first target that demonstrates the fuller experimentation and interoperability proposition. Later horizons expand and challenge the product; they are not excuses to postpone usefulness until the end of the roadmap.

---

## 5. Phase Roadmap

### P0 - Project Foundation and Delivery Baseline

- **Depends on:** Approved spine and roadmap.
- **Roadmap contribution:** Establishes the reproducible project boundary, delivery controls, test entry points, and minimal runnable shell.
- **Visible demonstration:** A new environment can follow documented setup, run checks, and launch the shell without undocumented local state.
- **Architectural checkpoint A0:** Application shape, component boundaries, repository organization, supported development environment, and dependency policy are explicit and proportionate.
- **Decisions due in the phase plan:** Application/frontend/backend shape; packaging and local runtime expectations; language/runtime versions; testing layers; CI policy; dependency/license workflow; decision-record format; fixture rules.
- **Status:** Not planned; awaiting roadmap approval.

### P1 - Canonical Workflow and Node Contract Kernel

- **Depends on:** Reconciled P0 evidence.
- **Roadmap contribution:** Creates the open workflow language and node-extension boundary that all later UI, runtime, and export behavior share.
- **Visible demonstration:** Valid, invalid, branched, and versioned example workflows can be inspected and round-tripped; invalid connections explain why they fail.
- **Architectural checkpoint A1:** Workflow semantics are independent of visual layout; typed node contracts and compatibility rules are testable without the UI.
- **Decisions due in the phase plan:** Serialization encoding; schema evolution and migration policy; node identity; type-system depth; contract registration and discovery.
- **Status:** Sequenced; not ready for detailed planning.

### P2 - Deterministic Execution and Run Foundations

- **Depends on:** Reconciled P1 evidence.
- **Roadmap contribution:** Turns validated semantic workflows into ordered execution, recorded runs, and traceable artifacts.
- **Visible demonstration:** A branched workflow executes headlessly in dependency order, reproduces deterministic results where expected, and rejects stale cache reuse.
- **Architectural checkpoint A2:** Runtime dispatch, intermediate representation, run metadata, artifact ownership, caching, and error envelopes remain separate from UI presentation.
- **Decisions due in the phase plan:** Execution isolation; local scheduling model; artifact and metadata persistence; seed policy; cache keys and invalidation; cancellation and failure propagation boundaries.
- **Status:** Sequenced; not ready for detailed planning.

### P3 - First Visual End-to-End Slice

- **Depends on:** Reconciled P2 evidence.
- **Roadmap contribution:** Proves that a visual graph can edit and execute the same canonical workflow without duplicating backend semantics.
- **Visible demonstration:** A user visually assembles, validates, saves, reloads, and executes one deliberately narrow real workflow, including one actionable failure path.
- **Architectural checkpoint A3:** Forms derive from node contracts; connection rules come from workflow types; displayed results come from recorded execution results.
- **Decisions due in the phase plan:** Minimal vertical-slice operations; essential graph interactions; result and error presentation; accessibility baseline; UI/runtime integration contract.
- **Status:** Sequenced; not ready for detailed planning.

### P4 - Data Intake, Profiling, and Preparation

- **Depends on:** Reconciled P3 evidence.
- **Roadmap contribution:** Makes real tabular data understandable and deliberately transformable without silent mutation.
- **Visible demonstration:** Titanic data is loaded, profiled, explicitly prepared, saved, and rerun; a data-quality finding leads to an appropriate corrective node.
- **Architectural checkpoint A4:** Inference is distinguishable from user-approved transformation; column/schema provenance survives each supported operation.
- **Decisions due in the phase plan:** Initial formats and size limits; type inference policy; profiling thresholds; bounded preparation and feature operations; preview and sampling rules; fixture provenance.
- **Status:** Sequenced; not ready for detailed planning.

### P5 - Baseline Supervised Modeling and Evaluation

- **Depends on:** Reconciled P4 evidence.
- **Roadmap contribution:** Delivers the first useful visual data-science product across data, preparation, training, evaluation, and interpretation.
- **Visible demonstration:** An approved Titanic workflow uses real libraries to train and compare at least the approved baseline path, with practical metrics and reproducible outputs.
- **Architectural checkpoint A5:** Target, split, preprocessing, model parameters, and metrics flow through explicit contracts and are verified at the library boundary.
- **Decisions due in the phase plan:** Initial task type or types; model families; split and validation policy; leakage checks; metrics; interpretation rules; model-artifact expectations.
- **Status:** Sequenced; not ready for detailed planning.

### P6 - Experiment Branching, Comparison, and Reasoning

- **Depends on:** Reconciled P5 evidence.
- **Roadmap contribution:** Makes experiments durable, comparable, explainable records of changed hypotheses and outcomes.
- **Visible demonstration:** A user branches a baseline, changes a feature or model parameter, reruns it, sees an accurate configuration/outcome diff, and inspects the earlier state.
- **Architectural checkpoint A6:** Workflow versions, run records, artifacts, hypotheses, and comparisons have clear identities and lineage without duplicating source-of-truth state.
- **Decisions due in the phase plan:** Experiment identity; snapshot and restoration semantics; retention; comparison dimensions; shared-upstream reuse; reasoning-note structure.
- **Status:** Sequenced; not ready for detailed planning.

### P7 - Export and Interoperability

- **Depends on:** Reconciled P6 evidence.
- **Roadmap contribution:** Demonstrates that ViDAP workflows can become readable, conventional data-science artifacts without semantic drift.
- **Visible demonstration:** A supported workflow exports to a structured notebook or script that runs independently and matches application results within approved tolerances.
- **Architectural checkpoint A7:** Runtime execution and code generation are separate consumers of the same canonical workflow or intermediate representation.
- **Decisions due in the phase plan:** Initial export formats; generated document structure; node-to-code traceability; dependency declarations; equivalence tolerances; unsupported-operation behavior.
- **Status:** Sequenced; not ready for detailed planning.

### P8 - Extended Tabular Modeling and Inspectable Automation

- **Depends on:** Reconciled P7 evidence.
- **Roadmap contribution:** Adds stronger modeling and optimization while preserving editable workflows, bounded resources, and visible decisions.
- **Visible demonstration:** An automated baseline or search exposes preprocessing, validation, model families, parameters, and metrics, then materializes a result as an editable graph.
- **Architectural checkpoint A8:** Automation composes approved node contracts and run infrastructure rather than creating a separate opaque execution path.
- **Decisions due in the phase plan:** Boosting libraries; optimizer/AutoML approach; search-space ownership; budgets and cancellation; imbalance handling; grouped/temporal validation subset; ensemble scope.
- **Status:** Sequenced; not ready for detailed planning.

### P9 - Real-World Tabular Robustness

- **Depends on:** Reconciled P8 evidence and an approved, permitted healthcare reference scenario.
- **Roadmap contribution:** Tests whether the product remains correct and understandable with time, grouping, higher cardinality, imbalance, ranking, or multiple related tables.
- **Visible demonstration:** The approved healthcare scenario executes end to end and communicates workload, retention, enrichment, and error tradeoffs in domain-appropriate terms.
- **Architectural checkpoint A9:** Necessary extensions remain general product capabilities rather than hard-coded healthcare behavior; performance and memory limitations are explicit.
- **Decisions due in the phase plan:** Dataset and permissions; privacy controls; entity/time semantics; success scenario; domain review method; required capability subset; local resource envelope.
- **Status:** Sequenced; not ready for detailed planning.

### P10 - Bounded Neural-Network Workflows

- **Depends on:** Reconciled P9 evidence and an approved bounded network representation.
- **Roadmap contribution:** Extends the workflow abstraction to a structured feed-forward network backed by a real neural-network framework.
- **Visible demonstration:** A supported network is assembled, shape-validated, trained, evaluated, saved, and exported; an incompatible layer connection fails actionably.
- **Architectural checkpoint A10:** Nested model structure, training configuration, and framework invocation remain explicit without turning ViDAP into a complete visual framework replacement.
- **Decisions due in the phase plan:** Framework; supported layers and activations; nested-graph representation; shape typing; training controls; reproducibility expectations; export surface.
- **Status:** Sequenced; not ready for detailed planning.

### P11 - Generality and Scientific Extension Validation

- **Depends on:** Reconciled core-product evidence, approved reference access, and explicit compute/storage boundaries.
- **Roadmap contribution:** Tests bounded claims about extending beyond ordinary tabular modeling to an unfamiliar scientific workflow.
- **Visible demonstration:** The approved scientific scenario proves specified extension claims, or yields a validated limitation report and a separately reviewable follow-on proposal.
- **Architectural checkpoint A11:** Domain-specific representations, metrics, and feature handling use intentional extension points without making the core product a universal scientific platform.
- **Decisions due in the phase plan:** Whether CASMI 2026 remains the reference; data/license access; bounded success criteria; compute budget; domain review; specialized representation and metric scope.
- **Status:** Sequenced; not ready for detailed planning.

---

## 6. Validation Dataset Progression

| Validation target | Roadmap use | Earliest phase | Completion evidence |
|---|---|---:|---|
| Small controlled fixtures | Contracts, errors, determinism, regression isolation | P0 | Versioned permitted fixtures with known expected results |
| Narrow integration dataset | First UI-to-runtime vertical slice | P3 | Real backend operation assembled and run through the UI |
| Reference A - Titanic | Data preparation, baseline modeling, comparisons, export, automation | P4-P8 | Increasingly complete end-to-end workflows with direct-library and export parity checks |
| Reference B - Healthcare | Complex tabular/domain robustness | P9 | Approved scenario, domain review, operational interpretation, resource characterization |
| Reference C - Scientific challenge candidate | Non-tabular/scientific extension claims | P11 | Bounded demonstrated claims or a validated limitation report |

Validation datasets prove specific claims; they do not define the product architecture. A dataset cannot be introduced until its provenance, license or terms, storage expectations, and privacy constraints are accepted.

---

## 7. Cross-Cutting Delivery Tracks

These tracks run through every applicable phase but do not become separate feature phases:

| Track | Required continuing evidence |
|---|---|
| Architecture and decisions | Current decision records, explicit boundaries, and no UI/runtime source-of-truth duplication |
| Quality and validation | Automated tests, representative acceptance path, independent review, and regression coverage |
| Reproducibility and provenance | Inputs, workflow version, parameters, seeds, environment-relevant metadata, results, and artifacts |
| Error experience | Plain-English cause/remedy plus preserved technical detail; no silent failure |
| Documentation and interpretation | Setup and behavior documentation plus practical explanations of meaningful results |
| Dependencies and licensing | Current inventory, compatible licenses, maintenance/packaging assessment, and controlled updates |
| Security and data responsibility | Bounded file/data handling, safe defaults, fixture provenance, and no unnecessary sensitive data |
| Performance and resources | Phase-appropriate size envelope, measured bottlenecks, cancellation where needed, and honest limitations |
| Compatibility and migration | Workflow/schema versions, backward-compatibility policy, migration tests where persistence becomes durable |
| Accessibility and usability | Keyboard/readability expectations, understandable validation, and task-based user acceptance appropriate to the phase |

No phase can defer a cross-cutting obligation when omitting it would make the delivered capability materially misleading, irreproducible, unsafe, or unmaintainable.

---

## 8. Requirement Coverage Map

The map identifies planned ownership and validation locations. It does not narrow the original requirement text.

| Overview requirement | Primary roadmap home | Coverage disposition |
|---|---|---|
| OV Section 1 - Purpose | P3-P11 | Demonstrated incrementally through useful real workflows |
| OV Section 2 - Product Goal | P3, P5, P8, P10 | Real computation and editable graphs demonstrated at increasing depth |
| OV Section 3 - Product Philosophy | P1-P10 | Program invariant; visible in contracts, automation, experiments, and export |
| OV Section 4 - Intended Users | P3-P10 | UX and interpretation acceptance criteria; revisited with domain validation |
| OV Section 5 - Core Workflow | P3-P8 | Narrow slice first, then full baseline, comparison, and export loop |
| OV Section 6 - Node System | P1, P3-P5, P8, P10-P11 | Contract kernel followed by progressively broader node families |
| OV Section 7 - Typed Connections | P1, P3-P5, P10 | Defined in kernel and validated in real workflows and nested models |
| OV Section 8 - Dataset Profiling | P4, P9, P11 | Tabular baseline, complex-domain expansion, scientific reassessment |
| OV Section 9 - Real Modeling Backends | P0, P5, P8, P10 | Dependency control plus verified backend integrations |
| OV Section 10 - Neural-Network Support | P10 | Explicit bounded implementation phase |
| OV Section 11 - AutoML | P8 | Inspectable automation producing editable workflows |
| OV Section 12 - Experiment System | P2, P6, P8-P9 | Run foundation, comparison UX, automation and domain validation |
| OV Section 13 - Results and Interpretation | P5-P6, P8-P9 | Baseline metrics, comparisons, automation, operational meaning |
| OV Section 14 - Hypothesis and Reasoning | P6 | Durable optional reasoning attached to experiments |
| OV Section 15 - Export and Interoperability | P7, P10 | Canonical export, followed by supported neural-network export |
| OV Section 16 - Workflow Format | P1, P7 | Open versioned format and downstream export traceability |
| OV Section 17 - Agent Compatibility | P1 architecture; post-core decision | Structured operations preserved; human-visible agent control remains explicitly deferred |
| OV Section 18 - Testing and Quality | P0-P11 | Cross-cutting delivery gate in every phase |
| OV Section 19 - Error Handling | P2-P5, then cross-cutting | Runtime envelope first; actionable UI and domain failures thereafter |
| OV Section 20 - Plain-English Planning | All planning and delivery artifacts | Mandatory approval and interpretation standard |
| OV Section 21 - Engineering Principles | P0-P11 | Program-wide invariants and phase acceptance criteria |
| OV Section 22 - Architecture Expectations | P0-P3, reinforced P6-P7 | Boundaries established before broad feature development |
| OV Section 22A - Canonical Execution Model | P1-P3, P7 | Workflow, IR, execution, UI, and export separation proven |
| OV Section 23 - Initial Non-Goals | P0-P11 | Continuous scope-control gate |
| OV Section 24 - Reference Datasets | P4-P9, P11 | Reference A, B, and C progression |
| OV Section 25 - Delivery Standard | P0-P11 | Phase completion gates and independent validation |
| OV Section 26 - Planning and Execution Model | All phases | Central governance and artifact chain |
| OV Section 27 - Step Planning | Phase plans and packets | Applied just in time after roadmap approval |
| OV Section 28 - Audit and Review | P0-P11 | Risk-scaled independent validation |
| OV Section 29 - Roadmap Requirement | This document | Maintained subordinate to specification and spine |
| OV Section 30 - Scope-Control Rule | P0-P11 | Change classification and smallest-robust-solution rule |
| OV Section 31 - Success Definition | H3-H8 | Demonstrated progressively, with fullest evidence across later horizons |

---

## 9. Major Risk Watchlist

| Risk | First control point | Roadmap response |
|---|---:|---|
| Framework choice dictates product architecture prematurely | P0 | Compare options against approved criteria; record the decision and rejected alternatives |
| Workflow format is too weak to evolve or too abstract to implement | P1 | Test concrete valid, invalid, branched, and versioned examples before UI dependence |
| Execution results depend on node creation order or hidden state | P2 | Dependency-order and repeatability tests; explicit run context and artifacts |
| UI and backend silently diverge | P3 | Contract-driven controls and boundary tests proving parameters reach runtime operations |
| Profiling silently mutates data or preparation leaks target information | P4-P5 | Explicit transformation graph, provenance, split-aware tests, actionable warnings |
| Metrics or interpretations overstate certainty | P5-P6 | Approved wording rules, representative cases, and domain-aware review where needed |
| Experiment lineage becomes ambiguous | P6 | Explicit identities, immutable run evidence, and tested restoration/comparison semantics |
| Generated notebooks drift from application behavior | P7 | Shared canonical input and execution-parity tests within stated tolerances |
| Automation becomes opaque or consumes unbounded resources | P8 | Editable outputs, decision visibility, explicit budgets, cancellation, and failure reporting |
| Healthcare validation creates privacy or domain-validity risk | P9 | Approved dataset governance and independent domain review before claims are accepted |
| Neural-network support expands into a framework replacement | P10 | Fixed supported subset and explicit non-goals; expansion requires scope approval |
| Scientific validation overgeneralizes from one challenge | P11 | Predeclared bounded claims and acceptance of a limitation report as a valid outcome |

Risks discovered during delivery are recorded at the narrowest responsible level and escalated when they affect a phase outcome, product requirement, or roadmap dependency.

---

## 10. Deferred and Out-of-Scope Horizons

The following items are not scheduled by this roadmap:

- human-visible agent control beyond preserving the structured operations needed for a later decision;
- distributed or cloud execution;
- production model serving and enterprise MLOps;
- multi-user collaboration, RBAC, and enterprise governance;
- production ETL orchestration or data-warehouse behavior;
- arbitrary Python or third-party notebook reconstruction into graphs;
- unrestricted neural-network architectures or a complete visual PyTorch replacement;
- a plugin marketplace, enterprise-scale data storage, or an autonomous data scientist.

These items cannot enter a phase through an implementation convenience. Adding one requires an approved scope proposal, impact analysis, and any necessary changes to the specification, spine, and roadmap.

---

## 11. Roadmap Maintenance Rules

Central maintains this document after accepted evidence or approved change. Each update must:

1. Preserve the prior version in history rather than rewriting completed facts.
2. Update phase status only from named evidence and reconciliation.
3. Link decisions, validation records, and material limitations when those artifacts exist.
4. Record new dependencies or deferrals without silently changing higher-level requirements.
5. Keep future phases coarse until their planning gate opens.
6. Avoid percentage-complete estimates and unsupported delivery dates.
7. Distinguish a demonstrated capability from a planned or inferred capability.

Calendar estimates may be added after Phase 0 establishes the repository baseline, technical shape, contributor assumptions, and an estimation method. They remain forecasts, not acceptance criteria.

---

## 12. Next Action After Roadmap Approval

After this roadmap is approved, Central should draft the detailed Phase 0 plan only. That plan should inspect the actual repository state, resolve or schedule the P0 decisions named above, define workstreams and acceptance evidence, and propose bounded execution-packet boundaries.

Approval of this roadmap will authorize Phase 0 planning, not implementation.
