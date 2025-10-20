# @greyhaven/claude-code-config v2.0.0

> Hooks and configuration setup for Grey Haven's Claude Code environment

[![npm version](https://badge.fury.io/js/%40greyhaven%2Fclaude-code-config.svg)](https://www.npmjs.com/package/@greyhaven/claude-code-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What This Package Does

This npm package provides **setup utilities** for Claude Code:

- ✅ **Hooks installation** - 7 production hooks for enhanced Claude Code experience
- ✅ **MCP configuration** - Interactive setup wizard for MCP servers
- ✅ **Project initialization** - Templates and scaffolding for new projects
- ✅ **Settings management** - Backup/restore configuration files
- ✅ **Diagnostics** - Doctor command to troubleshoot issues

## 🚫 What This Package Does NOT Do

- ❌ **Plugin distribution** - Use Git repository + plugin marketplace instead
- ❌ **Agent management** - Agents are loaded from plugin marketplace
- ❌ **Command management** - Commands are loaded from plugin marketplace

**Why?** Claude Code's plugin marketplace loads plugins from local filesystem, making npm distribution redundant. See [Migration Guide](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md) for details.

---

## 📦 Installation

### Quick Install

```bash
npm install -g @greyhaven/claude-code-config
```

### From Source

```bash
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
cd grey-haven-claude-code-config
npm install -g .
```

---

## 🚀 Quick Start

### 1. Install Hooks

```bash
claude-config install-hooks
```

**What it does**:
- Copies 7 hooks to `~/.claude/hooks/`
- Sets executable permissions
- Validates Python 3 installation

**Available hooks**:
- `subagent-context-preparer.py` - Prepare context for subagents
- `bash-permission-validator.py` - Validate bash commands
- `edit-permission-validator.py` - Validate file edits
- `write-permission-validator.py` - Validate file writes
- `agent-output-formatter.py` - Format agent outputs
- `mcp-tool-permission-validator.py` - Validate MCP tool calls
- `user-prompt-submit.py` - Process user prompts

### 2. Configure MCP Servers (Optional)

```bash
claude-config setup-mcp
```

**Interactive wizard** that configures:
- Firecrawl MCP server
- Linear MCP server
- Playwright MCP server
- Custom MCP servers

### 3. Create New Project (Optional)

```bash
claude-config create-project my-app
```

**What it creates**:
- `.claude/` directory with settings
- `.github/workflows/` with CI/CD templates
- `vitest.config.ts` for testing
- Project README template

---

## 📚 Using Plugins (Agents & Commands)

Plugins are **NOT** distributed via npm. Use Git + plugin marketplace instead.

### Step 1: Clone Repository

```bash
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git ~/grey-haven-plugins
```

### Step 2: Configure Plugin Marketplace

**Edit `~/.claude/settings.json`** (or `~/.claude/settings.local.json`):

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/Users/YOU/grey-haven-plugins/grey-haven-plugins"
    }],
    "install": [
      "grey-haven-core@grey-haven-plugins",
      "grey-haven-developer-experience@grey-haven-plugins",
      "grey-haven-observability@grey-haven-plugins",
      "grey-haven-infrastructure@grey-haven-plugins",
      "grey-haven-quality-assurance@grey-haven-plugins",
      "grey-haven-security@grey-haven-plugins",
      "grey-haven-data-engineering@grey-haven-plugins",
      "grey-haven-ai-ml@grey-haven-plugins",
      "grey-haven-mobile-development@grey-haven-plugins",
      "grey-haven-cloudflare@grey-haven-plugins",
      "grey-haven-linear-integration@grey-haven-plugins",
      "grey-haven-hooks@grey-haven-plugins"
    ]
  }
}
```

**⚠️ Replace `/Users/YOU/grey-haven-plugins/grey-haven-plugins` with your absolute path!**

Find your path:
```bash
cd ~/grey-haven-plugins/grey-haven-plugins && pwd
```

### Step 3: Verify Installation

```bash
# Start Claude Code
claude

# Test commands
/tdd-implement
/code-review
/security-scan
/doc-generate-api

# All 30+ commands should work!
```

**See [MIGRATION_V2.md](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md) for detailed setup guide.**

---

## 🛠️ CLI Commands

### Hooks Management

```bash
# Install all hooks to ~/.claude/hooks/
claude-config install-hooks

# Install to custom directory
claude-config install-hooks --target /path/to/.claude/hooks

# List available hooks
claude-config list-hooks

# Enable specific hook
claude-config enable-hook bash-permission-validator

# Disable specific hook
claude-config disable-hook bash-permission-validator
```

### Configuration

```bash
# Initialize .claude/ directory in current project
claude-config init

# Configure MCP servers (interactive wizard)
claude-config setup-mcp

# Backup user settings
claude-config backup-settings

# Restore from backup
claude-config restore-settings
```

### Project Setup

```bash
# Create new project with templates
claude-config create-project my-app

# Add GitHub Actions workflows
claude-config add-github-actions

# Add Vitest configuration
claude-config setup-vitest
```

### Utility

```bash
# Update to latest version
claude-config self-update

# Diagnose installation issues
claude-config doctor

# Show version
claude-config --version

# Show help
claude-config --help
```

---

## 🔧 Configuration

### Hooks Configuration

**Edit `~/.claude/settings.json`**:

```json
{
  "hooks": {
    "bash-permission-validator": {
      "enabled": true,
      "auto_approve_safe_commands": true,
      "blocked_commands": ["rm -rf /", ":(){ :|:& };:"]
    },
    "edit-permission-validator": {
      "enabled": true,
      "require_approval_for_large_files": true,
      "max_auto_approve_size_kb": 500
    },
    "write-permission-validator": {
      "enabled": true,
      "auto_approve_new_files": false,
      "protected_patterns": ["package.json", "*.env"]
    }
  }
}
```

### MCP Configuration

**Edit `~/.claude/settings.json`**:

```json
{
  "mcp": {
    "servers": {
      "firecrawl-mcp": {
        "command": "npx",
        "args": ["-y", "firecrawl-mcp"],
        "env": {
          "FIRECRAWL_API_KEY": "your-api-key"
        }
      },
      "linear": {
        "command": "npx",
        "args": ["-y", "@linear/mcp-server"],
        "env": {
          "LINEAR_API_KEY": "your-linear-key"
        }
      }
    },
    "auto_approve_tools": {
      "firecrawl_scrape": {
        "allowed_tools": ["mcp__firecrawl-mcp__firecrawl_scrape"]
      }
    }
  }
}
```

---

## 📖 Documentation

### Core Documentation

- **[Migration Guide](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md)** - Upgrade from v1.x to v2.0.0
- **[Architecture Plan](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/.claude/V2_ARCHITECTURE_PLAN.md)** - v2.0.0 design decisions
- **[Hooks Guide](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/.claude/hooks/README.md)** - Hook documentation
- **[Plugin Development](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/PLUGIN_DEVELOPMENT.md)** - Create custom plugins

### Available Plugins

**12 plugin categories, 26+ agents, 30+ commands**:

| Plugin | Agents | Commands | Description |
|--------|--------|----------|-------------|
| `grey-haven-core` | 3 | 5 | Core functionality (research, context, git) |
| `grey-haven-developer-experience` | 5 | 8 | DX tools (TDD, code review, docs) |
| `grey-haven-observability` | 2 | 3 | Monitoring, logging, metrics |
| `grey-haven-infrastructure` | 3 | 4 | IaC, deployment, scaling |
| `grey-haven-quality-assurance` | 2 | 3 | Testing, E2E, visual regression |
| `grey-haven-security` | 2 | 2 | Security scanning, vulnerability analysis |
| `grey-haven-data-engineering` | 2 | 2 | ETL, data pipelines, analytics |
| `grey-haven-ai-ml` | 2 | 1 | AI/ML workflows, model training |
| `grey-haven-mobile-development` | 2 | 1 | Mobile app development |
| `grey-haven-cloudflare` | 1 | 1 | Cloudflare Workers/Pages deployment |
| `grey-haven-linear-integration` | 1 | 1 | Linear project management |
| `grey-haven-hooks` | 0 | 0 | Hook documentation |

**See repository for full plugin documentation.**

---

## 🔄 Updating

### Update npm Package

```bash
# Update CLI tools (hooks, setup utilities)
npm update -g @greyhaven/claude-code-config

# Or use self-update command
claude-config self-update
```

### Update Plugins

```bash
# Update plugins (agents, commands)
cd ~/grey-haven-plugins
git pull origin main
```

**Best practice**: Update both weekly.

---

## 🐛 Troubleshooting

### Run Diagnostics

```bash
claude-config doctor
```

**Checks**:
- ✅ Python 3 installation
- ✅ Node.js installation
- ✅ Hooks installed and executable
- ✅ Settings.json valid
- ✅ Plugin marketplace configured
- ✅ MCP servers configured

### Common Issues

#### "Command not found: claude-config"

```bash
# Check npm global bin directory is in PATH
npm config get prefix

# Add to PATH (macOS/Linux)
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Reinstall
npm uninstall -g @greyhaven/claude-code-config
npm install -g @greyhaven/claude-code-config
```

#### "Python 3 is required"

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Verify
python3 --version
```

#### "Hooks not working"

```bash
# Check hooks exist
ls ~/.claude/hooks/

# Make executable (macOS/Linux)
chmod +x ~/.claude/hooks/*.py

# Verify Python can run them
python3 ~/.claude/hooks/bash-permission-validator.py
```

#### "Plugins not loading"

```bash
# Verify absolute path in settings.json
cat ~/.claude/settings.json | grep -A5 plugin

# Check directory exists
ls /Users/YOU/grey-haven-plugins/grey-haven-plugins/

# Restart Claude Code
```

---

## 🆚 v1.x vs v2.0.0

| Feature | v1.x | v2.0.0 |
|---------|------|--------|
| **Plugin distribution** | ✅ npm package | ❌ Git repository |
| **Hooks** | ✅ npm package | ✅ npm package |
| **MCP setup** | ❌ Manual | ✅ CLI wizard |
| **Project templates** | ❌ None | ✅ CLI scaffolding |
| **Package size** | ~2 MB | ~500 KB |
| **Update method** | `npm update` | `git pull` + `npm update` |
| **Maintenance** | ❌ High overhead | ✅ Low overhead |

**Why the change?** See [V2_ARCHITECTURE_PLAN.md](.claude/V2_ARCHITECTURE_PLAN.md).

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

### Development Setup

```bash
# Clone repository
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
cd grey-haven-claude-code-config

# Install development dependencies
npm install

# Run tests
npm test

# Lint
npm run lint
```

### Creating Plugins

See [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md) for guide on creating custom plugins.

---

## 📝 License

MIT © Grey Haven Studio

---

## 🔗 Links

- **GitHub**: https://github.com/greyhaven-ai/grey-haven-claude-code-config
- **npm**: https://www.npmjs.com/package/@greyhaven/claude-code-config
- **Issues**: https://github.com/greyhaven-ai/grey-haven-claude-code-config/issues
- **Discussions**: https://github.com/greyhaven-ai/grey-haven-claude-code-config/discussions

---

## ❓ FAQ

### Do I need this package?

**Maybe!** You need it if you want:
- ✅ Automated hook installation (`claude-config install-hooks`)
- ✅ MCP setup wizard (`claude-config setup-mcp`)
- ✅ Project scaffolding (`claude-config create-project`)
- ✅ Diagnostics (`claude-config doctor`)

**You DON'T need it if**:
- You only want plugins (use Git repository directly)
- You're comfortable manually copying hooks
- You don't need CLI utilities

### Can I use plugins without this package?

**Yes!** This package is **optional** for plugins.

**Required for plugins**:
1. Clone Git repository ✅
2. Configure plugin marketplace in settings.json ✅

**Optional**:
3. Install this npm package for CLI utilities ⚠️

### What happened to presets?

Presets are in the **Git repository**, not npm package.

**Location**: `grey-haven-plugins/.claude/presets/`

**Apply manually**:
```bash
cp ~/grey-haven-plugins/.claude/presets/recommended.json ./.claude/settings.json
```

### How do I migrate from v1.x?

See [MIGRATION_V2.md](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md) for complete guide.

**TL;DR**:
1. Clone Git repository
2. Configure plugin marketplace in settings.json
3. (Optional) Install v2.0.0 npm package for CLI utilities
4. Uninstall v1.x npm package

---

**Version**: 2.0.0
**Last Updated**: 2025-10-17
**Maintainer**: Grey Haven Studio
