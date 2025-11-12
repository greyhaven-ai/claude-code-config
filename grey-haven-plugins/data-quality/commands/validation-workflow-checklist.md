# Data Validation Workflow Checklist

**Use when implementing data validation for features, APIs, or database models.**

## Phase 1: Requirements Analysis

- [ ] Data fields identified (required vs optional)
- [ ] Data types defined for each field
- [ ] Format constraints documented (email, URL, phone, etc.)
- [ ] Range constraints defined (min/max values)
- [ ] Pattern constraints specified (regex patterns)
- [ ] Cross-field validations identified
- [ ] Business rules documented
- [ ] Database schema requirements clear
- [ ] Unique constraints identified
- [ ] Index requirements defined

## Phase 2: Test-First Development (TDD)

### Red Phase (Failing Tests)
- [ ] Test file structure created (`tests/validation/`)
- [ ] Test class created for schema
- [ ] Test for valid data written
- [ ] Tests for invalid formats written
- [ ] Tests for boundary conditions written
- [ ] Tests for cross-field validation written
- [ ] Tests for business rules written
- [ ] All tests fail (models don't exist yet)

### Green Phase (Minimal Implementation)
- [ ] Basic Pydantic model created
- [ ] Required fields added
- [ ] Basic types defined
- [ ] Tests run and some passing
- [ ] Iteratively add features until all tests pass

### Blue Phase (Refactor)
- [ ] Field validators added
- [ ] Model validators added
- [ ] Configuration optimized
- [ ] Code cleaned up
- [ ] All tests still passing

## Phase 3: Pydantic Model Implementation

### Field Definitions
- [ ] All fields defined with correct types
- [ ] Field() used for metadata
- [ ] Descriptions added to all fields
- [ ] Examples provided for documentation
- [ ] Default values set where appropriate
- [ ] Optional fields marked with Optional[]

### Constraints
- [ ] String length constraints (min_length, max_length)
- [ ] Numeric range constraints (ge, gt, le, lt)
- [ ] Pattern constraints (regex)
- [ ] Email validation (EmailStr)
- [ ] Constrained types used (constr, conint, confloat)

### Field Validators
- [ ] @field_validator decorators added
- [ ] Single-field validation logic implemented
- [ ] Custom error messages defined
- [ ] Validator methods use @classmethod
- [ ] Validators return validated value

### Model Validators
- [ ] @model_validator decorators added
- [ ] Cross-field validation logic implemented
- [ ] Business rules enforced
- [ ] mode='after' or mode='before' chosen appropriately
- [ ] Validators return self

### Configuration
- [ ] model_config dict defined
- [ ] str_strip_whitespace enabled if needed
- [ ] validate_assignment set appropriately
- [ ] json_schema_extra added with examples
- [ ] from_attributes set for ORM compatibility

## Phase 4: Database Schema Alignment

### SQLModel/SQLAlchemy Model
- [ ] Database model created
- [ ] Table name defined
- [ ] All fields mapped to columns
- [ ] Primary key defined
- [ ] Foreign keys defined
- [ ] Unique constraints added
- [ ] Indexes created
- [ ] Default values set
- [ ] Timestamps added (created_at, updated_at)
- [ ] tenant_id added (multi-tenant)

### Schema Alignment
- [ ] Pydantic fields match database columns
- [ ] Data types are compatible
- [ ] Constraints are consistent
- [ ] Schema alignment test created
- [ ] Test passing

### Migration
- [ ] Migration file generated
- [ ] Migration reviewed for correctness
- [ ] Migration tested on dev database
- [ ] Rollback tested
- [ ] Migration applied to production (when ready)

## Phase 5: API Integration

### Request Handling
- [ ] Request handler created
- [ ] Request body parsed
- [ ] Pydantic validation applied
- [ ] ValidationError caught
- [ ] Error formatted for API response
- [ ] Success response uses response schema

### Error Formatting
- [ ] ValidationErrorFormatter created
- [ ] Errors grouped by field
- [ ] Error messages clear and actionable
- [ ] HTTP 400 status for validation errors
- [ ] Response format consistent with API standards

### Testing
- [ ] Integration tests for valid requests
- [ ] Integration tests for invalid requests
- [ ] Error response format verified
- [ ] Status codes verified

## Phase 6: Data Quality Monitoring

### Great Expectations Setup
- [ ] Great Expectations initialized
- [ ] Data source configured
- [ ] Expectation suite created
- [ ] Expectations defined for each field
- [ ] Null checks added
- [ ] Uniqueness checks added
- [ ] Format checks added
- [ ] Range checks added

### Validation Scripts
- [ ] Batch validation script created
- [ ] Validation scheduled (cron/airflow)
- [ ] Results stored
- [ ] Alerts configured for failures
- [ ] Dashboard created for data quality metrics

## Phase 7: Observability

### Metrics
- [ ] Prometheus metrics defined
- [ ] validation_errors_total counter created
- [ ] validation_duration_seconds histogram created
- [ ] Metrics labeled appropriately (field, error_type)
- [ ] Metrics tracked in handlers

### Monitoring
- [ ] Grafana dashboard created
- [ ] Validation error rate chart added
- [ ] Validation latency chart added
- [ ] Error breakdown by field
- [ ] Alerts configured for high error rates

## Phase 8: Documentation

### OpenAPI Specification
- [ ] OpenAPI spec generation script created
- [ ] Request schema added to spec
- [ ] Response schema added to spec
- [ ] Error responses documented
- [ ] Examples included in spec
- [ ] Spec published to docs site

### Code Documentation
- [ ] Docstrings added to all schemas
- [ ] Field descriptions clear
- [ ] Validator logic documented
- [ ] Examples provided
- [ ] README updated with validation info

## Post-Implementation

### Testing
- [ ] Unit tests for all validators (>80% coverage)
- [ ] Integration tests for API endpoints
- [ ] End-to-end tests for full workflow
- [ ] Performance tests for validation speed
- [ ] All tests passing

### Performance
- [ ] Validation latency < 10ms (p95)
- [ ] No memory leaks
- [ ] Validators cached if expensive
- [ ] Profiling done if slow

### Security
- [ ] Passwords hashed before storage
- [ ] Sensitive data not logged
- [ ] Input sanitization applied
- [ ] SQL injection protection verified
- [ ] XSS protection verified

### Multi-Tenant
- [ ] tenant_id included in all schemas
- [ ] Tenant isolation tested
- [ ] RLS policies applied to database
- [ ] Cross-tenant access prevented

## Critical Validations

- [ ] All user input validated before processing
- [ ] Database schema matches Pydantic models
- [ ] Error messages don't leak sensitive information
- [ ] Validation errors return HTTP 400
- [ ] Server errors return HTTP 500
- [ ] OpenAPI spec matches implementation
- [ ] All tests passing (>80% coverage)
- [ ] Performance meets requirements (<10ms p95)
- [ ] Monitoring and alerting configured
- [ ] Documentation complete and accurate
