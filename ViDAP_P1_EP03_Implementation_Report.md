# ViDAP P1-EP03 — Worker Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P1_EP03.md` v0.1 |
| Authorization | Explicit user direction, 2026-09-20; packet `Approved for execution` |
| Role and result | Bounded worker; implementation and worker attestation complete; independent validation pending |

## 1. Authority, inputs, and baseline

Read in full before implementation: the current user direction;
`ViDAP_Overview.txt`; `ViDAP_Phased_Plan_Spine.md` v1.2;
`ViDAP_Roadmap.md` v2.5; `ViDAP_Phase_1_Plan.md` v1.4;
P1-EP01 and P1-EP02 reconciliation records; accepted Phase 0
reconciliations for D0.1–D0.7; `docs/dependency-controls.md`; and this packet.
EP01 and EP02 were present, unsuperseded, and accepted. Their boundaries were
preserved: contracts/registration are declarative; EP04 still owns
workflow-instance validation and diagnostics.

| Baseline item | Recorded state before changes |
|---|---|
| Branch / commit | `main` / `0f81dad284a1f01df0e1fccb25aa9231518bb572` |
| Sanitized remote | One GitHub `origin`; read only and unchanged |
| Pre-existing work | Modified `ViDAP_Phase_1_Plan.md`, `ViDAP_Roadmap.md`; untracked approved packet |
| Output collisions | None for report, `contracts.py`, `registry.py`, or `test_workflow_contracts.py`; existing `__init__.py` permitted to change |
| Prerequisites | Node `v24.21.0`; npm `11.19.0`; normal Windows uv `0.12.16`; locked CPython `3.14.7` |
| uv retry | Restricted uv path was access-denied; normal Windows invocation succeeded |
| `package-lock.json` SHA-256 | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` SHA-256 | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

`npm.cmd run setup` and `npm.cmd run check` passed against the inherited
baseline before the worker change. A new system-temporary location outside the
repository and OneDrive was confirmed for clean-copy proof.

## 2. Authorized implementation and requirement mapping

| Packet requirement | Authorized path and evidence |
|---|---|
| Immutable port, parameter, node, display, token, and default values | `python/src/vidap_workflow/contracts.py`; focused synthetic tests |
| Explicit immutable registry and exactly two specimens | `python/src/vidap_workflow/registry.py`; registry/specimen tests |
| Direct public contract/registry access while retaining EP02 compatibility | `python/src/vidap_workflow/__init__.py`; fresh public-import test |
| Required inline deterministic tests | `python/tests/test_workflow_contracts.py` |

`PortDefinition`, `ParameterDefinition`, `NodeDefinition`, and
`DisplayMetadata` are frozen slot values. The seven accepted nominal tokens,
input cardinalities, JSON-compatible parameter value kinds, and immutable
omitted-default sentinel are explicit. Defaults and constraint metadata are
recursively frozen. Constructors reject malformed type IDs, direction,
cardinality, nominal-token, value-kind, metadata, and duplicate-key definition
errors; they do not inspect workflows, resolve an override/default, apply a
constraint, infer types, or produce diagnostics.

`NodeRegistry` receives explicit `NodeDefinition` values, offers read-only
lookup, and functionally returns a new registry for one explicit addition.
Duplicate type IDs fail deterministically. The registry has exactly two
non-operational specimens: `vidap.kernel.contract-source` declares all seven
outputs; `vidap.kernel.contract-sink` declares all seven inputs and a
defaulted, constrained parameter. Neither has an operation key or runtime.

The existing EP02 `__all__` compatibility tuple remains exact while the
accepted values are available via direct package imports. The new contract and
registry modules use only the standard library; they do not import filesystem,
network, process, web, execution, experiment, export, or plugin/discovery
consumers.

## 3. Tests and final attestation

The focused suite passed 11 inline synthetic tests covering immutability,
tokens/directions/cardinality, explicit versus omitted defaults, constraints,
definition and registration failures, functional non-mutating registration,
specimens, and forbidden imports. It makes no workflow-instance validation,
diagnostic, migration, ordering, data/ML, or export claim.

Three worker-caused check failures were repaired only in Section 7: first,
the accepted EP02 `__all__` assertion required preservation of its exact tuple;
second, deliberate re-exports needed lint-valid re-export syntax; third, a new
test was corrected not to compare a class retained across a deliberate fresh
module import. After each repair, the complete required final attestation was
restarted from its first command.

Final attestation passed in packet order:

1. `npm.cmd run check`: formatting, lint, TypeScript/Python type checks, 10 web
   tests, 25 Python unit tests, build, 3 integration tests, and smoke passed.
2. `npm.cmd run coverage`: 10 web tests and all 28 Python tests passed; Python
   coverage total was 84% (no numeric threshold is required).
3. `npm.cmd run deps:inventory`: locked installed inventory completed.
4. `npm.cmd run license:check`: 431 installed locked packages passed policy.
5. `npm.cmd run deps:audit`: npm and Python scans reported no findings.
6. `git diff --check`: passed.

Both locks were rehashed after attestation and exactly match the recorded
baseline. No manifest, dependency, lock, package-manager policy,
configuration, CI, runtime policy, remote, stage, commit, or push changed.

## 4. Clean-copy proof and bounded cleanup

The first copy was discarded because it included ignored generated caches. A
new copy excluded repository metadata, environments, caches, build output, and
coverage output. Its first locked setup encountered a host-local shared uv
cache hard-link error, so the exact temporary copy was removed after path and
reparse-point checks. This was a host-cache condition, not a source or lock
change.

A fresh copy with an isolated private uv cache inside that bounded location
passed locked setup, all 11 focused contract tests, and `npm.cmd run check`
(zero exit status captured). Both exact temporary proof directories and their
private caches were removed after bounded-path and non-reparse checks. No
temporary copy remains.

## 5. Final scope and hygiene

Worker artifacts are exactly the five Section 7 paths:

- `python/src/vidap_workflow/contracts.py`
- `python/src/vidap_workflow/registry.py`
- `python/src/vidap_workflow/__init__.py`
- `python/tests/test_workflow_contracts.py`
- `ViDAP_P1_EP03_Implementation_Report.md`

The planning-document modifications and packet remain pre-existing work.
Ignored caches/environments/build output are covered by the accepted ignore
rules; no generated artifact is untracked. `.gitattributes` requires LF for
`.py` and `.md`, and `git diff --check` passed. The focused credential-pattern
scan was clear. No repository log or temporary file was found. The harness
ports 8000 and 5173 had no listener after checks.

## 6. Worker self-assessment and validation handoff

**Worker self-assessment only — not independent validation or Central
acceptance.** EP03-AC01 through EP03-AC14 are self-assessed as satisfied by
the recorded authority, scope, contract/registry implementation, test,
attestation, lock, clean-copy, and hygiene evidence. EP03-AC15 and EP03-AC16
remain pending: independent validation must return `Accept`, then Central must
explicitly accept P1-EP03.

Independent validator: follow packet Section 11. Read every governing input,
this report, and all Section 7 artifacts. Independently challenge token
exactness, immutability, defaults/constraints, duplicate errors, registry
behavior, direct imports, and non-operational specimens. Reproduce the full
attestation, locks, clean-copy/cleanup, hygiene, and exact scope. Confirm that
no validation/diagnostics, schema/migration, UI/API/process, persistence,
execution, data/ML, export, fixture, or plugin/discovery behavior entered.
Return exactly `Accept`, `Revise`, or `Blocked` with criterion-linked findings;
do not edit, accept for Central, mutate remote state, or begin P1-EP04.
