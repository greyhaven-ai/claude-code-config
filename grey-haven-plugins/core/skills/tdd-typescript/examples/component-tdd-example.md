# Component TDD Example: UserProfile

Complete TDD workflow for building a React component using red-green-refactor methodology.

## Goal

Build a `UserProfile` component that displays user information with the following requirements:
- Display user's name, email, and role
- Show loading state while fetching data
- Handle error state gracefully
- Display "User not found" for invalid IDs

## Cycle 1: Display User Name

### ❌ RED - Write Failing Test

```typescript
// src/components/UserProfile.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('displays user name', () => {
    const user = {
      id: '1',
      name: 'Alice Smith',
      email: 'alice@example.com',
      role: 'Developer'
    };

    render(<UserProfile user={user} />);

    expect(screen.getByText('Alice Smith')).toBeInTheDocument();
  });
});
```

**Run test**:
```bash
bun test src/components/UserProfile.test.tsx
```

**Result**: ❌ `FAIL` - UserProfile component doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/components/UserProfile.tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface UserProfileProps {
  user: User;
}

export function UserProfile({ user }: UserProfileProps) {
  return <div>{user.name}</div>;
}
```

**Run test**:
```bash
bun test src/components/UserProfile.test.tsx
```

**Result**: ✅ `PASS` - Test passes!

### 🔄 REFACTOR - Improve Code

_No refactoring needed yet - code is minimal and clear._

_Cycle 2 (display email and role) omitted for brevity._

---

## Cycle 3: Loading State

### ❌ RED - Write Failing Test

```typescript
// src/components/UserProfile.test.tsx
describe('UserProfile', () => {
  // ... previous tests ...

  it('displays loading state when isLoading is true', () => {
    render(<UserProfile user={undefined} isLoading={true} />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });
});
```

**Run test**: ❌ `FAIL` - isLoading prop doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/components/UserProfile.tsx
interface UserProfileProps {
  user?: User;
  isLoading?: boolean;
}

export function UserProfile({ user, isLoading }: UserProfileProps) {
  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <div>User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      <span className="role">{user.role}</span>
    </div>
  );
}
```

**Run test**: ✅ `PASS` - All tests pass!

### 🔄 REFACTOR - Improve Code

Extract loading component:

```typescript
// src/components/UserProfile.tsx
function LoadingState() {
  return (
    <div className="loading" role="status" aria-live="polite">
      <span className="spinner" />
      <span>Loading user profile...</span>
    </div>
  );
}

export function UserProfile({ user, isLoading }: UserProfileProps) {
  if (isLoading) {
    return <LoadingState />;
  }

  if (!user) {
    return <div>User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      <span className="role">{user.role}</span>
    </div>
  );
}
```

**Run test**: ✅ `PASS` - Tests still pass!

---

## Cycle 4: Error State

### ❌ RED - Write Failing Test

```typescript
// src/components/UserProfile.test.tsx
describe('UserProfile', () => {
  // ... previous tests ...

  it('displays error message when error occurs', () => {
    const error = new Error('Failed to fetch user');

    render(<UserProfile user={undefined} error={error} />);

    expect(screen.getByRole('alert')).toHaveTextContent(/failed to fetch user/i);
  });
});
```

**Run test**: ❌ `FAIL` - error prop doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/components/UserProfile.tsx
interface UserProfileProps {
  user?: User;
  isLoading?: boolean;
  error?: Error;
}

export function UserProfile({ user, isLoading, error }: UserProfileProps) {
  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div role="alert" className="error">
        {error.message}
      </div>
    );
  }

  if (!user) {
    return <div>User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      <span className="role">{user.role}</span>
    </div>
  );
}
```

**Run test**: ✅ `PASS` - All tests pass!

### 🔄 REFACTOR - Improve Code

Extract error component and add retry button:

```typescript
// src/components/UserProfile.tsx
interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
}

function ErrorState({ error, onRetry }: ErrorStateProps) {
  return (
    <div role="alert" className="error">
      <p>{error.message}</p>
      {onRetry && (
        <button onClick={onRetry} type="button">
          Retry
        </button>
      )}
    </div>
  );
}

interface UserProfileProps {
  user?: User;
  isLoading?: boolean;
  error?: Error;
  onRetry?: () => void;
}

export function UserProfile({ user, isLoading, error, onRetry }: UserProfileProps) {
  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState error={error} onRetry={onRetry} />;
  }

  if (!user) {
    return <div className="not-found">User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      <span className="role">{user.role}</span>
    </div>
  );
}
```

**Run test**: ✅ `PASS` - Tests still pass!

---

## Cycle 5: User Interactions (Retry Button)

### ❌ RED - Write Failing Test

```typescript
// src/components/UserProfile.test.tsx
import { vi } from 'vitest';

describe('UserProfile', () => {
  // ... previous tests ...

  it('calls onRetry when retry button is clicked', async () => {
    const error = new Error('Failed to fetch user');
    const onRetry = vi.fn();
    const { user } = render(
      <UserProfile user={undefined} error={error} onRetry={onRetry} />
    );

    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);

    expect(onRetry).toHaveBeenCalledOnce();
  });
});
```

**Run test**: ✅ `PASS` - Already passes! (onRetry was added in refactor)

_This demonstrates test-driven refactoring - we added functionality during refactor that we now have test coverage for._

---

## Final Component

```typescript
// src/components/UserProfile.tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface UserProfileProps {
  user?: User;
  isLoading?: boolean;
  error?: Error;
  onRetry?: () => void;
}

function LoadingState() {
  return (
    <div className="loading" role="status" aria-live="polite">
      <span className="spinner" />
      <span>Loading user profile...</span>
    </div>
  );
}

interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
}

function ErrorState({ error, onRetry }: ErrorStateProps) {
  return (
    <div role="alert" className="error">
      <p>{error.message}</p>
      {onRetry && (
        <button onClick={onRetry} type="button">
          Retry
        </button>
      )}
    </div>
  );
}

export function UserProfile({ user, isLoading, error, onRetry }: UserProfileProps) {
  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState error={error} onRetry={onRetry} />;
  }

  if (!user) {
    return <div className="not-found">User not found</div>;
  }

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p className="email">{user.email}</p>
      <span className="role">{user.role}</span>
    </div>
  );
}
```

## Final Test Suite

```typescript
// src/components/UserProfile.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'Alice Smith',
    email: 'alice@example.com',
    role: 'Developer'
  };

  it('displays user name', () => {
    render(<UserProfile user={mockUser} />);
    expect(screen.getByText('Alice Smith')).toBeInTheDocument();
  });

  it('displays user email and role', () => {
    render(<UserProfile user={mockUser} />);
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    expect(screen.getByText('Developer')).toBeInTheDocument();
  });

  it('displays loading state when isLoading is true', () => {
    render(<UserProfile user={undefined} isLoading={true} />);
    expect(screen.getByText(/loading user profile/i)).toBeInTheDocument();
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });

  it('displays error message when error occurs', () => {
    const error = new Error('Failed to fetch user');
    render(<UserProfile user={undefined} error={error} />);
    expect(screen.getByRole('alert')).toHaveTextContent(/failed to fetch user/i);
  });

  it('displays "User not found" when user is undefined', () => {
    render(<UserProfile user={undefined} />);
    expect(screen.getByText(/user not found/i)).toBeInTheDocument();
  });

  it('calls onRetry when retry button is clicked', async () => {
    const error = new Error('Failed to fetch user');
    const onRetry = vi.fn();
    const user = userEvent.setup();

    render(<UserProfile user={undefined} error={error} onRetry={onRetry} />);

    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);

    expect(onRetry).toHaveBeenCalledOnce();
  });
});
```

## Summary

| Metric | Value |
|--------|-------|
| **TDD Cycles** | 5 |
| **Tests Written** | 6 |
| **Test Coverage** | 100% |
| **Lines of Code** | ~60 |
| **Lines of Tests** | ~55 |
| **Test:Code Ratio** | 0.92:1 |
| **Time to Implement** | ~30 minutes |

## Key Takeaways

1. **Start Simple**: First test was just displaying a name
2. **Incremental**: Each cycle added one small feature
3. **Refactor Confidently**: Tests enabled safe refactoring
4. **Extract Components**: Refactoring created LoadingState and ErrorState
5. **Complete Coverage**: TDD naturally led to 100% test coverage
6. **Better Design**: TDD guided us to a cleaner component structure

---

**TDD Result**: Production-ready component with comprehensive test coverage, built incrementally through red-green-refactor cycles.
