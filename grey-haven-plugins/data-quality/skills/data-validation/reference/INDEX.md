# Data Validation Reference

Comprehensive reference documentation for Pydantic v2, SQLModel, and data quality patterns.

## Reference Materials

### Pydantic v2 Reference
**File**: [pydantic-v2-reference.md](pydantic-v2-reference.md)

Complete Pydantic v2 guide covering:
- Core concepts and migration from v1
- Field types and constraints (EmailStr, constr, conint, HttpUrl)
- Configuration with model_config
- Serialization modes (mode='json', mode='python')
- Error handling and custom error messages
- Performance optimization tips

**Use when**: Need comprehensive Pydantic v2 documentation or migrating from v1.

---

### Validators Reference
**File**: [validators-reference.md](validators-reference.md)

Complete guide to Pydantic validators:
- @field_validator for single-field validation
- @model_validator for cross-field validation
- Validator modes ('before', 'after', 'wrap')
- Accessing other field values with ValidationInfo
- Reusable validator functions
- Common validation patterns

**Use when**: Implementing custom validation logic beyond built-in constraints.

---

### SQLModel Alignment
**File**: [sqlmodel-alignment.md](sqlmodel-alignment.md)

Ensuring Pydantic schemas align with database models:
- Schema alignment validation patterns
- Type mapping (Pydantic ↔ SQLModel ↔ PostgreSQL)
- Multi-tenant patterns (tenant_id, RLS)
- Migration strategies
- Testing alignment
- Common misalignment issues

**Use when**: Building APIs with database persistence, ensuring data contracts match.

---

### Data Quality Monitoring
**File**: [data-quality-monitoring.md](data-quality-monitoring.md)

Monitoring data quality in production:
- Validation metrics tracking
- Error rate monitoring
- Data profiling patterns
- Alerting on validation failures
- Quality dashboards
- Integration with observability tools

**Use when**: Setting up production monitoring for data validation.

---

## Quick Reference

| Topic | Key Concepts | Common Use Cases |
|-------|-------------|------------------|
| **Pydantic v2** | Fields, validators, config | Request/response schemas |
| **Validators** | @field_validator, @model_validator | Custom business rules |
| **SQLModel Alignment** | Type mapping, migrations | Database persistence |
| **Data Quality** | Metrics, monitoring, alerts | Production reliability |

## Navigation

- **Examples**: [Examples Index](../examples/INDEX.md)
- **Templates**: [Templates Index](../templates/INDEX.md)
- **Main Agent**: [data-validator.md](../data-validator.md)

---

Return to [main agent](../data-validator.md)
