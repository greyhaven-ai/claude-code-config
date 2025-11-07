// tests/unit/lib/components/COMPONENT.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import YourComponent from "~/lib/components/YourComponent";

// Mock dependencies
vi.mock("~/lib/server/functions/YOUR_MODULE");

describe("YourComponent", () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  it("renders correctly with initial state", () => {
    render(<YourComponent />, { wrapper });
    expect(screen.getByText("Expected Text")).toBeInTheDocument();
  });

  it("handles user interaction", async () => {
    render(<YourComponent />, { wrapper });

    const button = screen.getByRole("button", { name: /click me/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText("Updated Text")).toBeInTheDocument();
    });
  });

  it("displays loading state", () => {
    render(<YourComponent isLoading={true} />, { wrapper });
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("displays error state", async () => {
    // Mock error
    vi.mocked(someFunction).mockRejectedValue(new Error("Test error"));

    render(<YourComponent />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
