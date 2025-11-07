# React TanStack Testing Reference

Comprehensive reference materials for testing React applications with TanStack ecosystem.

## Reference Overview

### Testing Setup
**File**: [testing-setup.md](testing-setup.md)

Complete configuration for Vitest and test environment:
- Vitest configuration for React testing
- Test environment setup (jsdom, globals)
- React Testing Library configuration
- MSW (Mock Service Worker) setup
- Test file patterns and structure

**Use when**: Setting up a new project or configuring testing infrastructure.

---

### Testing Best Practices
**File**: [testing-best-practices.md](testing-best-practices.md)

Patterns and best practices for effective testing:
- Custom test utilities and render functions
- Provider wrappers (Query, Router, Auth)
- Mock data factories
- Test organization strategies
- Coverage requirements

**Use when**: Creating reusable test utilities or establishing testing standards.

---

### Server Components Testing
**File**: [server-components-testing.md](server-components-testing.md)

Testing React Server Components and async patterns:
- Async component testing
- Suspense boundaries
- Server actions
- Streaming rendering
- Error boundaries

**Use when**: Testing React 19 Server Components or async data fetching.

---

### Common Patterns
**File**: [common-patterns.md](common-patterns.md)

Frequently used testing patterns:
- Loading states and skeletons
- Error boundaries and fallbacks
- Infinite queries and scrolling
- Prefetching strategies
- Optimistic updates

**Use when**: Testing common UI patterns like loading states or error handling.

---

## Quick Reference

| Topic | Key Concepts |
|-------|-------------|
| **Setup** | Vitest config, jsdom, MSW, cleanup |
| **Best Practices** | Custom utils, providers, factories |
| **Server Components** | Async testing, Suspense, streaming |
| **Common Patterns** | Loading, errors, infinite, prefetch |

## Testing Tools Reference

### Vitest
- **Fast** - Native ESM, parallel tests
- **Compatible** - Jest-compatible API
- **Built-in** - Coverage, mocking, snapshots

### React Testing Library
- **User-centric** - Test what users see/do
- **Queries** - getBy, findBy, queryBy
- **Events** - userEvent for realistic interactions

### MSW (Mock Service Worker)
- **Realistic** - Intercepts actual network requests
- **Flexible** - Override handlers per test
- **Portable** - Works in Node and browser

---

Return to [main agent](../react-tanstack-tester.md)
