# Async Standup Reference

Technical references for data extraction, intelligent features, automation, and configuration.

## Available References

### [data-sources.md](data-sources.md)
Detailed algorithms for extracting standup data from Git, Linear, and code analysis.
- **Git Commit Analysis** - Parsing conventional commits, extracting linked issues, calculating impact
- **Linear Integration** - GraphQL queries for issues, filtering by status, extracting blockers
- **Blocker Detection** - Identifying blockers from Linear labels, commit patterns, CI failures
- **Code Example Transformations** - Real examples of commit → accomplishment transformation

### [intelligent-features.md](intelligent-features.md)
Implementation details for accomplishment extraction, classification, and planning.
- **Accomplishment Extraction Algorithm** - TypeScript code for parsing commits and generating descriptions
- **Blocker Severity Classification** - Logic for categorizing blockers (critical, high, medium, low)
- **Smart Work Planning** - Capacity calculation and task allocation from backlog
- **Productivity Metrics Calculation** - Complete metrics tracking with velocity and focus time

### [automation-integration.md](automation-integration.md)
Complete integration setup for Slack, Linear, and GitHub Actions.
- **Slack Integration** - Webhook configuration, bot setup, scheduled posting
- **Linear Integration** - API authentication, project comment creation, issue linking
- **GitHub Actions Integration** - Complete workflow YAML with secrets and scheduling
- **Custom Integrations** - Discord, Microsoft Teams, email integration patterns

### [configuration.md](configuration.md)
Complete configuration schema with examples.
- **User Configuration** - Name, email, timezone, working hours
- **Integration Settings** - Linear, Slack, GitHub connection details
- **Metrics Preferences** - Coverage tracking, build time, velocity calculation
- **Format Preferences** - Default format, auto-posting, commit summarization

### [troubleshooting.md](troubleshooting.md)
Common issues and detailed troubleshooting steps.
- **No Commits Detected** - Git author email verification, timeframe debugging
- **Linear Issues Not Showing** - API authentication, filter debugging, team access
- **Metrics Inaccurate** - Multi-repo aggregation, incomplete data handling
- **Posting Failures** - Webhook verification, rate limiting, permission issues

## Quick Reference

**Need data extraction details?** → [data-sources.md](data-sources.md)
**Need implementation algorithms?** → [intelligent-features.md](intelligent-features.md)
**Need integration setup?** → [automation-integration.md](automation-integration.md)
**Need configuration schema?** → [configuration.md](configuration.md)
**Need troubleshooting help?** → [troubleshooting.md](troubleshooting.md)
