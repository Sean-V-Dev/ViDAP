# ViDAP P1-EP05 — Worker Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P1_EP05.md` version 0.1 |
| Approval | Explicit user direction, 2026-09-21 |
| Baseline | `main` at `af8059303dfc5f76fed279a504f43ebacb6a0be4` |
| Remote | `origin` configured as a GitHub HTTPS repository (sanitized) |
| Worker status | Evidence complete; independent validation pending |

## Preconditions and baseline

Before implementation, I read the approved packet, `ViDAP_Overview.txt`,
Spine v1.2, Roadmap v3.0, Phase 1 Plan v1.9, P1-EP01–P1-EP04
reconciliations, the Phase 0 plan, and D0.7’s accepted reconciliation.
The exact packet was approved; all four prerequisites were accepted and
unsuperseded. Node 24/npm and locked CPython 3.14 were callable.

`npm.cmd run setup` passed. The sandbox denied `uv.exe` during the first
aggregate check; retrying through the normal Windows `uv.exe` path and then
the full elevated check passed, proving a sandbox restriction rather than a
project prerequisite failure. The fixture baseline was one 483-byte synthetic
fixture. All four new fixture paths, the report, and the new test were absent.
A bounded clean-copy location outside the repository and OneDrive was available.

Pre-existing user work was preserved: modified P1 planning documents,
`contracts.py`, and `__init__.py`; untracked EP03/EP04 records and source/test
files; and the approved EP05 packet. No worker staging, commit, push, remote
mutation, dependency/lock/configuration/CI change, or next-packet work occurred.

## Scope and behavior

Only the ten Section 7 outputs were changed by this worker: the three
authorized workflow source files, one new compatibility test, four named JSON
fixtures, their manifest, and this report.

`validate_workflow_text(text, registry)` is a pure public workflow-package
import. It returns the existing immutable ordered diagnostics tuple, never a
parser exception or boolean. It has no document mutation, file I/O, UI/API,
network, process, persistence, execution, data/ML, export, plugin/discovery,
migration, second-version, or unknown-content-preservation behavior.

| Condition | Stable outcome |
|---|---|
| Exact `vidap.workflow` / `1.0` | Decode and normal validation |
| Missing, malformed, older, future version | `VIDAP-UNSUPPORTED-VERSION` / `unsupported` |
| Malformed JSON, non-object root, duplicate name | Structural diagnostic |
| Malformed non-version envelope | `VIDAP-MALFORMED-ENVELOPE` / `structural` |
| Unknown core field | `VIDAP-UNKNOWN-CORE-FIELD` / `structural` |
| `1.0` extension content | `VIDAP-UNSUPPORTED-EXTENSION` / `unsupported` |
| Unknown node | `VIDAP-UNKNOWN-NODE-TYPE` / `unsupported` |

| Requirement | Path/test evidence |
|---|---|
| Strict text boundary and no migration | `serialization.py`, `validation.py`, `__init__.py`; version tests |
| Unknown core/extension rejection | `serialization.py`; core-field and extension tests |
| Valid/invalid/branched/versioned examples | Four fixtures; expected-outcome tests |
| Integrity/provenance/consumer policy | Manifest test recalculates bytes and SHA-256 |
| Deterministic round trips/member order | Valid-fixture test |
| Prohibited behavior absent | Non-mutation/static-import test; retained suite |

## Fixtures

All fixtures are synthetic UTF-8 JSON and non-product test consumers. They
contain only IDs, static contract type names, and metadata; no personal,
sensitive, credential, path, network, telemetry, proprietary, or dataset
content. Every manifest record declares provenance, MIT terms, creation method,
expected result, permitted consumers, privacy attestation, Central reviewer,
and review date.

| Fixture | Bytes | SHA-256 | Expected result |
|---|---:|---|---|
| `valid-branched-v1.json` | 3378 | `11D3D5FCBBC66C2A5D038AF1A52A32DF7381AD33D3F143BDF2E18D23BB3C7299` | valid deterministic round trip |
| `invalid-unknown-node-v1.json` | 217 | `D89B09B97F7E3B4D0BE569EAAB8ACEF3A01245AB67F19E1A95ED8601A19C1DE8` | `VIDAP-UNKNOWN-NODE-TYPE` |
| `invalid-unknown-core-field-v1.json` | 153 | `3F5B2FF6E535006C457B4EF6B4A190EC9DBD0D498582A5108A7F9BEAD379380D` | `VIDAP-UNKNOWN-CORE-FIELD` |
| `unsupported-schema-version-v2.json` | 124 | `8B49BD802C3A9E48E831D47850A905AD6B5F4D1A5F0131BA32787E06872F2B1D` | `VIDAP-UNSUPPORTED-VERSION` |

The EP05 four-fixture total is 3872 bytes; all repository fixtures total 7808
bytes, below 64 KiB. Exact manifest byte/hash comparisons passed. The valid
fixture has one source, two sinks, 14 compatible edges, branches `table` to
both sinks, and satisfies every required sink input using only the accepted
non-operational contract specimens.

## Tests, attestation, and hygiene

Focused compatibility tests passed: 12 passed. Initial formatting found only
worker-created formatter changes and was repaired mechanically. The first
final aggregate run found that changing legacy `__all__` violated an inherited
EP02 test; the new entry stays an explicit import while `__all__` was restored.
The full required attestation then restarted and passed:

| Command | Result |
|---|---|
| `npm.cmd run check` | Passed: format, lint, types, 51 unit tests, build, 3 integration tests, smoke |
| `npm.cmd run coverage` | Passed: 54 Python tests, 87% total coverage |
| `npm.cmd run deps:inventory` | Passed; inventory only |
| `npm.cmd run license:check` | Passed |
| `npm.cmd run deps:audit` | Passed; no npm/Python advisory finding |
| `git diff --check` | Passed |

Both locks are byte-identical before/after: `package-lock.json`
`FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA`,
and `python/uv.lock`
`AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355`.
No dependency, manifest, configuration, CI, or runtime-policy path changed.
Targeted sensitive-content scanning found no worker-path hit. Generated build,
coverage, virtual-environment, and compiler/test caches remain ignored state,
not untracked work. The smoke listener was cleaned; no relevant listener or
temporary-copy/cache residue remains.

The first temporary setup hit a Windows shared-cache hardlink conflict. A
second attempt put its cache inside the copy, which lint correctly rejected.
Both bounded copies were removed. A fresh copy with a separate sibling cache
then passed locked setup, 12 focused tests, fixture integrity, and the full
`npm.cmd run check`; both exact temporary paths were verified removed.

## Worker self-assessment — not independent validation or Central acceptance

| Criterion | Assessment |
|---|---|
| EP05-AC01 through EP05-AC15 | Evidence supplied; worker assesses compliant |
| EP05-AC16 | Pending fresh independent-validator `Accept` |
| EP05-AC17 | Pending separate Central acceptance |

This is worker evidence only. It does not independently validate or accept
P1-EP05, and P1-EP06 has not begun.

## Independent-validation handoff

Follow packet Section 11: read every governing input, reconciliation, Section
7 output, and this report; independently reproduce strict diagnostics, fixture
integrity/consumer limits, deterministic branching/member-order behavior, locks,
full attestation, clean-copy proof, hygiene, and exact scope. Return exactly
`Accept`, `Revise`, or `Blocked` with criterion-linked findings.
