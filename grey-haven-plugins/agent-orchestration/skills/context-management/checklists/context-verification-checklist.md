# Context Verification Checklist

Comprehensive checklist for validating context save/restore operations.

**Workflow**: _______________
**Date**: _______________
**Verifier**: _______________

---

## Pre-Save Validation

### Required Fields Present
- [ ] `version` - Schema version number (e.g., "1.0")
- [ ] `workflow_id` - Unique identifier
- [ ] `timestamp` - ISO 8601 format
- [ ] `current_agent` - Agent saving context
- [ ] `phase` - Current workflow phase

**Score**: ___/5 required fields

### Essential Content
- [ ] `files_modified` - All changed files listed
- [ ] `decisions` - Key decisions documented
- [ ] `pending_actions` - Next steps clear
- [ ] `context_summary` - Human-readable summary (≤500 chars)

**Score**: ___/4 essential fields

### Data Quality
- [ ] No sensitive data (API keys, passwords)
- [ ] File paths are relative (not absolute)
- [ ] Timestamp is current (within last hour)
- [ ] Workflow ID follows naming convention
- [ ] All JSON is valid and parseable

**Score**: ___/5 quality checks

---

## Context Size Optimization

### Size Metrics
- **Target**: < 100KB for 80% of workflows
- **Actual Size**: _____ KB

- [ ] Size is reasonable for workflow complexity
- [ ] No redundant data included
- [ ] Large data compressed or externalized
- [ ] Conversation history pruned if > 50 messages

### Compression Opportunities
- [ ] Remove completed `pending_actions`
- [ ] Prune old `conversation_history` entries
- [ ] Externalize large file contents
- [ ] Compress checkpoint snapshots

**Optimization Score**: ___/8

---

## Serialization Validation

### JSON Validation
- [ ] Valid JSON syntax (no trailing commas)
- [ ] All strings properly escaped
- [ ] No circular references
- [ ] Dates in ISO 8601 format
- [ ] Schema validation passes

### Schema Compliance
- [ ] Matches context-schema-template.json
- [ ] All required fields present
- [ ] Field types correct (string, array, object)
- [ ] Enum values valid
- [ ] No extra unknown fields (or documented as custom)

**Serialization Score**: ___/10

---

## Handoff Readiness

### Next Agent Preparation
- [ ] `next_agent` specified (or null if complete)
- [ ] `pending_actions` are clear and actionable
- [ ] Required files are accessible
- [ ] Dependencies are documented
- [ ] Constraints are explicit

### Context Clarity
- [ ] `context_summary` accurately describes state
- [ ] `decisions` explain rationale
- [ ] No ambiguous pending actions
- [ ] Next steps prioritized
- [ ] Exit criteria defined

**Handoff Score**: ___/10

---

## Restore Validation

### Pre-Restore Checks
- [ ] Context file exists and is readable
- [ ] JSON is valid and parseable
- [ ] Version is compatible with current schema
- [ ] Workflow ID matches expected pattern
- [ ] Timestamp is reasonable (not too old)

### Context Loading
- [ ] All required fields successfully loaded
- [ ] No parsing errors or exceptions
- [ ] Type conversion successful
- [ ] No data loss during deserialization
- [ ] Context object fully initialized

### State Reconstruction
- [ ] `files_modified` paths resolve correctly
- [ ] Referenced files still exist
- [ ] Dependencies are satisfied
- [ ] Agent can resume from this state
- [ ] No missing critical information

**Restore Score**: ___/15

---

## Workflow Continuity

### State Consistency
- [ ] Previous agent's output available
- [ ] Current phase matches workflow progression
- [ ] No gaps in decision chain
- [ ] File modifications trackable
- [ ] Error log is complete

### Resume Capability
- [ ] Agent can determine next action from context
- [ ] All tools/resources available
- [ ] No manual intervention needed
- [ ] Progress is measurable
- [ ] Completion criteria clear

**Continuity Score**: ___/10

---

## Error Handling

### Error Resilience
- [ ] Handles missing optional fields gracefully
- [ ] Validates required fields before proceeding
- [ ] Provides clear error messages
- [ ] Suggests fixes for common issues
- [ ] Has rollback mechanism

### Error Logging
- [ ] `error_log` array present (if errors occurred)
- [ ] Errors include timestamp and agent
- [ ] Resolution status tracked
- [ ] Stack traces captured (if applicable)
- [ ] Impact assessment documented

**Error Handling Score**: ___/10

---

## Security & Privacy

### Sensitive Data
- [ ] No API keys in context
- [ ] No passwords or tokens
- [ ] No personal identifiable information (PII)
- [ ] No internal URLs or IPs (if sensitive)
- [ ] Secrets referenced by ID, not value

### Access Control
- [ ] Context stored in secure location
- [ ] File permissions appropriate
- [ ] Encrypted if contains sensitive references
- [ ] Access logged for audit trail
- [ ] Retention policy defined

**Security Score**: ___/10

---

## Performance Metrics

### Save Performance
- **Target**: < 200ms for save operation
- **Actual**: _____ ms

- [ ] Save time within target
- [ ] No blocking operations
- [ ] Async save if large context
- [ ] Compression applied if needed

### Restore Performance
- **Target**: < 500ms for restore operation
- **Actual**: _____ ms

- [ ] Restore time within target
- [ ] Lazy loading for large history
- [ ] Cached if frequently accessed
- [ ] Progress indicator for slow loads

**Performance Score**: ___/8

---

## Version Compatibility

### Schema Version
- [ ] Current version documented
- [ ] Migration path from older versions
- [ ] Backward compatibility maintained
- [ ] Breaking changes documented
- [ ] Version upgrade tested

### Agent Compatibility
- [ ] Context works with current agent versions
- [ ] Deprecated fields handled
- [ ] New fields have defaults
- [ ] Agent can skip unknown fields
- [ ] Compatibility matrix documented

**Compatibility Score**: ___/10

---

## Total Score Calculation

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Pre-Save Validation | ___/14 | 10% | ___ |
| Size Optimization | ___/8 | 5% | ___ |
| Serialization | ___/10 | 15% | ___ |
| Handoff Readiness | ___/10 | 15% | ___ |
| Restore Validation | ___/15 | 20% | ___ |
| Continuity | ___/10 | 15% | ___ |
| Error Handling | ___/10 | 10% | ___ |
| Security | ___/10 | 5% | ___ |
| Performance | ___/8 | 3% | ___ |
| Compatibility | ___/10 | 2% | ___ |

**Total Score**: ___/100

---

## Quality Gates

### Must Pass (Blocking)
- [ ] Total score ≥ 85
- [ ] No critical security issues
- [ ] All required fields present
- [ ] Restore test successful
- [ ] Next agent can load context

### Should Pass (Important)
- [ ] Size < 100KB
- [ ] Performance within targets
- [ ] Schema validation passes
- [ ] No errors in log

### Nice to Have
- [ ] Total score ≥ 95
- [ ] Full conversation history
- [ ] Comprehensive checkpoints
- [ ] Automated testing in place

**Gates Passed**: ___/13

---

## Checklist Results

**Context Status**: [ ] ✅ Valid / [ ] ⚠️ Needs Fixes / [ ] ❌ Invalid

**Critical Issues**: ___
**Important Issues**: ___
**Minor Issues**: ___

**Recommendation**:
[ ] Ready for handoff
[ ] Fix issues before handoff
[ ] Recreate context from scratch

---

## Common Issues & Fixes

### Issue: Context Too Large
**Symptom**: Size > 100KB
**Fix**:
- [ ] Remove completed actions
- [ ] Prune conversation history
- [ ] Externalize file contents
- [ ] Compress checkpoints

### Issue: Missing Required Fields
**Symptom**: Restore fails
**Fix**:
- [ ] Add all required fields from template
- [ ] Validate against schema
- [ ] Use context builder helper

### Issue: Sensitive Data Detected
**Symptom**: Security scan finds secrets
**Fix**:
- [ ] Remove API keys
- [ ] Redact passwords
- [ ] Reference secrets by ID
- [ ] Apply encryption if needed

### Issue: Stale Context
**Symptom**: Timestamp > 7 days old
**Fix**:
- [ ] Verify files still exist
- [ ] Validate dependencies current
- [ ] Update timestamp if still valid
- [ ] Archive if no longer needed

### Issue: Version Incompatibility
**Symptom**: Old version can't load
**Fix**:
- [ ] Run migration script
- [ ] Update to current schema
- [ ] Test with both versions
- [ ] Document breaking changes

---

## Action Items

### Immediate Fixes (if issues found)
1. [ ] Issue: _______________
   - Priority: Critical/High/Medium/Low
   - Fix: _______________
   - Owner: _______________

2. [ ] Issue: _______________
   - Priority: Critical/High/Medium/Low
   - Fix: _______________
   - Owner: _______________

### Process Improvements
- [ ] Update context template
- [ ] Add validation scripts
- [ ] Improve documentation
- [ ] Create migration tools

---

## Sign-off

**Verified By**: ___________
**Date**: ___________
**Status**: [ ] Approved / [ ] Conditionally Approved / [ ] Rejected

**Notes**:
_____________________________________________
_____________________________________________

---

## Quick Reference

**Minimum Valid Context:**
```json
{
  "version": "1.0",
  "workflow_id": "workflow-name",
  "timestamp": "2025-01-15T10:00:00Z",
  "current_agent": "agent-name",
  "phase": "phase-name"
}
```

**Typical Size Ranges:**
- Small: 5-20 KB
- Medium: 20-100 KB
- Large: 100-500 KB
- Very Large: 500KB+ (needs optimization)

**Critical Fields:**
- ✅ version, workflow_id, timestamp
- ✅ current_agent, phase
- ⚠️ next_agent, pending_actions
- ℹ️ context_summary

---

**Checklist Version**: 1.0
**Last Updated**: 2025-01-15
