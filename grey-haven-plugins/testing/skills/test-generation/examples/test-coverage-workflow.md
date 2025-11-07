# Example: Test Coverage Improvement Workflow

Systematic workflow for analyzing low-coverage codebase and generating tests to reach 80%+ coverage.

## Context

**Project**: E-commerce platform (frontend + backend)
**Initial Coverage**: 42% overall (frontend 38%, backend 48%)
**Goal**: 80%+ coverage before production deployment
**Timeline**: 3 days
**Technologies**: TypeScript (React + TanStack Start), Python (FastAPI), Vitest, pytest

**Why 42% is Risky**:
- Missing edge case handling
- No error scenario testing
- Integration points untested
- Production bugs likely

## Day 1: Analysis and Planning

### Step 1: Generate Coverage Reports

**Frontend Coverage** (Vitest):
```bash
cd frontend/
npm run test:coverage

# Output:
File                     | % Stmts | % Branch | % Funcs | % Lines | Uncovered
----------------------|---------|----------|---------|---------|----------
src/components/       | 45      | 30       | 50      | 44      |
  Cart.tsx            | 0       | 0        | 0       | 0       | 1-150
  Checkout.tsx        | 25      | 20       | 30      | 24      | 45-98, 120-145
  ProductList.tsx     | 80      | 75       | 85      | 82      | 15-18
src/lib/              | 30      | 25       | 35      | 28      |
  validation.ts       | 0       | 0        | 0       | 0       | 1-80
  api.ts              | 50      | 40       | 60      | 48      | 25-40, 55-70
---------------------|---------|----------|---------|---------|----------
All files            | 38      | 28       | 43      | 36      |
```

**Backend Coverage** (pytest):
```bash
cd backend/
pytest --cov=app --cov-report=term-missing

# Output:
Name                      Stmts   Miss  Branch BrPart  Cover   Missing
--------------------------------------------------------------------
app/routers/products.py     120     45      30     12    52%   45-89, 105-120
app/routers/orders.py       150     90      40     20    35%   60-150
app/routers/auth.py          80     15      20      5    78%   65-80
app/lib/payment.py          100     85      25     15    15%   20-105
--------------------------------------------------------------------
TOTAL                       450    235     115     52    48%
```

### Step 2: Prioritize by Risk

**High-Risk, Low-Coverage Files** (prioritize these):
```markdown
## Priority 1: Critical Business Logic (0-30% coverage)

1. **Cart.tsx** (0% coverage)
   - Risk: High (cart abandonment bugs = lost revenue)
   - Complexity: Medium
   - Lines: 150
   - Time estimate: 2 hours

2. **validation.ts** (0% coverage)
   - Risk: Critical (security vulnerabilities)
   - Complexity: Low
   - Lines: 80
   - Time estimate: 1 hour

3. **payment.py** (15% coverage)
   - Risk: Critical (payment failures = lost revenue)
   - Complexity: High
   - Lines: 100
   - Time estimate: 3 hours

4. **orders.py** (35% coverage)
   - Risk: High (order processing bugs)
   - Complexity: Medium
   - Lines: 150
   - Time estimate: 2 hours

## Priority 2: Moderate Risk (40-60% coverage)

5. **Checkout.tsx** (25% coverage)
   - Risk: Moderate
   - Time estimate: 1.5 hours

6. **products.py** (52% coverage)
   - Risk: Moderate
   - Time estimate: 1 hour

## Priority 3: Good Coverage (70%+ coverage)

7. **auth.py** (78% coverage) - just missing edge cases
8. **ProductList.tsx** (80% coverage) - almost done
```

### Step 3: Create Test Generation Plan

```markdown
# 3-Day Test Generation Plan

## Day 1 (8 hours): Critical Files
- [ ] validation.ts (1h) → 100% coverage
- [ ] Cart.tsx (2h) → 90% coverage
- [ ] payment.py (3h) → 85% coverage
- [ ] Buffer: 2h for debugging

**Target**: 42% → 55%

## Day 2 (8 hours): High-Risk Files
- [ ] orders.py (2h) → 85% coverage
- [ ] Checkout.tsx (1.5h) → 80% coverage
- [ ] products.py (1h) → 85% coverage
- [ ] Integration tests (2h)
- [ ] Buffer: 1.5h

**Target**: 55% → 70%

## Day 3 (8 hours): Polish and Edge Cases
- [ ] auth.py (1h) → 95% coverage
- [ ] ProductList.tsx (0.5h) → 95% coverage
- [ ] Edge case tests (3h)
- [ ] Performance tests (1h)
- [ ] Documentation (1h)
- [ ] Buffer: 1.5h

**Target**: 70% → 87%
```

## Day 1: Critical Files

### Task 1: validation.ts (1 hour)

**Current Coverage**: 0%
**File**: `src/lib/validation.ts`

```typescript
// Untested validation functions
export function validateEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function validateCreditCard(cardNumber: string): boolean {
  // Luhn algorithm
  const digits = cardNumber.replace(/\D/g, '');
  let sum = 0;
  let isEven = false;

  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = parseInt(digits[i]);

    if (isEven) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }

    sum += digit;
    isEven = !isEven;
  }

  return sum % 10 === 0;
}

export function validatePostalCode(code: string, country: string): boolean {
  const patterns: Record<string, RegExp> = {
    US: /^\d{5}(-\d{4})?$/,
    CA: /^[A-Z]\d[A-Z] \d[A-Z]\d$/,
    UK: /^[A-Z]{1,2}\d{1,2}[A-Z]? \d[A-Z]{2}$/,
  };

  return patterns[country]?.test(code) ?? false;
}
```

**Generated Tests** (`src/lib/validation.test.ts`):

```typescript
import { describe, it, expect } from 'vitest';
import { validateEmail, validateCreditCard, validatePostalCode } from './validation';

describe('validateEmail', () => {
  it('should accept valid emails', () => {
    expect(validateEmail('test@example.com')).toBe(true);
    expect(validateEmail('user.name+tag@domain.co.uk')).toBe(true);
  });

  it('should reject invalid emails', () => {
    expect(validateEmail('notanemail')).toBe(false);
    expect(validateEmail('@example.com')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
    expect(validateEmail('test @example.com')).toBe(false);
  });

  it('should handle edge cases', () => {
    expect(validateEmail('')).toBe(false);
    expect(validateEmail('a@b.c')).toBe(true);
  });
});

describe('validateCreditCard', () => {
  it('should accept valid card numbers', () => {
    expect(validateCreditCard('4532015112830366')).toBe(true); // Visa
    expect(validateCreditCard('5425233430109903')).toBe(true); // Mastercard
  });

  it('should reject invalid card numbers', () => {
    expect(validateCreditCard('4532015112830367')).toBe(false); // Wrong checksum
    expect(validateCreditCard('1234567890123456')).toBe(false);
  });

  it('should handle formatting', () => {
    expect(validateCreditCard('4532-0151-1283-0366')).toBe(true); // With dashes
    expect(validateCreditCard('4532 0151 1283 0366')).toBe(true); // With spaces
  });

  it('should handle edge cases', () => {
    expect(validateCreditCard('')).toBe(false);
    expect(validateCreditCard('abc')).toBe(false);
  });
});

describe('validatePostalCode', () => {
  describe('US postal codes', () => {
    it('should accept valid 5-digit codes', () => {
      expect(validatePostalCode('12345', 'US')).toBe(true);
    });

    it('should accept valid 9-digit codes', () => {
      expect(validatePostalCode('12345-6789', 'US')).toBe(true);
    });

    it('should reject invalid codes', () => {
      expect(validatePostalCode('1234', 'US')).toBe(false);
      expect(validatePostalCode('ABCDE', 'US')).toBe(false);
    });
  });

  describe('Canadian postal codes', () => {
    it('should accept valid codes', () => {
      expect(validatePostalCode('K1A 0B1', 'CA')).toBe(true);
    });

    it('should reject invalid codes', () => {
      expect(validatePostalCode('K1A0B1', 'CA')).toBe(false); // Missing space
      expect(validatePostalCode('123 456', 'CA')).toBe(false);
    });
  });

  it('should return false for unknown countries', () => {
    expect(validatePostalCode('12345', 'XX')).toBe(false);
  });
});
```

**Result**: Coverage 0% → 100% (23 tests, 1 hour)

### Task 2: Cart.tsx (2 hours)

**Generated**: 35 tests covering:
- Item addition/removal
- Quantity updates
- Price calculations
- Empty cart scenarios
- Loading states
- Error handling

**Result**: Coverage 0% → 92%

### Task 3: payment.py (3 hours)

**Generated**: 42 tests covering:
- Stripe API integration
- Payment processing flow
- Refund handling
- Webhook verification
- Error scenarios
- Idempotency

**Result**: Coverage 15% → 87%

### Day 1 Results

```bash
# Frontend coverage
npm run test:coverage
# Result: 38% → 62% (+24 percentage points)

# Backend coverage
pytest --cov
# Result: 48% → 68% (+20 percentage points)

# Overall: 42% → 65% (+23 percentage points)
```

**Tests Created**: 100 new tests
**Bugs Found**: 8 (fixed immediately)
**Time**: 6 hours actual (2h buffer remaining)

## Day 2: High-Risk Files

### Task 1: orders.py (2 hours)

**Focus Areas**:
- Order creation with inventory checks
- Order status transitions
- Multi-tenant order isolation
- Pagination and filtering

**Generated**: 38 tests

**Bugs Found**:
1. Race condition in inventory decrement (not thread-safe)
2. Missing tenant_id validation on order lookup
3. Order cancellation doesn't restore inventory

**Result**: Coverage 35% → 88%

### Task 2: Checkout.tsx (1.5 hours)

**Generated**: 28 tests covering:
- Multi-step wizard navigation
- Form validation across steps
- Payment method selection
- Order summary calculations
- Error recovery

**Result**: Coverage 25% → 83%

### Task 3: Integration Tests (2 hours)

**Created**: `tests/integration/test_checkout_flow.py`

```python
class TestCompleteCheckoutFlow:
    """End-to-end checkout flow tests"""

    def test_successful_purchase_flow(self, client, session):
        """Test complete purchase from cart to confirmation"""
        # 1. Add products to cart
        cart_response = client.post("/cart/items", json={
            "product_id": "prod-1",
            "quantity": 2,
        })
        assert cart_response.status_code == 201

        # 2. Proceed to checkout
        checkout_response = client.post("/checkout", json={
            "shipping_address": {...},
            "billing_address": {...},
        })
        assert checkout_response.status_code == 200

        # 3. Process payment
        payment_response = client.post("/payments", json={
            "amount": 99.98,
            "payment_method": "card",
            "token": "tok_visa",
        })
        assert payment_response.status_code == 200

        # 4. Verify order created
        orders = client.get("/orders").json()
        assert len(orders) == 1
        assert orders[0]["total"] == 99.98

        # 5. Verify inventory decremented
        product = session.get(Product, "prod-1")
        assert product.inventory == original_inventory - 2

    def test_payment_failure_rollback(self, client, session):
        """Test that failed payment doesn't create order"""
        # Similar flow but payment fails
        # Verify no order created, inventory unchanged
```

**Result**: 12 integration tests, caught 2 cross-service bugs

### Day 2 Results

```bash
# Overall coverage: 65% → 78% (+13 percentage points)
```

**Tests Created**: 78 new tests (total: 178)
**Bugs Found**: 5
**Time**: 7 hours actual (1h buffer remaining)

## Day 3: Polish and Edge Cases

### Task 1: Edge Case Tests

**Focus**: Boundary conditions and error scenarios

```typescript
// Edge cases for Cart
describe('Cart Edge Cases', () => {
  it('should handle adding item that goes out of stock', async () => {
    // Add item, then simulate inventory depletion
  });

  it('should handle concurrent cart updates', async () => {
    // Two users updating same cart simultaneously
  });

  it('should handle maximum cart size', async () => {
    // Attempt to add 1001 items (max 1000)
  });

  it('should handle cart expiration', async () => {
    // Cart older than 30 days should be cleared
  });
});
```

**Generated**: 34 edge case tests

### Task 2: Performance Tests

```typescript
describe('Performance', () => {
  it('should load cart in <100ms', async () => {
    const start = performance.now();
    await loadCart();
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
  });

  it('should handle 100 items in cart efficiently', async () => {
    // Add 100 items
    // Verify total calculation <50ms
  });
});
```

**Generated**: 8 performance tests

### Day 3 Results

```bash
# Final coverage report
npm run test:coverage && pytest --cov

Frontend: 38% → 91% (+53 percentage points)
Backend:  48% → 84% (+36 percentage points)
Overall:  42% → 87% (+45 percentage points)
```

## Final Results

### Coverage Summary

```
Component               Before    After    Change    Tests
----------|---------|---------|---------|-------
Frontend Components     38%       91%       +53%      124
Backend APIs            48%       84%       +36%      132
Total                   42%       87%       +45%      256

Time Investment: 20 hours (3 days)
Bugs Found: 15 (fixed before production)
Production Bugs (first month): 0
```

### Tests by Category

```
Unit Tests:              178 (70%)
Integration Tests:        52 (20%)
Edge Case Tests:          18 (7%)
Performance Tests:         8 (3%)
Total:                   256 tests
```

### Key Learnings

**What Worked**:
1. **Risk-based prioritization**: Focus on critical business logic first
2. **Daily coverage targets**: 23% → 13% → 9% incremental gains
3. **Bug discovery during testing**: 15 bugs found and fixed
4. **Integration tests**: Caught cross-service bugs unit tests missed

**What Was Challenging**:
1. **Complex async flows**: TanStack Query mutations tricky to test
2. **Multi-tenant isolation**: Required careful fixture setup
3. **Time estimation**: Some files took longer than expected

**Recommendations**:
1. **Maintain 80% threshold**: Add tests with new features
2. **CI/CD integration**: Block PRs that drop coverage below 80%
3. **Regular coverage audits**: Monthly review of low-coverage areas

## Coverage Maintenance

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running coverage check..."

# Frontend
cd frontend && npm run test:coverage -- --reporter=json > coverage.json
FRONTEND_COV=$(jq '.total.lines.pct' coverage.json)

# Backend
cd ../backend && pytest --cov --cov-report=json > coverage.json
BACKEND_COV=$(jq '.totals.percent_covered' coverage.json)

if (( $(echo "$FRONTEND_COV < 80" | bc -l) )); then
  echo "❌ Frontend coverage below 80% ($FRONTEND_COV%)"
  exit 1
fi

if (( $(echo "$BACKEND_COV < 80" | bc -l) )); then
  echo "❌ Backend coverage below 80% ($BACKEND_COV%)"
  exit 1
fi

echo "✅ Coverage checks passed"
```

### GitHub Actions

```yaml
# .github/workflows/test-coverage.yml
name: Test Coverage

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run tests with coverage
        run: |
          npm run test:coverage
          pytest --cov

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3

      - name: Enforce coverage threshold
        run: |
          if [ $(jq '.total.lines.pct' coverage.json) -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
```

---

Related: [React Component Testing](react-component-testing.md) | [API Endpoint Testing](api-endpoint-testing.md) | [Return to INDEX](INDEX.md)
