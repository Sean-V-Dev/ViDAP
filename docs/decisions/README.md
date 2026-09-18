# ViDAP Decision Records

Decision records are lightweight, durable explanations of consequential
choices. They complement the governing artifact chain; they do not create a
parallel governance system.

## When to create one

Create a record for an architecture, dependency, compatibility, security,
data-governance, or scope choice that has meaningful alternatives or lasting
consequences. Do not create one for routine implementation already contained
in an accepted packet.

## Identity and status

Use an immutable numeric ID and a descriptive filename, for example
`0001-local-boundary.md`. Do not renumber, rename, or rewrite an accepted
record to erase history.

Records use these statuses:

- `Proposed` — under consideration, not authoritative.
- `Accepted` — approved by Central under the governing authority chain.
- `Superseded` — replaced by a later record linked from this one.
- `Rejected` — considered and not selected.

Central owns acceptance. Independent evidence is required where the risk
warrants it. Supersede a decision by linking the records; do not rewrite the
earlier decision as if it never existed.

## Relationship to governing work

Each record links to the applicable product specification, phased-plan spine,
roadmap, phase plan, execution packet, and validation evidence. Higher
authority controls if records conflict with those artifacts.

The existing P0-EP01 and P0-EP02 decision reports and reconciliation records
remain authoritative in their current root locations. This directory does not
migrate or replace them.

Start from [the decision-record template](0000-decision-record-template.md).
