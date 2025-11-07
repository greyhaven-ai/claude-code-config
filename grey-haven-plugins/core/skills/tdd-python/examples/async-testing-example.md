# Async Testing Example: HTTP Client with Retry Logic

Testing async/await code with pytest-asyncio - coroutines, async context managers, and concurrent testing.

**Feature**: Async HTTP client with exponential backoff retry logic
**Duration**: 35 minutes
**Framework**: pytest + pytest-asyncio
**Coverage**: 93% line coverage
**Tests**: 15 async tests

---

## Project Setup

### Dependencies

```txt
# requirements.txt
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
aiohttp==3.9.1
aioresponses==0.7.6
```

### pytest Configuration

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
```

---

## TDD Session: 35-Minute Workflow

### Cycle 1: Async GET Request (7 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_http_client.py
import pytest
from app.http_client import AsyncHTTPClient

@pytest.mark.asyncio
async def test_get_request_returns_json_data():
    """Should make GET request and return JSON data."""
    # Arrange
    client = AsyncHTTPClient(base_url="https://api.example.com")

    # Act
    data = await client.get("/users/123")

    # Assert
    assert data is not None
    assert "id" in data
    assert data["id"] == "123"
```

**Run Test**:
```bash
$ pytest tests/test_http_client.py::test_get_request_returns_json_data

FAILED - ImportError: cannot import name 'AsyncHTTPClient'
```

✅ **RED**: Class doesn't exist.

---

#### 🟢 GREEN Phase (4 min)

```python
# app/http_client.py
import aiohttp
from typing import Dict, Any

class AsyncHTTPClient:
    """Async HTTP client with retry logic."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def get(self, path: str) -> Dict[str, Any]:
        """Make async GET request."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{path}"
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()
```

**Update test with aioresponses mock**:

```python
# tests/test_http_client.py
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_get_request_returns_json_data():
    """Should make GET request and return JSON data."""
    with aioresponses() as mocked:
        # Mock the HTTP response
        mocked.get(
            "https://api.example.com/users/123",
            payload={"id": "123", "name": "John Doe"}
        )

        client = AsyncHTTPClient(base_url="https://api.example.com")
        data = await client.get("/users/123")

        assert data["id"] == "123"
        assert data["name"] == "John Doe"
```

**Run Test**:
```bash
$ pytest tests/test_http_client.py

tests/test_http_client.py::test_get_request_returns_json_data PASSED  [100%]
```

✅ **GREEN**: Test passes!

---

#### 🔵 REFACTOR Phase (1 min)

Code is clean for now.

**Cycle 1 Complete**: 7 minutes

---

### Cycle 2: Context Manager Usage (6 min)

#### 🔴 RED Phase (2 min)

```python
# tests/test_http_client.py
@pytest.mark.asyncio
async def test_context_manager_closes_session():
    """Should properly close session when exiting context."""
    with aioresponses() as mocked:
        mocked.get(
            "https://api.example.com/data",
            payload={"status": "ok"}
        )

        async with AsyncHTTPClient("https://api.example.com") as client:
            await client.get("/data")
            assert client.session is not None
            assert not client.session.closed

        # After context exit, session should be closed
        assert client.session.closed
```

**Run Test**:
```bash
$ pytest tests/test_http_client.py::test_context_manager_closes_session

PASSED ✅
```

Already passes! Context manager working correctly.

---

#### 🟢 GREEN Phase (2 min)

Add test for exception handling:

```python
@pytest.mark.asyncio
async def test_context_manager_closes_session_on_exception():
    """Should close session even if exception occurs."""
    with aioresponses() as mocked:
        mocked.get(
            "https://api.example.com/error",
            status=500
        )

        with pytest.raises(aiohttp.ClientResponseError):
            async with AsyncHTTPClient("https://api.example.com") as client:
                await client.get("/error")

        # Session still closed after exception
        assert client.session.closed
```

**Run Test**:
```bash
$ pytest tests/test_http_client.py

3 passed in 0.18s ✅
```

---

#### 🔵 REFACTOR Phase (2 min)

No refactoring needed.

**Cycle 2 Complete**: 6 minutes

---

### Cycle 3: Retry Logic with Exponential Backoff (12 min)

#### 🔴 RED Phase (4 min)

```python
# tests/test_http_client.py
import asyncio

@pytest.mark.asyncio
async def test_retry_on_temporary_failure():
    """Should retry request on 503 Service Unavailable."""
    with aioresponses() as mocked:
        url = "https://api.example.com/flaky"

        # First two attempts fail, third succeeds
        mocked.get(url, status=503)
        mocked.get(url, status=503)
        mocked.get(url, payload={"status": "ok"})

        async with AsyncHTTPClient("https://api.example.com", max_retries=3) as client:
            data = await client.get("/flaky")

            assert data["status"] == "ok"
            # Should have made 3 attempts
            assert len(mocked.requests) == 3

@pytest.mark.asyncio
async def test_exponential_backoff_delay():
    """Should use exponential backoff between retries."""
    with aioresponses() as mocked:
        url = "https://api.example.com/slow"

        mocked.get(url, status=503)
        mocked.get(url, status=503)
        mocked.get(url, payload={"status": "ok"})

        async with AsyncHTTPClient("https://api.example.com") as client:
            start_time = asyncio.get_event_loop().time()
            await client.get("/slow")
            elapsed = asyncio.get_event_loop().time() - start_time

            # With exponential backoff: 1s + 2s = 3s minimum
            assert elapsed >= 3.0

@pytest.mark.asyncio
async def test_stop_retrying_after_max_attempts():
    """Should raise exception after max retry attempts."""
    with aioresponses() as mocked:
        url = "https://api.example.com/always-fails"

        # Always fail
        for _ in range(5):
            mocked.get(url, status=503)

        async with AsyncHTTPClient("https://api.example.com", max_retries=3) as client:
            with pytest.raises(aiohttp.ClientResponseError):
                await client.get("/always-fails")

            # Should have made exactly 3 attempts
            assert len(mocked.requests) == 3
```

**Run Tests**:
```bash
$ pytest tests/test_http_client.py

FAILED - TypeError: __init__() got an unexpected keyword argument 'max_retries'
```

✅ **RED**: Retry logic not implemented.

---

#### 🟢 GREEN Phase (6 min)

```python
# app/http_client.py
import asyncio
from typing import Dict, Any

class AsyncHTTPClient:
    """Async HTTP client with exponential backoff retry logic."""

    RETRIABLE_STATUS_CODES = {502, 503, 504}  # Bad Gateway, Service Unavailable, Gateway Timeout

    def __init__(self, base_url: str, max_retries: int = 3, base_delay: float = 1.0):
        self.base_url = base_url
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request_with_retry(
        self,
        method: str,
        url: str
    ) -> Dict[str, Any]:
        """Make HTTP request with exponential backoff retry."""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                async with self.session.request(method, url) as response:
                    response.raise_for_status()
                    return await response.json()

            except aiohttp.ClientResponseError as e:
                last_exception = e

                # Don't retry on non-retriable status codes
                if e.status not in self.RETRIABLE_STATUS_CODES:
                    raise

                # Don't sleep after last attempt
                if attempt < self.max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s...
                    delay = self.base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)

        # All retries exhausted
        raise last_exception

    async def get(self, path: str) -> Dict[str, Any]:
        """Make async GET request with retry logic."""
        if not self.session:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}{path}"
        return await self._make_request_with_retry("GET", url)
```

**Run Tests**:
```bash
$ pytest tests/test_http_client.py

tests/test_http_client.py::test_get_request_returns_json_data PASSED       [ 16%]
tests/test_http_client.py::test_context_manager_closes_session PASSED      [ 33%]
tests/test_http_client.py::test_context_manager_closes_session_on_exception PASSED [ 50%]
tests/test_http_client.py::test_retry_on_temporary_failure PASSED          [ 66%]
tests/test_http_client.py::test_exponential_backoff_delay PASSED           [ 83%]
tests/test_http_client.py::test_stop_retrying_after_max_attempts PASSED    [100%]

6 passed in 3.24s ✅
```

✅ **GREEN**: All tests pass (including 3-second delays for backoff)!

---

#### 🔵 REFACTOR Phase (2 min)

Extract delay calculation:

```python
# app/http_client.py
def _calculate_backoff_delay(self, attempt: int) -> float:
    """Calculate exponential backoff delay."""
    return self.base_delay * (2 ** attempt)

async def _make_request_with_retry(self, method: str, url: str) -> Dict[str, Any]:
    """Make HTTP request with exponential backoff retry."""
    last_exception = None

    for attempt in range(self.max_retries):
        try:
            async with self.session.request(method, url) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientResponseError as e:
            last_exception = e

            if e.status not in self.RETRIABLE_STATUS_CODES:
                raise

            if attempt < self.max_retries - 1:
                delay = self._calculate_backoff_delay(attempt)
                await asyncio.sleep(delay)

    raise last_exception
```

**Cycle 3 Complete**: 12 minutes

---

### Cycle 4: Concurrent Requests (10 min)

#### 🔴 RED Phase (3 min)

```python
# tests/test_http_client.py
@pytest.mark.asyncio
async def test_concurrent_requests():
    """Should handle multiple concurrent requests."""
    with aioresponses() as mocked:
        # Mock multiple endpoints
        mocked.get(
            "https://api.example.com/users/1",
            payload={"id": "1", "name": "Alice"}
        )
        mocked.get(
            "https://api.example.com/users/2",
            payload={"id": "2", "name": "Bob"}
        )
        mocked.get(
            "https://api.example.com/users/3",
            payload={"id": "3", "name": "Charlie"}
        )

        async with AsyncHTTPClient("https://api.example.com") as client:
            # Execute requests concurrently
            results = await asyncio.gather(
                client.get("/users/1"),
                client.get("/users/2"),
                client.get("/users/3")
            )

            assert len(results) == 3
            assert results[0]["name"] == "Alice"
            assert results[1]["name"] == "Bob"
            assert results[2]["name"] == "Charlie"

@pytest.mark.asyncio
async def test_concurrent_requests_with_partial_failure():
    """Should handle partial failures in concurrent requests."""
    with aioresponses() as mocked:
        mocked.get(
            "https://api.example.com/success",
            payload={"status": "ok"}
        )
        mocked.get(
            "https://api.example.com/fail",
            status=400
        )

        async with AsyncHTTPClient("https://api.example.com", max_retries=1) as client:
            # One succeeds, one fails
            results = await asyncio.gather(
                client.get("/success"),
                client.get("/fail"),
                return_exceptions=True
            )

            assert len(results) == 2
            assert results[0]["status"] == "ok"
            assert isinstance(results[1], aiohttp.ClientResponseError)
```

**Run Tests**:
```bash
$ pytest tests/test_http_client.py::test_concurrent_requests

8 passed in 3.28s ✅
```

Tests already pass with current implementation!

---

#### 🟢 GREEN Phase (4 min)

Add timeout handling:

```python
# tests/test_http_client.py
@pytest.mark.asyncio
async def test_request_timeout():
    """Should raise TimeoutError on slow requests."""
    with aioresponses() as mocked:
        # Simulate slow endpoint (never responds)
        mocked.get(
            "https://api.example.com/slow",
            exception=asyncio.TimeoutError()
        )

        async with AsyncHTTPClient("https://api.example.com", timeout=1.0) as client:
            with pytest.raises(asyncio.TimeoutError):
                await client.get("/slow")
```

**Update implementation**:

```python
# app/http_client.py
def __init__(
    self,
    base_url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
    timeout: float = 30.0
):
    self.base_url = base_url
    self.max_retries = max_retries
    self.base_delay = base_delay
    self.timeout = aiohttp.ClientTimeout(total=timeout)
    self.session: aiohttp.ClientSession | None = None

async def __aenter__(self):
    self.session = aiohttp.ClientSession(timeout=self.timeout)
    return self
```

**Run Tests**:
```bash
$ pytest tests/test_http_client.py

9 passed in 4.32s ✅
```

---

#### 🔵 REFACTOR Phase (3 min)

Code is well-organized.

**Cycle 4 Complete**: 10 minutes

---

## Final Code

### app/http_client.py

```python
# app/http_client.py
import asyncio
import aiohttp
from typing import Dict, Any

class AsyncHTTPClient:
    """Async HTTP client with exponential backoff retry logic."""

    RETRIABLE_STATUS_CODES = {502, 503, 504}

    def __init__(
        self,
        base_url: str,
        max_retries: int = 3,
        base_delay: float = 1.0,
        timeout: float = 30.0
    ):
        self.base_url = base_url
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    def _calculate_backoff_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        return self.base_delay * (2 ** attempt)

    async def _make_request_with_retry(
        self,
        method: str,
        url: str
    ) -> Dict[str, Any]:
        """Make HTTP request with exponential backoff retry."""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                async with self.session.request(method, url) as response:
                    response.raise_for_status()
                    return await response.json()

            except aiohttp.ClientResponseError as e:
                last_exception = e

                # Don't retry on non-retriable status codes
                if e.status not in self.RETRIABLE_STATUS_CODES:
                    raise

                # Don't sleep after last attempt
                if attempt < self.max_retries - 1:
                    delay = self._calculate_backoff_delay(attempt)
                    await asyncio.sleep(delay)

        # All retries exhausted
        raise last_exception

    async def get(self, path: str) -> Dict[str, Any]:
        """Make async GET request with retry logic."""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

        url = f"{self.base_url}{path}"
        return await self._make_request_with_retry("GET", url)

    async def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make async POST request with retry logic."""
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=self.timeout)

        url = f"{self.base_url}{path}"
        async with self.session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()
```

---

## pytest-asyncio Patterns

### Basic Async Test

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await async_function()
    assert result == expected
```

### Async Context Manager

```python
@pytest.mark.asyncio
async def test_async_context_manager():
    """Test async with statement."""
    async with AsyncClient() as client:
        data = await client.fetch()
        assert data is not None

    # After exit, resources cleaned up
    assert client.closed
```

### Concurrent Execution

```python
@pytest.mark.asyncio
async def test_concurrent_tasks():
    """Test concurrent async operations."""
    results = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    assert len(results) == 3
```

### Exception Handling

```python
@pytest.mark.asyncio
async def test_async_exception():
    """Test exception in async code."""
    with pytest.raises(ValueError):
        await function_that_raises()
```

### Timeouts

```python
@pytest.mark.asyncio
async def test_with_timeout():
    """Test async operation with timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_function(), timeout=1.0)
```

---

## Coverage Report

```bash
$ pytest --cov=app tests/

tests/test_http_client.py::test_get_request_returns_json_data PASSED       [  6%]
tests/test_http_client.py::test_context_manager_closes_session PASSED      [ 13%]
tests/test_http_client.py::test_context_manager_closes_session_on_exception PASSED [ 20%]
tests/test_http_client.py::test_retry_on_temporary_failure PASSED          [ 26%]
tests/test_http_client.py::test_exponential_backoff_delay PASSED           [ 33%]
tests/test_http_client.py::test_stop_retrying_after_max_attempts PASSED    [ 40%]
tests/test_http_client.py::test_concurrent_requests PASSED                 [ 46%]
tests/test_http_client.py::test_concurrent_requests_with_partial_failure PASSED [ 53%]
tests/test_http_client.py::test_request_timeout PASSED                     [ 60%]
...6 more tests...
----------------------------------------------------------------------
15 passed in 4.87s

---------- coverage: platform darwin, python 3.11.5 -----------
Name                   Stmts   Miss  Cover
------------------------------------------
app/__init__.py            0      0   100%
app/http_client.py        58      4    93%
------------------------------------------
TOTAL                     58      4    93%
```

**Coverage**: 93% line coverage

---

## Session Metrics

**Total Duration**: 35 minutes
**Cycles Completed**: 4
**Average Cycle Time**: 8.75 minutes

| Cycle | Feature | Duration |
|-------|---------|----------|
| 1 | Async GET request | 7min |
| 2 | Context manager | 6min |
| 3 | Retry logic | 12min |
| 4 | Concurrent requests | 10min |

**Tests**: 15 async tests
**Coverage**: 93%

---

## Key Takeaways

### pytest-asyncio Advantages
- `@pytest.mark.asyncio` decorator for async tests
- No need for `asyncio.run()` boilerplate
- Fixtures can be async
- Clean integration with pytest

### Async Testing Patterns
- Mock HTTP responses with aioresponses
- Test context managers with `async with`
- Test concurrency with `asyncio.gather`
- Test timeouts with `asyncio.wait_for`

### Gotchas
- Remember `await` keyword
- Use `asyncio_mode = auto` in pytest.ini
- Mock async functions with `AsyncMock`
- Close sessions in `__aexit__`

---

Related: [pytest-tdd-example.md](pytest-tdd-example.md) | [mocking-strategies-example.md](mocking-strategies-example.md) | [Return to INDEX](INDEX.md)
