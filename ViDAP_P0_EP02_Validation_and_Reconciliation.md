# ViDAP P0-EP02 Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | P0-EP02 - Quality, CI, Dependency, and Fixture Decisions |
| Status | Accepted by Central |
| Reconciliation date | 2026-09-17 |
| Decision report | `ViDAP_P0_EP02_Decision_Report.md` |
| Governing packet | `ViDAP_P0_EP02.md` version 1.0 |
| Independent verdict | `Accept`, returned in chat on 2026-09-17 |
| Authority | Explicit user direction and Central reconciliation under Spine Section 1 |

---

## 1. Purpose

This record preserves the independent validator's final verdict, reconciles the previously reported findings, and records Central's acceptance of D0.4-D0.7. The validator returned its structured report in chat, as permitted by P0-EP02 Section 18; this file is Central's durable preservation of that result rather than a validator-authored file.

This reconciliation accepts policy and tool-selection decisions only. It does not install tools, add configuration, create workflows or fixtures, change remote settings, scaffold the application, or authorize P0-EP03 execution.

---

## 2. Independent Revalidation Result

The independent validator returned `Accept` and concluded that:

- `V-EP02-001` and `V-EP02-002` are resolved;
- the Python audit flow is lock-faithful, hash-checked, non-resolving, and confined to a bounded temporary path;
- CI audit, artifact, and cleanup steps independently derive `RUNNER_TEMP\vidap-pip-audit` instead of relying on cross-step state;
- the local override is normalized, bounded beneath the temporary root, constrained to the expected directory name, and rejected if the target already exists;
- EP02-AC01 through EP02-AC19 pass;
- EP02-AC20's independent-validation condition is satisfied by the `Accept` verdict, leaving only Central acceptance of D0.4-D0.7;
- file scope remained compliant and no tooling, scaffolding, configuration, fixture, lockfile, workflow, or P0-EP03 work was added; and
- the validator did not accept the decisions on Central's behalf.

The validator cited the official uv export reference, the pip-audit project documentation, and GitHub's environment-file documentation in support of the corrected audit flow.

---

## 3. Finding Dispositions

### V-EP02-001 - Resolved and independently confirmed

The corrected procedure derives Python advisory input from the uv lock through `uv export --locked --all-extras --all-groups --no-emit-project --format requirements.txt`, retains hashes, disables pip dependency resolution, and prohibits representing `pip-audit --locked` as consuming `uv.lock`. The independent validator confirmed this is lock-faithful.

### V-EP02-002 - Resolved and independently confirmed

The corrected CI steps each derive the same fixed `RUNNER_TEMP\vidap-pip-audit` path for audit, artifact handling, and cleanup, without relying on environment state created by another step. The local override is fail-closed and constrained before recursive cleanup. The independent validator confirmed the correction.

No blocking finding remains. The non-blocking implementation-time checks and later-phase deferrals in the decision report remain in force.

---

## 4. Accepted Decisions

### D0.4 - Quality and test layers: Accepted

The accepted foundation quality roles are:

- TypeScript compiler checking with `tsc --noEmit`;
- Prettier for formatting checks and explicit repair;
- ESLint flat configuration with TypeScript, React Hooks, and JSX accessibility coverage;
- Vitest, React Testing Library, and jsdom for UI foundation tests;
- Ruff for Python formatting and linting;
- mypy for Python static typing;
- pytest with AnyIO and HTTPX ASGI transport for Python and in-process service tests;
- direct coverage.py and Vitest V8 reports, with no numeric Phase 0 coverage threshold; and
- a repository-owned Node 24 cross-process smoke harness.

Full browser end-to-end testing is deferred to P3. Exact compatible versions and executable configuration remain subject to the named P0-EP04 through P0-EP07 implementation gates.

### D0.5 - CI and branch expectations: Accepted

GitHub Actions on `windows-latest` is the blocking Phase 0 CI lane and must invoke the authoritative root `npm.cmd run` tasks. The accepted policy covers pull-request, `main` push, manual, and weekly scheduled triggers; read-only default permissions; no required secrets; lock-keyed caches; pinned third-party actions; concurrency and artifact handling; and review plus required-check expectations. This decision does not itself change repository or GitHub settings.

### D0.6 - Dependency, license, vulnerability, and update policy: Accepted

Locked installation uses `npm ci` and `uv sync --locked`. License evidence uses `license-checker-rseidelsohn` and `pip-licenses`; advisory evidence uses `npm audit` and the accepted uv-export-to-pip-audit flow. Unknown or disallowed licenses fail. High and critical findings require documented triage before merge, with only explicit, time-bounded Central exceptions. Dependabot is limited to npm and GitHub Actions in Phase 0; automated uv updates are deferred. No Phase 0 SBOM is required.

### D0.7 - Controlled fixture policy: Accepted

Phase 0 uses synthetic/generated-first UTF-8 text fixtures in `.json`, `.csv`, `.txt`, or `.yaml` form. Root `fixtures/` is limited to 16 KiB per file and 64 KiB total, with mandatory metadata, provenance, licensing, expected properties, and privacy controls. P0-EP07 may add one synthetic harness fixture no larger than 1 KiB. Later validation datasets, production data, personal data, sensitive data, and ambiguous-license data remain excluded.

---

## 5. Acceptance Decision

Central accepts D0.4-D0.7 as independently validated. EP02-AC20 is satisfied, and P0-EP02 is `Complete`.

P0-EP03 may now be drafted as a separate bounded packet. This acceptance does not create or approve that packet and does not authorize installation, configuration, scaffolding, fixture creation, workflow changes, remote changes, or product implementation.

---

## 6. Validation Sources Preserved from the Returned Report

- [uv export command reference](https://docs.astral.sh/uv/reference/cli/#uv-export)
- [pip-audit project documentation](https://pypi.org/project/pip-audit/)
- [GitHub Actions environment files](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands)

These links preserve the sources cited by the independent validator. The validator's `Accept` result, not this Central record, supplies the independent-validation conclusion.
