# Grey Haven Skills

Claude Skills for Grey Haven Studio workflows - enhancing code quality, commit hygiene, and pull request documentation.

## Overview

This plugin package contains three focused Skills that Claude automatically loads when relevant:

1. **code-style**: Apply Grey Haven coding standards
2. **commit-format**: Format commit messages using Conventional Commits
3. **pr-template**: Generate comprehensive pull request descriptions

## Skills Included

### grey-haven-code-style

**When Claude uses it**: When writing or reviewing code for Grey Haven projects

**What it does**:
- Applies TypeScript/JavaScript best practices
- Enforces React component patterns
- Follows Python PEP 8 conventions
- Ensures code organization standards
- Provides security and performance guidelines

**Example triggers**:
- "Write a React component for user authentication"
- "Review this code for style issues"
- "Refactor this function to follow our standards"

### grey-haven-commit-format

**When Claude uses it**: When creating git commits or reviewing commit messages

**What it does**:
- Formats messages using Conventional Commits
- Ensures proper type/scope/subject structure
- Provides commit message templates
- Validates against Grey Haven conventions

**Example triggers**:
- "Create a commit for these changes"
- "Review this commit message"
- "Write a commit message for this bug fix"

### grey-haven-pr-template

**When Claude uses it**: When creating or reviewing pull requests

**What it does**:
- Generates comprehensive PR descriptions
- Includes summary, motivation, implementation details
- Provides testing guidance and checklist
- Formats according to Grey Haven template

**Example triggers**:
- "Create a pull request description"
- "Write a PR for this feature"
- "Review this PR description for completeness"

## Installation

### Via Claude Code Plugin Marketplace

1. Install the plugin:
   ```
   /plugin install grey-haven-skills@grey-haven-plugins
   ```

2. Skills will be automatically available in Claude Code

### Via npm Package

Skills are included in `@greyhaven/claude-code-config` v2.1.0+:

```bash
npm install -g @greyhaven/claude-code-config
claude-config install-skills
```

### Manual Installation

Copy Skills to your local Skills directory:

```bash
# For personal use
cp -r grey-haven-skills/{code-style,commit-format,pr-template} ~/.claude/skills/

# For project use (shared with team)
cp -r grey-haven-skills/{code-style,commit-format,pr-template} .claude/skills/
```

## Usage

Skills are automatically invoked by Claude when relevant to your task. You don't need to explicitly call them.

### Automatic Invocation

Claude will load Skills based on their descriptions:

```
You: "Write a React component for displaying user profiles"
Claude: [Automatically loads grey-haven-code-style skill]
        [Generates component following Grey Haven standards]

You: "Create a commit for these authentication changes"
Claude: [Automatically loads grey-haven-commit-format skill]
        [Generates properly formatted commit message]

You: "Create a PR description for this OAuth feature"
Claude: [Automatically loads grey-haven-pr-template skill]
        [Generates comprehensive PR description]
```

### Explicit Reference (Optional)

You can explicitly mention Skills if needed:

```
"Use the code-style skill to review this file"
"Apply commit-format skill to this message"
"Generate a PR using the pr-template skill"
```

## Customization

You can customize these Skills for your organization:

1. **Fork this repository**
2. **Edit SKILL.md files** in each skill directory
3. **Update descriptions** to match your workflow
4. **Distribute to your team** via your own plugin marketplace

### Example Customization

Edit `code-style/SKILL.md`:

```markdown
---
name: acme-code-style
description: Apply Acme Corp coding standards including custom TypeScript patterns and React conventions
---

# Acme Corp Code Style Guide

[Your organization's standards here]
```

## Skill Structure

Each Skill follows this structure:

```
skill-name/
└── SKILL.md          # Skill definition with YAML frontmatter
```

### SKILL.md Format

```markdown
---
name: skill-identifier
description: Clear description of what this skill does and when to use it
---

# Skill Title

[Markdown content with instructions, examples, and guidelines]
```

## Development

### Testing Skills Locally

1. **Copy to local directory**:
   ```bash
   cp -r grey-haven-skills/code-style ~/.claude/skills/
   ```

2. **Test in Claude Code**:
   ```
   "Write a TypeScript function following our code standards"
   ```

3. **Check if Skill was loaded**:
   - Look for Skill usage in Claude's chain of thought
   - Verify output follows the Skill's guidelines

### Creating New Skills

1. **Use template structure**:
   ```bash
   mkdir ~/.claude/skills/my-skill
   touch ~/.claude/skills/my-skill/SKILL.md
   ```

2. **Define Skill in SKILL.md**:
   ```markdown
   ---
   name: my-skill
   description: When and how to use this skill
   ---

   # My Skill Instructions

   [Content here]
   ```

3. **Test and iterate**:
   - Test with various prompts
   - Refine description for better auto-invocation
   - Update instructions based on results

## Comparison with Agents

### When to Use Skills vs. Agents

**Use Skills for**:
- Focused, specific tasks (formatting, style checking)
- Automatic application of standards
- Guidance and templates
- Tasks that benefit from automatic invocation

**Use Agents for**:
- Complex multi-step workflows
- Autonomous task execution
- Operations requiring multiple tools
- Tasks needing explicit user control

### Skills + Agents = Better Workflows

Skills and agents work together:

```
You: "/code-review src/auth.ts"
Claude: [Launches code-quality-analyzer agent]
        [Agent automatically uses grey-haven-code-style skill]
        [Comprehensive code review with style checking]
```

## Troubleshooting

### Skill Not Loading

**Check description specificity**:
- Ensure description clearly indicates when to use
- Make description match your typical prompts
- Test with explicit Skill reference first

**Verify installation**:
```bash
ls ~/.claude/skills/
# Should show: code-style, commit-format, pr-template
```

**Check SKILL.md format**:
- YAML frontmatter must be valid
- Name and description are required
- Three dashes (`---`) before and after frontmatter

### Skill Loading Wrong Time

**Refine description**:
- Make description more specific
- Add conditions for when NOT to use
- Test with various prompts

### Multiple Skills Conflicting

Skills are designed to compose, but if conflicts occur:
- Make descriptions more distinct
- Use allowed-tools to restrict scope
- Consider merging related Skills

## Version History

### v1.0.0 (2025-10-20)
- Initial release with three core Skills
- code-style: Comprehensive coding standards
- commit-format: Conventional Commits formatting
- pr-template: Pull request documentation

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

## Support

- **Documentation**: [Grey Haven Claude Config Docs](https://github.com/greyhaven-ai/grey-haven-claude-code-config)
- **Issues**: [GitHub Issues](https://github.com/greyhaven-ai/grey-haven-claude-code-config/issues)
- **Discussions**: [GitHub Discussions](https://github.com/greyhaven-ai/grey-haven-claude-code-config/discussions)

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for details.
