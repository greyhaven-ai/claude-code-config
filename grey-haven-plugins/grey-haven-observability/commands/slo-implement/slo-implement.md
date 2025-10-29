---
name: slo-implement
description: Implement comprehensive SLO (Service Level Objective) framework with error budgets, burn rate monitoring, and SLO-based decision making. Define SLIs, calculate error budgets, configure burn rate alerts, and create SLO dashboards.
---

# SLO Implementation - Google SRE Framework

Comprehensive SLO (Service Level Objective) implementation following Google SRE best practices with error budgets, burn rate monitoring, and automated reporting.

## Overview

This command helps implement a production-ready SLO framework including:
- **SLI Definition** (Service Level Indicators) - what to measure
- **SLO Targets** - reliability goals by service tier
- **Error Budget** - allowed unreliability
- **Burn Rate Monitoring** - early warning system
- **SLO Dashboards** - real-time visibility
- **Decision Framework** - SLO-based release decisions

## Prerequisites

- Monitoring infrastructure (Prometheus + Grafana)
- Historical metrics (at least 1 week preferred)
- Defined service criticality tiers
- Stakeholder alignment on reliability targets

## SLO Framework Philosophy

**Key Principles:**
1. **Not 100% Uptime:** Perfect reliability slows innovation. Target 99.9% allows 43 minutes downtime/month for improvements.
2. **Error Budget:** Unreliability budget enables risk-taking. If budget remains, ship fast. If exhausted, freeze features and fix reliability.
3. **User-Centric:** Measure what users experience, not what servers report. Failed requests matter, not server reboots.
4. **Proactive Detection:** Burn rate alerts catch issues before SLO violation, preventing customer impact.

## Output Format

When implementing SLOs, provide:

1. **SLI Selection & Rationale**
   - Chosen indicators with justification
   - Measurement methodology
   - Data source configuration

2. **SLO Targets by Service Tier**
   - Critical (99.95%), Essential (99.9%), Standard (99.5%), Best Effort (99.0%)
   - Justification for tier assignment
   - Stakeholder sign-off

3. **Error Budget Calculation**
   - Monthly allowed downtime
   - Current budget status
   - Burn rate thresholds

4. **Prometheus Configuration**
   - Recording rules for SLI calculations
   - Burn rate alert rules (1h, 6h, 24h windows)
   - SLO compliance queries

5. **Grafana Dashboards**
   - SLO summary dashboard JSON
   - Per-service SLO details
   - Executive reporting view

6. **Decision Framework**
   - Release go/no-go criteria
   - Escalation procedures
   - Postmortem triggers

7. **Monthly SLO Report Template**
   - Compliance status
   - Incident summary
   - Recommendations

## Service Tier Classification

```python
# slo_framework.py - Service Tier Definitions
from enum import Enum
from dataclasses import dataclass

class ServiceTier(Enum):
    CRITICAL = {
        'availability': 99.95,  # 21.6 minutes/month downtime allowed
        'description': 'Revenue-critical, customer-facing, no acceptable downtime',
        'examples': ['Payment processing', 'Authentication', 'Core API']
    }
    ESSENTIAL = {
        'availability': 99.9,   # 43.2 minutes/month downtime allowed
        'description': 'Important features, degraded experience acceptable briefly',
        'examples': ['Search', 'Notifications', 'Analytics dashboard']
    }
    STANDARD = {
        'availability': 99.5,   # 3.6 hours/month downtime allowed
        'description': 'Non-critical features, can tolerate occasional failures',
        'examples': ['Reporting', 'Admin tools', 'Background jobs']
    }
    BEST_EFFORT = {
        'availability': 99.0,   # 7.2 hours/month downtime allowed
        'description': 'Experimental features, no guarantees',
        'examples': ['Beta features', 'Internal tools', 'Dev environments']
    }

@dataclass
class SLO:
    service_name: str
    tier: ServiceTier
    sli_type: str  # 'availability', 'latency', 'throughput'
    target: float  # e.g., 99.9 for availability, 0.5 for latency (seconds)
    window: str    # '30d', '7d', '90d'
    
    @property
    def error_budget_percentage(self) -> float:
        """Calculate allowed failure percentage"""
        if self.sli_type == 'availability':
            return 100 - self.target
        return self.target  # For latency, target is the threshold
    
    @property
    def monthly_downtime_minutes(self) -> float:
        """Calculate allowed downtime per month (for availability SLOs)"""
        if self.sli_type == 'availability':
            minutes_per_month = 30 * 24 * 60  # ~43,200 minutes
            return minutes_per_month * (100 - self.target) / 100
        return 0
```

## SLI Implementation

### Three Primary SLI Types

```python
# sli_calculator.py - SLI Calculation Functions

class SLICalculator:
    """Calculate Service Level Indicators"""
    
    @staticmethod
    def calculate_availability(total_requests: int, successful_requests: int) -> float:
        """
        Availability SLI: Percentage of successful requests
        
        Success defined as: HTTP 200-299, 400-499 (client errors don't count against SLO)
        Failure defined as: HTTP 500-599, timeouts, connection errors
        """
        if total_requests == 0:
            return 100.0
        return (successful_requests / total_requests) * 100
    
    @staticmethod
    def calculate_latency_sli(percentile_latency_ms: float, threshold_ms: float) -> float:
        """
        Latency SLI: Percentage of requests faster than threshold
        
        Example: If p95 latency is 350ms and threshold is 500ms, SLI = 100%
                 If p95 latency is 600ms and threshold is 500ms, SLI = ~95%
        """
        if percentile_latency_ms <= threshold_ms:
            return 100.0
        # Linear degradation beyond threshold
        degradation = ((percentile_latency_ms - threshold_ms) / threshold_ms) * 100
        return max(0, 100 - degradation)
    
    @staticmethod
    def calculate_error_rate_sli(
        total_requests: int,
        client_errors: int,
        server_errors: int,
        timeouts: int,
        business_logic_errors: int
    ) -> dict:
        """
        Error Rate SLI: Categorized error analysis
        
        Returns breakdown of error types for root cause analysis
        """
        if total_requests == 0:
            return {'total_error_rate': 0, 'breakdown': {}}
        
        errors = {
            'client_errors': client_errors,      # 4xx (not counted against SLO)
            'server_errors': server_errors,      # 5xx (counted)
            'timeouts': timeouts,                # Counted
            'business_errors': business_logic_errors  # Counted
        }
        
        # Only count server-side failures against SLO
        slo_impacting_errors = server_errors + timeouts + business_logic_errors
        error_rate = (slo_impacting_errors / total_requests) * 100
        
        return {
            'error_rate': error_rate,
            'breakdown': {k: (v/total_requests)*100 for k, v in errors.items()}
        }
```

### Prometheus Recording Rules

```yaml
# prometheus-slo-recording-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-recording-rules
  namespace: monitoring
spec:
  groups:
  - name: slo_calculations
    interval: 30s
    rules:
    
    # Availability SLI - Success Rate
    - record: service:sli:availability:success_rate_5m
      expr: |
        sum(rate(http_requests_total{status_code!~"5.."}[5m])) by (service)
        /
        sum(rate(http_requests_total[5m])) by (service)
        * 100
    
    - record: service:sli:availability:success_rate_30m
      expr: |
        sum(rate(http_requests_total{status_code!~"5.."}[30m])) by (service)
        /
        sum(rate(http_requests_total[30m])) by (service)
        * 100
    
    - record: service:sli:availability:success_rate_1h
      expr: |
        sum(rate(http_requests_total{status_code!~"5.."}[1h])) by (service)
        /
        sum(rate(http_requests_total[1h])) by (service)
        * 100
    
    - record: service:sli:availability:success_rate_24h
      expr: |
        sum(rate(http_requests_total{status_code!~"5.."}[24h])) by (service)
        /
        sum(rate(http_requests_total[24h])) by (service)
        * 100
    
    # Latency SLI - Percentile Calculations
    - record: service:sli:latency:p50_5m
      expr: |
        histogram_quantile(0.50, 
          sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
        )
    
    - record: service:sli:latency:p95_5m
      expr: |
        histogram_quantile(0.95, 
          sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
        )
    
    - record: service:sli:latency:p99_5m
      expr: |
        histogram_quantile(0.99, 
          sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
        )
    
    # Error Budget Calculations
    - record: service:error_budget:remaining_percentage
      expr: |
        (service:sli:availability:success_rate_30m - slo:target{type="availability"})
        /
        (100 - slo:target{type="availability"})
        * 100
    
    # Burn Rate Calculations (Multi-Window)
    - record: service:error_budget:burn_rate_1h
      expr: |
        (100 - service:sli:availability:success_rate_1h)
        /
        (100 - slo:target{type="availability"})
    
    - record: service:error_budget:burn_rate_6h
      expr: |
        (100 - service:sli:availability:success_rate_6h)
        /
        (100 - slo:target{type="availability"})
    
    - record: service:error_budget:burn_rate_24h
      expr: |
        (100 - service:sli:availability:success_rate_24h)
        /
        (100 - slo:target{type="availability"})
```

## Error Budget Management

```python
# error_budget.py - Error Budget Calculator

from datetime import datetime, timedelta
from enum import Enum

class BudgetStatus(Enum):
    HEALTHY = "healthy"           # >75% budget remaining
    ATTENTION = "attention"       # 50-75% budget remaining
    WARNING = "warning"           # 25-50% budget remaining
    CRITICAL = "critical"         # 10-25% budget remaining
    EXHAUSTED = "exhausted"       # <10% budget remaining

class ErrorBudgetManager:
    """Manage error budgets and burn rates"""
    
    def __init__(self, slo_target: float, window_days: int = 30):
        self.slo_target = slo_target
        self.window_days = window_days
        self.error_budget_percentage = 100 - slo_target
    
    def calculate_remaining_budget(
        self,
        actual_availability: float
    ) -> dict:
        """
        Calculate remaining error budget
        
        Example:
        - SLO Target: 99.9% (0.1% error budget)
        - Actual: 99.95% (0.05% errors)
        - Budget Used: 50% (0.05% / 0.1%)
        - Budget Remaining: 50%
        """
        actual_error_rate = 100 - actual_availability
        budget_used = (actual_error_rate / self.error_budget_percentage) * 100
        budget_remaining = 100 - budget_used
        
        # Calculate status
        if budget_remaining > 75:
            status = BudgetStatus.HEALTHY
        elif budget_remaining > 50:
            status = BudgetStatus.ATTENTION
        elif budget_remaining > 25:
            status = BudgetStatus.WARNING
        elif budget_remaining > 10:
            status = BudgetStatus.CRITICAL
        else:
            status = BudgetStatus.EXHAUSTED
        
        return {
            'target_availability': self.slo_target,
            'actual_availability': actual_availability,
            'error_budget_percentage': self.error_budget_percentage,
            'budget_used_percentage': budget_used,
            'budget_remaining_percentage': budget_remaining,
            'status': status.value,
            'allowed_downtime_minutes': self.calculate_downtime_minutes(),
            'used_downtime_minutes': self.calculate_downtime_minutes() * (budget_used/100)
        }
    
    def calculate_burn_rate(
        self,
        actual_error_rate: float,
        window_hours: int
    ) -> dict:
        """
        Calculate error budget burn rate
        
        Burn Rate = (Actual Error Rate) / (Allowed Error Rate)
        
        Examples:
        - Burn rate 1.0: Consuming budget at expected rate (OK)
        - Burn rate 14.4: Consuming budget 14.4x faster (CRITICAL)
        - Burn rate 0.5: Consuming budget 2x slower (HEALTHY)
        
        Google SRE Multi-Window Burn Rate Alerts:
        - Fast burn: 14.4x rate over 1h (consumes 2% of monthly budget)
        - Slow burn: 3x rate over 6h (consumes 10% of monthly budget)
        """
        hours_per_month = self.window_days * 24
        burn_rate = actual_error_rate / self.error_budget_percentage
        
        # Calculate budget consumed in this window
        budget_consumed_percentage = (window_hours / hours_per_month) * burn_rate * 100
        
        # Time until budget exhaustion at current rate
        if burn_rate > 0:
            hours_until_exhaustion = hours_per_month / burn_rate
        else:
            hours_until_exhaustion = float('inf')
        
        # Determine alert level
        if burn_rate >= 14.4:
            alert_level = "critical"  # Fast burn
        elif burn_rate >= 3.0:
            alert_level = "warning"   # Slow burn
        elif burn_rate >= 1.0:
            alert_level = "attention" # Normal consumption
        else:
            alert_level = "healthy"
        
        return {
            'burn_rate': burn_rate,
            'budget_consumed_percentage': budget_consumed_percentage,
            'hours_until_exhaustion': hours_until_exhaustion,
            'alert_level': alert_level,
            'window_hours': window_hours
        }
    
    def calculate_downtime_minutes(self) -> float:
        """Calculate allowed downtime in minutes for the window"""
        minutes_in_window = self.window_days * 24 * 60
        return minutes_in_window * (self.error_budget_percentage / 100)
```

## Burn Rate Alert Rules

```yaml
# prometheus-burn-rate-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-burn-rate-alerts
  namespace: monitoring
spec:
  groups:
  - name: slo_burn_rate_alerts
    rules:
    
    # Fast Burn Alert (14.4x burn rate over 1 hour)
    # Triggers when 2% of monthly error budget consumed in 1 hour
    - alert: SLOFastBurn
      expr: |
        service:error_budget:burn_rate_1h{slo_tier="critical"} > 14.4
        and
        service:error_budget:burn_rate_5m{slo_tier="critical"} > 14.4
      for: 2m
      labels:
        severity: critical
        slo_tier: critical
      annotations:
        summary: "Critical SLO fast burn detected"
        description: |
          Service {{ $labels.service }} is burning error budget at {{ $value }}x normal rate.
          At this rate, monthly budget will be exhausted in {{ div 720 $value | humanizeDuration }}.
          
          Current burn rate: {{ $value | humanize }}x
          1h window: {{ $value }}x
          5m window: {{ $value }}x
          
          IMMEDIATE ACTION REQUIRED
        runbook_url: "https://runbooks.example.com/slo-fast-burn"
    
    # Slow Burn Alert (3x burn rate over 6 hours)
    # Triggers when 10% of monthly error budget consumed in 6 hours
    - alert: SLOSlowBurn
      expr: |
        service:error_budget:burn_rate_6h{slo_tier="critical"} > 3
        and
        service:error_budget:burn_rate_30m{slo_tier="critical"} > 3
      for: 15m
      labels:
        severity: warning
        slo_tier: critical
      annotations:
        summary: "SLO slow burn detected"
        description: |
          Service {{ $labels.service }} is burning error budget at {{ $value }}x normal rate.
          At this rate, monthly budget will be exhausted in {{ div 720 $value | humanizeDuration }}.
          
          Investigation recommended.
        runbook_url: "https://runbooks.example.com/slo-slow-burn"
    
    # Budget Exhaustion Warning (< 10% remaining)
    - alert: SLOBudgetExhausted
      expr: |
        service:error_budget:remaining_percentage < 10
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Error budget nearly exhausted"
        description: |
          Service {{ $labels.service }} has only {{ $value }}% error budget remaining.
          
          FEATURE FREEZE - Focus on reliability improvements.
        runbook_url: "https://runbooks.example.com/error-budget-exhausted"
```

## Grafana SLO Dashboard

```python
# generate_slo_dashboard.py - Create SLO Dashboard JSON

def generate_slo_dashboard(service_name: str, slo_target: float):
    """Generate Grafana dashboard for SLO monitoring"""
    
    dashboard = {
        "dashboard": {
            "title": f"SLO Dashboard - {service_name}",
            "tags": ["slo", "reliability", service_name],
            "timezone": "utc",
            "panels": [
                # Panel 1: SLO Summary
                {
                    "title": "SLO Compliance (30d)",
                    "type": "stat",
                    "targets": [{
                        "expr": f'service:sli:availability:success_rate_30d{{service="{service_name}"}}'
                    }],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "percent",
                            "thresholds": {
                                "mode": "absolute",
                                "steps": [
                                    {"value": 0, "color": "red"},
                                    {"value": slo_target - 0.1, "color": "yellow"},
                                    {"value": slo_target, "color": "green"}
                                ]
                            }
                        }
                    }
                },
                
                # Panel 2: Error Budget Status
                {
                    "title": "Error Budget Remaining",
                    "type": "gauge",
                    "targets": [{
                        "expr": f'service:error_budget:remaining_percentage{{service="{service_name}"}}'
                    }],
                    "fieldConfig": {
                        "defaults": {
                            "unit": "percent",
                            "min": 0,
                            "max": 100,
                            "thresholds": {
                                "steps": [
                                    {"value": 0, "color": "red"},
                                    {"value": 10, "color": "orange"},
                                    {"value": 50, "color": "yellow"},
                                    {"value": 75, "color": "green"}
                                ]
                            }
                        }
                    }
                },
                
                # Panel 3: Burn Rate Trend
                {
                    "title": "Error Budget Burn Rate",
                    "type": "graph",
                    "targets": [
                        {
                            "expr": f'service:error_budget:burn_rate_1h{{service="{service_name}"}}',
                            "legendFormat": "1h window"
                        },
                        {
                            "expr": f'service:error_budget:burn_rate_6h{{service="{service_name}"}}',
                            "legendFormat": "6h window"
                        },
                        {
                            "expr": f'service:error_budget:burn_rate_24h{{service="{service_name}"}}',
                            "legendFormat": "24h window"
                        }
                    ],
                    "yaxes": [
                        {"label": "Burn Rate (x)", "format": "short"},
                        {"label": "", "show": False}
                    ],
                    "alert": {
                        "conditions": [{
                            "evaluator": {"type": "gt", "params": [14.4]},
                            "query": {"params": ["A", "5m", "now"]}
                        }]
                    }
                },
                
                # Panel 4: Availability Over Time
                {
                    "title": "Availability Trend (30d)",
                    "type": "graph",
                    "targets": [{
                        "expr": f'service:sli:availability:success_rate_1h{{service="{service_name}"}}'
                    }],
                    "yaxes": [
                        {
                            "label": "Availability %",
                            "format": "percent",
                            "min": slo_target - 1,
                            "max": 100
                        }
                    ],
                    "seriesOverrides": [{
                        "alias": "SLO Target",
                        "color": "red",
                        "fill": 0,
                        "linewidth": 2,
                        "dashes": True
                    }]
                },
                
                # Panel 5: Incident Annotations
                {
                    "title": "Recent Incidents",
                    "type": "table",
                    "targets": [{
                        "expr": f'ALERTS{{alertname=~"SLO.*", service="{service_name}"}}'
                    }],
                    "transformations": [
                        {"id": "organize", "options": {
                            "includeByName": {
                                "alertname": True,
                                "severity": True,
                                "Time": True
                            }
                        }}
                    ]
                }
            ]
        }
    }
    
    return dashboard
```

## SLO Reporting

```python
# slo_reporter.py - Generate SLO Reports

from datetime import datetime, timedelta
import jinja2

class SLOReporter:
    """Generate monthly SLO reports"""
    
    def generate_monthly_report(
        self,
        service_name: str,
        month: datetime,
        availability_data: dict,
        incidents: list
    ) -> str:
        """Generate HTML monthly SLO report"""
        
        template = jinja2.Template('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>SLO Report - {{ service_name }} - {{ month_str }}</title>
            <style>
                .healthy { color: green; }
                .warning { color: orange; }
                .critical { color: red; }
            </style>
        </head>
        <body>
            <h1>SLO Report: {{ service_name }}</h1>
            <h2>{{ month_str }}</h2>
            
            <h3>Executive Summary</h3>
            <ul>
                <li>Target Availability: {{ slo_target }}%</li>
                <li>Actual Availability: <span class="{{ status_class }}">{{ actual_availability }}%</span></li>
                <li>Error Budget Used: {{ budget_used }}%</li>
                <li>Status: <span class="{{ status_class }}">{{ status }}</span></li>
            </ul>
            
            <h3>Downtime Analysis</h3>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Allowed</th>
                    <th>Actual</th>
                </tr>
                <tr>
                    <td>Downtime (minutes)</td>
                    <td>{{ allowed_downtime_min }}</td>
                    <td>{{ actual_downtime_min }}</td>
                </tr>
                <tr>
                    <td>Failed Requests</td>
                    <td>{{ allowed_failures }}</td>
                    <td>{{ actual_failures }}</td>
                </tr>
            </table>
            
            <h3>Incidents ({{ incident_count }} total)</h3>
            <ul>
            {% for incident in incidents %}
                <li>
                    <strong>{{ incident.date }}</strong> - {{ incident.title }}
                    <br>Duration: {{ incident.duration_minutes }} minutes
                    <br>Impact: {{ incident.impact }}
                </li>
            {% endfor %}
            </ul>
            
            <h3>Recommendations</h3>
            <ul>
            {% for rec in recommendations %}
                <li>{{ rec }}</li>
            {% endfor %}
            </ul>
        </body>
        </html>
        ''')
        
        # Determine status and recommendations
        status, recommendations = self._analyze_performance(
            availability_data['actual_availability'],
            availability_data['target'],
            incidents
        )
        
        report = template.render(
            service_name=service_name,
            month_str=month.strftime('%B %Y'),
            slo_target=availability_data['target'],
            actual_availability=availability_data['actual_availability'],
            budget_used=availability_data['budget_used'],
            status=status,
            status_class=self._get_status_class(status),
            allowed_downtime_min=availability_data['allowed_downtime_minutes'],
            actual_downtime_min=availability_data['actual_downtime_minutes'],
            allowed_failures=availability_data['allowed_failures'],
            actual_failures=availability_data['actual_failures'],
            incidents=incidents,
            incident_count=len(incidents),
            recommendations=recommendations
        )
        
        return report
    
    def _analyze_performance(
        self,
        actual: float,
        target: float,
        incidents: list
    ) -> tuple:
        """Analyze performance and generate recommendations"""
        
        if actual >= target:
            status = "HEALTHY"
            recommendations = [
                "SLO target met successfully",
                "Consider investing error budget in feature development",
                "Continue current reliability practices"
            ]
        elif actual >= target - 0.05:
            status = "WARNING"
            recommendations = [
                "Close to SLO violation",
                "Investigate root causes of recent incidents",
                "Consider feature freeze if trend continues"
            ]
        else:
            status = "CRITICAL"
            recommendations = [
                "SLO VIOLATION - Feature freeze recommended",
                "Focus engineering effort on reliability improvements",
                "Conduct blameless postmortems for all incidents",
                "Implement additional monitoring and alerting"
            ]
        
        return status, recommendations
```

## SLO Decision Framework

```python
# slo_decision_framework.py - Release Decision Logic

class SLODecisionFramework:
    """Make release decisions based on SLO status"""
    
    def should_release(
        self,
        error_budget_remaining: float,
        release_risk: str,  # 'low', 'medium', 'high'
        recent_incidents: int
    ) -> dict:
        """
        Determine if release should proceed based on SLO status
        
        Decision Matrix:
        - Budget > 75% + Low Risk = APPROVE
        - Budget > 50% + Medium Risk = APPROVE with extra monitoring
        - Budget > 25% + High Risk = REJECT
        - Budget < 10% = FEATURE FREEZE
        """
        
        if error_budget_remaining < 10:
            return {
                'decision': 'REJECT',
                'reason': 'Error budget exhausted - Feature freeze in effect',
                'action': 'Focus on reliability improvements only'
            }
        
        if error_budget_remaining > 75:
            return {
                'decision': 'APPROVE',
                'reason': 'Healthy error budget - Safe to release',
                'action': 'Proceed with standard release process'
            }
        
        if error_budget_remaining > 50 and release_risk in ['low', 'medium']:
            return {
                'decision': 'APPROVE',
                'reason': 'Moderate error budget - Release with caution',
                'action': 'Enhanced monitoring, staged rollout recommended'
            }
        
        if error_budget_remaining > 25 and release_risk == 'low':
            return {
                'decision': 'APPROVE',
                'reason': 'Low error budget but low-risk change',
                'action': 'Blue-green deployment with automated rollback'
            }
        
        return {
            'decision': 'REJECT',
            'reason': f'Low error budget ({error_budget_remaining}%) + {release_risk} risk = Too risky',
            'action': 'Delay release until error budget recovers or reduce risk'
        }
    
    def calculate_toil_budget(
        self,
        engineer_hours_per_week: int,
        toil_hours: int
    ) -> dict:
        """
        Calculate toil budget based on Google SRE 50% rule
        
        SRE teams should spend:
        - 50% on engineering work (automation, tooling, new features)
        - 50% on operational work (toil, oncall, tickets)
        """
        
        total_hours = engineer_hours_per_week
        toil_percentage = (toil_hours / total_hours) * 100
        
        if toil_percentage > 50:
            status = "OVER_BUDGET"
            recommendation = "Excessive toil - Invest in automation"
        elif toil_percentage > 40:
            status = "WARNING"
            recommendation = "Approaching toil limit - Review processes"
        else:
            status = "HEALTHY"
            recommendation = "Toil within acceptable limits"
        
        return {
            'toil_percentage': toil_percentage,
            'toil_hours': toil_hours,
            'engineering_hours': total_hours - toil_hours,
            'status': status,
            'recommendation': recommendation
        }
```

## SLO Templates

### Template 1: API Service SLO

```yaml
# api-service-slo.yaml
slo:
  name: api-gateway-availability
  service: api-gateway
  tier: critical
  
  slis:
    - name: availability
      type: availability
      target: 99.9
      window: 30d
      query: |
        sum(rate(http_requests_total{service="api-gateway",status_code!~"5.."}[30d]))
        /
        sum(rate(http_requests_total{service="api-gateway"}[30d]))
        * 100
    
    - name: latency
      type: latency
      target_percentile: 95
      target_value: 500ms
      window: 30d
      query: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket{service="api-gateway"}[30d])) by (le)
        )
  
  error_budget:
    allowed_downtime_minutes: 43.2
    burn_rate_alerts:
      - window: 1h
        multiplier: 14.4
        severity: critical
      - window: 6h
        multiplier: 3
        severity: warning
```

### Template 2: Data Pipeline SLO

```yaml
# data-pipeline-slo.yaml
slo:
  name: data-pipeline-freshness
  service: analytics-pipeline
  tier: essential
  
  slis:
    - name: data_freshness
      type: freshness
      target: 99.0  # 99% of data processed within SLA
      window: 30d
      sla_minutes: 30
      query: |
        sum(rate(data_processed_within_sla_total[30d]))
        /
        sum(rate(data_processed_total[30d]))
        * 100
    
    - name: data_completeness
      type: completeness
      target: 99.95
      window: 30d
      query: |
        sum(rate(data_records_processed_total[30d]))
        /
        sum(rate(data_records_received_total[30d]))
        * 100
```

## Next Steps

After implementing SLOs:

1. Schedule weekly SLO review meetings (30 minutes)
2. Integrate SLO status into CI/CD pipelines
3. Create SLO-based release gates
4. Train team on error budget policies
5. Implement blameless postmortem culture
6. Set up automated monthly SLO reporting
7. Refine SLO targets based on actual performance

## References

- [Google SRE Book - Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Workbook - SLO Engineering Case Study](https://sre.google/workbook/slo-engineering-case-study/)
- [The Art of SLOs](https://cloud.google.com/blog/products/management-tools/the-art-of-slos)
- [Multiwindow, Multi-Burn-Rate Alerts](https://sre.google/workbook/alerting-on-slos/)
