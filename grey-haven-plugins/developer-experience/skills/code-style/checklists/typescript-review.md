# TypeScript/React Code Review Checklist

Use this checklist when reviewing TypeScript/React code or creating pull requests for Grey Haven projects.

## Formatting & Style

- [ ] **Line width**: Code lines do not exceed 90 characters
- [ ] **Indentation**: Uses 2 spaces (not tabs or 4 spaces)
- [ ] **Semicolons**: All statements end with semicolons
- [ ] **Quotes**: Uses double quotes for strings (not single quotes)
- [ ] **Trailing commas**: Has trailing commas in objects, arrays, function parameters
- [ ] **Prettier formatted**: Code is formatted with Prettier (`npm run format`)
- [ ] **ESLint passing**: No ESLint errors (`npm run lint`)

## TypeScript

- [ ] **Type safety**: No `any` types used unnecessarily (but allowed when appropriate)
- [ ] **Type annotations**: Complex types have proper interfaces/types defined
- [ ] **Imports organized**: Imports are auto-sorted (external → internal → relative)
- [ ] **Path aliases**: Uses `~/` path alias for src imports (not `../..`)
- [ ] **tsconfig compliance**: Follows strict TypeScript configuration

## Database Schema (Drizzle)

- [ ] **snake_case fields**: ALL database column names use snake_case (CRITICAL!)
  - ✅ `created_at`, `tenant_id`, `email_address`
  - ❌ `createdAt`, `tenantId`, `emailAddress`
- [ ] **Multi-tenant**: Tables include `tenant_id` or `tenantId` field
- [ ] **Indexes**: Frequently queried fields have indexes
- [ ] **RLS policies**: Row Level Security policies defined for multi-tenant isolation
- [ ] **Foreign keys**: Relationships use proper foreign key constraints

## React Components

- [ ] **Component structure**: Follows Grey Haven component pattern:
  1. Imports (auto-sorted)
  2. Types/Interfaces
  3. Component definition
  4. State management (hooks first)
  5. Queries/Mutations
  6. Effects
  7. Event handlers
  8. Conditional renders
  9. Main render
- [ ] **Naming**: Components use PascalCase (`UserProfile.tsx`)
- [ ] **Props typed**: Component props have TypeScript interfaces
- [ ] **Hooks named**: Custom hooks start with `use-` prefix
- [ ] **Default export**: Route components export default

## TanStack Query

- [ ] **Query keys**: Uses descriptive, unique query keys
- [ ] **staleTime**: Sets appropriate staleTime (default: 60000ms / 1 minute)
- [ ] **Error handling**: Handles loading and error states
- [ ] **Mutations**: Uses useMutation for data updates
- [ ] **Invalidation**: Invalidates queries after mutations

## Environment Variables

- [ ] **Validation**: Environment variables validated with @t3-oss/env-core and Zod
- [ ] **VITE_ prefix**: Client variables prefixed with `VITE_`
- [ ] **Types**: All env variables have proper Zod schemas
- [ ] **Documentation**: Env variables have JSDoc comments

## Multi-Tenant Architecture

- [ ] **Tenant isolation**: All queries filter by `tenant_id` / `tenantId`
- [ ] **RLS enabled**: Row Level Security policies enforce tenant boundaries
- [ ] **Context usage**: Uses tenant context from auth provider
- [ ] **API calls**: Includes tenant ID in API requests

## Testing

- [ ] **Tests exist**: Components/functions have corresponding tests
- [ ] **Coverage**: Maintains or improves test coverage (aim for >80%)
- [ ] **Test structure**: Tests follow Arrange-Act-Assert pattern
- [ ] **Mocking**: External dependencies are properly mocked

## Security

- [ ] **Input validation**: User inputs are validated (Zod schemas)
- [ ] **XSS prevention**: No dangerouslySetInnerHTML without sanitization
- [ ] **API security**: API endpoints require authentication
- [ ] **Secrets**: No secrets or API keys in code (use env variables)

## Accessibility

- [ ] **Semantic HTML**: Uses appropriate HTML elements
- [ ] **ARIA labels**: Interactive elements have accessible labels
- [ ] **Keyboard nav**: Interactive elements are keyboard accessible
- [ ] **Color contrast**: Text has sufficient color contrast

## Performance

- [ ] **Code splitting**: Large components use lazy loading if appropriate
- [ ] **Memoization**: Expensive calculations use useMemo/useCallback
- [ ] **Query optimization**: Database queries are efficient (no N+1)
- [ ] **Bundle size**: No unnecessary dependencies added

## Documentation

- [ ] **JSDoc comments**: Complex functions have JSDoc comments
- [ ] **README updated**: README reflects any new features/changes
- [ ] **Type exports**: Exported types are documented
- [ ] **Examples**: Complex patterns have usage examples

## Pre-commit Checks

- [ ] **Build passes**: `npm run build` completes without errors
- [ ] **Linting passes**: `npm run lint` has no errors
- [ ] **Type checking**: `npx tsc --noEmit` has no errors
- [ ] **Tests passing**: `npm test` passes all tests
- [ ] **Pre-commit hooks**: Husky pre-commit hooks all pass
