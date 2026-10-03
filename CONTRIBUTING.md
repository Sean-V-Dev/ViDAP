# Contributing to ViDAP

Thank you for helping shape ViDAP. The repository has a bounded Phase 0
foundation that is awaiting independent validation. It includes a small local
shell, not a runnable product application. Contributions should make approved
work clearer, safer, or more verifiable without implying that a planned
capability already exists.

## Supported setup and build commands

Windows is the only currently supported development environment. Install Node
24 LTS with its bundled npm and uv. CPython 3.14.7 is pinned in `python/` and
selected or provisioned by uv; no separate system Python setup is required.

From Windows PowerShell, use these authoritative commands:

```powershell
npm.cmd run setup
npm.cmd run build
```

`setup` installs only the committed npm and uv locks. `build` creates only
ignored web build output. Do not replace or casually regenerate
`package-lock.json` or `python/uv.lock`.

### When your shell cannot run the Windows commands

Some agents and tools run in a non-Windows shell (for example, a Linux shell
that can see this folder). If a packet or this guide requires an `npm.cmd` or
`powershell.exe` command and your shell cannot run it, that is not a blocker
by itself. Use this workaround instead of breaking the environment:

1. Do not run `setup`, `npm ci`, `npm install`, or `uv sync` against this
   checkout from that shell. The ignored `node_modules/` and `python/.venv/`
   are Windows installations and would be replaced.
2. Do not substitute `npm`, a different Node version, or a Linux equivalent
   and report it as the required check.
3. Do everything else from your shell: reading, authorized edits, and
   read-only checks such as hashes, Git scope, and fixture bytes. Any
   non-Windows probe runs only in a disposable copy outside the checkout and
   OneDrive, with its own caches, and is labeled as non-Windows evidence.
4. Give the user the exact ordered commands to run from the repository root
   in Windows PowerShell, and ask them to paste the output back.
5. Record that output in the report as a user-executed Windows run, claiming
   only the results and counts it actually shows. If the output cannot be
   obtained, stop as `Blocked` rather than inferring a pass.

## Local foundation tasks

Use these additional root tasks only after locked setup:

```powershell
npm.cmd run launch
npm.cmd run smoke
```

`launch` starts the known Python and Vite children on fixed loopback IPv4 ports
`127.0.0.1:8000` and `127.0.0.1:5173`, waits for the direct and proxied static
status response, then remains active. It does not open a browser; manually
open the printed `127.0.0.1:5173` URL and press Ctrl+C in that terminal to
stop its child process trees. `smoke` performs the same readiness proof and
automatic cleanup. It must never select a different port, bind publicly, write
a log/PID file, or terminate a process it did not start.

The browser app is the Phase 3 editor workspace (`apps/web/src/editor/`). It
reads node definitions, validation verdicts, and saved files only through
`/api/slice/`, and follows `DESIGN.md`; it must not copy parameter defaults,
ranges, or validation rules into UI code. Its tests replay responses recorded
from the real backend (`apps/web/src/editor/test-data/`); regenerate them with
the capture described in `ViDAP_P3_EP04A_Implementation_Report.md` when the
channel changes. `GET /api/status` is the static, input-free foundation response; it is not a
health/product API or a generic contract. The Phase 3 slice adds the local
`/api/slice/` channel (contracts, validate, run, and workflow save/load). It is
loopback-only and unauthenticated, refuses non-loopback hosts and foreign
origins, grants no CORS, and accepts only bounded JSON bodies. Graph
authoring, run controls, general data and model work, export, browser E2E,
hosting, and desktop work remain deferred.

`fixtures/p0-ep07-foundation-status.json` is the one synthetic ≤1 KiB EP07
fixture. It records expected static status evidence and required provenance,
terms, consumer, privacy, and review metadata. Only the EP07 harness/tests may
consume it; do not serve it, treat it as input, or add dataset-like fixtures.

`fixtures/p3-ep03b/` holds the Phase 3 slice's one synthetic CSV, its two
workflows, and their D0.7 manifest. Only the slice's first-party Dataset
operation and tests consume them; the CSV is regenerated only by its
checked-in deterministic generator, and any change needs a new fixture version
and manifest update.

## Local quality evidence

After `npm.cmd run setup`, use the locked root tasks below:

```powershell
npm.cmd run format:check
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run test:unit
npm.cmd run test:integration
npm.cmd run coverage
npm.cmd run check
```

`check` is the ordered non-mutating aggregate and runs `smoke` last. `coverage`
produces ignored V8 and coverage.py reports without a percentage requirement. `format:write` and
`lint:fix` are explicit repair actions and must not be folded into normal
checks. The current lint layer intentionally covers TypeScript-aware rules and
React Hooks; JSX accessibility linting is deferred under decision record 0001,
not completed or replaced by another linter.

## Dependency controls and CI expectations

After locked setup, run `npm.cmd run deps:inventory`, `npm.cmd run
license:check`, and `npm.cmd run deps:audit` when a change affects a manifest,
lock, dependency policy, or GitHub Action. These commands are evidence only:
they do not run a fix, accept a license, or prove a vulnerability is exploitable.
They use the installed locked graphs and preserve `package-lock.json` and
`python/uv.lock`.

The Windows GitHub Actions workflow invokes the same root setup, quality,
coverage, inventory, license, and audit tasks. It has read-only repository
permissions and no secrets. Dependabot proposes at most two weekly npm or
GitHub Actions update PRs per ecosystem; only patch/minor development-tool
updates may be grouped. Major and security updates remain individually
reviewable. UV bot updates, auto-merge, and bot trust bypasses are not used.

See [dependency controls](docs/dependency-controls.md) and accepted [Decision
Record 0003](docs/decisions/0003-ep06-locked-license-disposition.md),
[Decision Record 0004](docs/decisions/0004-ep06-generic-license-metadata-disposition.md),
and [Decision Record 0005](docs/decisions/0005-p3-slice-numeric-runtime-license-disposition.md)
for the allowed, review-required, prohibited, and literal-catalog license
treatment; advisory triage; temporary audit-output rules; the no-SBOM deferral;
and the no-auto-fix policy. Continue
to report suspected vulnerabilities through the private route in
[SECURITY.md](SECURITY.md).

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

Tests and documentation are delivery work, not cleanup. Do not invent public
project commands beyond the approved bounded setup, build, launch, and smoke
tasks.

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
Named uses so far: `.vidap-local/runs/` for attempt records and
`.vidap-local/workflows/` for backend-saved slice workflows and their
workspace-view sidecars.

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
