import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  ApiError,
  type LoadedWorkflow,
  type NodeContract,
  type SliceClient,
  type WorkflowDocument,
} from "./api";
import { Editor } from "./Editor";
import {
  COMPACT_HEIGHT,
  EXPANDED_HEIGHT,
  MOVE_STEP,
  NODE_WIDTH,
  PAD,
  REGION_HEADER,
  RAIL_WIDTH,
} from "./layout";
import { recorded } from "./test-data/recorded";

const ID = (n: number) => `41000000-0000-4000-8000-00000000000${n}`;
const clone = <T,>(value: T): T => structuredClone(value);

interface StubOptions {
  contracts?: NodeContract[];
  loaded?: LoadedWorkflow;
}

function stubClient(options: StubOptions = {}) {
  const loaded = options.loaded ?? recorded.loadExample;
  const client = {
    contracts: vi.fn<SliceClient["contracts"]>(() =>
      Promise.resolve(clone(options.contracts ?? recorded.contracts)),
    ),
    validate: vi.fn<SliceClient["validate"]>((document: WorkflowDocument) =>
      Promise.resolve(
        clone(
          document.nodes[3]?.parameters?.regularization === 0
            ? recorded.validateInvalid
            : recorded.validateValid,
        ),
      ),
    ),
    list: vi.fn<SliceClient["list"]>(() =>
      Promise.resolve(clone(recorded.list)),
    ),
    load: vi.fn<SliceClient["load"]>(() => Promise.resolve(clone(loaded))),
    save: vi.fn<SliceClient["save"]>((name: string) =>
      Promise.resolve({ ...clone(recorded.saveExample), name }),
    ),
    compare: vi.fn<SliceClient["compare"]>(() =>
      Promise.resolve(clone(recorded.compareUnchanged)),
    ),
  };
  return client;
}

async function openExample(
  client: ReturnType<typeof stubClient>,
  firstNode = "Model",
) {
  render(<Editor client={client} />);
  await waitFor(() => expect(client.contracts).toHaveBeenCalled());
  fireEvent.click(screen.getByRole("button", { name: "Open…" }));
  fireEvent.click(
    await screen.findByRole("button", { name: "capture-example" }),
  );
  await screen.findByRole("group", { name: firstNode });
  await waitFor(() => expect(client.validate).toHaveBeenCalled());
}

const node = (name: string) => screen.getByRole("group", { name });
const regionOf = (label: string) =>
  screen.getByRole("region", { name: `${label} region` });

describe("Editor workspace", () => {
  // Vitest globals are off, so Testing Library cannot register this itself.
  afterEach(cleanup);

  it("lays out the slice in its five regions with Not run chips", async () => {
    const client = stubClient();
    await openExample(client);
    for (const [region, name] of [
      ["DATA", "Dataset"],
      ["PREPARE", "Prepare Data"],
      ["VALIDATE / SPLIT", "Train/Test Split"],
      ["MODEL", "Model"],
      ["EVALUATE / COMPARE", "Evaluate"],
    ]) {
      expect(
        within(regionOf(region)).getByRole("group", { name }),
      ).toBeTruthy();
    }
    expect(screen.queryByRole("region", { name: /UNASSIGNED/ })).toBeNull();
    expect(screen.getAllByText("Not run")).toHaveLength(5);
    expect(
      screen.getByRole("button", { name: "Run" }).hasAttribute("disabled"),
    ).toBe(true);
    expect(screen.getByText("Run arrives in the next step.")).toBeTruthy();
  });

  it("shows each boundary value once on Outputs and once per consuming port", async () => {
    await openExample(stubClient());
    const outputs = within(regionOf("VALIDATE / SPLIT")).getByRole("list", {
      name: "VALIDATE / SPLIT outputs",
    });
    const splitEntries = within(outputs).getAllByRole("button");
    expect(splitEntries).toHaveLength(1);
    expect(splitEntries[0].textContent).toContain("Train/Test Split.split");
    expect(splitEntries[0].textContent).toContain("used by 2 nodes");
    const evaluateInputs = within(
      within(regionOf("EVALUATE / COMPARE")).getByRole("list", {
        name: "EVALUATE / COMPARE inputs",
      }),
    ).getAllByRole("button");
    expect(evaluateInputs.map((entry) => entry.textContent)).toEqual(
      expect.arrayContaining([
        expect.stringContaining("Train/Test Split.split"),
        expect.stringContaining("Model.model"),
      ]),
    );
    // The skip-region value does not appear in MODEL's rails at all.
    const modelInputs = within(regionOf("MODEL")).getByRole("list", {
      name: "MODEL inputs",
    });
    expect(within(modelInputs).getAllByRole("button")).toHaveLength(1);
    fireEvent.focus(splitEntries[0]);
    const card = screen.getByRole("tooltip");
    expect(card.textContent).toContain(
      "Produced by VALIDATE / SPLIT / Train/Test Split (split)",
    );
    expect(card.textContent).toContain("Used by MODEL / Model (split)");
    expect(card.textContent).toContain(
      "Used by EVALUATE / COMPARE / Evaluate (split)",
    );
  });

  it("never draws a wire outside its own region", async () => {
    await openExample(stubClient());
    for (const section of screen.getAllByRole("region", { name: / region$/ })) {
      const width = Number.parseFloat(section.style.width);
      for (const path of section.querySelectorAll("path")) {
        const numbers =
          (path.getAttribute("d") ?? "").match(/-?\d+(\.\d+)?/g) ?? [];
        const xs = numbers.filter((_, index) => index % 2 === 0).map(Number);
        for (const x of xs) {
          expect(x).toBeGreaterThanOrEqual(0);
          expect(x).toBeLessThanOrEqual(width);
        }
      }
    }
  });

  it("builds every setting from the contract, including changed bounds and labels", async () => {
    const contracts = clone(recorded.contracts);
    const model = contracts.find((item) => item.type === "vidap.slice.model")!;
    model.parameters[0] = {
      ...model.parameters[0],
      label: "Constraint strength",
      description: "Changed in the contract only.",
      constraints: { minimum: 0.5, maximum: 50 },
    };
    await openExample(stubClient({ contracts }));
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    const field = screen.getByLabelText("Constraint strength");
    expect(field.getAttribute("min")).toBe("0.5");
    expect(field.getAttribute("max")).toBe("50");
    expect(field.getAttribute("step")).toBe("any");
    expect(screen.getByText("Changed in the contract only.")).toBeTruthy();
    const split = screen.getByRole("group", { name: "Train/Test Split" });
    fireEvent.click(
      within(split).getByRole("button", { name: "Expand Train/Test Split" }),
    );
    expect(
      within(split).getByLabelText("Split seed").getAttribute("step"),
    ).toBe("1");
  });

  it("shows the backend's exact validation message on the node, then clears it", async () => {
    const client = stubClient();
    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    const field = screen.getByLabelText("Regularization");
    fireEvent.change(field, { target: { value: "0" } });
    const expected = recorded.validateInvalid.diagnostics[0];
    const model = node("Model");
    expect(await within(model).findByText(expected.message)).toBeTruthy();
    expect(within(model).getByText("Fix before running")).toBeTruthy();
    expect(within(model).getByText(expected.remedy)).toBeTruthy();
    const posted = client.validate.mock.calls.at(-1)![0];
    expect(posted.nodes[3].parameters?.regularization).toBe(0);
    fireEvent.change(field, { target: { value: "1" } });
    await waitFor(() =>
      expect(within(node("Model")).queryByText(expected.message)).toBeNull(),
    );
    expect(screen.getByText("● Unsaved changes")).toBeTruthy();
  });

  it("shows a problem not tied to a node in the workspace banner", async () => {
    const client = stubClient();
    const diagnostic = {
      ...clone(recorded.validateInvalid.diagnostics[0]),
      elementReference: "workflow",
    };
    client.validate.mockImplementation(() =>
      Promise.resolve({
        ...clone(recorded.validateInvalid),
        diagnostics: [diagnostic],
      }),
    );
    await openExample(client);
    const banner = await screen.findByRole("region", {
      name: "Workflow problems",
    });
    expect(banner.textContent).toContain("Fix before running");
    expect(banner.textContent).toContain(diagnostic.message);
    expect(within(node("Model")).queryByText(diagnostic.message)).toBeNull();
  });

  it("falls back to default placement when the saved layout is unreadable", async () => {
    const loaded = clone(recorded.loadExample);
    loaded.sidecar = null;
    loaded.sidecarNotice = "unreadable";
    await openExample(stubClient({ loaded }));
    expect(screen.getByText(/saved layout could not be read/)).toBeTruthy();
    expect(node("Model").style.left).toBe(`${RAIL_WIDTH + PAD}px`);
    expect(node("Model").style.top).toBe(`${REGION_HEADER + PAD}px`);
  });

  it("does not send text that is not a number", async () => {
    const client = stubClient();
    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    const calls = client.validate.mock.calls.length;
    fireEvent.change(screen.getByLabelText("Regularization"), {
      target: { value: "" },
    });
    expect(
      screen.getByText("Enter a number to update this setting."),
    ).toBeTruthy();
    await new Promise((resolve) => setTimeout(resolve, 500));
    expect(client.validate.mock.calls.length).toBe(calls);
  });

  it("resizes regions by keyboard and buttons without moving any node", async () => {
    await openExample(stubClient());
    const grip = screen.getByRole("separator", { name: "Resize DATA" });
    const before = node("Dataset").style.left;
    expect(grip.getAttribute("aria-valuenow")).toBe("400");
    fireEvent.keyDown(grip, { key: "ArrowRight" });
    expect(grip.getAttribute("aria-valuenow")).toBe("408");
    fireEvent.keyDown(grip, { key: "ArrowRight", shiftKey: true });
    expect(grip.getAttribute("aria-valuenow")).toBe("448");
    fireEvent.click(screen.getByRole("button", { name: "Narrow DATA" }));
    expect(grip.getAttribute("aria-valuenow")).toBe("408");
    fireEvent.keyDown(grip, { key: "Home" });
    expect(Number(grip.getAttribute("aria-valuenow"))).toBe(
      Number(grip.getAttribute("aria-valuemin")),
    );
    expect(node("Dataset").style.left).toBe(before);
    expect(node("Model").style.left).toBe(`${RAIL_WIDTH + 16}px`);
  });

  it("expands in place, pushes down nodes below, and restores them", async () => {
    const loaded = clone(recorded.loadNoLayout);
    loaded.workflow.nodes.push({
      id: ID(6),
      type: "vidap.slice.model",
      parameters: { regularization: 2 },
    });
    await openExample(stubClient({ loaded }), "Model 1");
    const second = node("Model 2");
    const top = Number.parseFloat(second.style.top);
    expect(top).toBe(REGION_HEADER + 16 + COMPACT_HEIGHT + 24);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model 1" }));
    expect(Number.parseFloat(node("Model 2").style.top)).toBe(
      top + EXPANDED_HEIGHT - COMPACT_HEIGHT,
    );
    fireEvent.click(screen.getByRole("button", { name: "Collapse Model 1" }));
    expect(Number.parseFloat(node("Model 2").style.top)).toBe(top);
    expect(screen.getByText(/default placement is used/)).toBeTruthy();
  });

  it("opens and closes focus mode and returns focus to the node", async () => {
    await openExample(stubClient());
    const model = node("Model");
    model.focus();
    fireEvent.keyDown(model, { key: "F" });
    const dialog = await screen.findByRole("dialog", {
      name: "Model, focus mode",
    });
    expect(within(dialog).getByLabelText("Regularization")).toBeTruthy();
    fireEvent.keyDown(dialog, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    await waitFor(() => expect(document.activeElement).toBe(node("Model")));
  });

  it("keeps Tab inside the focus-mode panel and hides the lifted node's wires", async () => {
    await openExample(stubClient());
    const wires = () =>
      regionOf("MODEL").querySelectorAll("svg.wires path").length;
    expect(wires()).toBeGreaterThan(0);
    node("Model").focus();
    fireEvent.keyDown(node("Model"), { key: "F" });
    const dialog = await screen.findByRole("dialog", {
      name: "Model, focus mode",
    });
    expect(wires()).toBe(0);
    const items = [
      ...dialog.querySelectorAll<HTMLElement>(
        'button, input, summary, [tabindex="0"]',
      ),
    ];
    const first = items[0];
    const last = items.at(-1)!;
    act(() => last.focus());
    fireEvent.keyDown(last, { key: "Tab" });
    expect(document.activeElement).toBe(first);
    fireEvent.keyDown(first, { key: "Tab", shiftKey: true });
    expect(document.activeElement).toBe(last);
  });

  it("shows a value changed in focus mode in the node's own field too", async () => {
    await openExample(stubClient());
    const split = node("Train/Test Split");
    fireEvent.click(
      within(split).getByRole("button", { name: "Expand Train/Test Split" }),
    );
    const field = (scope: HTMLElement) =>
      within(scope).getByLabelText<HTMLInputElement>("Test fraction");
    expect(field(split).value).toBe("0.25");
    split.focus();
    fireEvent.keyDown(split, { key: "F" });
    const dialog = await screen.findByRole("dialog", {
      name: "Train/Test Split, focus mode",
    });
    fireEvent.change(field(dialog), { target: { value: "0.4" } });
    fireEvent.keyDown(dialog, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    expect(field(node("Train/Test Split")).value).toBe("0.4");
  });

  it("does not mark the workflow unsaved for a change that changes nothing", async () => {
    const loaded = clone(recorded.loadExample);
    // Model already sits at its region's right limit.
    loaded.sidecar!.nodes[ID(4)].x = 400 - RAIL_WIDTH * 2 - NODE_WIDTH - PAD;
    await openExample(stubClient({ loaded }));
    fireEvent.click(screen.getByRole("button", { name: "100%" }));
    node("Model").focus();
    fireEvent.keyDown(node("Model"), { key: "m" });
    fireEvent.keyDown(node("Model"), { key: "ArrowRight" });
    fireEvent.keyDown(node("Model"), { key: "Escape" });
    expect(screen.getByText("Saved")).toBeTruthy();
    expect(screen.queryByText("● Unsaved changes")).toBeNull();
  });

  it("follows the graph by keyboard and announces where it goes", async () => {
    await openExample(stubClient());
    const status = screen.getByRole("status");
    node("Train/Test Split").focus();
    fireEvent.keyDown(node("Train/Test Split"), { key: "ArrowRight" });
    expect(document.activeElement).toBe(node("Model"));
    expect(status.textContent).toContain(
      "Model, 1 of 2 downstream of Train/Test Split.",
    );
    fireEvent.keyDown(node("Model"), { key: "ArrowRight", shiftKey: true });
    expect(document.activeElement).toBe(node("Evaluate"));
    expect(status.textContent).toContain(
      "Evaluate, 2 of 2 downstream of Train/Test Split.",
    );
    fireEvent.keyDown(node("Evaluate"), { key: "ArrowLeft" });
    expect(document.activeElement).toBe(node("Model"));
    fireEvent.keyDown(node("Model"), { key: "ArrowLeft" });
    expect(document.activeElement).toBe(node("Train/Test Split"));
    fireEvent.keyDown(node("Train/Test Split"), { key: "Enter" });
    expect(
      screen.getByRole("button", { name: "Collapse Train/Test Split" }),
    ).toBeTruthy();
  });

  it("moves a node in move mode and saves only the layout", async () => {
    const client = stubClient();
    await openExample(client);
    const model = node("Model");
    const left = Number.parseFloat(model.style.left);
    model.focus();
    fireEvent.keyDown(model, { key: "m" });
    expect(screen.getByRole("status").textContent).toContain("Moving Model.");
    fireEvent.keyDown(model, { key: "ArrowRight" });
    fireEvent.keyDown(model, { key: "ArrowDown", shiftKey: true });
    fireEvent.keyDown(model, { key: "Enter" });
    expect(Number.parseFloat(node("Model").style.left)).toBe(left + MOVE_STEP);
    fireEvent.keyDown(node("Model"), { key: "ArrowRight" });
    expect(Number.parseFloat(node("Model").style.left)).toBe(left + MOVE_STEP);
    fireEvent.click(screen.getByRole("button", { name: "85%" }));
    fireEvent.click(screen.getByRole("button", { name: "Expand Dataset" }));
    fireEvent.keyDown(
      screen.getByRole("separator", { name: "Resize PREPARE" }),
      {
        key: "ArrowRight",
      },
    );
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() => expect(client.save).toHaveBeenCalled());
    const [name, posted, sidecar, base, sideBase] = client.save.mock.calls[0];
    expect(name).toBe("capture-example");
    expect(JSON.stringify(posted)).toBe(
      JSON.stringify(recorded.loadExample.workflow),
    );
    expect(base).toBe(recorded.loadExample.workflowDigest);
    expect(sideBase).toBe(recorded.loadExample.sidecarDigest);
    expect(sidecar?.nodes[ID(4)]).toEqual({
      region: "MODEL",
      x: 16 + MOVE_STEP,
      y: 56,
    });
    expect(sidecar?.viewport.zoom).toBe(0.85);
    expect(sidecar?.regions.find((r) => r.key === "PREPARE")?.width).toBe(408);
    expect(await screen.findByText("Saved")).toBeTruthy();
  });

  it("refuses to overwrite: shows the backend's change summary and both actions", async () => {
    const client = stubClient();
    client.save.mockImplementationOnce(() =>
      Promise.reject(new ApiError(409, clone(recorded.saveConflict))),
    );
    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    fireEvent.change(screen.getByLabelText("Regularization"), {
      target: { value: "2" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    const banner = await screen.findByRole("region", {
      name: "Saved files changed",
    });
    expect(banner.textContent).toContain(
      "capture-example changed outside the editor. Your changes have not been saved.",
    );
    expect(banner.textContent).toContain(
      "Model · regularization: yours 1, on disk 0.5",
    );
    fireEvent.click(
      within(banner).getByRole("button", { name: "Reload from disk" }),
    );
    const confirm = screen.getByRole("alertdialog", {
      name: "Reload from disk?",
    });
    expect(document.activeElement).toBe(
      within(confirm).getByRole("button", { name: "Cancel" }),
    );
    fireEvent.keyDown(confirm, { key: "Escape" });
    expect(screen.queryByRole("alertdialog")).toBeNull();
    fireEvent.change(within(banner).getByLabelText("New name"), {
      target: { value: "my-copy" },
    });
    fireEvent.click(
      within(banner).getByRole("button", { name: "Save under new name" }),
    );
    await waitFor(() => expect(client.save).toHaveBeenCalledTimes(2));
    const [name, , , base, sideBase] = client.save.mock.calls[1];
    expect([name, base, sideBase]).toEqual(["my-copy", null, null]);
    await waitFor(() =>
      expect(
        screen.queryByRole("region", { name: "Saved files changed" }),
      ).toBeNull(),
    );
  });

  it("checks for outside changes when the window regains focus", async () => {
    const client = stubClient();
    await openExample(client);
    client.compare.mockImplementationOnce(() =>
      Promise.resolve(clone(recorded.compareChanged)),
    );
    act(() => {
      fireEvent.focus(window);
    });
    const banner = await screen.findByRole("region", {
      name: "Saved files changed",
    });
    expect(banner.textContent).toContain(
      "Model · regularization: yours 1, on disk 0.5",
    );
    expect(client.compare).toHaveBeenCalledWith(
      "capture-example",
      expect.anything(),
      recorded.loadExample.workflowDigest,
      recorded.loadExample.sidecarDigest,
    );
    // Nothing is unsaved, so neither the banner nor the confirmation claims
    // that anything will be lost.
    expect(banner.textContent).not.toContain("not been saved");
    fireEvent.click(
      within(banner).getByRole("button", { name: "Reload from disk" }),
    );
    const confirm = screen.getByRole("alertdialog", {
      name: "Reload from disk?",
    });
    expect(confirm.textContent).not.toContain("discards");
    fireEvent.click(within(confirm).getByRole("button", { name: "Reload" }));
    await waitFor(() => expect(client.load).toHaveBeenCalledTimes(2));
  });

  it("keeps a moved node inside its region, by pointer and by keyboard", async () => {
    await openExample(stubClient());
    const right = RAIL_WIDTH + (400 - RAIL_WIDTH * 2 - NODE_WIDTH - PAD);
    const model = node("Model");
    fireEvent.pointerDown(model.querySelector(".node-header")!, {
      button: 0,
      clientX: 0,
      clientY: 0,
    });
    expect(document.activeElement).toBe(model);
    fireEvent.pointerMove(window, { clientX: 2000, clientY: 0 });
    fireEvent.pointerUp(window);
    expect(Number.parseFloat(node("Model").style.left)).toBe(right);
    fireEvent.keyDown(node("Model"), { key: "m" });
    fireEvent.keyDown(node("Model"), { key: "ArrowRight", shiftKey: true });
    expect(Number.parseFloat(node("Model").style.left)).toBe(right);
    fireEvent.keyDown(node("Model"), { key: "ArrowLeft", shiftKey: true });
    expect(Number.parseFloat(node("Model").style.left)).toBe(RAIL_WIDTH);
  });

  it("ends move mode when focus leaves the node", async () => {
    await openExample(stubClient());
    node("Model").focus();
    fireEvent.keyDown(node("Model"), { key: "M" });
    expect(node("Model").classList.contains("node-moving")).toBe(true);
    act(() => node("Evaluate").focus());
    expect(node("Model").classList.contains("node-moving")).toBe(false);
    expect(screen.getByRole("status").textContent).toContain("Move finished.");
  });

  it("toggles a node by double-click on it, but not inside its fields", async () => {
    await openExample(stubClient());
    fireEvent.doubleClick(within(node("Model")).getByText("Not run"));
    expect(screen.getByRole("button", { name: "Collapse Model" })).toBeTruthy();
    fireEvent.doubleClick(screen.getByLabelText("Regularization"));
    expect(screen.getByRole("button", { name: "Collapse Model" })).toBeTruthy();
    fireEvent.doubleClick(
      within(node("Model")).getByRole("heading", { name: "Model" }),
    );
    expect(screen.getByRole("button", { name: "Expand Model" })).toBeTruthy();
  });

  it("focuses a gutter when it is pressed, so the arrow keys work", async () => {
    await openExample(stubClient());
    const grip = screen.getByRole("separator", { name: "Resize DATA" });
    fireEvent.pointerDown(grip, { button: 0, clientX: 0 });
    fireEvent.pointerUp(window);
    expect(document.activeElement).toBe(grip);
  });

  it("orders each region for Tab as Inputs, nodes, then Outputs", async () => {
    await openExample(stubClient());
    const region = regionOf("MODEL");
    const input = within(
      within(region).getByRole("list", { name: "MODEL inputs" }),
    ).getByRole("button");
    const output = within(
      within(region).getByRole("list", { name: "MODEL outputs" }),
    ).getByRole("button");
    const follows = (a: Element, b: Element) =>
      Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);
    expect(follows(input, node("Model"))).toBe(true);
    expect(follows(node("Model"), output)).toBe(true);
  });

  it("reports a refused load with the backend's message and keeps the workspace", async () => {
    const client = stubClient();
    client.load.mockImplementationOnce(() =>
      Promise.reject(new ApiError(404, clone(recorded.notFound))),
    );
    render(<Editor client={client} />);
    fireEvent.click(screen.getByRole("button", { name: "Open…" }));
    fireEvent.click(
      await screen.findByRole("button", { name: "capture-example" }),
    );
    expect(
      await screen.findByText(recorded.notFound.error.message),
    ).toBeTruthy();
    expect(screen.getByText("No workflow open")).toBeTruthy();
  });

  it("keeps the Phase 1 layout metadata untouched when saving", async () => {
    const loaded = clone(recorded.loadExample);
    loaded.workflow.layout = { nodePositions: { [ID(1)]: { x: 5, y: 7.5 } } };
    const client = stubClient({ loaded });
    await openExample(client);
    node("Dataset").focus();
    fireEvent.keyDown(node("Dataset"), { key: "M" });
    fireEvent.keyDown(node("Dataset"), { key: "ArrowDown" });
    fireEvent.keyDown(node("Dataset"), { key: "Escape" });
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    await waitFor(() => expect(client.save).toHaveBeenCalled());
    expect(client.save.mock.calls[0][1].layout).toEqual({
      nodePositions: { [ID(1)]: { x: 5, y: 7.5 } },
    });
  });
});
