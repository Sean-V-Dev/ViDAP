import { describe, expect, it } from "vitest";
import { Buffer } from "node:buffer";
import {
  FOUNDATION_STATUS,
  boundedDiagnostics,
  failureMessage,
  parseFixtureText,
  validateLoopbackStatusUrl,
  validateMode,
} from "./vidap-process-harness.mjs";

const fixture = {
  id: "p0-ep07-foundation-status",
  version: "1",
  path: "fixtures/p0-ep07-foundation-status.json",
  byteSize: 0,
  provenance: "synthetic",
  terms: "MIT",
  creationMethod: "hand-authored deterministic UTF-8 JSON",
  expectedStatus: FOUNDATION_STATUS,
  permittedConsumers: ["P0-EP07 harness", "P0-EP07 tests"],
  privacy: "No personal, sensitive, credential, path, network, or telemetry data.",
  reviewer: "Central",
  reviewDate: "2026-09-19",
};

function validFixtureText() {
  const initial = JSON.stringify(fixture);
  return JSON.stringify({ ...fixture, byteSize: Buffer.byteLength(initial, "utf8") + 2 });
}

describe("vidap process harness inputs", () => {
  it("rejects an unsupported mode without starting a process", () => {
    expect(() => validateMode("invalid")).toThrow('must be "launch" or "smoke"');
  });

  it("rejects non-loopback and alternate readiness targets", () => {
    expect(() => validateLoopbackStatusUrl("http://localhost:8000/api/status", 8000)).toThrow(
      "prescribed loopback",
    );
    expect(() => validateLoopbackStatusUrl("https://127.0.0.1:8000/api/status", 8000)).toThrow(
      "prescribed loopback",
    );
  });

  it("accepts only complete bounded fixture metadata", () => {
    expect(parseFixtureText(validFixtureText()).expectedStatus).toEqual(FOUNDATION_STATUS);
    expect(() => parseFixtureText("{not-json")).toThrow("valid UTF-8 JSON");
    expect(() => parseFixtureText(`${validFixtureText()}${" ".repeat(1_025)}`)).toThrow(
      "at or below 1024 bytes",
    );
  });

  it("keeps failure diagnostics bounded and actionable without a log file", () => {
    const diagnostics = boundedDiagnostics(Array.from({ length: 20 }, (_, index) => `line ${index}`));

    expect(diagnostics).toHaveLength(12);
    expect(failureMessage("Python readiness", "Use npm.cmd run setup.", diagnostics)).toContain(
      "Use npm.cmd run setup.",
    );
  });
});
