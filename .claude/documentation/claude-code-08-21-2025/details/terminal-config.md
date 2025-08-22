---
url: "https://docs.anthropic.com/en/docs/claude-code/terminal-config"
title: "Optimize your terminal setup - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Configuration

Optimize your terminal setup

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#themes-and-appearance)  Themes and appearance

Claude cannot control the theme of your terminal. That’s handled by your terminal application. You can match Claude Code’s theme to your terminal any time via the `/config` command.

For additional customization of the Claude Code interface itself, you can configure a [custom status line](https://docs.anthropic.com/en/docs/claude-code/statusline) to display contextual information like the current model, working directory, or git branch at the bottom of your terminal.

### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#line-breaks)  Line breaks

You have several options for entering linebreaks into Claude Code:

- **Quick escape**: Type `\` followed by Enter to create a newline
- **Keyboard shortcut**: Set up a keybinding to insert a newline

#### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#set-up-shift%2Benter-vs-code-or-iterm2-%3A)  Set up Shift+Enter (VS Code or iTerm2):

Run `/terminal-setup` within Claude Code to automatically configure Shift+Enter.

#### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#set-up-option%2Benter-vs-code%2C-iterm2-or-macos-terminal-app-%3A)  Set up Option+Enter (VS Code, iTerm2 or macOS Terminal.app):

**For Mac Terminal.app:**

1. Open Settings → Profiles → Keyboard
2. Check “Use Option as Meta Key”

**For iTerm2 and VS Code terminal:**

1. Open Settings → Profiles → Keys
2. Under General, set Left/Right Option key to “Esc+“

### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#notification-setup)  Notification setup

Never miss when Claude completes a task with proper notification configuration:

#### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#terminal-bell-notifications)  Terminal bell notifications

Enable sound alerts when tasks complete:

Copy

```sh
claude config set --global preferredNotifChannel terminal_bell

```

**For macOS users**: Don’t forget to enable notification permissions in System Settings → Notifications → \[Your Terminal App\].

#### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#iterm-2-system-notifications)  iTerm 2 system notifications

For iTerm 2 alerts when tasks complete:

1. Open iTerm 2 Preferences
2. Navigate to Profiles → Terminal
3. Enable “Silence bell” and Filter Alerts → “Send escape sequence-generated alerts”
4. Set your preferred notification delay

Note that these notifications are specific to iTerm 2 and not available in the default macOS Terminal.

#### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#custom-notification-hooks)  Custom notification hooks

For advanced notification handling, you can create [notification hooks](https://docs.anthropic.com/en/docs/claude-code/hooks#notification) to run your own logic.

### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#handling-large-inputs)  Handling large inputs

When working with extensive code or long instructions:

- **Avoid direct pasting**: Claude Code may struggle with very long pasted content
- **Use file-based workflows**: Write content to a file and ask Claude to read it
- **Be aware of VS Code limitations**: The VS Code terminal is particularly prone to truncating long pastes

### [​](https://docs.anthropic.com/en/docs/claude-code/terminal-config\#vim-mode)  Vim Mode

Claude Code supports a subset of Vim keybindings that can be enabled with `/vim` or configured via `/config`.

The supported subset includes:

- Mode switching: `Esc` (to NORMAL), `i`/ `I`, `a`/ `A`, `o`/ `O` (to INSERT)
- Navigation: `h`/ `j`/ `k`/ `l`, `w`/ `e`/ `b`, `0`/ `$`/ `^`, `gg`/ `G`
- Editing: `x`, `dw`/ `de`/ `db`/ `dd`/ `D`, `cw`/ `ce`/ `cb`/ `cc`/ `C`, `.` (repeat)

Was this page helpful?

YesNo

[Add Claude Code to your IDE](https://docs.anthropic.com/en/docs/claude-code/ide-integrations) [Memory management](https://docs.anthropic.com/en/docs/claude-code/memory)

On this page

- [Themes and appearance](https://docs.anthropic.com/en/docs/claude-code/terminal-config#themes-and-appearance)
- [Line breaks](https://docs.anthropic.com/en/docs/claude-code/terminal-config#line-breaks)
- [Set up Shift+Enter (VS Code or iTerm2):](https://docs.anthropic.com/en/docs/claude-code/terminal-config#set-up-shift%2Benter-vs-code-or-iterm2-%3A)
- [Set up Option+Enter (VS Code, iTerm2 or macOS Terminal.app):](https://docs.anthropic.com/en/docs/claude-code/terminal-config#set-up-option%2Benter-vs-code%2C-iterm2-or-macos-terminal-app-%3A)
- [Notification setup](https://docs.anthropic.com/en/docs/claude-code/terminal-config#notification-setup)
- [Terminal bell notifications](https://docs.anthropic.com/en/docs/claude-code/terminal-config#terminal-bell-notifications)
- [iTerm 2 system notifications](https://docs.anthropic.com/en/docs/claude-code/terminal-config#iterm-2-system-notifications)
- [Custom notification hooks](https://docs.anthropic.com/en/docs/claude-code/terminal-config#custom-notification-hooks)
- [Handling large inputs](https://docs.anthropic.com/en/docs/claude-code/terminal-config#handling-large-inputs)
- [Vim Mode](https://docs.anthropic.com/en/docs/claude-code/terminal-config#vim-mode)