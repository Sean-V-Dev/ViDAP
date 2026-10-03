# Decision Record: P3 Slice Numeric Runtime License Disposition

| Field | Value |
| --- | --- |
| Record | 0005 |
| Status | **Accepted** |
| Decision date | 2026-10-02 |
| Decision owner | Central (user-authorized) |
| Governing requirements | `ViDAP_Overview.txt`; accepted D0.6 in `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_Phase_3_Plan.md` v1.1; D3.1 and F2 in `ViDAP_P3_EP01_Validation_and_Reconciliation.md`; `ViDAP_P3_EP03A.md`; `ViDAP_P3_EP03A_Dependency_Review.md` (Revision 2, independently accepted); Decision Records 0003 and 0004 |

## Context

Accepted decision D3.1 fixes the Phase 3 slice's model to logistic
regression with a train/test split and evaluation. P3-EP03A reviewed adding
`scikit-learn==1.9.1` as the only new direct runtime dependency. In a
disposable copy, the addition locked seven new packages and changed no
existing one: scikit-learn 1.9.1, numpy 2.5.3, scipy 1.18.1, joblib 1.6.0,
threadpoolctl 3.7.0, narwhals 2.26.0, and cloudpickle 3.1.2.

Five of them pass the existing license gate on exact SPDX labels. The gate
fails closed on two:

- **numpy 2.5.3:** its gate value is the compound expression `BSD-3-Clause
  AND 0BSD AND MIT AND Zlib AND CC0-1.0`. Each component is individually
  allowed, but the gate does not parse compound expressions.
- **scipy 1.18.1:** its gate value is a 46,555-byte metadata text. It holds
  the BSD-3-Clause license, sections describing the bundled OpenBLAS, LAPACK
  and GCC runtime components, the GCC runtime library exception, and the
  GPLv3 text that governs that runtime library. The gate's first rule
  matches `*` and `custom` inside it.

The Windows wheels also bundle native components that the metadata-only gate
cannot see:

- **OpenBLAS DLLs in numpy and scipy:** OpenBLAS (BSD-3-Clause), LAPACK
  (BSD-3-Clause-Open-MPI), and the GCC runtime library (GPL-3.0-or-later WITH
  GCC-exception-3.1).
- **Microsoft Visual C++ runtime DLLs in scikit-learn and numpy:**
  scikit-learn's `COPYING` states Microsoft's Visual Studio redistribution
  terms (the files may be copied and distributed with a program, but not
  modified). numpy's copy is undocumented in its wheel.

The review found no prohibited top-level license. The independent validator
reproduced the gate results and both exact values and recommended the
disposition below.

This record is a bounded operational policy decision for the present lock
and role. It is not legal advice and makes no general decision about any
license family, label, or distribution model.

## Decision

P3-EP03B may add the following **literal package name, version, and gate
value** combinations, permitted only for their present unchanged, locally
installed, non-distributed runtime roles in the Phase 3 slice:

| Literal control key | Verified license | Present role | Required re-review trigger |
| --- | --- | --- | --- |
| `numpy@2.5.3` / `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` (50 characters, SHA-256 `365ECDF0EEDA8F7D03D67A4BBB06119DF487FF240E108DDE6F85BDF76C908781`) | The listed expression and its component license files; bundled native components as acknowledged below | Transitive numeric runtime for the slice's scikit-learn operations | Any version, gate value, role, modification, vendoring, packaging, or distribution change; retain all license files and bundled notices before any distribution. |
| `scipy@1.18.1` / the exact value in Appendix A of the P3-EP03A review: 46,555 UTF-8 bytes, LF line endings including one trailing LF, SHA-256 `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E` | BSD-3-Clause; bundled native components as acknowledged below | Transitive scientific runtime for scikit-learn | Same as numpy. |

It also acknowledges these bundled native components, outside the gate
catalog, with the same role limit and re-review trigger:

| Package | Bundled component | Terms relied on |
| --- | --- | --- |
| `numpy@2.5.3`, `scipy@1.18.1` | OpenBLAS DLL containing OpenBLAS, LAPACK, and the GCC runtime library | BSD-3-Clause; BSD-3-Clause-Open-MPI; GPL-3.0-or-later WITH GCC-exception-3.1, as documented in each wheel |
| `scikit-learn@1.9.1` | Microsoft Visual C++ runtime DLLs (`msvcp140`, `vcomp140`) | Microsoft Visual Studio redistribution terms as stated in scikit-learn's `COPYING` |
| `numpy@2.5.3` | Microsoft Visual C++ runtime DLL (`msvcp140`) | Undocumented in the wheel. For local, unmodified, non-distributed use only, Central accepts the analogy to the same Microsoft redistributable as scikit-learn's copy. Distribution re-opens this as a blocking question. |

The five other added packages (scikit-learn, joblib, threadpoolctl,
narwhals, cloudpickle) pass the existing gate on exact allowed labels and
need no catalog entry.

## Required implementation boundary

The implementation of this decision in P3-EP03B must:

- add a separate literal three-part catalog for this record (name, exact
  version, exact gate value) that reports record `0005`, the role, and the
  re-review trigger, and is consulted after Records 0003 and 0004;
- embed scipy's value as base64 decoded in the script, as Record 0004 does
  for `pip_api`, and prove before use that the decoded value has the SHA-256
  above;
- compare against the untrimmed gate value, as the existing catalogs do; and
- show `npm.cmd run license:check` passing on the real locked install, with
  no other change in disposition.

It must not:

- parse compound SPDX expressions, accept free-text BSD claims, or accept
  GCC-exception or Microsoft redistributable terms as general classes;
- use version ranges, name prefixes, wildcards, digests in place of the
  literal value, or role inference; or
- weaken the fail-closed result for any other value.

Records 0003 and 0004 remain in force and are not extended by this record.

## Known control gap

The license gate reads package metadata only and cannot see bundled native
components (P3-EP03A finding D-F5). This record does not change the gate to
inspect wheels. The gap is covered for now by this record's acknowledgment
table, the re-review trigger on every listed package, and the SBOM trigger
below. The gate stays fail-closed.

## SBOM

A formal software bill of materials is deferred again. Nothing is
distributed, the application runs only locally, and `deps:inventory` lists
every installed package. **Trigger:** before any installer, packaged Python
environment, desktop build, or other distribution, an SBOM that includes
bundled native components is required.

## Consequences

After acceptance, P3-EP03B may add `scikit-learn==1.9.1` to the runtime
dependencies, update `python/uv.lock`, and add the two catalog entries,
with fresh worker evidence and independent validation. This record does not
itself change a lock, manifest, or script, and it does not accept P3-EP03B.

## Alternatives considered

- **Parse compound SPDX expressions in the gate:** Deferred. It is a general
  control change that would need its own review, and literal entries cover
  the current need without weakening fail-closed behavior.
- **Use another model library or hand-written logistic regression:**
  Rejected in D3.1 and again in P3-EP03A. The alternatives either lack an
  established implementation or pull in the same numeric stack.
- **Key scipy by digest only:** Rejected. The existing catalogs match the
  literal value; the digest is a check, not the key.

## Revisit triggers

Revisit this record before any listed package's version or gate value
changes; before any listed package or bundled component is modified,
vendored, packaged, or distributed; before an installer, packaged
environment, or desktop build is introduced; or if the slice's role for
these packages changes. A later record must link to Records 0003, 0004, and
0005 rather than silently extending this catalog.
