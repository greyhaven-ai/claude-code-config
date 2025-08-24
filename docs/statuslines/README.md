# Statuslines Documentation

Custom statusline configurations for Claude Code that provide real-time information and engagement.

## 📚 Available Statuslines

### Built-in Configurations
- **[Complete Guide](./complete-guide.md)** - Comprehensive statusline documentation
- **Grey Haven Default** - Git integration, cost tracking, comprehensive info
- **Tamagotchi** - Virtual pet that evolves with your coding!
- **Productivity Dashboard** - Metrics and efficiency tracking
- **Minimalist** - Just the essentials
- **Context Aware** - Adapts to current activity

## 🚀 Quick Setup

```bash
# Copy statusline scripts
cp -r .claude/statuslines ~/.claude/

# Make executable
chmod +x ~/.claude/statuslines/*.sh

# Configure in settings.json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statuslines/grey-haven-default.sh",
    "padding": 0
  }
}
```

## 📊 Available Data

Statuslines receive JSON with:
- Model information
- Workspace/directory context
- Cost and usage metrics
- Session information
- Git status (if available)

## 🎨 Creating Custom Statuslines

1. Create script in `~/.claude/statuslines/`
2. Read JSON from stdin
3. Process with `jq`
4. Output formatted text
5. Keep execution under 300ms

See [Complete Guide](./complete-guide.md) for detailed instructions.