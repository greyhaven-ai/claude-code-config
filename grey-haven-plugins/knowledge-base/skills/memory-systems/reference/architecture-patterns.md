# Memory Architecture Patterns

Decision framework for choosing the right memory architecture.

## Decision Tree

```
What is your primary use case?
│
├─▶ Document retrieval (search, Q&A)
│   └─▶ Vector RAG
│
├─▶ Conversation memory (chat history)
│   └─▶ Vector + Entity hybrid
│
├─▶ Domain reasoning (complex queries)
│   └─▶ Knowledge Graph
│
├─▶ Change tracking (audits, history)
│   └─▶ Temporal Knowledge Graph
│
└─▶ All of the above
    └─▶ Hybrid with tiered storage
```

## Vector RAG Architecture

### When to Use

- Document search and retrieval
- FAQ systems
- Code search
- Simple Q&A over documents

### Architecture

```
Documents ──▶ Chunking ──▶ Embedding ──▶ Vector Store
                                              │
Query ──▶ Embedding ────────────────────▶ Similarity Search
                                              │
                                              ▼
                                         Top K Results
                                              │
                                              ▼
                              LLM ──▶ Answer with context
```

### Key Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Chunk size | 256-2048 tokens | 512 for general, 256 for code |
| Overlap | 0-50% | 10-20% to preserve context |
| Embedding model | Various | text-embedding-3-small for cost, ada-002 for quality |
| Vector dimensions | 256-3072 | 1536 balances quality/speed |
| Distance metric | Cosine, Euclidean, Dot | Cosine for normalized embeddings |

### Limitations

- No relationship awareness
- "Lost in similarity" - similar != relevant
- Recency bias without explicit handling

---

## Knowledge Graph Architecture

### When to Use

- Complex domain relationships
- Reasoning over entities
- Multi-hop queries
- Structured knowledge representation

### Architecture

```
Data ──▶ Entity Extraction ──▶ Relationship Detection ──▶ Graph Store
                                                              │
Query ──▶ Entity Recognition ──▶ Graph Traversal ────────────┘
                                         │
                                         ▼
                                   Subgraph Retrieval
                                         │
                                         ▼
                        LLM ──▶ Answer with graph context
```

### Schema Design

```
# Entities
(User) -[WORKS_AT]-> (Company)
(User) -[MENTIONED]-> (Topic)
(Document) -[ABOUT]-> (Topic)
(Document) -[CREATED_BY]-> (User)

# Properties
User: {name, email, role, last_active}
Company: {name, domain, employee_count}
Topic: {name, category, importance}
Document: {title, created_at, updated_at}
```

### Limitations

- Requires structured data or extraction
- More complex queries
- Schema evolution challenges

---

## Temporal Knowledge Graph

### When to Use

- Historical queries ("What did we know in January?")
- Change tracking and audits
- Causal reasoning
- Version control for knowledge

### Architecture

```
Knowledge ──▶ Version with timestamp ──▶ Temporal Store
                     │
Query (with time) ──▶ Point-in-time retrieval
                     │
                     ▼
              Historical context
```

### Time Modeling

```
# Option 1: Valid time (when fact is true)
(User)-[WORKS_AT {valid_from: 2023-01, valid_to: 2024-06}]->(Company)

# Option 2: Transaction time (when recorded)
(User)-[WORKS_AT {recorded_at: 2023-01-15}]->(Company)

# Option 3: Bitemporal (both)
(User)-[WORKS_AT {
  valid_from: 2023-01,
  valid_to: 2024-06,
  recorded_at: 2023-01-15,
  superseded_at: 2024-06-20
}]->(Company)
```

---

## Hybrid Architecture

### When to Use

- Complex systems with multiple query types
- Need both semantic search and reasoning
- Performance-critical applications
- Evolving requirements

### Architecture

```
                    ┌─────────────────────────────────────┐
                    │          Query Router               │
                    └─────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    Vector Store       Knowledge Graph      Entity Store
    (semantic)         (relationships)      (properties)
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                    ┌─────────────────────────────────────┐
                    │         Result Merger               │
                    └─────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────────────────────┐
                    │         Re-ranker                   │
                    └─────────────────────────────────────┘
                              │
                              ▼
                        Final Results
```

### Implementation Strategy

1. **Start simple** - Vector RAG for most use cases
2. **Add entity extraction** - When you need to track mentioned entities
3. **Add relationships** - When queries require multi-hop reasoning
4. **Add temporal** - When history matters

---

## Storage Technology Comparison

| Technology | Type | Best For | Grey Haven Use |
|------------|------|----------|----------------|
| Pinecone | Vector | Large-scale semantic search | Document retrieval |
| Weaviate | Vector + Graph | Hybrid queries | Knowledge base |
| Neo4j | Graph | Complex relationships | Domain modeling |
| Chroma | Vector | Local development | Testing/prototypes |
| PostgreSQL + pgvector | Vector | Existing Postgres stack | When you have Postgres |
| TerminusDB | Temporal Graph | Historical queries | Audit trails |

---

## Cost Considerations

### Vector Store Costs

| Provider | Storage ($/GB/mo) | Queries ($/1M) |
|----------|-------------------|----------------|
| Pinecone | $0.096 | $0.24 |
| Weaviate Cloud | $0.15 | Free (included) |
| Chroma (self-hosted) | Infrastructure only | - |

### Embedding Costs

| Model | $/1M tokens |
|-------|-------------|
| text-embedding-3-small | $0.02 |
| text-embedding-3-large | $0.13 |
| Voyage-3 | $0.06 |

### Calculation Example

```
Documents: 10,000
Avg length: 2,000 tokens
Chunks per doc: 4
Queries/day: 1,000

Storage:
  10,000 × 4 chunks × 1536 dimensions × 4 bytes = 245 MB
  Cost: ~$0.02/month

Queries:
  1,000/day × 30 = 30,000/month
  Cost: ~$0.007/month

Embeddings (one-time):
  10,000 docs × 2,000 tokens = 20M tokens
  Cost: ~$0.40 (text-embedding-3-small)

Total: ~$0.45 initial + $0.03/month
```

---

*Choose architecture based on query patterns, not technology hype*
