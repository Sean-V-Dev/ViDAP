# ViDAP P2-EP05 — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P2_EP05.md` version 0.3 |
| Worker report | `ViDAP_P2_EP05_Implementation_Report.md` |
| Independent-validation verdict | Accept; no unresolved finding |
| Central decision | P2-EP05 accepted; EP05-AC17 satisfied |
| Worker baseline/target commit | `f2d2b9526888b92094140f36aa191fdb2b8b927e` on `main` |
| Reconciliation date | 2026-09-25 |
| Owner | Central |

---

## 1. Purpose and authority

This record preserves the user's supplied final independent `Accept` for the
approved P2-EP05 v0.3 implementation and Central's separate acceptance. The
worker report's pending-validation language describes its earlier handoff;
the later independent verdict satisfies EP05-AC16. Central, not the worker or
validator, decides EP05-AC17 here. The retained v0.1 binding blocker and v0.2
publication findings are historical, not accepted implementation states.

## 2. Independent evidence and Central byte review

The validator reported no unresolved findings and accepted EP05-AC01 through
EP05-AC16. It inspected the fixed four-operation path and exact binding
revisions, challenged checked-integer behavior, and independently injected
pre-commit, post-commit acknowledgement, and failed-readback faults. The
pre-commit case retained pending ownership after rollback; the post-commit
case returned verified durable success; failed readback raised a sanitized
indeterminate error without changing terminal files. This preserves the
accepted immutable-terminal rule rather than rewriting a published record.

Central read the v0.3 packet and final worker report, inspected both exact
synthetic fixture documents and their manifest, and recalculated byte sizes
and SHA-256 from the current files:

| Fixture file | Bytes | SHA-256 |
|---|---:|---|
| `fixtures/p2-ep05/branched-success-v1.json` | 1,780 | `F2079F1A4BDADB073792BD19A26B43F2D5F7A8F5B81781715D180B95B78687D1` |
| `fixtures/p2-ep05/checked-overflow-v1.json` | 1,362 | `06F04CFF6D8F2642AADF28784C96AEF04DE4E41EAAD005F2079D6EEA695E7ED1` |
| `fixtures/p2-ep05/fixture-manifest.json` | 2,275 | `75B6584102E96E25DB9036445C91CFC16989D07502015596A98134A12870F49B` |

The first document has one literal value 3, two branches multiplying by 2
and 3, a join adding them, and a terminal emit: `3×2 + 3×3 = 15`. The second
adds the maximum signed 64-bit integer and 1, so overflow prevents its emit;
the independent literal is unrelated. Their IDs, edges, expected results,
synthetic provenance, MIT terms, permitted consumers, and explicit
non-sensitive classifications match the approved packet. No personal data,
credential, path, network identifier, or external dataset was found in the
fixture bytes. The three new files total 5,417 bytes; all root `fixtures/`
files total 13,225 bytes, within the approved bounds. Central accepts these
**exact bytes** for the bounded reference proof. The manifest's pending
byte-review field is a truthful worker-time snapshot; this reconciliation is
the later byte-level acceptance record, so the validated manifest is not
rewritten after validation.

The independently verified output envelope for value 15 is 68 UTF-8 bytes
with SHA-256
`53B600435D2936FA8D06EB0DB22E176676ABB8D75070B426AE909A91C9F6F2D6`.
The validator also checked actual branch and overflow runs, five computations
and five edge consumptions for the successful graph, a selected reuse key,
and the reported fixture and lock calculations.

The validator reported that the full ordered checks, locked setup, all 16
focused tests, and full check in a disposable copy passed. The copy, caches,
and generated attempts were removed. One host-dependent live-symlink test
was skipped; accepted Windows safety challenges passed. Central confirmed
the twelve authorized worker paths are the only worker changes, separately
from Central-owned planning changes, with no staged files and no lock change.
`git diff --check` passed. Both lock authorities still match the worker
report:

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Central did not rerun the complete worker attestation or independent
disposable-copy proof. The supplied fresh independent `Accept` is the
evidence for those checks.

## 3. Central decision and next boundary

Central accepts P2-EP05 v0.3 as the bounded headless scalar reference proof.
EP05-AC17 is satisfied and the packet is `Complete`. This accepts the four
fixed first-party reference operations, two reviewed synthetic fixtures,
one versioned scalar proof output, and the readback-based publication
classification. It does not approve a general numeric type, data or model
workflow, product UI/API, preview retention, cross-run cache, export, or
Phase 3 behavior.

P2-EP06 is now **ready to draft** as the separate Phase 2 closeout packet.
It is not yet approved or authorized for execution. Phase 2 itself remains
open until its closeout evidence is independently validated and Central
reconciles the phase exit criteria.
