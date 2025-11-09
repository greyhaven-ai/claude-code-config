# Knowledge Base Plugin

Ontological knowledge management system for capturing institutional memory, debugging sessions, architectural decisions, and team learnings in version-controlled Markdown with enforced metadata structure.

## Overview

Inspired by [kb-claude](https://github.com/alchemiststudiosDOTai/kb-claude), this plugin provides a comprehensive knowledge management system designed for engineering teams. It transforms scattered knowledge into a structured, searchable, and semantically organized institutional memory.

## Key Features

- **Ontological Organization**: 9 semantic types for knowledge categorization
- **Enforced Metadata**: YAML frontmatter with UUIDs, timestamps, and relations
- **Knowledge Graphs**: Visual relationship mapping and cluster analysis
- **Semantic Search**: Multi-dimensional search with relationship traversal
- **Validation**: Structural integrity and quality checks
- **Manifest Generation**: Automated indexes and catalogs
- **Git-Native**: Plain text Markdown for version control integration

## Semantic Types

Knowledge entries are organized into these ontological categories:

| Type | Directory | Purpose |
|------|-----------|---------|
| **metadata** | `.claude/kb/metadata/` | Component summaries, system overviews |
| **debug_history** | `.claude/kb/debug_history/` | Debugging sessions, investigations |
| **qa** | `.claude/kb/qa/` | Questions, answers, learning notes |
| **code_index** | `.claude/kb/code_index/` | File/module references, API docs |
| **patterns** | `.claude/kb/patterns/` | Reusable design patterns, best practices |
| **plans** | `.claude/kb/plans/` | Project plans, roadmaps |
| **cheatsheets** | `.claude/kb/cheatsheets/` | Quick references, command guides |
| **memory_anchors** | `.claude/kb/memory_anchors/` | Core concepts with persistent UUIDs |
| **other** | `.claude/kb/other/` | Uncategorized entries |

## Agents

### kb-entry-creator

Creates structured knowledge entries with proper metadata and semantic categorization.

**Use when**:
- Documenting debugging sessions
- Recording architectural decisions
- Capturing design patterns
- Creating Q&A entries
- Building code indexes

**Example**:
```
User: "I just fixed a memory leak in the worker pool. Document this for the team"
→ Uses kb-entry-creator to create structured debug_history entry
```

### kb-search-analyzer

Searches and synthesizes information across the knowledge base with relationship traversal.

**Use when**:
- Looking for past solutions
- Understanding system architecture
- Finding related knowledge
- Researching problem domains

**Example**:
```
User: "How does our authentication system work?"
→ Uses kb-search-analyzer to find and synthesize auth-related entries
```

### kb-ontology-mapper

Maps and visualizes knowledge base topology with graph analysis.

**Use when**:
- Understanding knowledge structure
- Finding orphaned entries
- Visualizing relationships
- Analyzing knowledge clusters

**Example**:
```
User: "Create a visual map of our authentication knowledge"
→ Uses kb-ontology-mapper to generate knowledge graph
```

### kb-validator

Validates knowledge base integrity with structural and metadata checks.

**Use when**:
- Before committing changes
- During knowledge base audits
- Ensuring quality standards
- Fixing structural issues

**Example**:
```
User: "Validate all KB entries before commit"
→ Uses kb-validator to check structure and metadata
```

### kb-manifest-generator

Generates comprehensive indexes, catalogs, and statistics.

**Use when**:
- Creating KB documentation
- Building searchable indexes
- Tracking knowledge growth
- Generating reports

**Example**:
```
User: "Generate an index of all knowledge entries"
→ Uses kb-manifest-generator to create comprehensive manifest
```

## Slash Commands

### /kb-create

Create a new knowledge base entry with guided prompts.

```bash
/kb-create                           # Interactive creation
/kb-create patterns                  # Create pattern entry
/kb-create debug_history "Fix timeout issue"  # Create with title
```

### /kb-search

Search knowledge base with semantic analysis.

```bash
/kb-search authentication            # Search for auth-related knowledge
/kb-search "timeout issues"          # Search phrase
/kb-search performance optimization  # Multi-keyword search
```

### /kb-list

List knowledge base entries with filtering.

```bash
/kb-list                            # Overview of all types
/kb-list patterns                   # List all patterns
/kb-list --recent                   # Recently updated entries
/kb-list --orphaned                 # Entries with no relations
```

### /kb-validate

Validate knowledge base structure and metadata.

```bash
/kb-validate                        # Comprehensive validation
/kb-validate --fix                  # Auto-fix issues when possible
```

### /kb-manifest

Generate knowledge base indexes and statistics.

```bash
/kb-manifest                        # Full index
/kb-manifest --type patterns        # Patterns manifest only
/kb-manifest --tags                 # Tag-based index
/kb-manifest --stats                # Statistics dashboard
```

## Knowledge Entry Structure

Every entry follows this structure:

```markdown
---
title: "Concise, descriptive title (60-80 chars)"
slug: "kebab-case-unique-identifier"
type: "semantic-category"
ontological_relations:
  - "[[related-entry-slug]]"
  - "[[another-related-entry]]"
tags:
  - "searchable-keyword"
  - "technology-name"
created_at: "2025-01-15T10:30:00Z"
updated_at: "2025-01-15T10:30:00Z"
uuid: "550e8400-e29b-41d4-a716-446655440000"
author: "team-member-name"
status: "draft | active | archived"
---

## Context
[Background and motivation]

## Problem/Question
[What is being addressed]

## Solution/Answer
[The knowledge being captured]

## Code Examples
\`\`\`language
// Relevant code snippets
\`\`\`

## References
- [External links]

## Lessons Learned
[Key takeaways]
```

## Workflow Examples

### Documenting a Bug Fix

```bash
# 1. Fix the bug
git commit -m "fix: resolve memory leak in worker pool"

# 2. Create knowledge entry
/kb-create debug_history

# Agent guides through:
# - Title: "Fixing Memory Leak in Worker Pool Using Weak References"
# - Tags: memory-leak, python, worker-pool, debugging
# - Relations: [[worker-pool-architecture]], [[python-memory-management]]
# - Content: Context, problem, solution, lessons learned

# 3. Entry created at:
# .claude/kb/debug_history/worker-pool-memory-leak-weak-refs.md
```

### Finding Past Solutions

```bash
# Search for timeout-related knowledge
/kb-search "timeout issues payment service"

# Agent returns:
# - 3 debug_history entries about timeouts
# - 2 patterns for timeout handling
# - 1 qa entry about timeout configuration
# - Synthesis of common solutions
# - Relationship graph showing connections
```

### Knowledge Base Audit

```bash
# Validate entire knowledge base
/kb-validate

# Report shows:
# - 8 issues found
# - 3 broken links
# - 1 duplicate slug
# - 2 type mismatches
# - 12 orphaned entries
# - Actionable fix recommendations
```

### Creating Knowledge Map

```bash
# Generate authentication knowledge graph
# User: "Map all authentication-related knowledge"

# Agent:
# 1. Searches for auth entries
# 2. Extracts ontological relations
# 3. Generates Mermaid diagram
# 4. Shows hub entries and clusters
# 5. Identifies knowledge gaps
```

## Integration with Claude Code

### Plugin Installation

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

### Pre-Commit Hook

Validate KB entries before commit:

```bash
#!/usr/bin/env python3
# .claude/hooks/kb-validator.py

import subprocess
import sys

result = subprocess.run(
    ["claude", "validate-kb"],
    capture_output=True
)

if result.returncode != 0:
    print("❌ KB validation failed:")
    print(result.stdout.decode())
    sys.exit(1)
```

## Best Practices

### Creating Entries

- **Be descriptive**: Titles should be searchable and clear
- **Tag generously**: Use 3-7 relevant tags
- **Link actively**: Connect to at least 1 related entry
- **Write for others**: Assume reader is unfamiliar with context
- **Include code**: Provide specific examples
- **Capture lessons**: What would you tell your future self?

### Maintaining Quality

- **Run validation regularly**: Before commits and weekly audits
- **Fix broken links**: Update or remove stale references
- **Archive obsolete entries**: Mark with `status: archived`
- **Update timestamps**: When making significant edits
- **Review orphans**: Link isolated entries or archive them

### Organizing Knowledge

- **Choose type carefully**: Semantic categorization is critical
- **Use memory_anchors**: For foundational concepts
- **Create patterns**: Extract reusable solutions
- **Document decisions**: Capture "why" in plans/metadata
- **Build clusters**: Group related knowledge with ontological links

### Searching Effectively

- **Start broad**: Search across all types first
- **Follow relations**: Traverse knowledge graphs
- **Use multiple keywords**: Combine terms for precision
- **Check multiple types**: Patterns + debug_history often together
- **Review manifests**: Browse indexes for discovery

## Comparison to kb-claude

| Feature | kb-claude (Rust CLI) | This Plugin |
|---------|---------------------|-------------|
| **Storage** | Plain Markdown + YAML | Plain Markdown + YAML |
| **Semantic Types** | 9 types | Same 9 types |
| **Metadata** | UUID, timestamps, relations | UUID, timestamps, relations |
| **Search** | CLI commands | Claude Code agents |
| **Validation** | Built-in validator | kb-validator agent |
| **Manifests** | Auto-generated | kb-manifest-generator |
| **Visualization** | Terminal output | Mermaid diagrams, graphs |
| **Integration** | Standalone CLI | Claude Code native |
| **Distribution** | Rust crates.io | Plugin marketplace |

**Advantages of this plugin**:
- Native Claude Code integration
- AI-powered search and synthesis
- Interactive knowledge creation
- Ontological graph analysis
- Rich visualizations (Mermaid)
- Contextual recommendations

**When to use kb-claude CLI**:
- Standalone knowledge management
- Non-Claude Code workflows
- Rust-based tooling preference
- CLI-only environments

## Roadmap

- [ ] Auto-linking based on content similarity
- [ ] Knowledge base statistics dashboard
- [ ] Temporal knowledge graphs (evolution over time)
- [ ] Export to various formats (PDF, HTML)
- [ ] Integration with documentation systems
- [ ] AI-suggested tags and relations
- [ ] Knowledge health metrics
- [ ] Collaborative editing workflows

## Contributing

To extend this plugin:

1. **Add new semantic types**: Update type enum and create directory
2. **Enhance agents**: Extend existing agents with new capabilities
3. **Create commands**: Add slash commands for workflows
4. **Improve validation**: Add new quality checks
5. **Build integrations**: Connect with external systems

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

## References

- [kb-claude GitHub](https://github.com/alchemiststudiosDOTai/kb-claude)
- [Grey Haven Plugin Marketplace](../README.md)
- [Claude Code Documentation](https://docs.claude.com/)

---

**Transform scattered knowledge into structured institutional memory.**
