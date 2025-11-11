---
allowed-tools: Bash, Read, Task
description: Validate knowledge base structural integrity and metadata completeness
argument-hint: [--fix]
---
Validate knowledge base: $ARGUMENTS

<context>
Comprehensive validation of knowledge base structure, metadata, and ontological consistency.
</context>

<requirements>
- Check YAML syntax
- Validate required fields
- Verify semantic type alignment
- Check ontological link validity
- Detect duplicate slugs
- Validate UUIDs and timestamps
- Assess content quality
</requirements>

<actions>
1. Use kb-validator agent for comprehensive validation
2. Generate validation report
3. If --fix flag: attempt auto-fixes
4. Present actionable recommendations
5. Optionally commit fixes
</actions>

Launch kb-validator agent to ensure knowledge base quality and integrity.
