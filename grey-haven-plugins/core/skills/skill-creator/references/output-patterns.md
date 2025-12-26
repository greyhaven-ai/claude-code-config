# Output Patterns

Patterns for producing consistent, high-quality output in skills.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Templates (API responses, data formats)

```markdown
## Report Structure

ALWAYS use this exact structure:

# [Analysis Title]

## Executive Summary
[One-paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Flexible Templates (when adaptation is useful)

```markdown
## Report Structure

Sensible default format (adapt as needed):

# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adapt sections based on discoveries]

## Recommendations
[Tailor to specific context]

Adjust sections for the analysis type.
```

## Examples Pattern

For skills where quality depends on seeing examples:

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow: type(scope): brief description, then detailed explanation.
```

Examples convey style and detail better than descriptions alone.

## Grey Haven Output Patterns

### Code Output

```markdown
## Code Style

Follow Grey Haven conventions:

**TypeScript:**
- 2-space indentation
- Single quotes for strings
- Explicit return types
- Interfaces over types (when possible)

**Python:**
- 4-space indentation
- Double quotes for strings
- Type hints on all functions
- Pydantic for data models
```

### Documentation Output

```markdown
## Documentation Format

### Function Documentation
```typescript
/**
 * Brief description of what the function does.
 *
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws ErrorType - When this error occurs
 *
 * @example
 * const result = myFunction('input');
 */
```

### Commit Documentation
```
type(scope): short description

Longer explanation if needed. Focus on WHY not WHAT.

Fixes #123
```
```

### API Response Output

```markdown
## API Response Format

Success response:
```json
{
  "success": true,
  "data": { ... },
  "metadata": {
    "requestId": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

Error response:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { ... }
  }
}
```
```

## Quality Markers

Add quality indicators to guide output:

```markdown
## Quality Checklist

Before submitting:
- [ ] All tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Types are explicit
- [ ] Edge cases handled
```

## Structured Output (LLM Integration)

For LLM pipelines requiring parsed output:

```markdown
## Structured Response

I will parse this programmatically. Respond with valid JSON:

{
  "summary": "Brief summary (1-2 sentences)",
  "category": "type_a" | "type_b" | "type_c",
  "confidence": 0.0 to 1.0,
  "reasoning": "Why this classification"
}

Ensure JSON is complete and parseable.
```

---

*Consistent output patterns improve reliability and user experience*
