#!/bin/bash
# Python API Scaffold Generator
# Generates a production-ready FastAPI + Pydantic v2 + PostgreSQL project

set -e

PROJECT_NAME="${1:-my-python-api}"
echo "🐍 Creating Python API scaffold: $PROJECT_NAME"

# Create directory structure
mkdir -p "$PROJECT_NAME"/{app/{api/{endpoints,deps},core,db,models,schemas,services,utils},tests/{unit,integration},alembic/versions,.github/workflows}

# Create pyproject.toml
cat > "$PROJECT_NAME/pyproject.toml" <<'EOF'
[project]
name = "my-python-api"
version = "0.1.0"
description = "FastAPI + Pydantic v2 + PostgreSQL API"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.25",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "A", "C4", "DTZ", "T10", "EM", "ISC", "ICN", "PIE", "PT", "RET", "SIM", "ARG", "PTH", "PD", "PGH", "PL", "TRY", "RUF"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
EOF

# Create main application
cat > "$PROJECT_NAME/app/main.py" <<'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import users, health
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
EOF

# Create config
cat > "$PROJECT_NAME/app/core/config.py" <<'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "My Python API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
EOF

# Create database session
cat > "$PROJECT_NAME/app/db/session.py" <<'EOF'
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
EOF

# Create User model
cat > "$PROJECT_NAME/app/models/user.py" <<'EOF'
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
EOF

# Create Pydantic schemas
cat > "$PROJECT_NAME/app/schemas/user.py" <<'EOF'
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=100)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
EOF

# Create health endpoint
cat > "$PROJECT_NAME/app/api/endpoints/health.py" <<'EOF'
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter()

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
EOF

# Create users endpoint
cat > "$PROJECT_NAME/app/api/endpoints/users.py" <<'EOF'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Hash password
    user = User(email=user_in.email, name=user_in.name, hashed_password="hashed")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
EOF

# Create test
cat > "$PROJECT_NAME/tests/unit/test_users.py" <<'EOF'
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "name": "Test User", "password": "SecurePass123!"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data
EOF

# Create .env.example
cat > "$PROJECT_NAME/.env.example" <<'EOF'
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:3000"]
EOF

# Create .gitignore
cat > "$PROJECT_NAME/.gitignore" <<'EOF'
__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
.pytest_cache/
.coverage
.mypy_cache/
.ruff_cache/
*.db
*.sqlite3
EOF

# Create README
cat > "$PROJECT_NAME/README.md" <<'EOF'
# My Python API

FastAPI + Pydantic v2 + PostgreSQL production-ready API.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"

# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
pytest --cov=app --cov-report=term-missing tests/
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

See deployment documentation for production setup.
EOF

# Create GitHub Actions workflow
cat > "$PROJECT_NAME/.github/workflows/test.yml" <<'EOF'
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy app
      - run: pytest --cov=app --cov-report=term-missing tests/
EOF

echo "✅ Python API scaffold created: $PROJECT_NAME"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  python -m venv venv && source venv/bin/activate"
echo "  pip install -e \".[dev]\""
echo "  cp .env.example .env  # Edit with your database credentials"
echo "  uvicorn app.main:app --reload"
