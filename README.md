# Feasibility Study Company: Website

Static marketing site for Feasibility Study Company, an independent feasibility and
market-study practice serving lenders and investors (SBA, USDA, EB-5, HUD-FHA, and
conventional institutional capital).

## Structure

```
/
├── index.html                          Home (self-contained; includes contact form)
├── asset-classes/
│   └── multifamily/index.html          Multifamily & apartments coverage
├── states/
│   └── texas/index.html                Texas market coverage
├── analytical-framework/index.html     Methodology: how a study is built
├── tools/
│   └── nda/index.html                  Client-side NDA generator (jsPDF, noindex)
├── netlify/
│   └── functions/contact.js            Serverless contact-form handler (Resend)
├── netlify.toml                        Netlify config (publish, functions, /api/contact rewrite)
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

Hosted on **Netlify**, deployed from this repository. Every push to the default
branch triggers an automatic deploy. No build step: the repository root is served
as static assets, and `netlify/functions/` is deployed as serverless functions.

- Build command: *(none)*
- Publish directory: **/** (repository root)
- Functions directory: **netlify/functions**

### Contact form

The footer contact form posts to `/api/contact`, which `netlify.toml` rewrites to
the `contact` function. That function relays the message via the **Resend** email
API. Set these environment variables in Netlify (Site settings → Environment
variables) for the form to send:

| Name | Example |
|---|---|
| `RESEND_API_KEY` | `re_...` (mark as secret) |
| `CONTACT_TO` | `info@feasibility-study-company.com` |
| `CONTACT_FROM` | `Feasibility Study Company <inquiries@feasibility-study-company.com>` |

The sending domain must be verified in Resend. See `DEPLOYMENT-contact-form.md`
(in the original package) for the full email setup.

### NDA generator

`/tools/nda/` is a fully client-side one-way NDA generator (jsPDF). Nothing is
transmitted or stored; it needs no backend. The page is `noindex`.

## Local preview

```bash
python3 -m http.server 8000
# open http://127.0.0.1:8000
```

## Brand

- Ink `#111114` · Signal red `#C8102E` · Rule `#E3E2DF`
- Typeface: Inter
