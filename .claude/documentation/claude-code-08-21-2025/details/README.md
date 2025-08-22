# Claude Code Documentation

This directory contains the official Claude Code documentation scraped from https://docs.anthropic.com/en/docs/claude-code/

## Documentation Structure

### Getting Started
- [Overview](./overview.md) - Introduction to Claude Code and its capabilities
- [Quickstart](./quickstart.md) - Get started with Claude Code in minutes
- [Common Workflows](./common-workflows.md) - Step-by-step guides for common tasks

### Configuration
- [Settings](./settings.md) - Configure Claude Code with global and project-level settings
- [Memory Management](./memory.md) - Manage Claude's memory across sessions with CLAUDE.md files
- [Security](./security.md) - Security safeguards and best practices

### Reference
- [CLI Reference](./cli-reference.md) - Complete reference for command-line interface
- [MCP Integration](./mcp.md) - Connect Claude Code to external tools via Model Context Protocol

### Support
- [Troubleshooting](./troubleshooting.md) - Solutions to common issues

## Quick Links

### Installation

**NPM Install** (requires Node.js 18+):
```bash
npm install -g @anthropic-ai/claude-code
```

**Native Install** (Beta):
```bash
# macOS, Linux, WSL
curl -fsSL claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

### Basic Usage

Start Claude Code:
```bash
claude
```

Quick query:
```bash
claude -p "explain this project"
```

Continue last conversation:
```bash
claude -c
```

### Key Features

- **Build features from descriptions** - Tell Claude what you want in plain English
- **Debug and fix issues** - Describe bugs or paste error messages for analysis
- **Navigate any codebase** - Ask questions about your codebase structure
- **Automate tedious tasks** - Fix lint issues, resolve conflicts, write release notes
- **Works in your terminal** - Not another chat window or IDE
- **Takes action** - Directly edits files, runs commands, creates commits
- **Unix philosophy** - Composable and scriptable
- **Enterprise-ready** - Built-in security, privacy, and compliance

### Configuration Files

- **User settings**: `~/.claude/settings.json`
- **Project settings**: `.claude/settings.json`
- **Project memory**: `./CLAUDE.md`
- **User memory**: `~/.claude/CLAUDE.md`

### Getting Help

- In Claude Code: Type `/help` or ask "how do I…"
- Report bugs: Use `/bug` command
- Community: Join the [Discord](https://www.anthropic.com/discord)
- GitHub: [anthropics/claude-code](https://github.com/anthropics/claude-code)

## Documentation Source

This documentation was crawled from the official Claude Code documentation at:
https://docs.anthropic.com/en/docs/claude-code/

Last updated: 2025-08-22