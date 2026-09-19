# ViDAP P0-EP06 — Locked Dependency License-Graph Review

| Field | Value |
| --- | --- |
| Purpose | Central evidence review before any license-policy amendment or exception |
| Review date | 2026-09-18 |
| Graph authorities | `package-lock.json` and `python/uv.lock` |
| npm lock SHA-256 | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| Python lock SHA-256 | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |
| Decision status | **Evidence only — no approval, exception, or policy amendment is made here** |

## 1. Scope and method

This review answers why the packages flagged by the P0-EP06 license gate are
in the **current locked graph**, what they do, and whether their code or data
reaches a current ViDAP output. It is not legal advice and is deliberately not
a generic approval of any license family.

Evidence was taken from the two lockfiles, installed package manifests and
license files, `npm explain`, the root manifests, the current source tree, and
the current Vite output. The build output is an ignored local artifact, not a
released package. At this Phase 0 point, the web entry renders `null`, the
Python application imports only `FastAPI`, no CSS source exists, and there is
no installer, release package, or deployment path. See `README.md` and
`ViDAP_P0_EP06.md` for the retained Phase 0 boundary.

The restricted review sandbox can read the synchronized locked Python
environment but cannot invoke `uv.exe`; consequently this review verifies the
Python identities, paths, and license texts from `uv.lock` and the installed
locked `.venv`, rather than claiming a second `pip-licenses` execution. The
normal Windows execution evidence in the EP06 implementation report remains
the source for the worker's successful locked setup and inventory run.

Therefore, the conclusions below are limited to this release behavior:

1. a local development checkout installs its locked development tools;
2. `npm.cmd run build` emits only ignored `apps/web/dist/index.html` and an
   application JavaScript asset; and
3. no `node_modules`, `.venv`, native package binary, package data file, or
   third-party notice bundle is currently shipped to an end user.

Any future installer, desktop shell, server bundle, Python environment
distribution, packaged `node_modules`, output containing third-party data, or
change that adds imports/use of the packages below invalidates the applicable
conclusion and requires a new review.

## 2. Cross-cutting findings

### No modification or vendoring

The packages are consumed unchanged through the locked package managers.
There is no `patch-package` configuration, patch directory, vendored copy, or
source import of a reviewed package in `apps/web/src` or `python/src`. The
only current source imports are the selected product foundations (`react`,
`react-dom`, and `FastAPI`). The installed `node_modules` and `.venv` trees
are ignored local state.

### What counts as reaching a user

For this review, “reaches a user” means a third-party package, binary, data
set, or covered source is present in a ViDAP release artifact or accompanies a
released application. A tool that runs only during installation, tests,
quality checks, or building does not reach the user merely because it exists in
a developer's local dependency tree.

The current `apps/web/dist` inspection found no CSS asset, no `lightningcss`
identifier, and no reviewed package code or data. That establishes only the
current scaffold result; it is not a promise about a later, non-empty frontend.

### License-text verification

Where a scanner label was ambiguous, the installed locked artifact was checked:

| Package | Scanner/metadata label | Locked artifact result |
| --- | --- | --- |
| `colorama@0.4.6` | `BSD License` | Its bundled `licenses/LICENSE.txt` is the three-clause BSD text: it has the source-retention condition, the binary-documentation retention condition, and the no-endorsement clause. SHA-256: `CAC35C02686E5D04A5A7140BFB3B36E73AED496656E891102E428886D7930318`. It is BSD-3-Clause, not an unresolved generic BSD license. |
| `packaging@26.3` | `Apache-2.0 OR BSD-2-Clause` | Its bundled `LICENSE` states that the software is available under **either** `LICENSE.APACHE` or `LICENSE.BSD`; both full texts are present. SHA-256: `0D542E0C8804E39AA7F37EB00DA5A762149DC682D7829451287E11B938E94594` (Apache-2.0) and `B70E7E9B742F1CC6F948B34C16AA39FFECE94196364BC88FF0D2180F0028FAC5` (BSD-2-Clause). |

The other entries have explicit SPDX declarations and their local license
files were spot-checked: the two Lightning CSS packages contain MPL-2.0;
`caniuse-lite` contains CC BY 4.0; the two CSSTools packages contain MIT-0;
and a representative BlueOak package contains Blue Oak Model License 1.0.0.

## 3. Frontend build review — Lightning CSS

| Question | Verified answer |
| --- | --- |
| Exact locked packages | `lightningcss@1.33.0` and optional platform package `lightningcss-win32-x64-msvc@1.33.0`, both `MPL-2.0`. Their installed `LICENSE` files have the same SHA-256: `5EBA353FE5076AC3432177F8AB1CF75E3AFCD0584251E37C3BFEAD5F447D040E`. |
| Why present / path | `vidap` → direct dev dependency `vite@8.3.0` → `lightningcss@1.33.0` → optional `lightningcss-win32-x64-msvc@1.33.0`. Vite declares Lightning CSS as a dependency for frontend CSS processing. |
| Role | Build-time tooling, specifically CSS transformation/minification capability. It is not a direct ViDAP dependency or an application runtime dependency. |
| Current use | There are no CSS source files or Lightning CSS configuration in the current scaffold. The current build created no CSS asset. The package is installed because Vite supports CSS processing, but its compiler was not evidenced as processing any ViDAP CSS in this build. |
| What reaches a user now | Neither the JavaScript wrapper, the Windows native binary, nor MPL-covered Lightning CSS code appears in the present built application output. The ignored build output contains only the app HTML and JavaScript bundle. |
| Modification | None. ViDAP does not patch, fork, vendor, or modify Lightning CSS or its native binary. |
| MPL consequence for this current usage | Because no Lightning CSS covered source or executable is currently distributed, there is no current distribution action to perform for Lightning CSS. If a later release distributes covered Lightning CSS code or executable form, MPL 2.0 requires the covered source to be available and license/copyright notices to be retained; a larger work may otherwise use its own terms. |
| Recommended decision | **Package/version-specific permitted exception, limited to `lightningcss@1.33.0` and `lightningcss-win32-x64-msvc@1.33.0` as unchanged, build-only tooling with no distributed covered material.** Re-review before adding CSS processing, a desktop/installer bundle, packaged `node_modules`, or any distribution that contains Lightning CSS code/binaries. This is not a general MPL-2.0 approval. |

## 4. npm entries

The table records the exact locked package/version and a concrete dependency
path. Where npm has hoisted identical copies, the package/version is one legal
item even though it has several physical installed copies; all top-level
introducers are stated where relevant.

| Package and license | Why present and dependency path | Role | Current user-facing material / modification | Decision recommendation |
| --- | --- | --- | --- | --- |
| `@csstools/color-helpers@6.1.1` — `MIT-0` | `vidap` → direct dev `jsdom@30.1.0` → `@asamuzakjp/css-color@7.0.0` → `@csstools/css-color-parser@4.2.3` → package | Test DOM/CSS-color emulation support | Test-only; absent from build output; unchanged | **Generally permitted license normalization** for exact SPDX MIT-0, with normal license-retention handling when material is distributed. |
| `@csstools/css-syntax-patches-for-csstree@1.1.14` — `MIT-0` | `vidap` → direct dev `jsdom@30.1.0` → package | Test DOM CSS-parser compatibility data | Test-only; absent from build output; unchanged | **Generally permitted license normalization** for exact SPDX MIT-0. |
| `caniuse-lite@1.0.30001810` — `CC-BY-4.0` | `vidap` → direct dev `eslint-plugin-react-hooks@7.1.1` → `@babel/core@7.29.7` → `@babel/helper-compilation-targets@7.29.7` → `browserslist@4.29.0` → package | Browser-capability reference data used by development tooling | No `caniuse-lite` data is in the current app output; unchanged | **Package/version-specific permitted exception, development-only.** If its data is later included in a distributable artifact, require an explicit CC BY 4.0 attribution/notice treatment. |
| `chownr@3.0.0` — `BlueOak-1.0.0` | `vidap` → direct dev `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → `pacote@21.5.1` → `tar@7.5.22` → package | File ownership helper used by the local license-inventory control | Control-only; not in app output; unchanged | **Package/version-specific permitted exception, control-only.** No end-user notice is presently triggered because the package is not distributed. |
| `common-ancestor-path@2.0.0` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → package | Filesystem-path helper for the control tool | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `glob@13.0.6` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/package-json@7.0.5` → package | File matching for the control tool | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `isexe@4.0.0` — `BlueOak-1.0.0` | Installed copies are introduced only by `license-checker-rseidelsohn@5.0.1`, for example `… → @npmcli/package-json@7.0.5 → @npmcli/git → which → package` | Executable-location helper for the control tool | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `lru-cache@11.5.2` — `BlueOak-1.0.0` | Introduced by both `jsdom@30.1.0` (for example `vidap → jsdom → package`) and `license-checker-rseidelsohn@5.0.1` (for example `… → @npmcli/arborist → package`); all copies are this version | In-memory caching in test or control tooling | Test/control-only; not distributed; unchanged | **Package/version-specific permitted exception** for the stated test/control paths. |
| `minimatch@10.2.6` — `BlueOak-1.0.0` | Introduced by direct dev `eslint@10.10.0`, `typescript-eslint@8.70.0`, and `license-checker-rseidelsohn@5.0.1`; one concrete path is `vidap → eslint → package` | Pattern matching for quality/control tools | Development/control-only; not distributed; unchanged | **Package/version-specific permitted exception** for the stated quality/control paths. |
| `minipass@7.1.3` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → `cacache@20.0.4` → package | Stream helper for package/control tooling | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `minipass-flush@1.0.7` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → `cacache@20.0.4` → package | Stream-flush helper for package/control tooling | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `path-scurry@2.0.2` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/package-json@7.0.5` → `glob@13.0.6` → package | Filesystem traversal helper for control tooling | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `tar@7.5.22` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → `pacote@21.5.1` → package | Package-archive handling for control tooling | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `yallist@5.0.0` — `BlueOak-1.0.0` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `@npmcli/arborist@9.6.0` → `pacote@21.5.1` → `tar@7.5.22` → package | Linked-list helper for control tooling | Control-only; not distributed; unchanged | Same bounded control-only exception. |
| `spdx-exceptions@2.5.0` — `CC-BY-3.0` | `vidap` → direct dev `license-checker-rseidelsohn@5.0.1` → `spdx-expression-parse@4.0.0` → package | SPDX exception-reference data used to parse license expressions | Control-only; its data is not in any current output; unchanged | **Package/version-specific permitted exception, control-only.** If the reference data is distributed, require CC BY 3.0 attribution/notice review. |
| `spdx-ranges@2.1.1` — `(MIT AND CC-BY-3.0)` | `vidap` → `license-checker-rseidelsohn@5.0.1` → `spdx-satisfies@6.0.0` → package | SPDX license-range comparison data for the control tool | Control-only; not distributed; unchanged | **Package/version-specific permitted exception, control-only**, retaining both license components if the package/data is ever distributed. Do not convert `AND` expressions into an automatic generally-permitted rule. |

### BlueOak condition relevant to the above entries

Blue Oak Model License 1.0.0 requires a person distributing any part of the
software to provide the license text or a link to it. Because all identified
BlueOak packages are current development, test, quality, or control tooling and
are not in the present application output, no end-user notice bundle is
currently required. The bounded exceptions above must be revisited if any of
those packages become distributable material.

## 5. Python entries

| Package and license | Why present and dependency path | Role | Current user-facing material / modification | Decision recommendation |
| --- | --- | --- | --- | --- |
| `colorama@0.4.6` — resolved BSD-3-Clause | `vidap-foundation` → direct dev `pytest@9.1.1` → package on Windows (`sys_platform == 'win32'`) | Test-only console-color support | No application import, output, or modification; not distributed | **Generally permitted normalization**, but only when a future generic `BSD License` label is verified against the actual locked license artifact as done here. |
| `packaging@26.3` — `Apache-2.0 OR BSD-2-Clause` | `vidap-foundation` → direct dev `pytest@9.1.1` → package; and `vidap-foundation` → direct dev `pip-audit@2.10.1` → package | Test and advisory-control tooling | No application import, output, or modification; not distributed | **Generally permitted normalization** for an exact verified `A OR B` expression only when every selectable branch is already permitted. Never apply this to `AND`, unknown, or unverified expressions. |
| `certifi@2026.7.22` — `MPL-2.0` | `vidap-foundation` → direct dev `httpx@0.28.1` → package; also `vidap-foundation` → direct dev `pip-audit@2.10.1` → `requests@2.34.2` → package | Development/integration HTTP client and advisory-tool CA-certificate bundle | The current application source does not import HTTPX, Requests, or Certifi. Certifi's CA bundle is not in the present application output; unchanged | **Package/version-specific permitted exception, non-distributed development/control use.** Re-review if ViDAP ships a Python environment, uses it at runtime, or distributes its certificate bundle. |
| `pathspec@1.1.1` — `MPL-2.0` | `vidap-foundation` → direct dev `mypy@2.3.1` → package | Static type-checker path-pattern support | Development-only; no product source imports, output, or modification | **Package/version-specific permitted exception, non-distributed development use.** Re-review if it becomes runtime or distributable material. |

### MPL condition relevant to Lightning CSS, Certifi, and PathSpec

The installed license texts are MPL 2.0. MPL 2.0 permits use and inclusion in a
larger work, but when covered source or executable form is distributed it
requires keeping the applicable notices and making the covered source available
under MPL terms. ViDAP currently distributes none of the covered material from
the three reviewed uses. That is why the recommendations are bounded to the
exact package/version and usage class rather than a generic MPL approval.

## 6. Decision-ready summary

No policy has changed. If Central chooses to amend the policy, the evidence
supports the following narrow candidates:

1. **General normalization candidates:** exact SPDX `MIT-0`; verified
   BSD-3-Clause behind a generic `BSD License` label; and a verified `A OR B`
   expression where every selected branch is already permitted. These should
   retain fail-closed behavior for unknown labels, unverified generic labels,
   and all `AND` expressions.
2. **Bounded exceptions only:** `lightningcss@1.33.0`,
   `lightningcss-win32-x64-msvc@1.33.0`, `certifi@2026.7.22`, and
   `pathspec@1.1.1`, solely for the unchanged, non-distributed usages stated
   above. No generic MPL rule follows.
3. **Bounded exception plus distribution trigger:** the listed BlueOak,
   CC-BY, and SPDX-data packages are confined to dev/test/control paths today.
   Their present use supports a package/version-specific exception with no
   current end-user notice bundle; any distribution of their code or data must
   trigger the recorded license-text/link or attribution review.

Before accepting any of those candidates, Central should decide whether the
project wants to retain `license-checker-rseidelsohn` and its control-only
transitive graph. Replacing it would remove many BlueOak/CC-BY findings but is
a different technical decision and must be evaluated independently; it is not
an automatic remedy.

## 7. Primary license references

- [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
- [Blue Oak Model License 1.0.0](https://blueoakcouncil.org/license/1.0.0.html)
- [Creative Commons Attribution 4.0 International legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)
- [SPDX MIT No Attribution (MIT-0)](https://spdx.org/licenses/MIT-0.html)
- [SPDX BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html)
- [SPDX BSD-2-Clause](https://spdx.org/licenses/BSD-2-Clause.html)
