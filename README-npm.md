# Claude Config

> Comprehensive configuration manager for Claude Code - manage presets, hooks, agents, and commands

## Installation

```bash
npm install -g @grey-haven/claude-config
```

Or using yarn:
```bash
yarn global add @grey-haven/claude-config
```

Or using bun:
```bash
bun install -g @grey-haven/claude-config
```

## Quick Start

```bash
# Initialize Claude Code configuration in your project
cd your-project
claude-config init

# Apply a preset configuration
claude-config preset recommended

# List available resources
claude-config list-presets      # 23 presets
claude-config list-commands     # 22 commands  
claude-config list-agents       # 19 agents
claude-config list-statuslines  # 20 statuslines
```

## Features

- **23 Preset Configurations**: From minimal to complete setups
- **22 Slash Commands**: Pre-configured commands for various workflows
- **19 Specialized Agents**: AI agents for different tasks
- **20 Statusline Options**: Customizable status displays
- **Hook Management**: Add, remove, and list hooks easily
- **Multiple Config Locations**: Local, project, and user-wide settings

## Available Presets

### Core
- `minimal` - Essential hooks only
- `recommended` - Balanced setup ⭐
- `complete` - Everything available
- `full` - All features

### Language-Specific
- `python-focused` - Python development
- `python-data-science` - Jupyter, pandas, ML
- `javascript-focused` - JS/TS development
- `react` - React/Next.js
- `bun-optimized` - Bun runtime

### Workflow-Specific  
- `quality` - Code quality focus
- `security` - Security validation
- `tdd` - Test-driven development
- `performance` - Performance monitoring
- `linear-workflow` - Linear integration

## Commands

```bash
# Core Commands
claude-config init                    # Initialize configuration
claude-config preset <name>           # Apply a preset
claude-config statusline <name>       # Set up statusline

# List Resources
claude-config list-presets            # Show available presets
claude-config list-commands           # Show slash commands
claude-config list-agents             # Show available agents
claude-config list-statuslines        # Show statuslines

# Hook Management
claude-config hook-add <event> <cmd>  # Add a hook
claude-config hook-list               # List hooks
claude-config hook-remove <event> <cmd> # Remove a hook

# Utilities
claude-config validate                # Validate configs
claude-config doctor                  # Check dependencies
claude-config self-update             # Update the CLI
```

## Configuration Locations

- **Local**: `.claude/settings.local.json` (not committed to git)
- **Project**: `.claude/settings.json` (committed to git)
- **User**: `~/.claude/settings.json` (global for all projects)

Use the `--location` flag to specify where to apply configurations:

```bash
claude-config preset minimal --location user     # User-wide
claude-config preset full --location project     # Project (committed)
claude-config preset recommended --location local # Local (default)
```

## Examples

### Python Project Setup
```bash
cd my-python-project
claude-config init
claude-config preset python-focused
claude-config statusline minimal
```

### React Application
```bash
cd my-react-app
claude-config init  
claude-config preset react
claude-config statusline colorful
```

### Security-Focused Development
```bash
cd secure-project
claude-config init
claude-config preset security
```

## Requirements

- Node.js >= 14.0.0
- Python 3 (automatically detected)
- Git (for update features)

## Updates

Keep claude-config up to date:

```bash
# Using the built-in command
claude-config self-update

# Or using npm
npm update -g @grey-haven/claude-config
```

## Documentation

Full documentation available at: [GitHub Repository](https://github.com/grey-haven/grey-haven-claude-config)

## License

MIT © Grey Haven Studio