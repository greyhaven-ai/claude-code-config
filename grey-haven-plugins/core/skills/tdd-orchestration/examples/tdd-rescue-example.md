# TDD Rescue Example: Recovery Protocols

How to recover from common TDD failures and anti-patterns - 3 real scenarios with step-by-step recovery.

## Scenario 1: RED Phase Failure (Test Passes Unexpectedly)

### The Problem

You write a test expecting it to fail, but it passes immediately!

```python
# tests/test_payment.py
def test_process_payment_with_insufficient_funds():
    """Should raise InsufficientFundsError when balance < amount."""
    # Arrange
    account = Account(balance=50.00)

    # Act & Assert
    with pytest.raises(InsufficientFundsError):
        process_payment(account, amount=100.00)
```

### Run Test (Expected: RED)

```bash
$ pytest tests/test_payment.py::test_process_payment_with_insufficient_funds

PASSED ✅  # Wait, what? This should FAIL!
```

**🚨 RED Phase Failure**: Test passed without implementation!

---

### Recovery Protocol: RED Phase Failure

#### Step 1: Identify Why Test Passed

**Possibility #1**: Implementation already exists

```python
# app/payment.py - Check if function exists
def process_payment(account, amount):
    # Oh no, someone already implemented this!
    if account.balance < amount:
        raise InsufficientFundsError("Insufficient funds")
    account.balance -= amount
```

**Resolution**: If implementation exists and is correct, test is still valuable (validates behavior). **Move to next test.**

**Possibility #2**: Test is too weak

```python
# The test might be catching a different exception!
def process_payment(account, amount):
    raise ValueError("Generic error")  # Wrong exception type!

# But pytest.raises() might catch ANY exception
# making test pass incorrectly
```

**Resolution**: Strengthen test to check specific exception.

**Possibility #3**: Test setup is wrong

```python
# Maybe InsufficientFundsError is imported incorrectly?
from app.exceptions import PaymentError  # Wrong import!
```

**Resolution**: Fix imports and test setup.

#### Step 2: Fix The Test

**Make test fail correctly**:

```python
def test_process_payment_with_insufficient_funds():
    """Should raise InsufficientFundsError when balance < amount."""
    account = Account(balance=50.00)

    with pytest.raises(InsufficientFundsError) as exc_info:
        process_payment(account, amount=100.00)

    # Verify exception message
    assert "Insufficient funds" in str(exc_info.value)
    assert account.balance == 50.00  # Balance unchanged
```

#### Step 3: Temporarily Break Implementation

```python
# app/payment.py - Comment out check
def process_payment(account, amount):
    # if account.balance < amount:
    #     raise InsufficientFundsError("Insufficient funds")
    account.balance -= amount  # Will allow negative balance!
```

#### Step 4: Verify Test Now Fails

```bash
$ pytest tests/test_payment.py::test_process_payment_with_insufficient_funds

FAILED ✅  # Good! Test catches the bug!

AssertionError: DID NOT RAISE InsufficientFundsError
```

#### Step 5: Restore Implementation

```python
# app/payment.py - Restore
def process_payment(account, amount):
    if account.balance < amount:
        raise InsufficientFundsError("Insufficient funds")
    account.balance -= amount
```

#### Step 6: Verify GREEN

```bash
$ pytest tests/test_payment.py::test_process_payment_with_insufficient_funds

PASSED ✅  # Test works correctly!
```

**✅ RED Phase Recovered**: Test now fails when it should, passes when it should.

---

## Scenario 2: GREEN Phase Failure (Test Won't Pass)

### The Problem

You've written a test (RED ✅), implemented the feature, but test still fails!

```python
# tests/test_cart.py
def test_add_item_to_cart():
    """Should add item to cart and update quantity."""
    cart = ShoppingCart()
    cart.add_item(product_id="prod-123", quantity=2)

    assert len(cart.items) == 1
    assert cart.items[0]["product_id"] == "prod-123"
    assert cart.items[0]["quantity"] == 2
    assert cart.total_items == 2
```

```python
# app/cart.py - Implementation
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id, quantity):
        self.items.append({
            "product_id": product_id,
            "quantity": quantity,
        })
        self.total_items = quantity  # Bug here!
```

### Run Test

```bash
$ pytest tests/test_cart.py::test_add_item_to_cart

FAILED 🔴

AssertionError: assert 1 == 2
  Expected total_items: 2
  Actual total_items: 1
```

**🚨 GREEN Phase Failure**: Implementation doesn't pass test!

---

### Recovery Protocol: GREEN Phase Failure

#### Option A: Debug the Implementation

**Step 1: Add Debugging Output**

```python
class ShoppingCart:
    def add_item(self, product_id, quantity):
        print(f"Adding {quantity} of {product_id}")  # Debug
        self.items.append({
            "product_id": product_id,
            "quantity": quantity,
        })
        print(f"Items: {self.items}")  # Debug
        self.total_items = quantity
        print(f"Total items: {self.total_items}")  # Debug
```

**Step 2: Run Test Again**

```bash
$ pytest tests/test_cart.py::test_add_item_to_cart -s

Adding 2 of prod-123
Items: [{'product_id': 'prod-123', 'quantity': 2}]
Total items: 2

FAILED 🔴
```

**Aha!** `total_items` is set to `quantity` directly, but test expects it to be 2.

Wait... test expects 2, `total_items` is 2, but test fails?

**Step 3: Check Test Again**

```python
# Hmm, assertion is checking len(cart.items) == 1 first
assert len(cart.items) == 1  # ✅ Passes
assert cart.items[0]["product_id"] == "prod-123"  # ✅ Passes
assert cart.items[0]["quantity"] == 2  # ✅ Passes
assert cart.total_items == 2  # 🔴 FAILS!
```

**Wait, what?!** Let me re-run...

```bash
$ pytest tests/test_cart.py::test_add_item_to_cart -vv

tests/test_cart.py::test_add_item_to_cart FAILED

>   assert cart.total_items == 2
E   AttributeError: 'ShoppingCart' object has no attribute 'total_items'
```

**Aha!** `total_items` attribute doesn't exist at initialization!

#### Step 4: Fix Implementation

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total_items = 0  # Initialize!

    def add_item(self, product_id, quantity):
        self.items.append({
            "product_id": product_id,
            "quantity": quantity,
        })
        self.total_items += quantity  # Add to existing total
```

#### Step 5: Verify GREEN

```bash
$ pytest tests/test_cart.py::test_add_item_to_cart

PASSED ✅
```

**✅ GREEN Phase Recovered**: Incremental debugging found the issue!

---

#### Option B: Simplify Implementation

If debugging doesn't work, try **simplest possible implementation**:

```python
# Fake it till you make it!
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total_items = 0

    def add_item(self, product_id, quantity):
        # Hardcode to make test pass
        self.items.append({
            "product_id": "prod-123",  # Hardcoded!
            "quantity": 2,             # Hardcoded!
        })
        self.total_items = 2  # Hardcoded!
```

```bash
$ pytest tests/test_cart.py::test_add_item_to_cart

PASSED ✅  # Now write more tests to force generalization!
```

Then write another test that breaks the hardcoding:

```python
def test_add_different_product():
    """Force implementation to use parameters."""
    cart = ShoppingCart()
    cart.add_item(product_id="prod-999", quantity=5)

    assert cart.items[0]["product_id"] == "prod-999"
    assert cart.items[0]["quantity"] == 5
```

This forces you to remove hardcoding!

---

## Scenario 3: REFACTOR Phase Failure (Tests Break)

### The Problem

All tests pass, you refactor code, tests break!

```python
# app/order.py - Before refactoring
def calculate_order_total(items):
    """Calculate total with tax."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * 0.08  # 8% tax
    return subtotal + tax
```

**Tests passing**: ✅ 15/15

**Refactor**: Extract tax calculation

```python
# app/order.py - After refactoring
def calculate_order_total(items):
    """Calculate total with tax."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = calculate_tax(subtotal)
    return subtotal + tax

def calculate_tax(amount):
    """Calculate tax amount."""
    TAX_RATE = 0.08
    return amount * TAX_RATE
```

### Run Tests

```bash
$ pytest tests/test_order.py

FAILED tests/test_order.py::test_calculate_order_total  🔴
FAILED tests/test_order.py::test_order_with_discount  🔴

13 passed, 2 failed
```

**🚨 REFACTOR Phase Failure**: Refactoring broke tests!

---

### Recovery Protocol: REFACTOR Phase Failure

#### Step 1: Revert Refactoring

```bash
$ git diff app/order.py
# Review changes

$ git checkout app/order.py
# Revert to last working version
```

#### Step 2: Verify Tests Pass Again

```bash
$ pytest tests/test_order.py

PASSED ✅ All 15 tests passing
```

**✅ Back to stable state**

#### Step 3: Refactor in Smaller Steps

**Baby Step #1**: Extract constant only

```python
def calculate_order_total(items):
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    TAX_RATE = 0.08  # Extract constant
    tax = subtotal * TAX_RATE
    return subtotal + tax
```

```bash
$ pytest tests/test_order.py

PASSED ✅ All 15 tests passing
```

**Baby Step #2**: Extract to module-level constant

```python
# app/order.py
TAX_RATE = 0.08  # Module level

def calculate_order_total(items):
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * TAX_RATE
    return subtotal + tax
```

```bash
$ pytest tests/test_order.py

PASSED ✅ All 15 tests passing
```

**Baby Step #3**: Extract tax calculation function

```python
TAX_RATE = 0.08

def calculate_tax(amount):
    """Calculate tax amount."""
    return amount * TAX_RATE

def calculate_order_total(items):
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = calculate_tax(subtotal)
    return subtotal + tax
```

```bash
$ pytest tests/test_order.py

PASSED ✅ All 15 tests passing
```

**✅ REFACTOR Phase Recovered**: Smaller steps succeeded!

#### Step 4: Why Did Original Refactoring Fail?

**Investigate failing tests**:

```python
# tests/test_order.py
def test_calculate_order_total():
    items = [{"price": 100, "quantity": 2}]

    result = calculate_order_total(items)

    # Test was hardcoded to OLD implementation!
    assert result == 216.0  # Assumed specific tax calculation

# But new implementation uses different rounding!
def calculate_tax(amount):
    return round(amount * TAX_RATE, 2)  # Added rounding!
```

**Resolution**: Update test to be less brittle

```python
def test_calculate_order_total():
    items = [{"price": 100, "quantity": 2}]

    result = calculate_order_total(items)

    # Don't hardcode expected value, calculate it!
    subtotal = 200
    expected_tax = subtotal * 0.08
    expected_total = subtotal + expected_tax

    assert result == expected_total  # More flexible!
```

---

## Scenario 4: Anti-Pattern Recovery (Test-After Development)

### The Problem

Developer writes entire feature, THEN writes tests.

```python
# Someone wrote 500 lines of code without tests!
class OrderProcessor:
    def process_order(self, order_data):
        # 200 lines of complex logic
        pass

    def validate_order(self, order):
        # 150 lines of validation
        pass

    def calculate_pricing(self, items):
        # 150 lines of pricing logic
        pass
```

**Tests**: 0
**Coverage**: 0%
**Defects**: Unknown
**Maintainability**: Low

---

### Recovery Protocol: Retroactive TDD

#### Step 1: Characterization Tests

**Write tests that describe CURRENT behavior**:

```python
# tests/test_order_processor_characterization.py
"""
Characterization tests - describe what code DOES,
not what it SHOULD do.
"""

def test_process_order_with_valid_data():
    """Capture current behavior."""
    processor = OrderProcessor()
    order_data = {"items": [{"id": 1, "price": 10}]}

    result = processor.process_order(order_data)

    # Whatever result is, that's the "correct" behavior for now
    assert result["status"] == "processed"  # Capture actual output
    assert result["total"] == 10
```

Run test, see what happens, then **update assertions to match actual output**.

#### Step 2: Identify Seams

**Find logical boundaries** to inject tests:

```python
class OrderProcessor:
    def process_order(self, order_data):
        # SEAM: Validation
        validation_result = self.validate_order(order_data)
        if not validation_result.valid:
            return {"status": "invalid"}

        # SEAM: Pricing
        pricing = self.calculate_pricing(order_data["items"])

        # SEAM: Payment
        payment = self.process_payment(pricing["total"])

        return {"status": "processed", "total": pricing["total"]}
```

#### Step 3: Test Seams Individually

```python
def test_validate_order_with_empty_items():
    """Test validation seam."""
    processor = OrderProcessor()

    result = processor.validate_order({"items": []})

    assert result.valid is False
    assert "items cannot be empty" in result.errors

def test_calculate_pricing_applies_discount():
    """Test pricing seam."""
    processor = OrderProcessor()

    result = processor.calculate_pricing([
        {"price": 100, "quantity": 10}  # Bulk discount
    ])

    assert result["subtotal"] == 1000
    assert result["discount"] == 100  # 10% bulk discount
    assert result["total"] == 900
```

#### Step 4: Refactor with Confidence

Now that you have tests, refactor safely:

```python
class OrderProcessor:
    def __init__(self, validator, pricer, payment_gateway):
        # Inject dependencies for better testing
        self.validator = validator
        self.pricer = pricer
        self.payment_gateway = payment_gateway

    def process_order(self, order_data):
        # Simplified with dependency injection
        validation = self.validator.validate(order_data)
        if not validation.valid:
            return {"status": "invalid"}

        pricing = self.pricer.calculate(order_data["items"])
        payment = self.payment_gateway.process(pricing["total"])

        return {"status": "processed", "total": pricing["total"]}
```

**✅ Anti-Pattern Recovered**: Code now has tests and better structure!

---

## Key Lessons

### RED Phase Failures

**Problem**: Test passes when it should fail
**Solution**: Temporarily break implementation, verify test fails, restore

### GREEN Phase Failures

**Problem**: Can't make test pass
**Solutions**:
1. Debug incrementally
2. Simplify implementation (hardcode if needed)
3. Pair program
4. Write smaller test

### REFACTOR Phase Failures

**Problem**: Tests break during refactoring
**Solutions**:
1. Revert immediately
2. Refactor in smaller steps
3. Run tests after each change
4. Update brittle tests

### Anti-Pattern Recovery

**Problem**: Code without tests (test-after)
**Solutions**:
1. Characterization tests (capture current behavior)
2. Test seams individually
3. Refactor with test coverage

---

## Prevention

### Prevent RED Phase Failures

```python
# Always verify test fails BEFORE implementing
$ pytest tests/test_new_feature.py
FAILED ✅  # Good!

# Then implement
# Then verify it passes
```

### Prevent GREEN Phase Failures

- **Start simple**: Hardcode if needed, generalize later
- **Debug incrementally**: Add print statements
- **Pair program**: Fresh eyes help
- **Take breaks**: Frustration clouds judgment

### Prevent REFACTOR Phase Failures

- **Small steps**: Change one thing at a time
- **Run tests frequently**: After every change
- **Version control**: Commit before refactoring
- **Time box**: If stuck after 15min, revert and try different approach

### Prevent Anti-Patterns

- **Team culture**: Test-first is non-negotiable
- **Code reviews**: Reject PRs without tests
- **Metrics**: Track coverage and mutation score
- **Pair programming**: Keep each other honest

---

Related: [Red-Green-Refactor Example](red-green-refactor-example.md) | [Outside-In TDD Example](outside-in-tdd-example.md) | [Mutation Testing Example](mutation-testing-example.md) | [Return to INDEX](INDEX.md)
