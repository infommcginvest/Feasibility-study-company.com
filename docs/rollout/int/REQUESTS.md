# Requests for integrator-owned files (FACTORY-2, ROLLOUT-1 ruling 13)

A builder never edits `data/site/`, `data/mesh/`, `netlify.toml`, `src/site.json`, `src/case-cards.json`, the index pages or any served HTML. It asks for a change in one file in its own branch:

```
docs/rollout/<lane>/requests.json
```

The integrator applies it at landing with `python3 scripts/requests.py docs/rollout/<lane>/requests.json`. Run `python3 scripts/requests.py docs/rollout/<lane>/requests.json` in your throwaway copy before the readiness check, so your gates see the change; `--check` validates the file and reports what is not applied yet.

## Rules

- One file per lane, kept for the whole roll-out. Add requests; never delete one that has landed (every request is idempotent, so re-applying a landed request changes nothing).
- Each request has a unique `id` (`<lane>-<n>`) and a `kind`.
- Paths are site paths with a trailing slash: `/states/tennessee/nashville/`.
- No figures in requests. Labels and one-line card text only, no market numbers (those belong on the page, cited).
- A malformed request returns the whole tranche with the error.

## The file

```json
{
  "lane": "geo-1",
  "requests": [
    {"id": "geo-1-1", "kind": "promised", "urls": ["/states/tennessee/nashville/", "/states/tennessee/memphis/"]}
  ]
}
```

## Every kind, with an example

**promised**: new metro or subtype slugs you chose (amendment A5). Until a URL is in `data/site/promised.json` (or already a pending target somewhere on the site), a link to it is a broken link. Add it in the tranche *before* the one that links it, or in the same tranche.
```json
{"id": "geo-1-1", "kind": "promised", "urls": ["/states/tennessee/nashville/", "/states/tennessee/knoxville/"]}
```

**chrome_link**: an item in a mega panel column of `data/site/chrome.json`. `mega` is `markets` or `assets`; `col` is the column's class or title (`states`, `metros`, `Published Studies`). `fallback` is where the link points while the page is pending; `hide_until_live` omits it until the page exists.
```json
{"id": "geo-1-2", "kind": "chrome_link", "mega": "markets", "col": "metros", "label": "Nashville", "href": "/states/tennessee/nashville/", "fallback": "/states/tennessee/#metros"}
```

**mesh_term**: a first-mention term link in `data/mesh/terms.json` (at most 15 per page, first prose mention only). `ignore_case` true for common nouns; omit it for proper nouns.
```json
{"id": "asset-2-1", "kind": "mesh_term", "key": "hub-cold-storage", "target": "/asset-classes/cold-storage/", "terms": ["cold storage", "refrigerated warehouse"], "ignore_case": true}
```

**topic_asset**: an asset class in `data/mesh/topics.json` (the family must be one of the families listed there: Hospitality and outdoor recreation, Storage, Fuel, auto and travel, Health, care and services, Food and retail, Housing and senior living, Industrial and logistics). FACTORY-2 already added the thirteen new hubs.
```json
{"id": "asset-4-1", "kind": "topic_asset", "url": "/asset-classes/meat-and-poultry-processing/", "name": "meat and poultry processing", "family": "Food and retail"}
```

**topic_program**: a practice area in `topics.json` `programs` (FACTORY-2 already added `/practice-areas/hud-and-agency/`).
```json
{"id": "method-1-1", "kind": "topic_program", "url": "/practice-areas/hud-and-agency/", "name": "HUD and agency"}
```

**topic_note**: which hubs and practice areas a research note informs (`program_wide` lists it on every case in its programs). The note page must exist when this lands: `mesh.py` refuses a note that does not.
```json
{"id": "method-1-2", "kind": "topic_note", "url": "/research-notes/sba-default-economics/", "hubs": ["/asset-classes/hotel/"], "programs": ["/practice-areas/sba-7a-504/"], "program_wide": true}
```

**fallback**: where a pending link to a promised page points until it lands, when the class fallback is not the truthful one (class fallbacks: a state to `/states/`, a metro to its state's `#metros`, a subtype to its hub, a hub to `/asset-classes/`, a case to `/case-studies/`).
```json
{"id": "asset-3-1", "kind": "fallback", "url": "/asset-classes/skilled-nursing/", "target": "/asset-classes/assisted-living-and-memory-care/#skilled-nursing"}
```

**folded**: a promised page folded into a section of its parent (ruling 6). The section's id equals the slug. Every link to that section becomes a pending link to the promised page, so it switches on the day the page ships.
```json
{"id": "geo-1-3", "kind": "folded", "url": "/states/florida/the-villages/", "target": "/states/florida/#the-villages"}
```

**unfolded**: a folded page that now ships on its own (for example a Texas metro that reaches its count in the marker pass). Land it in the same tranche as the page.
```json
{"id": "geo-1-4", "kind": "unfolded", "url": "/states/texas/mcallen/"}
```

**subtype_section**: the hub section that pending subtype links of a hub fall back to.
```json
{"id": "asset-1-1", "kind": "subtype_section", "hub": "/asset-classes/hotel/", "section": "subtypes"}
```

**redirect**: a 301 in `netlify.toml`. Only for a retired path that no longer exists as a page (the industrial hub's `/asset-classes/industrial/` alias ships in the same tranche as `/asset-classes/industrial-and-warehouse/`, ruling 16).
```json
{"id": "asset-2-2", "kind": "redirect", "from": "/asset-classes/industrial/*", "to": "/asset-classes/industrial-and-warehouse/", "status": 301}
```

**index_entry**: an entry on a section index the integrator owns (`/`, `/states/`, `/asset-classes/`, `/case-studies/`, `/practice-areas/`, `/research-notes/`, `/analytical-framework/`). The integrator writes it in the house markup in the landing. `line` is one sentence, no figures.
```json
{"id": "geo-1-5", "kind": "index_entry", "index": "/states/", "url": "/states/tennessee/", "label": "Tennessee", "line": "Nashville's growth, Memphis logistics and the Smoky Mountain visitor economy."}
```

## Case cards (no request needed)

A case's card on `/case-studies/` comes from `src/case-cards/<slug>.json`, which the CASE lane owns (ruling 1):

```json
{"slug": "hotel-south-carolina-sba", "card": "A new {in_keys}-key limited-service hotel ...: the 7(a) structure reaches {dscr_y2} in Year 2 at {equity_pct} equity.", "category": "SBA 7(a) · South Carolina", "asset": "Hotel & Hospitality", "title": "Hotel Feasibility Study, South Carolina: An SBA 7(a) Worked Case"}
```

`card` is a template filled by `casemodel.py` from the case's values (as `src/case-cards.json` is); `casemodel.py` refuses a card that contradicts the determination. `category`, `asset` and `title` are the index entry: the integrator places the card on `/case-studies/` at landing. A slug in both `src/case-cards.json` and `src/case-cards/` is an error.

## What FACTORY-2 already did, so you need not ask

- `data/site/promised.json`: every URL the eleven saved blocks assign (513), plus every pending target already on the site. GEO-4's and CASE-3's URLs are added when their blocks are saved.
- `chrome.json`: the ten new states not yet listed (Ohio was), hidden until built; the thirteen new hubs, pending to `/asset-classes/` until built.
- `topics.json`: the thirteen new hubs with their families (one new family, Industrial and logistics), land-border neighbours for all 43 states with a page or a promise, and `/practice-areas/hud-and-agency/`.
- `fallbacks.json`: the sixteen permanent rewrites of ruling 16.
- `src/types.json` and a template-driven `build.py`: a page type is `src/templates/<type>.html` plus an entry in `src/types.json`.

**page_type** (METHOD-1): the settings for a new template you commit (`src/templates/practice.html`, `framework.html`, `note.html`). Allowed values are in `src/types.json`'s `_about`; ranges and figure classes follow ruling 3 and amendment A6.
```json
{"id": "method-1-3", "kind": "page_type", "type": "framework", "settings": {"schema": "article", "byline": "byline-article", "mode": "article", "house": "house-a.css", "page_css": null, "cite": "fn", "article_section": "Analytical Framework", "range": [2500, 5000], "figures": "short"}}
```
