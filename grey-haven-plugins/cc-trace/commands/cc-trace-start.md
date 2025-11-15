---
name: cc-trace-start
description: Start a cc-trace capture session - launches mitmweb and provides instructions for running Claude Code through the proxy
---

Start a cc-trace capture session to intercept and debug Claude Code API requests. This command sets up the monitoring environment and provides step-by-step instructions.

## What This Command Does

1. **Verify Setup**
   - Check if mitmproxy is installed
   - Verify certificate exists and is trusted
   - Confirm prerequisites are met

2. **Start Monitoring**
   - Launch mitmweb with optimal settings
   - Configure traffic filtering for Anthropic API
   - Set up flow capture to disk

3. **Provide Launch Instructions**
   - Show how to run Claude Code through proxy
   - Display browser URL for viewing traffic
   - Explain capture session workflow

4. **Monitor Session**
   - Track active proxy connections
   - Display captured request count
   - Show real-time traffic statistics

## Usage

```bash
# Start a basic capture session
/cc-trace-start

# Start with custom flow file location
/cc-trace-start --output ~/my-flows.mitm

# Start with custom ports
/cc-trace-start --port 9090 --web-port 9091

# Start without saving flows to disk
/cc-trace-start --no-save
```

## Implementation

When you use this command, Claude will:

### Step 1: Pre-flight Checks

```bash
# Verify mitmproxy installation
if ! command -v mitmproxy &> /dev/null; then
    echo "❌ mitmproxy not installed. Run /cc-trace-setup first."
    exit 1
fi

# Check certificate exists
if [ ! -f ~/.mitmproxy/mitmproxy-ca-cert.pem ]; then
    echo "❌ Certificate not found. Run /cc-trace-setup first."
    exit 1
fi

# Check ports are available
if lsof -i :8080 &> /dev/null; then
    echo "⚠️  Port 8080 is already in use"
    echo "Suggestion: Use --port 9090 or kill the conflicting process"
    exit 1
fi

if lsof -i :8081 &> /dev/null; then
    echo "⚠️  Port 8081 is already in use"
    echo "Suggestion: Use --web-port 9091 or kill the conflicting process"
    exit 1
fi
```

### Step 2: Launch mitmweb

```bash
# Default configuration
LISTEN_PORT=8080
WEB_PORT=8081
FLOW_FILE="$HOME/claude-flows-$(date +%Y%m%d-%H%M%S).mitm"
FILTER="~d api.anthropic.com"

# Start mitmweb in background
echo "🚀 Starting mitmweb..."
echo "   Listen port: $LISTEN_PORT"
echo "   Web interface: http://127.0.0.1:$WEB_PORT"
echo "   Flow file: $FLOW_FILE"
echo ""

mitmweb \
  --listen-port $LISTEN_PORT \
  --web-port $WEB_PORT \
  --set flow_filter="$FILTER" \
  --save-stream-file "$FLOW_FILE" \
  --set web_open_browser=false \
  --set web_password=cc-trace \
  &> /tmp/mitmweb.log &

MITM_PID=$!
echo "✓ mitmweb started (PID: $MITM_PID)"
```

### Step 3: Wait for mitmweb to be Ready

```bash
echo "⏳ Waiting for mitmweb to start..."

for i in {1..10}; do
    if curl -s http://127.0.0.1:$WEB_PORT > /dev/null 2>&1; then
        echo "✓ mitmweb is ready!"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""
```

### Step 4: Display Instructions

```bash
cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║                   CC-Trace Capture Session                     ║
║                         ACTIVE                                 ║
╚════════════════════════════════════════════════════════════════╝

📡 mitmweb is running and ready to capture traffic!

┌─ NEXT STEPS ────────────────────────────────────────────────────┐
│                                                                  │
│  1. Open Browser                                                 │
│     → http://127.0.0.1:8081                                      │
│     → Password: cc-trace                                         │
│                                                                  │
│  2. Start Claude Code with Proxy (NEW TERMINAL)                 │
│     → bash ~/.claude/plugins/.../scripts/proxy-claude.sh        │
│                                                                  │
│     Or manually:                                                 │
│     → export HTTPS_PROXY=http://127.0.0.1:8080                  │
│     → export NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/..."         │
│     → export NODE_TLS_REJECT_UNAUTHORIZED=0                     │
│     → claude                                                     │
│                                                                  │
│  3. Use Claude Code Normally                                    │
│     All API requests will appear in your browser!                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

📊 CAPTURE INFO
   • Web Password: cc-trace
   • Filtering: api.anthropic.com only
   • Flow file: ~/claude-flows-20250114-153045.mitm
   • mitmweb PID: 12345

🛑 TO STOP
   • Type /exit in Claude Code
   • Press Ctrl+C in this terminal
   • Or run: kill 12345

⚠️  SECURITY REMINDER
   Captured flows contain API keys and sensitive data.
   Store securely and delete after analysis.

═══════════════════════════════════════════════════════════════════

Press Ctrl+C to stop capture session...
EOF

# Wait for interrupt
trap "echo ''; echo '🛑 Stopping capture session...'; kill $MITM_PID 2>/dev/null; exit 0" INT TERM

# Keep script alive and show status
while kill -0 $MITM_PID 2>/dev/null; do
    # Show request count every 10 seconds
    sleep 10
    REQUEST_COUNT=$(curl -s "http://127.0.0.1:$WEB_PORT/flows" 2>/dev/null | grep -o '"id":' | wc -l || echo "0")
    echo "📈 Captured requests: $REQUEST_COUNT"
done
```

### Step 5: Cleanup on Exit

```bash
echo ""
echo "🧹 Cleaning up..."
kill $MITM_PID 2>/dev/null || true
echo "✓ mitmweb stopped"
echo ""
echo "📁 Captured flows saved to:"
echo "   $FLOW_FILE"
echo ""
echo "💡 To analyze the captured flows:"
echo "   • View in browser: http://127.0.0.1:8081 (if still running)"
echo "   • Parse with script: bash scripts/show-last-prompt.sh $FLOW_FILE"
echo "   • Extract commands: python scripts/extract-slash-commands.py $FLOW_FILE"
```

## Output Format

The command provides a formatted display:

```
🚀 Starting cc-trace capture session...

✓ Pre-flight checks passed
✓ mitmproxy installed (v10.1.5)
✓ Certificate found and trusted
✓ Ports 8080, 8081 available
✓ mitmweb started (PID: 12345)

╔════════════════════════════════════════════════════════════════╗
║                   CC-Trace Capture Session                     ║
║                         ACTIVE                                 ║
╚════════════════════════════════════════════════════════════════╝

📡 mitmweb is running at http://127.0.0.1:8081

[Instructions displayed here...]

📈 Captured requests: 15
📈 Captured requests: 23
📈 Captured requests: 31
```

## Command Options

### --output PATH
Specify custom location for flow file:
```bash
/cc-trace-start --output ~/captures/session-001.mitm
```

### --port NUMBER
Use custom proxy port (default: 8080):
```bash
/cc-trace-start --port 9090
```

### --web-port NUMBER
Use custom web interface port (default: 8081):
```bash
/cc-trace-start --web-port 9091
```

### --no-save
Don't save flows to disk (memory only):
```bash
/cc-trace-start --no-save
```

### --filter EXPRESSION
Custom traffic filter (default: ~d api.anthropic.com):
```bash
/cc-trace-start --filter "~d api.anthropic.com & ~m POST"
```

### --verbose
Show detailed mitmweb logs:
```bash
/cc-trace-start --verbose
```

## What Gets Captured

**Request Data:**
- Full HTTP/HTTPS requests to api.anthropic.com
- Headers (including Authorization tokens)
- Request body (system prompts, messages, tools)
- Query parameters
- Timing information

**Response Data:**
- Status codes and headers
- Response body (streamed events)
- Token usage statistics
- Tool call results
- Error messages

## Browser Interface Features

Once mitmweb is running, the browser interface at `http://127.0.0.1:8081` provides:

- **Flow List**: All captured requests/responses
- **Detail View**: Inspect individual requests
- **Search**: Filter flows by content
- **Export**: Save individual flows
- **Replay**: Resend captured requests
- **Edit**: Modify and replay requests

## Workflow Example

```bash
# Terminal 1: Start capture session
$ /cc-trace-start
🚀 Starting mitmweb...
✓ mitmweb started (PID: 12345)
📡 Browse to http://127.0.0.1:8081

# Terminal 2: Run Claude with proxy
$ bash ~/.claude/plugins/.../scripts/proxy-claude.sh
🔍 Proxy configured for mitmproxy
🚀 Starting Claude Code...

$ # Use Claude normally - all requests are captured

# Terminal 1: Monitor
📈 Captured requests: 5
📈 Captured requests: 12
📈 Captured requests: 18

# When done, Ctrl+C in Terminal 1
^C
🛑 Stopping capture session...
✓ mitmweb stopped
📁 Flows saved to ~/claude-flows-20250114-153045.mitm
```

## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8080
lsof -i :8081

# Use different ports
/cc-trace-start --port 9090 --web-port 9091
```

### mitmweb Won't Start

```bash
# Check mitmproxy installation
mitmproxy --version

# Check for errors
tail -f /tmp/mitmweb.log

# Verify certificate
ls -la ~/.mitmproxy/mitmproxy-ca-cert.pem
```

### No Traffic Appearing

```bash
# Verify proxy environment in Claude terminal
echo $HTTPS_PROXY  # Should be http://127.0.0.1:8080
echo $NODE_EXTRA_CA_CERTS  # Should point to cert

# Test proxy connection
curl -x http://127.0.0.1:8080 https://api.anthropic.com
```

### Browser Interface Not Loading

```bash
# Check if mitmweb is running
ps aux | grep mitmweb

# Test web interface
curl http://127.0.0.1:8081

# Try different browser or clear cache
```

## Security Notes

⚠️ **Active Capture Session Warnings:**

- **All HTTPS traffic** from proxied applications is intercepted
- **API keys** are visible in captured requests
- **File contents** sent to Claude are captured
- **Conversation history** is recorded
- **TLS verification** is disabled (security risk)

**Recommendations:**
- Run capture sessions only when needed
- Use on isolated development machines
- Delete flow files after analysis
- Never commit flow files to version control
- Review captured data before sharing

## Related Commands

- `/cc-trace-setup` - Initial setup for cc-trace
- Use `cc-trace` agent for interactive analysis

## Advanced Usage

### Analyze Captured Flows

```bash
# View last prompt
bash scripts/show-last-prompt.sh ~/claude-flows-*.mitm

# Extract slash commands
python scripts/extract-slash-commands.py ~/claude-flows-*.mitm

# Parse streaming responses
cat response.txt | npx tsx scripts/parse-streamed-response.ts
```

### Filter Specific Traffic

```bash
# Only POST requests
/cc-trace-start --filter "~d api.anthropic.com & ~m POST"

# Only /messages endpoint
/cc-trace-start --filter "~u /messages"

# Large responses only
/cc-trace-start --filter "~bs 50000"
```

### Multiple Concurrent Sessions

```bash
# Session 1: Development work
/cc-trace-start --port 8080 --web-port 8081 --output ~/dev-flows.mitm

# Session 2: Testing work (different terminal)
/cc-trace-start --port 9090 --web-port 9091 --output ~/test-flows.mitm
```

## Performance Impact

- **Minimal overhead**: ~10-50ms per request
- **Memory usage**: ~100MB + flow storage
- **CPU usage**: <5% on modern hardware
- **Disk usage**: ~1-10MB per flow file (varies by session length)

## Quick Reference

```bash
# Standard session
/cc-trace-start

# Custom ports (if defaults in use)
/cc-trace-start --port 9090 --web-port 9091

# Save to specific location
/cc-trace-start --output ~/important-capture.mitm

# Memory only (no disk save)
/cc-trace-start --no-save

# Stop session
Ctrl+C (in the terminal running mitmweb)
```

---

**Tip**: Keep the browser interface open while using Claude Code to watch requests flow in real-time. This helps understand the tool call patterns and API interactions.
