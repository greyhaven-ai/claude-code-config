# Plugin Management Scripts

Automation tools for managing and validating Grey Haven Claude Code plugins.

## Scripts

### 1. fix-plugin-skills.py

Automatically updates `plugin.json` files to include all skills from the `skills/` directory.

**Usage:**
```bash
# Dry run (preview changes)
python scripts/fix-plugin-skills.py --dry-run

# Apply fixes
python scripts/fix-plugin-skills.py
```

**What it does:**
- Scans each plugin's `skills/` directory for SKILL.md files
- Compares with skills declared in `plugin.json`
- Adds missing skills to the `skills` array
- Removes skills that don't exist in the directory

**Example output:**
```
⚠ core
  Declared: 4 | Actual: 12
  Missing from plugin.json:
    + ./skills/code-quality-analysis
    + ./skills/tdd-python
    ...
  Updated plugin.json
```

### 2. validate-plugins.py

Comprehensive validation tool that checks plugins against Claude Code best practices.

**Usage:**
```bash
# Validate all plugins
python scripts/validate-plugins.py

# Validate specific plugin
python scripts/validate-plugins.py --plugin=core

# Verbose mode (detailed checks)
python scripts/validate-plugins.py --verbose

# Verbose for specific plugin
python scripts/validate-plugins.py --plugin=core --verbose
```

**What it checks:**

**Structure:**
- ✓ `.claude-plugin/` directory exists
- ✓ `plugin.json` is valid JSON
- ✓ Required fields present (name, version, description)
- ✓ Name follows kebab-case
- ✓ Version follows semver

**Skills:**
- ✓ Skills array matches actual `skills/` directory
- ✓ All skills have `SKILL.md` with frontmatter
- ✓ Skill names are kebab-case and < 64 chars
- ✓ Descriptions include activation triggers
- ✓ Descriptions are < 1024 chars

**Agents:**
- ✓ Agent frontmatter includes name and description
- ✓ Descriptions include trigger phrases ("Use when...", "Use PROACTIVELY...")
- ⚠ Warns if agent is > 300 lines
- ⚠ Suggests adding `model` field

**Commands:**
- ✓ Commands exist and are properly structured
- ✓ Frontmatter includes `description` and `argument-hint`

**File Management:**
- ⚠ Detects `-old` files that should be removed

**Example output:**
```
Plugin: core
============================================================

❌ Errors (1):
  • Skills missing from plugin.json: ./skills/tdd-python, ...

⚠️  Warnings (2):
  • Found 2 old agent files: tdd-python-old.md
  • Agent code-reviewer.md missing 'model' field

✓ Passed (8):
  • plugin.json exists
  • plugin.json is valid JSON
  • All agents have trigger phrases
  ...

Score: 54/100
```

**Exit codes:**
- `0` - No errors (warnings allowed)
- `1` - Errors found

## Workflow

### Initial Setup / Major Changes

1. **Run validation to see current state:**
   ```bash
   python scripts/validate-plugins.py
   ```

2. **Fix skills arrays:**
   ```bash
   # Preview changes
   python scripts/fix-plugin-skills.py --dry-run

   # Apply changes
   python scripts/fix-plugin-skills.py
   ```

3. **Re-validate:**
   ```bash
   python scripts/validate-plugins.py
   ```

4. **Fix remaining issues manually:**
   - Remove `-old` files
   - Add trigger phrases to agent descriptions
   - Add `model` fields to agents
   - Fix skill frontmatter

### Regular Maintenance

```bash
# After adding new skills
python scripts/fix-plugin-skills.py

# Before committing changes
python scripts/validate-plugins.py
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Validate Plugins
  run: python scripts/validate-plugins.py
```

## Requirements

- Python 3.7+
- PyYAML (`pip install pyyaml`)

## Best Practices Enforced

Based on official Claude Code documentation:

1. **Skills must be declared** - All skills in `skills/` must be listed in `plugin.json`
2. **Trigger phrases required** - Agents and skills need clear activation conditions
3. **Kebab-case naming** - Plugin names, skill names follow kebab-case
4. **Frontmatter required** - All agents and skills need YAML frontmatter
5. **Single responsibility** - Warns if agents are too long (>300 lines)
6. **Model specification** - Encourages explicit model selection

## Examples

### Fix a specific plugin

```bash
# Check the issue
python scripts/validate-plugins.py --plugin=core --verbose

# Fix skills
python scripts/fix-plugin-skills.py

# Verify fix
python scripts/validate-plugins.py --plugin=core
```

### Clean sweep

```bash
# Fix all skills
python scripts/fix-plugin-skills.py

# Full validation report
python scripts/validate-plugins.py --verbose > validation-report.txt

# Check summary
python scripts/validate-plugins.py
```

## Troubleshooting

**"Skills missing from plugin.json"**
- Run `fix-plugin-skills.py` to auto-fix

**"Skill missing frontmatter"**
- Add YAML frontmatter to `SKILL.md`:
  ```yaml
  ---
  name: skill-name
  description: "Description with trigger phrases"
  ---
  ```

**"Agent description lacks trigger phrases"**
- Add phrases like:
  - "Use when..."
  - "Use PROACTIVELY when..."
  - "MUST BE USED when..."
  - "Automatically invoked when user mentions..."

**"Found old agent files"**
- Remove or move to archive:
  ```bash
  rm grey-haven-plugins/core/agents/*-old.md
  ```

## Contributing

When creating new plugins, agents, or skills:

1. Follow the structure in existing plugins
2. Run `fix-plugin-skills.py` after adding skills
3. Run `validate-plugins.py` before committing
4. Aim for 90+ score on validation

## References

- [Claude Code Sub-Agents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
