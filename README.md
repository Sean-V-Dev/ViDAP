# ViDAP

ViDAP is an open-source, local-first visual data-science playground. Its goal
is to let people work with real data through an inspectable graph: explore and
transform data, train and evaluate established machine-learning libraries,
compare experiments, understand results in practical language, and export
conventional Python or Jupyter artifacts.

> **Phases 0, 1, and 2 are accepted.** Phase 3, the first visual end-to-end
> slice, is in progress: its five slice operations, the local `/api/slice/`
> channel, and workflow save/load exist, and the editor workspace opens, edits,
> validates, and saves slice workflows; adding, connecting, and running nodes
> in the editor come next.

## Intended architecture and prerequisites

The accepted direction is a TypeScript/React local web UI and a separate local
CPython/FastAPI host. The browser remains a visual editing and presentation
layer; future workflow and execution semantics are outside browser-only state.
The local shell, the headless workflow kernel, and the Phase 3 editor
workspace implement only bounded parts of this direction.

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
`build` produces only the ignored `apps/web/dist/` output. Both committed
lockfiles are authoritative and must not be casually regenerated or replaced.

## Launch and smoke

The supported runnable foundation is loopback-only. It starts the Python host
on `http://127.0.0.1:8000` and the Vite development server on
`http://127.0.0.1:5173`; the web server proxies only `/api` to the Python host.
Neither command opens a browser or exposes a LAN/public listener.

```powershell
npm.cmd run launch
npm.cmd run smoke
```

`launch` waits for the static local status seam, prints the web loopback URL,
and leaves both local processes running. Open the printed URL manually, then
press Ctrl+C in the launch terminal to stop its known child process trees.
`smoke` starts the same two processes, verifies the direct and Vite-proxied
`GET /api/status` response, validates the controlled fixture, and stops its
own children automatically. It has a finite 15-second startup timeout and does
not write logs, PID files, or application state.

The sole status body is
`{"application":"ViDAP","scope":"phase-0-foundation","status":"ready"}`.
It takes no input and reads no fixture, data, or state. The static fixture at
[`fixtures/p0-ep07-foundation-status.json`](fixtures/p0-ep07-foundation-status.json)
is synthetic metadata and an expected-result oracle for the EP07 harness and
tests only; it is not application data and is not served by the web shell.

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

`check` runs formatting, linting, types, unit tests, build, in-process
integration tests, and `smoke` last. `coverage` writes ignored Vitest V8 and
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
0003](docs/decisions/0003-ep06-locked-license-disposition.md), [Decision
Record 0004](docs/decisions/0004-ep06-generic-license-metadata-disposition.md),
and [Decision Record
0005](docs/decisions/0005-p3-slice-numeric-runtime-license-disposition.md).
They do not auto-fix dependencies, resolve a floating graph, create an SBOM, or
make legal or exploitability conclusions. See [dependency controls](docs/dependency-controls.md)
for the license policy, temporary-output guardrails, triage expectations, and
weekly update posture.

GitHub Actions runs the same root setup, quality, coverage, and dependency
control tasks on Windows for pull requests to `main`, pushes to `main`, manual
runs, and a weekly clean-cache run. Dependabot is limited to weekly npm and
GitHub Actions updates; it neither updates uv nor auto-merges anything.

## Scope today

Phase 0 establishes project policy and reproducible foundations. Phase 1 adds
the canonical `vidap.workflow`/`1.0` document, static node contracts, and
validation. The accepted Phase 2 kernel prepares, plans, dispatches, and
records headless attempts. The P2-EP05 reference proof uses four fixed
checked-integer operations and two synthetic workflows; successful runs write
one versioned scalar value in an owned local proof slot. The Phase 3 slice
adds five fixed operations (Dataset, Prepare Data, Train/Test Split, Model, and
Evaluate) over one controlled synthetic CSV, using scikit-learn's logistic
regression; a successful headless run records one versioned accuracy result in
the same owned slot. The local `/api/slice/` channel serves the slice
contracts, validates and runs workflows, and saves and loads them under
`.vidap-local/workflows/` with outside-change detection. The browser editor
(`npm.cmd run launch`, then the printed URL) opens a saved slice workflow in its
five regions, edits settings from the backend contracts, shows backend
validation on the node, and saves layout and settings without silent
overwrites. There is still no graph authoring or run control in the editor,
user data loading, model choice, export, authentication,
telemetry, hosted service, deployment, or desktop-wrapper capability.
`/api/status` remains the foundation status response;
automatic OpenAPI and documentation endpoints are disabled. Windows remains
the only supported platform until other environments are independently
validated. JSX accessibility linting is intentionally deferred by decision
record 0001 until a maintained compatible peer set and meaningful JSX exist.

## Authority and navigation

- [Product specification](ViDAP_Overview.txt)
- [Phased Plan Spine](ViDAP_Phased_Plan_Spine.md)
- [Roadmap](ViDAP_Roadmap.md)
- [Phase 0 plan](ViDAP_Phase_0_Plan.md)
- [Phase 1 reconciliation](ViDAP_P1_EP06_Validation_and_Reconciliation.md)
- [Phase 2 plan](ViDAP_Phase_2_Plan.md)
- [Accepted Phase 2 run foundation](ViDAP_P2_EP04_Validation_and_Reconciliation.md)
- [P2-EP05 reference proof packet](ViDAP_P2_EP05.md)
- [Phase 3 plan](ViDAP_Phase_3_Plan.md)
- [P3-EP03B slice operations packet](ViDAP_P3_EP03B.md)
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

`.vidap-local/runs/` holds explicitly owned local headless attempt records and
the selected proof output. Removal is by validated attempt ID; intermediate
values are not stored by default, and there is no cross-run cache promise.
Build, test, coverage, environment,
package-cache, and downloaded-data paths are untracked under `.gitignore`.
Approved tracked fixture content is permitted only under accepted D0.7 policy;
generated and local fixture subareas remain ignored. New mutable or generated
paths must be named and documented with their ignore rules in the same later
packet. Ignored state is not an approved location for secrets.

## License

ViDAP is licensed under the [MIT License](LICENSE).
