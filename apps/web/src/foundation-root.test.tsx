import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { FoundationRoot } from "./foundation-root";

describe("FoundationRoot", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the bounded checking state before the one status request settles", () => {
    const fetchMock = vi.fn<typeof fetch>();
    fetchMock.mockImplementation(() => new Promise<Response>(() => undefined));
    vi.stubGlobal("fetch", fetchMock);

    render(<FoundationRoot />);

    expect(
      screen.getByText("Checking the local foundation host."),
    ).not.toBeNull();
    expect(fetchMock).toHaveBeenCalledOnce();
    expect(fetchMock).toHaveBeenCalledWith("/api/status");
  });

  it("shows ready only for the exact static foundation status", async () => {
    const fetchMock = vi.fn<typeof fetch>();
    fetchMock.mockResolvedValue(
      new Response(
        JSON.stringify({
          application: "ViDAP",
          scope: "phase-0-foundation",
          status: "ready",
        }),
        { status: 200 },
      ),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<FoundationRoot />);

    expect(
      await screen.findByText("Local foundation host is ready."),
    ).not.toBeNull();
  });

  it("shows the actionable unavailable state for malformed status", async () => {
    const fetchMock = vi.fn<typeof fetch>();
    fetchMock.mockResolvedValue(
      new Response(JSON.stringify({ status: "ready" })),
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<FoundationRoot />);

    expect(
      await screen.findByText(/Local foundation host is unavailable/),
    ).not.toBeNull();
    expect(screen.getByText("npm.cmd run launch")).not.toBeNull();
  });

  it("shows the actionable unavailable state when the request fails", async () => {
    const fetchMock = vi.fn<typeof fetch>();
    fetchMock.mockRejectedValue(new Error("offline"));
    vi.stubGlobal("fetch", fetchMock);

    render(<FoundationRoot />);

    expect(
      await screen.findByText(/Local foundation host is unavailable/),
    ).not.toBeNull();
  });
});
