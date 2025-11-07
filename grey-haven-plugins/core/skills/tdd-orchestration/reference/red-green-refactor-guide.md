# Red-Green-Refactor Guide

Comprehensive guide to the core TDD cycle - write failing test, implement minimally, refactor with confidence.

## The Three Phases

### Overview

```
┌──────────────────────────────────────────────────────────┐
│                    TDD Cycle                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. 🔴 RED Phase: Write Failing Test                    │
│     │                                                    │
│     ├─ Write test for next small behavior              │
│     ├─ Run test → verify it FAILS                      │
│     └─ Validate test quality                            │
│                                                          │
│  2. 🟢 GREEN Phase: Make Test Pass                      │
│     │                                                    │
│     ├─ Write MINIMAL code to pass test                 │
│     ├─ Run test → verify it PASSES                     │
│     └─ Resist over-engineering                          │
│                                                          │
│  3. 🔵 REFACTOR Phase: Improve Design                   │
│     │                                                    │
│     ├─ Improve code quality                            │
│     ├─ Apply SOLID principles                           │
│     ├─ Remove duplication                               │
│     └─ Run ALL tests → verify behavior preserved       │
│                                                          │
│  4. ↻ REPEAT: Next behavior                             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 1: 🔴 RED (Write Failing Test)

### Purpose

Write a test that **defines behavior** for code that doesn't exist yet.

### Duration

**Target**: 3-10 minutes
- Simple test: 3-5 minutes
- Complex test: 5-10 minutes
- > 10 minutes: Test too complex, break it down

### Steps

#### 1. Identify Next Behavior

**Ask**: What's the smallest next behavior to implement?

```python
# Example: User authentication
# Behaviors to implement:
# 1. Login with valid credentials → returns user ✅ Start here!
# 2. Login with invalid password → returns None
# 3. Login with non-existent email → returns None
# 4. Login rate limiting
# 5. Password reset
```

**Pick ONE behavior** - the simplest one.

#### 2. Write Test

**Follow AAA Pattern**:
- **Arrange**: Setup test data
- **Act**: Execute behavior
- **Assert**: Verify result

```python
# tests/test_auth.py
def test_login_with_valid_credentials():
    """Should return user when credentials are valid."""
    # Arrange
    user = create_test_user(email="john@example.com", password="secret123")

    # Act
    result = login(email="john@example.com", password="secret123")

    # Assert
    assert result is not None
    assert result.email == "john@example.com"
    assert result.authenticated is True
```

#### 3. Run Test

```bash
$ pytest tests/test_auth.py::test_login_with_valid_credentials

FAILED tests/test_auth.py::test_login_with_valid_credentials
ImportError: cannot import name 'login' from 'app.auth'
```

**✅ Good RED**: Test fails because code doesn't exist.

**❌ Bad RED**: Test passes immediately (test is broken or code already exists).

#### 4. Validate Test Quality

**Quality Checklist**:
- ✅ Test name describes behavior (`test_login_with_valid_credentials`)
- ✅ Single behavior tested (login with valid credentials)
- ✅ Clear assertions (checks specific values)
- ✅ Follows AAA pattern
- ✅ Fails for right reason (code doesn't exist)
- ✅ Independent (doesn't depend on other tests)
- ✅ Fast (runs in milliseconds)

### Common RED Phase Mistakes

#### Mistake #1: Test Too Complex

```python
# ❌ Bad - Tests multiple behaviors
def test_user_authentication_flow():
    # Tests login, logout, session, password reset, rate limiting...
    # Too much!
```

**Fix**: One behavior per test.

#### Mistake #2: Weak Assertions

```python
# ❌ Bad - Vague assertions
def test_login():
    result = login("email", "password")
    assert result is not None  # Too weak!
    assert result  # Even weaker!
```

**Fix**: Specific assertions.

```python
# ✅ Good - Specific assertions
def test_login_with_valid_credentials():
    result = login("john@example.com", "secret123")
    assert result.email == "john@example.com"
    assert result.authenticated is True
```

#### Mistake #3: Test Passes on First Run

```python
# Test passes without implementation? 🤔
# Possible reasons:
# 1. Implementation already exists
# 2. Test is broken
# 3. Assertions too weak
```

**Fix**: Verify test fails, investigate why it passed.

---

## Phase 2: 🟢 GREEN (Make Test Pass)

### Purpose

Write **minimal** code to make the test pass - nothing more!

### Duration

**Target**: 5-15 minutes
- Simple implementation: 5-8 minutes
- Moderate complexity: 8-12 minutes
- Complex: 12-15 minutes
- > 15 minutes: Implementation too complex, break it down

### Steps

#### 1. Write Minimal Implementation

**Ask**: What's the **simplest** code that makes this test pass?

```python
# app/auth.py
def login(email: str, password: str):
    """Authenticate user."""
    # Minimal implementation - just make test pass!
    user = get_user_by_email(email)
    if user and verify_password(password, user.password_hash):
        user.authenticated = True
        return user
    return None
```

**Resist the urge to add**:
- Error handling for edge cases (add when test demands it)
- Logging (add when test demands it)
- Validation (add when test demands it)
- Optimization (add when test demands it)

#### 2. Run Test

```bash
$ pytest tests/test_auth.py::test_login_with_valid_credentials

PASSED ✅
```

**✅ Good GREEN**: Test passes!

**❌ Bad GREEN**: Test still fails (debug or simplify implementation).

#### 3. Run All Tests

```bash
$ pytest tests/

47 passed in 2.3s ✅
```

**Ensure no regressions** - new code doesn't break existing tests.

### Green Phase Techniques

#### Technique #1: Fake It

**Hardcode** the expected value to make test pass!

```python
# tests/test_discount.py
def test_calculate_discount_10_percent():
    result = calculate_discount(price=100, quantity=10)
    assert result == 90  # 10% discount

# Implementation - FAKE IT!
def calculate_discount(price, quantity):
    return 90  # Hardcoded!
```

**Why?** Forces you to write more tests that break the hardcoding.

```python
# Next test forces generalization
def test_calculate_discount_20_percent():
    result = calculate_discount(price=100, quantity=20)
    assert result == 80  # Now hardcoding breaks!

# Implementation - NOW generalize
def calculate_discount(price, quantity):
    if quantity >= 20:
        return price * 0.8
    elif quantity >= 10:
        return price * 0.9
    return price
```

#### Technique #2: Obvious Implementation

If solution is **obvious and simple**, just implement it.

```python
def test_add_numbers():
    assert add(2, 3) == 5

# Obvious implementation
def add(a, b):
    return a + b
```

#### Technique #3: Triangulation

Write multiple tests to **triangulate** toward general solution.

```python
def test_fibonacci_0():
    assert fibonacci(0) == 0

def test_fibonacci_1():
    assert fibonacci(1) == 1

def test_fibonacci_2():
    assert fibonacci(2) == 1

def test_fibonacci_5():
    assert fibonacci(5) == 5

# Triangulated implementation
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Common GREEN Phase Mistakes

#### Mistake #1: Over-Engineering

```python
# ❌ Bad - Adding features test doesn't need
def login(email, password):
    # Test only checks valid login, but we're adding...
    validate_email_format(email)  # Not tested!
    check_rate_limit(email)        # Not tested!
    log_login_attempt(email)       # Not tested!
    # ... 50 more lines
```

**Fix**: Only implement what test demands.

#### Mistake #2: Premature Optimization

```python
# ❌ Bad - Optimizing before needed
def calculate_total(items):
    # Using complex caching strategy for 5-item list...
    cache = LRUCache(maxsize=1000)
    # ... complex optimization
```

**Fix**: Make it work, then optimize (only if test demands it).

#### Mistake #3: Multiple Features

```python
# ❌ Bad - Implementing multiple behaviors at once
def login(email, password):
    # Implementing login, logout, session management all at once!
```

**Fix**: One test, one behavior, one implementation.

---

## Phase 3: 🔵 REFACTOR (Improve Design)

### Purpose

Improve code **design** without changing **behavior**.

### Duration

**Target**: 5-10 minutes
- Minor refactoring: 5 minutes
- Moderate refactoring: 10 minutes
- Major refactoring: Multiple cycles (don't spend >10min per cycle)

### Steps

#### 1. Identify Improvements

**Look for**:
- Code duplication (DRY violation)
- Long functions (>50 lines)
- Deep nesting (>3 levels)
- Complex conditionals
- Poor naming
- Missing abstractions
- SOLID violations

```python
# Before refactoring
def login(email, password):
    user = get_user_by_email(email)
    if not user:
        return None

    # Duplication: Password hashing logic repeated
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if password_hash == user.password_hash:
        user.authenticated = True
        return user

    return None
```

#### 2. Apply Refactoring

**Extract Method**:
```python
# After refactoring
def login(email, password):
    user = get_user_by_email(email)
    if not user:
        return None

    if _verify_password(password, user.password_hash):
        user.authenticated = True
        return user

    return None

def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    return bcrypt.checkpw(password.encode(), stored_hash.encode())
```

**Benefits**:
- ✅ Extracted reusable function
- ✅ Clear intention (`_verify_password`)
- ✅ Testable in isolation
- ✅ Easier to change password hashing strategy

#### 3. Run All Tests

```bash
$ pytest tests/

47 passed in 2.3s ✅
```

**Critical**: Tests must still pass after refactoring!

#### 4. Verify Coverage

```bash
$ pytest --cov=app tests/

Coverage: 87% (maintained) ✅
```

**Ensure coverage doesn't drop** - refactoring shouldn't remove tested code paths.

### Refactoring Patterns

#### Pattern #1: Extract Method

**Before**:
```python
def process_order(order):
    # Calculate total (complex logic)
    total = 0
    for item in order.items:
        total += item.price * item.quantity
        if item.quantity > 10:
            total *= 0.9  # 10% discount

    # Validate address (complex logic)
    if not order.address.street:
        raise ValueError("Street required")
    if not order.address.city:
        raise ValueError("City required")

    # Process payment (complex logic)
    # ... 20 more lines
```

**After**:
```python
def process_order(order):
    total = calculate_order_total(order.items)
    validate_address(order.address)
    process_payment(total, order.payment_method)

def calculate_order_total(items):
    # Extracted calculation logic
    pass

def validate_address(address):
    # Extracted validation logic
    pass
```

#### Pattern #2: Extract Class

**Before**:
```python
class Order:
    def __init__(self):
        # Order has too many responsibilities!
        self.items = []
        self.customer_email = ""
        self.billing_address = ""
        self.shipping_address = ""
        self.payment_card = ""
        self.payment_cvv = ""

    def calculate_total(self): pass
    def validate_payment(self): pass
    def send_confirmation_email(self): pass
```

**After**:
```python
class Order:
    def __init__(self):
        self.items = []
        self.customer = Customer()      # Extracted
        self.payment = Payment()        # Extracted
        self.shipping = Shipping()      # Extracted

class Customer:
    def __init__(self):
        self.email = ""

class Payment:
    def __init__(self):
        self.card_number = ""
        self.cvv = ""

    def validate(self): pass

class Shipping:
    def __init__(self):
        self.address = ""

    def send_confirmation(self): pass
```

#### Pattern #3: Replace Conditional with Polymorphism

**Before**:
```python
def calculate_price(product_type, base_price):
    if product_type == "book":
        return base_price * 0.9  # 10% discount
    elif product_type == "electronics":
        return base_price * 0.95  # 5% discount
    elif product_type == "clothing":
        return base_price * 0.85  # 15% discount
    else:
        return base_price
```

**After**:
```python
class Product:
    def calculate_price(self, base_price):
        return base_price

class Book(Product):
    def calculate_price(self, base_price):
        return base_price * 0.9

class Electronics(Product):
    def calculate_price(self, base_price):
        return base_price * 0.95

class Clothing(Product):
    def calculate_price(self, base_price):
        return base_price * 0.85
```

### Common REFACTOR Phase Mistakes

#### Mistake #1: Changing Behavior

```python
# ❌ Bad - Changed behavior during refactoring
def login(email, password):
    user = get_user_by_email(email)
    if user and verify_password(password, user.password_hash):
        # Added new feature during refactoring!
        log_successful_login(email)  # ❌ New behavior!
        user.authenticated = True
        return user
    return None
```

**Fix**: Refactoring = **same behavior, better design**. Add features in new cycles.

#### Mistake #2: Too Many Changes

```python
# ❌ Bad - Refactoring entire codebase at once
# Renamed 50 functions, extracted 20 classes, moved 100 files...
# Tests break: which change broke it? No idea!
```

**Fix**: Small incremental refactorings, run tests after each.

#### Mistake #3: Skipping Tests

```python
# ❌ Bad - Refactoring without running tests
# "I'm sure this won't break anything..."
# (It breaks everything)
```

**Fix**: Run tests after EVERY refactoring, no exceptions.

---

## TDD Rhythm

### Ideal Cycle Time

```
RED: 3-10 min   →   Write failing test
GREEN: 5-15 min →   Minimal implementation
REFACTOR: 5-10 min → Improve design
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 13-35 min per cycle ✅
```

### Flow State

**Goal**: Enter "flow state" where you're cycling rapidly.

**Indicators of good flow**:
- Completing 3-5 cycles per hour
- Tests always passing
- Small, focused commits
- No long debugging sessions

**Indicators of problems**:
- Stuck in GREEN phase >20 minutes
- Tests failing for >10 minutes
- Large, complex tests
- Skipping REFACTOR phase

### When to Commit

**Commit frequency**: After GREEN or after REFACTOR

```bash
# After GREEN (test passes)
$ git add -A
$ git commit -m "feat: add user login with valid credentials"

# After REFACTOR (design improved)
$ git add -A
$ git commit -m "refactor: extract password verification"
```

**Never commit broken tests** (except for WIP branches).

---

## Quality Gates

### Test Quality Gates

Before moving to GREEN:
- ✅ Test fails for right reason
- ✅ Test name describes behavior
- ✅ Single behavior per test
- ✅ Clear assertions
- ✅ Fast execution (<1s)

### Implementation Quality Gates

Before moving to REFACTOR:
- ✅ Test passes
- ✅ All tests still pass
- ✅ Coverage maintained or increased
- ✅ Minimal implementation (no over-engineering)

### Refactoring Quality Gates

Before moving to next cycle:
- ✅ All tests still pass
- ✅ Coverage maintained
- ✅ Behavior unchanged
- ✅ Design improved

---

## Troubleshooting

### Problem: Can't Think of Next Test

**Solution**: Look at what's NOT tested yet.

```python
# Current tests:
# ✅ Login with valid credentials
# ❓ What's missing?
# - Invalid password
# - Non-existent user
# - Empty email
# - Empty password
# - Rate limiting

# Pick the simplest missing behavior
```

### Problem: Test Won't Pass

**Solutions**:
1. Simplify implementation (hardcode if needed)
2. Debug incrementally (add print statements)
3. Write smaller test
4. Pair program

### Problem: Tests Break During Refactoring

**Solutions**:
1. Revert immediately (`git checkout`)
2. Smaller refactoring steps
3. Run tests after each change
4. Use IDE refactoring tools

---

Related: [TDD Methodologies](tdd-methodologies.md) | [Coverage Thresholds](coverage-thresholds.md) | [Refactoring Patterns](refactoring-patterns.md) | [Return to INDEX](INDEX.md)
