# ViDAP P1-EP02 — Implementation Report

| Field | Value |
|---|---|
| Packet | `ViDAP_P1_EP02.md` version 0.1 |
| Approval | Explicit user direction, 2026-09-20 |
| Worker scope | WS1.2 canonical document kernel only |
| Baseline branch / commit | `main` / `a2e8d308948ce9b4afee4ff5c72743c506972c7b` |
| Remote | Configured; identity intentionally redacted |
| Worker result | Validator-requested revision and renewed self-attestation complete; fresh independent validation pending |

## 1. Authority, inputs, baseline, and scope

The worker read the governing overview, phased spine, roadmap, Phase 1 plan,
P1-EP01 packet, P1-EP01 reconciliation, accepted Phase 0 constraints, and
this approved P1-EP02 packet.  The P1-EP01 reconciliation records Central's
acceptance of D1.1–D1.7; this work implements only the D1.1–D1.2 subset.

Before modification, Node 24/npm and the normal Windows uv-managed CPython
3.14 runtime were callable.  The first restricted call to uv was denied by the
execution environment; the required normal-Windows retry succeeded.  Locked
setup and the aggregate project check passed before the worker change.

Pre-existing work was left intact: three modified planning documents
(`ViDAP_P1_EP01.md`, `ViDAP_Phase_1_Plan.md`, and `ViDAP_Roadmap.md`) and two
untracked approval/packet documents (`ViDAP_P1_EP01_Validation_and_Reconciliation.md`
and `ViDAP_P1_EP02.md`).  The tracked workflow `__init__.py` was empty and
contained no conflicting user work; the other four authorized output paths did
not exist.  No other path was edited by this worker.

## 2. Lock and dependency authority

| Lock | SHA-256 before | SHA-256 after | Result |
|---|---|---|---|
| `package-lock.json` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` | `FB7119F6A4052FBFEEB243D413823767F3540199C03981BB5D170A84A14282FA` | Byte-identical |
| `python/uv.lock` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` | `AC31501B29599D38D0F1983763CED28F55ACB5216A6548F27172974AEC784355` | Byte-identical |

No manifest, dependency, package-manager, runtime-policy, or lock authority
changed.

## 3. Delivered bounded kernel

`python/src/vidap_workflow/__init__.py` exports only the document value types,
the optional layout values, the narrow decode exception, and three JSON
functions.  It imports no execution, experiment, export, FastAPI, Uvicorn, or
web code.

`python/src/vidap_workflow/document.py` defines frozen document, node, edge,
endpoint, position, viewport, and layout values.  Workflow, node, and edge IDs
must be canonical lowercase UUIDv4 text; endpoints are a node ID plus non-empty
immutable port key.  Node type IDs are non-empty strings.  Parameter values are
preserved as recursively immutable JSON-compatible mappings/sequences, and
nodes/edges are canonically ID-sorted.

`WorkflowDocument` semantic equality deliberately omits layout.  Layout is an
optional separate `nodePositions`/`viewport` structure, and its shape cannot
hold alternate edges, ports, parameters, types, validation state, or execution
hints.

`python/src/vidap_workflow/serialization.py` emits UTF-8-encodable Unicode JSON
text using two spaces, lexicographic object keys, a terminal newline, and stable
ID-ordered node/edge arrays.  Full serialization includes optional layout;
semantic serialization excludes it.  Constructors reject unencodable lone
surrogate text everywhere it could otherwise enter output.  The decoder accepts
member reordering and rejects bad JSON, duplicate object names, non-object
roots, wrong or missing envelope fields, extra basic-shape fields, explicit
`null` labels, malformed value shapes, and excessive nesting through the local
`WorkflowDecodeError` only.  It performs no repair and provides no P1-EP04
diagnostic contract.

The implementation deliberately does **not** implement a node registry,
contracts, type/cardinality/required-input checks, parameter constraints,
structured diagnostics, migration, extensions, graph-cycle checks, dependency
ordering, execution, persistence, API/UI behavior, data/ML behavior, export,
network access, or process launching.

## 4. Requirement and test mapping

| Packet requirement | Implemented evidence |
|---|---|
| Immutable document, node, edge, endpoint, and isolated layout values | `python/src/vidap_workflow/document.py` |
| Deterministic full and semantic JSON plus narrow decode boundary | `python/src/vidap_workflow/serialization.py` |
| Deliberate small public surface | `python/src/vidap_workflow/__init__.py` |
| Minimal round trip | `test_minimal_document_round_trips_to_identical_full_json` |
| Branched field/endpoint/identity preservation | `test_branched_document_round_trip_preserves_semantic_fields` |
| Collection/construction-order invariance | `test_collection_and_construction_order_do_not_change_canonical_json` |
| Layout exclusion from semantic equality/JSON | `test_layout_is_not_part_of_semantic_equality_or_serialization` |
| Reordered JSON object members | `test_reordered_json_object_members_decode_to_the_same_document` |
| Bad JSON/basic envelope rejection | `test_bad_json_and_basic_envelopes_raise_the_local_decode_signal` |
| UTF-8 lone-surrogate and deep-nesting rejection | `test_invalid_utf8_text_and_deeply_nested_input_raise_the_local_decode_signal` |
| Explicit null-label rejection without content loss | `test_explicit_null_label_is_rejected_without_silent_content_loss` |
| No forbidden consumer imports | `test_public_import_does_not_import_forbidden_consumer_packages` |

All test data is inline, synthetic, deterministic, and contains no controlled
fixture or claim of deferred validation/runtime behavior.

## 5. Command evidence

Focused implementation checks after the validator-requested correction passed:
Ruff formatting and linting, strict mypy (7 source files), and 13 focused unit
tests.

The required final attestation then passed in the required order:

1. `npm.cmd run check`: formatting, lint, type checks, web tests, 14 Python
   unit tests, build, 3 integration tests, and smoke check passed.
2. `npm.cmd run coverage`: 10 web tests and 17 Python tests passed; Python
   total coverage reported 87%.
3. `npm.cmd run deps:inventory`: passed with the existing locked inventory.
4. `npm.cmd run license:check`: passed.
5. `npm.cmd run deps:audit`: passed; zero npm advisories and no Python advisory
   findings were reported.
6. `git diff --check`: passed.

The initial attestation passed, but independent validation then found three
worker-owned issues: lone-surrogate UTF-8 failure, silent `null`-label loss and
uncaught deep recursion, and incomplete construction-order test coverage.  All
three were corrected within the authorized paths, and the complete sequence
above is the required full rerun after those corrections.

## 6. Clean-copy, hygiene, and cleanup evidence

A newly created, bounded temporary copy outside the repository and OneDrive
was used for the original evidence.  Its first locked setup attempt encountered
a Windows hard-link limitation while installing a cached wheel.  Retrying the
isolated setup with uv's temporary copy mode succeeded without changing
repository files, configuration, manifests, or locks.  A separate newly
created revision clean copy then used that same temporary copy mode from the
start; locked setup, all 13 focused workflow tests, and the complete
`npm.cmd run check` passed.  Both exact temporary copies, their virtual
environments, dependencies, build outputs, and test caches were removed.

The final whitespace check passed.  A focused sensitive-content scan of the
four code/test outputs found zero credential/private-key pattern matches.
Generated build, coverage, cache, and environment state remains ignored rather
than tracked or unignored.  A read-only listener check found zero Node/Python
listeners.  No listener was left by this packet; unrelated resident processes
were not modified.

## 7. Final file scope

Worker-created or worker-modified paths are exactly:

- `python/src/vidap_workflow/__init__.py`
- `python/src/vidap_workflow/document.py`
- `python/src/vidap_workflow/serialization.py`
- `python/tests/test_workflow_document.py`
- `ViDAP_P1_EP02_Implementation_Report.md`

No files were staged, committed, pushed, deleted from the repository, or
changed outside this list.

## 8. Worker self-assessment

| Criterion | Worker assessment |
|---|---|
| EP02-AC01–AC02 | Pass: authority, accepted decisions, baseline, pre-existing work, locks, and exact five-path scope recorded. |
| EP02-AC03–AC08 | Pass: small isolated public API; UUID/reference local shapes; deterministic full/semantic JSON; layout/order invariance; round trips; narrow safe decode rejection. |
| EP02-AC09–AC10 | Pass: deferred features remain absent; tests are inline, synthetic, deterministic, and bounded. |
| EP02-AC11–AC15 | Pass: required checks, clean-copy evidence, unchanged locks, cleanup, scope, whitespace, sensitive scan, and listener conclusion recorded. |
| EP02-AC16 | Pass: this report distinguishes worker work, pre-existing work, self-attestation, and pending independent validation. |
| EP02-AC17 | Pending: a fresh independent validator must reproduce and assess the packet. |
| EP02-AC18 | Pending: Central must explicitly accept P1-EP02. |

This is worker self-attestation only, not independent validation or Central
acceptance.  The next permitted action is independent validation under Section
11 of the packet; P1-EP03 remains unauthorized.

## 9. Independent-validation revision response

The worker addressed the returned `Revise` findings without expanding scope:

| Finding | Bounded correction | Regression evidence |
|---|---|---|
| EP02-AC05 / AC08: escaped lone surrogate made output non-UTF-8-encodable | All persisted JSON strings are now checked for UTF-8 encodability before construction or serialization. | The new UTF-8/deep-nesting test rejects an escaped lone-surrogate label and a direct constructor attempt; valid serialized output is UTF-8 encoded in the minimal round-trip test. |
| EP02-AC08 / AC16: explicit `label: null` was dropped; deep nesting leaked `RecursionError` | Decoder now distinguishes omitted labels from explicit labels, rejects non-string labels, and maps `RecursionError` to `WorkflowDecodeError`. | The new null-label test rejects that input; the UTF-8/deep-nesting test confirms the narrow local exception. |
| EP02-AC10: named order test did not construct values in reverse order | The helper now creates nodes and edges in reverse order independently of collection reversal. | The order test separately compares reverse construction and reverse collection order against the canonical output. |

This response is a renewed worker self-attestation, not a replacement for fresh
independent validation or Central acceptance.
