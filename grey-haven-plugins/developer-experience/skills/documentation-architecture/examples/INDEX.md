# Documentation Architecture Examples

Real-world examples of comprehensive documentation generation, architecture documentation, and coverage validation.

## Available Examples

### [OpenAPI 3.1 Generation from FastAPI](openapi-generation.md)

Complete workflow for automatic API documentation generation from FastAPI codebase.

**Scenario**: E-commerce API with 47 undocumented endpoints causing 12 integration issues/week

**Solution**: Enhanced OpenAPI generation, multi-language examples, interactive Swagger UI, CI/CD auto-generation

**Results**: Integration issues 12/week → 0.5/week (96% reduction), manual doc time 4hrs → 0 (automated)

**Key Techniques**: FastAPI OpenAPI customization, Pydantic v2 field validators, example generation scripts

---

### [System Architecture Documentation with Mermaid](architecture-docs.md)

Comprehensive system architecture documentation reducing onboarding time from 3-4 weeks to 4-5 days.

**Scenario**: No architecture docs, tribal knowledge spread across 8 developers, 3-4 week onboarding

**Solution**: 8 Mermaid diagrams, Architecture Decision Records, progressive disclosure, version-controlled

**Results**: Onboarding 3-4 weeks → 4-5 days (75% reduction), architecture questions 15hrs/week → 2hrs/week

**Key Techniques**: Mermaid diagrams (system, sequence, data flow, ER), ADR template, multi-tenant flow docs

---

### [Documentation Coverage Validation](coverage-validation.md)

Automated documentation coverage analysis with 80% threshold enforcement in CI/CD.

**Scenario**: Unknown coverage, 147 undocumented functions, no visibility into gaps

**Solution**: TypeScript coverage (ts-morph), Python coverage (AST), HTML reports, CI/CD enforcement

**Results**: TS 42% → 87%, Python 38% → 91%, API 51% → 95%, undocumented 147 → 18

**Key Techniques**: AST parsing, OpenAPI schema analysis, coverage threshold enforcement, HTML reports

---

## Common Patterns

1. **Automation First**: All documentation generated/validated automatically
2. **CI/CD Integration**: Updates on every commit, coverage checks block PRs
3. **Multi-Language Support**: Examples in TypeScript, Python, cURL
4. **Visual Documentation**: Mermaid diagrams for architecture, sequences, data models
5. **Progressive Disclosure**: Start with overview, drill into details

## Quick Reference

| Need | Example | Key Tool |
|------|---------|----------|
| API Documentation | [openapi-generation.md](openapi-generation.md) | FastAPI + Pydantic v2 |
| System Architecture | [architecture-docs.md](architecture-docs.md) | Mermaid + ADRs |
| Coverage Analysis | [coverage-validation.md](coverage-validation.md) | ts-morph + Python AST |

---

Related: [Reference Guides](../reference/INDEX.md) | [Templates](../templates/) | [Return to Agent](../docs-architect.md)
