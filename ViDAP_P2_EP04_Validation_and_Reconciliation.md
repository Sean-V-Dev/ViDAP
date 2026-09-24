# ViDAP P2-EP04 — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P2_EP04.md` version 0.1 |
| Worker report | `ViDAP_P2_EP04_Implementation_Report.md` |
| Independent-validation verdict | Accept; no unresolved finding |
| Central decision | P2-EP04 accepted; EP04-AC16 satisfied |
| Worker baseline commit | `c5296a96ab32239bdd40215e2dc98154c60218c3` |
| Reconciliation date | 2026-09-24 |
| Owner | Central |

---

## 1. Purpose and authority

This record preserves the user's supplied final independent `Accept` for the
approved P2-EP04 v0.1 implementation and Central's separate acceptance. The
worker report's pending-validation language describes its earlier handoff;
the later independent verdict satisfies EP04-AC15. Central, not the worker or
validator, decides EP04-AC16 here.

## 2. Independent evidence and Central check

The validator reported no unresolved findings and accepted EP04-AC01 through
EP04-AC15. It independently challenged creation, post-creation, first-write,
and four directory-swap paths, with no unrecorded UUID directory or
cross-attempt mutation remaining. Its key calculation matched SHA-256; each
of seven changed key components invalidated reuse. It checked actual sharing,
runtime failure, and malicious exception sanitization. The final ordered
attestation passed, as did locked setup, 26 focused tests (one host-dependent
live-symlink skip), and the full check in a fresh disposable copy. The copy
and caches were verified removed. The one skipped live-symlink test is
identified rather than counted as a pass; the validator accepted the
deterministic reparse and directory-swap challenges as sufficient here.

Central read the approved packet and the final worker report, inspected the
current artifact-allocation, attempt, and reuse source, and checked the Git
scope against the report's baseline. Before this Central reconciliation
write, `HEAD` was the worker baseline commit, no files were staged, and the
ten Section 7 worker paths were present alongside only the three pre-existing
Central-owned planning paths. `git diff --check` passed, and `.vidap-local`
was absent. Both lock authorities match the report:

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

Central also checked the narrow external API claim: Microsoft's
[`NtCreateFile` documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntcreatefile)
specifies that `FILE_CREATE` creates an absent file/directory and returns an
error if it already exists. The validator's actual Windows challenges, not
that documentation alone, support the artifact-safety verdict.

Central did not rerun the full worker attestation or independent disposable
copy. The supplied fresh independent `Accept` is the evidence for those
checks. The worker's earlier `Revise` findings are historical; the final
validator accepted the revised implementation and found no remaining issue.

## 3. Central decision and next boundary

Central accepts P2-EP04 v0.1 as the bounded run-foundation layer. EP04-AC16
is satisfied and the packet is `Complete`. Its immutable attempt records,
owned metadata-first local artifacts, visible within-attempt reuse, and
sanitized runtime diagnostics implement accepted D2.4–D2.7 within the
controlled scalar boundary. The test-local handlers and opaque proof slot
are not approved product operations, real data/model retention, or Phase 2
exit evidence. There is no persistent cross-run cache.

P2-EP05 — the actual deterministic scalar reference operation and workflow
proof under D2.8 — is now **ready to draft**. It requires its own bounded
packet and separate approval before implementation. Phase 2 is not yet
complete, and P2-EP06 closeout remains closed.
