# SLO Implementation Checklist

**Use when implementing SLOs for a service.**

## Prerequisites

- [ ] Monitoring infrastructure in place (Prometheus + Grafana)
- [ ] Historical metrics available (minimum 1 week, 4 weeks preferred)
- [ ] Service criticality tiers defined
- [ ] Stakeholder alignment on reliability philosophy

## Step 1: Service Tier Classification

- [ ] Assess business criticality of service
- [ ] Identify user impact of downtime
- [ ] Classify as Critical (99.95%), Essential (99.9%), Standard (99.5%), or Best Effort (99.0%)
- [ ] Document classification rationale
- [ ] Get stakeholder sign-off on tier assignment

## Step 2: SLI Selection

- [ ] Review available metrics for service
- [ ] Select 1-3 SLIs (avoid over-measurement)
- [ ] Choose availability SLI (most common)
- [ ] Add latency SLI for user-facing services
- [ ] Add error rate SLI for background services
- [ ] Document SLI selection rationale
- [ ] Define what counts as "success" vs "failure"
- [ ] Ensure client errors (4xx) don't count against SLO

## Step 3: SLO Target Setting

- [ ] Review historical performance data
- [ ] Start conservative (99% for new services)
- [ ] Set target based on business requirements
- [ ] Ensure target is achievable but meaningful
- [ ] Calculate monthly downtime allowance
- [ ] Calculate error budget percentage
- [ ] Document target rationale
- [ ] Get stakeholder sign-off on targets

## Step 4: Error Budget Calculation

- [ ] Calculate monthly allowed downtime (minutes)
- [ ] Calculate allowed failure percentage
- [ ] Define budget status levels (healthy, attention, warning, critical, exhausted)
- [ ] Set budget thresholds for each status level
- [ ] Define burn rate thresholds (1.0x, 3.0x, 14.4x)
- [ ] Document error budget policy
- [ ] Establish feature freeze criteria

## Step 5: Prometheus Configuration

### Recording Rules
- [ ] Create SLI recording rules (5m, 30m, 1h, 24h windows)
- [ ] Create availability success rate rules
- [ ] Create latency percentile rules (P50, P95, P99)
- [ ] Create error budget remaining rules
- [ ] Create burn rate calculation rules (1h, 6h, 24h)
- [ ] Test recording rules with historical data
- [ ] Verify rule performance (query time <5s)

### Alert Rules
- [ ] Create fast burn alert (14.4x over 1h) - CRITICAL
- [ ] Create slow burn alert (3x over 6h) - WARNING
- [ ] Create budget exhaustion alert (<10% remaining)
- [ ] Configure alert for conditions (1h AND 5m for fast burn)
- [ ] Set appropriate alert durations (2m for fast, 15m for slow)
- [ ] Add alert annotations (summary, description, runbook URL)
- [ ] Configure alert routing (PagerDuty, Slack, email)
- [ ] Test alerts with simulated incidents

## Step 6: Grafana Dashboard

- [ ] Create SLO summary dashboard
- [ ] Add SLO compliance gauge (with thresholds)
- [ ] Add error budget remaining gauge
- [ ] Add burn rate trend graph (1h, 6h, 24h windows)
- [ ] Add availability trend graph (30-day view)
- [ ] Add incident annotations table
- [ ] Configure dashboard alerts
- [ ] Set up dashboard links to runbooks
- [ ] Test dashboard with historical data
- [ ] Share dashboard URL with team

## Step 7: Decision Framework

- [ ] Define release go/no-go criteria
- [ ] Create decision matrix (budget vs risk)
- [ ] Establish escalation procedures
- [ ] Define postmortem triggers
- [ ] Document feature freeze policy
- [ ] Create release checklist referencing SLO status
- [ ] Train team on decision framework
- [ ] Get stakeholder sign-off on policies

## Step 8: Reporting

- [ ] Create monthly SLO report template
- [ ] Define report distribution list
- [ ] Schedule monthly SLO review meetings
- [ ] Set up automated report generation
- [ ] Create executive summary format
- [ ] Document recommendations process
- [ ] Establish report delivery schedule

## Step 9: Runbook Creation

- [ ] Create runbook for fast burn alert
- [ ] Create runbook for slow burn alert
- [ ] Create runbook for budget exhaustion
- [ ] Document investigation procedures
- [ ] Document escalation paths
- [ ] Add troubleshooting tips
- [ ] Link runbooks from alerts
- [ ] Review runbooks with on-call team

## Step 10: Team Training

- [ ] Train team on SLO concepts
- [ ] Explain error budget philosophy
- [ ] Walk through Grafana dashboards
- [ ] Review alert handling procedures
- [ ] Practice incident response scenarios
- [ ] Explain release decision framework
- [ ] Document Q&A from training sessions

## Step 11: CI/CD Integration

- [ ] Integrate SLO status check in CI/CD pipeline
- [ ] Create SLO-based release gates
- [ ] Add error budget check before deployments
- [ ] Fail pipeline if budget <10%
- [ ] Display SLO status in deployment dashboard
- [ ] Document override procedures for critical fixes

## Post-Implementation

- [ ] Monitor SLO performance for first week
- [ ] Review burn rate alerts for false positives
- [ ] Adjust alert thresholds if needed
- [ ] Collect team feedback
- [ ] Schedule first monthly review meeting
- [ ] Document lessons learned
- [ ] Refine SLO targets based on actual performance
- [ ] Share success stories with organization

## Ongoing Maintenance

- [ ] Weekly SLO review (30 minutes)
- [ ] Monthly detailed analysis
- [ ] Quarterly SLO target refinement
- [ ] Annual comprehensive SLO audit
- [ ] Continuous runbook improvements
- [ ] Regular team training refreshers

## Critical Validations

- [ ] SLO targets are achievable (not 100%)
- [ ] Client errors (4xx) don't count against SLO
- [ ] Multi-window burn rate alerts configured
- [ ] Feature freeze policy is clear and documented
- [ ] Stakeholders understand error budget concept
- [ ] Team trained on blameless postmortem culture
- [ ] Release decision framework is documented
- [ ] Monthly reporting is automated
- [ ] Runbooks are linked from all alerts
- [ ] CI/CD integration prevents deployments when budget exhausted
