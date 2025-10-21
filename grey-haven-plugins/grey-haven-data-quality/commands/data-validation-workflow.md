# Data Validation Workflow

**Trigger**: Use when implementing data validation for new features, APIs, or database models

**Purpose**: Systematically implement Pydantic v2 validation, ensure database schema alignment with PlanetScale PostgreSQL, and set up data quality monitoring

## When to Use

- Creating new API endpoints that accept user input
- Adding database tables or modifying schemas
- Building data processing pipelines
- Implementing data contracts between services
- Ensuring data quality in production

## Prerequisites

- PlanetScale PostgreSQL database configured
- Pydantic v2 installed (`pip install pydantic[email]>=2.0`)
- SQLAlchemy for ORM (`pip install sqlalchemy`)
- Great Expectations for monitoring (`pip install great-expectations`)
- pytest for testing (`pip install pytest`)

## Workflow Steps

### Phase 1: Requirements Analysis (5-10 minutes)

**Understand data requirements:**

1. **Identify data fields**:
   - What data needs validation?
   - Required vs optional fields?
   - Data types for each field?

2. **Define validation rules**:
   - Format constraints (email, URL, phone)?
   - Range constraints (min/max values)?
   - Pattern constraints (regex)?
   - Cross-field validations?
   - Business rules?

3. **Database considerations**:
   - Is this for a new table or existing?
   - What are PlanetScale schema requirements?
   - Any unique constraints or indexes?

**Example**:
```
User Registration Feature:
- Fields: email, username, password, age, role
- Validation: 
  - email: Valid email format, unique
  - username: 3-30 chars, alphanumeric + hyphens/underscores, unique
  - password: Min 12 chars, complexity rules
  - age: 13-120, integer
  - role: One of [user, admin, moderator], default 'user'
- Business rules:
  - Admins must be 18+
  - Usernames cannot contain profanity
```

### Phase 2: Test-First Development (15-30 minutes)

**Use TDD methodology with tdd-python-implementer:**

1. **Create test file structure**:
```python
# tests/validation/test_user_schema.py
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema, UserResponseSchema

class TestUserCreateSchema:
    """Test user creation validation."""
    
    def test_valid_user_data(self):
        """Valid user data passes validation."""
        # TODO: Implement
        pass
    
    def test_invalid_email_format(self):
        """Invalid email raises ValidationError."""
        # TODO: Implement
        pass
    
    def test_username_too_short(self):
        """Username under 3 chars fails."""
        # TODO: Implement
        pass
    
    # ... more tests
```

2. **Write failing tests** (Red phase):
```bash
pytest tests/validation/test_user_schema.py
# Expected: All tests fail (models don't exist yet)
```

3. **Implement Pydantic models** (Green phase):

Create minimal implementation:
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    age: int
```

Run tests:
```bash
pytest tests/validation/test_user_schema.py
# Expected: Some tests pass, refine implementation
```

4. **Refactor** (Blue phase):
- Add field validators
- Add model validators
- Add configuration
- Optimize performance

### Phase 3: Pydantic Model Implementation (20-40 minutes)

**Create production-ready Pydantic models:**

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
from typing import Optional, Literal
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
    @field_validator('username')
    @classmethod
    def username_no_profanity(cls, v: str) -> str:
        """Validate username doesn't contain profanity."""
        profanity_list = ['badword1', 'badword2']  # Load from config
        if any(word in v.lower() for word in profanity_list):
            raise ValueError('Username contains inappropriate content')
        return v
    
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

**Key Pydantic v2 patterns**:
- Use `Field()` for metadata and constraints
- Use `@field_validator` for single-field validation
- Use `@model_validator` for cross-field validation
- Use `model_config` dict (not `class Config`)
- Use `model_validate()` method (not `parse_obj`)
- Use `model_dump()` method (not `dict()`)

### Phase 4: Database Schema Alignment (15-25 minutes)

**Ensure Pydantic models match PlanetScale schema:**

1. **Create SQLAlchemy model**:
```python
# app/models/user.py
from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
import uuid

Base = declarative_base()

class UserRole(str, enum.Enum):
    """User role enum."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

class User(Base):
    """User model for PlanetScale PostgreSQL."""
    __tablename__ = 'users'
    
    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    username = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = Column(
        String(255),
        nullable=False
    )
    age = Column(
        Integer,
        nullable=False
    )
    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.USER
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    __table_args__ = (
        {'schema': 'public'}
    )
```

2. **Create Alembic migration**:
```bash
# Generate migration
alembic revision --autogenerate -m "Add users table"

# Review migration file
# alembic/versions/001_add_users_table.py

# Apply to PlanetScale branch
pscale branch create mydb feature-user-table
alembic upgrade head

# Test on branch
pscale shell mydb feature-user-table
```

3. **Validate schema alignment**:
```python
# tests/validation/test_schema_alignment.py
def test_pydantic_sqlalchemy_alignment():
    """Ensure Pydantic fields match SQLAlchemy columns."""
    from app.schemas.user import UserCreateSchema
    from app.models.user import User
    
    pydantic_fields = set(UserCreateSchema.model_fields.keys())
    sqlalchemy_columns = set(c.name for c in User.__table__.columns)
    
    # Check all Pydantic fields have corresponding columns
    # (excluding auto-generated fields like id, timestamps)
    expected_columns = {'email', 'username', 'age', 'role'}
    assert expected_columns.issubset(sqlalchemy_columns)
```

### Phase 5: API Integration (15-25 minutes)

**Integrate validation into Cloudflare Workers:**

```python
# workers/api/users.py
from pydantic import ValidationError
from app.schemas.user import UserCreateSchema, UserResponseSchema
from app.models.user import User
import bcrypt
from planetscale import connect

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

async def on_request_post(context):
    """Handle POST /api/users - Create user."""
    try:
        # 1. Parse request body
        data = await context.request.json()
        
        # 2. Validate with Pydantic
        user_data = UserCreateSchema.model_validate(data)
        
        # 3. Hash password
        password_hash = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # 4. Connect to PlanetScale
        conn = connect(
            host=context.env.PLANETSCALE_HOST,
            username=context.env.PLANETSCALE_USER,
            password=context.env.PLANETSCALE_PASSWORD
        )
        
        # 5. Insert user
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (email, username, password_hash, age, role, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id, email, username, role, created_at, updated_at
            """,
            (
                user_data.email,
                user_data.username,
                password_hash,
                user_data.age,
                user_data.role
            )
        )
        
        user_row = cursor.fetchone()
        conn.commit()
        
        # 6. Return validated response
        response_data = UserResponseSchema(
            id=user_row[0],
            email=user_row[1],
            username=user_row[2],
            role=user_row[3],
            created_at=user_row[4],
            updated_at=user_row[5]
        )
        
        return Response.json({
            'success': True,
            'user': response_data.model_dump()
        })
        
    except ValidationError as e:
        # Return formatted validation errors
        return Response.json(
            ValidationErrorFormatter.format_for_api(e),
            status=400
        )
    
    except Exception as e:
        # Log error, return generic message
        print(f"Error creating user: {e}")
        return Response.json({
            'success': False,
            'error': 'internal_error',
            'message': 'An error occurred'
        }, status=500)
```

### Phase 6: Data Quality Monitoring (20-30 minutes)

**Set up Great Expectations for quality monitoring:**

1. **Initialize Great Expectations**:
```bash
great_expectations init
```

2. **Create expectation suite**:
```python
# great_expectations/expectations/users_suite.py
import great_expectations as gx

context = gx.get_context()

# Create suite
suite = context.add_expectation_suite(
    expectation_suite_name="users_quality_suite"
)

# Add expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="email"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="email"
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="email",
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="age",
        min_value=13,
        max_value=120
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="role",
        value_set=['user', 'admin', 'moderator']
    )
)

context.save_expectation_suite(suite)
```

3. **Run validation**:
```python
# scripts/validate_user_data.py
import great_expectations as gx
import pandas as pd
from planetscale import connect

def validate_user_table():
    """Validate users table data quality."""
    # Connect to PlanetScale
    conn = connect(
        host=os.getenv('PLANETSCALE_HOST'),
        username=os.getenv('PLANETSCALE_USER'),
        password=os.getenv('PLANETSCALE_PASSWORD')
    )
    
    # Load data
    df = pd.read_sql("SELECT * FROM users", conn)
    
    # Get context and suite
    context = gx.get_context()
    suite = context.get_expectation_suite("users_quality_suite")
    
    # Validate
    validator = context.sources.pandas_default.read_dataframe(df)
    results = validator.validate(suite)
    
    # Check results
    if results.success:
        print("[OK] Data quality validation passed")
    else:
        print("[X] Data quality validation failed")
        for result in results.results:
            if not result.success:
                print(f"  - {result.expectation_config.expectation_type}")
    
    return results

if __name__ == '__main__':
    validate_user_table()
```

4. **Schedule monitoring**:
```yaml
# .github/workflows/data-quality.yml
name: Data Quality Monitoring

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install great-expectations pandas planetscale-python
      
      - name: Run data validation
        env:
          PLANETSCALE_HOST: ${{ secrets.PLANETSCALE_HOST }}
          PLANETSCALE_USER: ${{ secrets.PLANETSCALE_USER }}
          PLANETSCALE_PASSWORD: ${{ secrets.PLANETSCALE_PASSWORD }}
        run: |
          python scripts/validate_user_data.py
```

### Phase 7: Observability Integration (10-15 minutes)

**Add validation metrics:**

```python
# app/monitoring/validation_metrics.py
from prometheus_client import Counter, Histogram

validation_errors = Counter(
    'data_validation_errors_total',
    'Total data validation errors',
    ['model', 'field', 'error_type']
)

validation_duration = Histogram(
    'data_validation_duration_seconds',
    'Time spent validating data',
    ['model']
)

class MonitoredValidator:
    """Pydantic validator with metrics."""
    
    @staticmethod
    def validate(model_class, data):
        """Validate with metrics tracking."""
        model_name = model_class.__name__
        
        with validation_duration.labels(model=model_name).time():
            try:
                return model_class.model_validate(data)
            except ValidationError as e:
                # Track each validation error
                for error in e.errors():
                    field = '.'.join(str(loc) for loc in error['loc'])
                    error_type = error['type']
                    
                    validation_errors.labels(
                        model=model_name,
                        field=field,
                        error_type=error_type
                    ).inc()
                
                raise

# Use in API
from app.monitoring.validation_metrics import MonitoredValidator

async def on_request_post(context):
    try:
        data = await context.request.json()
        
        # Validate with metrics
        user_data = MonitoredValidator.validate(UserCreateSchema, data)
        
        # ... rest of handler
    except ValidationError as e:
        return Response.json(
            ValidationErrorFormatter.format_for_api(e),
            status=400
        )
```

**Create Grafana dashboard**:
```json
{
  "dashboard": {
    "title": "Data Validation Metrics",
    "panels": [
      {
        "title": "Validation Error Rate",
        "targets": [
          {
            "expr": "rate(data_validation_errors_total[5m])"
          }
        ]
      },
      {
        "title": "Validation Duration (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, data_validation_duration_seconds_bucket)"
          }
        ]
      }
    ]
  }
}
```

### Phase 8: Documentation (10-15 minutes)

**Generate API documentation:**

```python
# scripts/generate_api_docs.py
import json
from app.schemas.user import UserCreateSchema, UserResponseSchema

def generate_openapi_spec():
    """Generate OpenAPI specification."""
    spec = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Grey Haven API',
            'version': '1.0.0'
        },
        'paths': {
            '/api/users': {
                'post': {
                    'summary': 'Create new user',
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': UserCreateSchema.model_json_schema()
                            }
                        }
                    },
                    'responses': {
                        '200': {
                            'description': 'User created successfully',
                            'content': {
                                'application/json': {
                                    'schema': UserResponseSchema.model_json_schema()
                                }
                            }
                        },
                        '400': {
                            'description': 'Validation error'
                        }
                    }
                }
            }
        }
    }
    
    with open('docs/openapi.json', 'w') as f:
        json.dump(spec, f, indent=2)

if __name__ == '__main__':
    generate_openapi_spec()
```

## Checklist

Use this checklist to track progress:

### Phase 1: Requirements [OK]
- [ ] Data fields identified
- [ ] Validation rules defined
- [ ] Database schema requirements clear
- [ ] Business rules documented

### Phase 2: Testing [OK]
- [ ] Test file structure created
- [ ] Failing tests written (Red)
- [ ] Tests passing (Green)
- [ ] Code refactored (Blue)

### Phase 3: Pydantic Models [OK]
- [ ] Field definitions with types
- [ ] Field validators implemented
- [ ] Model validators implemented
- [ ] Configuration set (model_config)
- [ ] Examples provided

### Phase 4: Database [OK]
- [ ] SQLAlchemy model created
- [ ] Alembic migration generated
- [ ] Migration tested on PlanetScale branch
- [ ] Schema alignment validated

### Phase 5: API Integration [OK]
- [ ] Validation in request handlers
- [ ] Error formatting implemented
- [ ] Response schemas used
- [ ] Error handling tested

### Phase 6: Quality Monitoring [OK]
- [ ] Great Expectations initialized
- [ ] Expectation suite created
- [ ] Validation script implemented
- [ ] Monitoring scheduled

### Phase 7: Observability [OK]
- [ ] Prometheus metrics added
- [ ] Grafana dashboard created
- [ ] Metrics tested

### Phase 8: Documentation [OK]
- [ ] OpenAPI spec generated
- [ ] API docs published
- [ ] Examples documented

## Common Patterns

### Pattern 1: Nested Validation

```python
from typing import List

class AddressSchema(BaseModel):
    """Address validation."""
    street: str
    city: str
    state: constr(min_length=2, max_length=2)
    zip_code: constr(pattern=r'^\d{5}(-\d{4})?$')

class UserWithAddressSchema(BaseModel):
    """User with nested address."""
    email: EmailStr
    username: str
    addresses: List[AddressSchema] = Field(min_length=1, max_length=5)
    
    @model_validator(mode='after')
    def validate_primary_address(self):
        """Ensure at least one primary address."""
        # Custom validation logic
        return self
```

### Pattern 2: Conditional Validation

```python
class OrderSchema(BaseModel):
    """Order with conditional validation."""
    order_type: Literal['online', 'in-store']
    shipping_address: Optional[AddressSchema] = None
    
    @model_validator(mode='after')
    def validate_shipping(self):
        """Online orders require shipping address."""
        if self.order_type == 'online' and not self.shipping_address:
            raise ValueError('Online orders require shipping address')
        return self
```

### Pattern 3: Custom Types

```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Any

class PostalCode:
    """Custom postal code type."""
    
    def __init__(self, value: str):
        if not re.match(r'^\d{5}(-\d{4})?$', value):
            raise ValueError('Invalid postal code')
        self.value = value
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler
    ):
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema()
        )

class AddressSchema(BaseModel):
    zip_code: PostalCode
```

## Troubleshooting

### Issue: ValidationError not caught

**Problem**: Validation errors not being caught in API handlers

**Solution**: Ensure `ValidationError` is imported from `pydantic`:
```python
from pydantic import ValidationError  # Correct
# not from other libraries
```

### Issue: Schema mismatch with database

**Problem**: Pydantic model doesn't match SQLAlchemy schema

**Solution**: Create validation test:
```python
def test_schema_alignment():
    pydantic_fields = set(UserCreateSchema.model_fields.keys())
    db_columns = set(c.name for c in User.__table__.columns)
    assert expected_fields.issubset(db_columns)
```

### Issue: Slow validation performance

**Problem**: Validation taking too long

**Solutions**:
1. Use `model_config['validate_assignment'] = False`
2. Cache validators with `@lru_cache`
3. Use batch validation
4. Profile with `cProfile`

## Success Metrics

Track these metrics to ensure success:

1. **Validation Coverage**: % of API endpoints with Pydantic validation
2. **Data Quality Score**: % of Great Expectations checks passing
3. **Error Rate**: Validation errors per 1000 requests
4. **Performance**: p95 validation latency < 10ms
5. **Schema Alignment**: 100% Pydantic-SQLAlchemy alignment
6. **Test Coverage**: 100% of validation logic tested

## Integration with Other Agents

- **tdd-python-implementer**: For test-first validator development
- **observability-engineer**: For validation metrics and dashboards
- **security-analyzer**: For input sanitization
- **code-quality-analyzer**: For validator code quality
- **incident-responder**: For debugging validation failures in production
