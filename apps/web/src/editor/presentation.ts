// UI-owned presentation only (D3.4, DESIGN.md Sections 3 and 5): which region a
// node type sits in, region order and names, and the implementation-line text.
// No parameter, default, range, or validation data lives here; that comes from
// the backend contracts.

export interface RegionDefinition {
  key: string;
  label: string;
}

export const REGIONS: readonly RegionDefinition[] = [
  { key: "DATA", label: "DATA" },
  { key: "PREPARE", label: "PREPARE" },
  { key: "VALIDATE_SPLIT", label: "VALIDATE / SPLIT" },
  { key: "MODEL", label: "MODEL" },
  { key: "EVALUATE_COMPARE", label: "EVALUATE / COMPARE" },
];

export const UNASSIGNED: RegionDefinition = {
  key: "UNASSIGNED",
  label: "UNASSIGNED · type has no region",
};

const TYPE_REGION: Readonly<Record<string, string>> = {
  "vidap.slice.dataset": "DATA",
  "vidap.slice.prepare": "PREPARE",
  "vidap.slice.split": "VALIDATE_SPLIT",
  "vidap.slice.model": "MODEL",
  "vidap.slice.evaluate": "EVALUATE_COMPARE",
};

const IMPLEMENTATION_LINE: Readonly<Record<string, string>> = {
  "vidap.slice.dataset": "Controlled CSV",
  "vidap.slice.prepare": "Fill missing · Encode categories",
  "vidap.slice.split": "Single holdout",
  "vidap.slice.model": "Logistic regression",
  "vidap.slice.evaluate": "Accuracy on test rows",
};

/** Node types whose compact summary is a recorded result (shown after a run). */
const RESULT_SUMMARY: Readonly<Record<string, string>> = {
  "vidap.slice.evaluate": "Accuracy",
};

export function regionKeyForType(type: string): string {
  return TYPE_REGION[type] ?? UNASSIGNED.key;
}

export function implementationLine(type: string): string | null {
  return IMPLEMENTATION_LINE[type] ?? null;
}

export function resultSummaryLabel(type: string): string | null {
  return RESULT_SUMMARY[type] ?? null;
}

export function regionLabel(key: string): string {
  return (
    REGIONS.find((region) => region.key === key)?.label ??
    (key === UNASSIGNED.key ? UNASSIGNED.label : key)
  );
}

/** Short region names used in rail subtitles ("from VALIDATE / SPLIT"). */
export function regionShortLabel(key: string): string {
  return key === UNASSIGNED.key ? "UNASSIGNED" : regionLabel(key);
}
