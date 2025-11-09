# Performance Optimization Examples

Complete examples for optimizing Grey Haven applications.

## Available Examples

### [react-optimization.md](react-optimization.md)
React rendering optimization patterns.
- useMemo for expensive calculations
- React.memo for component memoization
- useCallback for stable function references

### [tanstack-query-optimization.md](tanstack-query-optimization.md)
TanStack Query caching and prefetching.
- staleTime configuration
- Query prefetching patterns
- Cache invalidation strategies

### [database-optimization.md](database-optimization.md)
Database query optimization.
- N+1 query prevention
- Connection pooling setup
- Index optimization

### [cloudflare-optimization.md](cloudflare-optimization.md)
Cloudflare Workers edge caching.
- Cache-Control headers
- KV storage patterns
- R2 object caching

### [bundle-optimization.md](bundle-optimization.md)
Bundle size and code splitting.
- Lazy loading components
- Tree shaking imports
- Dynamic imports

## Quick Reference

**Slow rendering?** → [react-optimization.md](react-optimization.md)
**Slow data fetching?** → [tanstack-query-optimization.md](tanstack-query-optimization.md)
**Slow database?** → [database-optimization.md](database-optimization.md)
**Slow edge?** → [cloudflare-optimization.md](cloudflare-optimization.md)
**Large bundle?** → [bundle-optimization.md](bundle-optimization.md)
