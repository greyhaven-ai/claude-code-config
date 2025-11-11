---
allowed-tools: Task
description: Generate or update knowledge base manifest with comprehensive index
argument-hint: [--refresh]
---
Generate knowledge base manifest: $ARGUMENTS
<ultrathink>
An index transforms chaos into cosmos. The manifest is the map that makes the territory navigable.
</ultrathink>
<megaexpertise type="knowledge-curator">
The assistant should use the knowledge-curator agent to scan all entries and generate a comprehensive, organized manifest document.
</megaexpertise>
<context>
Arguments: $ARGUMENTS
Knowledge base path: .claude/knowledge/
Manifest location: .claude/knowledge/manifest.md
Categories: metadata, qa, code_index, patterns, plans, concepts, memory_anchors
</context>
<requirements>
- Scan all knowledge entries across categories
- Extract metadata (title, tags, updated date, status)
- Organize by category with tables
- Include statistics and summary
- Provide quick navigation links
- Mark archived/deprecated entries
- Show relationship counts
</requirements>
<actions>
1. Launch Knowledge Curator Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the knowledge-curator agent.

   Prompt:
   "Generate a comprehensive knowledge base manifest.

   Please:
   1. Scan all entries in .claude/knowledge/ across all categories
   2. For each entry, extract:
      - UUID, title, type, tags
      - Status (active, archived, deprecated)
      - Created and updated timestamps
      - Relationship count
   3. Generate statistics:
      - Total entries by category
      - Total relationships
      - Most tagged topics
      - Recently updated entries
   4. Create manifest.md with structure:
      # Knowledge Base Manifest

      Last Updated: [timestamp]

      ## Summary Statistics
      - Total Entries: X
      - Active: X | Archived: X | Deprecated: X
      - Total Relationships: X
      - Most Common Tags: [top 5]

      ## Metadata (X entries)
      | Title | Tags | Updated | Status |
      |-------|------|---------|--------|
      | [Entry] | tag1, tag2 | 2025-11-10 | active |

      ## Patterns (X entries)
      [Similar table]

      [... for each category]

      ## Recently Updated (Last 7 days)
      [List of recently modified entries]

      ## Navigation Tips
      - Search by tag: /kb-search tag:tagname
      - View relationships: /kb-visualize
      - Add entry: /kb-add type title
   5. Write manifest to .claude/knowledge/manifest.md
   6. Provide summary of findings"
   ```

2. Present Results:
   - Manifest location
   - Key statistics
   - Recent changes
   - Navigation links
</actions>
The assistant should create a manifest that serves as both an index and a dashboard, giving instant insight into the knowledge base's structure and content.
