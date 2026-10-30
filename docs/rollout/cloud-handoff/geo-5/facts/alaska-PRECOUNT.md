# Alaska pre-count (GEO-5, 28 Oct 2026)

Method: ROLLOUT-1 ruling 6 with A4 and A6, read with I55 to I91, I109, I131 to I183 and the Montana precedent (I183). Fact sheet `alaska.facts.json` (212 rows: ST 99, MT 113; `taken` and `shared_geo5` trusted, everything else judged row by row against the research tables).
Dating by I77: (a) a publication, release, filing or last-update date printed in the Published cell, (b) an edition year in the title, (c) the reporting period of a periodic release. BLS Economy at a Glance and regional pages (Published cell shows a month only; the page prints only a retrieval date) are BORDERLINE but recognised periodic (BLS CES and LAUS), so they stay in the main reading and sit in the borderline column. The DOLWD/AHFC rental survey rows (live data page, no printed date, title carries the range 2010 - 2026, publisher not on the recognised list) are BORDERLINE and are NOT in the main reading.
Secondary rows (FRED relays of Census and BEA, Alaska Public Media, ADN, Alaska Business, CruiseMapper, Juneau Independent, Peninsula Clarion) stay in the main reading where the row names the original publisher and a date, and are listed so the sensitivity can remove them.
Register: `data/markets/series` read through `scripts/markets.py` lookup and formatter, each value checked against the 199 served pages by pagecheck; no null or flagged value counted; PEP series left out (the page will carry a Census Vintage 2025 population through FRED); pairs counted once when two keys hold the same value (co-02090 equals cbsa-21820, co-02110 equals cbsa-27940, co-02130 equals cbsa-28540, acs1_households equals acs1_occupied_units).
Spot check: 15 table lines (17 URLs, over 30 countable rows) fetched at their own URL (12 required): 15 of 15 confirmed, 0 not on page, 0 doors closed; two caveats on what the page prints are in the flags.

## Verdict table

Alaska has boroughs: every market is one borough, and the register county keys are `co-<FIPS>`. The register places Anchorage Municipality (02020) and Mat-Su (02170) in CBSA 11260 (Anchorage Metro), Fairbanks North Star (02090) in CBSA 21820, Juneau (02110) in micro CBSA 27940, Ketchikan Gateway (02130) in micro CBSA 28540; Kenai Peninsula (02122) and Kodiak Island (02150) are in no CBSA. Register free pairs below are distinct-value pairs with PEP excluded.

| Page | Facts | Countable (sheet) | Free research main reading (a/b/c) | Register free pairs, counted | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| anchorage (`co-02020`; `cbsa-11260` adds Mat-Su) | 44 | 18 | 15 (11/0/4) | 23 county, 20 CBSA; 10 | 25 | section (needs 21 research; 6 short) |
| mat-su (`co-02170`) | 15 | 5 | 5 (5/0/0) | 24; 10 | 15 | section |
| fairbanks (`co-02090`, `cbsa-21820`) | 20 | 6 | 5 (4/0/1) | 23 county, 21 CBSA; 10 | 15 | section |
| juneau (`co-02110`, `cbsa-27940`) | 12 | 7 | 6 (6/0/0) | 13 county, 11 CBSA; 10 | 16 | section |
| kenai-peninsula (`co-02122`) | 12 | 3 | 3 (3/0/0) | 13; 10 | 13 | section |
| ketchikan (`co-02130`, `cbsa-28540`) | 5 | 2 | 1 (1/0/0) | 14 county, 12 CBSA; 10 | 11 | section |
| kodiak (`co-02150`) | 5 | 1 | 1 (1/0/0) | 14; 10 | 11 | section |
| state, own rows only | 99 | 35 | 32 (27/0/5) | 36 (`ak`); 10 | 42 | state page |
| state with all seven markets folded | 212 | 77 | 68 (58/0/10) | 36 (`ak`) plus market keys; 10 | 78 | state page, clears R9 (20 research, 30 in all) |

The Countable (sheet) column is the sheet's own `countable` count. The main reading differs by four deletions (ST 134 rule values, ST 165 and ST 168 single project, MT 46 duplicate of MT 45) and by five borderline rental rows held out (MT 28, 30, 95, 116, 151): 77 sheet rows, minus 9, equal 68. By row: state 35 to 32, anchorage 18 to 15, fairbanks 6 to 5, juneau 7 to 6, ketchikan 2 to 1, mat-su 5 and kenai-peninsula 3 and kodiak 1 unchanged.

No market stands as a page. Anchorage, the largest, holds 15 free research figures against 21 and falls under every single reading; the other six hold 6 or fewer. Anchorage reaches 28 only if every site collision is ignored (31 with the shared GEO-5 values ignored too), which ruling 5 and I71 forbid, and its figures lean on the sources that must go: 3 secondary and 4 borderline rows.

Proposed slugs and section ids (none is promised in `data/site/promised.json`, so no folded request is made, as in Montana): `anchorage`, `mat-su`, `fairbanks`, `juneau`, `kenai-peninsula`, `ketchikan`, `kodiak`. MT headings: "Anchorage (Municipality of Anchorage)", "Matanuska-Susitna Borough (Wasilla and Palmer)", "Fairbanks North Star Borough", "Juneau (City and Borough)", "Kenai Peninsula Borough", "Ketchikan Gateway Borough", "Kodiak Island Borough". An alternative id for Mat-Su is `matanuska-susitna`. No Alaska case exists in `case-studies/` or `promised.json`, so A4 restricts no town.

## Sensitivity per market (free research figures, each family removed on its own)

| Page | Main | Without secondary | Without borderline | Without both | With the held-out rental rows | Without DOLWD borough population rows (live data page) | Without prior-period comparators | Without approximate rows (about, nearly, more than) | Without rows whose BLS page title is not printed | Harshest stack |
|---|---|---|---|---|---|---|---|---|---|---|
| anchorage | 15 | 12 | 11 | 8 | 17 | 14 | 15 | 14 | 13 | 6 |
| mat-su | 5 | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 4 |
| fairbanks | 5 | 5 | 4 | 4 | 6 | 4 | 5 | 5 | 5 | 3 |
| juneau | 6 | 4 | 6 | 4 | 7 | 5 | 5 | 6 | 6 | 3 |
| kenai-peninsula | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 2 |
| ketchikan | 1 | 1 | 1 | 1 | 2 | 0 | 1 | 1 | 1 | 0 |
| kodiak | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| state, own rows | 32 | 23 | 27 | 18 | 32 | 32 | 29 | 31 | 28 | 18 |
| state, all folded | 68 | 53 | 58 | 43 | 73 | 62 | 64 | 65 | 62 | 36 |

Counts of the removed families in the main reading: secondary 15 (state 9: ST 16, 19, 21, 61 to 64, 82, 149; anchorage 3: MT 40, 43, 45; mat-su 1: MT 74; juneau 2: MT 119, 120); borderline recognised 10 (state 5: ST 42, 43, 45, 46, 47; anchorage 4: MT 15, 17, 19, 21; fairbanks 1: MT 87); borough population rows read from the DOLWD live page 6 (MT 12, 85, 112, 131, 150, 162); prior-period comparators 4 (ST 16, 21, 64, MT 120); approximate rows 3 (ST 149, MT 49, MT 74); rows with no printed BLS title 6 (ST 43, 45, 46, 47, MT 19, 21).

Oahu rule (I180): a market that rests on secondary rows for half its count folds. Juneau holds 6, of which 2 are secondary and 2 more fall with the population and comparator readings; none of the seven comes near 21 to begin with.

## The state's harshest stack

Removals, in one stack: every secondary row, every borderline row (recognised and held-out), the six live-page borough population rows, the four prior-period comparators, the three approximate rows, and the rows with no printed BLS title.

| Reading | State page, all seven markets folded (research) | Total with 10 register |
|---|---|---|
| Main reading | 68 | 78 |
| Without secondary | 53 | 63 |
| Without borderline | 58 | 68 |
| Without secondary and borderline | 43 | 53 |
| Harshest stack | 36 | 46 |
| Harshest stack and every forecast row out (ST 72, 74, 75, 76, 77, 78, 80, 83: the Spring 2026 Revenue Forecast and the EIA forecast) | 28 | 38 |
| With the held-out rental rows | 73 | 83 |
| Site collisions ignored (every dated figure row, once per page; forbidden by ruling 5) | 135 across the eight pages | not a reading |

The state clears R9 on every reading shown: 20 research and 30 in all at READY, the lowest being 28 research and 38 in all. Its own rows alone (nothing folded in) hold 32 research (42 in all) on the main reading and 18 under the harshest stack, which is under 20 research on its own; the folds carry the harsh reading to 36. With no standing metro there is no reading with a metro taken out.

Caution on the cushion: the sheet's `taken` and `shared_geo5` fields were computed against 199 served pages and the other seven GEO-5 states' research at the freeze of the research (D11). The state's margin over 20 research is large, but 98 rows are lost to served pages (round values such as 4.3%, 20,000, 1.5 million recur on the site) and shared_geo5 grows as the other states are written; re-run the sheet before the page is frozen.

## Spot check (15 rows, URL opened, value and period looked for on the page)

| # | Row | Kind | Value looked for | Result |
|---|---|---|---|---|
| 1 | ST 19 | secondary, FRED relay | 737.270 thousand, 2025 annual | confirmed; page shows 2025 737.270 and 2024 736.537, last updated 3 Mar 2026, source U.S. Census Bureau |
| 2 | ST 61 | secondary, FRED relay | 73,634.8 million, 2025 | confirmed; last updated 30 Sep 2026, source BEA GDP by State |
| 3 | ST 64 and ST 63 | secondary, FRED relay | 56,342.4 (Q2 2025), 56,159.6 (Q2 2026) | confirmed both; last updated 30 Sep 2026, source BEA; note the page's latest quarter list also holds Q1 2026 56,340.3 |
| 4 | ST 21 | secondary, news relay | 1,163 net out-migration 2023 to 2024 | confirmed in the Peninsula Clarion article of 7 Jan 2025 (also 2,274 and Kenai 347) |
| 5 | ST 149 | secondary, news relay | nearly 460,000 July 2026 | confirmed; Alaska Public Media 12 Oct 2026, original Alaska International Airport System report |
| 6 | MT 40 | secondary, news relay | 40.5 consumer confidence | confirmed (also $481,000 Anchorage, about $474,200 Mat-Su); ADN 6 Aug 2026, report released 5 Aug 2026 by the Anchorage Economic Development Corporation, linked document "Anchorage Economic Trends" |
| 7 | MT 119 | secondary, news relay | 1,733,016 Juneau 2026 | confirmed in CruiseMapper 18 Oct 2026, credited to Juneau's tourism manager (a quoted person, not a publication) |
| 8 | MT 120 | secondary, news relay | 1,688,738 Juneau 2025 | confirmed; Juneau Independent 20 Nov 2025, credits the Docks and Harbors "The Tide Line" |
| 9 | ST 16 | secondary, news relay | 737,088 revised 2024 | confirmed ("up 1,649 people from the department's July 2024 population estimate of 737,088"); Alaska Public Media 30 Jan 2026, original Alaska Beacon by James Brooks |
| 10 | MT 15 and MT 17 | borderline (BLS Economy at a Glance) | 183.4 thousand nonfarm, 200.5 thousand labor force, Sep 2026 | values confirmed, marked preliminary; the only date on the page is "Data extracted on October 28, 2026" (a retrieval date), no release date |
| 11 | MT 28 | borderline (DOLWD rent, live page) | $1,562 / $1,746 Anchorage | values confirmed (Fairbanks $1,591, Juneau $1,623 too; 2025 Anchorage $1,474, vacancy 4.9 and 5.6); title "Alaska Rental Costs And Vacancy Rates, All Units, Selected Areas, 2010 - 2026"; the page prints no survey month or date, so "March 2026 survey" is not on this page |
| 12 | MT 12 | primary, DOLWD live page | 289,221 Anchorage | confirmed with "Last Update 07/01/2026" under "2025 Population Estimates by Borough, Census Area, and Economic Region"; the page does not print "1 July 2025" |
| 13 | ST 72, 76, 79 | primary | $75.26, 6,491.9, $87.6 billion | confirmed in the Spring 2026 Revenue Forecast; cover letter dated 13 March 2026 |
| 14 | MT 22, 23, 24, 92, 113 | primary release | 145,080; $1,579; 8,754; 35,985; 16,413 | confirmed in Table 2 of "County Employment and Wages in Alaska, First Quarter 2026", dated 4 Sep 2026 |
| 15 | ST 95, 96 and MT 49, 50 and ST 48 to 50 | primary | $54M, $83.1M; $57.5 million, 492,000 / 526,000; 30,293 / 23,914 / 6,379 | all confirmed (SBDC page "Last modified: October 14, 2026"; Visit Anchorage page cites the 5 Feb 2026 Report to the Community; BLS Business Employment Dynamics, 19 Aug 2026) |

Tally: 15 of 15 confirmed, 0 not on page, 0 doors closed. Rows fetched include 9 secondary and 3 borderline.

## Flags for the writer

1. Conflict inside the research (the owner's note): DOLWD says September 2026 jobs +0.1% year over year (ST 35, +300; taken by served pages, so it does not count) while BLS seasonally adjusted says +1.2% (ST 42, 340.7 thousand). Both may print with their own source, period and seasonal basis; neither is wrong. Do not compare them in words (I59, I60).
2. Population: DOLWD 738,737 for 1 Jul 2025 (ST 11, 26-2, 28 Jan 2026) and the Census figure relayed by FRED, 737.270 thousand for 2025 (ST 19; the research notes it differs). The page then holds a Census Vintage 2025 population, so no PEP population series may be used from the register (none is in the register_pairs). The FRED row is Census data, not a DOLWD relay: name the Census Bureau as publisher. QuickFacts was refused, so there is no Vintage 2025 borough table; borough populations are DOLWD only.
3. Anchorage air cargo: MT 45 (3.82 million tonnes, AEDC 2026 forecast via Alaska Business) and MT 46 (more than 3.85 million metric tons, Alaska International Airport System via Alaska Public Media) are the same series and period at different values. One counts (MT 45); print either with its source, not both as separate figures.
4. Fairbanks vacancy: DOLWD 10.1% (March 2026 survey, MT 96, taken) and the borough's quarterly 12.2% (March 2025, via KUAC, MT 97, taken) are different surveys and periods.
5. Anchorage unemployment: DOLWD 3.4% (MT 13) and BLS 3.6% (MT 14), both taken by served pages and so not counted; the research itself flags the difference.
6. Titles changed from the source: ST 16 lowercase with the comma dropped ("alaska population rises slightly but more people continue to move out than move in"; the page title is "Alaska population rises slightly, but more people continue to move out than move in" and the research took it from a search listing); the Anchorage occupational wage release (MT 25, 26) and probably the Fairbanks one (MT 91) had a dash in the source title replaced by a comma; ST 45, 46, 47 and MT 18 to 21 carry a placeholder in place of a title ("title not printed in the fetch"): per I176 these cannot be cited with an invented title, so those six countable rows (ST 43, 45, 46, 47, MT 19, 21) are weak.
7. BLS Economy at a Glance rows: the Published cell "2026-10" is inferred from the data extraction date; the page prints only "Data extracted on: October 28, 2026". They count as periodic (I77(c)) in the main reading and fall in the borderline column; every value is marked preliminary.
8. DOLWD rental rows: the research cites a "March 2026 survey" from a sister page; the cited page prints only years. They are held out of the main reading. Mat-Su 3.5%, Kenai 5.8%, Kodiak 7.8% and Ketchikan 8.4% vacancy values are taken by served pages anyway.
9. Dropped after review: ST 134 (Disaster Unemployment Assistance weekly range and 27 weeks: benefit rule values), ST 165 and ST 168 (Alaska LNG cost and investment: single project, I64), MT 46 (duplicate of MT 45). ST 79 (Permanent Fund value, $87.6 billion) is one fund's balance inside the state forecast document; it is counted as a state fiscal figure, but would go if the integrator reads it as a single entity.
10. Single-project and single-property rows not counted (market flag false or note says single-project): MT 53, 54, 55, 76, 77, 102, 142; ST 52, 84, 164, 166, 167, 169, 172 (the last group are also taken). Rule values not counted: MT 37, 38, 98, ST 106.
11. Undated rows (I86): the AHFC loan tables (ST 97, 98, MT 32, 33, 71, 72, 100, 101, 118, 139, 140, 153, 166), the foreclosure tables (ST 155, MT 34, 73) and the statewide housing page (ST 151 to 154) carry no publication date and their numbers must not be printed (unless the writer finds the research ties them to an edition year).
12. Context-unit rows the sheet does not read as figures (ST 41 +400 jobs, MT 35 about 400 units, MT 36 330 units, MT 132 +287 people, MT 141 +347 people) were tested with their unit; every one is already printed on a served page, so none counts.
13. MT 66 spells the borough "Mantanuska-Susitna" as the source does. MT 50 is Southcentral cruise capacity (a regional figure, not Anchorage alone) and MT 123 (Southeast tourism share) is regional. ST 63's note says "same series as row 39" and MT 45's note says "row 35": the row numbers in the notes do not match the table.
14. Anchorage's BLS metro rows (MT 15 to 21) cover CBSA 11260, which includes Mat-Su; the register's `cbsa-11260` reading also includes Mat-Su while the research sections are separate. In the state page use `co-02020` for the Anchorage section's register rows, or print the roster. The recommended ten register pairs mix state and market keys; each is free and not equal to any research value.
15. Register pairs recommended (also in the json): ak acs5 median household income $92,788; ak BEA per capita income $76,234; ak acs1 median home value $376,500; ak SBA 7(a) loans 919; ak SBA 504 volume $104.4 million; cbsa-11260 acs5 median household income $100,505; co-02090 acs5 median home value $298,200; co-02110 acs5 per capita income $54,089; cbsa-28540 acs5 median gross rent $1,505; co-02122 acs5 median household income $80,538. The register has 36 free distinct values at `ak` alone.
16. Doors the research reports closed (not worked around): Census QuickFacts, kpedd.org, matsugov.us, commerce.alaska.gov, Alaska Beacon (403), BLS Juneau metro page (404). No Juneau, Ketchikan or Kodiak unemployment, no broker, hotel or permit series exist in the research.
