# TanStack Router Testing Examples

Complete examples for testing TanStack Router navigation, routes, and data loading.

## Test Setup

### Router Test Configuration

```typescript
// src/test/router-utils.tsx
import { ReactElement } from 'react';
import { render } from '@testing-library/react';
import { createMemoryHistory, RouterProvider, createRootRoute, createRoute, createRouter } from '@tanstack/react-router';

export function renderWithRouter(
  ui: ReactElement,
  { initialEntries = ['/'] } = {}
) {
  const rootRoute = createRootRoute({
    component: () => ui,
  });

  const router = createRouter({
    routeTree: rootRoute,
    history: createMemoryHistory({ initialEntries }),
  });

  return render(<RouterProvider router={router} />);
}
```

## Example 1: Testing Route Navigation

### Component with Navigation

```typescript
// src/components/Navigation.tsx
import { Link } from '@tanstack/react-router';

export function Navigation() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to="/users">Users</Link>
    </nav>
  );
}
```

### Test Suite

```typescript
// src/components/Navigation.test.tsx
import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { createRootRoute, createRoute, createRouter, RouterProvider } from '@tanstack/react-router';
import { render } from '@testing-library/react';
import { Navigation } from './Navigation';

function Home() {
  return <div>Home Page</div>;
}

function About() {
  return <div>About Page</div>;
}

function Users() {
  return <div>Users Page</div>;
}

describe('Navigation', () => {
  it('navigates between routes', async () => {
    const user = userEvent.setup();

    // Create routes
    const rootRoute = createRootRoute({
      component: () => (
        <>
          <Navigation />
          <div id="content" />
        </>
      ),
    });

    const indexRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/',
      component: Home,
    });

    const aboutRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/about',
      component: About,
    });

    const usersRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/users',
      component: Users,
    });

    const routeTree = rootRoute.addChildren([indexRoute, aboutRoute, usersRoute]);
    const router = createRouter({ routeTree });

    render(<RouterProvider router={router} />);

    // Initially on home
    expect(screen.getByText('Home Page')).toBeInTheDocument();

    // Navigate to About
    await user.click(screen.getByRole('link', { name: /about/i }));
    expect(await screen.findByText('About Page')).toBeInTheDocument();

    // Navigate to Users
    await user.click(screen.getByRole('link', { name: /users/i }));
    expect(await screen.findByText('Users Page')).toBeInTheDocument();
  });
});
```

## Example 2: Testing Route Parameters

### Component Using Route Params

```typescript
// src/pages/UserProfile.tsx
import { useParams } from '@tanstack/react-router';

export function UserProfile() {
  const { userId } = useParams({ from: '/users/$userId' });

  return (
    <div>
      <h1>User Profile</h1>
      <p data-testid="user-id">User ID: {userId}</p>
    </div>
  );
}
```

### Test Suite

```typescript
// src/pages/UserProfile.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import { createRootRoute, createRoute, createRouter, RouterProvider } from '@tanstack/react-router';
import { createMemoryHistory } from '@tanstack/react-router';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('displays correct user ID from route params', () => {
    const rootRoute = createRootRoute();

    const userRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/users/$userId',
      component: UserProfile,
    });

    const routeTree = rootRoute.addChildren([userRoute]);
    const history = createMemoryHistory({ initialEntries: ['/users/123'] });
    const router = createRouter({ routeTree, history });

    render(<RouterProvider router={router} />);

    expect(screen.getByTestId('user-id')).toHaveTextContent('User ID: 123');
  });

  it('updates when route params change', () => {
    const rootRoute = createRootRoute();

    const userRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/users/$userId',
      component: UserProfile,
    });

    const routeTree = rootRoute.addChildren([userRoute]);
    const history = createMemoryHistory({ initialEntries: ['/users/123'] });
    const router = createRouter({ routeTree, history });

    const { rerender } = render(<RouterProvider router={router} />);

    expect(screen.getByTestId('user-id')).toHaveTextContent('User ID: 123');

    // Navigate to different user
    history.push('/users/456');
    rerender(<RouterProvider router={router} />);

    expect(screen.getByTestId('user-id')).toHaveTextContent('User ID: 456');
  });
});
```

## Example 3: Testing Protected Routes

### Protected Route Component

```typescript
// src/components/ProtectedRoute.tsx
import { useAuth } from '../hooks/useAuth';
import { Navigate } from '@tanstack/react-router';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
}
```

### Test Suite

```typescript
// src/components/ProtectedRoute.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { screen, render } from '@testing-library/react';
import { createRootRoute, createRoute, createRouter, RouterProvider } from '@tanstack/react-router';
import { ProtectedRoute } from './ProtectedRoute';
import * as useAuthModule from '../hooks/useAuth';

vi.mock('../hooks/useAuth');

function Dashboard() {
  return <div>Dashboard</div>;
}

function Login() {
  return <div>Login Page</div>;
}

describe('ProtectedRoute', () => {
  it('renders children when authenticated', () => {
    vi.mocked(useAuthModule.useAuth).mockReturnValue({
      isAuthenticated: true,
      user: { id: '1', name: 'Alice' },
      login: vi.fn(),
      logout: vi.fn(),
    });

    const rootRoute = createRootRoute();

    const dashboardRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/dashboard',
      component: () => (
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      ),
    });

    const loginRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/login',
      component: Login,
    });

    const routeTree = rootRoute.addChildren([dashboardRoute, loginRoute]);
    const router = createRouter({ routeTree });

    render(<RouterProvider router={router} />);

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('redirects to login when not authenticated', async () => {
    vi.mocked(useAuthModule.useAuth).mockReturnValue({
      isAuthenticated: false,
      user: null,
      login: vi.fn(),
      logout: vi.fn(),
    });

    const rootRoute = createRootRoute();

    const dashboardRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/dashboard',
      component: () => (
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      ),
    });

    const loginRoute = createRoute({
      getParentRoute: () => rootRoute,
      path: '/login',
      component: Login,
    });

    const routeTree = rootRoute.addChildren([dashboardRoute, loginRoute]);
    const router = createRouter({ routeTree });

    render(<RouterProvider router={router} />);

    // Should redirect and show login
    expect(await screen.findByText('Login Page')).toBeInTheDocument();
    expect(screen.queryByText('Dashboard')).not.toBeInTheDocument();
  });
});
```

## Example 4: Testing Route Loaders

### Route with Loader

```typescript
// src/routes/user.tsx
import { createRoute } from '@tanstack/react-router';

interface User {
  id: string;
  name: string;
  email: string;
}

export const userRoute = createRoute({
  path: '/users/$userId',
  loader: async ({ params }) => {
    const response = await fetch(`/api/users/${params.userId}`);
    if (!response.ok) throw new Error('User not found');
    return response.json() as Promise<User>;
  },
  component: function UserPage({ useLoaderData }) {
    const user = useLoaderData();
    return (
      <div>
        <h1>{user.name}</h1>
        <p>{user.email}</p>
      </div>
    );
  },
});
```

### Test Suite

```typescript
// src/routes/user.test.tsx
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest';
import { screen, render } from '@testing-library/react';
import { createRootRoute, createRouter, RouterProvider } from '@tanstack/react-router';
import { createMemoryHistory } from '@tanstack/react-router';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { userRoute } from './user';

const server = setupServer(
  http.get('/api/users/:userId', ({ params }) => {
    return HttpResponse.json({
      id: params.userId,
      name: 'Alice Johnson',
      email: 'alice@example.com',
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('userRoute', () => {
  it('loads and displays user data', async () => {
    const rootRoute = createRootRoute();
    const routeTree = rootRoute.addChildren([userRoute]);
    const history = createMemoryHistory({ initialEntries: ['/users/123'] });
    const router = createRouter({ routeTree, history });

    render(<RouterProvider router={router} />);

    // Wait for loader to complete
    expect(await screen.findByText('Alice Johnson')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });

  it('handles loader error', async () => {
    server.use(
      http.get('/api/users/:userId', () => {
        return new HttpResponse(null, { status: 404 });
      })
    );

    const rootRoute = createRootRoute();
    const routeTree = rootRoute.addChildren([userRoute]);
    const history = createMemoryHistory({ initialEntries: ['/users/999'] });
    const router = createRouter({ routeTree, history });

    render(<RouterProvider router={router} />);

    // Should show error (TanStack Router handles this automatically)
    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });
});
```

## Key Takeaways

1. **Memory History**: Use `createMemoryHistory` for controlled navigation in tests
2. **Route Setup**: Build complete route trees with `createRouter` for realistic tests
3. **Params Testing**: Pass `initialEntries` to test routes with params
4. **Protected Routes**: Mock authentication context to test access control
5. **Loaders**: Use MSW to mock loader data fetching

---

**Next**: [TanStack Table Testing](tanstack-table-testing.md) | **Previous**: [Query Testing](tanstack-query-testing.md)
