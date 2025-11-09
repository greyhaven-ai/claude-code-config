# CC-Trace Setup

Guide the user through setting up cc-trace for intercepting and analyzing Claude Code API requests.

## Instructions

1. Use the AskUserQuestion tool to determine:
   - What operating system they're using (macOS, Linux, Windows)
   - Whether this is their first time or they're troubleshooting
   - Their experience level with mitmproxy and HTTPS interception

2. Based on their answers, provide appropriate setup instructions:

### For First-Time Setup

**Step 1: Install mitmproxy**
- macOS: `brew install mitmproxy`
- Linux: `sudo apt-get install mitmproxy` or `sudo dnf install mitmproxy`
- Windows: Direct them to mitmproxy.org or use pip

**Step 2: Generate Certificate**
```bash
mitmproxy  # Start once, then quit with Ctrl+C
```

**Step 3: Trust Certificate**

*macOS*:
```bash
security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem
```

*Linux*:
```bash
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt
sudo update-ca-certificates
```

**Step 4: Configure Shell Function**

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

Reload: `source ~/.zshrc` (or `~/.bashrc`)

**Step 5: Verify Setup**

Run the verification script:
```bash
~/.config/claude/plugins/debugging/scripts/verify-setup.sh
```

3. After guiding through setup, explain how to start a capture session using `/cc-trace-start`

### For Troubleshooting

Common issues and solutions:

1. **No traffic appears**:
   - Check if mitmproxy is running: `lsof -i :8080`
   - Verify proxy environment variables are set
   - Ensure proxy_claude was run in the terminal where you start Claude

2. **Certificate errors**:
   - Re-trust the certificate
   - Restart terminal/browser after trusting
   - Verify certificate exists: `ls ~/.mitmproxy/mitmproxy-ca-cert.pem`

3. **Port conflicts**:
   - Use alternate ports: `mitmweb --listen-port 9090 --web-port 9091`
   - Update proxy_claude function with new ports

Always offer to run the verification script to diagnose issues automatically.
