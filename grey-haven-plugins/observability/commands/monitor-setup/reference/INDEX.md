# Monitoring Reference

Configuration references and patterns for production monitoring infrastructure.

## Available References

### [prometheus-operators.md](prometheus-operators.md)
PromQL operators and functions reference.
- Aggregation operators (sum, avg, max, min, count)
- Rate and increase functions (rate(), irate(), increase())
- Histogram functions (histogram_quantile())
- Label manipulation (label_replace(), label_join())
- Mathematical operators (+, -, *, /, %, ^)
- Comparison operators (==, !=, >, <, >=, <=)
- Logical operators (and, or, unless)
- Time series selectors ([5m], offset 5m)
- Vector matching (on, ignoring, group_left, group_right)

### [alertmanager-routing.md](alertmanager-routing.md)
AlertManager routing patterns and best practices.
- Route hierarchy design
- Matchers and regex patterns
- Receiver types (Slack, PagerDuty, webhook, email)
- Grouping strategies (by alertname, cluster, service)
- Time intervals (group_wait, group_interval, repeat_interval)
- Inhibition rules for related alerts
- Silences for maintenance windows
- Alert templates and customization
- Integration with incident management tools

### [grafana-variables.md](grafana-variables.md)
Grafana dashboard variables and templating.
- Query variables from Prometheus
- Custom variables (manual entry)
- Interval variables for time ranges
- Data source variables
- Chained variables (dependencies)
- Multi-value variables
- Variable syntax in queries ($variable, ${variable:pipe})
- Dashboard links with variables
- URL parameters for variables

### [metric-naming-conventions.md](metric-naming-conventions.md)
Prometheus metric naming best practices.
- Metric name structure (namespace_subsystem_name_unit)
- Unit suffixes (_seconds, _bytes, _ratio, _total)
- Label naming conventions (snake_case)
- Cardinality management (avoid high-cardinality labels)
- Reserved label names (__name__, job, instance)
- Histogram vs. summary metrics
- Counter vs. gauge metrics
- Recording rule naming (level:metric:operations)

## Quick Reference

**Need PromQL help?** → [prometheus-operators.md](prometheus-operators.md)
**Need AlertManager patterns?** → [alertmanager-routing.md](alertmanager-routing.md)
**Need Grafana variables?** → [grafana-variables.md](grafana-variables.md)
**Need metric naming?** → [metric-naming-conventions.md](metric-naming-conventions.md)
