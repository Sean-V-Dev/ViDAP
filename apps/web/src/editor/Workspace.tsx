// Regions, gutters, boundary rails, and wires (DESIGN.md Section 4). Each
// region draws only its own wires inside its own bounds, so nothing can cross
// a gutter: values leave through the Outputs rail and arrive on Inputs rails.

import { Fragment, useState } from "react";
import type { Diagnostic, JsonValue, WorkflowDocument } from "./api";
import type { ContractIndex, InputEntry, OutputEntry } from "./model";
import {
  boundaryEntries,
  consumersOf,
  localEdges,
  nodeById,
  regionOf,
} from "./model";
import {
  GUTTER_STEP,
  GUTTER_STEP_LARGE,
  MAX_REGION_WIDTH,
  RAIL_WIDTH,
  REGION_HEADER,
  minimumWidth,
  nodeWidth,
  portOffset,
  pushDownOffsets,
  regionHeight,
  stackRail,
  type Layout,
} from "./layout";
import { useMeasuredHeights } from "./measure";
import { NodeView } from "./NodeView";
import { UNASSIGNED, regionLabel, regionShortLabel } from "./presentation";

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
  const { document, contracts, names, layout, expanded } = props;
  const [card, setCard] = useState<HoverCard | null>(null);
  const [nodeHeights, measureNode] = useMeasuredHeights();
  const [railHeights, measureRail] = useMeasuredHeights();
  const offsets = document
    ? pushDownOffsets(document, layout.positions, expanded, nodeHeights)
    : {};
  const height = regionHeight(
    document,
    layout.positions,
    expanded,
    nodeHeights,
  );
  // A node lifted into focus mode leaves its slot empty; its wires are hidden
  // while it is lifted (DESIGN.md Section 5).
  const lifted = (nodeId: string) => nodeId === props.focusMode;
  const boundaries = document
    ? boundaryEntries(document)
    : { outputs: [] as OutputEntry[], inputs: [] as InputEntry[] };

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
                          className={`rail-entry type-${typeOf(entry.source.nodeId, entry.source.portKey, "output")}`}
                          data-rail="input"
                          data-edge-id={entry.edgeId}
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
                            from {regionShortLabel(entry.source.region)}
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
                            className="wire"
                            data-edge-id={edge.id}
                            d={curve(
                              RAIL_WIDTH +
                                from.x +
                                nodeWidth(edge.source.nodeId === expanded),
                              portY(
                                edge.source.nodeId,
                                edge.source.portKey,
                                "output",
                              ),
                              RAIL_WIDTH + to.x,
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
                        className="wire wire-rail"
                        data-value={id}
                        d={curve(
                          RAIL_WIDTH +
                            from.x +
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
                    if (!to || lifted(entry.nodeId)) {
                      return null;
                    }
                    return (
                      <path
                        key={entry.edgeId}
                        className="wire wire-rail"
                        data-edge-id={entry.edgeId}
                        d={curve(
                          RAIL_WIDTH,
                          (inputY.get(entry.edgeId) ?? REGION_HEADER) +
                            ENTRY_HALF,
                          RAIL_WIDTH + to.x,
                          portY(entry.nodeId, entry.portKey, "input"),
                        )}
                      />
                    );
                  })}
                </svg>
                {region === "DATA" &&
                  (!document || document.nodes.length === 0) && (
                    <p className="empty-hint">
                      Open a saved workflow to start.
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
                        style={{
                          left: RAIL_WIDTH + position.x,
                          top:
                            REGION_HEADER +
                            position.y +
                            (offsets[node.id] ?? 0),
                          visibility:
                            props.focusMode === node.id ? "hidden" : undefined,
                        }}
                        registerElement={(element) => {
                          props.registerNode(node.id)(element);
                          measureNode(node.id)(element);
                        }}
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
                          className={`rail-entry type-${typeOf(entry.nodeId, entry.portKey, "output")}`}
                          data-rail="output"
                          data-value={id}
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
      </div>
      <div className="results-band" aria-hidden="true" />
    </div>
  );
}
