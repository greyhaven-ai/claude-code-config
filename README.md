# Grey Haven Claude Code Configuration

**Version 2.1.0** - Hooks, Skills, configuration, and plugin marketplace for Claude Code

[![npm version](https://badge.fury.io/js/%40greyhaven%2Fclaude-code-config.svg)](https://www.npmjs.com/package/@greyhaven/claude-code-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What This Repository Provides

This repository contains Grey Haven Studio's comprehensive Claude Code ecosystem:

**12 Plugin Packages** with **26+ Agents** and **30+ Commands**

- Distributed via local plugin marketplace (not npm)
- Clone this repository and configure in Claude Code settings

**3 Claude Skills** for automatic code assistance

- Code style enforcement (TypeScript, React, Python)
- Commit message formatting (Conventional Commits)
- Pull request template generation

**npm Package** (`@greyhaven/claude-code-config`) for:

- ✅ Hook installation and management
- ✅ Skills installation and management
- ✅ MCP server configuration
- ✅ Project initialization
- ✅ Settings backup/restore
- ✅ Diagnostics

---

## 📦 Installation

### Option 1: Full Setup (Recommended)

**Get plugins + CLI tools**:

```bash
# 1. Clone repository for plugins
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git ~/grey-haven-plugins

# 2. Configure plugin marketplace in ~/.claude/settings.json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/Users/YOU/grey-haven-plugins/grey-haven-plugins"
    }],
    "install": [
      "core@grey-haven-plugins",
      "developer-experience@grey-haven-plugins",
      "observability@grey-haven-plugins",
      "cc-trace@grey-haven-plugins"
    ]
  }
}

# 3. (Optional) Install CLI tools for hook management
npm install -g @greyhaven/claude-code-config
claude-config install-hooks
```

### Option 2: Plugins Only

**If you only need agents and commands**:

```bash
# Clone and configure plugin marketplace
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git ~/grey-haven-plugins

# Add to ~/.claude/settings.json (see full config above)
```

No npm package required!

### Option 3: CLI Tools Only

**If you only need hook installation and setup utilities**:

```bash
npm install -g @greyhaven/claude-code-config
```

---

## 🚀 Quick Start

### 1. Install Hooks and Skills

```bash
claude-config install-hooks
claude-config install-skills
```

### 2. Test Installation

```bash
claude-config doctor
```

### 3. Use Skills and Plugins

Skills work automatically - just code naturally:

```
"Write a React component"     → grey-haven-code-style applies
"Create a commit message"     → grey-haven-commit-format applies
"Generate a PR description"   → grey-haven-pr-template applies
```

Use plugins via commands:

In Claude Code:
```bash
/tdd-implement          # Test-driven development
/code-review            # Code review analysis
/security-scan          # Security audit
/doc-generate-api       # API documentation
```

---

## 📦 Available Plugins

| Plugin | Description |
|--------|-------------|
| `core` | TDD implementation, code review, quality pipeline, debugging |
| `developer-experience` | Documentation, onboarding, API design, code style |
| `testing` | Playwright, Chrome E2E, visual regression testing |
| `deployment` | Cloudflare Workers/Pages deployment and debugging |
| `security` | OWASP security scanning, vulnerability analysis |
| `research` | API research with Firecrawl, Context7, TanStack patterns |
| `observability` | Monitoring, SLOs, metrics, performance tracking |
| `incident-response` | Debugging, runbooks, postmortem generation |
| `agent-orchestration` | Context management, workflow composition |
| `data-quality` | Pydantic validation, schema contracts, data quality |
| `linear` | Linear issue tracking, workflow integration |
| `cc-trace` | Claude Code API debugging with mitmproxy |
| `cloudflare-deployment-observability` | Deployment monitoring, CI/CD analytics |
| `knowledge-base` | Ontological knowledge management, long-term memory |
| `creative-writing` | 8 specialized agents for the complete writing process |

**Total**: 30+ agents, 40+ skills across 15 plugins

**Install format**: `plugin-name@grey-haven-plugins` (e.g., `core@grey-haven-plugins`)

---

## 🔧 CLI Commands

### Hooks Management

```bash
claude-config install-hooks         # Install hooks to ~/.claude/hooks/
claude-config list-hooks            # Show available hooks
```

### Configuration

```bash
claude-config init                  # Initialize .claude/ directory
claude-config backup-settings       # Backup user settings
claude-config restore-settings      # Restore from backup
```

### Diagnostics

```bash
claude-config doctor                # Diagnose installation
claude-config version               # Show version
```

---

## 📚 Documentation

- **[Migration Guide](MIGRATION_V2.md)** - Upgrade from v1.x to v2.0.0
- **[npm Package README](README-npm.md)** - CLI tool documentation
- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Architecture Plan](.claude/V2_ARCHITECTURE_PLAN.md)** - v2.0.0 design decisions

---

## 🔄 Updating

### Update Plugins

```bash
cd ~/grey-haven-plugins
git pull origin main
```

### Update CLI Tools

```bash
npm update -g @greyhaven/claude-code-config
# Or: claude-config self-update
```

---

## 🎯 Key Features

### 26+ Specialized Agents

**Core Functionality**:
- `docs-architect` - Technical documentation creation
- `code-quality-analyzer` - Multi-mode code analysis
- `tdd-python-implementer` - Test-driven Python development
- `tdd-typescript-implementer` - Test-driven TypeScript development

**Observability**:
- `observability-architect` - Monitoring setup
- `sli-slo-engineer` - SLI/SLO implementation

**Security**:
- `security-analyzer` - Vulnerability scanning
- `security-audit-orchestrator` - Comprehensive security audits

**[See full agent catalog in plugins/](grey-haven-plugins/)**

### 30+ Slash Commands

**Development**:
- `/tdd-implement` - TDD implementation workflow
- `/code-review` - Comprehensive code review
- `/refactor-clarity` - Clarity-focused refactoring

**Documentation**:
- `/doc-generate-api` - OpenAPI 3.1 generation
- `/doc-coverage` - Documentation coverage validation

**Security & Quality**:
- `/security-scan` - Security audit
- `/quality-pipeline` - Full quality check

**[See full command catalog in plugins/](grey-haven-plugins/)**

### 4 Production Hooks

- `subagent-context-preparer.py` - Optimize subagent context
- `security-validator.py` - Security validation
- `prompt-enhancer.py` - Enhance user prompts
- `work-completion-assistant.py` - Work completion tracking

---

## 🆚 v2.0.0 Changes

| Feature | v1.x | v2.0.0 |
|---------|------|--------|
| **Plugin distribution** | ✅ npm | ❌ Git + marketplace |
| **Hooks** | ✅ npm | ✅ npm (optional) |
| **CLI tools** | ✅ npm | ✅ npm (optional) |
| **Package size** | ~2 MB | ~500 KB |
| **Update method** | `npm update` | `git pull` + `npm update` |

**See [MIGRATION_V2.md](MIGRATION_V2.md) for complete migration guide.**

---

## 📋 System Requirements

### Required
- Claude Code installed
- Git

### Optional
- Python 3.8+ (for hooks)
- Node.js 14+ (for npm CLI tools)

### Check Installation

```bash
claude-config doctor
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

### Development Setup

```bash
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
cd grey-haven-claude-code-config
npm install
```

---

## 📄 License

MIT © Grey Haven Studio

---

## 🔗 Links

- **GitHub**: https://github.com/greyhaven-ai/grey-haven-claude-code-config
- **npm**: https://www.npmjs.com/package/@greyhaven/claude-code-config
- **Issues**: https://github.com/greyhaven-ai/grey-haven-claude-code-config/issues

---

**Built with ❤️ for the Claude Code community**
