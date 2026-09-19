# ViDAP

ViDAP is an open-source, local-first visual data-science playground. Its goal
is to let people work with real data through an inspectable graph: explore and
transform data, train and evaluate established machine-learning libraries,
compare experiments, understand results in practical language, and export
conventional Python or Jupyter artifacts.

> **Foundation scaffold is implemented and awaiting independent validation.** It
> builds an intentionally empty web entry point only; no runnable application
> shell or product behavior exists.

## Intended architecture and prerequisites

The accepted direction is a TypeScript/React local web UI and a separate local
CPython/FastAPI host. The browser remains a visual editing and presentation
layer; future workflow and execution semantics are outside browser-only state.
This describes intended architecture, not implementation.

Windows is the only currently supported development environment. Prerequisites
are Git, Node.js 24 LTS with its bundled npm, and uv. CPython 3.14.7 is pinned
in the Python workspace and is selected or provisioned by uv; a separate
system Python setup is not a contributor prerequisite.

## Setup and build

In Windows PowerShell, use `npm.cmd` so no PowerShell execution-policy change
is needed:

```powershell
npm.cmd run setup
npm.cmd run build
```

`setup` performs only locked npm installation and locked uv synchronization.
`build` produces only the ignored `apps/web/dist/` output from the empty web
entry point. Both committed lockfiles are authoritative and must not be
casually regenerated or replaced.

## Local quality commands

After setup, Windows contributors can run these locked, non-mutating checks:

```powershell
npm.cmd run format:check
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run test:unit
npm.cmd run test:integration
npm.cmd run coverage
npm.cmd run check
```

`check` runs formatting, linting, types, unit tests, build, and in-process
integration tests in that order. `coverage` writes ignored Vitest V8 and
coverage.py reports only; no Phase 0 coverage percentage is an acceptance
threshold. `format:write` and `lint:fix` are explicit opt-in repair commands
and never run through `check`.

## Dependency controls and CI

After setup, these locked control tasks inspect the installed npm and Python
graphs without changing either lock:

```powershell
npm.cmd run deps:inventory
npm.cmd run license:check
npm.cmd run deps:audit
```

They provide inventory, fail-closed license review, and advisory evidence; the
only reviewed exceptions are the literal entries in [Decision Record
0003](docs/decisions/0003-ep06-locked-license-disposition.md). They do not
auto-fix dependencies, resolve a floating graph, create an SBOM, or make legal
or exploitability conclusions. See [dependency controls](docs/dependency-controls.md)
for the license policy, temporary-output guardrails, triage expectations, and
weekly update posture.

GitHub Actions runs the same root setup, quality, coverage, and dependency
control tasks on Windows for pull requests to `main`, pushes to `main`, manual
runs, and a weekly clean-cache run. Dependabot is limited to weekly npm and
GitHub Actions updates; it neither updates uv nor auto-merges anything.

## Scope today

Phase 0 is establishing project policy and reproducible foundations. There is
no `dev`, `launch`, or `smoke` command, application shell, workflow schema,
API, dataset, model, hosted service, authentication, deployment, or
cross-platform support claim. Windows remains the only supported platform
until other environments are independently validated. JSX accessibility linting
is intentionally deferred by decision record 0001 until a maintained compatible
peer set and meaningful visible JSX exist.

## Authority and navigation

- [Product specification](ViDAP_Overview.txt)
- [Phased Plan Spine](ViDAP_Phased_Plan_Spine.md)
- [Roadmap](ViDAP_Roadmap.md)
- [Phase 0 plan](ViDAP_Phase_0_Plan.md)
- [P0-EP01 reconciliation](ViDAP_P0_EP01_Validation_and_Reconciliation.md)
- [P0-EP02 reconciliation](ViDAP_P0_EP02_Validation_and_Reconciliation.md)
- [Contribution guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Decision-record guide](docs/decisions/README.md)
- [MIT License](LICENSE)

## Contributing and reporting

Start with the [contribution guide](CONTRIBUTING.md). Report ordinary,
non-sensitive bugs and proposals through
[GitHub Issues](https://github.com/Sean-V-Dev/ViDAP/issues). Report suspected
vulnerabilities only through the private route in [SECURITY.md](SECURITY.md).

## Local and generated state

`.vidap-local/` is reserved for untracked developer or runtime state only when
a later packet names a legitimate use. Build, test, coverage, environment,
package-cache, and downloaded-data paths are untracked under `.gitignore`.
Approved tracked fixture content is permitted only under accepted D0.7 policy;
generated and local fixture subareas remain ignored. New mutable or generated
paths must be named and documented with their ignore rules in the same later
packet. Ignored state is not an approved location for secrets.

## License

ViDAP is licensed under the [MIT License](LICENSE).
