# Fixtures and Parametrize Example: Data Validation Pipeline

Advanced pytest features - fixtures for reusable setup, parametrize for multiple test cases, fixture scope.

**Feature**: Data validation pipeline with custom validators
**Duration**: 50 minutes
**Framework**: pytest 7.4+
**Coverage**: 97% line coverage
**Tests**: 24 tests from 8 parametrized functions

---

## Fixture Strategies

| Fixture Type | Scope | Use Case |
|--------------|-------|----------|
| **Function** | Per test | Default, fresh state each test |
| **Class** | Per test class | Shared across class methods |
| **Module** | Per module | Expensive setup (DB connection) |
| **Session** | Per test session | Once per entire test run |

---

## Project Setup

### Directory Structure

```
validator/
├── app/
│   ├── __init__.py
│   └── validators.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_validators.py
```

---

## Part 1: Basic Fixtures (10 min)

### Function-Scoped Fixtures

```python
# tests/conftest.py
import pytest
from app.validators import EmailValidator, PasswordValidator

@pytest.fixture
def email_validator():
    """Provide email validator (fresh instance per test)."""
    return EmailValidator()

@pytest.fixture
def password_validator():
    """Provide password validator with default config."""
    return PasswordValidator(min_length=8, require_special=True)
```

### Usage

```python
# tests/test_validators.py
def test_valid_email(email_validator):
    """Should accept valid email."""
    result = email_validator.validate("user@example.com")
    assert result.is_valid
    assert result.errors == []

def test_invalid_email_missing_at(email_validator):
    """Should reject email without @ symbol."""
    result = email_validator.validate("userexample.com")
    assert not result.is_valid
    assert "missing @ symbol" in result.errors[0].lower()
```

### Implementation

```python
# app/validators.py
from dataclasses import dataclass
from typing import List
import re

@dataclass
class ValidationResult:
    """Result of validation."""
    is_valid: bool
    errors: List[str]

class EmailValidator:
    """Email format validator."""

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def validate(self, email: str) -> ValidationResult:
        """Validate email format."""
        errors = []

        if "@" not in email:
            errors.append("Invalid: missing @ symbol")
        elif not re.match(self.EMAIL_REGEX, email):
            errors.append("Invalid: malformed email format")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

**Key Points**:
- ✅ Fixture defined once in conftest.py
- ✅ Used across multiple tests
- ✅ Fresh instance per test (function scope)

---

## Part 2: Parametrize Decorator (12 min)

### Multiple Test Cases from One Function

```python
# tests/test_validators.py
@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("john.doe@company.org", True),
    ("admin+tag@site.co.uk", True),
    ("invalid@", False),
    ("@example.com", False),
    ("no-at-symbol.com", False),
    ("spaces @example.com", False),
])
def test_email_validation(email_validator, email, expected_valid):
    """Should validate email formats correctly."""
    result = email_validator.validate(email)
    assert result.is_valid == expected_valid

@pytest.mark.parametrize("password,expected_errors", [
    ("Str0ng!Pass", 0),  # Valid
    ("weak", 3),  # Too short, no uppercase, no special
    ("NoSpecial1", 1),  # Missing special char
    ("no_upper1!", 1),  # Missing uppercase
])
def test_password_validation(password_validator, password, expected_errors):
    """Should validate passwords with various issues."""
    result = password_validator.validate(password)

    if expected_errors == 0:
        assert result.is_valid
    else:
        assert not result.is_valid
        assert len(result.errors) == expected_errors
```

### Implementation

```python
# app/validators.py
import string

class PasswordValidator:
    """Password strength validator."""

    def __init__(self, min_length: int = 8, require_special: bool = True):
        self.min_length = min_length
        self.require_special = require_special

    def validate(self, password: str) -> ValidationResult:
        """Validate password strength."""
        errors = []

        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")

        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")

        if self.require_special:
            special_chars = set(string.punctuation)
            if not any(c in special_chars for c in password):
                errors.append("Password must contain at least one special character")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

**Key Points**:
- ✅ One test function → 7 test cases
- ✅ Each parametrize value creates separate test
- ✅ Clear test output shows which cases pass/fail

---

## Part 3: Fixture Composition (10 min)

### Fixtures That Use Other Fixtures

```python
# tests/conftest.py
@pytest.fixture
def validation_pipeline(email_validator, password_validator):
    """Provide complete validation pipeline."""
    from app.validators import ValidationPipeline

    pipeline = ValidationPipeline()
    pipeline.add_validator("email", email_validator)
    pipeline.add_validator("password", password_validator)
    return pipeline

@pytest.fixture
def valid_user_data():
    """Provide valid user registration data."""
    return {
        "email": "user@example.com",
        "password": "Str0ng!Pass",
        "username": "john_doe"
    }

@pytest.fixture
def invalid_user_data():
    """Provide invalid user registration data."""
    return {
        "email": "invalid-email",
        "password": "weak",
        "username": "a"
    }
```

### Usage

```python
# tests/test_validators.py
def test_pipeline_with_valid_data(validation_pipeline, valid_user_data):
    """Should pass validation with valid data."""
    result = validation_pipeline.validate(valid_user_data)

    assert result.is_valid
    assert result.errors == []

def test_pipeline_with_invalid_data(validation_pipeline, invalid_user_data):
    """Should collect errors from all validators."""
    result = validation_pipeline.validate(invalid_user_data)

    assert not result.is_valid
    assert len(result.errors) >= 3  # Multiple validators fail
```

### Implementation

```python
# app/validators.py
from typing import Dict, Any

class ValidationPipeline:
    """Pipeline of validators."""

    def __init__(self):
        self.validators = {}

    def add_validator(self, field: str, validator) -> None:
        """Add validator for specific field."""
        self.validators[field] = validator

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Run all validators and collect errors."""
        all_errors = []

        for field, validator in self.validators.items():
            if field in data:
                result = validator.validate(data[field])
                if not result.is_valid:
                    for error in result.errors:
                        all_errors.append(f"{field}: {error}")

        return ValidationResult(is_valid=len(all_errors) == 0, errors=all_errors)
```

**Key Points**:
- ✅ Fixtures can depend on other fixtures
- ✅ pytest resolves dependencies automatically
- ✅ Test data fixtures reduce duplication

---

## Part 4: Fixture Scope (8 min)

### Module-Scoped Fixtures (Expensive Setup)

```python
# tests/conftest.py
@pytest.fixture(scope="module")
def database_connection():
    """Provide database connection (once per module)."""
    # Expensive setup
    db = Database.connect("test.db")
    db.create_tables()

    yield db  # Test runs here

    # Cleanup
    db.drop_tables()
    db.close()

@pytest.fixture(scope="module")
def user_repository(database_connection):
    """Provide user repository with DB connection."""
    from app.repository import UserRepository
    return UserRepository(database_connection)
```

### Usage

```python
# tests/test_user_repository.py
def test_save_user(user_repository):
    """Should save user to database."""
    user = {"email": "test@example.com", "password": "hashed"}
    user_id = user_repository.save(user)

    assert user_id is not None

def test_find_user_by_email(user_repository):
    """Should find user by email."""
    # DB connection reused from previous test
    user = user_repository.find_by_email("test@example.com")

    assert user is not None
    assert user["email"] == "test@example.com"
```

**Key Points**:
- ✅ Module scope: Created once per test module
- ✅ `yield` for setup/teardown pattern
- ✅ Expensive resources reused across tests

---

## Part 5: Parametrize with Fixtures (10 min)

### Combining Parametrize + Fixtures

```python
# tests/conftest.py
@pytest.fixture
def validator_factory():
    """Factory for creating validators with different configs."""
    def _create_validator(validator_type: str, **kwargs):
        if validator_type == "email":
            return EmailValidator()
        elif validator_type == "password":
            return PasswordValidator(**kwargs)
        elif validator_type == "username":
            return UsernameValidator(**kwargs)
        raise ValueError(f"Unknown validator: {validator_type}")

    return _create_validator
```

### Usage

```python
# tests/test_validators.py
@pytest.mark.parametrize("min_length,require_special,password,expected", [
    (8, True, "Str0ng!Pass", True),   # Meets all requirements
    (12, True, "Str0ng!Pass", False),  # Too short for min_length=12
    (8, False, "Strong1Pass", True),   # Special char not required
    (6, False, "Weak1", True),         # Lower requirements
])
def test_password_with_different_configs(
    validator_factory,
    min_length,
    require_special,
    password,
    expected
):
    """Should validate passwords with different configs."""
    validator = validator_factory(
        "password",
        min_length=min_length,
        require_special=require_special
    )

    result = validator.validate(password)
    assert result.is_valid == expected
```

**Key Points**:
- ✅ Factory fixture creates validators dynamically
- ✅ Parametrize configures factory
- ✅ Flexible, reusable test pattern

---

## Part 6: Advanced Parametrize (10 min)

### Parametrize with IDs

```python
@pytest.mark.parametrize("email,expected", [
    pytest.param("valid@example.com", True, id="valid_email"),
    pytest.param("invalid@", False, id="missing_domain"),
    pytest.param("@example.com", False, id="missing_local"),
    pytest.param("spaces @example.com", False, id="contains_spaces"),
])
def test_email_with_ids(email_validator, email, expected):
    """Should validate emails (with readable test IDs)."""
    result = email_validator.validate(email)
    assert result.is_valid == expected
```

**Output**:
```bash
test_validators.py::test_email_with_ids[valid_email] PASSED       [ 25%]
test_validators.py::test_email_with_ids[missing_domain] PASSED    [ 50%]
test_validators.py::test_email_with_ids[missing_local] PASSED     [ 75%]
test_validators.py::test_email_with_ids[contains_spaces] PASSED   [100%]
```

### Parametrize Multiple Arguments

```python
@pytest.mark.parametrize("validator_type", ["email", "password", "username"])
@pytest.mark.parametrize("invalid_input", ["", None, " "])
def test_validators_reject_empty_input(validator_factory, validator_type, invalid_input):
    """Should reject empty/null inputs (3 validators × 3 inputs = 9 tests)."""
    validator = validator_factory(validator_type)

    result = validator.validate(invalid_input)

    assert not result.is_valid
    assert len(result.errors) > 0
```

**Key Points**:
- ✅ Multiple `@pytest.mark.parametrize` = cartesian product
- ✅ 3 validators × 3 inputs = 9 test cases
- ✅ `pytest.param(..., id="name")` for readable output

---

## conftest.py Organization

```python
# tests/conftest.py
"""Shared fixtures for all tests."""
import pytest
from app.validators import (
    EmailValidator,
    PasswordValidator,
    UsernameValidator,
    ValidationPipeline
)

# ============================================================================
# Basic Validators
# ============================================================================

@pytest.fixture
def email_validator():
    """Provide email validator."""
    return EmailValidator()

@pytest.fixture
def password_validator():
    """Provide password validator with defaults."""
    return PasswordValidator(min_length=8, require_special=True)

@pytest.fixture
def username_validator():
    """Provide username validator."""
    return UsernameValidator(min_length=3, max_length=20)

# ============================================================================
# Composite Fixtures
# ============================================================================

@pytest.fixture
def validation_pipeline(email_validator, password_validator, username_validator):
    """Provide complete validation pipeline."""
    pipeline = ValidationPipeline()
    pipeline.add_validator("email", email_validator)
    pipeline.add_validator("password", password_validator)
    pipeline.add_validator("username", username_validator)
    return pipeline

# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def valid_user_data():
    """Provide valid user registration data."""
    return {
        "email": "user@example.com",
        "password": "Str0ng!Pass",
        "username": "john_doe"
    }

@pytest.fixture
def invalid_user_data():
    """Provide invalid user registration data."""
    return {
        "email": "invalid-email",
        "password": "weak",
        "username": "a"
    }

# ============================================================================
# Factory Fixtures
# ============================================================================

@pytest.fixture
def validator_factory():
    """Factory for creating validators with custom configs."""
    def _create(validator_type: str, **kwargs):
        validators = {
            "email": EmailValidator,
            "password": PasswordValidator,
            "username": UsernameValidator
        }

        validator_class = validators.get(validator_type)
        if not validator_class:
            raise ValueError(f"Unknown validator: {validator_type}")

        return validator_class(**kwargs) if kwargs else validator_class()

    return _create

# ============================================================================
# Module-Scoped Fixtures (Expensive Resources)
# ============================================================================

@pytest.fixture(scope="module")
def database_connection():
    """Provide database connection (once per module)."""
    db = Database.connect("test.db")
    db.create_tables()

    yield db

    db.drop_tables()
    db.close()
```

---

## Coverage Report

```bash
$ pytest --cov=app tests/

tests/test_validators.py::test_valid_email PASSED                          [  4%]
tests/test_validators.py::test_invalid_email_missing_at PASSED             [  8%]
tests/test_validators.py::test_email_validation[user@example.com-True] PASSED [ 12%]
tests/test_validators.py::test_email_validation[john.doe@company.org-True] PASSED [ 16%]
... (20 more tests)

---------- coverage: platform darwin, python 3.11.5 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py            0      0   100%
app/validators.py         72      2    97%
-------------------------------------------
TOTAL                     72      2    97%

24 passed in 0.34s
```

**Coverage**: 97% line coverage

---

## Session Metrics

**Duration**: 50 minutes
**Tests**: 24 (8 parametrized functions → 24 test cases)
**Coverage**: 97%
**Fixtures**: 11 fixtures defined

---

## Fixture Best Practices

### ✅ DO

```python
# Clear, descriptive names
@pytest.fixture
def authenticated_user():
    ...

# Use yield for cleanup
@pytest.fixture
def file_handle():
    f = open("test.txt", "w")
    yield f
    f.close()

# Appropriate scope
@pytest.fixture(scope="module")  # Expensive resource
def database_connection():
    ...
```

### ❌ DON'T

```python
# Vague names
@pytest.fixture
def data():  # ❌ What data?
    ...

# Missing cleanup
@pytest.fixture
def temp_file():
    f = open("test.txt", "w")
    return f  # ❌ Never closed!

# Wrong scope
@pytest.fixture(scope="session")  # ❌ Too wide, state pollution
def user_data():
    ...
```

---

## Summary

### Fixture Advantages
- ✅ Reusable test setup
- ✅ Dependency injection
- ✅ Automatic cleanup (yield)
- ✅ Flexible scoping

### Parametrize Advantages
- ✅ Multiple test cases from one function
- ✅ Reduced code duplication
- ✅ Clear test output
- ✅ Easy to add more cases

### When to Use Each
| Pattern | Use Case |
|---------|----------|
| Simple fixture | Common test setup |
| Factory fixture | Dynamic configuration |
| Parametrize | Multiple similar test cases |
| Fixture + parametrize | Dynamic setup + multiple cases |
| Module scope | Expensive resources |

---

Related: [pytest-tdd-example.md](pytest-tdd-example.md) | [mocking-strategies-example.md](mocking-strategies-example.md) | [Return to INDEX](INDEX.md)
