# FastAPI CRUD Endpoints

**Complete CRUD endpoint examples with repository pattern and tenant isolation.**

## Complete User CRUD

```python
# app/api/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate, PaginatedResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("", response_model=PaginatedResponse[UserRead], status_code=status.HTTP_200_OK)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    email_contains: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[UserRead]:
    """
    List all users in the current tenant with pagination and filtering.

    - **skip**: Number of records to skip (pagination offset)
    - **limit**: Maximum number of records to return (max 100)
    - **is_active**: Filter by active status (optional)
    - **email_contains**: Filter by email substring (optional)
    - **Returns**: Paginated list of users with public fields only
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)

    # Build filter criteria
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active
    if email_contains:
        filters["email_contains"] = email_contains

    users = await repository.list(filters=filters, skip=skip, limit=limit)
    total = await repository.count(filters=filters)

    return PaginatedResponse(
        items=users,
        total=total,
        skip=skip,
        limit=limit,
        has_more=(skip + limit) < total,
    )


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Get a single user by ID (tenant-isolated)."""
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Create a new user in the current tenant.

    - **email**: Valid email address (unique per tenant)
    - **full_name**: User's full name (1-255 characters)
    - **password**: At least 8 characters
    - **Returns**: Created user with ID, timestamps, and public fields

    **Errors**:
    - 409 Conflict: Email already exists in tenant
    - 422 Validation Error: Invalid email or weak password
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)

    try:
        user = await repository.create(user_data)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )


@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Update an existing user (tenant-isolated).

    All fields are optional - only provided fields will be updated.
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.update(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def partial_update_user(
    user_id: str,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """
    Partially update an existing user (tenant-isolated).

    Same as PUT but semantically indicates partial update.
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    user = await repository.update(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Soft-delete a user (tenant-isolated).

    Returns 204 No Content on success (no response body).
    """
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    success = await repository.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
```

## Repository Pattern with Tenant Isolation

```python
# app/repositories/user_repository.py
from sqlmodel import Session, select, func
from typing import Optional
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository with automatic tenant filtering."""

    def __init__(self, db: Session, tenant_id: str):
        self.db = db
        self.tenant_id = tenant_id

    async def list(
        self, filters: dict = None, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """List users (automatically filtered by tenant_id)."""
        statement = select(User).where(User.tenant_id == self.tenant_id)

        # Apply additional filters
        if filters:
            if "is_active" in filters:
                statement = statement.where(User.is_active == filters["is_active"])
            if "email_contains" in filters:
                statement = statement.where(User.email.contains(filters["email_contains"]))

        statement = statement.offset(skip).limit(limit).order_by(User.created_at.desc())

        result = await self.db.execute(statement)
        return result.scalars().all()

    async def count(self, filters: dict = None) -> int:
        """Count users (tenant-isolated)."""
        statement = select(func.count(User.id)).where(User.tenant_id == self.tenant_id)

        # Apply same filters as list()
        if filters:
            if "is_active" in filters:
                statement = statement.where(User.is_active == filters["is_active"])
            if "email_contains" in filters:
                statement = statement.where(User.email.contains(filters["email_contains"]))

        result = await self.db.execute(statement)
        return result.scalar_one()

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID (tenant-isolated)."""
        statement = select(User).where(
            User.id == user_id,
            User.tenant_id == self.tenant_id,
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user in the current tenant."""
        from app.utils.password import hash_password

        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            tenant_id=self.tenant_id,  # Automatic tenant assignment
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: str, user_data: UserUpdate) -> User | None:
        """Update an existing user (tenant-isolated)."""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: str) -> bool:
        """Soft-delete a user (tenant-isolated)."""
        user = await self.get_by_id(user_id)
        if not user:
            return False

        # Soft delete by setting deleted_at timestamp
        user.deleted_at = datetime.utcnow()
        await self.db.commit()
        return True
```

## Nested Resources

```python
# app/api/routes/organizations.py
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("/{org_id}/teams", response_model=list[TeamRead])
async def list_organization_teams(
    org_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TeamRead]:
    """List all teams in an organization (tenant-isolated)."""
    # Verify organization exists and belongs to tenant
    org_repo = OrganizationRepository(db, tenant_id=current_user.tenant_id)
    org = await org_repo.get_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {org_id} not found",
        )

    # Fetch teams for organization
    team_repo = TeamRepository(db, tenant_id=current_user.tenant_id)
    teams = await team_repo.list_by_organization(org_id, skip=skip, limit=limit)
    return teams


@router.post("/{org_id}/teams", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_organization_team(
    org_id: str,
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeamRead:
    """Create a new team in an organization."""
    # Verify organization exists
    org_repo = OrganizationRepository(db, tenant_id=current_user.tenant_id)
    org = await org_repo.get_by_id(org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with ID {org_id} not found",
        )

    # Create team
    team_repo = TeamRepository(db, tenant_id=current_user.tenant_id)
    team = await team_repo.create(team_data, organization_id=org_id)
    return team
```

**See also:**
- [pydantic-schemas.md](pydantic-schemas.md) - Request/response schema patterns
- [pagination.md](pagination.md) - Pagination and filtering examples
- [../templates/fastapi-crud-endpoint.py](../templates/fastapi-crud-endpoint.py) - CRUD template
