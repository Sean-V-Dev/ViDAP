# ViDAP P2-EP02 — Bounded Worker Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P2_EP02.md` version 0.2, approved for worker resumption |
| Worker state | v0.2 implementation and required worker attestation passed; fresh independent revalidation pending |
| Baseline commit | `28c4e0076556aba0cd968585a38f86bc40c0ac7f` |
| Branch | `main`, tracking `origin/main`, no ahead/behind count at baseline |
| Worker output | The five paths authorized by packet Section 7 only |

## Governing baseline and scope

The worker read the approved v0.2 packet and current user direction; the unversioned
`ViDAP_Overview.txt`; Spine v1.3; Roadmap v4.1; Phase 2 Plan v1.4; the
P2-EP01 v0.1 acceptance/reconciliation; Phase 1 Plan v2.3 and all P1
reconciliation records (including D1.1–D1.7, the document, static registry,
validation/diagnostics, strict compatibility, and Phase 1 closeout); Phase 0
Plan v1.9 and all P0 reconciliation records (topology, runtimes, quality,
dependency/license/audit controls, fixtures, and clean-environment policy);
`UX refinement.txt` as Phase 3+ consultative direction; and the existing v0.1
worker report as historical evidence. P2-EP01 and
D2.1–D2.8 were accepted prerequisites. No UX region, layout, or interactive
cache concept was used as Phase 2 meaning.

Before worker changes, the worktree already had modified
`ViDAP_Phase_2_Plan.md` and `ViDAP_Roadmap.md`, plus untracked
`ViDAP_P2_EP01.md`, `ViDAP_P2_EP01_Decision_Report.md`,
`ViDAP_P2_EP01_Validation_and_Reconciliation.md`, and `ViDAP_P2_EP02.md`.
Those pre-existing files were left untouched by the worker, including
Central's v0.2 packet amendment. At v0.2 resumption, the five worker paths
from v0.1 were already present; they were distinguished from the planning
changes above. There were no staged paths.
The target commit was the baseline commit above. The permitted ignored
dependency, cache, coverage, and build state existed separately from tracked
content. Node v24.21.0, npm 11.19.0, uv 0.12.16, and locked CPython 3.14.7
were used. At v0.2 resumption, baseline `npm.cmd run setup` passed. The
restricted environment denied `uv` during baseline `npm.cmd run check`; the
documented normal Windows retry passed the complete check before the v0.2
implementation.

Both lock authorities were recorded before work and remained identical after
all worker checks:

| Lock | SHA-256 before and after |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

The worker changed exactly these authorized paths:

1. `python/src/vidap_execution/__init__.py` — narrow public exports.
2. `python/src/vidap_execution/bindings.py` — frozen opaque static binding
   identifiers, revision, deterministic duplicate rejection, and exact lookup.
3. `python/src/vidap_execution/representation.py` — frozen node/edge/handoff
   values, validation-first preparation, resolved parameters, projection, and
   digest.
4. `python/tests/test_execution_representation.py` — 11 focused unit tests
   using only test-local declarative operational metadata.
5. `ViDAP_P2_EP02_Implementation_Report.md` — this evidence and handoff.

No registry, workflow kernel, manifest, lock, fixture, governing document,
existing test, remote, or other tracked path was changed by the worker.

## Decision-to-contract map

| Accepted decision | Boundary implemented or preserved here |
|---|---|
| D2.1 | `prepare_execution` is one synchronous, importable, in-process function. It has no process lifecycle or invocation. |
| D2.2 | A Phase 1-valid document and explicit `BindingMap` yield a frozen, layout-free representation with separate workflow-semantic digest and relevant contract/validation snapshot reference. Binding keys and revisions are opaque metadata, with no executable target or discovery. |
| D2.3 | Directed edge references are retained, ID-sorted only. No topological rank, schedule, result table, fan-out execution, or failure flow was added. |
| D2.4 | No attempt identity, run record, seed, environment fingerprint, timing, outcome, or artifact reference was added. |
| D2.5 | No persistence, output slot, managed path, write, or cleanup behavior was added to the product code. |
| D2.6 | No cache or reuse key/event exists. The semantic digest is a content identifier for this handoff, not a cache implementation. |
| D2.7 | Phase 1's ordered diagnostics are preserved verbatim on `PreparationFailure`. Binding refusal is a narrow pre-dispatch code, not a runtime-error envelope. |
| D2.8 | Tests use only local declarative node definitions with operation keys and non-callable metadata. No reference operation or fixture is implemented or invoked. |

The workflow-semantic digest is SHA-256 over UTF-8, compact JSON with object
names recursively ordered by RFC 8785's UTF-16 code-unit property rule. The
deterministic projection contains the accepted
`vidap.workflow`/`1.0` envelope, workflow ID, nodes sorted by stable ID with
node ID/type and **resolved** canonical parameters, and directed edges sorted
by edge ID with both node/port endpoints. Optional defaults are resolved from
the validated contract before hashing. Labels, node display metadata, layout,
viewport, JSON member order, and node/edge construction or collection order
are excluded. The operation key and binding revision are static binding
metadata carried by the representation, so changing them changes that value
but not the workflow-semantic digest. Unknown or invalid content is refused by
the Phase 1 boundary, and duplicate IDs are refused before a digest is made.
The projection helper is pure and returns inspection data; it is not a saved
workflow format.

The separate `contract_snapshot_ref` is lowercase SHA-256 hex over an
immutable declarative-contract projection using the same UTF-16 property
ordering and compact UTF-8 JSON encoding. The projection contains
`validationPolicy: "vidap.workflow-validation/1.0"`, `format:
"vidap.workflow"`, `schemaVersion: "1.0"`, and `nodeTypes`. `nodeTypes`
contains each **used** type once, sorted by `typeId`. Each entry contains
`typeId`, `operationKey` (null for absence), `inputs`, `outputs`, and
`parameters`. Ports are sorted by key: inputs carry `key`, `direction`,
`nominalType`, `cardinality`, and `required`; outputs carry `key`, `direction`,
and `nominalType`. Parameters are sorted by key and carry `key`, `valueKind`,
`required`, `defaultPresent`, complete `constraints`, and `default` only when
present. This distinguishes omission from explicit null. Nested default and
constraint arrays retain their Phase 1 order. The projection excludes all
display labels/descriptions, registry insertion order, unused definitions,
document layout, runtime binding targets, source bytes, paths, timestamps,
and diagnostic wording. Preparation calls Phase 1 validation before deriving
the reference. A used contract change can alter `contract_snapshot_ref` and
representation equality while leaving `semantic_digest` unchanged. The
reference records validation provenance; it does not replace validation,
authorize dispatch, or implement caching.

Focused tests prove a valid test-only workflow produces deterministic,
immutable values; nested input mutation cannot change a prepared value;
member/order/label/layout/viewport changes preserve projection, digest, and
representation meaning; workflow identity, node type, parameter/default,
edge identity, and directed-endpoint changes alter the digest or refuse when
invalid; operation key or binding revision changes alter the handoff;
invalid workflows preserve Phase 1 diagnostics; and missing, unbound,
duplicate, or revision-mismatched bindings refuse. A separate non-ASCII
challenge proves RFC 8785 key ordering where Python code-point order differs.
Snapshot tests independently calculate expected hashes; change a used output
port's type, input cardinality/requiredness, and parameter kind/default/
constraints; distinguish omitted from explicit-null defaults; retain
constraint-array order; and confirm display, declaration/registry order, and
unused-type changes leave the reference stable. Existing built-in specimens
remain non-operational. Binding and representation constructors
reject non-static or non-JSON values, and the static source inspection found
no callable target, import-path field, command, URL, dispatcher, scheduler,
cache, output, run, artifact, environment, seed, filesystem, subprocess,
network, UI/API, data/ML, or export behavior in the worker implementation.

## Final ordered worker attestation

These commands ran in packet order against the final v0.2 implementation
tree. All exited successfully:

| Order | Command | Result |
|---:|---|---|
| 1 | `npm.cmd run check` | Pass: formatting, lint, typecheck, 10 web tests, 62 Python unit tests, build, 3 Python integration tests, and loopback smoke. |
| 2 | `npm.cmd run coverage` | Pass: 10 web tests and 65 Python tests; Python total 87% (report-only, no threshold). |
| 3 | `npm.cmd run deps:inventory` | Pass: locked installed inventory produced. |
| 4 | `npm.cmd run license:check` | Pass: policy passed for 431 installed locked packages. |
| 5 | `npm.cmd run deps:audit` | Pass: npm reported zero vulnerabilities; Python reported no known vulnerabilities. |
| 6 | `git diff --check` | Pass: no whitespace errors. |

The focused local suite separately passed all 11 tests. The v0.1 digest
repair and its earlier complete attestation are historical evidence; every
command above was rerun after the v0.2 snapshot implementation. The
`uv`-using commands used the documented normal
Windows execution path after the known restricted-environment denial; no
interpreter or package-manager substitution and no TLS bypass was used.

## Clean-copy, hygiene, and residue evidence

One new disposable copy outside the repository and OneDrive used separate npm
and uv caches after the v0.2 snapshot implementation. It reproduced
`npm.cmd run setup`, all 11 focused tests, and `npm.cmd run check` (including
62 Python unit tests,
3 integration tests, and smoke). The exact copy and both caches were then
removed; an absence check returned true. No absolute temporary or user path
is retained in this report.

Final status inspection separated the two pre-existing modified planning
files and four pre-existing untracked planning/packet files from the five
worker paths. The staging area remained empty. Both lock hashes matched the
baseline. Generated web output, coverage, caches, dependency trees, and
Python environment were ignored state only. No non-ignored PID/log file was
found; neither prescribed loopback port (8000 or 5173) had a listener after
smoke. Worker-file text and scoped sensitive-content hygiene checks were
clean, and `git diff --check` passed. No remote state, commit, or staging
operation was performed.

## v0.1 Revise and v0.2 disposition

The independent validator returned `Revise` with two High findings:

1. **EP02-AC05/11, D2.2 digest ordering:** The earlier encoder used Python
   code-point `sort_keys=True`. That differed from the accepted RFC 8785
   property order for valid non-ASCII keys. The worker changed only the
   authorized representation and focused-test paths, added a supplementary-
   versus-BMP key challenge with an independently constructed expected hash,
   and reran the complete required final attestation and clean-copy proof.
   That repair was present at v0.2 resumption and was retained in the final
   implementation. Both the workflow digest and snapshot reference use the
   accepted UTF-16 property order. Fresh independent recheck remains pending.
2. **EP02-AC01/03/11, D2.2 snapshot reference:** The accepted P2-EP01
   decision and reconciliation require a contract/validation snapshot
   reference. Packet v0.1's required public contract omits its source,
   content, derivation, and relationship to the workflow-semantic digest.
   A read-only challenge changed a registered output port's nominal type and
   obtained equal current representations. Adding an arbitrary reference
   would have made a substitute design decision under v0.1. Central therefore
   clarified and approved v0.2 before this worker resumed. The worker added
   `contract_snapshot_ref` under that exact projection and tested the port
   challenge and other specified contract changes. Fresh independent recheck
   remains pending; the worker did not amend governing documents.

## Independent-validation handoff

The v0.2 worker implementation and final attestation are complete. **Independent
validation and Central acceptance remain pending.** A fresh validator should
read the approved v0.2 packet, governing inputs, and this report, and independently
challenge the five-path scope, Phase 1 validation boundary, semantic digest,
snapshot reference, binding refusals and immutability, all exclusions, locks,
final checks, clean-copy evidence, and hygiene. The validator should return
`Accept`, `Revise`, or `Blocked` with criterion-linked findings. This worker
makes no independent verdict, does not accept P2-EP02 for Central, and does
not begin P2-EP03.
