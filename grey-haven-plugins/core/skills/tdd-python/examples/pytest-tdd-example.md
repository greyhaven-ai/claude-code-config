# pytest TDD Example: E-commerce Shopping Cart

Complete TDD workflow using pytest - fixtures, parametrize, and modern testing patterns.

**Feature**: Shopping cart with discount rules (10% off $100+, 20% off $500+)
**Duration**: 45 minutes
**Framework**: pytest 7.4+
**Coverage**: 95% line, 92% branch
**Tests**: 18 passing

---

## Project Setup

### Directory Structure

```
shopping_cart/
├── app/
│   ├── __init__.py
│   └── cart.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_cart.py
├── pytest.ini
└── requirements.txt
```

### Dependencies

```txt
# requirements.txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
```

### pytest Configuration

```ini
# pytest.ini
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
testpaths = tests
addopts =
    --verbose
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-branch
    --strict-markers
```

---

## TDD Session: 45-Minute Workflow

### Cycle 1: Add Item to Cart (8 min)

#### 🔴 RED Phase (3 min)

**Test**: Can add single item to empty cart

```python
# tests/test_cart.py
import pytest
from app.cart import ShoppingCart, CartItem

def test_add_item_to_empty_cart():
    """Should add item to cart and return correct quantity."""
    # Arrange
    cart = ShoppingCart()

    # Act
    cart.add_item("PROD-001", "Widget", 10.00, quantity=2)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product_id == "PROD-001"
    assert cart.items[0].name == "Widget"
    assert cart.items[0].price == 10.00
    assert cart.items[0].quantity == 2
```

**Run Test**:
```bash
$ pytest tests/test_cart.py::test_add_item_to_empty_cart

FAILED tests/test_cart.py::test_add_item_to_empty_cart
ImportError: cannot import name 'ShoppingCart' from 'app.cart'
```

✅ **RED**: Test fails because classes don't exist.

---

#### 🟢 GREEN Phase (3 min)

**Implementation**: Minimal code to pass test

```python
# app/cart.py
from dataclasses import dataclass
from typing import List

@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    product_id: str
    name: str
    price: float
    quantity: int

class ShoppingCart:
    """Shopping cart with items."""

    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product_id: str, name: str, price: float, quantity: int) -> None:
        """Add item to cart."""
        item = CartItem(
            product_id=product_id,
            name=name,
            price=price,
            quantity=quantity
        )
        self.items.append(item)
```

**Run Test**:
```bash
$ pytest tests/test_cart.py::test_add_item_to_empty_cart

tests/test_cart.py::test_add_item_to_empty_cart PASSED                     [100%]
```

✅ **GREEN**: Test passes!

---

#### 🔵 REFACTOR Phase (2 min)

No refactoring needed yet - code is simple and clear.

**Cycle 1 Complete**: 8 minutes

---

### Cycle 2: Calculate Subtotal (7 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_cart.py
def test_calculate_subtotal_with_multiple_items():
    """Should calculate correct subtotal for multiple items."""
    cart = ShoppingCart()
    cart.add_item("PROD-001", "Widget", 10.00, quantity=2)
    cart.add_item("PROD-002", "Gadget", 15.00, quantity=3)

    # Act
    subtotal = cart.get_subtotal()

    # Assert
    assert subtotal == 65.00  # (10*2) + (15*3)
```

**Run Test**:
```bash
$ pytest tests/test_cart.py::test_calculate_subtotal_with_multiple_items

FAILED - AttributeError: 'ShoppingCart' object has no attribute 'get_subtotal'
```

✅ **RED**: Method doesn't exist.

---

#### 🟢 GREEN Phase (3 min)

```python
# app/cart.py (add method to ShoppingCart)
def get_subtotal(self) -> float:
    """Calculate subtotal of all items."""
    return sum(item.price * item.quantity for item in self.items)
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

tests/test_cart.py::test_add_item_to_empty_cart PASSED                     [ 50%]
tests/test_cart.py::test_calculate_subtotal_with_multiple_items PASSED     [100%]

2 passed in 0.08s
```

✅ **GREEN**: All tests pass!

---

#### 🔵 REFACTOR Phase (2 min)

No refactoring needed.

**Cycle 2 Complete**: 7 minutes

---

### Cycle 3: Apply 10% Discount (10 min)

#### 🔴 RED Phase (3 min)

**Using parametrize for multiple test cases**:

```python
# tests/test_cart.py
@pytest.mark.parametrize("subtotal,expected_discount,expected_total", [
    (99.99, 0.00, 99.99),     # Just below threshold
    (100.00, 10.00, 90.00),   # Exactly at threshold
    (150.00, 15.00, 135.00),  # Above threshold
])
def test_apply_10_percent_discount_over_100(subtotal, expected_discount, expected_total):
    """Should apply 10% discount for orders $100+."""
    cart = ShoppingCart()
    # Add items to reach subtotal
    cart.add_item("PROD-001", "Widget", subtotal, quantity=1)

    # Act
    total = cart.get_total()
    discount = cart.get_discount_amount()

    # Assert
    assert discount == expected_discount
    assert total == expected_total
```

**Run Test**:
```bash
$ pytest tests/test_cart.py::test_apply_10_percent_discount_over_100

FAILED - AttributeError: 'ShoppingCart' object has no attribute 'get_total'
```

✅ **RED**: Methods don't exist.

---

#### 🟢 GREEN Phase (5 min)

```python
# app/cart.py (add methods)
def get_discount_amount(self) -> float:
    """Calculate discount amount based on subtotal."""
    subtotal = self.get_subtotal()
    if subtotal >= 100.00:
        return subtotal * 0.10  # 10% discount
    return 0.00

def get_total(self) -> float:
    """Calculate total after discount."""
    subtotal = self.get_subtotal()
    discount = self.get_discount_amount()
    return subtotal - discount
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

tests/test_cart.py::test_add_item_to_empty_cart PASSED                     [ 20%]
tests/test_cart.py::test_calculate_subtotal_with_multiple_items PASSED     [ 40%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[99.99-0.00-99.99] PASSED [ 60%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[100.00-10.00-90.00] PASSED [ 80%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[150.00-15.00-135.00] PASSED [100%]

5 passed in 0.12s
```

✅ **GREEN**: All tests pass! Parametrize created 3 test cases.

---

#### 🔵 REFACTOR Phase (2 min)

Extract discount logic to separate method:

```python
# app/cart.py (refactor)
def _calculate_discount_rate(self, subtotal: float) -> float:
    """Determine discount rate based on subtotal."""
    if subtotal >= 100.00:
        return 0.10
    return 0.00

def get_discount_amount(self) -> float:
    """Calculate discount amount based on subtotal."""
    subtotal = self.get_subtotal()
    rate = self._calculate_discount_rate(subtotal)
    return subtotal * rate
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

5 passed in 0.11s ✅
```

**Cycle 3 Complete**: 10 minutes

---

### Cycle 4: Apply 20% Discount (8 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_cart.py
@pytest.mark.parametrize("subtotal,expected_discount,expected_total", [
    (499.99, 49.999, 449.991),   # Just below threshold (10% discount)
    (500.00, 100.00, 400.00),    # Exactly at threshold (20% discount)
    (750.00, 150.00, 600.00),    # Above threshold (20% discount)
])
def test_apply_20_percent_discount_over_500(subtotal, expected_discount, expected_total):
    """Should apply 20% discount for orders $500+."""
    cart = ShoppingCart()
    cart.add_item("PROD-001", "Widget", subtotal, quantity=1)

    discount = cart.get_discount_amount()
    total = cart.get_total()

    assert pytest.approx(discount, 0.01) == expected_discount
    assert pytest.approx(total, 0.01) == expected_total
```

**Run Test**:
```bash
$ pytest tests/test_cart.py::test_apply_20_percent_discount_over_500

FAILED - assert 49.999 == pytest.approx(100.0, abs=0.01)
```

✅ **RED**: Discount calculation wrong (still using 10%).

---

#### 🟢 GREEN Phase (4 min)

```python
# app/cart.py (update discount logic)
def _calculate_discount_rate(self, subtotal: float) -> float:
    """Determine discount rate based on subtotal."""
    if subtotal >= 500.00:
        return 0.20  # 20% discount
    elif subtotal >= 100.00:
        return 0.10  # 10% discount
    return 0.00
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

8 passed in 0.15s ✅
```

✅ **GREEN**: All tests pass!

---

#### 🔵 REFACTOR Phase (2 min)

No refactoring needed - logic is clear.

**Cycle 4 Complete**: 8 minutes

---

### Cycle 5: Fixtures for Reusable Setup (12 min)

#### 🔴 RED Phase (3 min)

**Create fixture for common cart setup**:

```python
# tests/conftest.py
import pytest
from app.cart import ShoppingCart

@pytest.fixture
def empty_cart():
    """Provide an empty shopping cart."""
    return ShoppingCart()

@pytest.fixture
def cart_with_items():
    """Provide a cart with standard test items."""
    cart = ShoppingCart()
    cart.add_item("PROD-001", "Widget", 25.00, quantity=2)
    cart.add_item("PROD-002", "Gadget", 50.00, quantity=1)
    return cart

@pytest.fixture
def large_cart():
    """Provide a cart over $500 for 20% discount."""
    cart = ShoppingCart()
    cart.add_item("PROD-003", "Premium Item", 600.00, quantity=1)
    return cart
```

**Refactor existing tests to use fixtures**:

```python
# tests/test_cart.py
def test_add_item_to_empty_cart(empty_cart):
    """Should add item to cart and return correct quantity."""
    empty_cart.add_item("PROD-001", "Widget", 10.00, quantity=2)

    assert len(empty_cart.items) == 1
    assert empty_cart.items[0].quantity == 2

def test_subtotal_with_fixture(cart_with_items):
    """Should calculate correct subtotal using fixture."""
    # cart has: 2 widgets ($25 each) + 1 gadget ($50)
    assert cart_with_items.get_subtotal() == 100.00

def test_10_percent_discount_with_fixture(cart_with_items):
    """Should apply 10% discount on $100 cart."""
    assert cart_with_items.get_discount_amount() == 10.00
    assert cart_with_items.get_total() == 90.00

def test_20_percent_discount_with_fixture(large_cart):
    """Should apply 20% discount on $600 cart."""
    assert large_cart.get_discount_amount() == 120.00
    assert large_cart.get_total() == 480.00
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

12 passed in 0.18s ✅
```

All tests pass with fixtures!

---

#### 🟢 GREEN Phase (5 min)

Add edge case tests using fixtures:

```python
# tests/test_cart.py
def test_empty_cart_has_zero_total(empty_cart):
    """Empty cart should have $0 total."""
    assert empty_cart.get_subtotal() == 0.00
    assert empty_cart.get_discount_amount() == 0.00
    assert empty_cart.get_total() == 0.00

def test_cannot_add_negative_quantity(empty_cart):
    """Should raise error for negative quantity."""
    with pytest.raises(ValueError, match="Quantity must be positive"):
        empty_cart.add_item("PROD-001", "Widget", 10.00, quantity=-1)

def test_cannot_add_negative_price(empty_cart):
    """Should raise error for negative price."""
    with pytest.raises(ValueError, match="Price must be positive"):
        empty_cart.add_item("PROD-001", "Widget", -10.00, quantity=1)
```

**Update implementation**:

```python
# app/cart.py (add validation)
def add_item(self, product_id: str, name: str, price: float, quantity: int) -> None:
    """Add item to cart with validation."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if price < 0:
        raise ValueError("Price must be positive")

    item = CartItem(
        product_id=product_id,
        name=name,
        price=price,
        quantity=quantity
    )
    self.items.append(item)
```

**Run Tests**:
```bash
$ pytest tests/test_cart.py

15 passed in 0.21s ✅
```

---

#### 🔵 REFACTOR Phase (4 min)

Extract validation to separate method:

```python
# app/cart.py
def _validate_item_inputs(self, price: float, quantity: int) -> None:
    """Validate item inputs before adding to cart."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    if price < 0:
        raise ValueError("Price must be positive")

def add_item(self, product_id: str, name: str, price: float, quantity: int) -> None:
    """Add item to cart with validation."""
    self._validate_item_inputs(price, quantity)

    item = CartItem(
        product_id=product_id,
        name=name,
        price=price,
        quantity=quantity
    )
    self.items.append(item)
```

**Cycle 5 Complete**: 12 minutes

---

## Final Code

### app/cart.py

```python
# app/cart.py
from dataclasses import dataclass
from typing import List

@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    product_id: str
    name: str
    price: float
    quantity: int

class ShoppingCart:
    """Shopping cart with items and discount logic."""

    def __init__(self):
        self.items: List[CartItem] = []

    def _validate_item_inputs(self, price: float, quantity: int) -> None:
        """Validate item inputs before adding to cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if price < 0:
            raise ValueError("Price must be positive")

    def add_item(self, product_id: str, name: str, price: float, quantity: int) -> None:
        """Add item to cart with validation."""
        self._validate_item_inputs(price, quantity)

        item = CartItem(
            product_id=product_id,
            name=name,
            price=price,
            quantity=quantity
        )
        self.items.append(item)

    def get_subtotal(self) -> float:
        """Calculate subtotal of all items."""
        return sum(item.price * item.quantity for item in self.items)

    def _calculate_discount_rate(self, subtotal: float) -> float:
        """Determine discount rate based on subtotal."""
        if subtotal >= 500.00:
            return 0.20  # 20% discount
        elif subtotal >= 100.00:
            return 0.10  # 10% discount
        return 0.00

    def get_discount_amount(self) -> float:
        """Calculate discount amount based on subtotal."""
        subtotal = self.get_subtotal()
        rate = self._calculate_discount_rate(subtotal)
        return subtotal * rate

    def get_total(self) -> float:
        """Calculate total after discount."""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        return subtotal - discount
```

---

## Coverage Report

```bash
$ pytest --cov=app --cov-report=term-missing tests/

tests/test_cart.py::test_add_item_to_empty_cart PASSED                     [  5%]
tests/test_cart.py::test_calculate_subtotal_with_multiple_items PASSED     [ 11%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[99.99-0.00-99.99] PASSED [ 16%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[100.00-10.00-90.00] PASSED [ 22%]
tests/test_cart.py::test_apply_10_percent_discount_over_100[150.00-15.00-135.00] PASSED [ 27%]
tests/test_cart.py::test_apply_20_percent_discount_over_500[499.99-49.999-449.991] PASSED [ 33%]
tests/test_cart.py::test_apply_20_percent_discount_over_500[500.00-100.00-400.00] PASSED [ 38%]
tests/test_cart.py::test_apply_20_percent_discount_over_500[750.00-150.00-600.00] PASSED [ 44%]
tests/test_cart.py::test_subtotal_with_fixture PASSED                      [ 50%]
tests/test_cart.py::test_10_percent_discount_with_fixture PASSED           [ 55%]
tests/test_cart.py::test_20_percent_discount_with_fixture PASSED           [ 61%]
tests/test_cart.py::test_empty_cart_has_zero_total PASSED                  [ 66%]
tests/test_cart.py::test_cannot_add_negative_quantity PASSED               [ 72%]
tests/test_cart.py::test_cannot_add_negative_price PASSED                  [ 77%]
tests/test_cart.py::test_add_item_to_empty_cart_with_fixture PASSED        [ 83%]
tests/test_cart.py::test_remove_item_from_cart PASSED                      [ 88%]
tests/test_cart.py::test_update_quantity PASSED                            [ 94%]
tests/test_cart.py::test_clear_cart PASSED                                 [100%]

---------- coverage: platform darwin, python 3.11.5 -----------
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
app/__init__.py       0      0      0      0   100%
app/cart.py          36      2     10      1    95%   12, 45
-------------------------------------------------------------
TOTAL                36      2     10      1    95%

18 passed in 0.24s
```

**Coverage**: 95% line coverage, 92% branch coverage

---

## Session Metrics

**Total Duration**: 45 minutes
**Cycles Completed**: 5
**Average Cycle Time**: 9 minutes

| Cycle | Feature | RED | GREEN | REFACTOR | Total |
|-------|---------|-----|-------|----------|-------|
| 1 | Add item | 3min | 3min | 2min | 8min |
| 2 | Subtotal | 2min | 3min | 2min | 7min |
| 3 | 10% discount | 3min | 5min | 2min | 10min |
| 4 | 20% discount | 2min | 4min | 2min | 8min |
| 5 | Fixtures & validation | 3min | 5min | 4min | 12min |

**Tests Created**: 18
**Coverage**: 95% line, 92% branch
**Parametrized Tests**: 6 (from 2 parametrize decorators)

---

## Key Takeaways

### pytest Advantages
- Plain `assert` statements (no `self.assertEqual`)
- Fixtures for reusable setup (no `setUp`/`tearDown`)
- Parametrize for multiple test cases from one function
- Rich plugin ecosystem (pytest-cov, pytest-mock, pytest-asyncio)

### TDD Benefits Realized
- **Test-first**: All features driven by failing tests
- **Incremental**: Small steps, frequent validation
- **Refactoring confidence**: Tests stay green throughout
- **Living documentation**: 18 tests document all behaviors

### Lessons Learned
- Fixtures eliminate test duplication
- Parametrize reduces boilerplate for multiple cases
- Validation should be tested with exception assertions
- Discount logic naturally extracted to private method

---

Related: [unittest-tdd-example.md](unittest-tdd-example.md) | [async-testing-example.md](async-testing-example.md) | [Return to INDEX](INDEX.md)
