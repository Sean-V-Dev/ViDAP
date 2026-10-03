import { describe, expect, it } from "vitest";
import type { Sidecar, WorkflowDocument } from "./api";
import {
  COMPACT_HEIGHT,
  EXPANDED_HEIGHT,
  MAX_REGION_WIDTH,
  NODE_WIDTH,
  PAD,
  RAIL_ENTRY_MIN_GAP,
  RAIL_ENTRY_SPACING,
  RAIL_WIDTH,
  REGION_HEADER,
  clampPosition,
  clampWidth,
  layoutFrom,
  minimumWidth,
  pushDownOffsets,
  regionHeight,
  sidecarFrom,
  stackRail,
} from "./layout";
import { recorded } from "./test-data/recorded";

const ID = (n: number) => `41000000-0000-4000-8000-00000000000${n}`;
const slice = (): WorkflowDocument =>
  structuredClone(recorded.loadExample.workflow);
const savedSidecar = (): Sidecar =>
  structuredClone(recorded.loadExample.sidecar!);

describe("layout", () => {
  it("restores the saved sidecar and keeps positions region-relative", () => {
    const { layout, usedDefaults } = layoutFrom(slice(), savedSidecar());
    expect(usedDefaults).toBe(false);
    expect(layout.positions[ID(4)]).toEqual({ x: 16, y: 16 });
    expect(layout.widths.MODEL).toBe(400);
  });

  it("falls back to deterministic placement and drops stale or misplaced entries", () => {
    const sidecar = savedSidecar();
    sidecar.nodes[ID(4)].region = "DATA";
    sidecar.nodes["49999999-0000-4000-8000-000000000000"] = {
      region: "DATA",
      x: 5,
      y: 5,
    };
    const { layout, usedDefaults } = layoutFrom(slice(), sidecar);
    expect(usedDefaults).toBe(true);
    expect(layout.positions[ID(4)]).toEqual({ x: PAD, y: PAD });
    const written = sidecarFrom(slice(), layout);
    expect(Object.keys(written.nodes).sort()).toEqual([1, 2, 3, 4, 5].map(ID));
    expect(written.nodes[ID(4)].region).toBe("MODEL");
  });

  it("clamps region widths between fitting the nodes and 900", () => {
    const document = slice();
    const positions = { [ID(1)]: { x: 300, y: 16 } };
    const minimum = minimumWidth(document, "DATA", positions);
    expect(minimum).toBe(RAIL_WIDTH * 2 + 300 + NODE_WIDTH + PAD);
    expect(clampWidth(document, "DATA", positions, 10)).toBe(minimum);
    expect(clampWidth(document, "DATA", positions, 5000)).toBe(
      MAX_REGION_WIDTH,
    );
  });

  it("keeps a moved node inside its region, so the region still fits it", () => {
    const document = slice();
    const right = 400 - RAIL_WIDTH * 2 - NODE_WIDTH - PAD;
    const kept = clampPosition({ x: 5000, y: -20 }, 400);
    expect(kept).toEqual({ x: right, y: 0 });
    expect(minimumWidth(document, "DATA", { [ID(1)]: kept })).toBe(400);
    expect(clampPosition({ x: -5, y: 30 }, 400)).toEqual({ x: 0, y: 30 });
  });

  it("pushes down only nodes below an expanded node in the same region", () => {
    const document = slice();
    document.nodes.push({
      id: ID(6),
      type: "vidap.slice.model",
      parameters: {},
    });
    const positions = {
      [ID(4)]: { x: 16, y: 16 },
      [ID(6)]: { x: 16, y: 160 },
      [ID(5)]: { x: 16, y: 160 },
    };
    expect(pushDownOffsets(document, positions, ID(4))).toEqual({
      [ID(6)]: EXPANDED_HEIGHT - COMPACT_HEIGHT,
    });
    expect(pushDownOffsets(document, positions, null)).toEqual({});
    expect(positions[ID(6)]).toEqual({ x: 16, y: 160 });
  });

  it("pushes down by measured height, so a node showing a message is never covered", () => {
    const document = slice();
    document.nodes.push({
      id: ID(6),
      type: "vidap.slice.model",
      parameters: {},
    });
    const positions = {
      [ID(4)]: { x: 16, y: 16 },
      [ID(6)]: { x: 16, y: 160 },
    };
    // Compact, not expanded, but 80 px taller while it shows a message.
    const heights = { [ID(4)]: COMPACT_HEIGHT + 80, [ID(6)]: COMPACT_HEIGHT };
    expect(pushDownOffsets(document, positions, null, heights)).toEqual({
      [ID(6)]: 80,
    });
    // The region grows to hold the pushed node at its measured height.
    expect(regionHeight(document, positions, null, heights)).toBe(
      REGION_HEADER + 160 + 80 + COMPACT_HEIGHT + PAD * 2,
    );
  });

  it("stacks rail entries by their measured heights", () => {
    const placed = stackRail(
      [
        { id: "a", y: 100 },
        { id: "b", y: 110 },
      ],
      { a: 64 },
    );
    expect(placed.get("b")).toBe(100 + 64 + RAIL_ENTRY_SPACING);
  });

  it("stacks rail entries so they never overlap", () => {
    const placed = stackRail([
      { id: "a", y: 100 },
      { id: "b", y: 110 },
      { id: "c", y: 400 },
    ]);
    expect(placed.get("a")).toBe(100);
    expect(placed.get("b")).toBe(100 + RAIL_ENTRY_MIN_GAP);
    expect(placed.get("c")).toBe(400);
  });
});
