---
url: "https://docs.anthropic.com/en/docs/claude-code/troubleshooting"
title: "Troubleshooting - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Build with Claude Code

Troubleshooting

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

## [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#common-installation-issues)  Common installation issues

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#windows-installation-issues%3A-errors-in-wsl)  Windows installation issues: errors in WSL

You might encounter the following issues in WSL:

**OS/platform detection issues**: If you receive an error during installation, WSL may be using Windows `npm`. Try:

- Run `npm config set os linux` before installation
- Install with `npm install -g @anthropic-ai/claude-code --force --no-os-check` (Do NOT use `sudo`)

**Node not found errors**: If you see `exec: node: not found` when running `claude`, your WSL environment may be using a Windows installation of Node.js. You can confirm this with `which npm` and `which node`, which should point to Linux paths starting with `/usr/` rather than `/mnt/c/`. To fix this, try installing Node via your Linux distribution’s package manager or via [`nvm`](https://github.com/nvm-sh/nvm).

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#linux-and-mac-installation-issues%3A-permission-or-command-not-found-errors)  Linux and Mac installation issues: permission or command not found errors

When installing Claude Code with npm, `PATH` problems may prevent access to `claude`.
You may also encounter permission errors if your npm global prefix is not user writable (eg. `/usr`, or `/usr/local`).

#### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#recommended-solution%3A-native-claude-code-installation)  Recommended solution: Native Claude Code installation

Claude Code has a native installation that doesn’t depend on npm or Node.js.

The native Claude Code installer is currently in beta.

Use the following command to run the native installer.

**macOS, Linux, WSL:**

Copy

```bash
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58

```

**Windows PowerShell:**

Copy

```powershell
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

This command installs the appropriate build of Claude Code for your operating system and architecture and adds a symlink to the installation at `~/.local/bin/claude`.

Make sure that you have the installation directory in your system PATH.

#### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#alternative-solution%3A-migrate-to-local-installation)  Alternative solution: Migrate to local installation

Alternatively, if Claude Code will run, you can migrate to a local installation:

Copy

```bash
claude migrate-installer

```

This moves Claude Code to `~/.claude/local/` and sets up an alias in your shell configuration. No `sudo` is required for future updates.

After migration, restart your shell, and then verify your installation:

On macOS/Linux/WSL:

Copy

```bash
which claude  # Should show an alias to ~/.claude/local/claude

```

On Windows:

Copy

```powershell
where claude  # Should show path to claude executable

```

Verify installation:

Copy

```bash
claude doctor # Check installation health

```

## [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#permissions-and-authentication)  Permissions and authentication

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#repeated-permission-prompts)  Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools
to run without approval using the `/permissions` command. See [Permissions docs](https://docs.anthropic.com/en/docs/claude-code/iam#configuring-permissions).

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#authentication-issues)  Authentication issues

If you’re experiencing authentication problems:

1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete the authentication process again

If problems persist, try:

Copy

```bash
rm -rf ~/.config/claude-code/auth.json
claude

```

This removes your stored authentication information and forces a clean login.

## [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#performance-and-stability)  Performance and stability

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#high-cpu-or-memory-usage)  High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you’re experiencing performance issues:

1. Use `/compact` regularly to reduce context size
2. Close and restart Claude Code between major tasks
3. Consider adding large build directories to your `.gitignore` file

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#command-hangs-or-freezes)  Command hangs or freezes

If Claude Code seems unresponsive:

1. Press Ctrl+C to attempt to cancel the current operation
2. If unresponsive, you may need to close the terminal and restart

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#esc-key-not-working-in-jetbrains-intellij%2C-pycharm%2C-etc-terminals)  ESC key not working in JetBrains (IntelliJ, PyCharm, etc.) terminals

If you’re using Claude Code in JetBrains terminals and the ESC key doesn’t interrupt the agent as expected, this is likely due to a keybinding clash with JetBrains’ default shortcuts.

To fix this issue:

1. Go to Settings → Tools → Terminal
2. Click the “Configure terminal keybindings” hyperlink next to “Override IDE Shortcuts”
3. Within the terminal keybindings, scroll down to “Switch focus to Editor” and delete that shortcut

This will allow the ESC key to properly function for canceling Claude Code operations instead of being captured by PyCharm’s “Switch focus to Editor” action.

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#search-and-discovery-issues)  Search and discovery issues

If Search tool, `@file` mentions, custom agents, and custom slash commands aren’t working, install system `ripgrep`:

Copy

```bash
# macOS (Homebrew)
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep

```

Then set `USE_BUILTIN_RIPGREP=0` in your [environment](https://docs.anthropic.com/en/docs/claude-code/settings#environment-variables).

## [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#markdown-formatting-issues)  Markdown formatting issues

Claude Code sometimes generates markdown files with missing language tags on code fences, which can affect syntax highlighting and readability in GitHub, editors, and documentation tools.

### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#missing-language-tags-in-code-blocks)  Missing language tags in code blocks

If you notice code blocks like this in generated markdown:

Copy

````markdown
```
function example() {
return "hello";
}
```

````

Instead of properly tagged blocks like:

Copy

````markdown
```javascript
function example() {
return "hello";
}
```

````

**Solutions:**

1. **Ask Claude to add language tags**: Simply request “Please add appropriate language tags to all code blocks in this markdown file.”

2. **Use post-processing hooks**: Set up automatic formatting hooks to detect and add missing language tags. See the [markdown formatting hook example](https://docs.anthropic.com/en/docs/claude-code/hooks-guide#markdown-formatting-hook) for implementation details.

3. **Manual verification**: After generating markdown files, review them for proper code block formatting and request corrections if needed.


### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#inconsistent-spacing-and-formatting)  Inconsistent spacing and formatting

If generated markdown has excessive blank lines or inconsistent spacing:

**Solutions:**

1. **Request formatting corrections**: Ask Claude to “Fix spacing and formatting issues in this markdown file.”

2. **Use formatting tools**: Set up hooks to run markdown formatters like `prettier` or custom formatting scripts on generated markdown files.

3. **Specify formatting preferences**: Include formatting requirements in your prompts or project [memory](https://docs.anthropic.com/en/docs/claude-code/memory) files.


### [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#best-practices-for-markdown-generation)  Best practices for markdown generation

To minimize formatting issues:

- **Be explicit in requests**: Ask for “properly formatted markdown with language-tagged code blocks”
- **Use project conventions**: Document your preferred markdown style in [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory)
- **Set up validation hooks**: Use post-processing hooks to automatically verify and fix common formatting issues

## [​](https://docs.anthropic.com/en/docs/claude-code/troubleshooting\#getting-more-help)  Getting more help

If you’re experiencing issues not covered here:

1. Use the `/bug` command within Claude Code to report problems directly to Anthropic
2. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues
3. Run `/doctor` to check the health of your Claude Code installation
4. Ask Claude directly about its capabilities and features - Claude has built-in access to its documentation

Was this page helpful?

YesNo

[Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/claude-code/mcp) [Overview](https://docs.anthropic.com/en/docs/claude-code/third-party-integrations)

On this page

- [Common installation issues](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#common-installation-issues)
- [Windows installation issues: errors in WSL](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#windows-installation-issues%3A-errors-in-wsl)
- [Linux and Mac installation issues: permission or command not found errors](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#linux-and-mac-installation-issues%3A-permission-or-command-not-found-errors)
- [Recommended solution: Native Claude Code installation](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#recommended-solution%3A-native-claude-code-installation)
- [Alternative solution: Migrate to local installation](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#alternative-solution%3A-migrate-to-local-installation)
- [Permissions and authentication](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#permissions-and-authentication)
- [Repeated permission prompts](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#repeated-permission-prompts)
- [Authentication issues](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#authentication-issues)
- [Performance and stability](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#performance-and-stability)
- [High CPU or memory usage](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#high-cpu-or-memory-usage)
- [Command hangs or freezes](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#command-hangs-or-freezes)
- [ESC key not working in JetBrains (IntelliJ, PyCharm, etc.) terminals](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#esc-key-not-working-in-jetbrains-intellij%2C-pycharm%2C-etc-terminals)
- [Search and discovery issues](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#search-and-discovery-issues)
- [Markdown formatting issues](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#markdown-formatting-issues)
- [Missing language tags in code blocks](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#missing-language-tags-in-code-blocks)
- [Inconsistent spacing and formatting](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#inconsistent-spacing-and-formatting)
- [Best practices for markdown generation](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#best-practices-for-markdown-generation)
- [Getting more help](https://docs.anthropic.com/en/docs/claude-code/troubleshooting#getting-more-help)