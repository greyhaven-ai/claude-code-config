# Skill Documentation Standards

This document defines the standard structure and best practices for Grey Haven skill documentation.

## Standard Directory Structure

All skills **MUST** follow this directory-based structure:

```
skill-name/
├── SKILL.md                    # Main skill definition (REQUIRED)
├── examples/                   # Real-world use cases (REQUIRED)
│   ├── INDEX.md               # Navigation guide
│   ├── basic-example.md       # Simple use case
│   ├── intermediate-example.md # Common scenario
│   └── advanced-example.md    # Complex workflow
├── reference/                  # Technical specifications (REQUIRED)
│   ├── INDEX.md               # Navigation guide
│   ├── api-reference.md       # API/function reference
│   ├── configuration.md       # Settings and options
│   └── troubleshooting.md     # Common issues
├── templates/                  # Copy-paste ready files (RECOMMENDED)
│   ├── config-template.yml
│   ├── code-template.ts
│   └── workflow-template.md
└── checklists/                 # Verification guides (RECOMMENDED)
    ├── quality-checklist.md
    └── review-checklist.md
```

## File Naming Conventions

**Directory names:**
- Use **singular** form: `reference/` not `references/`
- Use **lowercase kebab-case**: `api-design/` not `API_Design/`
- Standard names only: `examples/`, `reference/`, `templates/`, `checklists/`

**File names:**
- Use **lowercase kebab-case**: `api-reference.md` not `API_Reference.md`
- Be descriptive: `database-setup-example.md` not `example1.md`
- Use consistent prefixes for organization

## SKILL.md Requirements

Every skill must have a `SKILL.md` with YAML frontmatter:

```yaml
---
name: grey-haven-skill-name           # Kebab-case, prefixed
description: "Clear description with trigger phrases. Use when [scenarios]. When user mentions '[keywords]'."
---

# Skill Name

One-line value proposition.

## Description

2-3 paragraphs explaining what the skill provides.

## What's Included

### Examples (`examples/`)
- Brief list of what examples cover

### Reference Guides (`reference/`)
- Brief list of reference materials

### Templates (`templates/`)
- Brief list of templates available

### Checklists (`checklists/`)
- Brief list of checklists provided

## Use This Skill When

- ✅ Specific scenario 1
- ✅ Specific scenario 2
- ✅ When user mentions: "keywords", "phrases"

## Related Agents

- `agent-name` - What it does
- `another-agent` - What it does

## Quick Start

```bash
# Example commands showing how to use
cat examples/basic-example.md
cat reference/api-reference.md
```

---

**Skill Version**: 1.0
**Last Updated**: YYYY-MM-DD
```

## examples/ Directory

**Purpose:** Provide real-world, copy-paste ready examples

**Structure:**

```markdown
# INDEX.md
# Skill Name Examples

## Available Examples

1. **[Basic Example](basic-example.md)** - Simple use case for getting started
2. **[Intermediate Example](intermediate-example.md)** - Common real-world scenario
3. **[Advanced Example](advanced-example.md)** - Complex multi-step workflow
4. **[Edge Cases](edge-cases.md)** - Handling errors and unusual situations

## Usage

Start with the basic example if you're new to this skill. Move to intermediate
and advanced examples as you need more sophisticated patterns.
```

**Each example file should have:**

```markdown
# Example Title

**User request**: "What the user wants to accomplish"

**Scenario**: Brief context about when this applies

## Workflow

1. **Step 1**: Description
   ```language
   code example
   ```

2. **Step 2**: Description
   ```language
   code example
   ```

3. **Step 3**: Description
   ```language
   code example
   ```

## Expected Result

What happens when you run this example.

## Learn More

- See [reference/topic.md](../reference/topic.md) for details
- See [advanced-example.md](advanced-example.md) for next steps
```

**Best Practices:**
- Show complete, runnable code
- Progress from simple → complex
- Include expected outputs
- Reference related materials
- Use realistic scenarios

## reference/ Directory

**Purpose:** Provide comprehensive technical specifications

**Structure:**

```markdown
# INDEX.md
# Skill Name Reference

## Reference Materials

1. **[Architecture Overview](architecture.md)** - System components and data flow
2. **[API Reference](api-reference.md)** - Complete function/command reference
3. **[Configuration](configuration.md)** - All settings and environment variables
4. **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
5. **[Best Practices](best-practices.md)** - Guidelines and recommendations

## Quick Links

- For getting started: See [examples/](../examples/INDEX.md)
- For templates: See [templates/](../templates/)
```

**API Reference Template:**

```markdown
# API/Function Reference

## Function/Command Name

**Purpose**: One-line description

**Usage**:
```language
code signature
```

**Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param1 | string | Yes | - | What it does |
| param2 | number | No | 10 | What it does |

**Returns**:
```json
{
  "example": "return value",
  "structure": "shown here"
}
```

**Example**:
```language
complete example usage
```

**Errors**:
- `ERROR_CODE`: Cause and solution
- `ANOTHER_ERROR`: Cause and solution

**Implementation Notes**:
How it works internally, performance considerations, etc.

**See Also**:
- [Related function](related-function.md)
- [Examples](../examples/basic-example.md)
```

**Configuration Reference Template:**

```markdown
# Configuration

## Overview

Brief explanation of configuration system.

## Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| VAR_NAME | string | "value" | What it configures |

## Configuration Files

### file-name.yml

```yaml
example:
  configuration: "shown here"
  with: comments
```

## File Locations

- **Config**: `~/.config/tool/config.yml`
- **Cache**: `~/.cache/tool/`
- **Logs**: `~/.local/share/tool/logs/`
```

**Best Practices:**
- Document every option
- Show default values
- Include working examples
- Explain relationships
- Add troubleshooting section

## templates/ Directory

**Purpose:** Provide ready-to-use files and code stubs

**Organization:**
```
templates/
├── README.md              # Explains available templates
├── configs/               # Configuration files
│   ├── basic-config.yml
│   └── advanced-config.yml
├── code/                  # Code templates
│   ├── class-template.py
│   └── component-template.tsx
└── workflows/             # Process templates
    └── workflow-template.md
```

**Template Best Practices:**
- Use `TODO` comments for customization points
- Include helpful comments
- Provide sane defaults
- Show common variations
- Reference examples that use the template

## checklists/ Directory

**Purpose:** Provide verification and quality assurance guides

**Checklist Template:**

```markdown
# Quality Checklist

Use this checklist to verify [what this checks].

## Pre-[Action] Checks

- [ ] Requirement 1 met
- [ ] Requirement 2 verified
- [ ] Configuration valid

## [Action] Verification

- [ ] Step 1 completed successfully
- [ ] Output matches expected format
- [ ] No errors or warnings

## Post-[Action] Validation

- [ ] Integration points working
- [ ] Performance acceptable
- [ ] Documentation updated

## Scoring

- **20+ items checked**: Excellent ✅
- **15-19 items**: Good ⚠️
- **10-14 items**: Needs work 🔴
- **<10 items**: Not ready ❌

## Common Issues

**Issue**: Symptom
**Solution**: How to fix
```

**Best Practices:**
- Make items actionable (specific yes/no)
- Order by workflow (chronological)
- Include scoring criteria
- Add common issues section
- Reference where to find help

## Documentation Quality Standards

### Completeness

**Minimum (acceptable):**
- SKILL.md with frontmatter ✓
- examples/ with 2+ examples ✓
- reference/ with basic docs ✓

**Good (recommended):**
- All 4 directories present ✓
- INDEX.md files in each ✓
- 3+ examples (basic, intermediate, advanced) ✓
- Complete reference coverage ✓
- 2+ templates ✓
- 1+ checklist ✓

**Excellent (exemplary):**
- All of the above ✓
- Cross-references between files ✓
- Troubleshooting guides ✓
- Multiple templates per use case ✓
- Category-specific checklists ✓

### Clarity

- **Use active voice**: "Run this command" not "This command can be run"
- **Be specific**: "Set timeout to 30 seconds" not "Configure timeout appropriately"
- **Show, don't tell**: Include code examples with every explanation
- **Progressive disclosure**: Basic → Intermediate → Advanced
- **Consistent terminology**: Use the same terms throughout

### Accuracy

- **Test all examples**: Every code block must run successfully
- **Verify configurations**: All settings must be valid
- **Update regularly**: Review when underlying tools change
- **Include versions**: Note what versions were tested
- **Document limitations**: Be honest about what doesn't work

## INDEX.md Best Practices

Every `examples/`, `reference/`, `templates/`, and `checklists/` directory should have an `INDEX.md`:

**Purpose:**
- Help users navigate content
- Explain what's available
- Suggest learning paths
- Provide quick links

**Template:**

```markdown
# [Directory Name]

## Overview

Brief explanation of what this directory contains.

## Available [Files]

1. **[File 1](file-1.md)** - What it covers, when to use
2. **[File 2](file-2.md)** - What it covers, when to use
3. **[File 3](file-3.md)** - What it covers, when to use

## Recommended Path

If you're new:
1. Start with [basic file]
2. Then read [intermediate file]
3. Advanced users see [advanced file]

## Quick Reference

- Common task 1: See [file-name.md](file-name.md#section)
- Common task 2: See [other-file.md](other-file.md#section)
```

## Cross-Referencing

Link between related materials:

**In SKILL.md:**
```markdown
See [examples/basic-example.md](examples/basic-example.md) for usage.
```

**In examples:**
```markdown
For complete API reference, see [reference/api-reference.md](../reference/api-reference.md)
```

**In reference:**
```markdown
For working examples, see [examples/](../examples/INDEX.md)
```

**In templates:**
```markdown
This template is used in [examples/advanced-example.md](../examples/advanced-example.md)
```

## Migration from Old Patterns

### File-Based → Directory-Based

**Old pattern (deprecated):**
```
skill-name/
├── SKILL.md
├── EXAMPLES.md      # Single file
└── REFERENCE.md     # Single file
```

**New pattern (standard):**
```
skill-name/
├── SKILL.md
├── examples/        # Directory with multiple files
│   └── INDEX.md
└── reference/       # Directory with multiple files
    └── INDEX.md
```

**Migration steps:**
1. Create `examples/` and `reference/` directories
2. Split `EXAMPLES.md` into multiple example files
3. Split `REFERENCE.md` into focused reference files
4. Create INDEX.md files
5. Update SKILL.md references
6. Keep old files temporarily for reference
7. Remove old files after verification

## Validation

Use the validation script to check compliance:

```bash
python scripts/validate-plugins.py --plugin=plugin-name --verbose
```

**Checks:**
- Required directories exist
- INDEX.md files present
- SKILL.md has valid frontmatter
- Cross-references are valid
- File naming conventions followed

## Examples of Excellent Documentation

**Use these as templates:**

**Pure Directory-Based:**
- `agent-orchestration/context-management` ⭐
- `core/documentation-alignment`
- `core/prompt-engineering`

**Comprehensive Mixed:**
- `core/code-style` ⭐⭐
- `core/testing-strategy` ⭐⭐

**Study these to understand:**
- Clear structure
- Helpful navigation
- Complete coverage
- Good examples
- Useful templates

## Common Mistakes to Avoid

❌ **Don't:**
- Use `references/` (plural) - Use `reference/` (singular)
- Create `EXAMPLES.md` and `REFERENCE.md` files - Use directories
- Use vague descriptions - Be specific with trigger phrases
- Skip INDEX.md files - Navigation is essential
- Make examples too simple - Show real-world scenarios
- Document everything in SKILL.md - Split into focused files
- Use inconsistent naming - Follow kebab-case
- Forget cross-references - Link related materials

✅ **Do:**
- Use directory-based structure
- Include INDEX.md in each directory
- Write specific, actionable examples
- Document all configuration options
- Cross-reference related materials
- Test all code examples
- Update when underlying tools change
- Follow naming conventions

## Questions?

For help with documentation:
1. Review existing well-documented skills
2. Check this standards document
3. Run validation script
4. Ask in team channels

---

**Standards Version**: 1.0
**Last Updated**: 2025-11-09
**Maintained By**: Grey Haven Studio
