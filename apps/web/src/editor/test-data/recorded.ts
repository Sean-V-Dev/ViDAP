// Recorded responses captured from the real /api/slice/ backend for the
// editor tests. Regenerate with `node scripts/capture-editor-responses.mjs`
// while `npm.cmd run launch` runs; do not edit by hand.

import type {
  CompareResult,
  Diagnostic,
  LoadedWorkflow,
  NodeContract,
  RunResult,
  SaveResult,
  ValidateResult,
  WorkflowSummary,
} from "../api";

export interface ErrorBody {
  error: { code: string; message: string };
  diagnostics?: Diagnostic[];
  [key: string]: unknown;
}

export interface Recorded {
  contracts: NodeContract[];
  validateValid: ValidateResult;
  validateInvalid: ValidateResult;
  validateEmpty: ValidateResult;
  validateMissingInput: ValidateResult;
  validateTypeMismatch: ValidateResult;
  validateCycle: ValidateResult;
  saveExample: SaveResult;
  saveNoLayout: SaveResult;
  saveEmpty: SaveResult;
  list: WorkflowSummary[];
  loadExample: LoadedWorkflow;
  loadNoLayout: LoadedWorkflow;
  notFound: ErrorBody;
  saveRefused: ErrorBody;
  saveBadName: ErrorBody;
  saveNameTaken: ErrorBody;
  saveConflict: ErrorBody;
  compareChanged: CompareResult;
  compareUnchanged: CompareResult;
  runSuccess: RunResult;
  runRegularized: RunResult;
  runFailed: RunResult;
  runRefused: ErrorBody;
}

export const recorded: Recorded = {
  compareChanged: {
    changed: true,
    missing: false,
    sidecarDigest:
      "sha256:93c94b022f845fcaa97d79e64535241e516b9a3c11c923771d7815186d3e2518",
    summary: {
      edgesAdded: [],
      edgesRemoved: [],
      labelsChanged: [],
      layoutMetadataChanged: false,
      nodesAdded: [],
      nodesRemoved: [],
      parametersChanged: [
        {
          after: 0.5,
          before: 1,
          key: "regularization",
          nodeId: "41000000-0000-4000-8000-000000000004",
        },
      ],
    },
    workflowDigest:
      "sha256:7256643216c3b6210e5e2a2728f2375e728ee62fa36eb33f537acc98c296f6ac",
  },
  compareUnchanged: {
    changed: false,
    missing: false,
    sidecarDigest:
      "sha256:93c94b022f845fcaa97d79e64535241e516b9a3c11c923771d7815186d3e2518",
    summary: null,
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  contracts: [
    {
      description:
        "Loads the controlled synthetic slice dataset by its declared schema.",
      inputs: [],
      label: "Dataset",
      outputs: [
        {
          cardinality: null,
          key: "table",
          label: "Table",
          nominalType: "table",
          required: null,
        },
      ],
      parameters: [],
      type: "vidap.slice.dataset",
    },
    {
      description:
        "Fills missing numbers with a constant and encodes the declared categories as numbers. Learns nothing from the rows.",
      inputs: [
        {
          cardinality: "one",
          key: "table",
          label: "Table",
          nominalType: "table",
          required: true,
        },
      ],
      label: "Prepare Data",
      outputs: [
        {
          cardinality: null,
          key: "prepared",
          label: "Prepared table",
          nominalType: "table",
          required: null,
        },
      ],
      parameters: [
        {
          constraints: {
            maximum: 1000000,
            minimum: -1000000,
          },
          default: 0,
          description: "The number used in place of a missing value.",
          key: "missing_fill",
          kind: "number",
          label: "Missing value fill",
          required: false,
        },
      ],
      type: "vidap.slice.prepare",
    },
    {
      description:
        "Splits rows into training and test parts, keeping the label balance in both.",
      inputs: [
        {
          cardinality: "one",
          key: "table",
          label: "Table",
          nominalType: "table",
          required: true,
        },
      ],
      label: "Train/Test Split",
      outputs: [
        {
          cardinality: null,
          key: "split",
          label: "Split",
          nominalType: "split",
          required: null,
        },
      ],
      parameters: [
        {
          constraints: {
            maximum: 0.5,
            minimum: 0.1,
          },
          default: 0.25,
          description: "The share of rows held out for testing.",
          key: "test_fraction",
          kind: "number",
          label: "Test fraction",
          required: false,
        },
        {
          constraints: {
            maximum: 4294967295,
            minimum: 0,
          },
          default: 0,
          description: "Controls which rows are held out.",
          key: "seed",
          kind: "integer",
          label: "Split seed",
          required: false,
        },
      ],
      type: "vidap.slice.split",
    },
    {
      description:
        "Trains the slice's fixed model implementation, logistic regression, on the training part.",
      inputs: [
        {
          cardinality: "one",
          key: "split",
          label: "Split",
          nominalType: "split",
          required: true,
        },
      ],
      label: "Model",
      outputs: [
        {
          cardinality: null,
          key: "model",
          label: "Trained model",
          nominalType: "model",
          required: null,
        },
      ],
      parameters: [
        {
          constraints: {
            maximum: 10000,
            minimum: 0.0001,
          },
          default: 1,
          description: "Smaller values constrain the model more strongly.",
          key: "regularization",
          kind: "number",
          label: "Regularization",
          required: false,
        },
      ],
      type: "vidap.slice.model",
    },
    {
      description: "Measures the trained model's accuracy on the test part.",
      inputs: [
        {
          cardinality: "one",
          key: "model",
          label: "Trained model",
          nominalType: "model",
          required: true,
        },
        {
          cardinality: "one",
          key: "split",
          label: "Split",
          nominalType: "split",
          required: true,
        },
      ],
      label: "Evaluate",
      outputs: [
        {
          cardinality: null,
          key: "metrics",
          label: "Metrics",
          nominalType: "metrics",
          required: null,
        },
      ],
      parameters: [],
      type: "vidap.slice.evaluate",
    },
  ],
  list: [
    {
      hasSidecar: true,
      name: "capture-example",
      workflowDigest:
        "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
    },
    {
      hasSidecar: false,
      name: "capture-no-layout",
      workflowDigest:
        "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
    },
  ],
  loadExample: {
    name: "capture-example",
    sidecar: {
      format: "vidap.workspace-view",
      nodes: {
        "41000000-0000-4000-8000-000000000001": {
          region: "DATA",
          x: 16,
          y: 16,
        },
        "41000000-0000-4000-8000-000000000002": {
          region: "PREPARE",
          x: 16,
          y: 16,
        },
        "41000000-0000-4000-8000-000000000003": {
          region: "VALIDATE_SPLIT",
          x: 16,
          y: 16,
        },
        "41000000-0000-4000-8000-000000000004": {
          region: "MODEL",
          x: 16,
          y: 16,
        },
        "41000000-0000-4000-8000-000000000005": {
          region: "EVALUATE_COMPARE",
          x: 16,
          y: 16,
        },
      },
      regions: [
        {
          key: "DATA",
          width: 400,
        },
        {
          key: "PREPARE",
          width: 400,
        },
        {
          key: "VALIDATE_SPLIT",
          width: 400,
        },
        {
          key: "MODEL",
          width: 400,
        },
        {
          key: "EVALUATE_COMPARE",
          width: 400,
        },
      ],
      schemaVersion: "1.0",
      viewport: {
        x: 0,
        y: 0,
        zoom: 1,
      },
    },
    sidecarDigest:
      "sha256:93c94b022f845fcaa97d79e64535241e516b9a3c11c923771d7815186d3e2518",
    sidecarNotice: null,
    workflow: {
      edges: [
        {
          id: "42000000-0000-4000-8000-000000000001",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000001",
            portKey: "table",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000002",
            portKey: "table",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000002",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000002",
            portKey: "prepared",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "table",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000003",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "split",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000004",
            portKey: "split",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000004",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000004",
            portKey: "model",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000005",
            portKey: "model",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000005",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "split",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000005",
            portKey: "split",
          },
        },
      ],
      format: "vidap.workflow",
      nodes: [
        {
          id: "41000000-0000-4000-8000-000000000001",
          parameters: {},
          type: "vidap.slice.dataset",
        },
        {
          id: "41000000-0000-4000-8000-000000000002",
          parameters: {
            missing_fill: 0,
          },
          type: "vidap.slice.prepare",
        },
        {
          id: "41000000-0000-4000-8000-000000000003",
          parameters: {
            seed: 0,
            test_fraction: 0.25,
          },
          type: "vidap.slice.split",
        },
        {
          id: "41000000-0000-4000-8000-000000000004",
          parameters: {
            regularization: 1,
          },
          type: "vidap.slice.model",
        },
        {
          id: "41000000-0000-4000-8000-000000000005",
          parameters: {},
          type: "vidap.slice.evaluate",
        },
      ],
      schemaVersion: "1.0",
      workflowId: "40000000-0000-4000-8000-000000000001",
    },
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  loadNoLayout: {
    name: "capture-no-layout",
    sidecar: null,
    sidecarDigest: null,
    sidecarNotice: null,
    workflow: {
      edges: [
        {
          id: "42000000-0000-4000-8000-000000000001",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000001",
            portKey: "table",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000002",
            portKey: "table",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000002",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000002",
            portKey: "prepared",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "table",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000003",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "split",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000004",
            portKey: "split",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000004",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000004",
            portKey: "model",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000005",
            portKey: "model",
          },
        },
        {
          id: "42000000-0000-4000-8000-000000000005",
          source: {
            nodeId: "41000000-0000-4000-8000-000000000003",
            portKey: "split",
          },
          target: {
            nodeId: "41000000-0000-4000-8000-000000000005",
            portKey: "split",
          },
        },
      ],
      format: "vidap.workflow",
      nodes: [
        {
          id: "41000000-0000-4000-8000-000000000001",
          parameters: {},
          type: "vidap.slice.dataset",
        },
        {
          id: "41000000-0000-4000-8000-000000000002",
          parameters: {
            missing_fill: 0,
          },
          type: "vidap.slice.prepare",
        },
        {
          id: "41000000-0000-4000-8000-000000000003",
          parameters: {
            seed: 0,
            test_fraction: 0.25,
          },
          type: "vidap.slice.split",
        },
        {
          id: "41000000-0000-4000-8000-000000000004",
          parameters: {
            regularization: 1,
          },
          type: "vidap.slice.model",
        },
        {
          id: "41000000-0000-4000-8000-000000000005",
          parameters: {},
          type: "vidap.slice.evaluate",
        },
      ],
      schemaVersion: "1.0",
      workflowId: "40000000-0000-4000-8000-000000000001",
    },
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  notFound: {
    error: {
      code: "not-found",
      message: "No saved workflow has that name.",
    },
  },
  runFailed: {
    attemptId: "3dd33bd9-1243-485b-89f9-476918d0900a",
    diagnostics: [
      {
        attemptId: "3dd33bd9-1243-485b-89f9-476918d0900a",
        category: "execution",
        code: "unencoded-category-input",
        explanation:
          "The model received a category column that has not been converted to numbers.",
        nodeId: "41000000-0000-4000-8000-000000000004",
        operationKey: "vidap.slice.model",
        outcome: "failed",
        portKey: null,
        remedy: "Route the data through Prepare Data before the model.",
        technical: {
          causes: [],
          message:
            "Exception text withheld because it may contain sensitive values.",
          traceback: ["dispatch", "model", "_matrix"],
          type: "DeclaredFailure",
        },
      },
    ],
    metrics: null,
    nodes: [
      {
        nodeId: "41000000-0000-4000-8000-000000000001",
        operationKey: "vidap.slice.dataset",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000003",
        operationKey: "vidap.slice.split",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000004",
        operationKey: "vidap.slice.model",
        status: "failed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000005",
        operationKey: "vidap.slice.evaluate",
        status: "blocked",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000006",
        operationKey: "vidap.slice.prepare",
        status: "unrelated",
      },
    ],
    outcome: "failed",
    semanticDigest:
      "529d3eb5cb51477b4ecd4f9097cbbc35a46f8b64228a6aa6015e68c9a8a61e0e",
  },
  runRefused: {
    error: {
      code: "run-refused",
      message: "This workflow cannot be run as the slice.",
    },
  },
  runRegularized: {
    attemptId: "9be9b899-f39f-4f14-8dd0-c00283be287e",
    diagnostics: [],
    metrics: {
      accuracy: 0.55,
      correct: 22,
      format: "vidap.slice-metrics",
      schemaVersion: "1.0",
      testRows: 40,
    },
    nodes: [
      {
        nodeId: "41000000-0000-4000-8000-000000000001",
        operationKey: "vidap.slice.dataset",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000002",
        operationKey: "vidap.slice.prepare",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000003",
        operationKey: "vidap.slice.split",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000004",
        operationKey: "vidap.slice.model",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000005",
        operationKey: "vidap.slice.evaluate",
        status: "completed",
      },
    ],
    outcome: "succeeded",
    semanticDigest:
      "58f64131e443d6eb6dbe62860b617f3b2c2be0452b943ee9bafc401bff8c6c96",
  },
  runSuccess: {
    attemptId: "4ba2bd33-c474-481a-978c-0beb2d438235",
    diagnostics: [],
    metrics: {
      accuracy: 0.9,
      correct: 36,
      format: "vidap.slice-metrics",
      schemaVersion: "1.0",
      testRows: 40,
    },
    nodes: [
      {
        nodeId: "41000000-0000-4000-8000-000000000001",
        operationKey: "vidap.slice.dataset",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000002",
        operationKey: "vidap.slice.prepare",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000003",
        operationKey: "vidap.slice.split",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000004",
        operationKey: "vidap.slice.model",
        status: "completed",
      },
      {
        nodeId: "41000000-0000-4000-8000-000000000005",
        operationKey: "vidap.slice.evaluate",
        status: "completed",
      },
    ],
    outcome: "succeeded",
    semanticDigest:
      "b82b86b8ebf59e2099767f6d799e4c1fe15b73a5912a9aa5a6f3f925f34c41f3",
  },
  saveBadName: {
    error: {
      code: "invalid-name",
      message: "The workflow name is not allowed.",
    },
  },
  saveConflict: {
    error: {
      code: "conflict",
      message: "The saved files changed since they were loaded.",
    },
    missing: false,
    sidecarDigest:
      "sha256:93c94b022f845fcaa97d79e64535241e516b9a3c11c923771d7815186d3e2518",
    summary: {
      edgesAdded: [],
      edgesRemoved: [],
      labelsChanged: [],
      layoutMetadataChanged: false,
      nodesAdded: [],
      nodesRemoved: [],
      parametersChanged: [
        {
          after: 0.5,
          before: 1,
          key: "regularization",
          nodeId: "41000000-0000-4000-8000-000000000004",
        },
      ],
    },
    workflowDigest:
      "sha256:7256643216c3b6210e5e2a2728f2375e728ee62fa36eb33f537acc98c296f6ac",
  },
  saveEmpty: {
    name: "capture-empty",
    sidecarDigest: null,
    workflowDigest:
      "sha256:fcd4c0a0d11162200a78ccec954335d4d15a7504938dc670940f98d241d8339b",
  },
  saveExample: {
    name: "capture-example",
    sidecarDigest:
      "sha256:93c94b022f845fcaa97d79e64535241e516b9a3c11c923771d7815186d3e2518",
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  saveNameTaken: {
    error: {
      code: "conflict",
      message: "The saved files changed since they were loaded.",
    },
    missing: false,
    sidecarDigest: null,
    summary: {
      edgesAdded: [],
      edgesRemoved: [],
      labelsChanged: [],
      layoutMetadataChanged: false,
      nodesAdded: [],
      nodesRemoved: [],
      parametersChanged: [],
    },
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  saveNoLayout: {
    name: "capture-no-layout",
    sidecarDigest: null,
    workflowDigest:
      "sha256:db55a1637c426c7e5493a87a3891dad7d97fc90009ee217b79087f4a4492f0cb",
  },
  saveRefused: {
    diagnostics: [
      {
        category: "semantic",
        code: "VIDAP-MISSING-REQUIRED-INPUT",
        elementKind: "port",
        elementReference: "41000000-0000-4000-8000-000000000004:split",
        jsonPointer: null,
        message: "Required input 'split' is not connected.",
        remedy: "Add one compatible incoming edge.",
        severity: "error",
      },
    ],
    error: {
      code: "invalid-workflow",
      message: "The workflow is not valid.",
    },
  },
  validateCycle: {
    diagnostics: [
      {
        category: "semantic",
        code: "VIDAP-DIRECTED-CYCLE",
        elementKind: "workflow",
        elementReference: "40000000-0000-4000-8000-000000000003",
        jsonPointer: null,
        message: "Workflow connections contain a directed cycle.",
        remedy: "Remove an edge so the workflow is acyclic.",
        severity: "error",
      },
    ],
    valid: false,
  },
  validateEmpty: {
    diagnostics: [],
    valid: true,
  },
  validateInvalid: {
    diagnostics: [
      {
        category: "semantic",
        code: "VIDAP-PARAMETER-CONSTRAINT-VIOLATION",
        elementKind: "parameter",
        elementReference: "41000000-0000-4000-8000-000000000004:regularization",
        jsonPointer: null,
        message: "Parameter 'regularization' is below the minimum.",
        remedy: "Use a value within the declared numeric range.",
        severity: "error",
      },
    ],
    valid: false,
  },
  validateMissingInput: {
    diagnostics: [
      {
        category: "semantic",
        code: "VIDAP-MISSING-REQUIRED-INPUT",
        elementKind: "port",
        elementReference: "41000000-0000-4000-8000-000000000004:split",
        jsonPointer: null,
        message: "Required input 'split' is not connected.",
        remedy: "Add one compatible incoming edge.",
        severity: "error",
      },
    ],
    valid: false,
  },
  validateTypeMismatch: {
    diagnostics: [
      {
        category: "semantic",
        code: "VIDAP-MISSING-REQUIRED-INPUT",
        elementKind: "port",
        elementReference: "41000000-0000-4000-8000-000000000005:split",
        jsonPointer: null,
        message: "Required input 'split' is not connected.",
        remedy: "Add one compatible incoming edge.",
        severity: "error",
      },
      {
        category: "semantic",
        code: "VIDAP-NOMINAL-TYPE-MISMATCH",
        elementKind: "edge",
        elementReference: "42000000-0000-4000-8000-000000000005",
        jsonPointer: null,
        message: "Connected ports use different nominal types.",
        remedy: "Connect ports with the same declared type.",
        severity: "error",
      },
    ],
    valid: false,
  },
  validateValid: {
    diagnostics: [],
    valid: true,
  },
};
