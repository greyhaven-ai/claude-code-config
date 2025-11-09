# Testing Setup Reference

Complete configuration guide for Vitest, React Testing Library, and MSW in TanStack projects.

## Vitest Configuration

### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Key Options

| Option | Purpose | Value |
|--------|---------|-------|
| `globals` | Enable global test APIs (describe, it, expect) | `true` |
| `environment` | Test environment (jsdom for DOM testing) | `'jsdom'` |
| `setupFiles` | Files to run before each test file | `['./src/test/setup.ts']` |
| `coverage.provider` | Coverage provider | `'v8'` (faster) |
| `coverage.thresholds` | Minimum coverage percentages | 80% recommended |

## Test Setup File

### src/test/setup.ts

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, beforeAll, afterAll, vi } from 'vitest';
import { server } from './msw/server';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// MSW setup
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Mock window.matchMedia (for responsive components)
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver (for infinite scroll)
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock ResizeObserver (for table columns)
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Suppress console errors in tests (optional)
const originalError = console.error;
beforeAll(() => {
  console.error = (...args: any[]) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});
```

## MSW Setup

### src/test/msw/server.ts

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### src/test/msw/handlers.ts

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  // Users API
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);
  }),

  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Alice',
      email: 'alice@example.com',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: '3', ...body },
      { status: 201 }
    );
  }),

  // Auth API
  http.post('/api/auth/login', async ({ request }) => {
    const { email, password } = await request.json();

    if (email === 'test@example.com' && password === 'password') {
      return HttpResponse.json({
        token: 'mock-jwt-token',
        user: { id: '1', email, name: 'Test User' },
      });
    }

    return HttpResponse.json(
      { error: 'Invalid credentials' },
      { status: 401 }
    );
  }),
];
```

### Overriding Handlers in Tests

```typescript
import { server } from '../test/msw/server';
import { http, HttpResponse } from 'msw';

it('handles API error', async () => {
  // Override handler for this test
  server.use(
    http.get('/api/users', () => {
      return new HttpResponse(null, { status: 500 });
    })
  );

  // Test error handling...
});
```

## TanStack Query Setup

### src/test/query-client.ts

```typescript
import { QueryClient } from '@tanstack/react-query';

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,        // Don't retry failed queries in tests
        gcTime: 0,          // No garbage collection
        staleTime: 0,       // Always consider data stale
      },
      mutations: {
        retry: false,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {},      // Silence error logs in tests
    },
  });
}
```

## TanStack Router Setup

### src/test/router-utils.tsx

```typescript
import { createMemoryHistory, createRouter } from '@tanstack/react-router';
import { routeTree } from '../routeTree.gen';

export function createTestRouter(initialEntries = ['/']) {
  const history = createMemoryHistory({ initialEntries });

  return createRouter({
    routeTree,
    history,
    context: {
      // Mock auth context
      auth: {
        isAuthenticated: true,
        user: { id: '1', name: 'Test User' },
      },
    },
  });
}
```

## Custom Test Utilities

### src/test/test-utils.tsx

```typescript
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider } from '@tanstack/react-router';
import { createTestQueryClient } from './query-client';
import { createTestRouter } from './router-utils';

interface WrapperProps {
  children: React.ReactNode;
}

export function AllTheProviders({ children }: WrapperProps) {
  const queryClient = createTestQueryClient();
  const router = createTestRouter();

  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router}>
        {children}
      </RouterProvider>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options });
}

// Re-export everything from React Testing Library
export * from '@testing-library/react';
export { renderWithProviders as render };
```

## Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:run": "vitest run"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "@vitest/coverage-v8": "^1.0.4",
    "@vitest/ui": "^1.0.4",
    "jsdom": "^23.0.1",
    "msw": "^2.0.11",
    "vitest": "^1.0.4"
  }
}
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  }
}
```

## Coverage Configuration

### .gitignore

```
coverage/
.vitest/
```

### Coverage Thresholds

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
        // Per-file thresholds
        perFile: true,
      },
    },
  },
});
```

## Environment Variables

### .env.test

```bash
VITE_API_URL=http://localhost:3000/api
VITE_ENV=test
```

### Loading in Tests

```typescript
// src/test/setup.ts
import { loadEnv } from 'vite';

const env = loadEnv('test', process.cwd(), '');
process.env = { ...process.env, ...env };
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run test:coverage
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

## Troubleshooting

### Common Issues

**Issue**: `ReferenceError: describe is not defined`
**Solution**: Add `globals: true` to vitest config

**Issue**: `Cannot find module '@testing-library/jest-dom/vitest'`
**Solution**: Install `@testing-library/jest-dom` package

**Issue**: MSW not intercepting requests
**Solution**: Ensure `server.listen()` is called in `beforeAll`

**Issue**: Tests fail with "Act" warnings
**Solution**: Wrap async operations with `waitFor` or `findBy`

---

**Next**: [Testing Best Practices](testing-best-practices.md) | **Index**: [Reference Index](INDEX.md)
