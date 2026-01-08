# Claude Code Changelog Feature Matrix

Quick reference for plugin-relevant features by version.

## Feature Introduction Timeline

| Version | Feature | Plugin Impact | Priority |
|---------|---------|---------------|----------|
| **v2.1.0** | Skill hot-reload | Skills update without restart | Info |
| **v2.1.0** | `context: fork` | Isolated skill execution | Medium |
| **v2.1.0** | `agent` field in skills | Custom agent for skill | Medium |
| **v2.1.0** | Hooks in skill/agent frontmatter | Scoped validation | High |
| **v2.1.0** | `once: true` hook config | Run hook only once | Medium |
| **v2.1.0** | YAML lists in `allowed-tools` | Cleaner frontmatter | High |
| **v2.1.0** | Skills visible in slash menu | Default visibility | Info |
| **v2.1.0** | Prompt/agent hooks from plugins | Hook types expanded | Medium |
| **v2.0.74** | `allowed-tools` applied properly | Tool restrictions work | Critical |
| **v2.0.74** | LSP tool | Code intelligence | Low |
| **v2.0.64** | `disallowedTools` | Block dangerous tools | High |
| **v2.0.64** | Background agents | Async execution | Medium |
| **v2.0.64** | Named sessions | Session management | Low |
| **v2.0.64** | `/rules` support | Custom rules | Info |
| **v2.0.62** | `attribution` setting | Replaces includeCoAuthoredBy | Medium |
| **v2.0.59** | `agent` setting | Main thread agent config | Low |
| **v2.0.43** | `skills:` field | Auto-load subagent skills | High |

## Priority Levels

- **Critical**: Required for proper functionality
- **High**: Strongly recommended for best practices
- **Medium**: Recommended for enhanced experience
- **Low**: Nice to have
- **Info**: Awareness only

## Version Compatibility Notes

### Breaking Changes

| Version | Change | Migration Path |
|---------|--------|----------------|
| v2.0.74 | `allowed-tools` now enforced | Ensure tools are listed |
| v2.0.62 | `includeCoAuthoredBy` deprecated | Use `attribution` |
| v2.0.70 | `#` shortcut removed | Edit CLAUDE.md directly |

### Non-Breaking Additions

These can be adopted incrementally:
- `disallowedTools` (v2.0.64)
- `skills:` auto-load (v2.0.43)
- `context: fork` (v2.1.0)
- YAML-style lists (v2.1.0)
- Hook support (v2.1.0)

## Frontmatter Field Reference

### Agent Fields

```yaml
---
# Required
name: string                    # Agent identifier
description: string             # Description with examples

# Recommended (All versions)
model: sonnet|haiku|opus        # Model preference
color: string                   # Visual color

# v2.0.64+
tools:                          # Allowed tools (YAML list)
  - Tool1
  - Tool2
disallowedTools:                # Blocked tools
  - DangerousTool
  - mcp__*

# v2.1.0+
hooks:                          # Agent-scoped hooks
  PreToolUse:
    - command: "script.sh"
      once: true
---
```

### Skill Fields

```yaml
---
# Required
name: string                    # Skill identifier
description: string             # Description with triggers

# v2.0.43+
skills:                         # Auto-load for subagents
  - related-skill

# v2.0.74+
allowed-tools:                  # Tool restrictions
  - Read
  - Write

# v2.1.0+
context: fork                   # Isolated execution
agent: custom-agent             # Execution agent
user-invocable: false           # Hide from slash menu
hooks:                          # Skill-scoped hooks
  PreToolUse:
    - command: "validate.sh"
---
```

### Command Fields

```yaml
---
# Required
description: string             # Brief description

# Recommended
allowed-tools: Tool1, Tool2     # or YAML list
argument-hint: string           # Argument placeholder

# v2.1.0+
context: fork                   # Isolated execution
hooks:                          # Command-scoped hooks
  Stop:
    - command: "cleanup.sh"
---
```

## Feature Adoption Checklist by Version

### Minimum v2.0.74 Compliance
- [ ] `allowed-tools` in skills (now enforced)
- [ ] Valid plugin structure

### v2.0.64 Best Practices
- [ ] `disallowedTools` for agents
- [ ] Explicit `tools` lists

### v2.1.0 Modern Plugins
- [ ] YAML-style tool lists
- [ ] Hook support where beneficial
- [ ] `skills:` auto-load configured
- [ ] `context: fork` for isolation needs
