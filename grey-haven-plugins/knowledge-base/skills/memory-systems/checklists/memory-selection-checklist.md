# Memory System Selection Checklist

Use this to choose the right memory architecture for your use case.

## Phase 1: Requirements Analysis (Score: /20)

- [ ] **Query types documented** - What questions will the system answer? (5 pts)
- [ ] **Data types identified** - Documents, conversations, entities, relationships? (5 pts)
- [ ] **Scale estimated** - How many items, queries per day? (5 pts)
- [ ] **Latency requirements** - What's acceptable response time? (5 pts)

## Phase 2: Use Case Matching (Score: /30)

### Document Retrieval (Vector RAG)
- [ ] Primary use is finding relevant documents (5 pts)
- [ ] Queries are semantic/natural language (5 pts)
- [ ] Relationships between documents not critical (5 pts)

### Conversation Memory (Hybrid)
- [ ] Need to remember user context across sessions (5 pts)
- [ ] Important to track mentioned entities (5 pts)
- [ ] Recency matters (newer > older) (5 pts)

### Domain Reasoning (Knowledge Graph)
- [ ] Queries involve multiple entities (5 pts)
- [ ] Relationships are central to answers (5 pts)
- [ ] Need to traverse connections (5 pts)

### Historical Analysis (Temporal)
- [ ] Need "point in time" queries (5 pts)
- [ ] Track how knowledge changes (5 pts)
- [ ] Audit trail is important (5 pts)

## Phase 3: Architecture Selection

Based on scores from Phase 2, select architecture:

| Highest Score Section | Recommended Architecture |
|-----------------------|--------------------------|
| Document Retrieval | Vector RAG |
| Conversation Memory | Vector + Entity Store |
| Domain Reasoning | Knowledge Graph |
| Historical Analysis | Temporal Knowledge Graph |
| Multiple tied | Hybrid approach |

## Phase 4: Technology Selection (Score: /20)

- [ ] **Existing infrastructure reviewed** - What do we already have? (5 pts)
- [ ] **Team expertise assessed** - What can we maintain? (5 pts)
- [ ] **Cost calculated** - Storage + queries + embeddings (5 pts)
- [ ] **Vendor evaluated** - Managed vs self-hosted decision (5 pts)

## Phase 5: Implementation Validation (Score: /20)

- [ ] **Prototype built** - Test with real data subset (5 pts)
- [ ] **Accuracy measured** - Recall@K for retrieval (5 pts)
- [ ] **Latency tested** - P50 and P99 acceptable (5 pts)
- [ ] **Edge cases covered** - Empty results, large queries (5 pts)

---

## Quick Decision Matrix

| Question | If Yes → |
|----------|----------|
| Is it mostly document search? | Vector RAG |
| Do entities have relationships? | Knowledge Graph |
| Does history matter? | Temporal Graph |
| Is it conversation-based? | Hybrid with entity store |
| Budget < $100/mo and simple needs? | Simple Vector (Chroma/pgvector) |
| Scale > 1M items? | Managed service (Pinecone/Weaviate) |

---

## Architecture Trade-offs

| Factor | Vector RAG | Knowledge Graph | Temporal Graph |
|--------|------------|-----------------|----------------|
| Setup complexity | Low | High | Very High |
| Query complexity | Low | Medium | High |
| Relationship support | None | Full | Full + Time |
| Latency (P50) | 20-50ms | 50-200ms | 100-500ms |
| Storage efficiency | High | Medium | Low |
| Maintenance burden | Low | Medium | High |

---

## Red Flags

Stop and reconsider if:

- [ ] No clear query patterns defined
- [ ] Trying to use one architecture for everything
- [ ] Choosing technology before understanding requirements
- [ ] Ignoring existing infrastructure
- [ ] Over-engineering for current scale

---

## Recommended Starting Points

### For Most Projects
Start with **Vector RAG** (80% of use cases)

### For Chat Applications
Start with **Vector + Simple Entity Tracking**

### For Complex Domains
Start with **Knowledge Graph** (be prepared for complexity)

### For Compliance/Audit
Add **Temporal layer** to whatever base you choose

---

*Simpler architectures are easier to maintain and extend*
