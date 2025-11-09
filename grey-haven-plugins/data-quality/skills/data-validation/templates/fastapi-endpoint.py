"""
FastAPI Endpoint Template

Copy this template to create new API endpoints with validation.
Replace {ModelName}, {endpoint_prefix}, and {table_name} with your actual values.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from pydantic import ValidationError
from typing import List
from uuid import UUID

# Import your models and schemas
from app.models.{model_name} import {ModelName}
from app.schemas.{model_name} import (
    {ModelName}CreateSchema,
    {ModelName}UpdateSchema,
    {ModelName}ResponseSchema
)
from app.database import get_session
from app.auth import get_current_user, get_current_tenant_id


# Create router
# -------------

router = APIRouter(
    prefix="/api/{endpoint_prefix}",
    tags=["{endpoint_prefix}"]
)


# Create Endpoint
# --------------

@router.post(
    "/",
    response_model={ModelName}ResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new {ModelName}",
    description="Create a new {ModelName} with validation"
)
async def create_{model_name}(
    data: {ModelName}CreateSchema,
    session: Session = Depends(get_session),
    user_id: UUID = Depends(get_current_user),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """
    Create new {ModelName}.
    
    Validates:
    - Request data against Pydantic schema
    - Business rules (if any)
    - Uniqueness constraints
    - Multi-tenant isolation
    
    Returns:
        {ModelName}ResponseSchema: Created {ModelName}
    
    Raises:
        HTTPException 409: If duplicate exists
        HTTPException 422: If validation fails
    """
    
    # Check for duplicates (if applicable)
    existing = session.exec(
        select({ModelName})
        .where({ModelName}.email == data.email)
        .where({ModelName}.tenant_id == tenant_id)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="{ ModelName} with this email already exists"
        )
    
    # Create instance
    instance = {ModelName}(
        **data.model_dump(),
        user_id=user_id,
        tenant_id=tenant_id
    )
    
    session.add(instance)
    session.commit()
    session.refresh(instance)
    
    return {ModelName}ResponseSchema.model_validate(instance)


# Read Endpoints
# -------------

@router.get(
    "/{id}",
    response_model={ModelName}ResponseSchema,
    summary="Get {ModelName} by ID"
)
async def get_{model_name}(
    id: UUID,
    session: Session = Depends(get_session),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """
    Get {ModelName} by ID with tenant isolation.
    
    Returns:
        {ModelName}ResponseSchema: Found {ModelName}
    
    Raises:
        HTTPException 404: If not found
    """
    
    instance = session.exec(
        select({ModelName})
        .where({ModelName}.id == id)
        .where({ModelName}.tenant_id == tenant_id)
    ).first()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found"
        )
    
    return {ModelName}ResponseSchema.model_validate(instance)


@router.get(
    "/",
    response_model=List[{ModelName}ResponseSchema],
    summary="List {ModelName}s"
)
async def list_{model_name}s(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    session: Session = Depends(get_session),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """
    List {ModelName}s with pagination and filtering.
    
    Args:
        skip: Number of records to skip (default 0)
        limit: Maximum records to return (default 100, max 1000)
        status: Filter by status (optional)
    
    Returns:
        List[{ModelName}ResponseSchema]: List of {ModelName}s
    """
    
    # Build query
    statement = (
        select({ModelName})
        .where({ModelName}.tenant_id == tenant_id)
        .offset(skip)
        .limit(min(limit, 1000))
    )
    
    # Apply filters
    if status:
        statement = statement.where({ModelName}.status == status)
    
    # Execute
    results = session.exec(statement).all()
    
    return [
        {ModelName}ResponseSchema.model_validate(item)
        for item in results
    ]


# Update Endpoint
# --------------

@router.patch(
    "/{id}",
    response_model={ModelName}ResponseSchema,
    summary="Update {ModelName}"
)
async def update_{model_name}(
    id: UUID,
    data: {ModelName}UpdateSchema,
    session: Session = Depends(get_session),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """
    Update {ModelName} with partial data.
    
    Only provided fields are updated.
    
    Returns:
        {ModelName}ResponseSchema: Updated {ModelName}
    
    Raises:
        HTTPException 404: If not found
        HTTPException 422: If validation fails
    """
    
    # Get existing
    instance = session.exec(
        select({ModelName})
        .where({ModelName}.id == id)
        .where({ModelName}.tenant_id == tenant_id)
    ).first()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found"
        )
    
    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    
    # Update timestamp
    instance.updated_at = datetime.utcnow()
    
    session.add(instance)
    session.commit()
    session.refresh(instance)
    
    return {ModelName}ResponseSchema.model_validate(instance)


# Delete Endpoint
# --------------

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete {ModelName}"
)
async def delete_{model_name}(
    id: UUID,
    session: Session = Depends(get_session),
    tenant_id: UUID = Depends(get_current_tenant_id)
):
    """
    Delete {ModelName}.
    
    Soft delete by setting is_active = False.
    For hard delete, use session.delete() instead.
    
    Raises:
        HTTPException 404: If not found
    """
    
    instance = session.exec(
        select({ModelName})
        .where({ModelName}.id == id)
        .where({ModelName}.tenant_id == tenant_id)
    ).first()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{ModelName} not found"
        )
    
    # Soft delete
    instance.is_active = False
    instance.updated_at = datetime.utcnow()
    
    session.add(instance)
    session.commit()
    
    # For hard delete:
    # session.delete(instance)
    # session.commit()


# Error Handling
# -------------

@router.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    errors = {}
    
    for error in exc.errors():
        field = '.'.join(str(loc) for loc in error['loc'])
        message = error['msg']
        
        if field not in errors:
            errors[field] = []
        errors[field].append(message)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'success': False,
            'error': 'validation_error',
            'message': 'Request validation failed',
            'errors': errors
        }
    )


# Register Router
# --------------

# In your main FastAPI app:
# from app.api.{endpoint_prefix} import router as {model_name}_router
# app.include_router({model_name}_router)
