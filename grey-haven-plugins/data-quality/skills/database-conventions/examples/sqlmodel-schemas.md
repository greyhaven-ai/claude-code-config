# SQLModel Schema Examples

**Complete Python/SQLModel schema patterns.**

## Basic Model with Multi-Tenant

```python
# app/models/user.py
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User model with multi-tenant isolation."""
    
    __tablename__ = "users"
    
    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Timestamps (required on all tables)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    
    # Multi-tenant (required on all tables)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    
    # User fields
    email_address: str = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(max_length=255)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    last_login_at: Optional[datetime] = None
    
    # Soft delete
    deleted_at: Optional[datetime] = None
```

## Reusable Timestamp Mixin

```python
# app/models/base.py
from sqlmodel import Field
from datetime import datetime

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

# Use in models
class Team(TimestampMixin, SQLModel, table=True):
    __tablename__ = "teams"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    name: str = Field(max_length=255)
```

## One-to-Many Relationships

```python
# app/models/post.py
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

class Post(SQLModel, table=True):
    """Post model with author relationship."""
    
    __tablename__ = "posts"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    
    # Foreign key to users
    author_id: UUID = Field(foreign_key="users.id", index=True)
    
    title: str = Field(max_length=255)
    content: str
    is_published: bool = Field(default=False)
    
    # Relationship
    author: Optional["User"] = Relationship(back_populates="posts")

# Add to User model
class User(TimestampMixin, SQLModel, table=True):
    # ... (previous fields)
    posts: List["Post"] = Relationship(back_populates="author")
```

**See [../templates/sqlmodel-table.py](../templates/sqlmodel-table.py) for complete template.**
