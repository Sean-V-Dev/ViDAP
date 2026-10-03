# ViDAP P3-EP03A — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03A.md` version 0.1, approved 2026-10-02 |
| Worker output | `ViDAP_P3_EP03A_Dependency_Review.md` (Revision 2) |
| Output SHA-256 at reconciliation | `B179D26D1BA210DD86A9C4993A4221BE1B13445F398CCE60FA1EB0F6F9C191DF` |
| Independent-validation verdict | Accept on Revision 2, after one `Revise`; no unresolved finding |
| Central decision | Accepted with the user's authorization on 2026-10-02: Decision Record 0005 accepted; D-F1–D-F6 dispositioned; SBOM deferred with an explicit trigger; D3.1 unchanged; P3-EP03A complete |
| Baseline HEAD | `17652fc28eafa0b8e2b5be58c55df9ced0d7afff` on `main` |
| Reconciliation date | 2026-10-02 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied the independent `Accept` for Revision 2. The validator:

- decoded Appendix A itself and confirmed 46,555 bytes, the SHA-256, ASCII
  content, LF line endings, and one trailing LF;
- replayed `Get-LicenseDisposition` in order against both gate values,
  confirming scipy fails the first rule (`*` three times, `custom` three
  times) and numpy reaches the final default;
- confirmed the catalog key is built from the untrimmed value;
- confirmed the cloudpickle and threadpoolctl facts against PyPI and joblib
  1.6.0's requirements;
- accepted the D-F4 treatment of numpy's undocumented Microsoft runtime DLL
  as complete for this packet; and
- confirmed the repository state: both lock hashes at baseline, nothing
  staged, `diff --check` clean, no change under `python/`, `scripts/`,
  `docs/`, `.github/`, or the npm manifests, and only the report untracked
  besides the Central-owned files.

The validator could not run Windows commands or download wheels. It relied
on the user-run attestation and disposable-copy evidence, which matched.

**Validator-side incident.** The validator's first read-only `git status`
left an empty `.git/index.lock`, which would have blocked Git on Windows. With
the user's permission it deleted only that file and used lock-free reads
afterwards. Central confirmed the lock file is absent. No repository content
was affected.

This satisfies EP03A-AC01–EP03A-AC11.

## 2. Attestation

The final attestation is the user's Windows run on 2026-10-02 after
Revision 2 was written, recorded in the report's Section 9:

| Step | Result |
|---|---|
| `npm.cmd run check` | Exit 0 |
| `npm.cmd run coverage` | Exit 0 (web 87.5% of statements; Python 88%) |
| `npm.cmd run deps:inventory` | Exit 0 |
| `npm.cmd run license:check` | Exit 0 (431 packages) |
| `npm.cmd run deps:audit` | Exit 0 (no known vulnerabilities) |
| `git --no-pager diff --check` | Exit 0; only Git's line-ending notices for untouched tracked files |

Both lock hashes are unchanged (`FB7119F6…82FA`, `AC31501B…4355`), nothing
is staged, and `HEAD` is the baseline. Central did not rerun the
attestation.

## 3. Findings dispositioned

| ID | Finding | Central disposition |
|---|---|---|
| D-F1 | numpy fails closed on its compound SPDX expression | Literal catalog entry in Record 0005 |
| D-F2 | scipy fails closed on its full metadata text | Literal catalog entry in Record 0005, using the exact Appendix A value |
| D-F3 | OpenBLAS DLLs bundle LAPACK and the GCC runtime library | Acknowledged in Record 0005 for local, unmodified, non-distributed use |
| D-F4 | Microsoft C++ runtime DLLs in scikit-learn and numpy; numpy's undocumented | scikit-learn's acknowledged under its stated terms; numpy's accepted by analogy for local use only, with distribution re-opening it as a blocking question (Record 0005) |
| D-F5 | The gate cannot see bundled native components | Recorded as a known gap; gate stays fail-closed; covered by Record 0005's acknowledgment table and the SBOM trigger |
| D-F6 | Exact scipy value | Resolved in Revision 2; P3-EP03B embeds it as base64 and proves its SHA-256 |

**SBOM:** deferred again. Trigger: an SBOM including bundled native
components is required before any installer, packaged environment, desktop
build, or other distribution.

**D3.1:** unchanged; scikit-learn stays the slice's model library. Records
0003 and 0004 are unaffected; none of their revisit triggers fires.

## 4. Central decision and next boundary

With the user's authorization on 2026-10-02, Central accepts Decision Record
0005 and marks P3-EP03A complete. The next step is drafting P3-EP03B (backend slice
implementation), which needs the user's approval before any work. It will
carry Record 0005's implementation boundary, along with the D3.1–D3.4, F1,
F2, and F6 requirements.

Nothing here changes a lock, manifest, script, or remote state, and nothing
is staged, committed, or pushed.
