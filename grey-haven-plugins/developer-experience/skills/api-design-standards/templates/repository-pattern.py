# Grey Haven Studio - Repository Pattern Template
# Copy this template for new resource repositories

from sqlmodel import Session, select, func
from typing import Optional
from uuid import UUID

from app.models.resource import Resource  # TODO: Update import
from app.schemas.resource import ResourceCreate, ResourceUpdate  # TODO: Update import


# TODO: Update class name
class ResourceRepository:
    """Repository with automatic tenant filtering for Resource model."""

    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    async def list(
        self, filters: dict = None, skip: int = 0, limit: int = 100
    ) -> list[Resource]:
        """List resources (automatically filtered by tenant_id)."""
        statement = select(Resource).where(Resource.tenant_id == self.tenant_id)

        # Apply additional filters
        if filters:
            # TODO: Add your filter logic here
            # Example:
            # if "is_active" in filters:
            #     statement = statement.where(Resource.is_active == filters["is_active"])
            pass

        statement = statement.offset(skip).limit(limit).order_by(Resource.created_at.desc())

        result = await self.db.execute(statement)
        return result.scalars().all()

    async def count(self, filters: dict = None) -> int:
        """Count resources (tenant-isolated)."""
        statement = select(func.count(Resource.id)).where(
            Resource.tenant_id == self.tenant_id
        )

        # Apply same filters as list()
        if filters:
            # TODO: Add same filter logic as list()
            pass

        result = await self.db.execute(statement)
        return result.scalar_one()

    async def get_by_id(self, resource_id: str) -> Resource | None:
        """Get resource by ID (tenant-isolated)."""
        statement = select(Resource).where(
            Resource.id == resource_id,
            Resource.tenant_id == self.tenant_id,
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, resource_data: ResourceCreate) -> Resource:
        """Create a new resource in the current tenant."""
        resource = Resource(
            **resource_data.model_dump(),
            tenant_id=self.tenant_id,  # Automatic tenant assignment
        )
        self.db.add(resource)
        await self.db.commit()
        await self.db.refresh(resource)
        return resource

    async def update(
        self, resource_id: str, resource_data: ResourceUpdate
    ) -> Resource | None:
        """Update an existing resource (tenant-isolated)."""
        resource = await self.get_by_id(resource_id)
        if not resource:
            return None

        # Update only provided fields
        update_data = resource_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resource, field, value)

        await self.db.commit()
        await self.db.refresh(resource)
        return resource

    async def delete(self, resource_id: str) -> bool:
        """Soft-delete a resource (tenant-isolated)."""
        resource = await self.get_by_id(resource_id)
        if not resource:
            return False

        # Soft delete by setting deleted_at timestamp
        from datetime import datetime

        resource.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True
