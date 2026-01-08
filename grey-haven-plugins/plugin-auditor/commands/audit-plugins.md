---
description: Audit Claude plugins and skills for best practices, deprecations, and changelog compatibility
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - Task
  - TodoWrite
argument-hint: [plugin name or path, or 'all' for full audit]
---

Audit plugins for best practices and changelog compatibility: $ARGUMENTS

<context>
Auditing plugins against the latest Claude Code changelog and best practices.
This audit checks for:
- Plugin structure validity
- Deprecated patterns and settings
- Missing best practice features (allowed-tools, disallowedTools, etc.)
- New Claude Code features to adopt
- Security concerns
</context>

<requirements>
- Validate plugin directory structure
- Check agent/skill/command frontmatter
- Identify deprecated patterns
- Recommend feature adoption
- Generate actionable audit report
</requirements>

<actions>
1. **Identify Target Plugins**:
   - If $ARGUMENTS is 'all': Audit all installed plugins
   - If $ARGUMENTS is a plugin name: Find and audit that plugin
   - If $ARGUMENTS is a path: Audit plugin at that path
   - Default: Audit plugins in grey-haven-plugins/

2. **Fetch Latest Changelog** (if needed):
   ```
   Fetch https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
   Extract recent feature additions and deprecations
   ```

3. **For Each Plugin, Check**:

   **Structure Validation**:
   - .claude-plugin/plugin.json exists and is valid
   - Required directories present (agents/, commands/, or skills/)
   - README.md exists

   **Agent Frontmatter**:
   - Has name, description
   - Has model: (should be opus for quality work)
   - Has color: for identification
   - Uses YAML-style tool lists
   - Has disallowedTools to block dangerous tools
   - Has hooks: for validation (v2.1.0+)

   **Skill Frontmatter**:
   - Has name, description
   - Has skills: for auto-loading (v2.0.43+)
   - Has allowed-tools: with YAML list (v2.0.74+)
   - Consider context: fork (v2.1.0+)

   **Command Frontmatter**:
   - Has description
   - Has allowed-tools
   - Has argument-hint

   **Deprecation Checks**:
   - No includeCoAuthoredBy (use attribution)
   - No comma-separated tool lists (use YAML)

   **Security Review**:
   - Agents have appropriate tool restrictions
   - Skills have allowed-tools defined
   - No overly permissive access

4. **Generate Audit Report**:
   ```markdown
   # Plugin Audit Report

   ## Summary
   - Total plugins audited: X
   - Overall health: X/100
   - Deprecations found: X
   - Recommendations: X

   ## Plugin Details
   [Per-plugin analysis]

   ## Action Items
   [Prioritized list of improvements]
   ```

5. **Provide Specific Recommendations**:
   - High priority: Security and deprecation fixes
   - Medium priority: Feature adoption
   - Low priority: Documentation improvements
</actions>

The assistant should use the plugin-auditor subagent for detailed analysis and generate a comprehensive, actionable audit report.
