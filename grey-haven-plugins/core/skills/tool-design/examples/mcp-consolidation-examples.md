# MCP Consolidation Examples

Real-world examples of tool consolidation for improved LLM success rates.

## Example 1: File System Tools

### Before: 12 Tools
```typescript
// Individual operations
create_file(path: string, content: string)
read_file(path: string)
write_file(path: string, content: string)
delete_file(path: string)
rename_file(oldPath: string, newPath: string)
copy_file(source: string, destination: string)
move_file(source: string, destination: string)
get_file_info(path: string)

// Directory operations
create_directory(path: string)
list_directory(path: string)
delete_directory(path: string)
search_files(pattern: string, path: string)
```

**Problems**:
- Model confused between `write_file` and `create_file`
- `rename_file` vs `move_file` ambiguity
- 12 tools to understand

### After: 2 Tools
```typescript
file_operation(params: {
  action: 'create' | 'read' | 'write' | 'delete' | 'rename' | 'copy' | 'move' | 'info'
  path: string
  content?: string        // For create/write
  destination?: string    // For rename/copy/move
})

directory_operation(params: {
  action: 'create' | 'list' | 'delete' | 'search'
  path: string
  pattern?: string        // For search
  recursive?: boolean     // For list/delete
})
```

**Results**:
- 83% → 98% success rate
- 40% fewer tool calls per task
- Clear separation: file vs directory

---

## Example 2: Issue Tracker (Linear-style)

### Before: 15 Tools
```typescript
// Issue CRUD
create_issue(title, description, team, ...)
get_issue(id)
update_issue(id, updates)
delete_issue(id)
list_issues(filters)
search_issues(query)

// Issue relations
add_issue_label(issueId, labelId)
remove_issue_label(issueId, labelId)
assign_issue(issueId, userId)
unassign_issue(issueId)
set_issue_parent(issueId, parentId)
link_issues(issueId1, issueId2, type)

// Comments
add_comment(issueId, body)
list_comments(issueId)
delete_comment(commentId)
```

### After: 4 Tools
```typescript
issue(params: {
  action: 'create' | 'get' | 'update' | 'delete' | 'list' | 'search'
  id?: string
  data?: IssueData
  filters?: IssueFilters
  query?: string
})

issue_relations(params: {
  action: 'add_label' | 'remove_label' | 'assign' | 'unassign' | 'set_parent' | 'link'
  issueId: string
  targetId?: string       // labelId, userId, parentId, linkedIssueId
  linkType?: 'blocks' | 'relates' | 'duplicates'
})

comment(params: {
  action: 'add' | 'list' | 'delete'
  issueId?: string
  commentId?: string
  body?: string
})

project(params: {
  action: 'get' | 'list' | 'create' | 'update'
  id?: string
  data?: ProjectData
})
```

**Results**:
- Clear domain separation
- 15 → 4 tools (73% reduction)
- Each tool has focused responsibility

---

## Example 3: Web Scraping (Firecrawl-style)

### Before: 8 Tools
```typescript
scrape_url(url, options)
scrape_multiple(urls, options)
crawl_site(url, depth, options)
check_crawl_status(jobId)
extract_structured(url, schema)
search_web(query)
get_sitemap(url)
convert_to_markdown(html)
```

### After: 3 Tools
```typescript
scrape(params: {
  mode: 'single' | 'batch' | 'crawl'
  urls: string | string[]
  options?: {
    depth?: number          // For crawl
    schema?: object         // For extraction
    format?: 'markdown' | 'html' | 'json'
  }
})

search(params: {
  query: string
  limit?: number
  scrapeResults?: boolean   // Also scrape result pages
})

job_status(params: {
  jobId: string
})
```

**Results**:
- Unified scraping interface
- 8 → 3 tools (62% reduction)
- `convert_to_markdown` absorbed into format option
- `get_sitemap` absorbed into crawl mode

---

## Example 4: Database Operations

### Before: 10 Tools
```typescript
// Query
select_rows(table, columns, where)
select_one(table, id)
count_rows(table, where)

// Mutations
insert_row(table, data)
insert_many(table, rows)
update_row(table, id, data)
update_many(table, where, data)
delete_row(table, id)
delete_many(table, where)

// Schema
get_table_schema(table)
```

### After: 2 Tools
```typescript
query(params: {
  type: 'select' | 'count' | 'schema'
  table: string
  columns?: string[]
  where?: WhereClause
  limit?: number
  single?: boolean        // Return one row
})

mutate(params: {
  type: 'insert' | 'update' | 'delete'
  table: string
  data?: object | object[]
  where?: WhereClause
  id?: string             // For single row operations
})
```

**Results**:
- Query vs mutate separation (safe vs dangerous)
- 10 → 2 tools (80% reduction)
- Clearer intent for each operation type

---

## Consolidation Decision Matrix

Use this to decide what to consolidate:

| Pattern | Consolidation Strategy | Example |
|---------|----------------------|---------|
| CRUD operations | Action parameter | create/read/update/delete → `action:` |
| Similar queries | Type parameter | search_code/docs/issues → `type:` |
| Same domain | Group by entity | issue + issue_labels → `issue_relations` |
| Optional features | Options object | with/without recursion → `options: { recursive }` |
| Related workflows | Combine steps | navigate + wait + extract → `extract(url)` |

---

## What NOT to Consolidate

Keep separate when:

1. **Different permissions**
   ```typescript
   // Keep separate - different auth levels
   read_public_data()
   admin_delete_user()
   ```

2. **Different domains**
   ```typescript
   // Keep separate - unrelated functionality
   file_operation()    // Filesystem
   http_request()      // Network
   ```

3. **Complex combinations exceed 6 parameters**
   ```typescript
   // Too complex - split into focused tools
   universal_operation(
     domain, action, target, data,
     options, filters, format, callback
   )
   ```

4. **Debugging/metrics needs**
   ```typescript
   // Keep granular for tracking
   process_payment()   // Track separately
   send_notification() // Track separately
   ```

---

*These patterns achieve 60-80% tool reduction with 15-30% success improvement*
