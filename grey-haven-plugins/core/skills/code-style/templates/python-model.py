"""Example SQLModel Database Model Template.

Copy and adapt this for new Grey Haven database models.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column as SAColumn
from sqlmodel import JSON, Column, Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC datetime."""
    from datetime import UTC

    return datetime.now(UTC)


class ExampleDB(SQLModel, table=True):  # type: ignore[call-arg]
    """
    Example database model with multi-tenant support.

    This model demonstrates Grey Haven's database conventions:
    - snake_case field names
    - Multi-tenant isolation with tenant_id
    - UTC timestamps
    - Proper indexes
    - Comprehensive docstrings
    """

    __tablename__ = "examples"

    # Primary identification
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, description="Unique example identifier"
    )

    # Multi-tenant field (CRITICAL - always include!)
    tenant_id: UUID = Field(
        foreign_key="tenants.id", index=True, description="Owning tenant identifier"
    )

    # Example fields - all snake_case!
    name: str = Field(index=True, max_length=255, description="Example name")
    description: str | None = Field(
        default=None, max_length=1000, description="Optional description"
    )

    # Relationships (foreign keys)
    owner_id: UUID | None = Field(
        default=None, foreign_key="users.id", index=True, description="Owner user ID"
    )

    # Status flags
    is_active: bool = Field(default=True, description="Whether example is active")
    is_archived: bool = Field(default=False, description="Whether example is archived")

    # JSON metadata field
    metadata: dict | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Flexible JSON metadata storage",
    )

    # Numerical fields
    priority: int = Field(
        default=0, ge=0, le=10, description="Priority level (0-10)"
    )
    max_retries: int = Field(
        default=3, ge=0, description="Maximum number of retry attempts"
    )

    # Timestamps (UTC)
    created_at: datetime = Field(
        default_factory=utc_now, description="Creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=utc_now, description="Last update timestamp (UTC)"
    )
    archived_at: datetime | None = Field(
        default=None, description="Archive timestamp (UTC)"
    )

    # Uncomment if using custom UTCDateTime type
    # from app.db.db_types import UTCDateTime
    # created_at: datetime = Field(
    #     default_factory=utc_now,
    #     sa_column=SAColumn(UTCDateTime, nullable=False)
    # )
    # updated_at: datetime = Field(
    #     default_factory=utc_now,
    #     sa_column=SAColumn(UTCDateTime, nullable=False, onupdate=utc_now)
    # )


# Pydantic schemas for API (in separate schemas file)
# class ExampleBase(BaseModel):
#     """Base example schema with shared fields."""
#     name: str = Field(..., max_length=255)
#     description: str | None = None
#     is_active: bool = True
#     priority: int = Field(default=0, ge=0, le=10)
#
# class ExampleCreate(ExampleBase):
#     """Schema for creating an example."""
#     tenant_id: UUID
#
# class ExampleUpdate(BaseModel):
#     """Schema for updating an example (all fields optional)."""
#     name: str | None = None
#     description: str | None = None
#     is_active: bool | None = None
#     priority: int | None = Field(None, ge=0, le=10)
#
# class ExampleResponse(ExampleBase):
#     """Example response schema."""
#     id: UUID
#     tenant_id: UUID
#     owner_id: UUID | None
#     created_at: datetime
#     updated_at: datetime
#
#     model_config = ConfigDict(from_attributes=True)
