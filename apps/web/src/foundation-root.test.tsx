import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { FoundationRoot } from "./foundation-root";

describe("FoundationRoot", () => {
  it("intentionally renders no user-visible application content", () => {
    const { container } = render(<FoundationRoot />);

    expect(container.childElementCount).toBe(0);
    expect(container.textContent).toBe("");
  });
});
