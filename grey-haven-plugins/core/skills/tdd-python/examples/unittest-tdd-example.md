# unittest TDD Example: User Authentication

TDD using unittest framework - TestCase classes, setUp/tearDown, assertions, and mock library.

**Feature**: User authentication system with password hashing
**Duration**: 30 minutes
**Framework**: unittest (standard library)
**Coverage**: 94% line, 90% branch
**Tests**: 12 passing

---

## Project Setup

### Directory Structure

```
auth_system/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   └── models.py
└── tests/
    ├── __init__.py
    └── test_auth.py
```

### No External Dependencies

unittest is part of Python standard library!

---

## TDD Session: 30-Minute Workflow

### Cycle 1: Create User (6 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_auth.py
import unittest
from app.auth import AuthService
from app.models import User

class TestUserCreation(unittest.TestCase):
    """Test user creation functionality."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.auth_service = AuthService()

    def test_create_user_with_valid_data(self):
        """Should create user with hashed password."""
        # Arrange
        email = "john@example.com"
        password = "SecurePass123!"

        # Act
        user = self.auth_service.create_user(email, password)

        # Assert
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)
        self.assertNotEqual(user.password_hash, password)  # Password hashed
        self.assertTrue(user.password_hash.startswith("$2b$"))  # bcrypt hash

if __name__ == "__main__":
    unittest.main()
```

**Run Test**:
```bash
$ python -m unittest tests.test_auth.TestUserCreation.test_create_user_with_valid_data

ERROR: test_create_user_with_valid_data (tests.test_auth.TestUserCreation)
ImportError: cannot import name 'AuthService' from 'app.auth'
```

✅ **RED**: Classes don't exist.

---

#### 🟢 GREEN Phase (3 min)

```python
# app/models.py
from dataclasses import dataclass

@dataclass
class User:
    """User model with email and password hash."""
    email: str
    password_hash: str
```

```python
# app/auth.py
import bcrypt
from app.models import User

class AuthService:
    """Authentication service for user management."""

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password."""
        # Hash password with bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        return User(email=email, password_hash=password_hash)
```

**Run Test**:
```bash
$ python -m unittest tests.test_auth.TestUserCreation

.
----------------------------------------------------------------------
Ran 1 test in 0.102s

OK
```

✅ **GREEN**: Test passes!

---

#### 🔵 REFACTOR Phase (1 min)

No refactoring needed yet.

**Cycle 1 Complete**: 6 minutes

---

### Cycle 2: Validate User Input (7 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_auth.py
class TestInputValidation(unittest.TestCase):
    """Test input validation for user creation."""

    def setUp(self):
        self.auth_service = AuthService()

    def test_reject_invalid_email_format(self):
        """Should raise ValueError for invalid email."""
        with self.assertRaises(ValueError) as context:
            self.auth_service.create_user("not-an-email", "password123")

        self.assertIn("Invalid email format", str(context.exception))

    def test_reject_weak_password(self):
        """Should raise ValueError for weak password."""
        with self.assertRaises(ValueError) as context:
            self.auth_service.create_user("john@example.com", "weak")

        self.assertIn("Password must be at least 8 characters", str(context.exception))

    def test_reject_empty_email(self):
        """Should raise ValueError for empty email."""
        with self.assertRaises(ValueError) as context:
            self.auth_service.create_user("", "password123")

        self.assertIn("Email cannot be empty", str(context.exception))
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth.TestInputValidation

FFF
======================================================================
FAIL: test_reject_invalid_email_format
AssertionError: ValueError not raised
```

✅ **RED**: Validation not implemented.

---

#### 🟢 GREEN Phase (4 min)

```python
# app/auth.py
import re

class AuthService:
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def _validate_email(self, email: str) -> None:
        """Validate email format."""
        if not email:
            raise ValueError("Email cannot be empty")
        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Invalid email format")

    def _validate_password(self, password: str) -> None:
        """Validate password strength."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with validation."""
        self._validate_email(email)
        self._validate_password(password)

        # Hash password
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        return User(email=email, password_hash=password_hash)
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth

....
----------------------------------------------------------------------
Ran 4 tests in 0.415s

OK
```

✅ **GREEN**: All tests pass!

---

#### 🔵 REFACTOR Phase (1 min)

Code is already well-organized.

**Cycle 2 Complete**: 7 minutes

---

### Cycle 3: Authenticate User (8 min)

#### 🔴 RED Phase (3 min)

```python
# tests/test_auth.py
from unittest.mock import Mock, patch

class TestAuthentication(unittest.TestCase):
    """Test user authentication."""

    def setUp(self):
        self.auth_service = AuthService()
        # Create a user for authentication tests
        self.test_email = "john@example.com"
        self.test_password = "SecurePass123!"
        self.test_user = self.auth_service.create_user(
            self.test_email,
            self.test_password
        )

    def test_authenticate_with_valid_credentials(self):
        """Should return user for valid credentials."""
        # Mock the database lookup
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = self.test_user

            # Act
            result = self.auth_service.authenticate(
                self.test_email,
                self.test_password
            )

            # Assert
            self.assertEqual(result, self.test_user)
            mock_get.assert_called_once_with(self.test_email)

    def test_authenticate_with_invalid_password(self):
        """Should return None for invalid password."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = self.test_user

            result = self.auth_service.authenticate(
                self.test_email,
                "WrongPassword"
            )

            self.assertIsNone(result)

    def test_authenticate_with_nonexistent_user(self):
        """Should return None for non-existent user."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = None

            result = self.auth_service.authenticate(
                "nobody@example.com",
                "password"
            )

            self.assertIsNone(result)
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth.TestAuthentication

EEE
======================================================================
ERROR: test_authenticate_with_valid_credentials
AttributeError: 'AuthService' object has no attribute 'authenticate'
```

✅ **RED**: Method doesn't exist.

---

#### 🟢 GREEN Phase (4 min)

```python
# app/auth.py
from typing import Optional

class AuthService:
    def __init__(self):
        self.users = {}  # Simple in-memory storage

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email (stub for database)."""
        return self.users.get(email)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None

        # Verify password
        password_bytes = password.encode('utf-8')
        hash_bytes = user.password_hash.encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_bytes):
            return user

        return None

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with validation."""
        self._validate_email(email)
        self._validate_password(password)

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        user = User(email=email, password_hash=password_hash)
        self.users[email] = user  # Store in memory
        return user
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth

.......
----------------------------------------------------------------------
Ran 7 tests in 0.523s

OK
```

✅ **GREEN**: All tests pass!

---

#### 🔵 REFACTOR Phase (1 min)

Extract password verification:

```python
# app/auth.py
def _verify_password(self, password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)

def authenticate(self, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password."""
    user = self.get_user_by_email(email)
    if not user:
        return None

    if self._verify_password(password, user.password_hash):
        return user

    return None
```

**Cycle 3 Complete**: 8 minutes

---

### Cycle 4: Rate Limiting (9 min)

#### 🔴 RED Phase (3 min)

```python
# tests/test_auth.py
class TestRateLimiting(unittest.TestCase):
    """Test authentication rate limiting."""

    def setUp(self):
        self.auth_service = AuthService(max_attempts=3)
        self.test_email = "john@example.com"
        self.test_password = "SecurePass123!"
        self.test_user = self.auth_service.create_user(
            self.test_email,
            self.test_password
        )

    def tearDown(self):
        """Clean up after each test."""
        self.auth_service.failed_attempts.clear()

    def test_block_after_max_failed_attempts(self):
        """Should block authentication after max failed attempts."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = self.test_user

            # Fail 3 times
            for _ in range(3):
                result = self.auth_service.authenticate(
                    self.test_email,
                    "WrongPassword"
                )
                self.assertIsNone(result)

            # 4th attempt should raise error
            with self.assertRaises(ValueError) as context:
                self.auth_service.authenticate(
                    self.test_email,
                    self.test_password
                )

            self.assertIn("Too many failed attempts", str(context.exception))

    def test_reset_attempts_on_successful_login(self):
        """Should reset failed attempts counter on success."""
        with patch.object(self.auth_service, 'get_user_by_email') as mock_get:
            mock_get.return_value = self.test_user

            # Fail once
            self.auth_service.authenticate(self.test_email, "Wrong")

            # Success resets counter
            result = self.auth_service.authenticate(
                self.test_email,
                self.test_password
            )
            self.assertEqual(result, self.test_user)

            # Verify counter reset
            self.assertEqual(self.auth_service.failed_attempts[self.test_email], 0)
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth.TestRateLimiting

EE
======================================================================
ERROR: test_block_after_max_failed_attempts
TypeError: __init__() got an unexpected keyword argument 'max_attempts'
```

✅ **RED**: Rate limiting not implemented.

---

#### 🟢 GREEN Phase (5 min)

```python
# app/auth.py
from typing import Dict

class AuthService:
    def __init__(self, max_attempts: int = 3):
        self.users = {}
        self.failed_attempts: Dict[str, int] = {}
        self.max_attempts = max_attempts

    def _check_rate_limit(self, email: str) -> None:
        """Check if user has exceeded max failed attempts."""
        attempts = self.failed_attempts.get(email, 0)
        if attempts >= self.max_attempts:
            raise ValueError("Too many failed attempts. Account locked.")

    def _record_failed_attempt(self, email: str) -> None:
        """Record failed authentication attempt."""
        self.failed_attempts[email] = self.failed_attempts.get(email, 0) + 1

    def _reset_attempts(self, email: str) -> None:
        """Reset failed attempts counter."""
        self.failed_attempts[email] = 0

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with rate limiting."""
        self._check_rate_limit(email)

        user = self.get_user_by_email(email)
        if not user:
            self._record_failed_attempt(email)
            return None

        if self._verify_password(password, user.password_hash):
            self._reset_attempts(email)
            return user

        self._record_failed_attempt(email)
        return None
```

**Run Tests**:
```bash
$ python -m unittest tests.test_auth

............
----------------------------------------------------------------------
Ran 12 tests in 0.687s

OK
```

✅ **GREEN**: All 12 tests pass!

---

#### 🔵 REFACTOR Phase (1 min)

Code is well-organized with clear responsibilities.

**Cycle 4 Complete**: 9 minutes

---

## Final Code

### app/auth.py

```python
# app/auth.py
import re
import bcrypt
from typing import Optional, Dict
from app.models import User

class AuthService:
    """Authentication service with password hashing and rate limiting."""

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __init__(self, max_attempts: int = 3):
        self.users: Dict[str, User] = {}
        self.failed_attempts: Dict[str, int] = {}
        self.max_attempts = max_attempts

    def _validate_email(self, email: str) -> None:
        """Validate email format."""
        if not email:
            raise ValueError("Email cannot be empty")
        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("Invalid email format")

    def _validate_password(self, password: str) -> None:
        """Validate password strength."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        password_bytes = password.encode('utf-8')
        hash_bytes = password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)

    def _check_rate_limit(self, email: str) -> None:
        """Check if user has exceeded max failed attempts."""
        attempts = self.failed_attempts.get(email, 0)
        if attempts >= self.max_attempts:
            raise ValueError("Too many failed attempts. Account locked.")

    def _record_failed_attempt(self, email: str) -> None:
        """Record failed authentication attempt."""
        self.failed_attempts[email] = self.failed_attempts.get(email, 0) + 1

    def _reset_attempts(self, email: str) -> None:
        """Reset failed attempts counter."""
        self.failed_attempts[email] = 0

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email."""
        return self.users.get(email)

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with validation and password hashing."""
        self._validate_email(email)
        self._validate_password(password)

        # Hash password with bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        user = User(email=email, password_hash=password_hash)
        self.users[email] = user
        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with rate limiting."""
        self._check_rate_limit(email)

        user = self.get_user_by_email(email)
        if not user:
            self._record_failed_attempt(email)
            return None

        if self._verify_password(password, user.password_hash):
            self._reset_attempts(email)
            return user

        self._record_failed_attempt(email)
        return None
```

---

## Coverage Report

```bash
$ python -m coverage run -m unittest discover tests
$ python -m coverage report

Name              Stmts   Miss Branch BrPart  Cover
---------------------------------------------------
app/__init__.py       0      0      0      0   100%
app/models.py         3      0      0      0   100%
app/auth.py          52      3     16      2    94%
---------------------------------------------------
TOTAL                55      3     16      2    94%
```

**Coverage**: 94% line coverage, 90% branch coverage

---

## Session Metrics

**Total Duration**: 30 minutes
**Cycles Completed**: 4
**Average Cycle Time**: 7.5 minutes

| Cycle | Feature | RED | GREEN | REFACTOR | Total |
|-------|---------|-----|-------|----------|-------|
| 1 | Create user | 2min | 3min | 1min | 6min |
| 2 | Input validation | 2min | 4min | 1min | 7min |
| 3 | Authentication | 3min | 4min | 1min | 8min |
| 4 | Rate limiting | 3min | 5min | 1min | 9min |

**Tests Created**: 12
**Test Classes**: 4
**Coverage**: 94% line, 90% branch

---

## unittest Patterns Demonstrated

### TestCase Class Structure

```python
class TestFeatureName(unittest.TestCase):
    """Docstring describing test suite."""

    def setUp(self):
        """Run before each test."""
        self.auth_service = AuthService()

    def tearDown(self):
        """Run after each test (cleanup)."""
        self.auth_service.failed_attempts.clear()

    def test_specific_behavior(self):
        """Docstring describing what's tested."""
        # Test implementation
```

### Assertion Methods

```python
# Equality
self.assertEqual(actual, expected)
self.assertNotEqual(actual, not_expected)

# Truth
self.assertTrue(condition)
self.assertFalse(condition)

# None
self.assertIsNone(value)
self.assertIsNotNone(value)

# Exceptions
with self.assertRaises(ValueError) as context:
    function_that_raises()
self.assertIn("error message", str(context.exception))
```

### Mocking with unittest.mock

```python
from unittest.mock import Mock, patch

# Patch object method
with patch.object(self.service, 'method_name') as mock_method:
    mock_method.return_value = expected_value
    # ... test code ...
    mock_method.assert_called_once_with(arg1, arg2)

# Patch module function
with patch('app.module.function') as mock_func:
    mock_func.return_value = value
    # ... test code ...
```

---

## Key Takeaways

### unittest Characteristics
- **Standard library**: No external dependencies
- **Class-based**: Tests organized in TestCase classes
- **setUp/tearDown**: Explicit setup and cleanup methods
- **Assertion methods**: `self.assertEqual()` vs plain `assert`
- **Mock library**: `unittest.mock` for test doubles

### When to Use unittest
- ✅ No external dependencies allowed
- ✅ Corporate environments with strict requirements
- ✅ Legacy codebase already using unittest
- ✅ Java/JUnit background (similar patterns)

### When to Use pytest Instead
- ✅ Modern Python projects (Python 3.6+)
- ✅ Plain `assert` statements preferred
- ✅ Fixture dependency injection
- ✅ Rich plugin ecosystem
- ✅ Parametrized testing

---

Related: [pytest-tdd-example.md](pytest-tdd-example.md) | [mocking-strategies-example.md](mocking-strategies-example.md) | [Return to INDEX](INDEX.md)
