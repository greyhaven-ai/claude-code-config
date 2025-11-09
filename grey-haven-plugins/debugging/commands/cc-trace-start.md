# CC-Trace Start Session

Help the user start a cc-trace capture session to intercept Claude Code API requests.

## Instructions

1. First, verify setup is complete:
   - Ask if they've run `/cc-trace-setup` or if they need setup help
   - If unsure, offer to run the verification script

2. Explain the two-terminal workflow:

**Terminal 1: Start mitmweb**
```bash
mitmweb --web-port 8081 \
  --set flow_filter='~d api.anthropic.com' \
  --save-stream-file ~/claude-flows.mitm
```

Explanation:
- `--web-port 8081`: Web interface port (access at http://127.0.0.1:8081)
- `--set flow_filter='~d api.anthropic.com'`: Only capture Anthropic API calls
- `--save-stream-file ~/claude-flows.mitm`: Save flows to disk for later analysis

**Terminal 2: Run Claude Code with proxy**
```bash
proxy_claude
```

This sets the necessary proxy environment variables and launches Claude Code.

3. Confirm they can access the web interface:
   - Open browser to http://127.0.0.1:8081
   - Should see mitmweb interface (initially empty)

4. Explain what to expect:
   - As they interact with Claude Code, requests/responses will appear in mitmweb
   - Each API call will show request details, response, and timing
   - Filter syntax can be used to narrow down specific traffic

5. Suggest next steps:
   - Try a simple command to verify traffic is captured
   - Use `/cc-trace-analyze` to analyze the captured traffic
   - Use `/cc-trace-verify` to check if everything is working

## Quick Reference

**Common mitmweb filters**:
- `~m POST`: Only POST requests
- `~c 200`: Only successful responses (200 status)
- `~bs 50000`: Responses larger than 50KB
- `~d api.anthropic.com & ~m POST`: Multiple conditions (AND)

**Stop capture**:
- In Terminal 1: Press Ctrl+C to stop mitmweb
- In Terminal 2: Exit Claude Code normally
- Flows are saved to ~/claude-flows.mitm

**Cleanup**:
```bash
# Unset proxy (if needed to run Claude without proxy)
unset HTTP_PROXY HTTPS_PROXY NODE_EXTRA_CA_CERTS NODE_TLS_REJECT_UNAUTHORIZED
```
