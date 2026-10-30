# GEO-5 t7 freeze 1, attacker A (figures, dates, floors, research hygiene): /states/district-of-columbia/

Reviewed (cloud session, paths per CLOUD-PATHS.md): frozen copy `scratchpad/copies/f1-district-of-columbia/` (source `src/pages/states/district-of-columbia.html`, sha256 480d775e...28bef6f5, byte equal to the handoff draft `pages/district-of-columbia.html` by cmp; rendered `states/district-of-columbia/index.html`, sha256 c5ff00e2...1975a8d0; both equal to `FREEZE-district-of-columbia-f1.txt`). Research `ST-DISTRICT-OF-COLUMBIA.md` (sha256 57621a30...) and `MT-DISTRICT-OF-COLUMBIA.md` (sha256 9f440183...), both equal to `RESEARCH-SHA256.txt`; cited below as ST line n and MT line n (file lines, as the fact sheet and assignment cite them). Also `facts/district-of-columbia.facts.json`, `facts/district-of-columbia-PRECOUNT.md`, `assign/district-of-columbia.json`, `GATES-f1-district-of-columbia.txt` and `-g13.txt`, `data/markets/series/*.json` and `data/regulatory/sba.json` in the copy. No metro page stands (all five markets folded as sections).

Pagecheck rerun from inside the copy (`python3 -B scripts/qa/pagecheck.py --root . --stage ready --new /states/district-of-columbia/ --figures /states/district-of-columbia/`): words 6,126; counted 56 (research 48, register 8/8); overlap 0.72% (/states/virginia/). Equal to gate 3. The 48 research figures are the pre-count's 46 rows plus Matthews' own change rates 0.72% and 44.5% (MT lines 100 and 104, What cells); the WJLA row counts once (375,800; 312,500 collides by value with /states/south-carolina/). Register owner-occupied 134,683 and renter-occupied 189,808 are printed but do not count (repeat test).

## Fetches: none succeeded (closed door, recorded, not worked around)

The brief asks for at least 12 source URLs opened with WebFetch. Three were tried and each was refused by this cloud session's network policy before any request reached the source (WebFetch: "getaddrinfo ENOTFOUND ... outside the session's allowed network domains"):
- https://does.dc.gov/release/district-columbia-unemployment-rate-57-percent-august, .../district-columbia-unemployment-rate-56-percent-september, https://does.dc.gov/node/1798846: NOT FETCHED (host does.dc.gov not allowed in this session).
- https://ora-cfo.dc.gov/node/1815066: NOT FETCHED (host not allowed).
- https://www.bls.gov/regions/mid-atlantic/news-release/countyemploymentandwages_districtofcolumbia.htm: NOT FETCHED (host not allowed).
The tool's instruction after a second refused host is to stop trying further sites, so no other source was attempted, no search snippet, cache, mirror or other route was used in place of a refused page, and www2.census.gov was not touched. The fetch floor of this review is therefore NOT MET. Every "confirmed" below rests on the research row and, where it exists, the pre-count's own WebFetch spot check of 18 URLs on the Mac (PRECOUNT "Spot check"). Rows that neither I nor the pre-count opened are marked "row only". To close the gap, a session with does.dc.gov, ora-cfo.dc.gov, www.bls.gov, cushmanwakefield.com, cbre.com, washington.org, commercialobserver.com, hoodline.com, wjla.com, matthews.com, yardimatrix.com, strategicplan.nomabid.org, downtowndc.org, dmped.dc.gov, otr.cfo.dc.gov, cfo.dc.gov and api.census.gov allowed should open them; the findings below that need a fetch say so.

## Findings

### A1-1 MAJOR-FACTUAL: one DOES series printed from three releases on both sides of a revision (ruling 10)
- Page: #economy paragraph 3 (source line 328) and the table "Jobs located in the District, by release" (lines 335 and 338).
- Text: "Its release for August 2025 put the count at 751,000 [^14]. The release for June 2026 gave 721,800 [^15], and the release for August 2026 gave 713,600 [^16]. A later release can restate a month, so a study quotes each count with the release it came from ..." and the table rows "DOES monthly release | 751,000 | August 2025 | [^14]", "DOES monthly release | 721,800 | June 2026 | [^15]", "DOES monthly release | 713,600 | August 2026 | [^16]".
- Reproduction: ST lines 35, 32 and 29 give the three values from three DOES releases (2025-09-19, 2026-07-21, 2026-09-18), all one series: DOES's count of jobs located in the District. The research records the vintage break itself: ST line 34 notes that DOES's September 2025 release "reflects 2024 benchmark", so the August 2025 reading (an earlier release) is on the 2024 benchmark, and MT line 88 notes that DOES's October 2026 release has the "2025 annual benchmark applied". The page also cites the newest DOES District release (source 18, October 20, 2026) for sector and resident figures; its total (718,700, ST line 22) is not printed because /states/california/ takes it (facts.json `taken`), and ST line 22's note ("release prints +4,600 from August") implies that release restated August as well (my inference from the note; not fetched). The page says so in its own words ("A later release can restate a month"). ROLLOUT-1 ruling 10: "Never put two vintages of one series on one page"; GEO-5 D20 applied it to two population vintages of different years, and t5 attacker A1-1 to DOLWD migration of different years from two vintages. The same reading reaches a series whose August 2025 value is pre-benchmark and whose 2026 values are later readings.
- Stricter reading, for the verifier and the integrator: 739,200 (ORA's reading of BLS's preliminary November 2025 CES count, ST line 41, hero, #economy, table) is a pre-benchmark reading of the BLS District nonfarm series whose current reading the page prints as 719.9 thousand (ST line 37). D20 exempts different publishers' series; ORA relays BLS's own figure, so the exemption is doubtful. Deleting it rewrites the hero's lead fact, which is beyond a smallest fix, so I do not count it in my total; the integrator rules.
- Fix (deletion, one capital): line 328, replace "Its release for August 2025 put the count at 751,000 [^14]. The release for June 2026 gave 721,800 [^15], and the release for August 2026 gave 713,600 [^16]." with "The release for August 2026 gave 713,600 [^16]."; delete the two table rows for 751,000 and 721,800; sources 14 and 15 are then cited nowhere (each is cited only in that sentence and its row): drop both and renumber 16 to 37 as 14 to 35. Count: -2 (751,000; 721,800).

### A1-2 MAJOR-FACTUAL: 811 homes is the unit count of two named properties, counted as a market figure (I64, I66)
- Page: #conversions paragraph 1 (line 380) and FAQ 3 (line 73).
- Text: "two further projects, at 2121 Virginia Avenue NW in Foggy Bottom and 899 Maine Avenue SW near The Wharf, were conditionally awarded abatements for 811 homes, as Hoodline relayed the Mayor's release [^9,8]." and "two more projects, in Foggy Bottom and near The Wharf, were conditionally awarded abatements for 811 homes [^9]."
- Reproduction: ST line 100 measures "Homes in the two further conversions conditionally awarded abatements (2121 Virginia Avenue NW and 899 Maine Avenue SW)"; its note gives the two buildings' own counts (300 and 511, MT lines 27 and 59, both single-property and taken elsewhere). The pre-count spot check confirms Hoodline prints 811 as one total. A total for two named buildings describes those buildings (I64: unit count of a named site; I66 keeps counting only a total "over a portfolio or a market (many properties)"). The ten-conversion total 2,563 (ST line 97) is a program total and stays counted.
- Fix: wrap both occurrences: "for <span data-fsc-nocount>811</span> homes". Count: -1.

### A1-3 MAJOR-FACTUAL: the register row says "household" income for B19313, which is not household income
- Page: register table, line 355.
- Text: "Aggregate household income (B19313) | $52,696.6 million | 2020 to 2024, five-year | [^19]".
- Reproduction: `data/markets/series/acs5_aggregate_income.json` gives dc 52,696,645,000, fetched as B19313_001 (`scripts/markets_census.py` line 98; `data/markets/sources.json` query strings). B19313 is the aggregate income of persons that ACS divides by total population to get per capita income (B19301); aggregate household income is a different table (B19025, universe households). The register's own values show it: 52,696,645,000 / 77,348 (acs5_per_capita_income, dc) = 681,292.9, against acs5_pop dc 681,294, so the printed value is per capita income times population, not a household total. The label comes from the register script's label (`markets_census.py` line 260) and is also on /states/south-dakota/ and /states/virginia/ (only those three sources print it). Census table metadata was not fetched (closed door); the arithmetic above is from the register alone.
- Fix (deletion): "Aggregate household income (B19313)" becomes "Aggregate income (B19313)". Count unchanged. Integrator item: the same label on the two landed GEO-5 pages and in the register script.

### A1-4 MAJOR-FACTUAL: "CBRE's page does not print a vacancy level" is contradicted by the research row for the same page
- Page: #office paragraph 1, line 372.
- Text: "The two firms draw their inventories differently and measure absorption in their own ways, and CBRE's page does not print a vacancy level, so the readings do not form a single series and cannot be netted against each other."
- Reproduction: ST line 122 records, from the same CBRE URL and date as the page's source 7, "Prime (trophy) vacancy | 8.3% | Q3 2026"; ST line 120's note says the page "prints that overall vacancy fell 40 bps; level not stated". The page prints a prime vacancy level and an overall change; only the overall level is missing. (8.3% is taken by other pages, which is why it is not printed; that does not make the sentence true.) Not fetched.
- Fix (deletion): delete ", and CBRE's page does not print a vacancy level". Count unchanged.

### A1-5 MINOR: comparisons in words without the values (I59, I60(b))
- (a) #economy h2 (line 324): "Fewer federal jobs and fewer jobs in all: the District's payroll from August 2025 to September 2026." No District federal job count for August 2025 or September 2026 is on the page (169,000 is November 2025), and "fewer jobs in all" compares values from different series and releases (A1-1). Fix: data-h2 becomes "The District's payroll from August 2025 to September 2026." (deletion, one capital).
- (b) #economy paragraph 2 (line 327): "The same analysis ties the sharpest federal losses to the Deferred Resignation Program ...". ST lines 43 and 166 record the September to October 2025 loss tied to the program; neither records "sharpest" (a ranking across months). Low confidence: ORA was not fetchable. Fix: delete the sentence; the events table row "September to October 2025 ... [^1]" keeps the fact. Count unchanged.

### A1-6 MINOR: an inference across figures that no source states
- Page: #downtown-dc paragraph 1, line 459.
- Text: "Taken together with the citywide figures in the office section, the two numbers are consistent with tenants leaving older buildings in the core while the newest buildings east of it gain occupancy."
- Reproduction: MT lines 9 and 10 give the CBD's -42,500 sf "driven by Class B move-outs" and the East End's 70,400 sf with "Class A +46,000 sf". No row speaks of building age or "the newest buildings"; the conclusion joins those values with citywide figures (I60(b)).
- Fix: delete the sentence. Count unchanged.

### A1-7 MINOR: Matthews and Yardi read past what the rows carry
- (a) #washington-metro, line 502: "7,698 units delivered over the trailing twelve months, a pace the report shows slowing from 2024". MT line 102: "Trailing twelve-month deliveries, down 48.4%; 14,624 in 2024". The report's 48.4% is not against 2024 (7,698 against 14,624 is a fall of about 47.4%), so "slowing from 2024" is the page's own comparison with a value it does not print (I60(b)). Fix: delete ", a pace the report shows slowing from 2024".
- (b) line 503: "uses them for the direction of the regional market, deliveries slowing and sales volume returning, and builds". Same comparison, plus "returning" for a 44.5% rise. Fix: delete ", deliveries slowing and sales volume returning".
- (c) line 503: "Neither describes the District alone." MT lines 99 to 105 say Matthews does not state its geography (the "metro scale" is the researcher's inference), and the page itself says so two sentences earlier. Fix: delete the sentence.
- (d) #washington-metro paragraph 3 and FAQ 1: "375,800 to 312,500". The pre-count's fetch of WJLA reads "from about 375,800 jobs to 312,500". Verbatim restoration would add "about"; I leave the choice to the verifier (no count change either way).
- Count unchanged.

### A1-8 MINOR: the division's federal figure is the pre-benchmark reading the closing band tells a study not to use
- Page: FAQ 1 and #washington-metro paragraph 2 (line 498): "Its August release gave the twelve-month change in federal jobs in the division, August 2025 to August 2026, as -25,800 [^5]." CTA p (line 95): "A study commissioned now is written to the October releases rather than to a summer count a later release may have restated".
- Reproduction: MT line 91 (-25,800, release of 2026-09-30) and MT line 89 (-26,300, September 2025 to September 2026, release of 2026-10-28, which MT line 88 says has the "2025 annual benchmark applied"). The newer value is taken by /states/minnesota/ (facts.json), so the page prints the August reading, a summer count that the benchmarked October release restates. One value per series is printed (no ruling 10 breach); the page's advice contradicts its own figure.
- Fix (deletion): CTA p, delete " rather than to a summer count a later release may have restated" (leaving "is written to the October releases, and it says whether ..."). Alternative: delete -25,800 in both places (count -1), which would remove the division leg of the hero's three geographies. I recommend the CTA deletion.

### A1-9 MINOR: two events-table rows state more than the research dates
- (a) Line 432: "January 23, 2026 | Housing in Downtown awards announced; construction of The Geneva conversion launched | [^9,8]". January 23 is the publication date of both relays (ST lines 96 to 100); the rows date the events only as "announced Jan 2026" and "construction launched Jan 2026", and WTOP's article on the same conversions is dated 2026-01-22 (ST line 98), so the announcement may predate the 23rd. Fix: delete "23, " ("January 2026").
- (b) Line 434: "February 27, 2026 | The Chief Financial Officer's revenue estimates; the general sales tax increase postponed | [^23]". ST line 59 says the estimates report the postponement; it does not date the postponement to that day (#rules says it correctly: "according to the Chief Financial Officer's February 2026 revenue estimates"). Fix: delete "; the general sales tax increase postponed".

### A1-10 MINOR: the description prints 23.5% with no period
- Line 6: "... in Washington, DC, with office vacancy at 23.5%." (156 characters). The stats band and body give the period (third quarter of 2026, Cushman & Wakefield). The description is not page text for I89, but a searcher reads an undated rate. A dated version within 160 characters needs a word change ("... in DC, with office vacancy at 23.5% in Q3 2026." is 155 but drops "Washington"); left to attacker B and the SEO owner, with a capped review if changed.

### A1-11 MINOR (research hygiene, no page edit)
- MT line 109: note "-1.0% over the year"; the pre-count's fetch found a 0.5% change on a three-month basis. Not printed.
- MT line 37: note quotes "Page updated: March 2026"; the pre-count found "March 2026 - Updated to include more recent information". The page's source 30 date line paraphrases correctly.
- ST lines 29 and 35: notes say "a fall of 18,600 over the month" (August 2026) and "a fall of 21,900 over the month" (August 2025); one-month falls of that size beside the June and September notes suggest over-the-year changes misread. Not printed; relevant to A1-1 if a fetch shows August 2025 restated.
- ST lines 96 and 97 split "10 projects" (Hoodline) from "2,563" (Commercial Observer); the page cites Commercial Observer for both, which ST line 97's own What cell ("the 10 abated conversions") supports.
- Published cells for the BLS Economy at a Glance rows (ST line 37, MT lines 92 to 97) hold the extraction date, as the pre-count flagged; the page's source dates say "page read October 28, 2026", correctly.

## Item the RESUME asked: no Virginia county figure in the Washington metro section
PASS. Tag-stripped text of `<main>`: "Arlington" and "Alexandria" occur only in the metro's name ("Washington-Arlington-Alexandria") in #washington-metro and source 33's title; no Fairfax, Loudoun, Prince William, Falls Church, Manassas, Fredericksburg, Stafford, Spotsylvania, Fauquier, Clarke, Culpeper, Rappahannock, Warren or "Northern Virginia" anywhere on the page. Every figure in the section is a metro total (3,435,000; 3,292.0, 676.6, 769.4, 318.4, 78.5 thousand; 375,800 to 312,500; Yardi 4,101, $2,191, $2,227), a DC-MD division total (1,084,800; -25,800) or Matthews' Washington report (geography unstated, not a county). The section's own sentence "no figure for any single Virginia county" holds. None of the 56 counted values occurs on the Virginia or Northern Virginia drafts or on any other GEO-5 draft (text search of `pages/**`; the one hit, "811" on Colorado, is inside a FRED series id).

## Re-derived figures (value; citation; research row; result)
Results: "PC" = confirmed by the pre-count's WebFetch spot check; "row only" = value and period carried by the research row, source not opened by anyone in this round. My own fetches: none (see above).
1. 739,200, November 2025, preliminary; [^1]; ST 41; PC (ORA, January 28, 2026); "lowest since the year after the COVID-19 lows" is the row's What cell, not verified. A1-1 stricter reading.
2. 169,000 federal, November 2025; [^1]; ST 42; PC ("169.0 thousand").
3. 751,000, August 2025; [^14]; ST 35; row only. A1-1.
4. 721,800, June 2026; [^15]; ST 32; row only. A1-1.
5. 713,600, August 2026; [^16]; ST 29; row only.
6. 719.9 thousand, September 2026, SA, preliminary (borderline, D12); [^17]; ST 37; PC.
7. 715.8 thousand, March 2026; [^3]; ST 39; PC (release September 3, 2026).
8. 51.4 thousand establishments, Q1 2026; [^3]; ST 38; PC.
9. $2,725, Q1 2026 (stats, #economy, #costs); [^3]; ST 40; PC.
10. 160,900; [^18]; ST 23; PC (October 20, 2026).
11. 125,500; [^18]; ST 24; PC.
12. 17,600; [^18]; ST 27; PC.
13. 402,900; [^18]; ST 19; PC.
14. 380,400; [^18]; ST 20; PC.
15. 23.5%, Q3 2026 (description, stats, FAQ 2, #office); [^2]; ST 117; PC (date on the listing card; quarterly report, I77(c)).
16. $55.15 per sf; [^2]; ST 118; PC.
17. 360,154 sf "positive absorption"; [^7]; ST 120; PC (the page uses CBRE's word, as pre-count flag 4 asked). A1-4 on the next clause.
18. 218,400 sf Class A; [^7]; ST 121; PC.
19. 2,563 (secondary); [^8]; ST 97; PC on Commercial Observer.
20. 811 homes (secondary); [^9]; ST 100; PC on Hoodline ("an additional 811 homes"). A1-2.
21. 73,000+; [^21]; ST 151; PC ("more than 73,000").
22. 27.2 million, 2025; [^4]; ST 134; PC (May 6, 2026). ST 134's note says 2024 was also 27.2 million; the page attributes "slight growth" to the release's own title, correctly.
23. $11.9 billion; [^4]; ST 135; PC.
24. 114,013; [^4]; ST 137; PC.
25. -42,500 sf CBD, Class B move-outs; [^2]; MT 9; PC.
26. 70,400 sf East End, "led by Class A"; [^2]; MT 10 (Class A +46,000 sf); PC.
27. $788 million, 2024, "nearly one-third"; [^29]; MT 23; row only.
28. $645 million, FY2025 projected; [^29]; MT 24; row only.
29. 12,299; [^30]; MT 37; PC.
30. 1,356; [^30]; MT 39; PC.
31. 701,000 sq ft; [^30]; MT 40; PC.
32. 3,435,000, Washington MSA labor force, September 2026; [^28]; MT 87; PC.
33. 1,084,800, DC-MD division; [^28]; MT 88; PC.
34. -25,800, division federal, August to August; [^5]; MT 91; PC. A1-8.
35. 3,292.0 thousand, NSA, preliminary (borderline); [^33]; MT 92; PC.
36. 676.6 thousand government (borderline); [^33]; MT 93; PC; "does not separate federal" matches the row note.
37. 769.4 thousand (borderline); [^33]; MT 94; PC.
38. 318.4 thousand (borderline); [^33]; MT 95; PC.
39. 78.5 thousand (borderline); [^33]; MT 96; PC.
40. 375,800 to 312,500 (secondary); [^6]; ST 165; PC ("from about 375,800"). A1-7(d).
41. $2,227, Q2 2026; [^11]; MT 100; PC.
42. -0.72% over the year; [^11]; MT 100 What cell; row only.
43. 4,613 units; [^11]; MT 101; PC.
44. 7,698 units TTM; [^11]; MT 102; PC. A1-7(a).
45. $8.24 billion TTM; [^11]; MT 104; PC.
46. up 44.5%; [^11]; MT 104 What cell; row only.
47. 4,101 units, January to May 2026; [^34]; MT 108; PC.
48. $2,191, December 2025; [^12]; MT 109; PC ("the year is implied" by a February 2026 edition; acceptable).
Register, each equal to `data/markets/series/<series>.json` for `dc` (and `co-11001`, identical), none null, none flagged, one vintage each, no PEP and no acs1 twin on the page: 49. $109,870 (acs5_median_hh_income); 50. $77,348 (acs5_per_capita_income); 51. $52,696.6 million (acs5_aggregate_income, 52,696,645,000; A1-3); 52. 324,491 (acs5_households); 53. $1,954 (acs5_median_gross_rent); 54. $737,100 (acs5_median_home_value); 55. $78,079.5 million (bea_personal_income, 78,079,526,000); 56. $111,185 (bea_per_capita_income). Printed, not counted: 134,683 (acs5_owner_occupied) and 189,808 (acs5_renter_occupied), both equal to the series.
Uncounted values, each with a dated source (I86): 15.95% and 14.95%, April 1, 2023 to March 30, 2027 (ST 79, OTR notice of February 13, 2023), nocount; 15 years, 45 days, 22 days (ST 85, 86, Holland & Knight September 25, 2025), nocount; 20 years (ST 97 note, Commercial Observer January 23, 2026), nocount; EM-3643-DC, February 20, 2026, incident from January 19, 2026 (ST 108), nocount; May 18, 2026 submissions (MT 69); `sba:` values 13 CFR 120.160(b), SOP 50 10 8.1 effective 2026-10-01, 1.15x and 15% equal `data/regulatory/sba.json` (R43, sop, R28, R31).

## Rules checked with no finding beyond those above
- Every printed number traces to a dated research row or the register (I77, I86). None of the undated rows (Census snippet 693,645; Destination DC research page 36,187 and 3,220; CoStar snippet; Stream Realty; OTR rate and deed pages; WMATA; Southwest BID) and none of the single-project rows (The Geneva's $465 million, $575 million and 532; RFK $77 million; St. Elizabeths $1 billion; 183 acres) is printed; "532" occurs only inside source 9's URL.
- No research-computed sum printed (I55): 811 is Hoodline's own total, not 300 plus 511 (pre-count flag 7).
- Source titles equal the research's verbatim for all 33 research-backed sources (script comparison by URL); sources 19, 20, 35 and 36 use the register and SBA titles that 37 to 90 other page sources already carry (I176).
- Ruling 10 for the register: the research holds no newer vintage of any register series printed (its V2025 population is undated and not printed); one ACS product per measure.
- Rounded or same-fact repeats on other served pages (I71, I82): checked the office-repurposing research note (Housing in Downtown units and caps at other dates, different facts) and the Kentucky and South Carolina value collisions (different facts; pagecheck already drops 312,500).
- Gate output agrees with my pagecheck rerun; gate 13 is green in `-g13.txt`.

## Count after my confirmed findings
A1-1 removes 751,000 and 721,800 (-2); A1-2 wraps 811 (-1); A1-3 to A1-11 change no counted value. Simulated in memory with the copy's own `pagecheck.check` (the rendered page with the edits applied as strings, no file written): 53 counted (research 45, register 8). With A1-1's stricter reading (739,200 also removed) 52 (research 44, register 8); with A1-8's alternative (-25,800 removed) one fewer again. READY floors (A6: 30 in all, 20 research) hold on every route; landing floors (25, 15) hold.
