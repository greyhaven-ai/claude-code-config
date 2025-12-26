# LLM Project Development Checklist

Use this checklist before launching LLM-powered features to production.

## Phase 1: Task-Model Fit

- [ ] **Manual validation complete**: Tested ONE real example with target model
- [ ] **LLM suitability confirmed**: Task requires synthesis, not precise computation
- [ ] **Error tolerance acceptable**: Graceful degradation is OK for this use case
- [ ] **Latency acceptable**: Response time meets requirements (or background processing)
- [ ] **Cost estimated**: Calculated cost per operation at expected scale

## Phase 2: Pipeline Architecture

- [ ] **Stages defined**: acquire → prepare → process → parse → render
- [ ] **Only process is non-deterministic**: All other stages are deterministic
- [ ] **Tenant isolation**: All database queries include `tenant_id`
- [ ] **Cache directory set**: `.cache/pipelines/{tenant_id}/{pipeline_name}/`
- [ ] **Error handling**: Each stage has appropriate error handling

## Phase 3: File-Based State

- [ ] **Cache implemented**: LLM responses saved to files
- [ ] **Idempotent**: Re-running doesn't re-call LLM for completed items
- [ ] **Debuggable**: Intermediate files can be inspected
- [ ] **Resumable**: Pipeline can restart from any stage

## Phase 4: Structured Output

- [ ] **Schema defined**: Zod (TypeScript) or Pydantic (Python) schema
- [ ] **Parsing disclosed**: Prompt mentions "I will parse this programmatically"
- [ ] **Format specified**: Exact JSON structure in prompt
- [ ] **Validation tested**: Schema handles edge cases

## Phase 5: Integration

- [ ] **API route created**: Endpoint for triggering pipeline
- [ ] **Background processing**: Long operations run in background
- [ ] **Progress tracking**: User can see processing status
- [ ] **Error responses**: Meaningful error messages returned

## Phase 6: Testing

- [ ] **Unit tests**: prepare() and parse() functions tested
- [ ] **Integration tests**: Full pipeline with mock LLM
- [ ] **Edge cases**: Empty input, malformed response, timeouts
- [ ] **Tenant isolation**: Cross-tenant access prevented

## Phase 7: Observability

- [ ] **Logging**: Each stage logs start/complete/error
- [ ] **Cost tracking**: Token usage recorded
- [ ] **Cache metrics**: Hit/miss ratio tracked
- [ ] **Alerting**: Errors trigger alerts

## Phase 8: Production Readiness

- [ ] **Rate limiting**: LLM calls rate-limited appropriately
- [ ] **Retry logic**: Transient failures retried with backoff
- [ ] **Fallback**: Graceful degradation if LLM unavailable
- [ ] **Documentation**: Pipeline purpose and usage documented

## Cost Estimation Table

| Model | Input ($/M) | Output ($/M) | Typical Cost/Item |
|-------|-------------|--------------|-------------------|
| Haiku 3.5 | $0.80 | $4.00 | ~$0.005 |
| Sonnet 4 | $3.00 | $15.00 | ~$0.02 |
| Opus 4.5 | $15.00 | $75.00 | ~$0.10 |

**Estimate formula**: `(input_tokens / 1M * input_rate) + (output_tokens / 1M * output_rate)`

## Quick Reference

### Good Prompts

```
I will parse this programmatically. Respond with valid JSON:
{
  "field": "description of expected value",
  "list": ["array", "items"]
}
```

### Bad Prompts

```
Give me the information about this.
Format it nicely.
```

### Pipeline Stage Checklist

| Stage | Deterministic? | Retry Safe? | Required? |
|-------|----------------|-------------|-----------|
| Acquire | Yes | Yes | Yes |
| Prepare | Yes | Yes | Yes |
| Process | **No** | Cache first | Yes |
| Parse | Yes | Yes | Yes |
| Render | Yes | Idempotent | Yes |
