# GEO-5 research brief (one researcher per state; Sonnet)

You research ONE US state (or the District of Columbia) for feasibility-study-company.com, a firm that prepares market and feasibility studies for owners, developers and their SBA, USDA and bank lenders. Your two files feed a state page that must carry at least 20 counted research figures (target 40+), each a market figure with its own value, period, publisher, title and URL, dated, and found on no other page of the site. Volume of good, dated, primary figures is what matters. Write facts, never prose to copy.

## Output (exactly two files, nothing else written anywhere)

- `~/Downloads/fsc-rollout/drafts/geo-5/research/ST-<STATE>.md` (state economy, capital and lending, regulation, costs and insurance, hazards, statewide supply by asset class, the 2025 to 2026 events a lender will ask about)
- `~/Downloads/fsc-rollout/drafts/geo-5/research/MT-<STATE>.md` (its markets, one section per market)

`<STATE>` is the state name in capitals with hyphens: `VIRGINIA`, `NORTH-DAKOTA`, `DISTRICT-OF-COLUMBIA`.

Line 1 of each file is exactly `Research ID: ST-<STATE>` (or `MT-<STATE>`). Line 2: `Prepared: 2026-10-28 by GEO-5 research (web), accessed dates per row`. Then a short method note (5 lines max): which sources were primary, which doors were closed.

Figures go in markdown tables, ONE FIGURE PER ROW, rows never wrapped across lines, because pages cite `ST-<STATE> line <n>`. Columns, in this order:

`| # | Topic | Value | What it measures | Period | Published | Publisher | Title | URL | Kind | Note |`

- `#`: running number within the file (1, 2, 3...).
- `Value`: the number exactly as the source prints it (with unit, $, %).
- `Period`: the period the value describes (e.g. `1 Jul 2025`, `Q2 2026`, `FY2025`, `2024 annual`).
- `Published`: the document's publication, release, filing or effective date (YYYY-MM-DD or YYYY-MM), as the document itself shows it. If the page carries no date and is not a periodic release, write `undated`.
- `Title`: the document's own title, verbatim.
- `URL`: the exact page or file that prints the value (not a homepage).
- `Kind`: `primary` (the publisher's own data or document) or `secondary` (news, aggregator, relay of someone else's number; name the original in Note).
- `Note`: anything a checker needs: table or page number, "read on page", geography caveats, `single-property` if the value describes one named building, site or project rather than a market.

Group rows under `##` headings by topic (ST) or by market (MT). Under each heading add a `NOT FOUND:` line listing what you looked for and did not find (it becomes a stated gap on the page, never a number).

End each file with `## Doors closed` (URL, status or reason: 403, 429, robots, bot check, paywall, login) and `## Hygiene` (confirm the checks below).

## What dates a figure (house rule I77; undated figures do not count)

A figure is dated when tied to (a) a publication, release, filing or effective date, (b) an edition year in the document's title, or (c) the reporting period of a periodic document (a monthly or quarterly report, an annual statistical release, a 10-Q). A period printed on an undated, non-periodic web page ("2025 data") does NOT date it. Prefer documents with a visible date. Record the date you see; never guess one.

## What to collect (aim: ST 70 to 110 rows, MT 40 to 80 rows; every row dated)

State level (ST), by asset class where the evidence exists:
- population and migration: Census QuickFacts or the Census population estimates release on www.census.gov (Vintage 2025), state demographer releases, state labor department population or employment releases;
- employment and wages: BLS state and metro releases (bls.gov), state labor market information office monthly releases, unemployment rate with its month;
- GDP and industry: BEA state GDP by quarter (bea.gov release), state economic forecasts (state budget office, university bureau of business research);
- lending and capital: SBA district office announcements or FY2025 results (sba.gov), state small business credit programs (SSBCI allocations), state economic development finance programs, USDA Rural Development state office announcements, bank deposit totals from FDIC (dated), CDFI awards;
- regulation: state tax rates (lodging, sales, corporate) with effective dates, certificate of need, liquor licence rules, short-term rental laws, zoning reform statutes passed 2024 to 2026 with bill numbers and dates, environmental permitting;
- construction cost and insurance: published construction cost reports for the state's metros (Rider Levett Bucknall, Cumming, Mortenson, JLL, Turner city indices), state insurance department rate filings or reports, wage determinations;
- hazards: FEMA disaster declarations with numbers and dates, state hazard mitigation plan figures, wildfire, flood, earthquake, permafrost or winter data with dates;
- statewide supply by asset class: hotel (state tourism office or STR via a dated release: occupancy, ADR, RevPAR, room counts), multifamily (vacancy, rents from dated broker reports: CBRE, Cushman and Wakefield, Colliers, JLL, Marcus and Millichap, Newmark, Kidder Mathews, Berkadia, local brokers), self-storage, industrial, office, retail, senior housing (NIC MAP releases, state health department licensed bed counts), healthcare, agriculture and agribusiness (USDA NASS state releases), energy (EIA state profiles with release dates), tourism visitor counts and spending (state tourism office annual reports);
- 2025 to 2026 events: plant openings or closures with job counts, large projects, base realignments, data centers, energy projects, disasters, legislation, each with its date and a primary or news source.

Markets (MT): for each market below, the same families at metro, county or city level: population (Census Vintage 2025 county or metro estimates on www.census.gov), employment and unemployment (BLS metro release), city or county building permits and certificates of occupancy (city or county reports), broker quarterly reports by asset class for that market (vacancy, rent, absorption, construction pipeline, cap rates), hotel performance (convention and visitors bureau or tourism reports), traffic counts (state DOT AADT with year), airport passengers (airport annual or monthly statistics), major employers and announced projects with dates, local rules (short-term rental ordinances, zoning changes, impact fees with effective dates), local lenders and CDFIs or certified development companies serving the market.

## Figures that will NOT count (still record them only if useful context, marked in Note)

- US-wide or multi-state figures (they collide with other pages). Stay inside the state's own geography. For a metro that crosses a state line (for example Fargo-Moorhead or Sioux Falls), prefer the in-state county or city figure and say which in Note.
- The register series the site already holds for every state: ACS 5-year 2020-2024 and ACS 1-year 2024 estimates, County Business Patterns 2023, BEA personal income 2024, and SBA 7(a) and 504 loan-level FOIA totals. Do not spend effort on these series.
- Research-computed sums or comparisons (never add, divide or compare numbers yourself; record each number as the source prints it).
- Figures sourced only to an undated page.

## Hard rules (a breach voids the file)

- NEVER fetch anything on `www2.census.gov`. Use `www.census.gov`, `data.census.gov` pages or other publishers.
- Never work around a closed door: a 403, 429, robots.txt refusal, bot check, CAPTCHA, login or paywall is recorded in `## Doors closed` and you move to another publisher. Do not use archive.org, Google cache, proxies, other user agents or mirrors to reach a page that refused you. Finding the same figure in a different publisher's own document is fine.
- Never cite, name or use any of these, as a source or anywhere in your files (the brackets only stop this brief from matching itself; match case-insensitively): `m[m]cg`, `moh[e]lsky`, `union [m]etric`, `inno[w]ave`, `analytics[.]loan`, `loan analytic[s]`, `feasibility-study-consulta[n]t`, `wert-bera[t]er` or `wert bera[t]er`. If a source page you read is one of these sites, discard it and everything taken from it. Other consulting firms and brokers are fine.
- Never use an em dash or en dash in your files. Use commas, colons or "to".
- Never copy sentences from sources beyond the document title; record facts.
- Read only from the web and from the paths named here. Do not read or write anywhere else on this machine. Do not open any file named `.ghtoken`. No git commands. No database. Write only your two files.
- Every URL you cite must be one you actually opened (WebFetch) and saw the value on, or a search result snippet from the publisher's own domain that shows the value: mark the latter `Note: snippet` and prefer opening the page. Never attribute a figure to a source that does not carry it.
- Keep every network call bounded; if a fetch hangs or fails twice, record it and move on.

## Your report back (keep it short, under 250 words)

Rows in ST and MT; how many are primary and dated; how many secondary; how many undated; markets covered and rows per market; the main gaps; doors closed. Do not paste the files.
