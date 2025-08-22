---
url: "https://docs.anthropic.com/en/docs/claude-code/sub-agents"
title: "Subagents - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Build with Claude Code

Subagents

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

Custom subagents in Claude Code are specialized AI assistants that can be invoked to handle specific types of tasks. They enable more efficient problem-solving by providing task-specific configurations with customized system prompts, tools and a separate context window.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#what-are-subagents%3F)  What are subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Each subagent:

- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it’s allowed to use
- Includes a custom system prompt that guides its behavior

When Claude Code encounters a task that matches a subagent’s expertise, it can delegate that task to the specialized subagent, which works independently and returns results.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#key-benefits)  Key benefits

## Context preservation

Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives.

## Specialized expertise

Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks.

## Reusability

Once created, subagents can be used across different projects and shared with your team for consistent workflows.

## Flexible permissions

Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#quick-start)  Quick start

To create your first subagent:

1

Open the subagents interface

Run the following command:

Copy

```
/agents

```

2

Select 'Create New Agent'

Choose whether to create a project-level or user-level subagent

3

Define the subagent

- **Recommended**: Generate with Claude first, then customize to make it yours
- Describe your subagent in detail and when it should be used
- Select the tools you want to grant access to (or leave blank to inherit all tools)
- The interface shows all available tools, making selection easy
- If you’re generating with Claude, you can also edit the system prompt in your own editor by pressing `e`

4

Save and use

Your subagent is now available! Claude will use it automatically when appropriate, or you can invoke it explicitly:

Copy

```
> Use the code-reviewer subagent to check my recent changes

```

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#subagent-configuration)  Subagent configuration

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#file-locations)  File locations

Subagents are stored as Markdown files with YAML frontmatter in two possible locations:

| Type | Location | Scope | Priority |
| --- | --- | --- | --- |
| **Project subagents** | `.claude/agents/` | Available in current project | Highest |
| **User subagents** | `~/.claude/agents/` | Available across all projects | Lower |

When subagent names conflict, project-level subagents take precedence over user-level subagents.

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#file-format)  File format

Each subagent is defined in a Markdown file with this structure:

Copy

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.

```

#### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#configuration-fields)  Configuration fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent’s purpose |
| `tools` | No | Comma-separated list of specific tools. If omitted, inherits all tools from the main thread |

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#available-tools)  Available tools

Subagents can be granted access to any of Claude Code’s internal tools. See the [tools documentation](https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude) for a complete list of available tools.

**Recommended:** Use the `/agents` command to modify tool access - it provides an interactive interface that lists all available tools, including any connected MCP server tools, making it easier to select the ones you need.

You have two options for configuring tools:

- **Omit the `tools` field** to inherit all tools from the main thread (default), including MCP tools
- **Specify individual tools** as a comma-separated list for more granular control (can be edited manually or via `/agents`)

**MCP Tools**: Subagents can access MCP tools from configured MCP servers. When the `tools` field is omitted, subagents inherit all MCP tools available to the main thread.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#managing-subagents)  Managing subagents

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#using-the-%2Fagents-command-recommended)  Using the /agents command (Recommended)

The `/agents` command provides a comprehensive interface for subagent management:

Copy

```
/agents

```

This opens an interactive menu where you can:

- View all available subagents (built-in, user, and project)
- Create new subagents with guided setup
- Edit existing custom subagents, including their tool access
- Delete custom subagents
- See which subagents are active when duplicates exist
- **Easily manage tool permissions** with a complete list of available tools

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#direct-file-management)  Direct file management

You can also manage subagents by working directly with their files:

Copy

```bash
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file

```

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#using-subagents-effectively)  Using subagents effectively

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#automatic-delegation)  Automatic delegation

Claude Code proactively delegates tasks based on:

- The task description in your request
- The `description` field in subagent configurations
- Current context and available tools

To encourage more proactive subagent use, include phrases like “use PROACTIVELY” or “MUST BE USED” in your `description` field.

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#explicit-invocation)  Explicit invocation

Request a specific subagent by mentioning it in your command:

Copy

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error

```

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#example-subagents)  Example subagents

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#code-reviewer)  Code reviewer

Copy

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.

```

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#debugger)  Debugger

Copy

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not just symptoms.

```

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#data-scientist)  Data scientist

Copy

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.

```

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#best-practices)  Best practices

- **Start with Claude-generated agents**: We highly recommend generating your initial subagent with Claude and then iterating on it to make it personally yours. This approach gives you the best results - a solid foundation that you can customize to your specific needs.

- **Design focused subagents**: Create subagents with single, clear responsibilities rather than trying to make one subagent do everything. This improves performance and makes subagents more predictable.

- **Write detailed prompts**: Include specific instructions, examples, and constraints in your system prompts. The more guidance you provide, the better the subagent will perform.

- **Limit tool access**: Only grant tools that are necessary for the subagent’s purpose. This improves security and helps the subagent focus on relevant actions.

- **Version control**: Check project subagents into version control so your team can benefit from and improve them collaboratively.


## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#advanced-usage)  Advanced usage

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#chaining-subagents)  Chaining subagents

For complex workflows, you can chain multiple subagents:

Copy

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them

```

### [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#dynamic-subagent-selection)  Dynamic subagent selection

Claude Code intelligently selects subagents based on context. Make your `description` fields specific and action-oriented for best results.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#performance-considerations)  Performance considerations

- **Context efficiency**: Agents help preserve main context, enabling longer overall sessions
- **Latency**: Subagents start off with a clean slate each time they are invoked and may add latency as they gather context that they require to do their job effectively.

## [​](https://docs.anthropic.com/en/docs/claude-code/sub-agents\#related-documentation)  Related documentation

- [Slash commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands) \- Learn about other built-in commands
- [Settings](https://docs.anthropic.com/en/docs/claude-code/settings) \- Configure Claude Code behavior
- [Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) \- Automate workflows with event handlers

Was this page helpful?

YesNo

[Claude Code SDK](https://docs.anthropic.com/en/docs/claude-code/sdk) [Output styles](https://docs.anthropic.com/en/docs/claude-code/output-styles)

On this page

- [What are subagents?](https://docs.anthropic.com/en/docs/claude-code/sub-agents#what-are-subagents%3F)
- [Key benefits](https://docs.anthropic.com/en/docs/claude-code/sub-agents#key-benefits)
- [Quick start](https://docs.anthropic.com/en/docs/claude-code/sub-agents#quick-start)
- [Subagent configuration](https://docs.anthropic.com/en/docs/claude-code/sub-agents#subagent-configuration)
- [File locations](https://docs.anthropic.com/en/docs/claude-code/sub-agents#file-locations)
- [File format](https://docs.anthropic.com/en/docs/claude-code/sub-agents#file-format)
- [Configuration fields](https://docs.anthropic.com/en/docs/claude-code/sub-agents#configuration-fields)
- [Available tools](https://docs.anthropic.com/en/docs/claude-code/sub-agents#available-tools)
- [Managing subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents#managing-subagents)
- [Using the /agents command (Recommended)](https://docs.anthropic.com/en/docs/claude-code/sub-agents#using-the-%2Fagents-command-recommended)
- [Direct file management](https://docs.anthropic.com/en/docs/claude-code/sub-agents#direct-file-management)
- [Using subagents effectively](https://docs.anthropic.com/en/docs/claude-code/sub-agents#using-subagents-effectively)
- [Automatic delegation](https://docs.anthropic.com/en/docs/claude-code/sub-agents#automatic-delegation)
- [Explicit invocation](https://docs.anthropic.com/en/docs/claude-code/sub-agents#explicit-invocation)
- [Example subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents#example-subagents)
- [Code reviewer](https://docs.anthropic.com/en/docs/claude-code/sub-agents#code-reviewer)
- [Debugger](https://docs.anthropic.com/en/docs/claude-code/sub-agents#debugger)
- [Data scientist](https://docs.anthropic.com/en/docs/claude-code/sub-agents#data-scientist)
- [Best practices](https://docs.anthropic.com/en/docs/claude-code/sub-agents#best-practices)
- [Advanced usage](https://docs.anthropic.com/en/docs/claude-code/sub-agents#advanced-usage)
- [Chaining subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents#chaining-subagents)
- [Dynamic subagent selection](https://docs.anthropic.com/en/docs/claude-code/sub-agents#dynamic-subagent-selection)
- [Performance considerations](https://docs.anthropic.com/en/docs/claude-code/sub-agents#performance-considerations)
- [Related documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents#related-documentation)