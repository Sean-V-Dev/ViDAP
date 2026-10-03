// Read-only views over a workflow document and the backend contracts.
// Nothing here invents a parameter value, range, or validity verdict.

import type {
  ContractParameter,
  ContractPort,
  JsonValue,
  NodeContract,
  WorkflowDocument,
  WorkflowEdge,
  WorkflowNode,
} from "./api";
import { REGIONS, UNASSIGNED, regionKeyForType } from "./presentation";

export type ContractIndex = ReadonlyMap<string, NodeContract>;

export function indexContracts(contracts: NodeContract[]): ContractIndex {
  return new Map(contracts.map((contract) => [contract.type, contract]));
}

/** The document's value, else the contract default, else nothing. */
export function effectiveValue(
  node: WorkflowNode,
  parameter: ContractParameter,
): JsonValue | undefined {
  const own = node.parameters?.[parameter.key];
  if (own !== undefined) {
    return own;
  }
  return parameter.default;
}

export function regionOf(node: WorkflowNode): string {
  return regionKeyForType(node.type);
}

/** Regions shown, in order; UNASSIGNED only when it has nodes. */
export function visibleRegions(document: WorkflowDocument | null): string[] {
  const keys = REGIONS.map((region) => region.key);
  if (document?.nodes.some((node) => regionOf(node) === UNASSIGNED.key)) {
    keys.push(UNASSIGNED.key);
  }
  return keys;
}

export function regionIndex(key: string): number {
  const index = REGIONS.findIndex((region) => region.key === key);
  return index === -1 ? REGIONS.length : index;
}

/**
 * DESIGN.md Section 4 naming: the node's label, else the type's display label,
 * followed by 1, 2, … in stable node-ID order when several nodes share a type.
 */
export function displayNames(
  document: WorkflowDocument,
  contracts: ContractIndex,
): Map<string, string> {
  const byType = new Map<string, WorkflowNode[]>();
  for (const node of document.nodes) {
    const list = byType.get(node.type) ?? [];
    list.push(node);
    byType.set(node.type, list);
  }
  const names = new Map<string, string>();
  for (const [type, nodes] of byType) {
    const sorted = [...nodes].sort((a, b) => a.id.localeCompare(b.id));
    const typeLabel = contracts.get(type)?.label ?? type;
    sorted.forEach((node, index) => {
      if (typeof node.label === "string" && node.label.length > 0) {
        names.set(node.id, node.label);
      } else {
        names.set(
          node.id,
          sorted.length > 1 ? `${typeLabel} ${index + 1}` : typeLabel,
        );
      }
    });
  }
  return names;
}

export function nodeById(
  document: WorkflowDocument,
  id: string,
): WorkflowNode | undefined {
  return document.nodes.find((node) => node.id === id);
}

export function portOf(
  contracts: ContractIndex,
  node: WorkflowNode,
  key: string,
  direction: "input" | "output",
): ContractPort | undefined {
  const contract = contracts.get(node.type);
  const ports = direction === "input" ? contract?.inputs : contract?.outputs;
  return ports?.find((port) => port.key === key);
}

export function isCrossRegion(
  document: WorkflowDocument,
  edge: WorkflowEdge,
): boolean {
  const source = nodeById(document, edge.source.nodeId);
  const target = nodeById(document, edge.target.nodeId);
  if (!source || !target) {
    return false;
  }
  return regionOf(source) !== regionOf(target);
}

export interface OutputEntry {
  nodeId: string;
  portKey: string;
  region: string;
  consumers: { nodeId: string; portKey: string }[];
}

export interface InputEntry {
  edgeId: string;
  nodeId: string;
  portKey: string;
  region: string;
  source: { nodeId: string; portKey: string; region: string };
}

/**
 * Boundary values (DESIGN.md Section 4): one Outputs entry per produced value
 * that leaves its region, and one Inputs entry per consuming port that takes a
 * value from another region. Matching is by canonical node ID and port key.
 */
export function boundaryEntries(document: WorkflowDocument): {
  outputs: OutputEntry[];
  inputs: InputEntry[];
} {
  const outputs = new Map<string, OutputEntry>();
  const inputs: InputEntry[] = [];
  for (const edge of document.edges) {
    const source = nodeById(document, edge.source.nodeId);
    const target = nodeById(document, edge.target.nodeId);
    if (!source || !target || regionOf(source) === regionOf(target)) {
      continue;
    }
    const key = `${edge.source.nodeId}\u0000${edge.source.portKey}`;
    if (!outputs.has(key)) {
      outputs.set(key, {
        nodeId: source.id,
        portKey: edge.source.portKey,
        region: regionOf(source),
        consumers: consumersOf(document, source.id, edge.source.portKey),
      });
    }
    inputs.push({
      edgeId: edge.id,
      nodeId: target.id,
      portKey: edge.target.portKey,
      region: regionOf(target),
      source: {
        nodeId: source.id,
        portKey: edge.source.portKey,
        region: regionOf(source),
      },
    });
  }
  return { outputs: [...outputs.values()], inputs };
}

export function consumersOf(
  document: WorkflowDocument,
  nodeId: string,
  portKey: string,
): { nodeId: string; portKey: string }[] {
  return document.edges
    .filter(
      (edge) =>
        edge.source.nodeId === nodeId && edge.source.portKey === portKey,
    )
    .map((edge) => ({
      nodeId: edge.target.nodeId,
      portKey: edge.target.portKey,
    }))
    .sort((a, b) =>
      a.nodeId === b.nodeId
        ? a.portKey.localeCompare(b.portKey)
        : a.nodeId.localeCompare(b.nodeId),
    );
}

export function localEdges(document: WorkflowDocument): WorkflowEdge[] {
  return document.edges.filter((edge) => {
    const source = nodeById(document, edge.source.nodeId);
    const target = nodeById(document, edge.target.nodeId);
    return !!source && !!target && regionOf(source) === regionOf(target);
  });
}

export interface Positioned {
  id: string;
  region: string;
  y: number;
}

function byRegionThenY(a: Positioned, b: Positioned): number {
  const order = regionIndex(a.region) - regionIndex(b.region);
  if (order !== 0) {
    return order;
  }
  return a.y === b.y ? a.id.localeCompare(b.id) : a.y - b.y;
}

/** Downstream nodes of a node: nearest region first, then top to bottom. */
export function downstream(
  document: WorkflowDocument,
  nodeId: string,
  positions: ReadonlyMap<string, Positioned>,
): string[] {
  const ids = new Set(
    document.edges
      .filter((edge) => edge.source.nodeId === nodeId)
      .map((edge) => edge.target.nodeId),
  );
  return [...ids]
    .map((id) => positions.get(id))
    .filter((item): item is Positioned => item !== undefined)
    .sort(byRegionThenY)
    .map((item) => item.id);
}

/** Upstream nodes: the nodes that feed this one, nearest region first. */
export function upstream(
  document: WorkflowDocument,
  nodeId: string,
  positions: ReadonlyMap<string, Positioned>,
): string[] {
  const ids = new Set(
    document.edges
      .filter((edge) => edge.target.nodeId === nodeId)
      .map((edge) => edge.source.nodeId),
  );
  return [...ids]
    .map((id) => positions.get(id))
    .filter((item): item is Positioned => item !== undefined)
    .sort((a, b) => byRegionThenY(b, a))
    .map((item) => item.id);
}

/** The nearest node above (-1) or below (+1) in the same region. */
export function verticalNeighbour(
  nodeId: string,
  direction: -1 | 1,
  positions: ReadonlyMap<string, Positioned>,
): string | null {
  const current = positions.get(nodeId);
  if (!current) {
    return null;
  }
  const candidates = [...positions.values()].filter(
    (item) =>
      item.id !== nodeId &&
      item.region === current.region &&
      (direction === 1 ? item.y > current.y : item.y < current.y),
  );
  candidates.sort((a, b) => (direction === 1 ? a.y - b.y : b.y - a.y));
  return candidates[0]?.id ?? null;
}

/** A deep copy with one parameter changed; nothing else in the document moves. */
export function withParameter(
  document: WorkflowDocument,
  nodeId: string,
  key: string,
  value: JsonValue,
): WorkflowDocument {
  const copy = structuredClone(document);
  const node = copy.nodes.find((item) => item.id === nodeId);
  if (node) {
    node.parameters = { ...(node.parameters ?? {}), [key]: value };
  }
  return copy;
}

export function formatValue(value: JsonValue | undefined): string {
  if (value === undefined) {
    return "—";
  }
  if (value === null) {
    return "None";
  }
  return typeof value === "string" ? value : JSON.stringify(value);
}
