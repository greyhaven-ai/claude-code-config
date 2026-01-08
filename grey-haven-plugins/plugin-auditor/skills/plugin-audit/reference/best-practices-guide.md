# Plugin Best Practices Guide

Comprehensive guide for creating high-quality Claude Code plugins.

## Plugin Structure Best Practices

### Directory Organization

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           # Metadata
├── agents/
│   ├── primary-agent.md      # Main agent
│   └── helper-agent.md       # Supporting agent
├── commands/
│   ├── main-command.md       # Primary command
│   └── utility-command.md    # Helper commands
├── skills/
│   └── main-skill/
│       ├── SKILL.md          # Skill definition
│       ├── checklists/       # Quality checklists
│       ├── reference/        # Reference materials
│       ├── examples/         # Usage examples
│       └── templates/        # Output templates
├── README.md                 # Documentation
└── LICENSE                   # License file
```

### plugin.json Best Practices

```json
{
    "name": "my-plugin",
    "description": "Clear, concise description under 200 chars",
    "version": "1.0.0",
    "author": {
        "name": "Your Name or Organization"
    },
    "keywords": [
        "relevant",
        "searchable",
        "keywords"
    ],
    "license": "MIT",
    "skills": [
        "../skills/main-skill"
    ]
}
```

**Tips:**
- Keep `name` lowercase with hyphens
- Description should be scannable
- Keywords help discoverability
- Reference skills with relative paths

## Agent Writing Best Practices

### Description Structure

```yaml
description: "Expert [domain] agent that [primary capability]. Use when [trigger scenarios]. Triggers: '[keyword1]', '[keyword2]', '[keyword3]'. <example>Context: [scenario] user: \"[user message]\" assistant: \"[response]\" <commentary>[why this agent is appropriate]</commentary></example>"
```

**Key Elements:**
1. **Role Statement**: "Expert X that does Y"
2. **Use Cases**: "Use when..."
3. **Trigger Words**: Keywords that invoke this agent
4. **Examples**: Real conversation snippets

### Tool Configuration

```yaml
# Good: Explicit, minimal tools
tools:
  - Read
  - Write
  - Grep
  - Glob
  - TodoWrite

# Good: Block unneeded dangerous tools
disallowedTools:
  - WebFetch
  - WebSearch
  - mcp__*
  - NotebookEdit

# Bad: No restrictions (too permissive)
tools: all
```

**Principles:**
- Principle of least privilege
- Block MCP if not needed: `mcp__*`
- Block web access if not needed
- Always include `TodoWrite` for tracking

### Model Selection

| Model | Use Case |
|-------|----------|
| `opus` | Complex reasoning, quality output (default) |
| `sonnet` | Balanced quality/speed for simpler tasks |
| `haiku` | Fast, simple tasks, high volume |

```yaml
# Good: Default for quality work (recommended)
model: opus

# Good: Simpler tasks where speed matters
model: sonnet

# Good: Fast, simple operations
model: haiku
```

**Note:** Opus 4.5 is the most capable model and should be the default choice for agents that require quality reasoning and output. Use sonnet/haiku only when speed is more important than quality.

## Skill Writing Best Practices

### SKILL.md Structure

```yaml
---
name: skill-identifier
description: "Description with trigger words..."
skills:
  - related-skill-1        # Auto-load for subagents
allowed-tools:
  - Read
  - Write
  - Bash
---

# Skill Title

Brief overview paragraph.

## Description
Detailed description of skill capabilities.

## What's Included
- **Checklists**: [list]
- **Reference**: [list]
- **Examples**: [list]

## Use When
- Scenario 1
- Scenario 2

## Related Agents
- `agent-name`

**Skill Version**: 1.0
```

### Supporting Materials

**Checklists** (`checklists/`):
- Step-by-step validation lists
- Quality assurance guides
- Pre-submission checks

**Reference** (`reference/`):
- Technical documentation
- API references
- Pattern libraries

**Examples** (`examples/`):
- Real-world usage scenarios
- Before/after comparisons
- Common patterns

## Command Writing Best Practices

### Command Structure

```yaml
---
description: Brief, action-oriented description
allowed-tools: Read, Write, Bash, Task, TodoWrite
argument-hint: [what arguments to provide]
---

Execute action: $ARGUMENTS

<context>
Background information for the command
</context>

<requirements>
- Requirement 1
- Requirement 2
</requirements>

<actions>
1. Step 1
2. Step 2
3. Step 3
</actions>

Clear closing instruction for the agent.
```

### Argument Handling

```yaml
# Good: Clear hint
argument-hint: [feature description or file path]

# Good: Optional indicator
argument-hint: [optional: specific scope]

# Bad: No hint (confusing)
# (missing argument-hint)
```

## Security Best Practices

### Tool Restrictions

1. **Default Deny**: Start with minimal tools, add as needed
2. **Block Wildcards**: Use `mcp__*` to block all MCP if unused
3. **Audit Dangerous Tools**:
   - `Bash` - Can execute arbitrary commands
   - `Write` - Can overwrite files
   - `WebFetch` - Can access external resources

### Sensitive Data

1. Never hardcode credentials
2. Use environment variables via hooks
3. Don't log sensitive information

### Input Validation

1. Validate `$ARGUMENTS` in commands
2. Use hooks for pre-execution validation
3. Sanitize file paths

## Documentation Best Practices

### README.md Template

```markdown
# Plugin Name

Brief description of what the plugin does.

## Installation

How to install/enable the plugin.

## Features

- Feature 1: Description
- Feature 2: Description

## Commands

### /command-name
Description of what this command does.

**Usage:**
```
/command-name [arguments]
```

## Agents

### agent-name
When to use this agent and what it does.

## Configuration

Any configuration options or settings.

## Version Compatibility

- Claude Code v2.1.0+: Full support
- Claude Code v2.0.74+: Basic support

## License

License information.
```

### Description Writing Tips

1. **Be Specific**: "Analyzes TypeScript code for..." not "Helps with code"
2. **Include Triggers**: Words that should invoke this agent/skill
3. **Add Examples**: Show real usage scenarios
4. **State Prerequisites**: What the user needs before using

## Versioning Best Practices

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 → Initial release
1.1.0 → New features (backward compatible)
1.1.1 → Bug fixes
2.0.0 → Breaking changes
```

### Changelog Maintenance

Keep a CHANGELOG.md with:
- Version number and date
- Added features
- Changed behavior
- Deprecated items
- Removed features
- Fixed bugs

## Testing Best Practices

1. **Test Structure**: Verify plugin loads correctly
2. **Test Commands**: Run each command with various inputs
3. **Test Agents**: Verify agent triggers appropriately
4. **Test Edge Cases**: Empty inputs, invalid arguments
5. **Test Tool Restrictions**: Verify blocked tools are blocked
