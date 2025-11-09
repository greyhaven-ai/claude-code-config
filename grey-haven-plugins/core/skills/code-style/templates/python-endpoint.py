"""Example FastAPI Router Template.

Copy and adapt this for new Grey Haven API endpoints.
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

# Replace with your actual imports
from app.db.models.example import ExampleDB
from app.db.repositories.example_repository import ExampleRepository
from app.dependencies import get_current_user, get_example_repository
from app.schemas.example import ExampleCreate, ExampleResponse, ExampleUpdate

# 1. Create router with tags and dependencies
router = APIRouter(
    prefix="/examples",
    tags=["examples"],
    dependencies=[Depends(get_current_user)],  # Require authentication
)


# 2. POST endpoint - Create resource
@router.post("/", response_model=ExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_example(
    data: ExampleCreate,
    repo: Annotated[ExampleRepository, Depends(get_example_repository)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> ExampleResponse:
    """
    Create a new example resource.

    Args:
        data: Example creation data
        repo: Example repository dependency
        current_user: Currently authenticated user

    Returns:
        ExampleResponse: Created example

    Raises:
        HTTPException: If creation fails
    """
    # Create resource with tenant isolation
    example = await repo.create(data, tenant_id=current_user["tenant_id"])
    return ExampleResponse.model_validate(example)


# 3. GET endpoint - Retrieve single resource
@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(
    example_id: UUID,
    repo: Annotated[ExampleRepository, Depends(get_example_repository)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> ExampleResponse:
    """
    Get example by ID with tenant isolation.

    Args:
        example_id: Example UUID
        repo: Example repository dependency
        current_user: Currently authenticated user

    Returns:
        ExampleResponse: Example data

    Raises:
        HTTPException: If not found
    """
    # Get with tenant isolation
    example = await repo.get_by_id(example_id, tenant_id=current_user["tenant_id"])

    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Example not found"
        )

    return ExampleResponse.model_validate(example)


# 4. GET endpoint - List resources with pagination
@router.get("/", response_model=list[ExampleResponse])
async def list_examples(
    repo: Annotated[ExampleRepository, Depends(get_example_repository)],
    current_user: Annotated[dict, Depends(get_current_user)],
    limit: int = Query(100, ge=1, le=1000, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    is_active: bool | None = Query(None, description="Filter by active status"),
) -> list[ExampleResponse]:
    """
    List examples with pagination and filtering.

    Args:
        repo: Example repository dependency
        current_user: Currently authenticated user
        limit: Maximum number of items to return
        offset: Number of items to skip
        is_active: Optional filter by active status

    Returns:
        list[ExampleResponse]: List of examples
    """
    # List with tenant isolation
    examples = await repo.list_by_tenant(
        tenant_id=current_user["tenant_id"],
        limit=limit,
        offset=offset,
        is_active=is_active,
    )

    return [ExampleResponse.model_validate(e) for e in examples]


# 5. PATCH endpoint - Update resource
@router.patch("/{example_id}", response_model=ExampleResponse)
async def update_example(
    example_id: UUID,
    data: ExampleUpdate,
    repo: Annotated[ExampleRepository, Depends(get_example_repository)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> ExampleResponse:
    """
    Update example by ID with tenant isolation.

    Args:
        example_id: Example UUID
        data: Update data (partial fields)
        repo: Example repository dependency
        current_user: Currently authenticated user

    Returns:
        ExampleResponse: Updated example

    Raises:
        HTTPException: If not found
    """
    # Get existing example with tenant isolation
    example = await repo.get_by_id(example_id, tenant_id=current_user["tenant_id"])

    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Example not found"
        )

    # Update fields (exclude_unset to only update provided fields)
    update_dict = data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(example, field, value)

    # Save updates
    updated = await repo.update(example)
    return ExampleResponse.model_validate(updated)


# 6. DELETE endpoint - Delete resource
@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    example_id: UUID,
    repo: Annotated[ExampleRepository, Depends(get_example_repository)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> None:
    """
    Delete example by ID with tenant isolation.

    Args:
        example_id: Example UUID
        repo: Example repository dependency
        current_user: Currently authenticated user

    Raises:
        HTTPException: If not found
    """
    # Get existing example with tenant isolation
    example = await repo.get_by_id(example_id, tenant_id=current_user["tenant_id"])

    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Example not found"
        )

    # Delete
    await repo.delete(example_id, tenant_id=current_user["tenant_id"])
