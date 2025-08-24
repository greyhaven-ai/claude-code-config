# Hooks Documentation

Claude Code hooks provide deterministic control over the AI assistant's behavior through event-driven automation.

## 📚 Documentation

- **[Comprehensive Hook Guide](./comprehensive-guide.md)** - Complete guide covering basics to advanced patterns
  - Hook events and lifecycle
  - Configuration and implementation
  - Advanced workflow patterns
  - Security and performance
  - Examples and templates

- **[Integration Guide](./integration-guide.md)** - Hooks, commands, and agents working together
  - Integration patterns
  - Workflow orchestration
  - Practical examples

## 🎯 Quick Reference

### Hook Events
- `PreToolUse` - Before tool execution (can block)
- `PostToolUse` - After tool execution
- `UserPromptSubmit` - When prompt submitted
- `SessionStart` - Session initialization
- `Notification` - Claude notifications
- `Stop` / `SubagentStop` - Response completion
- `PreCompact` - Before context compaction

### Configuration Locations
- `~/.claude/settings.json` - User-wide settings
- `.claude/settings.json` - Project settings (version controlled)
- `.claude/settings.local.json` - Local overrides (not committed)

## 🚀 Quick Start

See [Getting Started](../getting-started/README.md) for installation and [Hook Activation Guide](../getting-started/hook-activation.md) for setup instructions.

## 💡 Common Use Cases

- **Security**: Validate operations before execution
- **Quality**: Auto-format and test after edits
- **Context**: Inject relevant information automatically
- **Workflow**: Chain complex operations seamlessly
- **Monitoring**: Track metrics and performance