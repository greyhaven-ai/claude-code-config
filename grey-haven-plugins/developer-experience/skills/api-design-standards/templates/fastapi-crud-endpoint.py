# Grey Haven Studio - FastAPI CRUD Endpoint Template
# Copy this template for new resource endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.repositories.resource_repository import ResourceRepository  # TODO: Update import
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate, PaginatedResponse  # TODO: Update import

# TODO: Update prefix, tags, and model name
router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.get("", response_model=PaginatedResponse[ResourceRead], status_code=status.HTTP_200_OK)
async def list_resources(
    skip: int = 0,
    limit: int = 100,
    # TODO: Add filter parameters as needed
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[ResourceRead]:
    """
    List all resources in the current tenant with pagination.

    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return (max 100)
    - **Returns**: Paginated list of resources
    """
    repository = ResourceRepository(db, tenant_id=current_user.tenant_id)

    # TODO: Build filter criteria if needed
    filters = {}

    resources = await repository.list(filters=filters, skip=skip, limit=limit)
    total = await repository.count(filters=filters)

    return PaginatedResponse(
        items=resources,
        total=total,
        skip=skip,
        limit=limit,
        has_more=(skip + limit) < total,
    )


@router.get("/{resource_id}", response_model=ResourceRead, status_code=status.HTTP_200_OK)
async def get_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourceRead:
    """Get a single resource by ID (tenant-isolated)."""
    repository = ResourceRepository(db, tenant_id=current_user.tenant_id)
    resource = await repository.get_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )
    return resource


@router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourceRead:
    """
    Create a new resource in the current tenant.

    **Errors**:
    - 409 Conflict: Duplicate resource
    - 422 Validation Error: Invalid data
    """
    repository = ResourceRepository(db, tenant_id=current_user.tenant_id)

    try:
        resource = await repository.create(resource_data)
        return resource
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource with this identifier already exists",
        )


@router.put("/{resource_id}", response_model=ResourceRead, status_code=status.HTTP_200_OK)
async def update_resource(
    resource_id: str,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResourceRead:
    """
    Update an existing resource (tenant-isolated).

    All fields are optional - only provided fields will be updated.
    """
    repository = ResourceRepository(db, tenant_id=current_user.tenant_id)
    resource = await repository.update(resource_id, resource_data)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )
    return resource


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Soft-delete a resource (tenant-isolated).

    Returns 204 No Content on success (no response body).
    """
    repository = ResourceRepository(db, tenant_id=current_user.tenant_id)
    success = await repository.delete(resource_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )
