---
allowed-tools: Write, Bash, Read, Task
description: Generate knowledge base manifest with indexes and statistics
argument-hint: [--type <type>] [--tags] [--stats]
---
Generate knowledge base manifest: $ARGUMENTS

<context>
Create comprehensive indexes, catalogs, and statistics for the knowledge base.
</context>

<requirements>
- Generate master index
- Create type-specific manifests
- Build tag-based indexes
- Calculate statistics
- Identify knowledge trends
- Generate visual knowledge maps
</requirements>

<actions>
1. Use kb-manifest-generator agent
2. Generate requested manifests:
   - Full index (default)
   - Type-specific (if --type specified)
   - Tag index (if --tags)
   - Statistics dashboard (if --stats)
3. Write manifest to .claude/kb/INDEX.md
4. Display summary
</actions>

Launch kb-manifest-generator agent to create comprehensive knowledge base documentation.
