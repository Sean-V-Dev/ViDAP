import * as matchers from "@testing-library/jest-dom/matchers";
import { cleanup } from "@testing-library/react";
import { afterEach, expect } from "vitest";

expect.extend(matchers);

// Vitest globals are off, so Testing Library cannot register its own cleanup.
afterEach(cleanup);
