# CLI Reference

## CLI commands

| Command | Description | Example |
| --- | --- | --- |
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"` |
| `claude -r "<session-id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish this PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure Model Context Protocol servers | See MCP documentation |

## CLI flags

| Flag | Description | Example |
| --- | --- | --- |
| `--add-dir` | Add additional working directories | `claude --add-dir ../apps ../lib` |
| `--allowedTools` | Allow tools without prompting | `"Bash(git log:*)" "Read"` |
| `--disallowedTools` | Disallow tools without prompting | `"Bash(git log:*)" "Edit"` |
| `--print`, `-p` | Print response without interactive mode | `claude -p "query"` |
| `--append-system-prompt` | Append to system prompt (with `--print`) | `claude --append-system-prompt "Custom"` |
| `--output-format` | Output format for print mode | `claude -p "query" --output-format json` |
| `--input-format` | Input format for print mode | `claude -p --input-format stream-json` |
| `--verbose` | Enable verbose logging | `claude --verbose` |
| `--max-turns` | Limit agentic turns in non-interactive mode | `claude -p --max-turns 3 "query"` |
| `--model` | Set model for session | `claude --model sonnet` |
| `--permission-mode` | Begin in specified permission mode | `claude --permission-mode plan` |
| `--permission-prompt-tool` | MCP tool for permission prompts | `claude -p --permission-prompt-tool mcp_auth` |
| `--resume` | Resume specific session | `claude --resume abc123 "query"` |
| `--continue` | Load most recent conversation | `claude --continue` |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution) | `claude --dangerously-skip-permissions` |

## Output formats

- `text`: Plain text output (default)
- `json`: JSON formatted output
- `stream-json`: Streaming JSON output

## Input formats

- `text`: Plain text input (default)
- `stream-json`: Streaming JSON input

## See also

- [Interactive mode](interactive-mode.md) - Shortcuts and interactive features
- [Slash commands](slash-commands.md) - Interactive session commands
- [Quickstart guide](quickstart.md) - Getting started with Claude Code
- [Common workflows](common-workflows.md) - Advanced workflows and patterns
- [Settings](settings.md) - Configuration options
- [SDK documentation](sdk.md) - Programmatic usage and integrations