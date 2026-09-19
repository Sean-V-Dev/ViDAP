import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FoundationRoot } from "./foundation-root";

describe("FoundationRoot", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the bounded checking state before the one status request settles", () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise<Response>(() => undefined)),
    );

    render(<FoundationRoot />);

    expect(
      screen.getByText("Checking the local foundation host."),
    ).toBeInTheDocument();
    expect(globalThis.fetch).toHaveBeenCalledOnce();
    expect(globalThis.fetch).toHaveBeenCalledWith("/api/status");
  });

  it("shows ready only for the exact static foundation status", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            application: "ViDAP",
            scope: "phase-0-foundation",
            status: "ready",
          }),
          { status: 200 },
        ),
      ),
    );

    render(<FoundationRoot />);

    expect(
      await screen.findByText("Local foundation host is ready."),
    ).toBeInTheDocument();
  });

  it("shows the actionable unavailable state for malformed status", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(new Response(JSON.stringify({ status: "ready" }))),
    );

    render(<FoundationRoot />);

    expect(
      await screen.findByText(/Local foundation host is unavailable/),
    ).toBeInTheDocument();
    expect(screen.getByText("npm.cmd run launch")).toBeInTheDocument();
  });

  it("shows the actionable unavailable state when the request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));

    render(<FoundationRoot />);

    expect(
      await screen.findByText(/Local foundation host is unavailable/),
    ).toBeInTheDocument();
  });
});
