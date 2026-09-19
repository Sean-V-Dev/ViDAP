# Decision Record: EP06 Generic License-Metadata Disposition

| Field | Value |
| --- | --- |
| Record | 0004 |
| Status | **Accepted** |
| Decision date | 2026-09-18 |
| Decision owner | Central (user-authorized) |
| Governing requirements | `ViDAP_Overview.txt`; `ViDAP_Phase_0_Plan.md`; accepted D0.6 in `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP06.md`; Decision Record 0003; `ViDAP_P0_EP06_Generic_License_Review.md` |

## Context

The P0-EP06 Windows license control correctly fails closed when the first
populated installed Python metadata field is not one of the existing policy's
recognized exact SPDX labels or a literal Decision Record 0003 catalog entry.
The review identified seven such claims in the current locked graph.

Each claim was traced from `python/uv.lock`, inspected in its corresponding
locked installed artifact, and found to be a `pip-audit` development/advisory
control dependency or a transitive dependency of that tool. No current ViDAP
application source imports any listed package, and no listed code, data, or
license-covered material is present in the current distributable output. The
packages are consumed unchanged.

This record is a bounded operational policy decision for the current lock. It
does not provide legal advice or a generic decision about any license family,
metadata label, or future distribution model.

## Decision

P0-EP06 may treat the following **literal package name, version, and gate
value** combinations as permitted only for their present unchanged,
non-distributed development/advisory-control roles:

| Literal control key | Verified locked license text | Present role | Required re-review trigger |
| --- | --- | --- | --- |
| `defusedxml@0.7.1` / `PSFL` | Python Software Foundation License Version 2 (`PSF-2.0`) | Transitive defensive-XML support in the `pip-audit` CycloneDX-support chain | Any version, gate value, role, modification, vendoring, or distribution change; retain applicable license text and notices before distribution. |
| `markdown-it-py@4.2.0` / `MIT License` | MIT | Transitive markdown rendering for `pip-audit` console presentation | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution. |
| `mdurl@0.1.2` / `MIT License` | MIT | Transitive URL parsing for the `pip-audit` markdown-rendering chain | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution. |
| `pip_api@0.0.35` / full `Apache License, Version 2.0` metadata text | Apache-2.0 | Transitive pip-environment access within `pip-audit` | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution. |
| `pip_audit@2.10.1` / `Apache Software License` | Apache-2.0 | Direct development dependency used only by `deps:audit` and the CI advisory-control job | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution. |
| `sortedcontainers@2.4.0` / `Apache 2.0` | Apache-2.0 | Transitive sorted-collection support in the `pip-audit` CycloneDX-support chain | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and any applicable NOTICE material before distribution. |
| `tomli_w@1.2.0` / `MIT License` | MIT | Transitive TOML-writing support in the `pip-audit` dependency chain | Any version, gate value, role, modification, vendoring, or distribution change; retain the license and copyright notice before distribution. |

The cited review records the exact dependency paths, installed license-file
locations, SHA-256 values, current build/output boundary, and modification
check behind this table. `pip_api`, `pip_audit`, and `tomli_w` are intentional
literal scanner identities; this record does not authorize an underscore/
hyphen or any other canonical-name transformation.

## Required implementation boundary

Any implementation of this decision must use a literal three-part catalog:
package name, exact locked version, and exact gate value. It must report this
record identifier and the limited role/re-review trigger for a catalog match.

It must not:

- approve `PSFL`, `MIT License`, `Apache Software License`, `Apache 2.0`, or
  full Apache license text as generic label classes;
- approve a package merely because it is related to `pip-audit`;
- normalize future metadata by parsing or guessing license text at runtime;
- use version ranges, name prefixes, wildcards, or role inference; or
- weaken the fail-closed result for a missing, unknown, ambiguous, custom, or
  otherwise unapproved claim.

Decision Record 0003 remains in force. This record supplements it only for
the seven literal entries above.

## Consequences

Once an approved EP06 packet revision authorizes implementation, the license
gate can permit these seven current findings while continuing to fail closed
for all other unapproved findings. A fresh worker and independent validator
must confirm that the catalog matches this decision exactly and that normal
locked setup, inventory, audit, and hosted Windows CI remain unchanged.

This decision does not accept P0-EP06, clear the separately identified
tracked `node-compile-cache/` hygiene issue, alter a lock, or authorize later
packet work.

## Alternatives considered

- **Approve the label families generally:** Rejected. Generic metadata labels
  can conceal materially different license texts or obligations.
- **Suppress the seven findings:** Rejected. It would hide future graph or
  metadata drift rather than preserving review.
- **Replace `pip-audit` now:** Deferred. It is a separate dependency-control
  decision and would require review of a new locked graph.

## Revisit triggers

Revisit this decision before any affected version or gate value changes; before
any listed package becomes runtime, bundled, vendored, modified, or
distributed; before an installer, desktop shell, or packaged Python environment
is introduced; or when the advisory-control tool is replaced. A later decision
record must link to both Records 0003 and 0004 rather than silently extending
this catalog.
