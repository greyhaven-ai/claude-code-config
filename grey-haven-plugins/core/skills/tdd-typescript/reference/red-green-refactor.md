# Red-Green-Refactor Methodology

The core Test-Driven Development (TDD) cycle for building software incrementally with confidence.

## The TDD Cycle

```
❌ RED → ✅ GREEN → 🔄 REFACTOR → ❌ RED → ...
```

### ❌ RED: Write Failing Test

**Goal**: Write a test for the **next** small piece of functionality.

**Rules**:
- Test should be specific and focused on one behavior
- Test should fail for the right reason (not syntax errors)
- Write only enough test to fail

**Example**:
```typescript
it('adds two numbers', () => {
  expect(add(2, 3)).toBe(5); // Test fails - add() doesn't exist
});
```

**Checklist**:
- [ ] Test is focused on single behavior
- [ ] Test fails when run
- [ ] Test fails with expected error message
- [ ] Test is readable and clear

---

### ✅ GREEN: Write Minimum Code

**Goal**: Make the test pass with the **simplest** possible code.

**Rules**:
- Write only enough code to make the test pass
- Don't worry about code quality yet
- Hardcoding is acceptable if it passes the test
- No premature optimization or abstraction

**Example**:
```typescript
function add(a: number, b: number): number {
  return a + b; // Simplest implementation
}
```

**Checklist**:
- [ ] Test passes when run
- [ ] All previous tests still pass
- [ ] Code is the simplest solution
- [ ] No extra functionality added

---

### 🔄 REFACTOR: Improve Code Quality

**Goal**: Improve code structure **without changing behavior**.

**Rules**:
- Tests must continue to pass throughout refactoring
- Improve readability, maintainability, and design
- Extract functions, rename variables, remove duplication
- Run tests after each small refactoring step

**Example**:
```typescript
// Before refactoring
function add(a: number, b: number): number {
  return a + b;
}

// After refactoring (better naming, validation)
/**
 * Adds two numbers together.
 * @throws {TypeError} If inputs are not numbers
 */
function add(a: number, b: number): number {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('Both arguments must be numbers');
  }
  return a + b;
}
```

**Checklist**:
- [ ] All tests still pass
- [ ] Code is more readable
- [ ] Duplication removed
- [ ] Names are clear and descriptive
- [ ] Complex logic extracted into functions

---

## TDD Principles

### 1. Test First, Always

**Why**: Tests drive the design and ensure testability.

**Bad**:
```typescript
// Write implementation first
function calculateDiscount(price: number, percent: number): number {
  return price * (percent / 100);
}

// Then write tests
it('calculates discount', () => {
  expect(calculateDiscount(100, 10)).toBe(10);
});
```

**Good**:
```typescript
// Write test first
it('calculates 10% discount', () => {
  expect(calculateDiscount(100, 10)).toBe(10); // Fails
});

// Then implement
function calculateDiscount(price: number, percent: number): number {
  return price * (percent / 100);
}
```

---

### 2. One Test at a Time

**Why**: Keeps focus small and prevents overwhelming complexity.

**Process**:
1. Write one test
2. Make it pass
3. Refactor if needed
4. Repeat with next test

---

### 3. Small Steps

**Why**: Easier to debug, faster feedback, less risk.

**Example - Building a Calculator**:
```
Cycle 1: Test addition of positive numbers
Cycle 2: Test addition with zero
Cycle 3: Test addition with negative numbers
Cycle 4: Test subtraction
Cycle 5: Test multiplication
...
```

Not all at once:
```
❌ Cycle 1: Test full calculator with all operations
```

---

### 4. Tests Should Be Fast

**Why**: Fast tests enable frequent running and quick feedback.

**Guidelines**:
- Unit tests should complete in milliseconds
- Avoid database/network calls in unit tests
- Mock external dependencies
- Run full suite in < 10 seconds for small projects

---

### 5. Tests Should Be Independent

**Why**: Tests should pass/fail regardless of order.

**Bad**:
```typescript
let counter = 0;

it('increments counter', () => {
  counter++; // Modifies shared state
  expect(counter).toBe(1);
});

it('increments counter again', () => {
  counter++; // Depends on previous test
  expect(counter).toBe(2); // Fails if run alone
});
```

**Good**:
```typescript
it('increments counter from 0 to 1', () => {
  const counter = createCounter(0);
  counter.increment();
  expect(counter.value).toBe(1);
});

it('increments counter from 5 to 6', () => {
  const counter = createCounter(5);
  counter.increment();
  expect(counter.value).toBe(6);
});
```

---

## Common Pitfalls

### Pitfall 1: Writing Too Much Test Code

**Problem**: Test is too complex or tests multiple behaviors.

**Example**:
```typescript
// Bad: Testing too much at once
it('handles user registration flow', () => {
  const user = createUser(userData);
  validateUser(user);
  saveUser(user);
  sendConfirmationEmail(user);
  expect(user.isActive).toBe(true);
  expect(user.emailSent).toBe(true);
  // ... more assertions
});
```

**Solution**: Break into smaller tests.

---

### Pitfall 2: Writing Too Much Production Code

**Problem**: Implementing features not required by current test.

**Example**:
```typescript
// Test only requires addition
it('adds two numbers', () => {
  expect(add(2, 3)).toBe(5);
});

// But implementation includes subtraction too
function add(a: number, b: number): number {
  return a + b;
}

function subtract(a: number, b: number): number { // Not needed yet!
  return a - b;
}
```

**Solution**: Implement only what the test requires.

---

### Pitfall 3: Skipping Refactor Phase

**Problem**: Code quality degrades over time.

**Example**:
```typescript
// After multiple cycles, code becomes messy
function processOrder(order: any) {
  if (order.items.length === 0) return { error: 'empty' };
  let total = 0;
  for (let i = 0; i < order.items.length; i++) {
    total += order.items[i].price * order.items[i].quantity;
    if (order.items[i].discount) {
      total -= order.items[i].price * (order.items[i].discount / 100);
    }
  }
  if (order.shipping === 'express') total += 10;
  return { total };
}
```

**Solution**: Refactor regularly.
```typescript
function processOrder(order: Order): OrderResult {
  if (isEmptyOrder(order)) {
    return { error: 'Order cannot be empty' };
  }

  const itemsTotal = calculateItemsTotal(order.items);
  const shippingCost = calculateShipping(order.shipping);

  return { total: itemsTotal + shippingCost };
}
```

---

### Pitfall 4: Not Running Tests Frequently

**Problem**: Long feedback loop, harder to identify cause of failure.

**Solution**:
- Run tests after every change (every 1-2 minutes)
- Use watch mode: `bun test --watch`
- Configure IDE to run tests automatically

---

### Pitfall 5: Testing Implementation Details

**Problem**: Tests break when refactoring, even though behavior is unchanged.

**Bad**:
```typescript
it('uses array.reduce internally', () => {
  const spy = vi.spyOn(Array.prototype, 'reduce');
  sum([1, 2, 3]);
  expect(spy).toHaveBeenCalled(); // Testing implementation
});
```

**Good**:
```typescript
it('returns sum of array elements', () => {
  expect(sum([1, 2, 3])).toBe(6); // Testing behavior
});
```

---

## Best Practices

### 1. Arrange-Act-Assert (AAA) Pattern

```typescript
it('increments counter', () => {
  // Arrange: Setup test data and dependencies
  const counter = createCounter(5);

  // Act: Execute the behavior being tested
  counter.increment();

  // Assert: Verify the outcome
  expect(counter.value).toBe(6);
});
```

---

### 2. Descriptive Test Names

**Bad**:
```typescript
it('works', () => { ... });
it('test1', () => { ... });
```

**Good**:
```typescript
it('returns 404 when user not found', () => { ... });
it('validates email format before saving', () => { ... });
```

---

### 3. One Assertion Per Test (Generally)

**Good**:
```typescript
it('adds two numbers', () => {
  expect(add(2, 3)).toBe(5);
});

it('handles negative numbers', () => {
  expect(add(-2, 3)).toBe(1);
});
```

**Exception**: Related assertions are acceptable.
```typescript
it('creates user with all fields', () => {
  const user = createUser(userData);
  expect(user.name).toBe('Alice');
  expect(user.email).toBe('alice@example.com');
  expect(user.role).toBe('developer');
});
```

---

### 4. Test Edge Cases

**Checklist**:
- [ ] Zero and negative values
- [ ] Empty strings and arrays
- [ ] Null and undefined
- [ ] Boundary values (min/max)
- [ ] Very large values
- [ ] Invalid input

---

### 5. Keep Tests DRY (But Not Too DRY)

**Balance**:
- Extract common setup into beforeEach
- Use helper functions for repeated logic
- But: keep test bodies readable and explicit

**Example**:
```typescript
describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService(mockDb);
  });

  it('creates user', () => {
    const result = service.create(userData);
    expect(result).toMatchObject(userData);
  });
});
```

---

## TDD Workflow Summary

```
1. ❌ RED: Write failing test
   - Think about what you want to build
   - Write test for next small piece
   - Run test, watch it fail

2. ✅ GREEN: Make test pass
   - Write simplest code possible
   - Get test to pass quickly
   - Don't worry about quality yet

3. 🔄 REFACTOR: Improve code
   - Clean up code
   - Remove duplication
   - Improve names
   - Tests still pass!

4. 🔄 REPEAT: Next feature
   - Return to step 1
   - Continue until feature complete
```

---

**TDD Result**: High-quality code with comprehensive test coverage, built incrementally with confidence.
