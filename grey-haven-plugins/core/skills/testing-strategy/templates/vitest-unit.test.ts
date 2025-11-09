// tests/unit/lib/utils/FEATURE.test.ts
import { describe, it, expect } from "vitest";
import { functionToTest } from "~/lib/utils/FEATURE";

describe("functionToTest", () => {
  it("handles valid input correctly", () => {
    const result = functionToTest("valid input");
    expect(result).toBe("expected output");
  });

  it("handles edge cases", () => {
    expect(functionToTest("")).toBe("");
    expect(functionToTest(null)).toBeNull();
  });

  it("throws error for invalid input", () => {
    expect(() => functionToTest("invalid")).toThrow("Error message");
  });
});
