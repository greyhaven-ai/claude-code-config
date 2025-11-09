# Data Validation Examples

Complete examples for Pydantic v2 validation, database schema alignment, and data quality monitoring.

## Examples Overview

### User Validation Example
**File**: [user-validation-example.md](user-validation-example.md)

Complete user validation workflow with:
- Pydantic v2 model with field validators
- Email, username, age validation
- Cross-field validation (admin age requirement)
- SQLModel database alignment
- FastAPI integration
- Validation error formatting
- Pytest test suite

**Use when**: Building user registration, profile management, or authentication.

---

### Order Validation Example
**File**: [order-validation-example.md](order-validation-example.md)

Complex order validation with:
- Nested object validation (order items, shipping address)
- Currency and pricing validation
- Inventory quantity checks
- Multi-tenant validation (tenant_id)
- Custom validators for business rules
- Database transaction validation

**Use when**: Building e-commerce, order management, or invoicing systems.

---

### Nested Validation Example
**File**: [nested-validation.md](nested-validation.md)

Advanced nested validation patterns:
- Nested Pydantic models
- List validation with min/max items
- Discriminated unions for polymorphic data
- Recursive validation (tree structures)
- Forward references
- Validation context passing

**Use when**: Working with complex JSON structures, API payloads, or hierarchical data.

---

## Quick Reference

| Example | Complexity | Key Patterns |
|---------|-----------|--------------|
| **User** | Basic | Field validators, cross-field validation |
| **Order** | Intermediate | Nested objects, business rules, transactions |
| **Nested** | Advanced | Discriminated unions, recursion, context |

## Common Patterns

### Basic Validation
```python
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: EmailStr
    age: int = Field(ge=13, le=120)
```

### Field Validator
```python
from pydantic import field_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError('Username too short')
        return v
```

### Model Validator
```python
from pydantic import model_validator

class User(BaseModel):
    role: str
    age: int

    @model_validator(mode='after')
    def check_admin_age(self):
        if self.role == 'admin' and self.age < 18:
            raise ValueError('Admins must be 18+')
        return self
```

---

Return to [main agent](../data-validator.md)
