# WEB-FSC-5 close

Lane: the markets data pipeline for feasibility-study-company.com (wave 1). Branch `web-fsc-5`, worktree `~/Downloads/wt-web-fsc-5`, cut from local `main` at `1d48cc2` (= `origin/main`; step zero in STEP0.md). Main later moved to `53ad912` (WEB-FSC-4) and is merged in. No served page changed. Records: DECISIONS.md (D1 to D51), STEP0.md, GATES.txt, CLOSE-TABLES.md (the tables in full, generated from the register by `docs/web-fsc-5/tools/close_tables.py`), evidence/step0/, freeze/.

## The outcome

The lane first closed on 16 October without landing: only data.sba.gov was open. The owner then:
- supplied the location of API keys already registered;
- ruled on the doors;
- corrected my reading of those rulings, which I had taken to make www2.census.gov fetchable for named files (D50).

It is in fact closed under the standing robots rule. The 16 files I had fetched from it are held, never loaded or published. Every series built from them was removed and rebuilt from open sources.

The register now holds **7 of the charter's 10 series**:
- Census population estimates (Vintage 2023, Census Data API);
- ACS 5-year (2020-2024) and 1-year (2024);
- County Business Patterns 2023 by asset class (Census Data API);
- BEA personal income (2024);
- SBA 7(a) and 504 FOIA.

It covers every state, all 3,222 counties, all 935 CBSAs (membership from the Census Data API roster) and the 253 site markets. CBP has no row for the ten Puerto Rico metro areas or for two counties (Kalawao, Hawaii; King, Texas); those cells are nulls with that reason, never zeros (D51).
- **238 markets are standalone**, all eight in Texas included.
- **224 of 253 carry data from every applicable source** (FOIA, ACS 5-year, population estimates, CBP, BEA) at the market itself. The seven Connecticut planning-region markets have the four Census and BEA sources but FOIA only as two scheme components (no market total); counting those, 231. hawaii/maui lacks only BEA, which publishes Maui County only combined with Kalawao.

**NOT FETCHED, each with its recorded refusal:**
- **Building permits:** www2.census.gov is closed by robots.txt, and the Census Data API has no county permits.
- **QCEW:** api.bls.gov's robots.txt is `Disallow: /`; data.bls.gov is closed by robots.txt and answers 403.
- **HUD Fair Market Rents:** an AWS WAF bot challenge.

{{GATES}}

## Series: vintage, period, status

| charter series | source used | status | vintage / period | rows behind it |
|---|---|---|---|---|
| Census population estimates | census_pep_api (Census Data API, keyed) | **FETCHED** | Vintage 2023, July 1, 2020 to July 1, 2023 | 4 responses |
| ACS 5-year | census_acs5 (API, keyed) | **FETCHED** | 2020-2024 | 114 responses (nation, states, counties, CBSAs, places, county subdivisions) |
| ACS 1-year | census_acs1 (API, keyed) | **FETCHED** | 2024 (areas of 65,000+) | 10 responses |
| Building Permits Survey | census_bps | NOT FETCHED | 2025 annual | www2.census.gov robots.txt; no permits on the Census Data API (D1, D50) |
| County Business Patterns | census_cbp (API, keyed, all industries per request) | **FETCHED** | 2023 (NAICS 2017 codes) | 55 responses |
| QCEW | bls_qcew, bls_qcew_api | NOT FETCHED | 2025 annual | robots.txt `Disallow: /` on data.bls.gov and api.bls.gov; data.bls.gov also 403 (D3, D35) |
| BEA personal income | bea_cainc1_api (BEA API, keyed) | **FETCHED** | 2024 | 9 responses; the metro request returned error 101, so CBSAs sum their counties |
| HUD Fair Market Rents | hud_fmr | NOT FETCHED | FY2027 | AWS WAF bot challenge (D5) |
| SBA 7(a) FOIA | sba_foia | **FETCHED** | as of 2026-06-30, approval FY1991 to FY2026 | 4 files, 1,961,455 rows |
| SBA 504 FOIA | sba_foia | **FETCHED** | as of 2026-06-30, approval FY1991 to FY2026 | 2 files, 229,049 rows |

The roster comes from census_geoinfo (API, 2025, 1,110 responses). The 2020 Connecticut towns come from census_dec2020_ct (API). The held www2 sources (census_pep Vintage 2025, census_bps, census_cbp_bulk, census_delineation, census_ct_crosswalk) are listed file by file in D50.

There are 57 series files. Each has a row in `sources.json` with its title, URL, vintage, period, retrieval date, sha256 (per file, or for API pulls the sha256 of the sorted response hashes), cadence and next release.

## Market compositions

253 of 253 site markets are in `geographies.json`, with every county and CBSA as rows. By how they compose:

- **cbsa-delineation (116):** the federal membership of the market's CBSA.
- **cbsa-union (13):** equal to the federal union of the CBSAs they touch.
- **judgement-region (37), with `review` set:** includes the CBSA-derived rows that differ from the federal union, with the difference written on the row.
- **single-county (40) and page-named-counties (19).**
- **sub-county (20):** 16 places or New England towns carry ACS only; the 4 tract-sets carry nothing.
- **connecticut-two-schemes (8):** planning-region markets take Census figures from their planning regions. fairfield-county takes ACS from its 23 towns (2020 Census, API). FOIA keeps two exact scheme components per market.

**111 rows carry `review` = true** for the owner; CLOSE-TABLES.md lists them. FOIA county strings join to 2025 FIPS by name: 3,215 matched, 26 unmatched (listed).

## NAICS map

43 of 43 classes: 18 exact, 17 partial, 8 proxy.
- CBP 2023 uses NAICS 2017 codes. Gate 5 found this when the 2022 codes returned no gas stations, and classes now sum their 2017 lists (D44).
- CBP withholds some 6-digit cells below the state. A class missing a cell under a larger parent is written as a lower bound with its "up to" amount (a count of establishments in all three CBP series), and the renderer refuses it without a flag (D45). The API publishes sectors 31-33, 44-45 and 48-49 only as ranges, and the range is the sector parent (D51).
- FOIA class figures before FY2001 undercount and are refused unless flagged (D25).

## FOIA status table and match rates

- 7(a) statuses: `P I F`, `CHGOFF`, `EXEMPT`, `CANCLD`, `COMMIT`. 504 statuses: `PIF`, `CHGOFF`, `EXEMPT`, `CANCLD`, `NOT FUNDED`, `CLOSED`.
- Charge-offs: 7(a) 220,688, 504 12,169. Cancelled: 242,790 and 32,314. Undisbursed: 21,123 and 8,516. None of the cancelled or undisbursed loans is ever in a denominator.
- Project-county match: 7(a) 99.969% and 504 99.984%.
- Exact-duplicate rows are counted as published and disclosed (D23).

## Reconciliation

- **FOIA:** 72 of 72 program-by-FY cells equal the raw files. State sums differ from `us` only by 5 loans with a blank ProjectState.
- **Census, state against the sum of its counties:**
  - ACS and PEP are equal in every state.
  - BEA: Virginia and Hawaii are named, because BEA publishes some counties only inside combined areas.
  - CBP: no state falls below the sum of its counties. Each difference is named as statewide records (which the API does not publish by county) plus withheld county cells, with the bound.

## Texas and the standalone count

Texas (`tx`) holds 865 values specific to it. All eight Texas markets are standalone, each drawing on 6 sources:

| market | values |
|---|---|
| austin | 853 |
| corpus-christi | 799 |
| dallas-fort-worth | 851 |
| el-paso | 774 |
| houston | 855 |
| lubbock | 785 |
| mcallen | 788 |
| san-antonio | 845 |

Nationally, 238 of 253 markets are standalone. The 15 that are not:
- the 4 tract-sets;
- 10 place or town markets with ACS only;
- fairfield-county (ACS from towns only).

{{FREEZE}}

{{LAND}}

## For the next lanes

**Putting a market figure on a page:**
- Write `<!--mkt:<geo>.<series>[.<class>] {"fmt": ...}-->...<!--/mkt:...-->`. Geo is `us`, a state code, `co-<FIPS>`, `cbsa-<code>`, a market (`texas/houston`) or a FOIA component (`connecticut/fairfield-county:legacy`).
- Put the source line beside it: `<!--mktsrc:<geo>.<series>-->...<!--/mktsrc:...-->`.
- Run `python3 scripts/markets.py` to fill them, `--check` to gate, and `audit` to rewrite `data/markets/audit.csv`.
- The renderer refuses:
  - a null;
  - a flagged value without `{"allow_flag": true}`: a small denominator, a CBP lower bound (say "at least"), or a class figure covering approval years before FY2001;
  - a partial or proxy class without `{"fit": ...}`;
  - an approximate Connecticut component without `{"scheme_fit": "approximate"}`;
  - a window on a single-period series;
  - a format that does not fit the unit;
  - a source line whose period no value on the page shows.

**Refreshing:** `python3 scripts/markets_fetch.py --refresh` re-pulls every source whose next release has passed, plus every NOT FETCHED source; www2.census.gov is refused at its door. It then rebuilds and prints each value that changed.
- Load the owner's keys into the environment for the run, and set the API user agent in `MARKETS_UA`.
- The geoinfo roster takes about 1,100 requests at about 4 seconds each.

**Next releases:**
- SBA FOIA as of 2026-09-30, about 2026-10-31.
- ACS 2021-2025, December 2026.
- PEP Vintage 2024 or later and CBP 2024, if and when they appear on the Census Data API. The API held PEP to Vintage 2023 and CBP to 2023 on 16 October.
- BEA county personal income 2025, in BEA's next county release.

**Size:** the register is about 54 MB against the 60 MB cap. A wave that adds many markets will need the FOIA series split by program or state.
