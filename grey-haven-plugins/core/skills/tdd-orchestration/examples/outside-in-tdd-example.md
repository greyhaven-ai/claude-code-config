# Outside-In TDD Example: Order Processing System

Feature-first TDD approach starting with acceptance tests and working inward through architectural layers.

## Scenario

**Feature**: Place order with payment processing
**User Story**: "As a customer, I want to place an order so that I can purchase products"
**Architecture**: API → Service → Repository → Database
**Methodology**: Outside-In TDD (London School)
**Timeline**: 4 days, 95% coverage, zero production defects

## Overview: Outside-In vs Inside-Out

### Outside-In (Feature-First)
```
Start: Acceptance Test (API level)
  ↓
Mock: Service layer
  ↓
Implement: Service (mock Repository)
  ↓
Implement: Repository (mock Database)
  ↓
Integrate: Remove mocks layer by layer
```

**Benefits**:
- ✅ User-focused: Starts with customer value
- ✅ Architecture-driven: Enforces clean boundaries
- ✅ Early feedback: API contract defined upfront
- ✅ Mockable: Easy to isolate layers

### Inside-Out (Component-First)
```
Start: Unit tests for domain models
  ↓
Implement: Repository layer
  ↓
Implement: Service layer
  ↓
Finally: API layer integration
```

**Benefits**:
- ✅ Foundation-first: Core logic solid before UI
- ✅ Minimal mocking: Real collaborators preferred
- ✅ Simple: No complex mock setup

---

## Day 1: Acceptance Test (API Layer)

### Step 1: RED - Write Acceptance Test

**Time**: 45 minutes

```python
# tests/acceptance/test_place_order.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_place_order_with_valid_payment(client):
    """
    Acceptance Criteria:
    - Customer can place order with credit card
    - Order total calculated correctly
    - Payment processed
    - Order confirmation returned
    """
    # Arrange
    order_data = {
        "customer_id": "cust-123",
        "items": [
            {"product_id": "prod-456", "quantity": 2, "price": 29.99},
            {"product_id": "prod-789", "quantity": 1, "price": 49.99},
        ],
        "payment": {
            "method": "credit_card",
            "card_number": "4242424242424242",
            "cvv": "123",
            "exp_month": "12",
            "exp_year": "2025",
        },
        "shipping_address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94102",
        },
    }

    # Act
    response = client.post("/api/orders", json=order_data)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["order_id"] is not None
    assert data["total"] == 109.97  # (29.99 * 2) + 49.99
    assert data["status"] == "confirmed"
    assert data["payment_status"] == "paid"
    assert "confirmation_number" in data
```

### Step 2: Run Test (Verify RED)

```bash
$ pytest tests/acceptance/test_place_order.py

FAILED tests/acceptance/test_place_order.py::test_place_order_with_valid_payment
404 Not Found: /api/orders  # Endpoint doesn't exist yet ✅
```

**✅ RED Phase Success**: Test fails for right reason

### Step 3: GREEN - API Endpoint (Mock Service)

**Time**: 30 minutes

```python
# app/api/orders.py
from fastapi import APIRouter, Depends
from app.services.order_service import OrderService
from app.schemas import OrderCreate, OrderResponse

router = APIRouter()

def get_order_service() -> OrderService:
    """Dependency injection for OrderService."""
    return OrderService()

@router.post("/orders", response_model=OrderResponse, status_code=201)
async def place_order(
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    """Place a new order with payment processing."""
    return service.place_order(order_data)
```

**At this point**: Service doesn't exist yet! We're designing the interface.

---

## Day 2: Service Layer

### Step 1: RED - Service Unit Test (Mock Repository)

**Time**: 30 minutes

```python
# tests/unit/test_order_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.order_service import OrderService
from app.schemas import OrderCreate

@pytest.fixture
def mock_order_repo():
    """Mock repository for testing service in isolation."""
    repo = Mock()
    repo.create_order.return_value = {
        "id": "order-123",
        "status": "pending",
        "total": 109.97,
    }
    return repo

@pytest.fixture
def mock_payment_gateway():
    """Mock payment gateway for testing."""
    gateway = Mock()
    gateway.process_payment.return_value = {
        "success": True,
        "transaction_id": "txn-456",
    }
    return gateway

def test_place_order_calculates_total_correctly(
    mock_order_repo,
    mock_payment_gateway,
):
    """Should calculate order total from items."""
    # Arrange
    service = OrderService(
        order_repo=mock_order_repo,
        payment_gateway=mock_payment_gateway,
    )

    order_data = OrderCreate(
        customer_id="cust-123",
        items=[
            {"product_id": "prod-456", "quantity": 2, "price": 29.99},
            {"product_id": "prod-789", "quantity": 1, "price": 49.99},
        ],
        payment={"method": "credit_card", "card_number": "4242..."},
        shipping_address={"street": "123 Main St", ...},
    )

    # Act
    result = service.place_order(order_data)

    # Assert
    assert result["total"] == 109.97  # (29.99 * 2) + 49.99
    assert result["status"] == "confirmed"

    # Verify repository called correctly
    mock_order_repo.create_order.assert_called_once()
    created_order = mock_order_repo.create_order.call_args[0][0]
    assert created_order.total == 109.97

    # Verify payment processed
    mock_payment_gateway.process_payment.assert_called_once()
```

### Step 2: Run Test (Verify RED)

```bash
$ pytest tests/unit/test_order_service.py

FAILED tests/unit/test_order_service.py::test_place_order_calculates_total_correctly
ImportError: cannot import name 'OrderService' from 'app.services'
```

**✅ RED Phase Success**

### Step 3: GREEN - Implement Service

**Time**: 1 hour

```python
# app/services/order_service.py
from app.schemas import OrderCreate, OrderResponse
from app.repositories.order_repository import OrderRepository
from app.gateways.payment_gateway import PaymentGateway

class OrderService:
    """Business logic for order processing."""

    def __init__(
        self,
        order_repo: OrderRepository,
        payment_gateway: PaymentGateway,
    ):
        self.order_repo = order_repo
        self.payment_gateway = payment_gateway

    def place_order(self, order_data: OrderCreate) -> OrderResponse:
        """
        Place order with payment processing.

        Steps:
        1. Calculate total
        2. Validate inventory
        3. Process payment
        4. Create order record
        5. Return confirmation
        """
        # Step 1: Calculate total
        total = self._calculate_total(order_data.items)

        # Step 2: Validate inventory (stubbed for now)
        # Will implement when repository exists

        # Step 3: Process payment
        payment_result = self.payment_gateway.process_payment(
            amount=total,
            payment_info=order_data.payment,
        )

        if not payment_result["success"]:
            raise PaymentFailedError("Payment processing failed")

        # Step 4: Create order
        order = self.order_repo.create_order(
            customer_id=order_data.customer_id,
            items=order_data.items,
            total=total,
            payment_transaction_id=payment_result["transaction_id"],
            shipping_address=order_data.shipping_address,
        )

        # Step 5: Return confirmation
        return OrderResponse(
            order_id=order["id"],
            total=order["total"],
            status="confirmed",
            payment_status="paid",
            confirmation_number=self._generate_confirmation_number(),
        )

    def _calculate_total(self, items: list) -> float:
        """Calculate order total from items."""
        return sum(item["price"] * item["quantity"] for item in items)

    def _generate_confirmation_number(self) -> str:
        """Generate unique confirmation number."""
        import uuid
        return f"CONF-{uuid.uuid4().hex[:8].upper()}"
```

### Step 4: Run Service Tests

```bash
$ pytest tests/unit/test_order_service.py

PASSED tests/unit/test_order_service.py::test_place_order_calculates_total_correctly ✅

Coverage: app/services/order_service.py: 92%
```

**Note**: Acceptance test still fails because repository/gateway don't exist!

---

## Day 3: Repository Layer

### Step 1: RED - Repository Test

**Time**: 20 minutes

```python
# tests/unit/test_order_repository.py
import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.repositories.order_repository import OrderRepository
from app.models import Order

@pytest.fixture
def session():
    """Create test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_order_saves_to_database(session):
    """Should save order to database and return with ID."""
    # Arrange
    repo = OrderRepository(session)

    # Act
    order = repo.create_order(
        customer_id="cust-123",
        items=[{"product_id": "prod-456", "quantity": 2, "price": 29.99}],
        total=59.98,
        payment_transaction_id="txn-456",
        shipping_address={"street": "123 Main St"},
    )

    # Assert
    assert order["id"] is not None
    assert order["customer_id"] == "cust-123"
    assert order["total"] == 59.98

    # Verify saved in database
    db_order = session.query(Order).filter_by(id=order["id"]).first()
    assert db_order is not None
    assert db_order.customer_id == "cust-123"
```

### Step 2: GREEN - Implement Repository

**Time**: 45 minutes

```python
# app/repositories/order_repository.py
from sqlmodel import Session
from app.models import Order, OrderItem

class OrderRepository:
    """Data access layer for orders."""

    def __init__(self, session: Session):
        self.session = session

    def create_order(
        self,
        customer_id: str,
        items: list,
        total: float,
        payment_transaction_id: str,
        shipping_address: dict,
    ) -> dict:
        """Create order record in database."""
        # Create order
        order = Order(
            customer_id=customer_id,
            total=total,
            payment_transaction_id=payment_transaction_id,
            shipping_address=shipping_address,
            status="confirmed",
        )

        self.session.add(order)
        self.session.flush()  # Get order ID

        # Create order items
        for item_data in items:
            item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )
            self.session.add(item)

        self.session.commit()
        self.session.refresh(order)

        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "total": order.total,
            "status": order.status,
        }
```

### Step 3: REFACTOR - Extract Validation

**Time**: 15 minutes

```python
# app/repositories/order_repository.py (refactored)
class OrderRepository:
    def create_order(self, customer_id, items, total, payment_transaction_id, shipping_address):
        """Create order record in database."""
        # Validate before creating
        self._validate_order_data(customer_id, items, total)

        order = self._create_order_record(
            customer_id, total, payment_transaction_id, shipping_address
        )

        self._create_order_items(order.id, items)

        self.session.commit()
        self.session.refresh(order)

        return self._order_to_dict(order)

    def _validate_order_data(self, customer_id, items, total):
        """Validate order data before creation."""
        if not customer_id:
            raise ValueError("customer_id is required")
        if not items:
            raise ValueError("items cannot be empty")
        if total <= 0:
            raise ValueError("total must be positive")

    def _create_order_record(self, customer_id, total, payment_transaction_id, shipping_address):
        """Create order database record."""
        order = Order(
            customer_id=customer_id,
            total=total,
            payment_transaction_id=payment_transaction_id,
            shipping_address=shipping_address,
            status="confirmed",
        )
        self.session.add(order)
        self.session.flush()
        return order

    def _create_order_items(self, order_id, items):
        """Create order item records."""
        for item_data in items:
            item = OrderItem(
                order_id=order_id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )
            self.session.add(item)

    def _order_to_dict(self, order):
        """Convert order model to dictionary."""
        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "total": order.total,
            "status": order.status,
        }
```

---

## Day 4: Integration & Remove Mocks

### Step 1: Integration Test (Real Components)

**Time**: 1 hour

```python
# tests/integration/test_order_integration.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app, get_session

@pytest.fixture
def client():
    """Create test client with real database."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_full_order_flow_with_real_components(client):
    """
    Integration test with real components (no mocks).
    Tests: API → Service → Repository → Database
    """
    # Arrange
    order_data = {
        "customer_id": "cust-123",
        "items": [
            {"product_id": "prod-456", "quantity": 2, "price": 29.99},
            {"product_id": "prod-789", "quantity": 1, "price": 49.99},
        ],
        "payment": {
            "method": "credit_card",
            "card_number": "4242424242424242",
        },
        "shipping_address": {"street": "123 Main St"},
    }

    # Act
    response = client.post("/api/orders", json=order_data)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["order_id"] is not None
    assert data["total"] == 109.97
    assert data["status"] == "confirmed"
    assert data["payment_status"] == "paid"

    # Verify order persisted in database
    order_id = data["order_id"]
    get_response = client.get(f"/api/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["order_id"] == order_id
```

### Step 2: Remove Mocks Layer by Layer

**Service → Repository Integration**:
```python
# Before (mocked repository)
service = OrderService(
    order_repo=Mock(),  # ❌ Mock
    payment_gateway=Mock(),
)

# After (real repository)
service = OrderService(
    order_repo=OrderRepository(session),  # ✅ Real
    payment_gateway=Mock(),  # Still mocked (external)
)
```

**Payment Gateway** (External service - keep mocked in tests):
```python
# tests/ - Mock payment gateway
@pytest.fixture
def mock_payment_gateway():
    with patch('app.gateways.payment_gateway.stripe') as mock:
        mock.charge.return_value = {"success": True, "id": "txn-123"}
        yield mock
```

### Step 3: Final Acceptance Test

```bash
$ pytest tests/acceptance/test_place_order.py

PASSED tests/acceptance/test_place_order.py::test_place_order_with_valid_payment ✅

Coverage Report:
  app/api/orders.py:                95%
  app/services/order_service.py:     98%
  app/repositories/order_repository.py: 92%
  Overall:                          95% ✅
```

---

## Results

### Timeline

| Day | Layer | Tests Written | Tests Passing | Coverage |
|-----|-------|---------------|---------------|----------|
| 1   | API (Acceptance) | 1 | 0 | N/A |
| 2   | Service | 5 | 5 | 98% |
| 3   | Repository | 4 | 4 | 92% |
| 4   | Integration | 3 | 13 (all) | 95% ✅ |

**Total**: 13 tests, 4 days, 95% coverage, zero production defects

### Test Pyramid

```
     /\
    /E2\       1 test (Acceptance)
   /____\
  /      \
 / Integ  \    3 tests (Integration)
/__________\
/            \
/    Unit     \  9 tests (Unit)
/______________\

Distribution: 69% unit, 23% integration, 8% acceptance ✅
Target:       70% unit, 20% integration, 10% E2E
```

### Benefits of Outside-In TDD

**1. User-Focused Development**:
- Started with customer value (place order)
- API contract defined upfront
- Features delivered incrementally

**2. Clean Architecture Enforced**:
- Clear layer boundaries (API → Service → Repository)
- Each layer has single responsibility
- Easy to test in isolation

**3. Mockability**:
- Mocked dependencies during development
- Replaced mocks with real implementations layer by layer
- Final integration tests with zero mocks (except external services)

**4. Fast Feedback**:
- Unit tests run in milliseconds
- Integration tests run in seconds
- Acceptance test validates full flow

---

## Common Pitfalls

### Pitfall #1: Too Many Mocks

**Problem**: Mock everything, including simple objects

```python
# ❌ Bad - Over-mocking
mock_address = Mock()
mock_address.street = "123 Main St"
mock_items = [Mock(), Mock()]
```

**Solution**: Only mock complex/external dependencies

```python
# ✅ Good - Mock external services only
payment_gateway = Mock()  # External service
order_repo = Mock()       # Complex database logic

# Use real objects for simple data
address = {"street": "123 Main St"}  # Plain dict
items = [{"product_id": "p1", "price": 29.99}]  # Plain list
```

### Pitfall #2: Forgetting Integration Tests

**Problem**: All unit tests pass with mocks, but integration fails

**Solution**: Write integration tests to verify layers work together

### Pitfall #3: Mocks Drift from Reality

**Problem**: Mock behavior doesn't match real implementation

```python
# Mock says: "Return list of orders"
mock_repo.get_orders.return_value = [...]

# Real implementation: "Returns paginated response"
repo.get_orders()  # Returns {"items": [...], "page": 1, "total": 100}

# Tests pass, production breaks! 💥
```

**Solution**: Use contract tests or keep mocks aligned with reality

---

Related: [Red-Green-Refactor Example](red-green-refactor-example.md) | [Mutation Testing Example](mutation-testing-example.md) | [TDD Rescue Example](tdd-rescue-example.md) | [Return to INDEX](INDEX.md)
