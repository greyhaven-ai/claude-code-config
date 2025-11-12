---
allowed-tools: Task
description: Recall relevant memories from long-term storage using semantic search
argument-hint: <query>
---
Recall memories: $ARGUMENTS
<ultrathink>
The past informs the present. Memories recalled at the right moment become superpowers for decision-making.
</ultrathink>
<megaexpertise type="memory-architect">
The assistant should use the memory-architect agent to perform semantic search across stored memories, returning the most relevant historical context.
</megaexpertise>
<context>
Query: $ARGUMENTS
Memory store path: .claude/memory/
Current directory: !`pwd`
Search types available: semantic (vector), full-text (BM25), metadata (filters)
</context>
<requirements>
- Perform semantic search if embeddings available
- Fall back to full-text search otherwise
- Support metadata filtering (type, tags, date range)
- Return ranked results with relevance scores
- Show summaries with links to full content
- Suggest related memories
</requirements>
<actions>
1. Parse Query:
   - Check for filters: "type:decision caching" or just "caching"
   - Extract search terms and metadata filters

2. Launch Memory Architect Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the memory-architect agent.

   Prompt:
   "Search long-term memory for: $ARGUMENTS

   Please:
   1. Check if ContextFrame is installed and memory store exists
   2. If available, perform semantic search using vector embeddings
   3. Otherwise, use BM25 full-text search
   4. Apply any metadata filters (type, tags, status, date range)
   5. Rank results by relevance score
   6. For top 5 results, show:
      - Title/summary (first 2 lines)
      - Memory type and date
      - Tags and components
      - Relevance score
      - UUID for retrieval
   7. Provide full content for the most relevant result
   8. Suggest related memories or knowledge entries

   If ContextFrame is not installed, provide instructions for installation."
   ```

3. Present Results:
   - Number of memories found
   - Top results with relevance scores
   - Full content of most relevant memory
   - Related suggestions
   - Links to knowledge base entries
</actions>
The assistant should make memory recall feel like having a knowledgeable colleague who remembers everything, surfacing the most relevant historical context instantly.
