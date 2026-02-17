# JSON-LD Schema Templates

Copy-paste ready Schema.org JSON-LD templates for common page types.

## Article (Blog Posts, News)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Article Title}",
  "description": "{Article Description}",
  "image": "{Featured Image URL}",
  "author": {
    "@type": "Person",
    "name": "{Author Name}",
    "url": "{Author Profile URL}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{Publisher Name}",
    "logo": {
      "@type": "ImageObject",
      "url": "{Logo URL}"
    }
  },
  "datePublished": "{YYYY-MM-DD}",
  "dateModified": "{YYYY-MM-DD}",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{Canonical URL}"
  }
}
```

## Organization (About Page, Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{Organization Name}",
  "url": "{Website URL}",
  "logo": "{Logo URL}",
  "description": "{Organization Description}",
  "sameAs": [
    "https://twitter.com/{handle}",
    "https://linkedin.com/company/{handle}",
    "https://github.com/{handle}"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "customer support",
    "email": "{email}",
    "url": "{contact page URL}"
  }
}
```

## Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{Product Name}",
  "description": "{Product Description}",
  "image": "{Product Image URL}",
  "brand": {
    "@type": "Brand",
    "name": "{Brand Name}"
  },
  "offers": {
    "@type": "Offer",
    "price": "{Price}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "{Product URL}"
  }
}
```

## SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{App Name}",
  "description": "{App Description}",
  "applicationCategory": "{Category}",
  "operatingSystem": "{OS}",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "author": {
    "@type": "Organization",
    "name": "{Publisher}"
  }
}
```

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{Section}",
      "item": "https://example.com/{section}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{Current Page}",
      "item": "https://example.com/{section}/{page}"
    }
  ]
}
```

## HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to {Task}",
  "description": "{Description}",
  "step": [
    {
      "@type": "HowToStep",
      "name": "{Step 1 Title}",
      "text": "{Step 1 Description}"
    },
    {
      "@type": "HowToStep",
      "name": "{Step 2 Title}",
      "text": "{Step 2 Description}"
    }
  ]
}
```

## Choosing the Right Schema

| Page Type | Schema Type | Key Fields |
|-----------|-------------|------------|
| Blog post | Article | headline, author, datePublished |
| Homepage | Organization | name, url, logo, sameAs |
| About page | Organization | name, description, contactPoint |
| Product page | Product | name, offers, brand |
| FAQ section | FAQPage | mainEntity (Question/Answer pairs) |
| Tutorial | HowTo | name, step |
| App/Tool | SoftwareApplication | name, applicationCategory, offers |
| Navigation | BreadcrumbList | itemListElement |
