// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    // Enable global test APIs
    globals: true,

    // Use jsdom for browser-like environment
    environment: "jsdom",

    // Run setup file before tests
    setupFiles: ["./tests/setup.ts"],

    // Coverage configuration
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.config.ts",
        "**/*.d.ts",
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },

    // Environment variables
    env: {
      DATABASE_URL_ADMIN: process.env.DATABASE_URL_ADMIN || "postgresql://localhost/test",
      REDIS_URL: process.env.REDIS_URL || "redis://localhost:6379",
    },
  },

  // Path aliases
  resolve: {
    alias: {
      "~": path.resolve(__dirname, "./src"),
    },
  },
});
