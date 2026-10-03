// Workspace geometry and the `vidap.workspace-view` sidecar (D3.4,
// DESIGN.md Sections 2–5). Positions are relative to a region's node area, so
// resizing a region never moves nodes in any other region. Nothing here
// touches the workflow document.

import type { NodeContract, Sidecar, WorkflowDocument } from "./api";
import type { Positioned } from "./model";
import { regionOf, visibleRegions } from "./model";

export const RAIL_WIDTH = 96;
export const NODE_WIDTH = 168;
export const EXPANDED_WIDTH = 290;
export const COMPACT_HEIGHT = 120;
export const EXPANDED_HEIGHT = 380;
export const REGION_HEADER = 40;
export const PAD = 16;
export const NODE_GAP = 24;
export const GUTTER_WIDTH = 24;
export const MAX_REGION_WIDTH = 900;
export const DEFAULT_REGION_WIDTH = 400;
export const PORT_TOP = 52;
export const PORT_STEP = 24;
export const RAIL_ENTRY_MIN_GAP = 48;
export const RAIL_ENTRY_SPACING = 4;
export const MOVE_STEP = 8;
export const MOVE_STEP_LARGE = 40;
export const GUTTER_STEP = 8;
export const GUTTER_STEP_LARGE = 40;

export interface Point {
  x: number;
  y: number;
}

export interface Layout {
  widths: Record<string, number>;
  positions: Record<string, Point>;
  viewport: { x: number; y: number; zoom: number };
}

export const ZOOM_LEVELS = [1, 0.85, 0.7] as const;

function nodesIn(document: WorkflowDocument, region: string) {
  return document.nodes
    .filter((node) => regionOf(node) === region)
    .sort((a, b) => a.id.localeCompare(b.id));
}

/** The narrowest width that still fits a region's nodes (DESIGN.md Section 4). */
export function minimumWidth(
  document: WorkflowDocument | null,
  region: string,
  positions: Record<string, Point>,
): number {
  let content = PAD * 2 + NODE_WIDTH;
  for (const node of document ? nodesIn(document, region) : []) {
    const position = positions[node.id];
    if (position) {
      content = Math.max(content, position.x + NODE_WIDTH + PAD);
    }
  }
  return Math.min(MAX_REGION_WIDTH, RAIL_WIDTH * 2 + content);
}

export function clampWidth(
  document: WorkflowDocument | null,
  region: string,
  positions: Record<string, Point>,
  width: number,
): number {
  const low = minimumWidth(document, region, positions);
  return Math.round(Math.min(MAX_REGION_WIDTH, Math.max(low, width)));
}

/**
 * Keep a moved node inside its region's node area: never above or left of it,
 * and never so far right that the region would no longer fit it. Moving never
 * resizes a region; the gutter does that.
 */
export function clampPosition(point: Point, regionWidth: number): Point {
  const right = Math.max(0, regionWidth - RAIL_WIDTH * 2 - NODE_WIDTH - PAD);
  return {
    x: Math.min(right, Math.max(0, point.x)),
    y: Math.max(0, point.y),
  };
}

/** Deterministic placement: one column, stacked in node-ID order. */
export function defaultPosition(index: number): Point {
  return { x: PAD, y: PAD + index * (COMPACT_HEIGHT + NODE_GAP) };
}

function isPoint(value: unknown): value is Point {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  const { x, y } = value as Record<string, unknown>;
  return (
    typeof x === "number" &&
    typeof y === "number" &&
    Number.isFinite(x) &&
    Number.isFinite(y)
  );
}

/**
 * Build the layout from a sidecar. Region membership is derived from the node
 * type; a sidecar entry for another region, or for an unknown node, is ignored.
 */
export function layoutFrom(
  document: WorkflowDocument,
  sidecar: Sidecar | null,
): { layout: Layout; usedDefaults: boolean } {
  const positions: Record<string, Point> = {};
  let usedDefaults = sidecar === null;
  for (const region of visibleRegions(document)) {
    let fallback = 0;
    for (const node of nodesIn(document, region)) {
      const saved = sidecar?.nodes[node.id];
      if (saved && saved.region === region && isPoint(saved)) {
        positions[node.id] = {
          x: Math.max(0, saved.x),
          y: Math.max(0, saved.y),
        };
      } else {
        positions[node.id] = defaultPosition(fallback);
        usedDefaults = true;
      }
      fallback += 1;
    }
  }
  const widths: Record<string, number> = {};
  for (const region of visibleRegions(document)) {
    const saved = sidecar?.regions.find((item) => item.key === region);
    widths[region] = clampWidth(
      document,
      region,
      positions,
      saved ? saved.width : DEFAULT_REGION_WIDTH,
    );
  }
  const viewport = sidecar?.viewport ?? { x: 0, y: 0, zoom: 1 };
  return {
    layout: {
      widths,
      positions,
      viewport: {
        x: Math.max(0, viewport.x),
        y: Math.max(0, viewport.y),
        zoom: (ZOOM_LEVELS as readonly number[]).includes(viewport.zoom)
          ? viewport.zoom
          : 1,
      },
    },
    usedDefaults,
  };
}

/** The sidecar for the current nodes only; stale node IDs are dropped. */
export function sidecarFrom(
  document: WorkflowDocument,
  layout: Layout,
): Sidecar {
  const nodes: Sidecar["nodes"] = {};
  for (const node of document.nodes) {
    const position = layout.positions[node.id];
    if (position) {
      nodes[node.id] = {
        region: regionOf(node),
        x: Math.round(position.x),
        y: Math.round(position.y),
      };
    }
  }
  return {
    format: "vidap.workspace-view",
    schemaVersion: "1.0",
    regions: visibleRegions(document).map((key) => ({
      key,
      width: layout.widths[key] ?? DEFAULT_REGION_WIDTH,
    })),
    nodes,
    viewport: { ...layout.viewport },
  };
}

/**
 * Temporary push-down (DESIGN.md Principle 3, walkthrough W4): while a node is
 * taller than compact (expanded, or showing a message), nodes below it in the
 * same region slide down by the extra height. `heights` holds measured node
 * heights; a node not measured yet uses its nominal height. Stored positions
 * never change; this returns display offsets only.
 */
export function pushDownOffsets(
  document: WorkflowDocument,
  positions: Record<string, Point>,
  expanded: string | null,
  heights: Readonly<Record<string, number>> = {},
): Record<string, number> {
  const offsets: Record<string, number> = {};
  for (const node of document.nodes) {
    const origin = positions[node.id];
    const extra = displayHeight(node.id, expanded, heights) - COMPACT_HEIGHT;
    if (!origin || extra <= 0) {
      continue;
    }
    const width = nodeWidth(node.id === expanded);
    for (const other of document.nodes) {
      const position = positions[other.id];
      if (
        other.id === node.id ||
        !position ||
        regionOf(other) !== regionOf(node) ||
        position.y <= origin.y
      ) {
        continue;
      }
      const overlaps =
        position.x < origin.x + width && position.x + NODE_WIDTH > origin.x;
      if (overlaps) {
        offsets[other.id] = (offsets[other.id] ?? 0) + extra;
      }
    }
  }
  return offsets;
}

export function nodeHeight(expanded: boolean): number {
  return expanded ? EXPANDED_HEIGHT : COMPACT_HEIGHT;
}

/** A node's measured height, or its nominal height before it is measured. */
export function displayHeight(
  id: string,
  expanded: string | null,
  heights: Readonly<Record<string, number>>,
): number {
  return heights[id] ?? nodeHeight(id === expanded);
}

export function nodeWidth(expanded: boolean): number {
  return expanded ? EXPANDED_WIDTH : NODE_WIDTH;
}

/** The vertical offset of a port inside its node. */
export function portOffset(
  contract: NodeContract | undefined,
  key: string,
  direction: "input" | "output",
): number {
  const ports =
    (direction === "input" ? contract?.inputs : contract?.outputs) ?? [];
  const index = Math.max(
    0,
    ports.findIndex((port) => port.key === key),
  );
  return PORT_TOP + index * PORT_STEP;
}

/**
 * Rail entry positions: each entry starts level with its port, then
 * overlapping entries stack downward by their measured heights so their text
 * never collides (DESIGN.md Section 4: rail text wraps, never truncated).
 */
export function stackRail(
  wanted: { id: string; y: number }[],
  heights: Readonly<Record<string, number>> = {},
): Map<string, number> {
  const placed = new Map<string, number>();
  let floor = -Infinity;
  for (const item of [...wanted].sort((a, b) =>
    a.y === b.y ? a.id.localeCompare(b.id) : a.y - b.y,
  )) {
    const y = Math.max(item.y, floor);
    placed.set(item.id, y);
    floor =
      y +
      Math.max(
        RAIL_ENTRY_MIN_GAP,
        (heights[item.id] ?? 0) + RAIL_ENTRY_SPACING,
      );
  }
  return placed;
}

export function positionedNodes(
  document: WorkflowDocument,
  positions: Record<string, Point>,
): Map<string, Positioned> {
  const result = new Map<string, Positioned>();
  for (const node of document.nodes) {
    const position = positions[node.id];
    if (position) {
      result.set(node.id, {
        id: node.id,
        region: regionOf(node),
        y: position.y,
      });
    }
  }
  return result;
}

export function regionHeight(
  document: WorkflowDocument | null,
  positions: Record<string, Point>,
  expanded: string | null,
  heights: Readonly<Record<string, number>> = {},
): number {
  let bottom = 320;
  if (document) {
    const offsets = pushDownOffsets(document, positions, expanded, heights);
    for (const node of document.nodes) {
      const position = positions[node.id];
      if (position) {
        bottom = Math.max(
          bottom,
          REGION_HEADER +
            position.y +
            (offsets[node.id] ?? 0) +
            displayHeight(node.id, expanded, heights) +
            PAD * 2,
        );
      }
    }
  }
  return bottom;
}
