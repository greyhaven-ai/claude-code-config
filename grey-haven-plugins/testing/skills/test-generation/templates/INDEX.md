# Test Generator Templates

Copy-paste templates for common testing scenarios - customize for your needs.

## Files in This Directory

### [unit-test-template.md](unit-test-template.md)
Ready-to-use unit test templates for TypeScript (Vitest) and Python (pytest) with AAA pattern, fixtures, and common test cases.

**When to use**: Creating new unit test files
**Languages**: TypeScript, Python

### [integration-test-template.md](integration-test-template.md)
Templates for integration tests covering API endpoints, database interactions, and multi-component workflows.

**When to use**: Testing interactions between components or services
**Languages**: TypeScript, Python

### [test-fixtures-template.md](test-fixtures-template.md)
Templates for test fixtures, factories, and test data builders with realistic examples.

**When to use**: Setting up test data and shared fixtures
**Languages**: TypeScript, Python

### [test-plan-template.md](test-plan-template.md)
Comprehensive test plan template for feature development with coverage goals, risk assessment, and test strategy.

**When to use**: Planning test coverage for new features or improvements
**Format**: Markdown checklist

## Usage

1. **Copy template** to your test directory
2. **Replace placeholders** (e.g., `ComponentName`, `YourService`)
3. **Customize** test cases for your specific needs
4. **Add tests** as you discover edge cases

## Template Conventions

**Placeholders**:
- `ComponentName` - Replace with your component name
- `functionName` - Replace with your function name
- `YourService` - Replace with your service class name
- `...` - Add more test cases

**Comments**:
- `// TODO:` - Action items to complete
- `// CUSTOMIZE:` - Areas to customize for your use case

---

Return to [agent documentation](../test-generator.md)
