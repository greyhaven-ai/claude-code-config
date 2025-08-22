---
url: "https://docs.anthropic.com/en/docs/claude-code/quickstart"
title: "Quickstart - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Getting started

Quickstart

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

This quickstart guide will have you using AI-powered coding assistance in just a few minutes. By the end, you’ll understand how to use Claude Code for common development tasks.

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#before-you-begin)  Before you begin

Make sure you have:

- A terminal or command prompt open
- A code project to work with

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-1%3A-install-claude-code)  Step 1: Install Claude Code

### [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#npm-install)  NPM Install

If you have [Node.js 18 or newer installed](https://nodejs.org/en/download/):

Copy

```sh
npm install -g @anthropic-ai/claude-code

```

### [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#native-install)  Native Install

Alternatively, try our new native install, now in beta.

**macOS, Linux, WSL:**

Copy

```bash
curl -fsSL claude.ai/install.sh | bash

```

**Windows PowerShell:**

Copy

```powershell
irm https://claude.ai/install.ps1 | iex

```

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-2%3A-start-your-first-session)  Step 2: Start your first session

Open your terminal in any project directory and start Claude Code:

Copy

```bash
cd /path/to/your/project
claude

```

You’ll see the Claude Code prompt inside a new interactive session:

Copy

```
✻ Welcome to Claude Code!

...

> Try "create a util logging.py that..."

```

Your credentials are securely stored on your system. Learn more in [Credential Management](https://docs.anthropic.com/en/docs/claude-code/iam#credential-management).

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-3%3A-ask-your-first-question)  Step 3: Ask your first question

Let’s start with understanding your codebase. Try one of these commands:

Copy

```
> what does this project do?

```

Claude will analyze your files and provide a summary. You can also ask more specific questions:

Copy

```
> what technologies does this project use?

```

Copy

```
> where is the main entry point?

```

Copy

```
> explain the folder structure

```

You can also ask Claude about its own capabilities:

Copy

```
> what can Claude Code do?

```

Copy

```
> how do I use slash commands in Claude Code?

```

Copy

```
> can Claude Code work with Docker?

```

Claude Code reads your files as needed - you don’t have to manually add context. Claude also has access to its own documentation and can answer questions about its features and capabilities.

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-4%3A-make-your-first-code-change)  Step 4: Make your first code change

Now let’s make Claude Code do some actual coding. Try a simple task:

Copy

```
> add a hello world function to the main file

```

Claude Code will:

1. Find the appropriate file
2. Show you the proposed changes
3. Ask for your approval
4. Make the edit

Claude Code always asks for permission before modifying files. You can approve individual changes or enable “Accept all” mode for a session.

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-5%3A-use-git-with-claude-code)  Step 5: Use Git with Claude Code

Claude Code makes Git operations conversational:

Copy

```
> what files have I changed?

```

Copy

```
> commit my changes with a descriptive message

```

You can also prompt for more complex Git operations:

Copy

```
> create a new branch called feature/quickstart

```

Copy

```
> show me the last 5 commits

```

Copy

```
> help me resolve merge conflicts

```

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-6%3A-fix-a-bug-or-add-a-feature)  Step 6: Fix a bug or add a feature

Claude is proficient at debugging and feature implementation.

Describe what you want in natural language:

Copy

```
> add input validation to the user registration form

```

Or fix existing issues:

Copy

```
> there's a bug where users can submit empty forms - fix it

```

Claude Code will:

- Locate the relevant code
- Understand the context
- Implement a solution
- Run tests if available

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#step-7%3A-test-out-other-common-workflows)  Step 7: Test out other common workflows

There are a number of ways to work with Claude:

**Refactor code**

Copy

```
> refactor the authentication module to use async/await instead of callbacks

```

**Write tests**

Copy

```
> write unit tests for the calculator functions

```

**Update documentation**

Copy

```
> update the README with installation instructions

```

**Code review**

Copy

```
> review my changes and suggest improvements

```

**Remember**: Claude Code is your AI pair programmer. Talk to it like you would a helpful colleague - describe what you want to achieve, and it will help you get there.

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#essential-commands)  Essential commands

Here are the most important commands for daily use:

| Command | What it does | Example |
| --- | --- | --- |
| `claude` | Start interactive mode | `claude` |
| `claude "task"` | Run a one-time task | `claude "fix the build error"` |
| `claude -p "query"` | Run one-off query, then exit | `claude -p "explain this function"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -r` | Resume a previous conversation | `claude -r` |
| `claude commit` | Create a Git commit | `claude commit` |
| `/clear` | Clear conversation history | `> /clear` |
| `/help` | Show available commands | `> /help` |
| `exit` or Ctrl+C | Exit Claude Code | `> exit` |

See the [CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference) for a complete list of commands.

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#pro-tips-for-beginners)  Pro tips for beginners

Be specific with your requests

Instead of: “fix the bug”

Try: “fix the login bug where users see a blank screen after entering wrong credentials”

Use step-by-step instructions

Break complex tasks into steps:

Copy

```
> 1. create a new database table for user profiles

```

Copy

```
> 2. create an API endpoint to get and update user profiles

```

Copy

```
> 3. build a webpage that allows users to see and edit their information

```

Let Claude explore first

Before making changes, let Claude understand your code:

Copy

```
> analyze the database schema

```

Copy

```
> build a dashboard showing products that are most frequently returned by our UK customers

```

Save time with shortcuts

- Use Tab for command completion
- Press ↑ for command history
- Type `/` to see all slash commands

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#what%E2%80%99s-next%3F)  What’s next?

Now that you’ve learned the basics, explore more advanced features:

[**Common workflows** \\
\\
Step-by-step guides for common tasks](https://docs.anthropic.com/en/docs/claude-code/common-workflows) [**CLI reference** \\
\\
Master all commands and options](https://docs.anthropic.com/en/docs/claude-code/cli-reference) [**Configuration** \\
\\
Customize Claude Code for your workflow](https://docs.anthropic.com/en/docs/claude-code/settings)

## [​](https://docs.anthropic.com/en/docs/claude-code/quickstart\#getting-help)  Getting help

- **In Claude Code**: Type `/help` or ask “how do I…”
- **Documentation**: You’re here! Browse other guides
- **Community**: Join our [Discord](https://www.anthropic.com/discord) for tips and support

Was this page helpful?

YesNo

[Overview](https://docs.anthropic.com/en/docs/claude-code/overview) [Common workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows)

On this page

- [Before you begin](https://docs.anthropic.com/en/docs/claude-code/quickstart#before-you-begin)
- [Step 1: Install Claude Code](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-1%3A-install-claude-code)
- [NPM Install](https://docs.anthropic.com/en/docs/claude-code/quickstart#npm-install)
- [Native Install](https://docs.anthropic.com/en/docs/claude-code/quickstart#native-install)
- [Step 2: Start your first session](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-2%3A-start-your-first-session)
- [Step 3: Ask your first question](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-3%3A-ask-your-first-question)
- [Step 4: Make your first code change](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-4%3A-make-your-first-code-change)
- [Step 5: Use Git with Claude Code](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-5%3A-use-git-with-claude-code)
- [Step 6: Fix a bug or add a feature](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-6%3A-fix-a-bug-or-add-a-feature)
- [Step 7: Test out other common workflows](https://docs.anthropic.com/en/docs/claude-code/quickstart#step-7%3A-test-out-other-common-workflows)
- [Essential commands](https://docs.anthropic.com/en/docs/claude-code/quickstart#essential-commands)
- [Pro tips for beginners](https://docs.anthropic.com/en/docs/claude-code/quickstart#pro-tips-for-beginners)
- [What’s next?](https://docs.anthropic.com/en/docs/claude-code/quickstart#what%E2%80%99s-next%3F)
- [Getting help](https://docs.anthropic.com/en/docs/claude-code/quickstart#getting-help)