// Graph authoring (P3-EP04B): pure edits to a workflow document. Each returns
// a new document and changes only `nodes` and `edges`; every other field, and
// every number spelling, is kept. Nothing here decides whether the result is
// valid: the backend's validation is the authority. The only contract checks
// are the early feedback DESIGN.md Section 4 allows (port types match) and the
// single-connection replacement (Section 5.4), both read from the contracts.

import type {
  ContractPort,
  Endpoint,
  NodeContract,
  WorkflowDocument,
  WorkflowEdge,
} from "./api";
import type { ContractIndex } from "./model";
import { nodeById, portOf } from "./model";
import { regionKeyForType } from "./presentation";

/** Lowercase UUIDv4 text, as the workflow format requires for every ID. */
export function newId(): string {
  return crypto.randomUUID();
}

export function newWorkflow(workflowId: string): WorkflowDocument {
  return {
    format: "vidap.workflow",
    schemaVersion: "1.0",
    workflowId,
    nodes: [],
    edges: [],
  };
}

/** The contract types that belong in a region, in the backend's order. */
export function typesForRegion(
  contracts: readonly NodeContract[],
  region: string,
): NodeContract[] {
  return contracts.filter(
    (contract) => regionKeyForType(contract.type) === region,
  );
}

/** A new node of `type` with no parameters: defaults stay in the contract. */
export function withNode(
  document: WorkflowDocument,
  id: string,
  type: string,
): WorkflowDocument {
  return {
    ...document,
    nodes: [...document.nodes, { id, type, parameters: {} }],
  };
}

export function edgesTouching(
  document: WorkflowDocument,
  nodeId: string,
): WorkflowEdge[] {
  return document.edges.filter(
    (edge) => edge.source.nodeId === nodeId || edge.target.nodeId === nodeId,
  );
}

/** The node and every connection touching it removed. */
export function withoutNode(
  document: WorkflowDocument,
  nodeId: string,
): WorkflowDocument {
  return {
    ...document,
    nodes: document.nodes.filter((node) => node.id !== nodeId),
    edges: document.edges.filter(
      (edge) => edge.source.nodeId !== nodeId && edge.target.nodeId !== nodeId,
    ),
  };
}

export function withoutEdge(
  document: WorkflowDocument,
  edgeId: string,
): WorkflowDocument {
  return {
    ...document,
    edges: document.edges.filter((edge) => edge.id !== edgeId),
  };
}

function port(
  document: WorkflowDocument,
  contracts: ContractIndex,
  endpoint: Endpoint,
  direction: "input" | "output",
): ContractPort | undefined {
  const node = nodeById(document, endpoint.nodeId);
  return node
    ? portOf(contracts, node, endpoint.portKey, direction)
    : undefined;
}

/** Early feedback only: the two ports' contract types are the same. */
export function compatible(
  document: WorkflowDocument,
  contracts: ContractIndex,
  source: Endpoint,
  target: Endpoint,
): boolean {
  const from = port(document, contracts, source, "output");
  const to = port(document, contracts, target, "input");
  return !!from && !!to && from.nominalType === to.nominalType;
}

export type ConnectOutcome =
  | { kind: "created"; document: WorkflowDocument; edge: WorkflowEdge }
  | {
      kind: "replaced";
      document: WorkflowDocument;
      edge: WorkflowEdge;
      replaced: WorkflowEdge[];
    }
  | { kind: "duplicate" }
  | { kind: "incompatible"; expected: string; offered: string };

/**
 * Connect `source` (an output) to `target` (an input). An exact duplicate is
 * not created; a port whose contract allows one connection has its existing
 * connection replaced.
 */
export function connect(
  document: WorkflowDocument,
  contracts: ContractIndex,
  source: Endpoint,
  target: Endpoint,
  edgeId: string,
): ConnectOutcome {
  const from = port(document, contracts, source, "output");
  const to = port(document, contracts, target, "input");
  if (!from || !to || from.nominalType !== to.nominalType) {
    return {
      kind: "incompatible",
      expected: to?.nominalType ?? "",
      offered: from?.nominalType ?? "",
    };
  }
  const into = document.edges.filter(
    (edge) =>
      edge.target.nodeId === target.nodeId &&
      edge.target.portKey === target.portKey,
  );
  if (
    into.some(
      (edge) =>
        edge.source.nodeId === source.nodeId &&
        edge.source.portKey === source.portKey,
    )
  ) {
    return { kind: "duplicate" };
  }
  const edge: WorkflowEdge = {
    id: edgeId,
    source: { ...source },
    target: { ...target },
  };
  if (to.cardinality === "one" && into.length > 0) {
    const replaced = new Set(into.map((item) => item.id));
    return {
      kind: "replaced",
      document: {
        ...document,
        edges: [
          ...document.edges.filter((item) => !replaced.has(item.id)),
          edge,
        ],
      },
      edge,
      replaced: into,
    };
  }
  return {
    kind: "created",
    document: { ...document, edges: [...document.edges, edge] },
    edge,
  };
}
