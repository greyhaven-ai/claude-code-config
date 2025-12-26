# Tool Consolidation Guide

Complete methodology for reducing tool count while improving capability.

## The Consolidation Process

### Step 1: Inventory

List all tools with:
- Name
- Description
- Parameters
- Usage frequency (if available)
- Dependencies

### Step 2: Group by Domain

Cluster tools into logical domains:

```
File Operations:
  - create_file, read_file, write_file, delete_file
  - list_directory, search_files

Issue Management:
  - create_issue, update_issue, list_issues
  - add_comment, get_comments
```

### Step 3: Identify Consolidation Candidates

Look for:
- **CRUD patterns** - Create/Read/Update/Delete → single tool with action param
- **Related queries** - Multiple similar queries → single tool with type param
- **Sequential operations** - Operations always used together → combine

### Step 4: Design Consolidated Tools

Each consolidated tool should:
- Have clear, unambiguous purpose
- Accept structured parameters
- Return consistent response format
- Handle errors gracefully

### Step 5: Validate with Use Cases

Test consolidated design against real workflows:
- Does it require fewer tool calls?
- Is parameter selection clear?
- Are edge cases handled?

## Consolidation Patterns

### Pattern 1: Action Parameter

**Before**:
```typescript
create_file(path, content)
read_file(path)
update_file(path, content)
delete_file(path)
```

**After**:
```typescript
file(action: 'create' | 'read' | 'update' | 'delete', path: string, content?: string)
```

### Pattern 2: Type Parameter

**Before**:
```typescript
search_code(query)
search_docs(query)
search_issues(query)
```

**After**:
```typescript
search(type: 'code' | 'docs' | 'issues', query: string)
```

### Pattern 3: Options Object

**Before**:
```typescript
list_files(path)
list_files_recursive(path)
list_files_with_filter(path, pattern)
list_files_with_details(path)
```

**After**:
```typescript
list_files(path: string, options?: {
  recursive?: boolean
  pattern?: string
  details?: boolean
})
```

### Pattern 4: Workflow Combination

**Before** (3 calls needed):
```typescript
navigate(url)
wait_for_selector(selector)
get_text(selector)
```

**After** (1 call):
```typescript
extract_text(url: string, selector: string, options?: { waitFor?: string })
```

## Case Study: Vercel d0

### Before (17 tools)
```
create_file, read_file, update_file, delete_file,
list_directory, search_files, get_file_info,
create_folder, rename_file, move_file, copy_file,
get_permissions, set_permissions, watch_file,
compress_file, decompress_file, calculate_hash
```

**Success rate**: 80%
**Common failures**: Wrong tool selection, parameter confusion

### After (2 tools)
```
file_operation(action, path, content?, options?)
directory_operation(action, path, options?)
```

**Success rate**: 100%
**Key insight**: Model can reason about 2 tools perfectly

### Consolidation Decisions

| Original Tools | Merged Into | Reasoning |
|----------------|-------------|-----------|
| create/read/update/delete_file | file_operation | CRUD pattern |
| rename/move/copy_file | file_operation(action: 'rename'/'move'/'copy') | File mutations |
| get_permissions/set_permissions | file_operation(options: {permissions}) | File metadata |
| compress/decompress | Removed | Rarely used |
| calculate_hash | Removed | Rarely used |
| watch_file | Removed | Not needed for generation |
| list_directory, search_files, create_folder | directory_operation | Directory operations |

## When NOT to Consolidate

Keep tools separate when:

1. **Different domains** - Don't merge file ops with API calls
2. **Complex parameters** - When merged params exceed 5-6 fields
3. **Different permissions** - When tools have different auth requirements
4. **Debugging** - When you need tool-level metrics

## Measuring Success

Track these metrics before/after consolidation:

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Tool count | 17 | 2 | <5 |
| Success rate | 80% | 100% | >95% |
| Avg calls per task | 8 | 4 | <5 |
| Wrong tool selections | 15% | 0% | <2% |

## Implementation Checklist

- [ ] Inventory complete with usage data
- [ ] Domains identified and grouped
- [ ] Consolidation candidates marked
- [ ] New tool interfaces designed
- [ ] Parameter schemas defined
- [ ] Use cases tested
- [ ] Metrics baseline captured
- [ ] Rollout plan created

---

*Based on Vercel d0 case study and Anthropic multi-agent research*
