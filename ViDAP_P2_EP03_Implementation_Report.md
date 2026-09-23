# ViDAP P2-EP03 — Implementation Report and Validation Handoff

| Field | Worker evidence |
|---|---|
| Packet | `ViDAP_P2_EP03.md` v0.1, approved 2026-09-22 |
| Worker status | Ready for fresh independent validation; Central acceptance pending |
| Branch and target | `main` at `4b27f23085dd44c654c73af29535654057713468` |
| Prerequisites | P2-EP01 D2.1–D2.8 accepted; P2-EP02 v0.2 independently accepted and centrally reconciled |
| Governing chain | `ViDAP_Overview.txt`; Spine v1.3; Roadmap v4.1; Phase 2 Plan v1.4; P2-EP01 reconciliation and decision report; P2-EP02 v0.2 and reconciliation; accepted Phase 1 and applicable Phase 0 controls; `UX refinement.txt` consultative for Phase 3+ only |

## 1. Baseline and exact scope

Before any write, the target was clean: no staged, unstaged, or untracked
paths and no pre-existing owner work. None of the six authorized output paths
collided with existing dirty work. `npm.cmd run setup` passed. The first
baseline `npm.cmd run check` reached Vitest, where three workers timed out
during startup. A normal Windows retry passed the entire baseline check,
including 62 selected Python unit tests, three integration tests, build, and
smoke. The restricted path had first denied `uv`; the retry used the accepted
normal Windows execution path without changing the interpreter, dependencies,
locks, or TLS policy.

The complete worker scope is exactly:

1. `python/src/vidap_execution/__init__.py`
2. `python/src/vidap_execution/planner.py`
3. `python/src/vidap_execution/dispatch.py`
4. `python/tests/test_execution_planner.py`
5. `python/tests/test_execution_dispatch.py`
6. `ViDAP_P2_EP03_Implementation_Report.md`

The first five are the only source/test changes; this report is the sixth.
Accepted Phase 1 and P2-EP02 paths, fixtures, manifests, CI, dependencies,
locks, governing artifacts, and remote state were not changed. Nothing was
staged, committed, or pushed.

| Lock authority | SHA-256 before and after |
|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` |

## 2. Implemented control path and decision boundaries

`plan_execution` is the validated synchronous entry. It calls accepted
P2-EP02 `prepare_execution` exactly once, then plans only its immutable
`ExecutionRepresentation`. It lets the original ordered Phase 1 diagnostics
and narrow binding refusals propagate unchanged. The plan carries fixed
`vidap.execution-plan/1.0` and `vidap.runtime-table/1.0` identifiers, the
accepted representation (including workflow semantic digest, contract
snapshot reference, resolved parameters, operation keys, and binding
revision), schedule, dependencies, and incoming-edge references. It has no
run identity, UI state, result, artifact, seed, environment, cache, or
callable. This applies D2.1–D2.2 within this packet's boundary.

The private representation planner checks dangling endpoints, duplicate
exact directed edges, self-dependencies, and cycles. These defensive checks
do not revalidate Phase 1 port contracts from the snapshot hash. Sorted Kahn
planning maintains a heap of currently ready canonical node IDs: after each
node is removed, newly ready successors enter that heap, so the smallest
currently ready ID wins. Dependencies are sorted by predecessor ID;
incoming edges are sorted by `(target port key, source node ID, source port
key, edge ID)`. An empty valid workflow yields an empty plan. Labels,
layout, viewport, and insertion order are never consulted.

`RuntimeTable` is a frozen, explicit, code-constructed handler table separate
from P2-EP02's non-executable `BindingMap`. Each `RuntimeRegistration` holds a
trusted handler for one `(operation key, binding revision)` pair. Before the
first call, dispatch checks the table revision against the plan, rejects
duplicate registrations, and requires one matching handler for every used
operation. Missing and revision-mismatched handlers refuse without a partial
invocation or fallback. Neither a workflow field nor binding metadata names
an executable target, import, path, command, or URL. No production handler is
registered or exported as a product run API.

Dispatch calls handlers sequentially with the representation's frozen
resolved parameters and endpoint-preserving incoming values in the plan's
edge order. Its per-call `(source node ID, output port key)` table stores a
source value once and supplies that same value to every branch consumer. A
join runs after all predecessors and receives distinct incoming edge records,
including multiple edges to one target port. The output mapping is checked
before publication; every source port required by an outgoing edge must be
present. A failed node publishes none of its outputs.

The first handler exception, malformed output mapping, or missing required
outgoing value returns one internal `StopReason` with category `execution`,
stable code (`handler-failed`, `invalid-handler-output`, or
`missing-output`), affected node and operation, and technical exception type
when applicable. Raw exception text and tracebacks are not placed in the
result. `DispatchResult` distinguishes completed node IDs, the failed ID,
transitive blocked descendants, and unrelated unstarted IDs. It exposes only
call-owned observations and an immutable view of that call's port table;
subsequent calls allocate a new table and invoke handlers anew. This is
D2.3's within-invocation fan-out only.

D2.6's complete semantic reuse key, reuse events, and any cache policy remain
for P2-EP04. D2.7's attempt-linked sanitized user-facing envelope and remedy
policy remain for P2-EP04; Phase 1 diagnostics are distinct pre-dispatch
refusals. D2.8's approved real product reference operation family remains for
P2-EP05. The test-local scalar handlers are **not approved product
operations or Phase 2 exit evidence**.

## 3. Focused evidence

The 21 focused EP03 tests exercise actual `plan_execution` and `dispatch`
source paths. They cover empty, linear, independent-root, branch, join, and
dynamic-ready graphs; a newly ready lower ID beating an older ready higher
ID; reversal of document/node/edge/registry construction; display and layout
invariance; matching workflow digest and contract snapshot; preparation
called once; original invalid-workflow diagnostics and unbound refusal;
direct challenges to dangling, duplicate-exact, self-dependent, and cyclic
representations; all handler preflight refusals before any call; scalar
branch/join computation; multiple incoming edges distinguished by endpoints
and sorted by target/source port identities; first failure and blocked versus
unrelated unstarted status; malformed/missing output with no partial
publication; and separate results and fresh computation on two calls.

Static inspection of the new source found no product operation registration,
file or network access, child process, UI/API, data/ML computation, export,
plugin discovery, persistent result, run record, artifact, generalized cache,
or later-packet implementation. Existing P2-EP02 bindings and representation
were neither modified nor repurposed as executable authority.

## 4. Ordered final attestation and isolated proof

After the final source/test change, the required local commands ran in this
exact order and all passed:

| Order | Command | Final result |
|---:|---|---|
| 1 | `npm.cmd run check` | Pass: formatting, lint, typecheck, 10 web tests, 83 Python unit tests, build, three Python integration tests, smoke |
| 2 | `npm.cmd run coverage` | Pass: 10 web tests; all 86 Python tests; Python total 88% reported coverage (no threshold claimed) |
| 3 | `npm.cmd run deps:inventory` | Pass: locked installed inventory generated |
| 4 | `npm.cmd run license:check` | Pass: policy checked 431 installed locked packages |
| 5 | `npm.cmd run deps:audit` | Pass: zero known npm/Python advisory findings reported |
| 6 | `git diff --check` | Pass: no tracked whitespace errors |

One earlier disposable proof copy passed locked setup and its then-current
20 focused tests, but its full check failed because isolated caches had been
placed inside the copied project and ESLint scanned third-party cache files.
The caches were moved outside the copied project, the full check then passed,
and that copy plus both cache paths were removed and verified absent. A final
test addition followed, so the complete local attestation above was rerun.

The final disposable copy was made outside the repository and OneDrive from
129 tracked and new source paths. Its npm and uv caches were isolated as
separate temp siblings outside the copied project. Locked `npm.cmd run setup`
passed, the 21 focused EP03 tests passed, and `npm.cmd run check` passed
through smoke. Only the exact copy and its two cache paths were recursively
removed after resolved-target containment/name checks; all three were
verified absent. No repository-relative cache or alternate interpreter was
used for this proof.

Final Git inspection shows precisely the five Python changes plus this
report, with no staged path or unrelated untracked path. Generated build,
coverage, environment, and interpreter/test caches remain ignored under the
existing policy. The new files end in newlines; formatting, whitespace, and
scoped sensitive-content checks found no credential or user-specific path.
The test's literal fake exception message exists only to prove sanitization.
No worker-owned PID/log file or listener on prescribed ports 8000/5173
remained after smoke. Both lock hashes still match Section 1.

## 5. Handoff and limitations

This is worker evidence, not an independent verdict. A fresh independent
validator should read the packet and all governing inputs, challenge the
planner/dispatcher and the exact six-path scope, reproduce the required
attestations and bounded clean-copy proof as permitted, and return `Accept`,
`Revise`, or `Blocked` with requirement-linked findings. EP03-AC14 and
EP03-AC15 remain pending that independent validation and Central's separate
reconciliation. No P2-EP04 or later work has begun.
