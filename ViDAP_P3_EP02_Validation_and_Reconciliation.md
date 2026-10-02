# ViDAP P3-EP02 — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP02.md` version 0.1, approved 2026-10-01 |
| Worker outputs | `ViDAP_P3_EP02_Decision_Report.md` (Revision 2), `DESIGN.md` v0.2, `docs/design/p3-ep02-prototype/` (prototype and 16 screenshots) |
| Output SHA-256 at reconciliation | Report `4316AE9181A1C559366740D2BF9DFC49D3F063B60BF7C5075787F2570F46B970`; `DESIGN.md` `537A7E87551245E43722FDCAC47ADE94FA6BB6385252705A84D947615558ABEA`; prototype `84E5A2DB20E91DE2FDBBF8DB00FEE7FF00111613BF01EE6286DD8502F2A711C9` |
| Independent-validation verdict | Accept on Revision 2, after one `Revise` (V1–V6 Medium, L1–L9 Low); no unresolved Critical, High, or Medium finding |
| Central decision | D3.5–D3.10 and `DESIGN.md` v0.2 accepted; G-F1 accepted; G-F8 declined; EP02-AC14 satisfied |
| Baseline HEAD | `678f1986cce18286c3b9ba9479ae0b919c8a3184` on `main` |
| Reconciliation date | 2026-10-02 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied the final independent `Accept` for Revision 2. The
validator checked every V1–V6 and L1–L9 fix in the files and the prototype,
not only in the report; measured the prototype at 1280 and 1920 pixels wide
at the 100% default zoom (no target under 24×24, no text under 10 pixels, no
truncated rail text, no top-bar overflow); confirmed the new sources (S8,
S9, S11, including `eslint-plugin-jsx-a11y-x` 0.2.0, MIT, ESLint `^9 || ^10`,
last commit 2026-09-30); reproduced all weighted totals; applied G1–G8; and
confirmed hygiene, the 16-screenshot limit, and that only the Section 9
paths changed. The user's walkthrough on 2026-10-01 is part of the evidence;
its findings W1–W5 were applied, and the re-walk of the revision is carried
to P3-EP06.

This satisfies EP02-AC01–EP02-AC13.

## 2. Attestation and the report's open sections (N1)

The validated report's Sections 10–11 still read "PENDING", and Section 10
says the validator's earlier run "was not returned before its verdict". The
validator did receive and confirm that run. Following the P3-EP01 precedent,
the validated report is not edited; this record supersedes both points.

The final attestation is the user's Windows run on the morning of
2026-10-02, after the outputs were last written on 2026-10-01 between 21:23
and 21:25, so it covers the final versions. The validator confirmed it:

| Step | Result |
|---|---|
| `npm.cmd run check` | Exit 0 (mypy 21 files; web 10 passed; Python unit 125 passed, 1 skipped; integration 3 passed) |
| `npm.cmd run coverage` | Exit 0 (web 87.5% of statements; Python 88%) |
| `npm.cmd run deps:inventory` | Exit 0 |
| `npm.cmd run license:check` | Exit 0 (431 packages) |
| `npm.cmd run deps:audit` | Exit 0 (no vulnerabilities in npm's 432 or Python's 57) |
| `git --no-pager diff --check` | Exit 0, no output |

Both lock hashes are unchanged, nothing is staged, and the untracked worker
files are exactly the Section 9 set. The one skip is the host-dependent
symlink test Phase 2 already accepted.

Central confirmed before writing this record: the hashes in the table above,
both locks (`FB7119F6…82FA`, `AC31501B…4355`), `HEAD` unchanged, and the
working tree (Central-owned plan and roadmap changes, the untracked P3
packets and records, and the P3-EP02 worker outputs). Central did not rerun
the attestation.

## 3. Decisions accepted

| Decision | Central acceptance |
|---|---|
| D3.5 | Vertical regions with resizable gutters; Inputs and Outputs rails; `Name.port` values matched by canonical node ID and port key; one Outputs entry per value and one Inputs entry per consuming port, level with their ports; hover card; trace that de-emphasizes without losing text contrast; connection feedback; invalid and right-to-left connections shown on rails; nothing crosses a gutter. |
| D3.6 | Compact nodes that expand in place with bounded internal scroll and temporary push-down; optional focus mode; no permanent inspector; controls derived only from existing D1.4 contract fields; graph navigation by arrow keys and a separate move mode. |
| D3.7 | Run control and primary result in the top bar; per-node status with icon and words; fixed-text runtime errors per F6 code; amber validation problems; conflict and busy banners. |
| D3.8 | Project-owned tokens and hand-built components on the existing stack; `DESIGN.md` as the single design authority with a review loop and independent review. |
| D3.9 | WCAG 2.2 Level AA at the default zoom, keyboard parity for every canvas action, and the compensating checks listed in the report. |
| D3.10 | The representative state set and the layered validation method, with the Section 8 walkthrough script reused in P3-EP06. |
| `DESIGN.md` v0.2 | Accepted as the authoritative ViDAP design system. Its header still says "Proposed"; this record is the acceptance. The first packet that edits `DESIGN.md` (expected P3-EP04) updates its status line and applies the N2 wording fix below. |

## 4. Findings dispositioned

| Item | Central disposition |
|---|---|
| G-F1 | **Accepted.** Decision record 0001's JSX accessibility-lint deferral is extended. P3-EP04 evaluates `eslint-plugin-jsx-a11y-x` with registry-verified peer, license, and maintenance evidence, noting it is still a 0.x release (N5), and either adopts it through D0.6 or records why not. |
| G-F2, G-F3, G-F7 | Carried to P3-EP04: keyboard connecting; expanding toward open space; turning off the graph library's arrow-key node moving in favor of graph navigation and move mode. |
| G-F4, G-F9, N4 | Carried to P3-EP04 and P3-EP06: at 1280×720 and 100% only about 2.5 regions fit. P3-EP06 runs the at-a-glance test on the real slice at that window size; overview zooms stay optional. |
| G-F5 | Dependency steps recheck versions, peers, and licenses in the registry before any install. |
| G-F6 | Noted for the next Phase 3 plan amendment: add decision record 0002 to the governing inputs. |
| G-F8 | **Declined for now.** F6 failure text stays fixed; no data values in error messages. |
| N2 | `DESIGN.md` overstates dimmed-text contrast: the actual minimum is 4.68:1 (muted 4.87, green status 4.68), which still passes AA. The wording is corrected when `DESIGN.md` is next edited. Dimmed node borders are about 1.5:1; P3-EP05 either accepts that as de-emphasis or keeps a 3:1 border, and records which. |
| N3 | P3-EP03/EP04: the Dataset node's row count comes from the contract description or a recorded result, not UI logic; "(fixed)" values come from the contract, never hard-coded in the UI. |
| N5 | See G-F1. |

## 5. Design refinements to revisit

These were raised during the walkthrough or in discussion with the user and
are recorded so they are not lost. None is scheduled yet; Central may plan
a design-refinement pass once the editor runs, for example before P3-EP06.

- A dark theme (tokens are already named by role).
- Typography beyond the platform UI font.
- Follow-ups on W1–W5 after the real-editor walkthrough.
- Expanded nodes overlapping a neighboring rail sideways (G-F3).
- Overview zooms below the size minimums (G-F9) and a possible mini-map or
  fit-to-screen view.
- The user's hypothesis that a vision-capable model reads regions more
  easily than wires, for any later agent work (OV §17).
- **Results dock (agreed with the user 2026-10-02):** the empty band below
  the regions is reserved for a future full-width, resizable, collapsible
  results dock that keeps results in view while editing (UX §15). The live
  results panel itself is Phase 5 work; automatic re-run on change with
  PREVIEW labeling (UX §16) and progress or heartbeat for long runs (which
  needs Phase 8 cancellation and lifecycle work) come later. Until then,
  P3-EP04 and P3-EP05 must not place other permanent UI in that band; the
  Phase 3 primary result stays in the top bar.

## 6. Central decision and next boundary

Central accepts P3-EP02 v0.1. EP02-AC14 is satisfied and the packet is
`Complete`. The design system and interaction decisions are now
authoritative for Phase 3 UI packets. This approves no dependency, product
code, endpoint, or schema change.

P3-EP03 — the backend slice (D3.1–D3.3, F1, F6, with F2 as a dependency
gate) — is now **ready to draft**. P3-EP04 and P3-EP05 follow and must apply
`DESIGN.md` and the carried items above.
