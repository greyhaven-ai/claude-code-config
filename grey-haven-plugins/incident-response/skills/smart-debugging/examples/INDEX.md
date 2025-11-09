# Smart Debug Examples

Complete examples demonstrating systematic debugging workflows from error triage to verified fixes.

## Available Examples

### [null-pointer-debug-example.md](null-pointer-debug-example.md)
Complete walkthrough of debugging a NoneType AttributeError.
- Stack trace analysis and root file identification
- Error pattern matching (null pointer pattern)
- Code inspection of problematic function
- Fix generation with 3 options (return early, default value, exception)
- Test-driven debugging with failing test creation
- Fix application and verification
- Root cause analysis using 5 Whys
- Prevention strategy implementation

### [type-error-debug-example.md](type-error-debug-example.md)
Debugging type mismatch and operand type errors.
- TypeError analysis (unsupported operand types)
- Type inference from stack trace
- Pattern matching for type mismatches
- Type validation fix generation
- Unit test creation for type validation
- Static analysis recommendations (mypy, Pydantic)
- Prevention through type hints

### [integration-failure-debug.md](integration-failure-debug.md)
Debugging API integration failures and contract violations.
- HTTP error analysis (400, 422, 500 responses)
- API contract validation against OpenAPI spec
- Request/response comparison
- Schema validation with Pydantic
- Integration test creation
- Observability integration (trace ID correlation)
- Rollback and deployment strategies

### [performance-bug-debug.md](performance-bug-debug.md)
Debugging performance-related bugs and slow queries.
- Performance profiling with cProfile
- Database query analysis (N+1 detection)
- Caching strategy implementation
- Optimization verification with benchmarks
- Delegation to performance-optimizer agent
- Production monitoring setup

## Quick Reference

**Need null pointer help?** → [null-pointer-debug-example.md](null-pointer-debug-example.md)
**Need type error help?** → [type-error-debug-example.md](type-error-debug-example.md)
**Need API debugging?** → [integration-failure-debug.md](integration-failure-debug.md)
**Need performance debugging?** → [performance-bug-debug.md](performance-bug-debug.md)
