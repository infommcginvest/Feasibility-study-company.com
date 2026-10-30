# Wyoming pre-count, RERUN 2 (GEO-5, Sonnet reader)

**This is rerun 2.** The first pre-count (69 research, 79 in all) is replaced. What changed: the supplement `ST-WYOMING-2.md` (72 rows, all primary, fact ids `ST-WYOMING-2 line <n>`; the research row number `#` is the position of the row among the 72, so the integrator's "rows 33 to 38" are lines 79 to 84, "row 56" is line 109, "rows 46, 47, 59" are lines 92, 93, 119, "row 20" is line 45) was judged fresh; the 199 first-pass rows keep their rerun-1 judgements (checked id by id against the regenerated sheet: none became `taken` or `shared_geo5`, none left it). The integrator rulings for the supplement were applied. Result: **30 supplement rows count (16 state rows, 14 in market sections); the state page holds 99 research (109 in all) on the main reading, up from 69 (79). Cheyenne rises from 14 to 19 free research figures and still does not stand as a metro page (21 needed); every market folds.**

Method (5 lines):
1. Rules: ROLLOUT-1 rulings 4 to 6, A4, A6, R9, I55 to I183 as the brief lists them, D12, D15 and D17 of the GEO-5 decisions, and the South Dakota rerun as the model for a supplement. Served tree ~/Downloads/wt-rollout-geo-5 at HEAD 8b2a94f (docs-only commit over 0090d74: `data/markets` and `src/pages` unchanged, so the 75 register pairs of the first run stand); `taken` and `shared_geo5` are the regenerated sheet's, unchanged for the 199 first-pass rows.
2. All 271 rows (ST 77, ST-2 72, MT 122) were judged: dated by (a) publication date, (b) edition year, (c) reporting period of a periodic release; not countable if rule value, code, single property or firm (I64, I66), claim, research arithmetic (I55), undated, a search-result snippet (integrator), no figure pagecheck reads, or `taken`/`shared_geo5`. A value counts once per page (I82); no key collision remains among the 99 kept rows (checked on pagecheck's keys).
3. Secondary rows count in the main reading when the row names the original publisher and a date (brief rule 3); the six first-pass exclusions stand (ST 63; MT 108, 109, 110, 136 name no original; MT 76 is a CEO's claim). All 72 supplement rows are primary, so the secondary count stays 41. BLS Economy at a Glance rows (11) stay counted as (c) and borderline (D12); two NASS Quick Stats rows are added to that borderline list (below); ST-2 line 22 and 45 are borderline and left out, as ST line 76 was in the first run.
4. Bare counts are read with the unit the row supplies when pagecheck reads the unit (jobs, visitors, listings, and so on): two more here (ST-2 line 14, "-63", and 15, "157", both "jobs", printed in the BLS table). "Claims" and "weeks" are not units pagecheck reads, so ST-2 line 21 (972 initial claims) is not a figure. Register: unchanged, `wy`, `co-56xxx` and single-state `cbsa-` keys, 10 free pairs available on the state page (26 before the family rule), no PEP, ACS or BEA population level (Vintage 2025 population, ST line 10).
5. Spot check: 16 pages opened, 13 of them supplement pages carrying all 30 counted supplement rows plus the 3 rows left out as borderline, and 3 first-pass secondary or borderline pages; see the table. No door closed, no www2.census.gov.

## Verdict table

Facts = rows of the page's section (the state row holds the state's own ST rows and the ST-2 rows under statewide headings). Countable (sheet) = the regenerated sheet's mechanical flag, which includes the served-site test. Register = free pairs after the family rule (counted: at most 10; free distinct series before the family rule in brackets).

| Page | Facts | Countable (sheet) | Free research, main reading (a/b/c) | Register | Total at READY | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| cheyenne | 56 | 17 | 19 (15/0/4) | 10 (22) | 29 | folds into the state page (section id `cheyenne`); 12 without secondary |
| casper | 38 | 11 | 12 (9/1/2) | 10 (24) | 22 | folds (section id `casper`) |
| laramie | 6 | 3 | 2 (2/0/0) | 8 (9) | 10 | folds (section id `laramie`) |
| gillette | 15 | 5 | 3 (3/0/0) | 9 (9) | 12 | folds (section id `gillette`) |
| jackson | 26 | 10 | 10 (10/0/0) | 9 (10) | 19 | folds (section id `jackson`) |
| rock-springs-green-river | 10 | 2 | 2 (2/0/0) | 9 (10) | 11 | folds (section id `rock-springs-green-river`) |
| sheridan | 11 | 3 | 4 (4/0/0) | 10 (11) | 14 | folds (section id `sheridan`) |
| state, own rows | 109 | 47 | 47 (40/0/7) | 10 (26) | 57 | state page (a new state: R9) |
| state, seven markets folded | 271 | 98 | 99 (85/1/13) | 10 | 109 | state page: clears R9 on the main reading |

(a/b/c): (a) printed publication date, (b) edition year in the title (only ST-2 line 109), (c) reporting period of a periodic release (the 11 BLS Economy at a Glance rows and the two NASS Quick Stats rows, whose Published cell is only the access date; see flag 5). The state own-row figure (40/0/7) has no (b) because ST-2 line 109 sits in the Casper section.

**Cheyenne does not stand as a metro page.** It holds 19 free research figures against the 21 required (14 before the supplement; the 5 new rows are three BLS OEWS Cheyenne wage rows, ST-2 line 85 to 87, and two DWS Laramie County employment rows, 89 and 90), 29 with the 10 register pairs against 30 required, and 12 once its 7 secondary rows are removed (8 without secondary and borderline), against the 20 the I180 rule asks. It fails all three tests. The supplement's Visit Cheyenne annual report rows (ST-2 line 79 to 84, dated by the edition year in the title under I77(b), as the integrator ruled) are all `taken` on the regenerated sheet and are out of the count; if the integrator overrode that, Cheyenne would hold 25 (18 without secondary, 14 without secondary and borderline), which still fails the I180 test; only if the six and also ST-2 line 88 and 91 (both `taken`) were released would it reach 27 (20 without secondary, 16 without secondary and borderline). See flag 3.

Standing metros taken out of the state page: none stands, so the state's count is the same either way: **99 research, 109 in all** (main reading). The state's own rows alone hold 47 research (57 in all), which also clear R9 without any fold.

Slugs proposed (unchanged; none in `data/site/promised.json`, none clashes with a `src/pages/states/*/` page or a section id; no Wyoming case town, so A4 does not bind): `cheyenne`, `casper`, `laramie`, `gillette`, `jackson`, `rock-springs-green-river` (two cities, one county, one micro area, filed together in the research), `sheridan`.

Supplement rows that count, by page (30): state ST-2 line 12, 13, 14, 15, 16, 18, 19, 55, 56, 57, 58, 59, 68, 69, 70, 71; cheyenne 85, 86, 87, 89, 90; casper 103, 105, 106, 109; laramie 118; gillette 128; rock-springs-green-river 148; sheridan 158, 159; jackson none (its three rows are all `taken`). Supplement rows not counted (42): 30 `taken` or shared (ST-2 line 17, 20, 30 to 37, 79 to 84, 88, 91, 102, 104, 107, 108, 117, 127, 138 to 140, 149, 150, 160), 6 single properties (46, 47, 60, 94, 129, 130; the last four are also `taken`), 3 snippets (92, 93, 119; 93 is also `taken`), 3 borderline or not a figure (21, 22, 45). The per-id reasons are in the JSON.

## Sensitivity, markets (free research figures; each page tested as a standing page, none of the others standing)

| Page | Main | Without secondary | Without borderline | Without both | Without live-page (FRED, BLS EAG) | Without preliminary | Without approximate | Without stale (before 1 Nov 2025) | Without bare counts | Without edition year only (b) | Without live data table or overview page (EIA, NASS) | Without single-venue (park, airport, event) | Without Prop 1 | Without broker-sponsored | Without multi-state park (Yellowstone) | With unnamed-original and claim rows added |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| state (own rows) | 47 | 32 | 40 | 25 | 36 | 42 | 46 | 41 | 43 | 47 | 42 | 37 | 46 | 47 | 37 | 48 |
| cheyenne | 19 | 12 | 15 | 8 | 11 | 15 | 18 | 15 | 16 | 19 | 19 | 17 | 19 | 19 | 19 | 19 |
| casper | 12 | 8 | 10 | 6 | 7 | 10 | 12 | 12 | 10 | 11 | 12 | 11 | 12 | 12 | 12 | 13 |
| laramie | 2 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| gillette | 3 | 1 | 3 | 1 | 2 | 3 | 3 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 6 |
| jackson | 10 | 1 | 10 | 1 | 9 | 10 | 10 | 6 | 9 | 10 | 10 | 5 | 10 | 8 | 10 | 11 |
| rock-springs-green-river | 2 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| sheridan | 4 | 2 | 4 | 2 | 3 | 4 | 4 | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 |

Families: secondary (41 rows, unchanged; the supplement has none); borderline (13 rows in the main reading: the 11 BLS Economy at a Glance rows and the 2 NASS Quick Stats rows); live-page = the 18 FRED relays plus the 11 BLS Economy at a Glance rows (29; the first pre-count's text said 15 FRED relays, its tables removed 29 and so did 18 plus 11); preliminary = the 11 EAG rows (Sep 2026, preliminary); approximate = ST 73 ("up to") and MT 48 ("approximately"); stale = published before 1 Nov 2025: the first run's nine rows plus the ten DWS Employment and Payroll county and state rows (ST-2 line 16, 18, 19, 89, 90, 118, 128, 148, 158, 159); bare counts = ST 35, 132, MT 27, 30, 48, 58, 73, 112, 142, 168 and ST-2 line 14, 15; edition year only (b) = ST-2 line 109; live data table or overview page = EIA natural gas (ST-2 line 55 to 57, release date printed) and NASS Quick Stats (58, 59); single-venue = Yellowstone (ST 116 to 121, ST-2 line 68 to 71; the park spans WY, MT and ID), Grand Teton (MT 129 to 131), Jackson Hole Airport (MT 127, 128), Cheyenne Frontier Days (MT 47, 48), Casper airport (ST-2 line 109); Prop 1 = ST 62 (ballot 3 Nov 2026); broker-sponsored = MT 140, 142; multi-state park = the ten Yellowstone rows.

Borderline, counted in the main reading and listed so the sensitivity can remove them, 13 rows: ST line 23, 24, 28, 29, 30 (Wyoming Economy at a Glance); MT line 16, 17, 18, 19 (Cheyenne MSA); MT line 63, 66 (Casper MSA): "September 2026 (preliminary)", "Data extracted on October 28, 2026", no release date, CES and LAUS monthly releases (D12). New: ST-2 line 58 and 59 (NASS Quick Stats, "2025 State Agriculture Overview for Wyoming", cattle and beef cow inventory on 1 Jan 2026): the Published cell prints 28 Oct 2026, which is the page's own "Quick Stats as of" stamp and the access date, so it dates nothing (a retrieval date never dates a row); the rows are counted because the January Cattle inventory is an annual statistical release identified by its date (1 Jan 2026, I77(c)) and the title carries the 2025 edition (I77(b)), and they are listed as borderline because the page is a live overview, not a release.

Borderline and left out of the main reading (add-back column): ST-2 line 22 (5,766 continued weeks claimed, DWS Monthly Unemployment Insurance Claims Report: the page prints "September 2026" and no release date, a live page and not a listed periodic release; +1 if accepted); ST-2 line 45 (FDIC summary record, DEP 8644242: year-only dating and no unit, not a figure pagecheck reads, so it cannot be added back as it stands) and ST line 76 (first run). ST-2 line 21 (972 initial claims, same page) is not a figure pagecheck reads.

## Sensitivity, state page (seven markets folded; free research figures)

| Reading | Research figures |
| --- | --- |
| main reading (all markets folded) | 99 |
| without secondary | 58 |
| without borderline | 86 |
| without both secondary and borderline | 45 |
| without live-page (FRED, BLS EAG) | 70 |
| without preliminary | 88 |
| without approximate | 97 |
| without stale (before 1 Nov 2025) | 80 |
| without bare counts | 87 |
| without edition year only (b) | 98 |
| without live data table or overview page (EIA, NASS) | 94 |
| without single-venue (park, airport, event) | 81 |
| without Prop 1 | 98 |
| without broker-sponsored | 97 |
| without multi-state park (Yellowstone) | 89 |
| primary rows with a printed publication date only (a; no EAG, no NASS, no edition year) | 44 |
| with unnamed-original and claim rows added (6) | 105 |
| the sheet's mechanical reading | 98 |
| seven markets as pages (the state's own rows only) | 47 |
| own rows without secondary | 32 |
| rows `taken` or shared that pass every other test, ignored (rough upper bound over the main reading: state 38, cheyenne 17, casper 14, laramie 1, gillette 4, jackson 10, rock-springs 3, sheridan 5; first run 62, supplement 30) | +92 |
| snippet rows if the integrator accepted them (ST-2 line 92; 119; 93 is also `taken`) | +2 |
| borderline rows left out, if accepted (ST-2 line 22 only; ST-2 line 45 and ST line 76 are not figures) | +1 |
| register counted (free pairs on the candidate list: 26) | 10 |

## The state's harshest stack (cumulative removals, in this order)

**A. The first pre-count's family stack** (the nine steps of the first run, new rows assigned to the existing families; the first run ended at 7 research, 17 in all):

| Step | Research left | In all (plus 10 register) |
| --- | --- | --- |
| main reading | 99 | 109 |
| + without secondary | 58 | 68 |
| + without borderline | 45 | 55 |
| + without live-page (FRED, BLS EAG) | 45 | 55 |
| + without preliminary | 45 | 55 |
| + without approximate | 44 | 54 |
| + without stale (before 1 Nov 2025) | 33 | 43 |
| + without bare counts | 29 | 39 |
| + without single-venue (park, airport, event) | 18 | 28 |
| + without Prop 1, broker-sponsored, multi-state park | 18 | 28 |

**B. The full harshest stack** (the same, with two new families inserted before single-venue: rows dated by an edition year alone, and live data tables or overview pages):

| Step | Research left | In all (plus 10 register) |
| --- | --- | --- |
| main reading | 99 | 109 |
| + without secondary | 58 | 68 |
| + without borderline | 45 | 55 |
| + without live-page (FRED, BLS EAG) | 45 | 55 |
| + without preliminary | 45 | 55 |
| + without approximate | 44 | 54 |
| + without stale (before 1 Nov 2025) | 33 | 43 |
| + without bare counts | 29 | 39 |
| + without edition year only (b) | 28 | 38 |
| + without live data table or overview page (EIA, NASS) | 25 | 35 |
| + without single-venue (park, airport, event) | 15 | 25 |
| + without Prop 1, broker-sponsored, multi-state park | 15 | 25 |

Reading: the state clears 20 research and 30 in all on the main reading (99 and 109), on every single family removed (lowest single removals: secondary, 58 and 68, then stale, 80 and 90, and single-venue, 81 and 91), without secondary (58 and 68) and without secondary and borderline (45 and 55; the first run left 17 and 27 there, under the floor). On stack A it ends at **18 research, 28 in all** (was 7 and 17), under R9's 20 and 30 by two; on stack B at **15 research, 25 in all**. Both stacks stay above the floors until the single-venue step (29 research, 39 in all before it); that step takes out the 11 remaining rows of the venue family (Yellowstone, Grand Teton, Jackson Hole Airport, Frontier Days, Casper airport). The 18 rows left on stack A are BLS Business Employment Dynamics (ST 31 to 33, ST-2 line 12, 13), BLS OEWS wages and jobs for Cheyenne and Casper (MT 24, 25, 70, 71, ST-2 line 85 to 87, 103, 105, 106) and the EIA natural gas rows (ST-2 line 55 to 57); on stack B the EIA rows go and 15 remain. The decisive change from the first run is that the state no longer rests on the BLS Economy at a Glance rows, secondary relays or park counts: 44 rows carry a printed publication date and are primary and not borderline. The top-up pass of D15 for Wyoming has done what it was ordered to do; the strict-stack margin is still thin (about two research figures below 20 on stack A), but the main reading clears R9 by 79 research and 79 in all.

Sheet cross-check: the sheet's `countable` flag holds 98 rows (67 first-pass, 31 supplement); mine holds 99 (69 and 30). Supplement overrides: added ST-2 line 14 and 15 (bare counts read with the unit "jobs"); removed ST-2 line 22 (borderline, no release date), 92 and 119 (snippets, integrator). First-pass overrides stand (added ST 35, 132, MT 27, 30, 48, 58, 73, 112, 142, 168; removed ST 63, 74, 145, MT 76, 108, 109, 110, 136).

## Spot check (16 pages opened with WebFetch; no door closed, no www2.census.gov)

| Row | Source | Result |
| --- | --- | --- |
| ST-2 line 12, 13, 14, 15 | BLS Business Employment Dynamics in Wyoming, Q4 2025 (primary) | Confirmed: 4,143 jobs (1.9 percent) at opening establishments, 2,668 jobs (1.3 percent) at closing establishments, retail trade net -63 jobs (-0.2 percent), professional and business services net 157 jobs (0.7 percent); release Friday, July 31, 2026. The net changes are printed, not research arithmetic. |
| ST-2 line 16, 89, 118, 128, 159 (lines 17, 108, 149 on the page are `taken`) | DWS Employment and Payroll, First Quarter 2025 (primary, stale) | Confirmed: statewide +717 jobs (0.3%) and +$140.7 million (3.4%); Laramie +834 (1.8%), Albany +99 (0.6%), Campbell -453 (-1.8%), Sweetwater -326 (-1.6%), Sheridan +281 (2.0%), Natrona +361 (0.9%); page date August 8, 2025. |
| ST-2 line 18, 19, 90, 148, 158 | DWS Employment and Payroll, Fourth Quarter 2024 (primary, stale) | Confirmed: statewide +1,805 jobs (0.6%), +$194.8 million (4.5%); Laramie +635 (1.3%), Sweetwater -575 (-2.7%), Sheridan +224 (1.6%); page date May 9, 2025. |
| ST-2 line 55, 56, 57 | EIA, Wyoming natural gas gross withdrawals and production (primary, live data table) | Confirmed: 1,197,527 gross withdrawals 2025, 938,131 marketed 2025, 998,117 dry 2024 (million cubic feet); "Release Date: 9/30/2026"; 2025 dry production is "Not reported". |
| ST-2 line 58, 59 (borderline) | NASS State Agriculture Overview for Wyoming | Confirmed: 1,160,000 all cattle and calves and 621,000 beef cows on 1 Jan 2026. Page title "USDA/NASS 2025 State Agriculture Overview for Wyoming"; the only date is "Survey data from Quick Stats as of Oct 28, 2026" (the access date), no release date. Counted under I77(b) and (c), listed as borderline. |
| ST-2 line 68 | NPS Yellowstone release 26011 (primary) | Confirmed: 570,272 recreation visits in May 2026; release June 9, 2026. |
| ST-2 line 69, 70 | NPS Yellowstone release 26016 (primary) | Confirmed: June 903,025; January to June 1,676,678; release July 9, 2026. |
| ST-2 line 71 | NPS Yellowstone release 26019 (primary) | Confirmed: January to July 2,635,384; release August 11, 2026. The page prints July 2026 as 958,706, one more than the 958,705 the first-pass relay (ST 121) carries. |
| ST-2 line 85, 86, 87 | BLS OEWS Cheyenne, May 2025 (primary) | Confirmed: management $54.72, healthcare practitioners and technical $55.50, food preparation and serving $15.43 mean hourly wage; release Wednesday, August 5, 2026. |
| ST-2 line 103, 105, 106 | BLS OEWS Casper, May 2025 (primary) | Confirmed: installation, maintenance and repair $30.75; mobile heavy equipment mechanics location quotient 4.26; electrical power-line installers $100,820 annual mean; release August 5, 2026. |
| ST-2 line 109 | Casper/Natrona County International Airport, 2025 Annual Report (primary, edition year) | Confirmed: 103,763 total 2025 enplanements; page title "2025 Annual Report: C/NCIA Hits 10-Year Enplanement Record - Casper/Natrona County International Airport"; the page prints no date (footer 2026; the annual report file path carries 2026/02, the research cites a 7 Jan 2026 press-release listing). Dated by the edition year in the title, I77(b), as the integrator ruled. |
| ST-2 line 21, 22 (borderline, out) | DWS Monthly Unemployment Insurance Claims Report | Value confirmed (972 initial claims, 5,766 continued weeks claimed, September 2026, down from 1,052 and 7,045 in September 2025); no release or update date on the page. Row 22 left out as borderline, row 21 is not a figure. |
| ST-2 line 45 (borderline, out) | FDIC BankFind API, summary, Wyoming 2025 | Confirmed: record CB_2025_WY DEP 8644242, BRANCHES 183, NUMEMP 1205; the only date field is YEAR "2025" (index createTimestamp 2026-09-16 is metadata); no unit. Left out. |
| ST line 23, 28, 29, 30 (first pass, borderline) | BLS Wyoming Economy at a Glance | Confirmed again: nonfarm 295.5 and government 71.3 thousand, Sept 2026 (preliminary), seasonally adjusted; "extraction date October 28, 2026", no release date. |
| ST line 10 (first pass, secondary) | FRED WYPOP | Confirmed: 588.753 thousand persons, 2025, Census Bureau, last updated Mar 3, 2026. |
| MT line 26 (first pass, secondary) | FRED MEDLISPRI56021 | Confirmed: $473,975, September 2026, Realtor.com via FRED, last updated October 1, 2026. |

Tally: 16 pages opened (13 supplement pages covering all 30 counted supplement rows and the 3 borderline-or-out rows; 3 first-pass pages: 2 secondary FRED relays and 1 BLS borderline page); **confirmed 16, not on page 0, door closed 0**. The first run's 21-page spot check (secondary relays, news articles, Yellowstone, BED, OEWS) stands for the first-pass rows and was not repeated. Rows moved by what the pages showed: ST-2 line 22 and 45 (no release date; no unit), ST-2 line 58, 59 (dated only by a retrieval stamp, kept as borderline), ST-2 line 109 (no date on page, kept under I77(b)).

## Flags for the writer

1. **Name clash.** "Laramie" is the city in Albany County (the Laramie section) and also the county of Cheyenne (Laramie County, co-56021). Print "Albany County" for the Laramie section and "Laramie County" only for Cheyenne.
2. **County, not city.** Every FRED population, the NLJ net-migration rows and the new DWS Employment and Payroll rows (Laramie, Natrona, Albany, Campbell, Sweetwater, Sheridan) are county figures: label them with the county. The BLS OEWS rows are for the Cheyenne MSA (Laramie County) and the Casper MSA (Natrona County). Jackson: print Teton County, Wyoming only (the CBSA takes in Teton County, Idaho); Jackson gets no supplement row.
3. **Visit Cheyenne annual report (ST-2 line 79 to 84) is `taken` and out.** The sheet takes all six on pagecheck matches whose pages look unrelated: 2.8 million appears on /asset-classes/grocery-store/ as "2.8 million+ workers" (an NAICS 44511 industry total), $17.6 million on /asset-classes/self-storage/ as a calculated cost per property, 3,700 on the Texas gas station case as fuel gallons. These look like coincidental value matches, not the same fact. I followed the brief and counted none; the integrator may override. If all six counted Cheyenne would hold 25 research, 18 without secondary rows and 14 without secondary and borderline, so it would still fold on the I180 test. With ST-2 line 88 and 91 (also `taken`, on the hotel asset-class page and the SBA default economics note) released too it would hold 27, 20 without secondary and 16 without secondary and borderline, and the rule's "one family at a time" reading would then be arguable; I report it as folded on the sheet as it stands. The report itself prints no day-level date (edition year 2025, page footer 2026) and its visitor impact figures are attributed on the web to Dean Runyan Associates; its full HTML title carries a suffix "Tourism & Economic Impact Insights" that the research omits.
4. **Snippet rows not countable (integrator):** ST-2 line 92, 93 (Cheyenne building permit revenue; the snippet for line 93 says "second quarter" for an Oct to Dec period) and 119 (University of Wyoming, 6,284 full-time undergraduates). Print none of them. ST-2 line 46, 47 (Business Ready Community grants), 60 (Energy Dominance Fund), 94 (PRCA museum) and 129, 130 (BWXT) are single properties: cited, never counted.
5. **NASS rows (ST-2 line 58, 59):** the title in the research drops the "USDA/NASS" prefix the page prints. The page is a live Quick Stats overview; cite "as of 28 Oct 2026" only as the retrieval stamp and the inventory date (1 January 2026) as the period; the 2025 edition is in the title. If the integrator reads them as undated they leave the main reading (99 becomes 97).
6. **BED net change (ST-2 line 14, 15):** print the unit ("net loss of 63 jobs", "net gain of 157 jobs"); pagecheck reads a two- or three-digit number only with a unit from its list. The release publishes only five industry sectors; ST-2 line 12 and 13 are openings and closings, a different series from ST 31 and 32 (all gains and losses), so both pairs stand.
7. **EIA (ST-2 line 55 to 57):** the unit is million cubic feet; a rescale (1.2 trillion cubic feet) is the same fact. Print the year with each value: gross withdrawals and marketed production are 2025, dry production is 2024 (the 2025 dry value is blank on the page).
8. **Yellowstone (ST 116 to 121, ST-2 line 68 to 71)** is a park in Wyoming, Montana and Idaho; print it as the park. The July 2026 month count differs by one between NPS (958,706, ST-2 line 71's page) and the Jackson Hole News&Guide relay (958,705, ST 121): do not print both; ST-2 line 71 counts the January to July total only.
9. **Casper airport (ST-2 line 109):** the Published cell, the press-release listing (7 Jan 2026) and the report file path (2026/02) do not agree on a day; print "2025 annual report" and no day.
10. **DWS Employment and Payroll rows are stale by the first run's test** (Q4 2024 released 9 May 2025, Q1 2025 released 8 Aug 2025; the researcher found no 2026 releases): print each with its quarter pair ("Q1 2024 to Q1 2025"), never as current.
11. **ST line 10:** 588.753 is thousands; print 588,753 residents. **MT 13** (SAIPE 2024 median household income) is a different series from the register's ACS median household income for the same county.
12. **Prop 1** (ST 62, MT 136, ST 65): the ballot is 3 Nov 2026; do not print the projection as live, or leave ST 62 out. **Dates that differ inside one source:** ST 60 (23 or 25 May 2026), ST 62 (27 or 28 Oct 2026); cite the page date.
13. **Unnamed originals and claim (out of the main reading, add-back +6 to 105):** ST 63, MT 108, 109, 110, 136 and MT 76. The Visit Casper industry page (MT 78 to 82) is undated. ST line 76 and ST-2 line 45 (FDIC) are out; ST line 54 has no figure; MT line 96 is a teaser.
14. **Titles changed from the source:** the research drops the site name suffix from page titles (Casper airport, NASS prefix, Visit Cheyenne suffix, above). Under I176 the research's wording is the title, so these stand as written; ST-2 line 47's title ("GENERAL FUND REVENUES Positive") is a snippet fragment and the row is out anyway.
15. **Conflicts inside the research:** ST-2 line 32's note flags the one-unit Yellowstone July difference; MT 28, 74 (days on market) and MT 143, 144 (undated broker page whose 131 closed sales do not match its price bands) stay out. No two kept rows disagree and no two share a key.
16. **Gaps:** hotel occupancy, building permits (the only Cheyenne permit rows are snippets), airports other than Casper, broker reports, traffic counts, county assessed valuations, Jackson Hole Airport and Office of Tourism county tables (binary PDFs) remain NOT FOUND for most markets. The supplement could not find any 2026 DWS monthly or quarterly release. No door was worked around here.
