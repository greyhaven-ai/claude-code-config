# tests/unit/repositories/test_FEATURE_repository.py
import pytest
from uuid import uuid4
from app.db.repositories.YOUR_repository import YourRepository
from app.db.models.YOUR_model import YourModel


@pytest.mark.unit
class TestYourRepository:
    """Unit tests for YourRepository."""

    async def test_get_by_id_success(self, session, tenant_id):
        """Test retrieving entity by ID."""
        repo = YourRepository(session)

        # Create test entity
        entity = YourModel(
            tenant_id=tenant_id,
            name="Test Entity",
        )
        session.add(entity)
        await session.commit()
        await session.refresh(entity)

        # Retrieve entity
        result = await repo.get_by_id(entity.id, tenant_id)

        assert result is not None
        assert result.id == entity.id
        assert result.name == "Test Entity"

    async def test_get_by_id_enforces_tenant_isolation(
        self, session, tenant_id
    ):
        """Test that get_by_id enforces tenant isolation."""
        repo = YourRepository(session)

        # Create entity
        entity = YourModel(tenant_id=tenant_id, name="Test")
        session.add(entity)
        await session.commit()

        # Try to access with different tenant_id
        different_tenant = uuid4()
        result = await repo.get_by_id(entity.id, different_tenant)

        assert result is None

    async def test_list_with_pagination(self, session, tenant_id):
        """Test list with pagination."""
        repo = YourRepository(session)

        # Create multiple entities
        entities = [
            YourModel(tenant_id=tenant_id, name=f"Entity {i}")
            for i in range(10)
        ]
        session.add_all(entities)
        await session.commit()

        # Get first page
        page1 = await repo.list(tenant_id, limit=5, offset=0)
        assert len(page1) == 5

        # Get second page
        page2 = await repo.list(tenant_id, limit=5, offset=5)
        assert len(page2) == 5

        # Verify no overlap
        page1_ids = {e.id for e in page1}
        page2_ids = {e.id for e in page2}
        assert page1_ids.isdisjoint(page2_ids)

    async def test_create_success(self, session, tenant_id):
        """Test creating new entity."""
        repo = YourRepository(session)

        entity = await repo.create(
            tenant_id=tenant_id,
            name="New Entity",
        )

        assert entity.id is not None
        assert entity.tenant_id == tenant_id
        assert entity.name == "New Entity"

    async def test_update_success(self, session, tenant_id):
        """Test updating existing entity."""
        repo = YourRepository(session)

        # Create entity
        entity = YourModel(tenant_id=tenant_id, name="Original")
        session.add(entity)
        await session.commit()

        # Update entity
        updated = await repo.update(
            entity.id,
            tenant_id,
            name="Updated",
        )

        assert updated.name == "Updated"

    async def test_delete_success(self, session, tenant_id):
        """Test deleting entity."""
        repo = YourRepository(session)

        # Create entity
        entity = YourModel(tenant_id=tenant_id, name="To Delete")
        session.add(entity)
        await session.commit()

        # Delete entity
        await repo.delete(entity.id, tenant_id)

        # Verify deletion
        result = await repo.get_by_id(entity.id, tenant_id)
        assert result is None
