---
name: cc-trace-setup
description: Automated setup assistant for cc-trace - install mitmproxy, configure certificates, and verify the environment for intercepting Claude Code API traffic
---

Set up cc-trace for intercepting and debugging Claude Code API requests using mitmproxy. This command will guide you through the complete setup process automatically.

## What This Command Does

1. **Check Prerequisites**
   - Verify operating system compatibility
   - Check for required tools (brew, python, etc.)
   - Confirm admin permissions available

2. **Install mitmproxy**
   - Install via platform package manager (Homebrew/apt/pip)
   - Verify installation successful
   - Check version compatibility (9.0+)

3. **Generate & Trust Certificate**
   - Generate mitmproxy CA certificate
   - Add to system keychain/trust store
   - Verify certificate trust status

4. **Verify Setup**
   - Run automated verification script
   - Test proxy configuration
   - Confirm certificate validation

5. **Provide Usage Instructions**
   - Show how to start capture sessions
   - Explain terminal setup
   - Demonstrate basic workflows

## Implementation Steps

When you use this command, Claude will:

### Step 1: Environment Check
```bash
# Check OS type
uname -s

# Check if Homebrew installed (macOS)
which brew

# Check if mitmproxy already installed
which mitmproxy
```

### Step 2: Install mitmproxy

**macOS:**
```bash
brew install mitmproxy
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update && sudo apt install -y mitmproxy
```

**Linux (RHEL/Fedora):**
```bash
sudo dnf install -y mitmproxy
```

**Universal (Python):**
```bash
pip install mitmproxy
```

Verify installation:
```bash
mitmproxy --version
```

### Step 3: Generate Certificate

Run mitmproxy briefly to generate CA certificate:
```bash
# Start and immediately stop mitmproxy to generate cert
timeout 2 mitmproxy 2>/dev/null || true
# OR
mitmproxy &
sleep 2
pkill mitmproxy
```

Verify certificate exists:
```bash
ls -la ~/.mitmproxy/mitmproxy-ca-cert.pem
```

### Step 4: Trust Certificate

**macOS:**
```bash
# Add certificate to system keychain
sudo security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem

# Verify trust
security find-certificate -c mitmproxy -a
```

**Linux (Debian/Ubuntu):**
```bash
# Copy certificate to trusted CA directory
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem \
  /usr/local/share/ca-certificates/mitmproxy.crt

# Update CA certificates
sudo update-ca-certificates
```

**Linux (RHEL/Fedora):**
```bash
# Copy certificate
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem \
  /etc/pki/ca-trust/source/anchors/mitmproxy.pem

# Update trust
sudo update-ca-trust
```

### Step 5: Verify Setup

Run the bundled verification script:
```bash
bash ~/.claude/plugins/marketplaces/grey-haven-plugins/grey-haven-plugins/cc-trace/scripts/verify-setup.sh
```

The script checks:
- ✓ mitmproxy installation
- ✓ Certificate generation
- ✓ Certificate trust (macOS)
- ✓ Proxy configuration readiness

### Step 6: Test Proxy Connection

```bash
# Start mitmproxy in background
mitmproxy --listen-port 8080 &
MITM_PID=$!

# Test proxy with curl
export HTTPS_PROXY=http://127.0.0.1:8080
export NODE_TLS_REJECT_UNAUTHORIZED=0
curl -I https://api.anthropic.com 2>&1

# Stop mitmproxy
kill $MITM_PID
unset HTTPS_PROXY NODE_TLS_REJECT_UNAUTHORIZED
```

## Success Criteria

Setup is complete when:
- ✅ mitmproxy is installed and working
- ✅ CA certificate exists at `~/.mitmproxy/mitmproxy-ca-cert.pem`
- ✅ Certificate is trusted by system (macOS/Linux)
- ✅ Proxy connection test succeeds
- ✅ Verification script passes all checks

## Usage After Setup

### Option 1: Using the Standalone Script (Recommended)

**Terminal 1 - Start mitmweb:**
```bash
mitmweb --web-port 8081 --set flow_filter='~d api.anthropic.com'
```

**Terminal 2 - Run Claude with proxy:**
```bash
bash ~/.claude/plugins/marketplaces/grey-haven-plugins/grey-haven-plugins/cc-trace/scripts/proxy-claude.sh
```

**Browser - View traffic:**
```
http://127.0.0.1:8081
```

### Option 2: Manual Environment Variables

**Terminal 2:**
```bash
export HTTP_PROXY=http://127.0.0.1:8080
export HTTPS_PROXY=http://127.0.0.1:8080
export NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
export NODE_TLS_REJECT_UNAUTHORIZED=0
claude
```

## Troubleshooting

### Certificate Trust Issues (macOS)

If certificate verification fails:
```bash
# Remove existing certificate
sudo security delete-certificate -c mitmproxy \
  /Library/Keychains/System.keychain 2>/dev/null || true

# Re-add with trust
sudo security add-trusted-cert -d -p ssl -p basic \
  -k /Library/Keychains/System.keychain \
  ~/.mitmproxy/mitmproxy-ca-cert.pem

# Open Keychain Access to verify manually
open /System/Applications/Utilities/Keychain\ Access.app
```

### Port Already in Use

```bash
# Check what's using port 8080
lsof -i :8080

# Kill conflicting process if needed
kill $(lsof -t -i:8080)

# Or use different port
mitmweb --listen-port 9090 --web-port 9091
```

### Permission Denied Errors

If you get permission errors:
```bash
# Ensure you have sudo access
sudo -v

# On Linux, you may need to add your user to relevant groups
sudo usermod -a -G ssl-cert $USER

# Log out and back in for group changes to take effect
```

### mitmproxy Not Starting

```bash
# Check Python version (requires 3.8+)
python3 --version

# Reinstall mitmproxy
pip uninstall mitmproxy
pip install mitmproxy

# Or via package manager
brew reinstall mitmproxy  # macOS
sudo apt reinstall mitmproxy  # Debian/Ubuntu
```

## Security Warnings

⚠️ **Important Security Considerations:**

1. **Local Use Only** - This setup is for local debugging on trusted development machines
2. **TLS Verification Disabled** - `NODE_TLS_REJECT_UNAUTHORIZED=0` disables certificate validation
3. **Sensitive Data** - Captured flows contain API keys, prompts, and file contents
4. **CA Trust** - Trusting mitmproxy's CA allows it to intercept ALL HTTPS traffic
5. **Temporary Setup** - Only use when actively debugging

**Best Practices:**
- Only enable proxy when actively debugging
- Clear captured flows after analysis
- Never share flow files publicly
- Remove certificate trust when done
- Use separate development machine for sensitive work

## Output Format

The command will provide:

1. **Installation Progress**
   ```
   🔧 Installing mitmproxy...
   ✓ mitmproxy 10.1.5 installed successfully

   🔐 Generating certificate...
   ✓ Certificate created: ~/.mitmproxy/mitmproxy-ca-cert.pem

   🔒 Adding certificate to system trust...
   ✓ Certificate trusted in system keychain
   ```

2. **Verification Results**
   ```
   🔍 Verifying setup...
   ✓ mitmproxy installation
   ✓ Certificate generation
   ✓ Certificate trust
   ✓ Proxy connectivity

   ✅ All checks passed! Setup complete.
   ```

3. **Usage Instructions**
   ```
   🚀 Ready to capture traffic!

   Terminal 1:
     mitmweb --web-port 8081 --set flow_filter='~d api.anthropic.com'

   Terminal 2:
     bash ~/.claude/plugins/.../scripts/proxy-claude.sh

   Browser:
     http://127.0.0.1:8081
   ```

## Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: 3.8+ (for mitmproxy)
- **Package Manager**: Homebrew (macOS), apt/dnf (Linux), or pip
- **Permissions**: Ability to trust system certificates (may require sudo)
- **Disk Space**: ~50MB for mitmproxy and dependencies

## Next Steps After Setup

1. **Start a Capture Session** - Follow usage instructions above
2. **Explore Traffic** - Open browser to view captured requests
3. **Analyze API Calls** - Use bundled scripts to extract data
4. **Learn Patterns** - Understand how Claude Code makes tool calls
5. **Optimize Usage** - Identify token consumption and redundant operations

## Related Commands

- `/cc-trace` - Interactive agent for debugging and analysis (coming soon)
- Use the `cc-trace` agent for guided troubleshooting

## Documentation

- **Plugin README**: `~/.claude/plugins/.../cc-trace/README.md`
- **Original Repository**: https://github.com/alexfazio/cc-trace
- **mitmproxy Docs**: https://docs.mitmproxy.org/

---

**Note**: This command performs automated setup. If you encounter issues, you can invoke the `cc-trace` agent for interactive troubleshooting assistance.
