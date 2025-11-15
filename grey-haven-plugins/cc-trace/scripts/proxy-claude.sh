#!/usr/bin/env bash
# CC-Trace proxy launcher - run Claude Code through mitmproxy
# Usage: bash scripts/proxy-claude.sh

set -e

# Set proxy environment variables
export HTTP_PROXY=http://127.0.0.1:8080
export HTTPS_PROXY=http://127.0.0.1:8080
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
export NODE_EXTRA_CA_CERTS="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
export NODE_TLS_REJECT_UNAUTHORIZED=0

echo "🔍 Proxy configured for mitmproxy (http://127.0.0.1:8080)"
echo "📜 Using CA cert: $NODE_EXTRA_CA_CERTS"
echo "🚀 Starting Claude Code..."
echo ""

# Run Claude Code with all arguments passed through
claude "$@"

# Clean up proxy variables when done
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy NODE_EXTRA_CA_CERTS NODE_TLS_REJECT_UNAUTHORIZED

echo ""
echo "🧹 Proxy environment cleaned up"
