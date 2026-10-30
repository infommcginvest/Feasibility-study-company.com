# Virginia pre-count (GEO-5, Sonnet reader)

Method: ROLLOUT-1 ruling 6, amendments A4 and A6, integrator rulings I55 to I183 as the brief lists them. Each of the 276 fact-sheet rows (69 ST, 207 MT) was judged for dating (I77 a/b/c), countability (rule values, single property, arithmetic, list counts, I82 repeats) and scope, trusting `taken` and `shared_geo5` as they stand. Rows whose own note says the original publisher is not named, and API or live-page rows of publishers outside the brief's recognised-periodic list (BLS CES/LAUS/QCEW, BEA, FHFA, Census permits), are out of the main reading and listed as borderline; BLS regional tables and Economy at a Glance pages (monthly period, no printed release date) are in the main reading as (c) and listed as borderline too.
A market stands only with 21 or more free research figures, research plus at most 10 register pairs of 30 or more, and 20 research once secondary rows, then borderline rows, are removed one family at a time (I180). Nine extra single-family removals (and a combined stack) are shown for every market. Register pairs were read from the series files: every Virginia geography has 26 to 28 non-null, unflagged non-population ACS or BEA pairs, so the register never limits a page below 10.
Spot check: 17 URLs opened by WebFetch (brief asks 12), weighted to secondary and borderline rows; no door closed; all 17 values confirmed on their pages. Northern Virginia uses Virginia jurisdictions only (co-51059 Fairfax, co-51013 Arlington, co-51107 Loudoun, co-51153 Prince William, co-51510 Alexandria city), no multi-state CBSA; no Washington metro-wide row exists in the Virginia research.
Counting conventions: a/b/c is the dating route (a release or publication date in the Published cell, b edition year in title, c period of a periodic document with no printed release date). No row rests on b alone. Free = countable by the fact sheet or by my override, after my drops, in the main reading. FRED relays carry the FRED last-updated stamp as their date and are secondary.

## Verdict table

| Page | Facts | Countable (fact sheet) | Free research, main reading (a/b/c) | Register | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| northern-virginia | 67 | 37 | 37 (36/0/1) | 10 (26 to 28 pairs available) | 47 | PAGE: northern-virginia. 37 free, 36 without borderline, 28 without secondary, 27 without both, 23 without brokers; research plus 10 register is 47 |
| richmond | 35 | 19 | 19 (15/0/4) | 10 (26 to 28 pairs available) | 29 | SECTION: 19 free, under 21 |
| hampton-roads | 37 | 21 | 21 (17/0/4) | 10 (26 to 28 pairs available) | 31 | SECTION: 21 free but 14 without secondary, 17 without borderline (fails the Oahu rule, I180) |
| roanoke | 16 | 10 | 10 (8/0/2) | 10 (26 to 28 pairs available) | 20 | SECTION: 10 free, under 21 |
| charlottesville | 17 | 11 | 11 (10/0/1) | 10 (26 to 28 pairs available) | 21 | SECTION: 11 free, under 21 |
| lynchburg | 7 | 5 | 5 (4/0/1) | 10 (26 to 28 pairs available) | 15 | SECTION: 5 free, under 21 |
| blacksburg-christiansburg | 11 | 6 | 6 (4/0/2) | 10 (26 to 28 pairs available) | 16 | SECTION: 6 free, under 21 |
| harrisonburg | 9 | 5 | 5 (4/0/1) | 10 (26 to 28 pairs available) | 15 | SECTION: 5 free, under 21 |
| winchester | 8 | 6 | 6 (5/0/1) | 10 (26 to 28 pairs available) | 16 | SECTION: 6 free, under 21 |
| state, own rows only | 69 | 32 | 25 (23/0/2) | 10 (28 pairs on va) | 35 | own rows alone clear R9's 20 research and 30 in all |
| state, NoVa standing as a page, 8 markets folded | 209 | 115 | 108 (90/0/18) | 10 | 118 | SHIPS (R9: 20 research and 30 in all) |
| state, all 9 markets folded | 276 | 152 | 145 (126/0/19) | 10 | 155 | SHIPS (R9) |

Reading: only Northern Virginia stands as its own metro page. Hampton Roads is the near miss (21 on the strict count, but its secondary rows are 7 of 21 and its borderline BLS table rows 4 of 21, so each single removal leaves it under 20). Richmond has 19 against the 21 needed. Every other market is far under. Slugs for the folded sections (ids on `/states/virginia/`): richmond, hampton-roads, roanoke, charlottesville, lynchburg, blacksburg-christiansburg, harrisonburg, winchester. No Virginia page is served and data/site/promised.json holds no Virginia entry (only west-virginia), so no folded request is made. The research puts Harrisonburg and Winchester under one MT heading; they are two separate MSAs (cbsa-25500, cbsa-49020), so they are counted as two markets (combined 11 free rows, still far under 21). Joint slug `shenandoah-valley` would hold the union of the two id lists.

## Per-market sensitivity (free research figures; each market tested as a standing page alone)

| Page | Main | Without secondary | Without borderline | Without both | Without FRED relays | Without non-FRED secondary | Without broker rows (CBRE, C&W) | Without scope-flagged rows | Without discontinued FRED GDP rows | Without conflict rows | Without my override | Without stale vintage | Harshest stack | With borderline-out rows added |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| northern-virginia | 37 | 28 | 36 | 27 | 29 | 36 | 23 | 36 | 37 | 31 | 36 | 37 | 20 | 38 |
| richmond | 19 | 16 | 15 | 12 | 16 | 19 | 12 | 19 | 18 | 19 | 19 | 19 | 12 | 19 |
| hampton-roads | 21 | 14 | 17 | 10 | 16 | 19 | 18 | 13 | 20 | 21 | 21 | 21 | 8 | 21 |
| roanoke | 10 | 7 | 8 | 5 | 7 | 10 | 8 | 10 | 9 | 10 | 10 | 10 | 5 | 10 |
| charlottesville | 11 | 2 | 10 | 1 | 7 | 6 | 11 | 11 | 10 | 9 | 11 | 11 | 1 | 11 |
| lynchburg | 5 | 2 | 4 | 1 | 2 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 1 | 5 |
| blacksburg-christiansburg | 6 | 3 | 4 | 1 | 3 | 6 | 6 | 6 | 5 | 6 | 6 | 6 | 1 | 6 |
| harrisonburg | 5 | 2 | 4 | 1 | 2 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 1 | 5 |
| winchester | 6 | 3 | 5 | 2 | 3 | 6 | 6 | 3 | 5 | 6 | 6 | 5 | 1 | 6 |
| state (own rows) | 25 | 12 | 23 | 10 | 17 | 20 | 25 | 25 | 25 | 23 | 25 | 25 | 10 | 30 |

Definitions. Secondary: the research's `secondary` kind (FRED relays of Realtor.com, FHFA, Census and BEA; FFXnow, ARLnow, WDBJ7, WVIR, Information Charlottesville, AviationPros, Holland & Knight, Governing). Borderline in the main reading: BLS regional metro tables (ro3fx pages, month-grain 2026-10 listing, no release date printed on the page, confirmed on the Northern Virginia table) and BLS Economy at a Glance pages (date is the page's extraction stamp). Scope-flagged: BLS Northern Virginia region wider than the five jurisdictions (MT line 28); Hampton Roads MSA rows whose area takes in Camden, Currituck and Gates counties in North Carolina (MT lines 127 to 129, 131 to 133, 148, 149; the OEWS release confirms the three NC counties); Winchester MSA rows that take in a West Virginia county (MT lines 253, 263, 265). Conflict rows: both sides of each recorded conflict that sit in the free set (NoVa office rent MT 47/51, office absorption MT 43/56, industrial rent MT 61/65; ST 81/89; Charlottesville MT 209/210). Override: MT 57. Stale vintage: MT 266.

Not shown for the others, but checked: removing FRED relays alone leaves Northern Virginia at 29; removing the 14 broker rows leaves it at 23; no single family takes it under 20.

## Northern Virginia in detail (the one standing page)

- Free ids (37): MT lines 11, 12, 13, 14, 15, 16, 18, 19, 20, 28, 30, 33, 35, 36, 37, 38, 39, 40, 41, 43, 44, 47, 51, 52, 53, 54, 55, 56, 57, 61, 63, 65, 66, 73, 74, 75, 76.
- Families: BLS QCEW county rows 11 to 20 except 17 (taken) = 9; BLS regional table 28 (c, borderline, scope); FFXnow 30; FRED permits 33, 35, 36 and FRED listing prices 37 to 41 (secondary, 9 with FFXnow); CBRE 43, 44, 47, 61, 63; C&W 51 to 57, 65, 66; MWAA 73 to 76. Broker rows 14, secondary 9, borderline 1, conflict rows 6, override 1.
- Per-jurisdiction labels the writer must keep: Fairfax, Arlington, Loudoun, Prince William, Alexandria city only. Broker figures are each broker's own Northern Virginia definition, not the five jurisdictions; the C&W county asking rents (Arlington, Alexandria, Fairfax, Loudoun) are Virginia counties; Prince William has no broker row.
- Dropped for Northern Virginia: MT 77 (borderline out). Not counted by the fact sheet and left so: LAUS county rows (all taken), MT 57 NSF lease (the 386,600 sf at 401 Dulany St is single-property), loudoun.gov data centre rows 68 to 72 (undated page; a printed as-of date does not date a non-periodic page, I77).
- Margin: the stack of secondary + borderline + scope + conflict rows + override leaves exactly 20 research (plus 10 register = 30). That is on the floor, not above it; the single-family tests all leave 23 or more. Treat Northern Virginia as a page with a thin stacked margin and watch the site collisions at landing (the `taken` column already removes 26 rows the served site prints).
- Register pairs for a Northern Virginia page (Virginia counties only, acs5 2020-2024 5-year, values from the series files; BEA is null for Fairfax and Prince William so it is not used):
  co-51059 (Fairfax) acs5_median_hh_income 153637; co-51013 (Arlington) acs5_median_hh_income 142114; co-51107 (Loudoun) acs5_median_hh_income 181765; co-51153 (Prince William) acs5_median_hh_income 131402; co-51510 (Alexandria) acs5_median_hh_income 119681; co-51059 (Fairfax) acs5_median_home_value 732800; co-51013 (Arlington) acs5_median_home_value 895000; co-51107 (Loudoun) acs5_median_home_value 743800; co-51153 (Prince William) acs5_median_home_value 530100; co-51510 (Alexandria) acs5_median_home_value 735100.

## The state page

- State's own rows: 25 free research figures (fact sheet 32 countable; I drop ST 11, 85, 83, 84, 111, 112, 113 and add none). Register 10 pairs on `va` (acs5 median household income 93170, median home value 383700, median gross rent 1579, per capita income 50666, households 3365732, owner occupied 2266609, renter occupied 1099123, aggregate income 441060065800; BEA personal income 681552175000 and per capita income 77351). No population series is used (the page has Vintage 2025 population, ruling 10).
- All nine markets folded: 145 research, 155 in all (a/b/c 126/0/19).
- With Northern Virginia standing as a page: 108 research, 118 in all.
- State own rows by family: without secondary 12, without borderline 23, without both 10, without conflict rows 23.

State sensitivity (research figures; every market folded | Northern Virginia standing):

| Reading | All folded | NoVa standing |
|---|---|---|
| Main | 145 | 108 |
| Without secondary | 89 | 61 |
| Without borderline | 126 | 90 |
| Without both | 70 | 43 |
| Without FRED relays | 102 | 73 |
| Without non-FRED secondary | 132 | 96 |
| Without broker rows (CBRE, C&W) | 119 | 96 |
| Without scope-flagged rows | 133 | 97 |
| Without discontinued FRED GDP rows | 137 | 100 |
| Without conflict rows | 135 | 104 |
| Without my override | 144 | 108 |
| Without stale vintage | 144 | 107 |
| Harshest stack | 60 | 40 |

Harshest stack for the state: remove all secondary rows, the borderline BLS table and Economy at a Glance rows, scope-flagged rows, both sides of every recorded conflict, the override and the stale-vintage row. All nine folded: 60 research (70 in all). Northern Virginia standing: 40 research (50 in all). Both clear R9 (20 research and 30 in all). The state's own rows alone fall to 10 under the stack, so the state page depends on its folded sections, as the Montana page did.

## Spot check (17 opened; brief asks 12)

| # | Row | URL host and page | Value and period | Result |
|---|---|---|---|---|
| 1 | MT 30 | ffxnow.com, Fairfax County jobless residents | 23,749, Jan 2026 (also 3.8% rate, MT 31) | confirmed; page dated 20 Apr 2026, original is the Virginia Department of Workforce Development and Advancement, released 16 Apr |
| 2 | MT 33 | fred.stlouisfed.org BPPRIV051059 | 2,862, 2025 annual | confirmed; title says Structures, unit label Units, Census Bureau source, updated 28 May 2026 |
| 3 | MT 37 | fred.stlouisfed.org MEDLISPRI51059 | $724,900, Sep 2026 | confirmed; Realtor.com original, updated 1 Oct 2026 |
| 4 | MT 28 | bls.gov ro3fx9538 (Northern Virginia table) | 1,647,917 employed, Sep 2026 (p) | confirmed; the page prints no release date, only the monthly columns and footnotes (borderline confirmed) |
| 5 | MT 43 | cbre.com Northern Virginia Office Figures Q3 2026 | +355,000 sq. ft. Q3 2026 (also 20.9%, $37.80, 1.7 million) | confirmed; page dated 30 Sep 2026 |
| 6 | MT 51 | cushmanwakefield.com Northern Virginia Office MarketBeat | $36.45 per sf Q3 2026 (also 23.6%, +413,800 sf) | confirmed; related-insights card shows 10/8/2026. Conflicts with CBRE (flag) |
| 7 | MT 73 | mwaa.com 2025 passengers release | 29.01 million (also 10.53, 24.89, more than 53.9 million) | confirmed; release 24 Feb 2026; headline says 54 million, body says more than 53.9 million |
| 8 | MT 11 | bls.gov county employment and wages, Virginia Q1 2026 | 622,779 Fairfax March 2026 | confirmed; release 2 Sep 2026; the page's own title uses an em dash before First Quarter 2026, the research writes a comma |
| 9 | ST 81 | hklaw.com data centre incentive alert | $928.6 million FY2023 | confirmed and attributed to JLARC December 2024; page dated 20 Aug 2026. Same page prints $48.6 billion (ST 83) and $33.2 billion (ST 84) with no source named, so those two are borderline out |
| 10 | ST 111 | api.fdic.gov banks summary | 774,205,639 deposits, 31 Dec 2025 | value confirmed; the records carry no createTime, the index metadata shows createTimestamp 2026-09-16, and no unit is stated (borderline out) |
| 11 | MT 162 | aviationpros.com Norfolk airport | 4,892,594 passengers 2025 (also 396,470 Dec 2025) | confirmed; Norfolk Airport Authority named, page dated 15 Jan 2026 |
| 12 | MT 209 | infocville.com Charlottesville population | 44,388 (also 118,356 Albemarle), 1 Jul 2025 | confirmed as Census figures; the page also prints Weldon Cooper 46,923 and 119,479; an editor's note says posted 27 May 2026 and backdated to 26 Mar 2026 |
| 13 | MT 77 | ffxnow.com Dulles enplanements | 13,859,735, 2025 | value confirmed; page names the FAA (preliminary figures), dated 2 Jul 2026, but the research row says the original is not named, so it stays borderline out |
| 14 | MT 148 | fred.stlouisfed.org ATNHPIUS47260Q | 388.95, Q2 2026 | confirmed; FHFA original, updated 25 Aug 2026; area is VA-NC |
| 15 | ST 126 | wdbj7.com tourism 2025 | 46.6 million overnight visitors (also $36.2 billion, 3.1%) | confirmed; Governor's Office release, Virginia Tourism Corporation data by Tourism Economics, 11 Aug 2026 |
| 16 | MT 132 | bls.gov OEWS Virginia Beach-Chesapeake-Norfolk May 2025 | $30.83 mean hourly (also 41,190 construction) | confirmed; release 10 Jul 2026; MSA includes Camden, Currituck and Gates counties NC; title uses an em dash before May 2025 |
| 17 | MT 97 | fred.stlouisfed.org NGMP40060 | 116,959.541 million, 2023 | confirmed; BEA original; the series title carries (DISCONTINUED), last updated 4 Dec 2024 |

Tally: 17 opened, 17 value-confirmed, 0 not on page, 0 doors closed. Rows demoted by the check: ST 83, ST 84 (no original named on the page), ST 111 (retrieval-type stamp, no unit). No www2.census.gov fetch.

## Flags for the writer

1. Broker conflicts, all recorded side by side, none resolved: Northern Virginia office asking rent CBRE $37.80 (MT 47) against C&W $36.45 (MT 51); office net absorption Q3 CBRE +355,000 sq. ft. (MT 43) against C&W +413,800 sf (MT 56); office vacancy CBRE 20.9% (MT 42, taken) against C&W 23.6% (MT 48, taken); year to date absorption CBRE 941,000 (MT 44) against C&W +369,800 (printed in the note to MT 56); industrial asking rent CBRE $18.10 (MT 61) against C&W $18.73 (MT 65); industrial vacancy CBRE 3.9% against C&W 5.0% (both taken); industrial absorption CBRE 266,000 (taken) against C&W +168,600 (MT 66). Richmond: office vacancy CBRE 12.3% against C&W 12.5%, industrial vacancy CBRE 5.2% against C&W 4.1% (all four taken). Each broker uses its own market definition; the page must name the broker and say so, and must not average or rank them.
2. Data centre exemption cost for FY2023: $928.6 million (JLARC via Holland & Knight, ST 81) against $685 million (Virginian-Pilot via Governing, ST 89, the research calls it a prior-year comparison). Both recorded; the second is a different outlet's reading of the same fiscal year. ST 83 and ST 84 on the H&K page carry no named source.
3. Charlottesville population: Census 44,388 and 118,356 (MT 209, 210) against Weldon Cooper 46,923 and 119,479 on the same page; only the Albemarle Weldon Cooper value is in the research row note. The page is dated by its byline (26 Mar 2026) but has an editor's note that it went up 27 May 2026.
4. State population: ST 10 (Weldon Cooper 8.88 million) and ST 11 (FRED, Census 8,880.107 thousand) are the same fact at two scales; only ST 10 counts (I82). MT 266 (Winchester city 29,294) is a Vintage 2024 value relayed by the city; ruling 10 forbids two vintages of one series on a page, so skip it on any page that prints a Vintage 2025 population.
5. FRED metro GDP rows (MT 97, 149, 181, 203, 224, 240, 264, 265) are series titled (DISCONTINUED) in the research and on the page, 2023 annual, last updated 4 Dec 2024. They are dated and count, but they are the stalest figures on the page; the research did not find a newer series.
6. FRED permit series BPPRIV is titled Structures and its unit label reads Units. Four sub-1,000 values (MT 144 Chesapeake 846, MT 199 Albemarle 729, MT 237 Montgomery 328, MT 259 Rockingham 685) have no figure pagecheck can read without a unit pagecheck knows, and calling them units or permits would mislabel the series; they are dropped. ST 65 is a seasonally adjusted permits value to five decimals (3,274.12673); print it rounded and labelled adjusted. ST 69 (47 days) reads as no figure.
7. MT 145 ($487,000) and MT 146 ($487,250) round to the same three-digit figure under pagecheck; they are different cities and both count, but a page that prints both should expect the matcher to treat one as a rounding of the other.
8. Titles changed from the source: the research replaces dashes with commas, so a source title printed on a page must be the research's title (I176) even where the live page title has a dash: County Employment and Wages in Virginia, First Quarter 2026 (page: dash); Business Employment Dynamics in Virginia, Second Quarter 2025; Occupational Employment and Wages in Virginia Beach-Chesapeake-Norfolk, May 2025 and Roanoke, May 2025 (page: dash before the month). Titles that already read as fragments (Housing Inventory: ..., RIC Sets Passenger and Cargo Records in 2025) are as the research gives them.
9. Dating by listing or stamp: BLS table and Economy at a Glance dates are month or extraction stamps (borderline, kept as (c)); C&W and CBRE dates come from the report page or the MarketBeat listing card (the research notes 'date is listing date' on MT 101, 102, 108 and others); FRED dates are the series' last-updated stamps and differ from the original release dates.
10. Scope: MT 28 (Northern Virginia region) takes in Fauquier, Stafford, Spotsylvania and Fredericksburg, wider than the five jurisdictions, and is not seasonally adjusted. Hampton Roads BLS, OEWS, FHFA and BEA rows are for the VA-NC MSA (Camden, Currituck, Gates). Winchester rows for the MSA include a West Virginia county; Roanoke MSA includes Salem, Botetourt, Craig, Franklin and Roanoke counties and Roanoke city. State the area beside each figure.
11. MT 57 (Alexandria +377,800 sf) is counted as a city submarket total although its note says single-property; the NSF occupancy of 386,600 sf at 401 Dulany St is single-property and must stay out of the count (I64). MT 156, 160, 161, 241 and 242 and ST 150 and 152 are single-property or one-project rows and stay out.
12. Loudoun County data centre rows (MT 68 to 72) come from an undated page: its as-of 1 March 2026 does not date a non-periodic page, so none counts and none should be printed as a figure unless dated by another source (I86). MT 186 (Roanoke C&W Q2 2026 industrial) has no printed report date and is a superseded quarter.
13. ST 85, 86, 87 and 92 (electricity tax rate and cap, exemption threshold, sales tax rate) are rule values: printable only dated and inside nocount. ST 100 to 103 (FEMA declarations) are code numbers and counts of areas, not figures.
14. Fact sheet `taken` removes 107 of the 276 rows (the served site already prints their first figure; 26 of Northern Virginia's 67, 29 of the state's 69) and `shared_geo5` flags 49 (48 of them also taken; Wyoming, Alaska, Colorado, the District of Columbia, Vermont and the Dakotas hold the same first figure). I trust both. The BLS LAUS county and city unemployment rates are nearly all taken, which is why Northern Virginia keeps 37 of 67.
15. Hygiene of the research: row numbers in notes (for example 'row 81' on Richmond office vacancy) are the table numbers, not file lines; fact ids use file line numbers. The research met 403 or 429 doors on Cresa, Northmarq, Multi Housing News, Newmark, Axios, Virginia Business, Chamber RVA, The Roanoke Star and Prince William Times.
