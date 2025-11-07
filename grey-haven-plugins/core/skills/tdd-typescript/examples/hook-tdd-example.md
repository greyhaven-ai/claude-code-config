# Hook TDD Example: useCounter

Complete TDD workflow for building a custom React hook using red-green-refactor methodology.

## Goal

Build a `useCounter` hook with the following requirements:
- Initialize with a starting value
- Increment and decrement counter
- Reset counter to initial value
- Set counter to specific value
- Enforce min and max bounds

## Cycle 1: Initialize Counter

### ❌ RED - Write Failing Test

```typescript
// src/hooks/useCounter.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value of 0', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });
});
```

**Run test**: ❌ `FAIL` - useCounter doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/hooks/useCounter.ts
import { useState } from 'react';

export function useCounter() {
  const [count, setCount] = useState(0);

  return { count };
}
```

**Run test**: ✅ `PASS`

### 🔄 REFACTOR

_No refactoring needed yet._

_Cycles 2 (custom initial value) omitted for brevity._

---

## Cycle 3: Increment Function

### ❌ RED - Write Failing Test

```typescript
import { act } from '@testing-library/react';

describe('useCounter', () => {
  // ... previous tests ...

  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(6);
  });
});
```

**Run test**: ❌ `FAIL` - increment function doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/hooks/useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount(count + 1);

  return { count, increment };
}
```

**Run test**: ✅ `PASS`

### 🔄 REFACTOR - Fix Closure Issue

Use functional update to avoid stale closure:

```typescript
// src/hooks/useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => c + 1);

  return { count, increment };
}
```

**Run test**: ✅ `PASS` - Tests still pass!

---

## Cycle 4: Decrement Function

### ❌ RED - Write Failing Test

```typescript
describe('useCounter', () => {
  // ... previous tests ...

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

**Run test**: ❌ `FAIL` - decrement function doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/hooks/useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => c + 1);
  const decrement = () => setCount((c) => c - 1);

  return { count, increment, decrement };
}
```

**Run test**: ✅ `PASS`

---

## Cycle 5: Reset Function

### ❌ RED - Write Failing Test

```typescript
describe('useCounter', () => {
  // ... previous tests ...

  it('resets counter to initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });
});
```

**Run test**: ❌ `FAIL` - reset function doesn't exist

### ✅ GREEN - Write Minimum Code

```typescript
// src/hooks/useCounter.ts
export function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => c + 1);
  const decrement = () => setCount((c) => c - 1);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}
```

**Run test**: ✅ `PASS`

_Cycle 6 (setValue function) omitted for brevity._

---

## Cycle 7: Min/Max Bounds

### ❌ RED - Write Failing Tests

```typescript
describe('useCounter', () => {
  // ... previous tests ...

  it('respects minimum bound', () => {
    const { result } = renderHook(() => useCounter(0, { min: 0 }));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(0); // Should not go below 0
  });

  it('respects maximum bound', () => {
    const { result } = renderHook(() => useCounter(10, { max: 10 }));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(10); // Should not go above 10
  });
});
```

**Run test**: ❌ `FAIL` - Bounds not enforced

### ✅ GREEN - Write Minimum Code

```typescript
// src/hooks/useCounter.ts
interface UseCounterOptions {
  min?: number;
  max?: number;
}

export function useCounter(
  initialValue = 0,
  options: UseCounterOptions = {}
) {
  const { min, max } = options;
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((c) => {
    const next = c + 1;
    if (max !== undefined && next > max) return c;
    return next;
  });

  const decrement = () => setCount((c) => {
    const next = c - 1;
    if (min !== undefined && next < min) return c;
    return next;
  });

  const reset = () => setCount(initialValue);

  const setValue = (value: number) => {
    if (min !== undefined && value < min) return;
    if (max !== undefined && value > max) return;
    setCount(value);
  };

  return { count, increment, decrement, reset, setValue };
}
```

**Run test**: ✅ `PASS`

### 🔄 REFACTOR - Extract Boundary Logic

```typescript
// src/hooks/useCounter.ts
interface UseCounterOptions {
  min?: number;
  max?: number;
}

export function useCounter(
  initialValue = 0,
  options: UseCounterOptions = {}
) {
  const { min, max } = options;
  const [count, setCount] = useState(initialValue);

  const clamp = (value: number): number => {
    if (min !== undefined && value < min) return min;
    if (max !== undefined && value > max) return max;
    return value;
  };

  const increment = () => setCount((c) => clamp(c + 1));
  const decrement = () => setCount((c) => clamp(c - 1));
  const reset = () => setCount(clamp(initialValue));
  const setValue = (value: number) => setCount(clamp(value));

  return { count, increment, decrement, reset, setValue };
}
```

**Run test**: ✅ `PASS` - Tests still pass!

---

## Final Hook

```typescript
// src/hooks/useCounter.ts
import { useState } from 'react';

interface UseCounterOptions {
  min?: number;
  max?: number;
}

export function useCounter(
  initialValue = 0,
  options: UseCounterOptions = {}
) {
  const { min, max } = options;
  const [count, setCount] = useState(initialValue);

  const clamp = (value: number): number => {
    if (min !== undefined && value < min) return min;
    if (max !== undefined && value > max) return max;
    return value;
  };

  const increment = () => setCount((c) => clamp(c + 1));
  const decrement = () => setCount((c) => clamp(c - 1));
  const reset = () => setCount(clamp(initialValue));
  const setValue = (value: number) => setCount(clamp(value));

  return { count, increment, decrement, reset, setValue };
}
```

## Final Test Suite

```typescript
// src/hooks/useCounter.test.ts
import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value of 0', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(6);
  });

  it('decrements counter', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets counter to initial value', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(12);

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(10);
  });

  it('sets counter to specific value', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.setValue(42);
    });

    expect(result.current.count).toBe(42);
  });

  it('respects minimum bound', () => {
    const { result } = renderHook(() => useCounter(0, { min: 0 }));

    act(() => {
      result.current.decrement();
      result.current.decrement();
    });

    expect(result.current.count).toBe(0);
  });

  it('respects maximum bound', () => {
    const { result } = renderHook(() => useCounter(10, { max: 10 }));

    act(() => {
      result.current.increment();
      result.current.increment();
    });

    expect(result.current.count).toBe(10);
  });

  it('clamps setValue within bounds', () => {
    const { result } = renderHook(() => useCounter(5, { min: 0, max: 10 }));

    act(() => {
      result.current.setValue(-5);
    });
    expect(result.current.count).toBe(0);

    act(() => {
      result.current.setValue(15);
    });
    expect(result.current.count).toBe(10);

    act(() => {
      result.current.setValue(7);
    });
    expect(result.current.count).toBe(7);
  });
});
```

## Summary

| Metric | Value |
|--------|-------|
| **TDD Cycles** | 7 |
| **Tests Written** | 9 |
| **Test Coverage** | 100% |
| **Lines of Code** | ~35 |
| **Lines of Tests** | ~90 |
| **Test:Code Ratio** | 2.6:1 |

## Key Takeaways

1. **renderHook**: Use `@testing-library/react`'s `renderHook` for testing hooks
2. **act()**: Wrap state updates in `act()` for proper React updates
3. **Functional Updates**: Use `setState((prev) => ...)` to avoid closure issues
4. **Test Callbacks**: Test that functions work, not implementation details
5. **Boundary Testing**: Test min/max values and edge cases
6. **Refactor Extract**: Extracted `clamp` function during refactoring

---

**TDD Result**: Production-ready custom hook with comprehensive test coverage and proper boundary handling.
