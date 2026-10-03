// The ViDAP editor workspace (P3-EP04A). It opens, edits, validates, and saves
// existing slice workflows through the `/api/slice/` channel only.

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import "./editor.css";
import {
  ApiError,
  type ChangeSummary,
  type Diagnostic,
  type JsonValue,
  type SliceClient,
  type WorkflowDocument,
  type WorkflowSummary,
} from "./api";
import { ConfirmDialog } from "./ConfirmDialog";
import {
  DEFAULT_REGION_WIDTH,
  MOVE_STEP,
  MOVE_STEP_LARGE,
  ZOOM_LEVELS,
  clampPosition,
  clampWidth,
  layoutFrom,
  positionedNodes,
  sidecarFrom,
  type Layout,
} from "./layout";
import {
  displayNames,
  downstream,
  indexContracts,
  nodeById,
  regionOf,
  upstream,
  verticalNeighbour,
  visibleRegions,
  withParameter,
  type ContractIndex,
} from "./model";
import { NodeView } from "./NodeView";
import { Workspace } from "./Workspace";

const VALIDATE_DELAY_MS = 400;
const FOCUSABLE =
  'button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';

interface OpenWorkflow {
  name: string;
  workflowDigest: string;
  sidecarDigest: string | null;
  document: WorkflowDocument;
}

interface Conflict {
  missing: boolean;
  summary: ChangeSummary | null;
}

interface Notice {
  tone: "info" | "warn" | "error";
  text: string;
  diagnostics?: Diagnostic[];
}

interface Confirmation {
  title: string;
  body: string;
  confirmLabel: string;
  onConfirm: () => void;
}

const EMPTY_LAYOUT: Layout = {
  widths: {},
  positions: {},
  viewport: { x: 0, y: 0, zoom: 1 },
};

function nodeIdOf(
  document: WorkflowDocument,
  reference: string,
): string | null {
  const id = reference.slice(0, 36);
  return document.nodes.some((node) => node.id === id) ? id : null;
}

function summaryLines(
  summary: ChangeSummary | null,
  names: ReadonlyMap<string, string>,
  contracts: ContractIndex,
): string[] {
  if (!summary) {
    return [];
  }
  if (summary.diskUnreadable) {
    return ["The file on disk can no longer be read as a workflow."];
  }
  const typeLabel = (type: string) => contracts.get(type)?.label ?? type;
  const nodeName = (id: string) => names.get(id) ?? id;
  const lines: string[] = [];
  for (const item of summary.nodesAdded ?? []) {
    lines.push(`Node added on disk: ${typeLabel(item.type)}`);
  }
  for (const item of summary.nodesRemoved ?? []) {
    lines.push(`Node removed on disk: ${nodeName(item.nodeId)}`);
  }
  const added = summary.edgesAdded?.length ?? 0;
  const removed = summary.edgesRemoved?.length ?? 0;
  if (added) {
    lines.push(
      `${added} ${added === 1 ? "connection" : "connections"} added on disk`,
    );
  }
  if (removed) {
    lines.push(
      `${removed} ${removed === 1 ? "connection" : "connections"} removed on disk`,
    );
  }
  for (const item of summary.parametersChanged ?? []) {
    lines.push(
      `${nodeName(item.nodeId)} · ${item.key}: yours ${JSON.stringify(item.before)}, on disk ${JSON.stringify(item.after)}`,
    );
  }
  for (const id of summary.labelsChanged ?? []) {
    lines.push(`Label changed on disk: ${nodeName(id)}`);
  }
  if (summary.layoutMetadataChanged) {
    lines.push("Stored layout metadata changed on disk");
  }
  return lines;
}

export function Editor({ client }: { client: SliceClient }) {
  const [contracts, setContracts] = useState<ContractIndex | null>(null);
  const [open, setOpen] = useState<OpenWorkflow | null>(null);
  const [layout, setLayout] = useState<Layout>(EMPTY_LAYOUT);
  const [dirty, setDirty] = useState(false);
  const [generation, setGeneration] = useState(0);
  const [diagnostics, setDiagnostics] = useState<Diagnostic[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [focusMode, setFocusMode] = useState<string | null>(null);
  const [moving, setMoving] = useState<string | null>(null);
  const [notice, setNotice] = useState<Notice | null>(null);
  const [conflict, setConflict] = useState<Conflict | null>(null);
  const [saveAsName, setSaveAsName] = useState("");
  const [listing, setListing] = useState<WorkflowSummary[] | null>(null);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [announcement, setAnnouncement] = useState("");
  const nodeElements = useRef(new Map<string, HTMLDivElement>());
  const validateTimer = useRef<number | undefined>(undefined);
  const validateSequence = useRef(0);
  const navigation = useRef<{ source: string; index: number } | null>(null);
  const scrollArea = useRef<HTMLDivElement | null>(null);
  const scrollPosition = useRef({ x: 0, y: 0 });

  useEffect(() => {
    let active = true;
    client.contracts().then(
      (items) => {
        if (active) {
          setContracts(indexContracts(items));
        }
      },
      (error: unknown) => {
        if (active) {
          setNotice({
            tone: "error",
            text:
              error instanceof ApiError
                ? error.message
                : "The node definitions could not be loaded.",
          });
        }
      },
    );
    return () => {
      active = false;
    };
  }, [client]);

  const announce = useCallback((text: string) => setAnnouncement(text), []);

  const requestValidation = useCallback(
    (document: WorkflowDocument, immediate = false) => {
      window.clearTimeout(validateTimer.current);
      const sequence = ++validateSequence.current;
      const run = () => {
        client.validate(document).then(
          (result) => {
            if (sequence === validateSequence.current) {
              setDiagnostics(result.diagnostics);
              announce(
                result.valid
                  ? "Workflow is valid."
                  : `${result.diagnostics.length} ${result.diagnostics.length === 1 ? "problem" : "problems"} to fix before running.`,
              );
            }
          },
          (error: unknown) => {
            if (
              sequence === validateSequence.current &&
              error instanceof ApiError
            ) {
              setDiagnostics(error.diagnostics);
              setNotice({
                tone: "error",
                text: error.message,
                diagnostics: error.diagnostics,
              });
            }
          },
        );
      };
      if (immediate) {
        run();
      } else {
        validateTimer.current = window.setTimeout(run, VALIDATE_DELAY_MS);
      }
    },
    [client, announce],
  );

  const loadWorkflow = useCallback(
    (name: string) => {
      client.load(name).then(
        (loaded) => {
          const { layout: next, usedDefaults } = layoutFrom(
            loaded.workflow,
            loaded.sidecar,
          );
          setOpen({
            name: loaded.name,
            workflowDigest: loaded.workflowDigest,
            sidecarDigest: loaded.sidecarDigest,
            document: loaded.workflow,
          });
          setLayout(next);
          setDirty(false);
          setExpanded(null);
          setFocusMode(null);
          setMoving(null);
          setConflict(null);
          setListing(null);
          setDiagnostics([]);
          setGeneration((value) => value + 1);
          setNotice(
            loaded.sidecarNotice
              ? {
                  tone: "warn",
                  text: "The saved layout could not be read, so default placement is used. Saving replaces it.",
                }
              : usedDefaults
                ? {
                    tone: "info",
                    text: "No saved layout for some or all nodes, so default placement is used.",
                  }
                : null,
          );
          announce(`Opened ${loaded.name}.`);
          requestValidation(loaded.workflow, true);
        },
        (error: unknown) => {
          setNotice({
            tone: "error",
            text:
              error instanceof ApiError
                ? error.message
                : "The workflow could not be opened.",
            diagnostics:
              error instanceof ApiError ? error.diagnostics : undefined,
          });
        },
      );
    },
    [client, announce, requestValidation],
  );

  const confirmThen = useCallback(
    (
      proceed: () => void,
      title: string,
      body: string,
      confirmLabel: string,
    ) => {
      if (!dirty) {
        proceed();
        return;
      }
      setConfirmation({ title, body, confirmLabel, onConfirm: proceed });
    },
    [dirty],
  );

  const showOpenList = () => {
    client.list().then(
      (items) => setListing(items),
      (error: unknown) =>
        setNotice({
          tone: "error",
          text:
            error instanceof ApiError
              ? error.message
              : "Saved workflows could not be listed.",
        }),
    );
  };

  const currentSidecar = (document: WorkflowDocument) =>
    sidecarFrom(document, {
      ...layout,
      viewport: { ...layout.viewport, ...scrollPosition.current },
    });

  const save = () => {
    if (!open) {
      return;
    }
    const sidecar = currentSidecar(open.document);
    client
      .save(
        open.name,
        open.document,
        sidecar,
        open.workflowDigest,
        open.sidecarDigest,
      )
      .then(
        (result) => {
          setOpen({
            ...open,
            workflowDigest: result.workflowDigest,
            sidecarDigest: result.sidecarDigest,
          });
          setDirty(false);
          setNotice(null);
          announce(`Saved ${open.name}.`);
        },
        (error: unknown) => {
          if (error instanceof ApiError && error.code === "conflict") {
            setConflict({ missing: error.missing, summary: error.summary });
            announce(
              "Save refused: the saved files changed outside the editor.",
            );
          } else {
            setNotice({
              tone: "error",
              text:
                error instanceof ApiError
                  ? error.message
                  : "The workflow was not saved.",
              diagnostics:
                error instanceof ApiError ? error.diagnostics : undefined,
            });
          }
        },
      );
  };

  const saveAs = () => {
    if (!open) {
      return;
    }
    const name = saveAsName.trim();
    const sidecar = currentSidecar(open.document);
    client.save(name, open.document, sidecar, null, null).then(
      (result) => {
        setOpen({
          ...open,
          name: result.name,
          workflowDigest: result.workflowDigest,
          sidecarDigest: result.sidecarDigest,
        });
        setDirty(false);
        setConflict(null);
        setSaveAsName("");
        setNotice(null);
        announce(`Saved as ${result.name}.`);
      },
      (error: unknown) => {
        setNotice({
          tone: "error",
          text:
            error instanceof ApiError && error.code === "conflict"
              ? `${error.message} A workflow with that name already exists; choose another name.`
              : error instanceof ApiError
                ? error.message
                : "The workflow was not saved.",
        });
      },
    );
  };

  // Outside changes: check whenever the window regains focus (D3.3).
  useEffect(() => {
    if (!open) {
      return;
    }
    const onFocus = () => {
      client
        .compare(
          open.name,
          open.document,
          open.workflowDigest,
          open.sidecarDigest,
        )
        .then(
          (result) => {
            if (result.changed) {
              setConflict({ missing: result.missing, summary: result.summary });
              announce("The saved files changed outside the editor.");
            }
          },
          () => undefined,
        );
    };
    window.addEventListener("focus", onFocus);
    return () => window.removeEventListener("focus", onFocus);
  }, [client, open, announce]);

  useEffect(() => {
    if (!dirty) {
      return;
    }
    const onBeforeUnload = (event: BeforeUnloadEvent) => {
      event.preventDefault();
    };
    window.addEventListener("beforeunload", onBeforeUnload);
    return () => window.removeEventListener("beforeunload", onBeforeUnload);
  }, [dirty]);

  useEffect(() => {
    if (scrollArea.current && generation > 0) {
      scrollPosition.current = { x: layout.viewport.x, y: layout.viewport.y };
      scrollArea.current.scrollTo?.(layout.viewport.x, layout.viewport.y);
    }
    // Only when a workflow is (re)opened; later scrolling is the user's.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [generation]);

  const names = useMemo(
    () =>
      open && contracts
        ? displayNames(open.document, contracts)
        : new Map<string, string>(),
    [open, contracts],
  );
  const regions = visibleRegions(open?.document ?? null);
  const diagnosticsByNode = useMemo(() => {
    const result = new Map<string, Diagnostic[]>();
    if (!open) {
      return result;
    }
    for (const item of diagnostics) {
      const id = nodeIdOf(open.document, item.elementReference);
      if (id) {
        result.set(id, [...(result.get(id) ?? []), item]);
      }
    }
    return result;
  }, [diagnostics, open]);
  const workspaceDiagnostics = open
    ? diagnostics.filter(
        (item) => !nodeIdOf(open.document, item.elementReference),
      )
    : [];

  const focusNode = (id: string) => {
    nodeElements.current.get(id)?.focus();
  };

  // A resize, move, or zoom that changes nothing leaves the workflow saved.
  const setWidth = (region: string, width: number) => {
    setLayout((current) => ({
      ...current,
      widths: { ...current.widths, [region]: width },
    }));
    setDirty(true);
  };

  const resize = (region: string, width: number) => {
    const next = clampWidth(
      open?.document ?? null,
      region,
      layout.positions,
      width,
    );
    if (next !== layout.widths[region]) {
      setWidth(region, next);
    }
  };

  const regionWidth = (current: Layout, id: string) => {
    const node = open ? nodeById(open.document, id) : undefined;
    return (
      (node ? current.widths[regionOf(node)] : undefined) ??
      DEFAULT_REGION_WIDTH
    );
  };

  const moveBy = (id: string, dx: number, dy: number) => {
    const position = layout.positions[id];
    if (!position) {
      return;
    }
    const next = clampPosition(
      { x: position.x + dx, y: position.y + dy },
      regionWidth(layout, id),
    );
    if (next.x === position.x && next.y === position.y) {
      return;
    }
    setLayout((current) => ({
      ...current,
      positions: { ...current.positions, [id]: next },
    }));
    setDirty(true);
  };

  // Leaving the node ends move mode, so the dashed outline never outlives it.
  const onNodeBlur = (id: string, event: React.FocusEvent<HTMLDivElement>) => {
    const next = event.relatedTarget;
    if (
      moving === id &&
      !(next instanceof Node && event.currentTarget.contains(next))
    ) {
      setMoving(null);
      announce("Move finished.");
    }
  };

  const onNodeKeyDown = (
    id: string,
    event: React.KeyboardEvent<HTMLDivElement>,
  ) => {
    if (event.target !== event.currentTarget || !open) {
      return;
    }
    if (moving === id) {
      const step = event.shiftKey ? MOVE_STEP_LARGE : MOVE_STEP;
      const moves: Record<string, [number, number]> = {
        ArrowLeft: [-step, 0],
        ArrowRight: [step, 0],
        ArrowUp: [0, -step],
        ArrowDown: [0, step],
      };
      const delta = moves[event.key];
      if (delta) {
        event.preventDefault();
        moveBy(id, delta[0], delta[1]);
      } else if (event.key === "Enter" || event.key === "Escape") {
        event.preventDefault();
        setMoving(null);
        announce("Move finished.");
      }
      return;
    }
    const positioned = positionedNodes(open.document, layout.positions);
    const name = (nodeId: string) => names.get(nodeId) ?? nodeId;
    switch (event.key) {
      case "ArrowRight": {
        event.preventDefault();
        const targets = downstream(open.document, id, positioned);
        if (targets.length === 0 && !event.shiftKey) {
          announce(`${name(id)} has no downstream nodes.`);
          return;
        }
        if (event.shiftKey) {
          const state = navigation.current;
          if (!state) {
            announce("Press Right first to follow a node's output.");
            return;
          }
          const siblings = downstream(open.document, state.source, positioned);
          const index = (state.index + 1) % siblings.length;
          navigation.current = { source: state.source, index };
          focusNode(siblings[index]);
          announce(
            `${name(siblings[index])}, ${index + 1} of ${siblings.length} downstream of ${name(state.source)}.`,
          );
          return;
        }
        navigation.current = { source: id, index: 0 };
        focusNode(targets[0]);
        announce(
          `${name(targets[0])}, 1 of ${targets.length} downstream of ${name(id)}.`,
        );
        return;
      }
      case "ArrowLeft": {
        event.preventDefault();
        const sources = upstream(open.document, id, positioned);
        if (sources.length === 0) {
          announce(`${name(id)} has no upstream nodes.`);
          return;
        }
        navigation.current = null;
        focusNode(sources[0]);
        announce(`${name(sources[0])}, feeds ${name(id)}.`);
        return;
      }
      case "ArrowUp":
      case "ArrowDown": {
        event.preventDefault();
        const next = verticalNeighbour(
          id,
          event.key === "ArrowUp" ? -1 : 1,
          positioned,
        );
        if (next) {
          navigation.current = null;
          focusNode(next);
        } else {
          announce(
            `No node ${event.key === "ArrowUp" ? "above" : "below"} in this region.`,
          );
        }
        return;
      }
      case "Enter":
        event.preventDefault();
        setExpanded((current) => (current === id ? null : id));
        return;
      case "Escape":
        if (expanded === id) {
          event.preventDefault();
          setExpanded(null);
        }
        return;
      case "f":
      case "F":
        event.preventDefault();
        setFocusMode(id);
        return;
      case "m":
      case "M":
        event.preventDefault();
        setMoving(id);
        announce(
          `Moving ${name(id)}. Arrow keys move it; Shift moves farther; Enter or Escape finishes.`,
        );
        return;
      default:
        return;
    }
  };

  const onHeaderPointerDown = (
    id: string,
    event: React.PointerEvent<HTMLDivElement>,
  ) => {
    if (event.button !== 0) {
      return;
    }
    const start = layout.positions[id];
    if (!start) {
      return;
    }
    // preventDefault stops text selection during the drag, but it also stops
    // the browser focusing the node, so focus it here for M and the arrows.
    event.preventDefault();
    nodeElements.current.get(id)?.focus({ preventScroll: true });
    const zoom = layout.viewport.zoom;
    const width = regionWidth(layout, id);
    const originX = event.clientX;
    const originY = event.clientY;
    let last = start;
    const onMove = (move: PointerEvent) => {
      const { x, y } = clampPosition(
        {
          x: start.x + (move.clientX - originX) / zoom,
          y: start.y + (move.clientY - originY) / zoom,
        },
        width,
      );
      last = { x: Math.round(x), y: Math.round(y) };
      const position = last;
      setLayout((current) => ({
        ...current,
        positions: { ...current.positions, [id]: position },
      }));
    };
    const onUp = () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      if (last.x !== start.x || last.y !== start.y) {
        setDirty(true);
      }
    };
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
  };

  const onGutterPointerDown = (
    region: string,
    event: React.PointerEvent<HTMLDivElement>,
  ) => {
    if (event.button !== 0) {
      return;
    }
    event.preventDefault();
    event.currentTarget.focus({ preventScroll: true });
    const startWidth = layout.widths[region] ?? 400;
    const originX = event.clientX;
    const zoom = layout.viewport.zoom;
    // Positions cannot change during a gutter drag, so the bounds hold.
    const positions = layout.positions;
    let applied = startWidth;
    const onMove = (move: PointerEvent) => {
      const next = clampWidth(
        open?.document ?? null,
        region,
        positions,
        startWidth + (move.clientX - originX) / zoom,
      );
      if (next !== applied) {
        applied = next;
        setWidth(region, next);
      }
    };
    const onUp = () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
  };

  const setZoom = (zoom: number) => {
    if (zoom === layout.viewport.zoom) {
      return;
    }
    setLayout((current) => ({
      ...current,
      viewport: { ...current.viewport, zoom },
    }));
    setDirty(true);
  };

  const onParameterChange = (nodeId: string, key: string, value: JsonValue) => {
    if (!open) {
      return;
    }
    const document = withParameter(open.document, nodeId, key, value);
    setOpen({ ...open, document });
    setDirty(true);
    requestValidation(document);
  };

  const closeFocusMode = () => {
    const id = focusMode;
    setFocusMode(null);
    if (id) {
      window.setTimeout(() => focusNode(id), 0);
    }
  };

  const focusedNode =
    open && focusMode
      ? open.document.nodes.find((node) => node.id === focusMode)
      : undefined;
  const zoom = layout.viewport.zoom;
  const conflictLines =
    conflict && contracts
      ? summaryLines(conflict.summary, names, contracts)
      : [];

  return (
    <div className="editor">
      <header className="top-bar">
        <h1 className="product">ViDAP</h1>
        <p className="workflow-state" aria-live="off">
          {open ? (
            <>
              <span className="workflow-name">{open.name}</span>{" "}
              <span className={dirty ? "state-unsaved" : "state-saved"}>
                {dirty ? "● Unsaved changes" : "Saved"}
              </span>
            </>
          ) : (
            "No workflow open"
          )}
        </p>
        <div className="top-actions">
          <button
            type="button"
            className="button"
            onClick={showOpenList}
            aria-expanded={listing !== null}
          >
            Open…
          </button>
          <button
            type="button"
            className="button"
            onClick={save}
            disabled={!open || !dirty}
          >
            Save
          </button>
          <div className="segmented" role="group" aria-label="Zoom">
            {ZOOM_LEVELS.map((level) => (
              <button
                key={level}
                type="button"
                className="segment"
                aria-pressed={zoom === level}
                onClick={() => setZoom(level)}
              >
                {Math.round(level * 100)}%
              </button>
            ))}
          </div>
        </div>
        <p className="primary-result">
          <span className="result-label">Result</span> <span>—</span>
        </p>
        <div className="run-area">
          <button
            type="button"
            className="button button-primary"
            disabled
            aria-describedby="run-reason"
          >
            Run
          </button>
          <span id="run-reason" className="run-reason">
            Run arrives in the next step.
          </span>
        </div>
      </header>

      <div className="banners">
        {listing && (
          <section
            className="banner banner-info"
            aria-label="Open a saved workflow"
          >
            <p className="banner-title">Open a saved workflow</p>
            {listing.length === 0 ? (
              <p>No saved workflows yet.</p>
            ) : (
              <ul className="open-list">
                {listing.map((item) => (
                  <li key={item.name}>
                    <button
                      type="button"
                      className="button"
                      onClick={() =>
                        confirmThen(
                          () => loadWorkflow(item.name),
                          "Discard unsaved changes?",
                          "Opening another workflow discards the changes you have not saved.",
                          "Discard and open",
                        )
                      }
                    >
                      {item.name}
                    </button>
                  </li>
                ))}
              </ul>
            )}
            <button
              type="button"
              className="button"
              onClick={() => setListing(null)}
            >
              Close
            </button>
          </section>
        )}
        {conflict && open && (
          <section
            className="banner banner-warn"
            aria-label="Saved files changed"
          >
            <p className="banner-title">
              {conflict.missing
                ? `${open.name} was removed or renamed outside the editor.`
                : `${open.name} changed outside the editor.`}
              {dirty && " Your changes have not been saved."}
            </p>
            {conflictLines.length > 0 && (
              <ul className="change-summary">
                {conflictLines.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            )}
            <div className="banner-actions">
              <button
                type="button"
                className="button"
                onClick={() =>
                  setConfirmation({
                    title: "Reload from disk?",
                    body: dirty
                      ? "Reloading discards the changes you have not saved and shows the saved files."
                      : "Reloading shows the saved files in place of the open copy.",
                    confirmLabel: dirty ? "Discard and reload" : "Reload",
                    onConfirm: () => loadWorkflow(open.name),
                  })
                }
                disabled={conflict.missing}
              >
                Reload from disk
              </button>
              <label className="save-as">
                <span>New name</span>
                <input
                  type="text"
                  value={saveAsName}
                  onChange={(event) => setSaveAsName(event.target.value)}
                />
              </label>
              <button
                type="button"
                className="button"
                onClick={saveAs}
                disabled={saveAsName.trim() === ""}
              >
                Save under new name
              </button>
            </div>
          </section>
        )}
        {notice && (
          <section
            className={`banner banner-${notice.tone}`}
            aria-label="Notice"
          >
            <p>{notice.text}</p>
            {notice.diagnostics && notice.diagnostics.length > 0 && (
              <ul>
                {notice.diagnostics.map((item, index) => (
                  <li key={`${item.code}-${index}`}>
                    {item.message} {item.remedy}
                  </li>
                ))}
              </ul>
            )}
            <button
              type="button"
              className="button"
              onClick={() => setNotice(null)}
            >
              Dismiss
            </button>
          </section>
        )}
        {workspaceDiagnostics.length > 0 && (
          <section
            className="banner banner-warn"
            aria-label="Workflow problems"
          >
            <p className="banner-title">Fix before running</p>
            <ul>
              {workspaceDiagnostics.map((item, index) => (
                <li key={`${item.code}-${index}`}>
                  {item.message} {item.remedy}
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>

      <div
        className="workspace"
        ref={scrollArea}
        onScroll={(event) => {
          scrollPosition.current = {
            x: Math.round(event.currentTarget.scrollLeft),
            y: Math.round(event.currentTarget.scrollTop),
          };
        }}
      >
        <div className="zoom-layer" style={{ transform: `scale(${zoom})` }}>
          <Workspace
            key={generation}
            document={open?.document ?? null}
            contracts={contracts ?? new Map()}
            names={names}
            regions={regions}
            layout={layout}
            expanded={expanded}
            focusMode={focusMode}
            moving={moving}
            diagnosticsByNode={diagnosticsByNode}
            registerNode={(id) => (element) => {
              if (element) {
                nodeElements.current.set(id, element);
              } else {
                nodeElements.current.delete(id);
              }
            }}
            onParameterChange={onParameterChange}
            onToggleExpanded={(id) =>
              setExpanded((current) => (current === id ? null : id))
            }
            onToggleFocusMode={(id) =>
              setFocusMode((current) => (current === id ? null : id))
            }
            onNodeKeyDown={onNodeKeyDown}
            onNodeBlur={onNodeBlur}
            onHeaderPointerDown={onHeaderPointerDown}
            onResize={resize}
            onGutterPointerDown={onGutterPointerDown}
          />
        </div>
      </div>

      {focusedNode && contracts && (
        <div
          className="focus-overlay"
          onClick={(event) => {
            if (event.target === event.currentTarget) {
              closeFocusMode();
            }
          }}
          onKeyDown={(event) => {
            if (event.key === "Escape") {
              event.preventDefault();
              closeFocusMode();
            } else if (event.key === "Tab") {
              // The panel is modal: Tab and Shift+Tab cycle inside it.
              const items = [
                ...event.currentTarget.querySelectorAll<HTMLElement>(FOCUSABLE),
              ].filter((item) => !item.matches(":disabled"));
              const first = items[0];
              const last = items.at(-1);
              const active = document.activeElement;
              const inside = event.currentTarget.contains(active);
              if (!first || !last) {
                return;
              }
              if (event.shiftKey && (active === first || !inside)) {
                event.preventDefault();
                last.focus();
              } else if (!event.shiftKey && (active === last || !inside)) {
                event.preventDefault();
                first.focus();
              }
            }
          }}
        >
          <div
            className="focus-panel"
            role="dialog"
            aria-modal="true"
            aria-label={`${names.get(focusedNode.id) ?? focusedNode.id}, focus mode`}
          >
            <NodeView
              node={focusedNode}
              contract={contracts.get(focusedNode.type)}
              name={names.get(focusedNode.id) ?? focusedNode.id}
              region={regionOf(focusedNode)}
              expanded
              focusMode
              moving={false}
              diagnostics={diagnosticsByNode.get(focusedNode.id) ?? []}
              registerElement={(element) => element?.focus()}
              onParameterChange={(key, value) =>
                onParameterChange(focusedNode.id, key, value)
              }
              onToggleExpanded={closeFocusMode}
              onToggleFocusMode={closeFocusMode}
              onKeyDown={() => undefined}
            />
          </div>
        </div>
      )}

      {confirmation && (
        <ConfirmDialog
          title={confirmation.title}
          body={confirmation.body}
          confirmLabel={confirmation.confirmLabel}
          onCancel={() => setConfirmation(null)}
          onConfirm={() => {
            setConfirmation(null);
            confirmation.onConfirm();
          }}
        />
      )}

      <div className="visually-hidden" aria-live="polite" role="status">
        {announcement}
      </div>
    </div>
  );
}
