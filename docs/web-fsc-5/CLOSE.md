# WEB-FSC-5 close

Lane: the markets data pipeline for feasibility-study-company.com (wave 1). Branch `web-fsc-5`, worktree `~/Downloads/wt-web-fsc-5`, cut from local `main` at `1d48cc2` (= `origin/main`; step zero in STEP0.md). No served page changed. Records: DECISIONS.md (D1 to D22), STEP0.md, GATES.txt, CLOSE-TABLES.md (every table below in full, generated from the register).

## The outcome in one paragraph

Only one of the six source hosts was open to this lane. www2.census.gov, data.bls.gov and apps.bea.gov/regional/zip are closed by their own robots.txt. The Census Data API now refuses every data request without a key, and `CENSUS_API_KEY` is not set. www.huduser.gov answers every path with an AWS WAF bot challenge. data.sba.gov is open. So the register holds the SBA 7(a) and 504 FOIA series in full: every approval FY1991 to FY2026, by state, site market and asset class, with status, NAICS and Connecticut handled as the traps require. Every Census, BLS, BEA and HUD series is NOT FETCHED with its reason. Without a Census roster there are no county or CBSA rows, and the 130 markets whose counties rest on CBSA membership, including all eight Texas metros, carry no figure yet. The pipeline, render script, audit and gates are built, and `--refresh` treats every NOT FETCHED source as due, so a run with a Census API key picks the Census sources up at once. Their parsers still have to be written against real responses (D22).

## Gates: 7 of 11 green

Green: 1 (no served file), 3 (reconciliation), 4 (FOIA status), 7 (no synthesized medians or averaged rates), 9 (Texas, with the reason stated for each market), 10 (names and identity), 11 (size: 29.63 MB, largest file well under 25 MB).

Red, each for a reason this lane cannot fix:

- **2 (coverage).** 253 of 253 markets are present, and every source and series row has every field. But there is no county or CBSA roster: the Census Data API needs a key and www2.census.gov is closed by robots.txt.
- **5 (NAICS).** Every class is graded, and FOIA loans are reported by code and edition. But CBP was NOT FETCHED, so no class can show a national establishment count.
- **6 (independent re-derivation).** `docs/web-fsc-5/gates/rederive.py` was written by a separate agent and imports nothing from the pipeline. With seed 20261016 it matched 304 of 304 sampled values, and a full second pass compared all 3,797,376 values in the 16 series with no mismatch. Quotas: Connecticut 48, multi-county 80, cross-state 32 (19 market values, 13 part values). The sub-county quota (3) cannot be met: the FOIA files carry no project field below the county, so no sub-county value exists to re-derive.
- **8 (render).** The mutation test passes: `--check` exits 0, then 1 after the mutation, then 0 after the revert. The fixture renders Texas and Fairfield County's Connecticut components. But the register holds no Houston value, and the renderer refuses the Houston marker with that reason.

The charter requires every gate green before landing, so this lane does not land. GATES.txt holds every command and its output.

## Series: vintage, period, status, rows

| charter series | fetch source(s) | status | vintage / period | why not, if not |
|---|---|---|---|---|
| Census population estimates | census_pep (V2025 files), census_pep_api (V2023 API) | NOT FETCHED | V2025, 2020-2025 | www2.census.gov robots.txt (D1); the API needs a key (D2) |
| ACS 5-year | census_acs5 | NOT FETCHED | 2020-2024 | Census Data API key wall (D2) |
| ACS 1-year | census_acs1 | NOT FETCHED | 2024 | Census Data API key wall (D2) |
| Building Permits Survey | census_bps | NOT FETCHED | 2025 annual, 2021-2025 | www2.census.gov robots.txt (D1). There is no BPS endpoint on the Census Data API. |
| County Business Patterns | census_cbp (API), census_cbp_bulk (files) | NOT FETCHED | 2023 | key wall (D2) and robots.txt (D1) |
| QCEW | bls_qcew | NOT FETCHED | 2025 annual | data.bls.gov robots.txt `Disallow: /` and HTTP 403 (D3) |
| BEA personal income | bea_cainc1 (zip), bea_cainc1_api | NOT FETCHED | 2024 | robots.txt disallows /regional/zip/ and returns 403; the API needs a UserID (D4) |
| HUD Fair Market Rents | hud_fmr | NOT FETCHED | FY2027 | AWS WAF bot challenge (D5) |
| SBA 7(a) FOIA | sba_foia | **FETCHED** | as of 2026-06-30; approval FY1991 to FY2026 | |
| SBA 504 FOIA | sba_foia | **FETCHED** | as of 2026-06-30; approval FY1991 to FY2026 | |

Geography rosters: county roster NOT FETCHED, CBSA delineation NOT FETCHED (census_geoinfo key wall; census_delineation on www2), and the 2020 Connecticut county subdivisions NOT FETCHED (key wall).

FOIA rows read: 7(a) 1,961,455 (four files) and 504 229,049 (two files); the per-file counts are in `data/markets/foia-status-counts.json`. Loans net of cancellations: 7(a) 1,718,665 and 504 196,735. Sixteen series files: loans, volume, cancelled, disbursed, charge-off count, charge-off amount, and the seasoned charge-off rates by count and by amount, for each program. Each carries `us`, 60 state and territory codes, 95 summed site markets and 18 component ids (16 Connecticut scheme components, and permian-basin's two state parts), each for "all" and 43 classes, in five windows plus by approval year. The 158 markets with no figure carry their reason under `nulls`. Every series has a row in `sources.json` with its exact files, sha256s, period and next release; the next SBA release is expected 2026-10-31.

## Market compositions

253 of 253 site markets are in `data/markets/geographies.json`, Ohio's columbus included. By kind: cbsa 116, county 51, county-set 62, place 16, tract-set 4, cross-state 4. By how they get figures now (`composition_source`):

- single-county 40, page-named-counties 20, judgement-region 35: 95 markets summed from their FOIA county strings.
- cbsa-delineation-pending 130: their counties come from CBSA membership, which comes from the OMB delineation file. The composers' recalled lists are kept, marked unverified, but no figure is built from them (D16).
- sub-county 20 (places and tract-sets): the FOIA project location is a county, so there is no FOIA figure at that grain.
- connecticut-two-schemes 8: no total, two exact components each (D15).

**111 rows carry `review` = true** and go to the owner. The full list, with counties, basis and reason, is in CLOSE-TABLES.md under "Review rows for the owner". Departures from the charter's own slug reading are in D17.

## NAICS map

43 of 43 classes, graded 22 exact, 13 partial, 8 proxy, 0 none. Partial and proxy classes cannot be printed by `scripts/markets.py` unless the marker states the fit. FOIA loans by class, code and NAICS edition are in `naics-evidence.json` and CLOSE-TABLES.md. 225,772 FOIA loans have a blank NaicsCode (7(a) 203,850, 504 21,922, mostly FY1991 to FY2000). They count in "all" and in no class. The edition lists rest on the mapping subagent's knowledge, not a concordance file (D14).

## FOIA status table and match rates

Every distinct status value, classified, with the evidence behind each category, is in CLOSE-TABLES.md. 7(a): `P I F`, `CHGOFF`, `EXEMPT`, `CANCLD`, `COMMIT`. 504: `PIF`, `CHGOFF`, `EXEMPT`, `CANCLD`, `NOT FUNDED`, `CLOSED`. Charge-offs: 7(a) 220,688 and 504 12,169 loans, under the single code `CHGOFF` (no split code in these files). Cancelled loans (7(a) 242,790, 504 32,314) and undisbursed loans (`COMMIT` 21,123, `NOT FUNDED` 8,516) are never in a charge-off denominator.

Geocoding: method project_county (ProjectState plus the ProjectCounty string SBA writes). 7(a) 99.969% of 1,961,455 rows and 504 99.984% of 229,049 rows carry a county. The 644 blank-county rows are reported unmatched and still count in their state and in `us`. The ZIP to ZCTA method is not available. By-state rates are in `foia-geocoding.json`.

## Reconciliation

FOIA: the register's `us` totals equal the raw files in every program and approval-FY cell (72 of 72: rows, loans net of cancellations, volume). The independent re-derivation (gate 6) reproduced the same totals: 7(a) 1,961,455 rows, 1,718,665 loans, $527,243,968,642; 504 229,049 rows, 196,735 loans, $129,055,577,411. State sums equal `us` except for 5 7(a) loans with a blank ProjectState, which count in `us` only. No Census, BLS or BEA additive series was fetched, so there is no county-to-state-to-nation reconciliation to run.

## Texas and the standalone count

Texas (state `tx`) holds 698 values specific to it. None of the eight Texas markets (austin, corpus-christi, dallas-fort-worth, el-paso, houston, lubbock, mcallen, san-antonio) is standalone. Each is one CBSA, and its member counties must come from the OMB delineation file, which this lane could not fetch. The audit states that reason on every row. Nationally, 95 of 253 markets are standalone, every one on SBA FOIA values only (`sources_contributing` = 1). The 25-value threshold says little with a single source (D21), so re-read it once Census series arrive.

## Freeze

The freeze record for this commit is written after it, in a records-only commit, as `docs/web-fsc-5/freeze/freeze-<sha>.json`. It holds the HEAD sha, the sha256 of `git archive HEAD`, every raw file's URL, retrieval time, bytes and sha256 (re-hashed from disk at the freeze), and the sha256 of every file under `data/markets/`. The data manifest sha256 is the sha256 of that raw and data state, in canonical JSON.

## Attackers and verifier

Pending at the freeze: two attackers on Opus (wrong values with their own sample; FOIA and NAICS mapping) and one verifier on Sonnet reading the frozen tree cold.

## Land and push

Not landed: gates 2, 5, 6 and 8 are red, and the charter lands only on all green. `main` is untouched, and nothing was deployed or pushed.

## For the next lanes

**Putting a market figure on a page:**
- Write a marker: `<!--mkt:<geo>.<series>[.<class>] {"fmt": "int"}-->...<!--/mkt:...-->`. Geo is `us`, a state code (`tx`), a market (`texas/houston`) or a component (`connecticut/fairfield-county:legacy`); the series is a file name under `data/markets/series/`; the class is an asset-class slug.
- Put the source line next to it: `<!--mktsrc:<geo>.<series> {"window": "fy2016_2025"}-->...<!--/mktsrc:...-->`.
- Run `python3 scripts/markets.py` to fill them and `python3 scripts/markets.py --check` to gate.
- The script refuses a null (and prints its reason), a flagged value unless `{"allow_flag": true}`, and a partial or proxy class unless the marker states `{"fit": ...}`.
- `python3 scripts/markets.py audit` rewrites `data/markets/audit.csv`.

**Refreshing:** `python3 scripts/markets_fetch.py --refresh` re-pulls every source whose next release has passed, plus every NOT FETCHED source. It rebuilds and prints each value that changed.

**What opens the rest:**
- A Census API key in `CENSUS_API_KEY` opens ACS 2020-2024 and 2024 1-year, CBP 2023, PEP Vintage 2023, the geoinfo rosters (counties, the CBSA delineation through summary level 313, places, county subdivisions) and the 2020 Connecticut towns. That would resolve the 130 pending markets, all of Texas included. Parsers for these still have to be written and checked against real responses.
- An owner ruling on www2.census.gov's robots.txt would open PEP Vintage 2025, the 2025 permits, the CBP bulk files and the delineation file.
- A BEA API UserID in `BEA_API_KEY` opens CAINC1.
- QCEW and HUD stay closed while their doors are shut.

**Next releases:** SBA FOIA as of 2026-09-30, expected about 2026-10-31. Census: ACS 2020-2024 is in the API now, 2021-2025 5-year is expected in December 2026, PEP Vintage 2026 in March 2027, and CBP 2024 when Census publishes it.
