# Meta Tags Templates

Copy-paste ready templates for SEO meta tags, Open Graph, and Twitter Cards.

## Essential Meta Tags

```html
<title>{Primary Keyword} - {Brand} | {Secondary Keyword}</title>
<meta name="description" content="{Compelling description with keyword, 150-160 chars}">
<meta name="keywords" content="{keyword1}, {keyword2}, {keyword3}">
<link rel="canonical" href="{canonical URL}">
<meta name="robots" content="index, follow">
```

## Open Graph (Facebook, LinkedIn, etc.)

```html
<meta property="og:title" content="{Title - max 60 chars}">
<meta property="og:description" content="{Description - max 160 chars}">
<meta property="og:image" content="{Image URL - 1200x630px}">
<meta property="og:url" content="{Canonical URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{Brand Name}">
<meta property="og:locale" content="en_US">
```

**og:type values:**
- `website` - Homepage, general pages
- `article` - Blog posts, articles
- `product` - Product pages
- `profile` - People/author pages

## Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Title - max 70 chars}">
<meta name="twitter:description" content="{Description - max 200 chars}">
<meta name="twitter:image" content="{Image URL - 1200x630px}">
<meta name="twitter:site" content="@{brand_handle}">
<meta name="twitter:creator" content="@{author_handle}">
```

## Complete Head Template

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- SEO -->
  <title>{Primary Keyword} - {Brand} | {Secondary Keyword}</title>
  <meta name="description" content="{150-160 char description with keyword}">
  <link rel="canonical" href="{canonical URL}">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:title" content="{Title}">
  <meta property="og:description" content="{Description}">
  <meta property="og:image" content="{Image URL 1200x630}">
  <meta property="og:url" content="{Canonical URL}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{Brand}">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{Title}">
  <meta name="twitter:description" content="{Description}">
  <meta name="twitter:image" content="{Image URL}">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{Page Title}",
    "description": "{Page Description}",
    "url": "{Canonical URL}"
  }
  </script>
</head>
```
