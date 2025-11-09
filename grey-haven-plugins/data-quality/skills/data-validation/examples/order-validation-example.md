# Order Validation Example

Complete workflow for complex order validation with nested objects, business rules, and database transactions.

## Goal

Build order validation system with:
- Nested validation (order items, shipping address)
- Currency and pricing validation
- Inventory quantity checks
- Multi-tenant validation (tenant_id)
- Custom business rule validators
- Database transaction validation
- FastAPI integration
- Comprehensive test coverage

## Step 1: Define Nested Pydantic Models

### OrderItem Schema

```python
# app/schemas/order.py
from pydantic import BaseModel, Field, field_validator, model_validator, UUID4
from typing import List
from decimal import Decimal
from datetime import datetime

class OrderItemSchema(BaseModel):
    """Order item data contract."""

    product_id: UUID4 = Field(..., description="Product UUID")
    quantity: int = Field(..., ge=1, le=999, description="Quantity (1-999)")
    unit_price: Decimal = Field(..., ge=Decimal("0.01"), max_digits=10, decimal_places=2)

    @field_validator('unit_price')
    @classmethod
    def validate_price_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Unit price must be positive')
        return v

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity


class ShippingAddressSchema(BaseModel):
    """Shipping address data contract."""

    street: str = Field(..., min_length=5, max_length=100)
    city: str = Field(..., min_length=2, max_length=50)
    state: str = Field(..., min_length=2, max_length=2, pattern=r'^[A-Z]{2}$')
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default='US', pattern=r'^[A-Z]{2}$')

    @field_validator('state')
    @classmethod
    def validate_us_state(cls, v: str) -> str:
        valid_states = {'AL', 'AK', 'AZ', 'CA', 'CO', 'FL', 'GA', 'NY', 'TX'}
        if v not in valid_states:
            raise ValueError(f'Invalid US state code: {v}')
        return v


class OrderCreateSchema(BaseModel):
    """Order creation data contract."""

    items: List[OrderItemSchema] = Field(..., min_length=1, max_length=50)
    shipping_address: ShippingAddressSchema
    notes: str | None = Field(default=None, max_length=500)

    @field_validator('items')
    @classmethod
    def validate_unique_products(cls, items: List[OrderItemSchema]):
        product_ids = [item.product_id for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError('Duplicate products in order')
        return items

    @model_validator(mode='after')
    def validate_order_total(self):
        total = sum(item.total_price for item in self.items)
        if total < Decimal("5.00"):
            raise ValueError('Order total must be at least $5.00')
        if total > Decimal("10000.00"):
            raise ValueError('Order total cannot exceed $10,000.00')
        return self

    @property
    def total_amount(self) -> Decimal:
        return sum(item.total_price for item in self.items)

    model_config = {'str_strip_whitespace': True, 'validate_assignment': True}
```

## Step 2: Define SQLModel Schemas

### Order Database Models

```python
# app/models/order.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from typing import List

class Order(SQLModel, table=True):
    """Order model for PostgreSQL."""
    __tablename__ = 'orders'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)

    total_amount: Decimal = Field(max_digits=10, decimal_places=2)
    status: str = Field(default='pending', max_length=20)
    notes: str | None = Field(default=None, max_length=500)

    shipping_street: str = Field(max_length=100)
    shipping_city: str = Field(max_length=50)
    shipping_state: str = Field(max_length=2)
    shipping_zip_code: str = Field(max_length=10)
    shipping_country: str = Field(default='US', max_length=2)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    """Order item model for PostgreSQL."""
    __tablename__ = 'order_items'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id", index=True)
    product_id: UUID = Field(foreign_key="products.id", index=True)

    quantity: int
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)
    total_price: Decimal = Field(max_digits=10, decimal_places=2)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    order: Order = Relationship(back_populates="items")
```

## Step 3: Business Rule Validation

### Inventory Check Validator

```python
# app/validators/inventory.py
from sqlmodel import Session, select
from app.models.product import Product
from app.schemas.order import OrderItemSchema, OrderCreateSchema
from uuid import UUID

class InventoryValidator:
    """Validate product availability."""

    def __init__(self, session: Session):
        self.session = session

    def validate_item_availability(
        self, item: OrderItemSchema, tenant_id: UUID
    ) -> tuple[bool, str | None]:
        """Check if product has sufficient inventory."""
        product = self.session.exec(
            select(Product)
            .where(Product.id == item.product_id)
            .where(Product.tenant_id == tenant_id)
        ).first()

        if not product:
            return False, f"Product not found"
        if not product.is_active:
            return False, f"Product not available"
        if product.stock_quantity < item.quantity:
            return False, f"Insufficient stock. Available: {product.stock_quantity}"
        if item.unit_price != product.price:
            return False, f"Price mismatch"

        return True, None

    def validate_order(
        self, order_data: OrderCreateSchema, tenant_id: UUID
    ) -> tuple[bool, list[str]]:
        """Validate all items in order."""
        errors = []
        for item in order_data.items:
            is_valid, error_msg = self.validate_item_availability(item, tenant_id)
            if not is_valid:
                errors.append(error_msg)
        return len(errors) == 0, errors
```

## Step 4: FastAPI Integration with Transaction

### Order Creation Endpoint

```python
# app/api/orders.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas.order import OrderCreateSchema
from app.models.order import Order, OrderItem
from app.validators.inventory import InventoryValidator
from app.database import get_session
from app.auth import get_current_user, get_current_tenant_id
from uuid import UUID

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/", status_code=201)
async def create_order(
    order_data: OrderCreateSchema,
    session: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """Create new order with validation and inventory check."""

    # Validate inventory
    validator = InventoryValidator(session)
    is_valid, errors = validator.validate_order(order_data, tenant_id)

    if not is_valid:
        raise HTTPException(
            status_code=422,
            detail={'error': 'validation_error', 'errors': errors}
        )

    try:
        # Create order
        order = Order(
            tenant_id=tenant_id,
            user_id=user_id,
            total_amount=order_data.total_amount,
            notes=order_data.notes,
            shipping_street=order_data.shipping_address.street,
            shipping_city=order_data.shipping_address.city,
            shipping_state=order_data.shipping_address.state,
            shipping_zip_code=order_data.shipping_address.zip_code,
            shipping_country=order_data.shipping_address.country,
        )
        session.add(order)
        session.flush()  # Get order.id

        # Create order items
        for item_data in order_data.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.total_price
            )
            session.add(order_item)

        # Update inventory
        for item_data in order_data.items:
            product = session.get(Product, item_data.product_id)
            product.stock_quantity -= item_data.quantity
            session.add(product)

        session.commit()
        session.refresh(order)

        return {
            'id': str(order.id),
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat()
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```

## Step 5: Comprehensive Tests

### Pytest Test Suite

```python
# tests/test_order_validation.py
import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.order import OrderItemSchema, ShippingAddressSchema, OrderCreateSchema


class TestOrderItemSchema:
    """Test order item validation."""

    def test_valid_order_item(self):
        data = {
            'product_id': '550e8400-e29b-41d4-a716-446655440000',
            'quantity': 2,
            'unit_price': Decimal('19.99')
        }
        item = OrderItemSchema(**data)
        assert item.quantity == 2
        assert item.total_price == Decimal('39.98')

    def test_negative_price(self):
        data = {
            'product_id': '550e8400-e29b-41d4-a716-446655440000',
            'quantity': 1,
            'unit_price': Decimal('-10.00')
        }
        with pytest.raises(ValidationError) as exc:
            OrderItemSchema(**data)
        assert 'positive' in str(exc.value.errors())


class TestShippingAddressSchema:
    """Test shipping address validation."""

    def test_valid_address(self):
        data = {
            'street': '123 Main St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip_code': '94102'
        }
        address = ShippingAddressSchema(**data)
        assert address.state == 'CA'
        assert address.country == 'US'

    def test_invalid_zip_format(self):
        data = {
            'street': '123 Main St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip_code': 'ABCDE'
        }
        with pytest.raises(ValidationError) as exc:
            ShippingAddressSchema(**data)
        errors = exc.value.errors()
        assert any(e['loc'] == ('zip_code',) for e in errors)


class TestOrderCreateSchema:
    """Test order creation validation."""

    def test_valid_order(self):
        data = {
            'items': [{
                'product_id': '550e8400-e29b-41d4-a716-446655440000',
                'quantity': 2,
                'unit_price': Decimal('19.99')
            }],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94102'
            }
        }
        order = OrderCreateSchema(**data)
        assert len(order.items) == 1
        assert order.total_amount == Decimal('39.98')

    def test_duplicate_products(self):
        product_id = '550e8400-e29b-41d4-a716-446655440000'
        data = {
            'items': [
                {'product_id': product_id, 'quantity': 2, 'unit_price': Decimal('19.99')},
                {'product_id': product_id, 'quantity': 1, 'unit_price': Decimal('19.99')}
            ],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94102'
            }
        }
        with pytest.raises(ValidationError) as exc:
            OrderCreateSchema(**data)
        assert 'Duplicate products' in str(exc.value.errors())

    def test_order_total_too_low(self):
        data = {
            'items': [{
                'product_id': '550e8400-e29b-41d4-a716-446655440000',
                'quantity': 1,
                'unit_price': Decimal('2.00')
            }],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94102'
            }
        }
        with pytest.raises(ValidationError) as exc:
            OrderCreateSchema(**data)
        assert 'at least $5.00' in str(exc.value.errors())

    def test_order_total_too_high(self):
        data = {
            'items': [{
                'product_id': '550e8400-e29b-41d4-a716-446655440000',
                'quantity': 1000,
                'unit_price': Decimal('20.00')  # Total = $20,000
            }],
            'shipping_address': {
                'street': '123 Main St',
                'city': 'San Francisco',
                'state': 'CA',
                'zip_code': '94102'
            }
        }
        with pytest.raises(ValidationError) as exc:
            OrderCreateSchema(**data)
        assert 'cannot exceed' in str(exc.value.errors())
```

## Summary

| Component | Lines | Purpose |
|-----------|-------|---------|
| **OrderItem Schema** | ~25 | Define item with price validation |
| **ShippingAddress Schema** | ~20 | Define address with state validation |
| **OrderCreate Schema** | ~35 | Define order with nested validation |
| **SQLModel Schemas** | ~40 | Define database models |
| **Inventory Validator** | ~35 | Business rule validation |
| **FastAPI Endpoint** | ~70 | Integrate validation in API |
| **Tests** | ~120 | Comprehensive validation tests |

## Key Takeaways

1. **Nested Validation**: Use List[OrderItemSchema] for nested objects
2. **Cross-Field Validation**: Use @model_validator for order total limits
3. **Business Rules**: Separate validator classes for complex logic
4. **Database Transactions**: Use session.flush() to get IDs before commit
5. **Multi-Tenant**: Always include tenant_id in queries
6. **Inventory Management**: Update stock in same transaction as order
7. **Error Handling**: Rollback transaction on any failure

---

**Next**: [Nested Validation Example](nested-validation.md) | **Index**: [Examples Index](INDEX.md)
