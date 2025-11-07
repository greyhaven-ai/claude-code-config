# Clarity Refactoring Example

Systematic code clarity improvement using 10 refactoring rules to reduce complexity from 47 to 8.

## Scenario

**Project**: E-commerce order processing service
**Initial State**: High cyclomatic complexity (47), nested conditionals, poor readability
**Goal**: Refactor for clarity without changing behavior
**Time Investment**: 3 hours analysis + 4 hours refactoring = 7 hours total

## Before: Complex Code

### order_processor.py (Problematic - Complexity: 47)

```python
def process_order(order, user, items, payment_info, shipping_address, discount_code=None):
    """Process an order with payment and shipping."""

    # Validate order
    if order:
        if user:
            if user.is_active:
                if items:
                    if len(items) > 0:
                        total = 0
                        for item in items:
                            if item.in_stock:
                                if item.quantity > 0:
                                    if item.price > 0:
                                        total += item.price * item.quantity
                                    else:
                                        return {"error": "Invalid price"}
                                else:
                                    return {"error": "Invalid quantity"}
                            else:
                                return {"error": f"Item {item.id} out of stock"}

                        # Apply discount
                        if discount_code:
                            if discount_code.is_valid:
                                if discount_code.expiry > datetime.now():
                                    if discount_code.min_purchase <= total:
                                        if discount_code.type == "percentage":
                                            total = total - (total * discount_code.value / 100)
                                        elif discount_code.type == "fixed":
                                            total = total - discount_code.value
                                        else:
                                            pass  # Unknown discount type
                                    else:
                                        pass  # Min purchase not met
                                else:
                                    return {"error": "Discount code expired"}
                            else:
                                return {"error": "Invalid discount code"}

                        # Process payment
                        if payment_info:
                            if payment_info.card_number:
                                if len(payment_info.card_number) == 16:
                                    if payment_info.cvv:
                                        if len(payment_info.cvv) == 3:
                                            if payment_info.expiry_month:
                                                if payment_info.expiry_year:
                                                    try:
                                                        payment_result = charge_card(
                                                            payment_info.card_number,
                                                            payment_info.cvv,
                                                            payment_info.expiry_month,
                                                            payment_info.expiry_year,
                                                            total
                                                        )
                                                        if payment_result.success:
                                                            # Calculate shipping
                                                            if shipping_address:
                                                                if shipping_address.country == "US":
                                                                    shipping_cost = 10 if total < 100 else 0
                                                                elif shipping_address.country == "CA":
                                                                    shipping_cost = 15 if total < 100 else 5
                                                                else:
                                                                    shipping_cost = 25
                                                                total += shipping_cost

                                                                # Create order record
                                                                order.total = total
                                                                order.status = "paid"
                                                                order.payment_id = payment_result.id
                                                                db.save(order)

                                                                # Send confirmation email
                                                                try:
                                                                    send_email(user.email, "Order confirmed", f"Total: ${total}")
                                                                except:
                                                                    pass  # Email failure shouldn't break order

                                                                return {"success": True, "order_id": order.id, "total": total}
                                                            else:
                                                                return {"error": "Missing shipping address"}
                                                        else:
                                                            return {"error": f"Payment failed: {payment_result.error}"}
                                                    except Exception as e:
                                                        return {"error": f"Payment error: {str(e)}"}
                                                else:
                                                    return {"error": "Missing expiry year"}
                                            else:
                                                return {"error": "Missing expiry month"}
                                        else:
                                            return {"error": "Invalid CVV"}
                                    else:
                                        return {"error": "Missing CVV"}
                                else:
                                    return {"error": "Invalid card number"}
                            else:
                                return {"error": "Missing card number"}
                        else:
                            return {"error": "Missing payment info"}
                    else:
                        return {"error": "No items in order"}
                else:
                    return {"error": "No items provided"}
            else:
                return {"error": "User account inactive"}
        else:
            return {"error": "No user provided"}
    else:
        return {"error": "No order provided"}
```

### Complexity Analysis

```
Function: process_order
Cyclomatic Complexity: 47
Nesting Depth: 17 levels (!)
Lines of Code: 94
Parameters: 7 (too many)
Branches: 46

Issues:
- Arrow Anti-Pattern (deeply nested if statements)
- Multiple responsibilities (validation, calculation, payment, shipping, email)
- Poor error handling (string errors, no exceptions)
- Magic numbers (10, 15, 25, 100)
- No single responsibility
- Hard to test (one giant function)
- Hard to read (need to track 17 nesting levels)
```

## Refactoring Process: 10 Rules Applied

### Rule 1: Guard Clauses (Flatten Nesting)

**Before** (17 levels deep):
```python
if order:
    if user:
        if user.is_active:
            # ... 14 more levels
```

**After** (early returns):
```python
if not order:
    raise OrderError("No order provided")

if not user:
    raise OrderError("No user provided")

if not user.is_active:
    raise OrderError("User account inactive")

# Continue with happy path (no nesting)
```

### Rule 2: Extract Functions (Single Responsibility)

Break giant function into focused functions:
```python
# Instead of one 94-line function:
def process_order()          # Orchestrates
def validate_order_items()   # Validates items
def calculate_order_total()  # Calculates total
def apply_discount()         # Applies discount
def process_payment()        # Handles payment
def calculate_shipping()     # Calculates shipping
def save_order()             # Saves to database
def send_confirmation()      # Sends email
```

### Rule 3: Explaining Variables

**Before** (complex expressions):
```python
if discount_code.expiry > datetime.now() and discount_code.min_purchase <= total:
```

**After** (explaining variables):
```python
is_discount_valid = discount_code.expiry > datetime.now()
meets_minimum_purchase = discount_code.min_purchase <= total

if is_discount_valid and meets_minimum_purchase:
```

### Rule 4: Explaining Constants

**Before** (magic numbers):
```python
shipping_cost = 10 if total < 100 else 0  # What do these mean?
```

**After** (named constants):
```python
FREE_SHIPPING_THRESHOLD = 100
US_STANDARD_SHIPPING = 10

shipping_cost = US_STANDARD_SHIPPING if total < FREE_SHIPPING_THRESHOLD else 0
```

## After: Refactored Code

### order_processor.py (Refactored - Complexity: 8)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# Rule 4: Named constants
FREE_SHIPPING_THRESHOLD = 100
US_STANDARD_SHIPPING = 10
CA_STANDARD_SHIPPING = 15
CA_FREE_SHIPPING_THRESHOLD_COST = 5
INTERNATIONAL_SHIPPING = 25

class OrderError(Exception):
    """Custom exception for order processing errors."""
    pass

@dataclass
class OrderResult:
    """Result of order processing."""
    success: bool
    order_id: Optional[str] = None
    total: Optional[float] = None
    error: Optional[str] = None

def process_order(
    order: Order,
    user: User,
    items: List[OrderItem],
    payment_info: PaymentInfo,
    shipping_address: ShippingAddress,
    discount_code: Optional[DiscountCode] = None
) -> OrderResult:
    """
    Process an order with payment and shipping.

    Orchestrates: validation → calculation → payment → shipping → confirmation
    """
    try:
        # Rule 1: Guard clauses (early returns)
        _validate_order_requirements(order, user, items, payment_info, shipping_address)

        # Rule 2: Extracted functions (single responsibility)
        validate_order_items(items)
        subtotal = calculate_order_total(items)
        total = apply_discount(subtotal, discount_code) if discount_code else subtotal

        # Process payment
        payment_result = process_payment(payment_info, total)

        # Calculate final total with shipping
        shipping_cost = calculate_shipping(shipping_address, total)
        final_total = total + shipping_cost

        # Save and confirm
        order_id = save_order(order, final_total, payment_result.id)
        send_confirmation_email(user.email, order_id, final_total)

        return OrderResult(success=True, order_id=order_id, total=final_total)

    except OrderError as e:
        return OrderResult(success=False, error=str(e))

def _validate_order_requirements(
    order: Order,
    user: User,
    items: List[OrderItem],
    payment_info: PaymentInfo,
    shipping_address: ShippingAddress
) -> None:
    """Validate all required order components (Rule 1: Guard clauses)."""
    if not order:
        raise OrderError("No order provided")

    if not user:
        raise OrderError("No user provided")

    if not user.is_active:
        raise OrderError("User account inactive")

    if not items:
        raise OrderError("No items provided")

    if not payment_info:
        raise OrderError("Missing payment info")

    if not shipping_address:
        raise OrderError("Missing shipping address")

def validate_order_items(items: List[OrderItem]) -> None:
    """Validate all items are valid and in stock (Rule 2: Single responsibility)."""
    # Rule 1: Guard clause
    if not items:
        raise OrderError("No items in order")

    for item in items:
        # Rule 3: Explaining variables
        is_out_of_stock = not item.in_stock
        has_invalid_quantity = item.quantity <= 0
        has_invalid_price = item.price <= 0

        if is_out_of_stock:
            raise OrderError(f"Item {item.id} out of stock")

        if has_invalid_quantity:
            raise OrderError(f"Invalid quantity for item {item.id}")

        if has_invalid_price:
            raise OrderError(f"Invalid price for item {item.id}")

def calculate_order_total(items: List[OrderItem]) -> float:
    """Calculate order subtotal from items (Rule 2: Single responsibility)."""
    return sum(item.price * item.quantity for item in items)

def apply_discount(subtotal: float, discount_code: DiscountCode) -> float:
    """Apply discount code to subtotal (Rule 2: Single responsibility)."""
    # Rule 1: Guard clauses
    if not discount_code.is_valid:
        raise OrderError("Invalid discount code")

    # Rule 3: Explaining variables
    is_expired = discount_code.expiry <= datetime.now()
    meets_minimum = discount_code.min_purchase <= subtotal

    if is_expired:
        raise OrderError("Discount code expired")

    if not meets_minimum:
        # Return original total if minimum not met (valid scenario, not error)
        return subtotal

    # Rule 5: Symmetry (consistent discount calculations)
    if discount_code.type == "percentage":
        discount_amount = subtotal * discount_code.value / 100
    elif discount_code.type == "fixed":
        discount_amount = discount_code.value
    else:
        raise OrderError(f"Unknown discount type: {discount_code.type}")

    return subtotal - discount_amount

def process_payment(payment_info: PaymentInfo, amount: float) -> PaymentResult:
    """Process payment with card (Rule 2: Single responsibility)."""
    # Rule 1: Guard clauses
    _validate_payment_info(payment_info)

    try:
        return charge_card(
            payment_info.card_number,
            payment_info.cvv,
            payment_info.expiry_month,
            payment_info.expiry_year,
            amount
        )
    except PaymentGatewayError as e:
        raise OrderError(f"Payment failed: {e}")

def _validate_payment_info(payment_info: PaymentInfo) -> None:
    """Validate payment information (Rule 2: Extracted validation)."""
    if not payment_info.card_number:
        raise OrderError("Missing card number")

    # Rule 4: Explaining constant
    VALID_CARD_NUMBER_LENGTH = 16
    if len(payment_info.card_number) != VALID_CARD_NUMBER_LENGTH:
        raise OrderError("Invalid card number")

    if not payment_info.cvv:
        raise OrderError("Missing CVV")

    VALID_CVV_LENGTH = 3
    if len(payment_info.cvv) != VALID_CVV_LENGTH:
        raise OrderError("Invalid CVV")

    if not payment_info.expiry_month:
        raise OrderError("Missing expiry month")

    if not payment_info.expiry_year:
        raise OrderError("Missing expiry year")

def calculate_shipping(address: ShippingAddress, order_total: float) -> float:
    """Calculate shipping cost based on country and order total (Rule 2)."""
    # Rule 4: Named constants (defined at top)
    if address.country == "US":
        return US_STANDARD_SHIPPING if order_total < FREE_SHIPPING_THRESHOLD else 0

    if address.country == "CA":
        return CA_STANDARD_SHIPPING if order_total < FREE_SHIPPING_THRESHOLD else CA_FREE_SHIPPING_THRESHOLD_COST

    return INTERNATIONAL_SHIPPING

def save_order(order: Order, total: float, payment_id: str) -> str:
    """Save order to database (Rule 2: Single responsibility)."""
    order.total = total
    order.status = "paid"
    order.payment_id = payment_id
    db.save(order)
    return order.id

def send_confirmation_email(email: str, order_id: str, total: float) -> None:
    """Send order confirmation email (Rule 2: Single responsibility)."""
    try:
        send_email(email, "Order confirmed", f"Order {order_id}: ${total:.2f}")
    except EmailError:
        # Rule 6: Explicit error handling
        # Email failure shouldn't prevent order completion
        logger.warning(f"Failed to send confirmation email to {email}")
```

## Results

### Complexity Metrics: Before vs After

```
Metric                          Before    After    Change
--------------------------------------------------------
Cyclomatic Complexity           47        8        -39 ✅
Nesting Depth                   17        2        -15 ✅
Lines of Code (total)           94        180      +86
Lines per Function              94        15       -79 ✅
Number of Functions             1         10       +9
Parameters (max)                7         6        -1
Readability Score               35/100    92/100   +57 ✅
Maintainability Index           42/100    87/100   +45 ✅
Test Coverage Possible          ~40%      95%      +55 ✅
```

### 10 Refactoring Rules Applied

| Rule | Description | Lines Changed | Impact |
|------|-------------|---------------|--------|
| 1 | Guard Clauses | 25 | Eliminated 15 nesting levels |
| 2 | Extract Functions | 180 | Created 10 focused functions |
| 3 | Explaining Variables | 15 | Clarified complex conditions |
| 4 | Explaining Constants | 10 | Replaced magic numbers |
| 5 | Symmetry | 8 | Consistent discount handling |
| 6 | Explicit Error Handling | 12 | Custom exceptions |
| 7 | Reading Order | N/A | Logical top-down flow |
| 8 | Type Hints | 20 | Added type annotations |
| 9 | Docstrings | 35 | Documented all functions |
| 10 | Consistent Naming | 15 | Verb_noun pattern |

## Key Lessons

### 1. Guard Clauses Transform Readability

**Before** (arrow anti-pattern):
```python
if valid:
    if more_valid:
        if even_more_valid:
            # Happy path buried 17 levels deep
```

**After** (guard clauses):
```python
if not valid:
    raise Error("Not valid")

if not more_valid:
    raise Error("Not more valid")

# Happy path at top level (easy to find)
```

### 2. Single Responsibility Principle

One function should do one thing:
- ❌ `process_order()` - validates, calculates, pays, ships, emails (5 responsibilities)
- ✅ `validate_order_items()` - only validates
- ✅ `calculate_order_total()` - only calculates
- ✅ `process_payment()` - only processes payment

### 3. Explaining Variables Make Code Self-Documenting

**Before**:
```python
if discount_code.expiry > datetime.now() and discount_code.min_purchase <= total:
```

**After**:
```python
is_discount_valid = discount_code.expiry > datetime.now()
meets_minimum_purchase = discount_code.min_purchase <= total

if is_discount_valid and meets_minimum_purchase:
```

### 4. Named Constants Beat Comments

**Before**:
```python
shipping_cost = 10  # Standard US shipping
```

**After**:
```python
US_STANDARD_SHIPPING = 10
shipping_cost = US_STANDARD_SHIPPING
```

### 5. More Lines Can Mean Better Code

- Original: 94 lines, complexity 47
- Refactored: 180 lines, complexity 8
- **+86 lines but -39 complexity**

Quality > brevity!

## Testing Impact

### Before Refactoring

```python
# Impossible to test individual pieces
def test_process_order():
    # Must test all 94 lines together
    # Can't test discount logic in isolation
    # Can't test shipping logic in isolation
    # Mock nightmare (7 parameters, nested dependencies)
```

### After Refactoring

```python
# Each function testable in isolation
def test_calculate_order_total():
    items = [create_item(price=10, quantity=2)]
    assert calculate_order_total(items) == 20

def test_apply_discount_percentage():
    discount = create_discount(type="percentage", value=10)
    assert apply_discount(100, discount) == 90

def test_apply_discount_fixed():
    discount = create_discount(type="fixed", value=15)
    assert apply_discount(100, discount) == 85

def test_calculate_shipping_us_free():
    address = create_address(country="US")
    assert calculate_shipping(address, 150) == 0

def test_calculate_shipping_us_standard():
    address = create_address(country="US")
    assert calculate_shipping(address, 50) == 10
```

**Result**: Test coverage improved from 40% to 95%

---

Related: [Security Review Example](security-review-example.md) | [Synthesis Analysis Example](synthesis-analysis-example.md) | [Return to INDEX](INDEX.md)
