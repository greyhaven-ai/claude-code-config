# Debugging Plugin

Advanced debugging and API tracing tools for Claude Code, featuring cc-trace for intercepting and analyzing Claude Code API requests using mitmproxy.

## Overview

This plugin provides comprehensive debugging capabilities for Claude Code development, with a focus on understanding and analyzing API interactions. The flagship feature is **cc-trace**, an interactive assistant that transforms Claude into a powerful tool for capturing and analyzing Claude Code's API communications.

## Features

### CC-Trace: API Request Interception

Intercept, debug, analyze, and review Claude Code API requests using mitmproxy.

**Core Capabilities**:
- 🔍 **Traffic Capture**: Browser-based inspection via mitmweb interface
- 🐍 **Programmatic Analysis**: Python scripts and custom tools for automated analysis
- 📊 **Learning Tool**: Inspect system prompts, tool calls, and context management
- 🔧 **Debugging**: Understand request/response patterns and identify issues
- ⚡ **Optimization**: Monitor token usage and optimize API interactions

**What You Can Observe**:
- Complete system prompts and instructions
- User messages and conversation history
- Tool definitions with schemas
- File contents loaded into context
- Token usage statistics
- Claude's reasoning blocks and tool calls
- Streaming events and response patterns

## Installation

This plugin is part of the Grey Haven plugin marketplace. To install:

1. Ensure the marketplace is configured in your `.claude/settings.json`:
```json
{
  "plugin": {
    "marketplaces": [{
      "name": "grey-haven-plugins",
      "source": "/path/to/grey-haven-plugins"
    }],
    "install": [
      "debugging@grey-haven-plugins"
    ]
  }
}
```

2. Reload Claude Code to activate the plugin

## Quick Start

### 1. Setup CC-Trace

Run the setup command to get started:
```
/cc-trace-setup
```

This interactive command will guide you through:
- Installing mitmproxy
- Generating and trusting certificates
- Configuring shell functions
- Verifying the setup

### 2. Verify Setup

Check that everything is configured correctly:
```
/cc-trace-verify
```

### 3. Start a Capture Session

Begin intercepting API traffic:
```
/cc-trace-start
```

This will guide you through:
- Starting mitmweb in one terminal
- Running Claude Code with proxy in another terminal
- Accessing the web interface

### 4. Analyze Captured Traffic

Analyze your captured API requests:
```
/cc-trace-analyze
```

Choose from several analysis options:
- View last user prompt
- Extract slash command expansions
- Parse streamed responses
- Manual inspection via web UI

## Available Commands

| Command | Description |
|---------|-------------|
| `/cc-trace-setup` | Interactive setup guide for cc-trace |
| `/cc-trace-start` | Start a capture session with mitmweb |
| `/cc-trace-analyze` | Analyze captured API traffic |
| `/cc-trace-verify` | Verify cc-trace setup and configuration |

## Available Skills

| Skill | Description |
|-------|-------------|
| `cc-trace` | Full interactive assistant for CC-Trace usage |

## Bundled Scripts

All scripts are located in the plugin's `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `verify-setup.sh` | Automated verification of cc-trace setup |
| `show-last-prompt.sh` | Extract last user prompt from flows |
| `extract-slash-commands.py` | Extract all user messages from flows |
| `parse-streamed-response.ts` | Parse streamed API responses |

## Common Use Cases

### 1. Learning Claude Code Internals

```bash
# Start capture session
/cc-trace-start

# Interact with Claude Code normally
# Then analyze in mitmweb UI at http://127.0.0.1:8081
```

**What to look for**:
- System prompts and how they're structured
- Tool definitions and schemas
- How context is assembled
- How file contents are included

### 2. Debugging Issues

```bash
# Reproduce issue with proxy running
/cc-trace-start

# After reproducing, analyze
/cc-trace-analyze
```

**What to check**:
- Request body to see what context was sent
- Response for errors or unexpected behavior
- Token usage to identify context issues
- Tool calls to verify correct parameters

### 3. Optimizing API Usage

```bash
# Capture normal workflow
/cc-trace-start

# Analyze token patterns
/cc-trace-analyze
```

**Optimization targets**:
- Reduce unnecessary context
- Optimize file inclusion
- Understand token distribution
- Monitor tool call efficiency

### 4. Understanding Tool Calls

```bash
# Capture an interaction with multiple tools
# Open mitmweb UI
# Look for content blocks with type: "tool_use"
```

**Analysis points**:
- Tool call sequencing (parallel vs sequential)
- Parameter construction
- Tool selection patterns
- Response handling

## Requirements

- **mitmproxy**: Install via `brew install mitmproxy` (macOS) or package manager
- **Node.js** (optional): For TypeScript parsing scripts
- **Python 3**: For analysis scripts (usually pre-installed)

## Security Considerations

⚠️ **Important**: This tool is for local debugging only.

- Decrypts HTTPS traffic using a local proxy
- Sets `NODE_TLS_REJECT_UNAUTHORIZED=0` (never use in production)
- Captured flows contain API keys and sensitive data
- Always clean up flows after sessions
- Never share flows without redacting sensitive information

**Cleanup after sessions**:
```bash
# Unset proxy variables
unset HTTP_PROXY HTTPS_PROXY NODE_EXTRA_CA_CERTS NODE_TLS_REJECT_UNAUTHORIZED

# Remove or archive flows
rm ~/claude-flows.mitm
# Or archive: mv ~/claude-flows.mitm ~/flows-archive/
```

## Troubleshooting

### No traffic appears in mitmweb

1. Verify mitmproxy is running: `lsof -i :8080`
2. Check proxy environment: `echo $HTTP_PROXY`
3. Ensure you ran `proxy_claude` in the terminal where you start Claude Code
4. Run verification: `/cc-trace-verify`

### Certificate errors

1. Re-trust certificate:
   ```bash
   security add-trusted-cert -d -p ssl -p basic \
     -k /Library/Keychains/System.keychain \
     ~/.mitmproxy/mitmproxy-ca-cert.pem
   ```
2. Restart terminal/Claude Code
3. Verify trust: `security verify-cert -c ~/.mitmproxy/mitmproxy-ca-cert.pem`

### Port conflicts

Use alternate ports:
```bash
mitmweb --listen-port 9090 --web-port 9091
```

Update proxy_claude function to use port 9090.

## Advanced Usage

### Custom Analysis Scripts

Create custom mitmproxy scripts for specialized analysis:

```python
# count-tools.py
from mitmproxy import http
import json

tool_count = {}

def response(flow: http.HTTPFlow):
    if "api.anthropic.com" not in flow.request.pretty_url:
        return

    data = json.loads(flow.response.content)
    for event in data.get('content', []):
        if event.get('type') == 'tool_use':
            name = event.get('name')
            tool_count[name] = tool_count.get(name, 0) + 1

def done():
    print("\nTool Call Statistics:")
    for tool, count in sorted(tool_count.items()):
        print(f"  {tool}: {count}")
```

Run with:
```bash
mitmdump -r ~/claude-flows.mitm -s count-tools.py
```

### Filtering and Export

**Filter by size**:
```bash
mitmweb --set flow_filter='~bs 100000'  # Only responses > 100KB
```

**Filter by status**:
```bash
mitmweb --set flow_filter='~c 200'  # Only successful requests
```

**Export flows**:
- In mitmweb UI, right-click on flow → Export → Choose format

### Replay Flows

Replay captured flows for testing:
```bash
mitmweb --rfile ~/claude-flows.mitm
```

## Attribution

Based on [cc-trace](https://github.com/alexfazio/cc-trace) by Alex Fazio.

Original work licensed under its respective license. This plugin integration is part of Grey Haven Studio's Claude Code configuration system.

## Support

- Run `/cc-trace-verify` to diagnose setup issues
- Check [mitmproxy documentation](https://docs.mitmproxy.org) for advanced usage
- Review bundled scripts in `scripts/` directory for examples

## License

MIT License - Copyright (c) 2025 Grey Haven Studio

---

**Happy Debugging!** 🔍

This plugin helps you understand Claude Code at a deeper level. Use it to learn, debug, and optimize your interactions with Claude Code's API.
