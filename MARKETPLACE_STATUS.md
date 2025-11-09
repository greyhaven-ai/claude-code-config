# Grey Haven Plugins Marketplace - Status Report

**Date:** November 9, 2025
**Marketplace Version:** 2.0.0
**Total Plugins:** 14

## Marketplace Configuration

The Grey Haven Plugins marketplace is configured and ready for distribution via GitHub.

### Location
- **Marketplace file:** `.claude-plugin/marketplace.json` (repository root)
- **Plugin source:** `grey-haven-plugins/` directory

### Installation Command
```bash
/plugin marketplace add greyhaven-ai/claude-code-config
```

## Plugin Inventory

All 14 plugins are properly configured with complete metadata:

| # | Plugin Name | Version | Category | Commands | Skills | Hooks |
|---|-------------|---------|----------|----------|--------|-------|
| 1 | core | 1.0.0 | development | 9 | - | - |
| 2 | developer-experience | 1.0.0 | productivity | 3 | - | - |
| 3 | testing | 1.0.0 | testing | 2 | - | - |
| 4 | deployment | 1.0.0 | deployment | 1 | - | - |
| 5 | security | 1.0.0 | security | 1 | - | - |
| 6 | research | 1.0.0 | documentation | 2 | - | - |
| 7 | hooks | 1.0.0 | automation | - | - | 37 |
| 8 | observability | 1.0.0 | operations | 3 | - | - |
| 9 | incident-response | 1.0.0 | operations | 1 | - | - |
| 10 | agent-orchestration | 1.0.0 | development | 3 | - | - |
| 11 | data-quality | 1.0.0 | quality | 1 | - | - |
| 12 | linear | 1.0.0 | project-management | 1 | - | - |
| 13 | browser-automation | 1.0.0 | automation | - | 1 | - |
| 14 | skills | 3.1.0 | standards | - | 16 | - |

**Total Resources:**
- **26 Commands** across 11 plugins
- **17 Skills** (16 in skills plugin + 1 browser-automation)
- **37 Hooks** in hooks plugin

## Validation Status

✅ **All plugins validated successfully**

### Checks Performed

1. ✅ All 14 plugins have `.claude-plugin/plugin.json` files
2. ✅ All required metadata fields present:
   - `name`, `version`, `description`
   - `author` (object format)
   - `license`, `category`, `keywords`
3. ✅ All command paths exist and are correctly declared
4. ✅ All source paths use correct `./` prefix
5. ✅ No unsupported schema fields (`categories`, `featured`)
6. ✅ Plugin structure follows Claude Code conventions

### Recent Updates

**November 9, 2025 - NEW PLUGIN**:
- **Added browser-automation plugin** - Integration of Browserbase's agent-browse tool
- Provides AI-powered browser automation using Stagehand framework
- Enables natural language web browsing, data extraction, and QA testing
- Includes complete skill documentation (SKILL.md, EXAMPLES.md, REFERENCE.md)
- Total plugin count: 13 → 14

**Commit a13132a** (November 4, 2025 - CRITICAL FIX):
- **Moved all 16 skills into `skills/` subdirectory** - Required by Claude Code documentation
- Skills were incorrectly at plugin root, now properly in `plugin-root/skills/skill-name/`
- Updated plugin.json paths from `./skill-name` to `./skills/skill-name`
- **This fix is essential for skills to load correctly**

**Commit b0a416a**:
- Added missing `description` to observability-monitoring skill
- Fixed skill name to match directory
- All 16 skills now have valid YAML frontmatter

**Commit 26e3675**:
- Removed invalid `category` field from all 13 plugin.json files
- `category` only belongs in marketplace.json, not plugin manifests

**Commit 5942998**:
- Added missing `author` and `license` to grey-haven-data-quality
- Added missing `author` and `license` to grey-haven-developer-experience

**Commit fa29b63**:
- Added explicit `commands` arrays to all 11 plugins with command subdirectories

**Commit 6fcf202**:
- Restructured 20 command files from flat structure to subdirectories

**Commit 88e0324**:
- Removed unsupported `categories` and `featured` fields from marketplace.json

## Command Structure

All commands follow the subdirectory pattern required by Claude Code:

```
grey-haven-plugins/
└── grey-haven-core/
    └── commands/
        ├── tdd-implement/
        │   └── tdd-implement.md
        ├── code-review/
        │   └── code-review.md
        └── ...
```

Commands are explicitly declared in marketplace.json:
```json
{
  "name": "grey-haven-core",
  "commands": [
    "./commands/tdd-implement/",
    "./commands/code-review/",
    ...
  ]
}
```

## Skills Structure

Skills follow the required subdirectory pattern per Claude Code documentation:

```
grey-haven-plugins/grey-haven-skills/
├── .claude-plugin/
│   └── plugin.json
└── skills/                      ← Required subdirectory
    ├── code-style/
    │   └── SKILL.md
    ├── testing-strategy/
    │   └── SKILL.md
    └── ... (14 more skills)
```

Skills are declared in plugin.json with paths to skills/ subdirectory:
```json
{
  "name": "grey-haven-skills",
  "skills": [
    "./skills/code-style",
    "./skills/testing-strategy",
    ...
  ]
}
```

**All 16 skills validated:**
- Valid YAML frontmatter with `name` and `description` fields
- Names use lowercase letters, numbers, and hyphens only
- Descriptions include what the skill does AND when to use it
- Proper directory structure: `plugin-root/skills/skill-name/SKILL.md`

## Testing Instructions

### For Fresh Installation

1. **Wait 2-3 minutes** for GitHub CDN to propagate changes
2. Open Claude Code
3. Remove existing marketplace (if any):
   ```
   /plugin marketplace remove grey-haven-plugins
   ```
4. Add marketplace:
   ```
   /plugin marketplace add greyhaven-ai/claude-code-config
   ```
5. Verify all 14 plugins appear:
   ```
   /plugin
   ```
6. Install desired plugins:
   ```
   /plugin install grey-haven-core@grey-haven-plugins
   /plugin install grey-haven-skills@grey-haven-plugins
   ```

### Expected Result

All 14 plugins should appear in the marketplace browser with:
- Complete descriptions
- Correct categories
- All commands/skills/hooks discoverable

## Validation Tool

A Python validation script is available for future maintenance:

```bash
python3 validate_plugins.py
```

This script checks:
- All required metadata fields
- Author field format (object vs string)
- Category presence
- Resource counts (commands, skills, hooks)

## Next Steps

1. **User Testing Required:** Confirm all 13 plugins appear in Claude Code marketplace browser after installation
2. **Documentation:** If testing succeeds, create comprehensive INSTALLATION.md with:
   - GitHub marketplace installation
   - Local development setup
   - Troubleshooting guide
3. **Version Management:** Plan for plugin versioning strategy as features evolve

## Architecture Compliance

✅ Follows Claude Code plugin marketplace specification:
- Marketplace at repository root (`.claude-plugin/`)
- Plugin directories with `.claude-plugin/plugin.json`
- Relative paths from marketplace to plugins
- Explicit command declarations for subdirectories
- Required metadata fields present
- Valid JSON schema

## Known Issues

None. All previous issues have been resolved:
- ✅ Schema validation errors (removed unsupported fields)
- ✅ Path prefix requirements (`./` restored)
- ✅ Command visibility (subdirectories explicitly declared)
- ✅ Missing metadata (all fields added)

## Contact

For issues or questions about the marketplace:
- GitHub: https://github.com/greyhaven-ai/claude-code-config
- Repository Issues: https://github.com/greyhaven-ai/claude-code-config/issues
