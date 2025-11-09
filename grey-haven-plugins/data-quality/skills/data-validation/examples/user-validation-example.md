# User Validation Example

Complete workflow for building user validation with Pydantic v2, database alignment, and testing.

## Goal

Build user validation system with:
- Email, username, age validation
- Custom validators (profanity check)
- Cross-field validation (admin age requirement)
- SQLModel database alignment
- FastAPI endpoint integration
- Comprehensive test coverage

## Step 1: Define Pydantic Model

### UserCreateSchema

```python
# app/schemas/user.py
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr, constr, conint
from typing import Literal
from datetime import datetime

class UserCreateSchema(BaseModel):
    """User creation data contract."""

    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["alice@greyhaven.io"]
    )

    username: constr(
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_-]+$'
    ) = Field(
        ...,
        description="Username (alphanumeric, hyphens, underscores only)"
    )

    age: conint(ge=13, le=120) = Field(
        ...,
        description="User age (must be 13+)"
    )

    role: Literal['user', 'admin', 'moderator'] = Field(
        default='user',
        description="User role"
    )

    # Field validator
    @field_validator('username')
    @classmethod
    def username_no_profanity(cls, v: str) -> str:
        """Validate username doesn't contain profanity."""
        profanity_list = ['bad', 'words', 'spam']
        if any(word in v.lower() for word in profanity_list):
            raise ValueError('Username contains inappropriate content')
        return v

    # Model validator (cross-field)
    @model_validator(mode='after')
    def check_admin_age(self):
        """Admins must be 18+."""
        if self.role == 'admin' and self.age < 18:
            raise ValueError('Admin users must be 18 or older')
        return self

    # Pydantic v2 configuration
    model_config = {
        'str_strip_whitespace': True,
        'validate_assignment': True,
        'json_schema_extra': {
            'examples': [{
                'email': 'alice@greyhaven.io',
                'username': 'alice_dev',
                'age': 28,
                'role': 'user'
            }]
        }
    }


class UserResponseSchema(BaseModel):
    """User response data contract."""

    id: str
    email: str
    username: str
    age: int
    role: str
    created_at: datetime

    model_config = {
        'from_attributes': True  # Enable ORM mode for SQLModel
    }
```

## Step 2: Define SQLModel Schema

### User Database Model

```python
# app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

class User(SQLModel, table=True):
    """User model for PostgreSQL."""
    __tablename__ = 'users'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=30, unique=True, index=True)
    age: int
    role: UserRole = Field(default=UserRole.USER)
    tenant_id: UUID = Field(foreign_key="tenants.id", index=True)  # Multi-tenant
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Step 3: Schema Alignment Validation

### Validate Pydantic ↔ SQLModel Alignment

```python
# app/validators/schema_alignment.py
from app.schemas.user import UserCreateSchema
from app.models.user import User

def validate_user_schema_alignment():
    """Ensure Pydantic model aligns with database schema."""
    
    # Get Pydantic fields
    pydantic_fields = set(UserCreateSchema.model_fields.keys())
    
    # Get SQLModel columns (exclude auto-generated)
    sqlmodel_columns = {
        col.name for col in User.__table__.columns
        if col.name not in ('id', 'tenant_id', 'created_at', 'updated_at')
    }
    
    # Check all Pydantic fields exist in database
    missing_in_db = pydantic_fields - sqlmodel_columns
    if missing_in_db:
        raise ValueError(f"Fields missing in database: {missing_in_db}")
    
    # Check field types match
    for field_name in pydantic_fields:
        pydantic_type = UserCreateSchema.model_fields[field_name].annotation
        sqlmodel_column = User.__table__.columns[field_name]
        
        # Type validation logic here
        # (simplified for example)
    
    return True


# Run validation on startup
if __name__ == '__main__':
    validate_user_schema_alignment()
    print("✓ Schema alignment validated")
```

## Step 4: FastAPI Integration

### API Endpoint with Validation

```python
# app/api/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.models.user import User
from app.database import get_session
from app.auth import get_current_tenant_id

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(
    user_data: UserCreateSchema,
    session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id)
):
    """Create new user with validation."""
    
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists"
        )
    
    # Check if username already exists
    existing_username = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()
    
    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already taken"
        )
    
    # Create user
    user = User(
        **user_data.model_dump(),
        tenant_id=tenant_id
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return UserResponseSchema.model_validate(user)


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: str,
    session: Session = Depends(get_session),
    tenant_id: str = Depends(get_current_tenant_id)
):
    """Get user by ID with tenant isolation."""
    
    user = session.exec(
        select(User)
        .where(User.id == user_id)
        .where(User.tenant_id == tenant_id)
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponseSchema.model_validate(user)
```

## Step 5: Validation Error Formatting

### User-Friendly Error Responses

```python
# app/middleware/validation_error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Format Pydantic validation errors for API responses."""
    
    errors = {}
    for error in exc.errors():
        field = '.'.join(str(loc) for loc in error['loc'])
        message = error['msg']
        error_type = error['type']
        
        if field not in errors:
            errors[field] = []
        
        # Make error messages user-friendly
        if error_type == 'string_too_short':
            message = f"Must be at least {error.get('ctx', {}).get('min_length', 0)} characters"
        elif error_type == 'string_too_long':
            message = f"Must be at most {error.get('ctx', {}).get('max_length', 0)} characters"
        elif error_type == 'value_error.email':
            message = "Invalid email address format"
        
        errors[field].append(message)
    
    return JSONResponse(
        status_code=422,
        content={
            'success': False,
            'error': 'validation_error',
            'message': 'Request validation failed',
            'errors': errors
        }
    )


# Register in FastAPI app
from fastapi import FastAPI

app = FastAPI()
app.add_exception_handler(ValidationError, validation_exception_handler)
```

## Step 6: Comprehensive Tests

### Pytest Test Suite

```python
# tests/test_user_validation.py
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema


class TestUserCreateSchema:
    """Test user creation validation."""
    
    def test_valid_user_data(self):
        """Test validation passes with valid data."""
        data = {
            'email': 'alice@greyhaven.io',
            'username': 'alice_dev',
            'age': 28,
            'role': 'user'
        }
        
        user = UserCreateSchema(**data)
        
        assert user.email == 'alice@greyhaven.io'
        assert user.username == 'alice_dev'
        assert user.age == 28
        assert user.role == 'user'
    
    def test_invalid_email(self):
        """Test validation fails with invalid email."""
        data = {
            'email': 'not-an-email',
            'username': 'alice_dev',
            'age': 28
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        assert any(e['loc'] == ('email',) for e in errors)
    
    def test_username_too_short(self):
        """Test validation fails with short username."""
        data = {
            'email': 'alice@greyhaven.io',
            'username': 'ab',  # Too short
            'age': 28
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        assert any(e['loc'] == ('username',) for e in errors)
    
    def test_username_invalid_characters(self):
        """Test validation fails with invalid characters."""
        data = {
            'email': 'alice@greyhaven.io',
            'username': 'alice@test',  # Invalid @ character
            'age': 28
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        assert any(e['loc'] == ('username',) for e in errors)
    
    def test_username_profanity_check(self):
        """Test validation fails with profanity."""
        data = {
            'email': 'test@greyhaven.io',
            'username': 'badword123',  # Contains profanity
            'age': 28
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        error_msg = next(e['msg'] for e in errors if e['loc'] == ('username',))
        assert 'inappropriate content' in error_msg
    
    def test_age_too_young(self):
        """Test validation fails with age < 13."""
        data = {
            'email': 'child@greyhaven.io',
            'username': 'child_user',
            'age': 10  # Too young
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        assert any(e['loc'] == ('age',) for e in errors)
    
    def test_age_too_old(self):
        """Test validation fails with age > 120."""
        data = {
            'email': 'old@greyhaven.io',
            'username': 'old_user',
            'age': 150  # Too old
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        assert any(e['loc'] == ('age',) for e in errors)
    
    def test_admin_age_requirement(self):
        """Test admin must be 18+."""
        data = {
            'email': 'teen@greyhaven.io',
            'username': 'teen_admin',
            'age': 16,
            'role': 'admin'  # Admin role but too young
        }
        
        with pytest.raises(ValidationError) as exc:
            UserCreateSchema(**data)
        
        errors = exc.value.errors()
        error_msg = str(errors)
        assert '18 or older' in error_msg
    
    def test_whitespace_stripping(self):
        """Test whitespace is stripped from strings."""
        data = {
            'email': '  alice@greyhaven.io  ',
            'username': '  alice_dev  ',
            'age': 28
        }
        
        user = UserCreateSchema(**data)
        
        assert user.email == 'alice@greyhaven.io'
        assert user.username == 'alice_dev'
    
    def test_default_role(self):
        """Test default role is 'user'."""
        data = {
            'email': 'alice@greyhaven.io',
            'username': 'alice_dev',
            'age': 28
            # role not provided
        }
        
        user = UserCreateSchema(**data)
        
        assert user.role == 'user'
```

## Summary

| Component | Lines | Purpose |
|-----------|-------|---------|
| **Pydantic Schema** | ~70 | Define data contract with validators |
| **SQLModel Schema** | ~20 | Define database model |
| **Schema Alignment** | ~30 | Validate Pydantic ↔ SQLModel match |
| **FastAPI Endpoint** | ~60 | Integrate validation in API |
| **Error Formatting** | ~40 | User-friendly error messages |
| **Tests** | ~150 | Comprehensive validation tests |

## Key Takeaways

1. **Field Validators**: Use `@field_validator` for single-field validation
2. **Model Validators**: Use `@model_validator` for cross-field validation
3. **Type Constraints**: `EmailStr`, `constr`, `conint` for built-in validation
4. **Schema Alignment**: Ensure Pydantic and SQLModel match
5. **Error Formatting**: Make validation errors user-friendly
6. **Comprehensive Tests**: Test all validation rules and edge cases
7. **Multi-Tenant**: Always include tenant_id for data isolation

---

**Next**: [Order Validation Example](order-validation-example.md) | **Index**: [Examples Index](INDEX.md)
