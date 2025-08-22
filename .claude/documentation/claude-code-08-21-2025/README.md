# Claude Code Documentation

Complete documentation for Claude Code, Anthropic's official CLI tool for AI-powered coding assistance.

## 📚 Documentation Structure

### Getting Started
- **[Overview](overview.md)** - Introduction to Claude Code, its capabilities, and why developers love it
- **[Quickstart](quickstart.md)** - Get up and running with Claude Code in minutes with practical examples

### Core Features
- **[Common Workflows](common-workflows.md)** - Step-by-step guides for everyday development tasks:
  - Understanding new codebases
  - Fixing bugs efficiently
  - Refactoring code
  - Working with tests
  - Creating pull requests
  - Using extended thinking
  - Working with images
  - Resume previous conversations
  - Running parallel sessions with Git worktrees
  - Using Claude as a Unix-style utility
  - Creating custom slash commands

### Configuration & Customization
- **[Settings](settings.md)** - Configure Claude Code behavior with hierarchical settings:
  - User, project, and enterprise settings
  - Permission configuration
  - Environment variables
  - Tool availability
  - Excluding sensitive files

- **[Memory Management](memory.md)** - Manage Claude's memory across sessions:
  - CLAUDE.md files for persistent instructions
  - Memory hierarchy (enterprise, project, user, local)
  - Import system for modular memories
  - Best practices for memory organization

- **[MCP Integration](mcp.md)** - Connect Claude Code to external tools via Model Context Protocol:
  - Popular MCP servers (Sentry, Linear, Notion, etc.)
  - Installing and managing MCP servers
  - Authentication with remote servers
  - Using MCP resources and prompts

### Reference
- **[CLI Reference](cli-reference.md)** - Complete command-line interface documentation:
  - CLI commands and flags
  - Output formats
  - Interactive vs non-interactive modes
  - Session management

### Administration & Support
- **[Security](security.md)** - Security safeguards and best practices:
  - Permission-based architecture
  - Protection against prompt injection
  - MCP security considerations
  - Reporting security issues

- **[Troubleshooting](troubleshooting.md)** - Solutions for common issues:
  - Installation problems
  - Authentication issues
  - Performance optimization
  - Markdown formatting issues

## 🚀 Quick Links

### Installation
```bash
# NPM (requires Node.js 18+)
npm install -g @anthropic-ai/claude-code

# Native installer (beta)
curl -fsSL claude.ai/install.sh | bash  # macOS/Linux/WSL
irm https://claude.ai/install.ps1 | iex  # Windows PowerShell
```

### Basic Usage
```bash
# Start interactive mode
claude

# Run a one-time task
claude "fix the build error"

# Query and exit
claude -p "explain this function"

# Continue previous conversation
claude --continue
```

### Essential Commands
| Command | Description |
| --- | --- |
| `claude` | Start interactive mode |
| `/help` | Show available commands |
| `/mcp` | Manage MCP servers |
| `/memory` | Edit memory files |
| `/permissions` | Configure permissions |
| `/config` | Adjust settings |
| `/bug` | Report issues |
| `exit` | Exit Claude Code |

## 📖 Additional Resources

### Official Resources
- [Claude Code GitHub Repository](https://github.com/anthropics/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic Trust Center](https://trust.anthropic.com/)
- [Anthropic Discord Community](https://www.anthropic.com/discord)

### Related Documentation
- IDE Integrations
- GitHub Actions
- SDK Documentation
- Development Containers
- Third-party Integrations (AWS Bedrock, Google Vertex AI)
- Corporate Proxy Configuration
- Identity and Access Management
- Monitoring and Usage Analytics
- Hooks and Custom Commands

## 📝 Documentation Notes

This documentation was extracted from the official Claude Code documentation at https://docs.anthropic.com/en/docs/claude-code/. 

For the most up-to-date information and additional details not covered here, please refer to the official documentation.

### Documentation Version
- Last updated: January 2025
- Claude Code version: Latest
- Documentation source: docs.anthropic.com

## 🤝 Contributing

To report documentation issues or suggest improvements:
1. Use the `/bug` command within Claude Code
2. Visit the [GitHub repository](https://github.com/anthropics/claude-code)
3. Join the [Anthropic Discord](https://www.anthropic.com/discord) community

---

*Claude Code - Your AI pair programmer in the terminal*