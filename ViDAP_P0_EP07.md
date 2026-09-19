# ViDAP P0-EP07 — Controlled Fixture and Minimal Runnable Shell

| Field | Value |
|---|---|
| Status | Complete — accepted by Central |
| Packet version | 0.1 |
| Parent phase plan | `ViDAP_Phase_0_Plan.md` version 1.0 |
| Prerequisites | P0-EP01 through P0-EP06 — Complete |
| Prerequisite reconciliations | `ViDAP_P0_EP01_Validation_and_Reconciliation.md`; `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP03_Validation_and_Reconciliation.md`; `ViDAP_P0_EP04_Validation_and_Reconciliation.md`; `ViDAP_P0_EP05_Validation_and_Reconciliation.md`; `ViDAP_P0_EP06_Validation_and_Reconciliation.md` |
| Workstream | WS0.6 — Fixtures and minimal shell |
| Packet type | Bounded local fixture, shell, loopback process-harness, and smoke-test implementation |
| Created | 2026-09-19 |
| Central acceptance | 2026-09-19 |
| Owner | Central |

---

## 1. Authorization boundary

Version 0.1 received fresh explicit user approval on 2026-09-19. No approval
of another packet or a later revision carries forward. Only this approval
authorizes one fresh bounded worker.

After approval, the worker may implement only the Section 7 paths, run the
local loopback processes required by the smoke test, and create the
implementation report. The worker may not self-validate, accept the packet,
commit, push, dispatch CI, open a browser, or begin P0-EP08 or later work.

P0-EP07 proves a tiny local integration seam. It must not become a disguised
prototype of a workflow editor, data loader, or product service.

---

## 2. Plain-English intent

ViDAP has an accepted React web area and a separate local Python execution-host
area, but Phase 0 currently has an intentionally empty web root and no running
processes. This packet adds the smallest honest proof that those foundations
can start locally together:

1. a recognizable browser shell that says it is a **Phase 0 foundation**;
2. one loopback-only Python status response with no product data or behavior;
3. one small synthetic fixture describing the expected status result; and
4. one Node 24 process harness that starts both local processes, waits for
   readiness, checks the web-to-Python status path, enforces a timeout, and
   terminates its child process trees on every exit path.

The human launch task leaves the two local processes running until the user
presses Ctrl+C. The smoke task starts, verifies, and stops them automatically.
Neither task opens a browser; after `launch` reports readiness, the user may
manually open the printed loopback URL.

---

## 3. Governing inputs and traceability

The worker and validator must read these sources in authority order:

1. Current explicit user direction approving this exact packet version, if
   given.
2. `ViDAP_Overview.txt`, especially the local-first, inspectability,
   actionable-error, provenance, and no-invisible-behavior requirements in
   §§1–3, 9, 18–23, and 25–30.
3. `ViDAP_Phased_Plan_Spine.md` version 1.1, especially its authority,
   bounded-execution, fixture/data, local-first, testability, and no
   self-acceptance invariants.
4. `ViDAP_Roadmap.md` version 1.1, especially Phase 0, its A0 checkpoint, and
   the explicit P0-EP07 next action.
5. `ViDAP_Phase_0_Plan.md` version 1.0, especially WS0.6, P0-G8, P0-EP07,
   Sections 7, 9–11, P0-AC05/P0-AC10/P0-AC11, and the Phase 0 exclusions.
6. `ViDAP_P0_EP01_Validation_and_Reconciliation.md`, authoritative for D0.1
   through D0.3: a local TypeScript/React UI, a separate local
   CPython/FastAPI host, loopback-only default boundary, one repository,
   Node 24/npm, uv-managed CPython 3.14, and no desktop wrapper.
7. `ViDAP_P0_EP02_Validation_and_Reconciliation.md` and
   `ViDAP_P0_EP02_Decision_Report.md`, authoritative for D0.4–D0.7. In
   particular, Q09 is a repository-owned Node 24 cross-process smoke harness
   with no orchestration dependency, and EP07 may add one synthetic text
   fixture of at most 1 KiB.
8. The P0-EP03 through P0-EP06 reconciliation records, authoritative for
   repository hygiene, runtime/lock discipline, quality-task boundaries, and
   CI/dependency-control constraints.
9. `docs/decisions/0001-ep05-frontend-quality-compatibility.md`, preserving
   the JSX-a11y deferral; and decision records `0003` and `0004`, preserving
   the locked dependency-license boundary.
10. This packet.

This packet implements only the P0-EP07 slice. It does not define a workflow
schema (P1), execution semantics (P2), browser end-to-end testing or
accessibility acceptance (P3), data loading/Titanic work (P4), models,
experiments, exports, packaging, or hosting.

---

## 4. Non-negotiable constraints

1. Windows is the only supported execution platform. All public commands use
   `npm.cmd run` and the existing Node 24/npm and uv-managed CPython 3.14
   contract.
2. `package.json`/`package-lock.json` and `python/pyproject.toml`/`python/uv.lock`
   remain the only manifest and lock authorities. This packet adds **no
   dependency** and both locks must remain byte-identical.
3. The existing root quality, build, coverage, inventory, license, and audit
   tasks retain their semantics. `check` may gain the new authoritative smoke
   task at its final position; it must remain non-mutating and fail fast.
4. The only local network traffic is loopback IPv4: the Python host binds only
   `127.0.0.1`, the Vite development server binds only `127.0.0.1`, and the
   smoke harness may request only those two loopback origins. No external
   network call, host binding, LAN access, CORS policy, credential, telemetry,
   upload, persistence, or user data is permitted.
5. The fixed development ports are `8000` for the Python host and `5173` for
   the web server. Strict binding must fail with an actionable port-conflict
   message rather than silently using another port or process.
6. The sole cross-boundary response is `GET /api/status`, through Vite's
   same-origin development proxy to the Python host. Its exact JSON body is
   `{"application":"ViDAP","scope":"phase-0-foundation","status":"ready"}`.
   It takes no input, reads no data, writes no state, exposes no health/product
   API, and must not become a generic route or versioned contract.
7. The visible React shell may show only the application name, its
   Phase 0/foundation limitation, and the bounded host status: checking,
   ready, or unavailable with a local startup remedy. It must use semantic
   HTML and no CSS/design system, graph canvas, node, edge, workflow,
   dataset, model, experiment, export, form, authentication, or product
   control.
8. The process harness uses Node 24 built-ins and the already locked local
   tools only. It must start child processes, capture bounded diagnostic lines,
   poll readiness with a finite timeout, reject non-loopback targets, and
   terminate process trees on success, timeout, child failure, Ctrl+C, and
   unexpected exit. It may not add `concurrently`, `wait-on`, `start-server-*`,
   `cross-env`, browser automation, a shell script, a global tool, or another
   task runner.
9. The one fixture is a UTF-8 JSON file under `fixtures/`, at most 1 KiB. It is
   hand-authored synthetic metadata and expected status evidence, not a data
   set. It contains the required stable ID/version, repository-relative path,
   byte size, synthetic provenance, MIT terms, deterministic creation method,
   expected properties, permitted consumers, privacy attestation, and
   reviewer/date. It contains no person, real dataset, credential, path,
   network identifier, or telemetry.
10. No hidden local state may remain after smoke. Logs, process output,
    temporary files, reports, caches, environments, and build output remain
    ignored; the harness must not write a log file or a PID file.

---

## 5. Preconditions and stop gates

Before changing a file, the worker must confirm and record:

1. This packet is explicitly approved and matches the approved version.
2. P0-EP01 through P0-EP06 are complete and all reconciliation records in
   Section 3 are present.
3. The current branch, commit, sanitized remote, existing worktree changes,
   and collisions with every Section 7 path.
4. Node 24/npm and the normal/elevated uv/CPython 3.14 path are callable;
   `npm.cmd run setup`, `check`, `coverage`, `build`, `deps:inventory`,
   `license:check`, and `deps:audit` pass with unchanged locks before this
   packet's intended changes.
5. The normal/elevated uv path has usable certificate trust before a required
   network-backed setup/audit operation. The known restricted-sandbox uv
   access issue must be retried through the normal Windows path; no TLS bypass
   or persistent certificate workaround is permitted.
6. Ports `127.0.0.1:8000` and `127.0.0.1:5173` are available for the bounded
   smoke proof, or a live conflicting process can be identified without being
   changed. A conflict is a blocker, not authority to kill an unrelated
   process or select another port.
7. The current locked Vite, Uvicorn, FastAPI, and Node 24 capabilities can
   implement the prescribed local process behavior without a new dependency,
   version update, lock rewrite, global installation, or framework policy
   change.
8. A worker-created temporary directory outside the repository and OneDrive is
   available for clean-copy and intentional failure evidence.

Stop and return a blocker if a required port is occupied, a process cannot be
started or cleaned up safely, a task changes a lock, a required change lies
outside Section 7, a fixture cannot meet D0.7 exactly, a process needs a
non-loopback/network operation, or the proposed behavior would imply product
semantics.

---

## 6. Objective and completion condition

### Objective

Implement a tiny deterministic fixture, a clearly limited visible shell, and
the local Windows process lifecycle needed to prove that the selected React and
FastAPI foundations start, reach each other through a loopback-only status
seam, and stop cleanly.

### Completion condition

P0-EP07 is complete only when:

1. The worker changes only the Section 7 paths, with no dependency or lock
   change.
2. The fixture meets every D0.7 and Section 4 constraint and is exercised by
   the smoke proof.
3. `launch` and `smoke` are documented root tasks; the latter is included at
   the end of `check` and is therefore exercised by existing Windows CI
   without changing the workflow.
4. The smoke command proves Python readiness, web readiness, the web proxy to
   the static Python status, an actionable failure path, and tree cleanup.
5. All existing and new local quality/control commands pass, both locks remain
   unchanged, and an isolated clean copy reproduces setup, checks, smoke, and
   cleanup.
6. A fresh independent validator returns `Accept`, including a user-authorized
   green hosted Windows run on the final commit.
7. Central reconciles the result before P0-EP08 is drafted.

---

## 7. Exact authorized outputs

The worker may create or modify only these paths:

| Path | Authorized purpose |
|---|---|
| `package.json` | Add the exact `launch` and `smoke` root tasks; append `smoke` to the existing non-mutating `check` aggregate. |
| `apps/web/index.html` | Replace the scaffold title with an accurate Phase 0 shell title only. |
| `apps/web/vite.config.ts` | Configure fixed loopback-only development host/port and the sole `/api` development proxy to the fixed loopback Python host. |
| `apps/web/src/foundation-root.tsx` | Replace the null root with the bounded semantic foundation shell and one status fetch. |
| `apps/web/src/foundation-root.test.tsx` | Replace the no-UI test with deterministic checking/ready/unavailable shell assertions. |
| `python/src/vidap_execution/app.py` | Disable FastAPI's automatic OpenAPI/docs endpoints and add the sole static `GET /api/status` foundation response to the existing app factory. |
| `python/tests/test_execution_app.py` | Add deterministic in-process assertions for the static status response and retain the no-product-route assertion. |
| `scripts/vidap-process-harness.mjs` | Node 24 built-in-only launch/smoke lifecycle, readiness, bounded diagnostics, timeout, loopback validation, and tree cleanup. |
| `scripts/vidap-process-harness.test.mjs` | Deterministic unit coverage of harness mode/target/fixture validation and failure diagnostics without launching a real process. |
| `fixtures/p0-ep07-foundation-status.json` | The one D0.7-compliant, ≤1 KiB synthetic expected-status fixture. |
| `README.md` | Accurate Windows setup, launch, smoke, loopback-only, fixture, status, and deferral documentation. |
| `CONTRIBUTING.md` | Accurate contributor expectations for the new bounded tasks and fixture policy. |
| `ViDAP_P0_EP07_Implementation_Report.md` | Worker evidence and independent-validation handoff. |

The worker may create only the existing `fixtures/` parent directory if it is
absent. It may not create any other path.

The worker must not modify manifests other than `package.json`; either lock;
CI/Dependabot files; ignore, license, security, decision, roadmap, phase-plan,
or reconciliation files; configuration outside this table; or any unrelated
user file.

---

## 8. Required implementation contract

### 8.1 Fixture contract

`fixtures/p0-ep07-foundation-status.json` must be valid UTF-8 JSON, contain no
more than 1,024 bytes, and state the expected exact static status object
`{"application":"ViDAP","scope":"phase-0-foundation","status":"ready"}`
used by the smoke check. It must also state the D0.7 metadata described in Section
4(9), including a byte count that matches the final file. It is hand-authored
synthetic fixture metadata, requires no generator or external checksum, and
may be consumed only by the EP07 harness/tests.

The fixture must not be served as an application asset, interpreted as input,
or read by the Python service at runtime. The Python response and the fixture
may share the same prescribed static values, but neither is a workflow,
dataset, configuration system, or generic status protocol.

### 8.2 Minimal status seam

The Python app factory must disable FastAPI's automatic OpenAPI, Swagger, and
ReDoc endpoints and expose exactly one new unauthenticated, input-free route:
`GET /api/status`. Its successful response is exactly
`{"application":"ViDAP","scope":"phase-0-foundation","status":"ready"}`.
It must not inspect a request body, headers, filesystem, environment, model,
graph, fixture, dataset, database, or third-party service. It must not expose
`/health`, `/docs`, product routes, workflow state, a versioned API, or an
error envelope.

The Vite development server must bind only `127.0.0.1:5173` with strict port
behavior and proxy only `/api` to `http://127.0.0.1:8000`. No browser CORS
configuration, proxy rewrite, alternate target, or production server behavior
is authorized.

`FoundationRoot` must render semantic, text-only HTML that identifies ViDAP and
states that the application is a Phase 0 foundation without workflow, data, or
model capabilities. On mount it requests only relative `/api/status` once.
It renders a bounded checking state, a ready state when the exact expected
response is received, and an unavailable state with the actionable local
remedy `npm.cmd run launch` when the request fails or is malformed. It must not
retry, poll, persist, log, render raw errors, or expose an editable UI.

### 8.3 Launch and smoke tasks

The root tasks are exactly:

| Task | Required behavior |
|---|---|
| `npm.cmd run launch` | Runs the harness in long-lived launch mode. It starts the locked Python Uvicorn process on `127.0.0.1:8000`, waits for its static status, starts the locked Vite development process on `127.0.0.1:5173`, verifies the same-origin proxied status, prints the manual loopback URL and Ctrl+C instruction, and remains active until interrupted. |
| `npm.cmd run smoke` | Runs the same harness in finite smoke mode. It performs the same bounded start/readiness/proxy verification, validates the response against the fixture, then terminates both child process trees and exits zero only when cleanup succeeds. |
| `npm.cmd run check` | Retains all prior checks in order and runs `smoke` last. It remains non-mutating and fails fast. |

The harness must start Uvicorn only through the locked Python workspace, using
the existing app factory and a loopback host/port. It must start Vite only
through the already installed local project tool. It must use explicit child
arguments, never a user-supplied command string or shell interpolation.

It must reject any mode other than `launch` or `smoke`, any readiness URL that
is not exact loopback HTTP on the prescribed ports, and any fixture that is
missing, over the size limit, malformed, or inconsistent with the expected
static properties. It must cap displayed child diagnostics, redact no values
by guessing, and never write diagnostics to a file.

The startup/readiness timeout must be finite and documented in the script. On
child exit, timeout, status mismatch, Ctrl+C, process error, or smoke success,
the harness must terminate its own known child process trees and wait for them
to exit. On Windows it may use the built-in `taskkill` only for its recorded
child PIDs and descendants; it must never target a port, process name, or
unrelated PID. It must report which bounded stage failed and the local remedy
(for example, an occupied prescribed port or a failed locked setup) without
printing environment values, absolute user paths, or credentials.

### 8.4 Tests, CI, and documentation

Tests must prove meaningful limited claims:

- Vitest/Testing Library verifies the shell's checking, exact-ready, malformed,
  and unavailable display states with mocked `fetch`; it makes no real network
  request.
- Existing in-process Python tests verify the exact static status response and
  retain the ordinary unknown-route assertion. They start no server and bind no
  port.
- The harness unit test verifies invalid modes, non-loopback target rejection,
  fixture metadata/size validation, and actionable bounded diagnostics without
  starting children.
- The smoke task is the one real cross-process proof. It verifies the fixture,
  Python loopback readiness, web loopback readiness, and the Vite-proxied
  status response, then proves cleanup by observing both known child processes
  exit. It must include a safely controlled startup-failure proof in a
  temporary copy—such as an explicitly invalid harness mode or a deliberately
  unavailable prescribed target—without killing or altering an unrelated
  process.

No browser automation, screenshot, E2E framework, actual browser opening,
public host binding, generic API-client library, mock server package, or test
fixture beyond the one JSON file is permitted.

Because the existing Windows CI invokes `npm.cmd run check`, adding `smoke` at
the end of that aggregate extends the same existing quality job. The worker
must not modify the workflow, create a separate CI job, or claim hosted proof.
README and CONTRIBUTING must state the exact human launch behavior, loopback
ports, Ctrl+C cleanup expectation, fixture boundary, smoke role, and all
remaining product deferrals.

---

## 9. Permitted scope

The worker may read governing files and current project files; run the existing
locked setup/quality/control commands; use normal/elevated uv where required;
start only the packet's two known loopback child processes; inspect Git
read-only; and use exact worker-created temporary directories outside the
repository and OneDrive for clean-copy and failure evidence.

The worker must return a blocker instead of adding a dependency, changing a
lock, choosing a new port, killing an unrelated process, weakening a timeout,
binding a public interface, adding a product route, changing CI, or broadening
the fixture.

---

## 10. Prohibited scope

The worker must not:

1. Add a workflow schema, graph/node/edge UI, React Flow use, data loader,
   profile, transform, model, experiment, result, export, persistence,
   authentication, telemetry, agent/LLM, or ML dependency.
2. Add a browser test, browser binary, screenshot, CSS/design system, icon,
   image, canvas, user input, form, navigation, or responsive product layout.
3. Add a hosted service, desktop wrapper, installer, container, public/LAN
   binding, cloud/API call, database, websocket, background worker, or queue.
4. Modify CI, Dependabot, locks, Python dependencies, `.gitignore`,
   `.gitattributes`, security/license/decision/governance documents, remote
   settings, or project/system environment settings.
5. Use `npx`, a global package, a new task runner/orchestrator, shell command
   interpolation, arbitrary PID/port/process-name termination, or a PowerShell
   policy/TLS workaround.
6. Stage, commit, push, dispatch CI, create a release/PR, modify repository
   settings, or claim hosted CI evidence.
7. Create any file outside Section 7 or begin P0-EP08, Phase 1, or later work.

---

## 11. Required execution sequence

After approval, the worker must:

1. Read every governing input and record approval, branch/commit/worktree,
   sanitized remote, pre-existing changes, and every Section 7 collision.
2. Reproduce the locked baseline setup, quality, coverage, build, and
   dependency-control commands; record both lock hashes before and after.
3. Verify the normal/elevated uv certificate posture before any necessary
   network-backed operation, and verify prescribed loopback ports are unused.
4. Create the one synthetic fixture first, validate its byte size and metadata,
   and prove it is tracked while generated/local fixture paths remain ignored.
5. Implement the static Python status, fixed loopback Vite proxy, semantic
   shell, and deterministic unit/in-process tests without adding dependencies.
6. Implement the Node built-in process harness and its unit tests, then add the
   exact root `launch`/`smoke` tasks and append smoke to `check`.
7. Run all individual root quality/control tasks, the aggregate check, coverage,
   build, and smoke; prove routine commands do not change locks or leave a
   running child process.
8. In an exact temporary copy outside the repository and OneDrive, reproduce
   locked setup, check, smoke, fixture validation, and cleanup with isolated
   npm/uv caches. Remove only that exact temporary copy and its known caches.
9. Demonstrate the controlled failure path without touching a live unrelated
   process. Confirm malformed/unavailable status produces bounded actionable
   diagnostics and that the harness cleans up its own children.
10. Update README/CONTRIBUTING, create the implementation report, run
    whitespace/link/sensitive-content/scope checks, and stop for independent
    validation.

---

## 12. Required worker evidence

`ViDAP_P0_EP07_Implementation_Report.md` must include:

1. Packet identity, approval, governing inputs, worker role, baseline, and
   exact Section 7 path comparison.
2. Starting/final branch, commit, sanitized remote, pre-existing work, and
   collision evidence.
3. Node/npm/uv/CPython facts, normal/elevated uv distinction if applicable,
   certificate-trust result, and pre/post lock hashes.
4. Fixture content summary without copying it verbatim: stable ID/version,
   byte size, synthetic provenance, terms, expected properties, permitted
   consumers, privacy attestation, and D0.7 validation result.
5. Static Python status route and web proxy/shell contract, including exact
   allowed loopback URLs, no-input/no-state statement, and all explicit
   product/API deferrals.
6. Launch/smoke harness design: child commands by role, readiness order,
   timeout, bounded logging, signal/error behavior, exact cleanup method, and
   proof that no child remains after smoke.
7. Individual task, aggregate check, smoke, build, coverage, fixture, and
   clean-copy results; preserve concise outcomes rather than verbose logs.
8. Unit/in-process/smoke/failure evidence and exact claims each test does and
   does not prove.
9. Documentation, ignore-state, whitespace, link, sensitive-content, and
   final exact-scope evidence.
10. P0-EP07 acceptance-criterion self-assessment, findings, deviations,
    blockers, and independent-validation readiness.

The report must not contain secrets, absolute user paths, raw environment
dumps, full child logs, copied lockfile bodies, external data, or a claim that
the worker accepted the packet or started P0-EP08.

---

## 13. Acceptance criteria

P0-EP07 may be accepted only when:

- **EP07-AC01:** Authority, prerequisites, baseline, repository identity,
  collisions, and pre-existing work are accurately recorded.
- **EP07-AC02:** Only Section 7 paths are changed; no dependency, lock, CI,
  governance, or unrelated path is changed.
- **EP07-AC03:** Both lock authorities remain byte-identical before and after
  every routine command.
- **EP07-AC04:** The fixture is one tracked UTF-8 JSON file under `fixtures/`,
  ≤1 KiB, synthetic, non-sensitive, and complete under D0.7 metadata rules.
- **EP07-AC05:** The fixture is neither a product dataset nor served/loaded as
  application data; only the bounded EP07 tests/harness consume it.
- **EP07-AC06:** The web shell is recognizable, semantic, text-only, and
  clearly limited to Phase 0 foundation status with no product claim.
- **EP07-AC07:** FastAPI automatic OpenAPI/docs endpoints are disabled, and the
  only exposed Python behavior is the static, input-free, loopback-only
  foundation `GET /api/status` route; no generic/product API, health endpoint,
  state, or data behavior exists.
- **EP07-AC08:** Vite binds only the prescribed loopback origin and proxies
  only `/api` to the prescribed loopback Python origin; no CORS/public/alternate
  target behavior is introduced.
- **EP07-AC09:** The shell accurately renders checking, exact-ready, and
  actionable-unavailable states without polling, retry, raw error, persistence,
  or real test-network use.
- **EP07-AC10:** `launch`, `smoke`, and the amended final `check` ordering are
  exact, documented root tasks with no global/new package dependency.
- **EP07-AC11:** The Node 24 harness rejects invalid mode/target/fixture input,
  uses only explicit local child commands, and bounds diagnostics/timeouts.
- **EP07-AC12:** The harness starts the locked Python and Vite children in the
  prescribed readiness order, verifies direct and proxied static status against
  the fixture, and reports actionable failures.
- **EP07-AC13:** Smoke terminates only its known child process trees on every
  success/failure/interruption path and leaves no listener, PID/log file, or
  other generated residue.
- **EP07-AC14:** Unit, in-process, harness-unit, and real smoke layers make the
  limited claims in Section 8.4 without browser automation or product behavior.
- **EP07-AC15:** Existing setup, quality, coverage, build, inventory, license,
  and advisory controls still pass; `check` passes with smoke last.
- **EP07-AC16:** Clean-copy setup, check, smoke, fixture validation, and
  cleanup reproduce from isolated state outside the repository and OneDrive.
- **EP07-AC17:** Controlled malformed/unavailable status or harness failure is
  actionable and preserves known-child cleanup without touching unrelated
  processes.
- **EP07-AC18:** README and CONTRIBUTING accurately document the supported
  Windows tasks, fixed loopback ports, manual browser step, Ctrl+C behavior,
  fixture boundary, and deferrals.
- **EP07-AC19:** Generated dependencies, environments, caches, reports, build
  output, logs, local state, and fixture-local/generated paths remain ignored
  and untracked; the authored fixture remains trackable.
- **EP07-AC20:** No graph/workflow/schema, data, model, experiment, export,
  browser/design, hosting, persistence, desktop, CI, dependency, or P0-EP08+
  work is introduced.
- **EP07-AC21:** No system/global/TLS/PowerShell policy change, remote mutation,
  staging, commit, push, or broad process termination occurs.
- **EP07-AC22:** Text/configuration/links/fixture metadata pass validation;
  sensitive-content and `git diff --check` pass.
- **EP07-AC23:** The implementation report is reproducible, sanitized, and
  distinguishes worker evidence from user-owned hosted evidence.
- **EP07-AC24:** No unresolved critical/high compatibility, fixture, process,
  safety, or scope finding remains; lesser findings are resolved or returned to
  Central.
- **EP07-AC25:** A fresh validator independently verifies all local evidence,
  static contracts, fixture policy, process cleanup, clean-copy behavior,
  exact scope, and absence of later work.
- **EP07-AC26:** A user-authorized hosted Windows run on the final commit is
  green and demonstrates the existing CI `check` path now includes smoke.
- **EP07-AC27:** Independent validation returns `Accept` after hosted evidence
  is available.
- **EP07-AC28:** Central explicitly accepts EP07 before P0-EP08 is drafted.

---

## 14. Independent validation and hosted-evidence boundary

Validation occurs in a fresh chat. The validator must read every governing
input, the approved packet, all Section 7 artifacts, and the implementation
report. It must independently reproduce normal/elevated locked setup,
quality/control tasks, smoke, clean-copy behavior, fixture checks, negative
paths, lock hashes, scope/ignore/sensitive-content checks, and the static
loopback/process contracts.

The validator must inspect the supplied hosted Windows run only after the user
has normally committed and pushed the final change. It must verify that the
existing `check` path actually ran smoke and that no process-related failure
was hidden. It must return `Blocked` for EP07-AC26/AC27 when such evidence is
absent or red.

The validator must not edit files, dispatch CI, change remote state, accept for
Central, create an EP07 decision/exception, or begin P0-EP08. It must return
one verdict (`Accept`, `Revise`, or `Blocked`) with criterion-linked findings,
severity/owner, direct evidence, lock hashes, cleanup conclusion, file-scope
conclusion, and an explicit boundary statement.

---

## 15. Fresh-chat handoff prompts

### Execution worker prompt

> Execute freshly approved `ViDAP_P0_EP07.md` version 0.1 as the bounded fixture/minimal-shell worker. Read every governing input, especially D0.1–D0.7, both accepted fixture/process constraints, and all P0-EP01 through P0-EP06 reconciliations. Modify only Section 7 paths. Add no dependency and do not change either lock, CI, governance, or remote state. Implement exactly one ≤1 KiB synthetic JSON fixture; the text-only Phase 0 shell; the sole static `/api/status` loopback seam; fixed loopback Vite proxy; and a Node 24 built-in-only `launch`/`smoke` process harness with bounded readiness, failure, and process-tree cleanup. Append smoke to `check`, but do not change the workflow. Prove all local tasks, isolated clean-copy smoke, fixture constraints, known-child cleanup, and bounded failure behavior. Do not open a browser, bind publicly, stage/commit/push, self-validate, or begin P0-EP08. Stop with `ViDAP_P0_EP07_Implementation_Report.md`.

### Independent validator prompt

> Act as the independent validator for freshly approved `ViDAP_P0_EP07.md` version 0.1. Read all governing inputs, every Section 7 artifact, and `ViDAP_P0_EP07_Implementation_Report.md`. Independently verify the single fixture and D0.7 metadata/size/provenance/privacy boundary; exact static status/proxy/shell limitation; no product semantics; Node harness input validation, fixed loopback binding, readiness, timeout, bounded diagnostics, and known-child process-tree cleanup; every local quality/control task, lock invariance, clean-copy and negative proof, scope, ignored-state, and sensitive-content results. Inspect a user-supplied final hosted Windows run and return `Blocked` if it is missing, red, or does not demonstrate smoke through `check`. Do not edit files, alter remote state, accept for Central, create a decision record, or begin P0-EP08. Return `Accept`, `Revise`, or `Blocked` with criterion-linked findings.

---

## 16. Next action

Version 0.1 is approved for one fresh bounded worker. Independent validation,
a user-owned hosted Windows run, and Central reconciliation are separate later
gates.
