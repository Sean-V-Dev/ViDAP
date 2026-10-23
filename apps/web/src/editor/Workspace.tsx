// Regions, gutters, boundary rails, and wires (DESIGN.md Section 4). Each
// region draws only its own wires inside its own bounds, so nothing can cross
// a gutter: values leave through the Outputs rail and arrive on Inputs rails.

import { Fragment, useState } from "react";
import type {
  Diagnostic,
  Endpoint,
  JsonValue,
  RuntimeDiagnostic,
  WorkflowDocument,
  WorkflowNode,
} from "./api";
import { AddMenu } from "./AddMenu";
import { compatible, typesForRegion } from "./authoring";
import type { ContractIndex, InputEntry, OutputEntry } from "./model";
import {
  boundaryEntries,
  consumersOf,
  localEdges,
  nodeById,
  regionOf,
  traceEdges,
} from "./model";
import {
  DEFAULT_REGION_WIDTH,
  GUTTER_STEP,
  GUTTER_STEP_LARGE,
  GUTTER_WIDTH,
  MAX_REGION_WIDTH,
  RAIL_WIDTH,
  REGION_HEADER,
  displayX,
  minimumWidth,
  nodeWidth,
  portOffset,
  pushDownOffsets,
  regionHeight,
  stackRail,
  type Layout,
} from "./layout";
import { useMeasuredHeights, type MeasureRef } from "./measure";
import {
  NodeView,
  type InputConnections,
  type NodeStatus,
  type PortState,
  type RecordedNodeResult,
} from "./NodeView";
import {
  UNASSIGNED,
  regionLabel,
  regionShortLabel,
  resultSummaryLabel,
} from "./presentation";

export interface WorkspaceProps {
  document: WorkflowDocument | null;
  contracts: ContractIndex;
  names: ReadonlyMap<string, string>;
  regions: string[];
  layout: Layout;
  expanded: string | null;
  focusMode: string | null;
  moving: string | null;
  diagnosticsByNode: ReadonlyMap<string, Diagnostic[]>;
  registerNode: (id: string) => (element: HTMLDivElement | null) => void;
  onParameterChange: (nodeId: string, key: string, value: JsonValue) => void;
  onToggleExpanded: (nodeId: string) => void;
  onToggleFocusMode: (nodeId: string) => void;
  onNodeKeyDown: (
    nodeId: string,
    event: React.KeyboardEvent<HTMLDivElement>,
  ) => void;
  onNodeBlur: (nodeId: string, event: React.FocusEvent<HTMLDivElement>) => void;
  onHeaderPointerDown: (
    nodeId: string,
    event: React.PointerEvent<HTMLDivElement>,
  ) => void;
  onResize: (region: string, width: number) => void;
  onGutterPointerDown: (
    region: string,
    event: React.PointerEvent<HTMLDivElement>,
  ) => void;
  // Measured node heights (owned by the editor, which also places new nodes).
  nodeHeights: Readonly<Record<string, number>>;
  measureNode: MeasureRef;
  // Authoring (P3-EP04B).
  connecting: Endpoint | null;
  invalidEdges: ReadonlySet<string>;
  problemPorts: ReadonlySet<string>;
  onAddNode: (region: string, type: string) => void;
  registerAddButton: (
    region: string,
  ) => (element: HTMLButtonElement | null) => void;
  onPortActivate: (
    nodeId: string,
    direction: "input" | "output",
    key: string,
  ) => void;
  onPortPointerDown: (
    nodeId: string,
    direction: "input" | "output",
    key: string,
    event: React.PointerEvent<HTMLButtonElement>,
  ) => void;
  onDisconnect: (edgeId: string) => void;
  onRemoveNode: (nodeId: string) => void;
  // Run, results, and trace (P3-EP05).
  nodeStatuses?: ReadonlyMap<string, NodeStatus>;
  runtimeDiagnosticsByNode?: ReadonlyMap<string, RuntimeDiagnostic[]>;
  recordedResult?: RecordedNodeResult | null;
  tracing?: Endpoint | null;
  onToggleTrace?: (source: Endpoint) => void;
}

const ENTRY_HALF = 12;

function curve(x1: number, y1: number, x2: number, y2: number): string {
  const bend = Math.max(24, Math.abs(x2 - x1) / 2);
  return `M ${x1} ${y1} C ${x1 + bend} ${y1}, ${x2 - bend} ${y2}, ${x2} ${y2}`;
}

interface HoverCard {
  id: string;
  lines: string[];
}

export function Workspace(props: WorkspaceProps) {
  const { document, contracts, names, layout, expanded, nodeHeights } = props;
  const [card, setCard] = useState<HoverCard | null>(null);
  const [railHeights, measureRail] = useMeasuredHeights();
  const offsets = document
    ? pushDownOffsets(
        document,
        layout.positions,
        expanded,
        nodeHeights,
        layout.widths,
      )
    : {};
  const height = regionHeight(
    document,
    layout.positions,
    expanded,
    nodeHeights,
    layout.widths,
  );
  // A node lifted into focus mode leaves its slot empty; its wires are hidden
  // while it is lifted (DESIGN.md Section 5).
  const lifted = (nodeId: string) => nodeId === props.focusMode;
  const boundaries = document
    ? boundaryEntries(document)
    : { outputs: [] as OutputEntry[], inputs: [] as InputEntry[] };
  const contractList = [...contracts.values()];
  const tracedValue = props.tracing
    ? `${props.tracing.nodeId}:${props.tracing.portKey}`
    : null;
  const tracedNodes = new Set<string>(
    props.tracing && document
      ? [
          props.tracing.nodeId,
          ...consumersOf(
            document,
            props.tracing.nodeId,
            props.tracing.portKey,
          ).map((consumer) => consumer.nodeId),
        ]
      : [],
  );
  const regionLeft = new Map<string, number>();
  let cursorX = 0;
  for (const region of props.regions) {
    regionLeft.set(region, cursorX);
    cursorX += (layout.widths[region] ?? DEFAULT_REGION_WIDTH) + GUTTER_WIDTH;
  }
  const totalWidth = Math.max(0, cursorX - GUTTER_WIDTH);
  const wireTraceClass = (sourceValue: string) =>
    tracedValue === null
      ? ""
      : sourceValue === tracedValue
        ? " wire-trace-hot"
        : " wire-trace-dim";
  // Outputs whose value feeds a connection the backend found invalid.
  const invalidOutputs = new Set(
    (document?.edges ?? [])
      .filter((edge) => props.invalidEdges.has(edge.id))
      .map((edge) => `${edge.source.nodeId}:${edge.source.portKey}`),
  );
  const nodeX = (nodeId: string) => {
    const position = layout.positions[nodeId];
    const node = document ? nodeById(document, nodeId) : undefined;
    if (!position || !node) {
      return 0;
    }
    return displayX(
      position,
      nodeId === expanded,
      layout.widths[regionOf(node)] ?? DEFAULT_REGION_WIDTH,
    );
  };
  const valueText = (nodeId: string, portKey: string) =>
    `${names.get(nodeId) ?? nodeId}.${portKey}`;
  const connectionsOf = (node: WorkflowNode): InputConnections[] =>
    (contracts.get(node.type)?.inputs ?? []).map((port) => ({
      portKey: port.key,
      label: port.label,
      sources: (document?.edges ?? [])
        .filter(
          (edge) =>
            edge.target.nodeId === node.id && edge.target.portKey === port.key,
        )
        .map((edge) => ({
          edgeId: edge.id,
          text: valueText(edge.source.nodeId, edge.source.portKey),
        })),
    }));
  const portState = (
    nodeId: string,
    direction: "input" | "output",
    key: string,
  ): PortState => {
    const source = props.connecting;
    if (!source || !document) {
      return null;
    }
    if (direction === "output") {
      return source.nodeId === nodeId && source.portKey === key
        ? "source"
        : null;
    }
    return compatible(document, contracts, source, { nodeId, portKey: key })
      ? "compatible"
      : "incompatible";
  };

  const portY = (
    nodeId: string,
    key: string,
    direction: "input" | "output",
  ) => {
    const node = document ? nodeById(document, nodeId) : undefined;
    const position = layout.positions[nodeId];
    if (!node || !position) {
      return REGION_HEADER;
    }
    return (
      REGION_HEADER +
      position.y +
      (offsets[nodeId] ?? 0) +
      portOffset(contracts.get(node.type), key, direction)
    );
  };
  // A line may break only after the dot, never inside a name (DESIGN.md
  // Section 2: rail text wraps and is never truncated).
  const valueName = (nodeId: string, portKey: string) => (
    <>
      {names.get(nodeId) ?? nodeId}.<wbr />
      {portKey}
    </>
  );
  const describe = (nodeId: string, portKey: string) => {
    const node = document ? nodeById(document, nodeId) : undefined;
    return `${regionShortLabel(node ? regionOf(node) : UNASSIGNED.key)} / ${names.get(nodeId) ?? nodeId} (${portKey})`;
  };
  const cardFor = (entry: OutputEntry): string[] => [
    `Produced by ${describe(entry.nodeId, entry.portKey)}`,
    ...entry.consumers.map(
      (consumer) => `Used by ${describe(consumer.nodeId, consumer.portKey)}`,
    ),
  ];
  const typeOf = (
    nodeId: string,
    portKey: string,
    direction: "input" | "output",
  ) => {
    const node = document ? nodeById(document, nodeId) : undefined;
    const ports =
      direction === "input"
        ? contracts.get(node?.type ?? "")?.inputs
        : contracts.get(node?.type ?? "")?.outputs;
    return ports?.find((port) => port.key === portKey)?.nominalType ?? "value";
  };

  return (
    <div className="workspace-rows">
      <div className="regions" style={{ height }}>
        {props.regions.map((region, index) => {
          const width = layout.widths[region] ?? 400;
          const nodes = document
            ? document.nodes.filter((node) => regionOf(node) === region)
            : [];
          const outputs = boundaries.outputs.filter(
            (entry) => entry.region === region,
          );
          const inputs = boundaries.inputs.filter(
            (entry) => entry.region === region,
          );
          const outputY = stackRail(
            outputs.map((entry) => ({
              id: `${entry.nodeId}:${entry.portKey}`,
              y: portY(entry.nodeId, entry.portKey, "output") - ENTRY_HALF,
            })),
            railHeights,
          );
          const inputY = stackRail(
            inputs.map((entry) => ({
              id: entry.edgeId,
              y: portY(entry.nodeId, entry.portKey, "input") - ENTRY_HALF,
            })),
            railHeights,
          );
          const isLast = index === props.regions.length - 1;
          const minimum = minimumWidth(document, region, layout.positions);
          const label = regionLabel(region);
          return (
            <Fragment key={region}>
              <section
                className={`region${region === UNASSIGNED.key ? " region-unassigned" : ""}`}
                style={{ width, height }}
                aria-label={`${label} region`}
                data-region={region}
              >
                <header className="region-header">
                  <h2>{label}</h2>
                  <span className="region-count">
                    {nodes.length} {nodes.length === 1 ? "node" : "nodes"}
                  </span>
                  {document && region !== UNASSIGNED.key && (
                    <AddMenu
                      regionLabel={label}
                      types={typesForRegion(contractList, region)}
                      onAdd={(type) => props.onAddNode(region, type)}
                      registerButton={props.registerAddButton(region)}
                    />
                  )}
                </header>
                <div
                  className="rail rail-inputs"
                  aria-label={`${label} inputs`}
                  role="list"
                >
                  <span className="rail-title" aria-hidden="true">
                    Inputs
                  </span>
                  {inputs.map((entry) => {
                    const id = entry.edgeId;
                    const top = inputY.get(id) ?? REGION_HEADER;
                    const invalid = props.invalidEdges.has(id);
                    const sourceKey = `${entry.source.nodeId}:${entry.source.portKey}`;
                    const isLit =
                      tracedValue !== null && sourceKey === tracedValue;
                    const isDim = tracedValue !== null && !isLit;
                    const traceClass = isLit
                      ? " rail-entry-lit"
                      : isDim
                        ? " rail-entry-dim"
                        : "";
                    return (
                      <div
                        role="listitem"
                        key={id}
                        ref={measureRail(id)}
                        style={{ top: top - REGION_HEADER }}
                        className="rail-slot"
                      >
                        <button
                          type="button"
                          className={`rail-entry type-${typeOf(entry.source.nodeId, entry.source.portKey, "output")}${invalid ? " rail-entry-invalid" : ""}${traceClass}`}
                          data-rail="input"
                          data-edge-id={entry.edgeId}
                          data-value={sourceKey}
                          data-trace-state={
                            isLit ? "highlighted" : isDim ? "dimmed" : undefined
                          }
                          aria-pressed={isLit}
                          onClick={() =>
                            props.onToggleTrace?.({
                              nodeId: entry.source.nodeId,
                              portKey: entry.source.portKey,
                            })
                          }
                          onKeyDown={(event) => {
                            if (event.key === "Enter" || event.key === " ") {
                              event.preventDefault();
                              props.onToggleTrace?.({
                                nodeId: entry.source.nodeId,
                                portKey: entry.source.portKey,
                              });
                            }
                          }}
                          onMouseEnter={() =>
                            setCard({
                              id,
                              lines: cardFor({
                                ...entry.source,
                                consumers: document
                                  ? consumersOf(
                                      document,
                                      entry.source.nodeId,
                                      entry.source.portKey,
                                    )
                                  : [],
                              }),
                            })
                          }
                          onMouseLeave={() => setCard(null)}
                          onFocus={() =>
                            setCard({
                              id,
                              lines: cardFor({
                                ...entry.source,
                                consumers: document
                                  ? consumersOf(
                                      document,
                                      entry.source.nodeId,
                                      entry.source.portKey,
                                    )
                                  : [],
                              }),
                            })
                          }
                          onBlur={() => setCard(null)}
                        >
                          <span className="rail-name">
                            {valueName(
                              entry.source.nodeId,
                              entry.source.portKey,
                            )}
                          </span>
                          <span className="rail-sub">
                            {invalid
                              ? "⚠ not allowed here"
                              : `from ${regionShortLabel(entry.source.region)}`}
                          </span>
                        </button>
                        {card?.id === id && (
                          <div className="hover-card" role="tooltip">
                            {card.lines.map((line) => (
                              <p key={line}>{line}</p>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
                <svg
                  className="wires"
                  width={width}
                  height={height}
                  aria-hidden="true"
                  focusable="false"
                >
                  {document &&
                    localEdges(document)
                      .filter((edge) => {
                        const source = nodeById(document, edge.source.nodeId);
                        return (
                          source !== undefined &&
                          regionOf(source) === region &&
                          !lifted(edge.source.nodeId) &&
                          !lifted(edge.target.nodeId)
                        );
                      })
                      .map((edge) => {
                        const from = layout.positions[edge.source.nodeId];
                        const to = layout.positions[edge.target.nodeId];
                        if (!from || !to) {
                          return null;
                        }
                        return (
                          <path
                            key={edge.id}
                            className={`wire${props.invalidEdges.has(edge.id) ? " wire-invalid" : ""}${wireTraceClass(`${edge.source.nodeId}:${edge.source.portKey}`)}`}
                            data-edge-id={edge.id}
                            d={curve(
                              RAIL_WIDTH +
                                nodeX(edge.source.nodeId) +
                                nodeWidth(edge.source.nodeId === expanded),
                              portY(
                                edge.source.nodeId,
                                edge.source.portKey,
                                "output",
                              ),
                              RAIL_WIDTH + nodeX(edge.target.nodeId),
                              portY(
                                edge.target.nodeId,
                                edge.target.portKey,
                                "input",
                              ),
                            )}
                          />
                        );
                      })}
                  {outputs.map((entry) => {
                    const from = layout.positions[entry.nodeId];
                    const id = `${entry.nodeId}:${entry.portKey}`;
                    if (!from || lifted(entry.nodeId)) {
                      return null;
                    }
                    return (
                      <path
                        key={id}
                        className={`wire wire-rail${invalidOutputs.has(id) ? " wire-invalid" : ""}${wireTraceClass(id)}`}
                        data-value={id}
                        d={curve(
                          RAIL_WIDTH +
                            nodeX(entry.nodeId) +
                            nodeWidth(entry.nodeId === expanded),
                          portY(entry.nodeId, entry.portKey, "output"),
                          width - RAIL_WIDTH,
                          (outputY.get(id) ?? REGION_HEADER) + ENTRY_HALF,
                        )}
                      />
                    );
                  })}
                  {inputs.map((entry) => {
                    const to = layout.positions[entry.nodeId];
                    const sourceKey = `${entry.source.nodeId}:${entry.source.portKey}`;
                    if (!to || lifted(entry.nodeId)) {
                      return null;
                    }
                    return (
                      <path
                        key={entry.edgeId}
                        className={`wire wire-rail${props.invalidEdges.has(entry.edgeId) ? " wire-invalid" : ""}${wireTraceClass(sourceKey)}`}
                        data-edge-id={entry.edgeId}
                        d={curve(
                          RAIL_WIDTH,
                          (inputY.get(entry.edgeId) ?? REGION_HEADER) +
                            ENTRY_HALF,
                          RAIL_WIDTH + nodeX(entry.nodeId),
                          portY(entry.nodeId, entry.portKey, "input"),
                        )}
                      />
                    );
                  })}
                </svg>
                {region === "DATA" &&
                  (!document || document.nodes.length === 0) && (
                    <p className="empty-hint">
                      {document
                        ? "Use + Add in each region to add its nodes."
                        : "Open a saved workflow, or start one with New."}
                    </p>
                  )}
                {document &&
                  nodes.map((node) => {
                    const position = layout.positions[node.id];
                    if (!position) {
                      return null;
                    }
                    return (
                      <NodeView
                        key={node.id}
                        node={node}
                        contract={contracts.get(node.type)}
                        name={names.get(node.id) ?? node.id}
                        region={region}
                        expanded={node.id === expanded}
                        focusMode={false}
                        moving={node.id === props.moving}
                        diagnostics={props.diagnosticsByNode.get(node.id) ?? []}
                        status={props.nodeStatuses?.get(node.id) ?? "not-run"}
                        runtimeDiagnostics={
                          props.runtimeDiagnosticsByNode?.get(node.id) ?? []
                        }
                        recordedResult={
                          resultSummaryLabel(node.type)
                            ? (props.recordedResult ?? null)
                            : null
                        }
                        traceState={
                          tracedValue === null
                            ? null
                            : tracedNodes.has(node.id)
                              ? "highlighted"
                              : "dimmed"
                        }
                        style={{
                          left: RAIL_WIDTH + nodeX(node.id),
                          top:
                            REGION_HEADER +
                            position.y +
                            (offsets[node.id] ?? 0),
                          visibility:
                            props.focusMode === node.id ? "hidden" : undefined,
                        }}
                        registerElement={props.registerNode(node.id)}
                        ports={{
                          state: (direction, key) =>
                            portState(node.id, direction, key),
                          problem: (direction, key) =>
                            direction === "input" &&
                            props.problemPorts.has(`${node.id}:${key}`),
                          onActivate: (direction, key) =>
                            props.onPortActivate(node.id, direction, key),
                          onPointerDown: (direction, key, event) =>
                            props.onPortPointerDown(
                              node.id,
                              direction,
                              key,
                              event,
                            ),
                        }}
                        connections={connectionsOf(node)}
                        onDisconnect={props.onDisconnect}
                        onRemove={() => props.onRemoveNode(node.id)}
                        onParameterChange={(key, value) =>
                          props.onParameterChange(node.id, key, value)
                        }
                        onToggleExpanded={() => props.onToggleExpanded(node.id)}
                        onToggleFocusMode={() =>
                          props.onToggleFocusMode(node.id)
                        }
                        onKeyDown={(event) =>
                          props.onNodeKeyDown(node.id, event)
                        }
                        onBlur={(event) => props.onNodeBlur(node.id, event)}
                        onHeaderPointerDown={(event) =>
                          props.onHeaderPointerDown(node.id, event)
                        }
                      />
                    );
                  })}
                {/* After the nodes, so Tab reads Inputs, nodes, Outputs. */}
                <div
                  className="rail rail-outputs"
                  aria-label={`${label} outputs`}
                  role="list"
                >
                  <span className="rail-title" aria-hidden="true">
                    Outputs
                  </span>
                  {outputs.map((entry) => {
                    const id = `${entry.nodeId}:${entry.portKey}`;
                    const top = outputY.get(id) ?? REGION_HEADER;
                    const count = new Set(entry.consumers.map((c) => c.nodeId))
                      .size;
                    const isLit = tracedValue !== null && id === tracedValue;
                    const isDim = tracedValue !== null && !isLit;
                    const traceClass = isLit
                      ? " rail-entry-lit"
                      : isDim
                        ? " rail-entry-dim"
                        : "";
                    return (
                      <div
                        role="listitem"
                        key={id}
                        ref={measureRail(id)}
                        style={{ top: top - REGION_HEADER }}
                        className="rail-slot"
                      >
                        <button
                          type="button"
                          className={`rail-entry type-${typeOf(entry.nodeId, entry.portKey, "output")}${invalidOutputs.has(id) ? " rail-entry-invalid" : ""}${traceClass}`}
                          data-rail="output"
                          data-value={id}
                          data-trace-state={
                            isLit ? "highlighted" : isDim ? "dimmed" : undefined
                          }
                          aria-pressed={isLit}
                          onClick={() =>
                            props.onToggleTrace?.({
                              nodeId: entry.nodeId,
                              portKey: entry.portKey,
                            })
                          }
                          onKeyDown={(event) => {
                            if (event.key === "Enter" || event.key === " ") {
                              event.preventDefault();
                              props.onToggleTrace?.({
                                nodeId: entry.nodeId,
                                portKey: entry.portKey,
                              });
                            }
                          }}
                          onMouseEnter={() =>
                            setCard({ id, lines: cardFor(entry) })
                          }
                          onMouseLeave={() => setCard(null)}
                          onFocus={() => setCard({ id, lines: cardFor(entry) })}
                          onBlur={() => setCard(null)}
                        >
                          <span className="rail-name">
                            {valueName(entry.nodeId, entry.portKey)}
                          </span>
                          <span className="rail-sub">
                            used by {count} {count === 1 ? "node" : "nodes"}
                          </span>
                        </button>
                        {card?.id === id && (
                          <div
                            className="hover-card hover-card-left"
                            role="tooltip"
                          >
                            {card.lines.map((line) => (
                              <p key={line}>{line}</p>
                            ))}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </section>
              {!isLast && (
                <div className="gutter" data-gutter-for={region}>
                  <button
                    type="button"
                    className="gutter-button"
                    aria-label={`Narrow ${label}`}
                    onClick={() =>
                      props.onResize(region, width - GUTTER_STEP_LARGE)
                    }
                  >
                    −
                  </button>
                  <div
                    className="gutter-grip"
                    role="separator"
                    tabIndex={0}
                    aria-orientation="vertical"
                    aria-label={`Resize ${label}`}
                    aria-valuenow={width}
                    aria-valuemin={minimum}
                    aria-valuemax={MAX_REGION_WIDTH}
                    onPointerDown={(event) =>
                      props.onGutterPointerDown(region, event)
                    }
                    onKeyDown={(event) => {
                      const step = event.shiftKey
                        ? GUTTER_STEP_LARGE
                        : GUTTER_STEP;
                      if (event.key === "ArrowLeft") {
                        event.preventDefault();
                        props.onResize(region, width - step);
                      } else if (event.key === "ArrowRight") {
                        event.preventDefault();
                        props.onResize(region, width + step);
                      } else if (event.key === "Home") {
                        event.preventDefault();
                        props.onResize(region, minimum);
                      } else if (event.key === "End") {
                        event.preventDefault();
                        props.onResize(region, MAX_REGION_WIDTH);
                      }
                    }}
                  />
                  <button
                    type="button"
                    className="gutter-button"
                    aria-label={`Widen ${label}`}
                    onClick={() =>
                      props.onResize(region, width + GUTTER_STEP_LARGE)
                    }
                  >
                    +
                  </button>
                </div>
              )}
            </Fragment>
          );
        })}
        {props.tracing && document && (
          <svg
            className="trace-wires"
            width={totalWidth}
            height={height}
            aria-hidden="true"
            focusable="false"
          >
            {traceEdges(document, props.tracing)
              .filter(
                (edge) =>
                  !lifted(edge.source.nodeId) && !lifted(edge.target.nodeId),
              )
              .map((edge) => {
                const sourceNode = nodeById(document, edge.source.nodeId);
                const targetNode = nodeById(document, edge.target.nodeId);
                if (!sourceNode || !targetNode) {
                  return null;
                }
                const sourceLeft = regionLeft.get(regionOf(sourceNode)) ?? 0;
                const targetLeft = regionLeft.get(regionOf(targetNode)) ?? 0;
                return (
                  <path
                    key={edge.id}
                    className="wire wire-trace"
                    data-trace-edge-id={edge.id}
                    d={curve(
                      sourceLeft +
                        RAIL_WIDTH +
                        nodeX(edge.source.nodeId) +
                        nodeWidth(edge.source.nodeId === expanded),
                      portY(edge.source.nodeId, edge.source.portKey, "output"),
                      targetLeft + RAIL_WIDTH + nodeX(edge.target.nodeId),
                      portY(edge.target.nodeId, edge.target.portKey, "input"),
                    )}
                  />
                );
              })}
          </svg>
        )}
      </div>
      <div className="results-band" aria-hidden="true" />
    </div>
  );
}
