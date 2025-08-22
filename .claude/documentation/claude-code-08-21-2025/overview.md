# Claude Code Overview

## Get started in 30 seconds

Prerequisites: [Node.js 18 or newer](https://nodejs.org/en/download/)

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to your project
cd your-awesome-project

# Start coding with Claude
claude
```

That's it! You're ready to start coding with Claude.

## What Claude Code does for you

- **Build features from descriptions**: Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.
- **Debug and fix issues**: Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.
- **Navigate any codebase**: Ask anything about your team's codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with MCP can pull from external datasources like Google Drive, Figma, and Slack.
- **Automate tedious tasks**: Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## Why developers love Claude Code

- **Works in your terminal**: Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.
- **Takes action**: Claude Code can directly edit files, run commands, and create commits. Need more? MCP lets Claude read your design docs in Google Drive, update your tickets in Jira, or use your custom developer tooling.
- **Unix philosophy**: Claude Code is composable and scriptable. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` works. Your CI can run `claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"`.
- **Enterprise-ready**: Use Anthropic's API, or host on AWS or GCP. Enterprise-grade security, privacy, and compliance is built-in.

## Next steps

- **Quickstart**: See Claude Code in action with practical examples
- **Common workflows**: Step-by-step guides for common workflows
- **Troubleshooting**: Solutions for common issues with Claude Code
- **IDE setup**: Add Claude Code to your IDE

## Additional resources

- **Host on AWS or GCP**: Configure Claude Code with Amazon Bedrock or Google Vertex AI
- **Settings**: Customize Claude Code for your workflow
- **Commands**: Learn about CLI commands and controls
- **Reference implementation**: Clone our development container reference implementation
- **Security**: Discover Claude Code's safeguards and best practices for safe usage
- **Privacy and data usage**: Understand how Claude Code handles your data