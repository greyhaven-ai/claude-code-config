# SEO/GEO Audit Checklist

Use this checklist when auditing a website's search optimization. Generate a report at the end.

## Technical SEO

- [ ] Page title present and contains primary keyword (50-60 chars)
- [ ] Meta description present and compelling (150-160 chars)
- [ ] H1 tag present, unique, contains primary keyword
- [ ] Heading hierarchy correct (H1 > H2 > H3, no skipping)
- [ ] Images have descriptive alt text
- [ ] Internal links to related content
- [ ] External links have `rel="noopener noreferrer"`
- [ ] Canonical URL set
- [ ] Mobile-friendly layout
- [ ] Page loads in < 3 seconds
- [ ] No broken links (4xx/5xx)
- [ ] HTTPS enabled

## Structured Data

- [ ] JSON-LD schema markup present
- [ ] Schema type appropriate (WebPage, Article, FAQPage, Product, etc.)
- [ ] Schema validates at schema.org validator
- [ ] Rich results eligible (Google Rich Results Test)
- [ ] FAQPage schema on pages with FAQ content
- [ ] Organization schema on about/home page
- [ ] Breadcrumb schema for navigation

## Social / Open Graph

- [ ] `og:title` set
- [ ] `og:description` set
- [ ] `og:image` set (1200x630 recommended)
- [ ] `og:url` set to canonical
- [ ] `og:type` set (website, article, product)
- [ ] Twitter Card meta tags present
- [ ] Social preview renders correctly

## AI Bot Access (GEO)

- [ ] robots.txt allows Googlebot
- [ ] robots.txt allows Bingbot
- [ ] robots.txt allows GPTBot
- [ ] robots.txt allows ChatGPT-User
- [ ] robots.txt allows PerplexityBot
- [ ] robots.txt allows ClaudeBot / anthropic-ai
- [ ] Sitemap.xml exists and is valid
- [ ] Sitemap submitted to Google Search Console
- [ ] Sitemap submitted to Bing Webmaster Tools

## GEO Content Quality

- [ ] Answer-first format (direct answer in first paragraph)
- [ ] Statistics included with sources
- [ ] Expert citations or quotations present
- [ ] Authoritative tone (no hedging language)
- [ ] Technical terms defined on first use
- [ ] Short paragraphs (2-3 sentences max)
- [ ] Bullet points and numbered lists for scannability
- [ ] Tables for comparison data
- [ ] Content updated within last 30 days
- [ ] No keyword stuffing

## Indexing Status

- [ ] Indexed in Google (`site:domain.com`)
- [ ] Indexed in Bing (`site:domain.com`)
- [ ] Indexed in Brave Search (`site:domain.com`)
- [ ] No noindex tags on important pages
- [ ] No robots.txt blocks on important pages

---

## Report Template

```markdown
## SEO/GEO Optimization Report

**URL:** [target URL]
**Date:** [audit date]
**Auditor:** Claude

### Score Summary

| Category | Score | Status |
|----------|-------|--------|
| Technical SEO | X/12 | [status] |
| Structured Data | X/7 | [status] |
| Social / Open Graph | X/7 | [status] |
| AI Bot Access | X/9 | [status] |
| GEO Content Quality | X/10 | [status] |
| Indexing | X/5 | [status] |
| **Overall** | **X/50** | **[status]** |

### Critical Issues (Fix Immediately)
1. [Issue + fix]

### High Priority (Fix This Week)
1. [Issue + fix]

### Recommendations (Improve Over Time)
1. [Recommendation]

### GEO Optimizations Applied
- [ ] FAQPage schema added
- [ ] Statistics included with citations
- [ ] Expert quotations added
- [ ] Answer-first structure implemented
- [ ] AI bots allowed in robots.txt
- [ ] Content freshness updated
```
