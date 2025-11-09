# React TanStack Testing Examples

Complete testing examples for React applications using TanStack ecosystem libraries.

## Examples Overview

### TanStack Query Testing
**File**: [tanstack-query-testing.md](tanstack-query-testing.md)

Testing server state management with TanStack Query:
- Query hooks (loading, success, error states)
- Mutation hooks with optimistic updates
- Query invalidation and cache management
- Infinite queries and pagination
- Prefetching and cache warming

**Use when**: Testing components that fetch data, manage server state, or use caching.

---

### TanStack Router Testing
**File**: [tanstack-router-testing.md](tanstack-router-testing.md)

Testing routing and navigation with TanStack Router:
- Route navigation and programmatic routing
- Route parameters and search params
- Protected routes and authentication
- Route loaders and actions
- Nested routes and layouts

**Use when**: Testing navigation, route-based data fetching, or protected pages.

---

### TanStack Table Testing
**File**: [tanstack-table-testing.md](tanstack-table-testing.md)

Testing data tables with TanStack Table:
- Column rendering and data display
- Sorting (ascending, descending, none)
- Filtering (global and column-specific)
- Pagination and page size changes
- Row selection (single and multiple)

**Use when**: Testing data grids, tables with sorting/filtering, or complex data displays.

---

### TanStack Form Testing
**File**: [tanstack-form-testing.md](tanstack-form-testing.md)

Testing forms with TanStack Form:
- Field validation (required, email, min/max)
- Form submission with valid/invalid data
- Validation error display
- Field states (touched, dirty, pristine)
- Schema validation with Zod

**Use when**: Testing forms with validation, complex field interactions, or submission handling.

---

## Quick Reference

| Library | Primary Use Case | Key Test Patterns |
|---------|-----------------|-------------------|
| **Query** | Data fetching | Loading states, mutations, cache |
| **Router** | Navigation | Routes, params, loaders, protected |
| **Table** | Data display | Sorting, filtering, pagination |
| **Form** | User input | Validation, submission, errors |

## Testing Tools

All examples use:
- **Vitest** - Fast unit test runner
- **React Testing Library** - User-centric testing
- **MSW** - API mocking
- **@testing-library/user-event** - User interactions

## Best Practices

1. **Test user behavior** - Focus on what users see and do
2. **Mock API calls** - Use MSW for realistic network mocking
3. **Test all states** - Loading, success, error, empty
4. **Use proper queries** - Prefer `getByRole` over `getByTestId`
5. **Async utilities** - Use `waitFor`, `findBy` for async operations

---

Return to [main agent](../react-tanstack-tester.md)
