# Connect Claude Code to tools via MCP

Claude Code can connect to hundreds of external tools and data sources through the Model Context Protocol (MCP), an open-source standard for AI-tool integrations.

## What you can do with MCP

With MCP servers connected, you can ask Claude Code to:

- **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
- **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
- **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our Postgres database."
- **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
- **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

## Popular MCP servers

### Development & Testing Tools

- **Sentry**: Monitor errors, debug production issues
  ```bash
  claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
  ```

- **Socket**: Security analysis for dependencies
  ```bash
  claude mcp add --transport http socket https://mcp.socket.dev/
  ```

- **Hugging Face**: Access to Hugging Face Hub and Gradio AI Applications
  ```bash
  claude mcp add --transport http hugging-face https://huggingface.co/mcp
  ```

### Project Management & Documentation

- **Linear**: Issue tracking and project management
  ```bash
  claude mcp add --transport sse linear https://mcp.linear.app/sse
  ```

- **Notion**: Read docs, update pages, manage tasks
  ```bash
  claude mcp add --transport http notion https://mcp.notion.com/mcp
  ```

- **Atlassian**: Manage Jira tickets and Confluence docs
  ```bash
  claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
  ```

### Infrastructure & DevOps

- **Cloudflare**: Build applications, analyze traffic, manage security
- **Netlify**: Create, deploy, and manage websites
  ```bash
  claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp
  ```

- **Vercel**: Search docs, manage projects and deployments
  ```bash
  claude mcp add --transport http vercel https://mcp.vercel.com/
  ```

## Installing MCP servers

### Option 1: Add a local stdio server

```bash
# Basic syntax
claude mcp add <name> <command> [args...]

# Example: Add Airtable server
claude mcp add airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

The `--` separates Claude's CLI flags from the server command.

### Option 2: Add a remote SSE server

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Example: Connect to Linear
claude mcp add --transport sse linear https://mcp.linear.app/sse

# With authentication
claude mcp add --transport sse private-api https://api.company.com/mcp \
  --header "X-API-Key: your-key-here"
```

### Option 3: Add a remote HTTP server

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

## Managing your servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp
```

## MCP installation scopes

- **Local scope** (default): Private to you in current project
- **Project scope**: Shared via `.mcp.json` file in version control
- **User scope**: Available across all your projects

```bash
# Add project-scoped server
claude mcp add shared-server --scope project /path/to/server

# Add user-scoped server
claude mcp add my-server --scope user /path/to/server
```

## Authenticate with remote MCP servers

Many cloud-based MCP servers require OAuth 2.0 authentication:

1. Add the server:
   ```bash
   claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
   ```

2. Use `/mcp` command in Claude Code to authenticate

3. Follow the browser authentication flow

## Use MCP resources

Reference MCP resources using @ mentions:

```
> Can you analyze @github:issue://123 and suggest a fix?
```

```
> Compare @postgres:schema://users with @docs:file://database/user-model
```

## Use MCP prompts as slash commands

MCP servers can expose prompts as slash commands:

```
> /mcp__github__list_prs
```

```
> /mcp__jira__create_issue "Bug in login flow" high
```

## Tips

- Use `--scope` flag to control server availability
- Set environment variables with `--env KEY=value`
- Configure timeout with `MCP_TIMEOUT` environment variable
- Windows users: Use `cmd /c` wrapper for npx commands
- Authentication tokens are stored securely and refreshed automatically