# Test File Template

Copy this template when creating new test files.

---

## Component Test Template

```typescript
// src/components/ComponentName.test.tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  const defaultProps = {
    // Define default props here
  };

  function renderComponent(props = {}) {
    return render(<ComponentName {...defaultProps} {...props} />);
  }

  describe('rendering', () => {
    it('renders with default props', () => {
      renderComponent();
      // Add assertions
    });

    it('renders with custom props', () => {
      renderComponent({ /* custom props */ });
      // Add assertions
    });
  });

  describe('interactions', () => {
    it('handles user interaction', async () => {
      const user = userEvent.setup();
      const onAction = vi.fn();

      renderComponent({ onAction });

      await user.click(screen.getByRole('button'));

      expect(onAction).toHaveBeenCalled();
    });
  });

  describe('edge cases', () => {
    it('handles null/undefined props', () => {
      renderComponent({ prop: null });
      // Add assertions
    });

    it('handles empty data', () => {
      renderComponent({ data: [] });
      // Add assertions
    });
  });
});
```

---

## Hook Test Template

```typescript
// src/hooks/useHookName.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useHookName } from './useHookName';

describe('useHookName', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useHookName());

    expect(result.current.value).toBe(expectedDefault);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useHookName(customValue));

    expect(result.current.value).toBe(customValue);
  });

  it('updates state', () => {
    const { result } = renderHook(() => useHookName());

    act(() => {
      result.current.update(newValue);
    });

    expect(result.current.value).toBe(newValue);
  });

  it('handles async operations', async () => {
    const { result } = renderHook(() => useHookName());

    await act(async () => {
      await result.current.fetchData();
    });

    expect(result.current.data).toBeDefined();
  });
});
```

---

## Utility Function Test Template

```typescript
// src/utils/functionName.test.ts
import { describe, it, expect } from 'vitest';
import { functionName } from './functionName';

describe('functionName', () => {
  describe('valid inputs', () => {
    it('handles basic case', () => {
      expect(functionName(input)).toBe(expected);
    });

    it('handles complex case', () => {
      expect(functionName(complexInput)).toEqual(complexExpected);
    });
  });

  describe('edge cases', () => {
    it('handles zero', () => {
      expect(functionName(0)).toBe(expectedForZero);
    });

    it('handles negative values', () => {
      expect(functionName(-1)).toBe(expectedForNegative);
    });

    it('handles null/undefined', () => {
      expect(functionName(null)).toBe('');
      expect(functionName(undefined)).toBe('');
    });

    it('handles empty input', () => {
      expect(functionName('')).toBe('');
    });

    it('handles large values', () => {
      expect(functionName(999999)).toBeDefined();
    });
  });

  describe('error handling', () => {
    it('throws for invalid input', () => {
      expect(() => functionName(invalid)).toThrow('Error message');
    });
  });
});
```

---

## API Route Test Template

```typescript
// src/api/routeName.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { routeName } from './routeName';
import { db } from '../lib/db';

describe('POST /api/resource', () => {
  beforeEach(async () => {
    await db.resource.deleteMany(); // Clean database
  });

  afterEach(async () => {
    await db.resource.deleteMany(); // Cleanup
  });

  describe('successful requests', () => {
    it('creates resource with valid data', async () => {
      const input = {
        // Valid input data
      };

      const result = await routeName({ data: input });

      expect(result.status).toBe(201);
      expect(result.body).toMatchObject(input);
    });
  });

  describe('validation errors', () => {
    it('returns 400 for missing required field', async () => {
      const input = {
        // Missing required field
      };

      const result = await routeName({ data: input });

      expect(result.status).toBe(400);
      expect(result.body.error).toContain('required');
    });

    it('returns 400 for invalid format', async () => {
      const input = {
        field: 'invalid-format'
      };

      const result = await routeName({ data: input });

      expect(result.status).toBe(400);
      expect(result.body.error).toContain('format');
    });
  });

  describe('database errors', () => {
    it('returns 409 for duplicate', async () => {
      const input = { /* data */ };

      await routeName({ data: input }); // Create first
      const result = await routeName({ data: input }); // Duplicate

      expect(result.status).toBe(409);
    });

    it('returns 500 for database failure', async () => {
      vi.spyOn(db.resource, 'create').mockRejectedValueOnce(
        new Error('Database error')
      );

      const result = await routeName({ data: {} });

      expect(result.status).toBe(500);
    });
  });
});
```

---

## Usage

1. Copy appropriate template
2. Replace `ComponentName`, `HookName`, or `functionName`
3. Update imports
4. Customize default props/inputs
5. Write tests following TDD cycle

---

**Template Version**: 1.0
