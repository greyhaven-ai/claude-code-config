# Test Code Review Checklist

Use this checklist when reviewing test code in pull requests.

## General Test Quality

### Test Structure

- [ ] **Clear test names**: Descriptive, follows `test_should_do_something_when_condition` pattern
- [ ] **One assertion focus**: Each test verifies one specific behavior
- [ ] **Arrange-Act-Assert**: Tests follow AAA pattern clearly
- [ ] **No magic numbers**: Test values are self-explanatory or use named constants
- [ ] **Readable setup**: Test setup is clear and concise

### Test Independence

- [ ] **No shared state**: Tests don't depend on each other
- [ ] **Can run in any order**: Tests pass when run individually or in any sequence
- [ ] **Proper cleanup**: Tests clean up resources (database, files, mocks)
- [ ] **Isolated changes**: Tests don't pollute global state
- [ ] **Fresh fixtures**: Each test gets fresh test data

### Test Coverage

- [ ] **New code is tested**: All new functions/components have tests
- [ ] **Edge cases covered**: Null, empty, invalid inputs tested
- [ ] **Error paths tested**: Error handling and failure scenarios verified
- [ ] **Happy path tested**: Normal, expected behavior verified
- [ ] **Branch coverage**: All if/else and switch branches tested

## TypeScript/Vitest Review

### Component Tests

- [ ] **Correct rendering**: Components render without errors
- [ ] **User interactions**: Click, input, form submissions tested
- [ ] **Loading states**: Loading indicators tested
- [ ] **Error states**: Error messages and boundaries tested
- [ ] **Async handling**: Uses `waitFor()` for async state changes
- [ ] **Query wrapper**: TanStack Query components wrapped correctly
- [ ] **Accessibility**: Uses semantic queries (`getByRole`, `getByLabelText`)

### Mocking

- [ ] **Appropriate mocking**: Mocks external dependencies (APIs, modules)
- [ ] **Not over-mocked**: Integration tests use real implementations where appropriate
- [ ] **Clear mock setup**: Mock configuration is easy to understand
- [ ] **Mock verification**: Tests verify mocks were called correctly
- [ ] **Mock cleanup**: Mocks cleared after each test (`vi.clearAllMocks()`)

### Best Practices

- [ ] **Path aliases**: Uses `~/ ` for imports (not relative paths)
- [ ] **TypeScript types**: Test code is properly typed
- [ ] **Testing Library**: Uses `@testing-library/react` best practices
- [ ] **Vitest globals**: Uses globals (`describe`, `it`, `expect`) correctly
- [ ] **No console warnings**: Tests don't produce React warnings

## Python/pytest Review

### Unit Tests

- [ ] **Isolated tests**: No external dependencies (database, network)
- [ ] **Fast execution**: Unit tests complete in < 100ms
- [ ] **Proper fixtures**: Uses pytest fixtures appropriately
- [ ] **Mocking external services**: Uses `unittest.mock` or `pytest-mock`
- [ ] **Type hints**: Test functions have type hints

### Integration Tests

- [ ] **Real dependencies**: Uses real database/services where appropriate
- [ ] **Transaction handling**: Tests verify rollback on errors
- [ ] **Tenant isolation**: Tests verify multi-tenant data separation
- [ ] **Async/await**: Async tests use `async def` and `await`
- [ ] **Database cleanup**: Fixtures clean up test data

### Markers

- [ ] **Correct markers**: Tests marked with `@pytest.mark.unit`, `@pytest.mark.integration`, etc.
- [ ] **Consistent markers**: Markers match test type (unit, integration, e2e, benchmark)
- [ ] **Slow marker**: Tests >5 seconds marked with `@pytest.mark.slow`

### Best Practices

- [ ] **Descriptive docstrings**: Test functions have clear docstrings
- [ ] **Factory usage**: Uses factory pattern for test data
- [ ] **No hardcoded IDs**: Uses `uuid4()` for test IDs
- [ ] **Proper imports**: Imports organized and clear
- [ ] **No test pollution**: Tests don't leave data in database

## Multi-Tenant Testing

### Tenant Isolation

- [ ] **Tenant ID filtering**: All queries filter by `tenant_id`
- [ ] **Cross-tenant access denied**: Tests verify users can't access other tenant's data
- [ ] **Tenant header required**: API tests include `X-Tenant-ID` header
- [ ] **Repository methods**: All repository methods accept `tenant_id` parameter
- [ ] **Query verification**: Tests verify correct `tenant_id` in database queries

### Security

- [ ] **Authentication tested**: Protected endpoints require auth
- [ ] **Authorization tested**: Users can only access authorized resources
- [ ] **Input validation**: Invalid input properly rejected
- [ ] **SQL injection protected**: No raw SQL in tests (uses ORM)
- [ ] **XSS protection**: Input sanitization tested where applicable

## Environment & Configuration

### Doppler

- [ ] **Doppler used**: Tests run with `doppler run --`
- [ ] **No hardcoded secrets**: No API keys or secrets in test code
- [ ] **Correct config**: Tests use `test` Doppler config
- [ ] **Environment isolation**: Test database separate from dev

### Test Data

- [ ] **Faker/factory-boy**: Random test data uses faker
- [ ] **Realistic data**: Test data resembles production data
- [ ] **No PII**: Test data doesn't contain real personal information
- [ ] **Deterministic when needed**: Uses seed for reproducible random data when necessary

## Performance

### Test Speed

- [ ] **Fast unit tests**: Unit tests < 100ms each
- [ ] **Reasonable integration tests**: Integration tests < 1 second each
- [ ] **Parallel execution**: Tests can run in parallel
- [ ] **No unnecessary waits**: No `sleep()` or arbitrary delays
- [ ] **Optimized queries**: Database queries efficient

### Resource Usage

- [ ] **Minimal test data**: Creates only necessary test data
- [ ] **Connection cleanup**: Database connections closed properly
- [ ] **Memory efficient**: No memory leaks in test setup
- [ ] **File cleanup**: Temporary files deleted after tests

## CI/CD Compatibility

### GitHub Actions

- [ ] **Passes in CI**: Tests pass in GitHub Actions
- [ ] **No flaky tests**: Tests pass consistently (not intermittent failures)
- [ ] **Correct services**: Required services (postgres, redis) configured
- [ ] **Coverage upload**: Coverage reports uploaded correctly
- [ ] **Timeout appropriate**: Tests complete within CI timeout limits

### Coverage

- [ ] **Meets threshold**: Coverage meets 80% minimum
- [ ] **No false positives**: Coverage accurately reflects tested code
- [ ] **Coverage trends**: Coverage doesn't decrease from baseline
- [ ] **Critical paths covered**: Important features have high coverage

## Documentation

### Test Documentation

- [ ] **Clear test names**: Test intent obvious from name
- [ ] **Helpful comments**: Complex test logic explained
- [ ] **Fixture documentation**: Custom fixtures documented
- [ ] **Test file organization**: Tests organized logically
- [ ] **README updated**: Testing docs updated if patterns changed

### Code Comments

- [ ] **Why, not what**: Comments explain why, not what code does
- [ ] **No commented-out code**: Old test code removed
- [ ] **TODO comments tracked**: Any TODOs have tracking tickets
- [ ] **No misleading comments**: Comments accurate and up-to-date

## Red Flags to Watch For

### Anti-Patterns

- [ ] ❌ Tests that only test mocks
- [ ] ❌ Tests with no assertions
- [ ] ❌ Tests that test private implementation
- [ ] ❌ Brittle tests that break on refactoring
- [ ] ❌ Tests that depend on execution order
- [ ] ❌ Excessive setup code (>50% of test)
- [ ] ❌ Tests with sleep/wait instead of proper async handling
- [ ] ❌ Tests that write to production database
- [ ] ❌ Tests that make real API calls
- [ ] ❌ Tests with hardcoded production credentials

### Smells

- [ ] ⚠️ Very long test functions (>50 lines)
- [ ] ⚠️ Duplicate test code (could use fixtures)
- [ ] ⚠️ Tests with multiple assertions on different behaviors
- [ ] ⚠️ Tests that take >5 seconds
- [ ] ⚠️ Tests that fail intermittently
- [ ] ⚠️ Tests with complex logic (loops, conditionals)
- [ ] ⚠️ Tests that require manual setup to run
- [ ] ⚠️ Missing error assertions
- [ ] ⚠️ Testing framework workarounds/hacks

## Approval Criteria

Before approving PR with tests:

- [ ] All tests pass locally and in CI
- [ ] Coverage meets minimum threshold (80%)
- [ ] Tests follow Grey Haven conventions
- [ ] No anti-patterns or red flags
- [ ] Test code is readable and maintainable
- [ ] Tests verify correct behavior (not just implementation)
- [ ] Security and tenant isolation tested
- [ ] Documentation updated if needed
