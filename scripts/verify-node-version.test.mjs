import { describe, expect, it } from "vitest";
import {
  unsupportedNodeMessage,
  validateNodeVersion,
} from "./verify-node-version.mjs";

describe("Node 24 guard", () => {
  it("accepts a Node 24 version", () => {
    expect(validateNodeVersion("24.21.0")).toBeNull();
  });

  it("rejects another major with the preinstall diagnostic", () => {
    const version = "23.11.0";

    expect(validateNodeVersion(version)).toBe(unsupportedNodeMessage(version));
  });
});
