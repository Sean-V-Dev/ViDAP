import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ApiError, type RunResult } from "./api";
import { Editor } from "./Editor";
import { recorded } from "./test-data/recorded";
import {
  ID,
  clone,
  node,
  openExample,
  regionOf,
  stubClient,
} from "./test-support";

describe("Editor run, results, runtime errors, and boundary trace (P3-EP05)", () => {
  it("gates Run on a valid non-empty workflow and shows Running… while in flight", async () => {
    const client = stubClient();
    render(<Editor client={client} />);
    await waitFor(() => expect(client.contracts).toHaveBeenCalled());

    const runButton = () => screen.getByRole("button", { name: /^Run/ });
    expect(runButton().hasAttribute("disabled")).toBe(true);
    expect(screen.getByText("Open or create a workflow to run.")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "New" }));
    await waitFor(() => expect(client.validate).toHaveBeenCalled());
    expect(runButton().hasAttribute("disabled")).toBe(true);
    expect(
      screen.getByText("Add the slice nodes before running."),
    ).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "Open…" }));
    fireEvent.click(
      await screen.findByRole("button", { name: "capture-example" }),
    );
    fireEvent.click(
      await screen.findByRole("button", { name: "Discard and open" }),
    );
    await screen.findByRole("group", { name: "Model" });
    await waitFor(() =>
      expect(runButton().hasAttribute("disabled")).toBe(false),
    );

    // Invalid parameter disables Run.
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    const regField = screen.getByLabelText("Regularization");
    fireEvent.change(regField, { target: { value: "0" } });
    expect(
      await screen.findAllByText("1 problem to fix before running."),
    ).not.toHaveLength(0);
    expect(runButton().hasAttribute("disabled")).toBe(true);

    // Restore valid parameter and verify in-flight Running state.
    fireEvent.change(regField, { target: { value: "1" } });
    await waitFor(() =>
      expect(runButton().hasAttribute("disabled")).toBe(false),
    );

    let resolveRun!: (value: RunResult) => void;
    client.run.mockImplementationOnce(
      () =>
        new Promise<RunResult>((resolve) => {
          resolveRun = resolve;
        }),
    );

    fireEvent.click(runButton());
    expect(
      screen
        .getByRole("button", { name: "Running…" })
        .getAttribute("aria-busy"),
    ).toBe("true");
    expect(
      screen.getByRole("button", { name: "Running…" }).hasAttribute("disabled"),
    ).toBe(true);
    expect(screen.getAllByText("Running")).toHaveLength(5);

    resolveRun(clone(recorded.runSuccess));
    await waitFor(() =>
      expect(screen.getByText("Accuracy 0.9 (36 / 40 test rows)")).toBeTruthy(),
    );
    expect(screen.getAllByText("Completed")).toHaveLength(5);
  });

  it("displays recorded accuracy in the top bar and on Evaluate, retains Last run on edit, and updates on re-run", async () => {
    const client = stubClient();
    await openExample(client);

    fireEvent.click(screen.getByRole("button", { name: "Run" }));
    await waitFor(() => expect(client.run).toHaveBeenCalledTimes(1));

    const resultBar = screen.getByLabelText("Primary result");
    expect(within(resultBar).getByText("Result")).toBeTruthy();
    expect(
      within(resultBar).getByText("Accuracy 0.9 (36 / 40 test rows)"),
    ).toBeTruthy();

    const evaluateNode = node("Evaluate");
    expect(
      within(evaluateNode).getByText("Accuracy 0.9 (36 / 40)"),
    ).toBeTruthy();
    fireEvent.click(
      within(evaluateNode).getByRole("button", { name: "Expand Evaluate" }),
    );
    expect(
      within(evaluateNode).getByText(
        "Recorded result: Accuracy 0.9 (36 / 40 test rows)",
      ),
    ).toBeTruthy();
    fireEvent.click(
      within(evaluateNode).getByRole("button", { name: "Collapse Evaluate" }),
    );

    // Editing Model regularization marks the previous result as Last run and resets chips.
    fireEvent.click(screen.getByRole("button", { name: "Expand Model" }));
    fireEvent.change(screen.getByLabelText("Regularization"), {
      target: { value: "0.0001" },
    });
    await waitFor(() =>
      expect(within(resultBar).getByText("Last run")).toBeTruthy(),
    );
    expect(
      within(resultBar).getByText("Accuracy 0.9 (36 / 40 test rows)"),
    ).toBeTruthy();
    expect(
      within(node("Evaluate")).getByText("Last run · Accuracy 0.9 (36 / 40)"),
    ).toBeTruthy();
    expect(screen.getAllByText("Not run")).toHaveLength(5);

    // Re-running with regularization = 0.0001 updates the recorded result to 0.55.
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "Run" }).hasAttribute("disabled"),
      ).toBe(false),
    );
    fireEvent.click(screen.getByRole("button", { name: "Run" }));
    await waitFor(() => expect(client.run).toHaveBeenCalledTimes(2));
    expect(
      within(resultBar).getByText("Accuracy 0.55 (22 / 40 test rows)"),
    ).toBeTruthy();
    expect(within(resultBar).getByText("Result")).toBeTruthy();
    expect(
      within(node("Evaluate")).getByText("Accuracy 0.55 (22 / 40)"),
    ).toBeTruthy();
  });

  it("renders completed, failed, blocked, and unrelated node statuses and declared runtime error details", async () => {
    const loaded = clone(recorded.loadExample);
    loaded.workflow.nodes[1] = {
      ...loaded.workflow.nodes[1],
      id: ID(6),
    };
    loaded.workflow.edges[0] = {
      ...loaded.workflow.edges[0],
      target: { nodeId: ID(6), portKey: "table" },
    };
    loaded.workflow.edges[1] = {
      ...loaded.workflow.edges[1],
      source: { nodeId: ID(1), portKey: "table" },
      target: { nodeId: ID(3), portKey: "table" },
    };
    const client = stubClient({ loaded });
    client.run.mockImplementationOnce(() =>
      Promise.resolve(clone(recorded.runFailed)),
    );

    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Run" }));
    await waitFor(() => expect(client.run).toHaveBeenCalledTimes(1));

    expect(within(node("Dataset")).getByText("Completed")).toBeTruthy();
    expect(
      within(node("Train/Test Split")).getByText("Completed"),
    ).toBeTruthy();
    expect(within(node("Model")).getByText("Failed")).toBeTruthy();
    expect(within(node("Evaluate")).getByText("Blocked")).toBeTruthy();
    expect(within(node("Prepare Data")).getByText("Unrelated")).toBeTruthy();

    const modelNode = node("Model");
    expect(modelNode.classList.contains("node-failed")).toBe(true);
    const diag = recorded.runFailed.diagnostics[0];
    expect(within(modelNode).getByText("Run failed")).toBeTruthy();
    expect(within(modelNode).getByText(diag.explanation)).toBeTruthy();
    expect(within(modelNode).getByText(diag.remedy)).toBeTruthy();
    expect(within(modelNode).getByText("Technical details")).toBeTruthy();
    expect(
      within(modelNode).getByText(`${diag.code} · ${diag.operationKey}`),
    ).toBeTruthy();
    expect(
      within(modelNode).getByText(`Attempt ${diag.attemptId}`),
    ).toBeTruthy();
    expect(
      within(modelNode).getByText(`Type ${diag.technical.type}`),
    ).toBeTruthy();
    expect(within(modelNode).getByText(diag.technical.message)).toBeTruthy();
    expect(
      within(modelNode).getByText(
        `Traceback ${diag.technical.traceback.join(" → ")}`,
      ),
    ).toBeTruthy();

    const resultBar = screen.getByLabelText("Primary result");
    expect(within(resultBar).getByText("Run failed on Model")).toBeTruthy();
  });

  it("renders a workspace-level runtime diagnostic when nodeId is null", async () => {
    const client = stubClient();
    const workspaceFailure = clone(recorded.runFailed);
    workspaceFailure.diagnostics = [
      {
        ...workspaceFailure.diagnostics[0],
        nodeId: null,
        code: "publication-failed",
        explanation: "The attempt record could not be published safely.",
        remedy:
          "Inspect and explicitly remove the owned pending attempt before retrying.",
      },
    ];
    client.run.mockImplementationOnce(() => Promise.resolve(workspaceFailure));

    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Run" }));
    const banner = await screen.findByRole("region", { name: "Run failed" });
    expect(
      within(banner).getByText(
        "The attempt record could not be published safely.",
      ),
    ).toBeTruthy();
    expect(
      within(banner).getByText(
        `publication-failed · Attempt ${workspaceFailure.diagnostics[0].attemptId}`,
      ),
    ).toBeTruthy();
  });

  it("handles 409 busy with a non-destructive retry banner and handles 422 run-refused", async () => {
    const client = stubClient();
    client.run.mockImplementationOnce(() =>
      Promise.reject(
        new ApiError(409, {
          error: { code: "busy", message: "Another run is in progress." },
        }),
      ),
    );

    await openExample(client);
    fireEvent.click(screen.getByRole("button", { name: "Run" }));

    const busyBanner = await screen.findByRole("region", {
      name: "Run busy",
    });
    expect(
      within(busyBanner).getByText("Another run is in progress."),
    ).toBeTruthy();

    fireEvent.click(within(busyBanner).getByRole("button", { name: "Retry" }));
    await waitFor(() => expect(client.run).toHaveBeenCalledTimes(2));
    await waitFor(() =>
      expect(screen.queryByRole("region", { name: "Run busy" })).toBeNull(),
    );
    expect(screen.getByText("Accuracy 0.9 (36 / 40 test rows)")).toBeTruthy();

    // Non-busy ApiError surfaces the backend message in the notice banner.
    client.run.mockImplementationOnce(() =>
      Promise.reject(new ApiError(422, clone(recorded.runRefused))),
    );
    fireEvent.click(screen.getByRole("button", { name: "Run" }));
    const noticeBanner = await screen.findByRole("region", { name: "Notice" });
    expect(
      within(noticeBanner).getByText(recorded.runRefused.error.message),
    ).toBeTruthy();
  });

  it("enters and exits Boundary Value Trace mode by click and keyboard, highlighting connected items and drawing cross-region dashed curves", async () => {
    await openExample(stubClient());

    const splitOutputs = within(regionOf("VALIDATE / SPLIT")).getByRole(
      "list",
      { name: "VALIDATE / SPLIT outputs" },
    );
    const splitChip = within(splitOutputs).getByRole("button");
    expect(splitChip.getAttribute("aria-pressed")).toBe("false");
    expect(document.querySelector("svg.trace-wires")).toBeNull();

    // Click the boundary rail entry to enter Trace Mode.
    fireEvent.click(splitChip);
    expect(splitChip.getAttribute("aria-pressed")).toBe("true");
    expect(splitChip.getAttribute("data-trace-state")).toBe("highlighted");

    const traceBanner = screen.getByRole("region", { name: "Trace" });
    expect(
      within(traceBanner).getByText("Tracing Train/Test Split.split"),
    ).toBeTruthy();

    // Producer and its two consumers across MODEL and EVALUATE / COMPARE are highlighted; others are dimmed.
    expect(node("Train/Test Split").getAttribute("data-trace-state")).toBe(
      "highlighted",
    );
    expect(node("Model").getAttribute("data-trace-state")).toBe("highlighted");
    expect(node("Evaluate").getAttribute("data-trace-state")).toBe(
      "highlighted",
    );
    expect(node("Dataset").getAttribute("data-trace-state")).toBe("dimmed");
    expect(node("Prepare Data").getAttribute("data-trace-state")).toBe(
      "dimmed",
    );

    // Matching input rail entries are highlighted; unrelated rail entries are dimmed.
    const modelInputs = within(
      within(regionOf("MODEL")).getByRole("list", { name: "MODEL inputs" }),
    ).getByRole("button");
    expect(modelInputs.getAttribute("data-trace-state")).toBe("highlighted");
    const dataOutputs = within(
      within(regionOf("DATA")).getByRole("list", { name: "DATA outputs" }),
    ).getByRole("button");
    expect(dataOutputs.getAttribute("data-trace-state")).toBe("dimmed");

    // Temporary cross-region dashed curves are drawn in svg.trace-wires, while intra-region SVGs stay within region bounds.
    const traceSvg = document.querySelector("svg.trace-wires");
    expect(traceSvg).toBeTruthy();
    expect(traceSvg!.querySelectorAll("path.wire-trace")).toHaveLength(2);
    for (const section of screen.getAllByRole("region", { name: / region$/ })) {
      expect(section.querySelectorAll("path.wire-trace")).toHaveLength(0);
    }

    // Pressing Escape exits Trace Mode.
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("region", { name: "Trace" })).toBeNull();
    expect(document.querySelector("svg.trace-wires")).toBeNull();
    expect(node("Model").getAttribute("data-trace-state")).toBeNull();

    // Enter via keyboard (Space) on a rail entry, then exit via Exit trace button.
    splitChip.focus();
    fireEvent.keyDown(splitChip, { key: " " });
    expect(screen.getByRole("region", { name: "Trace" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Exit trace" }));
    expect(screen.queryByRole("region", { name: "Trace" })).toBeNull();
  });
});
