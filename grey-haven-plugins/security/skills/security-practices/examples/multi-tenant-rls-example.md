# Multi-Tenant Row-Level Security (RLS) Example

Real-world example implementing PostgreSQL RLS policies to enforce tenant isolation in a Grey Haven multi-tenant application.

## Scenario

A SaaS application with multiple tenants (organizations) must ensure complete data isolation. A critical bug allowed Tenant A to access Tenant B's data due to missing RLS policies.

## The Problem

### Vulnerable Architecture (BEFORE)

**Database Schema:** `schema.sql`

```sql
-- ❌ VULNERABLE: No RLS policies
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    owner_id UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ❌ PROBLEM: No RLS policies!
-- Any user with database access can query all data
```

**Backend API:** `app/api/v1/projects.py`

```python
# ❌ VULNERABLE CODE
from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models.project import Project
from app.api.deps import get_session, get_current_user

router = APIRouter()

@router.get("/projects")
async def list_projects(
    session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """List all projects - VULNERABLE VERSION"""

    # ❌ PROBLEM: No tenant filtering!
    # Returns ALL projects from ALL tenants
    stmt = select(Project)
    result = await session.execute(stmt)
    projects = result.scalars().all()

    return {"projects": projects}
```

**Attack Scenario:**

1. Attacker (Tenant A) logs in normally
2. Uses DevTools to intercept API request
3. Modifies request to query arbitrary project IDs
4. Receives data from Tenant B's projects!

```bash
# Attacker's request
GET /api/projects/uuid-from-tenant-b

# ❌ Response includes Tenant B data!
{
  "id": "uuid-from-tenant-b",
  "name": "Secret Project",
  "tenant_id": "tenant-b-uuid",
  "description": "Confidential data..."
}
```

## The Solution: PostgreSQL RLS

### Step 1: Enable RLS on All Tables

```sql
-- ✅ SECURITY: Enable RLS on all multi-tenant tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
-- ... enable on ALL tables with tenant_id
```

### Step 2: Create RLS Policies

```sql
-- ✅ SECURITY: Tenant isolation policy for users table
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- ✅ SECURITY: Tenant isolation policy for projects table
CREATE POLICY tenant_isolation ON projects
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- ✅ SECURITY: Tenant isolation policy for documents table
CREATE POLICY tenant_isolation ON documents
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- ✅ SECURITY: Tenant isolation policy for comments table
CREATE POLICY tenant_isolation ON comments
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

**How RLS Works:**
- `USING (condition)` - Applied to SELECT, UPDATE, DELETE
- `current_setting('app.tenant_id')` - Session variable set per request
- Only rows matching condition are visible/modifiable

### Step 3: Admin Bypass Policy (Optional)

For admin users who need cross-tenant access:

```sql
-- ✅ SECURITY: Admin bypass policy
CREATE POLICY admin_full_access ON projects
    USING (
        current_setting('app.user_role', true) = 'admin'
        OR tenant_id = current_setting('app.tenant_id')::uuid
    );

-- Note: Use WITH CHECK for INSERT/UPDATE policies
CREATE POLICY admin_full_access_insert ON projects
    FOR INSERT
    WITH CHECK (
        current_setting('app.user_role', true) = 'admin'
        OR tenant_id = current_setting('app.tenant_id')::uuid
    );
```

### Step 4: Set Tenant Context in Application

**Backend:** `app/api/deps.py`

```python
# ✅ SECURE: Set tenant context for each request
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_session
from app.models.user import User

async def set_tenant_context(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Set PostgreSQL session variables for RLS"""

    # ✅ SECURITY: Set tenant_id from authenticated user
    await session.execute(
        text("SET LOCAL app.tenant_id = :tenant_id"),
        {"tenant_id": str(current_user.tenant_id)}
    )

    # ✅ SECURITY: Set user role for admin bypass (if needed)
    await session.execute(
        text("SET LOCAL app.user_role = :role"),
        {"role": current_user.role}
    )

    return current_user
```

**Usage in API Endpoints:**

```python
# ✅ SECURE CODE
from fastapi import APIRouter, Depends
from sqlmodel import select
from app.models.project import Project
from app.api.deps import get_session, set_tenant_context

router = APIRouter()

@router.get("/projects")
async def list_projects(
    session = Depends(get_session),
    current_user = Depends(set_tenant_context)  # ✅ Sets tenant context
):
    """List projects - SECURE VERSION"""

    # ✅ SECURITY: RLS automatically filters by tenant_id
    # No manual WHERE clause needed!
    stmt = select(Project)
    result = await session.execute(stmt)
    projects = result.scalars().all()

    # Only returns projects from current_user.tenant_id
    return {"projects": projects}

@router.get("/projects/{project_id}")
async def get_project(
    project_id: str,
    session = Depends(get_session),
    current_user = Depends(set_tenant_context)  # ✅ Sets tenant context
):
    """Get single project - SECURE VERSION"""

    # ✅ SECURITY: RLS automatically filters
    # If project belongs to different tenant, returns None
    stmt = select(Project).where(Project.id == project_id)
    result = await session.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project
```

### Step 5: Database Migration

**Alembic migration:** `alembic/versions/xxx_enable_rls.py`

```python
"""Enable RLS on all multi-tenant tables"""

from alembic import op

def upgrade():
    # Enable RLS
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE projects ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE documents ENABLE ROW LEVEL SECURITY")

    # Create policies
    op.execute("""
        CREATE POLICY tenant_isolation ON users
        USING (tenant_id = current_setting('app.tenant_id')::uuid)
    """)

    op.execute("""
        CREATE POLICY tenant_isolation ON projects
        USING (tenant_id = current_setting('app.tenant_id')::uuid)
    """)

    op.execute("""
        CREATE POLICY tenant_isolation ON documents
        USING (tenant_id = current_setting('app.tenant_id')::uuid)
    """)

def downgrade():
    # Drop policies
    op.execute("DROP POLICY IF EXISTS tenant_isolation ON users")
    op.execute("DROP POLICY IF EXISTS tenant_isolation ON projects")
    op.execute("DROP POLICY IF EXISTS tenant_isolation ON documents")

    # Disable RLS
    op.execute("ALTER TABLE users DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE projects DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE documents DISABLE ROW LEVEL SECURITY")
```

## Testing RLS

### Unit Tests

```python
# tests/test_rls.py
import pytest
from sqlalchemy import text
from app.models.user import User
from app.models.project import Project

@pytest.mark.asyncio
async def test_rls_isolates_tenants(session):
    """Test that RLS prevents cross-tenant access"""

    # Create two tenants
    tenant_a_id = "uuid-tenant-a"
    tenant_b_id = "uuid-tenant-b"

    # Create projects for each tenant
    project_a = Project(name="Project A", tenant_id=tenant_a_id)
    project_b = Project(name="Project B", tenant_id=tenant_b_id)

    session.add_all([project_a, project_b])
    await session.commit()

    # ✅ TEST: Set context to Tenant A
    await session.execute(
        text("SET LOCAL app.tenant_id = :tenant_id"),
        {"tenant_id": tenant_a_id}
    )

    # Query all projects
    result = await session.execute(select(Project))
    projects = result.scalars().all()

    # ✅ ASSERTION: Should only see Tenant A's project
    assert len(projects) == 1
    assert projects[0].id == project_a.id
    assert projects[0].tenant_id == tenant_a_id

    # ✅ TEST: Attempt to query Tenant B's project directly
    result = await session.execute(
        select(Project).where(Project.id == project_b.id)
    )
    forbidden_project = result.scalar_one_or_none()

    # ✅ ASSERTION: Should be None (RLS blocks access)
    assert forbidden_project is None

@pytest.mark.asyncio
async def test_admin_bypass(session):
    """Test that admin role can access all tenants"""

    # Set context with admin role
    await session.execute(
        text("SET LOCAL app.tenant_id = :tenant_id"),
        {"tenant_id": "uuid-tenant-a"}
    )
    await session.execute(
        text("SET LOCAL app.user_role = 'admin'")
    )

    # Query all projects
    result = await session.execute(select(Project))
    projects = result.scalars().all()

    # ✅ ASSERTION: Admin sees ALL projects
    assert len(projects) == 2  # Sees both Tenant A and B
```

### Integration Tests

```python
# tests/test_api_rls.py
import pytest
from fastapi.testclient import TestClient

def test_api_tenant_isolation(client: TestClient, tenant_a_token: str, tenant_b_project_id: str):
    """Test that API enforces tenant isolation"""

    # Tenant A user tries to access Tenant B's project
    response = client.get(
        f"/api/projects/{tenant_b_project_id}",
        headers={"Authorization": f"Bearer {tenant_a_token}"}
    )

    # ✅ ASSERTION: Should return 404 (RLS hides the project)
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_api_own_tenant_access(client: TestClient, tenant_a_token: str, tenant_a_project_id: str):
    """Test that users can access their own tenant's data"""

    response = client.get(
        f"/api/projects/{tenant_a_project_id}",
        headers={"Authorization": f"Bearer {tenant_a_token}"}
    )

    # ✅ ASSERTION: Should succeed
    assert response.status_code == 200
    assert response.json()["id"] == tenant_a_project_id
```

## Advanced: Separate Policies for CRUD

For fine-grained control, create separate policies for each operation:

```sql
-- SELECT policy (read access)
CREATE POLICY tenant_select ON projects
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- INSERT policy (create access)
CREATE POLICY tenant_insert ON projects
    FOR INSERT
    WITH CHECK (
        tenant_id = current_setting('app.tenant_id')::uuid
        AND owner_id = current_setting('app.user_id')::uuid
    );

-- UPDATE policy (modify access)
CREATE POLICY tenant_update ON projects
    FOR UPDATE
    USING (
        tenant_id = current_setting('app.tenant_id')::uuid
        AND owner_id = current_setting('app.user_id')::uuid
    )
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

-- DELETE policy (delete access)
CREATE POLICY tenant_delete ON projects
    FOR DELETE
    USING (
        tenant_id = current_setting('app.tenant_id')::uuid
        AND owner_id = current_setting('app.user_id')::uuid
    );
```

## Monitoring & Auditing

### Log RLS Context

```python
import structlog

logger = structlog.get_logger()

async def set_tenant_context(current_user: User, session: AsyncSession):
    """Set tenant context with audit logging"""

    await session.execute(
        text("SET LOCAL app.tenant_id = :tenant_id"),
        {"tenant_id": str(current_user.tenant_id)}
    )

    # ✅ AUDIT: Log tenant context for security monitoring
    logger.info(
        "tenant_context_set",
        user_id=str(current_user.id),
        tenant_id=str(current_user.tenant_id),
        role=current_user.role
    )

    return current_user
```

### Verify RLS is Active

```python
# Startup check
@app.on_event("startup")
async def verify_rls():
    """Verify RLS is enabled on all tables"""

    async with AsyncSession(engine) as session:
        result = await session.execute(text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            AND tablename IN ('users', 'projects', 'documents')
            AND NOT EXISTS (
                SELECT 1 FROM pg_policy
                WHERE tablename = pg_tables.tablename
            )
        """))

        tables_without_rls = result.scalars().all()

        if tables_without_rls:
            raise RuntimeError(
                f"RLS not enabled on tables: {tables_without_rls}"
            )

    print("✅ RLS verified on all tables")
```

## Security Checklist

- [x] **RLS enabled** on all multi-tenant tables
- [x] **Policies created** for tenant isolation
- [x] **Tenant context** set on every request
- [x] **No manual WHERE clauses** for tenant_id (RLS handles it)
- [x] **Admin bypass** implemented securely (if needed)
- [x] **Tests verify** cross-tenant access is blocked
- [x] **Audit logging** for tenant context changes
- [x] **Startup checks** verify RLS is active
- [x] **Migration** to enable RLS on existing data

## Key Takeaways

1. **RLS is defense in depth** - Even if application code forgets tenant filtering, database enforces it
2. **Set context per request** - Not per session (sessions can be reused)
3. **Test isolation** - Write tests that verify cross-tenant access is blocked
4. **Don't trust application layer alone** - Bugs happen, RLS is the safety net
5. **Monitor RLS context** - Log when tenant context is set for audit trail

## Common Pitfalls

❌ **Don't:**
- Forget to set tenant context (query will return no rows)
- Use global tenant context (sessions can be reused)
- Skip RLS on "internal" tables (all multi-tenant tables need RLS)
- Assume application-level checks are sufficient
- Disable RLS in production (even temporarily)

✅ **Do:**
- Enable RLS on ALL multi-tenant tables
- Set tenant context at request start (dependency injection)
- Test cross-tenant isolation thoroughly
- Monitor RLS context in logs
- Use RLS + application-level checks (defense in depth)

## Related Resources

- [Authentication Security Checklist](../checklists/authentication-security-checklist.md)
- [PostgreSQL RLS Documentation](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Input Validation Example](./input-validation-example.md)

---

**Vulnerability**: Cross-tenant data access
**Solution**: PostgreSQL Row-Level Security (RLS)
**Impact**: Complete tenant isolation at database layer ✅
**Defense Layer**: Database-level (cannot be bypassed by application bugs)
