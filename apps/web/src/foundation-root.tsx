import { useEffect, useState } from "react";

const expectedStatus = {
  application: "ViDAP",
  scope: "phase-0-foundation",
  status: "ready",
};

type FoundationStatus = "checking" | "ready" | "unavailable";

function isExpectedStatus(value: unknown): boolean {
  return JSON.stringify(value) === JSON.stringify(expectedStatus);
}

export function FoundationRoot() {
  const [status, setStatus] = useState<FoundationStatus>("checking");

  useEffect(() => {
    let active = true;

    void fetch("/api/status")
      .then(async (response) => {
        if (!response.ok || !isExpectedStatus(await response.json())) {
          throw new Error("The foundation status response was unavailable.");
        }

        if (active) {
          setStatus("ready");
        }
      })
      .catch(() => {
        if (active) {
          setStatus("unavailable");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <main>
      <h1>ViDAP</h1>
      <p>
        Phase 0 foundation only. Workflow, data, and model capabilities are not
        available.
      </p>
      <section aria-live="polite" aria-label="Local foundation status">
        <h2>Bounded host status</h2>
        {status === "checking" && <p>Checking the local foundation host.</p>}
        {status === "ready" && <p>Local foundation host is ready.</p>}
        {status === "unavailable" && (
          <p>
            Local foundation host is unavailable. Start it with{" "}
            <code>npm.cmd run launch</code>.
          </p>
        )}
      </section>
    </main>
  );
}
