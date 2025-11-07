# SLO Reference Documentation

Configuration references and formulas for SLO implementation.

## Available References

### [prometheus-rules.md](prometheus-rules.md)
Prometheus recording rules for SLI calculations.
- Availability SLI recording rules (5m, 30m, 1h, 24h windows)
- Latency SLI recording rules (P50, P95, P99 percentiles)
- Error rate SLI recording rules
- Error budget remaining calculations
- Burn rate calculations (1h, 6h, 24h windows)
- Complete Prometheus rule configurations
- Label conventions and best practices

### [alert-rules.md](alert-rules.md)
Prometheus alert rules for burn rate monitoring.
- Fast burn alert (14.4x over 1h) - CRITICAL
- Slow burn alert (3x over 6h) - WARNING
- Budget exhaustion alert (<10% remaining)
- Multi-window alert logic
- Alert severity levels
- Runbook URL integration
- Alert annotation templates

### [grafana-dashboards.md](grafana-dashboards.md)
Grafana dashboard JSON templates for SLO monitoring.
- SLO summary panel (gauge with thresholds)
- Error budget remaining panel (gauge)
- Burn rate trend panel (multi-window graph)
- Availability trend panel (30-day view)
- Incident annotations table
- Executive summary dashboard
- Per-service detail dashboards

### [slo-formulas.md](slo-formulas.md)
SLI calculation formulas and examples.
- Availability calculation
- Latency percentile calculation
- Error rate calculation
- Error budget formula
- Burn rate formula
- Time-until-exhaustion calculation
- Budget recovery estimation

## Quick Reference

**Need Prometheus rules?** → [prometheus-rules.md](prometheus-rules.md)
**Need alert configurations?** → [alert-rules.md](alert-rules.md)
**Need Grafana dashboards?** → [grafana-dashboards.md](grafana-dashboards.md)
**Need calculation formulas?** → [slo-formulas.md](slo-formulas.md)
