"""
SQLModel Database Model Template

Copy this template to create new database models.
Replace {ModelName} and {table_name} with your actual values.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional, List
from enum import Enum


# Optional: Define enum for status field
class {ModelName}Status(str, Enum):
    """Status enum for {ModelName}."""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class {ModelName}(SQLModel, table=True):
    """
    {ModelName} database model.
    
    Represents {table_name} table in PostgreSQL.
    Includes multi-tenant isolation via tenant_id.
    """
    
    __tablename__ = '{table_name}'
    
    # Primary Key
    # -----------
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique identifier"
    )
    
    # Multi-Tenant Isolation (REQUIRED)
    # ---------------------------------
    tenant_id: UUID = Field(
        foreign_key="tenants.id",
        index=True,
        description="Tenant for RLS isolation"
    )
    
    # Foreign Keys
    # -----------
    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID"
    )
    
    # Data Fields
    # ----------
    
    # String fields with length constraints
    name: str = Field(
        max_length=100,
        index=True,
        description="Display name"
    )
    
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        description="Email address"
    )
    
    # Optional text field
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional description"
    )
    
    # Integer field
    quantity: int = Field(
        description="Quantity"
    )
    
    # Decimal for currency
    price: Decimal = Field(
        max_digits=10,
        decimal_places=2,
        description="Price in USD"
    )
    
    # Enum/Status field
    status: str = Field(
        default='pending',
        max_length=20,
        index=True,
        description="Current status"
    )
    
    # Boolean field
    is_active: bool = Field(
        default=True,
        description="Active flag"
    )
    
    # JSON field (stored as JSONB in PostgreSQL)
    metadata: Optional[dict] = Field(
        default=None,
        sa_column_kwargs={"type_": "JSONB"},
        description="Additional metadata"
    )
    
    # Timestamps (REQUIRED)
    # --------------------
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp"
    )
    
    # Relationships
    # ------------
    
    # One-to-many: This model has many related items
    # items: List["RelatedItem"] = Relationship(back_populates="{model_name}")
    
    # Many-to-one: This model belongs to a user
    # user: Optional["User"] = Relationship(back_populates="{model_name}s")


# Related model example
# ---------------------

class {ModelName}Item(SQLModel, table=True):
    """Related items for {ModelName}."""
    
    __tablename__ = '{table_name}_items'
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Foreign key to parent
    {model_name}_id: UUID = Field(
        foreign_key="{table_name}.id",
        index=True
    )
    
    # Item fields
    name: str = Field(max_length=100)
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship back to parent
    {model_name}: Optional[{ModelName}] = Relationship(back_populates="items")


# Update parent model with relationship
{ModelName}.items = Relationship(back_populates="{model_name}")


# Database Migration
# ------------------

"""
After creating this model, generate a migration:

```bash
# Using Alembic
alembic revision --autogenerate -m "create {table_name} table"
alembic upgrade head
```

Migration will create:
- Table {table_name}
- Indexes on tenant_id, user_id, name, email, status
- Unique constraint on email
- Foreign key constraints
- Timestamps with defaults
"""


# Row-Level Security (RLS)
# ------------------------

"""
Enable RLS for multi-tenant isolation:

```sql
-- Enable RLS
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;

-- Create policy
CREATE POLICY tenant_isolation ON {table_name}
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

-- Grant access
GRANT SELECT, INSERT, UPDATE, DELETE ON {table_name} TO app_user;
```
"""


# Usage Example
# -------------

if __name__ == '__main__':
    from sqlmodel import Session, create_engine, select
    
    # Create engine
    engine = create_engine('postgresql://user:pass@localhost/db')
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Insert data
    with Session(engine) as session:
        item = {ModelName}(
            tenant_id=uuid4(),
            user_id=uuid4(),
            name='Test Item',
            email='test@example.com',
            quantity=10,
            price=Decimal('49.99'),
            status='active'
        )
        
        session.add(item)
        session.commit()
        session.refresh(item)
        
        print(f"Created {ModelName}: {item.id}")
    
    # Query data
    with Session(engine) as session:
        statement = select({ModelName}).where({ModelName}.status == 'active')
        results = session.exec(statement).all()
        
        print(f"Found {len(results)} active items")
