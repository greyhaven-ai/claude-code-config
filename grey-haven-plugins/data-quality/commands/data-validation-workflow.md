# Data Validation Workflow

**Trigger**: Use when implementing data validation for new features, APIs, or database models

**Purpose**: Systematically implement Pydantic v2 validation, ensure database schema alignment with PostgreSQL, and set up data quality monitoring

## When to Use

- Creating new API endpoints that accept user input
- Adding database tables or modifying schemas
- Building data processing pipelines
- Implementing data contracts between services
- Ensuring data quality in production

## Prerequisites

- PostgreSQL database configured
- Pydantic v2 installed (`pip install pydantic[email]>=2.0`)
- SQLModel for ORM (`pip install sqlmodel`)
- Great Expectations for monitoring (`pip install great-expectations`)
- pytest for testing (`pip install pytest`)

## Workflow Overview

**8-Phase systematic approach** (90-180 minutes total):

1. **Requirements Analysis** (5-10 min) - Define data fields and validation rules
2. **Test-First Development** (15-30 min) - Write tests before implementation (TDD)
3. **Pydantic Models** (20-40 min) - Create production-ready validation models
4. **Database Schema** (15-25 min) - Ensure Pydantic-SQLAlchemy alignment
5. **API Integration** (15-25 min) - Integrate validation into endpoints
6. **Quality Monitoring** (15-25 min) - Set up Great Expectations
7. **Observability** (10-15 min) - Add validation metrics
8. **Documentation** (10-15 min) - Generate OpenAPI specs

## Phase 1: Requirements Analysis

**Define what needs validation:**

1. **Identify data fields**:
   - Required vs optional fields
   - Data types for each field
   - Relationships between fields

2. **Define validation rules**:
   - Format constraints (email, URL, phone)
   - Range constraints (min/max values)
   - Pattern constraints (regex)
   - Cross-field validations
   - Business rules

3. **Database considerations**:
   - New table or existing table modification?
   - Unique constraints and indexes?
   - Migration strategy?

**Example Requirements**:
```
User Registration:
- email: Valid format, unique
- username: 3-30 chars, alphanumeric + hyphens/underscores, unique
- password: Min 12 chars, complexity rules
- age: 13-120, integer
- role: One of [user, admin, moderator], default 'user'
- Business rule: Admins must be 18+
```

## Phase 2: Test-First Development (TDD)

Use TDD methodology with tdd-python-implementer agent.

**Process**:
1. **Red**: Write failing tests (models don't exist yet)
2. **Green**: Implement minimal code to pass tests
3. **Blue**: Refactor for production quality

**Test Structure**:
```python
# tests/validation/test_user_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema

class TestUserCreateSchema:
    def test_valid_user_data(self):
        """Valid user data passes validation."""
        data = {
            "email": "test@example.com",
            "username": "test_user",
            "password": "SecurePass123!",
            "age": 25,
            "role": "user"
        }
        user = UserCreateSchema(**data)
        assert user.email == "test@example.com"

    def test_invalid_email_format(self):
        """Invalid email raises ValidationError."""
        with pytest.raises(ValidationError):
            UserCreateSchema(
                email="invalid-email",
                username="test",
                password="SecurePass123!",
                age=25
            )
```

## Phase 3: Pydantic Model Implementation

**Create production-ready Pydantic v2 models:**

```python
# app/schemas/user.py
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    EmailStr,
    constr,
    conint
)
from typing import Literal
from datetime import datetime
from uuid import UUID

class UserCreateSchema(BaseModel):
    """User creation data contract."""

    # Field definitions with constraints
    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["user@greyhaven.io"]
    )

    username: constr(
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_-]+$'
    ) = Field(
        ...,
        description="Username (alphanumeric, hyphens, underscores)"
    )

    password: constr(min_length=12) = Field(
        ...,
        description="Password (min 12 characters)"
    )

    age: conint(ge=13, le=120) = Field(
        ...,
        description="User age (13-120)"
    )

    role: Literal['user', 'admin', 'moderator'] = Field(
        default='user',
        description="User role"
    )

    # Field-level validators
    @field_validator('password')
    @classmethod
    def password_complexity(cls, v: str) -> str:
        """Validate password complexity."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*()_+-=' for c in v):
            raise ValueError('Password must contain special character')
        return v

    # Model-level validators
    @model_validator(mode='after')
    def validate_admin_age(self):
        """Admins must be 18+."""
        if self.role == 'admin' and self.age < 18:
            raise ValueError('Admin users must be 18 or older')
        return self

    # Pydantic v2 configuration
    model_config = {
        'str_strip_whitespace': True,
        'validate_assignment': True,
        'json_schema_extra': {
            'title': 'User Creation Schema v1.0',
            'examples': [{
                'email': 'alice@greyhaven.io',
                'username': 'alice_dev',
                'password': 'SecurePass123!',
                'age': 25,
                'role': 'user'
            }]
        }
    }

class UserResponseSchema(BaseModel):
    """User data returned from API."""

    id: UUID
    email: EmailStr
    username: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        'from_attributes': True,  # For ORM compatibility
    }
```

**Key Pydantic v2 Patterns**:
- Use `Field()` for metadata and constraints
- Use `@field_validator` for single-field validation
- Use `@model_validator` for cross-field validation
- Use `model_config` dict (not `class Config`)
- Use `model_validate()` method (not `parse_obj`)
- Use `model_dump()` method (not `dict()`)

## Phase 4: Database Schema Alignment

**Ensure Pydantic models match SQLAlchemy/SQLModel schema:**

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
    password_hash: str = Field(max_length=255)
    age: int
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Schema Alignment Test**:
```python
# tests/validation/test_schema_alignment.py
def test_pydantic_sqlalchemy_alignment():
    """Ensure Pydantic fields match SQLAlchemy columns."""
    from app.schemas.user import UserCreateSchema
    from app.models.user import User

    pydantic_fields = set(UserCreateSchema.model_fields.keys())
    sqlalchemy_columns = set(User.__table__.columns.keys())

    expected_columns = {'email', 'username', 'age', 'role'}
    assert expected_columns.issubset(sqlalchemy_columns)
```

## Phase 5: API Integration

**Integrate validation into API endpoints:**

```python
# API handler with validation
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema, UserResponseSchema

class ValidationErrorFormatter:
    """Format Pydantic errors for API responses."""

    @staticmethod
    def format_for_api(e: ValidationError) -> dict:
        """Format validation errors."""
        errors = {}
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            message = error['msg']

            if field not in errors:
                errors[field] = []
            errors[field].append(message)

        return {
            'success': False,
            'error': 'validation_error',
            'message': 'Request validation failed',
            'errors': errors
        }

async def create_user_handler(request):
    """Handle POST /api/users."""
    try:
        # 1. Parse and validate request body
        data = await request.json()
        user_data = UserCreateSchema.model_validate(data)

        # 2. Create user (hash password, save to DB)
        # ... implementation

        # 3. Return validated response
        return UserResponseSchema(...)

    except ValidationError as e:
        return ValidationErrorFormatter.format_for_api(e), 400
```

## Phase 6: Data Quality Monitoring

**Set up Great Expectations for continuous validation:**

```python
# data_quality/user_expectations.py
import great_expectations as ge

def create_user_expectations():
    """Define expectations for user data quality."""

    context = ge.get_context()

    # Create expectation suite
    suite = context.add_expectation_suite("user_data_quality")

    # Define expectations
    suite.expect_column_values_to_not_be_null("email")
    suite.expect_column_values_to_be_unique("email")
    suite.expect_column_values_to_match_regex("email", r'^[^@]+@[^@]+\.[^@]+$')
    suite.expect_column_values_to_be_between("age", min_value=13, max_value=120)

    return suite

def validate_batch(df):
    """Validate data batch."""
    context = ge.get_context()
    batch = context.get_batch(df, "user_data_quality")
    results = batch.validate()

    return results.success, results.statistics
```

## Phase 7: Observability

**Add validation metrics:**

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

validation_errors = Counter(
    'validation_errors_total',
    'Total validation errors',
    ['field', 'error_type']
)

validation_duration = Histogram(
    'validation_duration_seconds',
    'Time spent validating requests'
)

# Track in handler
with validation_duration.time():
    user_data = UserCreateSchema.model_validate(data)
```

## Phase 8: Documentation

**Generate OpenAPI specs from Pydantic models:**

```python
# Generate OpenAPI specification
spec = {
    'openapi': '3.1.0',
    'info': {'title': 'Grey Haven API', 'version': '1.0.0'},
    'paths': {
        '/api/users': {
            'post': {
                'summary': 'Create new user',
                'requestBody': {
                    'content': {
                        'application/json': {
                            'schema': UserCreateSchema.model_json_schema()
                        }
                    }
                },
                'responses': {
                    '200': {
                        'content': {
                            'application/json': {
                                'schema': UserResponseSchema.model_json_schema()
                            }
                        }
                    }
                }
            }
        }
    }
}
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete validation workflow examples
  - [user-registration-example.md](examples/user-registration-example.md) - Full user registration workflow
  - [nested-validation-example.md](examples/nested-validation-example.md) - Nested object validation
  - [conditional-validation-example.md](examples/conditional-validation-example.md) - Conditional field validation
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Pydantic v2 and validation references
  - [pydantic-v2-patterns.md](reference/pydantic-v2-patterns.md) - Pydantic v2 best practices
  - [field-validators.md](reference/field-validators.md) - Field validator reference
  - [model-validators.md](reference/model-validators.md) - Model validator reference
  - [great-expectations.md](reference/great-expectations.md) - Great Expectations setup
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [pydantic-schema.py](templates/pydantic-schema.py) - Pydantic model template
  - [sqlmodel-model.py](templates/sqlmodel-model.py) - SQLModel model template
  - [api-handler.py](templates/api-handler.py) - API handler with validation

- **[checklists/](checklists/)** - Validation implementation checklist
  - [validation-workflow-checklist.md](checklists/validation-workflow-checklist.md) - Complete workflow checklist

## When to Apply This Workflow

Use this workflow when:
- Creating new API endpoints that accept user input
- Adding or modifying database tables
- Building data processing pipelines
- Implementing data contracts between services
- Setting up data quality monitoring

## Critical Reminders

1. **Test-First**: Always write tests before implementing validation
2. **Pydantic v2**: Use `model_config` dict, not `class Config`
3. **Schema Alignment**: Ensure Pydantic and SQLModel fields match
4. **Error Formatting**: Format validation errors for API consumers
5. **Performance**: Profile validators, cache expensive operations
6. **Documentation**: Generate OpenAPI specs from Pydantic models
7. **Monitoring**: Track validation errors and latency
8. **Multi-Tenant**: Include tenant_id in all validation schemas
9. **Security**: Hash passwords before storing, never log sensitive data
10. **Quality**: Use Great Expectations for continuous data quality monitoring

## Integration with Other Agents

- **tdd-python-implementer**: For test-first validator development
- **observability-engineer**: For validation metrics and dashboards
- **security-analyzer**: For input sanitization validation
- **code-quality-analyzer**: For validator code quality review
