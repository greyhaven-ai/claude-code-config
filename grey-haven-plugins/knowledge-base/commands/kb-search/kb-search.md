---
allowed-tools: Task
description: Search the knowledge base for entries matching query, tags, or type
argument-hint: <query>
---
Search knowledge base: $ARGUMENTS
<ultrathink>
Knowledge is only valuable if it can be found. A well-indexed, searchable knowledge base transforms scattered documentation into accessible wisdom.
</ultrathink>
<megaexpertise type="knowledge-curator">
The assistant should use the knowledge-curator agent to perform comprehensive searches across all knowledge entries, returning relevant results ranked by relevance.
</megaexpertise>
<context>
Query: $ARGUMENTS
Knowledge base path: .claude/knowledge/
Current directory: !`pwd`
Categories available: metadata, qa, code_index, patterns, plans, concepts, memory_anchors
</context>
<requirements>
- Search across titles, tags, content, and relationships
- Support filtering by type (e.g., "patterns:retry" searches only patterns)
- Return ranked results with context snippets
- Show file paths for easy navigation
- Suggest related entries
</requirements>
<actions>
1. Parse Query:
   - Check for type filter: "type:query" or just "query"
   - Extract search terms

2. Launch Knowledge Curator Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the knowledge-curator agent.

   Prompt:
   "Search the knowledge base for: $ARGUMENTS

   Please:
   1. Search across entry titles, tags, and content
   2. Check YAML frontmatter for matching metadata
   3. Find entries with related tags
   4. Rank results by relevance
   5. Show title, type, tags, and content snippet for each result
   6. Provide file paths for easy access
   7. Suggest related entries that might also be relevant

   Present results in a clear, scannable format with the most relevant entries first."
   ```

3. Present Results:
   - Number of results found
   - Top results with snippets
   - File paths
   - Related suggestions
</actions>
The assistant should make knowledge discovery fast and intuitive, surfacing the most relevant entries with enough context to determine usefulness.
