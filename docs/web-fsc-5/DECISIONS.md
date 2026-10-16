# WEB-FSC-5 decisions

Each decision was taken without stopping, as speed rule 1 asks. Owner-facing items are marked **OWNER**.

## Doors (which hosts this lane may read)

**D1. www2.census.gov is closed by its robots.txt. OWNER.** The file opens with `User-agent: *`, a blank line, `User-agent: RavenCrawler`, then `Disallow: /`. RFC 9309 section 2.2 lets blank lines sit inside a group (`group = startgroupline *(startgroupline / emptyline) *(rule / emptyline)`), so `*` and `RavenCrawler` are one group and every unnamed agent is barred from the whole host. Google's reference parser reads it the same way: a new group starts only when a user-agent line follows a rule. The file is almost certainly an authoring slip, but the charter says never work around robots.txt, and the owner's 2026-09-22 and 2026-09-23 rulings that set robots aside applied to internal gathers, not to a lane whose output is served publicly. So PEP Vintage 2025, the Building Permits Survey, the CBP bulk files and the OMB delineation file (all on www2 only) are NOT FETCHED. The fetcher's evaluator was tested against the live robots bodies of all six hosts (12 of 12 cases), and against a control parser that splits groups on blank lines, which wrongly returns ALLOW for www2. **Reopen:** an owner ruling that www2.census.gov is fetchable; then `python3 scripts/markets_fetch.py --refresh` would fetch those files, but their parsers still have to be written against the real files.

**D2. The Census Data API is closed by a key wall. OWNER.** Every data request (acs/acs5 2024, acs/acs1 2024, cbp 2023, pep/charv 2023, geoinfo 2025, dec/pl 2020) returns HTTP 302 to `/data/missing_key.html` with `X-DataWebAPI-KeyError: 1`. The page says a valid key must be included with each data API request. The charter assumed keyless access with a daily limit; that is no longer true. `CENSUS_API_KEY` is not set, and creating an account is not something this lane does. **Reopen:** the owner requests a free key at api.census.gov and puts it in `CENSUS_API_KEY` for the run. The fetcher sends it on the request only and redacts it from every recorded URL.

**D3. BLS QCEW is closed.** data.bls.gov robots.txt is `User-agent: *` / `Disallow: /`, and `/cew/data/files/` returned 403 to a User-Agent that names the product and a contact address on feasibility-study-company.com, as BLS asks. NOT FETCHED.

**D4. BEA is closed.** apps.bea.gov robots.txt disallows `/regional/zip/` (CAINC1.zip), which also returned 403. robots allows `/api/`, but GetData needs a registered UserID (`BEA_API_KEY` not set). robots also allows `/regional/bearfacts/`, but BEARFACTS is an interactive fact-sheet app whose data come from the app's own `/data/...` calls, one area at a time and largely POST. That is not a published file, and this lane makes read-only GETs of published files. NOT FETCHED. **Reopen:** a BEA API UserID in `BEA_API_KEY`; the fetch plan for CAINC1 lines 1 to 3 (county, state and MSA) is already written.

**D5. HUD Fair Market Rents are closed.** www.huduser.gov answers every path, robots.txt included, with HTTP 202, an empty body and `x-amzn-waf-action: challenge`. That is a bot check, not worked around. NOT FETCHED.

**D6. api.census.gov robots.txt** comes back as HTTP 200 with a 247-byte WAF "Request Rejected" HTML page. It has no robots groups, so it evaluates as allow-all. This is moot while the key wall stands (D2).

**D7. data.sba.gov moved to Drupal 11.** The CKAN API (`/api/3/action/...`) and the old dataset slug are gone (404). The files are read from the dataset page `https://data.sba.gov/dataset/7a-504-foia` (robots allows `/dataset/` except `/dataset/search?`). The fetcher discovers them there every run, because their names carry the as-of date (`asof_260630`) and change every quarter. The run fetched six CSVs and the data dictionary as of 30 June 2026 (last modified 21 July 2026).

**D8. User-Agent:** `FSC-MarketsRegister/1.0 (federal statistics register for feasibility-study-company.com; contact info@feasibility-study-company.com)`. `info@` is the contact address the site already publishes (126 mentions); the commit identity's `noreply@` is not a contact.

**D9. No third-party Python.** The pipeline uses the standard library only (urllib, csv, zipfile with ElementTree for xlsx, json, hashlib), so there is no virtualenv and nothing installs system-wide. Every network call carries a 60 s socket timeout and at most 4 tries, and large files resume from a `.part` file with an HTTP Range request.

## Inputs read from the site

**D10. 253 market slugs.** A Python regex over all 160 HTML pages at the cut point found 253 distinct `/states/<state>/<market>/` anchors in 33 states: 8 in most, Hawaii 6, Missouri 7, Wisconsin 7, Ohio 1 (`columbus`, linked from the home page only; there is no Ohio state page). An earlier shell pipeline (`git grep -o | sed | sort -u`) returned 252, dropping `iowa/waterloo-cedar-falls`. The Python enumeration was checked per state against every `states/<state>/` reference, so the 252 was the instrument's fault, not the site's.

**D11. 43 asset classes.** The 28 built hubs plus the 15 unbuilt hub paths the charter lists. The site also links three more unbuilt hub paths: `/asset-classes/assisted-living/` and `/asset-classes/industrial/` (from two practice-area pages) and `/asset-classes/independent-living/` (from the assisted-living hub). Each is the short name of a class already in the 43 (`assisted-living-and-memory-care`, `industrial-and-warehouse`, `independent-living-and-ccrc`). They are recorded as aliases in `naics-map.json`, not as extra classes.
