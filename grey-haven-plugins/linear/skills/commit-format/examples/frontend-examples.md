# Frontend Commit Examples

Complete examples for TypeScript/TanStack Start commits.

## Simple Feature
```
feat(ui): add loading skeleton for user profile card
```

## Bug Fix with Context
```
fix(routes): prevent navigation flicker on auth check

Route loader was running auth check on every navigation causing
visible UI flicker. Moved auth check to layout's beforeLoad.

- Auth check in /_authenticated/_layout beforeLoad
- Prevents unnecessary auth calls on navigation
- Fixes flicker on protected routes

Fixes GREY-234
```

## TanStack Query Hook
```
feat(queries): add useUser custom hook for user profile

Create reusable custom hook wrapping TanStack Query for user profile
data fetching with automatic cache management.

- useUser hook with userId parameter
- Automatic stale time: 60 seconds
- Optimistic updates with onSuccess
- Type-safe return values

Related to GREY-456
```

## TanStack Start Server Function
```
feat(server): add createUser server function with validation

Create TanStack Start server function with Zod validation and
tenant isolation for user creation.

- POST server function with Zod schema
- Tenant ID from session context
- Returns User object or throws ValidationError
- Integration with UserRepository

Fixes GREY-567
```

## Drizzle Schema Change
```
feat(db): add users table with tenant isolation

Create users table following Grey Haven conventions with snake_case
fields and tenant_id for multi-tenant isolation.

- UUID primary key
- created_at, updated_at timestamps
- tenant_id with foreign key
- email_address unique constraint
- Index on tenant_id

Related to GREY-890
```

## Dependency Update
```
chore(deps): upgrade TanStack Query to v5.62.0

- Fixes type inference issues with useQuery
- Improves DevTools performance
- No breaking changes in our usage
```

## Refactoring
```
refactor(queries): extract query keys to constants

Move all TanStack Query keys to centralized queryKeys object for
consistency and type safety.

- queryKeys.ts with all key factories
- Type-safe key generation
- Easier cache invalidation
- Reduces typo errors
```
