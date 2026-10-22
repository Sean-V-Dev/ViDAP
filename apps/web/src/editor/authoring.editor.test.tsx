import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ApiError, type WorkflowDocument } from "./api";
import { Editor } from "./Editor";
import {
  COMPACT_HEIGHT,
  NODE_GAP,
  PAD,
  RAIL_WIDTH,
  REGION_HEADER,
} from "./layout";
import { recorded } from "./test-data/recorded";
import {
  ID,
  clone,
  node,
  openExample,
  regionOf,
  stubClient,
  type StubClient,
} from "./test-support";

const UUID4 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const status = () => screen.getByRole("status").textContent ?? "";
const lastValidated = (client: StubClient): WorkflowDocument =>
  client.validate.mock.calls.at(-1)![0];
const port = (scope: HTMLElement, name: RegExp) =>
  within(scope).getByRole("button", { name });

async function startNew(client: StubClient) {
  render(<Editor client={client} />);
  await waitFor(() => expect(client.contracts).toHaveBeenCalled());
  fireEvent.click(screen.getByRole("button", { name: "New" }));
  await waitFor(() => expect(client.validate).toHaveBeenCalled());
}

function add(region: string, label: string) {
  fireEvent.click(
    screen.getByRole("button", { name: `Add node to ${region}` }),
  );
  fireEvent.click(screen.getByRole("menuitem", { name: label }));
}

describe("Graph authoring (P3-EP04B)", () => {
  it("starts an untitled, unsaved, empty workflow with a fresh ID", async () => {
    const client = stubClient();
    await startNew(client);
    expect(screen.getByText("Untitled")).toBeTruthy();
    expect(screen.getByText("● Unsaved changes")).toBeTruthy();
    const posted = lastValidated(client);
    expect(posted.workflowId).toMatch(UUID4);
    expect(posted.nodes).toEqual([]);
    expect(posted.edges).toEqual([]);
    expect(
      screen.getByText("Use + Add in each region to add its nodes."),
    ).toBeTruthy();
  });

  it("saves an untitled workflow through Save as, with null bases", async () => {
    const client = stubClient();
    await startNew(client);
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    const banner = screen.getByRole("region", { name: "Save as" });
    fireEvent.change(within(banner).getByLabelText("Name"), {
      target: { value: "my-flow" },
    });
    fireEvent.click(within(banner).getByRole("button", { name: "Save" }));
    await waitFor(() => expect(client.save).toHaveBeenCalled());
    const [name, , , base, sideBase] = client.save.mock.calls[0];
    expect([name, base, sideBase]).toEqual(["my-flow", null, null]);
    expect(await screen.findByText("my-flow")).toBeTruthy();
    expect(screen.getByText("Saved")).toBeTruthy();
    expect(screen.queryByRole("region", { name: "Save as" })).toBeNull();
  });

  it("keeps the work when the backend refuses a name, a taken name, or an invalid workflow", async () => {
    const client = stubClient();
    await startNew(client);
    const tryName = async (refusal: ApiError, value: string) => {
      client.save.mockRejectedValueOnce(refusal);
      fireEvent.click(screen.getByRole("button", { name: "Save as…" }));
      const banner = screen.getByRole("region", { name: "Save as" });
      fireEvent.change(within(banner).getByLabelText("Name"), {
        target: { value },
      });
      fireEvent.click(within(banner).getByRole("button", { name: "Save" }));
      return screen.findByRole("region", { name: "Notice" });
    };
    const bad = await tryName(
      new ApiError(400, clone(recorded.saveBadName)),
      "Bad Name",
    );
    expect(bad.textContent).toContain(recorded.saveBadName.error.message);
    const taken = await tryName(
      new ApiError(409, clone(recorded.saveNameTaken)),
      "capture-no-layout",
    );
    expect(taken.textContent).toContain("choose another name");
    const refused = await tryName(
      new ApiError(422, clone(recorded.saveRefused)),
      "half-built",
    );
    await waitFor(() =>
      expect(refused.textContent).toContain("Fix before saving"),
    );
    expect(refused.textContent).toContain(
      recorded.saveRefused.diagnostics![0].message,
    );
    expect(screen.getByText("Untitled")).toBeTruthy();
    expect(screen.getByText("● Unsaved changes")).toBeTruthy();
  });

  it("adds contract types per region at the top, then below, moving nothing", async () => {
    const client = stubClient();
    await startNew(client);
    add("MODEL", "Model");
    const first = node("Model");
    await waitFor(() => expect(document.activeElement).toBe(first));
    expect(status()).toContain("Added Model to MODEL.");
    expect(first.style.left).toBe(`${RAIL_WIDTH + PAD}px`);
    expect(first.style.top).toBe(`${REGION_HEADER + PAD}px`);
    const firstId = first.dataset.nodeId;
    add("MODEL", "Model");
    // Numbering follows the random IDs, so find each node by its ID.
    const byId = (id: string | undefined) =>
      regionOf("MODEL").querySelector<HTMLElement>(`[data-node-id="${id}"]`)!;
    expect(byId(firstId).style.top).toBe(`${REGION_HEADER + PAD}px`);
    const second = [
      ...regionOf("MODEL").querySelectorAll<HTMLElement>("[data-node-id]"),
    ].find((item) => item.dataset.nodeId !== firstId)!;
    expect(second.style.top).toBe(
      `${REGION_HEADER + PAD + COMPACT_HEIGHT + NODE_GAP}px`,
    );
    expect(screen.getByRole("group", { name: "Model 1" })).toBeTruthy();
    expect(screen.getByRole("group", { name: "Model 2" })).toBeTruthy();
    const posted = lastValidated(client);
    expect(posted.nodes.map((item) => item.parameters)).toEqual([{}, {}]);
    expect(posted.nodes.every((item) => UUID4.test(item.id))).toBe(true);
  });

  it("builds the menu from the contracts and supports the keyboard", async () => {
    const contracts = clone(recorded.contracts);
    contracts[3].label = "Classifier";
    const client = stubClient({ contracts });
    await startNew(client);
    const button = screen.getByRole("button", { name: "Add node to MODEL" });
    fireEvent.keyDown(button, { key: "ArrowDown" });
    const item = await screen.findByRole("menuitem", { name: "Classifier" });
    await waitFor(() => expect(document.activeElement).toBe(item));
    fireEvent.keyDown(item, { key: "Escape" });
    expect(screen.queryByRole("menu")).toBeNull();
    expect(document.activeElement).toBe(button);
    expect(
      screen.queryByRole("button", { name: /Add node to UNASSIGNED/ }),
    ).toBeNull();
  });

  it("removes a node and its connections after confirmation", async () => {
    const client = stubClient();
    await openExample(client);
    const split = node("Train/Test Split");
    split.focus();
    fireEvent.keyDown(split, { key: "Delete" });
    const dialog = screen.getByRole("alertdialog", {
      name: "Remove Train/Test Split?",
    });
    expect(dialog.textContent).toContain("Its 3 connections are removed too.");
    fireEvent.click(within(dialog).getByRole("button", { name: "Remove" }));
    expect(
      screen.queryByRole("group", { name: "Train/Test Split" }),
    ).toBeNull();
    const posted = lastValidated(client);
    expect(posted.nodes.map((item) => item.id)).not.toContain(ID(3));
    expect(posted.edges).toHaveLength(2);
    expect(status()).toContain("Removed Train/Test Split.");
    await waitFor(() =>
      expect(document.activeElement).toBe(
        screen.getByRole("button", { name: "Add node to VALIDATE / SPLIT" }),
      ),
    );
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() => expect(client.save).toHaveBeenCalled());
    expect(client.save.mock.calls[0][2]?.nodes[ID(3)]).toBeUndefined();
  });

  it("explains an incompatible port, refuses a duplicate, and cancels with Escape", async () => {
    const client = stubClient();
    await openExample(client);
    fireEvent.click(port(node("Model"), /^Output port model/));
    const banner = screen.getByRole("region", { name: "Connecting" });
    expect(banner.textContent).toContain("Connecting from Model.model");
    const evaluateSplit = port(node("Evaluate"), /^Input port split/);
    expect(evaluateSplit.getAttribute("aria-label")).toContain(
      "cannot connect",
    );
    expect(
      port(node("Evaluate"), /^Input port model/).getAttribute("aria-label"),
    ).toContain("can connect");
    const before = client.validate.mock.calls.length;
    fireEvent.click(evaluateSplit);
    expect(banner.textContent).toContain(
      "Evaluate's Split expects split, not model.",
    );
    expect(client.validate.mock.calls.length).toBe(before);
    fireEvent.keyDown(node("Evaluate"), { key: "Escape" });
    expect(screen.queryByRole("region", { name: "Connecting" })).toBeNull();
    expect(status()).toBe("Connecting cancelled.");
    fireEvent.click(port(node("Train/Test Split"), /^Output port split/));
    fireEvent.click(port(node("Model"), /^Input port split/));
    expect(status()).toBe("Already connected.");
    expect(screen.queryByRole("region", { name: "Connecting" })).toBeNull();
  });

  it("connects by click and by drag, and replaces a single-connection input", async () => {
    const client = stubClient();
    await startNew(client);
    add("VALIDATE / SPLIT", "Train/Test Split");
    add("MODEL", "Model");
    // Ports are buttons in the Tab order, so Enter and Space work too.
    const output = port(node("Train/Test Split"), /^Output port split/);
    expect(output.tagName).toBe("BUTTON");
    expect(output.getAttribute("tabindex")).toBeNull();
    fireEvent.click(output);
    fireEvent.click(port(node("Model"), /^Input port split/));
    expect(status()).toContain(
      "Connected Train/Test Split.split to Model's Split.",
    );
    const first = lastValidated(client).edges;
    expect(first).toHaveLength(1);
    add("VALIDATE / SPLIT", "Train/Test Split");
    // Numbering follows the random IDs, so take the new node by its focus.
    let newest: HTMLElement | null = null;
    await waitFor(() => {
      newest = document.activeElement as HTMLElement;
      expect(newest.getAttribute("role")).toBe("group");
    });
    fireEvent.pointerDown(port(newest!, /^Output port split/), { button: 0 });
    fireEvent.pointerUp(port(node("Model"), /^Input port split/));
    expect(status()).toMatch(
      /^Replaced the connection from Train\/Test Split \d\.split\./,
    );
    const edges = lastValidated(client).edges;
    expect(edges).toHaveLength(1);
    expect(edges[0].id).not.toBe(first[0].id);
    expect(edges[0].source.nodeId).toBe(newest!.dataset.nodeId);
    expect(UUID4.test(edges[0].id)).toBe(true);
  });

  it("draws nothing across a gutter while connecting", async () => {
    await openExample(stubClient());
    fireEvent.click(port(node("Train/Test Split"), /^Output port split/));
    for (const section of screen.getAllByRole("region", { name: / region$/ })) {
      const width = Number.parseFloat(section.style.width);
      for (const path of section.querySelectorAll("path")) {
        const numbers =
          (path.getAttribute("d") ?? "").match(/-?\d+(\.\d+)?/g) ?? [];
        for (const x of numbers.filter((_, index) => index % 2 === 0)) {
          expect(Number(x)).toBeGreaterThanOrEqual(0);
          expect(Number(x)).toBeLessThanOrEqual(width);
        }
      }
    }
  });

  it("lists inputs with their sources and disconnects one", async () => {
    const client = stubClient();
    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    const list = within(node("Model")).getByRole("region", {
      name: "Model connections",
    });
    expect(list.textContent).toContain("Split ← Train/Test Split.split");
    fireEvent.click(
      within(list).getByRole("button", {
        name: "Disconnect Train/Test Split.split from Split",
      }),
    );
    expect(lastValidated(client).edges.map((edge) => edge.id)).not.toContain(
      "42000000-0000-4000-8000-000000000003",
    );
    expect(status()).toContain(
      "Disconnected Train/Test Split.split from Model.",
    );
    expect(
      within(node("Model")).getByRole("region", { name: "Model connections" })
        .textContent,
    ).toContain("Split: not connected");
  });

  it("shows edge, port, and workflow problems exactly as recorded", async () => {
    const client = stubClient();
    client.validate.mockImplementation(() =>
      Promise.resolve(clone(recorded.validateTypeMismatch)),
    );
    await openExample(client);
    const evaluate = node("Evaluate");
    for (const item of recorded.validateTypeMismatch.diagnostics) {
      expect(await within(evaluate).findByText(item.message)).toBeTruthy();
    }
    const entry = within(regionOf("EVALUATE / COMPARE")).getByText(
      "⚠ not allowed here",
    );
    expect(entry.closest(".rail-entry-invalid")).toBeTruthy();
    expect(
      regionOf("VALIDATE / SPLIT").querySelector(".rail-entry-invalid"),
    ).toBeTruthy();
    expect(
      port(evaluate, /^Input port split/).getAttribute("aria-label"),
    ).toContain("has a problem");
    client.validate.mockImplementation(() =>
      Promise.resolve(clone(recorded.validateCycle)),
    );
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    fireEvent.change(screen.getByLabelText("Regularization"), {
      target: { value: "2" },
    });
    const problems = await screen.findByRole("region", {
      name: "Workflow problems",
    });
    expect(problems.textContent).toContain(
      recorded.validateCycle.diagnostics[0].message,
    );
  });

  it("shows a missing required input on its node and port", async () => {
    const client = stubClient();
    client.validate.mockImplementation(() =>
      Promise.resolve(clone(recorded.validateMissingInput)),
    );
    await openExample(client);
    const model = node("Model");
    const item = recorded.validateMissingInput.diagnostics[0];
    expect(await within(model).findByText(item.message)).toBeTruthy();
    expect(within(model).getByText(item.remedy)).toBeTruthy();
    expect(
      port(model, /^Input port split/).getAttribute("aria-label"),
    ).toContain("has a problem");
    expect(
      screen.queryByRole("region", { name: "Workflow problems" }),
    ).toBeNull();
  });

  it("shifts an expanded node left into open space, without storing it", async () => {
    const client = stubClient();
    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    expect(node("Model").style.left).toBe(`${RAIL_WIDTH}px`);
    fireEvent.click(screen.getByRole("button", { name: "Collapse Model" }));
    expect(node("Model").style.left).toBe(`${RAIL_WIDTH + PAD}px`);
    expect(screen.getByText("Saved")).toBeTruthy();
  });

  it("changes only nodes and edges, keeping every other field", async () => {
    const client = stubClient();
    await openExample(client);
    add("MODEL", "Model");
    const posted = lastValidated(client);
    const original = recorded.loadExample.workflow;
    expect(posted.nodes.slice(0, original.nodes.length)).toEqual(
      original.nodes,
    );
    expect(posted.edges).toEqual(original.edges);
    expect({ ...posted, nodes: [], edges: [] }).toEqual({
      ...original,
      nodes: [],
      edges: [],
    });
  });
});
