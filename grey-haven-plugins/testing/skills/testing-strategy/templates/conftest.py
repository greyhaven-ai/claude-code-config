# tests/conftest.py
"""Shared test fixtures for all tests."""

import pytest
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from uuid import uuid4
from app.main import app
from app.db.models import Base

# Doppler provides DATABASE_URL_TEST at runtime
DATABASE_URL_TEST = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://localhost/test_db"
)


@pytest.fixture(scope="session")
async def engine():
    """Create test database engine."""
    engine = create_async_engine(DATABASE_URL_TEST, echo=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def session(engine):
    """Create test database session with automatic rollback."""
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    """Create test HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def tenant_id():
    """Provide test tenant ID."""
    return uuid4()


@pytest.fixture
async def test_user(session, tenant_id):
    """Create test user."""
    from app.db.models.user import User

    user = User(
        tenant_id=tenant_id,
        email_address="test@example.com",
        name="Test User",
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
async def authenticated_client(client, test_user, tenant_id):
    """Create authenticated HTTP client."""
    # Login and get token
    response = await client.post(
        "/api/auth/login",
        json={
            "email_address": test_user.email_address,
            "password": "testpassword",
        },
    )

    assert response.status_code == 200
    token = response.json()["access_token"]

    # Add auth header to client
    client.headers["Authorization"] = f"Bearer {token}"
    client.headers["X-Tenant-ID"] = str(tenant_id)

    return client
