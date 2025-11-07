# Pagination Patterns

**Offset-based and cursor-based pagination examples.**

## Offset-Based Pagination

```python
class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool

@router.get("", response_model=PaginatedResponse[UserRead])
async def list_users(skip: int = 0, limit: int = 100):
    repository = UserRepository(db, tenant_id=current_user.tenant_id)
    users = await repository.list(skip=skip, limit=limit)
    total = await repository.count()
    return PaginatedResponse(items=users, total=total, skip=skip, limit=limit, has_more=(skip + limit) < total)
```

## Cursor-Based Pagination (Recommended)

```python
class CursorPaginatedResponse[T](BaseModel):
    items: list[T]
    next_cursor: Optional[str]
    has_more: bool

@router.get("")
async def list_users(cursor: Optional[str] = None, limit: int = 100):
    users = await repository.list_cursor(cursor=cursor, limit=limit)
    next_cursor = users[-1].id if len(users) == limit else None
    return CursorPaginatedResponse(items=users, next_cursor=next_cursor, has_more=next_cursor is not None)
```

**See also:** [fastapi-crud.md](fastapi-crud.md) for complete examples
