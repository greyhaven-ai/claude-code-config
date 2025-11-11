# TDD Quality Checklist (TypeScript/JavaScript)

Verify strict Test-Driven Development discipline and test quality for TypeScript/JavaScript projects.

## Red-Green-Refactor Discipline

### Red Phase (Failing Test)
- [ ] **Test written before implementation**
- [ ] **Test fails for the right reason** (not syntax error)
- [ ] **Test failure message is clear**
- [ ] **Only one test failing** (focus on one thing at a time)
- [ ] **Test describes desired behavior** (not implementation)

### Green Phase (Pass Test)
- [ ] **Minimal code written** to pass test
- [ ] **No over-engineering** (simplest solution first)
- [ ] **Test now passes**
- [ ] **All existing tests still pass** (no regression)
- [ ] **Implementation focused on making test green**

### Refactor Phase
- [ ] **Code improved** while keeping tests green
- [ ] **Duplication removed**
- [ ] **Names improved** for clarity
- [ ] **Design patterns applied** where appropriate
- [ ] **All tests still passing** after refactor

## Test Quality (Vitest)

### Test Structure (AAA Pattern)
- [ ] **Arrange**: Setup clearly separated
- [ ] **Act**: Single action being tested
- [ ] **Assert**: Clear assertions with good messages
- [ ] **No logic in tests** (loops, conditionals minimal)

### Test Coverage
- [ ] **Unit tests** for all public functions
- [ ] **Integration tests** for component interactions
- [ ] **Edge cases covered** (null, undefined, empty, max values)
- [ ] **Error cases tested** (invalid input, exceptions)
- [ ] **Coverage > 90%** for new code
- [ ] **Branch coverage** adequate (not just line coverage)

### Test Independence
- [ ] **Tests run in any order** (no interdependencies)
- [ ] **Tests clean up after themselves**
- [ ] **No shared mutable state** between tests
- [ ] **beforeEach/afterEach used** for setup/teardown
- [ ] **Tests isolated** (can run individually)

### Test Naming
- [ ] **Descriptive test names** (describe behavior, not implementation)
- [ ] **Following pattern**: `should_returnValue_when_condition`
- [ ] **Easy to understand** what test verifies
- [ ] **Organized in describe blocks** by feature/function

## TypeScript Testing Best Practices

### Type Safety in Tests
- [ ] **Test data properly typed** (no `any`)
- [ ] **Mock types match** real types
- [ ] **Type assertions avoided** where possible
- [ ] **Factory functions** for test data generation

### Mocking (Vitest)
- [ ] **vi.mock()** used for external dependencies
- [ ] **Mocks configured properly** before tests
- [ ] **Mock return values set** appropriately
- [ ] **Mock calls verified** (expect(mock).toHaveBeenCalledWith())
- [ ] **Mocks cleared** between tests (vi.clearAllMocks())

### Async Testing
- [ ] **async/await** used correctly in tests
- [ ] **Promises resolved/rejected** in assertions
- [ ] **Timeouts configured** for long operations
- [ ] **No race conditions** in tests
- [ ] **waitFor** used for async state changes

## React Component Testing

### Testing Library Best Practices
- [ ] **Query by role/label** (not test IDs if possible)
- [ ] **User interactions simulated** (fireEvent, userEvent)
- [ ] **Async rendering handled** (waitFor, findBy*)
- [ ] **No implementation details** tested (state, props internal structure)
- [ ] **Accessibility checked** (roles, labels)

### Component Test Coverage
- [ ] **Render tests** (component displays correctly)
- [ ] **User interaction tests** (clicks, inputs work)
- [ ] **Conditional rendering** tested
- [ ] **Props validation** tested
- [ ] **Hooks tested** (useState, useEffect, custom hooks)

### Integration Tests
- [ ] **Multiple components** tested together
- [ ] **Data flow** tested (props, context)
- [ ] **API integration** mocked appropriately
- [ ] **Error boundaries** tested
- [ ] **Loading states** tested

## TanStack Query Testing

### Query Testing
- [ ] **QueryClient configured** for tests (no retries, fast failure)
- [ ] **Queries mocked** (MSW or vi.mock)
- [ ] **Loading states** tested
- [ ] **Error states** tested
- [ ] **Success states** tested
- [ ] **Query invalidation** tested

### Mutation Testing
- [ ] **Mutations mocked** appropriately
- [ ] **onSuccess callbacks** tested
- [ ] **onError callbacks** tested
- [ ] **Optimistic updates** tested (if used)

## Test Organization

### File Structure
- [ ] **Test files colocated** with source (*.test.ts, *.spec.ts)
- [ ] **Test utilities** in __tests__/utils/
- [ ] **Fixtures** in __tests__/fixtures/
- [ ] **Mocks** in __mocks__/
- [ ] **Clear directory structure**

### Test Utilities
- [ ] **Factory functions** for test data
- [ ] **Helper functions** for common setup
- [ ] **Custom matchers** where appropriate
- [ ] **Test utilities reused** (no duplication)

## Test Performance

### Speed
- [ ] **Unit tests run fast** (< 100ms each)
- [ ] **Integration tests acceptable** (< 500ms each)
- [ ] **No unnecessary waits** (waitFor used properly)
- [ ] **Parallel execution** enabled
- [ ] **Total suite runs < 10 seconds** (for fast feedback)

### CI Integration
- [ ] **Tests run in CI** (GitHub Actions, etc.)
- [ ] **Coverage reported** in CI
- [ ] **Failed tests fail build**
- [ ] **Coverage thresholds enforced**

## Test Maintainability

### Documentation
- [ ] **Complex tests commented** (why, not what)
- [ ] **Test intent clear** from name and structure
- [ ] **Test data meaningful** (no magic values)
- [ ] **Constants defined** for repeated values

### Refactoring
- [ ] **Test duplication removed**
- [ ] **Setup extracted** to beforeEach
- [ ] **Common assertions** extracted to utilities
- [ ] **Tests refactored** when source refactored

## Vitest Configuration

### Setup
- [ ] **vitest.config.ts** configured
- [ ] **globals: true** enabled (optional)
- [ ] **environment** set correctly (jsdom, node, happy-dom)
- [ ] **setupFiles** configured if needed
- [ ] **coverage thresholds** set (lines, functions, branches, statements)

### Coverage
- [ ] **Coverage provider** configured (v8 or istanbul)
- [ ] **Coverage directory** set
- [ ] **Coverage exclude** configured
- [ ] **Coverage reporter** set (text, html, json)

## Common Test Smells

Avoid these anti-patterns:

❌ **Don't:**
- Test implementation details (private methods, internal state)
- Share mutable state between tests
- Use actual timers (use vi.useFakeTimers())
- Test multiple things in one test
- Have long test files (> 500 lines)
- Use await sleep() for timing (use waitFor)
- Snapshot testing as primary strategy (use sparingly)

✅ **Do:**
- Test behavior and public API
- Isolate tests completely
- Mock timers for predictability
- One assertion focus per test
- Split large test files
- Use proper async utilities
- Assertions with clear messages

## Coverage Targets

### Minimum Coverage
- Lines: 90%
- Functions: 90%
- Branches: 85%
- Statements: 90%

### Critical Path Coverage
- Auth flows: 100%
- Payment processing: 100%
- Multi-tenant isolation: 100%
- Data validation: 100%

## Scoring

- **All red-green-refactor checks passed**: Excellent TDD discipline ✅
- **All test quality checks passed**: High-quality tests ✅
- **Coverage > 90%**: Great coverage ✅
- **Tests run fast (< 10s)**: Good performance ✅

**Overall:**
- **90+ items checked**: Excellent - Production ready ✅
- **75-89 items**: Good - Minor improvements ⚠️
- **60-74 items**: Fair - Significant work needed 🔴
- **<60 items**: Poor - TDD discipline lacking ❌

## Example Good Test

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should display user name when data loads successfully', async () => {
    // Arrange
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };
    vi.mocked(fetchUser).mockResolvedValue(mockUser);

    // Act
    render(<UserProfile userId="1" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });

  it('should display error message when data fails to load', async () => {
    // Arrange
    vi.mocked(fetchUser).mockRejectedValue(new Error('Network error'));

    // Act
    render(<UserProfile userId="1" />);

    // Assert
    await waitFor(() => {
      expect(screen.getByText(/error loading user/i)).toBeInTheDocument();
    });
  });
});
```

## Tools & Resources

**Testing:**
- Vitest (test runner)
- @testing-library/react (React testing)
- @testing-library/user-event (user interactions)
- happy-dom (lightweight DOM)

**Coverage:**
- @vitest/coverage-v8 (coverage provider)
- @vitest/ui (visual test runner)

**Related:**
- [Testing Strategy Skill](../../testing-strategy/SKILL.md)
- [TDD Python Checklist](../../tdd-python/checklists/tdd-quality-checklist.md)
- [React Testing Examples](../examples/react-component-testing.md)

---

**Total Items**: 100+ TDD & test quality checks
**Critical Items**: Red-Green-Refactor, Coverage, Test Independence
**Last Updated**: 2025-11-09
