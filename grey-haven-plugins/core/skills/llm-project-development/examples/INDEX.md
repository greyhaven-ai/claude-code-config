# Examples Index

Practical LLM pipeline implementations for Grey Haven projects.

## Contents

| File | Stack | Use Case |
|------|-------|----------|
| [tanstack-pipeline.md](tanstack-pipeline.md) | TanStack Start + React | Content summarization |
| [fastapi-pipeline.md](fastapi-pipeline.md) | FastAPI + SQLModel | Ticket classification |

## Quick Navigation

### TanStack Start Example

- **Use case**: Summarize long-form content for dashboards
- **Features**: React Query integration, Zod validation, file caching
- **Key files**: Base pipeline, content summarizer, API route

### FastAPI Example

- **Use case**: Classify support tickets automatically
- **Features**: Pydantic validation, background tasks, service layer
- **Key files**: Base pipeline, ticket classifier, API routes

## Common Patterns

Both examples demonstrate:

1. **Base pipeline class** with acquire → prepare → process → parse → render stages
2. **Tenant isolation** in all database queries
3. **File-based caching** to prevent re-processing
4. **Structured output** with schema validation (Zod/Pydantic)
5. **Error handling** with meaningful messages

## Related Templates

- [pipeline-template.ts](../templates/pipeline-template.ts) - TypeScript starter
- [pipeline-template.py](../templates/pipeline-template.py) - Python starter
