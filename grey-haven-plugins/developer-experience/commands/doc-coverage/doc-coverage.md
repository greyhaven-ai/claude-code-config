---
name: doc-coverage
description: Validate documentation coverage across codebase, identify gaps, and generate comprehensive coverage reports with actionable recommendations
---

# Documentation Coverage Validator

Analyze documentation completeness across your codebase and generate actionable coverage reports.

## What This Command Does

Scans your entire codebase to:
- **Calculate Coverage Percentages** - Function, class, API endpoint, and type documentation
- **Identify Missing Documentation** - Specific locations of undocumented code
- **Generate Gap Reports** - Prioritized list of documentation improvements
- **Track Coverage Trends** - Historical coverage data and trending
- **Enforce Coverage Thresholds** - CI/CD integration for quality gates
- **Provide Fix Suggestions** - Auto-fixable documentation gaps

## When to Use

- Before code reviews - Ensure new code is documented
- Pre-release validation - Verify documentation quality
- During refactoring - Update docs alongside code
- CI/CD pipeline checks - Automated coverage enforcement
- Quarterly documentation audits - Identify documentation debt
- Onboarding preparation - Ensure adequate documentation

## Quick Start

```bash
# Basic coverage check
/doc-coverage

# CI/CD enforcement (fail if < 80%)
/doc-coverage --threshold 80 --fail-below true

# API-only coverage
/doc-coverage --scope api --format html

# With historical trends
/doc-coverage --trend true
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--threshold` | Minimum coverage percentage (0-100) | `80` |
| `--fail-below` | Exit with error if below threshold | `false` |
| `--format` | Output: `markdown`, `json`, `html`, `console` | `markdown` |
| `--output` | Output file path | `docs/coverage-report.md` |
| `--scope` | Scope: `all`, `api`, `functions`, `types` | `all` |
| `--ignore` | Patterns to ignore (glob) | `[]` |
| `--trend` | Include historical trend analysis | `false` |
| `--fix-suggestions` | Generate auto-fix suggestions | `true` |

## Coverage Metrics

The command calculates coverage across 5 categories:

### 1. Function/Method Coverage
**Formula**: `(Documented Functions / Total Functions) × 100`

Checks for JSDoc (TypeScript) or docstrings (Python) with required tags:
- `@param` for each parameter
- `@returns` for return value
- `@throws` for exceptions

### 2. Class/Interface Coverage
Checks for class-level documentation describing:
- Purpose and responsibilities
- Attributes/properties
- Usage examples

### 3. API Endpoint Coverage
Requires documentation for:
- Endpoint path and method
- Request parameters (path, query, body)
- Response schema
- Error responses (4xx, 5xx)
- Authentication requirements
- Code example (at least one language)

### 4. Type Documentation Coverage
Checks for:
- Interface/type-level description
- Field-level comments for each property
- Enum value descriptions

### 5. Example Coverage
Requires at least one working code example per public function/endpoint demonstrating realistic usage.

**See [examples/coverage-metrics-examples.md](examples/coverage-metrics-examples.md)** for detailed examples of documented vs. undocumented code.

## Coverage Report Format

The command generates reports in 4 formats:

### Console Output
Formatted table with coverage percentages, visual indicators (✅ ⚠️ ❌), and module breakdown.

### Markdown Report
Comprehensive report with summary table, gaps by module, critical gaps list, recommendations, and historical trends.

### JSON Report
Machine-readable format with all metrics, gaps, and auto-fix suggestions. Perfect for CI/CD integration.

### HTML Report
Interactive report with charts, filtering, and drill-down capabilities (requires `--format html`).

**See [reference/report-formats.md](reference/report-formats.md)** for complete report format specifications and examples.

## CI/CD Integration

Integrate documentation coverage into your development workflow:

### GitHub Actions
Add coverage checks to pull requests with automatic PR comments showing coverage metrics.

### Pre-Commit Hook
Prevent commits with documentation coverage below threshold.

### GitLab CI, CircleCI, etc.
Similar integration patterns available for all major CI/CD platforms.

**See [reference/ci-cd-patterns.md](reference/ci-cd-patterns.md)** for complete workflows and configuration examples.

## Coverage Tracking

Store historical data in `.claude/coverage-history.json` to track trends over time. The command automatically:
- Records coverage percentage for each run
- Calculates trend (improving/declining)
- Shows historical comparison
- Identifies coverage regressions

**Format**: JSON with timestamps, commit hashes, and coverage breakdowns by category.

## Auto-Fix Examples

The command can generate documentation for:
- **Functions**: JSDoc/docstrings with inferred parameter types and descriptions
- **Types**: Interface descriptions and field-level comments
- **Classes**: Class-level docstrings with attributes and examples
- **API Endpoints**: OpenAPI-compliant documentation

**See [examples/auto-fix-examples.md](examples/auto-fix-examples.md)** for before/after examples of generated documentation.

## Best Practices

1. **Set Realistic Thresholds**
   - Start with current coverage as baseline
   - Increase gradually (+5% per quarter)
   - Different thresholds per category

2. **Focus on Public APIs First**
   - 100% coverage for public API endpoints
   - 90% coverage for public functions
   - Lower priority for internal utilities

3. **Quality Over Quantity**
   - Verify documentation accuracy
   - Ensure examples are tested
   - Keep descriptions concise but complete

4. **Automate Where Possible**
   - Use auto-fix for simple cases
   - Generate from types and schemas
   - Validate in CI/CD pipeline

5. **Regular Audits**
   - Quarterly documentation reviews
   - Update outdated examples
   - Improve based on feedback

## Troubleshooting

**Issue: Coverage lower than expected**
- JSDoc/docstrings not in standard format
- Comments instead of proper documentation
- Check with: `/doc-coverage --format json`

**Issue: False positives**
- Configure documentation patterns in `.claude/doc-coverage-config.json`

**Issue: Inconsistent calculation**
- Use `--strict true` (requires all tags)
- Or `--strict false` (lenient mode)

## Agent Coordination

Works with:
- **docs-architect** - Reviews coverage and generates missing docs
- **code-quality-analyzer** - Includes documentation in quality metrics
- **tdd-orchestrator** - Ensures tests document behavior
- **onboarding-coordinator** - Uses coverage data to prioritize docs

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete coverage examples
  - [coverage-metrics-examples.md](examples/coverage-metrics-examples.md) - Documented vs. undocumented code examples
  - [typescript-coverage-example.md](examples/typescript-coverage-example.md) - TypeScript project analysis
  - [python-coverage-example.md](examples/python-coverage-example.md) - Python project analysis
  - [api-coverage-example.md](examples/api-coverage-example.md) - REST API documentation coverage
  - [auto-fix-examples.md](examples/auto-fix-examples.md) - Before/after auto-fix examples
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Coverage standards
  - [coverage-metrics.md](reference/coverage-metrics.md) - Detailed metric calculations
  - [report-formats.md](reference/report-formats.md) - Output format specifications
  - [ci-cd-patterns.md](reference/ci-cd-patterns.md) - CI/CD integration patterns
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [github-actions-template.yaml](templates/github-actions-template.yaml) - GitHub Actions workflow
  - [pre-commit-hook.sh](templates/pre-commit-hook.sh) - Git pre-commit hook

- **[checklists/](checklists/)** - Documentation checklists
  - [coverage-improvement-checklist.md](checklists/coverage-improvement-checklist.md) - Improvement workflow

---

**Pro Tip**: Run `/doc-coverage --trend true` monthly to track documentation health over time. Set a coverage threshold in CI/CD to prevent documentation debt from accumulating.
