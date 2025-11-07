# Synthesis Analysis Example

Cross-file analysis identifying architectural issues and inconsistent patterns across a multi-module codebase.

## Scenario

**Project**: User management system (5 modules, 18 files, 2,400 lines)
**Initial State**: Inconsistent patterns, hidden dependencies, architectural drift
**Goal**: Identify cross-file issues and enforce consistent architecture
**Time Investment**: 4 hours analysis + 5 hours fixes = 9 hours total

## Codebase Structure

```
user-management/
├── api/
│   ├── users.py          # User CRUD endpoints
│   ├── auth.py           # Authentication endpoints
│   └── teams.py          # Team management endpoints
├── services/
│   ├── user_service.py   # User business logic
│   ├── auth_service.py   # Auth business logic
│   └── team_service.py   # Team business logic
├── models/
│   ├── user.py           # User data models
│   ├── team.py           # Team data models
│   └── session.py        # Session models
├── database/
│   ├── users_repo.py     # User database access
│   ├── teams_repo.py     # Team database access
│   └── connection.py     # DB connection management
└── utils/
    ├── validators.py     # Input validation
    ├── formatters.py     # Data formatting
    └── errors.py         # Error definitions
```

## Cross-File Issues Detected

### Issue 1: Inconsistent Error Handling

**Pattern Inconsistency Across 18 Files**:

```python
# api/users.py - Pattern A: HTTPException
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# api/auth.py - Pattern B: Custom exception
from utils.errors import AuthenticationError

@app.post("/login")
def login(email: str, password: str):
    user = auth_service.authenticate(email, password)
    if not user:
        raise AuthenticationError("Invalid credentials")  # Different pattern!
    return generate_token(user)

# api/teams.py - Pattern C: Dict with error key
@app.get("/teams/{team_id}")
def get_team(team_id: str):
    team = team_service.get_team(team_id)
    if not team:
        return {"error": "Team not found"}  # Yet another pattern!
    return team
```

**Impact**: 3 different error handling patterns across API layer
**Affected Files**: 3/3 API files (100%)
**Severity**: 🟡 Medium

### Issue 2: Duplicate Validation Logic

**Code Duplication Across 6 Files**:

```python
# api/users.py
def create_user(email: str, name: str):
    # Duplicate validation #1
    if not email or "@" not in email:
        raise ValueError("Invalid email")

    if not name or len(name) < 2:
        raise ValueError("Name too short")

    # ...

# services/user_service.py
def register_user(email: str, name: str):
    # Duplicate validation #2 (exact same code!)
    if not email or "@" not in email:
        raise ValueError("Invalid email")

    if not name or len(name) < 2:
        raise ValueError("Name too short")

    # ...

# database/users_repo.py
def insert_user(email: str, name: str):
    # Duplicate validation #3 (again!)
    if not email or "@" not in email:
        raise ValueError("Invalid email")

    if not name or len(name) < 2:
        raise ValueError("Name too short")

    # ...
```

**Impact**: Email validation duplicated in 6 files
**Total Duplicated Lines**: 78 lines
**Severity**: 🟠 High

### Issue 3: Hidden Database Dependencies

**Direct Database Access from Wrong Layers**:

```python
# api/users.py - API layer directly accessing database! (violates architecture)
from database.connection import get_db

@app.get("/users")
def list_users():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()  # ❌ Skips service layer!
    return users

# services/user_service.py - Service layer also accessing database
from database.connection import get_db

def get_user(user_id: str):
    db = get_db()
    user = db.execute(f"SELECT * FROM users WHERE id = '{user_id}'").fetchone()
    return user

# ✅ Should be:
# API → Service → Repository → Database
# But actual: API → Database (skipping 2 layers!)
```

**Impact**: 8 endpoints bypass service/repository layers
**Architectural Violation**: 67% of endpoints
**Severity**: 🔴 Critical

### Issue 4: Inconsistent Naming Conventions

**Mixed Naming Styles Across Modules**:

```python
# api/users.py - Uses snake_case
def get_user_by_id(user_id: str):
    pass

def create_new_user(email: str):
    pass

# services/user_service.py - Uses camelCase!
def getUserById(userId: str):  # Different style!
    pass

def createNewUser(email: str):  # Inconsistent!
    pass

# database/users_repo.py - Uses abbreviated names
def get_usr(usr_id: str):  # Cryptic abbreviations
    pass

def crt_usr(eml: str):  # Unreadable
    pass
```

**Impact**: 3 naming conventions across architecture
**Consistency Score**: 34/100
**Severity**: 🟡 Medium

### Issue 5: Circular Dependencies

**Module Import Cycles**:

```python
# services/user_service.py
from services.team_service import get_user_teams  # Imports team service

def get_user_with_teams(user_id: str):
    user = get_user(user_id)
    teams = get_user_teams(user_id)  # Calls team service
    return {**user, "teams": teams}

# services/team_service.py
from services.user_service import get_team_members  # Imports user service! ⚠️

def get_team_with_members(team_id: str):
    team = get_team(team_id)
    members = get_team_members(team_id)  # Calls user service
    return {**team, "members": members}

# Result: user_service ↔ team_service (circular dependency!)
```

**Impact**: Circular imports between services
**Affected Modules**: 2/3 services (67%)
**Severity**: 🔴 Critical

### Issue 6: Inconsistent Response Formats

**API Responses Lack Consistency**:

```python
# api/users.py - Returns model directly
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return User(id="123", email="john@example.com")  # Direct model

# api/auth.py - Returns dict with snake_case
@app.post("/login")
def login(email: str, password: str):
    return {"access_token": "...", "token_type": "bearer"}  # Dict, snake_case

# api/teams.py - Returns dict with camelCase!
@app.get("/teams/{team_id}")
def get_team(team_id: str):
    return {"teamId": "...", "teamName": "..."}  # Dict, camelCase!
```

**Impact**: 3 response formats across API
**API Consistency**: 23/100
**Severity**: 🟠 High

## Synthesis Analysis: Root Causes

### Architectural Analysis

```
Layer Violations Detected:

Expected Architecture:
┌────────────┐
│  API Layer │  ← Controllers, routing, HTTP
├────────────┤
│  Service   │  ← Business logic
├────────────┤
│ Repository │  ← Data access
├────────────┤
│  Database  │  ← PostgreSQL
└────────────┘

Actual Implementation:
┌────────────┐
│  API Layer │ ─┐
├────────────┤  │
│  Service   │  │ 67% of endpoints
├────────────┤  │ bypass this layer
│ Repository │  │
├────────────┤  │
│  Database  │ ◄┘
└────────────┘

Violations:
- 8/12 API endpoints access database directly
- 5/12 API endpoints skip service layer
- 3/6 services access database directly (should use repositories)
```

### Pattern Consistency Score

```
Category                Current  Target  Gap
-------------------------------------------
Error Handling          33/100   90/100  -57
Validation              28/100   95/100  -67
Naming Conventions      34/100   85/100  -51
Response Formats        23/100   90/100  -67
Architectural Layers    25/100   95/100  -70
Dependency Management   42/100   85/100  -43
-------------------------------------------
OVERALL CONSISTENCY:    31/100   90/100  -59 ⛔️

Status: ❌ NEEDS IMMEDIATE REFACTORING
```

## After: Consistent Architecture

### Fixed: Unified Error Handling

```python
# utils/errors.py - Single source of truth
from fastapi import HTTPException, status

class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} '{identifier}' not found", 404)

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"Validation error on '{field}': {message}", 422)

# Global error handler
@app.exception_handler(AppError)
def handle_app_error(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

# ✅ Now all APIs use consistent errors
@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = user_service.get_user(user_id)
    if not user:
        raise NotFoundError("User", user_id)  # Consistent!
    return user

@app.get("/teams/{team_id}")
def get_team(team_id: str):
    team = team_service.get_team(team_id)
    if not team:
        raise NotFoundError("Team", team_id)  # Consistent!
    return team
```

### Fixed: Centralized Validation

```python
# utils/validators.py - Single validation source
from pydantic import BaseModel, EmailStr, validator

class UserCreateSchema(BaseModel):
    email: EmailStr  # Pydantic validates email format
    name: str

    @validator('name')
    def validate_name(cls, value):
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        return value

# ✅ Now validation happens once in schema
@app.post("/users")
def create_user(user_data: UserCreateSchema):  # Automatic validation!
    return user_service.create_user(user_data)

# services/user_service.py - No validation duplication
def create_user(user_data: UserCreateSchema):
    # Schema already validated, just business logic here
    return repository.insert_user(user_data)
```

### Fixed: Proper Layering

```python
# ✅ API Layer - Only handles HTTP
@app.get("/users/{user_id}")
def get_user(user_id: str, service: UserService = Depends()):
    return service.get_user(user_id)  # Delegates to service

# ✅ Service Layer - Business logic
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: str) -> User:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

# ✅ Repository Layer - Data access
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

# Architecture respected: API → Service → Repository → Database
```

### Fixed: Consistent Naming

```python
# Naming convention: snake_case everywhere (Python standard)

# api/users.py
def get_user_by_id(user_id: str):  # ✅ Consistent
    pass

def create_new_user(email: str):  # ✅ Consistent
    pass

# services/user_service.py
def get_user_by_id(user_id: str):  # ✅ Consistent
    pass

def create_new_user(email: str):  # ✅ Consistent
    pass

# database/users_repo.py
def get_user_by_id(user_id: str):  # ✅ Consistent (no abbreviations)
    pass

def create_new_user(email: str):  # ✅ Consistent (full words)
    pass
```

### Fixed: Circular Dependencies

```python
# Solution: Create shared models module

# models/aggregates.py - Shared aggregation logic
def get_user_with_teams(user_id: str, user_repo, team_repo):
    """Aggregate user with teams (no service dependencies)."""
    user = user_repo.find_by_id(user_id)
    teams = team_repo.find_by_user_id(user_id)
    return {**user.dict(), "teams": teams}

# services/user_service.py - No imports from team_service
from models.aggregates import get_user_with_teams

def get_user_with_teams(self, user_id: str):
    return get_user_with_teams(user_id, self.user_repo, self.team_repo)

# services/team_service.py - No imports from user_service
# No circular dependency!
```

### Fixed: Response Consistency

```python
# All responses use Pydantic models with consistent format

from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    """Consistent user response format."""
    id: str
    email: str
    name: str
    created_at: datetime

class TeamResponse(BaseModel):
    """Consistent team response format."""
    id: str
    name: str
    created_at: datetime

class TokenResponse(BaseModel):
    """Consistent auth response format."""
    access_token: str
    token_type: str
    expires_in: int

# ✅ All endpoints return typed responses
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str): ...

@app.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: str): ...

@app.post("/login", response_model=TokenResponse)
def login(email: str, password: str): ...
```

## Results

### Pattern Consistency: Before vs After

```
Category                Before   After    Change
------------------------------------------------
Error Handling          33/100   95/100   +62 ✅
Validation              28/100   98/100   +70 ✅
Naming Conventions      34/100   92/100   +58 ✅
Response Formats        23/100   95/100   +72 ✅
Architectural Layers    25/100   98/100   +73 ✅
Dependency Management   42/100   90/100   +48 ✅
------------------------------------------------
OVERALL CONSISTENCY:    31/100   95/100   +64 ✅

Status: ✅ PRODUCTION READY
```

### Issues Fixed

| Issue | Files Affected | Fix Applied | Lines Changed |
|-------|----------------|-------------|---------------|
| Inconsistent Errors | 18/18 | Unified error handling | 156 |
| Duplicate Validation | 6/18 | Pydantic schemas | -78 (removed duplication) |
| Hidden Dependencies | 8/12 endpoints | Enforced layers | 243 |
| Naming Inconsistency | 18/18 | snake_case standard | 312 |
| Circular Dependencies | 2/3 services | Shared models | 87 |
| Response Inconsistency | 12/12 endpoints | Pydantic responses | 198 |

**Total**: 18 cross-file issues fixed, 918 lines changed

### Architecture Quality

```
Metric                           Before    After
--------------------------------------------------
Layer Violations                 67%       0% ✅
Circular Dependencies            2         0 ✅
Duplicate Code (lines)           312       45
Naming Consistency               34%       92% ✅
Response Format Consistency      23%       95% ✅
Test Coverage (integration)      35%       88% ✅
```

## Key Lessons

### 1. Synthesis Analysis Reveals Hidden Issues

Single-file reviews miss:
- Architectural violations across layers
- Inconsistent patterns across modules
- Circular dependencies
- Code duplication

### 2. Consistency Beats Cleverness

3 different error handling patterns = confusion
1 consistent pattern = clarity

### 3. Architecture Erosion is Gradual

```
Project start:   Clean layers, 95% compliance
Month 1:         Still good, 87% compliance
Month 3:         Drift begins, 72% compliance
Month 6:         Violations common, 45% compliance
Month 12:        Architecture ignored, 25% compliance  ← We were here
```

**Prevention**: Regular synthesis analysis (monthly)

### 4. Violations Cascade

```
1 API endpoint bypasses service layer
  ↓
Others copy the pattern
  ↓
Services bypass repositories
  ↓
Architecture collapses
```

**Fix early** to prevent cascade.

### 5. Refactoring ROI

```
Investment: 9 hours refactoring
Savings:
- 78 lines duplicate code removed
- 67% faster onboarding (consistent patterns)
- 53% fewer bugs (proper layers catch errors)
- 2.3x easier maintenance (predictable structure)

ROI: Every hour spent = 4 hours saved in maintenance
```

---

Related: [Security Review Example](security-review-example.md) | [Clarity Refactoring Example](clarity-refactoring-example.md) | [Return to INDEX](INDEX.md)
