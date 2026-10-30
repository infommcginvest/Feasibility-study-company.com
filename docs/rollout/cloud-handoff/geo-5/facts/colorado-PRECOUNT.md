# Colorado pre-count (GEO-5, Sonnet reader, 28 Oct 2026)

Method (5 lines).
1. Rules: ROLLOUT-1 rulings 4 to 6 as amended by A4 and A6, integrator rulings I55, I59, I60, I62, I64, I66, I69, I71, I77, I82, I86, I87, I91, I109, I131, I142, I154, I176, I180 and I183 with the Montana pre-count as the model. A market stands only at 21 free dated research figures, research plus at most 10 register at 30, and 20 research left after each secondary or borderline family is removed; a new state needs 20 research and 30 in all (R9).
2. Inputs read to the last line: ST-COLORADO (89 rows), MT-COLORADO (184 rows), the 273-fact sheet `colorado.facts.json` (tree `wt-rollout-geo-5`, pagecheck unchanged, served pages plus their sources lists, I71). `taken` and `shared_geo5` trusted; I re-checked the main set against all eight current fact sheets and found no further shared value. Within the file a value counts once.
3. Dating (I77): (a) = a full publication or release date in the Published cell, (b) = edition year in the title with no date (none here), (c) = month-only Published cell on a live BLS area page. Every (c) row is also BORDERLINE (live data page, recognised periodic BLS CES/LAUS release, so it stays in the main reading and is listed apart).
4. Register: each series read through `scripts/markets.py` for the state key `co` and each market's CBSA key (county key `co-08xxx` as the alternative reading), checked against the served site; flagged and null values excluded; PEP population never used (ST line 11 is the Vintage 2025 population). Free pairs are counted, at most 10 enter any total.
5. Spot check: 17 rows opened with WebFetch (12 required); none closed a door, none failed. Results below.

## Verdict table

Free research = my main reading (a/b/c). "Sheet" = the fact sheet's `countable`. Register = free pairs on the market's CBSA key (county key in brackets), 10 counted.

| Page | Facts | Sheet countable | Free research main reading (a/b/c) | Register | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| denver | 70 | 38 | 39 (38/0/1) | 16 free (18), 10 counted | 49 | PAGE (/states/colorado/denver/) |
| colorado-springs | 30 | 17 | 17 (16/0/1) | 15 free (17), 10 counted | 27 | folds, 4 short of 21 and 3 short of 30 |
| fort-collins | 19 | 11 | 11 (10/0/1) | 15 free (17), 10 counted | 21 | folds |
| greeley | 13 | 8 | 8 (6/0/2) | 15 free (17), 10 counted | 18 | folds |
| boulder | 16 | 7 | 7 (6/0/1) | 16 free (17), 10 counted | 17 | folds |
| pueblo | 10 | 6 | 6 (5/0/1) | 13 free (15), 10 counted | 16 | folds |
| grand-junction | 10 | 5 | 6 (5/0/1) | 16 free (18), 10 counted | 16 | folds |
| mountain-resort-counties | 16 | 7 | 8 (8/0/0) | no CBSA: four counties in four micropolitan CBSAs; county keys 13, 13, 11, 13 free | 18 | folds |
| state (own rows only) | 89 | 32 | 26 (23/0/3) | 20 free, 10 counted | 36 | page |
| state, every market folded | 273 | 131 | 128 (117/0/11) | 10 counted | 138 | page (R9 met) |
| state, Denver standing and the other seven folded | 203 | 93 | 89 (79/0/10) | 10 counted | 99 | page (R9 met) |

Arithmetic of the overrides: the sheet's 131 countable became 128. Taken out: ST lines 17, 37, 126, 127, 139, 156 and MT lines 243 (and MT 200, 217, 238, 239 once read with their unit, see below). Put in: MT line 44 (denver), MT 219 (grand-junction), MT 236 and 237 (mountain-resort-counties).

Slugs (no clash with any `src/pages/states` entry, none promised in `data/site/promised.json`; Colorado has no served page, no case and no case town, so A4 restricts nothing): denver, colorado-springs, fort-collins (heading "Fort Collins-Loveland (Larimer County) and Northern Colorado"), boulder, greeley, pueblo, grand-junction, mountain-resort-counties. mountain-resort-counties is the MT file's last section, treated as a market section.

Reading of the verdicts. Denver holds 39, 18 over the 21 floor, and never falls under 26 on any removal or on all of them together, so it stands. Colorado Springs, the other market tested hard, holds 17 on the sheet and 17 on my reading (no override adds a row): 13 of its 30 facts are taken, shared, not figures or an uncountable class, and it would need four more. It folds. No other market is within ten of the floor.

## Sensitivity, markets (free research figures; each column removes one family, none of the others)

Families: secondary = Kind secondary (FRED relays of Realtor.com, Census permits and BEA metro GDP); borderline = the BLS area-page rows (ids in the JSON); Matthews = Matthews Real Estate Investment Services reports (their charts credit CoStar, spot check 11); GDP = the 2023 metro GDP rows, FRED series labelled discontinued; approx = values led by about, more than, just under, roughly; preliminary = rows the research marks preliminary.

| Page | Verdict | Without secondary | Without borderline | Without both | Without Matthews | Without discontinued GDP | Without approximate | Without preliminary | Harshest stack |
|---|---|---|---|---|---|---|---|---|---|
| denver | 39 | 34 | 38 | 33 | 34 | 38 | 38 | 37 | 26 |
| colorado-springs | 17 | 13 | 16 | 12 | 15 | 16 | 17 | 16 | 10 |
| fort-collins | 11 | 8 | 10 | 7 | 9 (7 without the Northern Colorado region rows) | 10 | 11 | 10 | 5 |
| greeley | 8 | 5 | 6 | 3 | 8 | 7 | 8 | 6 | 3 |
| boulder | 7 | 4 | 6 | 3 | 7 | 6 | 7 | 6 | 3 |
| pueblo | 6 | 4 | 5 | 3 | 6 | 5 | 6 | 5 | 3 |
| grand-junction | 6 | 4 | 5 | 3 | 6 | 5 | 6 | 5 | 3 |
| mountain-resort-counties | 8 | 6 | 8 | 6 | 8 | 8 | 8 | 8 | 6 |

Harshest stack = secondary, borderline, Matthews, discontinued GDP, approximate, preliminary, and the ambiguous rows (Cherry Creek submarket MT 49; DEN airport and the airport relay, state rows ST 164 and 165) removed together.

Denver's secondary rows are MT 28, 29, 33, 34, 80 (permits, listings, GDP); its Matthews rows are MT 71 to 75; its borderline row is MT 13. Oahu rule (I180): after removing each family on its own Denver holds 33 to 38, so no family carries half of it (the secondary family is 5 of 39). Colorado Springs fails the rule too, but it already fails the floor.

Denver rows that sit on the state sheet: ST 155 (Denver metro travel spending), and if DEN is read as a Denver asset ST 164 and 165. If the integrator moves them to Denver (ruling 4), Denver is 40 to 42 and the state falls by the same.

## State page

| Reading | Research figures | Total with 10 register |
|---|---|---|
| Own rows only (nothing folded) | 26 (23/0/3) | 36 |
| Every market folded (Denver included) | 128 (117/0/11) | 138 |
| Denver standing, seven markets folded | 89 (79/0/10) | 99 |

Sensitivity of the state page, free research figures:

| Reading | Own rows | All markets folded | Denver standing, seven folded |
|---|---|---|---|
| verdict | 26 | 128 | 89 |
| without secondary | 6 | 84 | 50 |
| without borderline | 23 | 117 | 79 |
| without both | 3 | 73 | 40 |
| without Matthews | 26 | 119 | 85 |
| without discontinued GDP | 26 | 121 | 83 |
| without FRED relays | 19 | 97 | 63 |
| without approximate | 24 | 125 | 87 |
| without preliminary | 21 | 114 | 77 |
| without Northern Colorado region rows | 26 | 124 | 85 |
| without airport and submarket rows | 24 | 125 | 87 |
| harshest stack (all seven removals above) | 0 | 59 | 33 |

The state's harshest stack: remove secondary, borderline, Matthews, discontinued GDP, approximate, preliminary and the airport and submarket rows. Own rows fall to 0 (20 of the 26 are secondary, 3 more borderline, the last 3 are QCEW rows marked preliminary and one approximate FEMA figure). The page clears R9 only through its folded markets: all folded 59 research and 69 in all at the harshest, Denver standing 33 research and 43 in all. Both clear 20 and 30. The own-rows-only page (26 and 36 at the verdict) would sit over the floors only on the strict reading and would fall to 6 without secondary rows, so the sections are what the Colorado page rests on. State rows depend heavily on relays: all the tourism, DEN, budget, population and FRED rows are secondary.

## Spot check (17 rows opened, 12 required; secondary and borderline weighted)

| # | Row | Kind | URL host | Result |
|---|---|---|---|---|
| 1 | MT 13 Denver nonfarm 1,645.7 thousand, Sep 2026 | borderline | bls.gov area page | confirmed; the page prints no release date, only "Oct 2026" in the release list (supports the borderline call) |
| 2 | MT 18 Denver County employment 551,034 and MT 19 $2,354 | primary | bls.gov county release | confirmed; release date 4 Sep 2026; Pueblo 60,303 and $1,120 and Summit 23,889 also confirmed |
| 3 | MT 130, 131 Larimer 167,827 and $1,627 (up 11.5%); Jefferson, Boulder, El Paso | primary | bls.gov county release | confirmed, including the 11.5% outlier |
| 4 | MT 33 Denver median listing price $569,900, Sep 2026 | secondary | fred.stlouisfed.org | confirmed; Realtor.com source, updated 1 Oct 2026 |
| 5 | MT 80 Denver GDP 311,876.352, 2023 | secondary | fred.stlouisfed.org | confirmed; title carries DISCONTINUED, last updated 4 Dec 2024 (the page also lists a next release of 2 Dec 2026) |
| 6 | MT 28 Denver County permits 4,727, 2025 | secondary | fred.stlouisfed.org | confirmed; Census Bureau, updated 28 May 2026 |
| 7 | ST 45 Colorado GDP 609,250.7, Q2 2026 | secondary | fred.stlouisfed.org | confirmed; updated 30 Sep 2026 |
| 8 | ST 150 Colorado travel spending $29.2 billion | secondary | kjct8.com | confirmed; page credits Colorado Tourism Office, Dean Runyan and Longwoods; updated 29 Jul 2026 |
| 9 | ST 164, 165 DEN 82,427,962 and 4,867,484 passengers | secondary | aviationindustry-news.com | values confirmed, dated 29 Jan 2026; the page names no original source (the row names the DEN release of 28 Jan) |
| 10 | MT 37 metro Denver office net absorption -161,000 sq. ft. | primary | cbre.com | confirmed; printed as the words "negative 161,000", report dated 9 Oct 2026; 28.8% and 461,000 also confirmed |
| 11 | MT 76, 78 Denver 37.6 million visitors and 73,200 jobs | primary | visitdenver.com | confirmed; 21 May 2026 |
| 12 | MT 111, 112 Colorado Springs $194/SF and 391,462 SF | primary (Matthews) | matthews.com | confirmed; 27 Aug 2026; charts credited to CoStar Group |
| 13 | ST 67 LCS general fund revenue down $304 million | secondary | vaildaily.com | confirmed; article 21 Dec 2025; the article puts it as a decrease by the end of FY2025-26 against September |
| 14 | ST 28, 29, 30 Colorado employed 3,047.4, unemployed 131.9, nonfarm 2,973.8 thousand | borderline | bls.gov regional page | confirmed (preliminary, Sep 2026); no release date on the page |
| 15 | ST 122 FEMA more than $784,000 | primary | fema.gov press release | confirmed; 28 Sep 2026, R8-26-NR-032 |
| 16 | ST 11, 12, 13, 14, 15, 16 DOLA relay | secondary | content.govdelivery.com | confirmed, 27 Jan 2026; migration printed as "12,100 more left than arrived" and "15,356 more arrived", no signs; total net migration 3,256 and growth 0.4% confirmed |
| 17 | MT 99, 100, 101 Colorado Springs industrial $10.74, 357,000, 290,000 | primary | cbre.com | confirmed; 11 Aug 2026 |

Tally: 17 confirmed, 0 not on page, 0 door closed. Not opened: the FHFA, Realtor.com state FRED rows (ST 54, 55, 57), the Visit Colorado Springs release, Cushman and Savills pages (all taken or low weight).

## Rows judged out (beyond the sheet) and rows judged in

Out: ST 17 (same fact as ST 11, I82); ST 37 (rule value, the state minimum wage); ST 126 (one project, I64); ST 137 and 139 (one firm, Colorado Enterprise Fund, I64); ST 127 (KUNC damage estimate with no original publisher named); ST 156 (skier visits, the research says the source is not named); MT 243 (rule values, proposed AMI limits); MT 200, 217, 238, 239 (permit counts for Pueblo, Mesa, Routt, Pitkin: read with their unit, "226 units", "810 units", "218 units", "36 units", they are taken by served pages).
In: MT 44 (the sheet's market flag came from the Note about the TIAA move-out; the downtown total -483,000 is a market figure); MT 219 (988 listings), 236 (318 units) and 237 (223 units) (bare numbers on the sheet, untaken when read with their unit, as the Montana pre-count read permits and jobs).
Not figures to pagecheck and so not counted: median days on market (ST 56, MT 35, 97, 160; "N days" is never read) and the CPI index levels (MT 15, 16; 353.428 and 415.540 have the statute shape). Date, bill and deadline rows (ST 79 to 95, 106, 121, 142, 166) are rule or code values, not counted.
Doubtful rows kept in the main reading and shown in the harshest stack: ST 164 and 165 (an airport is one facility, I64, but the figure is traffic, not an attribute); MT 49 (Cherry Creek, a submarket of four projects).

## Flags for the writer

1. Source titles. The researcher replaced em dashes in titles with commas, so every title may differ from the document's own and I176 says a source title is the research's wording. Likely cases: "County Employment and Wages in Colorado, First Quarter 2026" (every QCEW row), "Occupational Employment and Wages in <area>, May 2025", "Consumer Price Index, Denver-Aurora-Lakewood area, September 2026", "State Employment and Unemployment, September 2026 (Table 1)", the CBRE "Figures" titles and the Cushman title (the research notes the suffix). None can be restored from the research, so the writer uses the title as the file gives it or drops the source. Titles ending "(area page)" (MT lines 11 to 14, 88 to 90, 125 to 128, 151 to 153, 174 to 178, 194 to 196, 211 to 213) are the researcher's descriptive names, not printed titles: do not cite them as titles. ST 28 to 30 ("BLS Mountain-Plains Information Office: Colorado") may be descriptive too. "Division of Housing Updates - August 26, 2026" keeps its printed hyphen.
2. ST 62 (FEMA DR-4944, declared 1 Sep 2026) rests on a search-result snippet; fema.gov returned 403. The row is not a counted figure, but the declaration date and incident period must not be printed as facts from it (I69).
3. BLS area pages and the BLS regional state page print no release date, only "Oct 2026". They are the borderline family (11 rows). If the integrator reads month grain as undated, Denver falls to 38, the state (all folded) to 117.
4. Discontinued GDP. The 2023 metro GDP rows (MT 80, 117, 143, 166, 186, 203, 220) are FRED series labelled DISCONTINUED, dated 4 Dec 2024, three years old; a newer BEA metro series may exist. They count (dated, original BEA named) and are the stale family in the sensitivity.
5. Broker rows. The Matthews reports credit CoStar for their charts (spot check 12); CBRE and Cushman are first-party. Matthews and CBRE report different universes (Colorado Springs industrial vacancy 4.4% CBRE against 6.0% Matthews, row note). Do not set them side by side as one series.
6. Conflicts inside the research. (a) Denver office: CBRE vacancy 28.8% and net absorption -161,000 (MT 26, 27), Cushman 27.1% and -395,100 (MT 36, 38), Savills leasing 2.8 million (MT 40) use three definitions (most are taken by the site); print one publisher's series per statement. (b) Denver tourism spending $10.5 billion (Visit Denver, Denver) against ST 155's $14.2 billion for the "Denver metro": different geographies, no definition in the research, and the Visit Denver page itself also prints $10.6 billion and nearly $8.8 billion beside $10.5 and $8.7 (MT 67, 69). (c) ST lines 14, 15, 16 are consistent (-12,100 + 15,356 = 3,256) but the sum is the publisher's, not ours. (d) Fort Collins: the CBRE Northern Colorado office and industrial rows (MT 135 to 140) and the Matthews NoCo rows (MT 140 to 142) cover Fort Collins, Loveland and Greeley submarkets; the Greeley section must not print them, and the Fort Collins section labels them Northern Colorado.
7. Geography. The Denver register key (cbsa-19740, ten counties: Adams, Arapahoe, Broomfield, Clear Creek, Denver, Douglas, Elbert, Gilpin, Jefferson, Park) is wider than the five counties the research measures; Colorado Springs adds Teller to El Paso. FRED labels the Denver CBSA "Denver-Aurora-Lakewood", BLS "Denver-Aurora-Centennial": use the register's name and label county rows with their county.
8. Ruling 4 and 5. If Denver stands, the state page must not repeat any figure the Denver page counts; the state's cards for the folded sections cite no value from the section. The 10 register pairs on the state page use key `co`; the Denver page uses cbsa-19740. No PEP population on either page (ST 11 is the Vintage 2025 level). The Denver CBSA has no SBA or BEA register value (unavailable), so its 10 are ACS, CBP establishments and employment.
9. Shared values. `shared_geo5` grows as states arrive; this count was re-checked against all eight current fact sheets and found no further shared value in the main set. Re-run it before the page is frozen.
10. Permits are read with the unit "units" and listings with "listings" (pagecheck reads a bare 2 or 3 digit number only before one of its unit words). A writer who prints "226 housing units" would change what pagecheck sees; use the unit words.
