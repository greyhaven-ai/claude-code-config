# Code Quality Analyzer Templates

Copy-paste report templates for security reviews, clarity refactorings, and synthesis analysis.

## Files in This Directory

### [security-report-template.md](security-report-template.md)
Comprehensive security review report template with OWASP Top 10 coverage, vulnerability classification, security scorecard, and remediation tracking.

**When to use**: After security review, for stakeholder reporting
**Format**: Markdown with tables and checklists

### [clarity-report-template.md](clarity-report-template.md)
Code clarity refactoring report template with complexity metrics, before/after comparisons, and maintainability improvements.

**When to use**: After clarity refactoring, for technical documentation
**Format**: Markdown with code examples and metrics

### [synthesis-report-template.md](synthesis-report-template.md)
Cross-file analysis report template with architectural violations, dependency issues, and consistency metrics.

**When to use**: After synthesis analysis, for architectural reviews
**Format**: Markdown with dependency graphs and issue lists

### [complete-audit-report-template.md](complete-audit-report-template.md)
Comprehensive quality audit report combining security, clarity, and synthesis analysis with executive summary and ROI metrics.

**When to use**: For complete codebase audits, executive reporting
**Format**: Markdown with executive summary and detailed findings

## Usage Instructions

1. **Copy template** to your project documentation
2. **Fill in placeholders**:
   - `[Project Name]` → Your project name
   - `[Date]` → Current date
   - `[Version]` → Version number
   - `[Analyst Name]` → Your name
3. **Complete sections** with your findings
4. **Add evidence** (code snippets, metrics, screenshots)
5. **Export** to PDF for stakeholder distribution

## Template Conventions

**Placeholders**:
- `[Project Name]` - Replace with project name
- `[Date]` - Replace with current date
- `[Analyst Name]` - Replace with reviewer name
- `[Version]` - Replace with version/commit
- `...` - Add more items as needed

**Status Indicators**:
- 🔴 Critical - Fix immediately
- 🟠 High - Fix before deployment
- 🟡 Medium - Fix soon
- 🟢 Low - Fix when convenient
- ✅ Completed
- ⏳ In Progress
- ❌ Blocked

**Severity Levels**:
- P0 (Critical): Production-blocking issues
- P1 (High): Must fix before deployment
- P2 (Medium): Should fix in next sprint
- P3 (Low): Nice to have

## Customization Tips

### For Different Stakeholders

**Executive Summary** (management):
- Focus on business impact and ROI
- Use visual indicators (✅❌)
- Include cost of inaction
- Highlight risks

**Technical Details** (developers):
- Include code examples
- Provide refactoring steps
- Link to relevant documentation
- Show metrics

**Compliance** (auditors):
- Include standards compliance
- Document all checks performed
- Provide evidence trail
- Reference frameworks (OWASP, CWE)

---

Return to [agent documentation](../code-quality-analyzer.md)
