# Plugin Audit Checklist

Comprehensive checklist for auditing Claude Code plugins against best practices and the latest changelog.

## Structure Validation

### Required Files
- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `plugin.json` has `name`, `description`, `version` fields
- [ ] `plugin.json` has `author` field with `name`
- [ ] At least one of: `agents/`, `commands/`, or `skills/` directory exists

### Recommended Structure
- [ ] `README.md` exists with plugin documentation
- [ ] `keywords` array in plugin.json for discoverability
- [ ] `license` field specified
- [ ] Skill directories have proper subdirectories (checklists/, reference/, examples/)

## Agent Frontmatter (v2.1.0 Standards)

### Required Fields
- [ ] `name:` - Agent identifier
- [ ] `description:` - Clear description with trigger words

### Recommended Fields
- [ ] `model:` - Explicit model preference (sonnet, haiku, opus)
- [ ] `color:` - Visual identification color
- [ ] `tools:` - YAML-style list of allowed tools
- [ ] `disallowedTools:` - Tools to explicitly block (v2.0.64+)

### Best Practices
- [ ] Description includes `<example>` blocks for LLM context
- [ ] Uses YAML-style lists instead of comma-separated values
- [ ] Blocks MCP tools if not needed: `mcp__*`
- [ ] Blocks dangerous tools: `WebFetch`, `WebSearch` if not required

### v2.1.0 Features
- [ ] `hooks:` defined for agent-scoped validation (if applicable)
- [ ] Hook configurations use `once: true` where appropriate

## Skill Frontmatter (v2.1.0 Standards)

### Required Fields
- [ ] `name:` - Skill identifier
- [ ] `description:` - Clear description with trigger words

### Recommended Fields (v2.0.43+)
- [ ] `skills:` - Related skills to auto-load for subagents
- [ ] `allowed-tools:` - YAML-style tool restrictions (v2.0.74+)

### v2.1.0 Features
- [ ] `context: fork` used for isolated execution if needed
- [ ] `agent:` field to specify execution agent if needed
- [ ] `hooks:` defined for skill-scoped validation
- [ ] `user-invocable: false` if skill shouldn't appear in slash menu

## Command Frontmatter

### Required Fields
- [ ] `description:` - Brief description

### Recommended Fields
- [ ] `allowed-tools:` - Tools available to command
- [ ] `argument-hint:` - Hint for command arguments

### v2.1.0 Features
- [ ] `context: fork` for isolated execution
- [ ] `hooks:` defined for command-scoped validation

## Deprecation Checks

### v2.0.62 Deprecations
- [ ] NOT using `includeCoAuthoredBy` (use `attribution` instead)

### v2.0.70 Deprecations
- [ ] NOT using `#` shortcut for memory (edit CLAUDE.md directly)

### Style Deprecations
- [ ] NOT using comma-separated `allowed-tools` (use YAML lists)
- [ ] NOT using inline tool lists in description

## Security Review

### Tool Restrictions
- [ ] Agents have appropriate `disallowedTools`
- [ ] Skills have `allowed-tools` restrictions
- [ ] No overly permissive tool access

### Dangerous Patterns
- [ ] No hardcoded credentials or secrets
- [ ] No commands that could damage user data
- [ ] Bash commands have appropriate guards

## Documentation Quality

### Description Quality
- [ ] Clear, concise descriptions
- [ ] Trigger words included for discoverability
- [ ] Example blocks for LLM context

### README Quality
- [ ] Installation instructions
- [ ] Usage examples
- [ ] Feature list
- [ ] Version compatibility notes

## Scoring Guide

| Score | Interpretation |
|-------|----------------|
| 90-100 | Excellent - Follows all best practices |
| 80-89 | Good - Minor improvements needed |
| 70-79 | Acceptable - Several improvements recommended |
| 60-69 | Needs Work - Multiple issues to address |
| <60 | Critical - Major restructuring needed |

### Score Breakdown
- Structure: 20 points
- Frontmatter: 25 points
- No Deprecations: 15 points
- Feature Adoption: 20 points
- Documentation: 10 points
- Security: 10 points
