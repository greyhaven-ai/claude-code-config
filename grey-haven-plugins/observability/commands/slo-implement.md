---
name: slo-implement
description: Implement comprehensive SLO (Service Level Objective) framework with error budgets, burn rate monitoring, and SLO-based decision making. Define SLIs, calculate error budgets, configure burn rate alerts, and create SLO dashboards.
---

# SLO Implementation - Google SRE Framework

Comprehensive SLO (Service Level Objective) implementation following Google SRE best practices.

## Overview

This command implements a production-ready SLO framework including:
- **SLI Definition** (Service Level Indicators) - What to measure
- **SLO Targets** - Reliability goals by service tier
- **Error Budget** - Allowed unreliability for innovation
- **Burn Rate Monitoring** - Early warning system before SLO violations
- **SLO Dashboards** - Real-time visibility into reliability
- **Decision Framework** - SLO-based release go/no-go criteria

## Prerequisites

- Monitoring infrastructure (Prometheus + Grafana)
- Historical metrics (at least 1 week, 4 weeks preferred)
- Defined service criticality tiers
- Stakeholder alignment on reliability targets

## SLO Framework Philosophy

**Key Principles:**

1. **Not 100% Uptime**: Perfect reliability slows innovation. Target 99.9% allows 43 minutes downtime/month for improvements and experimentation.

2. **Error Budget**: Unreliability budget enables risk-taking. If budget remains, ship fast. If exhausted, freeze features and focus on reliability.

3. **User-Centric**: Measure what users experience, not what servers report. Failed requests matter, not server reboots.

4. **Proactive Detection**: Burn rate alerts catch issues before SLO violation, preventing customer impact.

## Service Tier Classification

**Four tiers with different reliability targets:**

| Tier | Availability | Downtime/Month | Use Cases |
|------|-------------|----------------|-----------|
| **Critical** | 99.95% | 21.6 minutes | Payment processing, Authentication, Core API |
| **Essential** | 99.9% | 43.2 minutes | Search, Notifications, Analytics |
| **Standard** | 99.5% | 3.6 hours | Reporting, Admin tools, Background jobs |
| **Best Effort** | 99.0% | 7.2 hours | Beta features, Internal tools, Dev environments |

**Classification Guidelines:**
- **Critical**: Revenue-impacting, customer-facing, no acceptable downtime
- **Essential**: Important features, degraded experience acceptable briefly
- **Standard**: Non-critical features, can tolerate occasional failures
- **Best Effort**: Experimental features, no guarantees

## Three Primary SLI Types

### 1. Availability SLI
Percentage of successful requests over total requests.

**Definition**:
- Success: HTTP 200-299, 400-499 (client errors don't count against SLO)
- Failure: HTTP 500-599, timeouts, connection errors

**Calculation**:
```
Availability = (Successful Requests / Total Requests) × 100
```

**When to use**: APIs, web services, microservices

### 2. Latency SLI
Percentage of requests faster than a defined threshold.

**Definition**:
- Measure P50, P95, P99 latencies
- Set threshold based on user experience (e.g., 500ms)
- Count requests meeting threshold

**Calculation**:
```
Latency SLI = (Requests < Threshold / Total Requests) × 100
```

**When to use**: User-facing APIs, real-time services, interactive applications

### 3. Error Rate SLI
Percentage of requests without server-side errors.

**Definition**:
- Server errors: 5xx responses, timeouts, business logic failures
- Client errors (4xx) don't count against SLO
- Calculate error rate and invert for SLI

**Calculation**:
```
Error Rate = (Server Errors / Total Requests) × 100
SLI = 100 - Error Rate
```

**When to use**: Background jobs, data pipelines, batch processing

## Error Budget Management

**Error Budget = 100% - SLO Target**

Example for 99.9% SLO:
- Error budget: 0.1%
- Monthly downtime: 43.2 minutes
- If actual is 99.95%: 50% budget remaining (healthy)
- If actual is 99.85%: Budget exhausted (feature freeze)

**Budget Status Levels**:
- **Healthy** (>75% remaining): Safe to ship features
- **Attention** (50-75% remaining): Monitor closely
- **Warning** (25-50% remaining): Reduce risk, staged rollouts
- **Critical** (10-25% remaining): High-risk changes only
- **Exhausted** (<10% remaining): Feature freeze, focus on reliability

**Decision Matrix**:
```
Budget >75% + Low Risk    = APPROVE (standard release)
Budget >50% + Medium Risk = APPROVE (enhanced monitoring)
Budget >25% + Low Risk    = APPROVE (blue-green deployment)
Budget <10%               = FEATURE FREEZE (reliability only)
```

## Burn Rate Monitoring

**Burn Rate = (Actual Error Rate) / (Allowed Error Rate)**

Burn rate tells how fast you're consuming error budget:
- **1.0x**: Normal consumption rate (OK)
- **3.0x**: Slow burn - 10% monthly budget consumed in 6 hours
- **14.4x**: Fast burn - 2% monthly budget consumed in 1 hour

**Google SRE Multi-Window Alerts**:
1. **Fast Burn Alert** (14.4x over 1h) = CRITICAL
   - Triggers when 2% of monthly budget consumed in 1 hour
   - Requires immediate action

2. **Slow Burn Alert** (3x over 6h) = WARNING
   - Triggers when 10% of monthly budget consumed in 6 hours
   - Investigation recommended

**Why Multi-Window?**
- Catches both sudden spikes and gradual degradation
- Reduces false positives by requiring sustained burn rate
- Provides early warning before SLO violation

## Implementation Process

Follow these steps to implement SLOs:

### Step 1: Choose Service Tier
- Assess business criticality
- Identify user impact of downtime
- Classify as Critical, Essential, Standard, or Best Effort
- Get stakeholder sign-off

### Step 2: Define SLIs
- Select 1-3 SLIs per service (avoid over-measurement)
- Availability (most common)
- Latency (user-facing services)
- Error rate (background services)

### Step 3: Set SLO Targets
- Start conservative (99% for new services)
- Use historical data to inform targets
- Ensure targets are achievable but meaningful
- Document target rationale

### Step 4: Calculate Error Budget
- Monthly allowed downtime in minutes
- Allowed failure percentage
- Current budget status
- Burn rate thresholds

### Step 5: Configure Monitoring
- Prometheus recording rules for SLI calculations
- Burn rate alert rules (fast and slow burn)
- Grafana dashboards for visualization
- Monthly reporting automation

### Step 6: Establish Decision Framework
- Release go/no-go criteria
- Escalation procedures
- Postmortem triggers
- Feature freeze policy

## Output Format

When implementing SLOs, provide:

1. **SLI Selection & Rationale**
   - Chosen indicators with justification
   - Measurement methodology
   - Data source configuration

2. **SLO Targets by Service Tier**
   - Tier assignment with justification
   - Monthly downtime allowance
   - Stakeholder sign-off status

3. **Error Budget Calculation**
   - Allowed failure percentage
   - Monthly downtime budget
   - Current budget status
   - Burn rate thresholds

4. **Monitoring Configuration**
   - Prometheus recording rules
   - Burn rate alert rules (1h, 6h windows)
   - SLO compliance queries
   - Grafana dashboard JSON

5. **Decision Framework**
   - Release criteria matrix
   - Escalation procedures
   - Postmortem triggers

6. **Monthly SLO Report Template**
   - Compliance status
   - Incident summary
   - Recommendations

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete SLO implementation examples
  - [api-service-slo.md](examples/api-service-slo.md) - API service SLO implementation
  - [data-pipeline-slo.md](examples/data-pipeline-slo.md) - Data pipeline SLO implementation
  - [error-budget-calculation.md](examples/error-budget-calculation.md) - Error budget examples
  - [burn-rate-alerts.md](examples/burn-rate-alerts.md) - Burn rate alert setup
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Configuration references
  - [prometheus-rules.md](reference/prometheus-rules.md) - Prometheus recording rules
  - [alert-rules.md](reference/alert-rules.md) - Burn rate alert configurations
  - [grafana-dashboards.md](reference/grafana-dashboards.md) - Dashboard JSON templates
  - [slo-formulas.md](reference/slo-formulas.md) - SLI calculation formulas
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [api-slo-config.yaml](templates/api-slo-config.yaml) - API service SLO template
  - [pipeline-slo-config.yaml](templates/pipeline-slo-config.yaml) - Data pipeline SLO template
  - [monthly-report.html](templates/monthly-report.html) - Monthly report template

- **[checklists/](checklists/)** - SLO implementation checklists
  - [slo-implementation-checklist.md](checklists/slo-implementation-checklist.md) - Implementation checklist

## When to Apply This Command

Use this command when:
- Setting up SLOs for new or existing services
- Defining error budgets for release decisions
- Implementing burn rate monitoring
- Creating SLO dashboards
- Establishing reliability targets
- Implementing feature freeze policies based on error budgets

## Critical Reminders

1. **Start Conservative**: New services should start with 99% SLO, increase based on actual performance
2. **User-Centric**: Measure what users experience, not what servers report
3. **Multi-Window Alerts**: Use both fast (1h) and slow (6h) burn rate alerts
4. **Error Budget Policy**: Establish clear feature freeze policy when budget exhausted
5. **Monthly Reviews**: Review SLO performance monthly, adjust targets based on data
6. **Stakeholder Alignment**: Get executive sign-off on SLO targets and error budget policy
7. **Blameless Culture**: Use SLO violations as learning opportunities, not blame assignments
8. **Client Errors Don't Count**: 4xx errors are client mistakes, don't count against SLO
9. **Toil Budget**: SRE teams should spend <50% time on operational work (toil)
10. **Progressive Refinement**: Start simple (1-2 SLIs), add complexity as needed

## Next Steps

After implementing SLOs:

1. Schedule weekly SLO review meetings (30 minutes)
2. Integrate SLO status into CI/CD pipelines
3. Create SLO-based release gates
4. Train team on error budget policies
5. Implement blameless postmortem culture
6. Set up automated monthly SLO reporting
7. Refine SLO targets based on actual performance data

## References

- [Google SRE Book - Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Workbook - SLO Engineering Case Study](https://sre.google/workbook/slo-engineering-case-study/)
- [The Art of SLOs](https://cloud.google.com/blog/products/management-tools/the-art-of-slos)
