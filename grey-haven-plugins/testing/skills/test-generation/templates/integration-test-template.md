# Integration Test Template

Templates for integration tests covering API endpoints, database interactions, and multi-component workflows.

## TypeScript Integration Test

### API Integration Test (with TanStack Query)

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FeatureComponent } from './FeatureComponent';

describe('FeatureComponent Integration', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });

    // CUSTOMIZE: Mock API endpoints
    global.fetch = vi.fn();
  });

  afterEach(() => {
    queryClient.clear();
  });

  function renderWithProviders(ui: React.ReactElement) {
    return render(
      <QueryClientProvider client={queryClient}>
        {ui}
      </QueryClientProvider>
    );
  }

  describe('Complete User Flow', () => {
    it('should load data, allow edits, and save changes', async () => {
      // CUSTOMIZE: Mock initial data fetch
      (global.fetch as any)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ id: '123', name: 'John Doe', email: 'john@example.com' }),
        })
        // Mock update request
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ id: '123', name: 'Jane Doe', email: 'john@example.com' }),
        });

      // Render component
      renderWithProviders(<FeatureComponent userId="123" />);

      // Wait for data to load
      await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
      });

      // Edit name
      const nameInput = screen.getByLabelText(/name/i);
      fireEvent.change(nameInput, { target: { value: 'Jane Doe' } });

      // Submit form
      const submitButton = screen.getByRole('button', { name: /save/i });
      fireEvent.click(submitButton);

      // Wait for update to complete
      await waitFor(() => {
        expect(screen.getByText('Jane Doe')).toBeInTheDocument();
      });

      // Verify API calls
      expect(fetch).toHaveBeenCalledTimes(2);
      expect(fetch).toHaveBeenNthCalledWith(2, '/api/users/123', {
        method: 'PATCH',
        body: JSON.stringify({ name: 'Jane Doe' }),
        headers: { 'Content-Type': 'application/json' },
      });
    });

    it('should handle API errors gracefully', async () => {
      // CUSTOMIZE: Mock API error
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ error: 'Server error' }),
      });

      renderWithProviders(<FeatureComponent userId="123" />);

      // Wait for error message
      await waitFor(() => {
        expect(screen.getByText(/error loading data/i)).toBeInTheDocument();
      });
    });
  });

  describe('Multi-Step Workflow', () => {
    it('should complete checkout process', async () => {
      // CUSTOMIZE: Mock multiple API calls
      (global.fetch as any)
        // 1. Load cart
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ items: [{ id: '1', price: 99.99 }], total: 99.99 }),
        })
        // 2. Validate address
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ valid: true }),
        })
        // 3. Process payment
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ success: true, orderId: 'order-123' }),
        });

      renderWithProviders(<CheckoutFlow />);

      // Step 1: Review cart
      await waitFor(() => {
        expect(screen.getByText('$99.99')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /continue/i }));

      // Step 2: Enter shipping info
      await waitFor(() => {
        expect(screen.getByLabelText(/address/i)).toBeInTheDocument();
      });

      fireEvent.change(screen.getByLabelText(/address/i), {
        target: { value: '123 Main St' },
      });

      fireEvent.click(screen.getByRole('button', { name: /continue/i }));

      // Step 3: Payment
      await waitFor(() => {
        expect(screen.getByText(/payment/i)).toBeInTheDocument();
      });

      fireEvent.change(screen.getByLabelText(/card number/i), {
        target: { value: '4242424242424242' },
      });

      fireEvent.click(screen.getByRole('button', { name: /place order/i }));

      // Wait for confirmation
      await waitFor(() => {
        expect(screen.getByText(/order confirmed/i)).toBeInTheDocument();
        expect(screen.getByText('order-123')).toBeInTheDocument();
      });

      // Verify all API calls made
      expect(fetch).toHaveBeenCalledTimes(3);
    });
  });
});
```

## Python Integration Test

### FastAPI Integration Test

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app, get_session
from app.models import User, Order, Product

@pytest.fixture(name="engine")
def engine_fixture():
    """Create test database engine"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(name="session")
def session_fixture(engine):
    """Create test database session"""
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

class TestCompleteOrderFlow:
    """Integration tests for complete order flow"""

    def test_complete_purchase_flow(self, client: TestClient, session: Session):
        """
        Should complete full purchase flow:
        1. Create user
        2. Add products to cart
        3. Create order
        4. Process payment
        5. Verify inventory updated
        """
        # Step 1: Create user
        user_response = client.post("/users", json={
            "name": "John Doe",
            "email": "john@example.com",
            "role": "member",
        })
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        # Step 2: Create products
        product1 = Product(name="Product 1", price=50.00, inventory=10)
        product2 = Product(name="Product 2", price=25.00, inventory=5)
        session.add(product1)
        session.add(product2)
        session.commit()
        session.refresh(product1)
        session.refresh(product2)

        # Step 3: Add products to cart
        cart_response = client.post(f"/users/{user_id}/cart", json={
            "items": [
                {"product_id": product1.id, "quantity": 2},
                {"product_id": product2.id, "quantity": 1},
            ],
        })
        assert cart_response.status_code == 201

        # Step 4: Create order
        order_response = client.post(f"/users/{user_id}/orders", json={
            "shipping_address": "123 Main St",
            "billing_address": "123 Main St",
        })
        assert order_response.status_code == 201
        order_data = order_response.json()
        assert order_data["total"] == 125.00  # 50*2 + 25*1
        assert order_data["status"] == "pending"

        # Step 5: Process payment
        payment_response = client.post(f"/orders/{order_data['id']}/payment", json={
            "amount": 125.00,
            "payment_method": "card",
            "token": "tok_visa",
        })
        assert payment_response.status_code == 200
        assert payment_response.json()["status"] == "succeeded"

        # Step 6: Verify order updated
        updated_order = client.get(f"/orders/{order_data['id']}").json()
        assert updated_order["status"] == "completed"

        # Step 7: Verify inventory decremented
        session.refresh(product1)
        session.refresh(product2)
        assert product1.inventory == 8  # 10 - 2
        assert product2.inventory == 4  # 5 - 1

    def test_payment_failure_rollback(self, client: TestClient, session: Session):
        """Should rollback order when payment fails"""
        # CUSTOMIZE: Setup user and products
        user = User(name="John", email="john@example.com", role="member")
        product = Product(name="Test Product", price=100.00, inventory=10)
        session.add(user)
        session.add(product)
        session.commit()
        session.refresh(user)
        session.refresh(product)

        # Create order
        order_response = client.post(f"/users/{user.id}/orders", json={
            "items": [{"product_id": product.id, "quantity": 1}],
            "shipping_address": "123 Main St",
        })
        order_id = order_response.json()["id"]

        # Attempt payment with invalid token (should fail)
        payment_response = client.post(f"/orders/{order_id}/payment", json={
            "amount": 100.00,
            "payment_method": "card",
            "token": "tok_invalid",
        })

        # Verify payment failed
        assert payment_response.status_code == 400

        # Verify order still pending
        order = client.get(f"/orders/{order_id}").json()
        assert order["status"] == "pending"

        # Verify inventory NOT decremented
        session.refresh(product)
        assert product.inventory == 10
```

### Database Integration Test

```python
import pytest
from sqlmodel import Session, select
from app.models import User, Team, Membership
from app.services import TeamService

class TestTeamServiceIntegration:
    """Integration tests for team service with database"""

    @pytest.fixture
    def service(self, session: Session):
        """Create team service with real database"""
        return TeamService(session)

    def test_create_team_with_members(self, service: TeamService, session: Session):
        """Should create team and add members in single transaction"""
        # Create users
        user1 = User(name="Alice", email="alice@example.com", role="member")
        user2 = User(name="Bob", email="bob@example.com", role="member")
        session.add(user1)
        session.add(user2)
        session.commit()

        # Create team with members
        team = service.create_team_with_members(
            name="Engineering",
            member_ids=[user1.id, user2.id],
        )

        # Verify team created
        assert team.id is not None
        assert team.name == "Engineering"

        # Verify memberships created
        memberships = session.exec(
            select(Membership).where(Membership.team_id == team.id)
        ).all()
        assert len(memberships) == 2

        # Verify users associated
        team_users = [m.user_id for m in memberships]
        assert user1.id in team_users
        assert user2.id in team_users

    def test_transaction_rollback_on_error(self, service: TeamService, session: Session):
        """Should rollback transaction when error occurs"""
        user = User(name="Alice", email="alice@example.com", role="member")
        session.add(user)
        session.commit()

        # Attempt to create team with invalid member (should fail)
        with pytest.raises(ValueError):
            service.create_team_with_members(
                name="Engineering",
                member_ids=[user.id, "invalid-id"],  # Invalid ID
            )

        # Verify no team created (transaction rolled back)
        teams = session.exec(select(Team)).all()
        assert len(teams) == 0

        # Verify no memberships created
        memberships = session.exec(select(Membership)).all()
        assert len(memberships) == 0
```

### Multi-Service Integration Test

```python
import pytest
from unittest.mock import Mock, patch
from app.services import OrderService, InventoryService, PaymentService, EmailService

class TestOrderServiceIntegration:
    """Integration tests with multiple services"""

    @pytest.fixture
    def services(self, session):
        """Setup all services"""
        return {
            'inventory': InventoryService(session),
            'payment': Mock(spec=PaymentService),  # Mock external service
            'email': Mock(spec=EmailService),      # Mock external service
            'order': None,  # Will be created with other services
        }

    def test_complete_order_flow_with_services(self, services, session):
        """Should coordinate between multiple services"""
        # Setup mocks
        services['payment'].charge.return_value = {
            'success': True,
            'transaction_id': 'txn_123',
        }
        services['email'].send_confirmation.return_value = True

        # Create order service with all dependencies
        order_service = OrderService(
            session=session,
            inventory_service=services['inventory'],
            payment_service=services['payment'],
            email_service=services['email'],
        )

        # Setup test data
        product = Product(name="Test", price=100.00, inventory=10)
        session.add(product)
        session.commit()

        # Create order
        order = order_service.create_order({
            'user_id': 'user-123',
            'items': [{'product_id': product.id, 'quantity': 2}],
        })

        # Verify order created
        assert order.id is not None
        assert order.total == 200.00

        # Verify inventory updated (real service)
        session.refresh(product)
        assert product.inventory == 8

        # Verify payment processed (mocked service)
        services['payment'].charge.assert_called_once_with(200.00)

        # Verify email sent (mocked service)
        services['email'].send_confirmation.assert_called_once()
```

## Usage Instructions

1. **Copy template** to your integration test file
2. **Customize mocks** for external services
3. **Setup test database** with fixtures
4. **Add test scenarios** for complete workflows
5. **Verify all side effects** (database changes, API calls, etc.)
6. **Run tests**: `npm test integration/` or `pytest tests/integration/`

## Checklist

- [ ] Complete user flow tested end-to-end
- [ ] Multiple API calls tested in sequence
- [ ] Database transactions tested
- [ ] Rollback behavior tested on errors
- [ ] External services mocked appropriately
- [ ] All side effects verified
- [ ] Multi-step workflows tested
- [ ] Error recovery tested

---

Related: [Unit Test Template](unit-test-template.md) | [Test Fixtures Template](test-fixtures-template.md) | [Return to INDEX](INDEX.md)
