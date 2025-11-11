# Ontological Documentation Checklist

Systematic checklist for creating comprehensive ontological documentation.

## Pre-Documentation

- [ ] **Identify codebase scope** (frontend, backend, or full-stack)
- [ ] **Understand domain** (business concepts, terminology)
- [ ] **Set up documentation tools** (Mermaid, diagramming tools)
- [ ] **Review existing documentation** (READMEs, architecture docs)
- [ ] **Identify stakeholders** (who will use this documentation)

## Concept Extraction

### Frontend (TanStack Start)
- [ ] **Database schema extracted** (Drizzle tables, relationships)
- [ ] **Component hierarchy mapped** (React component tree)
- [ ] **Routes documented** (TanStack Router structure)
- [ ] **State management identified** (Context, queries, mutations)
- [ ] **Server functions cataloged** (API surface)

### Backend (FastAPI)
- [ ] **SQLModel entities documented** (all models)
- [ ] **Relationships mapped** (foreign keys, associations)
- [ ] **Repository pattern documented** (all repositories)
- [ ] **Service layer mapped** (business logic)
- [ ] **API endpoints cataloged** (all routes)
- [ ] **Pydantic schemas listed** (request/response models)

### Multi-Tenant Patterns
- [ ] **tenant_id fields identified** on all tables
- [ ] **RLS policies documented** (row level security)
- [ ] **Tenant isolation verified** in queries
- [ ] **Repository filters documented** (automatic tenant filtering)
- [ ] **Admin vs user access documented**

## Entity Documentation

### For Each Entity
- [ ] **Name and purpose** clearly stated
- [ ] **Attributes documented** (all fields with types)
- [ ] **Relationships documented** (to other entities)
- [ ] **Constraints documented** (unique, required, validation)
- [ ] **Business rules noted** (validation, lifecycle)

### Database Entities
- [ ] **Table name** documented
- [ ] **Primary key** identified
- [ ] **Foreign keys** documented
- [ ] **Indexes** listed
- [ ] **Timestamps** (created_at, updated_at)
- [ ] **Tenant isolation** (tenant_id field)

## Relationship Mapping

### Types of Relationships
- [ ] **One-to-One** relationships documented
- [ ] **One-to-Many** relationships documented
- [ ] **Many-to-Many** relationships documented
- [ ] **Join tables** identified (for many-to-many)
- [ ] **Cascade behavior** documented (delete, update)

### Relationship Documentation
- [ ] **Source entity** identified
- [ ] **Target entity** identified
- [ ] **Relationship name** clear and descriptive
- [ ] **Cardinality** specified
- [ ] **Business meaning** explained

## Architecture Documentation

### System Components
- [ ] **Frontend components** listed and categorized
- [ ] **Backend services** documented
- [ ] **Database** structure documented
- [ ] **External services** identified (Stripe, Resend, etc.)
- [ ] **Authentication system** documented (Better-auth)

### Data Flow
- [ ] **User actions** → **Frontend** flow documented
- [ ] **Frontend** → **Backend** API calls documented
- [ ] **Backend** → **Database** queries documented
- [ ] **Backend** → **External services** documented
- [ ] **Response flow** back to user documented

## Visualization

### Diagrams Created
- [ ] **Entity-Relationship Diagram** (ERD) for database
- [ ] **Component Hierarchy** for React components
- [ ] **Architecture Overview** showing all systems
- [ ] **Data Flow Diagrams** for critical paths
- [ ] **Multi-Tenant Isolation** diagram

### Diagram Quality
- [ ] **Clear labels** on all elements
- [ ] **Legend provided** (symbols explained)
- [ ] **Color coding** used effectively
- [ ] **Readable font size** and layout
- [ ] **Diagrams source-controlled** (Mermaid or PlantUML)

## Domain Model

### Business Concepts
- [ ] **Core domain entities** identified
- [ ] **Business processes** documented
- [ ] **Business rules** captured
- [ ] **Domain terminology** defined
- [ ] **Invariants** documented

### Semantic Relationships
- [ ] **"Is-a" relationships** (inheritance)
- [ ] **"Has-a" relationships** (composition)
- [ ] **"Uses" relationships** (dependencies)
- [ ] **Aggregation** relationships
- [ ] **Association** relationships

## Grey Haven Specific

### Multi-Tenant Architecture
- [ ] **Tenant model** documented
- [ ] **Organization model** documented
- [ ] **User-Tenant relationship** explained
- [ ] **Team structure** documented (if applicable)
- [ ] **RLS roles** explained (admin, authenticated, anon)

### Authentication & Authorization
- [ ] **Better-auth integration** documented
- [ ] **Session management** explained
- [ ] **User roles** documented
- [ ] **Permission model** explained
- [ ] **OAuth providers** listed

### Database Conventions
- [ ] **Naming conventions** documented (snake_case)
- [ ] **UUID usage** explained (primary keys)
- [ ] **Timestamp fields** standardized
- [ ] **Soft deletes** documented (if used)
- [ ] **Audit fields** documented (if used)

## Documentation Quality

### Completeness
- [ ] **All entities** documented
- [ ] **All relationships** documented
- [ ] **All business rules** captured
- [ ] **All external integrations** noted
- [ ] **All deployment architecture** documented

### Clarity
- [ ] **Technical jargon** explained
- [ ] **Domain terminology** consistent
- [ ] **Examples provided** where helpful
- [ ] **Diagrams clear** and readable
- [ ] **Navigation easy** (links, TOC)

### Maintainability
- [ ] **Documentation source-controlled** (with code)
- [ ] **Update process** defined
- [ ] **Ownership** assigned (who maintains)
- [ ] **Review schedule** established
- [ ] **Feedback mechanism** in place

## Automation

### Scripts Used
- [ ] **extract_concepts.py** run successfully
- [ ] **generate_ontology_diagram.py** produced diagrams
- [ ] **Output reviewed** and verified
- [ ] **Customizations documented**
- [ ] **Scripts committed** to repository

### Continuous Documentation
- [ ] **Documentation updates** in PR checklist
- [ ] **Schema changes** trigger doc updates
- [ ] **API changes** trigger doc updates
- [ ] **CI checks** for documentation completeness

## Stakeholder Review

### Technical Review
- [ ] **Developers reviewed** documentation
- [ ] **Technical accuracy** verified
- [ ] **Missing information** identified
- [ ] **Feedback incorporated**

### Business Review
- [ ] **Domain experts reviewed** business concepts
- [ ] **Business terminology** verified
- [ ] **Business rules** confirmed
- [ ] **Use cases validated**

## Deployment

### Documentation Delivery
- [ ] **Documentation committed** to repository
- [ ] **README updated** with links
- [ ] **Wiki/Confluence** updated (if used)
- [ ] **Team notified** of new documentation
- [ ] **Onboarding materials** updated

### Accessibility
- [ ] **Documentation discoverable** (easy to find)
- [ ] **Navigation clear** (links, search)
- [ ] **Formats appropriate** (markdown, diagrams)
- [ ] **Mobile-friendly** (if applicable)

## Scoring

- **90+ items checked**: Excellent - Comprehensive documentation ✅
- **75-89 items**: Good - Most areas covered ⚠️
- **60-74 items**: Fair - Significant gaps exist 🔴
- **<60 items**: Poor - Inadequate documentation ❌

## Priority Items

Address these first:
1. **Entity documentation** - Core to understanding
2. **Relationship mapping** - Critical for navigation
3. **Multi-tenant patterns** - Security-critical
4. **Data flow diagrams** - Helps debugging
5. **Automation setup** - Saves time

## Related Resources

- [Concept Extraction Guide](../reference/concept_extraction_guide.md)
- [Ontology Patterns](../reference/ontology_patterns.md)
- [Examples](../examples/INDEX.md)
- [Templates](../templates/)
- [Scripts](../scripts/)

---

**Total Items**: 100+ documentation checks
**Critical Items**: Entity docs, Relationships, Multi-tenant, Data flow
**Last Updated**: 2025-11-09
