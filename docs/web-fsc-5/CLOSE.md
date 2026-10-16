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

## Gates: 11 of 11 green

All eleven gates are green at `d82ece5`, the lane commit on top of the merge of main. GATES.txt holds each gate's checks and output; its runner is `python3 docs/web-fsc-5/gates/run_gates.py`.

- **1 (no served file):** 402 changed paths, all inside the lane.
- **2 (coverage):** all 253 site-market anchors at the cut point `1d48cc2` have a row. Every state, county and CBSA is present, and every source and series row has every field.
- **3 (reconciliation):** FOIA equals the raw files by program and FY. Every ACS, PEP, CBP and BEA state equals its county sum or is named with its measured difference.
- **4 (FOIA status):** every status is classified.
- **5 (NAICS):** every class is graded, and each carries a CBP 2023 national establishment count.
- **6 (independent re-derivation):** an independent subagent session wrote both checks against the raw files, importing nothing from the pipeline.
  - FOIA: 352 of 352 sampled values match, and a sweep of 4,416,192 values finds 0 problems.
  - Census and BEA, the one round on the affected series (D50): 797 sampled, 765 matched, 32 mismatched, all in CBP. The fixes are in D51.
  - After the fixes, the checker's unchanged script matches 767 of 767 and finds 0 problems in 698,030 values.
  - Quotas met: Connecticut 75, multi-county 264, sub-county 31, cross-state 98, medians 116 (multi-area medians null).
- **7 (aggregation):** no median is aggregated, and every rate is a ratio of sums.
- **8 (render):** the mutation test gives 0, 1, 0. The null marker is refused, and the fixture renders 6 Houston and 4 Connecticut markers.
- **9 (Texas):** `tx` holds 865 values; 8 of 8 markets are standalone.
- **10 (names and identity):** no match in lane files or commit identities.
- **11 (size):** 54.52 MB (52.00 MiB); largest file 4.93 MB; nothing under `_cache` is tracked.

BPS, QCEW and HUD are NOT FETCHED, each for a recorded refusal. Under the owner's 16 October ruling a series NOT FETCHED for a recorded refusal does not block landing; each is listed above with its reason.

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

## Freeze

The final freeze is the commit that holds this file together with its gate record (GATES.txt). Its record, `freeze/freeze-<sha>.json`, is written after that commit and committed in the records-only commit that follows. The record carries:
- the archive hash;
- the hash of every raw file and every data file;
- the 16 held www2 files, re-hashed where they are held to show they are unchanged.

**Final freeze record:**
- head `5b6c9f6358931d2a1fb58ffd06313a4685f2fb56`;
- archive sha256 `c6a4c14f3a3d1517fcf998ea60a8205a8134b2d73aa81e069bc9c6968b29d2e3`, reproduced with `git archive 5b6c9f6 | shasum -a 256`;
- data manifest sha256 `8e5937bf0fc7d8d7e5670946d2d251b03b204ab15e413c914d462cb46c9a3934`.

All 1,490 raw files are unchanged since retrieval, and the 16 held files are unchanged where they are held. 353 data files are hashed. See `freeze/freeze-5b6c9f6.json`. The gates were run at `d82ece5`: 11 of 11 green. The commit after it adds only GATES.txt and this file.

## Land and push

**Landed.** `git push . HEAD:main` from the worktree fast-forwarded local `main` `53ad912..5b6c9f6`; no other lane had landed since WEB-FSC-4. The records-only commit that holds this paragraph was fast-forwarded onto `main` after it. No served file changed (gate 1), and nothing was deployed.

**History.** Branch `web-fsc-5` is:
- `d2dabc6` (the first close);
- `4a95fb0`, a merge of main at `53ad912`;
- `d82ece5`, the lane commit;
- `5b6c9f6`, the gate record;
- this records-only commit.

The two commits that held the www2-built series (`7cff37f` and its merge `e334cfb`) sit only on the local branch `held-web-fsc-5-www2`. They are never pushed or bundled, and are ancestors of neither `main` nor `web-fsc-5` (D50).

**Push.** `git push origin main web-fsc-5`, with prompts disabled, failed for credentials: `fatal: could not read Username for 'https://github.com': terminal prompts disabled`. No credential was looked for, and `origin/main` is still `1d48cc2`.
- WEB-FSC-4 recorded that Netlify builds GitHub `main` on every push.
- This `main` carries WEB-FSC-4 and changes no served file.
- To publish, from the repository with the owner's credentials: `git push origin main web-fsc-5`, a fast-forward from `1d48cc2`.

**Bundle.** `main` and `web-fsc-5` at the commit that holds this paragraph go to `_bundles/web-fsc-5-<that sha>.bundle` in the repository root. The sha, size, sha256 and clone test are in the close reply. The held branch is not in the bundle.

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
