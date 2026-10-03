# ViDAP P3-EP04A — Independent Validation and Central Reconciliation

| Field | Value |
|---|---|
| Packet | `ViDAP_P3_EP04A.md` version 0.1, approved 2026-10-02 |
| Worker report | `ViDAP_P3_EP04A_Implementation_Report.md` (Revision 2) |
| Report SHA-256 at reconciliation | `3000AF55C4D1488D2D2E2299590636DF7BF958258D23FD6F48D4C67995DEB0B8` |
| Independent-validation verdict | `Accept` on Revision 2, after one `Revise` (R1–R5 blocking; N1–N6 lower severity); no unresolved finding |
| Central decision | P3-EP04A accepted; EP04A-AC14 satisfied. EP04A-AC12 counted as passed with the `deps:audit` triage in Section 4.1 |
| Baseline HEAD | `17652fc28eafa0b8e2b5be58c55df9ced0d7afff` on `main` |
| Reconciliation date | 2026-10-03 |
| Owner | Central |

---

## 1. Authority and independent result

The user supplied both verdicts from separate validation chats.

**Revision 1: `Revise`.** The validator drove the editor in headless Chrome
against the real backend.

- Five blocking defects:
  - R1: push-down ignored message height;
  - R2: rail entries overlapped;
  - R3: the page overflowed in a 1280×720 window;
  - R4: a field went stale after a focus-mode edit;
  - R5: Tab left the focus-mode panel.
- Six lower-severity items, N1–N6.

**Revision 2: `Accept`.** The validator re-checked in a headed Chrome window
at a real 1280×720 (125% display scale).

- R1–R5 and N1, N3, N4, and N6 are repaired.
- Nothing that previously passed has regressed:
  - layout never changes the workflow, including number spellings and Phase 1 layout metadata;
  - conflicts work with a real tab switch;
  - save and save-as digests;
  - gutters, keyboard navigation, move mode, and the leave-page prompt;
  - 24-pixel targets.
- `npm.cmd run check` exits 0 and `diff --check` is clean. Status, locks, listeners, and the workflow store are as reported.

The worker session (the local Claude Code session, acting as worker under
this Central role) also obtained two user walkthroughs on Windows. The first
found six defects, F1–F6, which were repaired before validation. The second
confirmed the Revision 2 repairs in a real browser (report Sections 9, 10,
and 17).

This satisfies EP04A-AC01–AC11 and AC13. AC12 is satisfied as recorded in
Section 4.1.

## 2. Central evidence check

Central confirmed the following before writing this record:

- **Repository state:** `HEAD` is unchanged. There are 42 status entries: the 41 baseline entries plus the report. Nothing is staged.
- **Lock files:** `package-lock.json` is `FB7119F6…82FA` and `python/uv.lock` is `8030A7C4…0A25`, unchanged since P3-EP03B.
- **Report:** its hash is in the table above.
- **Windows attestation:** report Section 12, a complete rerun after Revision 2:
  - `check` exit 0 (web 56 tests; Python unit 151 with 1 skip; integration 56 with 1 skip; build; smoke);
  - `coverage` exit 0 (web 84.7% of statements; Python 89%);
  - `deps:inventory` and `license:check` exit 0;
  - `deps:audit` exit 1 (Section 4.1);
  - `diff --check` clean;
  - no listeners.
- **Accepted editor source** (`apps/web/src/editor/`, excluding `test-data/`, whose hash is in its manifest):

| File | SHA-256 |
|---|---|
| `api.ts` | `83820FFF402A36E230C2906250FEF1CABCDF957405DF842A761B3A1076DF6420` |
| `api.test.ts` | `B8604547FD64190749F6688A8790A007F7499BC84C2EAE13602889358A7397C3` |
| `ConfirmDialog.tsx` | `A1A304FAC12F593FFCB78B2B5C5F64BA9CD6E5777ED68F19E4CA52A3C021F5D5` |
| `contract-source.test.ts` | `63DB7A4F1D642183B3791ED671AF92EFA76057F944041D19B62D428191D93E14` |
| `editor.css` | `D7C3BBF804FB3D65B3DF0DD8CFA3CE3D509FBECFAD2692F01D0B483E0C22F63F` |
| `editor.test.tsx` | `4985DA51CA603C009C9D5ABE581A6293A62529BDDF523497E088A574051E987A` |
| `Editor.tsx` | `490C0F980E771CA274B3C8682691B8C8552AD7A1D99A02332B8F7A70902E7C65` |
| `layout.ts` | `FE3B7FB531D7B34376928479210B62F7343062CB67AF9F02137912AD53DFE135` |
| `layout.test.ts` | `098BE36CCD2DC2989F7C2C784EA7086C12DECB4C72AB5DD96A3808D0FAD781A1` |
| `measure.ts` | `6C475DAF21688A474AB5BBF48DBE2A4FE01A7718AA44D2D5B809CAF07129A7F0` |
| `model.ts` | `FFBFEB6E604029AAA83EB3CD30961090832250AB9A1950B4A52F732DD46E538A` |
| `model.test.ts` | `53115529A43EDF447A06191F3769747BC5C0568519E598623947F4A9391C09CB` |
| `NodeView.tsx` | `4BC96B037CEEBF5E173D9AA876F113A25436167C90B4D654DA76D8925EC01BAB` |
| `presentation.ts` | `B68F70922D741297B89AE3D3E6C9B0C6F32210CAE133FF4090C15A7712AC7A1E` |
| `vite-env.d.ts` | `65996936FBB042915F7B74A200FCDDE7E410F32A669B1AB9597CFAA4B0FADDB5` |
| `Workspace.tsx` | `84BAAC27FD1F489A4DD5C292858DAC07EB084A44AE255E42D46F46BA328FE7D1` |

## 3. Accepted

- **The editor workspace replaces the Phase 0 placeholder.** It:
  - opens a saved slice workflow in its five regions;
  - edits settings through controls built only from `GET /api/slice/contracts`;
  - shows `validate` diagnostics on the node with the backend's exact text;
  - saves with both base digests and never overwrites silently.
- **Rendering approach (c), hand-built DOM and SVG.** Each region draws only its own wires, so nothing crosses a gutter. `@xyflow/react` stays locked and unused; removing it is a later dependency decision.
- **Layout is presentation-only (P3-AC08).** Positions are region-relative and live only in the sidecar. Moving never resizes a region. Push-down, region height, and rail stacking use measured heights. A layout-only save is byte-identical, including the number-spelling preservation in `api.ts` (Section 4, item 4).
- **Keyboard parity.**
  - Graph navigation with announcements;
  - move mode, which also ends when focus leaves the node;
  - Enter, double-click, or ▸ to expand;
  - focus mode with a contained Tab order;
  - gutters by keyboard and buttons;
  - a logical Tab order: Inputs, then the node, then Outputs.
- **Conflict handling.**
  - Compare runs on window focus.
  - The banner uses the backend's summary.
  - Reload always confirms, and its wording follows whether anything will be discarded.
  - Save-as uses `null` bases.
- **Accessibility lint (5.6): declined.** `eslint-plugin-jsx-a11y-x` 0.2.0 depends on `axe-core` (MPL-2.0, review-required under D0.6). The evidence goes to the decision record 0001 follow-up. Nothing was installed.
- **`DESIGN.md` edits:** the status is Accepted; the N2 dim-fill wording; the dimmed-border 3:1 question is deferred to P3-EP05.
- **Recorded test data** (`test-data/recorded.ts`, `E9EE4660…5B42`) and its D0.7 manifest. `centralReviewer` stays "pending" until the commit that records this acceptance.
- **Test isolation.** `editor.test.tsx` registers Testing Library cleanup explicitly, because the repository's Vitest config does not enable globals. The earlier cloud runs had masked this.

## 4. Observations dispositioned

### 4.1 `deps:audit`: time-bounded acceptance

| Field | Record |
|---|---|
| Advisory | [GHSA-ch52-4w7c-c8xp](https://github.com/advisories/GHSA-ch52-4w7c-c8xp), `http-cache-semantics` 4.2.0 (high). It accounts for all 11 npm findings |
| Path | `license-checker-rseidelsohn@5.0.1` › `@npmcli/arborist` › `npm-registry-fetch` › `make-fetch-happen` › `http-cache-semantics` |
| Directness and role | Transitive, development-only: the `license:check` tool. It is not in the web bundle or the Python runtime |
| Reachability and exposure | The flaw concerns `max-stale` handling in a shared HTTP cache, which could disclose cross-user cached responses. `license:check` reads locally installed package metadata on one user's machine. There is no shared cache and no second user, so Central judges it not reachable in ViDAP's use |
| Fix | None published (4.2.0 is the latest). npm's suggestion, a semver-major change to the license checker, would rewrite the lock and is not taken |
| Cause | Published after P3-EP03C's clean audit on the identical lock; not caused by this packet |
| Decision | **Accepted until recheck.** Later attestations report `deps:audit` exit 1 as this known finding, provided the npm findings are exactly this advisory and its 11 dependents, with Python clean. Any other finding is new and must be triaged |
| Recheck | By **2026-11-02** or at P3-EP06 closeout, whichever comes first, or as soon as a fixed `http-cache-semantics` is published. The fix then goes through a reviewed lock update in its own packet |
| Release | Must be resolved, or re-decided, before any distribution artifact |

### 4.2 Other observations

| Item | Central disposition |
|---|---|
| N2: an expanded Model or Split covers its own Outputs entry, so the mouse cannot reach its hover card (the keyboard can) | **Carried to P3-EP04B**, which decides G-F3 (expanding toward open space) alongside node placement. Report deviation 2 is corrected |
| N5: summary lines wrap to two or three lines; `DESIGN.md` §10 says "one summary line" | **Carried to P3-EP04B's `DESIGN.md` amendment.** Central's proposed reading: one line of content that may wrap and is never truncated |
| Re-validation: a tall compact node (a Dataset with a wrapped description) pushes the node below by the extra height even when the two would not overlap | **Carried to P3-EP04B:** push only by the overlap actually needed (DESIGN §12, "did ViDAP move a node on its own"). Low severity; nothing is hidden |
| Wires run beneath an overlapping node (user, Revision 2 walk) | **Carried to P3-EP04B** (connections and connection feedback) |
| Number spelling: the backend digest distinguishes `1.0` from `1`; the editor preserves the loaded spelling | **Accepted** as the editor-side fix. **Carried to P3-EP05** as a backend note: any other client must preserve spellings, or the channel must canonicalize number kinds |
| N1 channel note: names containing `/` or `..` get a non-standard 404 body from the router | **Carried to P3-EP05** (channel work). The editor now words such answers correctly |
| The capture scripts were temporary and are not tracked; `CONTRIBUTING.md` points to the report for regeneration | **Carried to P3-EP04B**, which will need new recorded responses and should authorize a tracked capture tool |
| UNASSIGNED is reachable only in unit tests (the backend refuses unknown types) | Accepted |
| The first `npm.cmd run launch` missed its 15-second readiness wait on a cold start | **Carried to P3-EP06** as an observation |
| Kicker shows the region label; Dataset omits row and column counts; Split's title wraps; a 16 px right margin after moving | Accepted as reported deviations |

**Carried unchanged from earlier records:**

- P3-EP04B: adding and removing nodes, with its `DESIGN.md` amendment; keyboard connecting (G-F2).
- P3-EP05: the 3:1 dimmed-border decision; run-record retention.
- P3-EP06: the intermittent Phase 2 test; the Windows symlink check; a re-walk at 1280×720.
- The next Phase 3 plan amendment lists decision record 0002 as an input (G-F6).

## 5. Central decision and next boundary

Central accepts P3-EP04A v0.1, and EP04A-AC14 is satisfied. The browser is
now the ViDAP editor workspace. It opens, edits, validates, and saves slice
workflows through the accepted channel, and layout never changes a workflow.

P3-EP04B (graph authoring) is now ready to draft. It needs its own approval
before any work. It must carry:

- the accepted EP04A editor and these channel contracts;
- the `DESIGN.md` amendment for adding and removing nodes, together with the N5 reading;
- connecting by pointer and keyboard (G-F2), connection feedback, and the wire-under-node note;
- G-F3 and N2;
- the push-down overlap refinement;
- a tracked capture tool for recorded responses;
- the `deps:audit` record in Section 4.1.

Beyond this record and the status updates to the packet, plan, and roadmap,
nothing here changes a source file, lock, or remote state. Nothing was
staged, committed, or pushed.
