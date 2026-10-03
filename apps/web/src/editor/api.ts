// The only client for the accepted `/api/slice/` channel. Every value the
// editor shows about node types, parameters, validity, and saved files comes
// through here; the editor computes none of it itself.

export type JsonValue =
  null | boolean | number | string | JsonValue[] | { [key: string]: JsonValue };

export interface ContractPort {
  key: string;
  nominalType: string;
  label: string;
  cardinality: string | null;
  required: boolean | null;
}

export interface ContractParameter {
  key: string;
  kind: string;
  required: boolean;
  label: string;
  description: string | null;
  default?: JsonValue;
  constraints: Record<string, JsonValue>;
}

export interface NodeContract {
  type: string;
  label: string;
  description: string | null;
  inputs: ContractPort[];
  outputs: ContractPort[];
  parameters: ContractParameter[];
}

export interface Endpoint {
  nodeId: string;
  portKey: string;
}

export interface WorkflowNode {
  id: string;
  type: string;
  label?: string;
  parameters?: Record<string, JsonValue>;
  [key: string]: JsonValue | undefined;
}

export interface WorkflowEdge {
  id: string;
  source: Endpoint;
  target: Endpoint;
  [key: string]: JsonValue | Endpoint | undefined;
}

export interface WorkflowDocument {
  format: string;
  schemaVersion: string;
  workflowId: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  [key: string]: JsonValue | WorkflowNode[] | WorkflowEdge[] | undefined;
}

export interface Diagnostic {
  code: string;
  severity: string;
  category: string;
  elementKind: string;
  elementReference: string;
  message: string;
  remedy: string;
  jsonPointer: string | null;
}

export interface ValidateResult {
  valid: boolean;
  diagnostics: Diagnostic[];
}

export interface SidecarRegion {
  key: string;
  width: number;
}

export interface SidecarNode {
  region: string;
  x: number;
  y: number;
}

export interface Sidecar {
  format: "vidap.workspace-view";
  schemaVersion: "1.0";
  regions: SidecarRegion[];
  nodes: Record<string, SidecarNode>;
  viewport: { x: number; y: number; zoom: number };
}

export interface WorkflowSummary {
  name: string;
  workflowDigest: string;
  hasSidecar: boolean;
}

export interface LoadedWorkflow {
  name: string;
  workflow: WorkflowDocument;
  workflowDigest: string;
  sidecar: Sidecar | null;
  sidecarDigest: string | null;
  sidecarNotice: "unreadable" | "unsupported" | null;
}

export interface SaveResult {
  name: string;
  workflowDigest: string;
  sidecarDigest: string | null;
}

export interface ChangeSummary {
  nodesAdded?: { nodeId: string; type: string }[];
  nodesRemoved?: { nodeId: string; type: string }[];
  edgesAdded?: { edgeId: string; source: Endpoint; target: Endpoint }[];
  edgesRemoved?: { edgeId: string; source: Endpoint; target: Endpoint }[];
  parametersChanged?: {
    nodeId: string;
    key: string;
    before: JsonValue;
    after: JsonValue;
  }[];
  labelsChanged?: string[];
  layoutMetadataChanged?: boolean;
  diskUnreadable?: boolean;
}

export interface CompareResult {
  changed: boolean;
  missing: boolean;
  workflowDigest: string | null;
  sidecarDigest: string | null;
  summary: ChangeSummary | null;
}

/** A refusal from the backend: only its fixed code, message, and listed extras. */
export class ApiError extends Error {
  readonly code: string;
  readonly status: number;
  readonly diagnostics: Diagnostic[];
  readonly workflowDigest: string | null;
  readonly sidecarDigest: string | null;
  readonly missing: boolean;
  readonly summary: ChangeSummary | null;

  constructor(status: number, body: unknown) {
    const envelope = readEnvelope(status, body);
    super(envelope.message);
    this.name = "ApiError";
    this.status = status;
    this.code = envelope.code;
    const extra = isRecord(body) ? body : {};
    this.diagnostics = Array.isArray(extra.diagnostics)
      ? (extra.diagnostics as Diagnostic[])
      : [];
    this.workflowDigest =
      typeof extra.workflowDigest === "string" ? extra.workflowDigest : null;
    this.sidecarDigest =
      typeof extra.sidecarDigest === "string" ? extra.sidecarDigest : null;
    this.missing = extra.missing === true;
    const summary: unknown = extra.summary;
    this.summary = isRecord(summary) ? summary : null;
  }
}

const UNAVAILABLE = {
  code: "unavailable",
  message: "The local ViDAP backend could not be reached.",
};

// The backend answered, but not with the fixed envelope; its text is not shown.
const UNEXPLAINED = {
  code: "unexplained",
  message:
    "The local ViDAP backend refused the request without an explanation.",
};

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function readEnvelope(
  status: number,
  body: unknown,
): { code: string; message: string } {
  if (isRecord(body) && isRecord(body.error)) {
    const { code, message } = body.error;
    if (typeof code === "string" && typeof message === "string") {
      return { code, message };
    }
  }
  return status === 0 ? UNAVAILABLE : UNEXPLAINED;
}

export interface SliceClient {
  contracts(): Promise<NodeContract[]>;
  validate(document: WorkflowDocument): Promise<ValidateResult>;
  list(): Promise<WorkflowSummary[]>;
  load(name: string): Promise<LoadedWorkflow>;
  save(
    name: string,
    document: WorkflowDocument,
    sidecar: Sidecar | null,
    baseWorkflowDigest: string | null,
    baseSidecarDigest: string | null,
  ): Promise<SaveResult>;
  compare(
    name: string,
    document: WorkflowDocument,
    baseWorkflowDigest: string | null,
    baseSidecarDigest: string | null,
  ): Promise<CompareResult>;
}

type Fetch = (input: string, init?: RequestInit) => Promise<Response>;

/**
 * Number spelling (P3-AC08, D3.3). A browser reads `1.0` and `1` as the same
 * number, but the backend's semantic identity tells them apart. The client
 * keeps the spelling of every number in a loaded workflow and writes a number
 * the user has not changed back exactly as it was read, so a layout-only save
 * never rewrites a parameter.
 */
export type Spellings = ReadonlyMap<string, string>;

const NUMBER = /-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/y;

function pointerToken(key: string): string {
  return key.replace(/~/g, "~0").replace(/\//g, "~1");
}

/** Every number in a JSON text whose spelling differs from the browser's. */
export function numberSpellings(text: string): Map<string, string> {
  JSON.parse(text);
  const spellings = new Map<string, string>();
  let index = 0;
  const skipSpace = () => {
    while (index < text.length && " \t\n\r".includes(text.charAt(index))) {
      index += 1;
    }
  };
  const readString = (): string => {
    const start = index;
    index += 1;
    while (text.charAt(index) !== '"') {
      index += text.charAt(index) === "\\" ? 2 : 1;
    }
    index += 1;
    return JSON.parse(text.slice(start, index)) as string;
  };
  const walk = (pointer: string): void => {
    skipSpace();
    const first = text.charAt(index);
    if (first === "{" || first === "[") {
      const object = first === "{";
      index += 1;
      let position = 0;
      skipSpace();
      while (text.charAt(index) !== (object ? "}" : "]")) {
        let token = String(position);
        if (object) {
          skipSpace();
          token = pointerToken(readString());
          skipSpace();
          index += 1;
        }
        walk(`${pointer}/${token}`);
        position += 1;
        skipSpace();
        if (text.charAt(index) === ",") {
          index += 1;
          skipSpace();
        }
      }
      index += 1;
      return;
    }
    if (first === '"') {
      readString();
      return;
    }
    NUMBER.lastIndex = index;
    const number = NUMBER.exec(text);
    if (number) {
      const spelled = number[0];
      index += spelled.length;
      if (JSON.stringify(Number(spelled)) !== spelled) {
        spellings.set(pointer, spelled);
      }
      return;
    }
    index += first === "f" ? 5 : 4;
  };
  walk("");
  return spellings;
}

/**
 * JSON text for a value, writing each number whose kept spelling still names
 * the same number with that spelling. Everything else matches JSON.stringify.
 */
export function writeJson(
  value: unknown,
  spellingAt: (pointer: string) => string | undefined,
  pointer = "",
): string {
  if (typeof value === "number") {
    const spelled = spellingAt(pointer);
    return spelled !== undefined && Object.is(Number(spelled), value)
      ? spelled
      : JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    const items = value.map((item: unknown, position) =>
      writeJson(item, spellingAt, `${pointer}/${position}`),
    );
    return `[${items.join(",")}]`;
  }
  if (isRecord(value)) {
    const members: string[] = [];
    for (const [key, item] of Object.entries(value)) {
      if (item !== undefined) {
        members.push(
          `${JSON.stringify(key)}:${writeJson(item, spellingAt, `${pointer}/${pointerToken(key)}`)}`,
        );
      }
    }
    return `{${members.join(",")}}`;
  }
  return JSON.stringify(value) ?? "null";
}

const WORKFLOW = "/workflow";

function within(spellings: Spellings, prefix: string) {
  return (pointer: string) =>
    pointer.startsWith(`${prefix}/`)
      ? spellings.get(pointer.slice(prefix.length))
      : undefined;
}

async function call<T>(
  fetcher: Fetch,
  method: string,
  path: string,
  body?: string,
): Promise<{ value: T; text: string }> {
  let response: Response;
  try {
    response = await fetcher(`/api/slice${path}`, {
      method,
      headers:
        body === undefined ? undefined : { "Content-Type": "application/json" },
      body,
    });
  } catch {
    throw new ApiError(0, null);
  }
  let text = "";
  let parsed: unknown;
  try {
    text = await response.text();
    parsed = JSON.parse(text);
  } catch {
    parsed = null;
  }
  if (!response.ok) {
    throw new ApiError(response.status, parsed);
  }
  return { value: parsed as T, text };
}

export function createSliceClient(
  fetcher: Fetch = (input, init) => fetch(input, init),
): SliceClient {
  const named = (name: string) => `/workflows/${encodeURIComponent(name)}`;
  // Kept spellings, by workflowId, for the workflows this client has loaded.
  const kept = new Map<string, Spellings>();
  const spellingsOf = (document: WorkflowDocument): Spellings =>
    kept.get(document.workflowId) ?? new Map<string, string>();
  return {
    async contracts() {
      const result = await call<{ contracts: NodeContract[] }>(
        fetcher,
        "GET",
        "/contracts",
      );
      return result.value.contracts;
    },
    async validate(document) {
      const result = await call<ValidateResult>(
        fetcher,
        "POST",
        "/validate",
        writeJson(document, within(spellingsOf(document), "")),
      );
      return result.value;
    },
    async list() {
      const result = await call<{ workflows: WorkflowSummary[] }>(
        fetcher,
        "GET",
        "/workflows",
      );
      return result.value.workflows;
    },
    async load(name) {
      const result = await call<LoadedWorkflow>(fetcher, "GET", named(name));
      const all = numberSpellings(result.text);
      const own = new Map<string, string>();
      for (const [pointer, spelled] of all) {
        if (pointer.startsWith(`${WORKFLOW}/`)) {
          own.set(pointer.slice(WORKFLOW.length), spelled);
        }
      }
      kept.set(result.value.workflow.workflowId, own);
      return result.value;
    },
    async save(name, document, sidecar, baseWorkflowDigest, baseSidecarDigest) {
      const body = {
        workflow: document,
        sidecar,
        baseWorkflowDigest,
        baseSidecarDigest,
      };
      const result = await call<SaveResult>(
        fetcher,
        "PUT",
        named(name),
        writeJson(body, within(spellingsOf(document), WORKFLOW)),
      );
      return result.value;
    },
    async compare(name, document, baseWorkflowDigest, baseSidecarDigest) {
      const body = {
        workflow: document,
        baseWorkflowDigest,
        baseSidecarDigest,
      };
      const result = await call<CompareResult>(
        fetcher,
        "POST",
        `${named(name)}/compare`,
        writeJson(body, within(spellingsOf(document), WORKFLOW)),
      );
      return result.value;
    },
  };
}
