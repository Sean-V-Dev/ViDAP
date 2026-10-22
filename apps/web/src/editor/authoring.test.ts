import { describe, expect, it } from "vitest";
import type { WorkflowDocument } from "./api";
import {
  compatible,
  connect,
  edgesTouching,
  newId,
  newWorkflow,
  typesForRegion,
  withNode,
  withoutEdge,
  withoutNode,
} from "./authoring";
import { indexContracts } from "./model";
import { recorded } from "./test-data/recorded";

const ID = (n: number) => `41000000-0000-4000-8000-00000000000${n}`;
const UUID4 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const contracts = indexContracts(recorded.contracts);
const slice = (): WorkflowDocument =>
  structuredClone(recorded.loadExample.workflow);
const at = (nodeId: string, portKey: string) => ({ nodeId, portKey });

describe("authoring (P3-EP04B)", () => {
  it("starts an empty workflow with a fresh lowercase UUIDv4", () => {
    const id = newId();
    expect(id).toMatch(UUID4);
    expect(newId()).not.toBe(id);
    expect(newWorkflow(id)).toEqual({
      format: "vidap.workflow",
      schemaVersion: "1.0",
      workflowId: id,
      nodes: [],
      edges: [],
    });
  });

  it("offers each region exactly the contract types mapped to it", () => {
    expect(
      typesForRegion(recorded.contracts, "MODEL").map((item) => item.type),
    ).toEqual(["vidap.slice.model"]);
    expect(typesForRegion(recorded.contracts, "UNASSIGNED")).toEqual([]);
    const extra = { ...recorded.contracts[3], type: "vidap.slice.model-b" };
    expect(typesForRegion([...recorded.contracts, extra], "MODEL")).toEqual([
      recorded.contracts[3],
    ]);
  });

  it("adds a node with no parameters and touches nothing else", () => {
    const before = slice();
    const after = withNode(before, ID(6), "vidap.slice.model");
    expect(after.nodes.at(-1)).toEqual({
      id: ID(6),
      type: "vidap.slice.model",
      parameters: {},
    });
    expect(after.nodes.slice(0, -1)).toEqual(before.nodes);
    expect(after.edges).toEqual(before.edges);
    expect({ ...after, nodes: [] }).toEqual({ ...before, nodes: [] });
  });

  it("removes a node together with every connection touching it", () => {
    const before = slice();
    expect(edgesTouching(before, ID(3))).toHaveLength(3);
    const after = withoutNode(before, ID(3));
    expect(after.nodes.map((node) => node.id)).not.toContain(ID(3));
    expect(after.edges.map((edge) => edge.id)).toEqual([
      "42000000-0000-4000-8000-000000000001",
      "42000000-0000-4000-8000-000000000004",
    ]);
    expect(withoutEdge(before, before.edges[0].id).edges).toEqual(
      before.edges.slice(1),
    );
  });

  it("marks compatibility from contract port types only", () => {
    const document = slice();
    expect(
      compatible(document, contracts, at(ID(3), "split"), at(ID(5), "split")),
    ).toBe(true);
    expect(
      compatible(document, contracts, at(ID(4), "model"), at(ID(5), "split")),
    ).toBe(false);
    // Changing a port's type in the contract changes the answer.
    const changed = structuredClone(recorded.contracts);
    changed[4].inputs[1].nominalType = "model";
    expect(
      compatible(
        document,
        indexContracts(changed),
        at(ID(4), "model"),
        at(ID(5), "split"),
      ),
    ).toBe(true);
  });

  it("creates, replaces a single-connection input, and refuses duplicates", () => {
    const empty = withNode(
      withNode(newWorkflow(newId()), ID(3), "vidap.slice.split"),
      ID(4),
      "vidap.slice.model",
    );
    const created = connect(
      empty,
      contracts,
      at(ID(3), "split"),
      at(ID(4), "split"),
      "edge-1",
    );
    expect(created.kind).toBe("created");
    if (created.kind !== "created") {
      return;
    }
    expect(created.document.edges).toEqual([
      { id: "edge-1", source: at(ID(3), "split"), target: at(ID(4), "split") },
    ]);
    expect(
      connect(
        created.document,
        contracts,
        at(ID(3), "split"),
        at(ID(4), "split"),
        "edge-2",
      ),
    ).toEqual({ kind: "duplicate" });
    const second = withNode(created.document, ID(6), "vidap.slice.split");
    const replaced = connect(
      second,
      contracts,
      at(ID(6), "split"),
      at(ID(4), "split"),
      "edge-3",
    );
    expect(replaced.kind).toBe("replaced");
    if (replaced.kind === "replaced") {
      expect(replaced.replaced.map((edge) => edge.id)).toEqual(["edge-1"]);
      expect(replaced.document.edges.map((edge) => edge.id)).toEqual([
        "edge-3",
      ]);
    }
    expect(
      connect(
        empty,
        contracts,
        at(ID(4), "model"),
        at(ID(4), "split"),
        "edge-4",
      ),
    ).toEqual({ kind: "incompatible", expected: "split", offered: "model" });
  });
});
