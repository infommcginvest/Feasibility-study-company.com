# South Dakota pre-count, RERUN 2 (GEO-5, Sonnet reader)

**This is rerun 2.** The first pre-count (58 research, 68 in all) is replaced. What changed: the supplement `ST-SOUTH-DAKOTA-2.md` (71 primary rows, fact ids `ST-SOUTH-DAKOTA-2 line <n>`; the research row number `#` is line minus 9 in the first table, so "rows 20 and 21" are lines 51 and 52) was judged fresh; first-pass rows keep their rerun-1 judgements (none became `taken` or `shared_geo5` in the regenerated sheet; checked id by id). The integrator rulings of D17 and the four of this call were applied. Result: **44 supplement rows count; the state page holds 102 research (112 in all) on the main reading, up from 58; every market still folds, Sioux Falls included.**

Method (5 lines):
1. Rules: ROLLOUT-1 rulings 4 to 6, A4, A6, R9, I55 to I183 as the brief lists them, D7 and D17 of GEO-5, and the Montana pre-count method. Served tree ~/Downloads/wt-rollout-geo-5 at HEAD 0090d74 (register data unchanged since b62fb39, all 70 register pairs re-read and equal); `taken` and `shared_geo5` from the regenerated sheet unchanged.
2. Every one of the 243 rows (74 ST, 71 ST-2, 98 MT) was judged: dated by (a) publication date, (b) edition year in the title, (c) reporting period of a periodic document or the issue month of a monthly bulletin (ruling 4 of this call); not countable if a rule value, code or bill number, single property or firm (I64, I66), research arithmetic, a date not a figure, undated, or `taken`/`shared_geo5`. A value counts once per page (I82); no key collision remains on the state page.
3. Sheet overrides, supplement: ST-2 line 72 ($410,000, a program purchase-price limit) is a rule value, dropped; ST-2 line 159 ($119,959,861.12) the sheet drops because the word "Sum" in the row trips its arithmetic test, but the city's own pivot prints that Grand Total, so it counts; ST-2 line 113 ("17 projects") is not a figure pagecheck reads (no unit "projects"), dropped; ST-2 lines 51 and 52 not countable (ruling 2); ST-2 lines 93, 95, 96 (NASS) count only because my spot check read them by name in the NASS file (ruling 1, below). First-pass overrides stand (ST 69, 72, MT 83 out; MT 143 and bare counts read with a unit in; ST 12 same fact as MT 11).
4. Markets: free research at least 21, research plus at most 10 register at least 30, and at least 20 once secondary rows (then borderline rows) are removed (I180). Sioux Falls uses Minnehaha and Lincoln county register figures only (D7); LMIC's Sioux Falls MSA rows (ST-2 line 104 to 106) include Rock County, Minnesota and stand only in the Sioux Falls section, labelled (ruling 3); county rows are preferred. Register: 10 free pairs available everywhere (70 pairs, unchanged), so the register adds 10 to every page.
5. Spot check: 24 pages opened, 49 rows, 19 of the pages and 41 of the rows supplement rows; see the table. No door closed, no www2.census.gov.

## Verdict table

Facts = rows of the page's section (the state row counts the state's own ST and ST-2 rows). Countable = rows that pass every rule before the served-site and GEO-5 sharing test (so it includes rows that are out only because `taken`; the last row counts the two duplicates twice). Register in brackets = free pairs available (at most 10 counted).

| Page | Facts | Countable | Free research, main reading (a/b/c) | Register (free pairs) | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| sioux-falls | 54 | 46 | 32 (23/5/4) | 10 (36) | 42 | folds into the state page (section id `sioux-falls`); 17 without secondary |
| rapid-city | 33 | 27 | 16 (11/4/1) | 10 (16) | 26 | folds (section id `rapid-city`) |
| aberdeen | 10 | 9 | 3 (1/1/1) | 10 (11) | 13 | folds (section id `aberdeen`) |
| brookings | 10 | 7 | 3 (1/1/1) | 10 (11) | 13 | folds (section id `brookings`) |
| watertown | 11 | 7 | 5 (1/1/3) | 10 (10) | 15 | folds (section id `watertown`) |
| mitchell-pierre | 14 | 14 | 5 (3/2/0) | 10 (22) | 15 | folds (section id `mitchell-pierre`) |
| state, own rows | 111 | 70 | 40 (28/5/7) | 10 (17) | 50 | state page (a new state: R9) |
| state, six markets folded | 243 | 180 | 102 (66/19/17) | 10 | 112 | state page: clears R9 on the main reading |

**Sioux Falls does not stand as a metro page.** The supplement lifts it to 32 free research figures (23/5/4 dated by a, b, c) and 42 in all, over the first floor of 21 and over 30. It fails the I180 test: 15 of its original 24 and none of the 8 new rows are secondary, so with secondary rows out it holds 9 + 8 = **17** (20 needed); without borderline it keeps 32; without secondary and borderline 17. It also leans on seven cross-state rows (four FRED/Realtor.com CBSA relays and the three LMIC MSA rows): without them 25; without city-level rows 24. It folds into the state page as section `sioux-falls`. Rapid City rises from 8 to 16 (8 without secondary), Watertown 1 to 5, Mitchell and Pierre 3 to 5, Aberdeen and Brookings 1 to 3; none is near 21.

Standing metros taken out of the state page: none, so the state's count is the same either way: **102 research, 112 in all** (main reading). For information, Sioux Falls' 32 rows are 32 of the state page's 102 (without them 70, deduplicated).

Slugs proposed (none promised in `data/site/promised.json`; no case town in South Dakota, A4 does not bind): `sioux-falls`, `rapid-city`, `aberdeen`, `brookings`, `watertown`, `mitchell-pierre` (Mitchell in the Mitchell micro area, Pierre in the Pierre micro area; the research files them together).

## Sensitivity, per market and for the state (free research figures; each market tested as a standing page)

Families: secondary (news relays, FRED relays, Bender and SDMHA articles via SiouxFalls.Business, Rapid City Post, KOTA, Dakota News Now, DTN, Pro Farmer: 40 counted rows); borderline (ST line 21, 22, 24, the live DLR economic snapshot, "Preliminary data; subject to revision", no release date); live-page (FRED series and the DLR snapshot); preliminary (those three plus BLS "(p)" Sep 2026 rows ST-2 line 29 to 31 and the two BLS Q1 2026 county-wage release rows, line 32 and 109); approximate (MT 59 "more than"); stale / prior-period (2023 and mid-2025 rows, plus the five 2024-vintage population rows and the Q1 2025 airport row); bare counts read with a unit (357 permits, 232 units, 79 units, and so on); cross-state; complement or label doubt (adds the Sioux Falls population conflict, the SDHDA income base, the 562,027 and 63,399 labels, the homeless post date); bulletin issue month only (e-Labor Bulletin rows dated by the issue month, ruling 4, I77(c)); periodic PDF with no issue date (airport statistics PDF, Watertown compilation); edition year only (b) with no day (LMIC 2025 QCEW annual report rows and the Commission on Gaming FY2025 report); NASS PDF rows; city-level.

| Reading | state own | sioux-falls | rapid-city | aberdeen | brookings | watertown | mitchell-pierre | state, six folded |
|---|---|---|---|---|---|---|---|---|
| main reading | 40 | 32 | 16 | 3 | 3 | 5 | 5 | 102 |
| without secondary | 29 | 17 | 8 | 2 | 2 | 4 | 2 | 64 |
| without borderline | 37 | 32 | 16 | 3 | 3 | 5 | 5 | 99 |
| without live-page (FRED, DLR snapshot) | 29 | 26 | 12 | 2 | 2 | 4 | 3 | 78 |
| without preliminary | 33 | 31 | 16 | 3 | 3 | 5 | 5 | 94 |
| without approximate | 40 | 32 | 15 | 3 | 3 | 5 | 5 | 101 |
| without stale / prior-period | 39 | 28 | 13 | 2 | 2 | 5 | 4 | 91 |
| without bare counts read with a unit | 39 | 29 | 15 | 3 | 2 | 3 | 5 | 96 |
| without cross-state CBSA/MSA | 40 | 25 | 16 | 3 | 3 | 5 | 5 | 95 |
| without complement or label doubt | 36 | 29 | 16 | 3 | 3 | 5 | 5 | 95 |
| without bulletin issue month only (ruling 4, I77c) | 36 | 31 | 15 | 2 | 2 | 5 | 5 | 94 |
| without periodic PDF, no issue date (c) | 40 | 29 | 16 | 3 | 3 | 2 | 5 | 96 |
| without edition year only (b), no day | 35 | 27 | 12 | 2 | 2 | 4 | 3 | 83 |
| without NASS PDF state rows (I69 ruling 1) | 37 | 32 | 16 | 3 | 3 | 5 | 5 | 99 |
| without city-level | 40 | 24 | 13 | 2 | 2 | 2 | 4 | 85 |
| without secondary and borderline | 26 | 17 | 8 | 2 | 2 | 4 | 2 | 61 |

Borderline (counted in the main reading as dated (c), listed so the sensitivity can remove them): ST line 21, 22 and 24 only. The supplement adds no live-API or live-data rows: every ST-2 row is a dated release, a bulletin issue, an annual report or a named document. The 2025 QCEW annual report pages are static report pages with the edition year in the title (b), not live data pages, so they are not borderline; they have their own column.

## Sensitivity, state page (six markets folded)

| Reading | Research figures |
|---|---|
| main reading (all markets folded, deduplicated) | 102 |
| without secondary | 64 |
| without borderline | 99 |
| without secondary and borderline | 61 |
| primary rows only | 64 |
| primary rows with a printed publication day (a) | 28 |
| NASS rows out (if the integrator does not accept my by-name reading) | 99 |
| six markets as pages (the state's own rows only) | 40 |
| own rows without secondary | 29 |
| register counted (free pairs 17 on the state page: 10) | 10 |

## The state's harshest stack (cumulative removals, in this order)

Full stack, 14 steps (the first eleven are the rerun-1 families, with the new rows assigned to them; the three new families, bulletin issue month, edition year only and NASS, sit before city-level):

| Step | Research left | In all (plus 10 register) |
|---|---|---|
| main reading | 102 | 112 |
| + without secondary | 64 | 74 |
| + without borderline | 61 | 71 |
| + without live-page (FRED, DLR snapshot) | 61 | 71 |
| + without preliminary | 56 | 66 |
| + without approximate | 56 | 66 |
| + without stale / prior-period | 50 | 60 |
| + without bare counts read with a unit | 47 | 57 |
| + without cross-state CBSA/MSA | 44 | 54 |
| + without complement or label doubt | 40 | 50 |
| + without bulletin issue month only (ruling 4, I77c) | 39 | 49 |
| + without periodic PDF, no issue date (c) | 34 | 44 |
| + without edition year only (b), no day | 18 | 28 |
| + without NASS PDF state rows (I69 ruling 1) | 15 | 25 |
| + without city-level | 11 | 21 |

Stack of the rerun-1 families only (ten removals plus city-level, no new family), for comparison with the first pre-count (which ended at 8 research):

| Step | Research left | In all |
|---|---|---|
| main reading | 102 | 112 |
| + secondary | 64 | 74 |
| + borderline | 61 | 71 |
| + live-page (FRED, DLR snapshot) | 61 | 71 |
| + preliminary | 56 | 66 |
| + approximate | 56 | 66 |
| + stale / prior-period | 50 | 60 |
| + bare counts read with a unit | 47 | 57 |
| + cross-state CBSA/MSA | 44 | 54 |
| + complement or label doubt | 40 | 50 |
| + periodic PDF, no issue date (c) | 35 | 45 |
| + city-level | 31 | 41 |

Reading: the state clears 20 research and 30 in all on the main reading (102 and 112), without secondary (64 and 74) and without secondary and borderline (61 and 71). On the rerun-1 stack it ends at **31 research, 41 in all**, still over both floors (was 8 and 18). On the full 14-step stack it ends at **11 research, 21 in all**, under both floors; the drop below 20 comes only at the step that removes every row dated by an edition year alone (34 to 18), a family I77(b) expressly allows. Primary rows with a printed publication day alone hold 28 (was 14). The state ships on the main reading with a margin of 82 over R9's 20 research and 82 over 30 in all.

Sheet cross-check: the regenerated sheet's mechanical `countable` flag holds 99 rows. My list (104 rows, 102 once MT 71 and MT 108 are collapsed on the state page) takes out 7 of them (ST 12, ST 69, ST 72, MT 83, and ST-2 line 51, 52 and 72) and adds 12 (ST 11 and ST 108, MT 11, 14, 15, 24, 71, 108, 121 and 143, and ST-2 line 159 and 161). The three NASS rows are in the sheet's 99 and in mine, now on evidence.

## Spot check (24 pages opened with WebFetch; no door closed, no www2.census.gov)

Supplement rows (19 pages, 41 rows). PDFs came back as binary from WebFetch; I read the text of the files the fetch saved with a PDF text script (pypdf, layout mode) and quote what it printed.

| Row | Source | Result |
|---|---|---|
| ST-2 line 29, 30, 31 (and 28 taken) | BLS State Employment and Unemployment, 2026 M09, laus_10202026.htm | Confirmed: Table 3, South Dakota, Sep 2026 (p): professional and business services 35.9, education and health services 81.6, government 80.6 (thousands); (p) = preliminary; release Tuesday 20 Oct 2026. |
| ST-2 line 32 and 109 | BLS County Employment and Wages, Q1 2026 | Confirmed: South Dakota $1,211, Minnehaha $1,369; release Friday 4 Sep 2026. |
| ST-2 line 23 to 26 (and 22 taken) | LMIC qcew2025_2_summary.aspx | Confirmed: $60,577, $71,093, 44,302, $24,183 (and 460,365); page title "Labor Market Information Center - 2025 QCEW Annual Report"; "Data subject to revision". Day not shown (b). |
| ST-2 line 11, 116, 128, 140, 151 (and 172 taken) | e-Labor Bulletin December 2025, "Where demographic data meets the road" | Confirmed: 924,669 (state), Sioux Falls 209,300, Rapid City 79,900, Aberdeen 27,900, Brookings 24,550 (Pierre 13,800, Mitchell 15,600), all 2024 Census PEP; the issue is December 2025, no day. Dated (c) by ruling 4. |
| ST-2 line 104, 105, 106 | LMIC qcew2025_10_sfmsa_est_work_pay.aspx | Confirmed: 177,999, $66,768, 34,900; the page says the MSA is Lincoln, Minnehaha, McCook and Turner counties of South Dakota and Rock County of Minnesota. Cross-state, labelled. |
| ST-2 line 108, 127, 139, 150, 162, 170, 171 | LMIC qcew2025_7_county_annual_pay.aspx | Confirmed: $66,906, $59,768, $56,565, $58,550, $54,662, $57,418, $64,153. The page's own title is the Annual Report title above and its table heading reads "Annual Pay for Covered Workers by County"; the research's title adds "2024 and 2025". See flag 9. |
| ST-2 line 107, 126 | LMIC qcew2025_6_county_workers.aspx | Confirmed: Minnehaha 139,770, Pennington 62,445. |
| ST-2 line 27 | e-Labor Bulletin April 2026, nonfarm year in review | Confirmed: 469,400, issue April 2026. |
| ST-2 line 34 | e-Labor Bulletin July 2026, industry projections | Confirmed 562,027 as "Total of All Industries" for 2034; the same table includes self-employed, unpaid family workers (25,801) and farm (34,087); the strictly nonfarm wage and salary total is 502,139. Label doubt, kept. |
| ST-2 line 35 | e-Labor Bulletin October 2026, occupational demand | Value printed (63,399, Total, All Occupations, October 2026), but the fetch warned that the column headers do not line up in its copy: the "Average Annual Openings" header sits over 3,856. Kept as "total annual openings" in the label-doubt family; the writer must open the page and check the column. |
| ST-2 line 74 | SDHDA statewide homeless count post | Confirmed 1,154 on "January 27"; the text speaks of the "2026 count"; the post date prints "Apr 22" with no year. Dated by the count and the 2026 count wording; year-less post date flagged. |
| ST-2 line 72 | SDHDA Give Me Five | Confirmed $410,000 "or less", launch 2 Nov 2026, dateline 10/13/26. Row dropped as a rule value (not a spot-check failure). |
| ST-2 line 73 | SDHDA Governor's House income limits | Confirmed "currently $103,400", effective 15 June 2026; post date "Jun 15" without year. Kept (state median income as a statistic), in label doubt. |
| ST-2 line 129, 130 | DOR newsroom, 2026 Sturgis rally | Confirmed: $1,404,408 total; $473,668 from 161 vendors in the southern Black Hills; release 09-01-2026. |
| ST-2 line 131 | rapairport.com post | Confirmed: 76,958 year to date, Q1 2025, post 04/11/2025. Stale. |
| ST-2 line 93, 95, 96 | NASS Crop Production (October 2026) crop1026.pdf | WebFetch returned binary; the saved file's text prints the rows by name: "South Dakota ... 6,350 5,840 171.0 145.0 151.0 1,085,850 881,840" under the corn header (area 2025 and 2026, yield 2025, September 1, October 1, production 2025 and 2026), "South Dakota ... 5,060 5,400 47.0 42.0 42.0 237,820 226,800" under soybeans, and the narrative "In South Dakota, the average yield is forecast at 1,959 pounds per acre, down 16 pounds per acre from last year's record high." Released Oct 9, 2026. Confirmed by name; counted under ruling 1, with its own column. |
| ST-2 line 114 | Sioux Falls airport minutes 25 Mar 2026 (PDF) | Confirmed by script: "February record of 62,556", total 123,567, meeting March 25, 2026. |
| ST-2 line 159, 160, 161 | Watertown "2025 Monthly Combined" (PDF) | Confirmed by script: heading "January - December 2025"; New Commercial Building 20 permits $52,312,150.00; New Single Family Dwelling 68 permits, 79 housing units, $26,132,301.00; Grand Total 1125 records, $119,959,861.12. The "Sum of" in the row is the pivot label; the total is printed, so it is not research arithmetic. No publication date in the text (file metadata not a printed date). |
| ST-2 line 62 | Commission on Gaming FY2025 annual report (PDF) | Confirmed by script: $2,315,908.04 to the State general fund per 42-7B-48.1; the same report prints 1.93% and the 9% rate (rule value, not counted). |

First-pass rows reopened (5 pages, 8 rows; the 19 pages of rerun 1 stand, all confirmed):

| Row | Source | Result |
|---|---|---|
| ST line 21, 22, 24 (borderline) | dlr.sd.gov/lmic/economic_snapshot.aspx | Confirmed: 484,700, 475,100, 470,500, Sep 2026; no release date printed; "Preliminary data; subject to revision". |
| ST line 29 (secondary) | FRED SDMFG | Confirmed: 43.8 thousand, Sep 2026, last updated 20 Oct 2026. |
| MT line 139 (secondary) | FRED MEDLISPRI33580 | Confirmed: $251,950, Sep 2026, Realtor.com, updated 1 Oct 2026. |
| MT line 121 (secondary) | FRED BPPRIV046029 | Confirmed: 142, annual 2025, "Units", title "New Private Housing Structures Authorized by Building Permits for Codington County, SD", updated 28 May 2026. |
| MT line 59, 60 (secondary) | Rapid City Post, 8 Jan 2026 | Confirmed: more than $390.9 million and 2,428 permits, attributed to the Building Services Division year-end report. |

Tally: **24 pages opened, confirmed 24, not on page 0, door closed 0.** Caveats on five: ST-2 line 35 (column order), line 34 (label), line 74 and 73 (post date without a year), line 72 (dropped as a rule value). No row was marked not countable by the spot check.

## Flags for the writer

1. **Sioux Falls MSA rows (ST-2 line 104 to 106, MT 44, 45, 47, 48) are cross-state.** LMIC's MSA includes Rock County, Minnesota; label them "the Sioux Falls metropolitan statistical area, including Rock County, Minnesota", in the Sioux Falls section only, and prefer the Minnehaha rows (line 107, 108, 109) for anything said about the city's market. MT 48 is a discontinued BEA series (2023).
2. **NASS (ST-2 line 93, 95, 96).** Counted because the NASS file I opened prints South Dakota by name on the row with the header printed above (area 2025 and 2026, yield, production); if the integrator does not accept a text-extraction reading as "a file that prints the value for South Dakota by name", these three go to dropped with the reason "column order rebuilt (I69)" and the state falls by 3 (99 research, 109 in all; the harshest stack by 3 less at the NASS step is already shown). ST-2 line 92 (151.0) and 94 (42.0) are `taken` by values already on served pages and out. The sunflower value is read from the narrative sentence, not a table.
3. **Ruling 2.** ST-2 line 51 and 52 (BFM revenue estimate, FY2026 surplus) are in `dropped`: search-result text only, PDFs never opened. They are unusable until a page that prints them is opened.
4. **Bulletin rows (ruling 4, I77(c)).** ST-2 line 11, 27, 34, 35, 116, 128, 140, 151 are dated only by an e-Labor Bulletin issue month (Dec 2025, Apr 2026, Jul 2026, Oct 2026). Cite them as that issue. They are one family in the sensitivity.
5. **Population conflicts.** ST-2 line 11 (924,669, PEP 2024) and ST line 11 (935,094, FRED, Census 1 Jul 2025) are the same series for different years; ST-2 line 116 (Sioux Falls 209,300, PEP 2024) sits beside MT 11 (224,676, SDPB quoting the city's 2025 year-end report). Print each only with its year and publisher, never as competing totals; the 2024 values are prior-vintage. Since the page carries a Vintage 2025 population, no PEP or ACS population pair is used from the register (unchanged).
6. **Labels.** ST-2 line 34: "Total of All Industries" includes self-employed and farm; do not call 562,027 wage and salary workers. ST-2 line 35: confirm the column is Total Openings. ST-2 line 73: the SDHDA page states $103,400 as the State Median Income for the program's income limits; print it as that statistic, not as a limit. ST-2 line 74: the post prints no year; cite the 27 January 2026 count.
7. **Bare counts and units.** pagecheck reads a number under 1,000 only with a listed unit. "79 units" (ST-2 line 161, from "79 housing units" in the research, print "79 units") is read; "17 projects" and "58 days" are not. Equal values across sections: 232 (Lincoln MT 24, Lawrence MT 71), 357 (Sioux Falls MT 14 permits, Brookings MT 108): once per page, the first counts.
8. **Preliminary values.** BLS Sep 2026 rows are marked (p) and the Q1 2026 county release is flagged preliminary by the researcher; print "preliminary". The DLR snapshot (ST line 21, 22, 24) is a live page that will move to October data; cite September 2026.
9. **Titles.** Under I176 use the research's wording. Rows 5 to 9 and 38 to 40, 51 to 54 carry "Labor Market Information Center - 2025 QCEW Annual Report"; rows 42, 54, 59, 63, 68 to 70 carry "Annual Pay for Covered Workers by County 2024 and 2025", which in my fetch was close to a table heading ("Annual Pay for Covered Workers by County") on a page whose own title is the Annual Report title: the writer should check which wording is the document's title before printing. Titles with a dash written as a hyphen: the BLS "County Employment and Wages in South Dakota - First Quarter 2026", the LMIC titles, ST line 57, 120, 121, the MT Sioux Falls titles.
10. **Dating.** QCEW rows and the gaming report are dated by an edition year in the title and show no day; the Watertown compilation by its title year and period (its PDF text prints no date); Brookings' monthly report is `taken`. Rapid City airport (ST-2 line 131) is Q1 2025 and stale; the airport statistics PDF (MT 41 to 43) is dated (c) only.
11. **Sturgis.** ST-2 line 129 and 130 (DOR tax collections, Aug 2026 rally) sit in the Rapid City section (Meade and Lawrence counties, southern Black Hills); ST line 57 and 58 (vehicles) sit on the state page. Rapid City Post, KOTA and Dakota News Now rows remain relays whose originals were not opened.
12. **Rows the state cannot print as counted.** Of the 71 supplement rows, 44 count, 21 are `taken` by served pages or shared with another new state, and 6 fall on other grounds (line 51, 52, 72, 82, 83, 113); see `dropped` in the JSON (for example the QCEW total 460,365, the Brookings permit values, the Sioux Falls permit averages, GDP growth 1.5%, the Freedom 250 impact, SBA loan limits).
13. **Closed doors in the research** (census.gov, fema.gov, rcgov.org, sdstate.edu, bfm.sd.gov timeouts, ellsworth.af.mil): none worked around. FEMA declaration codes (ST line 120, 121) and Census population rest on relays and stay out or uncounted as in rerun 1.
14. **Housekeeping.** The first JSON's `secondary_ids` omitted the two deduplicated FRED rows (MT 71, MT 108); they are secondary and are now listed. The JSON carries extra keys (`families`, `cross_state_ids`, `nass_ids_confirmed_by_name`) for the writer; the required keys are unchanged.
