import { describe, expect, it } from "vitest";
import type { WorkflowDocument } from "./api";
import {
  boundaryEntries,
  displayNames,
  downstream,
  effectiveValue,
  indexContracts,
  localEdges,
  upstream,
  verticalNeighbour,
  visibleRegions,
  withParameter,
} from "./model";
import { layoutFrom, positionedNodes } from "./layout";
import { recorded } from "./test-data/recorded";

const ID = (n: number) => `41000000-0000-4000-8000-00000000000${n}`;
const contracts = indexContracts(recorded.contracts);
const slice = (): WorkflowDocument =>
  structuredClone(recorded.loadExample.workflow);

function withSecondModel(document: WorkflowDocument): WorkflowDocument {
  const copy = structuredClone(document);
  copy.nodes.push({
    id: ID(6),
    type: "vidap.slice.model",
    parameters: { regularization: 2 },
  });
  return copy;
}

describe("model", () => {
  it("names nodes by label or type label, numbering shared types by ID", () => {
    const names = displayNames(slice(), contracts);
    expect(names.get(ID(1))).toBe("Dataset");
    expect(names.get(ID(4))).toBe("Model");
    const two = displayNames(withSecondModel(slice()), contracts);
    expect(two.get(ID(4))).toBe("Model 1");
    expect(two.get(ID(6))).toBe("Model 2");
    const labelled = slice();
    labelled.nodes[3].label = "Baseline";
    expect(displayNames(labelled, contracts).get(ID(4))).toBe("Baseline");
  });

  it("takes effective values from the document, then the contract default", () => {
    const model = recorded.contracts.find(
      (c) => c.type === "vidap.slice.model",
    )!;
    const parameter = model.parameters[0];
    const node = slice().nodes[3];
    expect(effectiveValue(node, parameter)).toBe(
      node.parameters?.[parameter.key],
    );
    const bare = { ...node, parameters: {} };
    expect(effectiveValue(bare, parameter)).toBe(parameter.default);
  });

  it("puts every value that leaves a region on exactly one Outputs entry", () => {
    const { outputs, inputs } = boundaryEntries(slice());
    const split = outputs.filter((entry) => entry.nodeId === ID(3));
    expect(split).toHaveLength(1);
    expect(split[0].consumers.map((c) => c.nodeId)).toEqual([ID(4), ID(5)]);
    // One Inputs entry per consuming port; the skip-region value arrives in
    // EVALUATE / COMPARE without touching MODEL.
    const intoEvaluate = inputs.filter((entry) => entry.nodeId === ID(5));
    expect(intoEvaluate.map((entry) => entry.source.nodeId).sort()).toEqual([
      ID(3),
      ID(4),
    ]);
    expect(inputs.every((entry) => entry.region !== entry.source.region)).toBe(
      true,
    );
    // In the slice every edge crosses a region, so there are no local wires.
    expect(localEdges(slice())).toEqual([]);
  });

  it("shows UNASSIGNED only when a node type has no region", () => {
    expect(visibleRegions(slice())).not.toContain("UNASSIGNED");
    const odd = slice();
    odd.nodes.push({ id: ID(7), type: "vidap.other.thing", parameters: {} });
    expect(visibleRegions(odd).at(-1)).toBe("UNASSIGNED");
    expect(visibleRegions(null)).toHaveLength(5);
  });

  it("navigates downstream nearest region first, upstream, and within a region", () => {
    const document = withSecondModel(slice());
    const { layout } = layoutFrom(document, null);
    const positions = positionedNodes(document, layout.positions);
    expect(downstream(document, ID(3), positions)).toEqual([ID(4), ID(5)]);
    expect(upstream(document, ID(5), positions)).toEqual([ID(4), ID(3)]);
    expect(verticalNeighbour(ID(4), 1, positions)).toBe(ID(6));
    expect(verticalNeighbour(ID(6), -1, positions)).toBe(ID(4));
    expect(verticalNeighbour(ID(4), -1, positions)).toBeNull();
  });

  it("changes one parameter without touching anything else", () => {
    const before = slice();
    const after = withParameter(before, ID(4), "regularization", 0.5);
    expect(after.nodes[3].parameters?.regularization).toBe(0.5);
    const restored = withParameter(after, ID(4), "regularization", 1);
    expect(restored).toEqual(before);
    expect(before.nodes[3].parameters?.regularization).toBe(1);
  });
});
