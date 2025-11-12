---
allowed-tools: Task
description: Add new knowledge entry to the knowledge base with structured metadata and relationships
argument-hint: <type> <title>
---
Add knowledge entry: $ARGUMENTS
<ultrathink>
Knowledge captured is knowledge preserved. Every important decision, pattern, or learning deserves a permanent home in the knowledge base where it can be discovered and connected.
</ultrathink>
<megaexpertise type="knowledge-curator">
The assistant should use the knowledge-curator agent to create structured, well-organized knowledge entries with proper categorization, tagging, and relationship mapping.
</megaexpertise>
<context>
Arguments: $ARGUMENTS
Working directory: !`pwd`
Knowledge base exists: !`test -d .claude/knowledge && echo "yes" || echo "no"`
Available types: metadata, qa, code_index, patterns, plans, concepts, memory_anchors
</context>
<requirements>
- Parse type and title from arguments
- Use knowledge-curator agent for entry creation
- Ensure proper YAML frontmatter with UUID, timestamps
- Auto-detect related entries for cross-linking
- Update manifest after creation
- Provide file path for easy access
</requirements>
<actions>
1. Parse Arguments:
   - Extract type (first argument)
   - Extract title (remaining arguments)
   - Validate type is one of: metadata, qa, code_index, patterns, plans, concepts, memory_anchors

2. Launch Knowledge Curator Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the knowledge-curator agent.

   Prompt:
   "Create a new knowledge base entry with the following details:
   - Type: [extracted type]
   - Title: [extracted title]

   Please:
   1. Search for related existing entries
   2. Generate proper YAML frontmatter with UUID and timestamps
   3. Create the markdown file in the appropriate category directory
   4. Suggest cross-links to related entries
   5. Update the knowledge base manifest
   6. Provide the file path and next steps"
   ```

3. Present Results:
   - Show the created entry path
   - List detected relationships
   - Suggest next actions (add content, link entries)
</actions>
The assistant should make knowledge capture effortless and ensure all entries are properly structured, searchable, and connected.
