import { describe, expect, it } from "vitest";
import api from "./api.ts?raw";
import confirmDialog from "./ConfirmDialog.tsx?raw";
import editor from "./Editor.tsx?raw";
import layout from "./layout.ts?raw";
import model from "./model.ts?raw";
import nodeView from "./NodeView.tsx?raw";
import presentation from "./presentation.ts?raw";
import workspace from "./Workspace.tsx?raw";
import { recorded } from "./test-data/recorded";

const sources: Record<string, string> = {
  api,
  confirmDialog,
  editor,
  layout,
  model,
  nodeView,
  presentation,
  workspace,
};

describe("single sources (A3)", () => {
  it("copies no parameter key, default, or bound from the contracts into the UI", () => {
    const forbidden = new Set<string>();
    for (const contract of recorded.contracts) {
      for (const parameter of contract.parameters) {
        forbidden.add(parameter.key);
        forbidden.add(parameter.label);
        for (const value of Object.values(parameter.constraints)) {
          if (typeof value === "number" && !Number.isInteger(value)) {
            forbidden.add(String(value));
          } else if (typeof value === "number" && Math.abs(value) > 1000) {
            forbidden.add(String(value));
          }
        }
        if (
          typeof parameter.default === "number" &&
          !Number.isInteger(parameter.default)
        ) {
          forbidden.add(String(parameter.default));
        }
      }
      if (contract.description) {
        forbidden.add(contract.description);
      }
    }
    expect(forbidden.size).toBeGreaterThan(5);
    for (const [file, text] of Object.entries(sources)) {
      for (const literal of forbidden) {
        expect(`${file}: ${text.includes(literal) ? literal : ""}`).toBe(
          `${file}: `,
        );
      }
    }
  });

  it("matches the recorded responses to the channel contract", () => {
    expect(recorded.contracts.map((item) => item.type)).toEqual([
      "vidap.slice.dataset",
      "vidap.slice.prepare",
      "vidap.slice.split",
      "vidap.slice.model",
      "vidap.slice.evaluate",
    ]);
    for (const contract of recorded.contracts) {
      expect(Object.keys(contract).sort()).toEqual(
        [
          "description",
          "inputs",
          "label",
          "outputs",
          "parameters",
          "type",
        ].sort(),
      );
    }
    expect(recorded.validateValid).toEqual({ valid: true, diagnostics: [] });
    expect(recorded.validateInvalid.valid).toBe(false);
    expect(recorded.loadExample.workflow.format).toBe("vidap.workflow");
    expect(recorded.loadExample.sidecar?.format).toBe("vidap.workspace-view");
    expect(recorded.loadNoLayout.sidecar).toBeNull();
    expect(recorded.saveConflict.error.code).toBe("conflict");
    expect(recorded.notFound.error.code).toBe("not-found");
    expect(recorded.compareChanged.changed).toBe(true);
    expect(recorded.compareUnchanged).toEqual({
      changed: false,
      missing: false,
      sidecarDigest: recorded.loadExample.sidecarDigest,
      summary: null,
      workflowDigest: recorded.loadExample.workflowDigest,
    });
  });
});
