# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Repository Overview

Grey Haven Studio's comprehensive Claude Code configuration system - v2.0.0

**What's in this repository**:
- 12 plugin packages with 26+ agents and 30+ commands (in `grey-haven-plugins/`)
- npm CLI package for hook installation and setup utilities
- Production hooks for enhanced Claude Code experience
- Comprehensive documentation and migration guides

## Project Structure

```
/
├── grey-haven-plugins/              # Plugin marketplace (15 plugins)
│   ├── core/
│   ├── developer-experience/
│   ├── creative-writing/
│   └── ... (12 more plugins)
├── .claude/
│   ├── hooks/                       # Production hooks (4 hooks)
│   │   ├── subagent-context-preparer.py
│   │   ├── security-validator.py
│   │   ├── prompt-enhancer.py
│   │   └── work-completion-assistant.py
│   ├── settings.json.template       # Settings template
│   ├── archive/                     # Old documentation
│   └── research/                    # Research documents
├── templates/                       # Project templates
├── docs/cli/                        # CLI documentation
├── claude-config                    # Python CLI script (v2.0.0)
├── bin/claude-config.js             # Node.js wrapper
├── package.json                     # npm package config (v2.0.0)
├── homebrew/claude-config.rb        # Homebrew formula (v2.0.0)
├── README.md                        # Main repository README
├── README-npm.md                    # npm package README
├── MIGRATION_V2.md                  # v1.x → v2.0.0 migration guide
└── LICENSE                          # MIT License
```

## v2.0.0 Architecture

**Key principle**: npm/Homebrew for hooks and setup, Git + plugin marketplace for plugins.

**Distribution strategy**:
- **Plugins**: Distributed via Git repository + local plugin marketplace
- **Hooks**: Distributed via npm/Homebrew (optional)
- **CLI tools**: Distributed via npm/Homebrew (optional)

**Why this change?**:
Claude Code's plugin marketplace loads plugins from local filesystem, making npm distribution of agents/commands redundant. This reduces package size by 75% and simplifies maintenance.

## Claude Code Configuration

The repository includes plugin marketplace configuration for loading all Grey Haven plugins:

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/absolute/path/to/grey-haven-plugins"
    }],
    "install": [
      "core@grey-haven-plugins",
      "developer-experience@grey-haven-plugins"
    ]
  }
}
```

## Development Workflow

### Working on Plugins

Plugins are in `grey-haven-plugins/` directory. Each plugin has:
- `agents/` - Agent definitions (.md files)
- `commands/` - Slash command definitions (.md files)
- `plugin.json` - Plugin metadata
- `README.md` - Plugin documentation

**To add a new plugin**:
1. Create directory in `grey-haven-plugins/`
2. Add `plugin.json` with metadata
3. Create `agents/` and/or `commands/` directories
4. Add to marketplace in `.claude/settings.json`

### Working on CLI

The Python CLI (`claude-config`) provides:
- Hook installation: `install-hooks`, `list-hooks`
- Configuration: `init`, `backup-settings`, `restore-settings`
- Diagnostics: `doctor`, `version`, `self-update`

**To test CLI changes**:
```bash
./claude-config --help
./claude-config list-hooks
./claude-config doctor
```

### Working on Hooks

Production hooks are in `.claude/hooks/` (root level, not subdirectories).

**Current production hooks**:
- `subagent-context-preparer.py` - Optimize subagent context
- `security-validator.py` - Security validation
- `prompt-enhancer.py` - Enhance prompts
- `work-completion-assistant.py` - Work tracking

**To add a new hook**:
1. Copy from `.claude/hooks/python/` to `.claude/hooks/`
2. Test with `./claude-config list-hooks`
3. Update `.claude/settings.json.template`

## npm Package Contents

**What's included in npm package** (v2.0.0):
- `bin/claude-config.js` - Node.js wrapper
- `claude-config` - Python CLI script
- `.claude/hooks/` - Production hooks (4 files)
- `.claude/settings.json.template` - Settings template
- `templates/` - Project templates
- `docs/cli/` - CLI documentation
- `LICENSE` - MIT license
- `README-npm.md` - npm README

**What's NOT in npm package**:
- `grey-haven-plugins/` - Plugins (too large, use Git instead)
- `.claude/archive/` - Old docs
- `.claude/research/` - Research docs
- Development files

## Testing

**Test CLI locally**:
```bash
./claude-config --help
./claude-config list-hooks
./claude-config install-hooks --dry-run
./claude-config doctor
```

**Test plugins**:
Load in Claude Code and test commands like `/tdd-implement`, `/code-review`

## Release Process

### npm Release

```bash
# Ensure on v2-dev branch with all changes
git checkout v2-dev

# Update version in claude-config (line 23)
# VERSION = "2.0.0"

# Test
./claude-config --version

# Commit
git add -A
git commit -m "chore: release v2.0.0"

# Tag
git tag -a v2.0.0 -m "Release v2.0.0"

# Publish to npm
npm publish

# Merge to main
git checkout main
git merge v2-dev
git push origin main
git push origin v2.0.0
```

### Homebrew Release

```bash
# Create tarball
git archive --format=tar.gz --prefix=claude-config-2.0.0/ v2.0.0 > claude-config-2.0.0.tar.gz

# Calculate SHA256
shasum -a 256 claude-config-2.0.0.tar.gz

# Update homebrew/claude-config.rb with SHA256
# sha256 "ACTUAL_SHA256_HERE"

# Test locally
brew install --build-from-source homebrew/claude-config.rb
claude-config --version
```

## Documentation Maintenance

**Keep these updated**:
- `README.md` - Main repository README
- `README-npm.md` - npm package README
- `MIGRATION_V2.md` - Migration guide
- `.claude/V2_ARCHITECTURE_PLAN.md` - Architecture decisions
- `.claude/V2_IMPLEMENTATION_SUMMARY.md` - Implementation guide

**Archive old docs** to `.claude/archive/` when no longer relevant.

## License

This project is licensed under the MIT License - Copyright (c) 2025 Grey Haven Studio.
