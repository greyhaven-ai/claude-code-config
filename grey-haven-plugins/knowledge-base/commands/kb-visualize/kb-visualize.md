---
allowed-tools: Task
description: Generate visual ontology graph showing knowledge relationships and structure
argument-hint: [type-filter]
---
Visualize knowledge ontology: $ARGUMENTS
<ultrathink>
A picture is worth a thousand links. Visualization reveals patterns invisible in linear text, making the implicit explicit.
</ultrathink>
<megaexpertise type="ontology-builder">
The assistant should use the ontology-builder agent to create visual knowledge graphs using Graphviz or Mermaid, with optional filtering by category.
</megaexpertise>
<context>
Filter: $ARGUMENTS
Knowledge base path: .claude/knowledge/
Output path: .claude/knowledge/ontology/
Available filters: metadata, qa, code_index, patterns, plans, concepts, memory_anchors, or "all"
</context>
<requirements>
- Parse all knowledge entries and relationships
- Build graph data structure
- Generate visual representation (Graphviz DOT or Mermaid)
- Color-code by entry type
- Show relationship types with different edge styles
- Perform gap analysis
- Provide actionable insights
- Save to file for viewing
</requirements>
<actions>
1. Parse Arguments:
   - Extract type filter if provided (default: "all")
   - Validate filter is recognized category

2. Launch Ontology Builder Agent:
   ```
   Use the Task tool with subagent_type="general-purpose" to invoke the ontology-builder agent.

   Prompt:
   "Generate visual ontology graph for knowledge base.
   Filter: $ARGUMENTS (or 'all' if no filter)

   Please:
   1. Scan all knowledge entries in .claude/knowledge/
   2. Parse YAML frontmatter for metadata and relationships
   3. Extract wiki-style [[links]] from content
   4. Build graph data structure:
      - Nodes: knowledge entries (with uuid, title, type, tags, status)
      - Edges: relationships (with type and directionality)
   5. Generate Graphviz DOT format with:
      - Color coding by type (metadata=blue, patterns=orange, etc.)
      - Different edge styles (solid, dashed, bold) for relationship types
      - Node styling for status (dashed=archived, dotted=deprecated)
   6. Create output directory: .claude/knowledge/ontology/
   7. Save DOT file and generate PNG/SVG using Graphviz
   8. Perform gap analysis:
      - Isolated entries (0 connections)
      - Poorly connected entries (< 2 connections)
      - Missing documentation areas
      - Broken references
   9. Generate text-based report with:
      - Summary statistics
      - Gap analysis findings
      - Relationship suggestions
      - Recommended actions
   10. If Graphviz not available, generate Mermaid diagram instead

   Provide both visual graph and textual analysis."
   ```

3. Present Results:
   - Graph file location (PNG/SVG or Mermaid)
   - Summary statistics
   - Gap analysis findings
   - Relationship suggestions
   - Recommended improvements
</actions>
The assistant should create visualizations that reveal knowledge structure at a glance and provide actionable insights for improving documentation coverage and connectivity.
