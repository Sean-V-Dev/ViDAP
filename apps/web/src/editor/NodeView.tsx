// One workflow node (DESIGN.md Section 5). Every label, hint, bound, default,
// and port comes from the backend contract; every message comes from backend
// validation.

import { useId, useState } from "react";
import type {
  ContractParameter,
  Diagnostic,
  JsonValue,
  NodeContract,
  WorkflowNode,
} from "./api";
import { effectiveValue, formatValue } from "./model";
import {
  implementationLine,
  regionShortLabel,
  resultSummaryLabel,
} from "./presentation";

export interface NodeViewProps {
  node: WorkflowNode;
  contract: NodeContract | undefined;
  name: string;
  region: string;
  expanded: boolean;
  focusMode: boolean;
  moving: boolean;
  diagnostics: Diagnostic[];
  style?: React.CSSProperties;
  registerElement?: (element: HTMLDivElement | null) => void;
  onParameterChange: (key: string, value: JsonValue) => void;
  onToggleExpanded: () => void;
  onToggleFocusMode: () => void;
  onKeyDown: (event: React.KeyboardEvent<HTMLDivElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLDivElement>) => void;
  onHeaderPointerDown?: (event: React.PointerEvent<HTMLDivElement>) => void;
}

// Double-click toggles the node from anywhere on it except its controls and
// its settings body, where a double-click selects text in a field.
const NO_DOUBLE_CLICK =
  "button, input, select, textarea, label, summary, .node-body";

function summaryLine(node: WorkflowNode, contract: NodeContract | undefined) {
  const result = resultSummaryLabel(node.type);
  if (result) {
    // Recorded results arrive with run support (P3-EP05); nothing is shown
    // that the backend did not record.
    return `${result} —`;
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
}: {
  contract: NodeContract | undefined;
  direction: "input" | "output";
}) {
  const ports =
    (direction === "input" ? contract?.inputs : contract?.outputs) ?? [];
  return (
    <div className={`ports ports-${direction}`}>
      {ports.map((port) => (
        <span
          key={port.key}
          className={`port port-${port.nominalType}`}
          role="img"
          aria-label={`${direction === "input" ? "Input" : "Output"} port ${port.key}, type ${port.nominalType}`}
          title={`${port.label} (${port.nominalType})`}
        />
      ))}
    </div>
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
  style,
  registerElement,
  onParameterChange,
  onToggleExpanded,
  onToggleFocusMode,
  onKeyDown,
  onBlur,
  onHeaderPointerDown,
}: NodeViewProps) {
  const headingId = useId();
  const kicker = regionShortLabel(region);
  const implementation = implementationLine(node.type);
  const hasProblems = diagnostics.length > 0;
  const classes = [
    "node",
    expanded || focusMode ? "node-expanded" : "node-compact",
    focusMode ? "node-focus" : "",
    hasProblems ? "node-warn" : "",
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
      <Ports contract={contract} direction="input" />
      <Ports contract={contract} direction="output" />
      {implementation && (
        <p className="node-implementation">{implementation}</p>
      )}
      {!open && <p className="node-summary">{summaryLine(node, contract)}</p>}
      <p className="chip chip-not-run">
        <span aria-hidden="true">–</span> Not run
      </p>
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
          <details className="node-advanced">
            <summary>Advanced</summary>
            <p>Type {node.type}</p>
            <p>Node ID {node.id}</p>
          </details>
        </div>
      )}
    </div>
  );
}
