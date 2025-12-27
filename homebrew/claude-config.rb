class ClaudeConfig < Formula
  desc "Hooks and configuration setup for Grey Haven's Claude Code environment"
  homepage "https://github.com/greyhaven-ai/claude-code-config"
  url "https://github.com/greyhaven-ai/claude-code-config/archive/v2.0.0.tar.gz"
  sha256 "540ee9105de4a9e97ad34f6a0b48ea72e7fed5bcf5e6df081be1e8d12488c17f"
  license "MIT"
  head "https://github.com/greyhaven-ai/claude-code-config.git", branch: "main"

  depends_on "git"
  depends_on "python@3.11" => :recommended

  def install
    # Install hooks and templates only (no agents/commands)
    libexec.install ".claude/hooks"
    libexec.install "templates"
    libexec.install "docs/cli"
    libexec.install "claude-config"

    # Create wrapper script that finds Python dynamically
    (bin/"claude-config").write <<~EOS
      #!/bin/bash
      export CLAUDE_CONFIG_GLOBAL=1
      export CLAUDE_CONFIG_HOME="#{libexec}"
      export FORCE_COLOR=1

      # Try to find Python 3 in common locations
      if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
      elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD="python"
      elif command -v uv &> /dev/null; then
        PYTHON_CMD="uv run python"
      else
        echo "Error: Python 3 is required but not found in PATH" >&2
        echo "" >&2
        echo "Install Python 3:" >&2
        echo "  macOS:    brew install python3" >&2
        echo "  Ubuntu:   sudo apt-get install python3" >&2
        echo "  Or use:   brew install uv" >&2
        exit 1
      fi

      exec $PYTHON_CMD "#{libexec}/claude-config" "$@"
    EOS

    chmod 0755, bin/"claude-config"
  end

  def caveats
    <<~EOS
      ┌─────────────────────────────────────────────────────────────┐
      │  Claude Config v2.0.0 - Hooks & Configuration Setup        │
      └─────────────────────────────────────────────────────────────┘

      🎯 This tool manages hooks and configuration for Claude Code.

      📦 For plugins (agents/commands), clone the repository:

        git clone https://github.com/greyhaven-ai/grey-haven-claude-code-config.git ~/grey-haven-plugins

      ⚙️  Then add to ~/.claude/settings.json:

        {
          "plugin": {
            "marketplaces": [{
              "source": "~/grey-haven-plugins/grey-haven-plugins"
            }],
            "install": [
              "core@grey-haven-plugins",
              "developer-experience@grey-haven-plugins"
            ]
          }
        }

      🚀 Quick Start Commands:

        claude-config install-hooks    # Install hooks to ~/.claude/hooks/
        claude-config setup-mcp         # Configure MCP servers
        claude-config create-project    # Initialize new project
        claude-config doctor            # Diagnose issues

      📚 Documentation:

        Migration Guide:  https://github.com/greyhaven-ai/grey-haven-claude-code-config/blob/main/MIGRATION_V2.md
        Full Docs:        https://github.com/greyhaven-ai/grey-haven-claude-code-config

      ⚠️  NOTE: v2.0.0 no longer includes agents/commands in Homebrew formula.
               Use Git repository + plugin marketplace instead.
    EOS
  end

  test do
    # Test that the wrapper script works
    system "#{bin}/claude-config", "--version"
    assert_match "2.0.0", shell_output("#{bin}/claude-config --version")

    # Test that hooks directory exists
    assert_predicate bin/"claude-config", :exist?
    assert_predicate bin/"claude-config", :executable?
  end
end
