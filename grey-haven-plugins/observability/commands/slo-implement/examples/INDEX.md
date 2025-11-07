# SLO Implementation Examples

Complete examples demonstrating SLO implementations for different service types.

## Available Examples

### [api-service-slo.md](api-service-slo.md)
Complete SLO implementation for API Gateway service.
- Service tier classification (Critical)
- Availability and latency SLIs
- 99.9% availability target
- Error budget calculation (43.2 minutes/month)
- Prometheus recording rules
- Burn rate alerts (fast and slow burn)
- Grafana dashboard configuration
- Release decision framework

### [data-pipeline-slo.md](data-pipeline-slo.md)
SLO implementation for data pipeline service.
- Service tier classification (Essential)
- Data freshness and completeness SLIs
- 99.0% freshness target (30-minute SLA)
- Error budget for batch processing
- Pipeline-specific metrics
- Backlog monitoring
- Processing time tracking

### [error-budget-calculation.md](error-budget-calculation.md)
Error budget calculation examples and scenarios.
- Budget calculation formulas
- Real-world examples (99.9%, 99.95%, 99.5% SLOs)
- Budget status determination (healthy, warning, critical, exhausted)
- Time-until-exhaustion calculations
- Budget recovery projections
- Release decision examples

### [burn-rate-alerts.md](burn-rate-alerts.md)
Burn rate alert configuration and tuning.
- Fast burn alert (14.4x over 1h) setup
- Slow burn alert (3x over 6h) setup
- Multi-window alert logic
- False positive reduction strategies
- Alert routing and escalation
- Runbook integration
- Alert tuning based on historical data

## Quick Reference

**Need API SLO example?** → [api-service-slo.md](api-service-slo.md)
**Need data pipeline SLO?** → [data-pipeline-slo.md](data-pipeline-slo.md)
**Need error budget help?** → [error-budget-calculation.md](error-budget-calculation.md)
**Need burn rate alerts?** → [burn-rate-alerts.md](burn-rate-alerts.md)
