# Grey Haven Studio - SQLModel Table Template
# Copy this template for new database tables

from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

# Reusable timestamp mixin
class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

# TODO: Update class and table name
class Resource(TimestampMixin, SQLModel, table=True):
    """Resource model with multi-tenant isolation."""
    
    __tablename__ = "resources"
    
    # Primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # Multi-tenant (REQUIRED on all tables)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)
    
    # TODO: Add your fields here (use snake_case!)
    name: str = Field(max_length=255)
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    
    # Soft delete (optional but recommended)
    deleted_at: Optional[datetime] = None
