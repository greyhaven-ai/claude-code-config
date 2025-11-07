# Validators Reference

Comprehensive guide to Pydantic field and model validators for custom validation logic.

## Field Validators

### Basic Field Validator

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  # Normalize
```

### Multiple Fields

```python
class Product(BaseModel):
    name: str
    sku: str

    @field_validator('name', 'sku')
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Validate multiple fields with same rule."""
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
```

### Validator Modes

#### Before Mode (Pre-validation)

```python
class Example(BaseModel):
    value: int

    @field_validator('value', mode='before')
    @classmethod
    def coerce_to_int(cls, v):
        """Convert string to int before type validation."""
        if isinstance(v, str):
            return int(v)
        return v

# Can parse string as int
example = Example(value='42')  # Works!
```

#### After Mode (Post-validation)

```python
class Example(BaseModel):
    email: str

    @field_validator('email', mode='after')
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Normalize after type validation."""
        return v.lower().strip()
```

#### Wrap Mode (Full Control)

```python
from pydantic import field_validator, ValidationInfo
from typing import Any

class Example(BaseModel):
    value: int

    @field_validator('value', mode='wrap')
    @classmethod
    def validate_with_wrap(cls, v: Any, handler, info: ValidationInfo) -> int:
        """Full control over validation."""
        try:
            # Call default validation
            result = handler(v)
            # Additional checks
            if result < 0:
                raise ValueError('Must be non-negative')
            return result
        except ValueError:
            # Fallback
            return 0
```

## Model Validators

### Cross-Field Validation

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def validate_date_range(self):
        """Validate relationship between fields."""
        if self.end_date < self.start_date:
            raise ValueError('end_date must be after start_date')
        return self
```

### Conditional Validation

```python
class Document(BaseModel):
    status: Literal['draft', 'published']
    content: str
    publish_date: Optional[date] = None

    @model_validator(mode='after')
    def validate_published(self):
        """Require fields for published documents."""
        if self.status == 'published':
            if not self.content or len(self.content) < 100:
                raise ValueError('Published documents must have substantial content')
            if not self.publish_date:
                raise ValueError('Published documents must have publish_date')
        return self
```

## Accessing Other Fields

### Using ValidationInfo

```python
from pydantic import field_validator, ValidationInfo

class User(BaseModel):
    role: str
    permissions: List[str]

    @field_validator('permissions')
    @classmethod
    def validate_permissions(cls, v: List[str], info: ValidationInfo) -> List[str]:
        """Validate permissions based on role."""
        role = info.data.get('role')

        if role == 'admin':
            # Admins can have any permissions
            return v

        # Regular users have restricted permissions
        allowed = {'read', 'write'}
        if any(p not in allowed for p in v):
            raise ValueError(f'Invalid permissions for role: {role}')

        return v
```

### Validation Context

```python
from pydantic import ValidationInfo

class Order(BaseModel):
    total: Decimal
    payment_method: str

    @field_validator('payment_method')
    @classmethod
    def validate_payment(cls, v: str, info: ValidationInfo) -> str:
        """Use context for validation."""
        context = info.context
        if context:
            max_cash = context.get('max_cash_amount', 1000)
            total = info.data.get('total', 0)

            if v == 'cash' and total > max_cash:
                raise ValueError(f'Cash payments limited to ${max_cash}')

        return v

# Use context
order = Order.model_validate(
    {'total': 1500, 'payment_method': 'cash'},
    context={'max_cash_amount': 1000}
)  # Raises error
```

## Reusable Validators

### Validator Functions

```python
from pydantic import field_validator

def validate_positive(v: float) -> float:
    """Reusable positive number validator."""
    if v <= 0:
        raise ValueError('Must be positive')
    return v

def validate_us_phone(v: str) -> str:
    """Reusable US phone validator."""
    import re
    pattern = r'^\d{3}-\d{3}-\d{4}$'
    if not re.match(pattern, v):
        raise ValueError('Invalid US phone format (XXX-XXX-XXXX)')
    return v

class Product(BaseModel):
    price: float
    weight: float

    _validate_price = field_validator('price')(classmethod(validate_positive))
    _validate_weight = field_validator('weight')(classmethod(validate_positive))

class Contact(BaseModel):
    phone: str
    mobile: str

    _validate_phone = field_validator('phone')(classmethod(validate_us_phone))
    _validate_mobile = field_validator('mobile')(classmethod(validate_us_phone))
```

## Common Validation Patterns

### Email Domain Restriction

```python
class CorporateUser(BaseModel):
    email: EmailStr

    @field_validator('email')
    @classmethod
    def validate_corporate_email(cls, v: str) -> str:
        """Restrict to corporate domain."""
        allowed_domains = ['company.com', 'company.net']
        domain = v.split('@')[1]
        if domain not in allowed_domains:
            raise ValueError(f'Email must use corporate domain')
        return v
```

### Password Strength

```python
class PasswordReset(BaseModel):
    new_password: str
    confirm_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Ensure password meets requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain number')
        return v

    @model_validator(mode='after')
    def passwords_match(self):
        """Ensure passwords match."""
        if self.new_password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
```

### URL Validation

```python
class SocialProfile(BaseModel):
    twitter_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None

    @field_validator('twitter_url')
    @classmethod
    def validate_twitter(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        """Validate Twitter URL format."""
        if v and 'twitter.com' not in str(v):
            raise ValueError('Must be a Twitter URL')
        return v

    @field_validator('linkedin_url')
    @classmethod
    def validate_linkedin(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        """Validate LinkedIn URL format."""
        if v and 'linkedin.com' not in str(v):
            raise ValueError('Must be a LinkedIn URL')
        return v
```

### List Uniqueness

```python
class Team(BaseModel):
    member_ids: List[UUID]

    @field_validator('member_ids')
    @classmethod
    def validate_unique_members(cls, v: List[UUID]) -> List[UUID]:
        """Ensure no duplicate members."""
        if len(v) != len(set(v)):
            raise ValueError('Duplicate member IDs found')
        return v
```

### Currency Validation

```python
class Transaction(BaseModel):
    amount: Decimal
    currency: str

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate currency amount."""
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v.as_tuple().exponent < -2:
            raise ValueError('Maximum 2 decimal places')
        return v

    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate ISO currency code."""
        valid_currencies = {'USD', 'EUR', 'GBP', 'JPY'}
        if v not in valid_currencies:
            raise ValueError(f'Invalid currency. Must be one of: {valid_currencies}')
        return v.upper()
```

### Conditional Required Fields

```python
class ShippingOrder(BaseModel):
    shipping_method: Literal['pickup', 'delivery']
    address: Optional[str] = None
    pickup_location: Optional[str] = None

    @model_validator(mode='after')
    def validate_shipping_details(self):
        """Require appropriate fields based on method."""
        if self.shipping_method == 'delivery' and not self.address:
            raise ValueError('Address required for delivery')
        if self.shipping_method == 'pickup' and not self.pickup_location:
            raise ValueError('Pickup location required')
        return self
```

### Profanity Filter

```python
class Comment(BaseModel):
    content: str

    @field_validator('content')
    @classmethod
    def validate_no_profanity(cls, v: str) -> str:
        """Block inappropriate content."""
        profanity_list = ['bad', 'words', 'here']  # In real app, use library
        content_lower = v.lower()
        if any(word in content_lower for word in profanity_list):
            raise ValueError('Content contains inappropriate language')
        return v
```

## Error Messages

### Custom Error Messages

```python
class Age(BaseModel):
    value: int

    @field_validator('value')
    @classmethod
    def validate_age(cls, v: int) -> int:
        """Validate age with custom message."""
        if v < 0:
            raise ValueError('Age cannot be negative')
        if v > 150:
            raise ValueError('Age exceeds reasonable maximum')
        if v < 18:
            raise ValueError(
                'Must be 18 or older',
                code='age_restriction'  # Custom error code
            )
        return v
```

### Detailed Error Context

```python
class Product(BaseModel):
    name: str
    price: Decimal

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Decimal, info: ValidationInfo) -> Decimal:
        """Provide context in error."""
        if v < 0:
            product_name = info.data.get('name', 'Unknown')
            raise ValueError(
                f'Price for "{product_name}" cannot be negative'
            )
        return v
```

## Best Practices

1. **Use Type Hints**: Always provide proper type hints for validator methods
2. **Return Values**: Always return the value (even if unchanged)
3. **Validator Order**: Validators run after type validation by default
4. **Reuse Logic**: Extract common validators to reusable functions
5. **Clear Messages**: Provide actionable error messages
6. **Performance**: Use `mode='before'` sparingly (it runs on every field)

## Summary

| Validator Type | Use Case | Example |
|----------------|----------|---------|
| **@field_validator** | Single field validation | Username format check |
| **@model_validator** | Cross-field validation | Start/end date comparison |
| **mode='before'** | Pre-process input | String to int conversion |
| **mode='after'** | Post-process value | Email normalization |
| **ValidationInfo** | Access other fields | Role-based permissions |
| **Reusable validators** | Share logic | Phone, email patterns |

---

**Previous**: [Pydantic v2 Reference](pydantic-v2-reference.md) | **Next**: [SQLModel Alignment](sqlmodel-alignment.md) | **Index**: [Reference Index](INDEX.md)
