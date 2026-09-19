import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["apps/web/src/**/*.test.{ts,tsx}", "scripts/**/*.test.mjs"],
    setupFiles: ["apps/web/src/test/setup.ts"],
    coverage: {
      provider: "v8",
      include: ["apps/web/src/**/*.{ts,tsx}"],
      exclude: ["apps/web/src/**/*.test.{ts,tsx}", "apps/web/src/test/**"],
      reporter: ["text", "html", "lcov"],
    },
  },
});
