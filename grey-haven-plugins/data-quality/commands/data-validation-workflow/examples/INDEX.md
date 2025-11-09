# Data Validation Workflow Examples

Complete examples demonstrating Pydantic v2 validation workflows.

## Available Examples

### [user-registration-example.md](user-registration-example.md)
Complete user registration validation workflow.
- Requirements analysis for user data
- TDD approach with failing tests
- Pydantic v2 model with field validators
- Model-level cross-field validation
- SQLModel database schema alignment
- API handler integration
- Error formatting for API responses
- OpenAPI spec generation

### [nested-validation-example.md](nested-validation-example.md)
Nested object validation patterns.
- Address validation within user schema
- List validation with min/max constraints
- Nested model validators
- Recursive validation for deeply nested objects
- Error handling for nested fields
- OpenAPI schema generation for nested types

### [conditional-validation-example.md](conditional-validation-example.md)
Conditional field validation based on other fields.
- Order schema with shipping requirements
- Payment schema with method-specific validation
- User schema with role-based constraints
- Model validators for conditional logic
- Error messages for conditional failures
- Testing strategies for conditional validation

## Quick Reference

**Need full workflow?** → [user-registration-example.md](user-registration-example.md)
**Need nested validation?** → [nested-validation-example.md](nested-validation-example.md)
**Need conditional logic?** → [conditional-validation-example.md](conditional-validation-example.md)
