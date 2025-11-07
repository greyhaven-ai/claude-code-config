# Data Validation Templates

Copy-paste templates for common data validation patterns.

## Available Templates

### Pydantic Model Template
**File**: [pydantic-model.py](pydantic-model.py)

Complete Pydantic v2 model template with:
- Field definitions with constraints
- Custom validators (@field_validator, @model_validator)
- model_config configuration
- Nested models
- Documentation

**Use when**: Starting a new API request/response schema.

---

### SQLModel Template
**File**: [sqlmodel-model.py](sqlmodel-model.py)

Complete SQLModel database template with:
- Table configuration
- Field definitions with PostgreSQL types
- Multi-tenant pattern (tenant_id)
- Timestamps (created_at, updated_at)
- Indexes and constraints
- Relationships

**Use when**: Creating a new database table.

---

### FastAPI Endpoint Template
**File**: [fastapi-endpoint.py](fastapi-endpoint.py)

Complete FastAPI endpoint template with:
- Router configuration
- Pydantic request/response schemas
- Dependency injection (session, tenant_id, user_id)
- Validation error handling
- Database operations
- Multi-tenant isolation

**Use when**: Creating a new API endpoint with validation.

---

## Quick Start

1. **Copy template** to your project
2. **Rename** model/endpoint appropriately
3. **Customize** fields and validators
4. **Test** with comprehensive test cases

## Navigation

- **Examples**: [Examples Index](../examples/INDEX.md)
- **Reference**: [Reference Index](../reference/INDEX.md)
- **Main Agent**: [data-validator.md](../data-validator.md)

---

Return to [main agent](../data-validator.md)
