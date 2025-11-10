#!/bin/bash
# Cloudflare Deployment Monitoring Script
#
# Usage: ./monitor-deployment.sh [worker-name] [environment]
# Example: ./monitor-deployment.sh production-worker production

set -euo pipefail

# Configuration
WORKER_NAME="${1:-production-worker}"
ENVIRONMENT="${2:-production}"
MONITOR_DURATION="${3:-300}"  # 5 minutes default
CHECK_INTERVAL=10
ERROR_THRESHOLD=0.01  # 1% error rate threshold

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check required tools
check_dependencies() {
    local deps=("wrangler" "curl" "jq")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "$dep is not installed. Please install it first."
            exit 1
        fi
    done
}

# Get deployment info
get_deployment_info() {
    log_info "Fetching deployment information for $WORKER_NAME..."

    # Get latest deployment
    DEPLOYMENT_INFO=$(wrangler deployments list --name "$WORKER_NAME" --json 2>/dev/null || echo "[]")

    if [ "$DEPLOYMENT_INFO" = "[]" ]; then
        log_warn "No deployments found for $WORKER_NAME"
        return 1
    fi

    LATEST_DEPLOYMENT=$(echo "$DEPLOYMENT_INFO" | jq -r '.[0].id')
    DEPLOYMENT_TIME=$(echo "$DEPLOYMENT_INFO" | jq -r '.[0].created_on')

    log_info "Latest deployment: $LATEST_DEPLOYMENT"
    log_info "Deployed at: $DEPLOYMENT_TIME"
}

# Monitor worker metrics
monitor_metrics() {
    local start_time=$(date +%s)
    local end_time=$((start_time + MONITOR_DURATION))

    log_info "Monitoring $WORKER_NAME for $MONITOR_DURATION seconds..."
    echo

    while [ $(date +%s) -lt $end_time ]; do
        # Get worker analytics
        ANALYTICS=$(curl -s -X GET \
            "https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/workers/scripts/${WORKER_NAME}/analytics" \
            -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
            -H "Content-Type: application/json")

        # Parse metrics
        REQUESTS=$(echo "$ANALYTICS" | jq -r '.result.requests // 0')
        ERRORS=$(echo "$ANALYTICS" | jq -r '.result.errors // 0')
        SUCCESS=$(echo "$ANALYTICS" | jq -r '.result.success // 0')
        DURATION_P50=$(echo "$ANALYTICS" | jq -r '.result.duration.p50 // 0')
        DURATION_P95=$(echo "$ANALYTICS" | jq -r '.result.duration.p95 // 0')
        DURATION_P99=$(echo "$ANALYTICS" | jq -r '.result.duration.p99 // 0')

        # Calculate error rate
        if [ "$REQUESTS" -gt 0 ]; then
            ERROR_RATE=$(echo "scale=4; $ERRORS / $REQUESTS" | bc)
        else
            ERROR_RATE=0
        fi

        # Display metrics
        clear
        echo "============================================="
        echo "  Cloudflare Worker Monitoring Dashboard"
        echo "============================================="
        echo
        echo "Worker:       $WORKER_NAME"
        echo "Environment:  $ENVIRONMENT"
        echo "Time:         $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Elapsed:      $(($(date +%s) - start_time))s / ${MONITOR_DURATION}s"
        echo
        echo "---------------------------------------------"
        echo "  Metrics"
        echo "---------------------------------------------"
        echo
        printf "Requests:     %'d\n" "$REQUESTS"
        printf "Errors:       %'d\n" "$ERRORS"
        printf "Success:      %'d\n" "$SUCCESS"
        echo
        echo "Error Rate:   $(printf '%.2f%%' $(echo "$ERROR_RATE * 100" | bc))"

        # Check if error rate exceeds threshold
        if (( $(echo "$ERROR_RATE > $ERROR_THRESHOLD" | bc -l) )); then
            echo -e "${RED}⚠ ERROR RATE ABOVE THRESHOLD!${NC}"
        else
            echo -e "${GREEN}✓ Error rate within threshold${NC}"
        fi

        echo
        echo "---------------------------------------------"
        echo "  Latency"
        echo "---------------------------------------------"
        echo
        printf "P50:          %'dms\n" "$DURATION_P50"
        printf "P95:          %'dms\n" "$DURATION_P95"
        printf "P99:          %'dms\n" "$DURATION_P99"
        echo
        echo "---------------------------------------------"

        # Check for anomalies
        if [ "$DURATION_P95" -gt 500 ]; then
            echo -e "${YELLOW}⚠ P95 latency above 500ms${NC}"
        fi

        if [ "$DURATION_P99" -gt 1000 ]; then
            echo -e "${RED}⚠ P99 latency above 1000ms${NC}"
        fi

        echo
        echo "Press Ctrl+C to stop monitoring"

        sleep $CHECK_INTERVAL
    done
}

# Check health endpoint
check_health() {
    log_info "Checking health endpoint..."

    local health_url="${HEALTH_URL:-https://${ENVIRONMENT}.example.com/health}"

    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$health_url" || echo "000")

    if [ "$RESPONSE" = "200" ]; then
        log_info "Health check passed (HTTP $RESPONSE)"
        return 0
    else
        log_error "Health check failed (HTTP $RESPONSE)"
        return 1
    fi
}

# Get recent logs
get_recent_logs() {
    log_info "Fetching recent logs..."

    # Tail logs for 30 seconds
    timeout 30 wrangler tail "$WORKER_NAME" --format=pretty | tee /tmp/worker-logs.txt || true

    # Count errors
    ERROR_COUNT=$(grep -i "error\|exception\|fail" /tmp/worker-logs.txt | wc -l || echo 0)

    if [ "$ERROR_COUNT" -gt 0 ]; then
        log_warn "Found $ERROR_COUNT error log entries"
        echo
        log_info "Recent errors:"
        grep -i "error\|exception\|fail" /tmp/worker-logs.txt | tail -5
    else
        log_info "No errors found in recent logs"
    fi
}

# Generate report
generate_report() {
    local report_file="deployment-report-$(date +%Y%m%d-%H%M%S).txt"

    log_info "Generating deployment report: $report_file"

    cat > "$report_file" <<EOF
Cloudflare Deployment Monitoring Report
========================================

Generated: $(date)
Worker: $WORKER_NAME
Environment: $ENVIRONMENT

Deployment Information
----------------------
Deployment ID: $LATEST_DEPLOYMENT
Deployed At: $DEPLOYMENT_TIME

Health Check
------------
Status: $(check_health && echo "PASSED" || echo "FAILED")

Recent Metrics
--------------
Requests: $REQUESTS
Errors: $ERRORS
Error Rate: $(printf '%.2f%%' $(echo "$ERROR_RATE * 100" | bc))
P50 Latency: ${DURATION_P50}ms
P95 Latency: ${DURATION_P95}ms
P99 Latency: ${DURATION_P99}ms

Recommendations
---------------
EOF

    # Add recommendations based on metrics
    if (( $(echo "$ERROR_RATE > $ERROR_THRESHOLD" | bc -l) )); then
        echo "⚠ ERROR RATE ELEVATED - Investigate error logs" >> "$report_file"
    fi

    if [ "$DURATION_P95" -gt 500 ]; then
        echo "⚠ P95 LATENCY HIGH - Optimize slow endpoints" >> "$report_file"
    fi

    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "⚠ ERRORS IN LOGS - Review error patterns" >> "$report_file"
    fi

    log_info "Report saved to $report_file"
}

# Main execution
main() {
    log_info "Starting Cloudflare deployment monitoring..."
    echo

    # Check dependencies
    check_dependencies

    # Check required environment variables
    if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
        log_error "CLOUDFLARE_API_TOKEN environment variable not set"
        exit 1
    fi

    if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
        log_error "CLOUDFLARE_ACCOUNT_ID environment variable not set"
        exit 1
    fi

    # Get deployment info
    get_deployment_info || exit 1

    # Check health
    check_health || log_warn "Health check failed, but continuing monitoring..."

    # Monitor metrics
    monitor_metrics

    # Get recent logs
    echo
    get_recent_logs

    # Generate report
    echo
    generate_report

    log_info "Monitoring complete!"
}

# Run main function
main "$@"
