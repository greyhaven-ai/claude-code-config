# Knowledge Base Plugin

Ontological knowledge management with long-term memory storage for Claude Code projects.

## Overview

The **knowledge-base** plugin combines structured knowledge organization (inspired by [kb-claude](https://github.com/alchemiststudiosDOTai/kb-claude)) with long-term memory storage using [ContextFrame](https://github.com/autocontext/contextframe). It provides a comprehensive system for capturing, organizing, and retrieving project knowledge with semantic search capabilities.

### Key Features

#### 📚 Structured Knowledge Base
- **Type-based organization**: Categorize knowledge as metadata, patterns, code_index, qa, plans, concepts, or memory_anchors
- **YAML frontmatter**: Rich metadata with UUIDs, tags, timestamps, and status tracking
- **Cross-linking**: Wiki-style `[[slug]]` references and explicit relationship types
- **Auto-generated manifests**: Comprehensive indexes of all knowledge

#### 🧠 Long-Term Memory Storage
- **ContextFrame integration**: Version-controlled, columnar storage with Lance
- **Semantic search**: Vector embeddings for intelligent memory recall
- **Full-text search**: BM25 search across all memory content
- **Memory commits**: Capture context at key moments (implementations, decisions, incidents, learnings, milestones)
- **Relationship tracking**: Link memories to knowledge entries

#### 🕸️ Ontological Visualization
- **Knowledge graphs**: Visual maps of relationships using Graphviz or Mermaid
- **Gap analysis**: Identify underdocumented areas and isolated entries
- **Relationship discovery**: Suggest meaningful connections
- **Density analysis**: Assess knowledge coverage by category and topic

## Installation

### 1. Install the Plugin

Add to your `.claude/settings.json`:

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

### 2. Optional: Install ContextFrame (for long-term memory)

```bash
# Basic installation
pip install contextframe

# With full features (embeddings, extraction, enhancement)
pip install contextframe[embed,extract,enhance]

# Individual extras:
# pip install contextframe[embed]    # OpenAI/Anthropic embeddings
# pip install contextframe[extract]  # Document extraction
# pip install contextframe[enhance]  # LLM enhancement
# pip install contextframe[serve]    # MCP server
```

**Note**: Knowledge base features work without ContextFrame. Memory features require ContextFrame installation.

### 3. Optional: Install Graphviz (for visualization)

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Or use pip
pip install graphviz
```

## Quick Start

### Creating Knowledge Entries

```bash
# Add a design pattern
/kb-add patterns "Retry Pattern for API Calls"

# Add architectural metadata
/kb-add metadata "Event Sourcing Architecture Decision"

# Add Q&A
/kb-add qa "How to Handle Database Migrations"

# Add code documentation
/kb-add code_index "Authentication Service API"
```

### Searching Knowledge

```bash
# Search across all entries
/kb-search "authentication"

# Search within a category
/kb-search "patterns:retry"

# Search by tags
/kb-search "tag:security"
```

### Creating Relationships

```bash
# Link entries together
/kb-relate auth-architecture oauth2-pattern implements

# Show hierarchy
/kb-relate user-service auth-architecture part-of

# Reference related concepts
/kb-relate rate-limiting auth-endpoints references
```

### Committing to Long-Term Memory

```bash
# After implementing a feature
/kb-memory-commit "Completed OAuth2 authentication with JWT tokens"

# After making a decision
/kb-memory-commit "Decided on PostgreSQL over MongoDB for user data"

# After resolving an incident
/kb-memory-commit "Fixed race condition in payment processing"
```

### Recalling Memories

```bash
# Semantic search across memories
/kb-memory-recall "authentication decisions"

# Find past implementations
/kb-memory-recall "type:implementation payment"

# Recall incidents
/kb-memory-recall "type:incident database"
```

### Generating Manifests and Visualizations

```bash
# Generate comprehensive manifest
/kb-manifest

# Visualize entire knowledge graph
/kb-visualize

# Visualize specific category
/kb-visualize patterns
```

## Directory Structure

After initialization, your project will have:

```
.claude/
├── knowledge/              # Structured knowledge base
│   ├── metadata/          # System metadata, architectural decisions
│   ├── qa/                # Questions & answers, troubleshooting
│   ├── code_index/        # Code references, API documentation
│   ├── patterns/          # Design patterns, best practices
│   ├── plans/             # Project plans, roadmaps
│   ├── concepts/          # Domain concepts, terminology
│   ├── memory_anchors/    # Critical learnings, important context
│   ├── ontology/          # Generated graphs and visualizations
│   └── manifest.md        # Auto-generated index
└── memory/                # Long-term memory storage (requires ContextFrame)
    ├── contextframe.lance/  # Lance dataset
    ├── embeddings/         # Embedding cache
    └── config.json         # Memory configuration
```

## Knowledge Entry Format

Each entry is a Markdown file with YAML frontmatter:

```markdown
---
uuid: 550e8400-e29b-41d4-a716-446655440000
type: patterns
title: Retry Pattern for API Calls
tags: [api, resilience, retry, error-handling]
created: 2025-11-10T10:30:00Z
updated: 2025-11-10T10:30:00Z
status: active
relations:
  - slug: circuit-breaker-pattern
    type: references
  - slug: api-error-handling
    type: implements
---

# Retry Pattern for API Calls

## Overview
Implements automatic retry logic for failed API requests with exponential backoff.

## Implementation
[Your content here]

## Related Concepts
- [[circuit-breaker-pattern]]
- [[api-error-handling]]
```

## Memory Record Format

Memories stored in ContextFrame:

```json
{
  "uuid": "770e8400-e29b-41d4-a716-446655440222",
  "type": "document",
  "content": "Implemented OAuth2 authentication system with JWT tokens...",
  "metadata": {
    "author": "claude-code",
    "project": "my-project",
    "commit_type": "implementation",
    "tags": ["authentication", "oauth2", "jwt", "security"],
    "component": "auth-service"
  },
  "relationships": [
    {
      "target_uuid": "knowledge-entry-uuid",
      "rel_type": "references"
    }
  ],
  "status": "active",
  "embedding": [0.1, 0.2, ...],
  "created_at": "2025-11-10T10:30:00Z",
  "modified_at": "2025-11-10T10:30:00Z"
}
```

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/kb-add` | Create new knowledge entry | `/kb-add patterns "Retry Pattern"` |
| `/kb-search` | Search knowledge base | `/kb-search "authentication"` |
| `/kb-relate` | Link two entries | `/kb-relate entry1 entry2 implements` |
| `/kb-memory-commit` | Store context in memory | `/kb-memory-commit "Completed feature X"` |
| `/kb-memory-recall` | Search memories | `/kb-memory-recall "caching decisions"` |
| `/kb-manifest` | Generate manifest | `/kb-manifest` |
| `/kb-visualize` | Create knowledge graph | `/kb-visualize patterns` |

## Available Agents

### knowledge-curator
Expert at creating and organizing structured knowledge entries with ontological relationships.

**Use when**: Documenting decisions, capturing patterns, indexing code, recording Q&A.

### memory-architect
Expert at long-term context storage and retrieval using ContextFrame with semantic search.

**Use when**: Committing implementations, storing decisions, recalling past context, searching memories.

### ontology-builder
Expert at mapping and visualizing knowledge relationships with gap analysis.

**Use when**: Understanding knowledge structure, identifying documentation gaps, creating visual graphs.

## Configuration

### Memory Configuration

Create `.claude/memory/config.json`:

```json
{
  "embedding_provider": "openai",
  "embedding_model": "text-embedding-3-small",
  "embedding_dimensions": 1536,
  "search_default_k": 5,
  "auto_embed": true,
  "dataset_path": ".claude/memory/contextframe.lance"
}
```

### Embedding Providers

#### OpenAI
```python
export OPENAI_API_KEY="your-key"
```

#### Anthropic
```python
export ANTHROPIC_API_KEY="your-key"
```

## Relationship Types

- **part-of**: Entry is component of another (e.g., "User Service" part-of "Service Architecture")
- **implements**: Entry implements concept/pattern (e.g., "Auth Service" implements "OAuth2 Pattern")
- **references**: Entry refers to another (e.g., "API Docs" references "Authentication")
- **contradicts**: Entry conflicts with another (useful for tracking decision changes)
- **supersedes**: Entry replaces older entry (e.g., "New Auth" supersedes "Old Auth")

## Memory Commit Types

- **implementation**: Feature or code implementation completed
- **decision**: Architectural or design decision made
- **incident**: Bug, issue, or incident resolved
- **learning**: New knowledge or pattern discovered
- **milestone**: Project milestone or major achievement

## Best Practices

### Knowledge Base

1. **Create entries early**: Document decisions when they're made, not later
2. **Use descriptive titles**: Make entries discoverable through search
3. **Tag comprehensively**: Include all relevant searchable terms
4. **Cross-link liberally**: Connect related concepts for navigation
5. **Update, don't duplicate**: Keep single source of truth
6. **Use appropriate types**: Choose the right category for findability
7. **Mark status**: Archive or deprecate outdated entries

### Long-Term Memory

1. **Commit at milestones**: After implementations, decisions, or resolutions
2. **Comprehensive context**: Capture enough detail for future understanding
3. **Rich metadata**: Tag thoroughly for future retrieval
4. **Link to knowledge**: Connect memories to knowledge base entries
5. **Use embeddings**: Enable semantic search for better recall
6. **Regular commits**: Don't wait until project end
7. **Status management**: Archive outdated memories

## Workflow Integration

### During Development
1. Document architectural decisions → `/kb-add metadata`
2. Capture design patterns → `/kb-add patterns`
3. Link related concepts → `/kb-relate`
4. Commit implementations → `/kb-memory-commit`

### During Debugging
1. Search for similar issues → `/kb-search`
2. Recall past solutions → `/kb-memory-recall`
3. Document resolution → `/kb-add qa`
4. Commit incident details → `/kb-memory-commit`

### During Planning
1. Review existing knowledge → `/kb-manifest`
2. Visualize architecture → `/kb-visualize`
3. Identify gaps → Check gap analysis
4. Document plans → `/kb-add plans`

## Troubleshooting

### ContextFrame Not Found

If you see "ContextFrame not installed":

```bash
pip install contextframe[embed]
```

Memory features require ContextFrame. Knowledge base features work independently.

### Graphviz Not Available

If visualization fails:

```bash
# Install Graphviz
brew install graphviz  # macOS
sudo apt install graphviz  # Linux

# Or the visualization will fall back to Mermaid diagrams
```

### No Embeddings Generated

Check your API keys:

```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."

# For Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or install embedding extras:

```bash
pip install contextframe[embed]
```

## Examples

See the `examples/` directory for:
- Sample knowledge entries
- Memory commit examples
- Configuration templates
- Visualization samples

## Credits

This plugin combines concepts from:
- **[kb-claude](https://github.com/alchemiststudiosDOTai/kb-claude)**: Structured, ontological knowledge base management
- **[ContextFrame](https://github.com/autocontext/contextframe)**: Long-term memory storage with semantic search

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

## Contributing

Issues and contributions welcome! This plugin is part of the Grey Haven Plugin Marketplace.
