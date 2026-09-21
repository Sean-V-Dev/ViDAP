# ViDAP P1-EP03 — Node-Contract Registry

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Execution approved | 2026-09-20 by explicit user direction |
| Completed | 2026-09-20 |
| Packet type | Bounded Python contract and static-registry implementation |
| Parent phase plan | `ViDAP_Phase_1_Plan.md` version 1.4 |
| Prerequisites | P1-EP01 and P1-EP02 complete |
| Prerequisite reconciliations | `ViDAP_P1_EP01_Validation_and_Reconciliation.md`; `ViDAP_P1_EP02_Validation_and_Reconciliation.md` |
| Workstream | WS1.3 — Contracts and registry |
| Authorized worker report | `ViDAP_P1_EP03_Implementation_Report.md` |
| Central reconciliation | `ViDAP_P1_EP03_Validation_and_Reconciliation.md` |
| Created | 2026-09-20 |
| Owner | Central |

---

## 1. Authorization Boundary

This approved packet authorizes one worker to add immutable, declarative
node/port/parameter contract values and an explicit static first-party registry
on top of P1-EP02's accepted workflow document kernel. The worker may modify
only the Section 7 paths.

This packet does not authorize workflow semantic validation or structured
diagnostics, a schema artifact, version migration, representative workflow
fixtures, UI/editor/form work, HTTP/API binding, persistence, process launch,
execution planning, caching, data loading, model training, prediction,
metrics, artifact generation, export, plugin discovery, external catalogs,
dependency/lockfile changes, CI changes, remote mutation, or P1-EP04 and
later work.

## 2. Plain-English Packet Intent

### What this packet will build

It gives the workflow kernel a small declarative catalog that says what a node
*claims* to accept and produce: stable node type ID, human-readable display
metadata, named input/output ports, nominal port types, input cardinality, and
parameter metadata. It also establishes the safe, static way that later
first-party node definitions can be added.

### What it will not build

It will not decide whether a particular workflow instance is valid, execute a
node, connect to data, render a form, or load a plugin. The contracts are
descriptions for later validation, UI, runtime, and export consumers—not
operations or permissions.

### How success will be demonstrated

Unit tests will construct contracts and static registries without a browser or
runtime, prove definitions are immutable, prove duplicate IDs and keys are
rejected at definition/registration time, preserve parameter metadata and
defaults, and prove no execution/web consumer is imported. Tests will not
claim that workflow edges, parameters, types, or required inputs have been
validated; P1-EP04 owns that work.

## 3. Governing Inputs

The worker and validator must read:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§6–7, 16, 18–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially invariants 3–4,
   10–13 and the Phase 1/Phase 2 boundaries.
4. `ViDAP_Roadmap.md` version 2.5, especially P1 and its next action.
5. `ViDAP_Phase_1_Plan.md` version 1.4, especially WS1.3, D1.3, D1.4,
   D1.7, Sections 7–10, and P1 acceptance criteria.
6. `ViDAP_P1_EP01_Validation_and_Reconciliation.md`, authoritative for
   accepted D1.3, D1.4, and D1.7.
7. `ViDAP_P1_EP02_Validation_and_Reconciliation.md`, authoritative for
   the accepted document/kernel ownership and D1.1–D1.2 boundaries.
8. Accepted Phase 0 decisions concerning Python 3.14/uv, root quality
   controls, dependency/license controls, fixtures, and repository hygiene.
9. This packet.

## 4. Inherited Decisions and Contract Boundaries

The implementation must preserve the following accepted decisions:

1. Ports use exactly the initial nominal tokens `table`, `target`,
   `split`, `model`, `predictions`, `metrics`, and `artifact`.
   These name workflow artifacts only; they do not select Python classes,
   libraries, operations, or data formats.
2. A port has an immutable key unique within its node definition. Inputs have
   cardinality `one` or `many`; outputs may fan out. Requiredness is
   declarative contract data.
3. A parameter contract has a stable key, declared value kind, required flag,
   optional default, and applicable declarative constraint metadata. Defaults
   are contract-owned. Workflow-node parameter overrides remain in the
   P1-EP02 document model.
4. Node definitions are declarative data: stable node type ID, display
   metadata, input/output port contracts, parameter contracts, and an optional
   non-executing `operationKey`. An operation key is not a callable, import
   path, command, URL, permission, runtime mapping, or export mapping.
5. The registry is an explicit static, first-party allowlist. It does not
   execute third-party code, scan a directory, import document-named paths,
   contact a registry, load a plugin, or automatically install anything.
6. Duplicate node-type registration and duplicate port/parameter keys are
   deterministic definition/registration errors. Unknown workflow node types,
   connection compatibility, input cardinality, required inputs, parameter
   values, cycle detection, and user-facing diagnostics remain P1-EP04 work.
7. Future extension is an approved static source contribution plus tests. A
   marketplace, remote catalog, manifest discovery, and dynamic plugin ABI
   are expressly deferred.

## 5. Preconditions and Stop Gates

Before changing a file, the worker must confirm and record:

1. This exact packet version has explicit execution approval.
2. P1-EP01 and P1-EP02 remain complete; their reconciliation records are
   present and unsuperseded.
3. Current branch, commit, sanitized remote identity, worktree state,
   pre-existing work, output-path collisions, and both lock hashes are known.
4. Node 24/npm and normal Windows uv-managed CPython 3.14 are callable. A
   restricted `uv.exe` denial must be retried through the normal Windows
   path before a project prerequisite failure is reported.
5. Inherited locked setup and aggregate checks pass before the worker change,
   with unchanged locks.
6. A new bounded temporary location outside the repository and OneDrive is
   available for clean-copy proof and safe removal.

Stop and report a blocker if the work needs a dependency, lock/manifest
change, schema file, fixture, semantic validator, diagnostic envelope,
migration, plugin/discovery mechanism, product operation, UI/API/process
behavior, unsafe cleanup, or any path outside Section 7.

## 6. Required Implementation

### 6.1 Contract values

Implement only immutable Python contract values under
`python/src/vidap_workflow/`:

- `PortDefinition`: key, direction, nominal type token, input cardinality
  where applicable, requiredness where applicable, display metadata, and no
  runtime behavior;
- `ParameterDefinition`: key, declared JSON-compatible value kind,
  requiredness, an explicit omitted-default sentinel or immutable optional
  default, and declarative constraint metadata;
- `NodeDefinition`: namespaced stable type ID, display metadata, separate
  input/output port collections, parameter collection, and optional
  non-executing operation key; and
- narrowly named immutable metadata values needed to make these definitions
  readable and testable.

The value constructors may reject malformed *definition* metadata:
empty/duplicate keys, invalid direction/cardinality/type-token/value-kind,
invalid default/constraint metadata shape, or malformed type IDs. They must
not validate workflow instance edges or parameter overrides, resolve defaults
for a workflow, apply value constraints, infer types, or create a diagnostic
contract.

### 6.2 Static registry

Implement an immutable `NodeRegistry` whose definitions are supplied
explicitly by first-party code. It may expose safe read-only lookup and a
functional method that returns a new registry after an explicit definition is
added. It must deterministically reject duplicate node type IDs and must not
provide filesystem, network, package, plugin, reflection, import-by-string,
or code-execution discovery.

Provide exactly two non-operational built-in **contract specimen** definitions:

- `vidap.kernel.contract-source`, with declared outputs that exercise the
  seven accepted nominal type tokens; and
- `vidap.kernel.contract-sink`, with declared inputs that exercise those
  same tokens and at least one parameter definition with an explicit default
  and declarative constraint metadata.

These specimens are not data loaders, transformations, models, predictors,
metrics, or artifact writers. They have no execution implementation, cannot
produce or consume real data, and are not a user-facing node palette. Their
sole purpose is to make the accepted registry/contract boundary concrete and
testable before real node families are selected in their owning phases.

### 6.3 Public API and dependency direction

Update the small `vidap_workflow` public surface to export only the accepted
contract and registry values, the immutable built-in registry, and any
necessary type constants. It must continue to import no web, execution,
experiment, export, FastAPI, Uvicorn, third-party plugin, filesystem,
subprocess, or network code.

Use only the existing Python 3.14 standard library and P1-EP02 workflow
values. Do not change project dependencies or locks.

### 6.4 Required tests

Use only inline synthetic test values. Do not create a fixture file. Tests
must prove:

1. Contract definitions are immutable and preserve their declared metadata.
2. Every initial nominal type token is represented by the two contract
   specimens, with clear input/output direction and input cardinality.
3. Parameter metadata preserves requiredness, explicit default versus omitted
   default, and supported declarative constraints without evaluating a
   workflow value.
4. Duplicate or malformed node type IDs, port keys, parameter keys, and
   registry registration fail deterministically at definition/registry time.
5. Registry lookup and functional static addition return only declarative
   definitions and do not mutate the prior registry.
6. Public imports do not transitively import execution, experiment, export,
   FastAPI, Uvicorn, plugin/discovery, filesystem, subprocess, or network
   consumers.
7. No test claims workflow node-type membership, edge direction/type/
   cardinality validity, required-input satisfaction, parameter-value
   validation, diagnostics, migration, extension compatibility, execution
   ordering, or real data/ML behavior.

## 7. Exact Authorized Repository Outputs

The worker may create or modify only:

| Path | Authorized purpose |
|---|---|
| `python/src/vidap_workflow/contracts.py` | Immutable declarative port, parameter, node, constraint, and type-token values. |
| `python/src/vidap_workflow/registry.py` | Immutable explicit static registry and the two non-operational contract specimens. |
| `python/src/vidap_workflow/__init__.py` | Deliberate public exports for the contract/registry surface only. |
| `python/tests/test_workflow_contracts.py` | Inline synthetic unit tests required by Section 6.4. |
| `ViDAP_P1_EP03_Implementation_Report.md` | Sanitized worker evidence and self-attestation. |

No other path may be added, changed, moved, staged, committed, or deleted.
In particular, do not modify the accepted document/serialization source,
existing tests, manifests, locks, configuration, CI, fixture area, web code,
execution/experiment/export packages, governing documents, or prior decision/
reconciliation records.

## 8. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read all governing inputs and record the required baseline, pre-existing
   work, output collisions, and lock hashes.
2. Run `npm.cmd run setup` and `npm.cmd run check` against the inherited
   baseline. Stop if either fails before the worker change.
3. Implement only the Section 7 paths. Keep the built-ins non-operational and
   all test data inline/synthetic.
4. Run focused Python tests while implementing. Then run the complete final
   attestation in this order:
   - `npm.cmd run check`;
   - `npm.cmd run coverage`;
   - `npm.cmd run deps:inventory`;
   - `npm.cmd run license:check`;
   - `npm.cmd run deps:audit`; and
   - `git diff --check`.
5. If a final check identifies a worker-caused issue, correct it only within
   Section 7 and rerun the *entire* final attestation from the first command.
   Do not report completion unless every required command passes. Stop with
   evidence if a failure is unrelated or needs broader authority.
6. Confirm both locks remain byte-identical; inspect exact changed/untracked
   scope, ignored state, text policy, sensitive-content scan, and absence of
   listeners, logs, caches, environments, and temporary copies.
7. In a new clean copy outside the repository and OneDrive, run locked setup,
   focused contract tests, and `npm.cmd run check`; verify results and safely
   remove only the exact bounded temporary copy/caches.
8. Write the implementation report and stop for independent validation. Do
   not self-validate, stage, commit, push, change remote state, or begin
   P1-EP04.

## 9. Required Worker Evidence

The worker report must include:

1. Packet/version/approval metadata; governing inputs; baseline; sanitized
   remote; pre-existing work; exact scope; and output collisions.
2. Before/after lock hashes and confirmation that no dependencies, manifests,
   locks, package managers, or runtime policies changed.
3. A requirement-to-path/test mapping for every Section 6 item.
4. Plain-English descriptions of contract metadata, static registration,
   built-in specimens, public exports, and the exact non-operational boundary.
5. Focused-test and full-attestation results, including any required rerun
   loop.
6. Clean-copy and bounded cleanup evidence.
7. Proof that no validation, diagnostics, migration, UI, API, process,
   execution, data/ML, export, plugin/discovery, or fixture behavior entered.
8. Scope, hygiene, sensitive-content, ignored-state, and final Git evidence.
9. Criterion-by-criterion self-assessment clearly labeled as worker
   self-assessment, not independent validation or Central acceptance.

## 10. Acceptance Criteria

P1-EP03 may be accepted only when:

- **EP03-AC01:** Authority, prerequisites, accepted D1 decisions, baseline,
  pre-existing work, locks, and exact scope are recorded accurately.
- **EP03-AC02:** Only the five Section 7 paths are changed/created by the
  worker, with no unauthorized/generated residue.
- **EP03-AC03:** Immutable declarative port, parameter, node, and registry
  values implement the accepted D1.3/D1.4/D1.7 contract metadata without
  runtime behavior.
- **EP03-AC04:** Port keys, directions, nominal tokens, input cardinality,
  requiredness, parameter keys/value kinds/defaults/constraint metadata, and
  node type IDs are explicit, immutable, and definition-local.
- **EP03-AC05:** Exactly the seven accepted nominal type tokens are used; no
  generic `any` wire, Python class, data format, structural type expression,
  or implicit coercion is introduced.
- **EP03-AC06:** The registry is explicit, static, first-party, immutable,
  and deterministic; duplicate registration fails; no plugin/discovery/code
  execution path exists.
- **EP03-AC07:** The two built-in contract specimens cover the accepted tokens
  but have no operation, runtime, data/ML, UI, or user-facing behavior.
- **EP03-AC08:** The public workflow surface remains small and imports no
  forbidden web/runtime/consumer/discovery code.
- **EP03-AC09:** Tests are inline, synthetic, deterministic, and prove
  definition/registry behavior without claiming P1-EP04 validation.
- **EP03-AC10:** No workflow-instance validation, diagnostics, schema,
  migration, extension compatibility, UI/API, process, persistence,
  execution, data/ML, export, fixture, or Phase 2 behavior is introduced.
- **EP03-AC11:** Baseline setup and the complete post-change final
  attestation—including quality, coverage, inventory, license, advisory,
  clean-copy, lock, and hygiene checks—passes after any worker-caused repair.
- **EP03-AC12:** Both locks remain byte-identical and no dependency,
  manifest, configuration, CI, or package-manager change occurs.
- **EP03-AC13:** Clean-copy evidence and cleanup are bounded, independent of
  OneDrive/repository state, and leave no residue.
- **EP03-AC14:** The implementation report is accurate, sanitized, and
  distinguishes worker evidence, pre-existing work, self-attestation, and
  independent-validation status.
- **EP03-AC15:** A fresh independent validator returns `Accept` with no
  unresolved Critical or High finding.
- **EP03-AC16:** Central explicitly accepts P1-EP03 before P1-EP04 is drafted.

## 11. Independent Validation Contract

A fresh independent validator must:

1. Read every governing input, the D1 and P1-EP02 reconciliations, this
   packet, all Section 7 artifacts, and the implementation report.
2. Independently inspect and challenge type-token exactness, contract
   immutability, defaults versus omission, constraint metadata,
   definition/registration duplicate failures, static-registry behavior,
   public imports, and non-operational specimens.
3. Confirm no contract API can discover/import/execute plugins or operations,
   and no workflow-instance validation/diagnostic behavior is claimed.
4. Reproduce the full final attestation, lock invariance, focused tests,
   clean-copy proof, cleanup, hygiene, and exact file scope.
5. Confirm P1-EP04/P1-EP05/Phase 2 boundaries remain intact.
6. Return exactly `Accept`, `Revise`, or `Blocked` with criterion-linked
   findings and owners.

The validator may not edit files, accept for Central, alter remote state, or
begin P1-EP04.

## 12. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P1_EP03.md` version 0.1 as the bounded node-contract registry worker. Read every governing input, especially the accepted D1.3/D1.4/D1.7 and P1-EP02 reconciliations, and follow the packet exactly. Modify only the five Section 7 paths. Implement only immutable declarative contract values and an explicit static first-party registry, including exactly the two non-operational contract specimens required by the packet. Use only the existing Python 3.14 standard library. Do not add dependencies, locks, fixtures, schemas, workflow-instance validation, diagnostics, migration, plugins/discovery, UI/API/process behavior, execution, persistence, data/ML, export, CI, or remote changes. Keep all tests inline and synthetic. Run the full final attestation; if it finds a worker-caused issue, fix it only within scope and rerun the complete sequence until it passes. Stop with the implementation report and independent-validation handoff; do not self-validate, accept for Central, stage/commit/push, or begin P1-EP04.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P1_EP03.md` version 0.1. Read all governing inputs, the D1 and P1-EP02 reconciliations, every Section 7 artifact, and `ViDAP_P1_EP03_Implementation_Report.md`. Follow Section 11 exactly. Independently verify nominal token exactness, immutable contract metadata, defaults versus omission, constraints, deterministic duplicate failures, static registry behavior, public imports, and the non-operational boundary of both specimens. Confirm no workflow-instance validation, diagnostics, migration, plugins/discovery, UI/API/process behavior, execution, persistence, data/ML, export, or Phase 2 behavior entered. Reproduce the full attestation, unchanged locks, clean-copy proof, cleanup, hygiene, and exact scope. Do not edit files, accept for Central, change remote state, or begin P1-EP04. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

## 13. Next Action

P1-EP03 is complete. Independent validation returned `Accept`, and Central
accepted the result in `ViDAP_P1_EP03_Validation_and_Reconciliation.md` on
2026-09-20. Central may now draft P1-EP04 as a separate bounded packet. This
completion does not authorize P1-EP04 execution or later implementation.
