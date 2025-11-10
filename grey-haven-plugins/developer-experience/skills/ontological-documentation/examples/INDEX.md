# Ontological Documentation Examples

Real-world examples of creating ontological documentation for Grey Haven systems.

## Available Examples

1. **[TanStack Start Ontology](tanstack-start-example.md)** - Frontend codebase analysis
   - Extracting concepts from Drizzle schemas
   - Mapping React component hierarchies
   - Documenting multi-tenant patterns
   - Visualizing route structure

2. **[FastAPI Ontology](fastapi-example.md)** - Backend codebase analysis
   - SQLModel entity relationships
   - Repository pattern documentation
   - Service layer mapping
   - API endpoint hierarchy

3. **[Multi-Tenant System Architecture](multi-tenant-ontology.md)** - Complete system documentation
   - Tenant isolation patterns
   - RLS policies visualization
   - Database schema relationships
   - Authentication flow

4. **[Domain Model Extraction](domain-model-extraction.md)** - Business concept mapping
   - Identifying domain entities
   - Relationship mapping
   - Business rule documentation
   - Semantic relationships

## Recommended Path

**For new projects:**
1. Start with [domain-model-extraction.md](domain-model-extraction.md)
2. Document frontend with [tanstack-start-example.md](tanstack-start-example.md)
3. Document backend with [fastapi-example.md](fastapi-example.md)
4. Complete system view with [multi-tenant-ontology.md](multi-tenant-ontology.md)

**For existing systems:**
1. Run extraction scripts on codebase
2. Follow [domain-model-extraction.md](domain-model-extraction.md) to identify concepts
3. Use templates to document findings

## Quick Reference

### Frontend Ontology
- See [tanstack-start-example.md](tanstack-start-example.md)
- Use `scripts/extract_concepts.py` for automation

### Backend Ontology
- See [fastapi-example.md](fastapi-example.md)
- Focus on repository and service patterns

### Visualization
- See [multi-tenant-ontology.md](multi-tenant-ontology.md)
- Use `scripts/generate_ontology_diagram.py`

## Related Materials

- **[Concept Extraction Guide](../reference/concept_extraction_guide.md)** - How to extract concepts
- **[Ontology Patterns](../reference/ontology_patterns.md)** - Common patterns
- **[Templates](../templates/)** - Ready-to-use ontology templates
- **[Scripts](../scripts/)** - Automation scripts

---

**Total Examples**: 4 comprehensive guides
**Coverage**: TanStack Start, FastAPI, Multi-tenant, Domain modeling
**Last Updated**: 2025-11-09
