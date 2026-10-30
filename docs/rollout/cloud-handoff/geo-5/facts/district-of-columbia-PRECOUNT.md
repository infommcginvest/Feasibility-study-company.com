# District of Columbia pre-count (GEO-5, Sonnet reader)

Method: ROLLOUT-1 rulings 4 to 6, amendments A4 and A6, integrator rulings I55 to I183 as the brief lists them. Each of the 170 fact-sheet rows (93 ST, 77 MT) was judged for dating (I77 a/b/c), countability (rule values, single property, arithmetic, list counts, I82 repeats) and scope; `taken` (served pages) and `shared_geo5` (another new state's research) were trusted as they stand: 84 rows are lost to them (42 ST, 42 MT), which leaves 86 free rows, of which 46 are counted and 40 are dropped with a reason (JSON `dropped`).
The District is both state and county (co-11001); its markets are submarkets of one city plus the Washington metro area. A submarket cannot be a metro page, so each one is reported as a section with its count. The Washington metro area is treated as a section of the District page (rule F7, two-state markets: the CBSA, cbsa-47900, takes in Virginia, Maryland and West Virginia counties that the Virginia drafts and the live Maryland page cover). A market stands as a page only with 21 free research figures, research plus at most 10 register at 30, and 20 research once secondary and borderline rows are removed one family at a time.
Dating route: (a) a publication or release date in the Published cell, (b) edition year in the title, (c) the period of a periodic document. Borderline: the five BLS Economy at a Glance rows (monthly period, but the page prints only "Data extracted on" Oct 28 2026, a retrieval date; recognised periodic BLS CES series, so counted as (c) and listed borderline) and ST 37 (same page type). Secondary rows count only when the row, or the sibling rows of the same article, name the original publisher and a date.
The undated rows the brief names (OTR tax-rate pages, the Census snippet, the CoStar snippet, the Stream Realty report, the Destination DC page) are out, and so are the same-class WMATA snippet and the undated Southwest BID page. Nothing is written to a repository.

## Verdict table

| Page | Facts | Countable (fact sheet) | Free research, main reading (a/b/c) | Register | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| downtown-dc (Downtown and the Central Business District) | 21 | 2 | 4 (4/0/0) | 10 (District co-11001, same values as the state's `dc`; 28 pairs) | 14 | SECTION: 4 free, under 21 |
| noma-union-market (NoMa and Union Market) | 12 | 3 | 3 (3/0/0) | 10 (District only) | 13 | SECTION: 3 free, under 21 |
| capitol-riverfront-southwest-waterfront (Capitol Riverfront (Navy Yard) and the Southwest Waterfront) | 5 | 0 | 0 | 10 (District only) | 10 | SECTION: 0 free, every row taken, single-property or undated |
| wards-7-and-8 (Wards 7 and 8 east of the Anacostia River) | 11 | 3 | 0 | 10 (District only) | 10 | SECTION: 0 free; the 3 sheet-countable rows are single-site land areas (I64) |
| washington-metro (Washington metropolitan area) | 28 (+1 ST) | 14 (+1 ST) | 15 (10/0/5) | 10 (cbsa-47900, 26 pairs; whole MSA) | 25 | SECTION of the District page (F7): 15 free, under 21, and the CBSA is multi-state in any case |
| state, own rows only | 93 | 31 | 24 (23/0/1) | 10 (`dc`, 28 pairs) | 34 | clears R9 on its own rows (20 research, 30 in all) |
| state, all five markets folded (the final reading) | 170 | 53 | 46 (40/0/6) | 10 | 56 | SHIPS (R9: 20 research and 30 in all) at the main reading; no metro stands, so taking a standing metro out changes nothing |

Where the 46 sit: state own 24, Downtown 4, NoMa 3, Capitol Riverfront and Southwest 0, Wards 7 and 8 0, Washington metro 15 (14 MT rows plus ST 165, the WJLA metro-wide federal employment row, which belongs to the metro under ruling 4). ST 156 and ST 157 (Downtown BID hotel revenue and fiscal impact) are the same facts as MT 23 and MT 24 and are counted once, in Downtown.
Fact-sheet count 53 to my 46: minus ST 67 (single financing transaction), ST 79 (hotel tax rate), ST 109 (relay with no original named), ST 169 (single project), MT 69, 70, 71 (single-site land areas).
Slugs (ids on `/states/district-of-columbia/`): downtown-dc, noma-union-market, capitol-riverfront-southwest-waterfront, wards-7-and-8, washington-metro. No district-of-columbia page is served and data/site/promised.json holds none, so no folded request is made.

## Per-market sensitivity (free research figures; each section tested as a standing page alone)

| Page | Main | Without secondary | Without borderline | Without both | Without broker rows | Without Matthews rows | Without DC-MD Division rows | Without NoMa page-update-stamp rows | Without BID 2024 rows | Harshest stack |
|---|---|---|---|---|---|---|---|---|---|---|
| downtown-dc | 4 | 4 | 4 | 4 | 2 | 4 | 4 | 4 | 2 | 0 |
| noma-union-market | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 3 | 0 |
| capitol-riverfront-southwest-waterfront | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| wards-7-and-8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| washington-metro | 15 | 14 | 10 | 9 | 15 | 11 | 13 | 15 | 15 | 3 |
| state, own rows | 24 | 22 | 23 | 21 | 20 | 24 | 24 | 24 | 24 | 12 |
| state, all folded | 46 | 43 | 40 | 37 | 40 | 42 | 44 | 43 | 44 | 15 |

Further single removals for the state with all folded: without superseded DOES monthly readings (ST 29, 32, 35) 43; without the ORA November 2025 rows (ST 41, 42) 44; without the CBRE rows that conflict with the taken C&W absorption (ST 120, 121) 44.

The state's harshest stack (all folded, 15): remove secondary rows (ST 97, 100, 165), borderline rows (ST 37, MT 92 to 96), superseded DOES months (ST 29, 32, 35), the ORA November 2025 rows (ST 41, 42), broker rows (ST 117, 118, 120, 121, MT 9, 10), Matthews rows (MT 100, 101, 102, 104), DC-MD Division rows (MT 88, 91), NoMa page-update-stamp rows (MT 37, 39, 40) and the BID 2024 rows (MT 23, 24). That leaves 15 research and 25 in all: UNDER the R9 floors (20 and 30) at the harshest reading. On its own rows alone the state's harshest stack is 12. The main reading and every single-family removal clear 20 research (lowest single removal: broker rows, 40 for the whole page; 20 for the own rows alone, exactly on the floor). Five of the families are already single points of failure for their sections, so the state margin is the folded markets, as in Montana and Delaware.
No market is near a page: the best, Washington metro, holds 15 (10 without borderline, 9 without both), 6 short of 21 and 11 short of the Oahu rule.
Site collisions: 84 of 170 rows are already taken or shared (the served site prints most DC round values; Virginia's research holds the DOES MSA unemployment, the Matthews vacancy and the Downtown BID jobs). Under A4 a landing page that prints one of the 46 can take it back; the margin over 20 is 26 on the main reading.

## Register (counted once, up to 10 per page)

The District's `dc` and `co-11001` hold identical values; they are one fact, not two pairs. There is no sub-District geography, so the four submarkets have no register value of their own. Pairs chosen for the state page (all acs5 2020 to 2024 unless BEA): median household income 109870, median home value 737100, median gross rent 1954, per capita income 77348, households 324491, owner occupied 134683, renter occupied 189808, aggregate income 52696645000, BEA personal income 78079526000, BEA per capita income 111185. No population series (never PEP; bea_population is 702250 from PEP). `dc` has 28 non-null, unflagged non-population pairs (26 ACS, 2 BEA). For the Washington section the CBSA reading (cbsa-47900, 26 pairs, no BEA) is listed in the JSON for completeness; a page holds at most 10 register in all, so those are not added to the state's 10.

## Spot check (18 URLs opened with WebFetch; the brief asks 12; no door closed)

| Row | Source (kind) | Result |
|---|---|---|
| ST 100 811 homes | Hoodline, 2026-01-23 (secondary) | confirmed: "an additional 811 homes, including 106 affordable units"; the 10 projects and 2,563 units on the same page; so 811 is printed, not the research's sum of 300 and 511 |
| ST 97 2,563 units | Commercial Observer, 2026-01-23 (secondary) | confirmed; also prints 300-unit and 511-unit projects |
| ST 165 375,800 to 312,500 | WJLA, 2026-07-21 (secondary) | confirmed: "from about 375,800 jobs to 312,500", region wide |
| ST 109 243 million gallons | MEAWW, 2026-02-21 (secondary) | confirmed in the body (headline says 200M); the page attributes it to the utility (DC Water), which the research row does not say |
| MT 92 to 96 | BLS Economy at a Glance, Washington MSA (borderline) | all five values confirmed (Sep 2026, preliminary); page prints no release date, only "Data extracted on: October 28, 2026" |
| ST 37 719.9 thousand | BLS Economy at a Glance, DC (borderline) | confirmed (Sep 2026, preliminary); same extraction date only |
| MT 87, 88, 91 | DOES Washington metro release (primary) | confirmed; release date Wednesday Oct 28 2026 printed; 3,435,000 is the Washington MSA labor force, 1,084,800 and the federal change are the DC-MD Division |
| MT 100 to 104 | Matthews Q2 2026 (primary) | confirmed: rent $2,227, net absorption 4,613, TTM completions 7,698, TTM volume $8.24B (Q2 alone $2.11B); date 9/9/26; geography not defined ("Washington D.C.", "the region") |
| MT 106, 108 | Yardi Matrix July 2026 (primary) | confirmed: $2,227 and 4,101 units; dated July 29, 2026 |
| MT 109 | Yardi Matrix February 2026 (primary) | $2,191 confirmed; the year is implied (December); the page's change is 0.5% on a three-month basis, the research row says -1.0% over the year (not confirmed) |
| MT 37, 39, 40 | NoMa BID strategic plan (primary) | values confirmed (12,299; 1,356; 701,000 sq ft at end of 2025); date printed as "March 2026 - Updated to include more recent information", not the research's "Page updated" wording |
| ST 134, 135, 137 | Destination DC release (primary) | confirmed: 27.2 million, $11.9 billion, 114,013; dated May 6, 2026 |
| ST 120, 121 | CBRE Q3 2026 (primary) | confirmed in substance: "360,154 sq. ft. of positive absorption", Class A "absorbed 218,400 sq. ft."; page dated September 30, 2026 |
| MT 9, 10, ST 117, 118 | Cushman & Wakefield MarketBeat (primary) | confirmed; the 10/8/2026 date sits on the listing card only |
| ST 41, 42 | ORA November 2025 report (primary) | confirmed: 739,200; federal 169.0 thousand (169,000); dated Jan 28 2026 |
| ST 151 | DMPED release (primary) | confirmed: "more than 73,000 total housing units"; dated July 10 2026 |
| ST 38, 39, 40 | BLS County Employment and Wages (primary) | confirmed; release date Sep 3 2026 |
| ST 19, 20, 23, 24, 27 | DOES September 2026 release (primary) | confirmed; dated Oct 20 2026 |

Tally: 18 opened, 18 confirmed (with the qualifications in the table), 0 not on page, 0 doors closed. No row was removed because of the spot check; ST 109 was already out (no original named in the row).

## Final step: the Virginia and Northern Virginia drafts

Searched `pages/virginia.html` and `pages/virginia/northern-virginia.html` (tag-stripped text, and the raw files plus both `.keys.json` for the larger values) for each of the 46 counted values and the 7 dropped-but-printed ones (402,900; 380,400; 160,900; 125,500; 17,600; 713,600; 721,800; 751,000; 719.9; 51.4; 715.8; 2,725; 739,200; 169,000; 2,563; 811; 23.5%; 55.15; 360,154; 218,400; 27.2 million; 11.9 billion; 114,013; 73,000; $788; $645; 42,500; 70,400; 12,299; 1,356; 701,000; 3,435,000; 1,084,800; 25,800; 3,292; 676.6; 769.4; 318.4; 78.5; 2,227; 4,613; 7,698; 8.24; 4,101; 2,191; 375,800; 312,500; 243 million; 5.25 million). Hits: none. The only overlaps are the `shared_geo5` rows the fact sheet already removed (Virginia's research, not drafts, holds the DOES MSA unemployment rates, the Matthews vacancy and the Downtown BID jobs figure).

## Flags for the writer

1. Matthews does not state its geography (District, metro or region). The rows sit under the metro heading in MT; the writer should call them "Matthews' Washington report" and not claim the District or the MSA. The $2,227 value is also Yardi's metro figure through May 2026; one value is one fact (kept at Matthews MT 100 per the fact sheet; MT 106 is dropped).
2. Geographies inside the DOES metro release: the title and headline rate (4.5 percent) are the DC-MD Division (the District, Charles and Prince George's counties MD); 3,435,000 and 3.7% are the Washington MSA; 1,084,800 and the federal change of -25,800 are the Division. The BLS EAG rows are the MSA (DC-VA-MD-WV). The Maryland and Virginia counties inside these are covered by other pages (F7).
3. BLS Economy at a Glance Published cells (2026-10-28) are the extraction date, a retrieval date; do not print them as release dates. Use the period (Sep 2026, preliminary).
4. CBRE (+360,154 sf, Q3 2026) and Cushman & Wakefield (-123,800 sf, taken at ST 119) disagree in sign; methodology differs. Print only the CBRE row with its publisher; CBRE says "positive absorption", not "net absorption".
5. The research replaced dashes with hyphens in titles (its Hygiene note). Source pages print some with dashes (Yardi "Report - February 2026" shows an en dash on the page, the WMATA report URL carries one). Use the research's title as given (I176) with no dash of your own.
6. NoMa rows depend on a month-only update stamp ("March 2026 - Updated to include more recent information") on a non-periodic strategic plan page; if the integrator reads that as not dating, NoMa goes to 0 and the state to 43.
7. ST 100's 811 is printed by Hoodline, but the same row's note offers Commercial Observer's 300 and 511; do not print an 811 as a sum of the two. 2,563 and 811 come from one Mayor's release relayed twice.
8. ST 109 (243 million gallons) is out of the main reading: the research row names no original; the page attributes it to the utility and its headline says 200M. Restoring it would need the research to carry DC Water.
9. Unemployment rates are four-way inconsistent across sources (DOES 5.6% Sep 2026, ORA 6.5% Nov 2025, DowntownDC 6.7% Dec 2025, BLS 6.2% Apr 2026; most taken): do not set them side by side.
10. The Downtown BID rows (MT 23, 24) describe 2024 and a FY2025 projection; they are stale next to the 2025 State of Downtown report (ST 45 to 47, taken).
11. ST 156 and 157 are the same facts as MT 23 and 24 (counted in Downtown). MT 29 is the same fact as ST 117 (counted on the state).
12. The WJLA metro federal figure (ST 165) belongs to the Washington metro section, not the state's own prose.
13. Hotel tax 15.95% (ST 79), the OTR rates and the RENTAL Act items are rule values: printable only with dates, in `data-fsc-nocount` (I62, I86); the OTR rates and deed tax are undated and are not printed at all (I86).
