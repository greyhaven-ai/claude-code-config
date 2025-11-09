---
allowed-tools: Bash, Grep, Read, Task
description: Search knowledge base with semantic analysis and relationship traversal
argument-hint: <query>
---
Search knowledge base: $ARGUMENTS

<context>
Perform semantic search across knowledge base entries, analyzing titles, tags, relations, and content. Synthesize findings and provide relationship context.
</context>

<requirements>
- Multi-dimensional search (title, tags, content, relations)
- Rank results by relevance
- Follow ontological links
- Synthesize coherent findings
- Identify knowledge patterns
</requirements>

<actions>
1. Parse search query: $ARGUMENTS
2. Use kb-search-analyzer agent for comprehensive search
3. Present results with relationship context
4. Suggest related entries
5. Offer to create entry if knowledge gap found
</actions>

Launch kb-search-analyzer agent to perform semantic search and synthesis.
