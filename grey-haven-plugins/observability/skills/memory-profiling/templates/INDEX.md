# Memory Profiler Templates

Ready-to-use templates for memory profiling reports and heap snapshot analysis.

## Templates Overview

### Memory Investigation Report

**File**: [memory-report-template.md](memory-report-template.md)

Template for documenting memory leak investigations:
- **Incident Summary**: Timeline, symptoms, impact
- **Investigation Steps**: Tools used, findings
- **Root Cause**: Code analysis, leak pattern identified
- **Fix Implementation**: Code changes, validation
- **Results**: Before/after metrics

**Use when**: Documenting memory leak investigations for team/postmortems

---

### Heap Snapshot Analysis Checklist

**File**: [heap-snapshot-analysis.md](heap-snapshot-analysis.md)

Step-by-step checklist for analyzing V8 heap snapshots:
- **Snapshot Collection**: When/how to capture snapshots
- **Comparison Analysis**: Finding leaks by comparing snapshots
- **Retainer Analysis**: Understanding why objects not GC'd
- **Common Patterns**: EventEmitter, closures, timers

**Use when**: Analyzing heap snapshots in Chrome DevTools

---

## Quick Usage

### Memory Report

1. Copy template: `cp templates/memory-report-template.md docs/investigations/memory-leak-YYYY-MM-DD.md`
2. Fill in sections as you investigate
3. Share with team for review

### Heap Analysis

1. Open template: `templates/heap-snapshot-analysis.md`
2. Follow checklist step-by-step
3. Document findings in memory report

---

## Related Documentation

- **Examples**: [Examples Index](../examples/INDEX.md) - Full investigation examples
- **Reference**: [Reference Index](../reference/INDEX.md) - Pattern catalog
- **Main Agent**: [memory-profiler.md](../memory-profiler.md) - Memory profiler agent

---

Return to [main agent](../memory-profiler.md)
