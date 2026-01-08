# Plugin Auditor

Audit Claude Code plugins and skills for best practices, deprecations, and compatibility with the latest Claude Code changelog.

## Features

- **Structure Validation**: Verify plugin directory structure and required files
- **Frontmatter Analysis**: Check agent/skill/command frontmatter for best practices
- **Deprecation Detection**: Identify deprecated patterns from recent changelog
- **Feature Adoption**: Recommend new features from recent Claude Code versions
- **Quality Scoring**: Score plugins on overall quality metrics
- **Security Review**: Check tool restrictions and dangerous patterns

## Installation

Add to your Claude Code settings:

```json
{
  "plugin": {
    "install": [
      "plugin-auditor@grey-haven-plugins"
    ]
  }
}
```

## Commands

### /audit-plugins

Audit plugins for best practices and changelog compatibility.

**Usage:**
```
/audit-plugins all                    # Audit all plugins
/audit-plugins core                   # Audit specific plugin
/audit-plugins ./path/to/plugin       # Audit plugin at path
```

## Agents

### plugin-auditor

Expert auditor that analyzes plugins against the latest changelog and best practices.

**Triggers:**
- "audit plugin"
- "check plugin"
- "validate skill"
- "plugin best practices"
- "deprecation check"
- "changelog compatibility"

## What Gets Checked

### Structure
- `.claude-plugin/plugin.json` validity
- Required directories (agents/, commands/, skills/)
- README documentation

### Agent Frontmatter
- `name` and `description` fields
- `model` specification (opus recommended)
- `color` for visual identification
- YAML-style `tools` lists
- `disallowedTools` for security
- `hooks` support (v2.1.0+)

### Skill Frontmatter
- `name` and `description` fields
- `skills` auto-load for subagents (v2.0.43+)
- `allowed-tools` restrictions (v2.0.74+)
- `context: fork` for isolation (v2.1.0+)

### Command Frontmatter
- `description` field
- `allowed-tools` field
- `argument-hint` field

### Deprecations Detected
- `includeCoAuthoredBy` (use `attribution`)
- Comma-separated tool lists (use YAML)
- Missing tool restrictions

## Audit Report

The auditor generates a comprehensive report including:

- **Overall Score**: 0-100 quality rating
- **Structure Analysis**: Directory and file validation
- **Frontmatter Analysis**: Per-agent/skill/command review
- **Deprecation Warnings**: Outdated patterns found
- **Feature Recommendations**: New features to adopt
- **Action Items**: Prioritized improvement list

## Scoring Criteria

| Category | Weight | Description |
|----------|--------|-------------|
| Structure | 20% | Valid directory structure |
| Frontmatter | 25% | Best practices in definitions |
| No Deprecations | 15% | No outdated patterns |
| Feature Adoption | 20% | Uses latest features |
| Documentation | 10% | README, examples present |
| Security | 10% | Tool restrictions in place |

## Reference Materials

The skill includes:

- **Checklists**: Complete audit checklist
- **Reference**: Changelog feature matrix, best practices guide, deprecation timeline
- **Examples**: Sample audit reports

## Version Compatibility

- **Claude Code v2.1.0+**: Full feature support
- **Claude Code v2.0.74+**: Core functionality

## License

MIT License - Copyright (c) 2025 Grey Haven Studio
