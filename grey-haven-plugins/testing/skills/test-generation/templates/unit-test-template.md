# Unit Test Template

Copy-paste unit test templates for TypeScript (Vitest) and Python (pytest).

## TypeScript / Vitest Template

### Basic Component Test

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  // CUSTOMIZE: Add setup if needed
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render with default props', () => {
      render(<ComponentName />);

      // CUSTOMIZE: Check for expected elements
      expect(screen.getByText('Expected Text')).toBeInTheDocument();
    });

    it('should render with custom props', () => {
      render(<ComponentName title="Custom Title" />);

      expect(screen.getByText('Custom Title')).toBeInTheDocument();
    });

    it('should not render when condition is false', () => {
      render(<ComponentName isVisible={false} />);

      // CUSTOMIZE: Check element is not present
      expect(screen.queryByText('Expected Text')).not.toBeInTheDocument();
    });
  });

  describe('User Interactions', () => {
    it('should handle button click', async () => {
      const handleClick = vi.fn();
      render(<ComponentName onClick={handleClick} />);

      // CUSTOMIZE: Replace with your button/element
      const button = screen.getByRole('button', { name: /click me/i });
      fireEvent.click(button);

      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should handle form input', async () => {
      const handleChange = vi.fn();
      render(<ComponentName onChange={handleChange} />);

      // CUSTOMIZE: Replace with your input
      const input = screen.getByLabelText(/name/i);
      fireEvent.change(input, { target: { value: 'John Doe' } });

      expect(handleChange).toHaveBeenCalledWith('John Doe');
    });

    it('should handle form submission', async () => {
      const handleSubmit = vi.fn();
      render(<ComponentName onSubmit={handleSubmit} />);

      // CUSTOMIZE: Fill in form fields
      const nameInput = screen.getByLabelText(/name/i);
      fireEvent.change(nameInput, { target: { value: 'John Doe' } });

      const submitButton = screen.getByRole('button', { name: /submit/i });
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(handleSubmit).toHaveBeenCalledWith({
          name: 'John Doe',
          // CUSTOMIZE: Add expected form data
        });
      });
    });
  });

  describe('Loading States', () => {
    it('should show loading state', () => {
      render(<ComponentName isLoading={true} />);

      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    it('should hide content while loading', () => {
      render(<ComponentName isLoading={true} />);

      expect(screen.queryByText('Expected Content')).not.toBeInTheDocument();
    });
  });

  describe('Error States', () => {
    it('should display error message', () => {
      const error = 'Something went wrong';
      render(<ComponentName error={error} />);

      expect(screen.getByText(error)).toBeInTheDocument();
    });

    it('should call error handler', () => {
      const handleError = vi.fn();
      render(<ComponentName onError={handleError} />);

      // CUSTOMIZE: Trigger error condition
      const button = screen.getByRole('button');
      fireEvent.click(button);

      expect(handleError).toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    it('should have accessible button', () => {
      render(<ComponentName />);

      // CUSTOMIZE: Check ARIA attributes
      const button = screen.getByRole('button', { name: /submit/i });
      expect(button).toHaveAttribute('aria-label', 'Submit form');
    });

    it('should have accessible form inputs', () => {
      render(<ComponentName />);

      // CUSTOMIZE: Check labels
      const input = screen.getByLabelText(/email/i);
      expect(input).toHaveAttribute('type', 'email');
    });
  });
});
```

### Service/Hook Test

```typescript
import { describe, it, expect, vi } from 'vitest';
import { YourService } from './YourService';

describe('YourService', () => {
  let service: YourService;

  beforeEach(() => {
    // CUSTOMIZE: Setup service dependencies
    const mockDependency = {
      method: vi.fn(),
    };

    service = new YourService(mockDependency);
  });

  describe('methodName', () => {
    it('should return expected result with valid input', async () => {
      // Arrange
      const input = { id: '123', name: 'Test' };

      // Act
      const result = await service.methodName(input);

      // Assert
      expect(result).toEqual({
        // CUSTOMIZE: Expected output
        id: '123',
        success: true,
      });
    });

    it('should throw error with invalid input', async () => {
      // Arrange
      const invalidInput = { id: '' };

      // Act & Assert
      await expect(service.methodName(invalidInput)).rejects.toThrow(
        'Invalid input'
      );
    });

    it('should call dependency method', async () => {
      // Arrange
      const input = { id: '123' };
      const mockMethod = vi.fn().mockResolvedValue({ success: true });
      service.dependency.method = mockMethod;

      // Act
      await service.methodName(input);

      // Assert
      expect(mockMethod).toHaveBeenCalledWith('123');
    });
  });
});
```

### Utility Function Test

```typescript
import { describe, it, expect } from 'vitest';
import { functionName } from './utils';

describe('functionName', () => {
  it('should handle valid input', () => {
    // CUSTOMIZE: Test cases
    expect(functionName('input')).toBe('expected output');
  });

  it('should handle edge cases', () => {
    expect(functionName('')).toBe('');
    expect(functionName(null)).toBe('');
    expect(functionName(undefined)).toBe('');
  });

  it('should throw error for invalid input', () => {
    expect(() => functionName('invalid')).toThrow('Error message');
  });

  // CUSTOMIZE: Parametrized tests for multiple inputs
  it.each([
    ['input1', 'output1'],
    ['input2', 'output2'],
    ['input3', 'output3'],
  ])('functionName(%s) should return %s', (input, expected) => {
    expect(functionName(input)).toBe(expected);
  });
});
```

## Python / pytest Template

### Basic Function Test

```python
import pytest
from app.services import YourService

class TestYourService:
    """Tests for YourService class"""

    @pytest.fixture
    def service(self):
        """Create service instance for tests"""
        # CUSTOMIZE: Setup dependencies
        return YourService()

    def test_method_name_with_valid_input(self, service):
        """Should return expected result with valid input"""
        # Arrange
        input_data = {"id": "123", "name": "Test"}

        # Act
        result = service.method_name(input_data)

        # Assert
        assert result["id"] == "123"
        assert result["success"] is True

    def test_method_name_with_invalid_input(self, service):
        """Should raise error with invalid input"""
        # Arrange
        invalid_input = {"id": ""}

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            service.method_name(invalid_input)

    def test_method_name_calls_dependency(self, service, mocker):
        """Should call dependency method"""
        # Arrange
        mock_method = mocker.patch.object(service.dependency, 'method')
        mock_method.return_value = {"success": True}

        # Act
        service.method_name({"id": "123"})

        # Assert
        mock_method.assert_called_once_with("123")
```

### FastAPI Endpoint Test

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.models import User

@pytest.fixture(name="session")
def session_fixture():
    """Create test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with database session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

class TestUserEndpoints:
    """Tests for user API endpoints"""

    def test_create_user(self, client: TestClient):
        """Should create user with valid data"""
        # Arrange
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "role": "member",
        }

        # Act
        response = client.post("/users", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    def test_create_user_with_duplicate_email(self, client: TestClient, session: Session):
        """Should reject duplicate email"""
        # Arrange
        existing_user = User(name="Jane", email="john@example.com", role="member")
        session.add(existing_user)
        session.commit()

        # Act
        response = client.post("/users", json={
            "name": "John Doe",
            "email": "john@example.com",
            "role": "member",
        })

        # Assert
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_get_user(self, client: TestClient, session: Session):
        """Should retrieve user by ID"""
        # Arrange
        user = User(name="John Doe", email="john@example.com", role="member")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Act
        response = client.get(f"/users/{user.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user.id
        assert data["name"] == "John Doe"

    def test_get_user_not_found(self, client: TestClient):
        """Should return 404 for non-existent user"""
        # Act
        response = client.get("/users/999")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
```

### Parametrized Test

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    ("test@", False),
])
def test_validate_email(input_value, expected):
    """Should validate email format correctly"""
    result = validate_email(input_value)
    assert result == expected

@pytest.mark.parametrize("age,valid", [
    (0, True),
    (18, True),
    (120, True),
    (-1, False),
    (121, False),
])
def test_validate_age(age, valid):
    """Should validate age range"""
    result = validate_age(age)
    assert result == valid
```

### Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Should handle async operation"""
    # Arrange
    service = AsyncService()

    # Act
    result = await service.async_method()

    # Assert
    assert result is not None
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_async_with_mock(mocker):
    """Should mock async dependency"""
    # Arrange
    mock_response = {"data": "test"}
    mocker.patch('app.services.async_api_call', return_value=mock_response)

    # Act
    result = await call_async_api()

    # Assert
    assert result == mock_response
```

## Usage Instructions

1. **Copy template** to your test file
2. **Replace placeholders**:
   - `ComponentName` → Your component name
   - `YourService` → Your service class name
   - `methodName` → Your method name
   - `functionName` → Your function name
3. **Customize assertions** for your specific logic
4. **Add more test cases** as needed
5. **Run tests**: `npm test` or `pytest`

## Checklist

- [ ] All happy path scenarios tested
- [ ] Error cases tested
- [ ] Edge cases tested (null, empty, boundary values)
- [ ] User interactions tested (if applicable)
- [ ] Loading states tested (if applicable)
- [ ] Accessibility tested (if applicable)
- [ ] All public methods tested
- [ ] Coverage > 80%

---

Related: [Integration Test Template](integration-test-template.md) | [Test Fixtures Template](test-fixtures-template.md) | [Return to INDEX](INDEX.md)
