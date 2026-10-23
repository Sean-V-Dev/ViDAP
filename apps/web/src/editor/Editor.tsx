// The ViDAP editor workspace (P3-EP04A), graph authoring (P3-EP04B), and run,
// results, error presentation, and boundary trace (P3-EP05). It opens, builds,
// edits, validates, saves, and runs slice workflows through `/api/slice/` only.

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import "./editor.css";
import {
  ApiError,
  type ChangeSummary,
  type Diagnostic,
  type Endpoint,
  type JsonValue,
  type RuntimeDiagnostic,
  type SliceClient,
  type SliceMetrics,
  type WorkflowDocument,
  type WorkflowSummary,
} from "./api";
import {
  connect,
  edgesTouching,
  newId,
  newWorkflow,
  withNode,
  withoutEdge,
  withoutNode,
} from "./authoring";
import { ConfirmDialog } from "./ConfirmDialog";
import {
  DEFAULT_REGION_WIDTH,
  MOVE_STEP,
  MOVE_STEP_LARGE,
  ZOOM_LEVELS,
  clampPosition,
  clampWidth,
  layoutFrom,
  placeNewNode,
  positionedNodes,
  sidecarFrom,
  type Layout,
} from "./layout";
import { useMeasuredHeights } from "./measure";
import {
  boundaryEntries,
  consumersOf,
  displayNames,
  downstream,
  formatMetrics,
  indexContracts,
  nodeById,
  portOf,
  regionOf,
  upstream,
  verticalNeighbour,
  visibleRegions,
  withParameter,
  type ContractIndex,
} from "./model";
import { NodeView, type NodeStatus } from "./NodeView";
import {
  UNASSIGNED,
  regionLabel,
  regionShortLabel,
  resultSummaryLabel,
} from "./presentation";
import { Workspace } from "./Workspace";

const VALIDATE_DELAY_MS = 400;
const FOCUSABLE =
  'button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])';

interface OpenWorkflow {
  /** `null` until a new workflow is first saved under a name. */
  name: string | null;
  workflowDigest: string | null;
  sidecarDigest: string | null;
  document: WorkflowDocument;
}

interface Conflict {
  missing: boolean;
  summary: ChangeSummary | null;
}

interface Notice {
  tone: "info" | "warn" | "error";
  title?: string;
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

/**
 * The node a diagnostic belongs on: an edge's consumer for an edge finding
 * (DESIGN.md Section 4), otherwise the node its reference starts with (node,
 * `nodeId:port`, `nodeId:parameter`). `null` means the workspace banner.
 */
function nodeIdOf(
  document: WorkflowDocument,
  diagnostic: Diagnostic,
): string | null {
  if (diagnostic.elementKind === "edge") {
    const edge = document.edges.find(
      (item) => item.id === diagnostic.elementReference,
    );
    return edge && nodeById(document, edge.target.nodeId)
      ? edge.target.nodeId
      : null;
  }
  const id = diagnostic.elementReference.slice(0, 36);
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
  const [saveAsOpen, setSaveAsOpen] = useState(false);
  const [connecting, setConnecting] = useState<Endpoint | null>(null);
  const [connectMessage, setConnectMessage] = useState<string | null>(null);
  const [validating, setValidating] = useState(false);
  const [running, setRunning] = useState(false);
  const [busy, setBusy] = useState(false);
  const [nodeStatuses, setNodeStatuses] = useState<
    ReadonlyMap<string, NodeStatus>
  >(new Map());
  const [runtimeDiagnostics, setRuntimeDiagnostics] = useState<
    RuntimeDiagnostic[]
  >([]);
  const [lastMetrics, setLastMetrics] = useState<SliceMetrics | null>(null);
  const [metricsStale, setMetricsStale] = useState(false);
  const [lastOutcome, setLastOutcome] = useState<"succeeded" | "failed" | null>(
    null,
  );
  const [tracing, setTracing] = useState<Endpoint | null>(null);
  const [nodeHeights, measureNode] = useMeasuredHeights();
  const nodeElements = useRef(new Map<string, HTMLDivElement>());
  const nodeCallbacks = useRef(
    new Map<string, (element: HTMLDivElement | null) => void>(),
  );
  const registerNode = useCallback(
    (id: string) => {
      const existing = nodeCallbacks.current.get(id);
      if (existing) {
        return existing;
      }
      const callback = (element: HTMLDivElement | null) => {
        if (element) {
          nodeElements.current.set(id, element);
        } else {
          nodeElements.current.delete(id);
        }
        measureNode(id)(element);
      };
      nodeCallbacks.current.set(id, callback);
      return callback;
    },
    [measureNode],
  );
  const focusedNodeElement = useRef<HTMLDivElement | null>(null);
  const registerFocusedNode = useCallback((element: HTMLDivElement | null) => {
    focusedNodeElement.current = element;
  }, []);
  const addButtons = useRef(new Map<string, HTMLButtonElement>());
  const validateTimer = useRef<number | undefined>(undefined);
  const validateSequence = useRef(0);
  const runSequence = useRef(0);
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

  // `action` (an authoring announcement) is said first and kept in front of
  // the verdict, so the live region never replaces one with the other.
  const requestValidation = useCallback(
    (document: WorkflowDocument, immediate = false, action = "") => {
      window.clearTimeout(validateTimer.current);
      const sequence = ++validateSequence.current;
      setValidating(true);
      if (action) {
        announce(action);
      }
      const run = () => {
        client.validate(document).then(
          (result) => {
            if (sequence === validateSequence.current) {
              setValidating(false);
              setDiagnostics(result.diagnostics);
              const verdict = result.valid
                ? "Workflow is valid."
                : `${result.diagnostics.length} ${result.diagnostics.length === 1 ? "problem" : "problems"} to fix before running.`;
              announce(action ? `${action} ${verdict}` : verdict);
            }
          },
          (error: unknown) => {
            if (
              sequence === validateSequence.current &&
              error instanceof ApiError
            ) {
              setValidating(false);
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

  const clearRunOnOpen = () => {
    runSequence.current += 1;
    setRunning(false);
    setBusy(false);
    setNodeStatuses(new Map());
    setRuntimeDiagnostics([]);
    setLastMetrics(null);
    setMetricsStale(false);
    setLastOutcome(null);
    setTracing(null);
  };

  const markRunEdited = (document: WorkflowDocument) => {
    runSequence.current += 1;
    setRunning(false);
    setBusy(false);
    setNodeStatuses(new Map());
    setRuntimeDiagnostics([]);
    setLastOutcome(null);
    setMetricsStale((current) => current || lastMetrics !== null);
    if (
      tracing &&
      !boundaryEntries(document).outputs.some(
        (entry) =>
          entry.nodeId === tracing.nodeId && entry.portKey === tracing.portKey,
      )
    ) {
      setTracing(null);
    }
  };

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
          setConnecting(null);
          setConnectMessage(null);
          setSaveAsOpen(false);
          clearRunOnOpen();
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

  // The channel saves only valid workflows; a refusal keeps the work open and
  // unsaved and lists what to fix (P3-EP04B §5.2).
  const refusedSave = (error: unknown): boolean => {
    if (error instanceof ApiError && error.code === "invalid-workflow") {
      setNotice({
        tone: "warn",
        title: "Fix before saving",
        text: error.message,
        diagnostics: error.diagnostics,
      });
      announce("Save refused: the workflow has problems to fix.");
      return true;
    }
    return false;
  };

  const save = () => {
    if (!open) {
      return;
    }
    const name = open.name;
    if (name === null) {
      setSaveAsOpen(true);
      return;
    }
    const sidecar = currentSidecar(open.document);
    client
      .save(
        name,
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
          announce(`Saved ${name}.`);
        },
        (error: unknown) => {
          if (error instanceof ApiError && error.code === "conflict") {
            setConflict({ missing: error.missing, summary: error.summary });
            announce(
              "Save refused: the saved files changed outside the editor.",
            );
          } else if (!refusedSave(error)) {
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
        setSaveAsOpen(false);
        setNotice(null);
        announce(`Saved as ${result.name}.`);
      },
      (error: unknown) => {
        if (refusedSave(error)) {
          return;
        }
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

  const startNew = () => {
    const document = newWorkflow(newId());
    setOpen({
      name: null,
      workflowDigest: null,
      sidecarDigest: null,
      document,
    });
    setLayout(layoutFrom(document, null).layout);
    setDirty(true);
    setExpanded(null);
    setFocusMode(null);
    setMoving(null);
    setConflict(null);
    setListing(null);
    setNotice(null);
    setDiagnostics([]);
    setConnecting(null);
    setConnectMessage(null);
    setSaveAsOpen(false);
    clearRunOnOpen();
    setGeneration((value) => value + 1);
    announce("Started a new workflow.");
    requestValidation(document, true);
  };

  // Outside changes: check whenever the window regains focus (D3.3). A new
  // workflow has no saved files yet, so there is nothing to compare.
  useEffect(() => {
    if (!open) {
      return;
    }
    const { name, workflowDigest } = open;
    if (name === null || workflowDigest === null) {
      return;
    }
    const onFocus = () => {
      client
        .compare(name, open.document, workflowDigest, open.sidecarDigest)
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
    if (!tracing || connecting || focusMode || moving || confirmation) {
      return;
    }
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        setTracing(null);
        announce("Trace closed.");
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [tracing, connecting, focusMode, moving, confirmation, announce]);

  useEffect(() => {
    if (focusMode) {
      focusedNodeElement.current?.focus();
    }
  }, [focusMode]);

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
      const id = nodeIdOf(open.document, item);
      if (id) {
        result.set(id, [...(result.get(id) ?? []), item]);
      }
    }
    return result;
  }, [diagnostics, open]);
  const workspaceDiagnostics = open
    ? diagnostics.filter((item) => !nodeIdOf(open.document, item))
    : [];
  const runtimeDiagnosticsByNode = useMemo(() => {
    const result = new Map<string, RuntimeDiagnostic[]>();
    if (!open) {
      return result;
    }
    for (const item of runtimeDiagnostics) {
      if (
        item.nodeId &&
        open.document.nodes.some((node) => node.id === item.nodeId)
      ) {
        result.set(item.nodeId, [...(result.get(item.nodeId) ?? []), item]);
      }
    }
    return result;
  }, [runtimeDiagnostics, open]);
  const workspaceRuntimeDiagnostics = open
    ? runtimeDiagnostics.filter(
        (item) =>
          !item.nodeId ||
          !open.document.nodes.some((node) => node.id === item.nodeId),
      )
    : [];
  const recordedResult = lastMetrics
    ? { metrics: lastMetrics, stale: metricsStale }
    : null;
  // Connections and input ports the backend found a problem with (DESIGN.md
  // Section 4): edge findings by edge ID; port findings, and the consumer end
  // of each problem edge, as `nodeId:port`.
  const { invalidEdges, problemPorts } = useMemo(() => {
    const edges = new Set<string>();
    const ports = new Set<string>();
    for (const item of diagnostics) {
      if (item.elementKind === "edge") {
        const edge = open?.document.edges.find(
          (candidate) => candidate.id === item.elementReference,
        );
        if (edge) {
          edges.add(edge.id);
          ports.add(`${edge.target.nodeId}:${edge.target.portKey}`);
        }
      } else if (item.elementKind === "port") {
        ports.add(item.elementReference);
      }
    }
    return { invalidEdges: edges, problemPorts: ports };
  }, [diagnostics, open]);

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
      case "Delete":
        event.preventDefault();
        requestRemove(id);
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
    markRunEdited(document);
    requestValidation(document);
  };

  // --- Authoring (P3-EP04B). Every edit changes only nodes and edges, marks
  // the workflow unsaved, and asks the backend to validate the result. ---

  // A discrete edit (not typing) is validated at once, not after the pause;
  // `action` is announced, then the verdict after it.
  const applyDocument = (document: WorkflowDocument, action: string) => {
    if (!open) {
      return;
    }
    setOpen({ ...open, document });
    setDirty(true);
    markRunEdited(document);
    requestValidation(document, true, action);
  };

  const valueLabel = (endpoint: Endpoint) =>
    `${names.get(endpoint.nodeId) ?? endpoint.nodeId}.${endpoint.portKey}`;

  const addNode = (region: string, type: string) => {
    if (!open || !contracts) {
      return;
    }
    const id = newId();
    const position = placeNewNode(
      open.document,
      layout.positions,
      region,
      nodeHeights,
    );
    const document = withNode(open.document, id, type);
    setLayout((current) => ({
      ...current,
      positions: { ...current.positions, [id]: position },
    }));
    const name = displayNames(document, contracts).get(id) ?? id;
    applyDocument(document, `Added ${name} to ${regionLabel(region)}.`);
    window.setTimeout(() => focusNode(id), 0);
  };

  const removeNode = (id: string) => {
    if (!open) {
      return;
    }
    const node = nodeById(open.document, id);
    if (!node) {
      return;
    }
    const name = names.get(id) ?? id;
    const region = regionOf(node);
    const above = verticalNeighbour(
      id,
      -1,
      positionedNodes(open.document, layout.positions),
    );
    setLayout((current) => {
      const positions = { ...current.positions };
      delete positions[id];
      return { ...current, positions };
    });
    if (expanded === id) {
      setExpanded(null);
    }
    if (focusMode === id) {
      setFocusMode(null);
    }
    if (moving === id) {
      setMoving(null);
    }
    if (connecting?.nodeId === id) {
      setConnecting(null);
      setConnectMessage(null);
    }
    applyDocument(withoutNode(open.document, id), `Removed ${name}.`);
    window.setTimeout(() => {
      if (above) {
        focusNode(above);
      } else {
        addButtons.current.get(region)?.focus();
      }
    }, 0);
  };

  const requestRemove = (id: string) => {
    if (!open) {
      return;
    }
    const name = names.get(id) ?? id;
    const count = edgesTouching(open.document, id).length;
    setConfirmation({
      title: `Remove ${name}?`,
      body:
        count === 0
          ? "It has no connections."
          : `Its ${count} ${count === 1 ? "connection is" : "connections are"} removed too.`,
      confirmLabel: "Remove",
      onConfirm: () => removeNode(id),
    });
  };

  const startConnecting = (source: Endpoint) => {
    setConnecting(source);
    setConnectMessage(null);
    announce(
      `Connecting from ${valueLabel(source)}. Choose an input port; Escape cancels.`,
    );
  };

  const cancelConnecting = () => {
    setConnecting(null);
    setConnectMessage(null);
    announce("Connecting cancelled.");
  };

  const completeConnection = (source: Endpoint, target: Endpoint) => {
    if (!open || !contracts) {
      return;
    }
    const outcome = connect(open.document, contracts, source, target, newId());
    const targetNode = nodeById(open.document, target.nodeId);
    const targetName = names.get(target.nodeId) ?? target.nodeId;
    const portLabel =
      (targetNode &&
        portOf(contracts, targetNode, target.portKey, "input")?.label) ??
      target.portKey;
    switch (outcome.kind) {
      case "incompatible": {
        const message = `${targetName}'s ${portLabel} expects ${outcome.expected}, not ${outcome.offered}.`;
        setConnectMessage(message);
        announce(message);
        return;
      }
      case "duplicate":
        setConnecting(null);
        setConnectMessage(null);
        announce("Already connected.");
        return;
      case "replaced":
        applyDocument(
          outcome.document,
          `Replaced the connection from ${valueLabel(outcome.replaced[0].source)}.`,
        );
        setConnecting(null);
        setConnectMessage(null);
        return;
      case "created":
        applyDocument(
          outcome.document,
          `Connected ${valueLabel(source)} to ${targetName}'s ${portLabel}.`,
        );
        setConnecting(null);
        setConnectMessage(null);
        return;
    }
  };

  const onPortActivate = (
    nodeId: string,
    direction: "input" | "output",
    portKey: string,
  ) => {
    if (direction === "output") {
      startConnecting({ nodeId, portKey });
    } else if (connecting) {
      completeConnection(connecting, { nodeId, portKey });
    } else {
      announce("Start from an output port to connect.");
    }
  };

  // Dragging from an output port: releasing over an input port completes the
  // connection; releasing anywhere else leaves connecting active.
  const onPortPointerDown = (
    nodeId: string,
    direction: "input" | "output",
    portKey: string,
    event: React.PointerEvent<HTMLButtonElement>,
  ) => {
    if (direction !== "output" || event.button !== 0) {
      return;
    }
    const source = { nodeId, portKey };
    startConnecting(source);
    const onUp = (up: PointerEvent) => {
      window.removeEventListener("pointerup", onUp);
      const target =
        up.target instanceof Element
          ? up.target.closest<HTMLElement>('[data-port-direction="input"]')
          : null;
      const targetNode = target?.dataset.nodeId;
      const targetPort = target?.dataset.portKey;
      if (targetNode && targetPort) {
        completeConnection(source, { nodeId: targetNode, portKey: targetPort });
      }
    };
    window.addEventListener("pointerup", onUp);
  };

  const disconnect = (edgeId: string) => {
    if (!open || !contracts) {
      return;
    }
    const edge = open.document.edges.find((item) => item.id === edgeId);
    if (!edge) {
      return;
    }
    applyDocument(
      withoutEdge(open.document, edgeId),
      `Disconnected ${valueLabel(edge.source)} from ${names.get(edge.target.nodeId) ?? edge.target.nodeId}.`,
    );
  };

  const closeFocusMode = () => {
    const id = focusMode;
    setFocusMode(null);
    if (id) {
      window.setTimeout(() => focusNode(id), 0);
    }
  };

  const describeEndpoint = (nodeId: string, portKey: string) => {
    const target = open ? nodeById(open.document, nodeId) : undefined;
    const region = target ? regionShortLabel(regionOf(target)) : UNASSIGNED.key;
    return `${region} / ${names.get(nodeId) ?? nodeId} (${portKey})`;
  };

  const toggleTrace = (source: Endpoint) => {
    if (!open) {
      return;
    }
    if (
      tracing &&
      tracing.nodeId === source.nodeId &&
      tracing.portKey === source.portKey
    ) {
      setTracing(null);
      announce("Trace closed.");
      return;
    }
    setTracing(source);
    const consumers = consumersOf(open.document, source.nodeId, source.portKey);
    const consumerText = consumers
      .map((item) => describeEndpoint(item.nodeId, item.portKey))
      .join(", ");
    announce(
      `Tracing ${valueLabel(source)}. From ${describeEndpoint(source.nodeId, source.portKey)} to ${consumers.length} ${consumers.length === 1 ? "consumer" : "consumers"}: ${consumerText}.`,
    );
  };

  const exitTrace = () => {
    setTracing(null);
    announce("Trace closed.");
  };

  const runReason = !open
    ? "Open or create a workflow to run."
    : open.document.nodes.length === 0
      ? "Add the slice nodes before running."
      : diagnostics.length > 0
        ? `${diagnostics.length} ${diagnostics.length === 1 ? "problem" : "problems"} to fix before running.`
        : validating
          ? "Checking workflow…"
          : running
            ? "Run in progress."
            : null;
  const canRun = runReason === null;

  const runWorkflow = () => {
    if (!open || !canRun) {
      return;
    }
    const sequence = ++runSequence.current;
    const doc = open.document;
    setRunning(true);
    setBusy(false);
    setNotice(null);
    setRuntimeDiagnostics([]);
    setNodeStatuses(
      new Map(doc.nodes.map((item) => [item.id, "running" as const])),
    );
    announce("Running workflow.");
    client.run(doc).then(
      (result) => {
        if (sequence !== runSequence.current) {
          return;
        }
        setRunning(false);
        setNodeStatuses(
          new Map(result.nodes.map((item) => [item.nodeId, item.status])),
        );
        setRuntimeDiagnostics(result.diagnostics);
        setLastOutcome(result.outcome);
        if (result.outcome === "succeeded" && result.metrics !== null) {
          setLastMetrics(result.metrics);
          setMetricsStale(false);
          announce(`Run completed. ${formatMetrics(result.metrics)}.`);
        } else {
          setMetricsStale((current) => current || lastMetrics !== null);
          const failedId =
            result.diagnostics.find((item) => item.nodeId)?.nodeId ??
            result.nodes.find((item) => item.status === "failed")?.nodeId;
          const failedName = failedId
            ? (names.get(failedId) ?? failedId)
            : null;
          announce(failedName ? `Run failed on ${failedName}.` : "Run failed.");
        }
      },
      (error: unknown) => {
        if (sequence !== runSequence.current) {
          return;
        }
        setRunning(false);
        setNodeStatuses(new Map());
        if (error instanceof ApiError && error.code === "busy") {
          setBusy(true);
          announce("Another run is in progress.");
        } else if (
          error instanceof ApiError &&
          error.code === "invalid-workflow"
        ) {
          setDiagnostics(error.diagnostics);
          setNotice({
            tone: "warn",
            title: "Fix before running",
            text: error.message,
            diagnostics: error.diagnostics,
          });
          announce("Run refused: the workflow has problems to fix.");
        } else {
          const message =
            error instanceof ApiError
              ? error.attemptId
                ? `${error.message} (Attempt ${error.attemptId})`
                : error.message
              : "The workflow could not be run.";
          setNotice({
            tone: "error",
            title: "Run failed",
            text: message,
            diagnostics:
              error instanceof ApiError ? error.diagnostics : undefined,
          });
          announce(message);
        }
      },
    );
  };

  const failedNodeId =
    runtimeDiagnostics.find((item) => item.nodeId)?.nodeId ??
    [...nodeStatuses.entries()].find(([, status]) => status === "failed")?.[0];
  const failedNodeName = failedNodeId
    ? (names.get(failedNodeId) ?? failedNodeId)
    : null;
  const tracedConsumers =
    tracing && open
      ? consumersOf(open.document, tracing.nodeId, tracing.portKey)
      : [];

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
    <div
      className="editor"
      onKeyDownCapture={(event) => {
        // Escape cancels connecting before anything else sees it.
        if (connecting && event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          cancelConnecting();
        } else if (
          tracing &&
          !focusMode &&
          !moving &&
          !confirmation &&
          event.key === "Escape"
        ) {
          event.preventDefault();
          event.stopPropagation();
          exitTrace();
        }
      }}
    >
      <header className="top-bar">
        <h1 className="product">ViDAP</h1>
        <p className="workflow-state" aria-live="off">
          {open ? (
            <>
              <span className="workflow-name">{open.name ?? "Untitled"}</span>{" "}
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
            onClick={() =>
              confirmThen(
                startNew,
                "Discard unsaved changes?",
                "Starting a new workflow discards the changes you have not saved.",
                "Discard and start new",
              )
            }
          >
            New
          </button>
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
          <button
            type="button"
            className="button"
            onClick={() => setSaveAsOpen(true)}
            disabled={!open}
            aria-expanded={saveAsOpen}
          >
            Save as…
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
        <p className="primary-result" aria-label="Primary result">
          <span className="result-label">
            {lastMetrics && metricsStale ? "Last run" : "Result"}
          </span>{" "}
          {lastMetrics ? (
            <>
              <span className="result-value">{formatMetrics(lastMetrics)}</span>
              {running && <span className="result-note"> · Running…</span>}
              {!running && lastOutcome === "failed" && (
                <span className="result-failed">
                  {" "}
                  · Run failed{failedNodeName ? ` on ${failedNodeName}` : ""}
                </span>
              )}
            </>
          ) : running ? (
            <span>Running…</span>
          ) : lastOutcome === "failed" ? (
            <span className="result-failed">
              Run failed{failedNodeName ? ` on ${failedNodeName}` : ""}
            </span>
          ) : (
            <span>—</span>
          )}
        </p>
        <div className="run-area">
          <button
            type="button"
            className="button button-primary"
            disabled={!canRun}
            aria-busy={running || undefined}
            aria-describedby={runReason ? "run-reason" : undefined}
            onClick={runWorkflow}
          >
            {running ? "Running…" : "Run"}
          </button>
          {runReason && (
            <span id="run-reason" className="run-reason">
              {runReason}
            </span>
          )}
        </div>
      </header>

      <div className="banners">
        {tracing && open && (
          <section className="banner banner-info" aria-label="Trace">
            <p className="banner-title">Tracing {valueLabel(tracing)}</p>
            <p>
              From {describeEndpoint(tracing.nodeId, tracing.portKey)} to{" "}
              {tracedConsumers.length}{" "}
              {tracedConsumers.length === 1 ? "consumer" : "consumers"}:{" "}
              {tracedConsumers
                .map((item) => describeEndpoint(item.nodeId, item.portKey))
                .join(", ")}
              . Dashed lines show the real connections temporarily.
            </p>
            <button type="button" className="button" onClick={exitTrace}>
              Exit trace
            </button>
          </section>
        )}
        {busy && (
          <section className="banner banner-info" aria-label="Run busy">
            <p className="banner-title">Another run is in progress.</p>
            <p>
              ViDAP runs one workflow at a time. Try again when it finishes.
            </p>
            <div className="banner-actions">
              <button
                type="button"
                className="button"
                onClick={runWorkflow}
                disabled={!canRun}
              >
                Retry
              </button>
              <button
                type="button"
                className="button"
                onClick={() => setBusy(false)}
              >
                Dismiss
              </button>
            </div>
          </section>
        )}
        {connecting && (
          <section className="banner banner-info" aria-label="Connecting">
            <p className="banner-title">
              Connecting from {valueLabel(connecting)} — choose an input port.
              Escape cancels.
            </p>
            {connectMessage && <p>{connectMessage}</p>}
            <button type="button" className="button" onClick={cancelConnecting}>
              Cancel
            </button>
          </section>
        )}
        {saveAsOpen && open && !conflict && (
          <section className="banner banner-info" aria-label="Save as">
            <p className="banner-title">Save as</p>
            <div className="banner-actions">
              <label className="save-as">
                <span>Name</span>
                <input
                  type="text"
                  value={saveAsName}
                  onChange={(event) => setSaveAsName(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && saveAsName.trim() !== "") {
                      saveAs();
                    }
                  }}
                />
              </label>
              <button
                type="button"
                className="button"
                onClick={saveAs}
                disabled={saveAsName.trim() === ""}
              >
                Save
              </button>
              <button
                type="button"
                className="button"
                onClick={() => setSaveAsOpen(false)}
              >
                Cancel
              </button>
            </div>
          </section>
        )}
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
                    onConfirm: () => {
                      if (open.name !== null) {
                        loadWorkflow(open.name);
                      }
                    },
                  })
                }
                disabled={conflict.missing || open.name === null}
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
            {notice.title && <p className="banner-title">{notice.title}</p>}
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
        {workspaceRuntimeDiagnostics.length > 0 && (
          <section className="banner banner-error" aria-label="Run failed">
            <p className="banner-title">Run failed</p>
            {workspaceRuntimeDiagnostics.map((item, index) => (
              <div key={`${item.code}-${item.attemptId}-${index}`}>
                <p className="message-headline">{item.explanation}</p>
                <p className="message-remedy">{item.remedy}</p>
                <details className="message-details">
                  <summary>Technical details</summary>
                  <p>
                    {item.code} · Attempt {item.attemptId}
                  </p>
                  <p>{item.technical.message}</p>
                </details>
              </div>
            ))}
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
            registerNode={registerNode}
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
            nodeHeights={nodeHeights}
            measureNode={measureNode}
            connecting={connecting}
            invalidEdges={invalidEdges}
            problemPorts={problemPorts}
            onAddNode={addNode}
            registerAddButton={(region) => (element) => {
              if (element) {
                addButtons.current.set(region, element);
              } else {
                addButtons.current.delete(region);
              }
            }}
            onPortActivate={onPortActivate}
            onPortPointerDown={onPortPointerDown}
            onDisconnect={disconnect}
            onRemoveNode={requestRemove}
            nodeStatuses={nodeStatuses}
            runtimeDiagnosticsByNode={runtimeDiagnosticsByNode}
            recordedResult={recordedResult}
            tracing={tracing}
            onToggleTrace={toggleTrace}
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
              status={nodeStatuses.get(focusedNode.id) ?? "not-run"}
              runtimeDiagnostics={
                runtimeDiagnosticsByNode.get(focusedNode.id) ?? []
              }
              recordedResult={
                resultSummaryLabel(focusedNode.type) ? recordedResult : null
              }
              registerElement={registerFocusedNode}
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
