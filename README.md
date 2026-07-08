# Feasibility Study Company — Website

Static marketing site for Feasibility Study Company, an independent feasibility and
market-study practice serving lenders and investors (SBA, USDA, EB-5, HUD-FHA, and
conventional institutional capital).

## Structure

```
/
├── index.html                          Home
├── asset-classes/
│   └── multifamily/index.html          Multifamily & apartments coverage
├── states/
│   └── texas/index.html                Texas market coverage
├── analytical-framework/index.html     Methodology: how a study is built
├── 404.html                            Branded not-found page
├── styles.css                          Global stylesheet (design tokens + layout)
├── favicon.svg                         Brand monogram favicon
├── og.png                              1200×630 social-share card
├── sitemap.xml                         Live, indexable URLs only
├── robots.txt                          Crawl directives + sitemap reference
└── feed.xml                            RSS channel (Research Notes)
```

The site is intentionally launched with four published pages; primary-nav links to
forthcoming sections (other states, asset classes, practice areas) resolve to the
branded `404.html` until those pages ship. Add each page to `sitemap.xml` as it goes live.

## Deployment

Hosted on **Cloudflare Pages**, deployed from this repository. Every push to the
default branch triggers an automatic build and deploy. No build step is required —
the repository root is served as static assets.

- Framework preset: **None**
- Build command: *(none)*
- Build output directory: **/** (repository root)

## Local preview

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000
```

## Brand

- Ink `#111114` · Signal red `#C8102E` · Rule `#E3E2DF`
- Typeface: Inter
