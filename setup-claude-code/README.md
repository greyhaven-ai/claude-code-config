# Setup Claude Code Directory

This directory contains the configuration system for Claude Code.

## Structure

```
setup-claude-code/
├── presets/              # 23 preset configurations
│   └── *.json           # Ready-to-use configuration templates
├── statuslines/          # Statusline configurations
│   └── statusline-catalog.json  # 20 statusline options
├── commands/             # Slash command definitions
│   └── commands-catalog.json    # 22 slash commands
└── agents/               # Agent definitions
    └── agents-catalog.json      # 19 specialized agents
```

## Using the CLI

All functionality is now accessible through the `claude-config` CLI:

### Basic Commands

```bash
# Initialize configuration
claude-config init

# Apply a preset (23 available)
claude-config preset recommended
claude-config list-presets

# Set up a statusline (20 available)
claude-config statusline grey-haven-default
claude-config list-statuslines

# View available commands and agents
claude-config list-commands
claude-config list-agents
```

### Hook Management

```bash
# Add a single hook
claude-config hook-add PostToolUse "echo 'Done'" --matcher "Edit|Write" --timeout 10

# Remove a hook
claude-config hook-remove PostToolUse "echo 'Done'"

# List all hooks
claude-config hook-list
```

### Configuration Locations

All commands support `--location` flag:
- `local` - `.claude/settings.local.json` (default, not committed)
- `project` - `.claude/settings.json` (version controlled)
- `user` - `~/.claude/settings.json` (user-wide)

## Available Presets (23)

### Core
- `minimal` - Essential hooks only
- `recommended` - Balanced setup ⭐
- `complete` - Everything available
- `full` - All features

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

## Available Statuslines (20)

### Categories
- **Simple**: minimal, git-aware, compact
- **Comprehensive**: grey-haven-default, productivity-dashboard, context-aware
- **Fun**: tamagotchi, emoji-status, time-based
- **Technical**: performance, productivity-metrics, progress-bar
- **Visual**: colorful, model-colors
- **Git-focused**: git-dirty, development
- **Branded**: grey-haven-branded, bun-development

## Quick Start

```bash
# For most users
claude-config preset recommended
claude-config statusline minimal

# For Python developers
claude-config preset python-focused
claude-config statusline development

# For teams
claude-config preset complete --location project
claude-config statusline grey-haven-default --location project

# Check everything is working
claude-config validate
claude-config doctor
```

## Help

```bash
# General help
claude-config --help

# Command-specific help
claude-config preset --help
claude-config hook-add --help
```