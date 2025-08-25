class ClaudeConfig < Formula
  desc "Comprehensive configuration manager for Claude Code"
  homepage "https://github.com/grey-haven/grey-haven-claude-config"
  url "https://github.com/grey-haven/grey-haven-claude-config/archive/v1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # Will be updated when creating release
  license "MIT"
  head "https://github.com/grey-haven/grey-haven-claude-config.git", branch: "main"

  depends_on "python@3.11"
  depends_on "git"

  def install
    # Install all files to libexec
    libexec.install Dir["*"]
    
    # Create wrapper script
    (bin/"claude-config").write <<~EOS
      #!/bin/bash
      export CLAUDE_CONFIG_GLOBAL=1
      export CLAUDE_CONFIG_HOME="#{libexec}"
      exec "#{Formula["python@3.11"].opt_bin}/python3" "#{libexec}/claude-config" "$@"
    EOS
    
    chmod 0755, bin/"claude-config"
  end

  def caveats
    <<~EOS
      Claude Config has been installed!
      
      Quick Start:
        claude-config --help              Show all commands
        claude-config init                Initialize in current directory
        claude-config list-presets        Show available presets
        claude-config preset recommended  Apply recommended preset
      
      To update from the repository:
        claude-config update
      
      Documentation:
        https://github.com/grey-haven/grey-haven-claude-config
    EOS
  end

  test do
    system "#{bin}/claude-config", "--help"
    assert_match "Claude Config", shell_output("#{bin}/claude-config --help")
  end
end