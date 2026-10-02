# ViDAP P3-EP03A — Slice Dependency and License Review

| Field | Value |
|---|---|
| Status | Draft; awaiting explicit user approval |
| Packet version | 0.1 |
| Packet type | Research and evidence; documentation-only repository change |
| Parent phase plan | `ViDAP_Phase_3_Plan.md` version 1.1 |
| Parent roadmap | `ViDAP_Roadmap.md` version 4.6, P3 |
| Prerequisites | P3-EP01 and P3-EP02 complete |
| Workstream | WS3.3 — Backend slice (first of two packets) |
| Gate covered | F2 (P3-EP01 reconciliation): license and dependency review before scikit-learn is installed |
| Authorized worker output | `ViDAP_P3_EP03A_Dependency_Review.md` |
| Central follow-up | A decision record on any review-required findings, then `ViDAP_P3_EP03A_Validation_and_Reconciliation.md` (Central only) |
| Created | 2026-10-02 |
| Owner | Central |

---

## 1. Why WS3.3 is split

P3-EP03 as planned (the backend slice) needs a new runtime dependency.
D0.6 lets a worker gather license evidence but not accept a review-required
license; that takes a Central decision record, as Records 0003 and 0004 did
for Phase 0. So WS3.3 runs as two packets:

- **P3-EP03A (this packet):** evaluate the dependency and its license
  findings without changing the repository's locks.
- **P3-EP03B (later):** after Central accepts or rejects the findings,
  implement the backend slice, including the lock change and any catalog
  update the decision record allows.

Later packet numbers (EP04 editor core, EP05 run/results/trace, EP06
closeout) are unchanged.

## 2. Authorization Boundary

This draft authorizes nothing. If the user explicitly approves this exact
version, one bounded worker may research current primary sources; build a
candidate dependency set in **one disposable copy outside the repository and
OneDrive**; download the candidate wheels into a disposable location to
inspect their contents; have the user run the Windows dependency controls
against that copy; and create only the report named above.

Approval does not authorize any change to `python/pyproject.toml`,
`python/uv.lock`, `package.json`, `package-lock.json`, the dependency-control
scripts or catalogs, decision records, source, tests, fixtures, CI, or remote
state. It does not accept any license; only Central can.

## 3. Plain-English Packet Intent

### What this packet does

It checks whether scikit-learn and everything it pulls in can be added to
ViDAP under the project's existing license and security rules, and lists
exactly which findings need a Central decision.

### Why this comes first

Compiled Python packages often bundle native libraries with their own
licenses (for example, SciPy has bundled a GCC runtime under the GPL with a
runtime exception). ViDAP's license control fails closed on those. Finding
this out in the middle of building the slice would stall the build; checking
first gives Central a clean decision to make.

### What it enables

A Central decision record that either accepts the exact findings (so
P3-EP03B can add the lock and update the literal catalog) or rejects them
(so D3.1 returns to Central for a different library choice).

### How success is demonstrated

The report lists every package the candidate adds, with version, license as
the control reads it, bundled native components and their licenses,
maintenance and advisory evidence, Windows and Python 3.14 wheel
availability, and size; it shows the real Windows control results against
the disposable copy; and it proposes literal catalog entries for every
review-required finding.

## 4. Governing Inputs

The worker and validator must read:

1. The explicit user approval of this exact packet version.
2. `ViDAP_Overview.txt` OV §§9, 21, 23, 25, 30 (dependency and license
   expectations).
3. `ViDAP_Phase_3_Plan.md` v1.1 and the roadmap's P3 entry.
4. `ViDAP_P3_EP01_Validation_and_Reconciliation.md` (D3.1 and F2) and
   `ViDAP_P3_EP01_Decision_Report.md` (E1–E8 and the candidate set).
5. Accepted D0.6 (`ViDAP_P0_EP02_Validation_and_Reconciliation.md`),
   `docs/dependency-controls.md`, and decision records 0003 and 0004,
   including their revisit triggers and literal-catalog rules.
6. `scripts/dependency-controls.ps1` (how the license gate reads metadata),
   `python/pyproject.toml`, `python/uv.lock`, and `CONTRIBUTING.md`
   (including the non-Windows workaround).
7. This packet.

## 5. Required Evidence

### Candidate set

Start from the accepted D3.1 candidate: **scikit-learn only** as a direct
runtime dependency, at the newest release that publishes CPython 3.14
Windows x64 wheels, pinned exactly in the project style, plus whatever it
requires (expected: NumPy, SciPy, Narwhals, joblib, threadpoolctl). Do not
add pandas or any other library. If the newest release is unsuitable,
explain why and evaluate the newest suitable one.

### Per package (direct and transitive)

For every package the candidate adds to the lock:

1. Exact version, release date, and the role (runtime, transitive of which
   package).
2. The license value **as the existing control reads it** (first populated
   of SPDX expression, package metadata, classifier) and the actual license
   text in the installed or wheel files.
3. For compiled wheels (`cp314-win_amd64`): every bundled native component
   (for example `.libs` folders, DLLs, bundled license files such as
   `LICENSES_bundled.txt`), with its license as stated in the wheel.
4. Maintenance evidence: release cadence, last release, and project status
   from primary sources.
5. Advisory evidence from the real `deps:audit` run on the disposable copy.
6. Installed size.

### Whole-candidate questions

- The exact lock delta: added packages and any change to existing locked
  packages (none expected; any change is a finding).
- Whether the existing D0.6 policy, Records 0003/0004, and the control's
  fixed reading order classify each package as allowed, review-required, or
  prohibited, using the real control output.
- The SBOM revisit trigger: `docs/dependency-controls.md` says to revisit an
  SBOM before "a later ML dependency". Recommend whether an SBOM is needed
  now or can be deferred again, with reasons.
- Records 0003/0004 revisit triggers: confirm the candidate changes no
  package they cover.
- Notice obligations: what notices would have to be retained if ViDAP were
  ever distributed, noting that nothing is distributed today.

### Proposal for Central

For each review-required finding, a proposed literal catalog entry in the
Record 0003/0004 style: package name, exact version, exact gate value,
verified license text, role, and re-review trigger. Draft decision-record
wording may be included in the report as a proposal only. If any finding
is prohibited with no acceptable path, say so plainly and recommend that
D3.1 return to Central.

## 6. Disposable Copy Rules

1. The copy lives in one new folder under the system temporary directory,
   outside the repository and OneDrive, with its own npm and uv caches. It
   contains the current repository files needed for setup and the controls.
2. The candidate is added in the copy only (for example by editing the
   copy's `python/pyproject.toml` and relocking with uv). The repository's
   own `pyproject.toml` and `uv.lock` are never touched.
3. The Windows steps in the copy (locked setup, `deps:inventory`,
   `license:check`, `deps:audit`) are run by the user from a script the
   worker provides, following the `CONTRIBUTING.md` workaround. The script
   prints only summary lines and exit codes, records the copy's resolved
   path for the report as "a temporary folder" (never the user path), and
   removes the copy and its caches at the end after checking they are inside
   the temporary root.
4. `license:check` is expected to fail on the candidate if review-required
   findings exist; that failure is the evidence, not a blocker.
5. Wheels downloaded for inspection stay in the worker's own disposable
   workspace and are not added to the repository.

## 7. Stop Gates

Stop with a `Blocked` report if: no suitable release has CPython 3.14
Windows x64 wheels; the candidate would change an existing locked package;
a disposable copy cannot be created and removed safely; or the evidence
cannot be gathered from primary sources and the real controls. A prohibited
license finding is reported, not a reason to stop.

## 8. Exact Authorized Output

The worker may create or modify only `ViDAP_P3_EP03A_Dependency_Review.md`.
No other repository path may change. The report contains: approval,
versions, and baseline; the candidate set and lock delta; the per-package
table; bundled-component findings; the real control results from the
disposable copy; the SBOM and revisit-trigger answers; proposed catalog
entries and draft decision wording; findings for Central; and the final
attestation. It contains no user paths, credentials, copied lockfiles, or
full command logs.

## 9. Final Attestation

On the repository (unchanged apart from the report), in order:
`npm.cmd run check`, `npm.cmd run coverage`, `npm.cmd run deps:inventory`,
`npm.cmd run license:check`, `npm.cmd run deps:audit`, and
`git --no-pager diff --check`, then lock hashes and
`git --no-pager status --porcelain --untracked-files=all`. Use the
`CONTRIBUTING.md` workaround if needed, with a summary-line script that
avoids Git's pager. Also inspect the report directly for whitespace, final
newline, user paths, and secrets. Locks must equal the baseline.

## 10. Acceptance Criteria

| ID | Criterion |
|---|---|
| EP03A-AC01 | Approval, prerequisites, versions, baseline, and locks are recorded without sensitive data. |
| EP03A-AC02 | The candidate is scikit-learn only, exactly pinned, with every added package listed; any change to an existing locked package is reported as a finding. |
| EP03A-AC03 | Every added package has version, role, license as the control reads it, verified license text, maintenance, advisory, wheel-availability, and size evidence from primary sources or the real controls. |
| EP03A-AC04 | Bundled native components in every compiled Windows wheel are listed with their licenses. |
| EP03A-AC05 | The real Windows `license:check` and `deps:audit` results on the disposable copy are recorded, including expected failures. |
| EP03A-AC06 | The SBOM trigger and Records 0003/0004 revisit triggers are answered with reasons. |
| EP03A-AC07 | Every review-required finding has a proposed literal catalog entry; any prohibited finding is stated plainly with a D3.1 recommendation. |
| EP03A-AC08 | The disposable copy and caches were created and removed safely outside the repository and OneDrive. |
| EP03A-AC09 | Only the report changed; locks are unchanged; the final attestation passes. |
| EP03A-AC10 | A fresh independent validator returns `Accept`. |
| EP03A-AC11 | Central records a decision on every finding before P3-EP03B is drafted. |

## 11. Independent Validation

A fresh validator reads the inputs and the report; rechecks package
versions, licenses, and bundled components from primary sources (and, where
possible, by inspecting the same wheels); confirms the proposed catalog
entries are literal and complete; reproduces the repository attestation and
may repeat the disposable-copy control run with its own bounded copy and
cleanup; and returns `Accept`, `Revise`, or `Blocked` with a Central
recommendation. The validator may not edit files, accept licenses, or write
the decision record.

## 12. Handoff Prompts

### Worker

> Execute approved `ViDAP_P3_EP03A.md` v0.1. Evaluate scikit-learn (exact pin, CPython 3.14 Windows wheels) and every package it adds, using primary sources, wheel inspection in your own disposable workspace, and the real Windows dependency controls run by the user in one disposable copy outside the repository and OneDrive. Create only `ViDAP_P3_EP03A_Dependency_Review.md`. Do not change any lock, manifest, script, catalog, decision record, or source. Run the Section 9 attestation and stop for independent validation.

### Validator

> Act as the independent validator for approved `ViDAP_P3_EP03A.md` v0.1. Recheck the report's package, license, and bundled-component evidence, confirm the proposed catalog entries are literal and complete, reproduce the Section 9 attestation, and return `Accept`, `Revise`, or `Blocked` with a Central recommendation. Do not edit files, accept licenses, or write the decision record.

## 13. Next Action

Review this draft. On explicit approval of this exact version, a worker
executes it. After validation, Central writes a decision record on the
findings and the reconciliation; P3-EP03B (backend slice implementation) is
then drafted for separate approval.
