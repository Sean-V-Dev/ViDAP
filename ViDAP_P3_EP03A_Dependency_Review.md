# ViDAP P3-EP03A — Slice Dependency and License Review Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP03A.md` v0.1, explicitly approved by the user 2026-10-02 |
| Revision | 2, 2026-10-02, responding to the independent `Revise` (Section 12) |
| Worker execution | 2026-10-02; Linux shell over the Windows checkout; disposable-copy and attestation steps run by the user on Windows per `CONTRIBUTING.md` |
| Worker result | Evidence complete; findings D-F1–D-F6 need a Central decision (Section 7); no prohibited top-level license on inspection; the exact scipy gate value is captured and verified (Appendix A); Revision 2 attestation passed (Section 9); ready for re-validation |
| Independent validation | Revision 1 returned `Revise`; Revision 2 awaits re-validation; this report is not a verdict |
| Central decision | Pending; no license is accepted by this report |

## 1. Authority, inputs, and baseline

Inputs read: the user's 2026-10-02 approval of this exact packet; OV §§9, 21,
23, 25, 30; Phase 3 plan v1.1; roadmap P3; the P3-EP01 reconciliation (D3.1,
F2) and decision report; accepted D0.6; `docs/dependency-controls.md`;
decision records 0003 and 0004; `scripts/dependency-controls.ps1`;
`python/pyproject.toml`; `python/uv.lock`; `CONTRIBUTING.md`.

Baseline before writing: branch `main`, `HEAD`
`17652fc28eafa0b8e2b5be58c55df9ced0d7afff`, nothing staged. Pre-existing
Central-owned changes: modified `ViDAP_P3_EP03A.md`, `ViDAP_Phase_3_Plan.md`,
and `ViDAP_Roadmap.md` (approval records). The output path did not exist.

| Lock | SHA-256 |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

**Environment note.** PyPI and the npm registry are blocked by the
organization's egress policy from both worker shells (proxy HTTP 403), so
the worker could not download wheels itself. All resolution, installation,
and wheel inspection ran on the user's Windows machine in the disposable
copy (Section 5), using a script the worker provided. Public project pages
supplied release and maintenance facts.

## 2. Sources (retrieved 2026-10-02)

| ID | Source | Fact used |
|---|---|---|
| P1 | pypi.org/project/scikit-learn | 1.9.1, released 2026-09-10; `License-Expression: BSD-3-Clause`; `cp314-win_amd64` wheel 8.4 MB; Python ≥3.11 |
| P2 | pypi.org/project/numpy | 2.5.3, released 2026-09-06; `cp314-win_amd64` wheel 12.7 MB |
| P3 | pypi.org/project/scipy | 1.18.1, released 2026-08-21; `cp314-win_amd64` wheel 37.4 MB; license shown only as classifier "OSI Approved :: BSD License" plus copyright text |
| P4 | pypi.org/project/joblib | 1.6.0, released 2026-08-31; BSD-3-Clause; pure Python |
| P5 | pypi.org/project/threadpoolctl (rechecked in Revision 2) | 3.7.0, released 2026-09-15; BSD-3-Clause; pure Python. Revision 1 relied on a stale view of the page showing 3.6.0 |
| P9 | pypi.org/project/cloudpickle (Revision 2) | 3.1.2, released 2025-11-03; BSD-3-Clause; pure Python |
| P6 | pypi.org/project/narwhals | 2.26.0, released 2026-09-08; MIT; zero dependencies |
| P7 | scikit-learn `build_tools/wheels/LICENSE_windows.txt` | The Windows wheel bundles "Microsoft Visual C++ Runtime Files" (`sklearn\.libs\*.dll`) under Microsoft's Visual Studio redistribution terms, which allow distributing the redistributable files with a program |
| P8 | github.com/scipy/scipy issue #7093 | Background: SciPy wheels have long bundled a GCC runtime under GPL with the runtime exception, documented in the wheel |
| W | User-run disposable-copy script (Section 5) | Lock delta, installed metadata, bundled license sections, DLL names, sizes, and the real control results |
| W2 | Second user-run disposable-copy script (Revision 2; same rules as Section 5) | Exact scipy gate value as base64 with length and SHA-256; numpy wheel search for Microsoft runtime terms; scikit-learn `COPYING` Microsoft section; threadpoolctl and cloudpickle sizes; reverse dependency of cloudpickle; verified cleanup |
| S | `scripts/dependency-controls.ps1` at the baseline | Exact gate rules and catalog key form (Section 6) |

## 3. Candidate

Direct runtime addition: **`scikit-learn==1.9.1`** only, the newest release,
which publishes CPython 3.14 Windows x64 wheels (P1). No pandas or other
library.

## 4. Lock delta

Adding the candidate in the copy resolved 64 packages and added exactly
seven to `python/uv.lock`; **no existing locked package changed or was
removed** (W). The extra install lines in the copy's output were the
existing runtime packages being installed into the copy's fresh
environment, not lock changes.

| Added package | Version | Role |
|---|---|---|
| scikit-learn | 1.9.1 | Direct runtime |
| numpy | 2.5.3 | Transitive runtime (scikit-learn, scipy) |
| scipy | 1.18.1 | Transitive runtime (scikit-learn) |
| joblib | 1.6.0 | Transitive runtime (scikit-learn) |
| threadpoolctl | 3.7.0 | Transitive runtime (scikit-learn) |
| narwhals | 2.26.0 | Transitive runtime (scikit-learn) |
| cloudpickle | 3.1.2 | Transitive runtime (joblib 1.6.0 requires `cloudpickle>=3.0`; W2) |

## 5. Disposable copy

The user ran the worker's script from the repository root on Windows. It
created one folder under the system temporary directory (refusing a path
inside OneDrive or the repository), copied the repository without `.git`,
environments, caches, or build output, set separate npm and uv caches inside
that folder, added the candidate there with `uv add`, ran locked
`npm.cmd run setup`, `deps:inventory`, `license:check`, and `deps:audit`,
inspected the new packages' installed metadata, bundled license sections,
DLLs, and sizes, and finally removed the folder and caches after checking
the path was the expected temporary child. It reported **"copy and caches
removed = True"**. The repository's own manifests and locks were never
touched.

Control results in the copy:

| Step | Exit | Result |
|---|---:|---|
| `npm.cmd run setup` | 0 | npm: 0 vulnerabilities; uv: 64 packages resolved |
| `npm.cmd run deps:inventory` | 0 | Lists all seven new Python packages as installed |
| `npm.cmd run license:check` | 1 | **Failed closed on two packages**: `numpy@2.5.3` and `scipy@1.18.1`, both marked `prohibited` from installed metadata (Section 6). Every other new package was not reported as a finding. Existing Record 0003/0004 matches were unchanged. |
| `npm.cmd run deps:audit` | 0 | npm: 0 vulnerabilities across 432; Python: no known vulnerabilities |

The PowerShell "NativeCommandError" lines in the output are PowerShell
wrapping normal stderr text from npm and uv; every step's exit code is as
shown.

**Second disposable copy (Revision 2, W2).** To answer the `Revise`, the
user ran a second worker script under the same rules: a fresh temporary
folder outside OneDrive and the repository, separate caches, the same
candidate added there, locked setup, then read-only inspection of the
installed packages. It printed the scipy gate value as base64 with its
character count, UTF-8 byte count, and SHA-256 computed on the user's
machine; searched every text and license file in the installed numpy
package for Microsoft runtime terms; printed the Microsoft section of
scikit-learn's `COPYING`; measured threadpoolctl and cloudpickle; and listed
which installed package requires cloudpickle. It reported **"removed =
True"**. The worker decoded the pasted base64 in its own shell and got
exactly 46,555 bytes with the same SHA-256, so the copy-paste did not alter
the value.

## 6. Per-package evidence

"Gate value" is what the control read: the first populated of SPDX
expression, metadata `License`, then classifier.

| Package | Gate value (W) | Control | Actual license text (W) | Bundled native components (W) | Installed size (W) | Maintenance (P) |
|---|---|---|---|---|---|---|
| scikit-learn 1.9.1 | `BSD-3-Clause` | Not a finding | `COPYING` (BSD-3-Clause) plus a bundled section | `msvcp140.dll`, `vcomp140.dll` in `sklearn\.libs`: Microsoft Visual C++ Runtime, Microsoft redistribution terms (P7) | 26.1 MB | Active; 1.9.1 on 2026-09-10 |
| numpy 2.5.3 | `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` | **prohibited** | `LICENSE.txt` and 16 component license files, all within the listed expression | `numpy.libs\libscipy_openblas64_…dll` (OpenBLAS BSD-3-Clause; LAPACK BSD-3-Clause-Open-MPI; GCC runtime library GPL-3.0-or-later WITH GCC-exception-3.1, per the wheel's bundled-license section); `numpy.libs\msvcp140-….dll` (Microsoft C++ runtime; no license, notice, or text file in the installed numpy package mentions it, W2) | 19.7 + 20.2 MB | Active; 2.5.3 on 2026-09-06 |
| scipy 1.18.1 | Metadata `License` field, 46,555 UTF-8 bytes, SHA-256 `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`: the BSD-3-Clause text, then the bundled-component sections, the GCC runtime exception text, and the full GPLv3 text (exact value in Appendix A) | **prohibited** | `LICENSE.txt`: BSD-3-Clause text plus a bundled section | `scipy.libs\libscipy_openblas-…dll` (same three components and licenses as numpy's) | 83.4 + 19.3 MB | Active; 1.18.1 on 2026-08-21 |
| joblib 1.6.0 | `BSD-3-Clause` | Not a finding | `LICENSE.txt` | None (pure Python) | 0.9 MB | Active; 1.6.0 on 2026-08-31 |
| threadpoolctl 3.7.0 | `BSD-3-Clause` | Not a finding | `LICENSE` | None | 91.7 KB, 7 files (W2) | Active; 3.7.0 on 2026-09-15 (P5) |
| narwhals 2.26.0 | `MIT` | Not a finding | `LICENSE.md` | None | 1.9 MB | Active; 2.26.0 on 2026-09-08 |
| cloudpickle 3.1.2 | `BSD-3-Clause` (metadata) | Not a finding | `LICENSE` | None | 71.1 KB, 10 files (W2) | Maintained; 3.1.2 on 2025-11-03 (P9); required by joblib |

Total installed addition is about 171 MB. All compiled packages provide
`cp314-win_amd64` wheels (P1–P3).

**Why the control failed (checked against `Get-LicenseDisposition` in S;
PowerShell `-match` is case-insensitive and unanchored, and the rules apply
in order):**

- **numpy:** the gate value `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND
  CC0-1.0` (50 characters, SHA-256
  `365ECDF0EEDA8F7D03D67A4BBB06119DF487FF240E108DDE6F85BDF76C908781`)
  matches no first-rule token, is not an exact allowed value, matches no
  review-required token, and matches no named prohibited token, so it falls
  to the final default `prohibited`. Every component is individually in the
  allow list; the control does not parse compound expressions.
- **scipy:** there is no SPDX expression, so the control reads the metadata
  `License` field. That value fails the **first rule**, which marks a value
  prohibited if it contains `unknown`, `none`, `unlicensed`, `custom`, `*`,
  or `see license`. It contains `*` three times (each bundled-component
  section has the line `Files: scipy.libs\libscipy_openblas*.dll`) and
  `custom` three times (inside "customarily" and "customer" in the GPLv3
  text). Revision 1 called this a "custom claim" about free BSD text; that
  was wrong. The value is not just BSD text, and the failure is a substring
  match on wildcard and GPL wording, not a judgment about the BSD license.
  Without the first rule, it would match the review-required token
  `binary`. The classifier ("OSI Approved :: BSD License") is never
  consulted, by design.

Neither failure reflects a non-permissive top-level license. scipy's GPLv3
text is there because it governs the bundled GCC runtime library (under
the GCC runtime exception, D-F3), not scipy itself.

**Catalog key form (S).** The catalog functions build the key as
`"$Name|$Version|$License"` from the **untrimmed** gate value and look it up
in a PowerShell hashtable (case-insensitive keys). The scipy value ends with
one line feed, which is part of the 46,555 bytes and the SHA-256, so it must
stay in the catalog key. Record 0004 already stores a long gate value
(`pip_api`) as base64 decoded in the script; Appendix A gives scipy's value
in the same form.

**Control blind spot (finding):** the license gate reads package metadata
only. It does not see bundled native components, so scikit-learn passes
even though it ships Microsoft runtime DLLs, and the GCC-runtime component
inside numpy's and scipy's OpenBLAS DLLs is visible only by inspecting the
wheels. D0.6 treats native and platform-binary components as review-required,
so these need a Central decision whether or not the gate flags them.

## 7. Findings for Central

| ID | Kind | Finding |
|---|---|---|
| D-F1 | Control finding | `numpy@2.5.3` fails closed on its compound SPDX expression, all of whose components are individually allowed. |
| D-F2 | Control finding | `scipy@1.18.1` fails closed because its 46,555-byte metadata `License` value contains `*` and `custom` (first gate rule, Section 6); scipy's own license is BSD-3-Clause, and the rest of the value documents bundled components. |
| D-F3 | Native, review-required | The OpenBLAS DLLs in numpy and scipy bundle the GCC runtime library under GPL-3.0-or-later WITH GCC-exception-3.1, and LAPACK under BSD-3-Clause-Open-MPI. |
| D-F4 | Native, review-required | scikit-learn and numpy bundle Microsoft Visual C++ runtime DLLs. scikit-learn's `COPYING` states Microsoft's Visual Studio redistribution terms for its copies (P7, W2): the files may be copied and distributed with a program but not modified. **numpy's `msvcp140` DLL is undocumented in its wheel**: no installed numpy license, notice, or text file mentions it (W2). Its terms are presumably the same Microsoft redistributable terms, but that is an inference by analogy, not evidence from numpy; Central decides whether that analogy is enough. |
| D-F5 | Control gap | The license gate does not inspect bundled native components (Section 6). |
| D-F6 | Evidence, resolved in Revision 2 | Revision 1 showed the scipy gate value truncated. The exact value is now captured on the user's machine and verified in the worker's shell: field `License-Metadata`, 46,555 UTF-8 bytes (equal to its character count), LF line endings, one trailing LF, SHA-256 `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`. Appendix A holds it as base64. P3-EP03B should embed that base64 as Record 0004 does for `pip_api`, and show that the decoded value has this SHA-256 and that `license:check` passes. |

No package has a prohibited top-level license on inspection, and nothing
indicates the GCC-exception or Microsoft redistributable terms block local,
unmodified, non-distributed use. **This is evidence, not legal advice.**
The worker does not recommend returning D3.1 to Central for a different
library: the alternatives in the P3-EP01 report either lack an established
implementation or pull in the same numeric stack.

### Proposed literal catalog entries (proposal only)

In the style of Records 0003 and 0004, each limited to the present unchanged,
locally installed, non-distributed **runtime** role:

| Literal control key | Verified license | Role | Re-review trigger |
|---|---|---|---|
| `numpy@2.5.3` / `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` | The listed expression and its component license files; bundled OpenBLAS DLL (BSD-3-Clause; LAPACK BSD-3-Clause-Open-MPI; GCC runtime GPL-3.0-or-later WITH GCC-exception-3.1) and Microsoft C++ runtime DLL | Transitive numeric runtime for the slice's scikit-learn operations | Any version, gate value, role, modification, vendoring, or distribution change; retain all license files and bundled notices before any distribution |
| `scipy@1.18.1` / the exact Appendix A value (46,555 bytes, SHA-256 `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`) | BSD-3-Clause; bundled OpenBLAS DLL as for numpy | Transitive scientific runtime for scikit-learn | Same as numpy |

And, outside the gate catalog (the gate does not flag them), a decision-record
acknowledgment of the bundled native components for `scikit-learn@1.9.1`
(Microsoft C++ runtime) and for numpy and scipy (OpenBLAS with GCC runtime
and LAPACK), with the same role and re-review trigger.

### Draft decision wording (proposal only)

> Decision Record 0005 permits `numpy@2.5.3` and `scipy@1.18.1` at their
> exact gate values (scipy's identified by its full value and SHA-256), and acknowledges the bundled native components of
> `numpy@2.5.3`, `scipy@1.18.1`, and `scikit-learn@1.9.1` listed in the
> P3-EP03A review, only for their present unchanged, locally installed,
> non-distributed runtime role in the Phase 3 slice. It links to Records
> 0003 and 0004 and does not extend them. It does not approve compound SPDX
> expressions, free-text BSD claims, GCC-exception or Microsoft
> redistributable terms as general classes. Re-review on any version, gate
> value, role, modification, vendoring, packaging, installer, or
> distribution change.

Whether to improve the gate itself (for example, to parse compound
expressions whose every component is allowed, or to list bundled native
components) is a separate Central choice; this report does not recommend
weakening fail-closed behavior.

## 8. Trigger questions

- **SBOM ("revisit before a later ML dependency"):** this is that trigger.
  The worker recommends **deferring a formal SBOM again**, because nothing is
  distributed, the app runs only locally, and `deps:inventory` already lists
  every installed package. The recommendation assumes Central records the
  deferral and sets the next trigger explicitly: before any installer,
  packaged environment, desktop build, or other distribution, an SBOM that
  includes bundled native components is required.
- **Records 0003/0004 revisit triggers:** none fires. The lock delta only
  adds packages; no package those records cover changes version, gate value,
  or role (W).
- **Notices if ever distributed:** every package's license files, numpy's 16
  component license files, the bundled OpenBLAS/LAPACK/GCC-runtime sections,
  and the Microsoft redistributable terms would have to be retained.

## 9. Final attestation and scope

**Revision 2: passed.** Revision 1's attestation also passed, but Revision
2 changed this report, so the user ran the packet's Section 9 sequence
again in Windows PowerShell from the repository root on 2026-10-02, after
Revision 2 was written. This is a user-executed Windows run under the
`CONTRIBUTING.md` workaround, using a summary-line script that avoids Git's
pager. The results are exactly as the output shows:

| Command | Exit | Captured evidence |
|---|---:|---|
| `npm.cmd run check` | 0 | "All checks passed!"; mypy "no issues found in 21 source files"; web 3 files, 10 tests passed; Python unit 125 passed, 1 skipped, 3 deselected; integration 3 passed |
| `npm.cmd run coverage` | 0 | Web 10 passed, 87.5% statements; Python 128 passed, 1 skipped, 88% total |
| `npm.cmd run deps:inventory` | 0 | Completed |
| `npm.cmd run license:check` | 0 | "License policy passed for 431 installed locked packages" |
| `npm.cmd run deps:audit` | 0 | npm: 0 vulnerabilities of 432; Python: 57 packages resolved, "No known vulnerabilities found" |
| `git --no-pager diff --check` | 0 | No whitespace errors; only Git's informational line-ending conversion warnings for tracked files this packet did not touch |

Lock hashes equal the Section 1 baseline:
`FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` and
`AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355`.
`git status` shows the three Central-owned modified files from Section 1 and
this report as the only untracked file; nothing is staged. The one Python
skip is the host-dependent symlink test Phase 2 already accepted.

Report hygiene, checked directly in Revision 2: LF line endings, no
trailing whitespace, final newline, no user paths, credentials, or raw
environment values. No setup, install, or package task ran from a Linux
shell against the checkout, and nothing was staged, committed, or pushed.

## 10. Worker self-assessment

| Criterion | Assessment |
|---|---|
| EP03A-AC01 | Met. |
| EP03A-AC02 | Met: scikit-learn only, exactly pinned; seven added packages; no existing package changed. |
| EP03A-AC03 | Met. numpy's Microsoft runtime DLL is shown to be undocumented in its wheel (D-F4), which is now a recorded finding rather than an open question; cloudpickle maintenance and dependent are recorded (P9, W2). |
| EP03A-AC04 | Met for every compiled wheel (numpy, scipy, scikit-learn). |
| EP03A-AC05 | Met: real control results recorded, including the expected `license:check` failure. |
| EP03A-AC06 | Met. |
| EP03A-AC07 | Met: proposed literal entries with the exact scipy value (Appendix A) and draft wording; no prohibited top-level license. |
| EP03A-AC08 | Met: two temporary copies (Revision 1 and Revision 2), each with its caches removed and the removal verified. |
| EP03A-AC09 | Met: only the report changed; locks unchanged; Revision 2 attestation passed. |
| EP03A-AC10–AC11 | Not self-assessed. |

## 11. Independent-validation handoff

Please re-validate Revision 2 against the inputs and the `Revise`
(Section 12). In particular, check:

- **Appendix A:** decode it and confirm 46,555 bytes and SHA-256 `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`. If
  possible, compare it with the `License-Metadata` value that `pip-licenses`
  reports for `scipy@1.18.1` in a bounded disposable copy.
- **The corrected explanation of the scipy failure** against
  `Get-LicenseDisposition`.
- **D-F4:** whether numpy's undocumented Microsoft runtime DLL needs more
  evidence or is a decision for Central.
- **The cloudpickle and threadpoolctl facts.**
- **The Revision 2 attestation** (Section 9).

Return `Accept`, `Revise`, or `Blocked`, with a Central recommendation on
D-F1–D-F6 and the SBOM deferral. This worker does not validate its own work
or accept any license.

## 12. Response to independent `Revise`

| Item raised | Revision 2 change |
|---|---|
| Exact scipy gate value missing; a literal catalog entry cannot be checked against a truncated string | Captured on the user's machine, verified in the worker's shell, and recorded in full (Appendix A), with length, SHA-256, line-ending and trailing-newline facts and the catalog key form (Sections 6–7, D-F6) |
| scipy failure explained wrongly | Corrected: the first gate rule matches `*` in the `Files:` lines and `custom` in the GPLv3 text; the value contains the bundled-component sections and full GPLv3, not only BSD text (Section 6, D-F2) |
| numpy failure path not shown precisely | Its exact value, length, and digest are recorded, and the rule path to the final default `prohibited` is traced (Section 6) |
| numpy's Microsoft runtime DLL terms not established | Every installed numpy text and license file was searched, and none mentions it; recorded as undocumented in the wheel, with scikit-learn's stated Microsoft terms given only as an analogy for Central (D-F4) |
| cloudpickle requirer and maintenance unknown | joblib 1.6.0 requires `cloudpickle>=3.0`; 3.1.2 released 2025-11-03, BSD-3-Clause, 71.1 KB (Sections 2, 4, 6) |
| threadpoolctl release date and size wrong or vague | 3.7.0 released 2026-09-15; 91.7 KB in 7 files; source P5 corrected (Sections 2, 6) |
| Attestation must reflect the revised report | Re-run by the user on Windows after Revision 2; passed (Section 9) |

## Appendix A. Exact scipy@1.18.1 gate value

- **Field:** `License-Metadata` as reported by `pip-licenses --from=all`.
- **Size:** 46,555 characters, which is also 46,555 UTF-8 bytes (ASCII only).
- **Line endings:** LF only, ending with one LF.
- **SHA-256 of the UTF-8 bytes:** `7F2F9E131A09F25323E392AAC37FB2E263C600BB9D1FFC7C3B6CA3E1D017573E`.

It is encoded below as standard base64, wrapped at 76 characters for
reading; join the lines with no separator before decoding. It begins
"Copyright (c) 2001-2002 Enthought, Inc. 2003, SciPy Developers." and
contains the BSD-3-Clause text, the three bundled-component sections for
`scipy.libs\libscipy_openblas*.dll` (OpenBLAS, LAPACK, GCC runtime library),
the GCC runtime library exception, and the GNU GPL version 3 text.

```text
Q29weXJpZ2h0IChjKSAyMDAxLTIwMDIgRW50aG91Z2h0LCBJbmMuIDIwMDMsIFNjaVB5IERldmVs
b3BlcnMuCiBBbGwgcmlnaHRzIHJlc2VydmVkLgoKIFJlZGlzdHJpYnV0aW9uIGFuZCB1c2UgaW4g
c291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdpdGggb3Igd2l0aG91dAogbW9kaWZpY2F0aW9uLCBh
cmUgcGVybWl0dGVkIHByb3ZpZGVkIHRoYXQgdGhlIGZvbGxvd2luZyBjb25kaXRpb25zCiBhcmUg
bWV0OgoKIDEuIFJlZGlzdHJpYnV0aW9ucyBvZiBzb3VyY2UgY29kZSBtdXN0IHJldGFpbiB0aGUg
YWJvdmUgY29weXJpZ2h0CiAgICBub3RpY2UsIHRoaXMgbGlzdCBvZiBjb25kaXRpb25zIGFuZCB0
aGUgZm9sbG93aW5nIGRpc2NsYWltZXIuCgogMi4gUmVkaXN0cmlidXRpb25zIGluIGJpbmFyeSBm
b3JtIG11c3QgcmVwcm9kdWNlIHRoZSBhYm92ZQogICAgY29weXJpZ2h0IG5vdGljZSwgdGhpcyBs
aXN0IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcKICAgIGRpc2NsYWltZXIgaW4gdGhl
IGRvY3VtZW50YXRpb24gYW5kL29yIG90aGVyIG1hdGVyaWFscyBwcm92aWRlZAogICAgd2l0aCB0
aGUgZGlzdHJpYnV0aW9uLgoKIDMuIE5laXRoZXIgdGhlIG5hbWUgb2YgdGhlIGNvcHlyaWdodCBo
b2xkZXIgbm9yIHRoZSBuYW1lcyBvZiBpdHMKICAgIGNvbnRyaWJ1dG9ycyBtYXkgYmUgdXNlZCB0
byBlbmRvcnNlIG9yIHByb21vdGUgcHJvZHVjdHMgZGVyaXZlZAogICAgZnJvbSB0aGlzIHNvZnR3
YXJlIHdpdGhvdXQgc3BlY2lmaWMgcHJpb3Igd3JpdHRlbiBwZXJtaXNzaW9uLgoKIFRISVMgU09G
VFdBUkUgSVMgUFJPVklERUQgQlkgVEhFIENPUFlSSUdIVCBIT0xERVJTIEFORCBDT05UUklCVVRP
UlMKICJBUyBJUyIgQU5EIEFOWSBFWFBSRVNTIE9SIElNUExJRUQgV0FSUkFOVElFUywgSU5DTFVE
SU5HLCBCVVQgTk9UCiBMSU1JVEVEIFRPLCBUSEUgSU1QTElFRCBXQVJSQU5USUVTIE9GIE1FUkNI
QU5UQUJJTElUWSBBTkQgRklUTkVTUyBGT1IKIEEgUEFSVElDVUxBUiBQVVJQT1NFIEFSRSBESVND
TEFJTUVELiBJTiBOTyBFVkVOVCBTSEFMTCBUSEUgQ09QWVJJR0hUCiBPV05FUiBPUiBDT05UUklC
VVRPUlMgQkUgTElBQkxFIEZPUiBBTlkgRElSRUNULCBJTkRJUkVDVCwgSU5DSURFTlRBTCwKIFNQ
RUNJQUwsIEVYRU1QTEFSWSwgT1IgQ09OU0VRVUVOVElBTCBEQU1BR0VTIChJTkNMVURJTkcsIEJV
VCBOT1QKIExJTUlURUQgVE8sIFBST0NVUkVNRU5UIE9GIFNVQlNUSVRVVEUgR09PRFMgT1IgU0VS
VklDRVM7IExPU1MgT0YgVVNFLAogREFUQSwgT1IgUFJPRklUUzsgT1IgQlVTSU5FU1MgSU5URVJS
VVBUSU9OKSBIT1dFVkVSIENBVVNFRCBBTkQgT04gQU5ZCiBUSEVPUlkgT0YgTElBQklMSVRZLCBX
SEVUSEVSIElOIENPTlRSQUNULCBTVFJJQ1QgTElBQklMSVRZLCBPUiBUT1JUCiAoSU5DTFVESU5H
IE5FR0xJR0VOQ0UgT1IgT1RIRVJXSVNFKSBBUklTSU5HIElOIEFOWSBXQVkgT1VUIE9GIFRIRSBV
U0UKIE9GIFRISVMgU09GVFdBUkUsIEVWRU4gSUYgQURWSVNFRCBPRiBUSEUgUE9TU0lCSUxJVFkg
T0YgU1VDSCBEQU1BR0UuCgogLS0tLQoKCiAtLS0tCgogVGhpcyBiaW5hcnkgZGlzdHJpYnV0aW9u
IG9mIFNjaVB5IGNhbiBhbHNvIGJ1bmRsZSB0aGUgZm9sbG93aW5nIHNvZnR3YXJlCiAoZGVwZW5k
aW5nIG9uIHRoZSBidWlsZCk6CgoKIE5hbWU6IE9wZW5CTEFTCiBGaWxlczogc2NpcHkubGlic1xs
aWJzY2lweV9vcGVuYmxhcyouZGxsCiBEZXNjcmlwdGlvbjogYnVuZGxlZCBhcyBhIGR5bmFtaWNh
bGx5IGxpbmtlZCBsaWJyYXJ5CiBBdmFpbGFiaWxpdHk6IGh0dHBzOi8vZ2l0aHViLmNvbS9PcGVu
TWF0aExpYi9PcGVuQkxBUy8KIExpY2Vuc2U6IEJTRC0zLUNsYXVzZQogICBDb3B5cmlnaHQgKGMp
IDIwMTEtMjAxNCwgVGhlIE9wZW5CTEFTIFByb2plY3QKICAgQWxsIHJpZ2h0cyByZXNlcnZlZC4K
CiAgIFJlZGlzdHJpYnV0aW9uIGFuZCB1c2UgaW4gc291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdp
dGggb3Igd2l0aG91dAogICBtb2RpZmljYXRpb24sIGFyZSBwZXJtaXR0ZWQgcHJvdmlkZWQgdGhh
dCB0aGUgZm9sbG93aW5nIGNvbmRpdGlvbnMgYXJlCiAgIG1ldDoKCiAgICAgIDEuIFJlZGlzdHJp
YnV0aW9ucyBvZiBzb3VyY2UgY29kZSBtdXN0IHJldGFpbiB0aGUgYWJvdmUgY29weXJpZ2h0CiAg
ICAgICAgIG5vdGljZSwgdGhpcyBsaXN0IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcg
ZGlzY2xhaW1lci4KCiAgICAgIDIuIFJlZGlzdHJpYnV0aW9ucyBpbiBiaW5hcnkgZm9ybSBtdXN0
IHJlcHJvZHVjZSB0aGUgYWJvdmUgY29weXJpZ2h0CiAgICAgICAgIG5vdGljZSwgdGhpcyBsaXN0
IG9mIGNvbmRpdGlvbnMgYW5kIHRoZSBmb2xsb3dpbmcgZGlzY2xhaW1lciBpbgogICAgICAgICB0
aGUgZG9jdW1lbnRhdGlvbiBhbmQvb3Igb3RoZXIgbWF0ZXJpYWxzIHByb3ZpZGVkIHdpdGggdGhl
CiAgICAgICAgIGRpc3RyaWJ1dGlvbi4KICAgICAgMy4gTmVpdGhlciB0aGUgbmFtZSBvZiB0aGUg
T3BlbkJMQVMgcHJvamVjdCBub3IgdGhlIG5hbWVzIG9mIAogICAgICAgICBpdHMgY29udHJpYnV0
b3JzIG1heSBiZSB1c2VkIHRvIGVuZG9yc2Ugb3IgcHJvbW90ZSBwcm9kdWN0cyAKICAgICAgICAg
ZGVyaXZlZCBmcm9tIHRoaXMgc29mdHdhcmUgd2l0aG91dCBzcGVjaWZpYyBwcmlvciB3cml0dGVu
IAogICAgICAgICBwZXJtaXNzaW9uLgoKICAgVEhJUyBTT0ZUV0FSRSBJUyBQUk9WSURFRCBCWSBU
SEUgQ09QWVJJR0hUIEhPTERFUlMgQU5EIENPTlRSSUJVVE9SUyAiQVMgSVMiCiAgIEFORCBBTlkg
RVhQUkVTUyBPUiBJTVBMSUVEIFdBUlJBTlRJRVMsIElOQ0xVRElORywgQlVUIE5PVCBMSU1JVEVE
IFRPLCBUSEUKICAgSU1QTElFRCBXQVJSQU5USUVTIE9GIE1FUkNIQU5UQUJJTElUWSBBTkQgRklU
TkVTUyBGT1IgQSBQQVJUSUNVTEFSIFBVUlBPU0UKICAgQVJFIERJU0NMQUlNRUQuIElOIE5PIEVW
RU5UIFNIQUxMIFRIRSBDT1BZUklHSFQgT1dORVIgT1IgQ09OVFJJQlVUT1JTIEJFCiAgIExJQUJM
RSBGT1IgQU5ZIERJUkVDVCwgSU5ESVJFQ1QsIElOQ0lERU5UQUwsIFNQRUNJQUwsIEVYRU1QTEFS
WSwgT1IgQ09OU0VRVUVOVElBTAogICBEQU1BR0VTIChJTkNMVURJTkcsIEJVVCBOT1QgTElNSVRF
RCBUTywgUFJPQ1VSRU1FTlQgT0YgU1VCU1RJVFVURSBHT09EUyBPUgogICBTRVJWSUNFUzsgTE9T
UyBPRiBVU0UsIERBVEEsIE9SIFBST0ZJVFM7IE9SIEJVU0lORVNTIElOVEVSUlVQVElPTikgSE9X
RVZFUgogICBDQVVTRUQgQU5EIE9OIEFOWSBUSEVPUlkgT0YgTElBQklMSVRZLCBXSEVUSEVSIElO
IENPTlRSQUNULCBTVFJJQ1QgTElBQklMSVRZLAogICBPUiBUT1JUIChJTkNMVURJTkcgTkVHTElH
RU5DRSBPUiBPVEhFUldJU0UpIEFSSVNJTkcgSU4gQU5ZIFdBWSBPVVQgT0YgVEhFCiAgIFVTRSBP
RiBUSElTIFNPRlRXQVJFLCBFVkVOIElGIEFEVklTRUQgT0YgVEhFIFBPU1NJQklMSVRZIE9GIFNV
Q0ggREFNQUdFLgoKCiBOYW1lOiBMQVBBQ0sKIEZpbGVzOiBzY2lweS5saWJzXGxpYnNjaXB5X29w
ZW5ibGFzKi5kbGwKIERlc2NyaXB0aW9uOiBidW5kbGVkIGluIE9wZW5CTEFTCiBBdmFpbGFiaWxp
dHk6IGh0dHBzOi8vZ2l0aHViLmNvbS9PcGVuTWF0aExpYi9PcGVuQkxBUy8KIExpY2Vuc2U6IEJT
RC0zLUNsYXVzZS1PcGVuLU1QSQogICBDb3B5cmlnaHQgKGMpIDE5OTItMjAxMyBUaGUgVW5pdmVy
c2l0eSBvZiBUZW5uZXNzZWUgYW5kIFRoZSBVbml2ZXJzaXR5CiAgICAgICAgICAgICAgICAgICAg
ICAgICAgIG9mIFRlbm5lc3NlZSBSZXNlYXJjaCBGb3VuZGF0aW9uLiAgQWxsIHJpZ2h0cwogICAg
ICAgICAgICAgICAgICAgICAgICAgICByZXNlcnZlZC4KICAgQ29weXJpZ2h0IChjKSAyMDAwLTIw
MTMgVGhlIFVuaXZlcnNpdHkgb2YgQ2FsaWZvcm5pYSBCZXJrZWxleS4gQWxsCiAgICAgICAgICAg
ICAgICAgICAgICAgICAgIHJpZ2h0cyByZXNlcnZlZC4KICAgQ29weXJpZ2h0IChjKSAyMDA2LTIw
MTMgVGhlIFVuaXZlcnNpdHkgb2YgQ29sb3JhZG8gRGVudmVyLiAgQWxsIHJpZ2h0cwogICAgICAg
ICAgICAgICAgICAgICAgICAgICByZXNlcnZlZC4KCiAgICRDT1BZUklHSFQkCgogICBBZGRpdGlv
bmFsIGNvcHlyaWdodHMgbWF5IGZvbGxvdwoKICAgJEhFQURFUiQKCiAgIFJlZGlzdHJpYnV0aW9u
IGFuZCB1c2UgaW4gc291cmNlIGFuZCBiaW5hcnkgZm9ybXMsIHdpdGggb3Igd2l0aG91dAogICBt
b2RpZmljYXRpb24sIGFyZSBwZXJtaXR0ZWQgcHJvdmlkZWQgdGhhdCB0aGUgZm9sbG93aW5nIGNv
bmRpdGlvbnMgYXJlCiAgIG1ldDoKCiAgIC0gUmVkaXN0cmlidXRpb25zIG9mIHNvdXJjZSBjb2Rl
IG11c3QgcmV0YWluIHRoZSBhYm92ZSBjb3B5cmlnaHQKICAgICBub3RpY2UsIHRoaXMgbGlzdCBv
ZiBjb25kaXRpb25zIGFuZCB0aGUgZm9sbG93aW5nIGRpc2NsYWltZXIuCgogICAtIFJlZGlzdHJp
YnV0aW9ucyBpbiBiaW5hcnkgZm9ybSBtdXN0IHJlcHJvZHVjZSB0aGUgYWJvdmUgY29weXJpZ2h0
CiAgICAgbm90aWNlLCB0aGlzIGxpc3Qgb2YgY29uZGl0aW9ucyBhbmQgdGhlIGZvbGxvd2luZyBk
aXNjbGFpbWVyIGxpc3RlZAogICAgIGluIHRoaXMgbGljZW5zZSBpbiB0aGUgZG9jdW1lbnRhdGlv
biBhbmQvb3Igb3RoZXIgbWF0ZXJpYWxzCiAgICAgcHJvdmlkZWQgd2l0aCB0aGUgZGlzdHJpYnV0
aW9uLgoKICAgLSBOZWl0aGVyIHRoZSBuYW1lIG9mIHRoZSBjb3B5cmlnaHQgaG9sZGVycyBub3Ig
dGhlIG5hbWVzIG9mIGl0cwogICAgIGNvbnRyaWJ1dG9ycyBtYXkgYmUgdXNlZCB0byBlbmRvcnNl
IG9yIHByb21vdGUgcHJvZHVjdHMgZGVyaXZlZCBmcm9tCiAgICAgdGhpcyBzb2Z0d2FyZSB3aXRo
b3V0IHNwZWNpZmljIHByaW9yIHdyaXR0ZW4gcGVybWlzc2lvbi4KCiAgIFRoZSBjb3B5cmlnaHQg
aG9sZGVycyBwcm92aWRlIG5vIHJlYXNzdXJhbmNlcyB0aGF0IHRoZSBzb3VyY2UgY29kZQogICBw
cm92aWRlZCBkb2VzIG5vdCBpbmZyaW5nZSBhbnkgcGF0ZW50LCBjb3B5cmlnaHQsIG9yIGFueSBv
dGhlcgogICBpbnRlbGxlY3R1YWwgcHJvcGVydHkgcmlnaHRzIG9mIHRoaXJkIHBhcnRpZXMuICBU
aGUgY29weXJpZ2h0IGhvbGRlcnMKICAgZGlzY2xhaW0gYW55IGxpYWJpbGl0eSB0byBhbnkgcmVj
aXBpZW50IGZvciBjbGFpbXMgYnJvdWdodCBhZ2FpbnN0CiAgIHJlY2lwaWVudCBieSBhbnkgdGhp
cmQgcGFydHkgZm9yIGluZnJpbmdlbWVudCBvZiB0aGF0IHBhcnRpZXMKICAgaW50ZWxsZWN0dWFs
IHByb3BlcnR5IHJpZ2h0cy4KCiAgIFRISVMgU09GVFdBUkUgSVMgUFJPVklERUQgQlkgVEhFIENP
UFlSSUdIVCBIT0xERVJTIEFORCBDT05UUklCVVRPUlMKICAgIkFTIElTIiBBTkQgQU5ZIEVYUFJF
U1MgT1IgSU1QTElFRCBXQVJSQU5USUVTLCBJTkNMVURJTkcsIEJVVCBOT1QKICAgTElNSVRFRCBU
TywgVEhFIElNUExJRUQgV0FSUkFOVElFUyBPRiBNRVJDSEFOVEFCSUxJVFkgQU5EIEZJVE5FU1Mg
Rk9SCiAgIEEgUEFSVElDVUxBUiBQVVJQT1NFIEFSRSBESVNDTEFJTUVELiBJTiBOTyBFVkVOVCBT
SEFMTCBUSEUgQ09QWVJJR0hUCiAgIE9XTkVSIE9SIENPTlRSSUJVVE9SUyBCRSBMSUFCTEUgRk9S
IEFOWSBESVJFQ1QsIElORElSRUNULCBJTkNJREVOVEFMLAogICBTUEVDSUFMLCBFWEVNUExBUlks
IE9SIENPTlNFUVVFTlRJQUwgREFNQUdFUyAoSU5DTFVESU5HLCBCVVQgTk9UCiAgIExJTUlURUQg
VE8sIFBST0NVUkVNRU5UIE9GIFNVQlNUSVRVVEUgR09PRFMgT1IgU0VSVklDRVM7IExPU1MgT0Yg
VVNFLAogICBEQVRBLCBPUiBQUk9GSVRTOyBPUiBCVVNJTkVTUyBJTlRFUlJVUFRJT04pIEhPV0VW
RVIgQ0FVU0VEIEFORCBPTiBBTlkKICAgVEhFT1JZIE9GIExJQUJJTElUWSwgV0hFVEhFUiBJTiBD
T05UUkFDVCwgU1RSSUNUIExJQUJJTElUWSwgT1IgVE9SVAogICAoSU5DTFVESU5HIE5FR0xJR0VO
Q0UgT1IgT1RIRVJXSVNFKSBBUklTSU5HIElOIEFOWSBXQVkgT1VUIE9GIFRIRSBVU0UKICAgT0Yg
VEhJUyBTT0ZUV0FSRSwgRVZFTiBJRiBBRFZJU0VEIE9GIFRIRSBQT1NTSUJJTElUWSBPRiBTVUNI
IERBTUFHRS4KCgogTmFtZTogR0NDIHJ1bnRpbWUgbGlicmFyeQogRmlsZXM6IHNjaXB5LmxpYnNc
bGlic2NpcHlfb3BlbmJsYXMqLmRsbAogRGVzY3JpcHRpb246IHN0YXRpY2FsbHkgbGlua2VkIHRv
IGZpbGVzIGNvbXBpbGVkIHdpdGggZ2NjCiBBdmFpbGFiaWxpdHk6IGh0dHBzOi8vZ2NjLmdudS5v
cmcvZ2l0Lz9wPWdjYy5naXQ7YT10cmVlO2Y9bGliZ2ZvcnRyYW4KIExpY2Vuc2U6IEdQTC0zLjAt
b3ItbGF0ZXIgV0lUSCBHQ0MtZXhjZXB0aW9uLTMuMQogICBDb3B5cmlnaHQgKEMpIDIwMDItMjAx
NyBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24sIEluYy4KCiAgIExpYmdmb3J0cmFuIGlzIGZyZWUg
c29mdHdhcmU7IHlvdSBjYW4gcmVkaXN0cmlidXRlIGl0IGFuZC9vciBtb2RpZnkKICAgaXQgdW5k
ZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBhcyBwdWJsaXNo
ZWQgYnkKICAgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyIHZlcnNpb24gMywg
b3IgKGF0IHlvdXIgb3B0aW9uKQogICBhbnkgbGF0ZXIgdmVyc2lvbi4KCiAgIExpYmdmb3J0cmFu
IGlzIGRpc3RyaWJ1dGVkIGluIHRoZSBob3BlIHRoYXQgaXQgd2lsbCBiZSB1c2VmdWwsCiAgIGJ1
dCBXSVRIT1VUIEFOWSBXQVJSQU5UWTsgd2l0aG91dCBldmVuIHRoZSBpbXBsaWVkIHdhcnJhbnR5
IG9mCiAgIE1FUkNIQU5UQUJJTElUWSBvciBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9T
RS4gIFNlZSB0aGUKICAgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgZm9yIG1vcmUgZGV0YWls
cy4KCiAgIFVuZGVyIFNlY3Rpb24gNyBvZiBHUEwgdmVyc2lvbiAzLCB5b3UgYXJlIGdyYW50ZWQg
YWRkaXRpb25hbAogICBwZXJtaXNzaW9ucyBkZXNjcmliZWQgaW4gdGhlIEdDQyBSdW50aW1lIExp
YnJhcnkgRXhjZXB0aW9uLCB2ZXJzaW9uCiAgIDMuMSwgYXMgcHVibGlzaGVkIGJ5IHRoZSBGcmVl
IFNvZnR3YXJlIEZvdW5kYXRpb24uCgogICBZb3Ugc2hvdWxkIGhhdmUgcmVjZWl2ZWQgYSBjb3B5
IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBhbmQKICAgYSBjb3B5IG9mIHRoZSBH
Q0MgUnVudGltZSBMaWJyYXJ5IEV4Y2VwdGlvbiBhbG9uZyB3aXRoIHRoaXMgcHJvZ3JhbTsKICAg
c2VlIHRoZSBmaWxlcyBDT1BZSU5HMyBhbmQgQ09QWUlORy5SVU5USU1FIHJlc3BlY3RpdmVseS4g
IElmIG5vdCwgc2VlCiAgIDxodHRwOi8vd3d3LmdudS5vcmcvbGljZW5zZXMvPi4KCgogLS0tLQoK
IEZ1bGwgdGV4dCBvZiBsaWNlbnNlIHRleHRzIHJlZmVycmVkIHRvIGFib3ZlIGZvbGxvd3MgKHRo
YXQgdGhleSBhcmUKIGxpc3RlZCBiZWxvdyBkb2VzIG5vdCBuZWNlc3NhcmlseSBpbXBseSB0aGUg
Y29uZGl0aW9ucyBhcHBseSB0byB0aGUKIHByZXNlbnQgYmluYXJ5IHJlbGVhc2UpOgoKIC0tLS0K
CiBHQ0MgUlVOVElNRSBMSUJSQVJZIEVYQ0VQVElPTgoKIFZlcnNpb24gMy4xLCAzMSBNYXJjaCAy
MDA5CgogQ29weXJpZ2h0IChDKSAyMDA5IEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbiwgSW5jLiA8
aHR0cDovL2ZzZi5vcmcvPgoKIEV2ZXJ5b25lIGlzIHBlcm1pdHRlZCB0byBjb3B5IGFuZCBkaXN0
cmlidXRlIHZlcmJhdGltIGNvcGllcyBvZiB0aGlzCiBsaWNlbnNlIGRvY3VtZW50LCBidXQgY2hh
bmdpbmcgaXQgaXMgbm90IGFsbG93ZWQuCgogVGhpcyBHQ0MgUnVudGltZSBMaWJyYXJ5IEV4Y2Vw
dGlvbiAoIkV4Y2VwdGlvbiIpIGlzIGFuIGFkZGl0aW9uYWwKIHBlcm1pc3Npb24gdW5kZXIgc2Vj
dGlvbiA3IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSwgdmVyc2lvbgogMyAoIkdQ
THYzIikuIEl0IGFwcGxpZXMgdG8gYSBnaXZlbiBmaWxlICh0aGUgIlJ1bnRpbWUgTGlicmFyeSIp
IHRoYXQKIGJlYXJzIGEgbm90aWNlIHBsYWNlZCBieSB0aGUgY29weXJpZ2h0IGhvbGRlciBvZiB0
aGUgZmlsZSBzdGF0aW5nIHRoYXQKIHRoZSBmaWxlIGlzIGdvdmVybmVkIGJ5IEdQTHYzIGFsb25n
IHdpdGggdGhpcyBFeGNlcHRpb24uCgogV2hlbiB5b3UgdXNlIEdDQyB0byBjb21waWxlIGEgcHJv
Z3JhbSwgR0NDIG1heSBjb21iaW5lIHBvcnRpb25zIG9mCiBjZXJ0YWluIEdDQyBoZWFkZXIgZmls
ZXMgYW5kIHJ1bnRpbWUgbGlicmFyaWVzIHdpdGggdGhlIGNvbXBpbGVkCiBwcm9ncmFtLiBUaGUg
cHVycG9zZSBvZiB0aGlzIEV4Y2VwdGlvbiBpcyB0byBhbGxvdyBjb21waWxhdGlvbiBvZgogbm9u
LUdQTCAoaW5jbHVkaW5nIHByb3ByaWV0YXJ5KSBwcm9ncmFtcyB0byB1c2UsIGluIHRoaXMgd2F5
LCB0aGUKIGhlYWRlciBmaWxlcyBhbmQgcnVudGltZSBsaWJyYXJpZXMgY292ZXJlZCBieSB0aGlz
IEV4Y2VwdGlvbi4KCiAwLiBEZWZpbml0aW9ucy4KCiBBIGZpbGUgaXMgYW4gIkluZGVwZW5kZW50
IE1vZHVsZSIgaWYgaXQgZWl0aGVyIHJlcXVpcmVzIHRoZSBSdW50aW1lCiBMaWJyYXJ5IGZvciBl
eGVjdXRpb24gYWZ0ZXIgYSBDb21waWxhdGlvbiBQcm9jZXNzLCBvciBtYWtlcyB1c2Ugb2YgYW4K
IGludGVyZmFjZSBwcm92aWRlZCBieSB0aGUgUnVudGltZSBMaWJyYXJ5LCBidXQgaXMgbm90IG90
aGVyd2lzZSBiYXNlZAogb24gdGhlIFJ1bnRpbWUgTGlicmFyeS4KCiAiR0NDIiBtZWFucyBhIHZl
cnNpb24gb2YgdGhlIEdOVSBDb21waWxlciBDb2xsZWN0aW9uLCB3aXRoIG9yIHdpdGhvdXQKIG1v
ZGlmaWNhdGlvbnMsIGdvdmVybmVkIGJ5IHZlcnNpb24gMyAob3IgYSBzcGVjaWZpZWQgbGF0ZXIg
dmVyc2lvbikgb2YKIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSAoR1BMKSB3aXRoIHRo
ZSBvcHRpb24gb2YgdXNpbmcgYW55CiBzdWJzZXF1ZW50IHZlcnNpb25zIHB1Ymxpc2hlZCBieSB0
aGUgRlNGLgoKICJHUEwtY29tcGF0aWJsZSBTb2Z0d2FyZSIgaXMgc29mdHdhcmUgd2hvc2UgY29u
ZGl0aW9ucyBvZiBwcm9wYWdhdGlvbiwKIG1vZGlmaWNhdGlvbiBhbmQgdXNlIHdvdWxkIHBlcm1p
dCBjb21iaW5hdGlvbiB3aXRoIEdDQyBpbiBhY2NvcmQgd2l0aAogdGhlIGxpY2Vuc2Ugb2YgR0ND
LgoKICJUYXJnZXQgQ29kZSIgcmVmZXJzIHRvIG91dHB1dCBmcm9tIGFueSBjb21waWxlciBmb3Ig
YSByZWFsIG9yIHZpcnR1YWwKIHRhcmdldCBwcm9jZXNzb3IgYXJjaGl0ZWN0dXJlLCBpbiBleGVj
dXRhYmxlIGZvcm0gb3Igc3VpdGFibGUgZm9yCiBpbnB1dCB0byBhbiBhc3NlbWJsZXIsIGxvYWRl
ciwgbGlua2VyIGFuZC9vciBleGVjdXRpb24KIHBoYXNlLiBOb3R3aXRoc3RhbmRpbmcgdGhhdCwg
VGFyZ2V0IENvZGUgZG9lcyBub3QgaW5jbHVkZSBkYXRhIGluIGFueQogZm9ybWF0IHRoYXQgaXMg
dXNlZCBhcyBhIGNvbXBpbGVyIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlvbiwgb3IgdXNlZAog
Zm9yIHByb2R1Y2luZyBhIGNvbXBpbGVyIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlvbi4KCiBU
aGUgIkNvbXBpbGF0aW9uIFByb2Nlc3MiIHRyYW5zZm9ybXMgY29kZSBlbnRpcmVseSByZXByZXNl
bnRlZCBpbgogbm9uLWludGVybWVkaWF0ZSBsYW5ndWFnZXMgZGVzaWduZWQgZm9yIGh1bWFuLXdy
aXR0ZW4gY29kZSwgYW5kL29yIGluCiBKYXZhIFZpcnR1YWwgTWFjaGluZSBieXRlIGNvZGUsIGlu
dG8gVGFyZ2V0IENvZGUuIFRodXMsIGZvciBleGFtcGxlLAogdXNlIG9mIHNvdXJjZSBjb2RlIGdl
bmVyYXRvcnMgYW5kIHByZXByb2Nlc3NvcnMgbmVlZCBub3QgYmUgY29uc2lkZXJlZAogcGFydCBv
ZiB0aGUgQ29tcGlsYXRpb24gUHJvY2Vzcywgc2luY2UgdGhlIENvbXBpbGF0aW9uIFByb2Nlc3Mg
Y2FuIGJlCiB1bmRlcnN0b29kIGFzIHN0YXJ0aW5nIHdpdGggdGhlIG91dHB1dCBvZiB0aGUgZ2Vu
ZXJhdG9ycyBvcgogcHJlcHJvY2Vzc29ycy4KCiBBIENvbXBpbGF0aW9uIFByb2Nlc3MgaXMgIkVs
aWdpYmxlIiBpZiBpdCBpcyBkb25lIHVzaW5nIEdDQywgYWxvbmUgb3IKIHdpdGggb3RoZXIgR1BM
LWNvbXBhdGlibGUgc29mdHdhcmUsIG9yIGlmIGl0IGlzIGRvbmUgd2l0aG91dCB1c2luZyBhbnkK
IHdvcmsgYmFzZWQgb24gR0NDLiBGb3IgZXhhbXBsZSwgdXNpbmcgbm9uLUdQTC1jb21wYXRpYmxl
IFNvZnR3YXJlIHRvCiBvcHRpbWl6ZSBhbnkgR0NDIGludGVybWVkaWF0ZSByZXByZXNlbnRhdGlv
bnMgd291bGQgbm90IHF1YWxpZnkgYXMgYW4KIEVsaWdpYmxlIENvbXBpbGF0aW9uIFByb2Nlc3Mu
CgogMS4gR3JhbnQgb2YgQWRkaXRpb25hbCBQZXJtaXNzaW9uLgoKIFlvdSBoYXZlIHBlcm1pc3Np
b24gdG8gcHJvcGFnYXRlIGEgd29yayBvZiBUYXJnZXQgQ29kZSBmb3JtZWQgYnkKIGNvbWJpbmlu
ZyB0aGUgUnVudGltZSBMaWJyYXJ5IHdpdGggSW5kZXBlbmRlbnQgTW9kdWxlcywgZXZlbiBpZiBz
dWNoCiBwcm9wYWdhdGlvbiB3b3VsZCBvdGhlcndpc2UgdmlvbGF0ZSB0aGUgdGVybXMgb2YgR1BM
djMsIHByb3ZpZGVkIHRoYXQKIGFsbCBUYXJnZXQgQ29kZSB3YXMgZ2VuZXJhdGVkIGJ5IEVsaWdp
YmxlIENvbXBpbGF0aW9uIFByb2Nlc3Nlcy4gWW91CiBtYXkgdGhlbiBjb252ZXkgc3VjaCBhIGNv
bWJpbmF0aW9uIHVuZGVyIHRlcm1zIG9mIHlvdXIgY2hvaWNlLAogY29uc2lzdGVudCB3aXRoIHRo
ZSBsaWNlbnNpbmcgb2YgdGhlIEluZGVwZW5kZW50IE1vZHVsZXMuCgogMi4gTm8gV2Vha2VuaW5n
IG9mIEdDQyBDb3B5bGVmdC4KCiBUaGUgYXZhaWxhYmlsaXR5IG9mIHRoaXMgRXhjZXB0aW9uIGRv
ZXMgbm90IGltcGx5IGFueSBnZW5lcmFsCiBwcmVzdW1wdGlvbiB0aGF0IHRoaXJkLXBhcnR5IHNv
ZnR3YXJlIGlzIHVuYWZmZWN0ZWQgYnkgdGhlIGNvcHlsZWZ0CiByZXF1aXJlbWVudHMgb2YgdGhl
IGxpY2Vuc2Ugb2YgR0NDLgoKIC0tLS0KCiAgICAgICAgICAgICAgICAgICAgIEdOVSBHRU5FUkFM
IFBVQkxJQyBMSUNFTlNFCiAgICAgICAgICAgICAgICAgICAgICAgIFZlcnNpb24gMywgMjkgSnVu
ZSAyMDA3CgogIENvcHlyaWdodCAoQykgMjAwNyBGcmVlIFNvZnR3YXJlIEZvdW5kYXRpb24sIElu
Yy4gPGh0dHA6Ly9mc2Yub3JnLz4KICBFdmVyeW9uZSBpcyBwZXJtaXR0ZWQgdG8gY29weSBhbmQg
ZGlzdHJpYnV0ZSB2ZXJiYXRpbSBjb3BpZXMKICBvZiB0aGlzIGxpY2Vuc2UgZG9jdW1lbnQsIGJ1
dCBjaGFuZ2luZyBpdCBpcyBub3QgYWxsb3dlZC4KCiAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgUHJlYW1ibGUKCiAgIFRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBpcyBhIGZyZWUs
IGNvcHlsZWZ0IGxpY2Vuc2UgZm9yCiBzb2Z0d2FyZSBhbmQgb3RoZXIga2luZHMgb2Ygd29ya3Mu
CgogICBUaGUgbGljZW5zZXMgZm9yIG1vc3Qgc29mdHdhcmUgYW5kIG90aGVyIHByYWN0aWNhbCB3
b3JrcyBhcmUgZGVzaWduZWQKIHRvIHRha2UgYXdheSB5b3VyIGZyZWVkb20gdG8gc2hhcmUgYW5k
IGNoYW5nZSB0aGUgd29ya3MuICBCeSBjb250cmFzdCwKIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMg
TGljZW5zZSBpcyBpbnRlbmRlZCB0byBndWFyYW50ZWUgeW91ciBmcmVlZG9tIHRvCiBzaGFyZSBh
bmQgY2hhbmdlIGFsbCB2ZXJzaW9ucyBvZiBhIHByb2dyYW0tLXRvIG1ha2Ugc3VyZSBpdCByZW1h
aW5zIGZyZWUKIHNvZnR3YXJlIGZvciBhbGwgaXRzIHVzZXJzLiAgV2UsIHRoZSBGcmVlIFNvZnR3
YXJlIEZvdW5kYXRpb24sIHVzZSB0aGUKIEdOVSBHZW5lcmFsIFB1YmxpYyBMaWNlbnNlIGZvciBt
b3N0IG9mIG91ciBzb2Z0d2FyZTsgaXQgYXBwbGllcyBhbHNvIHRvCiBhbnkgb3RoZXIgd29yayBy
ZWxlYXNlZCB0aGlzIHdheSBieSBpdHMgYXV0aG9ycy4gIFlvdSBjYW4gYXBwbHkgaXQgdG8KIHlv
dXIgcHJvZ3JhbXMsIHRvby4KCiAgIFdoZW4gd2Ugc3BlYWsgb2YgZnJlZSBzb2Z0d2FyZSwgd2Ug
YXJlIHJlZmVycmluZyB0byBmcmVlZG9tLCBub3QKIHByaWNlLiAgT3VyIEdlbmVyYWwgUHVibGlj
IExpY2Vuc2VzIGFyZSBkZXNpZ25lZCB0byBtYWtlIHN1cmUgdGhhdCB5b3UKIGhhdmUgdGhlIGZy
ZWVkb20gdG8gZGlzdHJpYnV0ZSBjb3BpZXMgb2YgZnJlZSBzb2Z0d2FyZSAoYW5kIGNoYXJnZSBm
b3IKIHRoZW0gaWYgeW91IHdpc2gpLCB0aGF0IHlvdSByZWNlaXZlIHNvdXJjZSBjb2RlIG9yIGNh
biBnZXQgaXQgaWYgeW91CiB3YW50IGl0LCB0aGF0IHlvdSBjYW4gY2hhbmdlIHRoZSBzb2Z0d2Fy
ZSBvciB1c2UgcGllY2VzIG9mIGl0IGluIG5ldwogZnJlZSBwcm9ncmFtcywgYW5kIHRoYXQgeW91
IGtub3cgeW91IGNhbiBkbyB0aGVzZSB0aGluZ3MuCgogICBUbyBwcm90ZWN0IHlvdXIgcmlnaHRz
LCB3ZSBuZWVkIHRvIHByZXZlbnQgb3RoZXJzIGZyb20gZGVueWluZyB5b3UKIHRoZXNlIHJpZ2h0
cyBvciBhc2tpbmcgeW91IHRvIHN1cnJlbmRlciB0aGUgcmlnaHRzLiAgVGhlcmVmb3JlLCB5b3Ug
aGF2ZQogY2VydGFpbiByZXNwb25zaWJpbGl0aWVzIGlmIHlvdSBkaXN0cmlidXRlIGNvcGllcyBv
ZiB0aGUgc29mdHdhcmUsIG9yIGlmCiB5b3UgbW9kaWZ5IGl0OiByZXNwb25zaWJpbGl0aWVzIHRv
IHJlc3BlY3QgdGhlIGZyZWVkb20gb2Ygb3RoZXJzLgoKICAgRm9yIGV4YW1wbGUsIGlmIHlvdSBk
aXN0cmlidXRlIGNvcGllcyBvZiBzdWNoIGEgcHJvZ3JhbSwgd2hldGhlcgogZ3JhdGlzIG9yIGZv
ciBhIGZlZSwgeW91IG11c3QgcGFzcyBvbiB0byB0aGUgcmVjaXBpZW50cyB0aGUgc2FtZQogZnJl
ZWRvbXMgdGhhdCB5b3UgcmVjZWl2ZWQuICBZb3UgbXVzdCBtYWtlIHN1cmUgdGhhdCB0aGV5LCB0
b28sIHJlY2VpdmUKIG9yIGNhbiBnZXQgdGhlIHNvdXJjZSBjb2RlLiAgQW5kIHlvdSBtdXN0IHNo
b3cgdGhlbSB0aGVzZSB0ZXJtcyBzbyB0aGV5CiBrbm93IHRoZWlyIHJpZ2h0cy4KCiAgIERldmVs
b3BlcnMgdGhhdCB1c2UgdGhlIEdOVSBHUEwgcHJvdGVjdCB5b3VyIHJpZ2h0cyB3aXRoIHR3byBz
dGVwczoKICgxKSBhc3NlcnQgY29weXJpZ2h0IG9uIHRoZSBzb2Z0d2FyZSwgYW5kICgyKSBvZmZl
ciB5b3UgdGhpcyBMaWNlbnNlCiBnaXZpbmcgeW91IGxlZ2FsIHBlcm1pc3Npb24gdG8gY29weSwg
ZGlzdHJpYnV0ZSBhbmQvb3IgbW9kaWZ5IGl0LgoKICAgRm9yIHRoZSBkZXZlbG9wZXJzJyBhbmQg
YXV0aG9ycycgcHJvdGVjdGlvbiwgdGhlIEdQTCBjbGVhcmx5IGV4cGxhaW5zCiB0aGF0IHRoZXJl
IGlzIG5vIHdhcnJhbnR5IGZvciB0aGlzIGZyZWUgc29mdHdhcmUuICBGb3IgYm90aCB1c2Vycycg
YW5kCiBhdXRob3JzJyBzYWtlLCB0aGUgR1BMIHJlcXVpcmVzIHRoYXQgbW9kaWZpZWQgdmVyc2lv
bnMgYmUgbWFya2VkIGFzCiBjaGFuZ2VkLCBzbyB0aGF0IHRoZWlyIHByb2JsZW1zIHdpbGwgbm90
IGJlIGF0dHJpYnV0ZWQgZXJyb25lb3VzbHkgdG8KIGF1dGhvcnMgb2YgcHJldmlvdXMgdmVyc2lv
bnMuCgogICBTb21lIGRldmljZXMgYXJlIGRlc2lnbmVkIHRvIGRlbnkgdXNlcnMgYWNjZXNzIHRv
IGluc3RhbGwgb3IgcnVuCiBtb2RpZmllZCB2ZXJzaW9ucyBvZiB0aGUgc29mdHdhcmUgaW5zaWRl
IHRoZW0sIGFsdGhvdWdoIHRoZSBtYW51ZmFjdHVyZXIKIGNhbiBkbyBzby4gIFRoaXMgaXMgZnVu
ZGFtZW50YWxseSBpbmNvbXBhdGlibGUgd2l0aCB0aGUgYWltIG9mCiBwcm90ZWN0aW5nIHVzZXJz
JyBmcmVlZG9tIHRvIGNoYW5nZSB0aGUgc29mdHdhcmUuICBUaGUgc3lzdGVtYXRpYwogcGF0dGVy
biBvZiBzdWNoIGFidXNlIG9jY3VycyBpbiB0aGUgYXJlYSBvZiBwcm9kdWN0cyBmb3IgaW5kaXZp
ZHVhbHMgdG8KIHVzZSwgd2hpY2ggaXMgcHJlY2lzZWx5IHdoZXJlIGl0IGlzIG1vc3QgdW5hY2Nl
cHRhYmxlLiAgVGhlcmVmb3JlLCB3ZQogaGF2ZSBkZXNpZ25lZCB0aGlzIHZlcnNpb24gb2YgdGhl
IEdQTCB0byBwcm9oaWJpdCB0aGUgcHJhY3RpY2UgZm9yIHRob3NlCiBwcm9kdWN0cy4gIElmIHN1
Y2ggcHJvYmxlbXMgYXJpc2Ugc3Vic3RhbnRpYWxseSBpbiBvdGhlciBkb21haW5zLCB3ZQogc3Rh
bmQgcmVhZHkgdG8gZXh0ZW5kIHRoaXMgcHJvdmlzaW9uIHRvIHRob3NlIGRvbWFpbnMgaW4gZnV0
dXJlIHZlcnNpb25zCiBvZiB0aGUgR1BMLCBhcyBuZWVkZWQgdG8gcHJvdGVjdCB0aGUgZnJlZWRv
bSBvZiB1c2Vycy4KCiAgIEZpbmFsbHksIGV2ZXJ5IHByb2dyYW0gaXMgdGhyZWF0ZW5lZCBjb25z
dGFudGx5IGJ5IHNvZnR3YXJlIHBhdGVudHMuCiBTdGF0ZXMgc2hvdWxkIG5vdCBhbGxvdyBwYXRl
bnRzIHRvIHJlc3RyaWN0IGRldmVsb3BtZW50IGFuZCB1c2Ugb2YKIHNvZnR3YXJlIG9uIGdlbmVy
YWwtcHVycG9zZSBjb21wdXRlcnMsIGJ1dCBpbiB0aG9zZSB0aGF0IGRvLCB3ZSB3aXNoIHRvCiBh
dm9pZCB0aGUgc3BlY2lhbCBkYW5nZXIgdGhhdCBwYXRlbnRzIGFwcGxpZWQgdG8gYSBmcmVlIHBy
b2dyYW0gY291bGQKIG1ha2UgaXQgZWZmZWN0aXZlbHkgcHJvcHJpZXRhcnkuICBUbyBwcmV2ZW50
IHRoaXMsIHRoZSBHUEwgYXNzdXJlcyB0aGF0CiBwYXRlbnRzIGNhbm5vdCBiZSB1c2VkIHRvIHJl
bmRlciB0aGUgcHJvZ3JhbSBub24tZnJlZS4KCiAgIFRoZSBwcmVjaXNlIHRlcm1zIGFuZCBjb25k
aXRpb25zIGZvciBjb3B5aW5nLCBkaXN0cmlidXRpb24gYW5kCiBtb2RpZmljYXRpb24gZm9sbG93
LgoKICAgICAgICAgICAgICAgICAgICAgICAgVEVSTVMgQU5EIENPTkRJVElPTlMKCiAgIDAuIERl
ZmluaXRpb25zLgoKICAgIlRoaXMgTGljZW5zZSIgcmVmZXJzIHRvIHZlcnNpb24gMyBvZiB0aGUg
R05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UuCgogICAiQ29weXJpZ2h0IiBhbHNvIG1lYW5zIGNv
cHlyaWdodC1saWtlIGxhd3MgdGhhdCBhcHBseSB0byBvdGhlciBraW5kcyBvZgogd29ya3MsIHN1
Y2ggYXMgc2VtaWNvbmR1Y3RvciBtYXNrcy4KCiAgICJUaGUgUHJvZ3JhbSIgcmVmZXJzIHRvIGFu
eSBjb3B5cmlnaHRhYmxlIHdvcmsgbGljZW5zZWQgdW5kZXIgdGhpcwogTGljZW5zZS4gIEVhY2gg
bGljZW5zZWUgaXMgYWRkcmVzc2VkIGFzICJ5b3UiLiAgIkxpY2Vuc2VlcyIgYW5kCiAicmVjaXBp
ZW50cyIgbWF5IGJlIGluZGl2aWR1YWxzIG9yIG9yZ2FuaXphdGlvbnMuCgogICBUbyAibW9kaWZ5
IiBhIHdvcmsgbWVhbnMgdG8gY29weSBmcm9tIG9yIGFkYXB0IGFsbCBvciBwYXJ0IG9mIHRoZSB3
b3JrCiBpbiBhIGZhc2hpb24gcmVxdWlyaW5nIGNvcHlyaWdodCBwZXJtaXNzaW9uLCBvdGhlciB0
aGFuIHRoZSBtYWtpbmcgb2YgYW4KIGV4YWN0IGNvcHkuICBUaGUgcmVzdWx0aW5nIHdvcmsgaXMg
Y2FsbGVkIGEgIm1vZGlmaWVkIHZlcnNpb24iIG9mIHRoZQogZWFybGllciB3b3JrIG9yIGEgd29y
ayAiYmFzZWQgb24iIHRoZSBlYXJsaWVyIHdvcmsuCgogICBBICJjb3ZlcmVkIHdvcmsiIG1lYW5z
IGVpdGhlciB0aGUgdW5tb2RpZmllZCBQcm9ncmFtIG9yIGEgd29yayBiYXNlZAogb24gdGhlIFBy
b2dyYW0uCgogICBUbyAicHJvcGFnYXRlIiBhIHdvcmsgbWVhbnMgdG8gZG8gYW55dGhpbmcgd2l0
aCBpdCB0aGF0LCB3aXRob3V0CiBwZXJtaXNzaW9uLCB3b3VsZCBtYWtlIHlvdSBkaXJlY3RseSBv
ciBzZWNvbmRhcmlseSBsaWFibGUgZm9yCiBpbmZyaW5nZW1lbnQgdW5kZXIgYXBwbGljYWJsZSBj
b3B5cmlnaHQgbGF3LCBleGNlcHQgZXhlY3V0aW5nIGl0IG9uIGEKIGNvbXB1dGVyIG9yIG1vZGlm
eWluZyBhIHByaXZhdGUgY29weS4gIFByb3BhZ2F0aW9uIGluY2x1ZGVzIGNvcHlpbmcsCiBkaXN0
cmlidXRpb24gKHdpdGggb3Igd2l0aG91dCBtb2RpZmljYXRpb24pLCBtYWtpbmcgYXZhaWxhYmxl
IHRvIHRoZQogcHVibGljLCBhbmQgaW4gc29tZSBjb3VudHJpZXMgb3RoZXIgYWN0aXZpdGllcyBh
cyB3ZWxsLgoKICAgVG8gImNvbnZleSIgYSB3b3JrIG1lYW5zIGFueSBraW5kIG9mIHByb3BhZ2F0
aW9uIHRoYXQgZW5hYmxlcyBvdGhlcgogcGFydGllcyB0byBtYWtlIG9yIHJlY2VpdmUgY29waWVz
LiAgTWVyZSBpbnRlcmFjdGlvbiB3aXRoIGEgdXNlciB0aHJvdWdoCiBhIGNvbXB1dGVyIG5ldHdv
cmssIHdpdGggbm8gdHJhbnNmZXIgb2YgYSBjb3B5LCBpcyBub3QgY29udmV5aW5nLgoKICAgQW4g
aW50ZXJhY3RpdmUgdXNlciBpbnRlcmZhY2UgZGlzcGxheXMgIkFwcHJvcHJpYXRlIExlZ2FsIE5v
dGljZXMiCiB0byB0aGUgZXh0ZW50IHRoYXQgaXQgaW5jbHVkZXMgYSBjb252ZW5pZW50IGFuZCBw
cm9taW5lbnRseSB2aXNpYmxlCiBmZWF0dXJlIHRoYXQgKDEpIGRpc3BsYXlzIGFuIGFwcHJvcHJp
YXRlIGNvcHlyaWdodCBub3RpY2UsIGFuZCAoMikKIHRlbGxzIHRoZSB1c2VyIHRoYXQgdGhlcmUg
aXMgbm8gd2FycmFudHkgZm9yIHRoZSB3b3JrIChleGNlcHQgdG8gdGhlCiBleHRlbnQgdGhhdCB3
YXJyYW50aWVzIGFyZSBwcm92aWRlZCksIHRoYXQgbGljZW5zZWVzIG1heSBjb252ZXkgdGhlCiB3
b3JrIHVuZGVyIHRoaXMgTGljZW5zZSwgYW5kIGhvdyB0byB2aWV3IGEgY29weSBvZiB0aGlzIExp
Y2Vuc2UuICBJZgogdGhlIGludGVyZmFjZSBwcmVzZW50cyBhIGxpc3Qgb2YgdXNlciBjb21tYW5k
cyBvciBvcHRpb25zLCBzdWNoIGFzIGEKIG1lbnUsIGEgcHJvbWluZW50IGl0ZW0gaW4gdGhlIGxp
c3QgbWVldHMgdGhpcyBjcml0ZXJpb24uCgogICAxLiBTb3VyY2UgQ29kZS4KCiAgIFRoZSAic291
cmNlIGNvZGUiIGZvciBhIHdvcmsgbWVhbnMgdGhlIHByZWZlcnJlZCBmb3JtIG9mIHRoZSB3b3Jr
CiBmb3IgbWFraW5nIG1vZGlmaWNhdGlvbnMgdG8gaXQuICAiT2JqZWN0IGNvZGUiIG1lYW5zIGFu
eSBub24tc291cmNlCiBmb3JtIG9mIGEgd29yay4KCiAgIEEgIlN0YW5kYXJkIEludGVyZmFjZSIg
bWVhbnMgYW4gaW50ZXJmYWNlIHRoYXQgZWl0aGVyIGlzIGFuIG9mZmljaWFsCiBzdGFuZGFyZCBk
ZWZpbmVkIGJ5IGEgcmVjb2duaXplZCBzdGFuZGFyZHMgYm9keSwgb3IsIGluIHRoZSBjYXNlIG9m
CiBpbnRlcmZhY2VzIHNwZWNpZmllZCBmb3IgYSBwYXJ0aWN1bGFyIHByb2dyYW1taW5nIGxhbmd1
YWdlLCBvbmUgdGhhdAogaXMgd2lkZWx5IHVzZWQgYW1vbmcgZGV2ZWxvcGVycyB3b3JraW5nIGlu
IHRoYXQgbGFuZ3VhZ2UuCgogICBUaGUgIlN5c3RlbSBMaWJyYXJpZXMiIG9mIGFuIGV4ZWN1dGFi
bGUgd29yayBpbmNsdWRlIGFueXRoaW5nLCBvdGhlcgogdGhhbiB0aGUgd29yayBhcyBhIHdob2xl
LCB0aGF0IChhKSBpcyBpbmNsdWRlZCBpbiB0aGUgbm9ybWFsIGZvcm0gb2YKIHBhY2thZ2luZyBh
IE1ham9yIENvbXBvbmVudCwgYnV0IHdoaWNoIGlzIG5vdCBwYXJ0IG9mIHRoYXQgTWFqb3IKIENv
bXBvbmVudCwgYW5kIChiKSBzZXJ2ZXMgb25seSB0byBlbmFibGUgdXNlIG9mIHRoZSB3b3JrIHdp
dGggdGhhdAogTWFqb3IgQ29tcG9uZW50LCBvciB0byBpbXBsZW1lbnQgYSBTdGFuZGFyZCBJbnRl
cmZhY2UgZm9yIHdoaWNoIGFuCiBpbXBsZW1lbnRhdGlvbiBpcyBhdmFpbGFibGUgdG8gdGhlIHB1
YmxpYyBpbiBzb3VyY2UgY29kZSBmb3JtLiAgQQogIk1ham9yIENvbXBvbmVudCIsIGluIHRoaXMg
Y29udGV4dCwgbWVhbnMgYSBtYWpvciBlc3NlbnRpYWwgY29tcG9uZW50CiAoa2VybmVsLCB3aW5k
b3cgc3lzdGVtLCBhbmQgc28gb24pIG9mIHRoZSBzcGVjaWZpYyBvcGVyYXRpbmcgc3lzdGVtCiAo
aWYgYW55KSBvbiB3aGljaCB0aGUgZXhlY3V0YWJsZSB3b3JrIHJ1bnMsIG9yIGEgY29tcGlsZXIg
dXNlZCB0bwogcHJvZHVjZSB0aGUgd29yaywgb3IgYW4gb2JqZWN0IGNvZGUgaW50ZXJwcmV0ZXIg
dXNlZCB0byBydW4gaXQuCgogICBUaGUgIkNvcnJlc3BvbmRpbmcgU291cmNlIiBmb3IgYSB3b3Jr
IGluIG9iamVjdCBjb2RlIGZvcm0gbWVhbnMgYWxsCiB0aGUgc291cmNlIGNvZGUgbmVlZGVkIHRv
IGdlbmVyYXRlLCBpbnN0YWxsLCBhbmQgKGZvciBhbiBleGVjdXRhYmxlCiB3b3JrKSBydW4gdGhl
IG9iamVjdCBjb2RlIGFuZCB0byBtb2RpZnkgdGhlIHdvcmssIGluY2x1ZGluZyBzY3JpcHRzIHRv
CiBjb250cm9sIHRob3NlIGFjdGl2aXRpZXMuICBIb3dldmVyLCBpdCBkb2VzIG5vdCBpbmNsdWRl
IHRoZSB3b3JrJ3MKIFN5c3RlbSBMaWJyYXJpZXMsIG9yIGdlbmVyYWwtcHVycG9zZSB0b29scyBv
ciBnZW5lcmFsbHkgYXZhaWxhYmxlIGZyZWUKIHByb2dyYW1zIHdoaWNoIGFyZSB1c2VkIHVubW9k
aWZpZWQgaW4gcGVyZm9ybWluZyB0aG9zZSBhY3Rpdml0aWVzIGJ1dAogd2hpY2ggYXJlIG5vdCBw
YXJ0IG9mIHRoZSB3b3JrLiAgRm9yIGV4YW1wbGUsIENvcnJlc3BvbmRpbmcgU291cmNlCiBpbmNs
dWRlcyBpbnRlcmZhY2UgZGVmaW5pdGlvbiBmaWxlcyBhc3NvY2lhdGVkIHdpdGggc291cmNlIGZp
bGVzIGZvcgogdGhlIHdvcmssIGFuZCB0aGUgc291cmNlIGNvZGUgZm9yIHNoYXJlZCBsaWJyYXJp
ZXMgYW5kIGR5bmFtaWNhbGx5CiBsaW5rZWQgc3VicHJvZ3JhbXMgdGhhdCB0aGUgd29yayBpcyBz
cGVjaWZpY2FsbHkgZGVzaWduZWQgdG8gcmVxdWlyZSwKIHN1Y2ggYXMgYnkgaW50aW1hdGUgZGF0
YSBjb21tdW5pY2F0aW9uIG9yIGNvbnRyb2wgZmxvdyBiZXR3ZWVuIHRob3NlCiBzdWJwcm9ncmFt
cyBhbmQgb3RoZXIgcGFydHMgb2YgdGhlIHdvcmsuCgogICBUaGUgQ29ycmVzcG9uZGluZyBTb3Vy
Y2UgbmVlZCBub3QgaW5jbHVkZSBhbnl0aGluZyB0aGF0IHVzZXJzCiBjYW4gcmVnZW5lcmF0ZSBh
dXRvbWF0aWNhbGx5IGZyb20gb3RoZXIgcGFydHMgb2YgdGhlIENvcnJlc3BvbmRpbmcKIFNvdXJj
ZS4KCiAgIFRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZSBmb3IgYSB3b3JrIGluIHNvdXJjZSBjb2Rl
IGZvcm0gaXMgdGhhdAogc2FtZSB3b3JrLgoKICAgMi4gQmFzaWMgUGVybWlzc2lvbnMuCgogICBB
bGwgcmlnaHRzIGdyYW50ZWQgdW5kZXIgdGhpcyBMaWNlbnNlIGFyZSBncmFudGVkIGZvciB0aGUg
dGVybSBvZgogY29weXJpZ2h0IG9uIHRoZSBQcm9ncmFtLCBhbmQgYXJlIGlycmV2b2NhYmxlIHBy
b3ZpZGVkIHRoZSBzdGF0ZWQKIGNvbmRpdGlvbnMgYXJlIG1ldC4gIFRoaXMgTGljZW5zZSBleHBs
aWNpdGx5IGFmZmlybXMgeW91ciB1bmxpbWl0ZWQKIHBlcm1pc3Npb24gdG8gcnVuIHRoZSB1bm1v
ZGlmaWVkIFByb2dyYW0uICBUaGUgb3V0cHV0IGZyb20gcnVubmluZyBhCiBjb3ZlcmVkIHdvcmsg
aXMgY292ZXJlZCBieSB0aGlzIExpY2Vuc2Ugb25seSBpZiB0aGUgb3V0cHV0LCBnaXZlbiBpdHMK
IGNvbnRlbnQsIGNvbnN0aXR1dGVzIGEgY292ZXJlZCB3b3JrLiAgVGhpcyBMaWNlbnNlIGFja25v
d2xlZGdlcyB5b3VyCiByaWdodHMgb2YgZmFpciB1c2Ugb3Igb3RoZXIgZXF1aXZhbGVudCwgYXMg
cHJvdmlkZWQgYnkgY29weXJpZ2h0IGxhdy4KCiAgIFlvdSBtYXkgbWFrZSwgcnVuIGFuZCBwcm9w
YWdhdGUgY292ZXJlZCB3b3JrcyB0aGF0IHlvdSBkbyBub3QKIGNvbnZleSwgd2l0aG91dCBjb25k
aXRpb25zIHNvIGxvbmcgYXMgeW91ciBsaWNlbnNlIG90aGVyd2lzZSByZW1haW5zCiBpbiBmb3Jj
ZS4gIFlvdSBtYXkgY29udmV5IGNvdmVyZWQgd29ya3MgdG8gb3RoZXJzIGZvciB0aGUgc29sZSBw
dXJwb3NlCiBvZiBoYXZpbmcgdGhlbSBtYWtlIG1vZGlmaWNhdGlvbnMgZXhjbHVzaXZlbHkgZm9y
IHlvdSwgb3IgcHJvdmlkZSB5b3UKIHdpdGggZmFjaWxpdGllcyBmb3IgcnVubmluZyB0aG9zZSB3
b3JrcywgcHJvdmlkZWQgdGhhdCB5b3UgY29tcGx5IHdpdGgKIHRoZSB0ZXJtcyBvZiB0aGlzIExp
Y2Vuc2UgaW4gY29udmV5aW5nIGFsbCBtYXRlcmlhbCBmb3Igd2hpY2ggeW91IGRvCiBub3QgY29u
dHJvbCBjb3B5cmlnaHQuICBUaG9zZSB0aHVzIG1ha2luZyBvciBydW5uaW5nIHRoZSBjb3ZlcmVk
IHdvcmtzCiBmb3IgeW91IG11c3QgZG8gc28gZXhjbHVzaXZlbHkgb24geW91ciBiZWhhbGYsIHVu
ZGVyIHlvdXIgZGlyZWN0aW9uCiBhbmQgY29udHJvbCwgb24gdGVybXMgdGhhdCBwcm9oaWJpdCB0
aGVtIGZyb20gbWFraW5nIGFueSBjb3BpZXMgb2YKIHlvdXIgY29weXJpZ2h0ZWQgbWF0ZXJpYWwg
b3V0c2lkZSB0aGVpciByZWxhdGlvbnNoaXAgd2l0aCB5b3UuCgogICBDb252ZXlpbmcgdW5kZXIg
YW55IG90aGVyIGNpcmN1bXN0YW5jZXMgaXMgcGVybWl0dGVkIHNvbGVseSB1bmRlcgogdGhlIGNv
bmRpdGlvbnMgc3RhdGVkIGJlbG93LiAgU3VibGljZW5zaW5nIGlzIG5vdCBhbGxvd2VkOyBzZWN0
aW9uIDEwCiBtYWtlcyBpdCB1bm5lY2Vzc2FyeS4KCiAgIDMuIFByb3RlY3RpbmcgVXNlcnMnIExl
Z2FsIFJpZ2h0cyBGcm9tIEFudGktQ2lyY3VtdmVudGlvbiBMYXcuCgogICBObyBjb3ZlcmVkIHdv
cmsgc2hhbGwgYmUgZGVlbWVkIHBhcnQgb2YgYW4gZWZmZWN0aXZlIHRlY2hub2xvZ2ljYWwKIG1l
YXN1cmUgdW5kZXIgYW55IGFwcGxpY2FibGUgbGF3IGZ1bGZpbGxpbmcgb2JsaWdhdGlvbnMgdW5k
ZXIgYXJ0aWNsZQogMTEgb2YgdGhlIFdJUE8gY29weXJpZ2h0IHRyZWF0eSBhZG9wdGVkIG9uIDIw
IERlY2VtYmVyIDE5OTYsIG9yCiBzaW1pbGFyIGxhd3MgcHJvaGliaXRpbmcgb3IgcmVzdHJpY3Rp
bmcgY2lyY3VtdmVudGlvbiBvZiBzdWNoCiBtZWFzdXJlcy4KCiAgIFdoZW4geW91IGNvbnZleSBh
IGNvdmVyZWQgd29yaywgeW91IHdhaXZlIGFueSBsZWdhbCBwb3dlciB0byBmb3JiaWQKIGNpcmN1
bXZlbnRpb24gb2YgdGVjaG5vbG9naWNhbCBtZWFzdXJlcyB0byB0aGUgZXh0ZW50IHN1Y2ggY2ly
Y3VtdmVudGlvbgogaXMgZWZmZWN0ZWQgYnkgZXhlcmNpc2luZyByaWdodHMgdW5kZXIgdGhpcyBM
aWNlbnNlIHdpdGggcmVzcGVjdCB0bwogdGhlIGNvdmVyZWQgd29yaywgYW5kIHlvdSBkaXNjbGFp
bSBhbnkgaW50ZW50aW9uIHRvIGxpbWl0IG9wZXJhdGlvbiBvcgogbW9kaWZpY2F0aW9uIG9mIHRo
ZSB3b3JrIGFzIGEgbWVhbnMgb2YgZW5mb3JjaW5nLCBhZ2FpbnN0IHRoZSB3b3JrJ3MKIHVzZXJz
LCB5b3VyIG9yIHRoaXJkIHBhcnRpZXMnIGxlZ2FsIHJpZ2h0cyB0byBmb3JiaWQgY2lyY3VtdmVu
dGlvbiBvZgogdGVjaG5vbG9naWNhbCBtZWFzdXJlcy4KCiAgIDQuIENvbnZleWluZyBWZXJiYXRp
bSBDb3BpZXMuCgogICBZb3UgbWF5IGNvbnZleSB2ZXJiYXRpbSBjb3BpZXMgb2YgdGhlIFByb2dy
YW0ncyBzb3VyY2UgY29kZSBhcyB5b3UKIHJlY2VpdmUgaXQsIGluIGFueSBtZWRpdW0sIHByb3Zp
ZGVkIHRoYXQgeW91IGNvbnNwaWN1b3VzbHkgYW5kCiBhcHByb3ByaWF0ZWx5IHB1Ymxpc2ggb24g
ZWFjaCBjb3B5IGFuIGFwcHJvcHJpYXRlIGNvcHlyaWdodCBub3RpY2U7CiBrZWVwIGludGFjdCBh
bGwgbm90aWNlcyBzdGF0aW5nIHRoYXQgdGhpcyBMaWNlbnNlIGFuZCBhbnkKIG5vbi1wZXJtaXNz
aXZlIHRlcm1zIGFkZGVkIGluIGFjY29yZCB3aXRoIHNlY3Rpb24gNyBhcHBseSB0byB0aGUgY29k
ZTsKIGtlZXAgaW50YWN0IGFsbCBub3RpY2VzIG9mIHRoZSBhYnNlbmNlIG9mIGFueSB3YXJyYW50
eTsgYW5kIGdpdmUgYWxsCiByZWNpcGllbnRzIGEgY29weSBvZiB0aGlzIExpY2Vuc2UgYWxvbmcg
d2l0aCB0aGUgUHJvZ3JhbS4KCiAgIFlvdSBtYXkgY2hhcmdlIGFueSBwcmljZSBvciBubyBwcmlj
ZSBmb3IgZWFjaCBjb3B5IHRoYXQgeW91IGNvbnZleSwKIGFuZCB5b3UgbWF5IG9mZmVyIHN1cHBv
cnQgb3Igd2FycmFudHkgcHJvdGVjdGlvbiBmb3IgYSBmZWUuCgogICA1LiBDb252ZXlpbmcgTW9k
aWZpZWQgU291cmNlIFZlcnNpb25zLgoKICAgWW91IG1heSBjb252ZXkgYSB3b3JrIGJhc2VkIG9u
IHRoZSBQcm9ncmFtLCBvciB0aGUgbW9kaWZpY2F0aW9ucyB0bwogcHJvZHVjZSBpdCBmcm9tIHRo
ZSBQcm9ncmFtLCBpbiB0aGUgZm9ybSBvZiBzb3VyY2UgY29kZSB1bmRlciB0aGUKIHRlcm1zIG9m
IHNlY3Rpb24gNCwgcHJvdmlkZWQgdGhhdCB5b3UgYWxzbyBtZWV0IGFsbCBvZiB0aGVzZSBjb25k
aXRpb25zOgoKICAgICBhKSBUaGUgd29yayBtdXN0IGNhcnJ5IHByb21pbmVudCBub3RpY2VzIHN0
YXRpbmcgdGhhdCB5b3UgbW9kaWZpZWQKICAgICBpdCwgYW5kIGdpdmluZyBhIHJlbGV2YW50IGRh
dGUuCgogICAgIGIpIFRoZSB3b3JrIG11c3QgY2FycnkgcHJvbWluZW50IG5vdGljZXMgc3RhdGlu
ZyB0aGF0IGl0IGlzCiAgICAgcmVsZWFzZWQgdW5kZXIgdGhpcyBMaWNlbnNlIGFuZCBhbnkgY29u
ZGl0aW9ucyBhZGRlZCB1bmRlciBzZWN0aW9uCiAgICAgNy4gIFRoaXMgcmVxdWlyZW1lbnQgbW9k
aWZpZXMgdGhlIHJlcXVpcmVtZW50IGluIHNlY3Rpb24gNCB0bwogICAgICJrZWVwIGludGFjdCBh
bGwgbm90aWNlcyIuCgogICAgIGMpIFlvdSBtdXN0IGxpY2Vuc2UgdGhlIGVudGlyZSB3b3JrLCBh
cyBhIHdob2xlLCB1bmRlciB0aGlzCiAgICAgTGljZW5zZSB0byBhbnlvbmUgd2hvIGNvbWVzIGlu
dG8gcG9zc2Vzc2lvbiBvZiBhIGNvcHkuICBUaGlzCiAgICAgTGljZW5zZSB3aWxsIHRoZXJlZm9y
ZSBhcHBseSwgYWxvbmcgd2l0aCBhbnkgYXBwbGljYWJsZSBzZWN0aW9uIDcKICAgICBhZGRpdGlv
bmFsIHRlcm1zLCB0byB0aGUgd2hvbGUgb2YgdGhlIHdvcmssIGFuZCBhbGwgaXRzIHBhcnRzLAog
ICAgIHJlZ2FyZGxlc3Mgb2YgaG93IHRoZXkgYXJlIHBhY2thZ2VkLiAgVGhpcyBMaWNlbnNlIGdp
dmVzIG5vCiAgICAgcGVybWlzc2lvbiB0byBsaWNlbnNlIHRoZSB3b3JrIGluIGFueSBvdGhlciB3
YXksIGJ1dCBpdCBkb2VzIG5vdAogICAgIGludmFsaWRhdGUgc3VjaCBwZXJtaXNzaW9uIGlmIHlv
dSBoYXZlIHNlcGFyYXRlbHkgcmVjZWl2ZWQgaXQuCgogICAgIGQpIElmIHRoZSB3b3JrIGhhcyBp
bnRlcmFjdGl2ZSB1c2VyIGludGVyZmFjZXMsIGVhY2ggbXVzdCBkaXNwbGF5CiAgICAgQXBwcm9w
cmlhdGUgTGVnYWwgTm90aWNlczsgaG93ZXZlciwgaWYgdGhlIFByb2dyYW0gaGFzIGludGVyYWN0
aXZlCiAgICAgaW50ZXJmYWNlcyB0aGF0IGRvIG5vdCBkaXNwbGF5IEFwcHJvcHJpYXRlIExlZ2Fs
IE5vdGljZXMsIHlvdXIKICAgICB3b3JrIG5lZWQgbm90IG1ha2UgdGhlbSBkbyBzby4KCiAgIEEg
Y29tcGlsYXRpb24gb2YgYSBjb3ZlcmVkIHdvcmsgd2l0aCBvdGhlciBzZXBhcmF0ZSBhbmQgaW5k
ZXBlbmRlbnQKIHdvcmtzLCB3aGljaCBhcmUgbm90IGJ5IHRoZWlyIG5hdHVyZSBleHRlbnNpb25z
IG9mIHRoZSBjb3ZlcmVkIHdvcmssCiBhbmQgd2hpY2ggYXJlIG5vdCBjb21iaW5lZCB3aXRoIGl0
IHN1Y2ggYXMgdG8gZm9ybSBhIGxhcmdlciBwcm9ncmFtLAogaW4gb3Igb24gYSB2b2x1bWUgb2Yg
YSBzdG9yYWdlIG9yIGRpc3RyaWJ1dGlvbiBtZWRpdW0sIGlzIGNhbGxlZCBhbgogImFnZ3JlZ2F0
ZSIgaWYgdGhlIGNvbXBpbGF0aW9uIGFuZCBpdHMgcmVzdWx0aW5nIGNvcHlyaWdodCBhcmUgbm90
CiB1c2VkIHRvIGxpbWl0IHRoZSBhY2Nlc3Mgb3IgbGVnYWwgcmlnaHRzIG9mIHRoZSBjb21waWxh
dGlvbidzIHVzZXJzCiBiZXlvbmQgd2hhdCB0aGUgaW5kaXZpZHVhbCB3b3JrcyBwZXJtaXQuICBJ
bmNsdXNpb24gb2YgYSBjb3ZlcmVkIHdvcmsKIGluIGFuIGFnZ3JlZ2F0ZSBkb2VzIG5vdCBjYXVz
ZSB0aGlzIExpY2Vuc2UgdG8gYXBwbHkgdG8gdGhlIG90aGVyCiBwYXJ0cyBvZiB0aGUgYWdncmVn
YXRlLgoKICAgNi4gQ29udmV5aW5nIE5vbi1Tb3VyY2UgRm9ybXMuCgogICBZb3UgbWF5IGNvbnZl
eSBhIGNvdmVyZWQgd29yayBpbiBvYmplY3QgY29kZSBmb3JtIHVuZGVyIHRoZSB0ZXJtcwogb2Yg
c2VjdGlvbnMgNCBhbmQgNSwgcHJvdmlkZWQgdGhhdCB5b3UgYWxzbyBjb252ZXkgdGhlCiBtYWNo
aW5lLXJlYWRhYmxlIENvcnJlc3BvbmRpbmcgU291cmNlIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGlz
IExpY2Vuc2UsCiBpbiBvbmUgb2YgdGhlc2Ugd2F5czoKCiAgICAgYSkgQ29udmV5IHRoZSBvYmpl
Y3QgY29kZSBpbiwgb3IgZW1ib2RpZWQgaW4sIGEgcGh5c2ljYWwgcHJvZHVjdAogICAgIChpbmNs
dWRpbmcgYSBwaHlzaWNhbCBkaXN0cmlidXRpb24gbWVkaXVtKSwgYWNjb21wYW5pZWQgYnkgdGhl
CiAgICAgQ29ycmVzcG9uZGluZyBTb3VyY2UgZml4ZWQgb24gYSBkdXJhYmxlIHBoeXNpY2FsIG1l
ZGl1bQogICAgIGN1c3RvbWFyaWx5IHVzZWQgZm9yIHNvZnR3YXJlIGludGVyY2hhbmdlLgoKICAg
ICBiKSBDb252ZXkgdGhlIG9iamVjdCBjb2RlIGluLCBvciBlbWJvZGllZCBpbiwgYSBwaHlzaWNh
bCBwcm9kdWN0CiAgICAgKGluY2x1ZGluZyBhIHBoeXNpY2FsIGRpc3RyaWJ1dGlvbiBtZWRpdW0p
LCBhY2NvbXBhbmllZCBieSBhCiAgICAgd3JpdHRlbiBvZmZlciwgdmFsaWQgZm9yIGF0IGxlYXN0
IHRocmVlIHllYXJzIGFuZCB2YWxpZCBmb3IgYXMKICAgICBsb25nIGFzIHlvdSBvZmZlciBzcGFy
ZSBwYXJ0cyBvciBjdXN0b21lciBzdXBwb3J0IGZvciB0aGF0IHByb2R1Y3QKICAgICBtb2RlbCwg
dG8gZ2l2ZSBhbnlvbmUgd2hvIHBvc3Nlc3NlcyB0aGUgb2JqZWN0IGNvZGUgZWl0aGVyICgxKSBh
CiAgICAgY29weSBvZiB0aGUgQ29ycmVzcG9uZGluZyBTb3VyY2UgZm9yIGFsbCB0aGUgc29mdHdh
cmUgaW4gdGhlCiAgICAgcHJvZHVjdCB0aGF0IGlzIGNvdmVyZWQgYnkgdGhpcyBMaWNlbnNlLCBv
biBhIGR1cmFibGUgcGh5c2ljYWwKICAgICBtZWRpdW0gY3VzdG9tYXJpbHkgdXNlZCBmb3Igc29m
dHdhcmUgaW50ZXJjaGFuZ2UsIGZvciBhIHByaWNlIG5vCiAgICAgbW9yZSB0aGFuIHlvdXIgcmVh
c29uYWJsZSBjb3N0IG9mIHBoeXNpY2FsbHkgcGVyZm9ybWluZyB0aGlzCiAgICAgY29udmV5aW5n
IG9mIHNvdXJjZSwgb3IgKDIpIGFjY2VzcyB0byBjb3B5IHRoZQogICAgIENvcnJlc3BvbmRpbmcg
U291cmNlIGZyb20gYSBuZXR3b3JrIHNlcnZlciBhdCBubyBjaGFyZ2UuCgogICAgIGMpIENvbnZl
eSBpbmRpdmlkdWFsIGNvcGllcyBvZiB0aGUgb2JqZWN0IGNvZGUgd2l0aCBhIGNvcHkgb2YgdGhl
CiAgICAgd3JpdHRlbiBvZmZlciB0byBwcm92aWRlIHRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZS4g
IFRoaXMKICAgICBhbHRlcm5hdGl2ZSBpcyBhbGxvd2VkIG9ubHkgb2NjYXNpb25hbGx5IGFuZCBu
b25jb21tZXJjaWFsbHksIGFuZAogICAgIG9ubHkgaWYgeW91IHJlY2VpdmVkIHRoZSBvYmplY3Qg
Y29kZSB3aXRoIHN1Y2ggYW4gb2ZmZXIsIGluIGFjY29yZAogICAgIHdpdGggc3Vic2VjdGlvbiA2
Yi4KCiAgICAgZCkgQ29udmV5IHRoZSBvYmplY3QgY29kZSBieSBvZmZlcmluZyBhY2Nlc3MgZnJv
bSBhIGRlc2lnbmF0ZWQKICAgICBwbGFjZSAoZ3JhdGlzIG9yIGZvciBhIGNoYXJnZSksIGFuZCBv
ZmZlciBlcXVpdmFsZW50IGFjY2VzcyB0byB0aGUKICAgICBDb3JyZXNwb25kaW5nIFNvdXJjZSBp
biB0aGUgc2FtZSB3YXkgdGhyb3VnaCB0aGUgc2FtZSBwbGFjZSBhdCBubwogICAgIGZ1cnRoZXIg
Y2hhcmdlLiAgWW91IG5lZWQgbm90IHJlcXVpcmUgcmVjaXBpZW50cyB0byBjb3B5IHRoZQogICAg
IENvcnJlc3BvbmRpbmcgU291cmNlIGFsb25nIHdpdGggdGhlIG9iamVjdCBjb2RlLiAgSWYgdGhl
IHBsYWNlIHRvCiAgICAgY29weSB0aGUgb2JqZWN0IGNvZGUgaXMgYSBuZXR3b3JrIHNlcnZlciwg
dGhlIENvcnJlc3BvbmRpbmcgU291cmNlCiAgICAgbWF5IGJlIG9uIGEgZGlmZmVyZW50IHNlcnZl
ciAob3BlcmF0ZWQgYnkgeW91IG9yIGEgdGhpcmQgcGFydHkpCiAgICAgdGhhdCBzdXBwb3J0cyBl
cXVpdmFsZW50IGNvcHlpbmcgZmFjaWxpdGllcywgcHJvdmlkZWQgeW91IG1haW50YWluCiAgICAg
Y2xlYXIgZGlyZWN0aW9ucyBuZXh0IHRvIHRoZSBvYmplY3QgY29kZSBzYXlpbmcgd2hlcmUgdG8g
ZmluZCB0aGUKICAgICBDb3JyZXNwb25kaW5nIFNvdXJjZS4gIFJlZ2FyZGxlc3Mgb2Ygd2hhdCBz
ZXJ2ZXIgaG9zdHMgdGhlCiAgICAgQ29ycmVzcG9uZGluZyBTb3VyY2UsIHlvdSByZW1haW4gb2Js
aWdhdGVkIHRvIGVuc3VyZSB0aGF0IGl0IGlzCiAgICAgYXZhaWxhYmxlIGZvciBhcyBsb25nIGFz
IG5lZWRlZCB0byBzYXRpc2Z5IHRoZXNlIHJlcXVpcmVtZW50cy4KCiAgICAgZSkgQ29udmV5IHRo
ZSBvYmplY3QgY29kZSB1c2luZyBwZWVyLXRvLXBlZXIgdHJhbnNtaXNzaW9uLCBwcm92aWRlZAog
ICAgIHlvdSBpbmZvcm0gb3RoZXIgcGVlcnMgd2hlcmUgdGhlIG9iamVjdCBjb2RlIGFuZCBDb3Jy
ZXNwb25kaW5nCiAgICAgU291cmNlIG9mIHRoZSB3b3JrIGFyZSBiZWluZyBvZmZlcmVkIHRvIHRo
ZSBnZW5lcmFsIHB1YmxpYyBhdCBubwogICAgIGNoYXJnZSB1bmRlciBzdWJzZWN0aW9uIDZkLgoK
ICAgQSBzZXBhcmFibGUgcG9ydGlvbiBvZiB0aGUgb2JqZWN0IGNvZGUsIHdob3NlIHNvdXJjZSBj
b2RlIGlzIGV4Y2x1ZGVkCiBmcm9tIHRoZSBDb3JyZXNwb25kaW5nIFNvdXJjZSBhcyBhIFN5c3Rl
bSBMaWJyYXJ5LCBuZWVkIG5vdCBiZQogaW5jbHVkZWQgaW4gY29udmV5aW5nIHRoZSBvYmplY3Qg
Y29kZSB3b3JrLgoKICAgQSAiVXNlciBQcm9kdWN0IiBpcyBlaXRoZXIgKDEpIGEgImNvbnN1bWVy
IHByb2R1Y3QiLCB3aGljaCBtZWFucyBhbnkKIHRhbmdpYmxlIHBlcnNvbmFsIHByb3BlcnR5IHdo
aWNoIGlzIG5vcm1hbGx5IHVzZWQgZm9yIHBlcnNvbmFsLCBmYW1pbHksCiBvciBob3VzZWhvbGQg
cHVycG9zZXMsIG9yICgyKSBhbnl0aGluZyBkZXNpZ25lZCBvciBzb2xkIGZvciBpbmNvcnBvcmF0
aW9uCiBpbnRvIGEgZHdlbGxpbmcuICBJbiBkZXRlcm1pbmluZyB3aGV0aGVyIGEgcHJvZHVjdCBp
cyBhIGNvbnN1bWVyIHByb2R1Y3QsCiBkb3VidGZ1bCBjYXNlcyBzaGFsbCBiZSByZXNvbHZlZCBp
biBmYXZvciBvZiBjb3ZlcmFnZS4gIEZvciBhIHBhcnRpY3VsYXIKIHByb2R1Y3QgcmVjZWl2ZWQg
YnkgYSBwYXJ0aWN1bGFyIHVzZXIsICJub3JtYWxseSB1c2VkIiByZWZlcnMgdG8gYQogdHlwaWNh
bCBvciBjb21tb24gdXNlIG9mIHRoYXQgY2xhc3Mgb2YgcHJvZHVjdCwgcmVnYXJkbGVzcyBvZiB0
aGUgc3RhdHVzCiBvZiB0aGUgcGFydGljdWxhciB1c2VyIG9yIG9mIHRoZSB3YXkgaW4gd2hpY2gg
dGhlIHBhcnRpY3VsYXIgdXNlcgogYWN0dWFsbHkgdXNlcywgb3IgZXhwZWN0cyBvciBpcyBleHBl
Y3RlZCB0byB1c2UsIHRoZSBwcm9kdWN0LiAgQSBwcm9kdWN0CiBpcyBhIGNvbnN1bWVyIHByb2R1
Y3QgcmVnYXJkbGVzcyBvZiB3aGV0aGVyIHRoZSBwcm9kdWN0IGhhcyBzdWJzdGFudGlhbAogY29t
bWVyY2lhbCwgaW5kdXN0cmlhbCBvciBub24tY29uc3VtZXIgdXNlcywgdW5sZXNzIHN1Y2ggdXNl
cyByZXByZXNlbnQKIHRoZSBvbmx5IHNpZ25pZmljYW50IG1vZGUgb2YgdXNlIG9mIHRoZSBwcm9k
dWN0LgoKICAgIkluc3RhbGxhdGlvbiBJbmZvcm1hdGlvbiIgZm9yIGEgVXNlciBQcm9kdWN0IG1l
YW5zIGFueSBtZXRob2RzLAogcHJvY2VkdXJlcywgYXV0aG9yaXphdGlvbiBrZXlzLCBvciBvdGhl
ciBpbmZvcm1hdGlvbiByZXF1aXJlZCB0byBpbnN0YWxsCiBhbmQgZXhlY3V0ZSBtb2RpZmllZCB2
ZXJzaW9ucyBvZiBhIGNvdmVyZWQgd29yayBpbiB0aGF0IFVzZXIgUHJvZHVjdCBmcm9tCiBhIG1v
ZGlmaWVkIHZlcnNpb24gb2YgaXRzIENvcnJlc3BvbmRpbmcgU291cmNlLiAgVGhlIGluZm9ybWF0
aW9uIG11c3QKIHN1ZmZpY2UgdG8gZW5zdXJlIHRoYXQgdGhlIGNvbnRpbnVlZCBmdW5jdGlvbmlu
ZyBvZiB0aGUgbW9kaWZpZWQgb2JqZWN0CiBjb2RlIGlzIGluIG5vIGNhc2UgcHJldmVudGVkIG9y
IGludGVyZmVyZWQgd2l0aCBzb2xlbHkgYmVjYXVzZQogbW9kaWZpY2F0aW9uIGhhcyBiZWVuIG1h
ZGUuCgogICBJZiB5b3UgY29udmV5IGFuIG9iamVjdCBjb2RlIHdvcmsgdW5kZXIgdGhpcyBzZWN0
aW9uIGluLCBvciB3aXRoLCBvcgogc3BlY2lmaWNhbGx5IGZvciB1c2UgaW4sIGEgVXNlciBQcm9k
dWN0LCBhbmQgdGhlIGNvbnZleWluZyBvY2N1cnMgYXMKIHBhcnQgb2YgYSB0cmFuc2FjdGlvbiBp
biB3aGljaCB0aGUgcmlnaHQgb2YgcG9zc2Vzc2lvbiBhbmQgdXNlIG9mIHRoZQogVXNlciBQcm9k
dWN0IGlzIHRyYW5zZmVycmVkIHRvIHRoZSByZWNpcGllbnQgaW4gcGVycGV0dWl0eSBvciBmb3Ig
YQogZml4ZWQgdGVybSAocmVnYXJkbGVzcyBvZiBob3cgdGhlIHRyYW5zYWN0aW9uIGlzIGNoYXJh
Y3Rlcml6ZWQpLCB0aGUKIENvcnJlc3BvbmRpbmcgU291cmNlIGNvbnZleWVkIHVuZGVyIHRoaXMg
c2VjdGlvbiBtdXN0IGJlIGFjY29tcGFuaWVkCiBieSB0aGUgSW5zdGFsbGF0aW9uIEluZm9ybWF0
aW9uLiAgQnV0IHRoaXMgcmVxdWlyZW1lbnQgZG9lcyBub3QgYXBwbHkKIGlmIG5laXRoZXIgeW91
IG5vciBhbnkgdGhpcmQgcGFydHkgcmV0YWlucyB0aGUgYWJpbGl0eSB0byBpbnN0YWxsCiBtb2Rp
ZmllZCBvYmplY3QgY29kZSBvbiB0aGUgVXNlciBQcm9kdWN0IChmb3IgZXhhbXBsZSwgdGhlIHdv
cmsgaGFzCiBiZWVuIGluc3RhbGxlZCBpbiBST00pLgoKICAgVGhlIHJlcXVpcmVtZW50IHRvIHBy
b3ZpZGUgSW5zdGFsbGF0aW9uIEluZm9ybWF0aW9uIGRvZXMgbm90IGluY2x1ZGUgYQogcmVxdWly
ZW1lbnQgdG8gY29udGludWUgdG8gcHJvdmlkZSBzdXBwb3J0IHNlcnZpY2UsIHdhcnJhbnR5LCBv
ciB1cGRhdGVzCiBmb3IgYSB3b3JrIHRoYXQgaGFzIGJlZW4gbW9kaWZpZWQgb3IgaW5zdGFsbGVk
IGJ5IHRoZSByZWNpcGllbnQsIG9yIGZvcgogdGhlIFVzZXIgUHJvZHVjdCBpbiB3aGljaCBpdCBo
YXMgYmVlbiBtb2RpZmllZCBvciBpbnN0YWxsZWQuICBBY2Nlc3MgdG8gYQogbmV0d29yayBtYXkg
YmUgZGVuaWVkIHdoZW4gdGhlIG1vZGlmaWNhdGlvbiBpdHNlbGYgbWF0ZXJpYWxseSBhbmQKIGFk
dmVyc2VseSBhZmZlY3RzIHRoZSBvcGVyYXRpb24gb2YgdGhlIG5ldHdvcmsgb3IgdmlvbGF0ZXMg
dGhlIHJ1bGVzIGFuZAogcHJvdG9jb2xzIGZvciBjb21tdW5pY2F0aW9uIGFjcm9zcyB0aGUgbmV0
d29yay4KCiAgIENvcnJlc3BvbmRpbmcgU291cmNlIGNvbnZleWVkLCBhbmQgSW5zdGFsbGF0aW9u
IEluZm9ybWF0aW9uIHByb3ZpZGVkLAogaW4gYWNjb3JkIHdpdGggdGhpcyBzZWN0aW9uIG11c3Qg
YmUgaW4gYSBmb3JtYXQgdGhhdCBpcyBwdWJsaWNseQogZG9jdW1lbnRlZCAoYW5kIHdpdGggYW4g
aW1wbGVtZW50YXRpb24gYXZhaWxhYmxlIHRvIHRoZSBwdWJsaWMgaW4KIHNvdXJjZSBjb2RlIGZv
cm0pLCBhbmQgbXVzdCByZXF1aXJlIG5vIHNwZWNpYWwgcGFzc3dvcmQgb3Iga2V5IGZvcgogdW5w
YWNraW5nLCByZWFkaW5nIG9yIGNvcHlpbmcuCgogICA3LiBBZGRpdGlvbmFsIFRlcm1zLgoKICAg
IkFkZGl0aW9uYWwgcGVybWlzc2lvbnMiIGFyZSB0ZXJtcyB0aGF0IHN1cHBsZW1lbnQgdGhlIHRl
cm1zIG9mIHRoaXMKIExpY2Vuc2UgYnkgbWFraW5nIGV4Y2VwdGlvbnMgZnJvbSBvbmUgb3IgbW9y
ZSBvZiBpdHMgY29uZGl0aW9ucy4KIEFkZGl0aW9uYWwgcGVybWlzc2lvbnMgdGhhdCBhcmUgYXBw
bGljYWJsZSB0byB0aGUgZW50aXJlIFByb2dyYW0gc2hhbGwKIGJlIHRyZWF0ZWQgYXMgdGhvdWdo
IHRoZXkgd2VyZSBpbmNsdWRlZCBpbiB0aGlzIExpY2Vuc2UsIHRvIHRoZSBleHRlbnQKIHRoYXQg
dGhleSBhcmUgdmFsaWQgdW5kZXIgYXBwbGljYWJsZSBsYXcuICBJZiBhZGRpdGlvbmFsIHBlcm1p
c3Npb25zCiBhcHBseSBvbmx5IHRvIHBhcnQgb2YgdGhlIFByb2dyYW0sIHRoYXQgcGFydCBtYXkg
YmUgdXNlZCBzZXBhcmF0ZWx5CiB1bmRlciB0aG9zZSBwZXJtaXNzaW9ucywgYnV0IHRoZSBlbnRp
cmUgUHJvZ3JhbSByZW1haW5zIGdvdmVybmVkIGJ5CiB0aGlzIExpY2Vuc2Ugd2l0aG91dCByZWdh
cmQgdG8gdGhlIGFkZGl0aW9uYWwgcGVybWlzc2lvbnMuCgogICBXaGVuIHlvdSBjb252ZXkgYSBj
b3B5IG9mIGEgY292ZXJlZCB3b3JrLCB5b3UgbWF5IGF0IHlvdXIgb3B0aW9uCiByZW1vdmUgYW55
IGFkZGl0aW9uYWwgcGVybWlzc2lvbnMgZnJvbSB0aGF0IGNvcHksIG9yIGZyb20gYW55IHBhcnQg
b2YKIGl0LiAgKEFkZGl0aW9uYWwgcGVybWlzc2lvbnMgbWF5IGJlIHdyaXR0ZW4gdG8gcmVxdWly
ZSB0aGVpciBvd24KIHJlbW92YWwgaW4gY2VydGFpbiBjYXNlcyB3aGVuIHlvdSBtb2RpZnkgdGhl
IHdvcmsuKSAgWW91IG1heSBwbGFjZQogYWRkaXRpb25hbCBwZXJtaXNzaW9ucyBvbiBtYXRlcmlh
bCwgYWRkZWQgYnkgeW91IHRvIGEgY292ZXJlZCB3b3JrLAogZm9yIHdoaWNoIHlvdSBoYXZlIG9y
IGNhbiBnaXZlIGFwcHJvcHJpYXRlIGNvcHlyaWdodCBwZXJtaXNzaW9uLgoKICAgTm90d2l0aHN0
YW5kaW5nIGFueSBvdGhlciBwcm92aXNpb24gb2YgdGhpcyBMaWNlbnNlLCBmb3IgbWF0ZXJpYWwg
eW91CiBhZGQgdG8gYSBjb3ZlcmVkIHdvcmssIHlvdSBtYXkgKGlmIGF1dGhvcml6ZWQgYnkgdGhl
IGNvcHlyaWdodCBob2xkZXJzIG9mCiB0aGF0IG1hdGVyaWFsKSBzdXBwbGVtZW50IHRoZSB0ZXJt
cyBvZiB0aGlzIExpY2Vuc2Ugd2l0aCB0ZXJtczoKCiAgICAgYSkgRGlzY2xhaW1pbmcgd2FycmFu
dHkgb3IgbGltaXRpbmcgbGlhYmlsaXR5IGRpZmZlcmVudGx5IGZyb20gdGhlCiAgICAgdGVybXMg
b2Ygc2VjdGlvbnMgMTUgYW5kIDE2IG9mIHRoaXMgTGljZW5zZTsgb3IKCiAgICAgYikgUmVxdWly
aW5nIHByZXNlcnZhdGlvbiBvZiBzcGVjaWZpZWQgcmVhc29uYWJsZSBsZWdhbCBub3RpY2VzIG9y
CiAgICAgYXV0aG9yIGF0dHJpYnV0aW9ucyBpbiB0aGF0IG1hdGVyaWFsIG9yIGluIHRoZSBBcHBy
b3ByaWF0ZSBMZWdhbAogICAgIE5vdGljZXMgZGlzcGxheWVkIGJ5IHdvcmtzIGNvbnRhaW5pbmcg
aXQ7IG9yCgogICAgIGMpIFByb2hpYml0aW5nIG1pc3JlcHJlc2VudGF0aW9uIG9mIHRoZSBvcmln
aW4gb2YgdGhhdCBtYXRlcmlhbCwgb3IKICAgICByZXF1aXJpbmcgdGhhdCBtb2RpZmllZCB2ZXJz
aW9ucyBvZiBzdWNoIG1hdGVyaWFsIGJlIG1hcmtlZCBpbgogICAgIHJlYXNvbmFibGUgd2F5cyBh
cyBkaWZmZXJlbnQgZnJvbSB0aGUgb3JpZ2luYWwgdmVyc2lvbjsgb3IKCiAgICAgZCkgTGltaXRp
bmcgdGhlIHVzZSBmb3IgcHVibGljaXR5IHB1cnBvc2VzIG9mIG5hbWVzIG9mIGxpY2Vuc29ycyBv
cgogICAgIGF1dGhvcnMgb2YgdGhlIG1hdGVyaWFsOyBvcgoKICAgICBlKSBEZWNsaW5pbmcgdG8g
Z3JhbnQgcmlnaHRzIHVuZGVyIHRyYWRlbWFyayBsYXcgZm9yIHVzZSBvZiBzb21lCiAgICAgdHJh
ZGUgbmFtZXMsIHRyYWRlbWFya3MsIG9yIHNlcnZpY2UgbWFya3M7IG9yCgogICAgIGYpIFJlcXVp
cmluZyBpbmRlbW5pZmljYXRpb24gb2YgbGljZW5zb3JzIGFuZCBhdXRob3JzIG9mIHRoYXQKICAg
ICBtYXRlcmlhbCBieSBhbnlvbmUgd2hvIGNvbnZleXMgdGhlIG1hdGVyaWFsIChvciBtb2RpZmll
ZCB2ZXJzaW9ucyBvZgogICAgIGl0KSB3aXRoIGNvbnRyYWN0dWFsIGFzc3VtcHRpb25zIG9mIGxp
YWJpbGl0eSB0byB0aGUgcmVjaXBpZW50LCBmb3IKICAgICBhbnkgbGlhYmlsaXR5IHRoYXQgdGhl
c2UgY29udHJhY3R1YWwgYXNzdW1wdGlvbnMgZGlyZWN0bHkgaW1wb3NlIG9uCiAgICAgdGhvc2Ug
bGljZW5zb3JzIGFuZCBhdXRob3JzLgoKICAgQWxsIG90aGVyIG5vbi1wZXJtaXNzaXZlIGFkZGl0
aW9uYWwgdGVybXMgYXJlIGNvbnNpZGVyZWQgImZ1cnRoZXIKIHJlc3RyaWN0aW9ucyIgd2l0aGlu
IHRoZSBtZWFuaW5nIG9mIHNlY3Rpb24gMTAuICBJZiB0aGUgUHJvZ3JhbSBhcyB5b3UKIHJlY2Vp
dmVkIGl0LCBvciBhbnkgcGFydCBvZiBpdCwgY29udGFpbnMgYSBub3RpY2Ugc3RhdGluZyB0aGF0
IGl0IGlzCiBnb3Zlcm5lZCBieSB0aGlzIExpY2Vuc2UgYWxvbmcgd2l0aCBhIHRlcm0gdGhhdCBp
cyBhIGZ1cnRoZXIKIHJlc3RyaWN0aW9uLCB5b3UgbWF5IHJlbW92ZSB0aGF0IHRlcm0uICBJZiBh
IGxpY2Vuc2UgZG9jdW1lbnQgY29udGFpbnMKIGEgZnVydGhlciByZXN0cmljdGlvbiBidXQgcGVy
bWl0cyByZWxpY2Vuc2luZyBvciBjb252ZXlpbmcgdW5kZXIgdGhpcwogTGljZW5zZSwgeW91IG1h
eSBhZGQgdG8gYSBjb3ZlcmVkIHdvcmsgbWF0ZXJpYWwgZ292ZXJuZWQgYnkgdGhlIHRlcm1zCiBv
ZiB0aGF0IGxpY2Vuc2UgZG9jdW1lbnQsIHByb3ZpZGVkIHRoYXQgdGhlIGZ1cnRoZXIgcmVzdHJp
Y3Rpb24gZG9lcwogbm90IHN1cnZpdmUgc3VjaCByZWxpY2Vuc2luZyBvciBjb252ZXlpbmcuCgog
ICBJZiB5b3UgYWRkIHRlcm1zIHRvIGEgY292ZXJlZCB3b3JrIGluIGFjY29yZCB3aXRoIHRoaXMg
c2VjdGlvbiwgeW91CiBtdXN0IHBsYWNlLCBpbiB0aGUgcmVsZXZhbnQgc291cmNlIGZpbGVzLCBh
IHN0YXRlbWVudCBvZiB0aGUKIGFkZGl0aW9uYWwgdGVybXMgdGhhdCBhcHBseSB0byB0aG9zZSBm
aWxlcywgb3IgYSBub3RpY2UgaW5kaWNhdGluZwogd2hlcmUgdG8gZmluZCB0aGUgYXBwbGljYWJs
ZSB0ZXJtcy4KCiAgIEFkZGl0aW9uYWwgdGVybXMsIHBlcm1pc3NpdmUgb3Igbm9uLXBlcm1pc3Np
dmUsIG1heSBiZSBzdGF0ZWQgaW4gdGhlCiBmb3JtIG9mIGEgc2VwYXJhdGVseSB3cml0dGVuIGxp
Y2Vuc2UsIG9yIHN0YXRlZCBhcyBleGNlcHRpb25zOwogdGhlIGFib3ZlIHJlcXVpcmVtZW50cyBh
cHBseSBlaXRoZXIgd2F5LgoKICAgOC4gVGVybWluYXRpb24uCgogICBZb3UgbWF5IG5vdCBwcm9w
YWdhdGUgb3IgbW9kaWZ5IGEgY292ZXJlZCB3b3JrIGV4Y2VwdCBhcyBleHByZXNzbHkKIHByb3Zp
ZGVkIHVuZGVyIHRoaXMgTGljZW5zZS4gIEFueSBhdHRlbXB0IG90aGVyd2lzZSB0byBwcm9wYWdh
dGUgb3IKIG1vZGlmeSBpdCBpcyB2b2lkLCBhbmQgd2lsbCBhdXRvbWF0aWNhbGx5IHRlcm1pbmF0
ZSB5b3VyIHJpZ2h0cyB1bmRlcgogdGhpcyBMaWNlbnNlIChpbmNsdWRpbmcgYW55IHBhdGVudCBs
aWNlbnNlcyBncmFudGVkIHVuZGVyIHRoZSB0aGlyZAogcGFyYWdyYXBoIG9mIHNlY3Rpb24gMTEp
LgoKICAgSG93ZXZlciwgaWYgeW91IGNlYXNlIGFsbCB2aW9sYXRpb24gb2YgdGhpcyBMaWNlbnNl
LCB0aGVuIHlvdXIKIGxpY2Vuc2UgZnJvbSBhIHBhcnRpY3VsYXIgY29weXJpZ2h0IGhvbGRlciBp
cyByZWluc3RhdGVkIChhKQogcHJvdmlzaW9uYWxseSwgdW5sZXNzIGFuZCB1bnRpbCB0aGUgY29w
eXJpZ2h0IGhvbGRlciBleHBsaWNpdGx5IGFuZAogZmluYWxseSB0ZXJtaW5hdGVzIHlvdXIgbGlj
ZW5zZSwgYW5kIChiKSBwZXJtYW5lbnRseSwgaWYgdGhlIGNvcHlyaWdodAogaG9sZGVyIGZhaWxz
IHRvIG5vdGlmeSB5b3Ugb2YgdGhlIHZpb2xhdGlvbiBieSBzb21lIHJlYXNvbmFibGUgbWVhbnMK
IHByaW9yIHRvIDYwIGRheXMgYWZ0ZXIgdGhlIGNlc3NhdGlvbi4KCiAgIE1vcmVvdmVyLCB5b3Vy
IGxpY2Vuc2UgZnJvbSBhIHBhcnRpY3VsYXIgY29weXJpZ2h0IGhvbGRlciBpcwogcmVpbnN0YXRl
ZCBwZXJtYW5lbnRseSBpZiB0aGUgY29weXJpZ2h0IGhvbGRlciBub3RpZmllcyB5b3Ugb2YgdGhl
CiB2aW9sYXRpb24gYnkgc29tZSByZWFzb25hYmxlIG1lYW5zLCB0aGlzIGlzIHRoZSBmaXJzdCB0
aW1lIHlvdSBoYXZlCiByZWNlaXZlZCBub3RpY2Ugb2YgdmlvbGF0aW9uIG9mIHRoaXMgTGljZW5z
ZSAoZm9yIGFueSB3b3JrKSBmcm9tIHRoYXQKIGNvcHlyaWdodCBob2xkZXIsIGFuZCB5b3UgY3Vy
ZSB0aGUgdmlvbGF0aW9uIHByaW9yIHRvIDMwIGRheXMgYWZ0ZXIKIHlvdXIgcmVjZWlwdCBvZiB0
aGUgbm90aWNlLgoKICAgVGVybWluYXRpb24gb2YgeW91ciByaWdodHMgdW5kZXIgdGhpcyBzZWN0
aW9uIGRvZXMgbm90IHRlcm1pbmF0ZSB0aGUKIGxpY2Vuc2VzIG9mIHBhcnRpZXMgd2hvIGhhdmUg
cmVjZWl2ZWQgY29waWVzIG9yIHJpZ2h0cyBmcm9tIHlvdSB1bmRlcgogdGhpcyBMaWNlbnNlLiAg
SWYgeW91ciByaWdodHMgaGF2ZSBiZWVuIHRlcm1pbmF0ZWQgYW5kIG5vdCBwZXJtYW5lbnRseQog
cmVpbnN0YXRlZCwgeW91IGRvIG5vdCBxdWFsaWZ5IHRvIHJlY2VpdmUgbmV3IGxpY2Vuc2VzIGZv
ciB0aGUgc2FtZQogbWF0ZXJpYWwgdW5kZXIgc2VjdGlvbiAxMC4KCiAgIDkuIEFjY2VwdGFuY2Ug
Tm90IFJlcXVpcmVkIGZvciBIYXZpbmcgQ29waWVzLgoKICAgWW91IGFyZSBub3QgcmVxdWlyZWQg
dG8gYWNjZXB0IHRoaXMgTGljZW5zZSBpbiBvcmRlciB0byByZWNlaXZlIG9yCiBydW4gYSBjb3B5
IG9mIHRoZSBQcm9ncmFtLiAgQW5jaWxsYXJ5IHByb3BhZ2F0aW9uIG9mIGEgY292ZXJlZCB3b3Jr
CiBvY2N1cnJpbmcgc29sZWx5IGFzIGEgY29uc2VxdWVuY2Ugb2YgdXNpbmcgcGVlci10by1wZWVy
IHRyYW5zbWlzc2lvbgogdG8gcmVjZWl2ZSBhIGNvcHkgbGlrZXdpc2UgZG9lcyBub3QgcmVxdWly
ZSBhY2NlcHRhbmNlLiAgSG93ZXZlciwKIG5vdGhpbmcgb3RoZXIgdGhhbiB0aGlzIExpY2Vuc2Ug
Z3JhbnRzIHlvdSBwZXJtaXNzaW9uIHRvIHByb3BhZ2F0ZSBvcgogbW9kaWZ5IGFueSBjb3ZlcmVk
IHdvcmsuICBUaGVzZSBhY3Rpb25zIGluZnJpbmdlIGNvcHlyaWdodCBpZiB5b3UgZG8KIG5vdCBh
Y2NlcHQgdGhpcyBMaWNlbnNlLiAgVGhlcmVmb3JlLCBieSBtb2RpZnlpbmcgb3IgcHJvcGFnYXRp
bmcgYQogY292ZXJlZCB3b3JrLCB5b3UgaW5kaWNhdGUgeW91ciBhY2NlcHRhbmNlIG9mIHRoaXMg
TGljZW5zZSB0byBkbyBzby4KCiAgIDEwLiBBdXRvbWF0aWMgTGljZW5zaW5nIG9mIERvd25zdHJl
YW0gUmVjaXBpZW50cy4KCiAgIEVhY2ggdGltZSB5b3UgY29udmV5IGEgY292ZXJlZCB3b3JrLCB0
aGUgcmVjaXBpZW50IGF1dG9tYXRpY2FsbHkKIHJlY2VpdmVzIGEgbGljZW5zZSBmcm9tIHRoZSBv
cmlnaW5hbCBsaWNlbnNvcnMsIHRvIHJ1biwgbW9kaWZ5IGFuZAogcHJvcGFnYXRlIHRoYXQgd29y
aywgc3ViamVjdCB0byB0aGlzIExpY2Vuc2UuICBZb3UgYXJlIG5vdCByZXNwb25zaWJsZQogZm9y
IGVuZm9yY2luZyBjb21wbGlhbmNlIGJ5IHRoaXJkIHBhcnRpZXMgd2l0aCB0aGlzIExpY2Vuc2Uu
CgogICBBbiAiZW50aXR5IHRyYW5zYWN0aW9uIiBpcyBhIHRyYW5zYWN0aW9uIHRyYW5zZmVycmlu
ZyBjb250cm9sIG9mIGFuCiBvcmdhbml6YXRpb24sIG9yIHN1YnN0YW50aWFsbHkgYWxsIGFzc2V0
cyBvZiBvbmUsIG9yIHN1YmRpdmlkaW5nIGFuCiBvcmdhbml6YXRpb24sIG9yIG1lcmdpbmcgb3Jn
YW5pemF0aW9ucy4gIElmIHByb3BhZ2F0aW9uIG9mIGEgY292ZXJlZAogd29yayByZXN1bHRzIGZy
b20gYW4gZW50aXR5IHRyYW5zYWN0aW9uLCBlYWNoIHBhcnR5IHRvIHRoYXQKIHRyYW5zYWN0aW9u
IHdobyByZWNlaXZlcyBhIGNvcHkgb2YgdGhlIHdvcmsgYWxzbyByZWNlaXZlcyB3aGF0ZXZlcgog
bGljZW5zZXMgdG8gdGhlIHdvcmsgdGhlIHBhcnR5J3MgcHJlZGVjZXNzb3IgaW4gaW50ZXJlc3Qg
aGFkIG9yIGNvdWxkCiBnaXZlIHVuZGVyIHRoZSBwcmV2aW91cyBwYXJhZ3JhcGgsIHBsdXMgYSBy
aWdodCB0byBwb3NzZXNzaW9uIG9mIHRoZQogQ29ycmVzcG9uZGluZyBTb3VyY2Ugb2YgdGhlIHdv
cmsgZnJvbSB0aGUgcHJlZGVjZXNzb3IgaW4gaW50ZXJlc3QsIGlmCiB0aGUgcHJlZGVjZXNzb3Ig
aGFzIGl0IG9yIGNhbiBnZXQgaXQgd2l0aCByZWFzb25hYmxlIGVmZm9ydHMuCgogICBZb3UgbWF5
IG5vdCBpbXBvc2UgYW55IGZ1cnRoZXIgcmVzdHJpY3Rpb25zIG9uIHRoZSBleGVyY2lzZSBvZiB0
aGUKIHJpZ2h0cyBncmFudGVkIG9yIGFmZmlybWVkIHVuZGVyIHRoaXMgTGljZW5zZS4gIEZvciBl
eGFtcGxlLCB5b3UgbWF5CiBub3QgaW1wb3NlIGEgbGljZW5zZSBmZWUsIHJveWFsdHksIG9yIG90
aGVyIGNoYXJnZSBmb3IgZXhlcmNpc2Ugb2YKIHJpZ2h0cyBncmFudGVkIHVuZGVyIHRoaXMgTGlj
ZW5zZSwgYW5kIHlvdSBtYXkgbm90IGluaXRpYXRlIGxpdGlnYXRpb24KIChpbmNsdWRpbmcgYSBj
cm9zcy1jbGFpbSBvciBjb3VudGVyY2xhaW0gaW4gYSBsYXdzdWl0KSBhbGxlZ2luZyB0aGF0CiBh
bnkgcGF0ZW50IGNsYWltIGlzIGluZnJpbmdlZCBieSBtYWtpbmcsIHVzaW5nLCBzZWxsaW5nLCBv
ZmZlcmluZyBmb3IKIHNhbGUsIG9yIGltcG9ydGluZyB0aGUgUHJvZ3JhbSBvciBhbnkgcG9ydGlv
biBvZiBpdC4KCiAgIDExLiBQYXRlbnRzLgoKICAgQSAiY29udHJpYnV0b3IiIGlzIGEgY29weXJp
Z2h0IGhvbGRlciB3aG8gYXV0aG9yaXplcyB1c2UgdW5kZXIgdGhpcwogTGljZW5zZSBvZiB0aGUg
UHJvZ3JhbSBvciBhIHdvcmsgb24gd2hpY2ggdGhlIFByb2dyYW0gaXMgYmFzZWQuICBUaGUKIHdv
cmsgdGh1cyBsaWNlbnNlZCBpcyBjYWxsZWQgdGhlIGNvbnRyaWJ1dG9yJ3MgImNvbnRyaWJ1dG9y
IHZlcnNpb24iLgoKICAgQSBjb250cmlidXRvcidzICJlc3NlbnRpYWwgcGF0ZW50IGNsYWltcyIg
YXJlIGFsbCBwYXRlbnQgY2xhaW1zCiBvd25lZCBvciBjb250cm9sbGVkIGJ5IHRoZSBjb250cmli
dXRvciwgd2hldGhlciBhbHJlYWR5IGFjcXVpcmVkIG9yCiBoZXJlYWZ0ZXIgYWNxdWlyZWQsIHRo
YXQgd291bGQgYmUgaW5mcmluZ2VkIGJ5IHNvbWUgbWFubmVyLCBwZXJtaXR0ZWQKIGJ5IHRoaXMg
TGljZW5zZSwgb2YgbWFraW5nLCB1c2luZywgb3Igc2VsbGluZyBpdHMgY29udHJpYnV0b3IgdmVy
c2lvbiwKIGJ1dCBkbyBub3QgaW5jbHVkZSBjbGFpbXMgdGhhdCB3b3VsZCBiZSBpbmZyaW5nZWQg
b25seSBhcyBhCiBjb25zZXF1ZW5jZSBvZiBmdXJ0aGVyIG1vZGlmaWNhdGlvbiBvZiB0aGUgY29u
dHJpYnV0b3IgdmVyc2lvbi4gIEZvcgogcHVycG9zZXMgb2YgdGhpcyBkZWZpbml0aW9uLCAiY29u
dHJvbCIgaW5jbHVkZXMgdGhlIHJpZ2h0IHRvIGdyYW50CiBwYXRlbnQgc3VibGljZW5zZXMgaW4g
YSBtYW5uZXIgY29uc2lzdGVudCB3aXRoIHRoZSByZXF1aXJlbWVudHMgb2YKIHRoaXMgTGljZW5z
ZS4KCiAgIEVhY2ggY29udHJpYnV0b3IgZ3JhbnRzIHlvdSBhIG5vbi1leGNsdXNpdmUsIHdvcmxk
d2lkZSwgcm95YWx0eS1mcmVlCiBwYXRlbnQgbGljZW5zZSB1bmRlciB0aGUgY29udHJpYnV0b3In
cyBlc3NlbnRpYWwgcGF0ZW50IGNsYWltcywgdG8KIG1ha2UsIHVzZSwgc2VsbCwgb2ZmZXIgZm9y
IHNhbGUsIGltcG9ydCBhbmQgb3RoZXJ3aXNlIHJ1biwgbW9kaWZ5IGFuZAogcHJvcGFnYXRlIHRo
ZSBjb250ZW50cyBvZiBpdHMgY29udHJpYnV0b3IgdmVyc2lvbi4KCiAgIEluIHRoZSBmb2xsb3dp
bmcgdGhyZWUgcGFyYWdyYXBocywgYSAicGF0ZW50IGxpY2Vuc2UiIGlzIGFueSBleHByZXNzCiBh
Z3JlZW1lbnQgb3IgY29tbWl0bWVudCwgaG93ZXZlciBkZW5vbWluYXRlZCwgbm90IHRvIGVuZm9y
Y2UgYSBwYXRlbnQKIChzdWNoIGFzIGFuIGV4cHJlc3MgcGVybWlzc2lvbiB0byBwcmFjdGljZSBh
IHBhdGVudCBvciBjb3ZlbmFudCBub3QgdG8KIHN1ZSBmb3IgcGF0ZW50IGluZnJpbmdlbWVudCku
ICBUbyAiZ3JhbnQiIHN1Y2ggYSBwYXRlbnQgbGljZW5zZSB0byBhCiBwYXJ0eSBtZWFucyB0byBt
YWtlIHN1Y2ggYW4gYWdyZWVtZW50IG9yIGNvbW1pdG1lbnQgbm90IHRvIGVuZm9yY2UgYQogcGF0
ZW50IGFnYWluc3QgdGhlIHBhcnR5LgoKICAgSWYgeW91IGNvbnZleSBhIGNvdmVyZWQgd29yaywg
a25vd2luZ2x5IHJlbHlpbmcgb24gYSBwYXRlbnQgbGljZW5zZSwKIGFuZCB0aGUgQ29ycmVzcG9u
ZGluZyBTb3VyY2Ugb2YgdGhlIHdvcmsgaXMgbm90IGF2YWlsYWJsZSBmb3IgYW55b25lCiB0byBj
b3B5LCBmcmVlIG9mIGNoYXJnZSBhbmQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoaXMgTGljZW5zZSwg
dGhyb3VnaCBhCiBwdWJsaWNseSBhdmFpbGFibGUgbmV0d29yayBzZXJ2ZXIgb3Igb3RoZXIgcmVh
ZGlseSBhY2Nlc3NpYmxlIG1lYW5zLAogdGhlbiB5b3UgbXVzdCBlaXRoZXIgKDEpIGNhdXNlIHRo
ZSBDb3JyZXNwb25kaW5nIFNvdXJjZSB0byBiZSBzbwogYXZhaWxhYmxlLCBvciAoMikgYXJyYW5n
ZSB0byBkZXByaXZlIHlvdXJzZWxmIG9mIHRoZSBiZW5lZml0IG9mIHRoZQogcGF0ZW50IGxpY2Vu
c2UgZm9yIHRoaXMgcGFydGljdWxhciB3b3JrLCBvciAoMykgYXJyYW5nZSwgaW4gYSBtYW5uZXIK
IGNvbnNpc3RlbnQgd2l0aCB0aGUgcmVxdWlyZW1lbnRzIG9mIHRoaXMgTGljZW5zZSwgdG8gZXh0
ZW5kIHRoZSBwYXRlbnQKIGxpY2Vuc2UgdG8gZG93bnN0cmVhbSByZWNpcGllbnRzLiAgIktub3dp
bmdseSByZWx5aW5nIiBtZWFucyB5b3UgaGF2ZQogYWN0dWFsIGtub3dsZWRnZSB0aGF0LCBidXQg
Zm9yIHRoZSBwYXRlbnQgbGljZW5zZSwgeW91ciBjb252ZXlpbmcgdGhlCiBjb3ZlcmVkIHdvcmsg
aW4gYSBjb3VudHJ5LCBvciB5b3VyIHJlY2lwaWVudCdzIHVzZSBvZiB0aGUgY292ZXJlZCB3b3Jr
CiBpbiBhIGNvdW50cnksIHdvdWxkIGluZnJpbmdlIG9uZSBvciBtb3JlIGlkZW50aWZpYWJsZSBw
YXRlbnRzIGluIHRoYXQKIGNvdW50cnkgdGhhdCB5b3UgaGF2ZSByZWFzb24gdG8gYmVsaWV2ZSBh
cmUgdmFsaWQuCgogICBJZiwgcHVyc3VhbnQgdG8gb3IgaW4gY29ubmVjdGlvbiB3aXRoIGEgc2lu
Z2xlIHRyYW5zYWN0aW9uIG9yCiBhcnJhbmdlbWVudCwgeW91IGNvbnZleSwgb3IgcHJvcGFnYXRl
IGJ5IHByb2N1cmluZyBjb252ZXlhbmNlIG9mLCBhCiBjb3ZlcmVkIHdvcmssIGFuZCBncmFudCBh
IHBhdGVudCBsaWNlbnNlIHRvIHNvbWUgb2YgdGhlIHBhcnRpZXMKIHJlY2VpdmluZyB0aGUgY292
ZXJlZCB3b3JrIGF1dGhvcml6aW5nIHRoZW0gdG8gdXNlLCBwcm9wYWdhdGUsIG1vZGlmeQogb3Ig
Y29udmV5IGEgc3BlY2lmaWMgY29weSBvZiB0aGUgY292ZXJlZCB3b3JrLCB0aGVuIHRoZSBwYXRl
bnQgbGljZW5zZQogeW91IGdyYW50IGlzIGF1dG9tYXRpY2FsbHkgZXh0ZW5kZWQgdG8gYWxsIHJl
Y2lwaWVudHMgb2YgdGhlIGNvdmVyZWQKIHdvcmsgYW5kIHdvcmtzIGJhc2VkIG9uIGl0LgoKICAg
QSBwYXRlbnQgbGljZW5zZSBpcyAiZGlzY3JpbWluYXRvcnkiIGlmIGl0IGRvZXMgbm90IGluY2x1
ZGUgd2l0aGluCiB0aGUgc2NvcGUgb2YgaXRzIGNvdmVyYWdlLCBwcm9oaWJpdHMgdGhlIGV4ZXJj
aXNlIG9mLCBvciBpcwogY29uZGl0aW9uZWQgb24gdGhlIG5vbi1leGVyY2lzZSBvZiBvbmUgb3Ig
bW9yZSBvZiB0aGUgcmlnaHRzIHRoYXQgYXJlCiBzcGVjaWZpY2FsbHkgZ3JhbnRlZCB1bmRlciB0
aGlzIExpY2Vuc2UuICBZb3UgbWF5IG5vdCBjb252ZXkgYSBjb3ZlcmVkCiB3b3JrIGlmIHlvdSBh
cmUgYSBwYXJ0eSB0byBhbiBhcnJhbmdlbWVudCB3aXRoIGEgdGhpcmQgcGFydHkgdGhhdCBpcwog
aW4gdGhlIGJ1c2luZXNzIG9mIGRpc3RyaWJ1dGluZyBzb2Z0d2FyZSwgdW5kZXIgd2hpY2ggeW91
IG1ha2UgcGF5bWVudAogdG8gdGhlIHRoaXJkIHBhcnR5IGJhc2VkIG9uIHRoZSBleHRlbnQgb2Yg
eW91ciBhY3Rpdml0eSBvZiBjb252ZXlpbmcKIHRoZSB3b3JrLCBhbmQgdW5kZXIgd2hpY2ggdGhl
IHRoaXJkIHBhcnR5IGdyYW50cywgdG8gYW55IG9mIHRoZQogcGFydGllcyB3aG8gd291bGQgcmVj
ZWl2ZSB0aGUgY292ZXJlZCB3b3JrIGZyb20geW91LCBhIGRpc2NyaW1pbmF0b3J5CiBwYXRlbnQg
bGljZW5zZSAoYSkgaW4gY29ubmVjdGlvbiB3aXRoIGNvcGllcyBvZiB0aGUgY292ZXJlZCB3b3Jr
CiBjb252ZXllZCBieSB5b3UgKG9yIGNvcGllcyBtYWRlIGZyb20gdGhvc2UgY29waWVzKSwgb3Ig
KGIpIHByaW1hcmlseQogZm9yIGFuZCBpbiBjb25uZWN0aW9uIHdpdGggc3BlY2lmaWMgcHJvZHVj
dHMgb3IgY29tcGlsYXRpb25zIHRoYXQKIGNvbnRhaW4gdGhlIGNvdmVyZWQgd29yaywgdW5sZXNz
IHlvdSBlbnRlcmVkIGludG8gdGhhdCBhcnJhbmdlbWVudCwKIG9yIHRoYXQgcGF0ZW50IGxpY2Vu
c2Ugd2FzIGdyYW50ZWQsIHByaW9yIHRvIDI4IE1hcmNoIDIwMDcuCgogICBOb3RoaW5nIGluIHRo
aXMgTGljZW5zZSBzaGFsbCBiZSBjb25zdHJ1ZWQgYXMgZXhjbHVkaW5nIG9yIGxpbWl0aW5nCiBh
bnkgaW1wbGllZCBsaWNlbnNlIG9yIG90aGVyIGRlZmVuc2VzIHRvIGluZnJpbmdlbWVudCB0aGF0
IG1heQogb3RoZXJ3aXNlIGJlIGF2YWlsYWJsZSB0byB5b3UgdW5kZXIgYXBwbGljYWJsZSBwYXRl
bnQgbGF3LgoKICAgMTIuIE5vIFN1cnJlbmRlciBvZiBPdGhlcnMnIEZyZWVkb20uCgogICBJZiBj
b25kaXRpb25zIGFyZSBpbXBvc2VkIG9uIHlvdSAod2hldGhlciBieSBjb3VydCBvcmRlciwgYWdy
ZWVtZW50IG9yCiBvdGhlcndpc2UpIHRoYXQgY29udHJhZGljdCB0aGUgY29uZGl0aW9ucyBvZiB0
aGlzIExpY2Vuc2UsIHRoZXkgZG8gbm90CiBleGN1c2UgeW91IGZyb20gdGhlIGNvbmRpdGlvbnMg
b2YgdGhpcyBMaWNlbnNlLiAgSWYgeW91IGNhbm5vdCBjb252ZXkgYQogY292ZXJlZCB3b3JrIHNv
IGFzIHRvIHNhdGlzZnkgc2ltdWx0YW5lb3VzbHkgeW91ciBvYmxpZ2F0aW9ucyB1bmRlciB0aGlz
CiBMaWNlbnNlIGFuZCBhbnkgb3RoZXIgcGVydGluZW50IG9ibGlnYXRpb25zLCB0aGVuIGFzIGEg
Y29uc2VxdWVuY2UgeW91IG1heQogbm90IGNvbnZleSBpdCBhdCBhbGwuICBGb3IgZXhhbXBsZSwg
aWYgeW91IGFncmVlIHRvIHRlcm1zIHRoYXQgb2JsaWdhdGUgeW91CiB0byBjb2xsZWN0IGEgcm95
YWx0eSBmb3IgZnVydGhlciBjb252ZXlpbmcgZnJvbSB0aG9zZSB0byB3aG9tIHlvdSBjb252ZXkK
IHRoZSBQcm9ncmFtLCB0aGUgb25seSB3YXkgeW91IGNvdWxkIHNhdGlzZnkgYm90aCB0aG9zZSB0
ZXJtcyBhbmQgdGhpcwogTGljZW5zZSB3b3VsZCBiZSB0byByZWZyYWluIGVudGlyZWx5IGZyb20g
Y29udmV5aW5nIHRoZSBQcm9ncmFtLgoKICAgMTMuIFVzZSB3aXRoIHRoZSBHTlUgQWZmZXJvIEdl
bmVyYWwgUHVibGljIExpY2Vuc2UuCgogICBOb3R3aXRoc3RhbmRpbmcgYW55IG90aGVyIHByb3Zp
c2lvbiBvZiB0aGlzIExpY2Vuc2UsIHlvdSBoYXZlCiBwZXJtaXNzaW9uIHRvIGxpbmsgb3IgY29t
YmluZSBhbnkgY292ZXJlZCB3b3JrIHdpdGggYSB3b3JrIGxpY2Vuc2VkCiB1bmRlciB2ZXJzaW9u
IDMgb2YgdGhlIEdOVSBBZmZlcm8gR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBpbnRvIGEgc2luZ2xl
CiBjb21iaW5lZCB3b3JrLCBhbmQgdG8gY29udmV5IHRoZSByZXN1bHRpbmcgd29yay4gIFRoZSB0
ZXJtcyBvZiB0aGlzCiBMaWNlbnNlIHdpbGwgY29udGludWUgdG8gYXBwbHkgdG8gdGhlIHBhcnQg
d2hpY2ggaXMgdGhlIGNvdmVyZWQgd29yaywKIGJ1dCB0aGUgc3BlY2lhbCByZXF1aXJlbWVudHMg
b2YgdGhlIEdOVSBBZmZlcm8gR2VuZXJhbCBQdWJsaWMgTGljZW5zZSwKIHNlY3Rpb24gMTMsIGNv
bmNlcm5pbmcgaW50ZXJhY3Rpb24gdGhyb3VnaCBhIG5ldHdvcmsgd2lsbCBhcHBseSB0byB0aGUK
IGNvbWJpbmF0aW9uIGFzIHN1Y2guCgogICAxNC4gUmV2aXNlZCBWZXJzaW9ucyBvZiB0aGlzIExp
Y2Vuc2UuCgogICBUaGUgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uIG1heSBwdWJsaXNoIHJldmlz
ZWQgYW5kL29yIG5ldyB2ZXJzaW9ucyBvZgogdGhlIEdOVSBHZW5lcmFsIFB1YmxpYyBMaWNlbnNl
IGZyb20gdGltZSB0byB0aW1lLiAgU3VjaCBuZXcgdmVyc2lvbnMgd2lsbAogYmUgc2ltaWxhciBp
biBzcGlyaXQgdG8gdGhlIHByZXNlbnQgdmVyc2lvbiwgYnV0IG1heSBkaWZmZXIgaW4gZGV0YWls
IHRvCiBhZGRyZXNzIG5ldyBwcm9ibGVtcyBvciBjb25jZXJucy4KCiAgIEVhY2ggdmVyc2lvbiBp
cyBnaXZlbiBhIGRpc3Rpbmd1aXNoaW5nIHZlcnNpb24gbnVtYmVyLiAgSWYgdGhlCiBQcm9ncmFt
IHNwZWNpZmllcyB0aGF0IGEgY2VydGFpbiBudW1iZXJlZCB2ZXJzaW9uIG9mIHRoZSBHTlUgR2Vu
ZXJhbAogUHVibGljIExpY2Vuc2UgIm9yIGFueSBsYXRlciB2ZXJzaW9uIiBhcHBsaWVzIHRvIGl0
LCB5b3UgaGF2ZSB0aGUKIG9wdGlvbiBvZiBmb2xsb3dpbmcgdGhlIHRlcm1zIGFuZCBjb25kaXRp
b25zIGVpdGhlciBvZiB0aGF0IG51bWJlcmVkCiB2ZXJzaW9uIG9yIG9mIGFueSBsYXRlciB2ZXJz
aW9uIHB1Ymxpc2hlZCBieSB0aGUgRnJlZSBTb2Z0d2FyZQogRm91bmRhdGlvbi4gIElmIHRoZSBQ
cm9ncmFtIGRvZXMgbm90IHNwZWNpZnkgYSB2ZXJzaW9uIG51bWJlciBvZiB0aGUKIEdOVSBHZW5l
cmFsIFB1YmxpYyBMaWNlbnNlLCB5b3UgbWF5IGNob29zZSBhbnkgdmVyc2lvbiBldmVyIHB1Ymxp
c2hlZAogYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbi4KCiAgIElmIHRoZSBQcm9ncmFt
IHNwZWNpZmllcyB0aGF0IGEgcHJveHkgY2FuIGRlY2lkZSB3aGljaCBmdXR1cmUKIHZlcnNpb25z
IG9mIHRoZSBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBjYW4gYmUgdXNlZCwgdGhhdCBwcm94
eSdzCiBwdWJsaWMgc3RhdGVtZW50IG9mIGFjY2VwdGFuY2Ugb2YgYSB2ZXJzaW9uIHBlcm1hbmVu
dGx5IGF1dGhvcml6ZXMgeW91CiB0byBjaG9vc2UgdGhhdCB2ZXJzaW9uIGZvciB0aGUgUHJvZ3Jh
bS4KCiAgIExhdGVyIGxpY2Vuc2UgdmVyc2lvbnMgbWF5IGdpdmUgeW91IGFkZGl0aW9uYWwgb3Ig
ZGlmZmVyZW50CiBwZXJtaXNzaW9ucy4gIEhvd2V2ZXIsIG5vIGFkZGl0aW9uYWwgb2JsaWdhdGlv
bnMgYXJlIGltcG9zZWQgb24gYW55CiBhdXRob3Igb3IgY29weXJpZ2h0IGhvbGRlciBhcyBhIHJl
c3VsdCBvZiB5b3VyIGNob29zaW5nIHRvIGZvbGxvdyBhCiBsYXRlciB2ZXJzaW9uLgoKICAgMTUu
IERpc2NsYWltZXIgb2YgV2FycmFudHkuCgogICBUSEVSRSBJUyBOTyBXQVJSQU5UWSBGT1IgVEhF
IFBST0dSQU0sIFRPIFRIRSBFWFRFTlQgUEVSTUlUVEVEIEJZCiBBUFBMSUNBQkxFIExBVy4gIEVY
Q0VQVCBXSEVOIE9USEVSV0lTRSBTVEFURUQgSU4gV1JJVElORyBUSEUgQ09QWVJJR0hUCiBIT0xE
RVJTIEFORC9PUiBPVEhFUiBQQVJUSUVTIFBST1ZJREUgVEhFIFBST0dSQU0gIkFTIElTIiBXSVRI
T1VUIFdBUlJBTlRZCiBPRiBBTlkgS0lORCwgRUlUSEVSIEVYUFJFU1NFRCBPUiBJTVBMSUVELCBJ
TkNMVURJTkcsIEJVVCBOT1QgTElNSVRFRCBUTywKIFRIRSBJTVBMSUVEIFdBUlJBTlRJRVMgT0Yg
TUVSQ0hBTlRBQklMSVRZIEFORCBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIKIFBVUlBPU0UuICBU
SEUgRU5USVJFIFJJU0sgQVMgVE8gVEhFIFFVQUxJVFkgQU5EIFBFUkZPUk1BTkNFIE9GIFRIRSBQ
Uk9HUkFNCiBJUyBXSVRIIFlPVS4gIFNIT1VMRCBUSEUgUFJPR1JBTSBQUk9WRSBERUZFQ1RJVkUs
IFlPVSBBU1NVTUUgVEhFIENPU1QgT0YKIEFMTCBORUNFU1NBUlkgU0VSVklDSU5HLCBSRVBBSVIg
T1IgQ09SUkVDVElPTi4KCiAgIDE2LiBMaW1pdGF0aW9uIG9mIExpYWJpbGl0eS4KCiAgIElOIE5P
IEVWRU5UIFVOTEVTUyBSRVFVSVJFRCBCWSBBUFBMSUNBQkxFIExBVyBPUiBBR1JFRUQgVE8gSU4g
V1JJVElORwogV0lMTCBBTlkgQ09QWVJJR0hUIEhPTERFUiwgT1IgQU5ZIE9USEVSIFBBUlRZIFdI
TyBNT0RJRklFUyBBTkQvT1IgQ09OVkVZUwogVEhFIFBST0dSQU0gQVMgUEVSTUlUVEVEIEFCT1ZF
LCBCRSBMSUFCTEUgVE8gWU9VIEZPUiBEQU1BR0VTLCBJTkNMVURJTkcgQU5ZCiBHRU5FUkFMLCBT
UEVDSUFMLCBJTkNJREVOVEFMIE9SIENPTlNFUVVFTlRJQUwgREFNQUdFUyBBUklTSU5HIE9VVCBP
RiBUSEUKIFVTRSBPUiBJTkFCSUxJVFkgVE8gVVNFIFRIRSBQUk9HUkFNIChJTkNMVURJTkcgQlVU
IE5PVCBMSU1JVEVEIFRPIExPU1MgT0YKIERBVEEgT1IgREFUQSBCRUlORyBSRU5ERVJFRCBJTkFD
Q1VSQVRFIE9SIExPU1NFUyBTVVNUQUlORUQgQlkgWU9VIE9SIFRISVJECiBQQVJUSUVTIE9SIEEg
RkFJTFVSRSBPRiBUSEUgUFJPR1JBTSBUTyBPUEVSQVRFIFdJVEggQU5ZIE9USEVSIFBST0dSQU1T
KSwKIEVWRU4gSUYgU1VDSCBIT0xERVIgT1IgT1RIRVIgUEFSVFkgSEFTIEJFRU4gQURWSVNFRCBP
RiBUSEUgUE9TU0lCSUxJVFkgT0YKIFNVQ0ggREFNQUdFUy4KCiAgIDE3LiBJbnRlcnByZXRhdGlv
biBvZiBTZWN0aW9ucyAxNSBhbmQgMTYuCgogICBJZiB0aGUgZGlzY2xhaW1lciBvZiB3YXJyYW50
eSBhbmQgbGltaXRhdGlvbiBvZiBsaWFiaWxpdHkgcHJvdmlkZWQKIGFib3ZlIGNhbm5vdCBiZSBn
aXZlbiBsb2NhbCBsZWdhbCBlZmZlY3QgYWNjb3JkaW5nIHRvIHRoZWlyIHRlcm1zLAogcmV2aWV3
aW5nIGNvdXJ0cyBzaGFsbCBhcHBseSBsb2NhbCBsYXcgdGhhdCBtb3N0IGNsb3NlbHkgYXBwcm94
aW1hdGVzCiBhbiBhYnNvbHV0ZSB3YWl2ZXIgb2YgYWxsIGNpdmlsIGxpYWJpbGl0eSBpbiBjb25u
ZWN0aW9uIHdpdGggdGhlCiBQcm9ncmFtLCB1bmxlc3MgYSB3YXJyYW50eSBvciBhc3N1bXB0aW9u
IG9mIGxpYWJpbGl0eSBhY2NvbXBhbmllcyBhCiBjb3B5IG9mIHRoZSBQcm9ncmFtIGluIHJldHVy
biBmb3IgYSBmZWUuCgogICAgICAgICAgICAgICAgICAgICAgRU5EIE9GIFRFUk1TIEFORCBDT05E
SVRJT05TCgogICAgICAgICAgICAgSG93IHRvIEFwcGx5IFRoZXNlIFRlcm1zIHRvIFlvdXIgTmV3
IFByb2dyYW1zCgogICBJZiB5b3UgZGV2ZWxvcCBhIG5ldyBwcm9ncmFtLCBhbmQgeW91IHdhbnQg
aXQgdG8gYmUgb2YgdGhlIGdyZWF0ZXN0CiBwb3NzaWJsZSB1c2UgdG8gdGhlIHB1YmxpYywgdGhl
IGJlc3Qgd2F5IHRvIGFjaGlldmUgdGhpcyBpcyB0byBtYWtlIGl0CiBmcmVlIHNvZnR3YXJlIHdo
aWNoIGV2ZXJ5b25lIGNhbiByZWRpc3RyaWJ1dGUgYW5kIGNoYW5nZSB1bmRlciB0aGVzZSB0ZXJt
cy4KCiAgIFRvIGRvIHNvLCBhdHRhY2ggdGhlIGZvbGxvd2luZyBub3RpY2VzIHRvIHRoZSBwcm9n
cmFtLiAgSXQgaXMgc2FmZXN0CiB0byBhdHRhY2ggdGhlbSB0byB0aGUgc3RhcnQgb2YgZWFjaCBz
b3VyY2UgZmlsZSB0byBtb3N0IGVmZmVjdGl2ZWx5CiBzdGF0ZSB0aGUgZXhjbHVzaW9uIG9mIHdh
cnJhbnR5OyBhbmQgZWFjaCBmaWxlIHNob3VsZCBoYXZlIGF0IGxlYXN0CiB0aGUgImNvcHlyaWdo
dCIgbGluZSBhbmQgYSBwb2ludGVyIHRvIHdoZXJlIHRoZSBmdWxsIG5vdGljZSBpcyBmb3VuZC4K
CiAgICAgPG9uZSBsaW5lIHRvIGdpdmUgdGhlIHByb2dyYW0ncyBuYW1lIGFuZCBhIGJyaWVmIGlk
ZWEgb2Ygd2hhdCBpdCBkb2VzLj4KICAgICBDb3B5cmlnaHQgKEMpIDx5ZWFyPiAgPG5hbWUgb2Yg
YXV0aG9yPgoKICAgICBUaGlzIHByb2dyYW0gaXMgZnJlZSBzb2Z0d2FyZTogeW91IGNhbiByZWRp
c3RyaWJ1dGUgaXQgYW5kL29yIG1vZGlmeQogICAgIGl0IHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUg
R05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgYXMgcHVibGlzaGVkIGJ5CiAgICAgdGhlIEZyZWUg
U29mdHdhcmUgRm91bmRhdGlvbiwgZWl0aGVyIHZlcnNpb24gMyBvZiB0aGUgTGljZW5zZSwgb3IK
ICAgICAoYXQgeW91ciBvcHRpb24pIGFueSBsYXRlciB2ZXJzaW9uLgoKICAgICBUaGlzIHByb2dy
YW0gaXMgZGlzdHJpYnV0ZWQgaW4gdGhlIGhvcGUgdGhhdCBpdCB3aWxsIGJlIHVzZWZ1bCwKICAg
ICBidXQgV0lUSE9VVCBBTlkgV0FSUkFOVFk7IHdpdGhvdXQgZXZlbiB0aGUgaW1wbGllZCB3YXJy
YW50eSBvZgogICAgIE1FUkNIQU5UQUJJTElUWSBvciBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIg
UFVSUE9TRS4gIFNlZSB0aGUKICAgICBHTlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZSBmb3IgbW9y
ZSBkZXRhaWxzLgoKICAgICBZb3Ugc2hvdWxkIGhhdmUgcmVjZWl2ZWQgYSBjb3B5IG9mIHRoZSBH
TlUgR2VuZXJhbCBQdWJsaWMgTGljZW5zZQogICAgIGFsb25nIHdpdGggdGhpcyBwcm9ncmFtLiAg
SWYgbm90LCBzZWUgPGh0dHA6Ly93d3cuZ251Lm9yZy9saWNlbnNlcy8+LgoKIEFsc28gYWRkIGlu
Zm9ybWF0aW9uIG9uIGhvdyB0byBjb250YWN0IHlvdSBieSBlbGVjdHJvbmljIGFuZCBwYXBlciBt
YWlsLgoKICAgSWYgdGhlIHByb2dyYW0gZG9lcyB0ZXJtaW5hbCBpbnRlcmFjdGlvbiwgbWFrZSBp
dCBvdXRwdXQgYSBzaG9ydAogbm90aWNlIGxpa2UgdGhpcyB3aGVuIGl0IHN0YXJ0cyBpbiBhbiBp
bnRlcmFjdGl2ZSBtb2RlOgoKICAgICA8cHJvZ3JhbT4gIENvcHlyaWdodCAoQykgPHllYXI+ICA8
bmFtZSBvZiBhdXRob3I+CiAgICAgVGhpcyBwcm9ncmFtIGNvbWVzIHdpdGggQUJTT0xVVEVMWSBO
TyBXQVJSQU5UWTsgZm9yIGRldGFpbHMgdHlwZSBgc2hvdyB3Jy4KICAgICBUaGlzIGlzIGZyZWUg
c29mdHdhcmUsIGFuZCB5b3UgYXJlIHdlbGNvbWUgdG8gcmVkaXN0cmlidXRlIGl0CiAgICAgdW5k
ZXIgY2VydGFpbiBjb25kaXRpb25zOyB0eXBlIGBzaG93IGMnIGZvciBkZXRhaWxzLgoKIFRoZSBo
eXBvdGhldGljYWwgY29tbWFuZHMgYHNob3cgdycgYW5kIGBzaG93IGMnIHNob3VsZCBzaG93IHRo
ZSBhcHByb3ByaWF0ZQogcGFydHMgb2YgdGhlIEdlbmVyYWwgUHVibGljIExpY2Vuc2UuICBPZiBj
b3Vyc2UsIHlvdXIgcHJvZ3JhbSdzIGNvbW1hbmRzCiBtaWdodCBiZSBkaWZmZXJlbnQ7IGZvciBh
IEdVSSBpbnRlcmZhY2UsIHlvdSB3b3VsZCB1c2UgYW4gImFib3V0IGJveCIuCgogICBZb3Ugc2hv
dWxkIGFsc28gZ2V0IHlvdXIgZW1wbG95ZXIgKGlmIHlvdSB3b3JrIGFzIGEgcHJvZ3JhbW1lcikg
b3Igc2Nob29sLAogaWYgYW55LCB0byBzaWduIGEgImNvcHlyaWdodCBkaXNjbGFpbWVyIiBmb3Ig
dGhlIHByb2dyYW0sIGlmIG5lY2Vzc2FyeS4KIEZvciBtb3JlIGluZm9ybWF0aW9uIG9uIHRoaXMs
IGFuZCBob3cgdG8gYXBwbHkgYW5kIGZvbGxvdyB0aGUgR05VIEdQTCwgc2VlCiA8aHR0cDovL3d3
dy5nbnUub3JnL2xpY2Vuc2VzLz4uCgogICBUaGUgR05VIEdlbmVyYWwgUHVibGljIExpY2Vuc2Ug
ZG9lcyBub3QgcGVybWl0IGluY29ycG9yYXRpbmcgeW91ciBwcm9ncmFtCiBpbnRvIHByb3ByaWV0
YXJ5IHByb2dyYW1zLiAgSWYgeW91ciBwcm9ncmFtIGlzIGEgc3Vicm91dGluZSBsaWJyYXJ5LCB5
b3UKIG1heSBjb25zaWRlciBpdCBtb3JlIHVzZWZ1bCB0byBwZXJtaXQgbGlua2luZyBwcm9wcmll
dGFyeSBhcHBsaWNhdGlvbnMgd2l0aAogdGhlIGxpYnJhcnkuICBJZiB0aGlzIGlzIHdoYXQgeW91
IHdhbnQgdG8gZG8sIHVzZSB0aGUgR05VIExlc3NlciBHZW5lcmFsCiBQdWJsaWMgTGljZW5zZSBp
bnN0ZWFkIG9mIHRoaXMgTGljZW5zZS4gIEJ1dCBmaXJzdCwgcGxlYXNlIHJlYWQKIDxodHRwOi8v
d3d3LmdudS5vcmcvcGhpbG9zb3BoeS93aHktbm90LWxncGwuaHRtbD4uCg==
```
