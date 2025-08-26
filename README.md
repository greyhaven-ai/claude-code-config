# Claude Config - Comprehensive Configuration Manager for Claude Code

A powerful CLI tool and configuration framework that enhances Claude Code with hooks, agents, slash commands, presets, and statuslines. Manage and deploy complete Claude Code configurations with a single command.

## 🌟 Features

- **🎨 20+ Presets** - Pre-configured setups for different workflows (TDD, API development, security, etc.)
- **🤖 19 Specialized Agents** - AI assistants for code quality, documentation, security, and more
- **⚡ 23 Slash Commands** - Custom commands for complex workflows
- **🪝 36 Hook Scripts** - Automated code analysis, testing, and validation
- **📊 10 Statuslines** - Fun and informative status indicators
- **🔧 CLI Tool** - Manage everything from the command line

## 📦 Installation

### Homebrew (Recommended)
```bash
brew tap greyhaven-ai/greyhaven
brew install claude-config
```

### npm
```bash
npm install -g @greyhaven/claude-code-config
```

### From Source
```bash
git clone https://github.com/greyhaven-ai/claude-code-config.git
cd claude-code-config
./claude-config wizard  # Interactive setup
```

## 🚀 Quick Start

### Interactive Setup (Easiest)
```bash
claude-config wizard
```

### Apply a Preset
```bash
# View available presets
claude-config list-presets

# Apply a preset
claude-config preset recommended     # Balanced setup for most projects
claude-config preset full           # Everything included
claude-config preset minimal        # Lightweight setup
claude-config preset tdd           # Test-driven development
claude-config preset api-backend   # API development focus
```

### Initialize in Current Directory
```bash
claude-config init
```

## 🎯 Key Commands

### Resource Management
```bash
# Add individual components
claude-config add-agent security-analyzer
claude-config add-command security/security-audit
claude-config add-hook python/api-contract-validator.py

# Install all resources
claude-config install-all-agents
claude-config install-all-commands
claude-config install-hooks

# List available resources
claude-config list-agents
claude-config list-commands
claude-config list-statuslines
claude-config list-presets
```

### Configuration Management
```bash
# Hook management
claude-config hook-add PreToolUse "echo 'Running pre-tool hook'" --matcher "Edit"
claude-config hook-list
claude-config hook-remove PreToolUse "echo 'Running pre-tool hook'"

# Statusline setup
claude-config statusline tamagotchi    # Fun pet in your status bar
claude-config statusline minimal       # Clean and simple

# Validation and troubleshooting
claude-config validate                 # Check configuration
claude-config doctor                   # Check system dependencies
```

## 📚 What's Included

### 🤖 Agents
Specialized AI assistants that extend Claude Code's capabilities:

- **Code Quality**: `code-clarity-refactorer`, `code-quality-analyzer`
- **Security**: `security-analyzer`, `security-orchestrator`
- **Testing**: `tdd-python`, `tdd-typescript`, `test-generator`
- **Documentation**: `tech-docs-maintainer`, `git-diff-documenter`
- **Performance**: `performance-optimizer`, `memory-profiler`
- **And more...**

### ⚡ Slash Commands
Custom commands for complex workflows:

- `/security-audit` - Comprehensive security analysis
- `/tdd-implement` - Test-driven implementation
- `/performance-optimize-chain` - Performance optimization workflow
- `/quality-pipeline` - Full quality check pipeline
- **And 19 more commands...**

### 🪝 Hooks
Automated scripts that run at key moments:

**Pre/Post Tool Use Hooks**:
- API contract validation
- Database query analysis
- Dependency impact analysis
- Security validation
- Code formatting and linting

**User Prompt Hooks**:
- Context injection
- Prompt enhancement
- Documentation fetching

### 🎨 Presets

Pre-configured combinations of agents, commands, and hooks:

| Preset | Description | Best For |
|--------|-------------|----------|
| `recommended` | Balanced setup with essential tools | Most projects |
| `full` | Complete setup with all features | Power users |
| `minimal` | Lightweight with core features | Simple projects |
| `tdd` | Test-driven development focus | TDD practitioners |
| `api-backend` | API development tools | Backend services |
| `react` | React/frontend optimized | React applications |
| `python-focused` | Python development tools | Python projects |
| `security` | Security-first configuration | Security-critical apps |

## 📁 Project Structure

```
claude-code-config/
├── .claude/                    # Claude Code configurations
│   ├── agents/                # Agent definitions
│   ├── commands/              # Slash command definitions
│   ├── hooks/                 # Hook implementations
│   │   ├── python/           # Python hooks (23 scripts)
│   │   ├── js/               # JavaScript hooks (8 scripts)
│   │   └── bash/             # Bash hooks (5 scripts)
│   └── project/              # Project-specific configs
├── setup-claude-code/         # Configuration assets
│   ├── presets/              # Preset definitions
│   ├── agents/               # Agent catalog
│   ├── commands/             # Command catalog
│   └── statuslines/          # Statusline definitions
├── claude-config             # Main CLI script
└── docs/                     # Documentation
```

## 🔧 Advanced Usage

### Merge with Existing Configuration
```bash
# Merge without overwriting existing files
claude-config init --merge

# Force overwrite
claude-config init --force
```

### Custom Configurations
```bash
# Import custom configuration
claude-config import ./my-config.json

# Add custom hooks
claude-config hook-add PreToolUse "/path/to/custom-hook.sh" \
  --matcher "Edit|Write" \
  --timeout 10
```

### Global vs Local Installation
```bash
# User-level configuration (applies to all projects)
claude-config preset recommended --user

# Project-level configuration (current directory)
claude-config preset recommended --local
```

## 📋 System Requirements

### Required
- Python 3.8+ or UV
- Git
- Ripgrep (rg)

### Optional but Recommended
- jq (JSON processing)
- Node.js/Bun (for JavaScript hooks)
- GitHub CLI (for issue creation)

### Check Dependencies
```bash
claude-config doctor
```

## 🔗 Links

- **Claude Code Documentation**: [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- **GitHub Repository**: [https://github.com/greyhaven-ai/claude-code-config](https://github.com/greyhaven-ai/claude-code-config)
- **npm Package**: [https://www.npmjs.com/package/@greyhaven/claude-code-config](https://www.npmjs.com/package/@greyhaven/claude-code-config)
- **Issue Tracker**: [https://github.com/greyhaven-ai/claude-code-config/issues](https://github.com/greyhaven-ai/claude-code-config/issues)

## 🎉 Acknowledgments

This project was inspired by and builds upon the excellent work from:
- [I Love Claude Code](https://github.com/alchemiststudiosDOTai/i-love-claude-code) by Alchemist Studios

Special thanks to the Claude Code community for their contributions and feedback.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## 📄 License

MIT License - Copyright (c) 2025 Grey Haven Studio

See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the Claude Code community**