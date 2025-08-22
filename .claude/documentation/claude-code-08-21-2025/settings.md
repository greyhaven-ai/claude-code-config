# Claude Code Settings

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL.

## Settings files

The `settings.json` file is our official mechanism for configuring Claude Code through hierarchical settings:

- **User settings** are defined in `~/.claude/settings.json` and apply to all projects.
- **Project settings** are saved in your project directory:
  - `.claude/settings.json` for settings that are checked into source control and shared with your team
  - `.claude/settings.local.json` for settings that are not checked in, useful for personal preferences and experimentation
- **Enterprise managed policy settings** take precedence over user and project settings:
  - macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
  - Linux and WSL: `/etc/claude-code/managed-settings.json`
  - Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

### Example settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

## Available settings

| Key | Description | Example |
| --- | --- | --- |
| `apiKeyHelper` | Custom script to generate an auth value | `/bin/generate_temp_api_key.sh` |
| `cleanupPeriodDays` | How long to retain chat transcripts (default: 30 days) | `20` |
| `env` | Environment variables for every session | `{"FOO": "bar"}` |
| `includeCoAuthoredBy` | Include "co-authored-by Claude" in commits (default: true) | `false` |
| `permissions` | Permission rules for tool access | See permission settings |
| `hooks` | Custom commands before/after tool executions | See hooks documentation |
| `model` | Override default model | `"claude-3-5-sonnet-20241022"` |
| `statusLine` | Custom status line configuration | See statusLine documentation |
| `forceLoginMethod` | Restrict login method | `claudeai` or `console` |
| `enableAllProjectMcpServers` | Auto-approve all MCP servers in `.mcp.json` | `true` |
| `enabledMcpjsonServers` | List of specific MCP servers to approve | `["memory", "github"]` |
| `disabledMcpjsonServers` | List of specific MCP servers to reject | `["filesystem"]` |
| `awsAuthRefresh` | Custom script for AWS auth refresh | `aws sso login --profile myprofile` |
| `awsCredentialExport` | Custom script for AWS credentials | `/bin/generate_aws_grant.sh` |

## Permission settings

| Keys | Description | Example |
| --- | --- | --- |
| `allow` | Permission rules to allow tool use | `["Bash(git diff:*)"]` |
| `ask` | Permission rules requiring confirmation | `["Bash(git push:*)"]` |
| `deny` | Permission rules to deny tool use | `["WebFetch", "Read(./.env)"]` |
| `additionalDirectories` | Additional working directories | `["../docs/"]` |
| `defaultMode` | Default permission mode | `"acceptEdits"` |
| `disableBypassPermissionsMode` | Prevent bypass mode | `"disable"` |

## Settings precedence

Settings are applied in order of precedence (highest to lowest):

1. **Enterprise managed policies** (`managed-settings.json`)
2. **Command line arguments**
3. **Local project settings** (`.claude/settings.local.json`)
4. **Shared project settings** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`)

## Excluding sensitive files

To prevent Claude Code from accessing sensitive files:

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

## Environment variables

Key environment variables for Claude Code:

| Variable | Purpose |
| --- | --- |
| `ANTHROPIC_API_KEY` | API key for Claude SDK |
| `ANTHROPIC_MODEL` | Custom model name |
| `CLAUDE_CODE_USE_BEDROCK` | Use AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI |
| `DISABLE_TELEMETRY` | Opt out of telemetry |
| `HTTP_PROXY` / `HTTPS_PROXY` | Proxy configuration |
| `MCP_TIMEOUT` | MCP server startup timeout |

## Configuration commands

- List settings: `claude config list`
- Get a setting: `claude config get <key>`
- Change a setting: `claude config set <key> <value>`
- Add to a list: `claude config add <key> <value>`
- Remove from a list: `claude config remove <key> <value>`

Use `--global` or `-g` flag for global configuration.

## Tools available to Claude

| Tool | Description | Permission Required |
| --- | --- | --- |
| **Bash** | Executes shell commands | Yes |
| **Edit** | Makes targeted file edits | Yes |
| **Glob** | Finds files by pattern | No |
| **Grep** | Searches file contents | No |
| **LS** | Lists files and directories | No |
| **MultiEdit** | Multiple edits on single file | Yes |
| **NotebookEdit** | Modifies Jupyter notebooks | Yes |
| **Read** | Reads file contents | No |
| **Task** | Runs sub-agents | No |
| **TodoWrite** | Manages task lists | No |
| **WebFetch** | Fetches URL content | Yes |
| **WebSearch** | Performs web searches | Yes |
| **Write** | Creates/overwrites files | Yes |