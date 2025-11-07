# Test Generator Examples

Real-world examples of comprehensive test suite generation for frontend components, backend APIs, and test coverage improvement.

## Files in This Directory

### [react-component-testing.md](react-component-testing.md)
Complete example of generating test suite for React component with TanStack Query - from no tests to 100% coverage. Shows unit tests, integration tests, user interaction tests, and accessibility tests.

**Scenario**: Payment form component with validation, API calls, and error handling - initially untested
**Result**: 42 tests generated, 100% coverage, caught 3 bugs during testing
**Technologies**: React 19, Vitest, Testing Library, TanStack Query

### [api-endpoint-testing.md](api-endpoint-testing.md)
Backend API testing example showing test generation for FastAPI endpoints - authentication, validation, database operations, and error handling.

**Scenario**: User management API endpoints with CRUD operations - 35% test coverage
**Result**: Coverage improved from 35% → 94%, 67 tests generated, found 5 edge case bugs
**Technologies**: FastAPI, pytest, SQLModel, PostgreSQL

### [test-coverage-workflow.md](test-coverage-workflow.md)
Step-by-step workflow for analyzing low-coverage codebase and systematically generating tests to reach 80%+ coverage.

**Scenario**: Legacy codebase with 42% coverage needs improvement for production deployment
**Result**: Coverage 42% → 87% over 3 days, 156 tests generated, zero production bugs first month
**Technologies**: Multi-language (TypeScript + Python), Vitest + pytest

## Navigation

**Parent**: [Test Generator Agent](../test-generator.md)
**Reference**: [Reference Index](../reference/INDEX.md)
**Templates**: [Templates Index](../templates/INDEX.md)

---

Return to [agent documentation](../test-generator.md)
