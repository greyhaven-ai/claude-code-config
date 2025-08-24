# Agents Documentation

Specialized AI assistants that extend Claude Code's capabilities for specific tasks.

## 📚 Agent Categories

### Code Quality & Analysis
- **[Code Quality Analyzer](../../.claude/agents/code-quality-analyzer.md)** - Multi-mode quality specialist
- **[Memory Profiler](../../.claude/agents/memory-profiler.md)** - Memory usage analyzer
- **[Performance Optimizer](../../.claude/agents/performance-optimizer.md)** - Performance enhancement specialist
- **[Security Analyzer](../../.claude/agents/security-analyzer.md)** - Security vulnerability detection

### Testing & Development
- **[TDD Python](../../.claude/agents/tdd-python.md)** - Test-driven Python development
- **[TDD TypeScript](../../.claude/agents/tdd-typescript.md)** - Test-driven TypeScript development
- **[Test Generator](../../.claude/agents/test-generator.md)** - Automated test creation
- **[React TanStack Tester](../../.claude/agents/react-tanstack-tester.md)** - React/TanStack testing

### Documentation & Research
- **[Tech Docs Maintainer](../../.claude/agents/tech-docs-maintainer.md)** - Documentation updates
- **[Tech Docs Orchestrator](../../.claude/agents/tech-docs-orchestrator.md)** - Documentation coordination
- **[Web Docs Researcher](../../.claude/agents/web-docs-researcher.md)** - Web documentation research

### Specialized Tools
- **[Bug Issue Creator](../../.claude/agents/bug-issue-creator.md)** - GitHub issue creation
- **[Prompt Engineer](../../.claude/agents/prompt-engineer.md)** - Prompt optimization
- **[Multi-Agent Synthesis Orchestrator](../../.claude/agents/multi-agent-synthesis-orchestrator.md)** - Multi-agent coordination

## 🔗 Agent Chaining

Agents can be chained together for complex workflows:

```markdown
memory-profiler → performance-optimizer → test-generator → tech-docs-maintainer
```

Each agent passes context to the next, enabling sophisticated multi-step operations.

## 🎯 Dynamic Agent Selection

Agents can be selected dynamically based on:
- File type detection
- Error patterns
- Project structure
- Git branch patterns

## 📖 Creating Custom Agents

See agent template in `.claude/agents/` for structure and patterns.