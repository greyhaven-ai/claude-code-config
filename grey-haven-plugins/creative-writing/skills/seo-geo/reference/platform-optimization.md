# Platform-Specific Optimization

Detailed ranking and citation factors for each AI search platform.

## ChatGPT (OpenAI)

**Search backend:** Bing + GPTBot crawling

**Key citation factors:**
- **Branded domain authority** - cited 11% more than third-party sources
- **Content freshness** - content updated within 30 days gets 3.2x more citations
- **Backlink profile** - sites with >350K referring domains average 8.4 citations
- **Content format match** - structure content similarly to ChatGPT response format

**Optimization checklist:**
- [ ] Allow GPTBot and ChatGPT-User in robots.txt
- [ ] Update content at least monthly
- [ ] Build authoritative backlink profile
- [ ] Use answer-first content structure
- [ ] Include structured data (JSON-LD)

**robots.txt:**
```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /
```

## Perplexity

**Search backend:** Proprietary crawling + multiple search APIs

**Key citation factors:**
- **FAQ Schema** - higher citation rate for FAQPage structured data
- **PDF documents** - prioritized for citation
- **Semantic relevance** - meaning over exact keyword matching
- **Content depth** - comprehensive coverage of topics

**Optimization checklist:**
- [ ] Allow PerplexityBot in robots.txt
- [ ] Implement FAQPage schema on relevant pages
- [ ] Host PDF versions of key content
- [ ] Focus on semantic richness over keyword density
- [ ] Provide comprehensive topic coverage

**robots.txt:**
```
User-agent: PerplexityBot
Allow: /
```

## Google AI Overview (SGE)

**Search backend:** Google Search infrastructure

**Key citation factors:**
- **E-E-A-T** (Experience, Expertise, Authority, Trust) - primary signal
- **Structured data** - Schema.org markup strongly prioritized
- **Topical authority** - content clusters with strong internal linking
- **Authoritative citations** - +132% visibility when citing authoritative sources

**Optimization checklist:**
- [ ] Implement comprehensive Schema.org markup
- [ ] Build topical authority with content clusters
- [ ] Include authoritative citations and references
- [ ] Demonstrate E-E-A-T through author bios, credentials
- [ ] Use internal linking to create topic clusters
- [ ] Ensure mobile-first indexing compatibility

**Content cluster structure:**
```
Pillar Page (broad topic, 3000+ words)
├── Cluster Article 1 (subtopic, 1500+ words)
├── Cluster Article 2 (subtopic, 1500+ words)
├── Cluster Article 3 (subtopic, 1500+ words)
└── All interlinked with descriptive anchor text
```

## Microsoft Copilot / Bing

**Search backend:** Bing Search index

**Key citation factors:**
- **Bing indexing** - required; if not indexed in Bing, cannot be cited
- **Microsoft ecosystem** - mentions on LinkedIn, GitHub help signals
- **Page speed** - < 2 seconds load time
- **Entity definitions** - clear, structured definitions of key concepts

**Optimization checklist:**
- [ ] Verify Bing indexing via Bing Webmaster Tools
- [ ] Optimize page speed (target < 2 seconds)
- [ ] Allow Bingbot in robots.txt
- [ ] Define key entities clearly in content
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Build Microsoft ecosystem presence (LinkedIn, GitHub)

**robots.txt:**
```
User-agent: Bingbot
Allow: /
```

## Claude (Anthropic)

**Search backend:** Brave Search

**Key citation factors:**
- **Brave Search indexing** - Claude uses Brave, not Google
- **Factual density** - data-rich content preferred
- **Structural clarity** - content that's easy to parse and extract from
- **Source attribution** - well-cited content with clear provenance

**Optimization checklist:**
- [ ] Verify indexing in Brave Search (search site:yourdomain.com)
- [ ] Allow ClaudeBot / anthropic-ai in robots.txt
- [ ] Maximize factual density (statistics, data, specific claims)
- [ ] Use clear heading hierarchy for structural clarity
- [ ] Include source citations for all claims

**robots.txt:**
```
User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /
```

## Comprehensive robots.txt Template

Allow all major AI bots:

```
# Traditional search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# AI search engines
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

# General
User-agent: *
Allow: /
Disallow: /private/
Disallow: /admin/

Sitemap: https://yourdomain.com/sitemap.xml
```
