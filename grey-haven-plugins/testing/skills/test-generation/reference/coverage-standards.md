# Coverage Standards

What different coverage percentages mean, when to aim for different levels, and how to interpret coverage reports.

## The 80% Rule

**Grey Haven Standard**: 80% minimum coverage for production code

**Why 80%**:
- Catches most critical bugs
- Balances effort vs value
- Achievable for most teams
- Allows flexibility for edge cases

**Not 100%**:
- Diminishing returns after 80%
- Some code is hard to test (error handlers for impossible states)
- Time better spent on other quality measures

## Coverage Types Explained

### Statement Coverage

**What it measures**: Percentage of code statements executed

```typescript
function validateAge(age: number): boolean {
  if (age < 0) {              // Statement 1
    return false;             // Statement 2
  }
  if (age > 120) {            // Statement 3
    return false;             // Statement 4
  }
  return true;                // Statement 5
}

// Test 1: validateAge(25) → Statements 1, 3, 5 executed (60%)
// Test 2: validateAge(-5) → Statements 1, 2 executed (40%)
// Test 3: validateAge(150) → Statements 1, 3, 4 executed (60%)
// All tests combined: 5/5 statements = 100% statement coverage
```

**Most common metric**, but can be misleading.

### Branch Coverage

**What it measures**: Percentage of decision branches executed

```typescript
function calculateDiscount(price: number, isPremium: boolean): number {
  if (isPremium) {            // Branch point: true/false
    return price * 0.8;       // Branch 1 (true)
  }
  return price;               // Branch 2 (false)
}

// Test 1: calculateDiscount(100, true) → Branch 1 covered
// Test 2: calculateDiscount(100, false) → Branch 2 covered
// Both tests: 100% branch coverage
```

**Better metric** than statement coverage - ensures all decision paths tested.

### Function Coverage

**What it measures**: Percentage of functions called

```typescript
// 3 functions total

function add(a: number, b: number): number {
  return a + b;
}

function subtract(a: number, b: number): number {
  return a - b;
}

function multiply(a: number, b: number): number {
  return a * b;
}

// Test suite calls add() and subtract() but not multiply()
// Function coverage: 2/3 = 66.7%
```

**Quick indicator** of untested code.

### Line Coverage

**What it measures**: Percentage of executable lines run

```typescript
function processUser(user: User): string {
  // Line 1: Variable declaration
  const name = user.name.trim();

  // Line 2: Condition
  if (name.length === 0) {
    // Line 3: Return statement
    return 'Invalid name';
  }

  // Line 4: Return statement
  return `Hello, ${name}`;
}

// Test with valid user: Lines 1, 2, 4 executed (75%)
// Test with empty name: Lines 1, 2, 3 executed (75%)
// Both tests: 4/4 lines = 100% line coverage
```

**Similar to statement coverage**, most commonly reported.

## Coverage Goals by Code Type

### Critical Business Logic: 95-100%

**Examples**:
- Payment processing
- Authentication/authorization
- Data validation
- Security checks
- Financial calculations

```typescript
// Payment processing - MUST have 100% coverage
function processPayment(amount: number, card: Card): PaymentResult {
  // Every path must be tested
  if (amount <= 0) {
    throw new Error('Invalid amount');
  }

  if (!validateCard(card)) {
    throw new Error('Invalid card');
  }

  if (card.balance < amount) {
    return { success: false, reason: 'Insufficient funds' };
  }

  // Charge card...
  return { success: true, transactionId: '...' };
}
```

**Why so high**: Bugs have severe consequences (lost revenue, security breaches).

### Standard Business Logic: 80-90%

**Examples**:
- CRUD operations
- API endpoints
- Data transformations
- Form validation
- State management

```typescript
// User management - target 80-90%
export class UserService {
  async createUser(data: CreateUserInput): Promise<User> {
    // Test happy path + common errors
    const validated = validateUserInput(data);
    const user = await this.db.insert(users).values(validated);
    await this.emailService.sendWelcome(user.email);
    return user;
  }

  async updateUser(id: string, data: UpdateUserInput): Promise<User> {
    // Test happy path + common errors
    const user = await this.getUser(id);
    const updated = await this.db.update(users).set(data).where(eq(users.id, id));
    return updated;
  }

  // OK to skip rare error scenarios
}
```

**Why 80-90%**: Balances thoroughness with development speed.

### Utility Functions: 60-80%

**Examples**:
- String formatting
- Date utilities
- Array helpers
- Configuration parsers

```typescript
// Utility functions - target 60-80%
export function formatPhoneNumber(phone: string): string {
  // Test common formats
  const digits = phone.replace(/\D/g, '');

  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  }

  // OK to skip uncommon international formats
  return phone;
}
```

**Why lower**: Lower risk, often simple logic.

### Generated Code: 0-50%

**Examples**:
- TypeScript type guards
- Drizzle migrations
- Auto-generated API clients
- Build scripts

```typescript
// Generated type guard - OK to skip
export function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj
  );
}
```

**Why skip**: High effort, low value - generated code rarely has bugs.

### Error Handlers: 40-60%

**Examples**:
- Global error handlers
- Fallback UI components
- Crash recovery
- Logging

```typescript
// Error boundary - test main paths, skip exotic errors
export class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Test common errors
    if (error instanceof NetworkError) {
      this.setState({ hasError: true, errorType: 'network' });
    } else if (error instanceof ValidationError) {
      this.setState({ hasError: true, errorType: 'validation' });
    } else {
      // OK to skip rare error types
      this.setState({ hasError: true, errorType: 'unknown' });
    }

    logError(error, errorInfo); // Mock in tests
  }
}
```

**Why lower**: Hard to trigger all error scenarios.

## Interpreting Coverage Reports

### Vitest Coverage Report

```bash
npm run test:coverage

File                     | % Stmts | % Branch | % Funcs | % Lines | Uncovered Lines
-------------------------|---------|----------|---------|---------|------------------
src/components/          | 85.5    | 78.2     | 88.9    | 84.8    |
  UserProfile.tsx        | 95.2    | 90.0     | 100     | 94.7    | 45-48
  Cart.tsx               | 72.4    | 65.5     | 75.0    | 71.8    | 23-35, 67-89
  Checkout.tsx           | 88.6    | 82.1     | 90.0    | 88.2    | 125-130
src/lib/                 | 68.4    | 60.2     | 70.0    | 67.9    |
  validation.ts          | 45.0    | 30.0     | 50.0    | 44.4    | 12-25, 40-55
  api.ts                 | 82.5    | 78.0     | 85.0    | 82.1    | 102-110
-------------------------|---------|----------|---------|---------|------------------
All files                | 76.95   | 69.2     | 79.45   | 76.35   |
```

### Reading the Report

**High Priority** (red flags):
- `validation.ts` (45% coverage) - Critical security code, needs immediate attention
- Branch coverage 60.2% in lib/ - Missing error handling tests

**Medium Priority**:
- `Cart.tsx` (72.4%) - Business logic, should reach 80%
- Lines 23-35, 67-89 uncovered - Likely edge cases

**Good Status**:
- `UserProfile.tsx` (95.2%) - Excellent coverage
- `Checkout.tsx` (88.6%) - Good coverage for complex component

### pytest Coverage Report

```bash
pytest --cov=app --cov-report=term-missing

Name                      Stmts   Miss  Branch  BrPart  Cover   Missing
----------------------------------------------------------------------
app/routers/users.py        120     15      30      5    87%   45-52, 89-95
app/routers/orders.py       150     45      40     12    68%   60-105, 120-140
app/services/payment.py     100     10      25      3    90%   85-95
app/lib/validation.py        80     35      20      8    56%   20-55
----------------------------------------------------------------------
TOTAL                       450     105     115     28    76%
```

### Reading the Report

**Critical Issues**:
- `validation.py` (56%) - Security risk, needs tests immediately
- `orders.py` (68%) - Below 80% threshold, missing error handling

**Good Coverage**:
- `payment.py` (90%) - Critical business logic well-tested
- `users.py` (87%) - Above threshold

**BrPart Column**: Partially covered branches (some paths tested, others not)

## Diminishing Returns Analysis

### Effort vs Value Curve

```
Value
│
│     ╱────────  (Diminishing returns)
│   ╱
│  ╱
│ ╱
│╱
└─────────────────────────> Effort
0%   40%   60%   80%   95%  100%

Coverage Percentage:
0-40%:   🚨 High risk, easy wins
40-60%:  ⚠️  Moderate risk, good ROI
60-80%:  ✅ Low risk, still valuable
80-95%:  🟡 Very low risk, diminishing returns
95-100%: 🔴 Minimal benefit, high effort
```

### Time Investment Example

**File**: `OrderService.ts` (150 lines)

```
Coverage   Time       Tests   Bugs Found   ROI
--------------------------------------------------------
0% → 40%   1 hour     12      5 critical   Excellent
40% → 60%  1.5 hours  18      3 moderate   Very Good
60% → 80%  2 hours    24      2 minor      Good
80% → 90%  3 hours    15      1 minor      Fair
90% → 100% 5 hours    8       0            Poor
--------------------------------------------------------
Total:     12.5 hours 77      11 bugs
```

**Optimal stopping point**: 80-85% coverage (6.5 hours, 57 tests, 10 bugs found)

## Coverage Exceptions

### When to Accept Lower Coverage

**Legitimate reasons**:

1. **Defensive programming**:
```typescript
function processData(data: unknown) {
  if (!data) return; // Safety check

  // TypeScript guarantees data exists here,
  // but defensive check can't be tested easily
  if (typeof data !== 'object') return;

  // Main logic...
}
```

2. **Error recovery for impossible states**:
```typescript
function getStatusColor(status: OrderStatus): string {
  switch (status) {
    case 'pending': return 'yellow';
    case 'completed': return 'green';
    case 'cancelled': return 'red';
    default:
      // TypeScript ensures this never happens,
      // but required for exhaustiveness checking
      return 'gray';
  }
}
```

3. **Platform-specific code**:
```typescript
function saveToClipboard(text: string) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text);
  } else {
    // Fallback for old browsers - hard to test
    const textarea = document.createElement('textarea');
    // ... legacy clipboard code
  }
}
```

### When NOT to Accept Lower Coverage

**Invalid excuses**:

❌ "This code is too complex to test"
- ✅ **Fix**: Refactor into testable units

❌ "I don't have time to write tests"
- ✅ **Fix**: Write tests first (TDD) or write tests immediately after

❌ "This code rarely changes"
- ✅ **Counter**: That's exactly when tests are most valuable (regression prevention)

❌ "The tests would be too slow"
- ✅ **Fix**: Mock external dependencies, use in-memory databases

## Coverage Best Practices

### 1. Track Coverage Trends

```bash
# Store coverage history
npm run test:coverage -- --reporter=json > coverage-$(date +%Y%m%d).json

# Monitor trends
echo "$(date): $(jq '.total.lines.pct' coverage-latest.json)%" >> coverage-history.txt
```

**Goal**: Coverage should never decrease on main branch.

### 2. Enforce Coverage Thresholds

**Vitest config**:
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      threshold: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
    },
  },
});
```

**pytest config**:
```ini
# pytest.ini
[pytest]
addopts = --cov=app --cov-fail-under=80
```

### 3. Coverage in CI/CD

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: npm run test:coverage

- name: Check coverage threshold
  run: |
    COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 80%"
      exit 1
    fi

- name: Upload to Codecov
  uses: codecov/codecov-action@v3
```

### 4. Focus on Meaningful Coverage

```typescript
// ❌ Bad: High coverage, low value
it('should have a name property', () => {
  const user = { name: 'John' };
  expect(user.name).toBeDefined(); // 100% coverage, useless test
});

// ✅ Good: Tests actual behavior
it('should format user name correctly', () => {
  const user = createUser({ firstName: 'John', lastName: 'Doe' });
  expect(user.fullName).toBe('John Doe'); // Tests real functionality
});
```

### 5. Prioritize Untested Critical Code

```bash
# Find files with <80% coverage
npm run test:coverage -- --reporter=json | jq '
  .files[] |
  select(.lines.pct < 80) |
  "\(.path): \(.lines.pct)%"
'

# Output:
# src/lib/validation.ts: 45%        ← Critical, fix first
# src/components/Cart.tsx: 72%      ← Business logic, fix second
# src/utils/formatters.ts: 65%      ← Utilities, fix third
```

## Coverage Anti-Patterns

### 1. Testing Implementation Details

```typescript
// ❌ Bad: Tests implementation, not behavior
it('should call setState', () => {
  const setState = vi.fn();
  // ...
  expect(setState).toHaveBeenCalled(); // Who cares?
});

// ✅ Good: Tests user-visible behavior
it('should display error message when form is invalid', () => {
  render(<Form />);
  fireEvent.submit(screen.getByRole('button'));
  expect(screen.getByText('Email is required')).toBeInTheDocument();
});
```

### 2. 100% Coverage at All Costs

```typescript
// ❌ Bad: Contorting code to reach 100%
export function complexLogic(data: Data) {
  /* istanbul ignore next */  // Coverage directive - code smell!
  if (process.env.NODE_ENV === 'test') {
    return mockResult;
  }

  // Real logic...
}

// ✅ Good: Accept 90% coverage, focus on valuable tests
```

### 3. Coverage Without Assertions

```typescript
// ❌ Bad: Code runs but nothing verified
it('should process order', () => {
  processOrder({ id: '123' });
  // 100% coverage, but no assertions - test proves nothing
});

// ✅ Good: Verify outcomes
it('should process order and update status', () => {
  const order = processOrder({ id: '123' });
  expect(order.status).toBe('completed');
  expect(order.processedAt).toBeDefined();
});
```

## Quick Reference

### Coverage Goals
- **Critical business logic**: 95-100%
- **Standard business logic**: 80-90%
- **Utility functions**: 60-80%
- **Generated code**: 0-50%
- **Error handlers**: 40-60%

### Coverage Types
- **Statement**: Lines executed
- **Branch**: Decision paths taken
- **Function**: Functions called
- **Line**: Executable lines run

### Interpreting Reports
- < 60%: 🚨 High risk
- 60-79%: ⚠️ Needs improvement
- 80-89%: ✅ Good
- 90%+: 🎯 Excellent

### Best Practices
1. Enforce 80% threshold in CI
2. Monitor coverage trends
3. Prioritize critical code
4. Focus on behavior, not implementation
5. Accept diminishing returns after 80-90%

---

Related: [Testing Patterns](testing-patterns.md) | [Mocking Strategies](mocking-strategies.md) | [Test Structure Guide](test-structure-guide.md) | [Return to INDEX](INDEX.md)
