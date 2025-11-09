# Testing Checklist

Use this checklist before submitting PRs to ensure comprehensive test coverage and quality.

## Pre-PR Testing Checklist

### Test Coverage

- [ ] All new functions/methods have unit tests
- [ ] All new components have component tests
- [ ] All new API endpoints have integration tests
- [ ] Critical user flows have E2E tests
- [ ] Code coverage is at least 80% (run `bun test --coverage` or `pytest --cov`)
- [ ] No coverage regression from previous version
- [ ] Security-critical code has 100% coverage (auth, payments, tenant isolation)

### Test Quality

- [ ] Tests follow naming convention: `test_should_do_something_when_condition`
- [ ] Each test has a single, clear assertion focus
- [ ] Tests are independent (can run in any order)
- [ ] Tests clean up after themselves (no database pollution)
- [ ] No hardcoded values (use constants or fixtures)
- [ ] Test data uses factories (faker/factory-boy)
- [ ] Mock external services (APIs, email, payments)
- [ ] Tests run in < 10 seconds (unit tests < 100ms each)

### Test Markers

- [ ] Unit tests marked with `@pytest.mark.unit` or in `tests/unit/`
- [ ] Integration tests marked with `@pytest.mark.integration` or in `tests/integration/`
- [ ] E2E tests marked with `@pytest.mark.e2e` or in `tests/e2e/`
- [ ] Slow tests marked with `@pytest.mark.slow` (> 5 seconds)

### Multi-Tenant Testing

- [ ] All database queries test tenant isolation
- [ ] Repository methods verify correct `tenant_id` filtering
- [ ] API endpoints test tenant header validation
- [ ] Cross-tenant access attempts are tested and fail correctly

### Environment Variables

- [ ] All tests use Doppler for environment variables
- [ ] No hardcoded secrets or API keys
- [ ] Test database is separate from development database
- [ ] `.env` files are NOT committed to repository
- [ ] CI uses `DOPPLER_TOKEN_TEST` secret

### Error Handling

- [ ] Tests verify error messages and status codes
- [ ] Edge cases are tested (null, empty, invalid input)
- [ ] Validation errors return correct HTTP status (422)
- [ ] Database errors are handled gracefully
- [ ] Tests verify rollback on transaction errors

### TypeScript Specific

- [ ] React Testing Library used for component tests
- [ ] TanStack Query components tested with QueryClientProvider wrapper
- [ ] Server function mocks use `vi.mock()`
- [ ] Async components use `waitFor()` for assertions
- [ ] Vitest globals enabled in config (`globals: true`)

### Python Specific

- [ ] Virtual environment activated before running tests
- [ ] Async fixtures used for async code (`async def`)
- [ ] FastAPI TestClient used for API tests
- [ ] Database fixtures use session-scoped engine
- [ ] SQLAlchemy sessions auto-rollback in fixtures

### CI/CD

- [ ] Tests pass locally with `bun test` or `doppler run -- pytest`
- [ ] Tests pass in CI (GitHub Actions)
- [ ] Coverage report uploaded to Codecov
- [ ] No test warnings or deprecation messages
- [ ] Pre-commit hooks pass (if configured)

## Test Types Checklist

### Unit Tests

- [ ] Test single function/class in isolation
- [ ] Mock all external dependencies
- [ ] No database or network calls
- [ ] Fast execution (< 100ms per test)
- [ ] Cover all code branches (if/else, try/catch)

### Integration Tests

- [ ] Test multiple components together
- [ ] Use real database (with cleanup)
- [ ] Test complete API request/response cycles
- [ ] Verify database state changes
- [ ] Test transaction handling

### E2E Tests

- [ ] Test complete user workflows
- [ ] Use Playwright for TypeScript
- [ ] Test from user perspective (UI interactions)
- [ ] Verify multi-step processes
- [ ] Test critical business flows

### Benchmark Tests

- [ ] Measure performance metrics
- [ ] Set performance thresholds
- [ ] Test with realistic data volumes
- [ ] Monitor for regressions

## Coverage Goals by Component

### Utility Functions

- [ ] 95%+ coverage
- [ ] All branches tested
- [ ] Edge cases handled

### Business Logic (Services)

- [ ] 90%+ coverage
- [ ] All business rules tested
- [ ] Error scenarios covered

### API Endpoints

- [ ] 85%+ coverage
- [ ] All HTTP methods tested
- [ ] All response codes verified

### Database Repositories

- [ ] 90%+ coverage
- [ ] CRUD operations tested
- [ ] Tenant isolation verified

### React Components

- [ ] 80%+ coverage
- [ ] Rendering tested
- [ ] User interactions tested
- [ ] Loading/error states tested

### Security Features

- [ ] 100% coverage
- [ ] Authentication tested
- [ ] Authorization tested
- [ ] Tenant isolation verified

## Common Testing Mistakes to Avoid

### Don't

- [ ] ❌ Test implementation details
- [ ] ❌ Test private methods directly
- [ ] ❌ Write tests that depend on execution order
- [ ] ❌ Use real external services in tests
- [ ] ❌ Hardcode test data
- [ ] ❌ Commit `.env` files
- [ ] ❌ Skip test cleanup
- [ ] ❌ Test multiple things in one test
- [ ] ❌ Forget to await async operations
- [ ] ❌ Mock too much (integration tests)

### Do

- [ ] ✅ Test public APIs and behaviors
- [ ] ✅ Write independent, isolated tests
- [ ] ✅ Mock external services
- [ ] ✅ Use test factories for data
- [ ] ✅ Use Doppler for environment variables
- [ ] ✅ Clean up test data
- [ ] ✅ Focus each test on one assertion
- [ ] ✅ Use `waitFor()` for async rendering
- [ ] ✅ Test error scenarios
- [ ] ✅ Verify tenant isolation

## Post-Testing Checklist

- [ ] All tests pass locally
- [ ] Coverage meets minimum threshold (80%)
- [ ] No failing tests in CI
- [ ] Coverage report reviewed
- [ ] Test output reviewed for warnings
- [ ] Performance acceptable (no slow tests)
- [ ] Documentation updated (if test patterns changed)
- [ ] Reviewers can understand test intent
