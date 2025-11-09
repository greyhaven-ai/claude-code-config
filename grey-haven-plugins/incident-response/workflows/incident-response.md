---
name: incident-response
description: Comprehensive production incident response workflow using SRE best practices. Orchestrates detection, triage, mitigation, communication, and postmortem phases with multi-agent coordination. Use for production outages, service degradation, or critical failures.
---
# Incident Response Workflow - SRE Production Incident Management
Comprehensive incident response workflow implementing Google SRE best practices with multi-agent orchestration for rapid detection, mitigation, and learning.
## Overview
This workflow provides end-to-end incident management from detection through postmortem, orchestrating specialized agents for different phases of incident response. It follows the incident command system with clear roles, communication protocols, and continuous learning loops.
## Workflow Phases
### Phase 1: Detection & Assessment (Minutes 0-5)
**Objective:** Quickly classify incident severity and assess customer impact.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="incident-responder"
 → Classify severity (SEV1/2/3/4)
 → Assess customer impact and affected services
 → Create incident ticket with initial details
2. Use Task tool with subagent_type="observability-engineer"
 → Check monitoring dashboards for anomalies
 → Correlate alerts across systems
 → Identify SLO violations and error budget impact
```
**Output:** Incident ticket, severity classification, initial impact assessment
**Decision Point:** If SEV1 (critical), immediately escalate to executives and proceed to Phase 2 with urgency.
---
### Phase 2: Incident Command & Communication (Minutes 5-10)
**Objective:** Establish incident command structure and begin stakeholder communication.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="incident-responder"
 → Assign incident commander role
 → Create war room (Slack channel, Zoom bridge)
 → Assign roles (technical lead, comms lead, scribe)
 → Post initial internal status update
2. Use Task tool with subagent_type="incident-responder"
 → Post external status page update
 → Notify customer support team
 → Brief executives if SEV1/SEV2
 → Set update frequency (SEV1: 15min, SEV2: 30min)
```
**Output:** War room created, roles assigned, initial communications sent
---
### Phase 3: Investigation & Root Cause Analysis (Minutes 10-30)
**Objective:** Identify root cause through systematic debugging and log analysis.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="devops-troubleshooter"
 → Analyze application and infrastructure logs
 → Check recent deployments for correlation
 → Identify error patterns and stack traces
2. Use Task tool with subagent_type="observability-engineer"
 → Query Prometheus metrics for anomalies
 → Analyze distributed traces in Jaeger
 → Check resource utilization (CPU, memory, disk)
3. Use Task tool with subagent_type="error-detective"
 → Search for similar past incidents
 → Correlate errors across microservices
 → Identify cascading failure patterns
4. Use Task tool with appropriate specialist (e.g., "backend-architect", "database-admin")
 → Deep dive into suspected root cause
 → Validate hypothesis with data
 → Recommend mitigation approach
```
**Output:** Root cause hypothesis, supporting evidence, mitigation options
**Decision Point:** If root cause unclear after 30 minutes, escalate to senior engineer and continue investigation in parallel with mitigation attempts.
---
### Phase 4: Mitigation & Resolution (Minutes 30-60)
**Objective:** Implement fix to restore service and verify customer impact resolved.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="incident-responder"
 → Evaluate mitigation options (rollback, scale, feature flag)
 → Make go/no-go decision on immediate fix
 → Coordinate deployment of mitigation
2. Use Task tool with domain specialist based on root cause:
 - "backend-architect" for application code issues
 - "database-admin" for database problems
 - "network-engineer" for network/connectivity issues
 - "security-analyzer" for security incidents
 → Implement mitigation (rollback, config change, hotfix)
 → Verify fix in staging if time permits
 → Deploy to production with monitoring
3. Use Task tool with subagent_type="observability-engineer"
 → Monitor metrics for recovery (error rate, latency)
 → Validate SLO metrics returning to normal
 → Check customer-facing indicators
```
**Output:** Mitigation deployed, service recovering, metrics improving
---
### Phase 5: Verification & Communication (Minutes 60-90)
**Objective:** Confirm full recovery and communicate resolution.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="observability-engineer"
 → Run smoke tests on critical paths
 → Verify all alerts have cleared
 → Confirm SLO metrics within target
 → Check error budget consumption
2. Use Task tool with subagent_type="incident-responder"
 → Post all-clear internal announcement
 → Update external status page (resolved)
 → Notify customer support of resolution
 → Brief executives on resolution and impact
 → Thank all responders publicly
```
**Output:** Service fully recovered, stakeholders informed, incident closed
---
### Phase 6: Postmortem & Learning (Within 48 Hours)
**Objective:** Conduct blameless postmortem and create action items to prevent recurrence.
**Agent Orchestration:**
```
1. Use Task tool with subagent_type="incident-responder"
 → Schedule postmortem meeting within 48 hours
 → Assign facilitator (not incident commander)
 → Prepare timeline document from incident notes
 → Gather all logs, metrics, traces for analysis
2. Use Task tool with subagent_type="incident-responder"
 → Facilitate blameless postmortem discussion
 → Apply 5 Whys to identify root cause
 → Create fishbone diagram for contributing factors
 → Document learnings and systemic issues
3. Use Task tool with subagent_type="incident-responder"
 → Create action items for prevention
 → Assign owners and due dates
 → Prioritize by impact and effort
 → Track in Linear
4. Use Task tool with relevant specialists for preventative measures:
 - "test-generator" → Create regression tests
 - "code-quality-analyzer" → Review code for similar patterns
 - "security-analyzer" → Audit for security implications
 - "observability-engineer" → Improve monitoring/alerting
5. Use Task tool with subagent_type="incident-responder"
 → Distribute postmortem report to organization
 → Update runbooks with new procedures
 → Share learnings in engineering all-hands
 → Archive incident for future reference
```
**Output:** Postmortem report, action items created, runbooks updated, team learning
---
## Severity-Based Variations
### SEV1 (Critical): Complete Outage, Revenue Stopped
**Timeline:** Resolve in < 60 minutes
**Communication:** Every 15 minutes, immediate executive notification
**Team:** Full incident response team, 24/7 availability
**Escalation:** Automatic executive escalation, PR team standby
**Example Agents:**
- incident-responder (Opus) - Critical decision-making
- devops-troubleshooter (Sonnet) - Rapid debugging
- observability-engineer (Opus) - Deep monitoring analysis
- security-analyzer (Opus) if breach suspected
---
### SEV2 (Major): Significant Degradation
**Timeline:** Resolve in < 4 hours
**Communication:** Every 30 minutes, executive notification if prolonged
**Team:** On-call engineer + specialists as needed
**Escalation:** Senior engineer if >2 hours
**Example Agents:**
- incident-responder (Opus) - Coordination
- devops-troubleshooter (Sonnet) - Investigation
- observability-engineer (Sonnet) - Metrics analysis
---
### SEV3 (Minor): Isolated Issues, Workarounds Available
**Timeline:** Resolve in < 24 hours
**Communication:** Hourly updates if customer-facing
**Team:** On-call engineer
**Escalation:** Team lead if >8 hours
**Example Agents:**
- incident-responder (Sonnet) - Lightweight coordination
- error-detective (Sonnet) - Pattern matching
---
### SEV4 (Cosmetic): UI Issues, No Functional Impact
**Timeline:** Fix in next sprint
**Communication:** No status page updates
**Team:** Regular development cycle
**Escalation:** None
**Example Agents:**
- bug-issue-creator (Haiku) - Create backlog ticket
---
## Example Usage
### Example 1: API Outage (SEV1)
```bash
/incident-response High error rate on checkout API, customers cannot complete purchases
```
**Workflow Execution:**
1. incident-responder: Classifies as SEV1, creates war room, pages team
2. observability-engineer: Analyzes metrics, identifies database connection pool exhaustion
3. database-admin: Increases connection pool size, restarts database proxy
4. observability-engineer: Monitors recovery, confirms error rate drops
5. incident-responder: Communicates resolution, schedules postmortem
---
### Example 2: Performance Degradation (SEV2)
```bash
/incident-response Slow API response times, p95 latency increased from 200ms to 2s
```
**Workflow Execution:**
1. incident-responder: Classifies as SEV2, creates incident ticket
2. performance-engineer: Profiles application, identifies N+1 query problem
3. backend-architect: Implements eager loading, deploys fix
4. observability-engineer: Validates latency returns to baseline
5. test-generator: Creates performance regression tests
---
### Example 3: Security Incident (SEV1)
```bash
/incident-response Suspicious authentication attempts, possible credential stuffing attack
```
**Workflow Execution:**
1. incident-responder: Classifies as SEV1 security incident
2. security-analyzer: Confirms attack pattern, identifies compromised accounts
3. incident-responder: Coordinates credential rotation, implements rate limiting
4. security-analyzer: Analyzes logs for data exfiltration, finds none
5. incident-responder: Notifies affected users, files security report
---
## Communication Templates
### Initial Internal Announcement
```
 INCIDENT DECLARED - SEV{severity}
**Incident:** {brief description}
**Impact:** {customer-facing effects}
**War Room:** #{slack-channel}
**IC:** {incident commander name}
Status updates every {15/30/60} minutes.
```
### Status Page Update
```
We are currently investigating {issue description}.
Customers may experience {specific impact}.
Next update in {timeframe}.
```
### All-Clear Message
```
SUCCESS: INCIDENT RESOLVED - SEV{severity}
**Incident:** {brief description}
**Duration:** {start time} - {end time} ({total minutes})
**Root Cause:** {one-sentence summary}
**Impact:** {customers/services affected}
Postmortem scheduled for {date/time}.
Thank you to all responders: {names}
```
## Metrics & Reporting
### Key Metrics
- **MTTD (Mean Time to Detect):** Alert firing → Incident creation
- **MTTR (Mean Time to Recovery):** Incident creation → Resolution
- **Customer Impact Duration:** First customer report → All-clear
- **Communication Latency:** Incident start → First status update
### Weekly Incident Report
```
Incidents This Week: {count}
- SEV1: {count} (avg MTTR: {minutes}min)
- SEV2: {count} (avg MTTR: {hours}h)
- SEV3: {count}
Top Root Causes:
1. {cause} - {count} incidents
2. {cause} - {count} incidents
Repeat Incidents: {count} (% of total)
Action Items Created: {count}
Action Items Completed: {count} ({percent}%)
```
## Integration with Other Plugins
### grey-haven-observability
- Provides monitoring data for investigation
- SLO metrics for impact assessment
- Dashboards for root cause analysis
### grey-haven-security
- Security incident classification
- Breach response procedures
- Forensic analysis coordination
### grey-haven-testing
- Post-incident regression tests
- Chaos engineering validation
- Integration test improvements
### grey-haven-deployment
- Rollback procedures
- Canary deployment coordination
- Feature flag management
## Best Practices
1. **Communicate Early and Often:** Over-communication is better than under-communication
2. **Assign Clear Roles:** Single incident commander, no confusion on decision authority
3. **Document Everything:** Timeline, decisions, actions for postmortem accuracy
4. **Blameless Culture:** Focus on systems, not people; create psychological safety
5. **Automate Runbooks:** Turn manual procedures into scripts where possible
6. **Learn from Every Incident:** Every incident reveals system weaknesses to fix
7. **Respect On-Call:** Fair compensation, reasonable alert frequency, burnout prevention
8. **Practice Regularly:** Incident simulations, chaos days, runbook reviews
## References
- [Google SRE Book - Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
- [Atlassian Incident Management Handbook](https://www.atlassian.com/incident-management)
- [Blameless Postmortems](https://sre.google/sre-book/postmortem-culture/)
---
**Next Steps After Incident:**
1. Complete postmortem within 48 hours
2. Implement action items with deadlines
3. Update runbooks with new procedures
4. Share learnings in team retrospective
5. Review MTTR trends for improvement opportunities
