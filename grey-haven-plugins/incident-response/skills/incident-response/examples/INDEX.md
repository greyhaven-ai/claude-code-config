# Incident Response Examples

Real-world production incident examples demonstrating systematic incident response, root cause analysis, mitigation strategies, and blameless postmortems.

## Available Examples

### SEV1: Critical Database Outage

**File**: [sev1-critical-database-outage.md](sev1-critical-database-outage.md)

Complete database failure causing total service outage:
- **Incident**: PostgreSQL primary failure, 100% error rate
- **Impact**: All services down, $50K revenue loss/hour
- **Root Cause**: Disk full on primary, replication lag spike
- **Resolution**: Promoted replica, cleared disk space, restored service
- **MTTR**: 45 minutes (detection → full recovery)
- **Prevention**: Disk monitoring alerts, automatic disk cleanup, replica promotion automation

**Key Learnings**:
- Importance of replica promotion runbooks
- Disk space monitoring thresholds
- Automated failover procedures

---

### SEV2: API Performance Degradation

**File**: [sev2-api-performance-degradation.md](sev2-api-performance-degradation.md)

Gradual performance degradation due to memory leak:
- **Incident**: API p95 latency 200ms → 5000ms over 2 hours
- **Impact**: 30% of users affected, slow page loads
- **Root Cause**: Memory leak in worker process, OOM killing workers
- **Resolution**: Identified leak with heap snapshot, deployed fix, restarted workers
- **MTTR**: 3 hours (detection → permanent fix)
- **Prevention**: Memory profiling in CI/CD, heap snapshot automation, worker restart automation

**Key Learnings**:
- Early detection through gradual alerts
- Heap snapshot analysis for memory leaks
- Temporary mitigation (worker restarts) vs permanent fix

---

### SEV3: Feature Flag Misconfiguration

**File**: [sev3-feature-flag-misconfiguration.md](sev3-feature-flag-misconfiguration.md)

Feature flag enabled for wrong audience causing confusion:
- **Incident**: Experimental feature shown to 20% of production users
- **Impact**: 200 support tickets, user confusion, no revenue impact
- **Root Cause**: Feature flag percentage set to 20% instead of 0%
- **Resolution**: Disabled flag, sent customer communication, updated flag process
- **MTTR**: 30 minutes (detection → resolution)
- **Prevention**: Feature flag code review, staging validation, gradual rollout process

**Key Learnings**:
- Feature flag validation before production
- Importance of clear documentation
- Quick rollback procedures

---

### Distributed Tracing Investigation

**File**: [distributed-tracing-investigation.md](distributed-tracing-investigation.md)

Using Jaeger distributed tracing to find microservice bottleneck:
- **Incident**: Checkout API slow (3s p95), unclear which service
- **Investigation**: Used Jaeger to trace request flow across 7 microservices
- **Root Cause**: Payment service calling external API synchronously (2.8s)
- **Resolution**: Moved external API call to async background job
- **Impact**: p95 latency 3000ms → 150ms (95% faster)

**Key Learnings**:
- Power of distributed tracing for microservices
- Synchronous external dependencies are dangerous
- Background jobs for non-critical operations

---

### Cascade Failure Prevention

**File**: [cascade-failure-prevention.md](cascade-failure-prevention.md)

Preventing cascade failure through circuit breakers and bulkheads:
- **Incident**: Auth service down, caused all dependent services to fail
- **Impact**: Complete outage instead of graceful degradation
- **Root Cause**: No circuit breakers, all services retrying auth indefinitely
- **Resolution**: Implemented circuit breakers, bulkhead isolation, fallback logic
- **Prevention**: Circuit breaker pattern, timeout configuration, graceful degradation

**Key Learnings**:
- Circuit breakers prevent cascade failures
- Bulkhead isolation limits blast radius
- Fallback logic enables graceful degradation

---

## Learning Outcomes

After studying these examples, you will understand:

1. **Incident Classification**: How to assess severity (SEV1-SEV4) based on impact
2. **Incident Command**: Role of IC, communication protocols, timeline management
3. **Root Cause Analysis**: 5 Whys, timeline reconstruction, data-driven investigation
4. **Mitigation Strategies**: Immediate actions, temporary fixes, permanent solutions
5. **Blameless Postmortems**: Focus on systems not people, actionable items, continuous improvement
6. **Communication**: Internal updates, external communications, executive briefings
7. **Prevention**: Monitoring improvements, runbook automation, architectural changes

---

## Related Documentation

- **Reference**: [Reference Index](../reference/INDEX.md) - Severity matrix, communication templates, RCA techniques
- **Templates**: [Templates Index](../templates/INDEX.md) - Incident timeline, postmortem, runbook templates
- **Main Agent**: [incident-responder.md](../incident-responder.md) - Incident responder agent

---

Return to [main agent](../incident-responder.md)
