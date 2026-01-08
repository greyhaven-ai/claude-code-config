# Deprecation Timeline

Tracking deprecated features, settings, and patterns in Claude Code.

## Active Deprecations

### v2.0.70 - Memory Shortcut Removed
| Item | `#` shortcut for quick memory entry |
|------|-------------------------------------|
| Status | Removed |
| Replacement | Edit CLAUDE.md directly |
| Impact | User workflow |
| Action Required | Update documentation referencing # shortcut |

### v2.0.62 - Git Attribution Setting
| Item | `includeCoAuthoredBy` setting |
|------|-------------------------------|
| Status | Deprecated |
| Replacement | `attribution` setting |
| Impact | Git commit configuration |
| Action Required | Update settings.json if using old setting |

**Migration:**
```json
// Old
{
  "includeCoAuthoredBy": true
}

// New
{
  "attribution": "co-authored-by"  // or "none", "trailer"
}
```

## Style Deprecations (Soft)

These are not breaking but are considered outdated patterns:

### Comma-Separated Tool Lists
| Item | Comma-separated `allowed-tools` |
|------|--------------------------------|
| Status | Discouraged (v2.1.0+) |
| Replacement | YAML-style lists |
| Impact | Frontmatter readability |
| Action Required | Convert to YAML format |

**Migration:**
```yaml
# Old (still works but discouraged)
allowed-tools: Read, Write, Bash, Grep

# New (preferred)
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
```

### Inline Tool Descriptions
| Item | Listing tools in description string |
|------|-------------------------------------|
| Status | Discouraged |
| Replacement | Separate `tools:` field |
| Impact | Agent clarity |
| Action Required | Move tool lists to proper field |

## Upcoming Changes to Watch

Based on changelog patterns, these may change in future versions:

### Potential Future Deprecations
- Old hook configuration formats
- Legacy permission patterns
- Older MCP configuration styles

### Features Being Replaced
- Manual skill registration (moving toward auto-discovery)
- Static tool configurations (moving toward dynamic)

## Version Compatibility Matrix

| Feature | Introduced | Deprecated | Removed |
|---------|------------|------------|---------|
| `includeCoAuthoredBy` | < v2.0 | v2.0.62 | - |
| `#` memory shortcut | < v2.0 | v2.0.70 | v2.0.70 |
| Comma tool lists | < v2.0 | - | - |
| `allowed-tools` enforcement | v2.0.74 | - | - |
| `disallowedTools` | v2.0.64 | - | - |
| `skills:` auto-load | v2.0.43 | - | - |
| `context: fork` | v2.1.0 | - | - |
| Frontmatter hooks | v2.1.0 | - | - |

## Checking for Deprecations

### Automated Check Commands

```bash
# Check for includeCoAuthoredBy
grep -r "includeCoAuthoredBy" ~/.claude/ .claude/

# Check for comma-separated tools
grep -rE "allowed-tools:\s*\w+,\s*\w+" --include="*.md"

# Check for old patterns in frontmatter
grep -rE "^tools:\s*\w+,\s*\w+" --include="*.md"
```

### Manual Review Checklist

- [ ] No `includeCoAuthoredBy` in settings
- [ ] No references to `#` shortcut in docs
- [ ] Tool lists use YAML format
- [ ] Agents use `disallowedTools` where appropriate
- [ ] Skills use `allowed-tools` (v2.0.74 requirement)

## Handling Deprecation Warnings

### Priority Levels

1. **Critical**: Features removed or breaking
   - `#` shortcut - Must update workflows

2. **High**: Features deprecated but still working
   - `includeCoAuthoredBy` - Should migrate soon

3. **Medium**: Style changes recommended
   - Comma-separated lists - Convert when convenient

4. **Low**: Best practice updates
   - Add new features like hooks

### Migration Strategy

1. **Identify**: Run deprecation checks
2. **Document**: List all deprecated items found
3. **Prioritize**: Critical > High > Medium > Low
4. **Migrate**: Update one pattern at a time
5. **Test**: Verify functionality after changes
6. **Document**: Update README with version compatibility
