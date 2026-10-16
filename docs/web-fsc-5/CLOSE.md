# WEB-FSC-5 close

Lane: the markets data pipeline for feasibility-study-company.com (wave 1). Branch `web-fsc-5`, worktree `~/Downloads/wt-web-fsc-5`, cut from local `main` at `1d48cc2` (= `origin/main`; step zero in STEP0.md). No served page changed. Records: DECISIONS.md (D1 to D32), STEP0.md, GATES.txt, CLOSE-TABLES.md (the tables below in full, generated from the register by `docs/web-fsc-5/tools/close_tables.py`), evidence/step0/, freeze/.

## The outcome in one paragraph

Only one of the six source hosts was open to this lane:

- www2.census.gov, data.bls.gov and apps.bea.gov/regional/zip are closed by their own robots.txt.
- The Census Data API refuses a keyless data request: HTTP 302 to `missing_key.html` with `X-DataWebAPI-KeyError: 1`, recorded in the manifest at 10:38:34Z. `CENSUS_API_KEY` is not set.
- www.huduser.gov answered with an AWS WAF bot challenge.
- data.sba.gov is open.

So the register holds the SBA 7(a) and 504 FOIA series in full: every approval FY1991 to FY2026, by state, site market and asset class, with status, NAICS and Connecticut handled as the traps require. Every Census, BLS, BEA and HUD series is NOT FETCHED with its reason. Without a Census roster there are no county or CBSA rows. The 137 markets whose counties rest on CBSA, CSA or micropolitan membership, including all eight Texas metros, carry no figure yet. The pipeline, render script, audit and gates are built. `--refresh` treats every NOT FETCHED source as due, and since the review the fetcher plans the CBSA-membership and county-subdivision pulls a key would allow. Those requests, and parsers for their responses, have never run against the live API (D22, D29).

## Gates: 7 of 11 green

Green: 1 (no served file), 3 (reconciliation), 4 (FOIA status), 7 (no synthesized medians or averaged rates; across all 29,392 rate cells the small-sample flag is set exactly when 1 to 29 loans were disbursed, a zero denominator gives a null with its own flag, and 30 or more carries no flag), 9 (Texas, with the reason stated for each market), 10 (names and identity), 11 (size: 31.63 MB, i.e. 30.17 MiB; largest file 1.95 MB).

Red, each for a reason this lane cannot fix:

- **2 (coverage).** The 253 site-market anchors are measured on the pages and all 253 are in `geographies.json`, and every source and series row has every field. But there is no county or CBSA roster (D1, D2).
- **5 (NAICS).** Every class is graded, and FOIA loans are reported by code and edition. But CBP was NOT FETCHED, so no class can show a national establishment count.
- **6 (independent re-derivation).** `docs/web-fsc-5/gates/rederive.py` was written by a separate subagent session. It imports nothing from the pipeline and implements the definitions from SBA's dictionary. On the final register, with seed 20261016, it matched 304 of 304 sampled values, and a full second pass compared all 3,644,608 values in the 16 series with no mismatch. Quotas: Connecticut 48, multi-county 80, cross-state 32. The sub-county quota (3) cannot be met: the FOIA files carry no project field below the county (ProjectCounty, ProjectState, CongressionalDistrict and SBADistrictOffice only), so no sub-county value exists to re-derive.
- **8 (render).** The mutation test passes: `--check` exits 0, then 1 after the mutation, then 0 after the revert. The fixture renders Texas and Fairfield County's two Connecticut components. But the register holds no Houston value, and the renderer refuses the Houston marker with that reason.

The charter requires every gate green before landing, so this lane does not land. GATES.txt holds each gate's checks and output, and the shell commands gates 1, 8 and 10 run. Its runner is `python3 docs/web-fsc-5/gates/run_gates.py`.

## Series: vintage, period, status

| charter series | fetch source(s) | status | vintage / period | why not, if not |
|---|---|---|---|---|
| Census population estimates | census_pep (V2025 files), census_pep_api (V2023 API) | NOT FETCHED | V2025, 2020-2025 | www2.census.gov robots.txt (D1); the API needs a key (D2) |
| ACS 5-year | census_acs5 | NOT FETCHED | 2020-2024 | key wall (D2) |
| ACS 1-year | census_acs1 | NOT FETCHED | 2024 | key wall (D2) |
| Building Permits Survey | census_bps | NOT FETCHED | 2025 annual, 2021-2025 | www2.census.gov robots.txt (D1). The API catalogue lists no county BPS dataset (evidence/step0). |
| County Business Patterns | census_cbp (API), census_cbp_bulk (files) | NOT FETCHED | 2023 | key wall (D2) and robots.txt (D1) |
| QCEW | bls_qcew | NOT FETCHED | 2025 annual | data.bls.gov robots.txt `Disallow: /` (D3) |
| BEA personal income | bea_cainc1 (zip), bea_cainc1_api | NOT FETCHED | 2024 | robots.txt disallows /regional/zip/; the API needs a UserID, and a keyless request returned an empty body (D4) |
| HUD Fair Market Rents | hud_fmr | NOT FETCHED | FY2027 | AWS WAF bot challenge (D5) |
| SBA 7(a) FOIA | sba_foia | **FETCHED** | as of 2026-06-30; approval FY1991 to FY2026 | |
| SBA 504 FOIA | sba_foia | **FETCHED** | as of 2026-06-30; approval FY1991 to FY2026 | |

Fetched: 2 of the charter's 10 series. Geography rosters (geoinfo counties, CBSAs and the summary-level-313 membership; the OMB delineation file; the 2020 Connecticut county subdivisions) are NOT FETCHED for the same reasons.

FOIA rows read: 7(a) 1,961,455 (four files) and 504 229,049 (two files). Loans net of cancellations: 7(a) 1,718,665 ($527,243,968,642 gross approval) and 504 196,735 ($129,055,577,411). There are sixteen series files: loans, volume, cancelled, disbursed, charge-off count, charge-off amount, and the seasoned charge-off rates by count and by amount, for each program. Each carries 167 geographies: `us`, the 60 ProjectState codes SBA writes (50 states, DC, PR, 7 other territories and freely associated states, and `TQ`, which is not a USPS code), 88 summed site markets, and 18 component ids (16 Connecticut scheme components and permian-basin's two state parts). Each geography carries "all" and the 43 classes. The additive series give five windows and a by-year array; the two rate series give one value pooled over the seasoned cohorts. The 165 markets with no figure carry their reason under `nulls`: composition-pending 137, not-published-at-this-grain 20, ct-split-coding 8. Every series has a row in `sources.json` with its exact files, sha256s, period and next release; the next SBA release is expected 2026-10-31.

## Market compositions

253 of 253 site markets are in `data/markets/geographies.json`, Ohio's columbus included. By kind: cbsa 116, county 51, county-set 62, place 16, tract-set 4, cross-state 4. By how they get figures now (`composition_source`):

- single-county 40, page-named-counties 19, judgement-region 29: 88 markets summed from their FOIA county strings. No string is duplicated within a market, none falls outside its state except in cross-state markets, and no county string sits in two summed markets.
- cbsa-delineation-pending 137: their counties come from CBSA, CSA or micropolitan membership, which only the OMB delineation file can confirm. The composers' recalled lists are kept, marked unverified, but no figure is built from them (D16, D27).
- sub-county 20 (places and tract-sets): the FOIA project location is a county.
- connecticut-two-schemes 8: no total, two exact components each (D15).

**111 rows carry `review` = true** for the owner. The full list, with counties, basis and reason, is in CLOSE-TABLES.md under "Review rows for the owner". D17 and D27 cover the departures and corrections.

## NAICS map

43 of 43 classes, graded 18 exact, 17 partial, 8 proxy, 0 none, after the attacker-two revisions (D26). A partial or proxy class cannot be printed unless the marker states the fit. FOIA loans by class, code and NAICS edition are in `naics-evidence.json` and CLOSE-TABLES.md. Blank NaicsCode: 7(a) 203,850 rows (176,915 net of cancellations) and 504 21,922 rows (18,655 net). They count in "all" and in no class. Before FY2001 the blanks fall on whole industries, so class figures for those years and for the window "all" undercount, and the renderer refuses them unless flagged (D25). The edition lists rest on the mapping subagent's knowledge, not a concordance file (D14).

## FOIA status table and match rates

CLOSE-TABLES.md classifies every distinct status value and gives the evidence behind each category:

- 7(a): `P I F`, `CHGOFF`, `EXEMPT`, `CANCLD`, `COMMIT`.
- 504: `PIF`, `CHGOFF`, `EXEMPT`, `CANCLD`, `NOT FUNDED`, `CLOSED`.
- Charge-offs: 7(a) 220,688 and 504 12,169 loans, under the single code `CHGOFF`. These files carry no split code.
- Cancelled loans (7(a) 242,790, 504 32,314) and undisbursed loans (`COMMIT` 21,123, `NOT FUNDED` 8,516) are never in a charge-off denominator.
- Raw-file properties are counted as published and disclosed (D23, D24). Exact-duplicate rows: 7(a) 1,918, of them 531 live ($250.5 million); 504 69, of them 3 live. Also one negative approval, and 182 charge-offs with a zero amount.

Geocoding uses method project_county: ProjectState plus the ProjectCounty string SBA writes. 7(a) 99.969% of 1,961,455 rows and 504 99.984% of 229,049 rows carry a county. The 644 blank-county rows are reported unmatched and still count in their state and in `us`. The ZIP to ZCTA method is not available. By-state rates are in `foia-geocoding.json`.

## Reconciliation

The register's `us` totals equal the raw files in every program and approval-FY cell: 72 of 72, on rows, loans net of cancellations and volume. The independent re-derivation (gate 6) reproduced the totals above. State sums equal `us` except for 5 7(a) loans with a blank ProjectState, which count in `us` only. No Census, BLS or BEA additive series was fetched, so there is no county-to-state-to-nation reconciliation to run.

## Texas and the standalone count

Texas (state `tx`) holds 698 values specific to it. None of the eight Texas markets (austin, corpus-christi, dallas-fort-worth, el-paso, houston, lubbock, mcallen, san-antonio) is standalone. Each is one CBSA, and its member counties must come from the OMB delineation file, which this lane could not fetch; the audit states that reason on every row. Nationally, 88 of 253 markets are standalone, every one on SBA FOIA values only (`sources_contributing` = 1). The 25-value threshold says little with a single source (D21), so re-read it when Census series arrive.

## Freeze, review and fixes

**Freeze 1** (`e7cc263`, archive sha256 `e901c068…`, data manifest sha256 `75f94397…`; `freeze/freeze-e7cc263.json`) went to three reviewers. Each wrote its own code against the raw files.

- **Verifier (Sonnet, cold):** 53 claims, 44 verified, 9 refuted; 0 blocker, 2 major, 10 minor. It found no wrong value: it recounted rows, totals, 72 FY cells, 222 market cells and 650 random cells. It also reproduced the archive hash, all raw and data hashes, and a byte-identical rebuild.
  - The refutations: the key wall rested on a constant message, not a recorded response (fixed, D2). A key would not have fetched CBSA membership (fixed, D29). 403 and WAF facts lived only in prose (evidence kept and disclosure added, D3 to D5, D30). GATES.txt wording (fixed). Process claims cannot be shown from the tree: which agent wrote rederive.py, and which models ran.
  - The minors: duplicate rows (D23), MiB vs MB (fixed), permian-basin's source (D31), TQ (D24), the literal "253" in the gate runner (now measured), the missing `cancelled` definition (added), and the post-freeze edits to rederive.py (diagnostics only; now part of freeze 2).
  - It disclosed one read-only `git ls-remote` that reached the network.
- **Attacker one (Opus, wrong values):** 125 comparisons from its own seeds, plus a full sweep of all 3,797,376 values. No value, numerator or denominator was wrong. 7 findings:
  - F1 (major): the amount-rate small-sample flag never fired. Fixed (D28).
  - F2 (major): seven summed markets rested on recalled CBSA, CSA or micropolitan membership. Fixed; now pending (D27).
  - F3 (major): hattiesburg omits Covington. Moot while pending; recorded on the row.
  - F4 (minor): wausau listed Price for Juneau. Fixed.
  - F5 (minor): rate periods. Fixed.
  - F6 (minor): source-line and format guards. Fixed.
  - F7 (minor): approximate CT components printed without a fit. Fixed.
  - It also confirmed the www2.census.gov robots reading (RFC 9309; Google's parser agrees).
- **Attacker two (Opus, FOIA and NAICS):** the arithmetic was exact (1.79 million market cells, 950,400 state cells); the 29 embedded newlines parse correctly; no status is unclassified. 9 findings:
  - A2-1 (major) and A2-2 (minor): pre-FY2001 class undercount. Resolved by a renderer-enforced flag, not imputation (D25).
  - A2-3 (major): auto-dealership missed RV, boat and motorcycle dealers. Fixed (D26).
  - A2-4, A2-5 and A2-7 (minor): tire dealers, coffee QSR, martial arts. Fixed (D26).
  - A2-6 (minor): two senior-housing grades. Fixed.
  - A2-8 (minor): the negative approval. Kept as published and disclosed (D24).
  - A2-9 (minor): labels. Fixed.

Every finding was reproduced from the raw files or the row text before it was acted on (DECISIONS D23 to D31). Of 16 attacker findings, 15 are fixed, and 1 (A2-8) is resolved by disclosure. The fixes change values, so the lane froze again, and all eleven gates and the independent re-derivation were rerun on the new freeze.

**Freeze 2** (`210aa6a`, archive sha256 `44c4157c…`, data manifest sha256 `2fb6f1d6…`; `freeze/freeze-210aa6a.json`) went to a re-check verifier (Sonnet). It reproduced all 12 resolutions:
- the recorded probes, and the planned CBSA-membership pulls (tested offline with HTTP blocked);
- the robots evidence and disclosures;
- F1 on all 29,392 rate cells (26,224 recomputed from raw);
- F2, F4, the renderer guards (39 test pages), the pre-FY2001 flag, and the NAICS revisions (re-derived from raw);
- the raw-file properties, and every changed CLOSE figure.

It found no regression: a sweep of 87,120 additive cells against its own raw recount showed 0 mismatches, and the only changed values are the ones the fixes explain. Its 10 minor points are fixed or disclosed for the final freeze (D32).

**The final freeze** is the commit that holds this file together with its gate record. Its record, `freeze/freeze-<sha>.json`, now also carries the manifest's door and probe records, and is written after it. The closing records-only commit copies the final freeze's hashes and the bundle into this file; it changes no data, script or gate file.

**Final freeze record:** head `6cff8d70aa29ecac24a001036778ab89a94f17d9`; archive sha256 `04c2bf7dd1a3f2a10e40f706bdc1edae09505618293b0032f4edb2db81401175` (reproduced with `git archive 6cff8d7 | shasum -a 256`); data manifest sha256 `48e3e5ce7cb7ab714db676ad880468b24bb63413ecbc08233bf681de92c5f916`. 7 raw files are unchanged since retrieval, 312 data files are hashed, and the manifest's 6 door and 2 probe records are carried; see `freeze/freeze-6cff8d7.json`. Gates at the final freeze: 7 of 11 green (GATES.txt). Gate 6, rerun on the final register: 304 of 304, and 3,644,608 values with 0 mismatches.

## Land and push

Not landed: gates 2, 5, 6 and 8 are red, and the charter lands only on all green. `main` is untouched, nothing was deployed, and nothing was pushed to `origin`. The branch `web-fsc-5` holds the work locally. A bundle of it is written to `<repo>/_bundles/` and clone-tested after the final freeze, and the closing records-only commit adds its name and the clone test.

## For the next lanes

**Putting a market figure on a page:**
- Write `<!--mkt:<geo>.<series>[.<class>] {"fmt": "int"}-->...<!--/mkt:...-->`. Geo is `us`, a state code (`tx`), a market (`texas/houston`) or a component (`connecticut/fairfield-county:legacy`); the series is a file name under `data/markets/series/`; the class is an asset-class slug.
- Put its source line beside it: `<!--mktsrc:<geo>.<series>-->...<!--/mktsrc:...-->`, with the same window or fy as the value.
- Run `python3 scripts/markets.py` to fill them and `python3 scripts/markets.py --check` to gate.
- The script refuses a null (printing its reason), a flagged value unless `{"allow_flag": true}`, a partial or proxy class unless the marker states `{"fit": ...}`, and an approximate Connecticut component unless `{"scheme_fit": "approximate"}`.
- It also refuses a class figure that includes approval years before FY2001 unless flagged, a rate with a window, and a source line whose period no value on the page shows.
- `python3 scripts/markets.py audit` rewrites `data/markets/audit.csv`.

**Refreshing:** `python3 scripts/markets_fetch.py --refresh` re-pulls every source whose next release has passed, plus every NOT FETCHED source, then rebuilds and prints each value that changed. It has been run once on this lane: 0 values changed.

**What opens the rest:**
- A Census API key in `CENSUS_API_KEY` lets the fetcher pull ACS 2020-2024 and 2024 1-year, CBP 2023, PEP Vintage 2023, and the geoinfo rosters. The rosters include counties, CBSAs, each CBSA's member counties (summary level 313), places and county subdivisions. It also opens the 2020 Connecticut towns.
- That would let the 137 pending markets, all of Texas included, be composed from the federal delineation.
- Those requests are planned but have never run, and the parsers for their responses still have to be written and checked against real data.
- An owner ruling on www2.census.gov's robots.txt would open PEP Vintage 2025, the 2025 permits, the CBP bulk files and the delineation file.
- A BEA API UserID in `BEA_API_KEY` opens CAINC1.
- QCEW and HUD stay closed while their doors are shut.

**Next releases:**
- SBA FOIA as of 2026-09-30, expected about 2026-10-31.
- ACS 2021-2025 5-year, expected December 2026.
- PEP Vintage 2026, March 2027.
- CBP 2024, when Census publishes it.
