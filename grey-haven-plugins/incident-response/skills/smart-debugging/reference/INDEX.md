# Smart Debug Reference

Debugging references and methodologies for systematic error resolution.

## Available References

### [error-patterns-database.md](error-patterns-database.md)
Complete error pattern catalog with fixes.
- **Null Pointer Errors** - NoneType, undefined, null reference
- **Type Errors** - Type mismatch, unsupported operand, conversion failures
- **Index Errors** - Array bounds, list access, slice errors
- **Key Errors** - Dictionary key missing, object property undefined
- **Import Errors** - Module not found, circular imports
- **Database Errors** - Connection refused, timeout, constraint violations
- **API Errors** - 400/422/500 responses, contract violations
- **Concurrency Errors** - Race conditions, deadlocks, async issues
- **Memory Errors** - Out of memory, memory leaks
- **Performance Errors** - Slow queries, N+1 problems, inefficient algorithms

### [stack-trace-patterns.md](stack-trace-patterns.md)
Stack trace reading and analysis guide.
- Python stack traces (Traceback format)
- JavaScript/TypeScript stack traces (Error.stack format)
- Java stack traces (Exception format)
- Identifying root file vs. propagation
- Filtering stdlib and third-party frames
- Understanding async stack traces
- Reading minified stack traces
- Source map integration

### [rca-methodology.md](rca-methodology.md)
Root cause analysis methodologies.
- **5 Whys** - Iterative questioning to root cause
- **Timeline Analysis** - Chronological event reconstruction
- **Fishbone Diagram** - Ishikawa cause categorization
- **Fault Tree Analysis** - Logic diagram of failure paths
- **Change Analysis** - Recent deployments and config changes
- **Comparative Analysis** - Working vs. broken environments
- **Reproducibility Testing** - Isolation of causal factors

### [fix-generation-patterns.md](fix-generation-patterns.md)
Code fix patterns for common errors.
- Null check patterns (guard clauses, optional chaining)
- Type validation patterns (isinstance, type hints)
- Error handling patterns (try-catch, error boundaries)
- Input validation patterns (Pydantic, zod)
- Defensive programming patterns
- Fail-fast vs. graceful degradation
- Error recovery strategies

## Quick Reference

**Need error patterns?** → [error-patterns-database.md](error-patterns-database.md)
**Need stack trace help?** → [stack-trace-patterns.md](stack-trace-patterns.md)
**Need RCA methods?** → [rca-methodology.md](rca-methodology.md)
**Need fix patterns?** → [fix-generation-patterns.md](fix-generation-patterns.md)
