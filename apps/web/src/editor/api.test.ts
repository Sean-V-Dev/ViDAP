import { describe, expect, it } from "vitest";
import {
  ApiError,
  createSliceClient,
  numberSpellings,
  writeJson,
  type WorkflowDocument,
} from "./api";

// A load response written the way the backend writes floats: `1.0`, `0.0`,
// and an exponent. The browser reads these as 1, 0, and 0.00001.
const LOADED = `{
  "name": "spelled",
  "workflow": {
    "format": "vidap.workflow",
    "schemaVersion": "1.0",
    "workflowId": "spelled-id",
    "nodes": [
      {"id": "a", "type": "t", "parameters": {"p": 1.0, "q": 0.0, "r": 1e-05, "s": 3, "a/b~c": 2.50}}
    ],
    "edges": []
  },
  "workflowDigest": "d1",
  "sidecar": null,
  "sidecarDigest": null,
  "sidecarNotice": null
}`;

const WORKFLOW_TEXT =
  '{"format":"vidap.workflow","schemaVersion":"1.0","workflowId":"spelled-id",' +
  '"nodes":[{"id":"a","type":"t","parameters":{"p":1.0,"q":0.0,"r":1e-05,"s":3,"a/b~c":2.50}}],' +
  '"edges":[]}';

function recordingFetcher() {
  const bodies: string[] = [];
  const fetcher = (input: string, init?: RequestInit) => {
    if (typeof init?.body === "string") {
      bodies.push(init.body);
    }
    const text = input.endsWith("/workflows/spelled")
      ? LOADED
      : input.endsWith("/validate")
        ? '{"valid":true,"diagnostics":[]}'
        : input.endsWith("/compare")
          ? '{"changed":false,"missing":false,"workflowDigest":"d1","sidecarDigest":null,"summary":null}'
          : '{"name":"spelled","workflowDigest":"d1","sidecarDigest":null}';
    return Promise.resolve(new Response(text, { status: 200 }));
  };
  return { fetcher, bodies };
}

describe("number spelling (P3-AC08)", () => {
  it("finds every number the browser would spell differently", () => {
    expect([...numberSpellings(LOADED)]).toEqual([
      ["/workflow/nodes/0/parameters/p", "1.0"],
      ["/workflow/nodes/0/parameters/q", "0.0"],
      ["/workflow/nodes/0/parameters/r", "1e-05"],
      ["/workflow/nodes/0/parameters/a~1b~0c", "2.50"],
    ]);
  });

  it("posts an unchanged workflow byte-identical to the one loaded", async () => {
    const { fetcher, bodies } = recordingFetcher();
    const client = createSliceClient(fetcher);
    const loaded = await client.load("spelled");
    expect(loaded.workflow.nodes[0]?.parameters?.p).toBe(1);
    await client.validate(loaded.workflow);
    await client.compare("spelled", loaded.workflow, "d1", null);
    await client.save(
      "spelled",
      structuredClone(loaded.workflow),
      null,
      "d1",
      null,
    );
    expect(bodies[0]).toBe(WORKFLOW_TEXT);
    expect(bodies[1]).toBe(
      `{"workflow":${WORKFLOW_TEXT},"baseWorkflowDigest":"d1","baseSidecarDigest":null}`,
    );
    expect(bodies[2]).toBe(
      `{"workflow":${WORKFLOW_TEXT},"sidecar":null,"baseWorkflowDigest":"d1","baseSidecarDigest":null}`,
    );
  });

  it("writes a changed number plainly, and the kept spelling once it is changed back", async () => {
    const { fetcher, bodies } = recordingFetcher();
    const client = createSliceClient(fetcher);
    const loaded = await client.load("spelled");
    const changed: WorkflowDocument = structuredClone(loaded.workflow);
    const parameters = changed.nodes[0]?.parameters ?? {};
    parameters.p = 0;
    await client.validate(changed);
    parameters.p = 1;
    await client.validate(changed);
    expect(bodies[0]).toContain('"p":0,"q":0.0');
    expect(bodies[1]).toBe(WORKFLOW_TEXT);
  });

  it("matches JSON.stringify when nothing was kept", () => {
    const value = { a: [1, 2.5, null, "x/y"], b: { c: true }, d: undefined };
    expect(writeJson(value, () => undefined)).toBe(JSON.stringify(value));
  });

  it("says unreachable only when the backend did not answer", () => {
    const answered = new ApiError(404, { detail: "Not Found" });
    expect(answered.message).not.toContain("could not be reached");
    expect(answered.message).not.toContain("Not Found");
    expect(new ApiError(0, null).message).toContain("could not be reached");
  });
});
