# Documentation Quality Checklist

**Use when creating or reviewing documentation.**

## Accuracy

- [ ] All code examples are tested and verified
- [ ] API contracts match actual implementation
- [ ] Version numbers are correct and up-to-date
- [ ] External links are valid (not 404)
- [ ] Screenshots reflect current UI
- [ ] Configuration examples are accurate
- [ ] Environment variables are correctly documented
- [ ] Dependency versions match package.json/requirements.txt

## Completeness

- [ ] All public APIs are documented
- [ ] All required parameters are explained
- [ ] All optional parameters have defaults documented
- [ ] Response formats are specified with examples
- [ ] Error cases are covered with status codes
- [ ] Authentication requirements are clear
- [ ] Rate limiting is documented
- [ ] Deprecation notices are included where needed
- [ ] Migration guides for breaking changes
- [ ] Changelog is up-to-date

## API Documentation

- [ ] OpenAPI 3.1 specification is valid
- [ ] All endpoints have descriptions
- [ ] Request/response schemas are complete
- [ ] Multi-language code examples (TypeScript, Python, cURL)
- [ ] Authentication flows documented
- [ ] Error responses documented
- [ ] Interactive documentation (Swagger UI/Redoc) works
- [ ] Try-it-now functionality tested

## Architecture Documentation

- [ ] Executive summary for stakeholders
- [ ] Mermaid system architecture diagram
- [ ] Sequence diagrams for key flows
- [ ] Data flow diagrams
- [ ] Integration points documented
- [ ] Security model explained
- [ ] ADRs (Architectural Decision Records) included
- [ ] Database schema documented

## Code Examples

- [ ] TypeScript examples follow Grey Haven patterns
- [ ] Python examples follow Grey Haven patterns
- [ ] cURL examples are complete and correct
- [ ] Examples use realistic data
- [ ] Examples show error handling
- [ ] Examples demonstrate authentication
- [ ] Examples are syntax-highlighted
- [ ] Examples are copy-paste ready

## Consistency

- [ ] Uniform terminology throughout
- [ ] Consistent formatting (headings, lists, code blocks)
- [ ] Standard code example format
- [ ] Unified voice and tone
- [ ] Consistent naming conventions
- [ ] Cross-references use standard format
- [ ] Diagrams follow consistent style

## Accessibility

- [ ] Content is searchable
- [ ] Clear navigation structure
- [ ] Mobile-responsive design
- [ ] WCAG 2.1 AA compliant
- [ ] Alt text for images and diagrams
- [ ] Keyboard navigation works
- [ ] Color contrast meets standards
- [ ] Screen reader compatible

## Usability

- [ ] Progressive disclosure (simple → complex)
- [ ] Practical examples and use cases
- [ ] Troubleshooting guides included
- [ ] Quick reference sections provided
- [ ] Table of contents for long docs
- [ ] Search functionality works
- [ ] Clear call-to-action buttons
- [ ] Getting started guide present

## Documentation Coverage

- [ ] Function coverage >80%
- [ ] API coverage >80%
- [ ] Type coverage >80%
- [ ] No critical gaps in documentation
- [ ] Coverage report generated
- [ ] CI/CD validation passes

## Grey Haven Standards

- [ ] Cloudflare Workers patterns documented
- [ ] TanStack Start patterns included
- [ ] FastAPI patterns covered
- [ ] Multi-tenant patterns explained
- [ ] tenant_id filtering documented
- [ ] RLS policies explained
- [ ] Doppler secrets management documented
- [ ] bun package manager (NOT npm!)

## CI/CD Integration

- [ ] Documentation generates automatically on merge
- [ ] Pre-commit hooks validate coverage
- [ ] Broken link checker runs
- [ ] Code examples are tested
- [ ] Coverage threshold enforced (<80% fails build)
- [ ] Deployment to Cloudflare Pages configured

## Deployment

- [ ] Deployed to correct environment (staging/production)
- [ ] Custom domain configured
- [ ] SSL certificate valid
- [ ] Redirects configured (if needed)
- [ ] Analytics tracking enabled
- [ ] Search indexing configured
- [ ] CDN caching configured

## Maintenance

- [ ] Quarterly documentation audit scheduled
- [ ] User feedback collection in place
- [ ] Version support matrix documented
- [ ] Deprecation timeline clear
- [ ] Migration guides for breaking changes
- [ ] Contact information for support
- [ ] Contribution guidelines present

## Pre-Release

- [ ] All checklist items above completed
- [ ] Documentation reviewed by team
- [ ] Examples tested on staging
- [ ] Coverage meets >80% threshold
- [ ] No broken links
- [ ] Mobile testing completed
- [ ] Accessibility audit passed
- [ ] User testing feedback incorporated
