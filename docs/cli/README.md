# Claude Config CLI Documentation

`claude-config` is a comprehensive command-line tool for managing Claude Code configurations, hooks, agents, and statuslines.

## Installation

```bash
# Clone the repository
git clone https://github.com/greyhaven-ai/claude-code-config.git

# Make CLI executable
chmod +x claude-code-config/claude-config

# Add to PATH (optional)
ln -s $(pwd)/claude-code-config/claude-config /usr/local/bin/claude-config
```

## Quick Start

```bash
# Initialize Claude configuration in current project
claude-config init

# Apply a preset configuration
claude-config preset quality

# Check system dependencies
claude-config doctor

# Set up a fun statusline
claude-config statusline tamagotchi
```

## Commands

### `init` - Initialize Configuration

Initialize Claude Code configuration in a project directory.

```bash
claude-config init [path]
```

**Options:**
- `path` - Target directory (default: current directory)

**Creates:**
- `.claude/` directory structure
- Basic `settings.json`
- `CLAUDE.md` template

### `preset` - Apply Preset Configuration

Apply a pre-defined configuration preset.

```bash
claude-config preset <name> [--location {local|project|user}]
```

**23 Available Presets** including:
- `minimal` - Essential hooks and basic statusline
- `recommended` - Grey Haven's recommended balanced setup
- `complete` - Every available hook, agent, and command
- `quality` - Testing, linting, and code quality
- `security` - Security validation and scanning
- `tdd` - Test-driven development workflow
- `python-focused` - Optimized for Python projects
- `javascript-focused` - Optimized for JS/TS projects
- See full list: `claude-config list-presets`

**Options:**
- `--location` - Where to apply preset (default: local)
  - `local` - `.claude/settings.local.json` (not committed)
  - `project` - `.claude/settings.json` (version controlled)
  - `user` - `~/.claude/settings.json` (user-wide)

### `list-presets` - List Available Presets

Display all available preset configurations.

```bash
claude-config list-presets
```

### `import` - Import Configuration

Import an existing configuration file.

```bash
claude-config import <path> [--location {local|project|user}]
```

**Options:**
- `path` - Path to configuration JSON file
- `--location` - Where to import (default: local)

### `validate` - Validate Configuration

Check configuration files for errors.

```bash
claude-config validate [--location {all|local|project|user}]
```

**Options:**
- `--location` - Which configs to validate (default: all)

**Validates:**
- JSON syntax
- Hook event names
- Configuration structure
- Required fields

### `install-hooks` - Install Hook Scripts

Copy hook scripts to project directory.

```bash
claude-config install-hooks [path]
```

**Options:**
- `path` - Target directory (default: current)

**Installs:**
- Python hooks
- Bash hooks
- JavaScript hooks

### `statusline` - Set Up Statusline

Configure a specific statusline.

```bash
claude-config statusline <name> [--location {local|project|user}]
```

**20 Available Statuslines** including:
- `grey-haven-default` - Comprehensive info with git
- `tamagotchi` - Virtual pet that evolves
- `productivity-dashboard` - Metrics and efficiency
- `minimal` - Just essentials
- `context-aware` - Adapts to activity
- `git-aware` - Shows git branch and status
- `cost-tracker` - Tracks session costs
- See full list: `claude-config list-statuslines`

### `list-statuslines` - List Available Statuslines

Display all available statusline configurations by category.

```bash
claude-config list-statuslines
```

### `doctor` - System Check

Check system for required dependencies.

```bash
claude-config doctor
```

**Checks:**
- Required: `git`, `ripgrep`
- Recommended: `jq`, `python3`
- Optional: `node`, `bun`, `uv`
- Claude Code directory

## Preset Details

### Minimal Preset

```json
{
  "hooks": {
    "SessionStart": [...],
    "PostToolUse": [...]
  },
  "statusLine": {
    "type": "command",
    "command": "minimal statusline"
  }
}
```

**Use when:** You want lightweight setup with essential features.

### Quality Preset

```json
{
  "hooks": {
    "PreToolUse": ["validation"],
    "PostToolUse": ["formatting", "testing"],
    "Stop": ["verify tests pass"]
  }
}
```

**Use when:** Code quality is a priority.

### Security Preset

```json
{
  "hooks": {
    "PreToolUse": ["security validation"],
    "PostToolUse": ["secret scanning"],
    "SessionStart": ["load policies"]
  }
}
```

**Use when:** Working with sensitive code or data.

### TDD Preset

```json
{
  "hooks": {
    "PreToolUse": ["ensure tests exist"],
    "PostToolUse": ["run tests", "coverage"],
    "Stop": ["enforce test pass"]
  }
}
```

**Use when:** Following test-driven development.

### Full Preset

Includes all available hooks, comprehensive monitoring, and advanced features.

**Use when:** You want maximum automation and assistance.

## Configuration Hierarchy

Claude Code checks settings in this order:

1. `~/.claude/settings.json` - User-wide settings
2. `.claude/settings.json` - Project settings (version controlled)
3. `.claude/settings.local.json` - Local overrides (not committed)

Settings are merged, with local overrides taking precedence.

## Examples

### Setting Up a New Project

```bash
# Initialize configuration
claude-config init

# Apply quality preset
claude-config preset quality

# Set up fun statusline
claude-config statusline tamagotchi

# Validate everything works
claude-config validate
```

### Importing Team Configuration

```bash
# Import shared team config
claude-config import team-config.json --location project

# Install necessary hooks
claude-config install-hooks

# Validate
claude-config validate
```

### Security-First Setup

```bash
# Apply security preset
claude-config preset security --location project

# Add custom security hooks
claude-config import custom-security.json

# Verify setup
claude-config validate
```

## Troubleshooting

### Command not found

```bash
# Make executable
chmod +x claude-config

# Add to PATH
export PATH="$PATH:/path/to/claude-code-config"
```

### Missing dependencies

```bash
# Check what's missing
claude-config doctor

# Install required tools
brew install ripgrep jq  # macOS
apt-get install ripgrep jq  # Linux
```

### Configuration not loading

```bash
# Validate configuration
claude-config validate

# Check file locations
ls -la .claude/
ls -la ~/.claude/
```

### Hooks not executing

```bash
# Check permissions
chmod +x .claude/hooks/**/*.{py,sh,js}

# Validate configuration
claude-config validate --location all
```

## Advanced Usage

### Creating Custom Presets

1. Create preset file in `setup-claude-code/presets/`:

```json
{
  "name": "My Custom Preset",
  "description": "Description here",
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  },
  "statusLine": {...}
}
```

2. Apply preset:

```bash
claude-config preset my-custom
```

### Combining Presets

```bash
# Start with quality
claude-config preset quality

# Layer on security
claude-config import security-additions.json

# Add custom statusline
claude-config statusline productivity-dashboard
```

### Environment-Specific Configuration

```bash
# Development
claude-config preset tdd --location local

# Production
claude-config preset security --location local

# CI/CD
claude-config preset minimal --location local
```

## Best Practices

1. **Start Simple**: Begin with minimal preset, add features as needed
2. **Version Control**: Commit `.claude/settings.json`, ignore `.claude/settings.local.json`
3. **Team Consistency**: Share project settings, allow local overrides
4. **Regular Validation**: Run `claude-config validate` after changes
5. **Documentation**: Update `CLAUDE.md` with project-specific context

## Contributing

To add new presets or features:

1. Create preset in `setup-claude-code/presets/`
2. Test with `claude-config preset <name>`
3. Document in this file
4. Submit pull request

## Support

- Check `claude-config doctor` for system issues
- Run `claude-config validate` for configuration problems
- See [Troubleshooting Guide](../troubleshooting.md) for common issues
- Open issue on GitHub for bugs or features