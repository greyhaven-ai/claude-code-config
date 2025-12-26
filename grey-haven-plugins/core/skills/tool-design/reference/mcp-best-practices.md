# MCP Tool Design Best Practices

Guidelines for creating effective Model Context Protocol tools.

## Naming Conventions

### Use Verb-Noun Pattern
```
get_user           // Good
user               // Ambiguous
fetchUserData      // Inconsistent casing
```

### Consistent Casing
```
get_user, list_projects, create_issue    // Good (snake_case)
getUser, listProjects, createIssue       // Acceptable (camelCase)
GetUser, LIST_PROJECTS, Create-Issue     // Bad (inconsistent)
```

### Avoid Abbreviations
```
get_configuration    // Good
get_config           // Acceptable
get_cfg              // Bad
```

### MCP Prefixes
```
mcp__server__tool    // Standard MCP format
server_tool          // Without prefix (avoid collisions)
```

## Parameter Design

### Use Clear Types
```typescript
// Good
interface SearchParams {
  query: string
  limit: number
  includeArchived: boolean
}

// Bad
interface SearchParams {
  q: string        // Abbreviated
  n: number        // Unclear purpose
  a: boolean       // No context
}
```

### Provide Defaults
```typescript
search(query: string, options?: {
  limit?: number       // Default: 10
  offset?: number      // Default: 0
  sort?: 'asc' | 'desc' // Default: 'desc'
})
```

### Use Enums for Fixed Options
```typescript
// Good
action: 'create' | 'read' | 'update' | 'delete'

// Bad
action: string  // What values are valid?
```

### Required vs Optional
```typescript
interface CreateIssue {
  // Required - always needed
  title: string
  team: string

  // Optional - sensible defaults exist
  description?: string
  priority?: 1 | 2 | 3 | 4
  labels?: string[]
}
```

## Descriptions

### Tool Description
Every tool needs:
1. **What it does** (1 sentence)
2. **When to use it** (use cases)
3. **What it returns** (output format)

```typescript
{
  name: "search_issues",
  description: `
    Search for issues across the workspace.
    Use when finding issues by title, description, or labels.
    Returns array of issue objects with id, title, state, and assignee.
  `
}
```

### Parameter Descriptions
```typescript
{
  name: "query",
  description: "Search query. Supports title, description, and label:value syntax."
}

{
  name: "limit",
  description: "Maximum results to return. Range: 1-100. Default: 10."
}
```

## Response Format

### Consistent Structure
```typescript
// Good - consistent wrapper
interface ToolResponse<T> {
  success: boolean
  data?: T
  error?: string
}

// Usage
{ success: true, data: { issues: [...] } }
{ success: false, error: "Rate limit exceeded" }
```

### Include Metadata
```typescript
interface ListResponse<T> {
  data: T[]
  pagination: {
    total: number
    hasMore: boolean
    cursor?: string
  }
}
```

### Meaningful Errors
```typescript
// Good
{ success: false, error: "Issue ABC-123 not found in project XYZ" }

// Bad
{ success: false, error: "Not found" }
{ success: false, error: "Error" }
```

## Error Handling

### Graceful Degradation
```typescript
try {
  const result = await fetchData(id)
  return { success: true, data: result }
} catch (error) {
  if (error.status === 404) {
    return { success: false, error: `Item ${id} not found` }
  }
  if (error.status === 429) {
    return { success: false, error: "Rate limited. Retry in 60 seconds." }
  }
  return { success: false, error: `Unexpected error: ${error.message}` }
}
```

### Actionable Messages
```typescript
// Good - tells user what to do
"API key not configured. Set FIRECRAWL_API_KEY environment variable."

// Bad - just states problem
"Authentication failed"
```

## Performance

### Batch Operations
```typescript
// Good - one call for multiple items
get_issues(ids: string[]): Issue[]

// Less efficient - multiple calls
get_issue(id: string): Issue  // Called N times
```

### Pagination
```typescript
list_issues(options?: {
  limit?: number     // Page size
  cursor?: string    // Pagination cursor
})
```

### Caching Hints
```typescript
{
  name: "get_documentation",
  description: "Fetches documentation. Results cached for 1 hour.",
  // Or include cache control in response
}
```

## Security

### Input Validation
```typescript
function sanitizePath(path: string): string {
  // Prevent path traversal
  if (path.includes('..')) {
    throw new Error('Path traversal not allowed')
  }
  return path
}
```

### Scope Limitations
```typescript
{
  name: "list_files",
  description: "Lists files in allowed directories only. Cannot access system files."
}
```

### Credential Handling
```typescript
// Never include credentials in responses
{
  user: { name: "John", email: "john@example.com" }
  // NOT: apiKey, password, token
}
```

## Testing Tools

### Required Tests
1. **Happy path** - Normal operation
2. **Edge cases** - Empty input, max values
3. **Error cases** - Invalid input, missing resources
4. **Security** - Path traversal, injection

### Test Template
```typescript
describe('search_issues', () => {
  it('returns matching issues for valid query', async () => {
    const result = await searchIssues({ query: 'bug' })
    expect(result.success).toBe(true)
    expect(result.data.length).toBeGreaterThan(0)
  })

  it('returns empty array for no matches', async () => {
    const result = await searchIssues({ query: 'nonexistent12345' })
    expect(result.success).toBe(true)
    expect(result.data).toEqual([])
  })

  it('handles invalid query gracefully', async () => {
    const result = await searchIssues({ query: '' })
    expect(result.success).toBe(false)
    expect(result.error).toContain('Query required')
  })
})
```

---

*Following these practices improves tool usability by LLMs and reduces errors.*
