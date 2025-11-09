# CC-Trace Plugin

Interactive assistant for intercepting, debugging, analyzing and reviewing Claude Code API requests using mitmproxy.

## Overview

CC-Trace transforms Claude Code from a black box into a transparent system by enabling you to capture and analyze HTTPS traffic between the CLI and Anthropic's API. See exactly what data flows in both directions, understand how Claude interprets your tasks, and optimize your usage patterns.

## Features

### 🔧 Setup & Configuration
- **Multi-platform support**: macOS, Linux, and Windows
- **Certificate management**: Automated CA certificate generation and trust
- **Shell configuration**: Proxy wrapper functions for seamless usage
- **Automated verification**: Built-in diagnostics to confirm correct setup

### 📡 Traffic Capture
- **Web interface mode** (mitmweb): Browser-based traffic viewing
- **CLI mode** (mitmproxy): Terminal-based interactive interface
- **Persistent capture**: Save flows to disk for analysis
- **Real-time monitoring**: Watch API calls as they happen

### 🔍 Analysis & Inspection
- **Request analysis**: Inspect system prompts, tool definitions, file contents
- **Response analysis**: See tool calls, token usage, thinking blocks
- **Pattern discovery**: Compare prompts, track token consumption, identify inefficiencies
- **Optimization**: Find redundant operations and improve prompt engineering

### 🛠️ Diagnostic Tools
- **Systematic troubleshooting**: Step-by-step issue resolution
- **Common issues covered**: Certificate errors, port conflicts, proxy configuration
- **Verification checkpoints**: Confirm each step before proceeding

## Quick Start

### Installation (macOS with Homebrew)

```bash
# Install mitmproxy
brew install mitmproxy

# Generate and trust certificate
mitmproxy && (sleep 1; pkill mitmproxy)
sudo security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem

# Add proxy function to ~/.zshrc
cat >> ~/.zshrc << 'EOF'
proxy_claude() {
    export HTTPS_PROXY=http://127.0.0.1:8080
    export NODE_TLS_REJECT_UNAUTHORIZED=0
    claude "$@"
    unset HTTPS_PROXY NODE_TLS_REJECT_UNAUTHORIZED
}
EOF
source ~/.zshrc
```

### Basic Usage

```bash
# Terminal 1: Start mitmproxy with web interface
mitmweb --web-port 8081 \
  --set flow_filter='~d api.anthropic.com' \
  --save-stream-file ~/claude-flows.mitm

# Terminal 2: Run Claude Code through proxy
proxy_claude

# Browser: View captured traffic
open http://127.0.0.1:8081
```

## Agent Available

### `cc-trace`
Interactive assistant for all CC-Trace functionality. Invoke this agent to:
- Get guided setup assistance
- Capture and analyze API traffic
- Debug unexpected behavior
- Learn Claude Code internals
- Optimize token usage

**Trigger examples:**
- "help me setup cc-trace"
- "debug my api calls"
- "capture claude code traffic"
- "analyze my token usage"
- "why is claude making these tool calls?"

## Use Cases

### 1. Understanding Tool Call Patterns
Capture traffic while Claude performs multi-step tasks to see which tools are called in parallel vs. sequential, and understand dependencies.

### 2. Optimizing Token Usage
Track token consumption across different task types to identify high-cost operations and refactor prompts accordingly.

### 3. Debugging Unexpected Behavior
Examine the exact system prompt Claude received and tool call parameters to identify misunderstandings or configuration issues.

### 4. Learning System Prompts
Compare system prompts for various command types to understand how Claude Code adapts its instructions for different tasks.

## What You Can Inspect

**In Requests:**
- System prompts and instructions
- User messages and conversation history
- Tool definitions with JSON schemas
- File contents and git status
- Model configuration (temperature, max_tokens, streaming)

**In Responses:**
- Text responses and reasoning
- Tool call parameters
- Token usage statistics (prompt_tokens, completion_tokens)
- Thinking blocks (internal reasoning)
- Streaming events and deltas

## Security Warnings

⚠️ **Local Debugging Only** - This tool is for local debugging on trusted development machines only. Never use in production.

⚠️ **Disable Certificate Verification** - `NODE_TLS_REJECT_UNAUTHORIZED=0` disables TLS certificate validation. Use only temporarily for debugging.

⚠️ **Sensitive Data** - Captured flows contain API keys, prompts, file contents, and configuration. Store securely and never share publicly without redaction.

⚠️ **CA Certificate Trust** - Trusting mitmproxy's CA allows it to intercept **all** HTTPS traffic from applications that trust it, not just Claude Code.

## Requirements

- **mitmproxy**: v9.0+ (install via Homebrew, apt, pip, etc.)
- **Python**: 3.8+ (for mitmproxy)
- **Shell**: bash, zsh, or compatible shell
- **Permissions**: Ability to trust system certificates (may require sudo)

## Platform Support

- ✅ macOS (Homebrew)
- ✅ Linux (apt, yum, dnf, pip)
- ✅ Windows (Scoop, Chocolatey, pip)

## Troubleshooting

Common issues and solutions:

### No Traffic Appearing
1. Verify mitmproxy is running: `ps aux | grep mitmproxy`
2. Check environment variables: `echo $HTTPS_PROXY`
3. Confirm certificate trust
4. Test proxy: `curl -x http://127.0.0.1:8080 https://api.anthropic.com`

### Certificate Errors
1. Regenerate: `mitmproxy && (sleep 1; pkill mitmproxy)`
2. Re-trust using platform-specific commands
3. Clear certificate cache

### Port Conflicts
1. Check ports: `lsof -i :8080` or `lsof -i :8081`
2. Use alternative ports: `--listen-port 8082 --web-port 8083`

For detailed troubleshooting, invoke the `cc-trace` agent and describe your issue.

## References

This plugin is based on [alexfazio/cc-trace](https://github.com/alexfazio/cc-trace), an interactive debugging tool for Claude Code API requests.

Original repository includes additional scripts and reference documentation:
- `verify-setup.sh` - Automated setup verification
- `parse-streamed-response.ts` - Parse Server-Sent Events
- `extract-slash-commands.py` - Extract command expansions
- `show-last-prompt.sh` - Display recent prompts

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

Original cc-trace by Alex Fazio - Microsoft Reference Source License (MS-RSL)

## Support

For issues or questions:
1. Invoke the `cc-trace` agent for interactive assistance
2. Check the [original cc-trace repository](https://github.com/alexfazio/cc-trace)
3. Review [mitmproxy documentation](https://docs.mitmproxy.org/)

## Contributing

Contributions welcome! This plugin is part of the [Grey Haven Claude Code Configuration](https://github.com/greyhaven-ai/claude-code-config) repository.

---

**Made with ❤️ by Grey Haven Studio**
