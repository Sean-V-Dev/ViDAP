// Shared helpers for the editor component tests: a stubbed client that
// replays the recorded backend responses, and common queries.

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { expect, vi } from "vitest";
import type {
  LoadedWorkflow,
  NodeContract,
  SliceClient,
  WorkflowDocument,
} from "./api";
import { Editor } from "./Editor";
import { recorded } from "./test-data/recorded";

export const ID = (n: number) => `41000000-0000-4000-8000-00000000000${n}`;
export const clone = <T,>(value: T): T => structuredClone(value);

export interface StubOptions {
  contracts?: NodeContract[];
  loaded?: LoadedWorkflow;
}

export function stubClient(options: StubOptions = {}) {
  const loaded = options.loaded ?? recorded.loadExample;
  return {
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
}

export type StubClient = ReturnType<typeof stubClient>;

export async function openExample(client: StubClient, firstNode = "Model") {
  render(<Editor client={client} />);
  await waitFor(() => expect(client.contracts).toHaveBeenCalled());
  fireEvent.click(screen.getByRole("button", { name: "Open…" }));
  fireEvent.click(
    await screen.findByRole("button", { name: "capture-example" }),
  );
  await screen.findByRole("group", { name: firstNode });
  await waitFor(() => expect(client.validate).toHaveBeenCalled());
}

export const node = (name: string) => screen.getByRole("group", { name });
export const regionOf = (label: string) =>
  screen.getByRole("region", { name: `${label} region` });
