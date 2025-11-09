# Pydantic Schema Examples

**Complete Pydantic schema patterns for request/response validation.**

## Request/Response Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator, model_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Shared fields for User schemas."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)
    password_confirm: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Ensure password meets complexity requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        """Ensure password and password_confirm match."""
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Schema for reading user data (public fields only)."""
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
```

## Nested Schemas

```python
# app/schemas/organization.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from app.schemas.team import TeamRead


class OrganizationBase(BaseModel):
    """Shared fields for Organization schemas."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization."""
    pass


class OrganizationRead(OrganizationBase):
    """Organization with nested teams."""
    id: str
    tenant_id: str
    teams: list[TeamRead] = []  # Nested teams
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Custom Validation

```python
# app/schemas/user.py
from pydantic import field_validator, model_validator
import re


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Ensure username is alphanumeric."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError("Username must contain only letters, numbers, hyphens, and underscores")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Ensure email is from allowed domain."""
        allowed_domains = ["example.com", "greyhaven.studio"]
        domain = v.split("@")[1]
        if domain not in allowed_domains:
            raise ValueError(f"Email must be from {', '.join(allowed_domains)}")
        return v

    @model_validator(mode="after")
    def validate_username_not_in_email(self) -> "UserCreate":
        """Ensure username is not part of email."""
        if self.username.lower() in self.email.lower():
            raise ValueError("Username cannot be part of email address")
        return self
```

**See also:**
- [fastapi-crud.md](fastapi-crud.md) - CRUD endpoints using these schemas
- [../templates/pydantic-schemas.py](../templates/pydantic-schemas.py) - Schema template
