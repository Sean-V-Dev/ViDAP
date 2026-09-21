# ViDAP P1-EP06 — Phase 1 Evidence Closeout: Worker Report

| Field | Evidence |
|---|---|
| Packet | `ViDAP_P1_EP06.md` v0.1 |
| Authority | Current explicit user direction; packet status is `Approved — execution authorized` |
| Role | Bounded evidence worker only; not independent validation or Central acceptance |
| Sole worker repository output | This report |
| Baseline | `main` at `af8059303dfc5f76fed279a504f43ebacb6a0be4` |
| Remote | One configured remote; untouched |

## Authority, inputs, prerequisites, and baseline

The worker read the approved packet and current direction; the full product
overview; Spine v1.2; Roadmap v3.3; Phase 1 Plan v2.2; Phase 0 Plan v1.9;
accepted P0 decisions/reconciliations; all P1-EP01–EP05 packets, worker
reports, and reconciliations; current package/tasks and lock authorities;
dependency controls; ignore/attribute policy; CI; workflow source/tests; and
the P1-EP05 fixtures and manifest.

EP01 through EP05 are present and unsuperseded. Their reconciliation records
respectively accept D1.1–D1.7, the document kernel, static contracts/registry,
validation/diagnostics, and strict compatibility/controlled fixture proof.
This historical acceptance is not a substitute for the current reproduction.

Before this report, preserved pre-existing work included modified planning and
workflow-package paths and untracked EP03–EP06 packets/evidence, P1-EP05
fixtures, and workflow compatibility/validation paths. The report path was
absent. None of that pre-existing work is attributed to EP06; nothing was
staged, committed, pushed, deleted, or remotely changed.

| Lock authority | SHA-256 before | SHA-256 after final attestation |
|---|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

The sandbox denied direct access to the locked Python toolchain. The required
normal-Windows retry completed locked setup and the required checks; this is a
known execution-environment restriction, not a project or lock failure.

## Decision and layer reconciliation

| Decision | Accepted and reproduced boundary |
|---|---|
| D1.1 | Open UTF-8 JSON `vidap.workflow`, exact version `1.0`, stable serialization; no UI or validator aid is semantic authority. |
| D1.2 | Stable lowercase UUIDv4 workflow/node/edge IDs and directed endpoints; layout, member order, and creation order are non-semantic. |
| D1.3 | Exact nominal tokens: `table`, `target`, `split`, `model`, `predictions`, `metrics`, `artifact`; no implicit conversion. |
| D1.4 | Immutable declarative port/node/parameter contracts; defaults and constraints are contract-owned. |
| D1.5 | Pure ordered immutable `VIDAP-` diagnostics: structural, semantic, and unsupported categories, with affected element and plain-English remedy. |
| D1.6 | Only `vidap.workflow`/`1.0`; strict visible rejection, no migration, fallback, or unknown-content acceptance. |
| D1.7 | Explicit immutable first-party registry; no discovery, dynamic loading, marketplace, or code execution. |

Workflow/schema owns document meaning, serialization, contracts, compatibility,
and validation. Layout is presentation metadata only. The two registry
specimens are explicitly non-operational. Execution semantics/scheduling,
intermediate representation, run identity, caching/artifacts, persistence,
runtime failure behavior, UI/API/editor, and export remain unselected and
outside Phase 1.

## P1 acceptance traceability and current evidence

| Criterion | Accepted evidence | Current reproduction and limitation | Result |
|---|---|---|---|
| P1-AC01 | EP01 reconciliation | D1.1–D1.7 chain checked; no new decision made | Supported |
| P1-AC02 | EP02, EP05 | Programmatic frozen values serialize/deserialize canonical JSON; valid fixture round-trips | Supported; no UI/process needed |
| P1-AC03 | EP02, EP04 | UUID/endpoints and duplicate/dangling diagnostics in source/tests | Supported; not scheduling |
| P1-AC04 | EP03 | Immutable contracts, seven tokens, static registry specimens | Supported; declarations only |
| P1-AC05 | EP04 | Direction/type/cardinality/required-input/parameter diagnostic coverage | Supported; no runtime operation |
| P1-AC06 | EP02, EP04, EP05 | Layout, member, collection, and construction order invariance tests | Supported; future execution meaning deferred |
| P1-AC07 | EP02, EP05 | Valid, invalid, branched, versioned fixtures and deterministic round trips | Supported; fixtures are evidence consumers |
| P1-AC08 | EP01, EP05 | Missing/malformed/older/future/core/extension/node content visibly fails | Supported; no migration/future-reader claim |
| P1-AC09 | EP03, EP05 | Explicit registry and consumer/import-boundary tests | Supported; extension distribution deferred |
| P1-AC10 | EP02–EP05 | Package/source inspection finds no P1 execution, data/ML, UI/API workflow, persistence, export, or plugin behavior | Supported |
| P1-AC11 | EP05 and current controls | Locked setup, attestation, inventory, license, audit, fixture integrity, hygiene | Supported by final worker evidence |
| P1-AC12 | Phase 1 Plan §9 | Requires independent validation and Central reconciliation | Pending; not worker-acceptance-capable |

## Direct evidence, fixture boundary, and exclusions

The public workflow package exposes immutable document values, declarative
contracts/registry, a narrow decode boundary, and pure validation. It uses
stable key/ID ordering, UTF-8 JSON, and semantic serialization that excludes
layout. Text validation returns stable diagnostics rather than raw parser
exceptions. The registry has exactly `vidap.kernel.contract-source` and
`vidap.kernel.contract-sink`, spanning the seven nominal types with no
operation key. Source and import-boundary tests show no execution, experiment,
export, FastAPI/Uvicorn, network, subprocess, filesystem, browser, or plugin
consumer in the workflow surface.

The P1-EP05 manifest identifies four synthetic UTF-8 fixtures totaling 3,872
bytes: one valid branched workflow and three invalid/versioned inputs. It
records exact SHA-256/size, MIT terms, provenance, expected result, privacy
attestation, reviewer/date, and only these consumers: P1-EP05 tests and Phase
1 validation/closeout evidence. Focused checks recompute exact bytes/hashes.
They are not product data, persistence, served content, or semantic authority.

## Final worker attestation, hygiene, and clean-copy evidence

After this report was created, the complete final attestation was rerun on the
final target in the exact required order, and every command passed:

1. `npm.cmd run check`
2. `npm.cmd run coverage`
3. `npm.cmd run deps:inventory`
4. `npm.cmd run license:check`
5. `npm.cmd run deps:audit`
6. `git diff --check`

Both lock hashes remained unchanged. Locked dependency inventory, license
policy, and advisory controls completed without a lock rewrite or automatic
remediation. `git diff --check` was clean. Focused Phase 1 suites and
fixture-integrity checks also passed.

Only normal ignored setup/build/coverage/environment/cache state was created.
It remained ignored. A focused sensitive-content scan of this report and the
Phase 1 workflow/fixture paths found no credentials, private keys,
user-specific absolute paths, or raw environment values. The text policy
requires LF for this report and the relevant Python/JSON files. Listener checks
found no process residue on the prescribed harness ports.

One new bounded clean copy and one isolated cache were created outside the
checkout and OneDrive. Locked setup, focused Phase 1 Python suites,
fixture-integrity checks, and `npm.cmd run check` passed. The copy and cache
were separately bounded, confirmed ordinary directories rather than reparse
points, removed, and verified absent. Temporary locations are intentionally
described without user-specific absolute paths.

## Phase 2 handoff and worker assessment

Accepted inputs for later planning are the canonical `1.0` document, stable
identities/endpoints, static declarative contracts/registry, exact nominal
types, pure diagnostics, strict compatibility policy, and controlled fixture
evidence. Phase 1 deliberately leaves execution semantics, dependency
scheduling, intermediate representation, run identity, seed/environment
capture, cache invalidation, artifact ownership, persistence, and runtime
failure policy undecided. This report selects none of them.

| EP06 criterion | Worker self-assessment |
|---|---|
| EP06-AC01–AC02 | Pass: authority, prerequisite/decision chain, baseline, pre-existing work, locks, inventory, and sole-report scope recorded. |
| EP06-AC03–AC05 | Pass: current source/test/fixture and final-control evidence supports the kernel and exclusions. |
| EP06-AC06 | Pass: Phase 2 handoff is bounded and deliberately undecided. |
| EP06-AC07–AC09 | Pass: final commands, clean copy, cleanup, locks, hygiene, sanitization, and scope evidence recorded. |
| EP06-AC10 | Pending: fresh independent validator `Accept` required. |
| EP06-AC11 | Pending: Central alone may reconcile P1-AC12 and accept. |

Independent-validation handoff: follow EP06 §11. Independently reread every
governing/P1 artifact; challenge all P1-AC01–P1-AC12 traceability, strict
compatibility, deterministic diagnostics/round trips, static registry,
fixture integrity/consumer limits, exclusions, scope/hygiene, locks, complete
attestation, and a separately bounded clean-copy proof. Return exactly
`Accept`, `Revise`, or `Blocked` with criterion-linked findings and a P1-AC12
recommendation. Do not edit tracked files, accept for Central, reconcile, or
begin Phase 2/P2-EP01.

This is worker evidence only: it does not independently validate or accept
P1-EP06 or Phase 1 and does not authorize Phase 2 planning.
