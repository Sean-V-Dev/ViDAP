// One workflow node (DESIGN.md Section 5). Every label, hint, bound, default,
// and port comes from the backend contract; every message comes from backend
// validation.

import { useId, useState } from "react";
import type {
  ContractParameter,
  Diagnostic,
  JsonValue,
  NodeContract,
  NodeRunStatus,
  RuntimeDiagnostic,
  SliceMetrics,
  WorkflowNode,
} from "./api";
import {
  effectiveValue,
  formatCompactMetrics,
  formatMetrics,
  formatValue,
} from "./model";
import {
  implementationLine,
  regionShortLabel,
  resultSummaryLabel,
} from "./presentation";

export type NodeStatus = "not-run" | "running" | NodeRunStatus;

export type TraceState = "highlighted" | "dimmed" | null;

export interface RecordedNodeResult {
  metrics: SliceMetrics;
  stale: boolean;
}

export interface NodeViewProps {
  node: WorkflowNode;
  contract: NodeContract | undefined;
  name: string;
  region: string;
  expanded: boolean;
  focusMode: boolean;
  moving: boolean;
  diagnostics: Diagnostic[];
  status?: NodeStatus;
  runtimeDiagnostics?: RuntimeDiagnostic[];
  recordedResult?: RecordedNodeResult | null;
  traceState?: TraceState;
  style?: React.CSSProperties;
  registerElement?: (element: HTMLDivElement | null) => void;
  onParameterChange: (key: string, value: JsonValue) => void;
  onToggleExpanded: () => void;
  onToggleFocusMode: () => void;
  onKeyDown: (event: React.KeyboardEvent<HTMLDivElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLDivElement>) => void;
  onHeaderPointerDown?: (event: React.PointerEvent<HTMLDivElement>) => void;
  /** Port controls for connecting (P3-EP04B); static glyphs when absent. */
  ports?: PortInteraction;
  /** The expanded node's Connections section (inputs and their sources). */
  connections?: InputConnections[];
  onDisconnect?: (edgeId: string) => void;
  onRemove?: () => void;
}

export type PortState = "source" | "compatible" | "incompatible" | null;

export interface PortInteraction {
  state: (direction: "input" | "output", key: string) => PortState;
  problem: (direction: "input" | "output", key: string) => boolean;
  onActivate: (direction: "input" | "output", key: string) => void;
  onPointerDown: (
    direction: "input" | "output",
    key: string,
    event: React.PointerEvent<HTMLButtonElement>,
  ) => void;
}

export interface InputConnections {
  portKey: string;
  label: string;
  sources: { edgeId: string; text: string }[];
}

const PORT_STATE_TEXT: Record<Exclude<PortState, null>, string> = {
  source: ", connecting from here",
  compatible: ", can connect",
  incompatible: ", cannot connect",
};

const STATUS_CHIP: Record<
  NodeStatus,
  { icon: string; label: string; className: string; title?: string }
> = {
  "not-run": {
    icon: "–",
    label: "Not run",
    className: "chip chip-not-run",
  },
  running: {
    icon: "◌",
    label: "Running",
    className: "chip chip-running",
  },
  completed: {
    icon: "✓",
    label: "Completed",
    className: "chip chip-completed",
  },
  failed: {
    icon: "✕",
    label: "Failed",
    className: "chip chip-failed",
  },
  blocked: {
    icon: "⊘",
    label: "Blocked",
    className: "chip chip-blocked",
    title: "Not run: depends on a failed node.",
  },
  unrelated: {
    icon: "○",
    label: "Unrelated",
    className: "chip chip-unrelated",
    title: "Not started: does not depend on the failed node.",
  },
};

// Double-click toggles the node from anywhere on it except its controls and
// its settings body, where a double-click selects text in a field.
const NO_DOUBLE_CLICK =
  "button, input, select, textarea, label, summary, .node-body";

function summaryLine(
  node: WorkflowNode,
  contract: NodeContract | undefined,
  recordedResult?: RecordedNodeResult | null,
) {
  const result = resultSummaryLabel(node.type);
  if (result) {
    if (!recordedResult) {
      return `${result} —`;
    }
    const prefix = recordedResult.stale ? "Last run · " : "";
    return `${prefix}${result} ${formatCompactMetrics(recordedResult.metrics)}`;
  }
  if (!contract || contract.parameters.length === 0) {
    return contract?.description ?? "";
  }
  return contract.parameters
    .map(
      (parameter) =>
        `${parameter.label} ${formatValue(effectiveValue(node, parameter))}`,
    )
    .join(" · ");
}

function numericAttribute(value: JsonValue | undefined): number | undefined {
  return typeof value === "number" ? value : undefined;
}

function ParameterField({
  node,
  parameter,
  onChange,
}: {
  node: WorkflowNode;
  parameter: ContractParameter;
  onChange: (value: JsonValue) => void;
}) {
  const id = useId();
  const hintId = `${id}-hint`;
  const value = effectiveValue(node, parameter);
  const text =
    typeof value === "number" || typeof value === "string" ? String(value) : "";
  const [draft, setDraft] = useState(text);
  const [unparsed, setUnparsed] = useState(false);
  // The document is the one source (DESIGN.md Principle 4). When its value
  // changes elsewhere (another copy of this node, a reload), show it here,
  // unless this field's own text already means that value (e.g. "0." for 0).
  const [shown, setShown] = useState(value);
  if (!Object.is(shown, value)) {
    setShown(value);
    if (draft.trim() === "" || Number(draft) !== value) {
      setDraft(text);
      setUnparsed(false);
    }
  }
  const allowed = parameter.constraints.allowedValues;
  const hint = parameter.description ? (
    <p className="field-hint" id={hintId}>
      {parameter.description}
    </p>
  ) : null;

  if (Array.isArray(allowed)) {
    return (
      <div className="field">
        <label htmlFor={id}>{parameter.label}</label>
        <select
          id={id}
          aria-describedby={parameter.description ? hintId : undefined}
          value={JSON.stringify(value ?? null)}
          onChange={(event) =>
            onChange(JSON.parse(event.target.value) as JsonValue)
          }
        >
          {allowed.map((option) => (
            <option key={JSON.stringify(option)} value={JSON.stringify(option)}>
              {formatValue(option)}
            </option>
          ))}
        </select>
        {hint}
      </div>
    );
  }
  if (parameter.kind === "boolean") {
    return (
      <div className="field field-check">
        <input
          id={id}
          type="checkbox"
          aria-describedby={parameter.description ? hintId : undefined}
          checked={value === true}
          onChange={(event) => onChange(event.target.checked)}
        />
        <label htmlFor={id}>{parameter.label}</label>
        {hint}
      </div>
    );
  }
  if (parameter.kind === "integer" || parameter.kind === "number") {
    return (
      <div className="field">
        <label htmlFor={id}>{parameter.label}</label>
        <input
          id={id}
          type="number"
          inputMode="decimal"
          aria-describedby={parameter.description ? hintId : undefined}
          min={numericAttribute(parameter.constraints.minimum)}
          max={numericAttribute(parameter.constraints.maximum)}
          step={parameter.kind === "integer" ? 1 : "any"}
          value={draft}
          onChange={(event) => {
            const text = event.target.value;
            setDraft(text);
            const parsed = Number(text);
            const ok = text.trim() !== "" && Number.isFinite(parsed);
            setUnparsed(!ok);
            if (ok) {
              setShown(parsed);
              onChange(parsed);
            }
          }}
        />
        {unparsed && (
          <p className="field-note" role="note">
            Enter a number to update this setting.
          </p>
        )}
        {hint}
      </div>
    );
  }
  if (parameter.kind === "string") {
    return (
      <div className="field">
        <label htmlFor={id}>{parameter.label}</label>
        <input
          id={id}
          type="text"
          aria-describedby={parameter.description ? hintId : undefined}
          value={typeof value === "string" ? value : ""}
          onChange={(event) => onChange(event.target.value)}
        />
        {hint}
      </div>
    );
  }
  return (
    <div className="field">
      <span className="field-label">{parameter.label}</span>
      <span className="field-fixed">{formatValue(value)} (fixed)</span>
      {hint}
    </div>
  );
}

function Ports({
  contract,
  direction,
  nodeId,
  interaction,
}: {
  contract: NodeContract | undefined;
  direction: "input" | "output";
  nodeId: string;
  interaction: PortInteraction | undefined;
}) {
  const ports =
    (direction === "input" ? contract?.inputs : contract?.outputs) ?? [];
  return (
    <div className={`ports ports-${direction}`}>
      {ports.map((port) => {
        const name = `${direction === "input" ? "Input" : "Output"} port ${port.key}, type ${port.nominalType}`;
        const title = `${port.label} (${port.nominalType})`;
        const dot = (
          <span
            className={`port-dot port-${port.nominalType}`}
            aria-hidden="true"
          />
        );
        if (!interaction) {
          return (
            <span
              key={port.key}
              className="port"
              role="img"
              aria-label={name}
              title={title}
            >
              {dot}
            </span>
          );
        }
        const state = interaction.state(direction, port.key);
        const problem = interaction.problem(direction, port.key);
        const classes = [
          "port",
          state ? `port-${state}` : "",
          problem ? "port-problem" : "",
        ]
          .filter(Boolean)
          .join(" ");
        return (
          <button
            key={port.key}
            type="button"
            className={classes}
            aria-label={`${name}${state ? PORT_STATE_TEXT[state] : ""}${problem ? ", has a problem" : ""}`}
            title={title}
            data-node-id={nodeId}
            data-port-key={port.key}
            data-port-direction={direction}
            onClick={() => interaction.onActivate(direction, port.key)}
            onPointerDown={(event) =>
              interaction.onPointerDown(direction, port.key, event)
            }
          >
            {dot}
            {state === "incompatible" && (
              <span className="port-cross" aria-hidden="true">
                ✕
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

function Connections({
  name,
  connections,
  onDisconnect,
}: {
  name: string;
  connections: InputConnections[];
  onDisconnect: ((edgeId: string) => void) | undefined;
}) {
  return (
    <section className="node-connections" aria-label={`${name} connections`}>
      <p className="field-label">Connections</p>
      <ul>
        {connections.flatMap((input) =>
          input.sources.length === 0
            ? [<li key={input.portKey}>{input.label}: not connected</li>]
            : input.sources.map((source) => (
                <li key={source.edgeId}>
                  <span>
                    {input.label} ← {source.text}
                  </span>
                  {onDisconnect && (
                    <button
                      type="button"
                      className="button"
                      aria-label={`Disconnect ${source.text} from ${input.label}`}
                      onClick={() => onDisconnect(source.edgeId)}
                    >
                      Disconnect
                    </button>
                  )}
                </li>
              )),
        )}
      </ul>
    </section>
  );
}

export function NodeView({
  node,
  contract,
  name,
  region,
  expanded,
  focusMode,
  moving,
  diagnostics,
  status = "not-run",
  runtimeDiagnostics = [],
  recordedResult = null,
  traceState = null,
  style,
  registerElement,
  onParameterChange,
  onToggleExpanded,
  onToggleFocusMode,
  onKeyDown,
  onBlur,
  onHeaderPointerDown,
  ports,
  connections,
  onDisconnect,
  onRemove,
}: NodeViewProps) {
  const headingId = useId();
  const kicker = regionShortLabel(region);
  const implementation = implementationLine(node.type);
  const resultLabel = resultSummaryLabel(node.type);
  const hasProblems = diagnostics.length > 0;
  const hasRuntimeFailures = runtimeDiagnostics.length > 0;
  const chip = STATUS_CHIP[status];
  const classes = [
    "node",
    expanded || focusMode ? "node-expanded" : "node-compact",
    focusMode ? "node-focus" : "",
    hasProblems ? "node-warn" : "",
    status === "failed" || hasRuntimeFailures ? "node-failed" : "",
    traceState === "highlighted" ? "node-trace-lit" : "",
    traceState === "dimmed" ? "node-trace-dim" : "",
    moving ? "node-moving" : "",
  ]
    .filter(Boolean)
    .join(" ");
  const open = expanded || focusMode;

  return (
    <div
      ref={registerElement}
      className={classes}
      style={style}
      tabIndex={0}
      role="group"
      aria-labelledby={headingId}
      aria-description={`${regionShortLabel(region)} region. Arrow keys move between connected nodes; Enter expands; F opens focus mode; M moves the node.`}
      data-node-id={node.id}
      data-trace-state={traceState ?? undefined}
      onKeyDown={onKeyDown}
      onBlur={onBlur}
      onDoubleClick={(event) => {
        if (
          !(event.target instanceof Element) ||
          !event.target.closest(NO_DOUBLE_CLICK)
        ) {
          onToggleExpanded();
        }
      }}
    >
      <div className="node-header" onPointerDown={onHeaderPointerDown}>
        <span className="node-kicker">{kicker}</span>
        <h3 className="node-title" id={headingId}>
          {name}
        </h3>
        <div className="node-actions">
          <button
            type="button"
            className="icon-button"
            aria-expanded={open}
            aria-label={open ? `Collapse ${name}` : `Expand ${name}`}
            onClick={onToggleExpanded}
            onPointerDown={(event) => event.stopPropagation()}
          >
            {open ? "▾" : "▸"}
          </button>
          <button
            type="button"
            className="icon-button"
            aria-pressed={focusMode}
            aria-label={
              focusMode
                ? `Close focus mode for ${name}`
                : `Open ${name} in focus mode`
            }
            onClick={onToggleFocusMode}
            onPointerDown={(event) => event.stopPropagation()}
          >
            ⤢
          </button>
        </div>
      </div>
      <Ports
        contract={contract}
        direction="input"
        nodeId={node.id}
        interaction={ports}
      />
      <Ports
        contract={contract}
        direction="output"
        nodeId={node.id}
        interaction={ports}
      />
      {implementation && (
        <p className="node-implementation">{implementation}</p>
      )}
      {!open && (
        <p className="node-summary">
          {summaryLine(node, contract, recordedResult)}
        </p>
      )}
      <p className={chip.className} title={chip.title}>
        <span aria-hidden="true">{chip.icon}</span> {chip.label}
      </p>
      {hasRuntimeFailures && (
        <div className="node-message node-message-err">
          <p className="message-label message-label-err">Run failed</p>
          {runtimeDiagnostics.map((item, index) => (
            <div key={`${item.code}-${item.attemptId}-${index}`}>
              <p className="message-headline">{item.explanation}</p>
              <p className="message-remedy">{item.remedy}</p>
              <details className="message-details">
                <summary>Technical details</summary>
                <p>
                  {item.code}
                  {item.operationKey ? ` · ${item.operationKey}` : ""}
                  {item.portKey ? ` · ${item.portKey}` : ""}
                </p>
                <p>Attempt {item.attemptId}</p>
                {item.technical.type && <p>Type {item.technical.type}</p>}
                <p>{item.technical.message}</p>
                {item.technical.traceback.length > 0 && (
                  <p>Traceback {item.technical.traceback.join(" → ")}</p>
                )}
                {item.technical.causes.length > 0 && (
                  <p>Causes {item.technical.causes.join(" → ")}</p>
                )}
              </details>
            </div>
          ))}
        </div>
      )}
      {hasProblems && (
        <div className="node-message node-message-warn">
          <p className="message-label">Fix before running</p>
          {diagnostics.map((item, index) => (
            <div key={`${item.code}-${item.elementReference}-${index}`}>
              <p className="message-headline">{item.message}</p>
              <p className="message-remedy">{item.remedy}</p>
              <details className="message-details">
                <summary>Technical details</summary>
                <p>
                  {item.code}
                  {item.jsonPointer ? ` · ${item.jsonPointer}` : ""}
                </p>
              </details>
            </div>
          ))}
        </div>
      )}
      {open && (
        <div
          className="node-body"
          onWheel={(event) => event.stopPropagation()}
          onPointerDown={(event) => event.stopPropagation()}
        >
          {contract?.description && (
            <p className="node-description">{contract.description}</p>
          )}
          {resultLabel && recordedResult && (
            <p className="node-recorded-result">
              {recordedResult.stale ? "Last run: " : "Recorded result: "}
              {formatMetrics(recordedResult.metrics)}
            </p>
          )}
          {contract && contract.parameters.length > 0 ? (
            contract.parameters.map((parameter) => (
              <ParameterField
                key={parameter.key}
                node={node}
                parameter={parameter}
                onChange={(value) => onParameterChange(parameter.key, value)}
              />
            ))
          ) : (
            <p className="field-hint">This step has no settings.</p>
          )}
          {connections && connections.length > 0 && (
            <Connections
              name={name}
              connections={connections}
              onDisconnect={onDisconnect}
            />
          )}
          <details className="node-advanced">
            <summary>Advanced</summary>
            <p>Type {node.type}</p>
            <p>Node ID {node.id}</p>
            {onRemove && (
              <button
                type="button"
                className="button button-danger"
                onClick={onRemove}
              >
                Remove node
              </button>
            )}
          </details>
        </div>
      )}
    </div>
  );
}
