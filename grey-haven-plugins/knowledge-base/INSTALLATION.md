# Knowledge Base Plugin - Installation Guide

Complete installation instructions for the knowledge-base plugin.

## Prerequisites

- Claude Code installed and running
- Python 3.8+ (for optional ContextFrame memory features)
- Git (for repository management)

## Installation Steps

### 1. Clone or Update Grey Haven Plugins Repository

If you haven't already:

```bash
git clone https://github.com/greyhaven-studio/claude-code-config.git
cd claude-code-config
```

Or if you already have it:

```bash
cd claude-code-config
git pull origin main
```

### 2. Configure Claude Code Plugin Marketplace

Edit your `~/.claude/settings.json` (or your project's `.claude/settings.json`):

```json
{
  "plugin": {
    "marketplaces": [
      {
        "name": "grey-haven-plugins",
        "source": "/absolute/path/to/claude-code-config/grey-haven-plugins"
      }
    ],
    "install": [
      "knowledge-base@grey-haven-plugins"
    ]
  },
  "permissions": {
    "allow": [],
    "deny": [],
    "ask": []
  }
}
```

**Important**: Replace `/absolute/path/to/claude-code-config/grey-haven-plugins` with the actual absolute path on your system.

To find the absolute path:
```bash
cd claude-code-config/grey-haven-plugins
pwd
```

### 3. Restart Claude Code

After updating settings, restart Claude Code to load the plugin.

### 4. Verify Installation

In Claude Code, try a command:

```bash
/kb-manifest
```

If it works, the plugin is installed correctly!

---

## Optional: Install ContextFrame for Memory Features

The knowledge base works without ContextFrame, but memory features require it.

### Basic Installation

```bash
pip install contextframe
```

### Full Installation (Recommended)

```bash
pip install contextframe[embed,extract,enhance]
```

This includes:
- `embed`: Embedding generation (OpenAI, Anthropic, Cohere)
- `extract`: Document extraction (PDF, DOCX, HTML)
- `enhance`: LLM enhancement capabilities

### Configure Embedding Provider

#### Option A: OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

Edit `.claude/memory/config.json`:
```json
{
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "embedding_dimensions": 1536
}
```

#### Option B: Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Note: Anthropic doesn't provide embedding models directly. Consider using OpenAI or Voyage AI for embeddings.

#### Option C: No Embeddings (Basic Mode)

You can still use full-text search without embeddings:

```json
{
  "embedding_provider": "none",
  "auto_embed": false
}
```

---

## Optional: Install Graphviz for Visualizations

### macOS
```bash
brew install graphviz
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install graphviz
```

### Windows
Download from: https://graphviz.org/download/

Or use pip:
```bash
pip install graphviz
```

**Note**: If Graphviz is not available, visualizations will fall back to Mermaid diagrams.

---

## Directory Structure After Installation

Your project will have these directories after first use:

```
your-project/
├── .claude/
│   ├── settings.json          # Plugin configuration
│   ├── knowledge/             # Knowledge base (auto-created)
│   │   ├── metadata/
│   │   ├── patterns/
│   │   ├── code_index/
│   │   ├── qa/
│   │   ├── plans/
│   │   ├── concepts/
│   │   ├── memory_anchors/
│   │   └── manifest.md
│   └── memory/                # Memory storage (auto-created)
│       ├── contextframe.lance/
│       ├── embeddings/
│       └── config.json
```

---

## Configuration Options

### Plugin Configuration (settings.json)

```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/path/to/grey-haven-plugins"
    }],
    "install": [
      "knowledge-base@grey-haven-plugins"
    ]
  }
}
```

### Memory Configuration (.claude/memory/config.json)

See `examples/memory-config-example.json` for a complete configuration template.

Key settings:

```json
{
  "embedding_provider": "openai|anthropic|none",
  "embedding_model": "text-embedding-3-small",
  "embedding_dimensions": 1536,
  "search_default_k": 5,
  "auto_embed": true,
  "dataset_path": ".claude/memory/contextframe.lance"
}
```

---

## Verifying Installation

### Test Knowledge Base Commands

```bash
# Create an entry
/kb-add metadata "Test Entry"

# Search for it
/kb-search "test"

# Generate manifest
/kb-manifest
```

### Test Memory Commands (if ContextFrame installed)

```bash
# Commit to memory
/kb-memory-commit "Test memory commit"

# Recall from memory
/kb-memory-recall "test"
```

### Test Visualization (if Graphviz installed)

```bash
/kb-visualize
```

Check for output in `.claude/knowledge/ontology/`

---

## Troubleshooting

### Plugin Not Found

**Symptoms**: Commands like `/kb-add` show "command not found"

**Solutions**:
1. Check `settings.json` has correct absolute path
2. Restart Claude Code
3. Verify plugin directory exists:
   ```bash
   ls -la /path/to/grey-haven-plugins/knowledge-base/
   ```

### ContextFrame Import Error

**Symptoms**: "ContextFrame not installed" errors

**Solutions**:
```bash
pip install contextframe[embed]

# Verify installation
python -c "import contextframe; print(contextframe.__version__)"
```

### Embedding Generation Fails

**Symptoms**: "Failed to generate embeddings"

**Solutions**:
1. Check API key is set:
   ```bash
   echo $OPENAI_API_KEY
   ```
2. Verify provider in config:
   ```bash
   cat .claude/memory/config.json
   ```
3. Test API key:
   ```bash
   python -c "from openai import OpenAI; client = OpenAI(); print('OK')"
   ```

### Graphviz Not Found

**Symptoms**: "Graphviz not installed" or visualization fails

**Solutions**:
```bash
# Install Graphviz
brew install graphviz  # macOS
sudo apt install graphviz  # Linux

# Verify
dot -V
```

### Permission Errors

**Symptoms**: "Permission denied" when creating directories

**Solutions**:
```bash
# Check permissions
ls -la .claude/

# Fix permissions
chmod -R u+w .claude/
```

### Memory Store Corruption

**Symptoms**: "Failed to open Lance dataset"

**Solutions**:
```bash
# Backup and rebuild
mv .claude/memory/contextframe.lance .claude/memory/contextframe.lance.backup

# Memory will reinitialize on next use
/kb-memory-commit "Rebuilding memory store"
```

---

## Uninstallation

### Remove Plugin

Edit `~/.claude/settings.json` and remove:

```json
"install": [
  "knowledge-base@grey-haven-plugins"  // Remove this line
]
```

Restart Claude Code.

### Remove Data

To remove all knowledge and memory data:

```bash
# Backup first!
tar -czf claude-kb-backup.tar.gz .claude/knowledge .claude/memory

# Remove
rm -rf .claude/knowledge
rm -rf .claude/memory
```

### Uninstall Dependencies

```bash
pip uninstall contextframe lance pyarrow graphviz
```

---

## Upgrading

### Update Plugin

```bash
cd claude-code-config
git pull origin main
```

Restart Claude Code.

### Update ContextFrame

```bash
pip install --upgrade contextframe[embed,extract,enhance]
```

### Migrate Data (if needed)

Data migrations are typically not required. If needed, instructions will be in release notes.

---

## Getting Help

- **Plugin Issues**: Create issue at https://github.com/greyhaven-studio/claude-code-config/issues
- **ContextFrame Issues**: See https://github.com/autocontext/contextframe
- **Claude Code**: See https://docs.anthropic.com/claude-code

---

## Next Steps

After installation:
1. Read the [Quick Start Guide](examples/QUICKSTART.md)
2. Review [README](README.md) for full documentation
3. Check out [example knowledge entry](examples/sample-knowledge-entry.md)
4. Start documenting your project!

Happy knowledge building! 📚🧠
