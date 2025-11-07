# Clarity Refactoring Rules

10 proven refactoring rules for improving code clarity, reducing complexity, and eliminating technical debt.

## Rule 1: Guard Clauses (Flatten Nesting)

**Problem**: Deeply nested if statements (arrow anti-pattern)

**Solution**: Use early returns to keep the happy path at the lowest nesting level

**Before** (Nesting Depth: 5):
```python
def process_order(order, user, items):
    if order:
        if user:
            if user.is_active:
                if items:
                    if len(items) > 0:
                        # Happy path buried 5 levels deep
                        return create_order(order, user, items)
                    else:
                        return {"error": "Empty items"}
                else:
                    return {"error": "No items"}
            else:
                return {"error": "User inactive"}
        else:
            return {"error": "No user"}
    else:
        return {"error": "No order"}
```

**After** (Nesting Depth: 1):
```python
def process_order(order, user, items):
    # Guard clauses handle error cases early
    if not order:
        raise OrderError("No order")

    if not user:
        raise OrderError("No user")

    if not user.is_active:
        raise OrderError("User inactive")

    if not items or len(items) == 0:
        raise OrderError("No items")

    # Happy path at top level (easy to find and read)
    return create_order(order, user, items)
```

**Benefits**:
- Reduces nesting from 5 levels to 1
- Happy path immediately visible
- Easier to add new validation
- Complexity reduced by 60-80%

## Rule 2: Extract Functions (Single Responsibility)

**Problem**: Giant functions with multiple responsibilities

**Solution**: Break into focused functions, each doing one thing

**Before** (One 80-line function):
```python
def handle_user_registration(email, password, name, address):
    # Validate email (responsibility 1)
    if not email or "@" not in email:
        return {"error": "Invalid email"}

    # Check duplicate (responsibility 2)
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return {"error": "Email exists"}

    # Hash password (responsibility 3)
    hashed = bcrypt.hash(password)

    # Create user (responsibility 4)
    user = User(email=email, password=hashed, name=name)
    db.add(user)
    db.commit()

    # Send welcome email (responsibility 5)
    send_email(email, "Welcome!", "Thanks for signing up!")

    # Create profile (responsibility 6)
    profile = Profile(user_id=user.id, address=address)
    db.add(profile)
    db.commit()

    return {"success": True, "user_id": user.id}
```

**After** (Six focused functions):
```python
def handle_user_registration(email: str, password: str, name: str, address: str):
    """Orchestrate user registration (single responsibility: coordination)."""
    validate_email(email)
    check_email_not_exists(email)
    hashed_password = hash_password(password)
    user = create_user(email, hashed_password, name)
    send_welcome_email(user.email)
    create_user_profile(user.id, address)
    return {"success": True, "user_id": user.id}

def validate_email(email: str) -> None:
    """Validate email format."""
    if not email or "@" not in email:
        raise ValidationError("Invalid email")

def check_email_not_exists(email: str) -> None:
    """Check email doesn't already exist."""
    if db.query(User).filter(User.email == email).first():
        raise ValidationError("Email already exists")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.hash(password)

def create_user(email: str, hashed_password: str, name: str) -> User:
    """Create user record in database."""
    user = User(email=email, password=hashed_password, name=name)
    db.add(user)
    db.commit()
    return user

def send_welcome_email(email: str) -> None:
    """Send welcome email to new user."""
    send_email(email, "Welcome!", "Thanks for signing up!")

def create_user_profile(user_id: str, address: str) -> None:
    """Create user profile with address."""
    profile = Profile(user_id=user_id, address=address)
    db.add(profile)
    db.commit()
```

**Benefits**:
- Each function has clear, single purpose
- Easier to test (test each function independently)
- Easier to reuse (call `hash_password` from anywhere)
- Better naming (function names document what code does)

## Rule 3: Explaining Variables

**Problem**: Complex conditions that require mental effort to understand

**Solution**: Extract conditions into well-named variables

**Before** (Mental overhead):
```python
if user.age >= 18 and user.country in ["US", "CA", "GB"] and user.email_verified and not user.blocked:
    # What does this condition really mean?
    allow_access()
```

**After** (Self-documenting):
```python
is_adult = user.age >= 18
is_supported_country = user.country in ["US", "CA", "GB"]
is_verified = user.email_verified
is_not_blocked = not user.blocked

is_eligible_user = is_adult and is_supported_country and is_verified and is_not_blocked

if is_eligible_user:
    allow_access()
```

**Benefits**:
- Condition meaning immediately clear
- Easy to modify (change one variable)
- Easy to debug (inspect each variable)
- Documents business logic

## Rule 4: Explaining Constants

**Problem**: Magic numbers and strings with unclear meaning

**Solution**: Replace with named constants

**Before** (Magic numbers):
```python
def calculate_shipping(weight, country):
    if weight < 1:
        return 5
    elif weight < 5:
        return 10
    elif weight < 10:
        return 15
    else:
        return 25

    if country == "US":
        return price * 0.9  # What does 0.9 mean?
```

**After** (Named constants):
```python
# Shipping constants
LIGHT_PACKAGE_THRESHOLD_KG = 1
LIGHT_PACKAGE_SHIPPING_USD = 5

MEDIUM_PACKAGE_THRESHOLD_KG = 5
MEDIUM_PACKAGE_SHIPPING_USD = 10

HEAVY_PACKAGE_THRESHOLD_KG = 10
HEAVY_PACKAGE_SHIPPING_USD = 15

VERY_HEAVY_PACKAGE_SHIPPING_USD = 25

US_SHIPPING_DISCOUNT = 0.10  # 10% discount for US customers

def calculate_shipping(weight: float, country: str) -> float:
    if weight < LIGHT_PACKAGE_THRESHOLD_KG:
        price = LIGHT_PACKAGE_SHIPPING_USD
    elif weight < MEDIUM_PACKAGE_THRESHOLD_KG:
        price = MEDIUM_PACKAGE_SHIPPING_USD
    elif weight < HEAVY_PACKAGE_THRESHOLD_KG:
        price = HEAVY_PACKAGE_SHIPPING_USD
    else:
        price = VERY_HEAVY_PACKAGE_SHIPPING_USD

    if country == "US":
        price *= (1 - US_SHIPPING_DISCOUNT)

    return price
```

**Benefits**:
- Numbers have clear meaning
- Easy to update (change constant, not scattered code)
- Documents business rules
- Type safety with constants

## Rule 5: Symmetry (Consistent Patterns)

**Problem**: Similar operations handled differently

**Solution**: Make similar code look similar

**Before** (Inconsistent):
```python
def process_payment(payment_type, amount):
    if payment_type == "credit_card":
        result = charge_card(amount)
        if result["success"]:
            return True
        else:
            return False
    elif payment_type == "paypal":
        try:
            paypal_charge(amount)
            return True
        except:
            return False
    elif payment_type == "crypto":
        crypto_result = process_crypto(amount)
        return crypto_result == "ok"
```

**After** (Symmetric):
```python
def process_payment(payment_type: PaymentType, amount: float) -> bool:
    """Process payment through configured gateway."""
    if payment_type == PaymentType.CREDIT_CARD:
        return _process_credit_card_payment(amount)

    if payment_type == PaymentType.PAYPAL:
        return _process_paypal_payment(amount)

    if payment_type == PaymentType.CRYPTO:
        return _process_crypto_payment(amount)

    raise ValueError(f"Unknown payment type: {payment_type}")

def _process_credit_card_payment(amount: float) -> bool:
    result = charge_card(amount)
    return result.get("success", False)

def _process_paypal_payment(amount: float) -> bool:
    try:
        paypal_charge(amount)
        return True
    except PaymentError:
        return False

def _process_crypto_payment(amount: float) -> bool:
    result = process_crypto(amount)
    return result == "ok"
```

**Benefits**:
- Consistent structure (all payment types handled same way)
- Easy to add new payment types
- Pattern recognition (code looks familiar)

## Rule 6: Delete Dead Code

**Problem**: Commented-out code, unused imports, unreachable branches

**Solution**: Delete ruthlessly (version control preserves history)

**Before** (Cluttered):
```python
import json
import csv  # Unused import
from datetime import datetime
# import pandas  # Commented out

def process_data(data):
    # Old implementation (2022)
    # result = old_process(data)
    # if result:
    #     return result
    # else:
    #     return None

    # New implementation (2024)
    result = new_process(data)
    return result

    # This code never runs
    legacy_cleanup()
    send_email("admin@example.com")
```

**After** (Clean):
```python
import json
from datetime import datetime

def process_data(data):
    """Process data using current algorithm."""
    return new_process(data)
```

**Benefits**:
- Less code to read and maintain
- No confusion about which code is active
- Git history preserves old code if needed

## Rule 7: Consistent Naming

**Problem**: Inconsistent naming conventions across codebase

**Solution**: Choose one style and enforce it

**Python: snake_case for functions, PascalCase for classes**:
```python
# ✅ Good: Consistent naming
class UserService:
    def create_user(self, email: str) -> User:
        pass

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        pass

    def update_user_email(self, user_id: str, new_email: str) -> None:
        pass

# ❌ Bad: Mixed naming
class userService:  # Should be PascalCase
    def createUser(self, email: str) -> User:  # Should be snake_case
        pass

    def GetUserById(self, userId: str) -> Optional[User]:  # Inconsistent
        pass

    def update_user_Email(self, user_id: str, newEmail: str) -> None:  # Mixed!
        pass
```

**TypeScript: camelCase for functions, PascalCase for types**:
```typescript
// ✅ Good: Consistent naming
interface User {
  userId: string;
  emailAddress: string;
}

function createUser(email: string): User {
  // ...
}

function getUserById(userId: string): User | null {
  // ...
}

// ❌ Bad: Mixed naming
interface user {  // Should be PascalCase
  user_id: string;  // Should be camelCase
  EmailAddress: string;  // Inconsistent
}

function CreateUser(email: string): User {  // Should be camelCase
  // ...
}
```

## Rule 8: Reading Order (Top-Down)

**Problem**: Helper functions defined before they're used

**Solution**: Define functions in the order they're called

**Before** (Bottom-up reading):
```python
def _validate_email(email):
    # ...

def _check_duplicate(email):
    # ...

def _create_user(email, password):
    # ...

def register_user(email, password):
    # Main function at bottom (need to scroll to find it)
    _validate_email(email)
    _check_duplicate(email)
    return _create_user(email, password)
```

**After** (Top-down reading):
```python
def register_user(email, password):
    """Main function at top (easy to find)."""
    _validate_email(email)
    _check_duplicate(email)
    return _create_user(email, password)

def _validate_email(email):
    """Helper functions follow in order they're called."""
    # ...

def _check_duplicate(email):
    # ...

def _create_user(email, password):
    # ...
```

**Benefits**:
- Read code like a story (top to bottom)
- Main logic first, details later
- Easy to navigate

## Rule 9: Parameter Explicitness

**Problem**: Hidden dependencies, global state, side effects

**Solution**: Make all dependencies explicit parameters

**Before** (Hidden dependencies):
```python
# Global state (hidden dependency)
current_user = None

def create_order(items):
    # Where does current_user come from? (not obvious)
    if not current_user:
        raise Error("Not authenticated")

    total = calculate_total(items)

    # Hidden dependency on database global
    db.save_order(current_user.id, items, total)
```

**After** (Explicit dependencies):
```python
def create_order(user: User, items: List[Item], db: Database) -> Order:
    """Create order for user (all dependencies explicit)."""
    if not user:
        raise Error("Not authenticated")

    total = calculate_total(items)
    return db.save_order(user.id, items, total)

# Usage makes dependencies clear
order = create_order(
    user=get_current_user(),
    items=cart.items,
    db=get_database()
)
```

**Benefits**:
- Clear what function needs
- Easy to test (pass mock dependencies)
- No hidden side effects

## Rule 10: Type Hints

**Problem**: Unclear function contracts

**Solution**: Add type hints for parameters and return values

**Before** (No types):
```python
def calculate_discount(price, discount_code):
    # What types are these? Return type?
    if discount_code:
        return price * (1 - discount_code.value / 100)
    return price
```

**After** (With types):
```python
from typing import Optional

def calculate_discount(
    price: float,
    discount_code: Optional[DiscountCode]
) -> float:
    """Calculate price after discount."""
    if discount_code:
        return price * (1 - discount_code.value / 100)
    return price
```

**Benefits**:
- Clear function contract
- IDE autocomplete and validation
- Catch type errors at compile time
- Self-documenting

## Applying the Rules: Decision Tree

```
Start with messy code
    ↓
Is it nested >3 levels?
    Yes → Rule 1: Guard Clauses
    ↓
Does function do >1 thing?
    Yes → Rule 2: Extract Functions
    ↓
Are conditions complex?
    Yes → Rule 3: Explaining Variables
    ↓
Are there magic numbers?
    Yes → Rule 4: Explaining Constants
    ↓
Is similar code inconsistent?
    Yes → Rule 5: Symmetry
    ↓
Is there commented/unused code?
    Yes → Rule 6: Delete Dead Code
    ↓
Are naming conventions mixed?
    Yes → Rule 7: Consistent Naming
    ↓
Are helpers before main logic?
    Yes → Rule 8: Reading Order
    ↓
Are dependencies hidden?
    Yes → Rule 9: Parameter Explicitness
    ↓
Are types unclear?
    Yes → Rule 10: Type Hints
    ↓
Measure complexity reduction
```

## Measuring Improvement

**Before Refactoring**:
```python
def complex_function():
    if condition1:
        if condition2:
            if condition3:
                # 8 responsibilities mixed together
                # 150 lines
                # Cyclomatic complexity: 34
                pass
```

**Metrics**:
- Cyclomatic Complexity: 34
- Lines of Code: 150
- Nesting Depth: 8
- Functions: 1

**After Refactoring** (applying rules 1-10):
```python
def orchestrator_function():
    validate_preconditions()
    result = process_data()
    handle_result(result)
    return result
```

**Metrics**:
- Cyclomatic Complexity: 3 (-91%)
- Lines of Code: 175 (+25 lines, but 8 focused functions)
- Nesting Depth: 1 (-87%)
- Functions: 8 (each < 20 lines)

**Result**: Much more maintainable despite slightly more total lines

## Quick Reference Card

| Rule | When to Apply | Impact |
|------|---------------|--------|
| 1. Guard Clauses | Nesting > 3 levels | -60-80% complexity |
| 2. Extract Functions | Function > 30 lines or multiple responsibilities | +50-70% maintainability |
| 3. Explaining Variables | Complex boolean conditions | +40% readability |
| 4. Explaining Constants | Magic numbers present | +30% clarity |
| 5. Symmetry | Similar operations inconsistent | +35% pattern recognition |
| 6. Delete Dead Code | Comments/unused code | -10-20% LOC |
| 7. Consistent Naming | Mixed conventions | +25% readability |
| 8. Reading Order | Bottom-up organization | +30% navigability |
| 9. Parameter Explicitness | Global state/hidden deps | +60% testability |
| 10. Type Hints | Unclear contracts | +40% safety |

---

Related: [Security Checklist](security-checklist.md) | [Code Quality Metrics](code-quality-metrics.md) | [Return to INDEX](INDEX.md)
