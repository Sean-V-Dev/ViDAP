# ViDAP P1-EP04 — Validation and Diagnostics

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Execution authorized | 2026-09-20 by explicit user direction, recorded in worker report |
| Completed | 2026-09-21 |
| Packet type | Bounded Python workflow validation implementation |
| Parent phase plan | `ViDAP_Phase_1_Plan.md` version 1.6 |
| Prerequisites | P1-EP01 through P1-EP03 complete |
| Prerequisite reconciliations | `ViDAP_P1_EP01_Validation_and_Reconciliation.md`; `ViDAP_P1_EP02_Validation_and_Reconciliation.md`; `ViDAP_P1_EP03_Validation_and_Reconciliation.md` |
| Workstream | WS1.4 — Semantic validation |
| Authorized worker report | `ViDAP_P1_EP04_Implementation_Report.md` |
| Central reconciliation | `ViDAP_P1_EP04_Validation_and_Reconciliation.md` |
| Created | 2026-09-20 |
| Owner | Central |

---

## 1. Authorization Boundary

This is a draft. It is not executable until Central explicitly approves this
exact version.

Approval would authorize one worker to add deterministic workflow-instance
structural/semantic validation and stable actionable diagnostics on the
accepted document and static-contract layers. The worker may modify only the
Section 7 paths.

This packet does not authorize new workflow document fields, schema artifacts,
version migration, fixture files, UI/editor/forms, HTTP/API binding,
persistence, process launch, dependency-order planning, caching, data/ML
operations, export, dynamic extension loading, dependencies/locks, CI,
remote mutation, or P1-EP05 and later work.

## 2. Plain-English Packet Intent

### What this packet will build

It adds one deterministic answer to the question, “Is this workflow ready for
a future runner?” Rather than returning only yes/no or throwing raw errors, it
returns an ordered set of plain-English, machine-identifiable findings that
point to the affected workflow element and suggest a repair.

### What it will not build

Validation does not run a workflow, pick a schedule, execute an operation,
load data, render an error, save a document, or send a response over HTTP. It
also does not define migrations or use fixtures to claim broader compatibility.

### How success will be demonstrated

Inline synthetic tests will prove valid workflow acceptance and deterministic,
actionable diagnostics for duplicate identities, unknown nodes/ports,
direction/type/cardinality/required-input failures, invalid parameter values,
and cycles. Equivalent construction/layout/order variants must receive the
same semantic validation outcome.

## 3. Governing Inputs

The worker and validator must read:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially OV §§6–7, 16, 18–19, 21–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.2, especially invariants 3–4,
   10–13 and Phase 1/Phase 2 boundaries.
4. `ViDAP_Roadmap.md` version 2.7, especially P1 and its next action.
5. `ViDAP_Phase_1_Plan.md` version 1.6, especially D1.5, WS1.4, Sections
   7–10, and P1 acceptance criteria.
6. `ViDAP_P1_EP01_Validation_and_Reconciliation.md`, authoritative for
   D1.3–D1.6 diagnostic/compatibility decisions.
7. `ViDAP_P1_EP02_Validation_and_Reconciliation.md` and
   `ViDAP_P1_EP03_Validation_and_Reconciliation.md`, authoritative for the
   accepted document kernel and contract/registry boundaries.
8. Accepted Phase 0 decisions for Python 3.14/uv, root quality/dependency
   controls, fixtures, and hygiene.
9. This packet.

## 4. Inherited Validation Contract

The implementation must preserve the accepted D1.5 model:

1. `validate_workflow(document, registry)` is a pure, deterministic Python
   operation returning an ordered immutable collection of diagnostics. An
   empty collection means valid.
2. Diagnostics have stable code, severity, category, affected-element
   reference, plain-English message, plain-English remedy, and optional
   non-contract technical detail or JSON Pointer location.
3. Categories are exactly `structural`, `semantic`, and `unsupported`.
   Initial validation findings use severity `error`; the value model may
   represent `warning` without treating warnings as validity.
4. Structural validation precedes semantic validation. It reports duplicate
   node/edge identities and exact duplicate edges without depending on UI
   order or execution behavior.
5. Semantic validation uses the static registry to check known node types,
   known ports and direction, exact nominal type matching, input cardinality,
   required inputs, parameter keys, required/default handling, parameter
   value kinds, supported declarative constraints, and directed acyclicity.
6. An absent node type or unsupported constraint vocabulary is visibly
   `unsupported`; it is never auto-installed, substituted, or silently
   treated as valid.
7. Layout, viewport, construction order, collection order, JSON member order,
   labels, and execution concerns cannot change semantic validation outcome.
8. The validator does not mutate a document, resolve defaults into it, repair
   content, throw raw validation exceptions as its public result, choose a
   dependency order, or invoke an operation key.
9. P1-EP05 remains responsible for version/migration and representative
   workflow/fixture proof. This packet preserves the current `1.0` document
   boundary but does not implement migration or an extension-compatibility
   policy.

## 5. Required Validation Vocabulary

Stable diagnostic codes must use the `VIDAP-` prefix and remain documented in
source/test constants. At minimum, implement distinct codes for:

| Area | Required diagnostic coverage |
|---|---|
| Structural | duplicate node ID, duplicate edge ID, duplicate exact edge |
| Unsupported | unknown node type, unsupported parameter-constraint key |
| Endpoints | dangling node, unknown port, reversed direction |
| Connections | nominal-type mismatch, input cardinality exceeded, missing required input |
| Parameters | unknown key, missing required parameter, wrong declared kind, declared constraint violation |
| Graph | directed cycle |

The initial declarative parameter-constraint vocabulary is:

- `allowedValues`;
- `minimum` and `maximum` for numeric values;
- `minLength`, `maxLength`, and `pattern` for strings;
- `minItems`, `maxItems`, and `uniqueItems` for arrays;
- `requiredKeys` for object values; and
- `nullable` for any declared value kind.

Constraints apply only when a parameter is present or has a contract default;
the implementation reports findings but does not modify parameter maps. A
constraint irrelevant to its value kind is an unsupported contract condition,
not an ignored hint. Regex checks use Python's standard library only and must
fail visibly for invalid pattern metadata.

## 6. Required Implementation

### 6.1 Diagnostic values and public API

Add immutable diagnostic values under `python/src/vidap_workflow/` with
explicit fields for code, severity, category, affected-element kind/reference,
message, remedy, optional JSON Pointer, and optional technical detail. Expose
a small pure `validate_workflow` public function. It must accept a
`WorkflowDocument` and `NodeRegistry` and return diagnostics rather than
raising for ordinary invalid workflow state.

Diagnostics must have a stable deterministic ordering independent of
construction/collection/layout order. Keep their human-facing text concise,
actionable, and free of source paths, environment data, stack traces, or raw
exception exposure.

### 6.2 Structural and semantic checks

Implement only the checks named in Sections 4–5. A validator may report
multiple independent errors in a single pass, but it must avoid misleading
cascade errors when a prerequisite is unknown. For example, an edge endpoint
on an unknown node must not also be reported as a known-port type mismatch.

The implementation must:

- identify duplicate workflow IDs/edges and exact duplicate edges even though
  the immutable document model canonicalizes collection order;
- resolve each node type only against the supplied static registry;
- resolve endpoint ports only after a known node type is available;
- require output-to-input direction, exact nominal-token equality, and
  `one` input cardinality compliance;
- identify required input ports lacking a valid compatible incoming edge;
- evaluate parameter override/default state against the definition without
  mutating document values;
- use only the Section 5 constraint vocabulary; and
- detect directed cycles as invalid graph semantics without exposing or
  retaining a topological order.

No code in this packet may read/write a workflow file, call a node operation,
import a runtime/UI/consumer package, create a process, access a network, or
use the validation result to trigger behavior.

### 6.3 Tests

Use inline synthetic values and the two accepted non-operational specimen
definitions. Do not add a fixture. Tests must prove:

1. A valid source-to-sink workflow covering the nominal types has no
   diagnostics.
2. Each required code class in Section 5 yields an `error` diagnostic with
   stable code/category/affected element, plain-English message, and remedy.
3. Unknown nodes and unsupported constraint keys are `unsupported`, not
   silently valid.
4. Wrong direction/type/cardinality/missing input cases are separately tested.
5. Required/unknown/wrong-kind/default/constraint parameter cases are
   separately tested without parameter mutation.
6. A cycle is diagnosed without an execution-order claim.
7. Layout, construction order, collection order, and JSON member ordering do
   not change the ordered semantic diagnostic collection.
8. Diagnostics and validation results are immutable, deterministic, and
   public imports do not pull web, execution, experiment, export, FastAPI,
   Uvicorn, filesystem, subprocess, network, or plugin/discovery code.
9. No test claims version migration, extension compatibility, a UI/API error
   envelope, persistence, real data/ML operation, export, or Phase 2
   scheduling/caching behavior.

## 7. Exact Authorized Repository Outputs

The worker may create or modify only:

| Path | Authorized purpose |
|---|---|
| `python/src/vidap_workflow/contracts.py` | Define/freeze the accepted parameter-constraint vocabulary only. |
| `python/src/vidap_workflow/diagnostics.py` | Immutable diagnostic values and stable code/category/severity constants. |
| `python/src/vidap_workflow/validation.py` | Pure structural/semantic validator only. |
| `python/src/vidap_workflow/__init__.py` | Deliberate diagnostic/validation public exports only. |
| `python/tests/test_workflow_validation.py` | Inline synthetic tests required by Section 6.3. |
| `ViDAP_P1_EP04_Implementation_Report.md` | Sanitized worker evidence and self-attestation. |

No other path may be created, modified, moved, staged, committed, or deleted.
Do not modify the document/serialization, registry, existing test, manifest,
lock, configuration, CI, fixture, web, execution/experiment/export, governing,
or prior reconciliation paths.

## 8. Required Execution Sequence and Final Attestation

After explicit approval, the worker must:

1. Read every governing input and record the baseline, pre-existing work,
   output collisions, and both lock hashes.
2. Run `npm.cmd run setup` and `npm.cmd run check` against the inherited
   baseline. Stop if either fails before the worker change.
3. Implement only Section 7. Keep all test values inline and synthetic.
4. Run focused Python tests while implementing. Then run the complete final
   attestation in this order:
   - `npm.cmd run check`;
   - `npm.cmd run coverage`;
   - `npm.cmd run deps:inventory`;
   - `npm.cmd run license:check`;
   - `npm.cmd run deps:audit`; and
   - `git diff --check`.
5. If a final check identifies a worker-caused issue, fix it only within
   Section 7 and rerun the *entire* final attestation from the first command.
   Do not report completion unless every command passes. Stop with evidence if
   a failure is unrelated or needs broader authority.
6. Confirm both locks remain byte-identical; inspect exact scope, ignored
   state, text policy, sensitive-content scan, and no listener/log/cache/
   environment/temporary-copy residue.
7. In a new clean copy outside the repository and OneDrive, run locked setup,
   focused validation tests, and `npm.cmd run check`; verify results and
   safely remove only the exact bounded temporary copy/caches.
8. Write the implementation report and stop for independent validation. Do
   not self-validate, stage, commit, push, alter remote state, or begin
   P1-EP05.

## 9. Required Worker Evidence

The report must include:

1. Packet/version/approval, governing inputs, baseline, sanitized remote,
   pre-existing work, exact output scope, and collision evidence.
2. Before/after lock hashes and confirmation that no dependencies/manifests/
   locks/configuration/CI/runtime policy changed.
3. Requirement-to-path/test mapping for Sections 4–6.
4. The diagnostic taxonomy/codes and validation stages, with representative
   plain-English examples but no excessive logs.
5. Evidence that diagnostics are ordered, immutable, actionable, and remain
   separate from raw decode errors and later UI/API representation.
6. Focused-test and complete final-attestation results, including any repair/
   rerun cycle.
7. Clean-copy setup/test/check and bounded cleanup evidence.
8. Scope, hygiene, sensitive-content, ignored-state, listener, and final Git
   evidence.
9. Criterion-by-criterion worker self-assessment clearly labeled as not
   independent validation or Central acceptance.

## 10. Acceptance Criteria

P1-EP04 may be accepted only when:

- **EP04-AC01:** Authority, prerequisites, accepted decisions, baseline,
  pre-existing work, locks, and exact scope are recorded accurately.
- **EP04-AC02:** Only the six Section 7 paths are changed/created by the
  worker, with no unauthorized/generated residue.
- **EP04-AC03:** Diagnostics are immutable, structured, deterministic, and
  have the accepted stable fields and ordered collection behavior.
- **EP04-AC04:** Structural, semantic, and unsupported categories are
  distinct; invalid workflow state returns findings rather than raw validator
  exceptions or a bare boolean.
- **EP04-AC05:** All required duplicate/endpoint/connection/parameter/cycle
  conditions have actionable stable diagnostic coverage.
- **EP04-AC06:** Exact nominal type matching, input cardinality, required
  inputs, defaults, and supported constraint vocabulary are evaluated without
  mutating the workflow or executing behavior.
- **EP04-AC07:** Unknown node types and unsupported constraint metadata fail
  visibly as unsupported and are never auto-installed, substituted, ignored,
  or silently accepted.
- **EP04-AC08:** Layout, viewport, labels, construction order, collection
  order, and JSON object-member order cannot alter semantic diagnostics.
- **EP04-AC09:** No version migration, extension compatibility, fixture,
  UI/API, process, persistence, execution plan/cache, data/ML, export,
  plugin/discovery, or Phase 2 behavior is introduced.
- **EP04-AC10:** Tests are inline, synthetic, deterministic, and prove the
  required validation/diagnostic behavior without a browser, server, network,
  process, or real operation.
- **EP04-AC11:** Baseline setup and complete post-change final attestation,
  including quality, coverage, inventory, license, advisory, clean-copy,
  lock, and hygiene checks, pass after any worker-caused repair.
- **EP04-AC12:** Locks remain byte-identical and no dependency, manifest,
  configuration, CI, package-manager, or runtime policy change occurs.
- **EP04-AC13:** Clean-copy evidence/cleanup is bounded and leaves no
  residue.
- **EP04-AC14:** The implementation report is accurate, sanitized, and
  distinguishes worker evidence, pre-existing work, self-attestation, and
  independent-validation status.
- **EP04-AC15:** A fresh independent validator returns `Accept` with no
  unresolved Critical or High finding.
- **EP04-AC16:** Central explicitly accepts P1-EP04 before P1-EP05 is drafted.

## 11. Independent Validation Contract

A fresh independent validator must:

1. Read every governing input, all prerequisite reconciliations, this packet,
   all Section 7 artifacts, and the implementation report.
2. Independently challenge every required diagnostic class, ordering/
   immutability/layout invariance, supported constraint behavior, and
   prevention of cascaded misleading diagnostics.
3. Confirm validation is pure/non-mutating and cannot execute operations,
   choose a schedule, import consumers, or expose an HTTP/UI error contract.
4. Reproduce full attestation, lock invariance, focused tests, clean-copy
   proof, cleanup, hygiene, and exact scope.
5. Verify P1-EP05 and Phase 2 boundaries remain intact.
6. Return exactly `Accept`, `Revise`, or `Blocked` with criterion-linked
   findings and owners.

The validator may not edit files, accept for Central, alter remote state, or
begin P1-EP05.

## 12. Fresh-Chat Handoff Prompts

### Execution worker prompt

> Execute approved `ViDAP_P1_EP04.md` version 0.1 as the bounded validation-and-diagnostics worker. Read every governing input and the accepted P1-EP01 through P1-EP03 reconciliations, then follow the packet exactly. Modify only the six Section 7 paths. Implement only the pure deterministic workflow-instance validator and immutable actionable diagnostic values required by the packet, using the existing document and static registry. Do not add dependencies, locks, schemas, migrations, fixtures, UI/API/process behavior, persistence, execution ordering/caching, data/ML, export, plugin/discovery, CI, or remote changes. Keep tests inline and synthetic. Run the full final attestation; if it finds a worker-caused issue, fix it only within scope and rerun the complete sequence until it passes. Stop with the implementation report and independent-validation handoff; do not self-validate, accept for Central, stage/commit/push, or begin P1-EP05.

### Independent validator prompt

> Act as the independent validator for approved `ViDAP_P1_EP04.md` version 0.1. Read all governing inputs, all prerequisite reconciliations, every Section 7 artifact, and `ViDAP_P1_EP04_Implementation_Report.md`. Follow Section 11 exactly. Independently challenge every diagnostic class, code/category/actionability, ordering/immutability/layout invariance, parameter/default/constraint behavior, unknown/unsupported handling, and prevention of misleading cascades. Confirm validation is pure and cannot execute operations, choose a schedule, import consumers, or expose HTTP/UI behavior. Reproduce full attestation, unchanged locks, clean-copy proof, cleanup, hygiene, and exact scope. Do not edit files, accept for Central, change remote state, or begin P1-EP05. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

## 13. Next Action

P1-EP04 is complete. Independent validation returned `Accept`, and Central
accepted the result in `ViDAP_P1_EP04_Validation_and_Reconciliation.md` on
2026-09-21. Central may now draft P1-EP05 as a separate bounded packet. This
completion does not authorize P1-EP05 execution or later implementation.
