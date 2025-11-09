# Incident Response Templates

Ready-to-use templates for incident timelines, blameless postmortems, and runbooks. Copy and fill in for your incidents.

## Available Templates

### Incident Timeline Template

**File**: [incident-timeline-template.md](incident-timeline-template.md)

Real-time incident tracking template:
- Incident overview (ID, severity, impact)
- Chronological timeline (minute-by-minute)
- Role assignments (IC, Tech Lead, Comms)
- Status updates
- Resolution summary

**Use when**: Tracking ongoing incident in real-time

---

### Postmortem Template

**File**: [postmortem-template.md](postmortem-template.md)

Blameless postmortem template:
- Executive summary
- Timeline reconstruction
- Root cause analysis (5 Whys)
- Contributing factors
- Action items with owners
- Lessons learned

**Use when**: Documenting incident after resolution (within 24-48 hours)

---

### Runbook Template

**File**: [runbook-template.md](runbook-template.md)

Standard runbook structure:
- Problem description
- Diagnostic steps with commands
- Mitigation procedures
- Escalation paths
- Success criteria

**Use when**: Creating new runbook or updating existing one

---

## Template Usage

**How to use**:
1. Copy template to your documentation system
2. Fill in all `[FILL IN]` sections
3. Remove optional sections if not applicable
4. Share with team for review

**When to create**:
- **Incident Timeline**: As soon as SEV1/SEV2 declared (real-time)
- **Postmortem**: Within 24-48 hours of incident resolution
- **Runbook**: After any new incident type or process improvement

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - See completed examples
- **Reference**: [Reference Index](../reference/INDEX.md) - RCA techniques, communication templates
- **Main Agent**: [incident-responder.md](../incident-responder.md) - Incident responder agent

---

Return to [main agent](../incident-responder.md)
