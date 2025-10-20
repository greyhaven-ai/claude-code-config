# V2.0.0 Architecture Plan
## Reducing npm/Homebrew Reliance While Maintaining Utility

**Date**: 2025-10-17
**Current Version**: v1.2.8 (npm), v1.0.0 (Homebrew)
**Target Version**: v2.0.0

---

## Executive Summary

**Goal**: Refocus npm package and Homebrew formula on **hooks and config management only**, removing plugin distribution functionality now handled by the plugin marketplace.

**Key Principle**: npm/Homebrew should be **optional convenience tools**, not required infrastructure.

**Primary Distribution**: Git repository cloning + local plugin marketplace

---

## Current State Analysis

### What v1.2.8 Does (npm package)

```json
{
  "name": "@greyhaven/claude-code-config",
  "version": "1.2.8",
  "description": "Comprehensive configuration manager for Claude Code - manage presets, hooks, agents, and commands"
}
```

**Architecture**:
- Node.js wrapper (`bin/claude-config.js`) spawns Python CLI (`claude-config`)
- Python CLI manages: presets, hooks, agents, commands, statuslines
- Postinstall script: sets permissions, displays welcome message
- Includes in package: `.claude/hooks/`, `setup-claude-code/`, `docs/cli/`

**Current functionality**:
1. ✅ **Hooks management** - Install/configure hooks
2. ✅ **Config management** - Presets, settings.json
3. ❌ **Plugin distribution** - Agents, commands (now redundant with plugin marketplace)
4. ✅ **Project initialization** - `claude-config init`
5. ✅ **Self-update** - `claude-config self-update`

### What v1.0.0 Does (Homebrew)

```ruby
class ClaudeConfig < Formula
  desc "Comprehensive configuration manager for Claude Code"
  url "https://github.com/greyhaven-ai/claude-code-config/archive/v1.0.0.tar.gz"
end
```

**Architecture**:
- Bash wrapper finds Python 3 dynamically
- Installs all files to `libexec`
- Creates `claude-config` binary in `bin/`

**Issues**:
- Outdated (v1.0.0 vs npm v1.2.8)
- Same functionality overlap as npm package

### Plugin Marketplace Architecture

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "./grey-haven-plugins"  // Local filesystem!
    }],
    "install": [
      "grey-haven-core@grey-haven-plugins",
      "grey-haven-developer-experience@grey-haven-plugins"
      // ... 12 plugins total
    ]
  }
}
```

**Key insight**: Plugins loaded from local filesystem, NOT npm!

---

## V2.0.0 Vision

### Core Philosophy

**npm/Homebrew purpose**: Setup automation for things **NOT** in the plugin marketplace

**What's NOT in plugin marketplace**:
1. **Hooks** (`.claude/hooks/`) - Configuration, not functionality
2. **Settings** (`.claude/settings.json`, `settings.local.json`) - User preferences
3. **MCP configurations** - Server setup, permissions
4. **Project templates** - `.github/workflows/`, `vitest.config.ts`, etc.

**What IS in plugin marketplace**:
1. ✅ Agents (26+ agents across 12 plugins)
2. ✅ Commands (30+ commands across 12 plugins)
3. ✅ Workflow templates (`.claude/workflow-templates/`)
4. ✅ Documentation (`.claude/*.md`)

### V2.0.0 Scope Reduction

#### KEEP in npm/Homebrew v2.0.0:

```bash
# Hooks management
claude-config install-hooks       # Copy hooks to ~/.claude/hooks/
claude-config enable-hook <name>  # Enable specific hook
claude-config list-hooks          # Show available hooks

# Config management
claude-config init                # Initialize .claude/ directory
claude-config setup-mcp           # Configure MCP servers
claude-config backup-settings     # Backup user settings
claude-config restore-settings    # Restore from backup

# Project setup
claude-config create-project <name>  # Initialize new project
claude-config add-github-actions     # Add CI/CD templates
claude-config setup-vitest           # Add test configuration

# Utility
claude-config self-update         # Update npm package
claude-config doctor              # Diagnose installation issues
```

#### REMOVE from npm/Homebrew v2.0.0:

```bash
# These are now handled by plugin marketplace:
❌ claude-config list-presets         # Use git clone + marketplace
❌ claude-config preset <name>        # Use git clone + marketplace
❌ claude-config list-agents          # Use plugin marketplace
❌ claude-config add-agent <name>     # Use plugin marketplace
❌ claude-config list-commands        # Use plugin marketplace
```

---

## V2.0.0 Architecture

### Package Structure

```
@greyhaven/claude-code-config/
├── bin/
│   └── claude-config.js           # Node.js wrapper
├── scripts/
│   ├── postinstall.js             # Setup automation
│   └── hooks/                     # Hook installation scripts
├── .claude/
│   ├── hooks/                     # 7 production hooks
│   │   ├── subagent-context-preparer.py
│   │   ├── bash-permission-validator.py
│   │   ├── edit-permission-validator.py
│   │   ├── write-permission-validator.py
│   │   ├── agent-output-formatter.py
│   │   ├── mcp-tool-permission-validator.py
│   │   └── user-prompt-submit.py
│   └── settings.json.template     # Template for user settings
├── templates/
│   ├── github-actions/            # CI/CD templates
│   ├── vitest/                    # Test configuration
│   └── project-init/              # New project scaffolding
├── docs/
│   └── cli/
│       ├── GETTING_STARTED.md
│       ├── HOOKS_GUIDE.md
│       └── MCP_SETUP.md
├── package.json                   # v2.0.0 with reduced scope
├── README-npm.md                  # Updated README
└── claude-config                  # Refactored Python CLI
```

**Total package size**: ~500 KB (down from ~2 MB in v1.2.8)

### Updated package.json

```json
{
  "name": "@greyhaven/claude-code-config",
  "version": "2.0.0",
  "description": "Hooks and configuration setup for Grey Haven's Claude Code environment",
  "main": "lib/index.js",
  "bin": {
    "claude-config": "./bin/claude-config.js"
  },
  "scripts": {
    "postinstall": "node scripts/postinstall.js"
  },
  "keywords": [
    "claude",
    "claude-code",
    "hooks",
    "configuration",
    "setup",
    "cli",
    "mcp",
    "grey-haven"
  ],
  "files": [
    "bin/",
    "scripts/",
    ".claude/hooks/",
    ".claude/settings.json.template",
    "templates/",
    "docs/cli/",
    "LICENSE",
    "README-npm.md",
    "claude-config"
  ],
  "engines": {
    "node": ">=14.0.0"
  },
  "preferGlobal": true
}
```

### CLI Command Mapping

| v1.2.8 Command | v2.0.0 Status | Alternative |
|----------------|---------------|-------------|
| `init` | ✅ Keep | Project initialization |
| `list-presets` | ❌ Remove | Git clone + marketplace |
| `preset <name>` | ❌ Remove | Git clone + marketplace |
| `list-agents` | ❌ Remove | Plugin marketplace |
| `add-agent` | ❌ Remove | Plugin marketplace |
| `list-commands` | ❌ Remove | Plugin marketplace |
| `self-update` | ✅ Keep | npm update |
| `install-hooks` | ✅ **NEW** | Hook installation |
| `setup-mcp` | ✅ **NEW** | MCP configuration |
| `create-project` | ✅ **NEW** | Project scaffolding |
| `doctor` | ✅ **NEW** | Diagnostics |

---

## Migration Strategy

### Phase 1: Breaking Changes (v2.0.0)

**What users need to do**:

```bash
# Old workflow (v1.2.8)
npm install -g @greyhaven/claude-code-config
claude-config preset recommended

# New workflow (v2.0.0)
# 1. Clone repository for plugins
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
cd grey-haven-claude-code-config

# 2. Add to .claude/settings.json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/full/path/to/grey-haven-claude-code-config/grey-haven-plugins"
    }],
    "install": [
      "grey-haven-core@grey-haven-plugins",
      "grey-haven-developer-experience@grey-haven-plugins"
    ]
  }
}

# 3. (Optional) Install CLI for hooks/setup
npm install -g @greyhaven/claude-code-config
claude-config install-hooks
claude-config setup-mcp
```

### Phase 2: Deprecation Warnings (v1.2.9 - Transitional Release)

Before releasing v2.0.0, release v1.2.9 with deprecation warnings:

```bash
$ claude-config preset recommended

⚠️  WARNING: This command will be removed in v2.0.0

   The plugin marketplace now handles agents and commands.
   To migrate:

   1. Clone repository:
      git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git

   2. Add to .claude/settings.json:
      {
        "plugin": {
          "marketplaces": [{
            "source": "/path/to/grey-haven-claude-code-config/grey-haven-plugins"
          }]
        }
      }

   3. See migration guide:
      https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md

Continuing with preset installation...
```

### Phase 3: v2.0.0 Release

**Breaking changes**:
- ❌ Remove `preset` command
- ❌ Remove `list-agents`, `add-agent` commands
- ❌ Remove `list-commands` command
- ❌ Remove agent/command files from npm package
- ✅ Add `install-hooks` command
- ✅ Add `setup-mcp` command
- ✅ Add `create-project` command
- ✅ Add `doctor` command

**Package size reduction**: ~75% smaller (2 MB → ~500 KB)

---

## Homebrew Formula v2.0.0

### Updated claude-config.rb

```ruby
class ClaudeConfig < Formula
  desc "Hooks and configuration setup for Grey Haven's Claude Code environment"
  homepage "https://github.com/greyhaven-ai/claude-code-config"
  url "https://github.com/greyhaven-ai/claude-code-config/archive/v2.0.0.tar.gz"
  sha256 "TBD_AFTER_RELEASE"
  license "MIT"
  head "https://github.com/greyhaven-ai/claude-code-config.git", branch: "main"

  depends_on "git"
  depends_on "node" => :optional  # For npm integration

  def install
    # Install hooks and templates only
    libexec.install ".claude/hooks"
    libexec.install "templates"
    libexec.install "docs/cli"
    libexec.install "claude-config"

    # Create wrapper script
    (bin/"claude-config").write <<~EOS
      #!/bin/bash
      export CLAUDE_CONFIG_GLOBAL=1
      export CLAUDE_CONFIG_HOME="#{libexec}"

      if command -v python3 &> /dev/null; then
        exec python3 "#{libexec}/claude-config" "$@"
      elif command -v uv &> /dev/null; then
        exec uv run python "#{libexec}/claude-config" "$@"
      else
        echo "Error: Python 3 is required" >&2
        exit 1
      fi
    EOS

    chmod 0755, bin/"claude-config"
  end

  def caveats
    <<~EOS
      Claude Config v2.0.0 has been installed!

      This tool manages hooks and configuration for Claude Code.
      For plugins (agents/commands), clone the repository:

        git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git

      Quick Start:
        claude-config install-hooks    Install hooks to ~/.claude/hooks/
        claude-config setup-mcp         Configure MCP servers
        claude-config create-project    Initialize new project

      Documentation:
        https://github.com/greyhaven-ai/claude-code-config
    EOS
  end

  test do
    system "#{bin}/claude-config", "--help"
    assert_match "hooks", shell_output("#{bin}/claude-config --help")
  end
end
```

---

## CLI Refactoring Plan

### New Python CLI Structure

```python
#!/usr/bin/env python3
"""
Claude Config CLI v2.0.0 - Hooks and Configuration Setup

Focused on:
- Hook installation and management
- MCP server configuration
- Project initialization
- Settings backup/restore
"""

VERSION = "2.0.0"

class ClaudeConfigManager:
    def __init__(self):
        self.repo_dir = Path(__file__).parent
        self.hooks_dir = self.repo_dir / '.claude' / 'hooks'
        self.templates_dir = self.repo_dir / 'templates'

    # === NEW COMMANDS ===

    def install_hooks(self, target: Optional[str] = None):
        """Install hooks to ~/.claude/hooks/ or project directory"""
        target_dir = Path(target) if target else Path.home() / '.claude' / 'hooks'
        target_dir.mkdir(parents=True, exist_ok=True)

        for hook in self.hooks_dir.glob('*.py'):
            shutil.copy2(hook, target_dir / hook.name)
            print(f"✅ Installed {hook.name}")

    def setup_mcp(self):
        """Configure MCP servers in settings.json"""
        # Interactive MCP server setup wizard
        pass

    def create_project(self, name: str, template: str = 'default'):
        """Initialize new project with templates"""
        # Create project structure with .claude/, .github/, etc.
        pass

    def doctor(self):
        """Diagnose installation and configuration issues"""
        checks = [
            self._check_python_version(),
            self._check_hooks_installed(),
            self._check_settings_json(),
            self._check_mcp_servers(),
            self._check_plugin_marketplace()
        ]
        # Print diagnostic report
        pass

    # === REMOVED COMMANDS ===

    # ❌ def list_presets(self)
    # ❌ def apply_preset(self, name: str)
    # ❌ def list_agents(self)
    # ❌ def add_agent(self, name: str)
```

### New CLI Help Output

```bash
$ claude-config --help

Claude Config v2.0.0 - Hooks and Configuration Setup for Claude Code

USAGE:
  claude-config <command> [options]

COMMANDS:
  Hooks Management:
    install-hooks [--target DIR]    Install hooks to ~/.claude/hooks/
    list-hooks                      Show available hooks
    enable-hook <name>              Enable specific hook
    disable-hook <name>             Disable specific hook

  Configuration:
    init                            Initialize .claude/ directory
    setup-mcp                       Configure MCP servers
    backup-settings                 Backup user settings
    restore-settings                Restore from backup

  Project Setup:
    create-project <name>           Initialize new project
    add-github-actions              Add CI/CD templates
    setup-vitest                    Add test configuration

  Utility:
    self-update                     Update to latest version
    doctor                          Diagnose installation issues
    version                         Show version
    help                            Show this help

PLUGIN MARKETPLACE:
  For agents and commands, use the plugin marketplace:

  1. Clone repository:
     git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git

  2. Add to .claude/settings.json:
     {
       "plugin": {
         "marketplaces": [{
           "source": "/path/to/grey-haven-claude-code-config/grey-haven-plugins"
         }]
       }
     }

  See: https://github.com/greyhaven-ai/grey-haven-claude-code-config

VERSION: 2.0.0
```

---

## Documentation Updates

### New README-npm.md

```markdown
# @greyhaven/claude-code-config

Hooks and configuration setup for Grey Haven's Claude Code environment.

## What This Package Does

This npm package provides:
- ✅ **Hooks installation** - 7 production hooks for Claude Code
- ✅ **MCP configuration** - Setup wizard for MCP servers
- ✅ **Project initialization** - Templates for new projects
- ✅ **Settings management** - Backup/restore configuration

## What This Package Does NOT Do

- ❌ Plugin distribution - Use Git + plugin marketplace instead
- ❌ Agent management - Agents are in plugins
- ❌ Command management - Commands are in plugins

## Installation

```bash
npm install -g @greyhaven/claude-code-config
```

## Quick Start

```bash
# Install hooks
claude-config install-hooks

# Configure MCP servers
claude-config setup-mcp

# Create new project
claude-config create-project my-app
```

## Using Plugins (Agents & Commands)

Plugins are distributed via Git, not npm:

```bash
# 1. Clone repository
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
cd grey-haven-claude-code-config

# 2. Add to ~/.claude/settings.json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/full/path/to/grey-haven-claude-code-config/grey-haven-plugins"
    }],
    "install": [
      "grey-haven-core@grey-haven-plugins",
      "grey-haven-developer-experience@grey-haven-plugins",
      "grey-haven-observability@grey-haven-plugins"
    ]
  }
}
```

## Migration from v1.x

See [MIGRATION_V2.md](https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md)

## Available Hooks

- `subagent-context-preparer.py` - Prepare context for subagents
- `bash-permission-validator.py` - Validate bash commands
- `edit-permission-validator.py` - Validate file edits
- `write-permission-validator.py` - Validate file writes
- `agent-output-formatter.py` - Format agent outputs
- `mcp-tool-permission-validator.py` - Validate MCP tool calls
- `user-prompt-submit.py` - Process user prompts

## Commands

```bash
claude-config install-hooks        # Install hooks
claude-config setup-mcp            # Configure MCP
claude-config create-project       # New project
claude-config doctor               # Diagnose issues
claude-config self-update          # Update package
```

## License

MIT - Grey Haven Studio
```

### New MIGRATION_V2.md

Create comprehensive migration guide in repository root explaining:
- Why v2.0.0 changes were made
- Step-by-step migration process
- Side-by-side comparison of old vs new workflows
- Troubleshooting common issues

---

## Timeline

### Week 1: Preparation (Before v2.0.0)

**Days 1-2**: Release v1.2.9 with deprecation warnings
- Add warnings to `preset`, `list-agents`, `add-agent` commands
- Update README with migration notice
- Create MIGRATION_V2.md guide

**Days 3-5**: Test v1.2.9 in production
- Ensure warnings display correctly
- Gather user feedback
- Update documentation based on feedback

**Days 6-7**: Prepare v2.0.0 release
- Refactor Python CLI (remove preset/agent management)
- Update package.json to v2.0.0
- Update Homebrew formula to v2.0.0
- Create release notes

### Week 2: v2.0.0 Release

**Day 1**: Release v2.0.0
```bash
# npm
npm version 2.0.0
npm publish

# Homebrew (create PR)
brew bump-formula-pr claude-config \
  --url=https://github.com/greyhaven-ai/claude-code-config/archive/v2.0.0.tar.gz
```

**Days 2-7**: Monitor and support
- Monitor GitHub issues
- Answer migration questions
- Update docs based on user feedback
- Patch releases (v2.0.1, v2.0.2) if needed

### Week 3-4: Stabilization

- Ensure all users successfully migrated
- Update all documentation
- Create video tutorial for new workflow
- Close v1.x support

---

## Success Metrics

### Package Size Reduction

| Metric | v1.2.8 | v2.0.0 | Change |
|--------|--------|--------|--------|
| npm package size | ~2 MB | ~500 KB | -75% |
| Files included | 200+ | ~50 | -75% |
| Dependencies | Node + Python | Node + Python | Same |

### User Experience

**Old workflow (v1.2.8)**:
```bash
npm install -g @greyhaven/claude-code-config  # 2 MB download
claude-config preset recommended               # 30 seconds
```

**New workflow (v2.0.0)**:
```bash
# One-time setup
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
# Add to settings.json (manual, 2 minutes)

# Optional CLI for hooks
npm install -g @greyhaven/claude-code-config  # 500 KB download
claude-config install-hooks                   # 5 seconds
```

**Trade-offs**:
- ❌ More complex initial setup (Git clone + settings.json edit)
- ✅ 75% smaller npm package
- ✅ Direct access to latest plugins (Git pull)
- ✅ Clearer separation of concerns (hooks vs plugins)
- ✅ npm/Homebrew become optional, not required

### Maintenance Burden

| Aspect | v1.2.8 | v2.0.0 | Change |
|--------|--------|--------|--------|
| Files to maintain in npm | 200+ | ~50 | -75% |
| CLI commands | 12 | 8 | -33% |
| Update frequency | Weekly | Monthly | -75% |
| Support complexity | High | Low | Simpler |

---

## Risk Assessment

### High Risk: User Confusion

**Risk**: Users don't understand why they need to clone repo AND install npm package

**Mitigation**:
1. Clear documentation explaining "npm for hooks, Git for plugins"
2. Deprecation warnings in v1.2.9 (1-2 weeks before v2.0.0)
3. Migration guide with screenshots
4. Video tutorial
5. FAQ section

### Medium Risk: Breaking Workflows

**Risk**: Teams have automated workflows using `claude-config preset`

**Mitigation**:
1. v1.2.9 deprecation warnings give advance notice
2. Keep v1.2.x available on npm indefinitely
3. Provide conversion script: `claude-config migrate-to-v2`
4. Support both workflows during transition (1-2 months)

### Low Risk: Homebrew Update Delays

**Risk**: Homebrew PR approval takes time

**Mitigation**:
1. Keep Homebrew v1.0.0 functional (just outdated)
2. Document manual installation if needed
3. Consider moving to `brew tap greyhaven-ai/tap` for faster updates

---

## Alternative: Keep Both Workflows

**Option B**: Support BOTH npm distribution AND Git marketplace

### Dual Mode v2.0.0

```bash
# Mode 1: Legacy npm-only (simpler, larger package)
npm install -g @greyhaven/claude-code-config
claude-config preset recommended  # Still works, but deprecated

# Mode 2: Git marketplace (recommended, smaller package)
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git
# Add to settings.json
npm install -g @greyhaven/claude-code-config  # Optional, for hooks only
```

**Trade-offs**:
- ✅ Easier migration (both workflows supported)
- ✅ No breaking changes
- ❌ Larger npm package (can't reduce size)
- ❌ Maintenance burden (support two distribution methods)
- ❌ User confusion (which method to use?)

**Recommendation**: **Proceed with Option A (v2.0.0 with breaking changes)** for long-term maintainability.

---

## Decision Matrix

| Factor | Keep npm Distribution | Remove npm Distribution |
|--------|----------------------|------------------------|
| Package size | ❌ 2 MB | ✅ 500 KB (-75%) |
| User experience | ✅ Simpler (one command) | ❌ More steps (Git + settings) |
| Maintenance | ❌ High (dual sync) | ✅ Low (hooks only) |
| Clarity | ❌ Confusing overlap | ✅ Clear separation |
| Migration pain | ✅ Low (no breaking changes) | ❌ High (breaking changes) |
| Long-term sustainability | ❌ Technical debt | ✅ Clean architecture |

**Final Recommendation**: **Proceed with v2.0.0 removal of plugin distribution**

**Rationale**:
1. Plugin marketplace is the future - embrace it fully
2. Maintaining dual distribution is technical debt
3. Breaking changes are acceptable with proper migration path
4. Smaller npm package = faster installs, better UX long-term
5. Clearer mental model: "npm for hooks, Git for plugins"

---

## Next Steps

1. ✅ **Review this plan** - Stakeholder approval
2. Create v1.2.9 with deprecation warnings
3. Test v1.2.9 for 1-2 weeks
4. Refactor Python CLI for v2.0.0
5. Update package.json, Homebrew formula
6. Create MIGRATION_V2.md guide
7. Release v2.0.0
8. Monitor and support migration

**Target release date**: 2 weeks from approval

---

## Questions to Resolve

1. **Deprecation timeline**: How long to warn users before v2.0.0?
   - **Recommendation**: 2 weeks minimum, 4 weeks ideal

2. **Keep v1.x on npm?**: Should we unpublish or deprecate?
   - **Recommendation**: Deprecate but keep available indefinitely

3. **Homebrew tap?**: Should we create `brew tap greyhaven-ai/tap`?
   - **Recommendation**: Yes, for faster updates without Homebrew core PR delays

4. **Migration script?**: Should we provide automated migration?
   - **Recommendation**: Yes, `claude-config migrate-to-v2` that edits settings.json

5. **Support timeline?**: How long to support v1.x questions?
   - **Recommendation**: 3 months active support, 6 months passive support

---

## Appendix: File Size Breakdown

### v1.2.8 (Current)

```
@greyhaven/claude-code-config/
├── .claude/
│   ├── hooks/                  ~50 KB
│   ├── agents/                 ~500 KB ❌ Remove in v2.0.0
│   ├── commands/               ~300 KB ❌ Remove in v2.0.0
│   └── presets/                ~200 KB ❌ Remove in v2.0.0
├── setup-claude-code/          ~400 KB ❌ Remove in v2.0.0
├── docs/                       ~100 KB
└── bin/ + scripts/             ~50 KB
─────────────────────────────────────
TOTAL:                          ~1.6 MB
```

### v2.0.0 (Proposed)

```
@greyhaven/claude-code-config/
├── .claude/
│   ├── hooks/                  ~50 KB ✅ Keep
│   └── settings.json.template  ~5 KB ✅ Keep
├── templates/
│   ├── github-actions/         ~20 KB ✅ Keep
│   ├── vitest/                 ~10 KB ✅ Keep
│   └── project-init/           ~30 KB ✅ Keep
├── docs/cli/                   ~50 KB ✅ Keep
└── bin/ + scripts/             ~50 KB ✅ Keep
─────────────────────────────────────
TOTAL:                          ~215 KB
```

**Actual package size with dependencies**: ~500 KB (compression + metadata)

---

**END OF ARCHITECTURE PLAN**
