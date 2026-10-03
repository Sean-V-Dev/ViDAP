# ViDAP Design System

| Field | Value |
|---|---|
| Status | **Accepted** by Central on 2026-10-02 in `ViDAP_P3_EP02_Validation_and_Reconciliation.md`; the authoritative ViDAP design system |
| Version | 0.2 |
| Governing decisions | Decision record 0002; Phase 3 plan v1.1 (D3.5–D3.10); `UX refinement.txt` |
| Evidence | `docs/design/p3-ep02-prototype/` (throwaway prototype and state screenshots) |
| Applies to | Every user-facing ViDAP surface, starting with the Phase 3 editor |

ViDAP is an analytical workspace. The graph is the main object on screen.
Every visual choice here exists to help a person see the shape of an
experiment at a glance, then investigate, then verify. Decoration that does
not serve that path is left out.

## 1. Principles

1. **Glance, investigate, verify.** The normal canvas answers: where the data
   entered, what happened to it, which approach is used, where branches are,
   and what the current outcome is (UX §24). Detail is one action away, and
   technical detail one more.
2. **Structure over wiring.** Show responsibilities, not function calls.
   Long-distance dependencies end at region boundaries and are revealed on
   demand (UX §§1, 4, 5).
3. **The user owns the layout.** ViDAP never rearranges nodes on its own.
   Layout help is an explicit action (UX §§3, 6, 20). The one exception is
   temporary: when a node grows (expanded, or showing a message), nodes
   directly below it in the same region slide down so nothing is covered,
   and slide back when it shrinks. Stored positions never change.
4. **Never magical.** Every shown value traces to a canonical workflow edge,
   a backend contract, or a recorded result. Nothing visual is a second
   source of truth (OV §22A.5; A3).
5. **Quiet by default.** Neutral surfaces; color is reserved for meaning
   (selection, status, port type). One accent color.

## 2. Tokens

Tokens are defined once as CSS custom properties and consumed everywhere.
Contrast ratios below are computed against white (`--surface`) and the
canvas, per WCAG 2.2.

### Color

| Token | Value | Use | Contrast |
|---|---|---|---|
| `--canvas` | `#F4F5F7` | App background behind regions | — |
| `--surface` | `#FFFFFF` | Nodes, panels, rail values | — |
| `--region` | `#FAFBFC` | Region background | — |
| `--text` | `#1B1F24` | Primary text | 16.6:1 |
| `--text-2` | `#4A5361` | Secondary text | 7.8:1 |
| `--muted` | `#5F6977` | Labels, hints | 5.6:1 |
| `--border` | `#D5DAE1` | Decorative separators only | — |
| `--border-strong` | `#7A8494` | Control and node borders, wires, gutter grip | 3.8:1 (3.5:1 on canvas) |
| `--accent` | `#2457C5` | Selection, focus, primary action, trace | 6.5:1 |
| `--ok` | `#1E7A46` | Completed | 5.4:1 |
| `--err` | `#B42318` | Runtime failure | 6.6:1 |
| `--warn` | `#8A5A00` | Validation problems, conflicts, prototype/preview labels | 5.9:1 |
| `--t-table` / `--t-split` / `--t-model` / `--t-metrics` | `#0E6A87` / `#6E45B8` / `#A84B0C` / `#3D6B12` | Port-type glyphs | 5.7–6.6:1 |
| `--dim-fill` / `--dim-border` | `#EEF0F3` / `#C9CFD7` | De-emphasized items during trace | text keeps ≥ 4.68:1 (primary text 14.5:1); the dimmed border is about 1.5:1, see Section 9 |

Tinted backgrounds (`--accent-bg #E8EEFB`, `--ok-bg #E7F4EC`, `--err-bg
#FDECEA`, `--warn-bg #FFF4DB`) keep their foreground at 4.7:1 or better.
Phase 3 ships a light theme only. Tokens are named by role so a dark theme
can be added later without renaming; that is a revisit item, not a Phase 3
requirement.

### Typography

- Family: the platform UI font (`Segoe UI` on Windows, then `system-ui`).
  Technical detail uses `Cascadia Mono`/`Consolas`. No web fonts.
- Scale: 10 (kickers and rail labels, uppercase, letter-spaced), 11 (meta,
  summaries), 12 (body in panels), 13 (default and node titles), 14 (app
  title). Nothing below 10 at the default zoom.
- Numbers use tabular figures so metrics and parameters line up.

### Spacing, size, zoom, and window

- 4-pixel grid: 4, 8, 12, 16, 24.
- Radius 6 for nodes, panels, and controls; 4 for small controls; pill
  shapes only for status chips.
- Every pointer target is at least 24×24 CSS pixels at the default zoom
  (WCAG 2.5.8). Gutters are 24 wide (the visible grip is 4×56).
- Compact node: 168 wide, content-driven height. Expanded node: 290 wide,
  body capped (about 230 tall in place, 60% of the viewport in focus mode)
  with internal scrolling.
- Boundary rails: 96 wide. Rail text wraps; it is never truncated.
- **Default zoom is 100%**, where every size and text minimum holds. 85% and
  70% are an explicit overview the user chooses; they may fall below the
  minimums, so nothing may require them. The zoom and other top-bar
  controls are never scaled.
- **Minimum supported window: 1280×720.** The top bar wraps to a second line
  rather than overflowing; the workspace scrolls horizontally; regions never
  reflow into a different order.

## 3. Layout and information hierarchy

- **Top bar:** product name, view and zoom controls, the primary result, and
  Run. The primary result stays in the top bar so a change and its
  consequence stay connected (UX §15).
- **Banners** sit under the top bar for workspace-level states: trace,
  connecting, save conflict, busy. They never cover the canvas.
- **Workspace:** vertical regions left to right in responsibility order. The
  slice uses DATA, PREPARE, VALIDATE / SPLIT, MODEL, EVALUATE / COMPARE
  (UX §2). Regions are responsibility zones, not required stages.
- **UNASSIGNED region:** a node whose type has no region appears in an extra
  region at the far right, shown only when it has nodes, with an amber dashed
  border and the header "UNASSIGNED · type has no region".
- No permanent side inspector (UX §10).

**Information hierarchy (what is read first):**

1. Region names (the shape of the experiment).
2. Node titles and their status chips.
3. The primary result in the top bar.
4. Implementation lines and one-line summaries.
5. Rail values and wires.
6. Everything else (hints, technical detail) only on expansion or request.

Weight and size follow that order: bold 13 for titles, uppercase 10 for
region and kicker labels, regular 11 for summaries, muted 10 for rail
subtitles. Color emphasis is reserved for status and selection, so it never
competes with titles.

## 4. Regions, gutters, boundary interfaces, and connections

- Each region has a header (name and node count), an **Inputs** rail on its
  left edge, an **Outputs** rail on its right edge, and its own nodes.
- **Within a region**, connections are ordinary short wires.
- **Across regions**, a wire runs from the producer to its region's Outputs
  rail and stops. The value continues from the matching entry on each
  consuming region's Inputs rail. **Nothing crosses a gutter** (UX §4.5),
  including invalid and in-progress connections.
- **Naming.** A boundary value is shown as `Name.port` with its type glyph.
  `Name` is the node's label when the workflow gives it one, otherwise the
  type's display label, followed by 1, 2, … in stable node-ID order when
  several nodes share a type (for example `Model 1.model`, `Model 2.model`).
  Node titles use the same name. Display names are never used for matching:
  values are matched by the canonical node ID and port key (UX §4.4).
- **One Outputs entry per value**, level with the port that produces it,
  saying how many nodes use it ("used by 4 nodes").
- **One Inputs entry per consuming port**, level with the port it feeds,
  saying where it comes from ("from SPLIT"). If two nodes in a region use
  the same value, each gets its own entry, the way two scripts each import
  the same module. This deliberately refines the UX §4.2 sketch, where one
  entry fans out, because fan-out made local wires cross (walkthrough W2).
  Overlapping entries stack.
- **Hover or keyboard focus** on a boundary value shows a card listing the
  producer and every consumer as `REGION / node (port)` (UX §5).
- **Trace (X-ray):** Enter or click on a boundary value highlights the
  producer, consumers, and their rail entries with an accent outline, gives
  unrelated items the dim fill (text stays readable), and draws the real
  connections as dashed lines across regions. A banner names what is being
  traced. Escape or the banner button exits. Trace never changes the
  workflow.
- **Gutters** resize the region on their left by pointer drag, by arrow keys
  (Shift for larger steps), or by − and + buttons (WCAG 2.5.7). A region's
  width is between the narrowest width that still fits its nodes and 900
  pixels. ViDAP never moves nodes to make room. Node positions are relative
  to their region, so resizing never displaces nodes inside other regions.

### Connection feedback

- **Starting a connection** from an output port shows a "Connecting" banner,
  marks the source port, outlines every compatible input port in accent,
  and dims incompatible ports with a ✕. Compatibility in this early feedback
  comes from the port types in the backend contracts; the backend's
  validation result is still the authority.
- **Dropping on an incompatible port** does not create a connection; the
  banner says why (for example "Model expects split, not metrics").
- **A connection that exists but is invalid** (for example loaded from a
  file, or found invalid by backend validation) is shown amber: an amber
  Outputs entry on the producer's rail, an amber Inputs entry ("⚠ not allowed
  here") on the consumer's rail, short amber dashed wires to each port, and
  the "Fix before running" message on the consumer. It still never crosses a
  gutter.
- **A connection to an earlier region** (right to left) is shown the same
  way as any cross-region value: it leaves the producer's Outputs rail and
  arrives on the consumer's Inputs rail. Whether it is valid is decided by
  workflow validation (for example cycles), not by region order.

### The three complexity forms (UX §7)

Long-distance wires are handled by boundaries; local tangles by explicit
align/tidy, reroute points, and highlighting; conceptual overload by
composite nodes and progressive disclosure.

## 5. Nodes

- **Compact:** responsibility kicker (uppercase), title, implementation line,
  a one-line summary, and a status chip. Ports sit on the edges: inputs
  left, outputs right, with type glyphs. Slice summaries:

| Node | Implementation line | Summary line |
|---|---|---|
| Dataset | "Controlled CSV · <fixture name>" | row count and declared column count |
| Prepare Data | "Fill missing · Encode categories" | missing-value fill |
| Train/Test Split | "Single holdout" | test fraction and seed |
| Model | the fixed implementation, for example "Logistic regression" | regularization |
| Evaluate | "Accuracy on test rows" | the recorded accuracy after a run, "—" before |

- **Expanded (in place):** Enter, double-click, or the ▸ button. Shows
  parameters, the steps inside a composite node, and an Advanced section.
  The body is bounded and scrolls internally; scrolling it never pans or
  zooms the canvas. Nodes directly below it in the same region slide down
  while it is expanded and return when it collapses (walkthrough W4). It can
  still overlap a neighboring rail or region sideways; expanding toward open
  space is a P3-EP04 option.
- **Focus mode (escape hatch):** F or the ⤢ button lifts the node into a
  centered, larger panel over a dimmed canvas. Its wires are hidden while
  lifted. Escape or clicking the dim area returns it.
- **Input separation (UX §9.3):** drag a node only by its header; edit only
  inside the body; scroll the body with the wheel; pan with the workspace
  scrollbars; zoom with the zoom control. No gesture does two of these.
- **Controls come from the existing D1.4 contracts, with no new contract
  fields:**
  - `boolean` → checkbox.
  - Any kind with `allowedValues` → a select listing those values.
  - `integer` → numeric field, step 1.
  - `number` → numeric field with no step restriction.
  - `minimum`/`maximum` → the field's bounds; values outside them are still
    flagged by backend validation.
  - `nullable` → an extra "None" choice.
  - Values the slice fixes (for example the solver) → read-only text marked
    "(fixed)".
  - Labels and hints come from the contract's display `label` and
    `description`.
- **Generic Model responsibility:** the kicker says MODEL; the
  implementation line names the fixed implementation (UX §11).
- **Keyboard (walkthrough W5):** Tab reaches nodes, rail values, gutters,
  and controls. On a node, Right arrow follows its output to the first
  downstream node (nearest region first) and announces how many there are;
  Shift+Right steps to the next downstream node of the same source. Left
  arrow goes back to the node that feeds it; Up and Down move to the nearest
  node above or below in the same region. Enter expands; F opens focus mode;
  M enters move mode, where arrow keys move the node (Shift for larger
  steps) and Enter or Escape finishes. Ports have accessible names ("Input
  port split, type split").

## 6. States and status language

| State | Shown as |
|---|---|
| Not run | Grey chip "– Not run" |
| Running | Accent chip "◌ Running"; Run button disabled and labeled "Running…" |
| Completed | Green chip "✓ Completed" |
| Failed | Red chip "✕ Failed", red node outline, and an error message on the node |
| Blocked | Grey dashed chip "⊘ Blocked" (depends on a failed node; tooltip explains) |
| Unrelated | Grey dotted chip "○ Unrelated" (not started; does not depend on the failure; tooltip explains) |
| Validation problem | Amber outline and an amber "Fix before running" message; Run disabled |
| Selected / focused | Accent outline; keyboard focus always visible |

Every status has an icon and words as well as color (WCAG 1.4.1).

- **Runtime errors (D2.7, F6)** show on the affected node: a small uppercase
  "Run failed" label, then the cause as the bold headline in body-text color,
  then a one-line remedy, then collapsed "Technical details". The chip
  already says Failed, so the headline is the cause, not a repeat of the
  status (walkthrough W3). **All of this text is the fixed text for the
  failure code** (for example "A text column reached the model without
  encoding"); it never includes values from the data or the exception.
- **Validation diagnostics (Phase 1)** use the same structure with an amber
  "Fix before running" label, so they never look like a failed run.
- **Save conflict:** amber banner with the backend's change summary and two
  actions, Reload from disk and Save under a new name (D3.3).
- **Busy:** accent banner explaining that one run happens at a time.
- **Empty canvas:** regions stay visible with one short hint in DATA.
- Anything not from the backend (prototype, future previews) is labeled in
  amber, for example "illustrative" or "PREVIEW" (UX §16).

## 7. Controls, panels, and dialogs

- One primary button per view (Run). Secondary buttons are outlined.
- Segmented controls for mutually exclusive views (Regions / Free canvas,
  zoom).
- **Control states:** default (outlined); hover (light region fill);
  pressed or selected (accent tint and accent text); keyboard focus (2-pixel
  accent ring, 2-pixel offset); disabled (60% opacity, not-allowed cursor,
  and a reason nearby, for example the busy banner). States never rely on
  color alone.
- Prefer in-place disclosure and banners to dialogs. Use a dialog only for a
  destructive confirmation; it traps focus and returns it on close.
- Tooltips and hover cards also open on keyboard focus and never hold the
  only copy of important information.

## 8. Charts (forward rule)

Phase 3 shows metrics as numbers. When charts arrive (Phases 4–6), they use
these tokens, label axes and units, choose aggregation, faceting, or top-N
before an unreadable chart, mark preview data, and keep the
glance-investigate-verify path. Chart specifics are decided by their owning
phase.

## 9. Accessibility baseline (D3.9)

Target: WCAG 2.2 Level AA for the editor, at the default zoom.

- Text contrast at least 4.5:1; component and graphic boundaries at least
  3:1 (1.4.3, 1.4.11). The token table meets both. Dimmed items during trace
  keep text at 4.68:1 or better; their dimmed border (about 1.5:1) is
  de-emphasis, and P3-EP05 either accepts that or keeps a 3:1 border, and
  records which.
- Every action is keyboard-operable (2.1.1): select, navigate between
  connected nodes, move (move mode), expand, focus mode, trace and exit,
  gutter resize, run, view and zoom. Connecting by keyboard is designed in
  P3-EP04, because the graph library's documented keyboard support covers
  focus, selection, and moving, not connecting.
- Focus is always visible and never fully hidden (2.4.7, 2.4.11).
- Every drag has a non-drag alternative (2.5.7). Targets are at least 24×24
  (2.5.8).
- Color is never the only cue (1.4.1).
- Nodes, ports, boundary values, and gutters have accessible names; gutters
  use the separator role with current width; status changes, navigation
  counts, and trace descriptions are announced through a polite live region.
- Motion is minimal and disabled under reduced-motion preferences.

## 10. Noise reduction and progressive disclosure

- Show at most one summary line per compact node.
- Hide port labels on compact nodes; types show as glyphs, names on hover,
  in the boundary card, and to assistive technology.
- Collapse technical detail by default; never remove it.
- De-emphasize, don't hide, during trace, so orientation is kept.

## 11. Design and UX support mechanism

This file is the single authority for visual decisions. It is kept current
by the review loop below rather than by a third-party design generator or a
component catalog.

1. Each packet that changes UI names the `DESIGN.md` sections it applies and
   captures the representative states it touches.
2. Before handoff, the worker checks those states against the checklist in
   Section 12 and the token table.
3. An independent validator reviews the same states against this file
   (decision record 0002).
4. A needed change to this file is proposed in the packet and accepted by
   Central; code may not silently diverge.

Optional aids may help generate options, but their output is a draft and
never overrides this file. A component catalog (for example Storybook) is a
reasonable later addition once the editor has enough components to justify
it; it would go through the dependency controls first.

## 12. Review checklist

- Can a viewer answer the UX §24 questions from the normal canvas?
- Does every cross-region dependency, valid or not, end at rails and trace
  on demand?
- Is every value shown from a contract or a recorded result, and is every
  error message the fixed text for its code?
- Do the states match Section 6 wording, icons, and colors?
- Are contrast, focus, keyboard, target-size, and non-drag rules met at the
  default zoom and at 1280×720?
- Did any gesture do two things, or did ViDAP move a node on its own (other
  than the temporary push-down)?
- Is anything not from the backend labeled as such?
