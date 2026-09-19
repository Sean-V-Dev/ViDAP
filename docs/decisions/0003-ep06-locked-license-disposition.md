# Decision Record: EP06 Locked-License Disposition

| Field | Value |
|---|---|
| ID | 0003 |
| Status | Accepted |
| Date | 2026-09-18 |
| Owners | Central |
| Governing requirements | `ViDAP_Overview.txt`; `ViDAP_Phase_0_Plan.md`; accepted D0.6 in `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP06.md`; `ViDAP_P0_EP06_Implementation_Report.md`; `ViDAP_P0_EP06_License_Graph_Review.md` |

## Context

P0-EP06 correctly stopped when its new fail-closed license gate encountered
licenses outside D0.6's original short allowlist. Central required a
locked-graph and release-behavior review before making any disposition. That
review establishes that the current findings are either exact, verified
normalization cases or unchanged development, test, build, and control-tool
dependencies that do not reach the current Phase 0 application output.

This decision amends the operational implementation of D0.6 only. It does not
change ViDAP's MIT license, make a legal conclusion, approve a license family
generically, distribute a notice bundle, or authorize a dependency/lock change.

## Decision

### 1. Exact normalizations

The license gate may classify an unambiguous, exact SPDX `MIT-0` declaration as
permitted. The current graph evidence is the two packages below. The remaining
normalizations are permitted only when the package name, locked version, and
declared license exactly match the evidence below:

| Locked package | Verified disposition |
|---|---|
| `@csstools/color-helpers@6.1.1`, `@csstools/css-syntax-patches-for-csstree@1.1.14` | Current exact SPDX `MIT-0` instances; permitted under the general MIT-0 normalization. |
| `colorama@0.4.6` | Its actual locked wheel license text is BSD-3-Clause despite the generic scanner label `BSD License`; permitted as BSD-3-Clause. |
| `packaging@26.3` | Its actual locked wheel supplies both Apache-2.0 and BSD-2-Clause texts and states `Apache-2.0 OR BSD-2-Clause`; permitted by selecting either already-permitted branch. |

This is not a blanket acceptance of generic BSD labels or multi-license
metadata. A future generic label, changed version, unknown expression, or any
`AND` expression remains unapproved until separately reviewed.

### 2. Bounded MPL-2.0 exceptions

The following exact package/version and usage combinations are permitted while
they remain unchanged and non-distributed:

| Locked package | Bounded permitted use |
|---|---|
| `lightningcss@1.33.0`; `lightningcss-win32-x64-msvc@1.33.0` | Vite's unchanged build-only CSS-processing capability. The current scaffold has no CSS source and does not include either package or binary in its output. |
| `certifi@2026.7.22` | Development/integration HTTP-client and advisory-tool certificate-bundle support only; it is not imported by the current application or included in its output. |
| `pathspec@1.1.1` | Development-only mypy path-pattern support; it is not an application dependency or output. |

This is not a generic MPL-2.0 approval. The exception ends if a package version,
dependency path, role, modification status, or release model changes; if a
covered source, executable, certificate bundle, or native binary is
distributed; or if an installer, desktop shell, packaged environment, or
packaged `node_modules` is introduced. Central must then re-review the
applicable MPL notices and source-availability obligations before release.

### 3. Bounded BlueOak and CC-BY exceptions

The following exact locked packages are permitted only for their current
development, test, quality, or local dependency-control roles:

| License | Locked packages |
|---|---|
| `BlueOak-1.0.0` | `chownr@3.0.0`; `common-ancestor-path@2.0.0`; `glob@13.0.6`; `isexe@4.0.0`; `lru-cache@11.5.2`; `minimatch@10.2.6`; `minipass@7.1.3`; `minipass-flush@1.0.7`; `path-scurry@2.0.2`; `tar@7.5.22`; `yallist@5.0.0`. |
| `CC-BY-4.0` | `caniuse-lite@1.0.30001810`. |
| `CC-BY-3.0` | `spdx-exceptions@2.5.0`. |
| `MIT AND CC-BY-3.0` | `spdx-ranges@2.1.1`, as a package/version-specific control-tool exception only. |

No listed package code or data is currently in a ViDAP release output. If any
listed material is distributed, Central must first record the applicable
license-text/link and attribution treatment. The `spdx-ranges` exception does
not create a general rule accepting `AND` expressions.

### 4. Automation limits

The EP06 control implementation must use a literal package/version/license
catalog for the bounded exceptions and state the matched record ID in its
diagnostic. It must not use ranges, name prefixes, wildcard license matching,
or infer a package's role from metadata. A changed version/license, a package
not listed above, a missing license, an unknown/ambiguous/custom label, or any
non-approved review-required/prohibited license must still fail closed.

## Alternatives considered

- **Disable or soften the license gate:** Rejected. It would discard the
  actual-graph review and allow future unexamined findings through.
- **Approve MPL, BlueOak, CC-BY, or multi-license expressions generally:**
  Rejected. Their obligations depend on exact material and distribution use.
- **Replace `license-checker-rseidelsohn` now:** Deferred. That would be a
  distinct tooling/dependency decision; it is not necessary to resolve the
  current graph with an auditable policy.
- **Treat local installation as end-user distribution:** Rejected for this
  current scope. The reviewed packages reside only in ignored development
  environments and are not part of the defined Phase 0 output.

## Consequences and tradeoffs

The EP06 gate remains fail-closed and obtains a concrete audit trail for each
currently known exception. It also carries a maintenance cost: each changed
locked package, new package, changed role, or release-model change must be
reviewed rather than silently inheriting this decision. That is intentional.

Distribution is a separate trigger. If a future release includes package code,
binary, or data covered by these exceptions, it must add the appropriate
third-party license, attribution, and source-availability treatment before
release. This record does not provide legal advice.

## Validation evidence

`ViDAP_P0_EP06_License_Graph_Review.md` records the exact package versions,
dependency paths, functions, installed license-text checks, current build
inspection, modification check, and release-behavior boundary. The earlier
`ViDAP_P0_EP06_Implementation_Report.md` documents the original fail-closed
stop. A fresh EP06 worker and independent validator must verify that the
revised control exactly implements this record and leaves all other cases
blocked.

## Follow-up owners

- **Central:** revise EP06 to version 0.2, require fresh user approval, and
  retain this record and the graph review as governing inputs.
- **Fresh EP06 worker:** update only the authorized EP06 implementation files
  so the classifier reflects this exact record; rerun the full control evidence.
- **Independent validator:** verify every catalog entry, the negative cases,
  current locked graph, release-output boundary, and fresh evidence.

## Supersession and revisit triggers

Revisit this decision before any affected version or license changes; before a
reviewed package becomes runtime, bundled, vendored, modified, or distributed;
before an installer/desktop shell/packaged environment is introduced; or when
the dependency-control tool is replaced. A later decision record must link to
this one rather than rewriting it.
