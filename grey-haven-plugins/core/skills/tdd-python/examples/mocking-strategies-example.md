# Mocking Strategies Example: Email Notification Service

Comprehensive mocking strategies - when to mock, mock vs stub vs spy, patching techniques.

**Feature**: Email notification service with external SMTP API
**Duration**: 40 minutes
**Framework**: pytest + unittest.mock
**Coverage**: 96% line coverage
**Mocks**: 8 different strategies demonstrated

---

## Mocking Strategies Overview

| Strategy | Purpose | When to Use |
|----------|---------|-------------|
| **Mock** | Verify behavior/calls | Testing interactions |
| **Stub** | Return canned data | Isolate from real dependencies |
| **Spy** | Partial mock | Test real object + verify calls |
| **Patch** | Replace at runtime | External dependencies |
| **MagicMock** | Auto-generate methods | Unknown interfaces |
| **AsyncMock** | Async functions | async/await code |

---

## Project Setup

### Dependencies

```txt
pytest==7.4.3
pytest-mock==3.12.0
```

---

## TDD Session: 40-Minute Workflow

### Strategy 1: Basic Mock (Verify Calls)

#### Use Case
Test that email service calls SMTP client with correct parameters.

```python
# tests/test_email_service.py
from unittest.mock import Mock
import pytest
from app.email_service import EmailService

def test_send_email_calls_smtp_client():
    """Should call SMTP client with correct parameters."""
    # Arrange: Create mock SMTP client
    mock_smtp = Mock()
    service = EmailService(smtp_client=mock_smtp)

    # Act
    service.send_email(
        to="user@example.com",
        subject="Test",
        body="Hello"
    )

    # Assert: Verify method was called with exact arguments
    mock_smtp.send.assert_called_once_with(
        to="user@example.com",
        subject="Test",
        body="Hello",
        from_email="noreply@system.com"
    )
```

#### Implementation

```python
# app/email_service.py
class EmailService:
    """Email notification service."""

    DEFAULT_FROM = "noreply@system.com"

    def __init__(self, smtp_client):
        self.smtp_client = smtp_client

    def send_email(self, to: str, subject: str, body: str) -> None:
        """Send email via SMTP client."""
        self.smtp_client.send(
            to=to,
            subject=subject,
            body=body,
            from_email=self.DEFAULT_FROM
        )
```

**Key Points**:
- ✅ Verify method called once: `assert_called_once_with()`
- ✅ Check exact arguments passed
- ✅ No need to check return value (void method)

---

### Strategy 2: Stub (Return Fake Data)

#### Use Case
Stub SMTP client to return success/failure without real network calls.

```python
def test_send_email_returns_success_status():
    """Should return success when SMTP sends successfully."""
    # Arrange: Stub returns success
    stub_smtp = Mock()
    stub_smtp.send.return_value = {"status": "sent", "message_id": "123"}

    service = EmailService(smtp_client=stub_smtp)

    # Act
    result = service.send_email(
        to="user@example.com",
        subject="Test",
        body="Hello"
    )

    # Assert
    assert result["status"] == "sent"
    assert result["message_id"] == "123"
```

#### Implementation

```python
# app/email_service.py (update)
def send_email(self, to: str, subject: str, body: str) -> dict:
    """Send email via SMTP client."""
    return self.smtp_client.send(
        to=to,
        subject=subject,
        body=body,
        from_email=self.DEFAULT_FROM
    )
```

**Key Points**:
- ✅ Stub returns canned data: `return_value`
- ✅ No real SMTP connection needed
- ✅ Fast, deterministic tests

---

### Strategy 3: Patch Decorator

#### Use Case
Replace module-level SMTP client without changing constructor.

```python
from unittest.mock import patch

@patch('app.email_service.SMTPClient')
def test_send_email_with_patched_smtp(mock_smtp_class):
    """Should create SMTP client and send email."""
    # Arrange: Mock the class constructor
    mock_instance = Mock()
    mock_smtp_class.return_value = mock_instance

    service = EmailService()

    # Act
    service.send_email(
        to="user@example.com",
        subject="Test",
        body="Hello"
    )

    # Assert
    mock_smtp_class.assert_called_once()  # Constructor called
    mock_instance.send.assert_called_once()  # Instance method called
```

#### Implementation

```python
# app/email_service.py (alternate version)
from app.smtp import SMTPClient

class EmailService:
    def __init__(self):
        self.smtp_client = SMTPClient()

    def send_email(self, to: str, subject: str, body: str) -> dict:
        return self.smtp_client.send(
            to=to,
            subject=subject,
            body=body,
            from_email=self.DEFAULT_FROM
        )
```

**Key Points**:
- ✅ Patch at import location: `'app.email_service.SMTPClient'`
- ✅ Mock constructor returns mock instance
- ✅ No dependency injection needed

---

### Strategy 4: Context Manager Patch

#### Use Case
Patch only within specific scope.

```python
def test_send_email_with_context_manager_patch():
    """Should patch SMTP client using context manager."""
    with patch('app.email_service.SMTPClient') as mock_smtp_class:
        mock_instance = Mock()
        mock_smtp_class.return_value = mock_instance

        service = EmailService()
        service.send_email("user@example.com", "Test", "Hello")

        mock_instance.send.assert_called_once()

    # Outside context: real SMTPClient used again
```

**Key Points**:
- ✅ Scope limited to context
- ✅ Cleanup automatic
- ✅ Multiple patches possible

---

### Strategy 5: MagicMock (Auto-Generated Methods)

#### Use Case
Mock object with unknown interface (auto-generates attributes).

```python
from unittest.mock import MagicMock

def test_send_email_template():
    """Should use template service to render email body."""
    # Arrange: MagicMock auto-generates methods
    mock_template_service = MagicMock()
    mock_template_service.render.return_value = "<html>Rendered</html>"

    mock_smtp = Mock()
    service = EmailService(
        smtp_client=mock_smtp,
        template_service=mock_template_service
    )

    # Act
    service.send_templated_email(
        to="user@example.com",
        template="welcome.html",
        context={"name": "John"}
    )

    # Assert
    mock_template_service.render.assert_called_once_with(
        "welcome.html",
        {"name": "John"}
    )
    mock_smtp.send.assert_called_once()
```

#### Implementation

```python
# app/email_service.py (add method)
def send_templated_email(
    self,
    to: str,
    template: str,
    context: dict
) -> dict:
    """Send email using template."""
    body = self.template_service.render(template, context)

    return self.smtp_client.send(
        to=to,
        subject=context.get("subject", "Notification"),
        body=body,
        from_email=self.DEFAULT_FROM
    )
```

**Key Points**:
- ✅ MagicMock auto-generates attributes
- ✅ No need to define all methods
- ✅ Good for complex interfaces

---

### Strategy 6: Side Effects (Dynamic Behavior)

#### Use Case
Mock behavior changes based on arguments.

```python
def test_retry_on_transient_failure():
    """Should retry when SMTP returns transient error."""
    # Arrange: First call fails, second succeeds
    mock_smtp = Mock()
    mock_smtp.send.side_effect = [
        Exception("Connection timeout"),  # First attempt
        {"status": "sent", "message_id": "456"}  # Second attempt (retry)
    ]

    service = EmailService(smtp_client=mock_smtp, max_retries=2)

    # Act
    result = service.send_email("user@example.com", "Test", "Hello")

    # Assert
    assert result["status"] == "sent"
    assert mock_smtp.send.call_count == 2  # Called twice
```

#### Implementation

```python
# app/email_service.py
import time

class EmailService:
    def __init__(self, smtp_client, template_service=None, max_retries=3):
        self.smtp_client = smtp_client
        self.template_service = template_service
        self.max_retries = max_retries

    def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send email with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return self.smtp_client.send(
                    to=to,
                    subject=subject,
                    body=body,
                    from_email=self.DEFAULT_FROM
                )
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait before retry

        raise last_exception  # All retries failed
```

**Key Points**:
- ✅ `side_effect` can be list of return values
- ✅ Or list of exceptions
- ✅ Or callable for dynamic behavior

---

### Strategy 7: Spy (Partial Mock)

#### Use Case
Test real object but verify calls made.

```python
from unittest.mock import Mock, patch

def test_send_email_logs_activity():
    """Should log email activity to audit service."""
    # Arrange: Real email service, spy on logger
    real_logger = Mock()
    service = EmailService(
        smtp_client=Mock(),
        logger=real_logger
    )

    # Act
    service.send_email("user@example.com", "Test", "Hello")

    # Assert: Spy verifies logger called
    real_logger.info.assert_called_with(
        "Email sent to user@example.com"
    )
```

#### Implementation

```python
# app/email_service.py
class EmailService:
    def __init__(self, smtp_client, template_service=None, max_retries=3, logger=None):
        self.smtp_client = smtp_client
        self.template_service = template_service
        self.max_retries = max_retries
        self.logger = logger

    def send_email(self, to: str, subject: str, body: str) -> dict:
        """Send email with logging."""
        result = self.smtp_client.send(
            to=to,
            subject=subject,
            body=body,
            from_email=self.DEFAULT_FROM
        )

        if self.logger:
            self.logger.info(f"Email sent to {to}")

        return result
```

**Key Points**:
- ✅ Spy = mock that wraps real object
- ✅ Real behavior + verification
- ✅ Use `wraps` parameter: `Mock(wraps=real_object)`

---

### Strategy 8: pytest-mock (mocker Fixture)

#### Use Case
Cleaner mocking with pytest fixture.

```python
def test_send_email_with_mocker_fixture(mocker):
    """Should use pytest-mock mocker fixture."""
    # Arrange: mocker.patch is cleaner
    mock_smtp = mocker.Mock()
    mock_smtp.send.return_value = {"status": "sent"}

    service = EmailService(smtp_client=mock_smtp)

    # Act
    result = service.send_email("user@example.com", "Test", "Hello")

    # Assert
    assert result["status"] == "sent"
    mock_smtp.send.assert_called_once()


def test_patch_with_mocker(mocker):
    """Should patch using mocker fixture."""
    mock_smtp_class = mocker.patch('app.email_service.SMTPClient')
    mock_instance = mocker.Mock()
    mock_smtp_class.return_value = mock_instance

    service = EmailService()
    service.send_email("user@example.com", "Test", "Hello")

    mock_instance.send.assert_called_once()
```

**Key Points**:
- ✅ `mocker` fixture from pytest-mock
- ✅ Auto-cleanup (no manual `stop()`)
- ✅ Cleaner syntax than `@patch`

---

## Decision Matrix: When to Use Each Strategy

| Scenario | Strategy | Reason |
|----------|----------|--------|
| Verify method called | Mock | Need to check interactions |
| Return fake data | Stub | Isolate from real dependency |
| Replace module import | Patch | No constructor injection |
| Complex interface | MagicMock | Auto-generate methods |
| Dynamic behavior | Side Effect | Different behavior per call |
| Test real + verify | Spy | Real behavior + tracking |
| pytest project | mocker fixture | Cleaner syntax |
| Async functions | AsyncMock | async/await support |

---

## Anti-Patterns to Avoid

### ❌ Over-Mocking

```python
# BAD: Mocking everything (integration test disguised as unit test)
def test_send_email_with_over_mocking():
    mock_smtp = Mock()
    mock_template = Mock()
    mock_logger = Mock()
    mock_validator = Mock()
    mock_formatter = Mock()
    # ... too many mocks!
```

**Fix**: Mock only external boundaries (database, API, filesystem).

### ❌ Testing Implementation Details

```python
# BAD: Testing private method calls
def test_internal_method_called():
    service = EmailService(Mock())
    service.send_email("user@example.com", "Test", "Hello")

    # Don't test internal implementation!
    service._format_email.assert_called_once()  # ❌ BAD
```

**Fix**: Test public interface only.

### ❌ Brittle Mocks

```python
# BAD: Tight coupling to implementation
mock_smtp.send.assert_called_with(
    "user@example.com",  # Positional args brittle
    "Test",
    "Hello"
)
```

**Fix**: Use keyword arguments for clarity and flexibility.

---

## Coverage Report

```bash
$ pytest --cov=app tests/

---------- coverage: platform darwin, python 3.11.5 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py            0      0   100%
app/email_service.py      48      2    96%
-------------------------------------------
TOTAL                     48      2    96%
```

**Coverage**: 96% line coverage

---

## Summary: Mocking Best Practices

### When to Mock
- ✅ External services (HTTP API, database)
- ✅ Slow operations (file I/O, network)
- ✅ Non-deterministic code (random, time)
- ✅ Third-party libraries
- ❌ Simple pure functions
- ❌ Internal business logic

### Mock Verification
```python
# Verify called
mock.method.assert_called()
mock.method.assert_called_once()
mock.method.assert_called_with(arg1, kwarg1=value)
mock.method.assert_called_once_with(arg1, kwarg1=value)

# Verify call count
assert mock.method.call_count == 3

# Verify NOT called
mock.method.assert_not_called()

# Get call arguments
args, kwargs = mock.method.call_args
```

### Common Patterns
```python
# Return value
mock.method.return_value = result

# Raise exception
mock.method.side_effect = ValueError("error")

# Multiple calls
mock.method.side_effect = [result1, result2, result3]

# Dynamic behavior
def dynamic_response(arg):
    return f"Response for {arg}"
mock.method.side_effect = dynamic_response
```

---

Related: [pytest-tdd-example.md](pytest-tdd-example.md) | [unittest-tdd-example.md](unittest-tdd-example.md) | [Return to INDEX](INDEX.md)
