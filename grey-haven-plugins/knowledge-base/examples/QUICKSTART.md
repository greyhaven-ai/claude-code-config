# Knowledge Base Plugin - Quick Start Guide

Get started with the knowledge-base plugin in 5 minutes.

## Step 1: Install the Plugin

Add to `.claude/settings.json`:

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

Restart Claude Code to load the plugin.

## Step 2: Create Your First Knowledge Entry

Document an architectural decision:

```bash
/kb-add metadata "API Authentication Strategy"
```

Claude will:
- Create `.claude/knowledge/metadata/api-authentication-strategy.md`
- Generate UUID and timestamps
- Add YAML frontmatter
- Suggest related entries

Edit the file to add your content!

## Step 3: Add a Design Pattern

```bash
/kb-add patterns "Retry Pattern with Exponential Backoff"
```

## Step 4: Search Your Knowledge

```bash
/kb-search "authentication"
```

Returns all entries related to authentication.

## Step 5: Link Related Entries

```bash
/kb-relate api-authentication-strategy retry-pattern-exponential-backoff implements
```

This creates a relationship: "API Authentication Strategy" implements "Retry Pattern".

## Step 6: Generate a Manifest

```bash
/kb-manifest
```

Creates `.claude/knowledge/manifest.md` with a complete index of your knowledge base.

## Step 7 (Optional): Install ContextFrame for Memory

For long-term memory with semantic search:

```bash
pip install contextframe[embed]

# Set your API key for embeddings
export OPENAI_API_KEY="sk-..."
```

## Step 8 (Optional): Commit to Memory

After implementing a feature:

```bash
/kb-memory-commit "Completed OAuth2 authentication with JWT tokens"
```

## Step 9 (Optional): Recall Memories

When you need historical context:

```bash
/kb-memory-recall "authentication decisions we made"
```

## Step 10 (Optional): Visualize Your Knowledge

```bash
# Install Graphviz first
brew install graphviz  # or: sudo apt install graphviz

# Generate graph
/kb-visualize
```

Creates `.claude/knowledge/ontology/ontology.png` showing your knowledge structure.

---

## Common Workflows

### During Feature Development

1. **Before Starting**:
   ```bash
   /kb-search "feature-related-topic"
   /kb-memory-recall "type:implementation similar-feature"
   ```

2. **During Implementation**:
   ```bash
   /kb-add patterns "New Pattern Discovered"
   /kb-add code_index "Important Module API"
   ```

3. **After Completion**:
   ```bash
   /kb-memory-commit "Completed feature X with pattern Y"
   /kb-manifest  # Update the index
   ```

### During Bug Fixing

1. **Search for Similar Issues**:
   ```bash
   /kb-search "bug-related-keywords"
   /kb-memory-recall "type:incident similar-symptoms"
   ```

2. **Document the Fix**:
   ```bash
   /kb-add qa "How to Fix [Problem]"
   /kb-memory-commit "Fixed bug in [component]"
   ```

### During Architectural Planning

1. **Review Existing Knowledge**:
   ```bash
   /kb-manifest
   /kb-visualize
   ```

2. **Document Decisions**:
   ```bash
   /kb-add metadata "Architecture Decision: [Topic]"
   /kb-add plans "Q4 Roadmap"
   ```

3. **Link Related Concepts**:
   ```bash
   /kb-relate decision1 decision2 contradicts
   /kb-relate new-plan old-plan supersedes
   ```

---

## Tips for Success

### 1. Document Early and Often
Don't wait until the end of a project. Document decisions when you make them.

### 2. Use Descriptive Titles
"OAuth2 JWT Implementation" is better than "Auth stuff"

### 3. Tag Comprehensively
More tags = easier to find later. Include:
- Technology names (postgres, redis, react)
- Domains (authentication, payment, api)
- Types (security, performance, architecture)

### 4. Cross-Link Related Entries
Use `[[slug]]` syntax and `/kb-relate` to build a knowledge graph

### 5. Update Rather Than Duplicate
Use `/kb-search` before creating new entries to avoid duplicates

### 6. Regular Manifests
Run `/kb-manifest` weekly to keep your index fresh

### 7. Visualize Periodically
Run `/kb-visualize` monthly to identify knowledge gaps

---

## Knowledge Entry Types - When to Use

| Type | Use For | Example |
|------|---------|---------|
| **metadata** | Architectural decisions, configuration, system metadata | "Database Choice: PostgreSQL vs MongoDB" |
| **patterns** | Design patterns, coding conventions, best practices | "Circuit Breaker Pattern" |
| **code_index** | API documentation, module guides, code references | "User Service API Reference" |
| **qa** | Questions & answers, troubleshooting, how-tos | "How to Debug Memory Leaks" |
| **plans** | Project plans, roadmaps, feature specifications | "Q4 2025 Feature Roadmap" |
| **concepts** | Domain concepts, terminology, mental models | "Event Sourcing Explained" |
| **memory_anchors** | Critical learnings, important context, project history | "Why We Migrated from REST to GraphQL" |

---

## Memory Commit Types - When to Use

| Type | Use For | Example |
|------|---------|---------|
| **implementation** | Completed features, code implementations | "Completed payment processing integration" |
| **decision** | Architecture or design decisions | "Decided to use microservices over monolith" |
| **incident** | Bug resolutions, incident responses | "Fixed race condition in checkout flow" |
| **learning** | New patterns discovered, lessons learned | "Discovered better approach to rate limiting" |
| **milestone** | Project milestones, major achievements | "Reached 1M users, system performed well" |

---

## Troubleshooting

### Commands Not Found

Restart Claude Code after installing the plugin.

### ContextFrame Errors

```bash
pip install contextframe[embed]
```

Memory features require ContextFrame. Knowledge base works without it.

### Graphviz Visualization Fails

```bash
brew install graphviz  # macOS
sudo apt install graphviz  # Linux
```

Or the system will fall back to Mermaid diagrams.

### No Search Results

Check if knowledge base exists:
```bash
ls -la .claude/knowledge/
```

If empty, create your first entry with `/kb-add`.

---

## Next Steps

1. **Read the full README**: `grey-haven-plugins/knowledge-base/README.md`
2. **Explore examples**: Check out `examples/sample-knowledge-entry.md`
3. **Configure memory**: Copy `examples/memory-config-example.json` to `.claude/memory/config.json`
4. **Start documenting**: Make knowledge capture a habit!

---

## Getting Help

- Plugin issues: Check the README
- ContextFrame issues: https://github.com/autocontext/contextframe
- Grey Haven plugins: https://github.com/your-org/grey-haven-plugins

Happy knowledge building! 📚🧠
