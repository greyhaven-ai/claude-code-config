# Grey Haven Claude Code Configuration

A comprehensive collection of hooks, agents, and configurations to enhance Claude Code's capabilities for modern development workflows.

## 🚀 Quick Start

```bash
# Clone this repository
git clone https://github.com/grey-haven/claude-code-config.git

# Run setup in your project
bash claude-code-config/setup.sh /path/to/your/project
```

## 📁 Repository Structure

```
grey-haven-claude-code-config/
├── .claude/                    # Template directory (copy to projects)
│   ├── hooks/                 # Hook implementations
│   │   ├── python/           # Python-based hooks (13 hooks)
│   │   ├── javascript/       # JavaScript/TypeScript hooks (4 hooks)
│   │   ├── bash/             # Shell script hooks (4 hooks)
│   │   └── README.md         # Hook documentation
│   ├── agents/                # AI agent configurations
│   └── CLAUDE.md             # Project instructions for Claude
├── docs/                      # Documentation
│   └── hooks/
│       └── index.md          # Comprehensive hook guide
├── setup.sh                   # Main setup script (auto-detects project type)
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## 🌟 Features

### 🪝 Hooks (17 Advanced Hooks)

**Context Intelligence**
- **Smart Context Injector** - Analyzes prompts and loads relevant code
- **Branch Context Loader** - Loads context based on git branch patterns

**Code Analysis**
- **Dependency Impact Analyzer** - Shows what depends on code before editing
- **Similar Code Finder** - Finds similar patterns after edits
- **Performance Regression Detector** - Detects performance issues

**Testing & Quality**
- **Smart Test Runner** - Runs only affected tests
- **Coverage Gap Finder** - Shows uncovered code in changed files
- **Test Data Generator** - Generates realistic test data
- **Incremental Type Checker** - Type checks only changed files

**Documentation & Migration**
- **Auto-Documentation Fetcher** - Fetches library documentation
- **Code Narrator** - Generates plain English explanations
- **Migration Assistant** - Detects outdated patterns

**API & Database**
- **API Contract Validator** - Validates API changes against OpenAPI specs
- **Database Query Analyzer** - Analyzes SQL queries for performance

**Code Organization & Quality**
- **Smart Import Organizer** - Organizes and cleans imports
- **Code Linter** - Runs ruff, eslint, prettier, and other linters
- **Pre-commit Runner** - Executes pre-commit checks automatically

### 🤖 Agents
Specialized AI assistants for specific tasks (coming soon)

## 💻 Supported Environments

- **Python Projects** - Uses `uv` for dependency management
- **JavaScript/TypeScript** - Uses `bunx` (Bun) or `npx` (Node.js)
  - Automatic detection of project type
  - Language-specific hook versions (JS test runner, type checker, etc.)
- **Multi-language** - Hooks support Python, JS/TS, Go, Rust, Java

## 📋 Prerequisites

### Required
- `git` - Version control
- `ripgrep` (rg) - Fast file searching

### Environment Specific

**For Python hooks:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**For JavaScript/TypeScript projects:**
```bash
# Install Bun (recommended)
curl -fsSL https://bun.sh/install | bash

# Or use Node.js/npm
# https://nodejs.org/
```

### Optional
- `jq` - JSON processing (recommended)

## 🔧 Installation

### Interactive Setup

```bash
# Run the setup script
bash setup.sh /path/to/your/project

# Choose what to install:
# 1) Hooks only
# 2) Agents only
# 3) Everything
# 4) Custom selection
```

### Manual Installation

1. Copy the `.claude` directory to your project:
```bash
cp -r .claude /your/project/
```

2. Update paths in `.claude/settings.json` to point to the hooks

## 🎯 Usage

### Testing Hooks

```bash
# Test a Python hook
echo '{"prompt": "test"}' | .claude/implementations/hooks/python/smart-context-injector.py

# Test a Bash hook
echo '{"branch": "feature/test"}' | .claude/implementations/hooks/bash/branch-context-loader.sh
```

### Claude Code Commands

- `/hooks` - View active hooks
- `/agents` - List available agents
- `/help` - Get help

## 📚 Documentation

- **Hooks Guide**: `.claude/implementations/hooks/index.md`
- **Agents Guide**: `.claude/agents/guide.md`
- **Hook Documentation**: `.claude/implementations/hooks/docs/README.md`

## 🛠️ Customization

### Disable Specific Hooks

Edit `.claude/settings.json` and remove or comment out unwanted hooks:

```json
{
  "hooks": {
    "sessionStart": [
      // "/path/to/hook"  <- Commented out
    ]
  }
}
```

### Add Custom Documentation Sources

Edit hooks like `auto-documentation-fetcher.py` to add your libraries:

```python
DOC_SOURCES = {
    'your-library': 'https://docs.your-library.com/',
    # ...
}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "uv: command not found" | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| "ripgrep: command not found" | Install ripgrep: `brew install ripgrep` or `apt-get install ripgrep` |
| Hook not executing | Check permissions: `chmod +x .claude/implementations/hooks/*/*.{py,sh}` |
| JSON parse errors | Validate: `jq . < .claude/settings.json` |

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch
3. Follow existing patterns for new hooks
4. Test with multiple project types
5. Submit a pull request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🎉 Acknowledgments

Built for the Claude Code community to enhance development workflows with intelligent automation.

---

**Happy coding with Grey Haven tools! 🚀**