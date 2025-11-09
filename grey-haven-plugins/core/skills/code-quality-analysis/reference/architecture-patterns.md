# Architecture Patterns

Best practices for clean architecture, layering, dependency management, and preventing architectural erosion.

## Layered Architecture

### 3-Layer Architecture (Standard)

```
┌──────────────────────────┐
│   Presentation Layer     │  ← API endpoints, controllers, routes
├──────────────────────────┤
│   Business Logic Layer   │  ← Services, domain logic, use cases
├──────────────────────────┤
│   Data Access Layer      │  ← Repositories, database, external APIs
└──────────────────────────┘
```

**Rules**:
1. Higher layers depend on lower layers (never reverse)
2. Each layer has single responsibility
3. No layer skipping (API must go through Business, not directly to Data)

### Implementation Example

**Correct Layering**:
```python
# ✅ API Layer (Presentation)
from fastapi import APIRouter
from services.user_service import UserService

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: str, service: UserService = Depends()):
    """API layer only handles HTTP, delegates to service."""
    return service.get_user(user_id)

# ✅ Service Layer (Business Logic)
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: str) -> User:
        """Business logic: validation, authorization, etc."""
        user = self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

# ✅ Repository Layer (Data Access)
from sqlmodel import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Data access only, no business logic."""
        return self.db.query(User).filter(User.id == user_id).first()
```

**Incorrect Layering** (Anti-pattern):
```python
# ❌ API directly accessing database (skips 2 layers!)
@router.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends()):
    user = db.query(User).filter(User.id == user_id).first()
    return user

# ❌ Service accessing database directly (skips repository)
class UserService:
    def get_user(self, user_id: str, db: Session) -> User:
        return db.query(User).filter(User.id == user_id).first()
```

## Dependency Injection

**Problem**: Tight coupling between components

**Solution**: Inject dependencies instead of creating them

### Without DI (Tight Coupling)

```python
# ❌ Bad: Tight coupling
class UserService:
    def __init__(self):
        self.db = Database()  # Creates dependency internally
        self.email = EmailService()  # Can't replace with mock

    def create_user(self, email: str):
        user = User(email=email)
        self.db.save(user)
        self.email.send_welcome(email)
```

**Problems**:
- Hard to test (can't mock `Database` or `EmailService`)
- Hard to change implementation
- Service "owns" dependencies

### With DI (Loose Coupling)

```python
# ✅ Good: Dependency injection
class UserService:
    def __init__(self, db: Database, email: EmailService):
        self.db = db  # Dependencies injected
        self.email = email

    def create_user(self, email: str):
        user = User(email=email)
        self.db.save(user)
        self.email.send_welcome(email)

# Testing becomes easy
def test_create_user():
    mock_db = Mock(spec=Database)
    mock_email = Mock(spec=EmailService)

    service = UserService(db=mock_db, email=mock_email)
    service.create_user("test@example.com")

    mock_db.save.assert_called_once()
    mock_email.send_welcome.assert_called_once()
```

### DI Container (FastAPI Example)

```python
from fastapi import Depends
from typing import Annotated

# Define dependencies
def get_db() -> Database:
    return Database()

def get_email_service() -> EmailService:
    return EmailService()

def get_user_repository(
    db: Annotated[Database, Depends(get_db)]
) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repository)

# Use in endpoints
@app.get("/users/{user_id}")
def get_user(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return service.get_user(user_id)
```

## Circular Dependency Prevention

**Problem**: Module A imports Module B, Module B imports Module A

### Detecting Circular Dependencies

```bash
# Python
pydeps app/ --show-cycles

# Output:
app.services.user_service → app.services.team_service → app.services.user_service
```

### Example Circular Dependency

```python
# ❌ Bad: Circular dependency
# services/user_service.py
from services.team_service import get_user_teams

class UserService:
    def get_user_with_teams(self, user_id):
        user = self.get_user(user_id)
        teams = get_user_teams(user_id)  # Calls team service
        return {**user, "teams": teams}

# services/team_service.py
from services.user_service import get_team_members  # ← Circular!

class TeamService:
    def get_team_with_members(self, team_id):
        team = self.get_team(team_id)
        members = get_team_members(team_id)  # Calls user service
        return {**team, "members": members}
```

### Solution 1: Extract to Shared Module

```python
# ✅ Good: Shared aggregation service
# services/aggregation_service.py
class AggregationService:
    def __init__(self, user_repo, team_repo):
        self.user_repo = user_repo
        self.team_repo = team_repo

    def get_user_with_teams(self, user_id):
        user = self.user_repo.find_by_id(user_id)
        teams = self.team_repo.find_by_user_id(user_id)
        return {**user, "teams": teams}

# No circular dependencies!
```

### Solution 2: Dependency Inversion

```python
# ✅ Good: Use interfaces/protocols
from typing import Protocol

class TeamProvider(Protocol):
    def get_teams_for_user(self, user_id: str) -> List[Team]:
        ...

class UserService:
    def __init__(self, team_provider: TeamProvider):
        self.team_provider = team_provider

    def get_user_with_teams(self, user_id):
        user = self.get_user(user_id)
        teams = self.team_provider.get_teams_for_user(user_id)
        return {**user, "teams": teams}
```

## Module Organization

### Feature-Based Structure (Recommended)

```
app/
├── features/
│   ├── users/
│   │   ├── api.py          # User API endpoints
│   │   ├── service.py      # User business logic
│   │   ├── repository.py   # User data access
│   │   ├── models.py       # User models
│   │   └── tests/
│   ├── orders/
│   │   ├── api.py
│   │   ├── service.py
│   │   ├── repository.py
│   │   └── tests/
│   └── payments/
│       ├── api.py
│       ├── service.py
│       └── repository.py
└── shared/
    ├── database.py         # Shared database connection
    ├── errors.py           # Shared error definitions
    └── utils.py            # Shared utilities
```

**Benefits**:
- All user-related code in one place
- Easy to find related files
- Can extract feature to separate service
- Clear boundaries

### Layer-Based Structure (Traditional)

```
app/
├── api/
│   ├── users.py
│   ├── orders.py
│   └── payments.py
├── services/
│   ├── user_service.py
│   ├── order_service.py
│   └── payment_service.py
├── repositories/
│   ├── user_repository.py
│   ├── order_repository.py
│   └── payment_repository.py
└── models/
    ├── user.py
    ├── order.py
    └── payment.py
```

**Drawbacks**:
- Related code scattered across directories
- Harder to extract features
- Less clear boundaries

## Interface Segregation

**Principle**: Clients shouldn't depend on interfaces they don't use

### Before (Fat Interface)

```python
# ❌ Bad: Fat interface
class UserRepository:
    def find_by_id(self, user_id): ...
    def find_by_email(self, email): ...
    def find_all(self): ...
    def create(self, user): ...
    def update(self, user): ...
    def delete(self, user_id): ...
    def find_by_role(self, role): ...
    def find_active_users(self): ...
    def find_by_created_date(self, date): ...
    # 20+ methods...

# Service only needs 2 methods but depends on all 20!
class LoginService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, email, password):
        user = self.user_repo.find_by_email(email)  # Only uses 1 method
        # ...
```

### After (Segregated Interfaces)

```python
# ✅ Good: Segregated interfaces
from typing import Protocol

class UserFinder(Protocol):
    def find_by_email(self, email: str) -> Optional[User]: ...

class UserCreator(Protocol):
    def create(self, user: User) -> User: ...

class UserUpdater(Protocol):
    def update(self, user: User) -> User: ...

# Service depends only on what it needs
class LoginService:
    def __init__(self, user_finder: UserFinder):
        self.user_finder = user_finder  # Only depends on finder

    def authenticate(self, email: str, password: str):
        user = self.user_finder.find_by_email(email)
        # ...

# Repository implements all interfaces
class UserRepository(UserFinder, UserCreator, UserUpdater):
    def find_by_email(self, email: str) -> Optional[User]: ...
    def create(self, user: User) -> User: ...
    def update(self, user: User) -> User: ...
```

## Repository Pattern

**Purpose**: Abstract data access from business logic

### Implementation

```python
# ✅ Repository interface
from typing import Protocol, List, Optional

class UserRepository(Protocol):
    def find_by_id(self, user_id: str) -> Optional[User]: ...
    def find_by_email(self, email: str) -> Optional[User]: ...
    def find_all(self) -> List[User]: ...
    def save(self, user: User) -> User: ...
    def delete(self, user_id: str) -> None: ...

# ✅ SQL implementation
class SQLUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

# ✅ Can swap implementations without changing business logic
class InMemoryUserRepository:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def save(self, user: User) -> User:
        self.users[user.id] = user
        return user

# ✅ Service doesn't care about implementation
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository  # Works with any implementation

    def create_user(self, email: str) -> User:
        if self.repository.find_by_email(email):
            raise ValueError("Email exists")

        user = User(email=email)
        return self.repository.save(user)
```

## Service Layer Pattern

**Purpose**: Encapsulate business logic, orchestrate operations

### Example

```python
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        inventory: InventoryService,
        payment: PaymentService,
        notifications: NotificationService
    ):
        self.order_repo = order_repo
        self.inventory = inventory
        self.payment = payment
        self.notifications = notifications

    def create_order(self, user_id: str, items: List[OrderItem]) -> Order:
        """
        Business logic: validate, process payment, update inventory, notify.
        Orchestrates multiple operations across services.
        """
        # Business validation
        self._validate_order_items(items)

        # Check inventory
        if not self.inventory.check_availability(items):
            raise OutOfStockError("Some items unavailable")

        # Calculate total
        total = self._calculate_total(items)

        # Process payment
        payment_result = self.payment.charge(user_id, total)
        if not payment_result.success:
            raise PaymentError("Payment failed")

        # Create order
        order = Order(user_id=user_id, items=items, total=total)
        order = self.order_repo.save(order)

        # Update inventory
        self.inventory.decrement_stock(items)

        # Send notification
        self.notifications.send_order_confirmation(user_id, order.id)

        return order
```

## Preventing Architectural Erosion

### 1. Architectural Tests

```python
# tests/architecture/test_layer_violations.py
import ast
import os

def test_no_repository_imports_in_api_layer():
    """API layer should not import repositories directly."""
    api_files = glob.glob("app/api/**/*.py", recursive=True)

    for file_path in api_files:
        with open(file_path) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if "repositories" in node.module:
                    pytest.fail(
                        f"{file_path} imports from repositories layer. "
                        f"API should only depend on services."
                    )

def test_no_database_imports_in_services():
    """Services should not import database directly."""
    service_files = glob.glob("app/services/**/*.py", recursive=True)

    for file_path in service_files:
        with open(file_path) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "sqlalchemy" or "database.connection" in node.module:
                    pytest.fail(
                        f"{file_path} imports database directly. "
                        f"Services should only use repositories."
                    )
```

### 2. Dependency Rules

```python
# pyproject.toml
[tool.dependency-check]
allow = [
    "api -> services",
    "api -> models",
    "services -> repositories",
    "services -> models",
    "repositories -> database",
]

deny = [
    "api -> repositories",  # API must go through services
    "api -> database",      # API must not access database
    "services -> database", # Services must use repositories
]
```

### 3. Code Review Checklist

```markdown
## Architecture Review Checklist

Layer Compliance:
- [ ] API endpoints only call services (not repositories/database)
- [ ] Services use repositories (not direct database access)
- [ ] Repositories only contain data access logic

Dependency Injection:
- [ ] Dependencies injected (not created internally)
- [ ] Testable with mocks

Circular Dependencies:
- [ ] No circular imports detected
- [ ] Dependencies flow in one direction

Separation of Concerns:
- [ ] Business logic in services (not API or repositories)
- [ ] Validation at appropriate layer
- [ ] No mixed responsibilities
```

## Quick Reference

### Architectural Principles

| Principle | Description | Benefit |
|-----------|-------------|---------|
| Separation of Concerns | Each layer/module has single purpose | Easier to change |
| Dependency Inversion | Depend on interfaces, not implementations | Flexibility |
| Single Responsibility | Each class/function does one thing | Easier to understand |
| Open/Closed | Open for extension, closed for modification | Safe evolution |
| Interface Segregation | Many small interfaces > one large interface | Loose coupling |

### Common Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Layer Skipping | API → Database | API → Service → Repository → Database |
| Circular Dependency | A → B → A | Extract shared code to C |
| God Class | 500-line class doing everything | Split into focused classes |
| Tight Coupling | Service creates dependencies | Use dependency injection |
| Mixed Concerns | Business logic in API | Move to service layer |

---

Related: [Security Checklist](security-checklist.md) | [Clarity Refactoring Rules](clarity-refactoring-rules.md) | [Code Quality Metrics](code-quality-metrics.md) | [Return to INDEX](INDEX.md)
