# Commands Documentation

Slash commands that orchestrate complex workflows by chaining multiple agents and tools.

## 📚 Core Documentation

- **[Commands vs Agents](./commands-vs-agents.md)** - Understanding the distinction between commands and agents
- **[Command Creation Guide](./creation-guide.md)** - How to create custom commands *(coming soon)*
- **[Command Chaining Patterns](./chaining-patterns.md)** - Advanced chaining techniques *(coming soon)*

## 📚 Command Categories

### Quality & Testing
- **[Quality Pipeline](../../.claude/commands/quality-pipeline.md)** - Complete quality assurance workflow
- **[TDD Implement](../../.claude/commands/tdd-implement.md)** - Test-driven implementation
- **[Code Review](../../.claude/commands/code-review.md)** - Comprehensive code review

### Performance & Optimization
- **[Performance Optimize Chain](../../.claude/commands/performance-optimize-chain.md)** - Memory → Performance → Tests → Docs
- **[Refactor Clarity](../../.claude/commands/refactor-clarity.md)** - Code clarity improvements

### Security
- **[Security Audit](../../.claude/commands/security/security-audit.md)** - Full security audit
- **[Security Scan](../../.claude/commands/security/security-scan.md)** - Quick security scan

### Development Workflows
- **[Feature Full Cycle](../../.claude/commands/feature-full-cycle.md)** - Complete feature implementation
- **[Debug Chain](../../.claude/commands/debug-chain.md)** - Intelligent debugging workflow

### Linear Integration
- **[Continue Work](../../.claude/commands/linear/continue-work.md)** - Resume Linear issue work
- **[Continue Debugging](../../.claude/commands/linear/continue-debugging.md)** - Continue debugging issue
- **[Continue Testing](../../.claude/commands/linear/continue-testing.md)** - Continue testing issue
- **[Debug Systematic](../../.claude/commands/linear/debug-systematic.md)** - Systematic debugging
- **[Implement Feature](../../.claude/commands/linear/implenent-feature.md)** - Feature implementation
- **[Plan Implementation](../../.claude/commands/linear/plan-implementation.md)** - Planning workflow
- **[Retroactive Git](../../.claude/commands/linear/retroactive-git.md)** - Git history management

### MCP Server Workflows
- **[Chrome Frontend Debug](../../.claude/commands/chrome-server/frontend-debug-chain.md)** - Frontend debugging with Chrome
- **[Chrome E2E Development](../../.claude/commands/chrome-server/e2e-test-development.md)** - E2E test creation
- **[Cloudflare Deploy Debug](../../.claude/commands/cloudflare/deploy-debug-chain.md)** - Cloudflare deployment
- **[Context7 Library Learning](../../.claude/commands/context7/library-learn-implement.md)** - Learn & implement with docs
- **[Playwright Visual Tests](../../.claude/commands/playwright/visual-test-chain.md)** - Visual regression testing
- **[Firecrawl API Research](../../.claude/commands/firecrawl/api-research.md)** - API documentation research

### Utilities
- **[Pre-Compact](../../.claude/commands/pre-compact.md)** - Prepare for context compaction

## 🔗 Command Chaining Patterns

Commands demonstrate advanced patterns:
- Sequential agent execution with context passing
- Conditional branching based on findings
- Dynamic agent selection based on tech stack
- Error recovery and retry logic

## 🎯 Creating Custom Commands

Commands follow this structure:
```yaml
---
allowed-tools: [list of tools]
description: Brief description
argument-hint: [expected arguments]
---

Command implementation...
```