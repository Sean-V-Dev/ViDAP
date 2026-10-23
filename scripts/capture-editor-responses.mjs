// Capture the /api/slice/ responses the editor tests replay (P3-EP04B §5.7,
// extended in P3-EP05 §5.8 for /api/slice/run).
//
// Run from the repository root while `npm.cmd run launch` is running:
//   node scripts/capture-editor-responses.mjs [http://127.0.0.1:8000]
//
// It saves only `capture-*` workflows under .vidap-local/workflows/, removes
// the attempt directories it created under .vidap-local/runs/, restores or
// removes everything it changed, and writes
// apps/web/src/editor/test-data/recorded.ts (formatted with the locked
// Prettier), then prints that file's SHA-256 and size for the manifest.

import { Buffer } from "node:buffer";
import { createHash } from "node:crypto";
import { readdir, readFile, rm, rmdir, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import * as prettier from "prettier";

const root = fileURLToPath(new globalThis.URL("..", import.meta.url));
const workflows = `${root}.vidap-local/workflows/`;
const runs = `${root}.vidap-local/runs/`;
const fixture = `${root}fixtures/p3-ep03b/slice-success-v1.json`;
const output = `${root}apps/web/src/editor/test-data/recorded.ts`;
const base = process.argv[2] ?? "http://127.0.0.1:8000";
const CAPTURE_NAMES = ["capture-example", "capture-no-layout", "capture-empty"];

const id = (prefix, n) => `${prefix}000000-0000-4000-8000-00000000000${n}`;
const REGIONS = [
  "DATA",
  "PREPARE",
  "VALIDATE_SPLIT",
  "MODEL",
  "EVALUATE_COMPARE",
];
const SIDECAR = {
  format: "vidap.workspace-view",
  schemaVersion: "1.0",
  regions: REGIONS.map((key) => ({ key, width: 400 })),
  nodes: Object.fromEntries(
    REGIONS.map((region, index) => [
      id("41", index + 1),
      { region, x: 16, y: 16 },
    ]),
  ),
  viewport: { x: 0, y: 0, zoom: 1 },
};

// A workflow given as text is sent byte for byte, so number spellings such as
// `1.0` survive (JavaScript would re-serialize them as `1`).
const json = (value) =>
  typeof value === "string" ? value : JSON.stringify(value);

async function call(method, path, body, expected) {
  const response = await globalThis.fetch(`${base}/api/slice${path}`, {
    method,
    headers:
      body === undefined ? undefined : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : json(body),
  });
  const value = await response.json();
  if (response.status !== expected) {
    throw new Error(
      `${method} ${path}: expected ${expected}, got ${response.status} ${JSON.stringify(value)}`,
    );
  }
  return value;
}

const save = (name, workflow, sidecar, baseWorkflow, baseSidecar, expected) =>
  call(
    "PUT",
    `/workflows/${encodeURIComponent(name)}`,
    `{"workflow":${json(workflow)},"sidecar":${JSON.stringify(sidecar)},` +
      `"baseWorkflowDigest":${JSON.stringify(baseWorkflow)},` +
      `"baseSidecarDigest":${JSON.stringify(baseSidecar)}}`,
    expected,
  );

const compare = (name, workflow, loaded) =>
  call(
    "POST",
    `/workflows/${name}/compare`,
    `{"workflow":${json(workflow)},` +
      `"baseWorkflowDigest":${JSON.stringify(loaded.workflowDigest)},` +
      `"baseSidecarDigest":${JSON.stringify(loaded.sidecarDigest)}}`,
    200,
  );

async function removeCaptures(names) {
  for (const name of names) {
    for (const suffix of [".vidap.json", ".vidap-view.json"]) {
      await rm(`${workflows}${name}${suffix}`, { force: true });
    }
  }
}

async function removeRuns(attemptIds) {
  for (const attemptId of attemptIds) {
    if (typeof attemptId === "string" && attemptId.length > 0) {
      await rm(`${runs}${attemptId}`, { recursive: true, force: true });
    }
  }
  try {
    const remaining = await readdir(runs);
    if (remaining.length === 0) {
      await rmdir(runs);
    }
  } catch {
    // `.vidap-local/runs` does not exist or is non-empty.
  }
}

function sortKeys(value) {
  if (Array.isArray(value)) {
    return value.map(sortKeys);
  }
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, sortKeys(value[key])]),
    );
  }
  return value;
}

async function capture() {
  // `document` is the fixture's exact text; `clone()` is a parsed copy for
  // the deliberately changed variants, whose spellings do not matter.
  const document = await readFile(fixture, "utf8");
  const clone = () => JSON.parse(document);
  const out = {};

  await removeCaptures(CAPTURE_NAMES);

  out.contracts = (await call("GET", "/contracts", undefined, 200)).contracts;

  // Validation verdicts, one per diagnostic kind the editor renders.
  out.validateValid = await call("POST", "/validate", document, 200);
  const invalid = clone();
  invalid.nodes[3].parameters.regularization = 0;
  out.validateInvalid = await call("POST", "/validate", invalid, 200);
  const empty = {
    format: "vidap.workflow",
    schemaVersion: "1.0",
    workflowId: id("40", 2),
    nodes: [],
    edges: [],
  };
  out.validateEmpty = await call("POST", "/validate", empty, 200);
  const missingInput = clone();
  missingInput.edges = missingInput.edges.filter(
    (edge) => edge.target.nodeId !== id("41", 4),
  );
  out.validateMissingInput = await call("POST", "/validate", missingInput, 200);
  const mismatch = clone();
  mismatch.edges[4].source = { nodeId: id("41", 4), portKey: "model" };
  out.validateTypeMismatch = await call("POST", "/validate", mismatch, 200);
  const cycle = {
    format: "vidap.workflow",
    schemaVersion: "1.0",
    workflowId: id("40", 3),
    nodes: [1, 2].map((n) => ({
      id: id("43", n),
      type: "vidap.slice.prepare",
      parameters: {},
    })),
    edges: [
      [1, 2],
      [2, 1],
    ].map(([from, to], index) => ({
      id: id("44", index + 1),
      source: { nodeId: id("43", from), portKey: "prepared" },
      target: { nodeId: id("43", to), portKey: "table" },
    })),
  };
  out.validateCycle = await call("POST", "/validate", cycle, 200);

  // Saving and loading.
  out.saveExample = await save(
    "capture-example",
    document,
    SIDECAR,
    null,
    null,
    200,
  );
  out.saveNoLayout = await save(
    "capture-no-layout",
    document,
    null,
    null,
    null,
    200,
  );
  out.list = (await call("GET", "/workflows", undefined, 200)).workflows;
  out.loadExample = await call(
    "GET",
    "/workflows/capture-example",
    undefined,
    200,
  );
  out.loadNoLayout = await call(
    "GET",
    "/workflows/capture-no-layout",
    undefined,
    200,
  );
  out.notFound = await call("GET", "/workflows/capture-absent", undefined, 404);
  const incomplete = {
    ...empty,
    workflowId: id("40", 4),
    nodes: [{ id: id("41", 4), type: "vidap.slice.model", parameters: {} }],
  };
  out.saveRefused = await save(
    "capture-incomplete",
    incomplete,
    null,
    null,
    null,
    422,
  );
  out.saveBadName = await save("Capture Bad", empty, null, null, null, 400);
  out.saveNameTaken = await save(
    "capture-no-layout",
    document,
    null,
    null,
    null,
    409,
  );
  out.saveEmpty = await save("capture-empty", empty, null, null, null, 200);
  await removeCaptures(["capture-empty"]);

  // An outside edit: refused save, then compare before and after restoring.
  const path = `${workflows}capture-example.vidap.json`;
  const original = await readFile(path);
  const text = original.toString("utf8");
  const edited = text.replace('"regularization": 1.0', '"regularization": 0.5');
  if (edited === text) {
    throw new Error("capture-example has no regularization 1.0 to edit");
  }
  const loaded = out.loadExample;
  try {
    await writeFile(path, edited, "utf8");
    out.saveConflict = await save(
      "capture-example",
      document,
      SIDECAR,
      loaded.workflowDigest,
      loaded.sidecarDigest,
      409,
    );
    out.compareChanged = await compare("capture-example", document, loaded);
  } finally {
    await writeFile(path, original);
  }
  out.compareUnchanged = await compare("capture-example", document, loaded);

  // Slice execution: baseline success, regularized variant, declared runtime
  // failure (with completed, failed, blocked, and unrelated node statuses),
  // and refused non-slice workflow.
  const createdAttempts = [];
  try {
    out.runSuccess = await call("POST", "/run", document, 200);
    createdAttempts.push(out.runSuccess.attemptId);

    const regularized = document.replace(
      '"regularization": 1.0',
      '"regularization": 0.0001',
    );
    if (regularized === document) {
      throw new Error("fixture has no regularization 1.0 to replace");
    }
    out.runRegularized = await call("POST", "/run", regularized, 200);
    createdAttempts.push(out.runRegularized.attemptId);

    // Dataset (41..1) feeds both Train/Test Split (41..3) and an unconsumed
    // Prepare Data (41..6), bypassing Prepare Data on the path to Model (41..4)
    // and Evaluate (41..5). Schedule order is 41..1 (completed), 41..3
    // (completed), 41..4 (failed: unencoded-category-input), 41..5 (blocked),
    // and 41..6 (unrelated).
    const unencoded = clone();
    unencoded.nodes[1] = {
      ...unencoded.nodes[1],
      id: id("41", 6),
    };
    unencoded.edges[0] = {
      ...unencoded.edges[0],
      target: { nodeId: id("41", 6), portKey: "table" },
    };
    unencoded.edges[1] = {
      ...unencoded.edges[1],
      source: { nodeId: id("41", 1), portKey: "table" },
      target: { nodeId: id("41", 3), portKey: "table" },
    };
    out.runFailed = await call("POST", "/run", unencoded, 200);
    createdAttempts.push(out.runFailed.attemptId);

    out.runRefused = await call("POST", "/run", empty, 422);
  } finally {
    await removeRuns(createdAttempts);
  }

  return sortKeys(out);
}

const KEYS = {
  contracts: "NodeContract[]",
  validateValid: "ValidateResult",
  validateInvalid: "ValidateResult",
  validateEmpty: "ValidateResult",
  validateMissingInput: "ValidateResult",
  validateTypeMismatch: "ValidateResult",
  validateCycle: "ValidateResult",
  saveExample: "SaveResult",
  saveNoLayout: "SaveResult",
  saveEmpty: "SaveResult",
  list: "WorkflowSummary[]",
  loadExample: "LoadedWorkflow",
  loadNoLayout: "LoadedWorkflow",
  notFound: "ErrorBody",
  saveRefused: "ErrorBody",
  saveBadName: "ErrorBody",
  saveNameTaken: "ErrorBody",
  saveConflict: "ErrorBody",
  compareChanged: "CompareResult",
  compareUnchanged: "CompareResult",
  runSuccess: "RunResult",
  runRegularized: "RunResult",
  runFailed: "RunResult",
  runRefused: "ErrorBody",
};

const result = await capture();
const missing = Object.keys(KEYS).filter((key) => !(key in result));
if (missing.length > 0) {
  throw new Error(`missing captures: ${missing.join(", ")}`);
}
const source = `// Recorded responses captured from the real /api/slice/ backend for the
// editor tests. Regenerate with \`node scripts/capture-editor-responses.mjs\`
// while \`npm.cmd run launch\` runs; do not edit by hand.

import type {
  CompareResult,
  Diagnostic,
  LoadedWorkflow,
  NodeContract,
  RunResult,
  SaveResult,
  ValidateResult,
  WorkflowSummary,
} from "../api";

export interface ErrorBody {
  error: { code: string; message: string };
  diagnostics?: Diagnostic[];
  [key: string]: unknown;
}

export interface Recorded {
${Object.entries(KEYS)
  .map(([key, type]) => `  ${key}: ${type};`)
  .join("\n")}
}

export const recorded: Recorded = ${JSON.stringify(result, null, 2)};
`;
const options = (await prettier.resolveConfig(output)) ?? {};
const formatted = await prettier.format(source, {
  ...options,
  filepath: output,
});
await writeFile(output, formatted, "utf8");
const bytes = Buffer.byteLength(formatted, "utf8");
const sha256 = createHash("sha256")
  .update(formatted)
  .digest("hex")
  .toUpperCase();
console.log(
  `captured ${Object.keys(result).length} responses to apps/web/src/editor/test-data/recorded.ts`,
);
console.log(`sha256 ${sha256}  bytes ${bytes}`);
