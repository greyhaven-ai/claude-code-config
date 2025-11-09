# Performance Optimization Checklist

**Use before production deployment.**

## Frontend Performance

- [ ] React components memoized with React.memo where appropriate
- [ ] Expensive calculations wrapped in useMemo
- [ ] Event handlers wrapped in useCallback
- [ ] TanStack Query staleTime configured (5 minutes default)
- [ [ ] Query prefetching implemented for navigation
- [ ] Code splitting for large components (lazy loading)
- [ ] Bundle size under 200KB (check with bun run analyze)
- [ ] Images optimized (WebP, lazy loading)
- [ ] Fonts preloaded or self-hosted

## Backend Performance

- [ ] N+1 query problems eliminated (use joins or selectinload)
- [ ] Database connection pooling configured
- [ ] Indexes created for frequently queried columns
- [ ] API response times under 200ms
- [ ] Pagination implemented for large datasets
- [ ] Async/await used throughout FastAPI

## Database Performance

- [ ] Indexes on foreign keys
- [ ] Indexes on tenant_id for multi-tenant isolation
- [ ] Query execution time under 50ms
- [ ] Connection pool size appropriate (20-50)
- [ ] No full table scans (check EXPLAIN)

## Cloudflare Workers

- [ ] Cache-Control headers set appropriately
- [ ] KV storage used for frequently accessed data
- [ ] Edge caching enabled where possible
- [ ] Response compression enabled

## Metrics Verification

- [ ] Lighthouse FCP < 1.8s
- [ ] Lighthouse LCP < 2.5s
- [ ] Lighthouse TTI < 3.8s
- [ ] Lighthouse CLS < 0.1
- [ ] API response time < 200ms
- [ ] Database query time < 50ms
- [ ] Bundle size < 200KB

## Monitoring

- [ ] Performance monitoring enabled
- [ ] Error tracking configured (Sentry)
- [ ] Database slow query logging enabled
- [ ] Cloudflare analytics configured
