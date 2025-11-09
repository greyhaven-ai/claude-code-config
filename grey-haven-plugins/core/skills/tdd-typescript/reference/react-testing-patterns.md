# React Testing Patterns

Essential patterns for testing React components and hooks with Testing Library.

## Component Testing

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/react';
import { UserCard } from './UserCard';

it('renders user name', () => {
  const user = { name: 'Alice', email: 'alice@example.com' };

  render(<UserCard user={user} />);

  expect(screen.getByText('Alice')).toBeInTheDocument();
});
```

### Query Methods

| Method | When Not Found | Use Case |
|--------|---------------|----------|
| `getBy...` | Throws error | Element should exist |
| `queryBy...` | Returns null | Element might not exist |
| `findBy...` | Rejects promise | Async, element will appear |

**Examples**:
```typescript
// Assert element exists
expect(screen.getByRole('button')).toBeInTheDocument();

// Check element doesn't exist
expect(screen.queryByText('Error')).not.toBeInTheDocument();

// Wait for async element
const button = await screen.findByRole('button');
```

### User Interactions

```typescript
import { userEvent } from '@testing-library/user-event';

it('handles button click', async () => {
  const user = userEvent.setup();
  const onClick = vi.fn();

  render(<Button onClick={onClick}>Click me</Button>);

  await user.click(screen.getByRole('button'));

  expect(onClick).toHaveBeenCalled();
});

it('handles form input', async () => {
  const user = userEvent.setup();

  render(<input type="text" />);

  await user.type(screen.getByRole('textbox'), 'Hello');

  expect(screen.getByRole('textbox')).toHaveValue('Hello');
});
```

## Hook Testing

### Basic Hook Test

```typescript
import { renderHook } from '@testing-library/react';
import { useCounter } from './useCounter';

it('increments counter', () => {
  const { result } = renderHook(() => useCounter());

  act(() => {
    result.current.increment();
  });

  expect(result.current.count).toBe(1);
});
```

### Hook with Props

```typescript
it('initializes with custom value', () => {
  const { result } = renderHook(
    ({ initialValue }) => useCounter(initialValue),
    { initialProps: { initialValue: 10 } }
  );

  expect(result.current.count).toBe(10);
});
```

### Async Hooks

```typescript
it('fetches data', async () => {
  const { result } = renderHook(() => useFetchUser('1'));

  await waitFor(() => {
    expect(result.current.data).toBeDefined();
  });

  expect(result.current.data.name).toBe('Alice');
});
```

## Query Strategies

### By Role (Preferred)

```typescript
screen.getByRole('button', { name: /submit/i });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('heading', { level: 1 });
```

### By Label

```typescript
screen.getByLabelText('Email');
screen.getByLabelText(/password/i);
```

### By Text

```typescript
screen.getByText('Welcome');
screen.getByText(/hello/i);
```

### By Test ID (Last Resort)

```typescript
screen.getByTestId('user-card');
```

## Async Testing

### waitFor

```typescript
it('displays data after loading', async () => {
  render(<UserProfile userId="1" />);

  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });
});
```

### findBy (Combines getBy + waitFor)

```typescript
it('displays data', async () => {
  render(<UserProfile userId="1" />);

  const name = await screen.findByText('Alice');
  expect(name).toBeInTheDocument();
});
```

## Testing Loading States

```typescript
it('shows loading spinner', () => {
  render(<UserProfile userId="1" isLoading={true} />);

  expect(screen.getByRole('status')).toBeInTheDocument();
  expect(screen.queryByText('Alice')).not.toBeInTheDocument();
});
```

## Testing Error States

```typescript
it('displays error message', () => {
  const error = new Error('Failed to load');

  render(<UserProfile error={error} />);

  expect(screen.getByRole('alert')).toHaveTextContent(/failed to load/i);
});
```

## Mocking API Calls

### TanStack Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function renderWithQuery(component) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false }
    }
  });

  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
}

it('fetches and displays user', async () => {
  renderWithQuery(<UserProfile userId="1" />);

  const name = await screen.findByText('Alice');
  expect(name).toBeInTheDocument();
});
```

## Custom Render

```typescript
// test-utils.tsx
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function AllProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false }
    }
  });

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options?: RenderOptions
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

// In tests
it('renders component', () => {
  renderWithProviders(<MyComponent />);
});
```

## Accessibility Testing

### Test with Roles

```typescript
it('has accessible button', () => {
  render(<Button>Submit</Button>);

  const button = screen.getByRole('button', { name: /submit/i });
  expect(button).toBeInTheDocument();
});
```

### Test ARIA Attributes

```typescript
it('marks invalid field', () => {
  render(<Input error="Required" />);

  const input = screen.getByRole('textbox');
  expect(input).toHaveAttribute('aria-invalid', 'true');
});
```

## Form Testing

```typescript
it('submits form', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'alice@example.com',
    password: 'password123'
  });
});
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `render()` | Render component |
| `screen.getByRole()` | Query by ARIA role (preferred) |
| `screen.getByText()` | Query by visible text |
| `screen.findBy...()` | Query async (returns promise) |
| `screen.queryBy...()` | Query that might not exist |
| `userEvent.click()` | Simulate click |
| `userEvent.type()` | Simulate typing |
| `waitFor()` | Wait for assertion to pass |
| `act()` | Wrap state updates |
| `renderHook()` | Test custom hooks |

---

**Best Practice**: Query by role/label (accessibility), use userEvent for interactions, test user behavior not implementation.
