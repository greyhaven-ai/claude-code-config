---
allowed-tools: Write, Bash, Task
description: Create a new knowledge base entry with guided prompts and validation
argument-hint: [type] [title]
---
Create knowledge base entry: $ARGUMENTS

<context>
You are creating a new knowledge base entry. The kb-entry-creator agent will guide you through proper metadata structure, semantic categorization, and ontological linking.
</context>

<requirements>
- Determine semantic type (metadata, debug_history, qa, code_index, patterns, plans, cheatsheets, memory_anchors, other)
- Generate UUID and timestamps
- Extract relevant tags from content
- Identify ontological relations
- Validate YAML structure
- Create entry in correct directory
</requirements>

<actions>
1. If type/title provided in $ARGUMENTS, use them; otherwise ask user
2. Use kb-entry-creator agent to create structured entry
3. Validate entry with kb-validator
4. Commit to git with semantic message: `docs(kb): add {type} entry for {title}`
</actions>

Launch kb-entry-creator agent to create a structured knowledge entry with proper metadata and semantic organization.
