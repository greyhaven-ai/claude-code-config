# Data Validation Reference

Reference documentation for Pydantic v2 validation and data quality tools.

## Available References

### [pydantic-v2-patterns.md](pydantic-v2-patterns.md)
Pydantic v2 best practices and patterns.
- Field definitions with Field()
- Constrained types (constr, conint, confloat)
- Field validators (@field_validator)
- Model validators (@model_validator)
- Configuration (model_config dict)
- Serialization (model_dump, model_dump_json)
- Deserialization (model_validate, model_validate_json)
- JSON schema generation
- ORM mode (from_attributes)

### [field-validators.md](field-validators.md)
Complete field validator reference.
- @field_validator decorator patterns
- Single-field validation rules
- Custom validation functions
- Validator chaining
- Error message customization
- Performance optimization
- Common validation patterns (email, phone, URL)

### [model-validators.md](model-validators.md)
Complete model validator reference.
- @model_validator decorator patterns
- Cross-field validation logic
- mode='before' vs mode='after'
- Complex business rules
- Conditional validation
- Error handling strategies
- Testing model validators

### [great-expectations.md](great-expectations.md)
Great Expectations setup and usage.
- Installation and configuration
- Creating expectation suites
- Data quality checks
- Validation results interpretation
- Integration with data pipelines
- Monitoring and alerting
- Batch validation patterns

## Quick Reference

**Need Pydantic patterns?** → [pydantic-v2-patterns.md](pydantic-v2-patterns.md)
**Need field validators?** → [field-validators.md](field-validators.md)
**Need model validators?** → [model-validators.md](model-validators.md)
**Need data quality tools?** → [great-expectations.md](great-expectations.md)
