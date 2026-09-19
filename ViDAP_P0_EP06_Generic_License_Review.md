# ViDAP P0-EP06 — Generic License-Metadata Review

| Field | Value |
| --- | --- |
| Purpose | Central evidence review for the seven remaining fail-closed Python license claims |
| Review date | 2026-09-18 |
| Graph authority | `python/uv.lock` and the corresponding locked installed `.venv` artifacts |
| Python lock SHA-256 | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |
| Decision status | **Evidence only — this document makes no exception, policy amendment, or legal conclusion.** |

## 1. Why this review exists

The hosted Windows `dependency-license-windows` job now starts and reaches the
license gate. That gate correctly fails closed for seven Python packages whose
selected package-metadata value is not one of the policy's exact SPDX labels or
the literal catalog entries in Decision Record 0003.

The seven findings are metadata-normalization questions, not newly discovered
runtime product dependencies. The lock, the installed artifacts, and their
current paths were reviewed before proposing any disposition. This document is
not legal advice and does not approve a license family generally.

## 2. Review boundary and method

The current Phase 0 boundary remains unchanged:

1. ViDAP's only direct Python application dependencies are `fastapi` and
   `uvicorn`.
2. `pip-audit` is a direct **development** dependency used only by the EP06
   dependency-advisory control (`npm.cmd run deps:audit`) and its Windows CI
   job.
3. The seven packages below are `pip-audit` itself or its transitive
   dependencies. No current application source imports any of them.
4. The current web build contains the app HTML and JavaScript only. There is
   no installer, packaged Python environment, bundled dependency tree, or
   released application artifact.
5. No package is patched, forked, vendored, or otherwise modified by ViDAP;
   all are consumed unchanged from the locked package manager artifacts.

Accordingly, none of the seven packages' code, data, or license-covered files
reaches an end user in the current Phase 0 output. A later Python runtime
bundle, desktop/installer deliverable, packaged environment, vendored copy, or
use outside the dependency-control path invalidates this conclusion and
requires a new review.

## 3. Exact findings and resolved license texts

The control chooses the first populated declaration in this order: SPDX
expression, package metadata, then classifier. The **gate value** below is
therefore the exact value that made each finding fail. The **artifact result**
comes from the locked installed license file, identified by SHA-256.

| Locked package | Gate value | Actual locked license evidence | Dependency path and current role | Current distribution / modification | Decision-ready recommendation |
| --- | --- | --- | --- | --- | --- |
| `defusedxml@0.7.1` | `PSFL` | `LICENSE`, SHA-256 `B80CE9DA8C42A1F91079627FBBE2BF27210AE108A0FFE5F077D5B08E076C24C8`, begins **Python Software Foundation License Version 2**. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → `cyclonedx-python-lib@11.12.0` → `py-serializable@2.1.0` → package. Defensive XML handling in the advisory tool's CycloneDX-support chain. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to the verified Python Software Foundation License Version 2 / `PSF-2.0` result. If distributed later, retain the applicable license text and notices. |
| `markdown-it-py@4.2.0` | `MIT License` | `licenses/LICENSE`, SHA-256 `4A2260D6E2CD0F5A151A1E86DBFE7D3ED552B1E2BEABF9941C1BA5C49CBCE484`, is canonical MIT text. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → `rich@15.0.0` → package. Markdown rendering support for the advisory tool's console presentation. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `MIT`. If distributed later, retain the license text and copyright notice. |
| `mdurl@0.1.2` | `MIT License` | `LICENSE`, SHA-256 `7C605DF6E28667A9603118E98274F64A49CE3EED0D26FCCCE9534A345E0EF955`, is canonical MIT text. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → `rich@15.0.0` → `markdown-it-py@4.2.0` → package. URL parsing support for the advisory tool's markdown-rendering chain. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `MIT`. If distributed later, retain the license text and copyright notice. |
| `pip_api@0.0.35` | full `Apache License, Version 2.0` text in package metadata | `licenses/LICENSE`, SHA-256 `14ED54990120EFEA26042269885DF36E1B53DB858BF04B40C8CFC8C5E12F6FB1`, is Apache License 2.0. The underscore name is the literal `pip-licenses` scanner identity; the lock/distribution project name is `pip-api`. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → package. Pip-environment access used within the advisory-control tool. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `Apache-2.0`. If distributed later, retain the license; preserve any applicable NOTICE material. |
| `pip_audit@2.10.1` | `Apache Software License` classifier | `licenses/LICENSE`, SHA-256 `0D542E0C8804E39AA7F37EB00DA5A762149DC682D7829451287E11B938E94594`, is Apache License 2.0. The underscore name is the literal `pip-licenses` scanner identity; the lock/distribution project name is `pip-audit`. | `vidap-foundation` → direct dev package. The EP06 advisory-control command invokes it against a temporary hash-preserving export; it is not application code. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `Apache-2.0`. If distributed later, retain the license; preserve any applicable NOTICE material. |
| `sortedcontainers@2.4.0` | `Apache 2.0` | `LICENSE`, SHA-256 `1DB7CAE7FCE6452E2E608E401A0F953E0133E4C2D75DB69FB8AE851D2086F5B6`, states it is licensed under Apache License, Version 2.0. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → `cyclonedx-python-lib@11.12.0` → package. Sorted-collection support in the advisory tool's CycloneDX-support chain. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `Apache-2.0`. If distributed later, retain the license; preserve any applicable NOTICE material. |
| `tomli_w@1.2.0` | `MIT License` | `LICENSE`, SHA-256 `B80816B0D530B8ACCB4C2211783790984A6E3B61922C2B5EE92F3372AB2742FE`, is canonical MIT text. The underscore name is the literal `pip-licenses` scanner identity; the lock/distribution project name is `tomli-w`. | `vidap-foundation` → direct dev `pip-audit@2.10.1` → package. TOML-writing support within the advisory-control dependency chain. | Control-only, unchanged, and absent from current output. | **Package/version-specific permitted normalization candidate** to verified `MIT`. If distributed later, retain the license text and copyright notice. |

## 4. What this does and does not support

The evidence supports a **literal package/version/gate-value catalog** if
Central decides to allow these current locked development-control packages.
It does **not** support:

- a blanket approval of labels such as `MIT License`, `Apache Software
  License`, `Apache 2.0`, or `PSFL`;
- approval of a different version of any listed package;
- treating an uninspected full-text metadata field as equivalent to SPDX;
- approving a package merely because it is a `pip-audit` transitive
  dependency; or
- changing the current fail-closed behavior for future unknown or ambiguous
  claims.

If Central accepts a bounded disposition, the implementation must match the
scanner's literal three-part identity: package name, locked version, and the
gate value in the table. The implementation should not rewrite the metadata,
infer the actual license at runtime, or use prefixes, wildcards, ranges, or
generic license-family rules.

## 5. Central decision options

1. **Create a new Decision Record 0004** that adds only the seven literal
   package/version/gate-value entries above, each restricted to unchanged,
   non-distributed development/advisory-control use and with the stated
   re-review trigger.
2. **Defer one or more entries.** The license job must remain red for each
   deferred entry; it is not permissible to suppress the finding.
3. **Replace or remove the relevant development tool.** That is a separate
   scoped dependency decision and must be evaluated against its own new locked
   graph.

No option here resolves the separately identified committed
`node-compile-cache/` hygiene issue. That correction needs its own authorized
scope and a corrective commit.
