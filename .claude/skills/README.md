# Grey Haven Skills

This directory contains Claude Skills that can be installed globally for Grey Haven workflows.

## What Are Skills?

Skills are folders of instructions that Claude loads dynamically when relevant to your task. They provide:

- Automatic application of coding standards
- Consistent commit message formatting
- Comprehensive PR template generation

## Installation

### Global Installation (Recommended)

Install Skills to your home directory for use across all projects:

```bash
claude-config install-skills
```

This copies Skills to `~/.claude/skills/`

### Project-Specific Installation

Copy Skills to your project for team sharing:

```bash
cp -r .claude/skills/* ./.claude/skills/
git add .claude/skills/
git commit -m "chore: add Grey Haven Skills"
```

## Available Skills

### grey-haven-code-style
- Applies TypeScript, React, and Python coding standards
- Loaded automatically when writing or reviewing code
- See: [grey-haven-plugins/grey-haven-skills/code-style/](../../grey-haven-plugins/grey-haven-skills/code-style/)

### grey-haven-commit-format
- Formats commit messages using Conventional Commits
- Loaded automatically when creating commits
- See: [grey-haven-plugins/grey-haven-skills/commit-format/](../../grey-haven-plugins/grey-haven-skills/commit-format/)

### grey-haven-pr-template
- Generates comprehensive pull request descriptions
- Loaded automatically when creating PRs
- See: [grey-haven-plugins/grey-haven-skills/pr-template/](../../grey-haven-plugins/grey-haven-skills/pr-template/)

## Usage

Skills work automatically - just use Claude Code naturally:

```
"Write a React component"          → code-style skill loads
"Create a commit message"           → commit-format skill loads
"Generate a PR description"         → pr-template skill loads
```

## Distribution

Skills are distributed via:

1. **npm package**: `@greyhaven/claude-code-config`
2. **Plugin marketplace**: `grey-haven-skills@grey-haven-plugins`
3. **Direct copy**: From this directory

Choose the method that works best for your workflow.

## Documentation

For complete documentation, see:
- [Skills Analysis](../research/SKILLS_ANALYSIS_AND_INTEGRATION.md)
- [Plugin README](../../grey-haven-plugins/grey-haven-skills/README.md)
- [Claude Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
