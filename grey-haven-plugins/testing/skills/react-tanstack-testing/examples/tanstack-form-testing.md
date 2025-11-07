# TanStack Form Testing Examples

Complete examples for testing TanStack Form validation, submission, and field states.

## Test Setup

### Form Dependencies

```typescript
// src/test/form-utils.tsx
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';

export function renderForm(ui: ReactElement, options?: RenderOptions) {
  return render(ui, options);
}
```

## Example 1: Basic Form with Validation

### Form Component

```typescript
// src/components/UserForm.tsx
import { useForm } from '@tanstack/react-form';
import { zodValidator } from '@tanstack/zod-form-adapter';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be at least 18 years old'),
});

export function UserForm({ onSubmit }: { onSubmit: (data: any) => void }) {
  const form = useForm({
    defaultValues: {
      name: '',
      email: '',
      age: 0,
    },
    onSubmit: async ({ value }) => {
      onSubmit(value);
    },
    validatorAdapter: zodValidator,
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      <div>
        <form.Field
          name="name"
          validators={{
            onChange: userSchema.shape.name,
          }}
          children={(field) => (
            <div>
              <label htmlFor="name">Name</label>
              <input
                id="name"
                value={field.state.value}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              {field.state.meta.errors.length > 0 && (
                <span role="alert">{field.state.meta.errors[0]}</span>
              )}
            </div>
          )}
        />
      </div>

      <div>
        <form.Field
          name="email"
          validators={{
            onChange: userSchema.shape.email,
          }}
          children={(field) => (
            <div>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={field.state.value}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              {field.state.meta.errors.length > 0 && (
                <span role="alert">{field.state.meta.errors[0]}</span>
              )}
            </div>
          )}
        />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Test Suite

```typescript
// src/components/UserForm.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { screen, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserForm } from './UserForm';

describe('UserForm', () => {
  it('renders all form fields', () => {
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('shows validation error for short name', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Name'), 'A');
    await user.tab(); // Trigger blur/validation

    expect(await screen.findByRole('alert')).toHaveTextContent('Name must be at least 2 characters');
  });

  it('shows validation error for invalid email', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Email'), 'invalid-email');
    await user.tab();

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email address');
  });

  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Name'), 'Alice Johnson');
    await user.type(screen.getByLabelText('Email'), 'alice@example.com');
    await user.click(screen.getByRole('button', { name: 'Submit' }));

    expect(onSubmit).toHaveBeenCalledWith({
      name: 'Alice Johnson',
      email: 'alice@example.com',
      age: 0,
    });
  });

  it('does not submit form with invalid data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UserForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Name'), 'A');
    await user.type(screen.getByLabelText('Email'), 'invalid');
    await user.click(screen.getByRole('button', { name: 'Submit' }));

    expect(onSubmit).not.toHaveBeenCalled();
  });
});
```

## Example 2: Testing Field States

### Form with Field State Display

```typescript
// src/components/FieldStateForm.tsx
import { useForm } from '@tanstack/react-form';

export function FieldStateForm() {
  const form = useForm({
    defaultValues: {
      username: '',
    },
  });

  return (
    <form>
      <form.Field
        name="username"
        children={(field) => (
          <div>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />

            <div data-testid="field-states">
              <span data-testid="is-touched">{field.state.meta.isTouched ? 'Touched' : 'Untouched'}</span>
              <span data-testid="is-dirty">{field.state.meta.isDirty ? 'Dirty' : 'Pristine'}</span>
              <span data-testid="is-valid">{field.state.meta.errors.length === 0 ? 'Valid' : 'Invalid'}</span>
            </div>
          </div>
        )}
      />
    </form>
  );
}
```

### Test Suite

```typescript
// src/components/FieldStateForm.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FieldStateForm } from './FieldStateForm';

describe('FieldStateForm', () => {
  it('field starts untouched and pristine', () => {
    render(<FieldStateForm />);

    expect(screen.getByTestId('is-touched')).toHaveTextContent('Untouched');
    expect(screen.getByTestId('is-dirty')).toHaveTextContent('Pristine');
  });

  it('field becomes touched after blur', async () => {
    const user = userEvent.setup();
    render(<FieldStateForm />);

    const input = screen.getByLabelText('Username');
    await user.click(input);
    await user.tab(); // Blur the field

    expect(screen.getByTestId('is-touched')).toHaveTextContent('Touched');
  });

  it('field becomes dirty after value change', async () => {
    const user = userEvent.setup();
    render(<FieldStateForm />);

    await user.type(screen.getByLabelText('Username'), 'alice');

    expect(screen.getByTestId('is-dirty')).toHaveTextContent('Dirty');
  });
});
```

## Example 3: Testing Async Validation

### Form with Async Validation

```typescript
// src/components/UsernameForm.tsx
import { useForm } from '@tanstack/react-form';

async function checkUsernameAvailable(username: string): Promise<boolean> {
  const response = await fetch(`/api/check-username?username=${username}`);
  return response.json();
}

export function UsernameForm({ onSubmit }: { onSubmit: (data: any) => void }) {
  const form = useForm({
    defaultValues: {
      username: '',
    },
    onSubmit: async ({ value }) => {
      onSubmit(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      <form.Field
        name="username"
        validators={{
          onChangeAsync: async ({ value }) => {
            if (value.length < 3) {
              return 'Username must be at least 3 characters';
            }

            const isAvailable = await checkUsernameAvailable(value);
            if (!isAvailable) {
              return 'Username already taken';
            }

            return undefined;
          },
        }}
        children={(field) => (
          <div>
            <label htmlFor="username">Username</label>
            <input
              id="username"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
            />

            {field.state.meta.isValidating && (
              <span data-testid="validating">Checking availability...</span>
            )}

            {field.state.meta.errors.length > 0 && (
              <span role="alert">{field.state.meta.errors[0]}</span>
            )}
          </div>
        )}
      />

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Test Suite

```typescript
// src/components/UsernameForm.test.tsx
import { describe, it, expect, vi, beforeAll, afterEach, afterAll } from 'vitest';
import { screen, render, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { UsernameForm } from './UsernameForm';

const server = setupServer(
  http.get('/api/check-username', ({ request }) => {
    const url = new URL(request.url);
    const username = url.searchParams.get('username');
    return HttpResponse.json(username !== 'taken');
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('UsernameForm', () => {
  it('shows validating indicator during async validation', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UsernameForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Username'), 'alice');

    expect(screen.getByTestId('validating')).toHaveTextContent('Checking availability...');
  });

  it('accepts available username', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UsernameForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Username'), 'available');

    await waitFor(() => {
      expect(screen.queryByTestId('validating')).not.toBeInTheDocument();
    });

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('rejects taken username', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<UsernameForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText('Username'), 'taken');

    expect(await screen.findByRole('alert')).toHaveTextContent('Username already taken');
  });
});
```

## Example 4: Testing Form Reset

### Form with Reset Button

```typescript
// src/components/ResettableForm.tsx
import { useForm } from '@tanstack/react-form';

export function ResettableForm() {
  const form = useForm({
    defaultValues: {
      name: '',
      email: '',
    },
  });

  return (
    <form>
      <div>
        <label htmlFor="name">Name</label>
        <form.Field
          name="name"
          children={(field) => (
            <input
              id="name"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
            />
          )}
        />
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <form.Field
          name="email"
          children={(field) => (
            <input
              id="email"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
            />
          )}
        />
      </div>

      <button type="button" onClick={() => form.reset()}>
        Reset
      </button>
    </form>
  );
}
```

### Test Suite

```typescript
// src/components/ResettableForm.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ResettableForm } from './ResettableForm';

describe('ResettableForm', () => {
  it('resets form fields to default values', async () => {
    const user = userEvent.setup();
    render(<ResettableForm />);

    const nameInput = screen.getByLabelText('Name') as HTMLInputElement;
    const emailInput = screen.getByLabelText('Email') as HTMLInputElement;

    // Fill in form
    await user.type(nameInput, 'Alice');
    await user.type(emailInput, 'alice@example.com');

    expect(nameInput.value).toBe('Alice');
    expect(emailInput.value).toBe('alice@example.com');

    // Reset form
    await user.click(screen.getByRole('button', { name: 'Reset' }));

    expect(nameInput.value).toBe('');
    expect(emailInput.value).toBe('');
  });
});
```

## Key Takeaways

1. **Zod Validation**: Use `zodValidator` for type-safe schema validation
2. **Field States**: Test touched, dirty, pristine, and valid states
3. **Async Validation**: Use MSW to mock async validation endpoints
4. **Error Display**: Test that validation errors appear correctly
5. **Submission**: Test form submission with both valid and invalid data
6. **Reset**: Test form reset functionality clears all fields

---

**Previous**: [Table Testing](tanstack-table-testing.md) | **Index**: [Examples Index](INDEX.md)
