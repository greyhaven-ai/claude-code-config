# Claude Config - Installation Guide

## Overview

Claude Config is a comprehensive configuration management tool for Claude Code. This guide covers multiple installation methods to suit your preferences.

## Quick Install

### NPM (Recommended - Easiest)
```bash
npm install -g @grey-haven/claude-config
```

### Yarn
```bash
yarn global add @grey-haven/claude-config
```

### Bun
```bash
bun install -g @grey-haven/claude-config
```

### Homebrew (macOS/Linux)
```bash
# Add the tap (first time only)
brew tap grey-haven/tools

# Install claude-config
brew install claude-config
```

## Installation Methods

### Method 1: NPM Package (Recommended - Cross-platform)

The npm package is the easiest way to install and includes automatic updates:

```bash
# Install globally
npm install -g @grey-haven/claude-config

# Verify installation
claude-config --help

# Update to latest version
claude-config self-update
# or
npm update -g @grey-haven/claude-config
```

**Advantages:**
- Single command installation
- Automatic dependency management
- Easy updates
- Cross-platform support
- No manual PATH configuration

### Method 2: Homebrew (macOS/Linux)

For Homebrew users:

```bash
# Add our tap
brew tap grey-haven/tools

# Install
brew install claude-config

# Update
brew upgrade claude-config
```

**Advantages:**
- Integrates with Homebrew ecosystem
- Manages Python dependency automatically
- Easy uninstall with `brew uninstall claude-config`

### Method 3: Script Installation

```bash
# Clone the repository
git clone https://github.com/grey-haven/grey-haven-claude-config.git
cd grey-haven-claude-config

# Run the installation script
./install.sh
```

The installation script will:
- Clone/update the repository to `~/.claude-config`
- Create a wrapper script in `~/.local/bin/claude-config`
- Add `~/.local/bin` to your PATH if needed
- Set up update commands

### Method 2: Manual Installation

1. **Clone the repository**
```bash
git clone https://github.com/grey-haven/grey-haven-claude-config.git ~/.claude-config
```

2. **Create wrapper script**
```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/claude-config << 'EOF'
#!/bin/bash
export CLAUDE_CONFIG_GLOBAL=1
export CLAUDE_CONFIG_HOME="$HOME/.claude-config"
exec python3 "$CLAUDE_CONFIG_HOME/claude-config" "$@"
EOF
chmod +x ~/.local/bin/claude-config
```

3. **Add to PATH**
Add this to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export PATH="$PATH:$HOME/.local/bin"
```

4. **Reload shell configuration**
```bash
source ~/.bashrc  # or ~/.zshrc
```

## Usage

Once installed globally, you can use `claude-config` from any directory:

### Basic Commands

```bash
# Initialize Claude Code configuration in current project
claude-config init

# Apply a preset configuration
claude-config preset recommended
claude-config preset python-focused
claude-config preset security

# List available resources
claude-config list-presets      # Show 23 available presets
claude-config list-commands     # Show 22 slash commands
claude-config list-agents       # Show 19 agents
claude-config list-statuslines  # Show 20 statuslines

# Set up a statusline
claude-config statusline minimal
claude-config statusline grey-haven-default

# Manage hooks
claude-config hook-add PreToolUse "echo 'Starting tool'" --matcher "Edit|Write"
claude-config hook-list
claude-config hook-remove PreToolUse "echo 'Starting tool'"
```

### Configuration Locations

The `--location` flag controls where configurations are applied:

```bash
# Local project configuration (default)
claude-config preset recommended --location local

# User-wide configuration
claude-config preset minimal --location user

# Project configuration (committed to git)
claude-config preset complete --location project
```

Configuration files:
- **Local**: `.claude/settings.local.json` (project-specific, not committed)
- **Project**: `.claude/settings.json` (project-specific, committed)
- **User**: `~/.claude/settings.json` (applies to all projects)

### Keeping Updated

```bash
# Update claude-config from repository
claude-config update

# Sync local changes with repository (requires write access)
claude-config sync

# Or manually update
cd ~/.claude-config
git pull origin main
```

## Available Presets

### Core Presets
- `minimal` - Essential hooks only
- `recommended` - Balanced setup ⭐
- `complete` - Everything available
- `full` - All features enabled

### Language-Specific
- `python-focused` - Python development
- `python-data-science` - Jupyter, pandas, ML
- `javascript-focused` - JS/TS development
- `bun-optimized` - Bun runtime
- `react` - React/Next.js

### Workflow-Specific
- `quality` - Code quality focus
- `security` - Security validation
- `tdd` - Test-driven development
- `testing-focus` - Test generation
- `performance` - Performance monitoring

### Specialized
- `documentation` - Auto-documentation
- `migration` - Legacy code updates
- `linear-workflow` - Linear integration
- `api-backend` - API development
- `integrated-workflow` - Advanced orchestration
- `mcp-integration` - MCP server commands
- `subagent-orchestration` - Multi-agent workflows
- `code-quality` - Quality-focused hooks

## Quick Start Examples

### For a New Python Project
```bash
cd my-python-project
claude-config init
claude-config preset python-focused
claude-config statusline minimal
```

### For React Development
```bash
cd my-react-app
claude-config init
claude-config preset react
claude-config statusline colorful
```

### For Security-Focused Development
```bash
cd secure-project
claude-config init
claude-config preset security
claude-config hook-add PreToolUse "$CLAUDE_PROJECT_DIR/.claude/hooks/python/security-validator.py"
```

## Troubleshooting

### Command not found
If `claude-config` is not found after installation:
1. Restart your terminal
2. Or manually source your shell config: `source ~/.bashrc`
3. Check if `~/.local/bin` is in your PATH: `echo $PATH`

### Permission denied
Make sure the scripts are executable:
```bash
chmod +x ~/.claude-config/claude-config
chmod +x ~/.local/bin/claude-config
```

### Python not found
Claude Config requires Python 3. Install it with:
- macOS: `brew install python3`
- Ubuntu/Debian: `sudo apt install python3`
- Other: Check your package manager

### Git not found
Git is required for updates. Install it with:
- macOS: `brew install git`
- Ubuntu/Debian: `sudo apt install git`
- Other: Check your package manager

## Advanced Usage

### Custom Statuslines
```bash
# Create custom statusline
cat > ~/.claude/statuslines/custom.sh << 'EOF'
#!/bin/bash
input=$(cat)
echo "🚀 $(echo "$input" | jq -r '.model.display_name') | $(date +%H:%M)"
EOF
chmod +x ~/.claude/statuslines/custom.sh

# Use it
claude-config statusline custom
```

### Combining Presets
You can apply multiple presets in sequence:
```bash
claude-config preset minimal
claude-config preset security
claude-config preset linear-workflow
```

### Project Templates
Create a template configuration and reuse it:
```bash
# Save current config as template
cp .claude/settings.json ~/my-template.json

# Apply template to new project
cd new-project
claude-config import ~/my-template.json
```

## Contributing

To contribute new presets, agents, or commands:

1. Fork the repository
2. Add your configurations to the appropriate catalog
3. Test thoroughly
4. Submit a pull request

## Support

- Documentation: `/docs/cli/`
- Issues: [GitHub Issues](https://github.com/grey-haven/grey-haven-claude-config/issues)
- Updates: Run `claude-config update` regularly

## License

MIT License - Copyright (c) 2025 Grey Haven Studio