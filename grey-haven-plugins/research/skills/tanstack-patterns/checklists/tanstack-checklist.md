# TanStack Patterns Checklist

**Use before creating PR for TanStack Start/Router/Query code.**

## TanStack Router

- [ ] File structure follows conventions (`__root.tsx`, `_layout.tsx`, `$param.tsx`)
- [ ] Root route includes QueryClient provider
- [ ] Protected routes use `beforeLoad` for auth checks
- [ ] Loaders use `loader` for data fetching
- [ ] Route params are type-safe
- [ ] Navigation uses type-safe `Link` component
- [ ] Redirects include return URL in search params

## TanStack Query

- [ ] QueryClient configured with Grey Haven defaults (staleTime: 60000)
- [ ] Query keys follow pattern: specific to general (["user", userId])
- [ ] Query keys don't include function names
- [ ] staleTime set appropriately for data type
- [ ] Error states handled in components
- [ ] Loading states handled in components
- [ ] Mutations invalidate queries after success
- [ ] Optimistic updates use `onMutate` and rollback on error

## Server Functions

- [ ] All server functions include `tenant_id` parameter
- [ ] Server functions use correct HTTP method (GET/POST/DELETE)
- [ ] Multi-tenant isolation with `tenant_id` filtering
- [ ] Error handling with appropriate error messages
- [ ] Return types are type-safe
- [ ] Server functions used with TanStack Query hooks

## Multi-Tenant

- [ ] `tenant_id` included in all server functions
- [ ] `tenant_id` included in all query keys
- [ ] `useTenant()` hook used for consistent tenant access
- [ ] Queries use `enabled: !!tenantId` guard
- [ ] RLS policies applied when using RLS pattern
- [ ] Test cases verify tenant isolation

## Caching Strategy

- [ ] Auth data: 5 minutes staleTime
- [ ] User profiles: 1 minute staleTime
- [ ] Lists: 1 minute staleTime
- [ ] Static/config: 10 minutes staleTime
- [ ] Realtime: 0 staleTime (always refetch)
- [ ] Prefetching used for performance optimization

## Performance

- [ ] Prefetching on hover/navigation
- [ ] Parallel queries for independent data
- [ ] Dependent queries use `enabled` option
- [ ] Infinite queries for pagination
- [ ] Background refetching configured appropriately

## Code Quality

- [ ] Custom hooks created for reusable query logic
- [ ] Query logic separated from component logic
- [ ] Type-safe throughout (params, return types, mutations)
- [ ] DevTools enabled in development
- [ ] No console errors or warnings

## Testing

- [ ] Route loaders tested
- [ ] Server functions tested
- [ ] Query hooks tested
- [ ] Mutation logic tested
- [ ] Tenant isolation tested
- [ ] Error handling tested

## Documentation

- [ ] Complex query logic documented
- [ ] Custom hooks documented
- [ ] Server functions documented with JSDoc
- [ ] Route loaders documented
