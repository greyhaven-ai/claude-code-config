# Type Error Debug Example

Debugging type mismatch errors using systematic analysis and type validation.

## Error Encountered

**Environment**: Development
**Severity**: SEV3 (Bug blocking feature development)

### Error Message

```python
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

### Context

Developer implementing new pricing calculation feature receives cryptic type error.

## Stack Trace Analysis

```python
Traceback (most recent call last):
  File "/app/services/pricing.py", line 45, in calculate_total
    total = base_price + discount
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Pattern Match**: `type_mismatch` - Incompatible types in operation

## Code Inspection

```python
# services/pricing.py
def calculate_total(base_price: int, discount: str) -> int:
    """Calculate final price after discount."""
    # Line 45 - THE PROBLEM
    total = base_price + discount  # int + str = TypeError!
    return total
```

**Issue**: `discount` parameter typed as `str` but used in numeric operation.

## Root Cause

API returns discount as string `"10"` instead of integer `10`. Type hint says `str`, but function logic expects `int`.

## Fix Options

### Option 1: Convert String to Int

```python
def calculate_total(base_price: int, discount: str) -> int:
    """Calculate final price after discount."""
    discount_int = int(discount)  # Convert string to int
    total = base_price - discount_int
    return total
```

**Issue**: Still accepts `str` - misleading type hint!

### Option 2: Fix Type Hint (Correct!)

```python
def calculate_total(base_price: int, discount: int) -> int:
    """Calculate final price after discount."""
    total = base_price - discount
    return total
```

**Better**: Type hint matches expected usage.

### Option 3: Input Validation with Pydantic

```python
from pydantic import BaseModel, validator

class PricingInput(BaseModel):
    base_price: int
    discount: int

    @validator('discount')
    def discount_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Discount must be positive')
        return v

def calculate_total(input: PricingInput) -> int:
    """Calculate final price after discount."""
    return input.base_price - input.discount
```

**Best**: Validates at API boundary, type-safe!

## Test

```python
def test_calculate_total_with_valid_types():
    """Test with correct types."""
    result = calculate_total(100, 10)
    assert result == 90

def test_calculate_total_rejects_string_discount():
    """Test rejects string discount."""
    with pytest.raises(ValidationError):
        PricingInput(base_price=100, discount="10")
```

## Prevention

1. **Static type checking**: Run `mypy` in CI/CD
2. **Pydantic validation**: Validate all API inputs
3. **Integration tests**: Test with real API responses

**Type Safety Enforcement**:
```bash
# mypy config
[mypy]
python_version = 3.11
strict = True
disallow_untyped_defs = True
```

---

**Result**: Type error caught at dev time, not production. Type hints + Pydantic prevent recurrence.
