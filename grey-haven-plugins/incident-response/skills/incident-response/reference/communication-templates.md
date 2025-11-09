# Communication Templates

Copy-paste templates for incident communications across all channels and severity levels.

## Internal Communications

### SEV1 Incident Start

```
🚨 SEV1 INCIDENT DECLARED 🚨
Incident ID: INC-YYYY-MM-DD-XXX
Impact: [Brief description - e.g., "100% outage, database down"]
Affected Services: [List services]
Customer Impact: [All users / X% of users / Specific feature unavailable]

Roles:
- Incident Commander: @[name]
- Technical Lead: @[name]
- Communications Lead: @[name]

War Room:
- Slack: #incident-XXX
- Zoom: [link]

Status: Investigating
Next Update: [Time] (15 minutes or on status change)
Runbook: [Link if available]
```

### SEV2 Incident Start

```
⚠️ SEV2 INCIDENT
Incident ID: INC-YYYY-MM-DD-XXX
Impact: [Brief description - e.g., "API degraded, 30% users affected"]
Symptoms: [What users are experiencing]

IC: @[name]
Status: Investigating [suspected cause]
Next Update: 30 minutes
```

### Incident Update

```
📊 UPDATE #[N] (T+[X] minutes)
Root Cause: [What we found OR "Still investigating"]
Mitigation: [What we're doing]
Impact: [Current status - improving/stable/worsening]
ETA: [Expected resolution time OR "Unknown"]
Next Update: [Time]
```

### Incident Resolved

```
🎉 INCIDENT RESOLVED (T+[X] minutes/hours)
Final Status: All services operational
Root Cause: [Brief summary]
Fix Applied: [What was done]
Monitoring: Ongoing for [duration]

Postmortem: Scheduled for [date/time]
Timeline: [Link to detailed timeline]
```

## External Communications

### Status Page - Investigating

```
🔴 INVESTIGATING - [Brief Title]

We are investigating reports of [issue description].
Our team is actively working to identify the cause.

Affected: [Service names]
Started: [HH:MM UTC]
Next Update: [HH:MM UTC]
```

### Status Page - Identified

```
🟡 IDENTIFIED - [Issue Title]

We have identified the issue as [brief cause].
Our team is implementing a fix.

Affected: [Service names]
Started: [HH:MM UTC]
Identified: [HH:MM UTC]
Est. Resolution: [HH:MM UTC]
```

### Status Page - Monitoring

```
🟢 MONITORING - [Issue Title] Resolved

The issue has been resolved and services are operating normally.
We are monitoring to ensure stability.

Started: [HH:MM UTC]
Resolved: [HH:MM UTC]
Duration: [X] minutes
```

### Customer Email - SEV1 Postmortem

```
Subject: Service Disruption - [Date] Postmortem

Dear [Product Name] Customers,

On [Date] at [Time UTC], we experienced a service disruption that affected [all users / X% of users] for approximately [duration].

What Happened:
[2-3 sentence summary of the incident]

Impact:
- Duration: [X] minutes
- Affected Users: [percentage or description]
- Services Impacted: [list]

Root Cause:
[1-2 sentence explanation of root cause]

Resolution:
[1-2 sentences on how we fixed it]

Prevention:
We have implemented the following measures to prevent recurrence:
1. [Measure 1]
2. [Measure 2]
3. [Measure 3]

We sincerely apologize for the inconvenience and appreciate your patience.

[Team Name]
[Company Name]
```

## Executive Briefings

### Initial Notification (SEV1 only)

```
Subject: SEV1 Incident - [Brief Title]

Summary:
- Incident ID: INC-YYYY-MM-DD-XXX
- Started: [HH:MM UTC]
- Impact: [All users affected / X% affected / revenue stopped]
- Status: [Investigating / Mitigation in progress]

Current Situation:
[2-3 sentences explaining what's happening]

Response:
- IC: [Name]
- Team: [X] engineers actively working
- ETA: [Time if known, "Unknown" if not]

Business Impact:
- Revenue: [Estimated $ per hour OR "Minimal"]
- Customers: [Number affected]
- SLA: [Yes/No breach, details]

Next Update: [Time]
```

### Resolution Summary (Executive)

```
Subject: SEV1 Resolved - [Brief Title]

Incident INC-YYYY-MM-DD-XXX has been resolved after [duration].

Timeline:
- Started: [HH:MM UTC]
- Identified: [HH:MM UTC]
- Resolved: [HH:MM UTC]
- Total Duration: [X] minutes

Impact:
- Customers Affected: [Number / percentage]
- Revenue Loss: [$X estimated]
- SLA Breach: [Yes/No]

Root Cause:
[1-2 sentences]

Resolution:
[1-2 sentences on fix]

Prevention:
[2-3 key action items with owners and dates]

Postmortem: Scheduled for [date/time]

[IC Name]
```

## Related Documentation

- **Severity Matrix**: [incident-severity-matrix.md](incident-severity-matrix.md) - When to use each template
- **Examples**: [Examples Index](../examples/INDEX.md) - Real communications from incidents
- **Templates**: [Templates Index](../templates/INDEX.md) - Full incident timeline and postmortem templates

---

Return to [reference index](INDEX.md)
