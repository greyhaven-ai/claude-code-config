# Troubleshooting

## Common installation issues

### Windows installation issues: errors in WSL

- **OS/platform detection issues**: Run `npm config set os linux` before installation or install with `npm install -g @anthropic-ai/claude-code --force --no-os-check` (Do NOT use `sudo`)
- **Node not found errors**: If you see `exec: node: not found`, install Node via your Linux distribution's package manager or via nvm

### Linux and Mac installation issues

**Recommended solution: Native installation**

```bash
# macOS, Linux, WSL:
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell:
irm https://claude.ai/install.ps1 | iex
```

**Alternative solution: Migrate to local installation**

```bash
claude migrate-installer
```

This moves Claude Code to `~/.claude/local/` and sets up an alias. No `sudo` required for future updates.

## Permissions and authentication

### Repeated permission prompts

Use `/permissions` command to allow specific tools to run without approval.

### Authentication issues

1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete authentication again

If problems persist:
```bash
rm -rf ~/.config/claude-code/auth.json
claude
```

## Performance and stability

### High CPU or memory usage

1. Use `/compact` regularly to reduce context size
2. Close and restart Claude Code between major tasks
3. Consider adding large build directories to your `.gitignore` file

### Command hangs or freezes

1. Press Ctrl+C to attempt to cancel the current operation
2. If unresponsive, close the terminal and restart

### ESC key not working in JetBrains terminals

1. Go to Settings → Tools → Terminal
2. Click "Configure terminal keybindings" next to "Override IDE Shortcuts"
3. Delete the "Switch focus to Editor" shortcut

### Search and discovery issues

If Search tool, `@file` mentions, custom agents, and custom slash commands aren't working, install system `ripgrep`:

```bash
# macOS (Homebrew)
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep
```

Then set `USE_BUILTIN_RIPGREP=0` in your environment.

## Markdown formatting issues

### Missing language tags in code blocks

Solutions:
1. Ask Claude to add language tags: "Please add appropriate language tags to all code blocks"
2. Use post-processing hooks to detect and add missing language tags
3. Review generated markdown files for proper formatting

### Best practices for markdown generation

- Be explicit in requests: Ask for "properly formatted markdown with language-tagged code blocks"
- Use project conventions: Document your preferred markdown style in CLAUDE.md
- Set up validation hooks: Use post-processing hooks to verify and fix common formatting issues

## Getting more help

1. Use `/bug` command within Claude Code to report problems directly
2. Check the GitHub repository for known issues
3. Run `/doctor` to check the health of your Claude Code installation
4. Ask Claude directly about its capabilities and features