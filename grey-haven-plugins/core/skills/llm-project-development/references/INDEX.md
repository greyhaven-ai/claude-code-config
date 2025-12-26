# References Index

Methodology foundations and code patterns for LLM project development.

## Contents

| File | Description |
|------|-------------|
| [case-studies.md](case-studies.md) | Karpathy, Vercel d0, Manus, Anthropic case studies |
| [pipeline-patterns.md](pipeline-patterns.md) | TypeScript/Python code patterns for pipelines |

## Quick Navigation

### Case Studies

- **Karpathy's HN Time Capsule**: Manual validation, file-based state, structured output
- **Vercel d0**: Architectural reduction (17 → 2 tools = 100% success)
- **Manus Agent**: KV-cache optimization, append-only context
- **Anthropic Multi-Agent**: Handoff patterns, tool specialization

### Pipeline Patterns

- **Base Pipeline Class**: TypeScript and Python templates
- **State Management**: File-based checkpointing
- **Concurrent Execution**: Rate-limited parallel processing
- **Error Handling**: Retry with backoff, graceful degradation
- **Cost Tracking**: Token counting and estimation

## Related Skills

- [grey-haven-prompt-engineering](../../../core/skills/prompt-engineering/SKILL.md)
- [grey-haven-data-validation](../../../data-quality/skills/data-validation/SKILL.md)
