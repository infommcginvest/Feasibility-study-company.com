# The page factory (src/)

Nothing under `src/` is served (`netlify.toml` answers `/src/*` with 404). Every page built by
the factory has one source file here and one served file at its URL. Edit the source, never
the served `index.html`.

```
src/site.json                        deploy_date used by "DEPLOY" dates
src/templates/base.html              head, chrome regions, main, footer (shared)
src/templates/{state,metro,hub,subtype,case}.html   main layout per page type
src/templates/partials/              house CSS (byte for byte), factory.css, chrome partials
src/pages/<url path>.html            one source per page, e.g. src/pages/states/texas/houston.html
data/cases/<slug>.json               case model inputs (case pages only)
scripts/build.py                     renders sources into served pages
scripts/casemodel.py                 computes cases and fills their <!--case:--> regions
```

## Build order

```
python3 scripts/build.py                  # or --page /states/texas/houston/
python3 scripts/chrome.py                 # when present (WEB-FSC-4)
python3 scripts/byline.py
python3 scripts/regulatory.py
python3 scripts/markets.py                # when present (WEB-FSC-5)
python3 scripts/casemodel.py
python3 scripts/mesh.py                   # when present (WEB-FSC-4)
python3 scripts/links.py --relink         # when present (WEB-FSC-4)
python3 scripts/sitemap.py                # when present (WEB-FSC-4)
```
Every script has `--check`. `build.py --check` compares each served page with a fresh render
everywhere outside the script-owned regions (`chrome:`, `mesh:`, `fsc:`, `sba:`, `mkt:`, `case:`).

## How to add a page

1. Create `src/pages/<url path>.html` (the URL `/states/texas/houston/` lives at
   `src/pages/states/texas/houston.html`).
2. Write the front matter and body below. Run the build order. Commit the source, the served
   page and anything the scripts rewrote.

## How to add a case

1. Write `data/cases/<slug>.json` (format below) and `src/pages/case-studies/<slug>.html`.
2. Put `{{case:<table>}}` where each model table goes and `{{case:v.<value>}}` wherever prose
   states a number the model computes. Never type a model number by hand.
3. Run the build order; `python3 scripts/casemodel.py --case <slug>` prints the computed model
   and the list of values.

## Source file format

The file opens with a JSON front matter block between two lines of three hyphens, then the
body:

```
---
{
  "type": "metro",
  "url": "/states/texas/houston/",
  "title": "Houston Feasibility Study, Texas | Feasibility Study Company",
  "description": "Meta description, 140 to 160 characters.",
  "og_description": "optional; defaults to description",
  "h1": "Houston Feasibility Studies",
  "eyebrow": "Texas &middot; Houston",
  "hero_sub": "First-screen answer, one paragraph, may cite [^3].",
  "hero_secondary": {"text": "Jump to supply", "href": "#supply"},
  "breadcrumb": [["Home", "/"], ["Markets", "/states/"], ["Texas", "/states/texas/"], ["Houston"]],
  "service": {"name": "Houston Feasibility Studies", "serviceType": "Feasibility study consulting",
              "areaServed": {"@type": "City", "name": "Houston"}, "description": "..."},
  "published": "DEPLOY",
  "updated": "DEPLOY",
  "stats": [{"num": "7.8", "unit": "M", "label": "Metro residents, July 2025 [^1]"}],
  "faq": {"eyebrow": "Houston Questions", "h2": "Houston feasibility study questions.",
          "items": [{"q": "Question?", "a": "Answer with a citation [^4]."}]},
  "cta": {"h2": "Underwriting a Houston project? Start with the market read.", "p": "One or two sentences."},
  "sources_lede": "Every figure on this page traces to a named, dated source.",
  "sources": [
    {"publisher": "U.S. Census Bureau", "title": "Vintage 2025 County Population Estimates",
     "date": "March 2026 (population as of July 1, 2025)", "url": "https://www.census.gov/..."}
  ]
}
---
<section id="economy" data-eyebrow="Economic Base" data-h2="What Houston runs on." data-lede="optional">
<div class="prose">
<p>Prose with a citation [^1].</p>
</div>
<div class="data-table-wrap">
<table class="data">
<thead><tr><th scope="col">Indicator</th><th scope="col">Figure</th><th scope="col">Period</th><th scope="col">Source</th></tr></thead>
<tbody>
<tr><td>Population</td><td>7,796,182</td><td>July 1, 2025</td><td>[^1]</td></tr>
</tbody>
</table>
</div>
</section>
```

Front matter rules:
- `type`: state, metro, hub, subtype or case. `url` must match the file's place under `src/pages`.
- `published` and `updated`: ISO dates, or `"DEPLOY"` for `src/site.json` `deploy_date`. New
  pages: both `"DEPLOY"`. Rebuilt pages: keep the old published date; `updated` is `"DEPLOY"`.
- Cases also carry `"data_as_of": "2026-10"` and may set `"case_slug"` (defaults to the last URL segment).
- `sources`: every entry needs `publisher`, `title`, `date` and an absolute `url`; optional `note`.
  Numbering is the list order, from 1. Cite by number: `[^3]`, `[^3,7]`.
- `faq` items render visibly and as FAQPage JSON-LD. `title` and `description` are plain text.

Body rules:
- The body is a sequence of `<section id="..." data-h2="...">...</section>` elements and nothing
  else. Optional `data-eyebrow`, `data-lede`; `data-layout="split"` puts everything after
  `<!--aside-->` in the right column (use `<aside class="panel">` there). No nested sections.
  Grey and white bands alternate automatically. Section ids must be unique and must not be
  `faq`, `sources` or `main`.
- Inside a section use house markup: `<div class="prose">` for text (`<p>`, `<ul>`, `<ol>`,
  `<h3>`), `<div class="data-table-wrap"><table class="data">` for tables (add `num` to the
  class for right-aligned numbers, `wide` for tables of five or more columns), `<ol class="failures">`
  with `<li><div><h3>..</h3><p>..</p></div></li>` for numbered failure lists, `<div class="metro-grid">`
  with `<div class="metro"><div class="metro-tag">..</div><h3><a>..</a></h3><p>..</p></div>` for
  market cards, `<ul class="link-cols">` for link lists, `<ul class="case-list">` with
  `<li><a href="..">Title</a><span>one line</span></li>` for case lists.
- SBA rules go through `sba:` markers, written with the current value inside:
  `<!--sba:dscr.standard_7a.value-->1.15x<!--/sba:dscr.standard_7a.value-->`. Common paths and their
  values today: `sop.name` (SOP 50 10 8.1 with Technical Policy Updates), `sop.short` (SOP 50 10 8.1),
  `sop.effective {"fmt": "date"}` (`<time datetime="2026-10-01">October 1, 2026</time>`),
  `equity.startup_7a.value` (10%), `equity.coo_initial_acquisition.value` (10%),
  `equity.sba_504_standard.value` (10%), `equity.sba_504_new_or_special.value` (15%),
  `equity.sba_504_new_and_special.value` (20%), `dscr.standard_7a.value` (1.15x),
  `dscr.coo_initial_acquisition.value` (1.25x), `dscr.sba_504.value` (1.15x), `limits.max_7a.value`
  ($5 million), `limits.max_504.value` ($5 million), `limits.max_504_manufacturer.value` ($5.5 million),
  `limits.combined.value` ($10 million), `rates.prime.value` (7.00%), `rates.peg.value` (5.00%),
  `fees_fy2027.upfront_504.value` (0.50%), `fees_fy2027.waiver_7a_max_loan.value` ($700,000),
  `terms.real_estate_max_years.value` (25), `terms.coo_amortization_years.value` (10),
  `jobs_504.per_job.value` ($95,000), `regulation.feasibility_study.value`
  (13 CFR 120.160(b): SBA may require professional appraisals, a survey, or a feasibility study).
  The full list is `data/regulatory/sba.json`. SBA "may require" a feasibility study; never write
  that SBA requires one.
- Case pages: `{{case:glance}}` and the other tables, `{{case:v.dscr_y2}}` for values.
- Never use em dashes or en dashes in any encoding (build.py refuses them). Use a hyphen for
  ranges ("2025 to 2026" reads better) and a comma, colon or parentheses elsewhere.
- Links: only to pages that exist (or to pages built in the same lane). Contextual links in
  prose use plain `<a href="/path/">anchor</a>`.

## Case input file (data/cases/<slug>.json)

```
{
  "slug": "car-wash-texas-sba",                 (must equal the file name)
  "page": "/case-studies/car-wash-texas-sba/",
  "program": "sba_504",                         (sba_7a | sba_504 | usda_bi | hud_232)
  "sba": {"purpose": "startup", "business_age": "new", "special_purpose": true,
          "manufacturer": false, "rural_fee_waiver": false},
  "rule_sources": {"sop": 31, "fees": 32, "prime": 33, "program": 30},
  "stabilized_year": 3,
  "dscr_test_year": 2,
  "units": {"label": "tunnel", "count": 1},
  "inputs": {
    "land": {"value": 1450000, "fmt": "$", "label": "Land, 1.6 acres", "source": [12]},
    "cars": {"value": [92000, 118000, 131000, 134000, 137000], "fmt": "n", "label": "Cars washed",
             "assumption": "Ramp to the county benchmark of ... over three years; the benchmark is [^14]."}
  },
  "uses": [{"key": "land", "label": "Land", "expr": "land", "class": "real_estate", "basis": "[^12]"}],
  "revenue": [{"key": "retail", "label": "Retail washes", "expr": "cars * retail_share * retail_price", "basis": "cars x share x price [^14]"}],
  "cost_of_sales": [],
  "opex": [{"key": "labor", "label": "Labor", "expr": "labor * (1 + wage_growth) ** y", "basis": "[^20]"}],
  "proposed": {"equity_pct": 0.15, "note": "the sponsor proposes 15% equity"},
  "historical": {"ebitda": [{"label": "FY2024", "value": 410000}, {"label": "FY2025", "value": 455000}], "use": "last"},
  "breakeven": {"input": "cars", "label": "cars washed"},
  "sensitivity": {"rows": {"input": "cars", "label": "Car volume", "steps": [-0.2, -0.1, 0, 0.1, 0.2]},
                  "cols": {"input": "retail_price", "label": "Average ticket", "steps": [-0.15, -0.075, 0, 0.075, 0.15]}},
  "glance": [["Location", "Seguin, Guadalupe County, Texas, on the I-10 corridor [^3]"],
             ["Total project cost", "{tpc}"], ["Determination", "..."]]
}
```

- Every input carries exactly one of `"source": [n, ...]` (numbers in the page's sources list) or
  `"assumption": "reasoning"`. A value is a number, or a list of five numbers (one per year).
  `fmt`: `$`, `$2`, `%`, `%2`, `x`, `cpg` (dollars per gallon shown as cents), `n`, `n1`, `n2`, `yr`.
- Expressions use input names, `y` (year index 0 to 4), `+ - * / **`, `min`, `max`, `round`; a
  five-value input used bare means its value for the year. Revenue lines can be referred to later
  as `rev_<key>` and `rev_total`; cost of sales as `cos_<key>`, `cos_total`, `gp_total`; opex lines
  as `opex_<key>`; `tpc` is total project cost.
- `uses[].class`: `real_estate`, `equipment`, `working_capital`, `business` or `other`. For 7(a),
  real estate at 51% or more of uses gives a 25-year term; for an acquisition the real estate share
  amortizes over 25 years and the business share over 10 (sba.json).
- Program inputs. `sba_7a`: `sba_guaranty_pct` (cited), optional `rate_7a` (else Prime plus the
  maximum spread from sba.json), optional `non_re_years`. `sba_504`: `tpl_rate`, `tpl_amort_years`,
  `debenture_rate`, `debenture_years`. `usda_bi`: `bi_guarantee_pct`, `bi_fee_pct`, `bi_rate`,
  `bi_amort_years`, `bi_equity_min_pct`, `bi_dscr_floor`, optional `bi_loan_cap`. `hud_232`:
  `hud_max_ltc`, `hud_dscr_floor`, `hud_rate`, `hud_mip_annual`, `hud_amort_years`, optional
  `hud_upfront_fees`. SBA equity tiers, DSCR floors, size limits, fees and Prime come from
  sba.json; `rule_sources` names the page's source numbers for the SOP (`sop`), the FY2027 fee
  notice (`fees`), H.15 Prime (`prime`) and, for USDA or HUD, the program source (`program`).
- `sba.purpose`: `startup` (7(a) test: projected DSCR in `dscr_test_year`, default Year 2) or
  `acquisition` (Appendix 15: historical EBITDA from `historical`, labelled illustrative, against
  the 1.25x floor). For 504 the equity tier follows `business_age` (`new` = two years or less) and
  `special_purpose`; `manufacturer` raises the debenture limit.
- The engine sizes the proposed structure, tests it, and when a test fails restructures: equity to
  the tier, the loan or debenture to its limit, then the smallest equity share that meets the
  floor in the test year.
- Tables: `glance`, `inputs`, `revenue`, `opex`, `uses`, `sources`, `loan`, `proforma`, `dscr`,
  `determination`, `verdict`, `breakeven`, `sensitivity`. Values: `v.tpc`, `v.equity_pct`,
  `v.loan_total`, `v.ds`, `v.dscr_y1` to `v.dscr_y5` (and `_proposed`), `v.noi_y1` to `v.noi_y5`,
  `v.rev_y3`, `v.breakeven_pct`, `v.cushion_pct`, `v.in_<input>` and more (`casemodel.py --case`).
  `glance` rows may hold `{value}` placeholders such as `{tpc}`.
