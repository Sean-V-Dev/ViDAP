import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { URL, fileURLToPath } from "node:url";
import { setTimeout as delay } from "node:timers/promises";
import { spawn } from "node:child_process";
import { Buffer } from "node:buffer";

export const FOUNDATION_STATUS = Object.freeze({
  application: "ViDAP",
  scope: "phase-0-foundation",
  status: "ready",
});

export const STARTUP_TIMEOUT_MS = 15_000;
const POLL_INTERVAL_MS = 200;
const DIAGNOSTIC_LINE_LIMIT = 12;
const FIXTURE_LIMIT_BYTES = 1024;
const REPOSITORY_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const FIXTURE_PATH = resolve(
  REPOSITORY_ROOT,
  "fixtures/p0-ep07-foundation-status.json",
);

export function validateMode(mode) {
  if (mode !== "launch" && mode !== "smoke") {
    throw new Error('Harness mode must be "launch" or "smoke".');
  }

  return mode;
}

export function validateLoopbackStatusUrl(value, port) {
  let url;

  try {
    url = new URL(value);
  } catch {
    throw new Error(
      "Readiness target must be an exact loopback HTTP status URL.",
    );
  }

  if (
    url.protocol !== "http:" ||
    url.hostname !== "127.0.0.1" ||
    url.port !== String(port) ||
    url.pathname !== "/api/status" ||
    url.search !== "" ||
    url.hash !== ""
  ) {
    throw new Error(
      "Readiness target must use the prescribed loopback status URL.",
    );
  }

  return url;
}

export function validateFixtureData(fixture, byteSize) {
  if (!Number.isInteger(byteSize) || byteSize > FIXTURE_LIMIT_BYTES) {
    throw new Error("Fixture must be valid UTF-8 JSON at or below 1024 bytes.");
  }

  if (
    fixture === null ||
    typeof fixture !== "object" ||
    Array.isArray(fixture) ||
    fixture.id !== "p0-ep07-foundation-status" ||
    fixture.version !== "1" ||
    fixture.path !== "fixtures/p0-ep07-foundation-status.json" ||
    fixture.byteSize !== byteSize ||
    fixture.provenance !== "synthetic" ||
    fixture.terms !== "MIT" ||
    fixture.creationMethod !== "hand-authored deterministic UTF-8 JSON" ||
    fixture.privacy !==
      "No personal, sensitive, credential, path, network, or telemetry data." ||
    fixture.reviewer !== "Central" ||
    fixture.reviewDate !== "2026-09-19" ||
    JSON.stringify(fixture.expectedStatus) !==
      JSON.stringify(FOUNDATION_STATUS) ||
    !Array.isArray(fixture.permittedConsumers) ||
    fixture.permittedConsumers.length !== 2 ||
    fixture.permittedConsumers[0] !== "P0-EP07 harness" ||
    fixture.permittedConsumers[1] !== "P0-EP07 tests"
  ) {
    throw new Error(
      "Fixture metadata does not match the bounded EP07 status contract.",
    );
  }

  return fixture;
}

export function parseFixtureText(text) {
  const byteSize = Buffer.byteLength(text, "utf8");
  let fixture;

  try {
    fixture = JSON.parse(text);
  } catch {
    throw new Error("Fixture must contain valid UTF-8 JSON.");
  }

  return validateFixtureData(fixture, byteSize);
}

export function boundedDiagnostics(lines) {
  return lines.slice(-DIAGNOSTIC_LINE_LIMIT).map((line) => line.slice(0, 240));
}

export function failureMessage(stage, remedy, lines = []) {
  const diagnosticCount = boundedDiagnostics(lines).length;
  return `P0-EP07 ${stage} failed. ${remedy} Captured ${diagnosticCount} bounded child diagnostic line(s) without writing a log file.`;
}

async function readFixture() {
  return parseFixtureText(await readFile(FIXTURE_PATH, "utf8"));
}

function captureChildOutput(child, name) {
  const lines = [];
  const append = (chunk) => {
    for (const line of String(chunk).split(/\r?\n/u)) {
      if (line) {
        lines.push(`${name}: ${line}`);
      }
    }
  };

  child.stdout?.on("data", append);
  child.stderr?.on("data", append);
  return lines;
}

function startChild(name, command, args) {
  const child = spawn(command, args, {
    cwd: REPOSITORY_ROOT,
    shell: false,
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });
  const record = {
    child,
    name,
    diagnostics: captureChildOutput(child, name),
    closed: false,
    error: null,
  };

  child.once("error", (error) => {
    record.error = error.message;
  });
  child.once("close", () => {
    record.closed = true;
  });
  return record;
}

function childFailure(records) {
  return records.find((record) => record.error !== null || record.closed);
}

async function requestExactStatus(target) {
  const response = await Promise.race([
    globalThis.fetch(target),
    delay(1_000).then(() => {
      throw new Error("A loopback status request exceeded one second.");
    }),
  ]);

  if (!response.ok) {
    throw new Error("The loopback status request did not return HTTP 200.");
  }

  const body = await response.json();
  if (JSON.stringify(body) !== JSON.stringify(FOUNDATION_STATUS)) {
    throw new Error(
      "The loopback status response did not match the static foundation status.",
    );
  }
}

async function waitForStatus(target, records, stage) {
  const deadline = Date.now() + STARTUP_TIMEOUT_MS;

  while (Date.now() < deadline) {
    const failedChild = childFailure(records);
    if (failedChild) {
      throw new Error(
        failureMessage(
          stage,
          "Confirm locked setup succeeds and the prescribed loopback port is available.",
          failedChild.diagnostics,
        ),
      );
    }

    try {
      await requestExactStatus(target);
      return;
    } catch (error) {
      if (
        error.message ===
        "The loopback status response did not match the static foundation status."
      ) {
        throw new Error(
          failureMessage(
            stage,
            "Confirm the local foundation uses the locked static status response.",
            records.flatMap((record) => record.diagnostics),
          ),
        );
      }
      await delay(POLL_INTERVAL_MS);
    }
  }

  throw new Error(
    failureMessage(
      stage,
      "Confirm the prescribed loopback port is unused and rerun npm.cmd run setup.",
      records.flatMap((record) => record.diagnostics),
    ),
  );
}

async function waitForChildExit(record) {
  if (record.closed) {
    return;
  }

  await Promise.race([
    new Promise((resolveExit) => {
      record.child.once("close", resolveExit);
    }),
    delay(5_000).then(() => {
      throw new Error(
        `${record.name} did not exit after process-tree termination.`,
      );
    }),
  ]);
}

async function stopChild(record) {
  if (record.closed || record.child.pid === undefined) {
    return;
  }

  const taskkill = spawn(
    "taskkill",
    ["/pid", String(record.child.pid), "/t", "/f"],
    { shell: false, stdio: "ignore", windowsHide: true },
  );
  await new Promise((resolveTaskkill, rejectTaskkill) => {
    taskkill.once("error", rejectTaskkill);
    taskkill.once("close", resolveTaskkill);
  });
  await waitForChildExit(record);
}

async function stopChildren(records) {
  const activeRecords = [...records].reverse();
  for (const record of activeRecords) {
    await stopChild(record);
  }
}

function startPythonHost() {
  return startChild("Python host", "uv", [
    "--directory",
    "python",
    "run",
    "--locked",
    "uvicorn",
    "vidap_execution.app:create_app",
    "--factory",
    "--host",
    "127.0.0.1",
    "--port",
    "8000",
  ]);
}

function startWebHost() {
  return startChild("Vite host", process.execPath, [
    "node_modules/vite/bin/vite.js",
    "--config",
    "apps/web/vite.config.ts",
    "--host",
    "127.0.0.1",
    "--port",
    "5173",
    "--strictPort",
  ]);
}

async function waitForLaunchExit(records) {
  await Promise.race(
    records.map(
      (record) =>
        new Promise((resolveExit) => {
          record.child.once("close", resolveExit);
        }),
    ),
  );
  throw new Error(
    failureMessage(
      "launch lifecycle",
      "Restart with npm.cmd run launch after resolving the local startup issue.",
      records.flatMap((record) => record.diagnostics),
    ),
  );
}

export async function runHarness(mode) {
  validateMode(mode);
  const fixture = await readFixture();
  const directStatus = validateLoopbackStatusUrl(
    "http://127.0.0.1:8000/api/status",
    8000,
  );
  const proxiedStatus = validateLoopbackStatusUrl(
    "http://127.0.0.1:5173/api/status",
    5173,
  );
  const records = [];
  let signalCleanup = false;

  const onSignal = () => {
    if (!signalCleanup) {
      signalCleanup = true;
      void stopChildren(records).finally(() => {
        process.exitCode = 130;
      });
    }
  };

  process.once("SIGINT", onSignal);
  process.once("SIGTERM", onSignal);

  try {
    records.push(startPythonHost());
    await waitForStatus(directStatus, records, "Python readiness");
    records.push(startWebHost());
    await waitForStatus(proxiedStatus, records, "web proxy readiness");

    if (
      JSON.stringify(fixture.expectedStatus) !==
      JSON.stringify(FOUNDATION_STATUS)
    ) {
      throw new Error(
        "Fixture expected status is inconsistent with the static foundation response.",
      );
    }

    if (mode === "launch") {
      console.log(
        "ViDAP Phase 0 foundation is ready at http://127.0.0.1:5173.",
      );
      console.log(
        "Open that loopback URL manually; press Ctrl+C to stop both local processes.",
      );
      await waitForLaunchExit(records);
    }

    console.log(
      "Smoke verified the direct and proxied loopback foundation status.",
    );
  } finally {
    process.removeListener("SIGINT", onSignal);
    process.removeListener("SIGTERM", onSignal);
    await stopChildren(records);
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runHarness(process.argv[2]).catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
