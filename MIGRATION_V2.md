# Migration Guide: v1.x → v2.0.0

**Last Updated**: 2025-10-17
**Target Audience**: Users of @greyhaven/claude-code-config v1.x
**Estimated Migration Time**: 10-15 minutes

---

## 🎯 What's Changing in v2.0.0

### TL;DR

**v1.x**: npm package distributed everything (hooks, agents, commands, presets)
**v2.0.0**: npm package handles **hooks and config only**, plugins distributed via **Git + marketplace**

### Why This Change?

Claude Code introduced a **plugin marketplace** that loads plugins from local filesystem. This makes npm distribution of agents/commands redundant and creates maintenance overhead.

**Benefits of v2.0.0**:
- ✅ 75% smaller npm package (500 KB vs 2 MB)
- ✅ Direct access to latest plugins via Git
- ✅ Clearer separation: npm for setup, Git for functionality
- ✅ Easier plugin development (edit locally, see changes immediately)

---

## 📊 Side-by-Side Comparison

### Old Workflow (v1.x)

```bash
# Installation
npm install -g @greyhaven/claude-code-config

# Apply preset (includes hooks + agents + commands)
claude-config preset recommended

# Done! ✅
```

**What npm v1.x provided**:
- ✅ Hooks
- ✅ Agents (26+ agents)
- ✅ Commands (30+ commands)
- ✅ Presets
- ✅ Settings templates

### New Workflow (v2.0.0)

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
      "grey-haven-core@grey-haven-plugins",
      "grey-haven-developer-experience@grey-haven-plugins",
      "grey-haven-observability@grey-haven-plugins"
    ]
  }
}

# 3. (Optional) Install CLI for hooks and setup
npm install -g @greyhaven/claude-code-config
claude-config install-hooks
claude-config setup-mcp

# Done! ✅
```

**What npm v2.0.0 provides**:
- ✅ Hooks
- ✅ MCP configuration
- ✅ Project templates
- ✅ Setup utilities
- ❌ Agents (now in Git repository)
- ❌ Commands (now in Git repository)
- ❌ Presets (now in Git repository)

---

## 🚀 Step-by-Step Migration

### Prerequisites

- ✅ Claude Code installed
- ✅ Git installed
- ✅ Node.js 14+ (if using npm package)

### Step 1: Clone the Repository

**Purpose**: Get all plugins (agents, commands, workflow templates)

```bash
# Choose a location for the repository
cd ~
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git grey-haven-plugins

# Verify installation
ls grey-haven-plugins/grey-haven-plugins/
# Should see: grey-haven-core/, grey-haven-developer-experience/, etc.
```

**Windows users**:
```powershell
cd $HOME
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git grey-haven-plugins
```

### Step 2: Configure Plugin Marketplace

**Purpose**: Tell Claude Code where to load plugins from

#### Option A: Using claude-config CLI (Recommended)

```bash
# If you have v1.x installed, upgrade to v2.0.0 first
npm update -g @greyhaven/claude-code-config

# Automatic configuration (easiest!)
claude-config migrate-to-v2 --repo-path ~/grey-haven-plugins
```

This automatically:
1. Backs up your current `~/.claude/settings.json`
2. Adds plugin marketplace configuration
3. Installs hooks to `~/.claude/hooks/`

#### Option B: Manual Configuration

**Edit `~/.claude/settings.json`** (create if doesn't exist):

```json
{
  "plugin": {
    "marketplaces": [
      {
        "name": "grey-haven-plugins",
        "source": "/Users/YOUR_USERNAME/grey-haven-plugins/grey-haven-plugins"
      }
    ],
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

**⚠️ IMPORTANT**: Replace `/Users/YOUR_USERNAME/grey-haven-plugins/grey-haven-plugins` with the **absolute path** to your cloned repository's `grey-haven-plugins/` subdirectory.

**Find your absolute path**:
```bash
cd ~/grey-haven-plugins/grey-haven-plugins && pwd
# Copy this output into settings.json
```

### Step 3: Install Hooks (Optional but Recommended)

**Purpose**: Get all 7 production hooks for enhanced Claude Code experience

#### Option A: Using claude-config CLI

```bash
# Install/upgrade npm package
npm install -g @greyhaven/claude-code-config

# Install hooks to ~/.claude/hooks/
claude-config install-hooks
```

#### Option B: Manual Installation

```bash
# Copy hooks from repository
cp ~/grey-haven-plugins/.claude/hooks/*.py ~/.claude/hooks/

# Make them executable (macOS/Linux)
chmod +x ~/.claude/hooks/*.py
```

**Hooks installed**:
- `subagent-context-preparer.py` - Prepare context for subagents
- `bash-permission-validator.py` - Validate bash commands
- `edit-permission-validator.py` - Validate file edits
- `write-permission-validator.py` - Validate file writes
- `agent-output-formatter.py` - Format agent outputs
- `mcp-tool-permission-validator.py` - Validate MCP tool calls
- `user-prompt-submit.py` - Process user prompts

### Step 4: Verify Installation

**Test plugin loading**:

```bash
# Start Claude Code
claude

# In Claude Code, run:
/help

# You should see all Grey Haven commands like:
# /tdd-implement, /code-review, /security-scan, etc.
```

**Verify hooks**:

```bash
ls ~/.claude/hooks/
# Should show all 7 .py files
```

**Check plugin marketplace**:

```bash
cat ~/.claude/settings.json
# Should show plugin.marketplaces configuration
```

### Step 5: Clean Up (Optional)

**Remove old npm v1.x package** (if upgrading):

```bash
# Uninstall old version
npm uninstall -g @greyhaven/claude-code-config

# Reinstall v2.0.0 (optional, for CLI utilities)
npm install -g @greyhaven/claude-code-config@2.0.0
```

**Remove old preset files** (if you had v1.x):

These are no longer used since presets are in the Git repository:

```bash
# Only if you want to clean up
rm -rf ~/.claude-config/  # Old v1.x installation
```

---

## 🔧 Updating Plugins

### Old Way (v1.x)

```bash
npm update -g @greyhaven/claude-code-config
# Or: claude-config self-update
```

### New Way (v2.0.0)

```bash
# Update plugins (agents, commands)
cd ~/grey-haven-plugins
git pull origin main

# Update CLI tools (hooks, setup utilities) - optional
npm update -g @greyhaven/claude-code-config
```

**Best practice**: Update both repository and npm package weekly.

---

## 🐛 Troubleshooting

### Issue: "Plugin marketplace not loading"

**Symptoms**: `/help` doesn't show Grey Haven commands

**Solution**:
```bash
# 1. Verify absolute path in settings.json
cat ~/.claude/settings.json
# Check that "source" points to correct directory

# 2. Verify directory exists
ls /Users/YOUR_USERNAME/grey-haven-plugins/grey-haven-plugins/
# Should show grey-haven-core/, grey-haven-developer-experience/, etc.

# 3. Restart Claude Code
# Exit and restart
```

### Issue: "Hooks not working"

**Symptoms**: Hooks don't execute on bash/edit/write operations

**Solution**:
```bash
# 1. Check hooks are in correct location
ls ~/.claude/hooks/
# Should show .py files

# 2. Make hooks executable (macOS/Linux)
chmod +x ~/.claude/hooks/*.py

# 3. Verify Python 3 is installed
python3 --version
# Should show Python 3.x

# 4. Test hook manually
python3 ~/.claude/hooks/bash-permission-validator.py
```

### Issue: "Command not found: claude-config"

**Symptoms**: `claude-config` command doesn't work after npm install

**Solution**:
```bash
# 1. Verify npm global bin directory is in PATH
npm config get prefix
# Should show /usr/local or ~/.npm-global

# 2. Add to PATH (if not already)
# macOS/Linux - add to ~/.zshrc or ~/.bashrc:
export PATH="$(npm config get prefix)/bin:$PATH"

# 3. Reinstall package
npm uninstall -g @greyhaven/claude-code-config
npm install -g @greyhaven/claude-code-config

# 4. Verify installation
claude-config --version
```

### Issue: "Python not found" error

**Symptoms**: `claude-config` fails with "Python 3 is required"

**Solution**:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Windows
# Download from https://www.python.org/downloads/

# Verify
python3 --version
```

### Issue: "Settings.json gets overwritten"

**Symptoms**: Plugin configuration disappears after Claude Code restart

**Solution**:
```bash
# Use settings.local.json for plugin configuration
# (This file is never overwritten by Claude Code)

# Move plugin config from settings.json to settings.local.json
cat ~/.claude/settings.json  # Copy plugin block
# Edit ~/.claude/settings.local.json and paste

# Verify
cat ~/.claude/settings.local.json
```

---

## 📝 Configuration Reference

### Minimal Configuration

**For plugins only** (no npm package):

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/absolute/path/to/grey-haven-plugins/grey-haven-plugins"
    }],
    "install": [
      "grey-haven-core@grey-haven-plugins"
    ]
  }
}
```

### Recommended Configuration

**All plugins + custom settings**:

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
  },
  "mcp": {
    "servers": {
      "firecrawl-mcp": {
        "command": "npx",
        "args": ["-y", "firecrawl-mcp"],
        "env": {
          "FIRECRAWL_API_KEY": "your-api-key"
        }
      }
    },
    "auto_approve_tools": {
      "firecrawl_scrape": {
        "allowed_tools": ["mcp__firecrawl-mcp__firecrawl_scrape"]
      }
    }
  },
  "hooks": {
    "bash-permission-validator": {"enabled": true},
    "edit-permission-validator": {"enabled": true},
    "write-permission-validator": {"enabled": true},
    "subagent-context-preparer": {"enabled": true},
    "agent-output-formatter": {"enabled": true},
    "mcp-tool-permission-validator": {"enabled": true},
    "user-prompt-submit": {"enabled": true}
  }
}
```

### Advanced: Multiple Marketplaces

**If you have your own plugins + Grey Haven plugins**:

```json
{
  "plugin": {
    "marketplaces": [
      {
        "name": "grey-haven-plugins",
        "source": "/Users/YOU/grey-haven-plugins/grey-haven-plugins"
      },
      {
        "name": "my-custom-plugins",
        "source": "/Users/YOU/my-plugins"
      }
    ],
    "install": [
      "grey-haven-core@grey-haven-plugins",
      "my-custom-agent@my-custom-plugins"
    ]
  }
}
```

---

## 🎓 FAQ

### Q: Do I need the npm package at all?

**A**: No! The npm package (`@greyhaven/claude-code-config`) is **optional** in v2.0.0.

**What you MUST do**:
1. Clone Git repository ✅ Required
2. Add plugin marketplace to settings.json ✅ Required

**What is OPTIONAL**:
3. Install npm package for CLI utilities ⚠️ Optional

**Use npm package if you want**:
- `claude-config install-hooks` - Automated hook installation
- `claude-config setup-mcp` - MCP configuration wizard
- `claude-config create-project` - Project scaffolding
- `claude-config doctor` - Diagnostics

**Skip npm package if**:
- You only need plugins (agents, commands)
- You're comfortable manually copying hooks
- You don't need CLI utilities

### Q: Can I install plugins without Git?

**A**: No, in v2.0.0 the Git repository is required for plugins.

**Alternatives**:
1. Download ZIP from GitHub (not recommended, hard to update)
2. Wait for v1.x (deprecated, will not receive updates)

### Q: What happened to presets?

**A**: Presets are now **included in the Git repository**, not npm package.

**Location**: `grey-haven-plugins/.claude/presets/`

**Apply a preset manually**:
```bash
# Copy preset to your project
cp ~/grey-haven-plugins/.claude/presets/recommended.json ./.claude/settings.json
```

**Or use the CLI** (if you have npm package installed):
```bash
# Coming soon in v2.1.0
claude-config apply-preset recommended
```

### Q: How do I contribute plugins?

**A**: Fork the Git repository, add your plugin, submit PR!

**Process**:
```bash
# 1. Fork on GitHub
# https://github.com/greyhaven-ai/grey-haven-claude-code-config

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/grey-haven-claude-code-config.git

# 3. Create plugin
cd grey-haven-claude-code-config/grey-haven-plugins
mkdir my-plugin
cd my-plugin
# Add agents/, commands/, README.md, plugin.json

# 4. Test locally
# Update your settings.json to point to your fork

# 5. Submit PR
git add .
git commit -m "feat: add my-plugin with X agent"
git push
# Create PR on GitHub
```

### Q: Will v1.x still work?

**A**: Yes, but it's **deprecated** and won't receive updates.

**v1.x support timeline**:
- **Now - 3 months**: Active support (bug fixes)
- **3-6 months**: Passive support (critical security fixes only)
- **6+ months**: Unsupported (please migrate to v2.0.0)

**v1.x will remain on npm indefinitely**, but won't receive new features or plugins.

### Q: Can I use both v1.x and v2.0.0?

**A**: Not recommended, they conflict.

**If you must**:
- Use v1.x on one machine
- Use v2.0.0 on another machine
- Don't mix on same machine (hooks and settings.json will conflict)

### Q: What if I just want to update hooks?

**A**: Copy hooks from Git repository, skip npm package entirely.

```bash
# Clone repo
git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git ~/grey-haven-plugins

# Copy hooks
cp ~/grey-haven-plugins/.claude/hooks/*.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.py

# Done! No npm package needed.
```

---

## 📞 Getting Help

### GitHub Issues

**For bugs or feature requests**:
https://github.com/greyhaven-ai/grey-haven-claude-code-config/issues

**Before posting**:
1. Search existing issues
2. Include your OS, Node version, Python version
3. Attach relevant config files (`settings.json`, logs)

### Diagnostics

**Run doctor command** (if you have npm package):
```bash
claude-config doctor
```

**Output includes**:
- Python version
- Node version
- Hooks installation status
- Plugin marketplace configuration
- MCP server status
- Settings.json validation

**Manual diagnostics**:
```bash
# Check Python
python3 --version

# Check Node
node --version

# Check npm package
npm list -g @greyhaven/claude-code-config

# Check hooks
ls -la ~/.claude/hooks/

# Check settings
cat ~/.claude/settings.json | jq '.plugin'

# Check Git repository
ls ~/grey-haven-plugins/grey-haven-plugins/
```

---

## 🎉 Success Checklist

After migration, you should have:

- ✅ Git repository cloned to `~/grey-haven-plugins`
- ✅ `~/.claude/settings.json` or `~/.claude/settings.local.json` configured with plugin marketplace
- ✅ Hooks installed to `~/.claude/hooks/` (7 .py files)
- ✅ `/help` in Claude Code shows Grey Haven commands
- ✅ (Optional) npm package v2.0.0 installed globally
- ✅ (Optional) `claude-config --version` shows v2.0.0

**Test commands**:
```bash
# In Claude Code
/tdd-implement          # Should work
/code-review            # Should work
/security-scan          # Should work
/doc-generate-api       # Should work

# All 30+ commands should be available!
```

---

## 📚 Additional Resources

- **Architecture Plan**: [V2_ARCHITECTURE_PLAN.md](.claude/V2_ARCHITECTURE_PLAN.md)
- **Repository README**: [README.md](README.md)
- **Plugin Development Guide**: [PLUGIN_DEVELOPMENT.md](PLUGIN_DEVELOPMENT.md)
- **Hooks Documentation**: [.claude/hooks/README.md](.claude/hooks/README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

## 🚨 Breaking Changes Summary

| Feature | v1.x | v2.0.0 |
|---------|------|--------|
| **Plugin distribution** | npm package | Git repository |
| **Hooks installation** | npm package | npm package OR manual copy |
| **Presets** | `claude-config preset <name>` | Copy from Git repo |
| **Agents** | npm package | Git repository |
| **Commands** | npm package | Git repository |
| **CLI utilities** | npm package | npm package (optional) |
| **Package size** | ~2 MB | ~500 KB |
| **Update method** | `npm update` | `git pull` + `npm update` (optional) |

---

**Last Updated**: 2025-10-17
**Version**: 2.0.0
**Maintainer**: Grey Haven Studio

For questions or issues: https://github.com/greyhaven-ai/grey-haven-claude-code-config/issues
