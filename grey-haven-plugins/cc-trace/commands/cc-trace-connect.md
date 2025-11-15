---
name: cc-trace-connect
description: Display instructions and commands for connecting Claude Code to an active mitmproxy capture session
---

Display instructions and ready-to-use commands for starting Claude Code through the mitmproxy proxy. Use this after running `/cc-trace-start` to get the exact commands needed.

## What This Command Does

1. **Check mitmweb Status**
   - Verify mitmweb is running
   - Show current PID and ports
   - Display flow file location

2. **Provide Connection Commands**
   - Show the proxy script command
   - Display manual environment variable setup
   - Provide one-liner option for quick start

3. **Display Current Session Info**
   - Web interface URL and password
   - Proxy configuration details
   - Flow file location

## Usage

```bash
# Show connection instructions
/cc-trace-connect
```

## Implementation

When you use this command, Claude will:

### Step 1: Check mitmweb Status

```bash
# Check if mitmweb is running
if ps aux | grep -v grep | grep "mitmweb.*8080" > /dev/null 2>&1; then
    echo "✓ mitmweb is running"
    MITM_PID=$(ps aux | grep -v grep | grep "mitmweb.*8080" | awk '{print $2}')
    echo "  PID: $MITM_PID"
else
    echo "✗ mitmweb is not running"
    echo "  Run /cc-trace-start first"
    exit 1
fi
```

### Step 2: Display Connection Instructions

```bash
cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║           Connect Claude Code to CC-Trace Session              ║
╚════════════════════════════════════════════════════════════════╝

📡 mitmweb is ACTIVE and ready to capture traffic!

┌─ OPTION 1: Using Proxy Script (Recommended - Easiest!) ─────────┐
│                                                                  │
│  Open a NEW terminal window and copy-paste this command:        │
│                                                                  │
│  bash ~/.claude/plugins/marketplaces/grey-haven-plugins/grey-haven-plugins/cc-trace/scripts/proxy-claude.sh
│                                                                  │
│  This automatically sets up the proxy, runs Claude, and cleans  │
│  up when you exit. No shell configuration needed!               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌─ OPTION 2: Environment Variables One-Liner ─────────────────────┐
│                                                                  │
│  HTTP_PROXY=http://127.0.0.1:8080 \                             │
│  HTTPS_PROXY=http://127.0.0.1:8080 \                            │
│  NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/mitmproxy-ca-cert.pem" \ │
│  NODE_TLS_REJECT_UNAUTHORIZED=0 \                               │
│  claude                                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌─ OPTION 3: Manual Setup ─────────────────────────────────────────┐
│                                                                  │
│  In a new terminal, run these commands:                         │
│                                                                  │
│  export HTTP_PROXY=http://127.0.0.1:8080                        │
│  export HTTPS_PROXY=http://127.0.0.1:8080                       │
│  export NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/mitmproxy-ca-cert.pem" │
│  export NODE_TLS_REJECT_UNAUTHORIZED=0                          │
│  claude                                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

📊 SESSION INFO
   • Web Interface: http://127.0.0.1:8081
   • Password: cc-trace
   • Proxy Port: 8080
   • mitmweb PID: 24007

💡 WHAT HAPPENS NEXT
   1. Open new terminal
   2. Run one of the commands above
   3. Use Claude Code normally
   4. All API traffic appears at http://127.0.0.1:8081

⚠️  IMPORTANT
   • Don't run these commands in THIS terminal
   • You need a SEPARATE terminal for the proxied Claude session
   • This session will continue to show mitmweb status

═══════════════════════════════════════════════════════════════════
EOF
```

### Step 3: Show Current Capture Status

```bash
# Show flow file info
FLOW_FILE=$(ps aux | grep -v grep | grep "mitmweb.*8080" | grep -o "claude-flows-[0-9-]*.mitm" | head -1)
if [ -n "$FLOW_FILE" ]; then
    echo ""
    echo "📁 Flow File: ~/$FLOW_FILE"
    if [ -f "$HOME/$FLOW_FILE" ]; then
        FLOW_SIZE=$(ls -lh "$HOME/$FLOW_FILE" | awk '{print $5}')
        echo "   Size: $FLOW_SIZE"
    fi
fi

# Check port status
echo ""
echo "🔌 Port Status:"
if lsof -i :8080 > /dev/null 2>&1; then
    echo "   ✓ Port 8080 (proxy) - LISTENING"
else
    echo "   ✗ Port 8080 (proxy) - NOT LISTENING"
fi

if lsof -i :8081 > /dev/null 2>&1; then
    echo "   ✓ Port 8081 (web) - LISTENING"
else
    echo "   ✗ Port 8081 (web) - NOT LISTENING"
fi
```

## Output Format

The command provides formatted output with:

```
╔════════════════════════════════════════════════════════════════╗
║           Connect Claude Code to CC-Trace Session              ║
╚════════════════════════════════════════════════════════════════╝

✓ mitmweb is running (PID: 24007)

[Three connection options displayed in boxes]

📊 SESSION INFO
   • Web Interface: http://127.0.0.1:8081
   • Password: cc-trace
   • Proxy Port: 8080
   • Flow File: ~/claude-flows-20251114-160545.mitm

[Additional status information]
```

**Important**: When copying commands, copy ONLY the actual command text, not the box-drawing characters (│, ┐, ┘, etc.). For Option 1, copy just:
```
bash ~/.claude/plugins/marketplaces/grey-haven-plugins/grey-haven-plugins/cc-trace/scripts/proxy-claude.sh
```

## Error Handling

### mitmweb Not Running

```
✗ mitmweb is not running

To start a capture session:
1. Run /cc-trace-start
2. Then run /cc-trace-connect
```

### Certificate Not Found

```
⚠️  Warning: mitmproxy certificate not found

Run /cc-trace-setup to generate and trust the certificate
```

### Port Conflicts

```
⚠️  Port 8080 is in use but mitmweb is not running

Check what's using the port:
  lsof -i :8080

Kill the conflicting process or use different ports
```

## Use Cases

### 1. After Starting mitmweb

You've just run `/cc-trace-start` and need to know how to connect:

```bash
/cc-trace-connect
```

Get the exact commands to run in a new terminal.

### 2. Forgot Connection Details

You started mitmweb earlier and can't remember the password or commands:

```bash
/cc-trace-connect
```

See all connection info and session details.

### 3. Sharing Setup with Team

Need to show someone how to connect to an active session:

```bash
/cc-trace-connect
```

Share the output with ready-to-use commands.

## Quick Reference

```bash
# Start capture session
/cc-trace-start

# Get connection instructions
/cc-trace-connect

# In new terminal, use one of the provided commands
# Then use Claude Code normally
```

## Related Commands

- `/cc-trace-setup` - Initial setup for cc-trace
- `/cc-trace-start` - Start a capture session
- Use `cc-trace` agent for interactive troubleshooting

## Tips

1. **Use Option 1** - The proxy script is the easiest, just one command to copy
2. **Keep this terminal open** - It shows you the connection commands
3. **Open a new terminal** - Don't close this one, open another
4. **Copy the ENTIRE command** - Don't include the box characters (│)
5. **Check the browser** - Make sure http://127.0.0.1:8081 is accessible
6. **Use the password** - Enter `cc-trace` when prompted

## Common Workflow

```bash
# Terminal 1 (this one)
/cc-trace-start        # Start mitmweb
/cc-trace-connect      # Get connection commands

# Terminal 2 (new)
# Copy-paste one of the commands from /cc-trace-connect output
# Use Claude Code normally
# Exit when done

# Browser
# Open http://127.0.0.1:8081
# Enter password: cc-trace
# Watch traffic in real-time
```

## What You'll See

After connecting and using Claude Code in the proxied terminal:

**In Browser (http://127.0.0.1:8081):**
- List of all API requests
- System prompts sent to Claude
- Tool definitions and parameters
- User messages and file contents
- Tool call results
- Token usage per request
- Streaming response events

**In Proxied Terminal:**
- Normal Claude Code interface
- No visible difference in functionality
- All features work as expected

**In This Terminal:**
- Status updates
- Flow file size growing
- Request count (if monitoring enabled)

---

**Note**: You cannot run the proxy commands in this terminal. This is an active Claude session. You need a separate terminal to start a new Claude instance through the proxy.
