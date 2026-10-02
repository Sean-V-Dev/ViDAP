# ViDAP P3-EP01 — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP01.md` version 0.1, approved 2026-10-01 |
| Worker report | `ViDAP_P3_EP01_Decision_Report.md`, Revision 3 |
| Worker report SHA-256 at reconciliation | `89AE5D4F10ADEE7DBF4B89B1A2F14A1C242699E095612761B3F282C1D769F15C` |
| Independent-validation verdict | Accept on Revision 3, after two `Revise` rounds (V1–V12, V13–V16); no unresolved Critical, High, or Medium finding |
| Central decision | D3.1–D3.4 accepted; F1 and F6 accepted as narrow Phase 2 extensions; F2 retained as a P3-EP03 gate; EP01-AC12 satisfied |
| Baseline HEAD | `678f1986cce18286c3b9ba9479ae0b919c8a3184` on `main` |
| Reconciliation date | 2026-10-01 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied the final independent `Accept` for Revision 3 of the
decision report. The validator rechecked every external source, reproduced
all 15 weighted totals, applied gates G1–G10 independently with matching
results, and found V1–V14 resolved with no hidden Phase 4/5 policy, UI
authority, schema change, dependency selection, or service growth.

The attestation for Revision 3 was a user-executed Windows run under the
`CONTRIBUTING.md` workaround, started after Revision 3 was saved. The
validator confirmed its timing and results: `check` passed through smoke
(mypy 21 files; web 10 passed; Python unit 125 passed, 1 skipped,
3 deselected; integration 3 passed); `coverage` passed (web 87.5% of
statements; Python 128 passed, 1 skipped, 88%); `deps:inventory` completed;
`license:check` passed for 431 packages; `deps:audit` found no npm (432) or
Python (57) vulnerabilities; `git diff --check` reported no errors, only
Git line-ending conversion warnings; locks unchanged; the report is the only
worker change, and nothing is staged. The one skip is the host-dependent
symlink test Phase 2 already accepted.

This independent result satisfies EP01-AC01–EP01-AC11. This packet's run
was the first use of the `CONTRIBUTING.md` non-Windows workaround; it
produced valid, independently confirmed evidence.

## 2. Central evidence check

Before writing this record, Central confirmed the current report hash in
the table above, both lock hashes
(`FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` and
`AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355`),
`HEAD` unchanged, and the working tree: Central-owned changes to the
Phase 3 plan and roadmap, the untracked packet, and the untracked report,
with nothing staged. Central did not rerun the attestation; the
user-executed run and the validator's confirmation supply that evidence.

The validated worker report is not edited after validation. Its remaining
wording issues (V17, V18, and the "No output" cell) are recorded and
resolved here instead.

## 3. Decisions accepted

| Decision | Central acceptance |
|---|---|
| D3.1 | Accepted. Five responsibility-level nodes in five regions (Dataset, Prepare Data, Train/Test Split, Model, Evaluate) over one controlled synthetic CSV with a declared schema; nothing learned in Prepare; scikit-learn as the sole candidate library; a generic Model responsibility with one fixed implementation; Split's output shared by Model and Evaluate, with Split → Evaluate skipping the MODEL region; `regularization` as the measurable UI parameter; the unencoded-category failure with deterministic input checks. All listed Phase 4/5 policies stay open, including task types, type inference, learned transforms, and leakage-aware ordering. |
| D3.2 | Accepted. Narrow synchronous `/api/slice/` JSON endpoints in the existing loopback FastAPI shell, with host, origin, content-type, size, and single-run limits; metrics only from owned-slot readback; the 2-second / unresponsive-editor escalation to Central. |
| D3.3 | Accepted. Backend-owned workflow files under `.vidap-local/workflows/`, written only by the canonical serializer and loaded through the Phase 1 reader and validation; base-digest conflict refusal covering workflow and sidecar together; backend-built change summaries; no silent overwrite. |
| D3.4 | Accepted. A versioned `vidap.workspace-view` sidecar owns region widths, region-relative node positions, and viewport; region membership is derived from node type in UI-owned presentation; the sidecar is the only position source; no Phase 1 change. |

## 4. Findings dispositioned

| Item | Central disposition |
|---|---|
| F1 | **Accepted** as a narrow D2.5/D2.8 extension: one additional fixed first-party output authority for slice metrics in the existing bounded slot, under the same ownership, atomic publication, readback, and indeterminate-publication rules. No other output authority is approved. |
| F6 | **Accepted** as a narrow D2.7 extension: first-party handlers may raise declared failure codes from a closed static list, each with fixed explanation and remedy text. Exception text stays withheld, the category stays `execution`, and any other exception still maps to `handler-failed`. |
| F2 | **Retained as a gate** in P3-EP03's dependency step: the bundled native libraries in every compiled wheel (NumPy, SciPy, scikit-learn), including SciPy's GCC-runtime-exception code, must pass D0.6 review before installation. If the review fails, D3.1 returns to Central. |
| F3 | P3-EP03 names `.vidap-local/workflows/` in the ignore rules and documentation. |
| F4, F5 | Carried to P3-EP02: region membership is fixed by type for the slice, and the prototype must include a region with several connected nodes. |
| V17 | The D3.1 bullet "Fits Phase 2 without policy changes" is read as "apart from F1 and F6". |
| V18 | The Section 10 handoff's "Revision 2" wording is superseded by this record. |
| V15 | **Central clarification for P3-EP03:** `POST run` runs the posted document, not the saved file; the response's semantic digest is the identity. Saving to a name that already exists requires the base digest of that file; a save with no base digest to an existing name is refused as a conflict, so a new workflow can never overwrite another by name. |
| V16 | **Central clarification for P3-EP03:** existing Phase 1 layout metadata in a loaded document is deliberately left as-is and is expected to become stale relative to the editor's sidecar. It is round-tripped unchanged, never displayed, and never treated as current. |
| Run-table cell | The Revision 3 `git diff --check` result had no errors, with Git line-ending conversion warnings only. |

## 5. Central decision and next boundary

Central accepts P3-EP01 v0.1. EP01-AC12 is satisfied and the packet is
`Complete`. This accepts decisions and two narrow Phase 2 extensions as
design boundaries only. It does not approve any dependency, fixture, source,
endpoint, persistence, UI, or schema change; those require their own
approved packets with full evidence.

P3-EP02 — design and interaction decisions (D3.5–D3.10), including the
design system and a throwaway interaction prototype — is now **ready to
draft**. P3-EP03 follows the Phase 3 plan and its own approval.
