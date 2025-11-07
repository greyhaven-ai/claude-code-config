# Server Components Testing

Testing patterns for React 19 Server Components, Suspense, and async rendering.

## Testing Async Server Components

### Basic Async Component

```typescript
// src/components/AsyncUserProfile.tsx
export async function AsyncUserProfile({ userId }: { userId: string }) {
  // Fetch data in Server Component
  const response = await fetch(`/api/users/${userId}`);
  const user = await response.json();

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Test Suite

```typescript
// src/components/AsyncUserProfile.test.tsx
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest';
import { render, screen } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { AsyncUserProfile } from './AsyncUserProfile';

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

describe('AsyncUserProfile', () => {
  it('renders user data after loading', async () => {
    // Render async component
    const component = await AsyncUserProfile({ userId: '123' });
    render(component);

    expect(screen.getByText('Alice Johnson')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
  });
});
```

## Testing with Suspense Boundaries

### Component with Suspense

```typescript
// src/app/users/[userId]/page.tsx
import { Suspense } from 'react';
import { AsyncUserProfile } from '@/components/AsyncUserProfile';

export default function UserProfilePage({ params }: { params: { userId: string } }) {
  return (
    <Suspense fallback={<div>Loading user profile...</div>}>
      <AsyncUserProfile userId={params.userId} />
    </Suspense>
  );
}
```

### Test Suite

```typescript
// src/app/users/[userId]/page.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import UserProfilePage from './page';

describe('UserProfilePage', () => {
  it('shows loading state initially', () => {
    render(<UserProfilePage params={{ userId: '123' }} />);

    expect(screen.getByText('Loading user profile...')).toBeInTheDocument();
  });

  it('renders user profile after loading', async () => {
    render(<UserProfilePage params={{ userId: '123' }} />);

    // Wait for async component to resolve
    expect(await screen.findByText('Alice Johnson')).toBeInTheDocument();
  });
});
```

## Testing Streaming Rendering

### Streaming Component

```typescript
// src/components/StreamingUserList.tsx
export async function StreamingUserList() {
  const response = await fetch('/api/users', {
    // Enable streaming
    next: { revalidate: 60 },
  });
  const users = await response.json();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          <Suspense fallback={<div>Loading {user.name}...</div>}>
            <UserCard userId={user.id} />
          </Suspense>
        </li>
      ))}
    </ul>
  );
}
```

### Test Suite

```typescript
// src/components/StreamingUserList.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StreamingUserList } from './StreamingUserList';

describe('StreamingUserList', () => {
  it('progressively renders user cards', async () => {
    const component = await StreamingUserList();
    render(component);

    // All users should eventually appear
    expect(await screen.findByText('Alice Johnson')).toBeInTheDocument();
    expect(await screen.findByText('Bob Smith')).toBeInTheDocument();
  });

  it('shows loading placeholders while streaming', () => {
    render(<Suspense fallback={<div>Loading list...</div>}><StreamingUserList /></Suspense>);

    expect(screen.getByText('Loading list...')).toBeInTheDocument();
  });
});
```

## Testing Server Actions

### Server Action

```typescript
// src/actions/createUser.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email }),
  });

  if (!response.ok) {
    throw new Error('Failed to create user');
  }

  const user = await response.json();

  // Revalidate users list
  revalidatePath('/users');

  return user;
}
```

### Test Suite

```typescript
// src/actions/createUser.test.ts
import { describe, it, expect, vi } from 'vitest';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { createUser } from './createUser';

// Mock revalidatePath
vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
}));

const server = setupServer(
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: '123', ...body },
      { status: 201 }
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('createUser', () => {
  it('creates user via server action', async () => {
    const formData = new FormData();
    formData.append('name', 'Charlie');
    formData.append('email', 'charlie@example.com');

    const user = await createUser(formData);

    expect(user).toEqual({
      id: '123',
      name: 'Charlie',
      email: 'charlie@example.com',
    });
  });

  it('revalidates path after creation', async () => {
    const { revalidatePath } = await import('next/cache');

    const formData = new FormData();
    formData.append('name', 'Diana');
    formData.append('email', 'diana@example.com');

    await createUser(formData);

    expect(revalidatePath).toHaveBeenCalledWith('/users');
  });
});
```

## Testing Form Actions

### Form with Server Action

```typescript
// src/components/UserForm.tsx
import { createUser } from '@/actions/createUser';

export function UserForm() {
  return (
    <form action={createUser}>
      <label htmlFor="name">Name</label>
      <input id="name" name="name" required />

      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" required />

      <button type="submit">Create User</button>
    </form>
  );
}
```

### Test Suite

```typescript
// src/components/UserForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserForm } from './UserForm';

// Mock the server action
vi.mock('@/actions/createUser', () => ({
  createUser: vi.fn(),
}));

describe('UserForm', () => {
  it('submits form with server action', async () => {
    const { createUser } = await import('@/actions/createUser');
    const user = userEvent.setup();

    render(<UserForm />);

    await user.type(screen.getByLabelText('Name'), 'Alice');
    await user.type(screen.getByLabelText('Email'), 'alice@example.com');
    await user.click(screen.getByRole('button', { name: 'Create User' }));

    expect(createUser).toHaveBeenCalledWith(expect.any(FormData));

    const formData = (createUser as any).mock.calls[0][0] as FormData;
    expect(formData.get('name')).toBe('Alice');
    expect(formData.get('email')).toBe('alice@example.com');
  });
});
```

## Testing Error Boundaries

### Error Boundary Component

```typescript
// src/components/AsyncUserError.tsx
export async function AsyncUserError({ userId }: { userId: string }) {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error(`User ${userId} not found`);
  }

  const user = await response.json();
  return <div>{user.name}</div>;
}

// src/app/users/[userId]/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div role="alert">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Test Suite

```typescript
// src/app/users/[userId]/error.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Error from './error';

describe('Error Boundary', () => {
  it('displays error message', () => {
    const error = new Error('User not found');
    const reset = vi.fn();

    render(<Error error={error} reset={reset} />);

    expect(screen.getByRole('alert')).toHaveTextContent('User not found');
  });

  it('calls reset on try again', async () => {
    const user = userEvent.setup();
    const error = new Error('User not found');
    const reset = vi.fn();

    render(<Error error={error} reset={reset} />);

    await user.click(screen.getByRole('button', { name: 'Try again' }));

    expect(reset).toHaveBeenCalled();
  });
});
```

## Testing Parallel Data Fetching

### Parallel Async Components

```typescript
// src/app/dashboard/page.tsx
import { Suspense } from 'react';

async function UserStats() {
  const response = await fetch('/api/stats/users');
  const stats = await response.json();
  return <div>{stats.count} users</div>;
}

async function PostStats() {
  const response = await fetch('/api/stats/posts');
  const stats = await response.json();
  return <div>{stats.count} posts</div>;
}

export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<div>Loading user stats...</div>}>
        <UserStats />
      </Suspense>
      <Suspense fallback={<div>Loading post stats...</div>}>
        <PostStats />
      </Suspense>
    </div>
  );
}
```

### Test Suite

```typescript
// src/app/dashboard/page.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Dashboard from './page';

describe('Dashboard', () => {
  it('loads components in parallel', async () => {
    render(<Dashboard />);

    // Both should load independently
    expect(await screen.findByText('150 users')).toBeInTheDocument();
    expect(await screen.findByText('300 posts')).toBeInTheDocument();
  });

  it('shows individual loading states', () => {
    render(<Dashboard />);

    expect(screen.getByText('Loading user stats...')).toBeInTheDocument();
    expect(screen.getByText('Loading post stats...')).toBeInTheDocument();
  });
});
```

## Key Takeaways

1. **Async Components**: Await component render before passing to `render()`
2. **Suspense**: Test both fallback and resolved states
3. **Server Actions**: Mock server actions and verify FormData
4. **Error Boundaries**: Test error display and reset functionality
5. **Parallel Fetching**: Each Suspense boundary loads independently

---

**Next**: [Common Patterns](common-patterns.md) | **Previous**: [Best Practices](testing-best-practices.md)
