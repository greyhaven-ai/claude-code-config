---
url: "https://docs.anthropic.com/en/docs/claude-code/cli-reference"
title: "CLI reference - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Reference

CLI reference

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

## [​](https://docs.anthropic.com/en/docs/claude-code/cli-reference\#cli-commands)  CLI commands

| Command | Description | Example |
| --- | --- | --- |
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file | claude -p "query"` | Process piped content | `cat logs.txt | claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"` |
| `claude -r "<session-id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish this PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp). |

## [​](https://docs.anthropic.com/en/docs/claude-code/cli-reference\#cli-flags)  CLI flags

Customize Claude Code’s behavior with these command-line flags:

| Flag | Description | Example |
| --- | --- | --- |
| `--add-dir` | Add additional working directories for Claude to access (validates each path exists as a directory) | `claude --add-dir ../apps ../lib` |
| `--allowedTools` | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](https://docs.anthropic.com/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Read"` |
| `--disallowedTools` | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](https://docs.anthropic.com/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"` |
| `--print`, `-p` | Print response without interactive mode (see [SDK documentation](https://docs.anthropic.com/en/docs/claude-code/sdk) for programmatic usage details) | `claude -p "query"` |
| `--append-system-prompt` | Append to system prompt (only with `--print`) | `claude --append-system-prompt "Custom instruction"` |
| `--output-format` | Specify output format for print mode (options: `text`, `json`, `stream-json`) | `claude -p "query" --output-format json` |
| `--input-format` | Specify input format for print mode (options: `text`, `stream-json`) | `claude -p --output-format json --input-format stream-json` |
| `--verbose` | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes) | `claude --verbose` |
| `--max-turns` | Limit the number of agentic turns in non-interactive mode | `claude -p --max-turns 3 "query"` |
| `--model` | Sets the model for the current session with an alias for the latest model ( `sonnet` or `opus`) or a model’s full name | `claude --model claude-sonnet-4-20250514` |
| `--permission-mode` | Begin in a specified [permission mode](https://docs.anthropic.com/en/docs/claude-code/iam#permission-modes) | `claude --permission-mode plan` |
| `--permission-prompt-tool` | Specify an MCP tool to handle permission prompts in non-interactive mode | `claude -p --permission-prompt-tool mcp_auth_tool "query"` |
| `--resume` | Resume a specific session by ID, or by choosing in interactive mode | `claude --resume abc123 "query"` |
| `--continue` | Load the most recent conversation in the current directory | `claude --continue` |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution) | `claude --dangerously-skip-permissions` |

The `--output-format json` flag is particularly useful for scripting and
automation, allowing you to parse Claude’s responses programmatically.

For detailed information about print mode ( `-p`) including output formats,
streaming, verbose logging, and programmatic usage, see the
[SDK documentation](https://docs.anthropic.com/en/docs/claude-code/sdk).

## [​](https://docs.anthropic.com/en/docs/claude-code/cli-reference\#see-also)  See also

- [Interactive mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode) \- Shortcuts, input modes, and interactive features
- [Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) \- Interactive session commands
- [Quickstart guide](https://docs.anthropic.com/en/docs/claude-code/quickstart) \- Getting started with Claude Code
- [Common workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows) \- Advanced workflows and patterns
- [Settings](https://docs.anthropic.com/en/docs/claude-code/settings) \- Configuration options
- [SDK documentation](https://docs.anthropic.com/en/docs/claude-code/sdk) \- Programmatic usage and integrations

Was this page helpful?

YesNo

[Status line configuration](https://docs.anthropic.com/en/docs/claude-code/statusline) [Interactive mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)

On this page

- [CLI commands](https://docs.anthropic.com/en/docs/claude-code/cli-reference#cli-commands)
- [CLI flags](https://docs.anthropic.com/en/docs/claude-code/cli-reference#cli-flags)
- [See also](https://docs.anthropic.com/en/docs/claude-code/cli-reference#see-also)