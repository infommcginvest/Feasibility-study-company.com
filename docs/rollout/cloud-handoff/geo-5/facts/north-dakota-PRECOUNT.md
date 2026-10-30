# North Dakota pre-count (GEO-5, 28 Oct 2026)

Method: ROLLOUT-1 rulings 4 to 6 with A4 and A6 (research 20 at READY for the state, 30 in all; a metro needs 21 free countable dated research figures, research plus at most 10 register 30, and 20 research once secondary and borderline rows are removed one family at a time), R9, and the integrator rulings I55 to I182 the brief names (I77 dating, I69, I86, I82, I91, I109, I64 and I66, I183 and the Montana table as the precedent for method). The matcher is the fact sheet's: `taken` (served pages that already print the first figure, by pagecheck's value and rounding rules, sources lists included, I71) and `shared_geo5` are trusted; every other call is made row by row here.
Rows: 191 (ST 67, MT 124). Mechanical countable 77 (ST 25, MT 52). Judgement removals from those 77: 9 FDIC API rows (borderline, held out of the main reading), 12 bi-state rows (the county or metro includes Minnesota; the brief says Fargo uses Cass County and Fargo city only, and the same in-state rule is applied to Grand Forks, see flag 1), and the Bismarck tax-levy reimbursement (an event amount the researcher flagged). Main reading: 55 free research figures (state own 21, markets 34), all dated as (a), a publication or release date in the Published cell (FRED rows by the page's printed last-updated date, flag 6); (b) and (c) are 0 in the main reading.
Dating of the borderline class: FDIC BankFind and Summary of Deposits API rows print no date (spot check confirms: only an index creation stamp) and FDIC is not in the brief's list of recognised periodic releases, so the 9 FDIC rows are borderline and out of the main reading. BLS Economy at a Glance rows carry the extraction stamp (28 Oct 2026, a retrieval date, which never dates a row) and are dated by period only under (c); BLS CES/LAUS is recognised, so they would count in the main reading and sit in the borderline list, but all four free ones are bi-state and none is in the in-state main reading. BLS LAUS API and county rows are all taken by served pages, so they do not enter any count.
Register: ND has no site market and no states/north-dakota page; series hold `nd`, `co-38xxx` and `cbsa-xxxxx` keys. Every geography has at least 14 non-null, unflagged, non-PEP-population pairs, so the cap of 10 is always reachable and the register is never the limit (the ND page has the Vintage 2025 population 799,358, so no PEP population is used). Case towns (A4): none; no served case, promised URL or data/site file names a North Dakota town, so Fargo, Bismarck, Mandan, Grand Forks, Minot, Williston, Watford City and Dickinson carry no restriction.

## Verdict table

| Page | Facts | Countable (mechanical) | Free research, main reading (a/b/c) | Register | Total at READY | Verdict |
|---|---|---|---|---|---|---|
| fargo | 37 | 14 | 6 (6/0/0) | 10 | 16 | folds into the state page (needs 21 research) |
| bismarck-mandan | 29 | 13 | 11 (11/0/0) | 10 | 21 | folds into the state page (needs 21 research) |
| grand-forks | 16 | 8 | 4 (4/0/0) | 10 | 14 | folds into the state page (needs 21 research) |
| minot | 10 | 8 | 7 (7/0/0) | 10 | 17 | folds into the state page (needs 21 research) |
| williston | 24 | 6 | 4 (4/0/0) | 10 | 14 | folds into the state page (needs 21 research) |
| dickinson | 8 | 3 | 2 (2/0/0) | 10 | 12 | folds into the state page (needs 21 research) |
| state, own rows only | 67 | 25 | 21 (21/0/0) | 10 | 31 | state page (a new state: R9) |
| state, all six markets folded | 191 | 77 | 55 (55/0/0) | 10 | 65 | ships if the page holds 20 research and 30 in all at READY (R9): clears both |

No market stands: the best, Bismarck-Mandan, holds 11 free research figures against the 21 required, and no sensitivity brings any market to 21 under the rules (the most generous reading, which lets taken rows, bi-state rows, FDIC rows, undated populations and unit-context rows all count, reaches Fargo 29, Bismarck-Mandan 21, Williston 19, Grand Forks 12, Minot 8, Dickinson 5, which I71, I77, I86 and the Fargo in-state instruction forbid). Folded sections: fargo, bismarck-mandan, grand-forks, minot, williston, dickinson, each with its slug as id. None was promised (data/site has no ND entry), so no folded request is made.

## Per-market sensitivity (free research figures; each market tested as a standing page, none of the others standing)

| Page | Main reading | Without secondary | Without borderline (recognised, counted in main) | Without both | With FDIC borderline rows | With bi-state rows | With unit-context rows (+2) | With undated citypopulation.de rows (I109 not met) | Without airport boardings (single-facility risk) | Harshest stack | Site collisions ignored, everything generous | Register available (non-null, unflagged, no PEP population) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fargo | 6 | 3 | 6 | 3 | 6 | 14 | 8 | 9 | 3 | 1 | 29 | CBSA 22020 32; Cass 35 |
| bismarck-mandan | 11 | 6 | 11 | 6 | 12 | 11 | 11 | 15 | 8 | 4 | 21 | CBSA 13900 32; Burleigh 35; Morton 21 |
| grand-forks | 4 | 2 | 4 | 2 | 4 | 8 | 4 | 6 | 4 | 2 | 12 | CBSA 24220 32; county 35 |
| minot | 7 | 2 | 7 | 2 | 8 | 7 | 7 | 7 | 7 | 2 | 8 | CBSA 33500 32; Ward 35 |
| williston | 4 | 3 | 4 | 3 | 6 | 4 | 4 | 8 | 4 | 3 | 19 | CBSA 48780 18 (Williams only); Williams 21; McKenzie 21 (no CBSA) |
| dickinson | 2 | 2 | 2 | 2 | 3 | 2 | 2 | 4 | 2 | 2 | 5 | CBSA 19860 18; Stark 21 |

No recognised-borderline row is in an in-state main reading (the four BLS Economy at a Glance rows are bi-state; every BLS LAUS API row is taken), so 'without borderline' equals the main reading; with the four bi-state EAG rows allowed and then removed as borderline, Fargo reads 14 then 12 and Grand Forks 8 then 6. Secondary families removed one at a time: none of the six markets keeps 20 research under any single removal (Bismarck-Mandan without secondary 6, the best of the six). Fargo: 3 of 6 free figures are secondary or relay (FRED/Realtor.com, FRED/BEA, Inforum); Bismarck-Mandan 5 of 11; Grand Forks 2 of 4; Minot 5 of 7; Williston 1 of 4; Dickinson 0 of 2.

## State page, every market folded (free research figures)

| Reading | Research | Total with register 10 |
|---|---|---|
| Main reading (state own 21 + fargo 6, bismarck-mandan 11, grand-forks 4, minot 7, williston 4, dickinson 2) | 55 | 65 |
| Without secondary, aggregator and news-relay rows | 30 | 40 |
| Without recognised-borderline rows | 55 | 65 |
| With FDIC borderline rows (+9) | 64 | 74 |
| With bi-state rows (+12) | 67 | 77 |
| With unit-context rows (+2) | 57 | 67 |
| With the undated citypopulation.de rows (+15, I109 not met) | 70 | 80 |
| Without airport boardings (six Fargo and Bismarck airport rows) | 49 | 59 |
| Harshest stack | 24 | 34 |
| Site collisions ignored, everything generous (not allowed by the rules) | 133 | 143 |

State own rows only (nothing folded): main 21 (total 31), without secondary 12, harshest 10. With any standing metro taken out: no metro stands, so the count is the same 55. State beside all six metros as pages (before any fold) would hold 21 research and 31 in all, which is why the folds carry the page.

Harshest stack for the state: remove, together, all secondary and relay rows (25), the six airport boardings (single-facility risk, I64), the BND 2024 prior-year comparator (ST line 49), the discontinued 2023 Bismarck MSA GDP series (MT line 73) and the one preliminary reading (ST line 24; the others are taken). Result: 24 research (state own 10, markets 14: fargo 1, bismarck-mandan 4, grand-forks 2, minot 2, williston 3, dickinson 2), 34 in all with the register's 10. That is 4 over the research floor of 20 and 4 over 30 in all, so the page clears R9 at the harshest reading, thinly. Weak points in that stack: it rests on BLS QCEW rows (16 of the 24: state 2, county 14), the BND annual-report rows, and the NDAC releases.

## Spot check (12 fetches; 12 chosen rows, 27 rows confirmed because rows share pages)

| Row | Value | URL host | Result |
|---|---|---|---|
| ST 14, MT 116, MT 117 (secondary) | 799,358; 68,233; 75,694 | minotdailynews.com (2026-03-26) | confirmed; article says the 'metropolitan area that includes Ward, McHenry and Renville counties' is 75,694, so not a research sum; also prints 68,186 for 2024 |
| ST 78, 79, 80, 86 (secondary) | 34.583 million bbl; 3.58 BCF/day; 19,961; 3,040 | minotdailynews.com (2026-08-25) | confirmed for June 2026; page credits the 20 Aug 2026 monthly report |
| MT 29 (secondary, unit-context) | 281 permits, Fargo, Jul 2025 | stacker.com (2026-05-01) | confirmed; credited to Redfin analysis of monthly permits in the city |
| MT 76 (secondary, FRED) | $499,923, Sep 2026 | fred.stlouisfed.org MEDLISPRI38015 | confirmed; source Realtor.com, last updated 1 Oct 2026 |
| ST 70 (secondary, FRED/FHFA) | 539.91, Q2 2026 | fred.stlouisfed.org NDSTHPI | confirmed; last updated 25 Aug 2026 |
| MT 73 (secondary, FRED/BEA) | 9,430.711 million, 2023 | fred.stlouisfed.org NGMP13900 | confirmed; title carries (DISCONTINUED); last updated 4 Dec 2024 |
| ST 59, 60, 61, 62 (borderline) | 59,309,013; 51,007,223; 626,626; 4,765,228 | api.fdic.gov banks/summary | confirmed (records CB_2025_ND and SI_2025_ND); no release date printed, only an index creation stamp, so borderline stands |
| MT 124 (borderline) | 3,185,567 ($ thousands), Ward, 2025 | api.fdic.gov banks/sod | confirmed; no data date printed (index creation stamp only), borderline stands |
| ST 107, MT 44, MT 81 (secondary) | 1,322,791; 590,542; 309,533 | inforum.com (2026-01-23) | confirmed |
| ST 110, 111, MT 45, MT 82 (primary) | 104,380; 973,044; 49,464; 25,218 | aero.nd.gov (2026-10-21) | confirmed |
| ST 30, 31, MT 121, 122 (primary) | 420,702; $1,333; 30,481; $1,234 | bls.gov county employment and wages (2026-09-04) | confirmed, Table 2, Q1 2026 |

Tally: 12 fetches (11 distinct hosts and pages plus the two FDIC API calls), 12 of 12 chosen rows confirmed (secondary 8, borderline 2, primary 2), 27 rows confirmed in all because rows share pages; 0 not on page, 0 door closed. No row is marked not countable by the check; the FDIC rows stay borderline because the API prints no data date. No closed door was met and none was worked around.

## Flags for the writer

1. Bi-state geography. Fargo (Cass County plus Clay County, Minnesota) and Grand Forks (plus Polk County, Minnesota): the BLS metro labor force and payroll rows (MT 17, 18, 96, 97), FHFA and BEA MSA rows (MT 27, 28, 103, 106) and the Fargo-Moorhead broker rows (MT 34, 37, 39, 40) include Minnesota. They are outside the main reading per the in-state instruction for Fargo; the same rule is applied to Grand Forks as an extension, and the bi-state sensitivity shows what is lost (+8 Fargo, +4 Grand Forks). The Fargo and Grand Forks sections would print Cass County, Fargo city, Grand Forks County and Grand Forks city only. Bismarck's MSA (Burleigh, Morton and Oliver counties) is wholly in North Dakota but takes in Oliver County, which the section's county list does not name; Minot's MSA is Ward, McHenry and Renville (MT 117 matches it); Williston micro is Williams County only, McKenzie County has no CBSA (register uses co-38105 and co-38053); Dickinson micro takes in Billings and Golden Valley counties besides Stark.
2. The 15 citypopulation.de rows (MT lines 13, 14, 15, 57 to 60, 93, 94, 133 to 136, 164, 165) are undated, and the method note says only 'relaying Census (undated, context only)', no vintage, so I109 is not met. They also look mislabelled: every county level equals the register's 2024 value (bea_population and acs1_pop 2024: Cass 200,945; Burleigh 103,107; Morton 34,194; Grand Forks 73,771; Williams 40,763; McKenzie 14,782; Stark 33,767), not a 1 July 2025 estimate. Do not print them as 2025 levels; the dated 2025 levels are ST 14 and MT 116 to 118. Printing them would also repeat register values.
3. Population conflict: Minot Daily News gives Ward County 68,186 for 2024 and 68,233 for 2025; the register's 2024 value for Ward (bea_population, acs1_pop) is 68,427. Do not print the 2024 pair beside the register value.
4. Conflict inside the research: ST 109 (NDAC release of 2026-07-20) gives a prior-year first-half comparison of 654,350 while ST 108 (release of 2025-07-14) gives 654,304 for the same half. Print only one, with its release.
5. ST 13 and ST 14 are the same fact (FRED thousands and the Minot article); only ST 14 counts (I82). ST 94 (25.6 million visitors) is also in another new state's research and is out. ST 49 (BND 2024 net income) is a prior-year comparator printed in the 2025 release; it counts as a dated release value but is removed in the harshest stack.
6. FRED relays: the date taken is the page's printed last-updated date (all spot-checked rows matched), the original publisher (BEA, FHFA, Realtor.com) is named in the research, so they count as secondary. The three MSA GDP series (MT 28, 73, 103) are marked DISCONTINUED on FRED and hold 2023 data (last updated 4 Dec 2024); only MT 73 (Bismarck, in-state) is in the main reading. County real GDP is in thousands of chained 2017 dollars and the state's is in millions of chained 2017 dollars; units must be printed as the rows give them.
7. BLS Economy at a Glance pages: the Published cell (2026-10-28) is the extraction stamp, a retrieval date. LAUS county annual-average rows (MT 20, 65, 67, 99, 120, 138, 140, 167) are an 11-month average excluding October 2025 (data not collected during the federal funding lapse), not a full-year average. All are taken, but the label '2025 annual' must not be printed as a full-year average.
8. Not market figures (researcher flagged, confirmed): the Burleigh County tax-levy error reimbursement of $269,942 (MT 84), the Williston air-service change (MT 156), FEMA declaration numbers and individual FEMA county counts (ST 123 to 132, MT 49, 85, 108, 154, 155; code numbers and lists the page can name, I91). Single-property rows (ST 140, 141, MT 38, 47, 48, 107, 171) are I64 and I66 and stay out.
9. Airport boardings (ST 107 to 112, MT 44 to 46, 81 to 83) are counted as market demand figures, not single-facility attributes; if the integrator reads the six per-airport rows as I64 (one named facility), the state falls from 55 to 49 and the harshest stack is already without them.
10. Unit-context rows: bare counts pagecheck does not read as the cell stands. MT 26 (712 active listings, Cass, Sep 2026) and MT 29 (281 permits, Fargo, Jul 2025) are free if printed with 'listings' and 'permits'; they are outside the main reading. All other Stacker permit months, the rig counts, ST 84 (93 permits, taken by Utah) and ST 85 are taken or unread.
11. Title wording: ST lines 55 to 57 (Flex PACE) title reads 'Flex PACE Program - Bank of North Dakota', a spaced hyphen that may stand for a separator on the source page (not fetched); those rows are undated, taken and not counted, but cite the title as the research gives it (I176). The Stacker, Minot Daily News, Inforum and aero.nd.gov titles match the pages fetched.
12. Thin research: the researcher's search budget ran out (broker, local-rule, permit and hotel lookups are NOT FOUND for every market), so every market section rests on BLS QCEW, FRED and airport rows; the sections should be short and say so. Williston's apartment, hotel and permit data are NOT FOUND, and MT 149 (Watford City hotel occupancy 59.2%) is taken by a served page.
13. FDIC rows (9 borderline): state class CB and SI summaries (ST 59 to 62) and county SOD deposits (MT 74, 124, 147, 148, 170; MT 24 and 75 are taken). If the integrator accepts the FDIC annual releases as recognised periodic, the state reads 64 (total 74) and every market gains 0 to 2.
