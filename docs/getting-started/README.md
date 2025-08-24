# Getting Started

Quick setup guide for Grey Haven Claude Code configurations.

## 🚀 Quick Install

```bash
# Clone repository
git clone https://github.com/grey-haven/claude-code-config.git

# Run setup script
bash claude-code-config/setup-claude-code/setup.sh /path/to/your/project

# Or manual setup
cp -r claude-code-config/.claude /your/project/
```

## 📋 Prerequisites

### Required
- `git` - Version control
- `ripgrep` (`rg`) - Fast file searching
- Claude Code 1.0.80+

### Language-Specific

**Python Projects:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**JavaScript/TypeScript:**
```bash
curl -fsSL https://bun.sh/install | bash
```

## 🔧 Configuration

### Settings Hierarchy
1. `~/.claude/settings.json` - User-wide settings
2. `.claude/settings.json` - Project settings
3. `.claude/settings.local.json` - Local overrides

### Basic Configuration
```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "UserPromptSubmit": []
  },
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statuslines/grey-haven-default.sh"
  }
}
```

## 📚 Next Steps

1. **[Activate Hooks](./hook-activation.md)** - Enable automation
2. **[Configure Statusline](../statuslines/README.md)** - Customize display
3. **[Explore Commands](../commands/README.md)** - Learn workflows
4. **[Understand Agents](../agents/README.md)** - AI assistants

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "command not found" | Install missing prerequisites |
| Hook not running | Check executable permissions |
| Settings not loading | Validate JSON syntax |

## 📖 Documentation Structure

- **[Hooks](../hooks/)** - Event automation
- **[Agents](../agents/)** - AI assistants  
- **[Commands](../commands/)** - Workflows
- **[Statuslines](../statuslines/)** - Display customization
- **[Workflows](../workflows/)** - Complete processes