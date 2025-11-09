# CC-Trace Verify Setup

Run the cc-trace verification script to check if everything is properly configured.

## Instructions

1. Run the verification script:

```bash
~/.config/claude/plugins/debugging/scripts/verify-setup.sh
```

2. Interpret the results:

The script checks:

✅ **mitmproxy Installation**: Confirms mitmproxy is installed and shows version
✅ **Certificate Exists**: Verifies ~/.mitmproxy/mitmproxy-ca-cert.pem exists
✅ **Certificate Trusted**: Checks if certificate is in system keychain (macOS)
✅ **Shell Function**: Confirms proxy_claude function is defined
✅ **Port Availability**: Ensures ports 8080 and 8081 are free
✅ **Node.js Available**: Verifies Node.js for TypeScript parsing (optional)

3. Based on results, provide guidance:

### If All Checks Pass

The setup is complete! Next steps:
- Use `/cc-trace-start` to begin a capture session
- Try capturing a simple interaction
- Use `/cc-trace-analyze` to examine the captured traffic

### If Checks Fail

Common issues and fixes:

**mitmproxy not found**:
```bash
# macOS
brew install mitmproxy

# Linux
sudo apt-get install mitmproxy  # Debian/Ubuntu
sudo dnf install mitmproxy      # Fedora
```

**Certificate not found**:
```bash
# Generate certificate by running mitmproxy once
mitmproxy  # Press Ctrl+C to quit after it starts
```

**Certificate not trusted**:
```bash
# macOS
security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem

# Linux
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt
sudo update-ca-certificates
```

**proxy_claude function not found**:

Add to `~/.zshrc` or `~/.bashrc`:
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

Then reload: `source ~/.zshrc`

**Ports in use**:
```bash
# Find what's using the port
lsof -i :8080
lsof -i :8081

# Either stop the process or use different ports
mitmweb --listen-port 9090 --web-port 9091
```

**Node.js not found** (optional):
```bash
# macOS
brew install node

# Linux
sudo apt-get install nodejs npm  # Debian/Ubuntu
sudo dnf install nodejs npm      # Fedora
```

4. Offer to run full setup if multiple checks fail:
   - Use `/cc-trace-setup` for guided setup

## Manual Verification

If the script doesn't work or user wants to check manually:

```bash
# Check mitmproxy
which mitmproxy
mitmproxy --version

# Check certificate
ls -la ~/.mitmproxy/mitmproxy-ca-cert.pem

# Check certificate trust (macOS)
security verify-cert -c ~/.mitmproxy/mitmproxy-ca-cert.pem

# Check shell function
type proxy_claude

# Check ports
lsof -i :8080
lsof -i :8081
```

## After Verification

Once everything passes:
1. Start a capture session: `/cc-trace-start`
2. Test with a simple Claude Code interaction
3. Verify traffic appears in mitmweb UI
4. Try analysis tools: `/cc-trace-analyze`

Remind: This tool is for local debugging only. Never use in production or share captured flows without redacting sensitive data.
