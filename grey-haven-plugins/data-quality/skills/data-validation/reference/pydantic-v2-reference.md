# Pydantic v2 Reference

Comprehensive guide to Pydantic v2 for data validation in Grey Haven applications.

## Core Concepts

### BaseModel

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    """All Pydantic models inherit from BaseModel."""
    id: int
    name: str
    email: str
```

### Field Definitions

```python
from pydantic import Field
from typing import Optional

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=99999.99)
    description: Optional[str] = Field(None, max_length=500)
    in_stock: bool = Field(default=True)
```

## Field Types and Constraints

### String Constraints

```python
from pydantic import constr, EmailStr, HttpUrl

class UserProfile(BaseModel):
    # Email validation
    email: EmailStr

    # String with constraints
    username: constr(
        min_length=3,
        max_length=30,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )

    # URL validation
    website: HttpUrl

    # Optional string with max length
    bio: Optional[constr(max_length=500)] = None
```

### Numeric Constraints

```python
from pydantic import conint, confloat
from decimal import Decimal

class OrderItem(BaseModel):
    # Integer constraints
    quantity: conint(ge=1, le=999)

    # Float constraints
    weight: confloat(gt=0, le=1000.0)

    # Decimal for currency (recommended)
    price: Decimal = Field(..., max_digits=10, decimal_places=2, gt=0)
```

### Date and Time

```python
from datetime import datetime, date, time
from pydantic import Field, AwareDatetime

class Event(BaseModel):
    # Naive datetime
    created_at: datetime

    # Timezone-aware datetime
    scheduled_at: AwareDatetime

    # Date only
    event_date: date

    # Time only
    event_time: time

    # Past date constraint
    birth_date: date = Field(..., le=date.today())
```

### Collections

```python
from typing import List, Set, Dict
from pydantic import Field

class Team(BaseModel):
    # List with min/max items
    members: List[str] = Field(..., min_length=1, max_length=50)

    # Set (no duplicates)
    tags: Set[str] = Field(default_factory=set)

    # Dict
    metadata: Dict[str, str] = Field(default_factory=dict)

    # List with item constraints
    scores: List[conint(ge=0, le=100)] = []
```

### Enums and Literals

```python
from enum import Enum
from typing import Literal

class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

class User(BaseModel):
    # Enum field
    role: UserRole = UserRole.USER

    # Literal (inline)
    status: Literal['active', 'inactive', 'suspended'] = 'active'
```

## Model Configuration

### model_config

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name: str
    email: str

    model_config = ConfigDict(
        # Strip whitespace from strings
        str_strip_whitespace=True,

        # Validate on assignment
        validate_assignment=True,

        # Enable ORM mode (for SQLModel)
        from_attributes=True,

        # Forbid extra fields
        extra='forbid',

        # Use enum values (not names)
        use_enum_values=True,

        # Populate by field name (not alias)
        populate_by_name=True,

        # JSON schema customization
        json_schema_extra={
            'examples': [{
                'name': 'Alice Johnson',
                'email': 'alice@example.com'
            }]
        }
    )
```

## Validation

### Field Validators

```python
from pydantic import field_validator

class User(BaseModel):
    username: str
    email: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  # Normalize to lowercase

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Restrict to company domain."""
        if not v.endswith('@company.com'):
            raise ValueError('Must use company email')
        return v
```

### Model Validators

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def validate_date_range(self):
        """Ensure end_date is after start_date."""
        if self.end_date < self.start_date:
            raise ValueError('end_date must be after start_date')
        return self
```

### Validator Modes

```python
from pydantic import field_validator

class Example(BaseModel):
    value: int

    # Before validation - receives raw input
    @field_validator('value', mode='before')
    @classmethod
    def parse_value(cls, v):
        if isinstance(v, str):
            return int(v)
        return v

    # After validation - receives typed value
    @field_validator('value', mode='after')
    @classmethod
    def validate_range(cls, v: int) -> int:
        if v < 0 or v > 100:
            raise ValueError('Must be 0-100')
        return v
```

## Serialization

### Model Dump

```python
user = User(name='Alice', email='alice@example.com')

# Python dict
user_dict = user.model_dump()

# JSON string
user_json = user.model_dump_json()

# Exclude fields
user_dict = user.model_dump(exclude={'password'})

# Include only specific fields
user_dict = user.model_dump(include={'name', 'email'})

# Exclude None values
user_dict = user.model_dump(exclude_none=True)
```

### Serialization Modes

```python
from datetime import datetime
from pydantic import BaseModel, field_serializer

class Event(BaseModel):
    name: str
    created_at: datetime

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime, _info):
        """Custom datetime serialization."""
        return dt.isoformat()

# Mode-specific serialization
event.model_dump(mode='json')  # JSON-compatible types
event.model_dump(mode='python')  # Python objects
```

## Error Handling

### ValidationError

```python
from pydantic import ValidationError

try:
    user = User(name='', email='invalid')
except ValidationError as e:
    # Get errors as list of dicts
    errors = e.errors()
    # [
    #   {
    #     'type': 'string_too_short',
    #     'loc': ('name',),
    #     'msg': 'String should have at least 1 character',
    #     'input': '',
    #     'ctx': {'min_length': 1}
    #   },
    #   {
    #     'type': 'value_error',
    #     'loc': ('email',),
    #     'msg': 'Invalid email format',
    #     'input': 'invalid'
    #   }
    # ]

    # JSON format
    print(e.json())
```

### Custom Error Messages

```python
from pydantic import Field, field_validator

class User(BaseModel):
    age: int = Field(..., ge=13, le=120)

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Must be 18 or older to register', code='age_restriction')
        return v
```

## Advanced Patterns

### Computed Fields

```python
from pydantic import computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
```

### Field Aliases

```python
from pydantic import Field

class User(BaseModel):
    # API uses 'userName', Python uses 'user_name'
    user_name: str = Field(..., alias='userName')
    email_address: str = Field(..., alias='emailAddress')

    model_config = {'populate_by_name': True}

# Parse from API
user = User.model_validate({'userName': 'alice', 'emailAddress': 'alice@example.com'})

# Access in Python
print(user.user_name)  # 'alice'
```

### Root Validators

```python
from pydantic import RootModel
from typing import List

class UserList(RootModel[List[User]]):
    """Validate list of users."""
    root: List[User]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

users = UserList([
    {'name': 'Alice', 'email': 'alice@example.com'},
    {'name': 'Bob', 'email': 'bob@example.com'}
])
```

## Performance Tips

### Avoid Unnecessary Validation

```python
# Parse with validation
user = User.model_validate(data)

# Parse without validation (trusted data)
user = User.model_construct(**data)
```

### Reuse Models

```python
# Cache model schemas
from pydantic import TypeAdapter

user_adapter = TypeAdapter(User)

# Reuse for multiple validations
user1 = user_adapter.validate_python(data1)
user2 = user_adapter.validate_python(data2)
```

### Lazy Validation

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

    model_config = {
        # Only validate changed fields
        'validate_assignment': False,
        # Defer validation until access
        'defer_build': True
    }
```

## Migration from Pydantic v1

### Key Changes

| Pydantic v1 | Pydantic v2 |
|-------------|-------------|
| `class Config:` | `model_config = ConfigDict(...)` |
| `@validator` | `@field_validator` / `@model_validator` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `parse_obj()` | `model_validate()` |
| `orm_mode = True` | `from_attributes = True` |

### Example Migration

**Pydantic v1:**
```python
class User(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator('name')
    def validate_name(cls, v):
        return v.strip()
```

**Pydantic v2:**
```python
class User(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()
```

## Summary

| Feature | Syntax | Use Case |
|---------|--------|----------|
| **Field Types** | `EmailStr`, `constr`, `conint` | Type constraints |
| **Validation** | `@field_validator`, `@model_validator` | Custom rules |
| **Config** | `model_config = ConfigDict(...)` | Model behavior |
| **Serialization** | `.model_dump()`, `.model_dump_json()` | Export data |
| **Error Handling** | `ValidationError.errors()` | Parse validation failures |

---

**Next**: [Validators Reference](validators-reference.md) | **Index**: [Reference Index](INDEX.md)
