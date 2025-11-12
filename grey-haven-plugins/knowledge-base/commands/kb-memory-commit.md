---
allowed-tools: Task
description: Commit current context to long-term memory with semantic embeddings
argument-hint: <context-description>
---
Commit to long-term memory: $ARGUMENTS
<ultrathink>
Memory transforms experience into wisdom. What we remember shapes what we can imagine and achieve.
</ultrathink>
<megaexpertise type="memory-architect">
The assistant should use the memory-architect agent to capture and store context in ContextFrame with proper metadata, embeddings, and relationships.
</megaexpertise>
<context>
Context description: $ARGUMENTS
Current directory: !`pwd`
Recent git commits: !`git log --oneline -5 2>/dev/null || echo "No git history"`
Memory store path: .claude/memory/
Commit types: implementation, decision, incident, learning, milestone
</context>
<requirements>
- Capture comprehensive context summary
- Generate semantic embeddings if available
- Link to related knowledge base entries
- Include git context (commits, branch, files)
- Tag appropriately for future retrieval
- Store in ContextFrame with proper metadata
</requirements>
<actions>
1. Analyze Current Context:
   - Recent git activity
   - Changed files
   - Related knowledge entries
   - Session activities

2. Determine Memory Type:
   - implementation: Feature or code implementation
   - decision: Architectural or design decision
   - incident: Bug, issue, or incident resolution
   - learning: New knowledge or pattern discovered
   - milestone: Project milestone or major achievement

3. Launch Memory Architect Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the memory-architect agent.

   Prompt:
   "Commit the following context to long-term memory:
   Description: $ARGUMENTS

   Please:
   1. Analyze recent git commits and changes
   2. Identify the memory type (implementation, decision, incident, learning, or milestone)
   3. Create a comprehensive context summary (2-5 paragraphs)
   4. Extract relevant tags, components, and metadata
   5. Search for related knowledge base entries to link
   6. Create a ContextFrame record with:
      - UUID
      - Content summary
      - Metadata (type, tags, component, git info)
      - Relationships to knowledge entries
      - Status: active
   7. Generate semantic embedding if embedding service is configured
   8. Store in .claude/memory/contextframe.lance
   9. Confirm storage and provide UUID for future reference

   If ContextFrame is not installed, provide instructions for installation."
   ```

4. Present Results:
   - Memory UUID
   - Commit type and tags
   - Embedding status
   - Linked knowledge entries
   - Storage confirmation
</actions>
The assistant should make memory commits comprehensive yet efficient, ensuring critical context is preserved with rich metadata for future semantic retrieval.
