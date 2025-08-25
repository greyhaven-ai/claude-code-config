class ClaudeConfig < Formula
  desc "Comprehensive configuration manager for Claude Code"
  homepage "https://github.com/greyhaven-ai/claude-code-config"
  url "https://github.com/greyhaven-ai/claude-code-config/archive/v1.0.0.tar.gz"
  sha256 "6091f0a196783414de152262ab69e9682ec533a6e9702d08ae21f0c9ee5a13cc"
  license "MIT"
  head "https://github.com/greyhaven-ai/claude-code-config.git", branch: "main"

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
        https://github.com/greyhaven-ai/claude-code-config
    EOS
  end

  test do
    system "#{bin}/claude-config", "--help"
    assert_match "Claude Config", shell_output("#{bin}/claude-config --help")
  end
end