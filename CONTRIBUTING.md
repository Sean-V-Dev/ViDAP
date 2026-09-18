# Contributing to ViDAP

Thank you for helping shape ViDAP. The repository is still pre-scaffold: it
has no runnable application or project commands yet. Contributions should make
the approved work clearer, safer, or more verifiable without implying that a
planned capability already exists.

## Authority and approval

Work follows this authority chain:

1. Current explicit user direction and accepted decision records.
2. The [product specification](ViDAP_Overview.txt).
3. The [phased plan spine](ViDAP_Phased_Plan_Spine.md),
   [roadmap](ViDAP_Roadmap.md), and approved phase plan.
4. An approved bounded execution packet.
5. Implementation evidence, independent validation, and Central reconciliation.

An approved packet is required before implementation. Anyone may propose a
defect fix, clarification, dependency change, or scope proposal, but a proposal
is not approval to implement it. Routine work that fits an accepted packet does
not need a new decision record.

## A small-change path

1. Identify the governing requirement or packet and keep the proposed change
   within its file and behavior boundary.
2. Use a focused branch and a clear commit message; no particular commit syntax
   is required by this repository.
3. Open a pull request for review when a change is ready. Describe the evidence
   below and link the governing authority.
4. Escalate instead of expanding scope when the work reveals a defect,
   clarification need, dependency change, or scope proposal.

No branch rule, reviewer count, or automated enforcement is claimed until a
later approved packet configures it.

## Change evidence

Every proposed change should say:

- what changed and why;
- the user-visible effect, including any intentional absence of a user-visible
  effect;
- verification performed and its result;
- files affected;
- dependency and license impact;
- data and fixture impact;
- limitations or unresolved findings; and
- the linked governing requirement, decision, or approved packet.

Tests and documentation are delivery work, not cleanup. Executable project
commands will be added only by approved P0-EP04 through P0-EP06 work; do not
invent commands before then.

## Dependencies, data, and durable decisions

Dependency additions or updates must follow accepted D0.6 policy: use the
approved lockfile and review path, provide license and vulnerability evidence,
and do not rely on unreviewed automatic merging. External or sensitive datasets
must not enter through convenience. Fixtures follow accepted D0.7: they are
synthetic/generated-first, have known provenance and permitted use, document
expected properties, and contain no personal or sensitive data.

Use the [decision-record convention](docs/decisions/README.md) for a
consequential architecture, dependency, compatibility, security,
data-governance, or scope choice that has meaningful alternatives or lasting
consequences.

## Repository safety and local state

Never commit credentials, tokens, personal data, sensitive data, absolute user
paths, environments, caches, build output, or transient artifacts. The
reserved `.vidap-local/` location is untracked repository-local state only when
a later packet names a legitimate need; it is not an approved secret store.

Build, test, coverage, environment, package-cache, and downloaded-data paths
are untracked under `.gitignore`. Approved tracked fixtures remain possible at
the root `fixtures/` area under D0.7, while generated and local fixture
subareas are ignored. A later packet that introduces mutable or generated paths
must name them and update the ignore and documentation rules in the same
change.

## Security reports

Report ordinary non-sensitive bugs and proposals through
[GitHub Issues](https://github.com/Sean-V-Dev/ViDAP/issues). Do not disclose a
vulnerability publicly; follow [SECURITY.md](SECURITY.md) for the private route.
