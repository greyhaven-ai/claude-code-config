---
allowed-tools: Task
description: Create relationship between two knowledge entries
argument-hint: <entry1-slug> <entry2-slug> <relationship-type>
---
Create knowledge relationship: $ARGUMENTS
<ultrathink>
Knowledge gains power through connection. Isolated facts become insights when linked with purpose and meaning.
</ultrathink>
<megaexpertise type="ontology-specialist">
The assistant should use the knowledge-curator agent to create bidirectional relationships between entries with proper relationship typing.
</megaexpertise>
<context>
Arguments: $ARGUMENTS
Knowledge base path: .claude/knowledge/
Relationship types:
  - part-of: Entry is component of another
  - implements: Entry implements concept/pattern from another
  - references: Entry refers to another
  - contradicts: Entry conflicts with another (for tracking decisions)
  - supersedes: Entry replaces an older entry
</context>
<requirements>
- Parse entry slugs and relationship type
- Validate both entries exist
- Update YAML frontmatter in both entries
- Consider bidirectional linking appropriately
- Update manifest if needed
</requirements>
<actions>
1. Parse Arguments:
   - Extract entry1 slug
   - Extract entry2 slug
   - Extract relationship type (part-of, implements, references, contradicts, supersedes)
   - Validate relationship type is recognized

2. Launch Knowledge Curator Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the knowledge-curator agent.

   Prompt:
   "Create a relationship between knowledge entries:
   - Entry 1: [entry1-slug]
   - Entry 2: [entry2-slug]
   - Relationship: [entry1] [relationship-type] [entry2]

   Please:
   1. Find both entries in the knowledge base
   2. Validate they exist
   3. Update entry1's YAML frontmatter to add the relationship
   4. Determine if bidirectional linking is appropriate:
      - part-of → has-part (bidirectional)
      - implements → implemented-by (bidirectional)
      - references → optional bidirectional
      - supersedes → superseded-by (bidirectional)
   5. Update both files as needed
   6. Update the manifest
   7. Confirm the relationship was created

   Show the updated relationship graph for both entries."
   ```

3. Present Results:
   - Confirm relationship created
   - Show updated frontmatter
   - Display relationship graph
   - Suggest other potential relationships
</actions>
The assistant should make relationship creation seamless and ensure the knowledge graph remains consistent and meaningful.
