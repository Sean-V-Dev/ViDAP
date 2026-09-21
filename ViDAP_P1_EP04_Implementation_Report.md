# ViDAP P1-EP04 — Worker Implementation Report

| Field | Evidence |
|---|---|
| Packet | `ViDAP_P1_EP04.md` version 0.1 |
| Worker authority | Current explicit user direction: execute the approved packet as the bounded worker |
| Worker result | Implementation and required worker attestation complete; awaiting independent validation |
| Branch / baseline revision | `main` / `af8059303dfc5f76fed279a504f43ebacb6a0be4` |
| Sanitized remote state | A configured origin was present; no remote operation was performed. |

## 1. Authority, governing inputs, and baseline

The packet file still described v0.1 as a draft, but the current explicit user
direction expressly approved execution of that exact packet. Under the approved
authority order, that direction authorized this bounded work only.

Before implementation, the worker read the packet; `ViDAP_Overview.txt`;
`ViDAP_Phased_Plan_Spine.md` v1.2; `ViDAP_Roadmap.md` v2.7;
`ViDAP_Phase_1_Plan.md` v1.6; P1-EP01, P1-EP02, and P1-EP03 reconciliation
records; and the accepted Phase 0 plan/reconciliation inputs governing CPython
3.14/uv, locked quality controls, fixtures, and hygiene. The accepted handoff
is a UI-independent document kernel, immutable static contracts/registry, and
no workflow-instance validation before this packet.

The baseline contained these unrelated, pre-existing changes, which were
preserved:

- modified: `ViDAP_P1_EP03.md`, `ViDAP_Phase_1_Plan.md`, and
  `ViDAP_Roadmap.md`;
- untracked: `ViDAP_P1_EP03_Validation_and_Reconciliation.md` and
  `ViDAP_P1_EP04.md`.

None of the six authorized EP04 outputs existed at baseline. The initial and
final SHA-256 hashes match for both lock authorities:

| Lock | SHA-256 before and after |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

`npm.cmd run setup` passed at baseline. The restricted environment initially
denied the locked Python formatter during `npm.cmd run check`; the same
unchanged baseline check passed using the normal Windows permission path.

## 2. Exact implementation scope

Only the six packet-authorized paths were created or modified by this worker:

- `python/src/vidap_workflow/contracts.py`
- `python/src/vidap_workflow/diagnostics.py`
- `python/src/vidap_workflow/validation.py`
- `python/src/vidap_workflow/__init__.py`
- `python/tests/test_workflow_validation.py`
- this report

No dependency, manifest, lock, configuration, CI, fixture, governing document,
runtime policy, remote state, staged content, commit, or push was changed.

## 3. Delivered validation model

`Diagnostic` is an immutable structured value with stable `VIDAP-` code,
severity, category, affected-element kind/reference, concise plain-English
message and remedy, plus optional JSON Pointer and technical detail. The pure
`validate_workflow(document, registry)` function returns an ordered immutable
tuple; it does not mutate a document, resolve defaults into it, execute an
operation, choose a schedule, access files or the network, or expose raw
validation exceptions as an invalid-workflow result.

The validator orders structural findings before unsupported findings before
semantic findings, then uses stable code and element sort keys. It covers:

- structural duplicate node IDs, edge IDs, and exact endpoint-pair edges;
- unsupported node types and parameter constraint vocabulary/metadata;
- dangling nodes, unknown ports, reversed directions, nominal type mismatch,
  one-input cardinality, and missing required inputs;
- unknown/missing/wrong-kind parameters, contract defaults without mutation,
  all accepted declarative constraints, invalid regex metadata, and directed
  cycles.

For example, a missing required input says which `node-id:port` needs one
compatible incoming edge; an unknown type explains that it must be registered
or replaced. Endpoint processing stops before port/type checks when a node or
contract prerequisite is unknown, avoiding misleading cascades.

## 4. Requirement-to-path/test mapping

| Packet requirement | Implementation | Inline synthetic evidence |
|---|---|---|
| Immutable stable diagnostics and public pure API | `diagnostics.py`, `validation.py`, `__init__.py` | structure, immutability, import-boundary tests |
| Frozen accepted constraint vocabulary | `contracts.py` | exact vocabulary assertion and constraint cases |
| Structural, unsupported, endpoint, connection, and cycle checks | `validation.py` | valid workflow; structural; unsupported; endpoint; connection; cycle tests |
| Parameter/default/kind/constraint behavior without mutation | `validation.py` | parameter and all-vocabulary constraint tests |
| Determinism independent of construction, collection, layout, and member order | `validation.py` | layout/construction/collection invariance test |
| No consumer/runtime imports | `__init__.py`, `validation.py` | guarded public-import test |

All test values are inline and synthetic. No fixture, workflow file I/O, UI/API,
persistence, execution planning/caching, data/ML operation, export, migration,
extension policy, or plugin/discovery behavior was introduced.

## 5. Worker test and attestation evidence

Focused implementation checks passed after three worker-local repairs (a
constraint-vocabulary tuple/set expression, static typing around frozen JSON
values, and object-valued array support for `uniqueItems`):

- focused validation suite: 13 passed;
- focused formatting, Ruff lint, and strict mypy: passed.

The complete final attestation passed in the packet-required order:

1. `npm.cmd run check`
2. `npm.cmd run coverage`
3. `npm.cmd run deps:inventory`
4. `npm.cmd run license:check`
5. `npm.cmd run deps:audit` — no JavaScript or Python advisory finding
6. `git diff --check`

The third repair was identified after an earlier green attestation; per packet
instruction, the worker reran this entire sequence from `npm.cmd run check`.
The results listed above are that final rerun.

### Post-validation revision

Fresh independent review found that conflicting duplicate node definitions
could select their semantic representative by collection order. The worker
revised `validation.py` to select a duplicate-ID representative using a stable
semantic key (ID, type, and recursively ordered parameter values, excluding
labels and layout). An inline regression test proves the same diagnostics for
reversed conflicting duplicate definitions. The complete attestation and
fresh clean-copy reproduction passed after this revision (14 focused validation
tests passed in the clean copy), and both bounded temporary paths were removed.
A fresh independent validator must assess the final result.

The final commands used normal Windows permissions because the restricted
environment denies access to the locked Python toolchain. This is an execution
environment distinction, not a repository change.

## 6. Clean-copy, lock, and hygiene evidence

A temporary clean copy outside both the repository and OneDrive completed
locked setup, the focused validation suite (13 passed), and `npm.cmd run
check`. Its first setup attempt exposed an inherited shared uv-cache hardlink
error. The worker removed only that temporary copy's partial virtual
environment, retried with one bounded temporary uv cache, and the retry passed.
Both exact temporary paths were then verified removed.

Final checks confirmed the unchanged lock hashes above, the exact worker scope
plus the named pre-existing work, clean whitespace, expected ignored generated
state, no packet-related listener, no `htmlcov` residue, and no sensitive
content match in the five code/test outputs. No temporary copy/cache created by
this packet remains. Existing ignored local generated directories were neither
tracked nor altered as worker scope.

## 7. Worker self-assessment — not independent validation or Central acceptance

| Criterion group | Worker self-assessment |
|---|---|
| EP04-AC01 to AC02 | Evidence records authority, baseline, locks, pre-existing work, and exact six-path scope. |
| EP04-AC03 to AC08 | Immutable deterministic diagnostics and the required structural, semantic, unsupported, parameter, cycle, and invariance behavior are implemented and tested. |
| EP04-AC09 to AC10 | Scope remains non-operational and tests are inline, synthetic, deterministic, and consumer-free. |
| EP04-AC11 to AC13 | Baseline/setup, final attestation, locks, hygiene, and clean-copy evidence passed. |
| EP04-AC14 | This report distinguishes worker evidence from independent validation. |
| EP04-AC15 to AC16 | Pending: a fresh independent validator and Central acceptance are required. |

## 8. Independent-validation handoff

Independent validator: read every governing input, all Section 7 artifacts,
and this report. Reproduce the packet Section 11 challenges, including every
diagnostic class, stable ordering/immutability, layout/order invariance,
parameter defaults and constraints, unknown/unsupported handling, no-cascade
behavior, purity/import boundaries, complete attestation, unchanged locks,
clean-copy evidence, cleanup, hygiene, exact scope, and preserved P1-EP05 /
Phase 2 boundaries. Do not edit files, accept for Central, change remote state,
or begin P1-EP05. Return exactly `Accept`, `Revise`, or `Blocked` with
criterion-linked findings and owners.
