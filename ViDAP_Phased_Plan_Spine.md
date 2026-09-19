# ViDAP Phased Plan Spine

**Status:** Approved, amended
**Version:** 1.2
**Approved:** 2026-09-17
**Amended:** 2026-09-19 (worker completion-attestation clarification)
**Source of truth:** `ViDAP_Overview.txt`
**Purpose:** Define the stable implementation sequence, phase boundaries, and approval gates without expanding into detailed phase plans or execution instructions.

---

## 1. Authority and Artifact Model

This spine is subordinate to the current user direction and the product specification. It organizes the specification; it does not replace or reinterpret it.

Authority descends in this order:

1. Current explicit user direction.
2. Approved clarifications and decision records.
3. `ViDAP_Overview.txt`.
4. This approved Phased Plan Spine.
5. The living roadmap derived from the spine.
6. An approved plan for one phase.
7. Bounded execution packets derived from that phase plan.
8. Implementation and validation evidence.

If two artifacts conflict, the higher-authority artifact controls and Central records the conflict rather than silently resolving it in a lower-level artifact.

The planning and delivery chain is:

`Product Specification -> Phased Plan Spine -> Roadmap -> Phase Plan -> Execution Packet -> Implementation -> Independent Validation -> Central Reconciliation`

### Artifact boundaries

- **Spine:** Stable outcomes, dependencies, scope boundaries, and gates across the whole project.
- **Roadmap:** Milestones, dependency relationships, validation targets, visible deliverables, deferrals, and status.
- **Phase plan:** Just-in-time decomposition of one phase into workstreams, decisions, tests, and proposed packets.
- **Execution packet:** One bounded, implementable, independently verifiable unit of work.
- **Validation record:** Evidence that delivered behavior meets the packet, phase, and specification.
- **Decision record:** A durable explanation of a consequential choice, alternatives, and implications.

Approval of one artifact authorizes creation of the next planning artifact only. It does not authorize implementation unless an execution packet is separately approved for execution.

---

## 2. Planning Controls

### 2.1 Status model

Planning and delivery artifacts use these states:

- **Draft:** Open for review; not authoritative.
- **Approved:** Accepted as the governing baseline for its scope.
- **Active:** Approved and currently being worked.
- **Blocked:** Unable to advance without a named decision or dependency.
- **Complete:** Acceptance evidence has passed independent validation and Central reconciliation.
- **Superseded:** Replaced by a newer approved version while retained for history.

### 2.2 Change control

Discoveries are classified before changing the plan:

- **Defect:** Approved behavior was implemented incorrectly.
- **Clarification:** Existing intent needs a more precise expression without changing scope.
- **Dependency change:** An external library, platform, or prerequisite alters the viable approach.
- **Scope proposal:** New or materially expanded behavior not already required.

Scope proposals require explicit approval. Lower-level artifacts may not silently introduce them. The default response to implementation difficulty is the smallest robust solution satisfying the approved requirement.

### 2.3 Just-in-time detail

Only the next phase is expanded into a detailed phase plan. Later phases remain at spine and roadmap resolution until evidence from preceding phases is reconciled. This prevents early assumptions from becoming false precision.

### 2.4 Requirement traceability

The section numbers in `ViDAP_Overview.txt` are the canonical requirement anchors, cited as `OV §N`. Detailed plans may introduce finer requirement IDs, but must retain their link to the originating overview section.

Every execution packet must cite:

- its parent phase and phase-plan item;
- the overview requirements it advances;
- its acceptance evidence;
- any explicit exclusions or deferrals.

Every overview requirement must ultimately be implemented, explicitly deferred with rationale, or explicitly excluded by approved scope change.

### 2.5 Decision timing

Technology selections remain open until their owning phase has enough evidence to evaluate compatibility, maintainability, licensing, packaging, testability, and user impact. The spine does not preselect a frontend framework, backend framework, persistence engine, workflow encoding, AutoML library, or optional model family.

### 2.6 Worker completion attestation

Every execution packet must name the final local commands and evidence required for a worker-completion attestation. Before reporting implementation complete or requesting independent validation, the worker must run those commands against the final post-change working tree. If a required command fails, the worker must repair the failure within packet scope and rerun the applicable attestation, or return a named blocker; pre-change results never count as completion evidence.

The worker report must record the final commands, their successful outcomes, and any packet-required lock, cleanup, or generated-state evidence. A worker may not defer required checks to the validator.

This attestation is evidence for validation, not validation itself. The worker cannot issue an independent verdict, accept work for Central, or replace the validator's independent reproduction and review.

---

## 3. Program-Wide Invariants

These constraints apply to every relevant phase and packet:

1. **Real computation:** Supported nodes invoke established data-science or ML implementations, not simulations or UI-only approximations.
2. **Visible semantics:** Important transformations, parameters, validation choices, and automated decisions remain inspectable and editable.
3. **Canonical workflow:** Visual layout is not the runtime. Execution and export derive from a structured, versioned workflow and semantic execution representation.
4. **Layer separation:** UI, graph/schema, execution, experiment/state, and export responsibilities remain logically separated.
5. **Determinism and provenance:** Runs record the workflow, inputs, parameters, environment-relevant metadata, seeds, results, and artifacts required for appropriate reproduction.
6. **Typed contracts:** Node inputs, outputs, parameters, validation, runtime behavior, result representation, and supported export behavior are explicit.
7. **No silent behavior:** Parameters cannot be ignored; failures cannot be hidden; caches cannot silently return stale results.
8. **Actionable errors:** User-facing explanations identify the affected operation and likely remedy while preserving technical diagnostics.
9. **Plain-English meaning:** Plans, approvals, and important results explain practical meaning without requiring specialist notation.
10. **Open interoperability:** Persisted workflows are inspectable, versioned, and programmatically manipulable. Exported artifacts do not trap the user in the UI.
11. **Testing as delivery:** Tests and representative acceptance evidence are part of each capability, not deferred cleanup.
12. **License and dependency control:** Dependencies must be compatible with an MIT-licensed project and assessed for maintenance, packaging, and security implications.
13. **No runtime LLM dependency:** Normal workflow execution and deterministic code export do not require an LLM to generate arbitrary source code.
14. **Proportional architecture:** Extensibility required by the specification is preserved without generalizing into distributed compute, enterprise MLOps, or other stated non-goals.
15. **Data responsibility:** Fixtures and validation datasets require known provenance, permitted use, manageable storage, and no unnecessary sensitive information.
16. **Intentional visual design and UX:** User-facing capabilities require intentional, coherent visual hierarchy, interaction quality, accessibility, and readability at realistic information density. Functional correctness alone is insufficient; substantial UI work must follow an approved concise design system or equivalent and receive proportionate independent visual/UX review.
17. **Completion claims require final evidence:** An execution worker cannot call work complete based on an implementation narrative, pre-change command output, or a belief that the validator will discover defects. The packet-defined post-change attestation must be green, or the worker must return a blocker.

---

## 4. Phased Implementation Spine

The requirement citations below identify primary ownership, not exclusive applicability. Cross-cutting requirements may govern several phases even when they are not repeated in every citation. The roadmap must include a complete coverage view so that no overview requirement disappears between phases.

### Phase 0 — Project Foundation and Delivery Baseline

**Outcome:** A reproducible, inspectable project foundation on which implementation can proceed safely.

**Includes:** Repository and environment baseline; selected initial application shape; development setup; automated test and quality entry points; CI expectations; dependency and license inventory process; documentation conventions; decision-record mechanism; versioning policy; representative fixture policy; and a minimal runnable shell proving the chosen components can be built and tested together.

**Excludes:** Product feature implementation, graph semantics, ML workflows, and speculative production infrastructure.

**Entry gate:** Spine and roadmap approved; Phase 0 plan approved; unresolved foundational decisions have owners and decision criteria.

**Exit evidence:** A clean environment can reproduce setup, build, test, and launch the minimal shell; dependency/license checks are actionable; project conventions and ownership boundaries are documented.

**Primary requirements:** OV §§9, 18, 20–23, 25–30.

---

### Phase 1 — Canonical Workflow and Node Contract Kernel

**Outcome:** A UI-independent, versioned representation of workflows and extensible node definitions.

**Includes:** Workflow schema; stable node identity; typed ports; node parameter contracts; edges and subgraph representation; semantic validation; serialization/deserialization; schema version handling; node registration/extension boundary; separation of visual metadata from executable semantics.

**Excludes:** A production visual editor, broad data operations, model training, and generated notebooks.

**Entry gate:** Phase 0 complete; workflow-format and compatibility decisions approved.

**Exit evidence:** Representative valid, invalid, branched, and versioned workflows round-trip deterministically; invalid connections and configurations produce useful validation results; layout changes do not alter workflow semantics.

**Primary requirements:** OV §§6–7, 16–17, 18, 21–22A, 25.

---

### Phase 2 — Deterministic Execution and Run Foundations

**Outcome:** Validated workflows can be executed headlessly through a deterministic engine, producing recorded results and artifacts.

**Includes:** Dependency-derived ordering; intermediate execution representation; runtime node dispatch; failure propagation; run identity; seed and environment metadata; artifact references; initial experiment/run record; shared-upstream behavior; explicit cache correctness rules; technical and user-oriented error envelopes.

**Excludes:** Full experiment comparison UX, AutoML, advanced models, and notebook export.

**Entry gate:** Phase 1 complete; execution semantics and artifact ownership decisions approved.

**Exit evidence:** Small reference workflows execute independently of node creation order or visual position; branching and invalid graphs behave predictably; repeated deterministic runs reproduce appropriate results; cache behavior cannot disguise changed inputs or parameters.

**Primary requirements:** OV §§12, 18–19, 21–22A, 25.

---

### Phase 3 — First Visual End-to-End Slice

**Outcome:** A user can construct, validate, save, load, and run a deliberately narrow real workflow through the visual interface.

**Includes:** Initial graph editor; contract-driven node configuration; typed connection feedback; run controls and status; basic result presentation; an intentionally small CSV-to-baseline-result workflow using real backend operations; visible validation and error details; and an approved concise visual design system or equivalent that governs substantial UI implementation. The slice proves integration with only the minimum operations needed and does not preempt the broader data or modeling policies owned by later phases.

**Excludes:** Broad node coverage, polished exploration, comprehensive modeling, and advanced experiment management.

**Entry gate:** Phase 2 complete; the vertical-slice capability and UX acceptance path are approved. Before substantial user-facing UI packets are approved, the Phase 3 plan must approve the visual design system or equivalent, its design/UX support mechanism, representative states, and proportionate validation method.

**Exit evidence:** A fresh user can assemble and execute the selected reference slice; the saved graph is the same canonical workflow used by the runtime; UI parameters demonstrably reach backend operations; a representative failure is understandable and actionable; and independent proportionate visual/UX review confirms the approved design system, hierarchy, interaction, accessibility, and representative-state expectations.

**Primary requirements:** OV §§2–7, 18–22A, 25, 31.

---

### Phase 4 — Data Intake, Profiling, and Preparation

**Outcome:** Users can understand and deliberately prepare real tabular data without invisible mutation.

**Includes:** Selected local tabular formats; schema and type inference; profiling; distributions and missingness; cardinality and identifier warnings; explicit filtering, selection, imputation, categorical encoding, scaling, and a bounded feature-engineering set; data-quality messages linked to relevant actions; provenance across transformations.

**Excludes:** Universal data-source support, warehouse integration, arbitrary code transforms, and domain-specific scientific formats.

**Entry gate:** Phase 3 complete; supported dataset constraints and profiling/privacy policy approved.

**Exit evidence:** Titanic-scale reference data can be loaded, profiled, prepared, saved, and rerun; transformations are explicit in the graph; representative bad data produces actionable failures; outputs match direct library behavior.

**Primary requirements:** OV §§5–9, 18–19, 21–25; validation target OV §24 Reference A.

---

### Phase 5 — Baseline Supervised Modeling and Evaluation

**Outcome:** A user can build and understand genuine end-to-end baseline classification and/or regression workflows within an explicitly approved initial task boundary.

**Includes:** Target definition; supported split and validation strategy; leakage-aware boundaries; a small representative model set; training configuration; predictions; appropriate metrics; confusion/error views where applicable; practical metric interpretation; overfit/underfit signals where defensible.

**Excludes:** Exhaustive algorithm coverage, AutoML, custom neural networks, causal claims, and production serving.

**Entry gate:** Phase 4 complete; initial task types, model families, evaluation policy, and interpretation wording are approved.

**Exit evidence:** The approved Titanic workflow trains and evaluates real libraries end to end; graph parameters are verified at the library boundary; results are reproducible; interpretations remain accurate and avoid unsupported certainty.

**Primary requirements:** OV §§2–5, 9, 13, 18–25, 31; validation target OV §24 Reference A.

---

### Phase 6 — Experiment Branching, Comparison, and Reasoning

**Outcome:** Experiments become durable, comparable artifacts rather than isolated executions.

**Includes:** Branch comparison; shared upstream computation with transparent reuse; graph/run snapshots; configuration and outcome diffs; restoration or inspection of prior states; practical comparison narratives; optional observation, hypothesis, expected effect, actual result, and interpretation fields.

**Excludes:** Multi-user collaboration, enterprise governance, and autonomous agent experimentation.

**Entry gate:** Phase 5 complete; experiment identity, lineage, and retention rules approved.

**Exit evidence:** Users can compare preprocessing, feature, model, and parameter variants; the system accurately identifies what changed and how outcomes changed; prior runs retain sufficient provenance for inspection and appropriate reproduction.

**Primary requirements:** OV §§5, 12–14, 18, 21–25, 31.

---

### Phase 7 — Export and Interoperability

**Outcome:** Supported workflows can leave the application as useful, conventional, reproducible data-science artifacts.

**Includes:** Readable Python and/or Jupyter generation from the canonical workflow representation; predictions/data output; selected model artifacts; traceability from nodes to generated sections; deterministic generators for supported operations; parity tests between runtime and export within defined tolerances.

**Excludes:** Arbitrary notebook-to-graph reconstruction and guaranteed lossless round trips for third-party-edited notebooks.

**Entry gate:** Phase 6 complete; supported export surface and parity tolerances approved.

**Exit evidence:** A supported reference workflow exports to a readable artifact that executes independently and produces equivalent results within approved tolerances; unsupported operations are reported explicitly rather than silently omitted.

**Primary requirements:** OV §§3, 15–18, 21–25, 31.

---

### Phase 8 — Extended Tabular Modeling and Inspectable Automation

**Outcome:** Users can explore stronger model families and optimization assistance without losing visibility or control.

**Includes:** Approved gradient-boosting family or families; hyperparameter search; additional validation strategies such as grouped or temporal splits where supported; imbalance handling; selected ensembles; inspectable AutoML/baseline generation that yields editable workflows; resource limits and cancellation behavior.

**Excludes:** Opaque best-model endpoints, unlimited searches, hidden preprocessing, and autonomous analytical decision-making.

**Entry gate:** Phase 7 complete; library/license evaluation, search-budget policy, and editable-automation design approved.

**Exit evidence:** Automated and manually configured experiments expose preprocessing, validation, parameters, and metrics; generated workflows can be edited and rerun; resource limits and failures are visible; direct-library parity is tested.

**Primary requirements:** OV §§6, 8–9, 11–14, 18–25, 30–31.

---

### Phase 9 — Real-World Tabular Robustness

**Outcome:** The architecture and user experience are validated against materially more complex, domain-relevant data than the initial benchmark.

**Includes:** Selection and governance of the healthcare reference dataset; necessary bounded support for multiple tables, time, grouping/aggregation, high-cardinality categories, imbalance, ranking, or entity-level analysis; operational result interpretation; performance and memory characterization.

**Excludes:** Healthcare-specific product hard-coding, clinical claims, production deployment, or a general data warehouse/ETL platform.

**Entry gate:** Phase 8 complete; dataset permission, success scenario, privacy constraints, and required capability subset approved.

**Exit evidence:** The approved healthcare scenario runs end to end; domain review finds transformations and interpretations conceptually valid; limitations and resource behavior are documented; improvements remain general where the specification requires generality.

**Primary requirements:** OV §§4–5, 8, 12–14, 18–25, 30–31; validation target OV §24 Reference B.

---

### Phase 10 — Bounded Neural-Network Workflows

**Outcome:** Users can construct and execute a constrained, inspectable feed-forward neural-network workflow backed by a real framework.

**Includes:** Approved layer and activation subset; nested model graph or equivalent structured representation; shape/compatibility validation; training configuration; reproducibility controls; evaluation integration; supported export behavior.

**Excludes:** Arbitrary PyTorch replacement, unrestricted architectures, custom CUDA, foundation-model training, and invisible generated code.

**Entry gate:** Earlier workflow/runtime abstractions have survived real-world validation; neural-network representation and scope are approved.

**Exit evidence:** Supported networks validate, train, evaluate, save, and export as specified; invalid shapes and configurations fail actionably; configuration reaches the underlying framework exactly as represented.

**Primary requirements:** OV §§2, 6, 9–10, 15, 18–25, 30–31.

---

### Phase 11 — Generality and Scientific Extension Validation

**Outcome:** Determine, with evidence, whether the architecture can support a complex unfamiliar scientific workflow without distorting the core product.

**Includes:** A bounded feasibility and implementation scope for the approved scientific reference; extension points needed for non-tabular representations, specialized metrics, domain feature handling, and larger-scale local execution; documented architectural findings and any separately approved capabilities.

**Excludes:** A promise to solve the entire competition, distributed compute, universal scientific tooling, or unapproved specialization of the core product.

**Entry gate:** Core product capabilities are stable; the reference dataset, licensing, storage, compute budget, and success criteria are approved.

**Exit evidence:** The approved scientific scenario demonstrates the selected extension claims, or produces a validated limitation report and scoped follow-on proposal; no result may be presented as generality evidence beyond what was actually tested.

**Primary requirements:** OV §§6–10, 18–25, 30–31; validation target OV §24 Reference C.

---

## 5. Program Milestones

The roadmap will refine these milestones without changing their meaning:

- **Foundation ready:** Phase 0 complete.
- **Executable architecture proven:** Phases 1–2 complete.
- **Visual interaction proven:** Phase 3 complete.
- **First useful data-science workflow:** Phases 4–5 complete.
- **Core experimentation product:** Phases 6–7 complete.
- **Inspectable advanced tabular product:** Phase 8 complete.
- **Real-world tabular validation:** Phase 9 complete.
- **Neural-network depth demonstrated:** Phase 10 complete.
- **Scientific extensibility assessed:** Phase 11 complete.

These milestones are capability statements, not release promises. Release packaging and version numbering will be proposed in the roadmap and approved separately.

---

## 6. Phase Readiness and Completion Gates

A phase may enter detailed planning only when:

- its predecessor evidence has been reconciled, unless an explicitly independent planning dependency is documented;
- its input assumptions are current;
- unresolved product decisions are visible;
- its intended outcome remains consistent with the approved spine;
- its planning effort will not prematurely lock a later-phase choice.

A phase may enter execution only when its phase plan is approved and its first execution packet is bounded, testable, approved, and defines its final worker-completion attestation commands. Where applicable, this includes quality, test, build, smoke, dependency, and cleanup checks; the exact commands remain packet-specific.

A phase is complete only when:

- all required packets have accepted validation evidence;
- automated tests and the phase-level representative workflow pass;
- user-facing behavior, failure behavior, and documentation meet the phase plan;
- dependency and license records are current;
- deviations, limitations, and deferred items are recorded;
- Central reconciles the evidence against the phase outcome and relevant overview requirements.

Passing tests alone is necessary but not sufficient for completion.

---

## 7. Validation Scaling

Validation depth increases with the risk of misleading or irreversible behavior.

- **Routine:** Styling, labels, and isolated presentation behavior.
- **Standard:** Node UI, ordinary transformations, and bounded application behavior.
- **Strong:** Workflow serialization, contract validation, execution ordering, caching, experiment lineage, reproducibility, model parameter propagation, metrics, and export parity.
- **Specialized:** Domain-sensitive interpretation, temporal/grouped validation, AutoML decisions, neural-network semantics, migration behavior, and scientific extension claims.

Implementers do not provide final acceptance for their own work. Independent review may be lightweight, but it must examine the relevant requirement and evidence rather than merely confirm that tests ran. It is not a substitute for the worker's required post-change attestation.

---

## 8. Deferred Decisions Register

The following choices are deliberately unresolved at spine level:

| Decision | Required by | Decision criteria |
|---|---:|---|
| Application/frontend/backend shape | Phase 0 plan | Local usability, packaging, separation of concerns, testability, contributor accessibility |
| Workflow serialization encoding and compatibility policy | Phase 1 plan | Openness, readability, deterministic behavior, evolution, source-control suitability |
| Execution isolation and artifact persistence | Phase 2 plan | Reproducibility, failure containment, local simplicity, inspectability |
| Initial vertical-slice operation set | Phase 3 plan | Architectural coverage with minimal breadth and real user value |
| Visual design system or equivalent, design/UX support mechanism, and visual validation method | Phase 3 plan | Analytical-workspace hierarchy, readability, information density, accessibility, interaction quality, maintained support, and proportionate reviewability |
| Initial supported data formats and size bounds | Phase 4 plan | Common usefulness, reliability, packaging, memory behavior |
| Initial task types, model families, and metric policy | Phase 5 plan | Real-world legitimacy, interpretability, testability, dependency cost |
| Export formats and equivalence tolerances | Phase 7 plan | User value, readable output, reproducibility, library behavior |
| Boosting, optimization, and AutoML dependencies | Phase 8 plan | License, transparency, maintenance, resource control, editable output |
| Healthcare validation dataset | Phase 9 plan | Permission, privacy, representative complexity, stable access |
| Neural-network framework and supported layer subset | Phase 10 plan | Ecosystem maturity, packaging, determinism, export fit |
| Scientific reference commitment and success boundary | Phase 11 plan | Data access, compute, architectural learning value, bounded scope |
| Human-visible agent control capability | Post-core roadmap decision | Deterministic human workflow maturity, constrained operations, auditability, safety, clear user value |

Deferral is not permission to make these decisions implicitly during unrelated work.

---

## 9. Explicit Program Exclusions

Unless the product specification and spine are deliberately amended, the program does not introduce distributed cluster computing, cloud ML orchestration, production serving, enterprise MLOps, multi-user collaboration, RBAC, a data warehouse, production ETL orchestration, arbitrary Python-to-graph reconstruction, a complete visual PyTorch replacement, new ML algorithms, custom CUDA, foundation-model training, universal dataset/task support, an autonomous data scientist, a plugin marketplace, or enterprise-scale storage.

Agent compatibility remains an architectural consideration and later controlled capability. It is not a prerequisite for deterministic human-driven graph construction and execution.

---

## 10. Next Planning Action

The next subordinate artifact is `ViDAP_Roadmap.md`. The roadmap elaborates milestones, dependencies, validation demonstrations, architectural checkpoints, deferrals, and status while preserving the phase boundaries above.

Only after the roadmap is approved should Central draft the detailed Phase 0 plan. No execution packet or implementation work is authorized by approval of this spine alone.
