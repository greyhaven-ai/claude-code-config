---
url: "https://docs.anthropic.com/en/docs/claude-code/memory"
title: "Manage Claude's memory - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Configuration

Manage Claude's memory

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#determine-memory-type)  Determine memory type

Claude Code offers four memory locations in a hierarchical structure, each serving a different purpose:

| Memory Type | Location | Purpose | Use Case Examples | Shared With |
| --- | --- | --- | --- | --- |
| **Enterprise policy** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | Company coding standards, security policies, compliance requirements | All users in organization |
| **Project memory** | `./CLAUDE.md` | Team-shared instructions for the project | Project architecture, coding standards, common workflows | Team members via source control |
| **User memory** | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Code styling preferences, personal tooling shortcuts | Just you (all projects) |
| **Project memory (local)** | `./CLAUDE.local.md` | Personal project-specific preferences | _(Deprecated, see below)_ Your sandbox URLs, preferred test data | Just you (current project) |

All memory files are automatically loaded into Claude Code’s context when launched. Files higher in the hierarchy take precedence and are loaded first, providing a foundation that more specific memories build upon.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#claude-md-imports)  CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:

Copy

```
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md

```

Both relative and absolute paths are allowed. In particular, importing files in user’s home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is now deprecated in favor of imports since they work better across multiple git worktrees.

Copy

```
# Individual Preferences
- @~/.claude/my-project-instructions.md

```

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.

Copy

```
This code span will not be treated as an import: `@anthropic-ai/claude-code`

```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#how-claude-looks-up-memories)  How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory _/_ and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in _foo/bar/_, and have memories in both _foo/CLAUDE.md_ and _foo/bar/CLAUDE.md_.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#quickly-add-memories-with-the-%23-shortcut)  Quickly add memories with the `\#` shortcut

The fastest way to add a memory is to start your input with the `#` character:

Copy

```
# Always use descriptive variable names

```

You’ll be prompted to select which memory file to store this in.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#directly-edit-memories-with-%2Fmemory)  Directly edit memories with `/memory`

Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#set-up-project-memory)  Set up project memory

Suppose you want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands.

Bootstrap a CLAUDE.md for your codebase with the following command:

Copy

```
> /init

```

Tips:

- Include frequently used commands (build, test, lint) to avoid repeated searches
- Document code style preferences and naming conventions
- Add important architectural patterns specific to your project
- CLAUDE.md memories can be used for both instructions shared with your team and for your individual preferences.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#organization-level-memory-management)  Organization-level memory management

Enterprise organizations can deploy centrally managed CLAUDE.md files that apply to all users.

To set up organization-level memory management:

1. Create the enterprise memory file in the appropriate location for your operating system:

- macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
- Linux/WSL: `/etc/claude-code/CLAUDE.md`
- Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`

2. Deploy via your configuration management system (MDM, Group Policy, Ansible, etc.) to ensure consistent distribution across all developer machines.

## [​](https://docs.anthropic.com/en/docs/claude-code/memory\#memory-best-practices)  Memory best practices

- **Be specific**: “Use 2-space indentation” is better than “Format code properly”.
- **Use structure to organize**: Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
- **Review periodically**: Update memories as your project evolves to ensure Claude is always using the most up to date information and context.

Was this page helpful?

YesNo

[Terminal configuration](https://docs.anthropic.com/en/docs/claude-code/terminal-config) [Status line configuration](https://docs.anthropic.com/en/docs/claude-code/statusline)

On this page

- [Determine memory type](https://docs.anthropic.com/en/docs/claude-code/memory#determine-memory-type)
- [CLAUDE.md imports](https://docs.anthropic.com/en/docs/claude-code/memory#claude-md-imports)
- [How Claude looks up memories](https://docs.anthropic.com/en/docs/claude-code/memory#how-claude-looks-up-memories)
- [Quickly add memories with the # shortcut](https://docs.anthropic.com/en/docs/claude-code/memory#quickly-add-memories-with-the-%23-shortcut)
- [Directly edit memories with /memory](https://docs.anthropic.com/en/docs/claude-code/memory#directly-edit-memories-with-%2Fmemory)
- [Set up project memory](https://docs.anthropic.com/en/docs/claude-code/memory#set-up-project-memory)
- [Organization-level memory management](https://docs.anthropic.com/en/docs/claude-code/memory#organization-level-memory-management)
- [Memory best practices](https://docs.anthropic.com/en/docs/claude-code/memory#memory-best-practices)