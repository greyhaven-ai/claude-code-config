# TDD Methodologies

Comprehensive comparison of TDD approaches - Chicago School, London School, ATDD, BDD, Outside-In, Inside-Out, and Hexagonal TDD.

## Overview

```
Methodology        | Focus              | Test Doubles    | Start Point
-------------------|--------------------|-----------------|------------------
Chicago School     | State testing      | Minimal mocking | Domain logic
London School      | Interaction testing| Heavy mocking   | Collaborations
ATDD              | Acceptance criteria| Integration     | User stories
BDD               | Behavior scenarios | Given-When-Then | Features
Outside-In        | API-first          | Mocks           | User interface
Inside-Out        | Domain-first       | Real objects    | Core logic
Hexagonal TDD     | Ports & adapters   | Adapters        | Domain boundaries
```

---

## 1. Chicago School (Classicist/Detroit School)

### Philosophy

**State-based testing** with **minimal mocking**. Test the **state** of the system after operations.

### Principles

- ✅ Use real collaborators when possible
- ✅ Mock only external dependencies (database, API, filesystem)
- ✅ Test through public interfaces
- ✅ Focus on final state, not interactions

### Example

```python
# Chicago School - Testing state
class TestShoppingCart:
    def test_add_item_increases_total(self):
        # Arrange
        cart = ShoppingCart()  # Real object
        product = Product(price=29.99)  # Real object

        # Act
        cart.add_item(product, quantity=2)

        # Assert
        assert cart.total == 59.98  # Test final STATE
        assert len(cart.items) == 1
```

### When to Use

✅ **Good for**:
- Domain logic
- Business rules
- Algorithms
- Data transformations
- Simple dependencies

❌ **Avoid when**:
- Many external dependencies
- Slow dependencies (database, API)
- Complex collaborator setup

### Pros & Cons

**Pros**:
- ✅ Tests reflect real system behavior
- ✅ Easier to refactor (tests less coupled to implementation)
- ✅ Fewer mocks to maintain
- ✅ Catches integration issues

**Cons**:
- ❌ Slower tests (real objects)
- ❌ Harder to isolate failures
- ❌ Complex setup for many dependencies

---

## 2. London School (Mockist)

### Philosophy

**Interaction-based testing** with **heavy mocking**. Test **interactions** between objects.

### Principles

- ✅ Mock all collaborators
- ✅ Test one class in complete isolation
- ✅ Verify method calls and interactions
- ✅ Design emerges from mocking needs

### Example

```python
# London School - Testing interactions
class TestOrderService:
    def test_place_order_calls_payment_gateway(self):
        # Arrange
        payment_gateway = Mock()  # Mock collaborator
        inventory = Mock()        # Mock collaborator
        email_service = Mock()    # Mock collaborator

        service = OrderService(payment_gateway, inventory, email_service)

        # Act
        service.place_order(order_data)

        # Assert - Verify INTERACTIONS
        payment_gateway.charge.assert_called_once_with(amount=100.00)
        inventory.reserve_items.assert_called_once()
        email_service.send_confirmation.assert_called_once()
```

### When to Use

✅ **Good for**:
- Microservices architecture
- Layered architecture (API → Service → Repository)
- Complex collaborations
- Designing new systems (outside-in TDD)

❌ **Avoid when**:
- Simple business logic
- Algorithm implementation
- Minimal dependencies
- Rapid prototyping

### Pros & Cons

**Pros**:
- ✅ Fast tests (mocks are lightweight)
- ✅ Easy to isolate failures
- ✅ Forces good design (loose coupling)
- ✅ Clear interfaces emerge

**Cons**:
- ❌ Tests coupled to implementation
- ❌ Refactoring breaks tests
- ❌ Many mocks to maintain
- ❌ Can miss integration bugs

---

## 3. ATDD (Acceptance Test-Driven Development)

### Philosophy

**Customer-focused testing**. Write acceptance tests from user stories BEFORE implementation.

### Principles

- ✅ Three Amigos (Product Owner, Developer, Tester)
- ✅ Acceptance criteria define "done"
- ✅ Tests written in business language
- ✅ End-to-end testing

### Example

```python
# ATDD - User story acceptance test
"""
User Story: As a customer, I want to reset my password
            so that I can regain access to my account.

Acceptance Criteria:
1. System sends reset email when user requests it
2. Email contains unique reset link valid for 1 hour
3. User can set new password using link
4. Old password no longer works after reset
"""

class TestPasswordReset:
    def test_customer_can_reset_forgotten_password(self):
        # Given a registered customer
        customer = create_customer(email="john@example.com")

        # When they request password reset
        response = client.post("/password/reset", json={
            "email": "john@example.com"
        })

        # Then reset email is sent
        assert response.status_code == 200
        assert email_sent_to("john@example.com")

        # And email contains valid reset link
        reset_link = get_reset_link_from_email()
        assert reset_link_valid_for_1_hour(reset_link)

        # When customer clicks link and sets new password
        client.post(reset_link, json={"new_password": "new-secret"})

        # Then they can login with new password
        response = client.post("/login", json={
            "email": "john@example.com",
            "password": "new-secret"
        })
        assert response.status_code == 200

        # And old password no longer works
        response = client.post("/login", json={
            "email": "john@example.com",
            "password": "old-secret"
        })
        assert response.status_code == 401
```

### When to Use

✅ **Good for**:
- User-facing features
- Customer requirements
- Business-driven development
- Complex workflows

❌ **Avoid when**:
- Technical infrastructure
- Internal APIs
- Performance optimization
- Refactoring tasks

### Pros & Cons

**Pros**:
- ✅ Validates business value
- ✅ Clear definition of "done"
- ✅ Shared understanding (3 Amigos)
- ✅ Catches requirement misunderstandings early

**Cons**:
- ❌ Slow tests (full integration)
- ❌ Requires stakeholder involvement
- ❌ Can be brittle (UI changes break tests)

---

## 4. BDD (Behavior-Driven Development)

### Philosophy

**Behavior specification in natural language**. Tests describe WHAT system does, not HOW.

### Principles

- ✅ Given-When-Then format
- ✅ Business-readable scenarios
- ✅ Living documentation
- ✅ Executable specifications

### Example (Gherkin/Cucumber)

```gherkin
# BDD - Feature file
Feature: Shopping Cart Discounts
  As a customer
  I want to receive bulk discounts
  So that I save money on large orders

  Scenario: 10% discount for 10+ items
    Given I have an empty shopping cart
    When I add 12 units of "Widget" at $10.00 each
    Then the subtotal should be $120.00
    And a 10% discount should be applied
    And the total should be $108.00

  Scenario: 20% discount for 20+ items
    Given I have an empty shopping cart
    When I add 25 units of "Gadget" at $20.00 each
    Then the subtotal should be $500.00
    And a 20% discount should be applied
    And the total should be $400.00
```

```python
# BDD - Step definitions
from behave import given, when, then

@given('I have an empty shopping cart')
def step_empty_cart(context):
    context.cart = ShoppingCart()

@when('I add {quantity:d} units of "{product}" at ${price:f} each')
def step_add_items(context, quantity, product, price):
    context.cart.add_item(product, quantity, price)

@then('the total should be ${expected:f}')
def step_verify_total(context, expected):
    assert context.cart.total == expected
```

### When to Use

✅ **Good for**:
- Customer-facing features
- Complex business rules
- Living documentation
- Stakeholder communication

❌ **Avoid when**:
- Low-level algorithms
- Technical infrastructure
- Performance optimization

### Pros & Cons

**Pros**:
- ✅ Business-readable tests
- ✅ Living documentation
- ✅ Bridges business-technical gap
- ✅ Clear acceptance criteria

**Cons**:
- ❌ Setup overhead (Gherkin + step definitions)
- ❌ Can be verbose
- ❌ Maintenance burden

---

## 5. Outside-In TDD

### Philosophy

**Start from the outside** (user interface/API) and work inward through layers.

### Principles

- ✅ Start with acceptance test
- ✅ Mock collaborators as you go deeper
- ✅ Implement layers top-down
- ✅ Remove mocks layer by layer

### Workflow

```
1. Write acceptance test (API level) - FAILS
   ↓
2. Write service layer test (mock repository) - FAILS
   ↓
3. Implement service layer - acceptance test still fails
   ↓
4. Write repository layer test (mock database) - FAILS
   ↓
5. Implement repository layer - acceptance test PASSES
   ↓
6. Remove mocks, use real implementations
```

### Example

```python
# Step 1: Acceptance test (outside)
def test_get_user_profile(client):
    response = client.get("/users/123")
    assert response.json()["email"] == "john@example.com"

# Step 2: Service layer test (mock repository)
def test_user_service_get_user(mocker):
    mock_repo = mocker.Mock()
    mock_repo.find_by_id.return_value = User(email="john@example.com")

    service = UserService(mock_repo)
    user = service.get_user("123")

    assert user.email == "john@example.com"

# Step 3: Repository layer test (mock database)
def test_repository_find_by_id(session):
    repo = UserRepository(session)
    user = repo.find_by_id("123")
    assert user is not None
```

### When to Use

✅ **Good for**:
- New features
- Clean architecture
- Layered systems
- API-first development

❌ **Avoid when**:
- Refactoring existing code
- Algorithmic problems
- Simple CRUD operations

### Pros & Cons

**Pros**:
- ✅ User-focused development
- ✅ API contract defined early
- ✅ Clean layer boundaries
- ✅ Mockable design

**Cons**:
- ❌ Many mocks initially
- ❌ Requires architectural discipline
- ❌ Can over-design

---

## 6. Inside-Out TDD

### Philosophy

**Start from the inside** (domain logic) and work outward to UI.

### Principles

- ✅ Start with core domain logic
- ✅ Use real objects (minimal mocking)
- ✅ Build foundation first
- ✅ UI/API added last

### Workflow

```
1. Write domain model test - FAILS
   ↓
2. Implement domain model - PASSES
   ↓
3. Write repository test - FAILS
   ↓
4. Implement repository - PASSES
   ↓
5. Write service test - FAILS
   ↓
6. Implement service - PASSES
   ↓
7. Write API test - FAILS
   ↓
8. Implement API - PASSES
```

### Example

```python
# Step 1: Domain logic (inside)
def test_order_calculates_total():
    order = Order()
    order.add_item(price=10.00, quantity=2)
    assert order.total == 20.00

# Step 2: Repository layer
def test_repository_saves_order(session):
    order = Order(total=20.00)
    repo = OrderRepository(session)
    saved = repo.save(order)
    assert saved.id is not None

# Step 3: Service layer
def test_service_creates_order():
    service = OrderService(repo=OrderRepository())
    order = service.create_order(items=[...])
    assert order.total == 20.00

# Step 4: API layer (outside)
def test_api_create_order(client):
    response = client.post("/orders", json={...})
    assert response.status_code == 201
```

### When to Use

✅ **Good for**:
- Complex domain logic
- Algorithms
- Core business rules
- Refactoring existing systems

❌ **Avoid when**:
- User stories drive development
- API contract must be defined early
- Microservices (need clear boundaries upfront)

### Pros & Cons

**Pros**:
- ✅ Solid foundation (domain logic first)
- ✅ Fewer mocks
- ✅ Real object interactions
- ✅ Simpler tests

**Cons**:
- ❌ API design deferred
- ❌ May not match user needs
- ❌ Rework if requirements change

---

## 7. Hexagonal TDD (Ports & Adapters)

### Philosophy

**Test domain logic in isolation** from infrastructure using ports (interfaces) and adapters (implementations).

### Principles

- ✅ Domain logic depends on ports (interfaces)
- ✅ Adapters implement ports
- ✅ Test domain with mock adapters
- ✅ Test real adapters separately

### Architecture

```
┌─────────────────────────────────────────┐
│          Domain Logic (Core)            │
│  - Business rules                       │
│  - Entities                             │
│  - Use cases                            │
└─────────────────┬───────────────────────┘
                  │ depends on
                  ↓
┌─────────────────────────────────────────┐
│           Ports (Interfaces)            │
│  - Repository port                      │
│  - Email port                           │
│  - Payment port                         │
└─────────────────┬───────────────────────┘
                  │ implemented by
                  ↓
┌─────────────────────────────────────────┐
│          Adapters (Infrastructure)      │
│  - PostgreSQL adapter                   │
│  - SendGrid adapter                     │
│  - Stripe adapter                       │
└─────────────────────────────────────────┘
```

### Example

```python
# Port (interface)
class PaymentPort:
    """Port for payment processing."""
    def charge(self, amount: float, payment_info: dict) -> PaymentResult:
        raise NotImplementedError

# Domain logic (depends on port)
class OrderService:
    def __init__(self, payment_port: PaymentPort):
        self.payment = payment_port

    def place_order(self, order: Order):
        result = self.payment.charge(order.total, order.payment_info)
        if not result.success:
            raise PaymentError()
        order.status = "paid"
        return order

# Test with mock adapter
def test_order_service_processes_payment():
    mock_payment = Mock(spec=PaymentPort)
    mock_payment.charge.return_value = PaymentResult(success=True)

    service = OrderService(payment_port=mock_payment)
    order = service.place_order(Order(total=100.00))

    assert order.status == "paid"
    mock_payment.charge.assert_called_once()

# Real adapter (Stripe)
class StripePaymentAdapter(PaymentPort):
    def charge(self, amount, payment_info):
        stripe_result = stripe.Charge.create(
            amount=int(amount * 100),
            currency="usd",
            source=payment_info["token"]
        )
        return PaymentResult(success=stripe_result.paid)

# Test real adapter separately
def test_stripe_adapter_charges_card():
    adapter = StripePaymentAdapter()
    result = adapter.charge(100.00, {"token": "tok_visa"})
    assert result.success is True
```

### When to Use

✅ **Good for**:
- Complex domain logic
- Multiple infrastructure options (Postgres, MySQL, MongoDB)
- Microservices
- Clean architecture

❌ **Avoid when**:
- Simple CRUD applications
- Tightly coupled to specific infrastructure
- Rapid prototyping

### Pros & Cons

**Pros**:
- ✅ Domain logic completely isolated
- ✅ Easy to swap infrastructure
- ✅ Testable without external dependencies
- ✅ Clear boundaries

**Cons**:
- ❌ More abstractions (ports + adapters)
- ❌ Boilerplate code
- ❌ Overkill for simple apps

---

## Decision Matrix

### Choose Methodology Based On

| If you have... | Use... | Why... |
|----------------|--------|--------|
| Simple business logic | Chicago School | Minimal mocking, straightforward |
| Layered architecture | London School | Clear layer isolation |
| User stories | ATDD | Business-driven development |
| Stakeholder involvement | BDD | Shared language |
| New feature | Outside-In | API contract first |
| Core algorithm | Inside-Out | Domain logic first |
| Complex domain | Hexagonal | Infrastructure independence |

---

Related: [Red-Green-Refactor Guide](red-green-refactor-guide.md) | [Coverage Thresholds](coverage-thresholds.md) | [Mutation Testing Reference](mutation-testing-reference.md) | [Return to INDEX](INDEX.md)
