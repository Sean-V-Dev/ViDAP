# Decision Record: Visual Design and UX Quality Amendment

| Field | Value |
|---|---|
| ID | 0002 |
| Status | Accepted |
| Date | 2026-09-18 |
| Owners | Central; future user-facing frontend phase owners |
| Governing requirements | Current user direction; `ViDAP_Overview.txt`; `ViDAP_Phased_Plan_Spine.md`; `ViDAP_Roadmap.md` |

## Context

ViDAP must make complex data-science workflows and results understandable at a glance without sacrificing technical depth. Functional rendering alone does not ensure hierarchy, readability, coherent interaction, accessibility, or useful presentation at realistic information density. Without an explicit requirement, later implementation agents could default to generic UI patterns rather than an intentional analytical workspace.

## Decision

Visual design and UX quality are continuing product-quality requirements for every user-facing capability. Functional correctness alone is not sufficient for acceptance of user-facing work.

Before substantial production UI is implemented, the owning Phase 3 plan must create and approve a concise ViDAP visual design system or equivalent artifact, tentatively `DESIGN.md`. It must cover typography, spacing/density, layout, color/accent use, node/state language, controls/panels/dialogs, chart principles, information hierarchy, accessibility, interaction states, proportionate responsive/minimum-window expectations, noise reduction, and progressive disclosure.

The Phase 3 plan must also evaluate and select a maintained frontend-design/UX skill, plugin, review workflow, or equivalent instruction package that is suitable at that time. No present third-party tool is selected or installed by this decision.

## Consequences and tradeoffs

The graph remains the visually dominant workspace. Nodes, results, comparisons, warnings, errors, and metrics must communicate role and state without decorative clutter. Technical detail is progressively disclosed; key results support a glance-to-investigate-to-verify path. Charts are chosen for readability at the represented density, with aggregation, density, sampling, faceting, or top-N alternatives considered when a chart would otherwise become unreadable.

This is not a demand for decorative or infographic-like UI. It requires clear, intentional, coherent, readable, appropriately information-dense presentation. It does not change Phase 0 scope, pause P0-EP05, authorize a design artifact now, or authorize frontend implementation before its owning phase.

## Validation evidence

User-facing execution packets must define proportionate visual/UX evidence in addition to automated code tests. Depending on the capability, this may include comparison to the approved design artifact, representative screenshots/states, keyboard and accessibility checks, visual regression checks, realistic-density review, and independent visual/UX review. The implementing worker cannot be the sole authority for visual acceptability.

## Follow-up owners

- **Phase 3 plan:** define the initial visual system, agent/review mechanism, representative states, and validation method before substantial UI packets.
- **Phases 4-10:** apply and evolve the approved system for data, modeling, results, experiments, automation, real-world density, and nested-network work as relevant.
- **Central:** revisit the guidance only through an explicit decision when evidence or product needs warrant it.

## Supersession and revisit triggers

Revisit when the first user-facing Phase 3 plan supplies evidence about the chosen UI architecture, when a maintained design-support mechanism materially changes, or when a later capability exposes visual-density, accessibility, or interaction needs not covered by the approved design artifact.
