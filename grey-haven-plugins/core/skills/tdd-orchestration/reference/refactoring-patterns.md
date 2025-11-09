# Refactoring Patterns Reference

Comprehensive catalog of refactoring patterns with SOLID principles for the REFACTOR phase of TDD.

## Core Principles

### The Golden Rule of Refactoring

**Never change behavior during refactoring.**

```python
# ❌ BAD: Adding feature during refactoring
def login(email, password):
    user = get_user(email)
    if user and verify_password(password, user.password_hash):
        log_login_attempt(email)  # ❌ NEW FEATURE added during refactor!
        return user
    return None

# ✅ GOOD: Only improving structure
def login(email, password):
    user = get_user(email)
    if user and _verify_credentials(user, password):  # ✅ Extract method
        return user
    return None

def _verify_credentials(user, password):
    """Extracted for clarity."""
    return verify_password(password, user.password_hash)
```

### When to Refactor

**Refactor when**:
- ✅ Tests are passing
- ✅ Code smells detected
- ✅ Duplication exists
- ✅ Complexity is high

**Don't refactor when**:
- ❌ Tests are failing
- ❌ Adding new features
- ❌ Under time pressure (tech debt)
- ❌ No tests exist (write tests first!)

---

## Pattern 1: Extract Method

### When to Use

**Symptoms**:
- Long functions (>50 lines)
- Multiple levels of abstraction
- Repeated code blocks
- Complex logic that needs explanation

### Before

```python
def process_order(order_data):
    # Validate order (10 lines)
    if not order_data.get("items"):
        raise ValueError("Items required")
    if not order_data.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order_data.get("payment_method"):
        raise ValueError("Payment method required")

    # Calculate pricing (15 lines)
    subtotal = 0
    for item in order_data["items"]:
        price = item["price"]
        quantity = item["quantity"]
        if quantity >= 10:
            price *= 0.9  # Bulk discount
        subtotal += price * quantity

    tax = subtotal * 0.08
    total = subtotal + tax

    # Process payment (20 lines)
    payment_info = {
        "amount": total,
        "method": order_data["payment_method"],
        "customer": order_data["customer_id"]
    }
    payment_result = payment_gateway.charge(payment_info)
    if not payment_result["success"]:
        raise PaymentError("Payment failed")

    # Save order (10 lines)
    order = Order(
        customer_id=order_data["customer_id"],
        items=order_data["items"],
        total=total,
        status="confirmed"
    )
    db.save(order)

    return order
```

**Problems**: 55 lines, 4 responsibilities, hard to test, low cohesion.

### After

```python
def process_order(order_data):
    """Process order with validation, pricing, and payment."""
    _validate_order_data(order_data)
    total = _calculate_order_total(order_data["items"])
    _process_payment(total, order_data)
    return _save_order(order_data, total)

def _validate_order_data(order_data):
    """Validate required order fields."""
    if not order_data.get("items"):
        raise ValueError("Items required")
    if not order_data.get("customer_id"):
        raise ValueError("Customer ID required")
    if not order_data.get("payment_method"):
        raise ValueError("Payment method required")

def _calculate_order_total(items):
    """Calculate order total with discounts and tax."""
    subtotal = sum(
        _calculate_item_price(item["price"], item["quantity"])
        for item in items
    )
    tax = subtotal * 0.08
    return subtotal + tax

def _calculate_item_price(price, quantity):
    """Calculate item price with bulk discount."""
    if quantity >= 10:
        price *= 0.9  # 10% bulk discount
    return price * quantity

def _process_payment(amount, order_data):
    """Process payment through gateway."""
    payment_info = {
        "amount": amount,
        "method": order_data["payment_method"],
        "customer": order_data["customer_id"]
    }
    result = payment_gateway.charge(payment_info)
    if not result["success"]:
        raise PaymentError("Payment failed")

def _save_order(order_data, total):
    """Save order to database."""
    order = Order(
        customer_id=order_data["customer_id"],
        items=order_data["items"],
        total=total,
        status="confirmed"
    )
    db.save(order)
    return order
```

**Benefits**:
- ✅ Each function has single responsibility
- ✅ Easy to test individually
- ✅ Clear intent from function names
- ✅ Reusable components

---

## Pattern 2: Extract Class

### When to Use

**Symptoms**:
- God class (>500 lines, many responsibilities)
- Many fields related to same concept
- Methods always use same subset of fields

### Before

```python
class Order:
    """God class with too many responsibilities."""

    def __init__(self):
        # Order info
        self.id = None
        self.status = "pending"
        self.created_at = None

        # Customer info
        self.customer_email = ""
        self.customer_name = ""
        self.customer_phone = ""

        # Billing info
        self.billing_street = ""
        self.billing_city = ""
        self.billing_state = ""
        self.billing_zip = ""

        # Shipping info
        self.shipping_street = ""
        self.shipping_city = ""
        self.shipping_state = ""
        self.shipping_zip = ""

        # Payment info
        self.payment_method = ""
        self.card_number = ""
        self.card_cvv = ""
        self.card_expiry = ""

        # Items
        self.items = []

    def validate_customer(self):
        """Validates customer information."""
        # 20 lines of validation

    def validate_billing_address(self):
        """Validates billing address."""
        # 15 lines of validation

    def validate_shipping_address(self):
        """Validates shipping address."""
        # 15 lines of validation

    def validate_payment(self):
        """Validates payment information."""
        # 25 lines of validation

    # ... 30 more methods (500+ lines total)
```

### After

```python
class Order:
    """Clean order class with single responsibility."""

    def __init__(self):
        self.id = None
        self.status = "pending"
        self.created_at = None
        self.customer = Customer()
        self.billing_address = Address()
        self.shipping_address = Address()
        self.payment = PaymentInfo()
        self.items = []

    def validate(self):
        """Validate all order components."""
        self.customer.validate()
        self.billing_address.validate()
        self.shipping_address.validate()
        self.payment.validate()


class Customer:
    """Extracted customer information."""

    def __init__(self):
        self.email = ""
        self.name = ""
        self.phone = ""

    def validate(self):
        """Validate customer information."""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email")
        if not self.name:
            raise ValueError("Name required")


class Address:
    """Extracted address information."""

    def __init__(self):
        self.street = ""
        self.city = ""
        self.state = ""
        self.zip = ""

    def validate(self):
        """Validate address."""
        if not self.street:
            raise ValueError("Street required")
        if not self.city:
            raise ValueError("City required")


class PaymentInfo:
    """Extracted payment information."""

    def __init__(self):
        self.method = ""
        self.card_number = ""
        self.cvv = ""
        self.expiry = ""

    def validate(self):
        """Validate payment information."""
        if self.method == "credit_card":
            if not self.card_number or len(self.card_number) != 16:
                raise ValueError("Invalid card number")
            if not self.cvv or len(self.cvv) != 3:
                raise ValueError("Invalid CVV")
```

**Benefits**:
- ✅ Single Responsibility Principle
- ✅ Easier to test (smaller classes)
- ✅ Reusable components
- ✅ Clear ownership of data

---

## Pattern 3: Replace Conditional with Polymorphism

### When to Use

**Symptoms**:
- Many `if`/`elif`/`else` or `switch` statements
- Type checking (`isinstance`, `typeof`)
- Adding new types requires modifying existing code

### Before

```python
def calculate_shipping_cost(order, shipping_type):
    """Calculate shipping cost based on type."""
    if shipping_type == "standard":
        if order.total < 50:
            return 5.99
        else:
            return 0  # Free shipping over $50

    elif shipping_type == "express":
        if order.total < 50:
            return 12.99
        else:
            return 7.99  # Reduced for large orders

    elif shipping_type == "overnight":
        if order.weight > 5:
            return 29.99 + (order.weight - 5) * 2
        else:
            return 29.99

    elif shipping_type == "international":
        base = 19.99
        return base + (order.weight * 3)

    else:
        raise ValueError(f"Unknown shipping type: {shipping_type}")

# Adding new shipping type requires modifying this function! ❌
```

### After

```python
class ShippingStrategy:
    """Base shipping strategy."""

    def calculate_cost(self, order):
        raise NotImplementedError


class StandardShipping(ShippingStrategy):
    """Standard shipping calculation."""

    def calculate_cost(self, order):
        if order.total < 50:
            return 5.99
        return 0  # Free shipping


class ExpressShipping(ShippingStrategy):
    """Express shipping calculation."""

    def calculate_cost(self, order):
        if order.total < 50:
            return 12.99
        return 7.99


class OvernightShipping(ShippingStrategy):
    """Overnight shipping calculation."""

    def calculate_cost(self, order):
        base = 29.99
        if order.weight > 5:
            return base + (order.weight - 5) * 2
        return base


class InternationalShipping(ShippingStrategy):
    """International shipping calculation."""

    def calculate_cost(self, order):
        base = 19.99
        return base + (order.weight * 3)


# Factory pattern for creation
SHIPPING_STRATEGIES = {
    "standard": StandardShipping(),
    "express": ExpressShipping(),
    "overnight": OvernightShipping(),
    "international": InternationalShipping(),
}

def calculate_shipping_cost(order, shipping_type):
    """Calculate shipping cost using strategy pattern."""
    strategy = SHIPPING_STRATEGIES.get(shipping_type)
    if not strategy:
        raise ValueError(f"Unknown shipping type: {shipping_type}")
    return strategy.calculate_cost(order)

# Adding new type: Just create new class! ✅
class SameDayShipping(ShippingStrategy):
    def calculate_cost(self, order):
        return 39.99

SHIPPING_STRATEGIES["same_day"] = SameDayShipping()
```

**Benefits**:
- ✅ Open/Closed Principle (open for extension, closed for modification)
- ✅ Easy to add new types
- ✅ Each strategy tested independently
- ✅ No complex conditionals

---

## Pattern 4: Introduce Parameter Object

### When to Use

**Symptoms**:
- Functions with 4+ parameters
- Same parameters passed to multiple functions
- Parameters always travel together

### Before

```python
def create_user(
    email,
    password,
    first_name,
    last_name,
    phone,
    street,
    city,
    state,
    zip_code,
    country,
    date_of_birth,
    newsletter_opt_in
):
    """Too many parameters! Hard to call correctly."""
    user = User(
        email=email,
        password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        # ... 20 more lines
    )
    return user

# Calling is error-prone
user = create_user(
    "john@example.com",
    "password123",
    "John",
    "Doe",
    "555-1234",
    "123 Main St",
    "Springfield",
    "IL",
    "62701",
    "USA",
    "1990-01-01",
    True
)  # Which parameter is which? 🤔
```

### After

```python
class UserRegistrationData:
    """Parameter object for user registration."""

    def __init__(self):
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""
        self.phone = ""
        self.address = Address()
        self.date_of_birth = None
        self.newsletter_opt_in = False

    def validate(self):
        """Validate all fields."""
        if not self.email:
            raise ValueError("Email required")
        if not self.password or len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        # ... more validation


def create_user(registration_data: UserRegistrationData):
    """Create user from registration data."""
    registration_data.validate()

    user = User(
        email=registration_data.email,
        password=hash_password(registration_data.password),
        first_name=registration_data.first_name,
        last_name=registration_data.last_name,
        phone=registration_data.phone,
        address=registration_data.address,
        date_of_birth=registration_data.date_of_birth,
    )

    if registration_data.newsletter_opt_in:
        subscribe_to_newsletter(user.email)

    return user


# Calling is clear and type-safe
data = UserRegistrationData()
data.email = "john@example.com"
data.password = "password123"
data.first_name = "John"
data.last_name = "Doe"
# ... etc

user = create_user(data)  # ✅ Clear intent
```

**Benefits**:
- ✅ Fewer function parameters
- ✅ Related data grouped together
- ✅ Easier to extend (add new field to object)
- ✅ Validation logic centralized

---

## Pattern 5: Replace Magic Numbers with Named Constants

### When to Use

**Symptoms**:
- Numbers with unclear meaning
- Same number repeated in multiple places
- Calculations with unexplained values

### Before

```python
def calculate_late_fee(days_overdue, balance):
    """Calculate late fee for overdue balance."""
    if days_overdue <= 7:
        return 0
    elif days_overdue <= 30:
        return balance * 0.05  # What is 0.05?
    elif days_overdue <= 60:
        return balance * 0.10  # What is 0.10?
    else:
        return min(balance * 0.15, 100)  # Why 100?

def send_reminder(days_overdue):
    """Send payment reminder."""
    if days_overdue == 7:  # Magic number repeated
        send_email("First reminder")
    elif days_overdue == 14:
        send_email("Second reminder")
    elif days_overdue == 30:  # Same as above function
        send_email("Final notice")
```

### After

```python
# Named constants with clear meaning
GRACE_PERIOD_DAYS = 7
FIRST_TIER_DAYS = 30
SECOND_TIER_DAYS = 60

FIRST_TIER_RATE = 0.05  # 5% late fee
SECOND_TIER_RATE = 0.10  # 10% late fee
THIRD_TIER_RATE = 0.15  # 15% late fee

MAX_LATE_FEE = 100.00  # Maximum late fee cap

FIRST_REMINDER_DAYS = 7
SECOND_REMINDER_DAYS = 14
FINAL_NOTICE_DAYS = 30


def calculate_late_fee(days_overdue, balance):
    """Calculate late fee for overdue balance."""
    if days_overdue <= GRACE_PERIOD_DAYS:
        return 0
    elif days_overdue <= FIRST_TIER_DAYS:
        return balance * FIRST_TIER_RATE
    elif days_overdue <= SECOND_TIER_DAYS:
        return balance * SECOND_TIER_RATE
    else:
        fee = balance * THIRD_TIER_RATE
        return min(fee, MAX_LATE_FEE)


def send_reminder(days_overdue):
    """Send payment reminder."""
    if days_overdue == FIRST_REMINDER_DAYS:
        send_email("First reminder")
    elif days_overdue == SECOND_REMINDER_DAYS:
        send_email("Second reminder")
    elif days_overdue == FINAL_NOTICE_DAYS:
        send_email("Final notice")
```

**Benefits**:
- ✅ Self-documenting code
- ✅ Easy to change values (one place)
- ✅ Prevents typos (reuse constant)
- ✅ Clear business rules

---

## SOLID Principles

### S: Single Responsibility Principle

**A class should have one reason to change.**

```python
# ❌ Multiple responsibilities
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save_to_database(self):
        """Database responsibility"""
        pass

    def send_welcome_email(self):
        """Email responsibility"""
        pass

    def log_activity(self):
        """Logging responsibility"""
        pass

# ✅ Single responsibility
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class UserRepository:
    """Database responsibility"""
    def save(self, user):
        pass


class EmailService:
    """Email responsibility"""
    def send_welcome_email(self, user):
        pass


class ActivityLogger:
    """Logging responsibility"""
    def log_activity(self, user, action):
        pass
```

### O: Open/Closed Principle

**Open for extension, closed for modification.**

See [Replace Conditional with Polymorphism](#pattern-3-replace-conditional-with-polymorphism).

### L: Liskov Substitution Principle

**Subtypes must be substitutable for base types.**

```python
# ❌ Violates LSP
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly!")  # ❌ Breaks contract!

# ✅ Respects LSP
class Bird:
    def move(self):
        raise NotImplementedError

class FlyingBird(Bird):
    def move(self):
        return "Flying"

class Penguin(Bird):
    def move(self):
        return "Swimming"  # ✅ Fulfills contract differently
```

### I: Interface Segregation Principle

**Clients shouldn't depend on interfaces they don't use.**

```python
# ❌ Fat interface
class Worker:
    def work(self):
        pass

    def eat_lunch(self):
        pass

class Robot(Worker):
    def work(self):
        return "Working"

    def eat_lunch(self):
        raise Exception("Robots don't eat!")  # ❌ Forced to implement unused method

# ✅ Segregated interfaces
class Workable:
    def work(self):
        pass

class Eatable:
    def eat_lunch(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        return "Working"

    def eat_lunch(self):
        return "Eating"

class Robot(Workable):  # Only implements what it needs
    def work(self):
        return "Working"
```

### D: Dependency Inversion Principle

**Depend on abstractions, not concretions.**

```python
# ❌ Depends on concrete class
class OrderService:
    def __init__(self):
        self.email_service = GmailService()  # ❌ Hardcoded dependency

    def place_order(self, order):
        # ...
        self.email_service.send(order.customer_email, "Order confirmed")

# ✅ Depends on abstraction
class EmailService:  # Abstract interface
    def send(self, to, subject, body):
        raise NotImplementedError

class GmailService(EmailService):
    def send(self, to, subject, body):
        # Gmail implementation
        pass

class SendGridService(EmailService):
    def send(self, to, subject, body):
        # SendGrid implementation
        pass

class OrderService:
    def __init__(self, email_service: EmailService):  # ✅ Inject dependency
        self.email_service = email_service

    def place_order(self, order):
        # ...
        self.email_service.send(order.customer_email, "Order confirmed")

# Easy to swap implementations
service = OrderService(email_service=GmailService())
service = OrderService(email_service=SendGridService())
service = OrderService(email_service=MockEmailService())  # For testing
```

---

## Refactoring Safety

### Always Run Tests

```bash
# Before refactoring
$ pytest
47 passed ✅

# After each refactoring step
$ pytest
47 passed ✅

# If tests fail, REVERT IMMEDIATELY
$ git checkout app/myfile.py
```

### Small Steps

```python
# ❌ Bad: Refactor everything at once
# - Rename 20 functions
# - Extract 10 classes
# - Change 50 files
# Tests break: Which change broke it? 🤔

# ✅ Good: One refactoring at a time
# Step 1: Extract one method
$ git add -A && git commit -m "refactor: extract calculate_total"
$ pytest  # ✅ Still passing

# Step 2: Rename for clarity
$ git add -A && git commit -m "refactor: rename to calculate_order_total"
$ pytest  # ✅ Still passing

# Step 3: Extract class
$ git add -A && git commit -m "refactor: extract Order class"
$ pytest  # ✅ Still passing
```

---

Related: [Red-Green-Refactor Guide](red-green-refactor-guide.md) | [TDD Methodologies](tdd-methodologies.md) | [Coverage Thresholds](coverage-thresholds.md) | [Return to INDEX](INDEX.md)
