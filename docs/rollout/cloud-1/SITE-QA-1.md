# SITE-QA-1: main pages, links, about and contact (CLOUD-1, 4 Nov 2026)

Owner request (4 Nov): make sure the main pages, the links, the about page and the rest work. Checked on the deploy tree of main `1559002d` (what production serves: `git archive` without `docs`, `src`, `data/markets`). The live domain cannot be reached from the cloud container (its network policy refuses it), so nothing here was checked against production itself.

## What was checked, and the result on main
| Check | Result |
|---|---|
| Every internal link, stylesheet, script, image and form target on all 213 served pages, resolved against the files and `netlify.toml` redirects | 0 broken |
| Every in-page and cross-page anchor (`#id`) | 0 missing |
| `sitemap.xml` | 211 URLs, all resolve; every indexable page is listed; `robots.txt` allows all and names the sitemap |
| One title, one H1, a meta description, a canonical that matches the URL, JSON-LD that parses | all pages (the 404 page has no canonical and is `noindex`, as it should) |
| 22 main pages in headless Chromium at 1440 and 390 (home, about, every section index, legal pages, the NDA tool, the 404 page, and a state, metro, hub, subtype, case, practice area and note) | status 200, an H1, no script error, no failed local asset, no broken image, no page-level sideways scroll |
| Contact form on the home page | an empty submit sends nothing; a filled submit posts name, email, organization, project type, message and the honeypot to `/api/contact` and shows the thank-you message; the function validates, drops honeypot posts and reads its mail key from Netlify's environment |
| Mobile menu at 390 and 360 | **broken**: the house CSS hides every header link under 680px and leaves only the Inquiries button, so phones had no way to reach Practice Areas, Asset Classes, Framework, Research, About or Markets from the header |
| Common typed addresses | **missing**: `/about`, `/about-us`, `/contact`, `/contact-us` returned 404 |

## Fixes on this branch (`cloud/site-qa-1`)
1. `scripts/chrome.py`: the header region now carries one small rule for screens under 680px: the primary links show as a wrapped second row under the logo, and the taller header scrolls away instead of staying stuck over the page. Desktop and tablet are unchanged (the header stays sticky there). The rule lives inside the `chrome:header` region, so the chain puts it on all 213 pages; no page body, source or stylesheet changes.
2. `netlify.toml`: 301 redirects `/about` and `/about-us` to `/the-practice/`, and `/contact` and `/contact-us` to `/#contact`.

## Gates on a copy with the fixes (chain run, `gates.py --stage landing --site-wide`)
- `chrome.py` rewrote 213 pages, 0 problems; `chrome.py --check`: 0 out of date.
- Gates 2, 9 (links site-wide), 10, 11, 12 (212 pages), 13 (1440 and 390) and 14 green. Gate 1 reports the home page without a BreadcrumbList and the index and legal pages without an author `@id`: identical to unchanged main (those pages are not content pages), not caused by this change.
- 45 browser loads after the fix (15 pages at 390, 360 and 1440): 0 sideways scroll, 0 off-screen menu links, 0 script errors; the same seven links on every page at 390.

## For the integrator
Merge, run the chain (it re-renders every page's header region), gates, deploy. The redirects take effect with the deploy.

## Noted, not changed
- The desktop header has no Case Studies item (it is in the footer and on the home page). Adding one is a `data/site/chrome.json` change and a desktop layout decision: owner's call.
- External links (census.gov, bls.gov, sba.gov and others, about 2,400 in all) could not be checked from the cloud: the network policy refuses those hosts.
