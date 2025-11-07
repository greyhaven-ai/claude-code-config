# Grey Haven Studio - Pydantic Schema Template
# Copy this template for new resource schemas

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


# TODO: Update model name
class ResourceBase(BaseModel):
    """Shared fields for Resource schemas."""

    # TODO: Add your base fields here
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: bool = True


class ResourceCreate(ResourceBase):
    """Schema for creating a new resource."""

    # TODO: Add creation-specific fields
    # Example: password, external_id, etc.

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Add custom validation if needed."""
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()


class ResourceUpdate(BaseModel):
    """Schema for updating an existing resource (all fields optional)."""

    # TODO: Add updateable fields (all optional)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ResourceRead(ResourceBase):
    """Schema for reading resource data (public fields only)."""

    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse[T](BaseModel):
    """Generic paginated response."""

    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool
