# Dependency, License, and Advisory Controls

ViDAP's dependency controls review the actual locked, installed npm and Python
graphs. They are evidence for human review, not an SBOM, a safety guarantee,
or legal advice.

## Local commands

After `npm.cmd run setup`, run the following from Windows PowerShell:

```powershell
npm.cmd run deps:inventory
npm.cmd run license:check
npm.cmd run deps:audit
```

`deps:inventory` prints direct and transitive installed-package facts without
resolving, installing, writing a tracked report, or changing a lock.
`license:check` uses the locked local Node and Python tools and fails closed.
`deps:audit` runs `npm audit --json` plus a temporary, hash-preserving export
of `uv.lock` through `pip-audit --require-hashes --disable-pip --strict`. It
never uses `pip-audit --locked`, `npm audit fix`, `pip-audit --fix`, floating
resolution, or a hand-maintained requirements authority.

The audit script removes its local temporary directory in all cases. A local
`VIDAP_AUDIT_DIR` is honored only when it names a previously absent
`vidap-pip-audit-<32 lowercase hex>` child of the resolved system temporary
directory. The temporary root itself must be an existing non-reparse directory
outside the checkout and OneDrive. CI ignores that variable and uses only its
fixed runner-temporary child. Do not point the override at the repository,
OneDrive, a reparse point, or an existing location.

## License posture

The automatic policy allows SPDX-identified MIT, MIT-0, BSD-2-Clause,
BSD-3-Clause, ISC, Apache-2.0, 0BSD, Zlib, PSF-2.0, and CC0-1.0 when required
notices can be retained. It fails closed for GPL-only, AGPL, SSPL,
Commons-Clause/BUSL, non-commercial/no-derivatives, unlicensed, missing,
ambiguous, or custom claims. MPL, EPL, LGPL, CDDL, Artistic, Unicode/data,
multi-license, platform-binary, material-notice, generated, and native cases
are review-required and also fail closed unless an exact accepted catalog entry
applies.

[Decision Record 0003](decisions/0003-ep06-locked-license-disposition.md) and
[Decision Record 0004](decisions/0004-ep06-generic-license-metadata-disposition.md)
amend D0.6 only for their literal package/version/license-or-gate-value
catalogs. The control prints the record ID, limited role, and distribution
re-review trigger for every catalog match. A changed version, license string,
gate value, package role, or any unlisted package still fails closed; the
catalogs do not use ranges, prefixes, wildcards, inferred roles, or package-name
normalization.

For Python metadata, the control uses the first populated declaration field in
this fixed order: SPDX expression, package metadata, then classifier. It never
searches later fields for an allowed alternative. A generic label or a
non-SPDX full-text claim therefore remains an unapproved finding unless the
selected package/version/license-or-gate-value is an exact Record 0003 or 0004
catalog entry.

Tool metadata and scanner output begin review; they do not decide legal
compatibility or exploitability. A Central decision is required before a
review-required or prohibited finding can be accepted. No exception is created
by these controls, and required notices must be retained when distribution
obligations apply.

## Advisory and update handling

An advisory is triaged for the affected package and version, dependency path,
directness, severity/CVSS when supplied, reachability, exposure, platform,
exploit maturity, fixed version, and mitigation. A clean scan is not proof of
safety; an alert is not proof of exploitability. Critical findings are
acknowledged within one business day and high findings within five business
days. An unresolved reachable critical or high issue blocks merge or release
unless Central records a time-bounded mitigation and recheck.

Review locks and direct dependencies weekly, and perform emergency updates when
triage requires them. Dependabot may propose weekly npm and GitHub Actions
updates only: it has a two-PR limit per ecosystem and groups only patch/minor
development-tool updates within that ecosystem. Major and security updates stay
individually reviewable. There is no auto-merge, bot bypass, Dependabot UV
update, automatic fix, or Phase 0 SBOM. Revisit an SBOM before the first public
release, a later ML dependency, or distribution artifacts.

CI repeats the root locked setup and control tasks on `windows-latest`. Its
temporary Python advisory JSON may be retained as a 14-day artifact; no
dependency environment, cache, checkout, fixture, secret, or broader report is
uploaded. Suspected vulnerabilities continue to use the private route in
[`SECURITY.md`](../SECURITY.md).
