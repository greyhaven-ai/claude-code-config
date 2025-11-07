# SQLModel Alignment Reference

Ensuring Pydantic validation schemas align with SQLModel database models for Grey Haven applications.

## Core Concept

**Problem**: Pydantic schemas define API contracts, SQLModel defines database structure. Misalignment causes runtime errors.

**Solution**: Validate alignment programmatically and use shared patterns.

## Type Mapping

### Pydantic ↔ SQLModel ↔ PostgreSQL

| Pydantic Type | SQLModel Type | PostgreSQL Type |
|---------------|---------------|-----------------|
| `str` | `str` | `TEXT` / `VARCHAR(n)` |
| `int` | `int` | `INTEGER` |
| `float` | `float` | `DOUBLE PRECISION` |
| `Decimal` | `Decimal` | `NUMERIC(p, s)` |
| `bool` | `bool` | `BOOLEAN` |
| `datetime` | `datetime` | `TIMESTAMP` |
| `date` | `date` | `DATE` |
| `UUID` | `UUID` | `UUID` |
| `List[T]` | - | `ARRAY` / separate table |
| `Dict[K, V]` | - | `JSONB` |

### Example Alignment

```python
# Pydantic Schema (API)
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class UserCreateSchema(BaseModel):
    """User creation request."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    age: int = Field(..., ge=13, le=120)


# SQLModel (Database)
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    """User database model."""
    __tablename__ = 'users'

    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = SQLField(foreign_key="tenants.id", index=True)

    # Fields from UserCreateSchema
    email: str = SQLField(max_length=255, unique=True, index=True)
    username: str = SQLField(max_length=30, unique=True, index=True)
    age: int

    # Auto-managed fields
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)
```

## Alignment Validation

### Automated Schema Checker

```python
# app/validators/schema_alignment.py
from typing import Set, Dict
from pydantic import BaseModel
from sqlmodel import SQLModel

def validate_schema_alignment(
    pydantic_model: type[BaseModel],
    sqlmodel_model: type[SQLModel],
    exclude_db_fields: Set[str] = None
) -> Dict[str, list[str]]:
    """Validate Pydantic schema aligns with SQLModel."""

    if exclude_db_fields is None:
        exclude_db_fields = {'id', 'tenant_id', 'created_at', 'updated_at'}

    issues = {
        'missing_in_db': [],
        'missing_in_api': [],
        'type_mismatches': []
    }

    # Get field names
    pydantic_fields = set(pydantic_model.model_fields.keys())
    sqlmodel_fields = {
        col.name for col in sqlmodel_model.__table__.columns
        if col.name not in exclude_db_fields
    }

    # Check for missing fields
    issues['missing_in_db'] = list(pydantic_fields - sqlmodel_fields)
    issues['missing_in_api'] = list(sqlmodel_fields - pydantic_fields)

    # Check type alignment
    for field_name in pydantic_fields & sqlmodel_fields:
        pydantic_type = pydantic_model.model_fields[field_name].annotation
        sqlmodel_column = sqlmodel_model.__table__.columns[field_name]

        # Type checking (simplified)
        if not _types_compatible(pydantic_type, sqlmodel_column.type):
            issues['type_mismatches'].append(
                f"{field_name}: {pydantic_type} vs {sqlmodel_column.type}"
            )

    # Raise if any issues
    if any(issues.values()):
        raise ValueError(f"Schema alignment issues: {issues}")

    return issues


def _types_compatible(pydantic_type, sqlmodel_type) -> bool:
    """Check if types are compatible."""
    # Implementation depends on your type mapping rules
    return True  # Simplified for example
```

### Usage in Tests

```python
# tests/test_schema_alignment.py
import pytest
from app.schemas.user import UserCreateSchema
from app.models.user import User
from app.validators.schema_alignment import validate_schema_alignment

def test_user_schema_alignment():
    """Verify User schema aligns with database model."""
    issues = validate_schema_alignment(
        pydantic_model=UserCreateSchema,
        sqlmodel_model=User
    )
    assert not any(issues.values()), f"Alignment issues: {issues}"
```

## Multi-Tenant Patterns

### Always Include tenant_id

```python
# Pydantic Schema
class OrderCreateSchema(BaseModel):
    """Order creation (tenant_id injected by API)."""
    items: List[OrderItemSchema]
    shipping_address: ShippingAddressSchema

# SQLModel
class Order(SQLModel, table=True):
    """Order database model."""
    __tablename__ = 'orders'

    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = SQLField(foreign_key="tenants.id", index=True)  # Required!

    # Order fields...
```

### Row-Level Security (RLS)

```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Grant access
GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO app_user;
```

### API Integration

```python
# app/api/orders.py
from fastapi import Depends
from app.auth import get_current_tenant_id

@router.post("/")
async def create_order(
    order_data: OrderCreateSchema,
    tenant_id: UUID = Depends(get_current_tenant_id),
    session: Session = Depends(get_session)
):
    """Create order with tenant isolation."""

    # Inject tenant_id
    order = Order(
        **order_data.model_dump(),
        tenant_id=tenant_id
    )

    session.add(order)
    session.commit()
    return order
```

## Migration Strategies

### Adding New Fields

```python
# 1. Update SQLModel first
class User(SQLModel, table=True):
    # ... existing fields ...
    phone: Optional[str] = SQLField(default=None, max_length=20)

# 2. Create migration
"""
alembic revision --autogenerate -m "add user phone field"
"""

# 3. Update Pydantic schema
class UserCreateSchema(BaseModel):
    # ... existing fields ...
    phone: Optional[str] = Field(None, max_length=20, pattern=r'^\d{3}-\d{3}-\d{4}$')
```

### Renaming Fields

```python
# 1. Add new field to SQLModel
class User(SQLModel, table=True):
    username: str = SQLField(max_length=30)  # New name
    user_name: Optional[str] = SQLField(max_length=30)  # Old (nullable)

# 2. Create migration with data copy
"""
def upgrade():
    op.add_column('users', sa.Column('username', sa.String(30)))
    op.execute("UPDATE users SET username = user_name")
    op.alter_column('users', 'username', nullable=False)

def downgrade():
    op.drop_column('users', 'username')
"""

# 3. Update Pydantic schema
class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)

# 4. Deploy and verify

# 5. Remove old field
"""
def upgrade():
    op.drop_column('users', 'user_name')
"""
```

## Common Misalignment Issues

### Issue 1: String Length Mismatch

```python
# ❌ Bad - different max lengths
class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=50)  # API allows 50

class User(SQLModel, table=True):
    username: str = SQLField(max_length=30)  # DB only accepts 30

# ✅ Good - aligned
class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=30)

class User(SQLModel, table=True):
    username: str = SQLField(max_length=30)
```

### Issue 2: Optional Mismatch

```python
# ❌ Bad - API optional, DB required
class UserCreateSchema(BaseModel):
    email: Optional[EmailStr] = None

class User(SQLModel, table=True):
    email: str = SQLField(nullable=False)  # NOT NULL in DB

# ✅ Good - aligned
class UserCreateSchema(BaseModel):
    email: EmailStr  # Required

class User(SQLModel, table=True):
    email: str = SQLField(nullable=False)
```

### Issue 3: Missing Fields

```python
# ❌ Bad - field in API but not DB
class OrderCreateSchema(BaseModel):
    priority: int  # New field not in DB

class Order(SQLModel, table=True):
    # priority field missing!
    pass

# ✅ Good - field in both
class OrderCreateSchema(BaseModel):
    priority: int = Field(default=0, ge=0, le=5)

class Order(SQLModel, table=True):
    priority: int = SQLField(default=0)
```

### Issue 4: Enum Mismatch

```python
# ❌ Bad - different enum values
class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'

class UserCreateSchema(BaseModel):
    role: UserRole

class User(SQLModel, table=True):
    role: str  # No enum constraint in DB!

# ✅ Good - aligned with DB constraint
"""
CREATE TYPE user_role AS ENUM ('user', 'admin', 'moderator');
ALTER TABLE users ADD CONSTRAINT role_check
    CHECK (role IN ('user', 'admin', 'moderator'));
"""

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

class User(SQLModel, table=True):
    role: UserRole = SQLField(sa_column=Column(Enum(UserRole)))
```

## Testing Patterns

### Test Schema Alignment

```python
def test_all_schemas_aligned():
    """Test all Pydantic/SQLModel pairs are aligned."""
    schema_pairs = [
        (UserCreateSchema, User),
        (OrderCreateSchema, Order),
        (ProductCreateSchema, Product),
    ]

    for pydantic_model, sqlmodel_model in schema_pairs:
        issues = validate_schema_alignment(pydantic_model, sqlmodel_model)
        assert not any(issues.values()), f"{pydantic_model.__name__} misaligned"
```

### Test Round-Trip

```python
def test_user_round_trip(session):
    """Test data survives Pydantic → DB → Pydantic."""
    # Create via Pydantic
    create_data = UserCreateSchema(
        email='alice@example.com',
        username='alice',
        age=28
    )

    # Save to DB
    user = User(**create_data.model_dump(), tenant_id=uuid4())
    session.add(user)
    session.commit()
    session.refresh(user)

    # Load from DB
    loaded_user = session.get(User, user.id)

    # Verify fields match
    assert loaded_user.email == create_data.email
    assert loaded_user.username == create_data.username
    assert loaded_user.age == create_data.age
```

## Best Practices

1. **Single Source of Truth**: Define constraints once, reuse across schemas
2. **Automated Validation**: Run alignment checks in CI/CD
3. **Migration-First**: Update database schema before API schema
4. **Test Coverage**: Test all schema pairs in unit tests
5. **Type Safety**: Use enums for categorical data
6. **Documentation**: Document any intentional mismatches
7. **Tenant Isolation**: Always include tenant_id in multi-tenant models

## Summary

| Aspect | Guideline | Example |
|--------|-----------|---------|
| **Type Alignment** | Pydantic and SQLModel types must match | `str` in both |
| **Length Constraints** | max_length must match | `max_length=30` |
| **Nullability** | Optional must match nullable | `Optional[str]` + `nullable=True` |
| **Multi-Tenant** | Always include tenant_id | `tenant_id: UUID` |
| **Migrations** | Update DB first, then API | Alembic migration |
| **Testing** | Automated alignment checks | `validate_schema_alignment()` |

---

**Previous**: [Validators Reference](validators-reference.md) | **Next**: [Data Quality Monitoring](data-quality-monitoring.md) | **Index**: [Reference Index](INDEX.md)
