# TDD TypeScript Examples

Complete TDD examples for TypeScript/React applications using Vitest and React Testing Library.

## Available Examples

### [component-tdd-example.md](component-tdd-example.md)
Full TDD cycle for a React component.
- **Red Phase** - Write failing test for UserProfile component
- **Green Phase** - Implement minimum code to pass
- **Refactor Phase** - Improve code quality and structure
- **Cycles** - Multiple iterations of red-green-refactor
- **Result** - Fully tested, production-ready component

### [hook-tdd-example.md](hook-tdd-example.md)
TDD workflow for custom React hooks.
- **useCounter Hook** - State management hook with TDD
- **Testing Strategy** - renderHook from @testing-library/react
- **Edge Cases** - Boundary testing (min/max values)
- **Async Hooks** - Testing hooks with async operations
- **Dependencies** - Testing hooks with dependencies

### [utility-tdd-example.md](utility-tdd-example.md)
TDD for pure TypeScript utility functions.
- **Pure Functions** - Validation, formatting, calculations
- **Type Safety** - TypeScript types guide test cases
- **Edge Cases** - Null, undefined, empty, boundary values
- **Test Organization** - describe blocks for grouping
- **Fast Tests** - Unit tests with no dependencies

### [api-route-tdd-example.md](api-route-tdd-example.md)
TDD for TanStack Start API routes.
- **Server Functions** - Testing createServerFn
- **Request Validation** - Zod schema validation with TDD
- **Response Handling** - Success and error responses
- **Database Integration** - Testing with test database
- **Authentication** - Testing protected routes

## Quick Reference

**Need component testing?** → [component-tdd-example.md](component-tdd-example.md)
**Need hook testing?** → [hook-tdd-example.md](hook-tdd-example.md)
**Need utility function testing?** → [utility-tdd-example.md](utility-tdd-example.md)
**Need API route testing?** → [api-route-tdd-example.md](api-route-tdd-example.md)

## TDD Cycle Summary

```
1. RED: Write failing test
2. GREEN: Write minimum code to pass
3. REFACTOR: Improve code quality
4. REPEAT: Continue until feature complete
```
