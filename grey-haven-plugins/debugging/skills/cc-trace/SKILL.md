# CC-Trace: Claude Code API Request Interception Assistant

Transform Claude into an interactive assistant for capturing and analyzing Claude Code's API communications using mitmproxy. This skill supports three primary use cases: learning Claude Code internals, debugging issues, and optimizing API usage.

## Core Capabilities

**Setup & Configuration**
- Step-by-step installation guidance for macOS, Linux, and Windows
- Certificate generation and trust procedures across platforms
- Shell configuration with the `proxy_claude` function
- Automated verification script to validate complete setup

**Traffic Capture & Analysis**
- Browser-based inspection via mitmweb interface
- Programmatic analysis using Python scripts and custom tools
- Server-Sent Events (SSE) parsing for streamed responses
- Flow export and replay functionality

**Learning & Optimization**
- System prompt inspection and comparison
- Tool call sequence analysis (parallel vs. sequential execution)
- Token usage pattern recognition
- Context management strategy exploration

## Getting Started

### Initial Assessment

Use the AskUserQuestion tool to assess the user's current state:

1. **Current setup status**:
   - First time user (needs full setup)
   - Troubleshooting existing setup
   - Ready to use (setup complete)

2. **Operating system**: macOS, Linux, or Windows

3. **Preferred interaction mode**:
   - Browser only (manual inspection through web UI)
   - CLI + Claude Code (programmatic analysis with scripts)
   - Both (visual exploration + automated analysis)

4. **Experience level**: Familiarity with proxies and HTTPS interception

### Quick Setup Guide (Experienced Users)

For users who indicate they're experienced or want quick instructions:

**Installation**:
```bash
# macOS
brew install mitmproxy

# Linux
sudo apt-get install mitmproxy  # Debian/Ubuntu
sudo dnf install mitmproxy      # Fedora

# Windows
Use pip or download from mitmproxy.org
```

**Certificate Setup (macOS)**:
```bash
# Generate certificate
mitmproxy  # Start once, then quit with Ctrl+C

# Trust certificate
security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem
```

**Shell Configuration**:

Add this function to `~/.zshrc` or `~/.bashrc`:

```bash
proxy_claude() {
    export HTTP_PROXY=http://127.0.0.1:8080
    export HTTPS_PROXY=http://127.0.0.1:8080
    export NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
    export NODE_TLS_REJECT_UNAUTHORIZED=0
    echo "🔍 Proxy configured for mitmproxy"
    claude
}
```

Then reload: `source ~/.zshrc` (or `~/.bashrc`)

**Verification**:

Run the verification script from the plugin:
```bash
~/.config/claude/plugins/debugging/scripts/verify-setup.sh
```

### Starting a Capture Session

**Terminal 1** - Start mitmweb:
```bash
mitmweb --web-port 8081 \
  --set flow_filter='~d api.anthropic.com' \
  --save-stream-file ~/claude-flows.mitm
```

**Terminal 2** - Run Claude Code with proxy:
```bash
proxy_claude
```

**Access web interface**: http://127.0.0.1:8081

## What You Can Observe

### In Requests
- Complete system prompts and instructions
- User messages and conversation history
- Tool definitions with descriptions and schemas
- File contents loaded into context
- Git status and repository information
- Model configuration parameters

### In Responses
- Claude's text responses and reasoning blocks
- Tool calls with complete parameters
- Token usage statistics (input/output counts)
- Streaming events and delta updates
- Stop reasons explaining generation termination

## Essential Commands & Scripts

### Filter Syntax (mitmweb UI)

```bash
~d api.anthropic.com              # Filter by domain
~m POST                           # Filter by HTTP method
~c 200                            # Filter by status code
~bs 50000                         # Response size > 50KB
~d api.anthropic.com & ~m POST    # Combined (AND)
```

### Bundled Analysis Scripts

All scripts are located in `~/.config/claude/plugins/debugging/scripts/`:

**Show last user prompt**:
```bash
./show-last-prompt.sh [flow-file]
```

**Extract all slash command expansions**:
```bash
mitmdump -r ~/claude-flows.mitm -s extract-slash-commands.py
```

**Parse streamed response** (from clipboard):
```bash
pbpaste | npx tsx parse-streamed-response.ts
```

**Verify setup**:
```bash
./verify-setup.sh
```

### Diagnostic Commands

```bash
# Verify mitmproxy is listening
lsof -i :8080

# Check proxy environment
echo $HTTP_PROXY
echo $HTTPS_PROXY
echo $NODE_EXTRA_CA_CERTS

# Test certificate trust
security verify-cert -c ~/.mitmproxy/mitmproxy-ca-cert.pem
```

## Interaction Guidelines

### For First-Time Users

1. **Assess experience level** - Ask about familiarity with proxies and HTTPS interception
2. **Choose platform** - Provide platform-specific instructions
3. **Guide through setup**:
   - Install mitmproxy
   - Generate and trust certificate
   - Configure shell function
   - Verify setup
4. **Start simple** - Begin with browser-only mode
5. **Demonstrate value** - Show what they can learn from first capture

### For Troubleshooting

**No traffic appears**:
- Verify mitmproxy is running: `lsof -i :8080`
- Check proxy environment is set in correct terminal
- Confirm certificate is trusted
- Test with: `curl -v https://api.anthropic.com`

**Certificate errors**:
- Re-trust the certificate
- Restart browser/Claude Code after trusting
- Check system keychain (macOS) or certificate store

**Port conflicts**:
- Use alternate ports: `mitmweb --listen-port 9090 --web-port 9091`
- Update proxy_claude function accordingly

**SSL/TLS errors**:
- Verify NODE_EXTRA_CA_CERTS points to mitmproxy cert
- Check NODE_TLS_REJECT_UNAUTHORIZED is set to 0
- Ensure certificate was generated (check ~/.mitmproxy/)

### For Analysis Sessions

**Learning system behavior**:
1. Capture a simple interaction
2. Open mitmweb UI and examine request/response
3. Use scripts to extract specific information
4. Compare different scenarios (e.g., with/without file context)

**Debugging issues**:
1. Reproduce the issue with mitmproxy running
2. Filter flows to relevant time window
3. Examine request to see what context was sent
4. Check response for errors or unexpected behavior
5. Export flow for sharing: Right-click → Export

**Optimizing usage**:
1. Monitor token usage across different operations
2. Identify context that could be reduced
3. Test tool call patterns (parallel vs. sequential)
4. Measure response times for different request sizes

## Security Notes

⚠️ **Important Security Considerations**:

- This tool decrypts HTTPS traffic for local debugging only
- `NODE_TLS_REJECT_UNAUTHORIZED=0` disables certificate validation
- **NEVER use in production environments**
- Captured flows contain API keys and sensitive data
- Store flows securely and clean up after sessions
- Don't share flows without redacting sensitive information

**Cleanup after sessions**:
```bash
# Unset proxy
unset HTTP_PROXY HTTPS_PROXY NODE_EXTRA_CA_CERTS NODE_TLS_REJECT_UNAUTHORIZED

# Remove old flows
rm ~/claude-flows.mitm
```

## Advanced Features

### Custom mitmproxy Scripts

Users can create custom Python scripts for advanced analysis:

```python
# Example: Count tool calls
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

Run with: `mitmdump -r ~/claude-flows.mitm -s count-tools.py`

### Filtering and Export

**Save specific flows**:
```bash
# Only save large responses
mitmweb --save-stream-file large-only.mitm \
  --set flow_filter='~bs 100000'

# Only save errors
mitmweb --save-stream-file errors.mitm \
  --set flow_filter='~c 4'
```

**Replay flows**:
```bash
mitmdump -r ~/claude-flows.mitm --server-replay ~/claude-flows.mitm
```

## Next Steps

After completing setup, suggest users:

1. **Start with verification**: Run `verify-setup.sh` to confirm everything works
2. **Begin capture session**: Follow the interaction mode that matches their workflow
3. **Explore bundled scripts**: Try `show-last-prompt.sh` on their first capture
4. **Read detailed docs**: Reference the documentation in the reference/ directory
5. **Create custom scripts**: Build analysis tools for their specific needs

## Support Resources

- **mitmproxy documentation**: https://docs.mitmproxy.org
- **cc-trace repository**: https://github.com/alexfazio/cc-trace
- **Verification script**: Run to diagnose setup issues
- **Example scripts**: Located in plugin scripts directory

Remember: This tool is for learning and debugging. Always respect API terms of service and handle captured data responsibly.
