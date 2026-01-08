---
name: grey-haven-plugin-audit
description: "Comprehensive Claude Code plugin auditing skill for validating structure, detecting deprecated patterns, and recommending best practices based on the latest changelog. Use when auditing plugins, checking for deprecations, validating plugin structure, preparing plugins for release, or ensuring compatibility with recent Claude Code versions. Triggers: 'audit plugin', 'check plugin health', 'validate skill', 'plugin deprecation', 'changelog compatibility', 'plugin best practices'."
skills:
  - grey-haven-code-style
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - TodoWrite
---

# Plugin Audit Skill

Comprehensive Claude Code plugin and skill auditing against the latest changelog and best practices.

## Description

Expert-level auditing of Claude Code plugins including structure validation, deprecation detection, feature adoption recommendations, and quality scoring based on the official changelog.

## What's Included

- **Checklists**: Plugin structure checklist, frontmatter checklist, deprecation checklist
- **Reference**: Changelog feature matrix, best practices guide, deprecation timeline
- **Examples**: Audit report examples, before/after improvements

## Use When

- Auditing plugin structure and quality
- Checking for deprecated patterns
- Preparing plugins for new Claude Code releases
- Validating skill and agent frontmatter
- Ensuring best practices compliance

## Related Agents

- `plugin-auditor`

## Audit Categories

1. **Structure Validation** - Directory layout, required files
2. **Frontmatter Quality** - Agent/skill/command frontmatter
3. **Deprecation Detection** - Outdated patterns and settings
4. **Feature Adoption** - New changelog features to adopt
5. **Security Review** - Tool restrictions, dangerous patterns
6. **Documentation** - README, examples, descriptions

**Skill Version**: 1.0
