# GEO-5 t3 freeze 1, attacker A (figures, dates, floors, research hygiene)

Tranche t3: `/states/south-dakota/` (no metro page; six markets folded as sections). Frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t3/`. Page source `src/pages/states/south-dakota.html` sha256 68eb5362... (equal to `drafts/geo-5/pages/south-dakota.html` and to FREEZE-t3-f1). Research: `ST-SOUTH-DAKOTA.md`, `ST-SOUTH-DAKOTA-2.md` (supplement), `MT-SOUTH-DAKOTA.md`.

Method: read the page source in full; read all three research files, the assignment, the pre-count (md and json) and D17, D19, D20; ran `scripts/qa/pagecheck.py --figures` in the copy (107 counted: 98 research, 9 register); compared every register value with `data/markets/series/<series>.json`; compared every source title and date with the research row for its URL by script; opened 27 source documents with WebFetch (list at the end). No 403, 429, robots refusal or bot check met. Nothing fetched from www2.census.gov. The NASS PDF came back as binary from WebFetch; I read the text of the file the fetch saved with macOS PDFKit (script in my scratchpad), outside any repository.

## Findings

### A1-1. MAJOR-FACTUAL. The 2025 job openings total is printed as the sum of its components (I55, I59; the integrator's instruction)
Page: `/states/south-dakota/`, section `#economy`, Projections paragraph.
Quoted: "Its October 2026 bulletin projects 63,399 total openings a year across all occupations from 2024 to 2034, adding growth, people leaving the labor force and workers changing occupations [^7]."
Reproduction: opened `https://dlr.sd.gov/lmic/lb/2026/lbart_oct2026_occupational_demand_projections_2024_2034.aspx` (issue "October 2026"; source line "Labor Market Information Center, South Dakota Department of Labor and Regulation, August 2026"). The Total, All Occupations row prints 523,468 / 562,027 / 38,559 / 3,856 / 27,054 / 32,489 / 63,399; 63,399 sits in the last position, under "Total Openings" (the "Average Annual Openings" header is a group header over the four openings columns, so the value is confirmed as total openings). No sentence on the page says the total is the sum of growth, exits and transfers; the text says demand "has two components: employment growth" and separations. "adding growth, people leaving the labor force and workers changing occupations" states an addition the source does not print, which is the check the writer did by hand. The page does not print the three component values, so the reader cannot see inputs (I60(b)).
Fix (deletion): replace ", adding growth, people leaving the labor force and workers changing occupations [^7]." with " [^7]." The next sentence ("Openings measure turnover as well as growth") and FAQ 3's "a count that includes turnover as well as growth" already say what the source says. FAQ 3 does not print the sum or the components: no change there.

### A1-2. MAJOR-FACTUAL. The SDMHA $1,002 is a one-bedroom average, printed as "an average rent"
Page: `/states/south-dakota/`, FAQ 5 and section `#sioux-falls` (Apartments).
Quoted (FAQ 5): "its July 2025 survey had market-rate vacancy at 5.43% and an average rent of $1,002, excluding properties in lease-up [^12]."
Quoted (#sioux-falls): "Its July 2025 survey had market-rate vacancy at 5.43% and an average rent of $1,002, excluding properties in lease-up [^12]."
Reproduction: research MT-SOUTH-DAKOTA line 38 labels the row "Average rent, one-bedroom | $1,002". Opened `https://siouxfalls.business/?p=174122` (Aug. 11, 2025): "A one-bedroom averages $1,002 versus $994 last year", under the city-wide rents paragraph; the lease-up exclusion is printed ("Those don't include new-construction properties still being leased up"). The page drops the unit type and so states a different measure (an all-unit average rent) than the source carries.
Fix (two identical edits): "an average rent of $1,002" becomes "an average one-bedroom rent of $1,002" in FAQ 5 and in the Apartments paragraph.

### A1-3. MAJOR-FACTUAL. The SDMHA comparison caution is misattributed
Page: `/states/south-dakota/`, section `#sioux-falls` (Apartments) and FAQ 5.
Quoted (#sioux-falls): "The two surveys cover different samples, and the association's own caution about comparing them applies; an apartment study treats them as readings, not a trend line, and surveys the competitors around its site."
Quoted (FAQ 5): "The two samples differ, so a study for a new building treats them as readings, canvasses the competitors nearest its site and reads the pipeline from ..."
Reproduction: opened `https://siouxfalls.business/?p=185065` (March 16, 2026). Its only caution is "That makes it somewhat hard to compare with one year ago", which refers to the January 2025 survey (20,000 units, 9.46 percent), not to the July 2025 survey the page sets beside January 2026. The article itself compares January 2026 with July 2025 directly ("increased to 6.62 percent in January from 5.68 percent in the previous reporting period"). So "the association's own caution about comparing them" is not on the source. "The two surveys cover different samples" / "The two samples differ" compares two sample sizes the page does not print (14,409 units responding in January 2026 against 17,067 market-rate units in July 2025, both research note values): a comparison in words without the inputs (I60(b)).
Fix (deletions): #sioux-falls: "The two surveys cover different samples, and the association's own caution about comparing them applies; an apartment study treats them as readings" becomes "An apartment study treats them as readings". FAQ 5: "The two samples differ, so a study for a new building treats them as readings" becomes "A study for a new building treats them as readings".

### A1-4. MAJOR-FACTUAL. Lawrence County is not in the Rapid City metro area the LMIC tabulates
Page: `/states/south-dakota/`, section `#rapid-city`, first paragraph (and by consequence "The metro area had 74,312 covered workers").
Quoted: "The Black Hills market here is Pennington, Meade and Lawrence counties, the Rapid City metro area as the Labor Market Information Center draws it, all inside South Dakota."
Reproduction: opened `https://dlr.sd.gov/lmic/qcew2025_9_rcmsa_est_work_pay.aspx`: total 7,928 establishments, 74,312 workers, $59,377 (confirmed), but the page names no counties (only "Totals may not add due to rounding. Data subject to revision."). Research ST-SOUTH-DAKOTA-2 line 124 says only "In-state MSA". So the composition is uncited. It is also wrong: the county workers page the research cites (ST-SOUTH-DAKOTA-2 line 126 note) gives Pennington 62,445, Meade 9,178 and Lawrence 13,694 for 2025; the three together exceed the MSA's 74,312, so Lawrence cannot be inside that MSA (the OMB Rapid City MSA is Pennington and Meade; Lawrence County is the Spearfish micropolitan area). This check is mine and is not to be printed.
Fix (deletion): "The Black Hills market here is Pennington, Meade and Lawrence counties, the Rapid City metro area as the Labor Market Information Center draws it, all inside South Dakota." becomes "The Black Hills market here is Pennington, Meade and Lawrence counties, all inside South Dakota." and "The metro area had 74,312 covered workers in 2025 at average annual pay of $59,377 [^63]." becomes "The Rapid City metro area as the Labor Market Information Center tabulates it had 74,312 covered workers in 2025 at average annual pay of $59,377 [^63]."

### A1-5. MAJOR-FACTUAL. Fall River County is not Pennington County's neighbour
Page: `/states/south-dakota/`, section `#rapid-city` (Projects and gaps).
Quoted: "Straight-line winds in December 2025 brought DR-4903-SD for Pennington County, and its neighbors Custer and Fall River [^38]."
Reproduction: research ST-SOUTH-DAKOTA line 120 (source 38) lists "public assistance in Custer, Fall River and Pennington counties" and says nothing about adjacency. Fall River County borders Custer County to its north and does not touch Pennington County (Custer and Oglala Lakota counties lie between them). The "neighbors" claim is uncited and wrong for Fall River.
Fix: "for Pennington County, and its neighbors Custer and Fall River [^38]" becomes "for Pennington, Custer and Fall River counties [^38]".

### A1-6. MINOR. Tourism's 16.5% is the release's ratio of tourism's state and local tax revenue to state sales tax collections
Page: `/states/south-dakota/`, hero_sub, stats band, `#brief`, `#visitors` (and the description).
Quoted (hero): "tourism generated 16.5% of South Dakota's state sales tax collections in 2025"; stats label "Share of South Dakota's state sales tax collections generated by tourism in 2025 [^1]"; `#brief`: "tourism accounted for 16.5% of total state sales tax collections [^1]".
Reproduction: opened `https://sdvisit.com/newsroom/2025-shows-continued-strength-south-dakotas-tourism-industry` (1/21/2026): "Tourism activity also generated $406.1 million in state and local tax revenue, representing 16.5% of all state sales tax collections." 14.97 million, $5.16 billion, 59,145 and $406.1 million confirmed. Read literally, the 16.5% sets tourism's state and local tax revenue (all taxes) against state sales tax collections; it is not a statement that 16.5% of sales tax collections came from tourism. The research row (ST-SOUTH-DAKOTA line 55) labels it "Tourism share of total state sales tax collections", and the Department's framing invites that reading, so I rate this MINOR; the verifier may judge it higher, since it is the lead fact.
Fix (smallest, `#visitors` keeps its wording closest to the source and needs none): in `#brief`, "and generating $406.1 million in state and local taxes; tourism accounted for 16.5% of total state sales tax collections [^1]" becomes "and generating $406.1 million in state and local taxes, which the Department puts at 16.5% of all state sales tax collections [^1]". Hero and stats band may stay if the verifier accepts the Department's framing.

### A1-7. MINOR. "counted two ways" survives the ruling 10 deletion
Page: `/states/south-dakota/`, section `#economy`, first paragraph.
Quoted: "The population base is small and counted two ways. FRED relays the Census Bureau's Vintage 2025 estimate of 935.094 thousand ..."
Reproduction: `diff work/south-dakota.pre-r10.html pages/south-dakota.html` shows D20 deleted the Vintage 2024 state figure (924,669) and the sentence explaining the two vintages but kept the opener, which now announces a second count the paragraph no longer gives (the bulletin is cited next only for migration). `grep` of the rendered page: 935.094 once; no 924,669, 925,000 or "925 thousand". Ruling 10 holds for the state geography: one vintage.
Fix: "The population base is small and counted two ways. FRED relays" becomes "FRED relays".

### A1-8. MINOR. Source 21's date names a vintage the bulletin does not print
Page: sources list, source 21.
Quoted: "e-Labor Bulletin, December 2025 (Census Bureau estimates for 2024, Vintage 2024)".
Reproduction: opened `https://dlr.sd.gov/lmic/lb/2025/lbart_dec2025_population.aspx`: issue "December 2025"; 209,300, 79,900, 27,900 (third), 24,550 (fourth) confirmed; it cites "U.S. Census Bureau, Population Estimates Program" and names no vintage. "Vintage 2024" is the researcher's inference (ST-SOUTH-DAKOTA-2 lines 116, 128, 140, 151 notes).
Fix: "(Census Bureau estimates for 2024, Vintage 2024)" becomes "(Census Bureau estimates for 2024)".

### A1-9. MINOR. "including $4.19 million" asserts a part-whole the release does not state
Page: FAQ 6 and section `#supply`.
Quoted (FAQ 6): "$59.4 million to developments, including $4.19 million of Housing Tax Credits, announced on December 10, 2025 [^13]."; `#supply`: "announced $59.4 million awarded to developments, including $4.19 million of Housing Tax Credits [^13]".
Reproduction: opened `https://www.sdhousing.org/news-blog/affordable-housing-awards-2025` (dateline "PIERRE, SD (12.10.25)"; post header "Dec 9" with no year, the dateline carries the date the page prints). The release says the Board "awarded $59.4 million to support the construction and rehabilitation..." and then "The developments received $42 million in bond financing, $3.25 million in Housing Infrastructure Financing, $4.19 million in Housing Tax Credits, $6.26 million in HOME..., $1.93 million... and $2.62 million...". It never says the $59.4 million includes the tax credits, and its own program list does not reconcile to $59.4 million, so "including" is the writer's inference.
Fix: "including $4.19 million of Housing Tax Credits" becomes "and $4.19 million of Housing Tax Credits among the amounts the developments received" (both places), or delete the clause and its value from FAQ 6 and keep it in `#supply` only.

### A1-10. MINOR. "Mitchell's series rests on a small sample of listings" has no source
Page: section `#mitchell-pierre`.
Quoted: "Mitchell's series rests on a small sample of listings, so a study reads several months of it, not one."
Reproduction: opened `https://fred.stlouisfed.org/series/MEDLISPRI33580`: Sep 2026 251,950 confirmed, updated Oct 1, 2026; no note on sample size or reliability. "small sample" is the researcher's note on MT-SOUTH-DAKOTA line 139, not a statement of FRED or Realtor.com.
Fix: "Mitchell's series rests on a small sample of listings, so a study reads several months of it, not one." becomes "A study reads several months of a listing series, not one."

### A1-11. MINOR. Two Sioux Falls metro figures carry no boundary label, which the page promises
Page: section `#sioux-falls` (Homes; Air traffic and output), against `#metros` ("This page reads Minnehaha and Lincoln counties for Sioux Falls and labels every metro-wide figure where it appears").
Quoted: "FHFA's all-transactions index for the Sioux Falls metro area read 365.85 ... [^59]"; "BEA's last GDP figure for the Sioux Falls metro area is for 2023, 30,084.975 million dollars ... [^62]".
Reproduction: the Realtor.com figures are labelled ("published on its own metro boundary"); the LMIC rows are labelled as including Rock County, Minnesota (FAQ 4: "each for a metro area that takes in Rock County, Minnesota [^9]"; `#sioux-falls`: "labelled here as including Rock County, Minnesota"); I confirmed on `qcew2025_10_sfmsa_est_work_pay.aspx` that the LMIC MSA is "Lincoln, Minnehaha, McCook and Turner counties of South Dakota and Rock County of Minnesota" (177,999; $66,768; 34,900 confirmed). The FHFA and BEA figures say only "metro area".
Fix: "for the Sioux Falls metro area read 365.85" becomes "for the Sioux Falls metro area, on FHFA's own boundary, read 365.85"; "for the Sioux Falls metro area is for 2023" becomes "for the Sioux Falls metro area, on BEA's own boundary, is for 2023".

### A1-12. MINOR (record only, no edit proposed). The January 2026 article restates the July 2025 market-rate vacancy at another value
Reproduction: `?p=185065` says "Occupancy for market rate properties increased from 5.52 percent in July 2025 to 6.41 percent in January" (the article calls a vacancy rate "occupancy"); the page prints July 2025 market-rate vacancy as 5.43% from the August 2025 article (`?p=174122`: "showed a 5.43 percent vacancy in market rate apartment units in July"). Both values are cited correctly to their own sources; the page prints only one, so I82 is not breached. The 6.41% label on the page (vacancy) follows the research and the arithmetic of the article, not its word "occupancy". Recorded for the verifier; no change.

## Items the integrator asked to be tested

1. NASS Crop Production rows (881,840; 226,800; 1,959). CONFIRMED by name and position. Opened `https://esmis.nal.usda.gov/sites/default/release-files/796123/crop1026.pdf` ("Released October 9, 2026"). PDFKit prints each table's state stub list first and then each column as a run of values, so the state name is not on the value line in my extraction; I matched by position. Corn for Grain table: 33 stub rows (31 states, Other States, United States), South Dakota the 26th; in every one of the seven columns the 26th value is South Dakota's and the 33rd is the US total (area 2025 6,350, area 2026 5,840, yield 2025 171.0, Sept 1 145.0, Oct 1 151.0, production 2025 1,085,850, production 2026 881,840; US 90,948 / 88,506 / 186.5 / 178.8 / 181.2 / 16,963,628 / 16,033,944). Soybeans for Beans: 30 stub rows, South Dakota 25th: 5,060 / 5,400 / 47.0 / 42.0 / 42.0 / 237,820 / 226,800; US 80,417 / 85,881 / 53.1 / 4,561,605 in the 30th position. Column order is the printed header order (no rebuilding needed). A neighbouring row checks the alignment independently (North Dakota corn 4,450 x 132.0 = 587,400 at the same positions). Sunflower: "In South Dakota, the average yield is forecast at 1,959 pounds per acre, down 16 pounds per acre from last year's record high." Pods: "pod counts are down in 7 of the 11 published States. South Dakota showed the greatest decrease, down 414 pods per 18 square feet". The page's "among the states surveyed" matches "the 11 published States". No finding.
2. LMIC Sioux Falls metro rows (177,999; $66,768; 34,900). CONFIRMED and labelled at both printings (FAQ 4 and `#sioux-falls`), and the `#metros` paragraph names Rock County, Minnesota. They sit only in FAQ 4 and the Sioux Falls section (D17). The other metro-wide Sioux Falls figures: A1-11.
3. FRED manufacturing 43.8 thousand. The premise is REFUTED: the value is in the writer's assignment. `assign/south-dakota.json` `state_facts` carries `ST-SOUTH-DAKOTA line 29 | 43.8 (thousands)`; the pre-count lists it in `state_free_ids` and `secondary_ids` and spot-checked it. FRED SDMFG opened: "Sep 2026: 43.8", thousands of persons, seasonally adjusted, updated Oct 20, 2026. Source 23's title and date match the research. It sits in one sentence with the QCEW's 44,302 (2025 annual average covered workers): two different series, no comparison in words, no ruling 10 issue. No finding.
4. Job openings 63,399: A1-1 (the sum stated in words in `#economy`); FAQ 3 is clean. 562,027 (July 2026 bulletin) opened: "Total of All Industries ... 523,468 ... 562,027", in a table titled "South Dakota Wage and Salaried Workers by Industry Division 2024-2034" that also carries self-employed and unpaid family workers (25,801) and farm (34,087) rows; the page's "includes self-employed, unpaid family and farm workers and is not a wage and salary figure" is right. The research row's "What it measures" (ST-SOUTH-DAKOTA-2 line 34, "Wage and salaried workers in all industries") is wrong, a research-hygiene note only.
5. Population estimates. CONFIRMED: one state vintage remains (935.094 thousand, Vintage 2025, FRED SDPOP, source 20); no 924,669 or 925,000 anywhere on the rendered page. The deletion's leftover opener: A1-7. Sioux Falls city: 209,300 (Census estimate for 2024, LMIC bulletin, source 21) and 224,676 (the city's own figure via SDPB, source 52) are each labelled with publisher and year, and the page says the city figure "is a city estimate, not a Census figure". Note for the verifier: the cities' Census figures are for 2024 and the state's for 2025; under the brief's reading of ruling 10 (one vintage of a series per geography) that holds. Read literally, ruling 10's "Never put two vintages of one series on one page" would also reach them.
6. SDHDA rows whose posts print no year. Opened all three. Income limits (source 35): post header "Jun 15", no year; the text says "Effective June 15, 2026" and "the State Median Income, currently $103,400", so the value is dated by an effective date (I77(a)) and the page's label ("rest on a State Median Income of $103,400") is the source's; title matches. Homeless count (source 46): post header "Apr 22", no year; "A total of 1,154 people were identified as experiencing homelessness in South Dakota on January 27"; the text says "2026" several times ("the 2026 PIT count"), which dates the count; the April 22, 2026 publication year rests on the research's news-index entry (ST-SOUTH-DAKOTA-2 line 74), which the research carries, so I69 is met. The URL slug says "2025-pit-count", the text says 2026: recorded, no edit. Awards (source 13): dateline "12.10.25" carries the December 10, 2025 the page prints; A1-9 on "including".
7. e-Labor Bulletin rows dated by issue month. CONFIRMED that each page prints its issue month: December 2025 (population), April 2026 (469,400, "Not Seasonally Adjusted"), July 2026 (562,027), October 2026 (63,399; the source line also says "August 2026", the data date). The page cites each as "e-Labor Bulletin, <month year>" (I77(c), pre-count ruling 4). A1-8 on source 21's vintage words.

## Counted figures re-derived (49 of 98 research, plus all 9 register)

Value on page | citation | research row | source check
- 16.5% | [^1] | ST line 55 | sdvisit release 1/21/2026, opened: carried (wording A1-6)
- 14.97 million | [^1] | ST line 50 | opened: carried
- $5.16 billion | [^1] | ST line 51 | opened: carried
- 59,145 | [^1] | ST line 52 | opened: carried
- $406.1 million | [^1] | ST line 53 | opened: carried
- 881,840 (thousand bu) | [^2] | ST-2 line 93 | NASS PDF, opened: carried, SD by position
- 226,800 (thousand bu) | [^2] | ST-2 line 95 | NASS PDF, opened: carried
- 1,959 lb per acre | [^2] | ST-2 line 96 | NASS PDF, opened: carried, named sentence
- $1,211 | [^3] | ST-2 line 32 | BLS county release Sep 4, 2026, opened: carried, "Data are preliminary"
- $1,369 | [^3] | ST-2 line 109 | same, opened: carried
- $1,404,408 | [^4] | ST-2 line 129 | DOR 09-01-2026, opened: carried, "an 11% decrease"
- $473,668 | [^4] | ST-2 line 130 | opened: carried, up 15%
- 448,166 | [^5] | ST line 57 | SDDOT Aug 17, 2026, opened: carried, five-year average 2021-2025
- 484,700 | [^6] | ST line 21 | DLR snapshot, opened: September 2026, SA, "Preliminary data; subject to revision"
- 475,100 | [^6] | ST line 22 | opened: carried
- 470,500 | [^6] | ST line 24 | opened: carried
- 63,399 | [^7] | ST-2 line 35 | opened: carried in the Total Openings position (A1-1)
- $60,577 | [^8] | ST-2 line 23 | qcew2025_2_summary, opened: carried
- $71,093 | [^8] | ST-2 line 24 | opened: carried
- 44,302 | [^8] | ST-2 line 25 | opened: carried
- $24,183 | [^8] | ST-2 line 26 | opened: carried
- 177,999 | [^9] | ST-2 line 104 | qcew2025_10, opened: carried, MSA with Rock County
- $66,768 | [^9] | ST-2 line 105 | opened: carried
- 34,900 | [^9] | ST-2 line 106 | opened: carried
- $66,906 | [^10,53] | ST-2 line 108 | qcew2025_7, opened: carried
- $59,768 | [^10,53] | ST-2 line 127 | opened: carried
- $56,565 | [^53] | ST-2 line 139 | opened: carried (2024 $54,431)
- $58,550 | [^53] | ST-2 line 150 | opened: carried
- $54,662 | [^53] | ST-2 line 162 | opened: carried
- $57,418 | [^53] | ST-2 line 170 | opened: carried
- $64,153 | [^53] | ST-2 line 171 | opened: carried
- 6.62% | [^11] | MT line 33 | SFB ?p=185065, opened: carried
- 93.38% | [^11] | MT line 34 | opened: carried
- 6.41% | [^11] | MT line 35 | opened: carried (article's label "occupancy", A1-12)
- 5.43% | [^12] | MT line 37 | SFB ?p=174122, opened: carried
- $1,002 | [^12] | MT line 38 | opened: carried as one-bedroom (A1-2)
- $59.4 million | [^13] | ST line 109 | SDHDA, opened: carried
- $4.19 million | [^13] | ST line 111 | opened: carried (A1-9)
- 35.9 / 81.6 / 80.6 (thousand) | [^14] | ST-2 lines 29, 30, 31 | BLS Oct 20, 2026, opened: Table 3 "Sept. 2026(p)": carried
- 55.7 (thousand) | [^15] | ST line 30 | FRED SDLEIH, opened: carried
- 43.8 (thousand) | [^23] | ST line 29 | FRED SDMFG, opened: carried
- 562,027 | [^26] | ST-2 line 34 | July 2026 bulletin, opened: carried
- 469,400 | [^22] | ST-2 line 27 | April 2026 bulletin, opened: carried, NSA
- 209,300 / 79,900 / 27,900 / 24,550 | [^21] | ST-2 lines 116, 128, 140, 151 | Dec 2025 bulletin, opened: carried, ranks third and fourth
- $103,400 | [^35] | ST-2 line 73 | SDHDA, opened: carried
- 1,154 | [^46] | ST-2 line 74 | SDHDA, opened: carried
- 74,312 / $59,377 | [^63] | ST-2 lines 124, 125 | qcew2025_9, opened: carried (A1-4)
- $1,327,437,573 / 5,615 / $711.6 million / $314.2 million / 357 / 403 | [^48] | MT lines 12, 13, 17, 18, 14, 15 | Sioux Falls permit stats (Jan 14, 2026), opened: carried; $711.6 million includes $192.2 million for apartments
- $251,950 | [^77] | MT line 139 | FRED MEDLISPRI33580, opened: carried (A1-10)

Checked against the research and source titles and dates only (not reopened; the pre-count's spot check opened them): 935.094 (ST 11), 168,482 (ST 58), 642.50 (ST 104), 3,581 (ST 106), $4,770 and $6,268 (ST 130, 131), 82,001.9 and 59,865.2 (ST 38, 39), $2,315,908.04 (ST-2 62), 62,445 and 139,770 (ST-2 126, 107), 62,556 (ST-2 114), 76,958 (ST-2 131), $119,959,861.12 / $52,312,150.00 / 79 (ST-2 159 to 161), 224,676 (MT 11), 2,044 / 232 (MT 23, 24), 680,000 sq ft / $168 million / 1,120 acres (MT 29 to 31), 754,686 / 46,696,248 lbs / 18,506 (MT 41 to 43), $362,200 / 1,469 / 365.85 / 30,084.975 (MT 44, 45, 47, 48), $390.9 million / 2,428 / 58,519 / 452,195 / $417,450 / 489.32 / 9,425.612 (MT 59, 60, 74, 72, 77, 80, 81), $339,225 (MT 94), 357 Brookings (MT 108, a repeat of the Sioux Falls 357, counted once), 142 (MT 121), $324,950 (MT 141), $109,689,512 (MT 143). All match their rows, period and source.

Register (9 of 9 counted): $75,081, $40,550, $36,795.9 million (36,795,922,400), 365,544, 250,621, 114,923, $946, 163,311, 475,223, each equal to `data/markets/series/acs5_*.json` `values.sd.all.v`; none null; no flag on any value (acs5_pop65 carries only an MOE approximation note). No PEP or second ACS vintage used.

Sources (script over all 81 entries): every research-backed source's title equals the research title for its URL (I176) and every date equals the research's published value or its stated periodic/edition dating; sources 27, 80 and 81 are the register and `sba:` sources (not in research, as expected). No figure found attributed to a source that does not carry it. No single-property value printed as a figure (Smithfield, Gemini, REDI, Elevate and the airport grant are named without amounts), so no I64 nocount wrap is missing.

## Count after my confirmed findings

Every fix above is a deletion, a relabel or a recast that keeps the value and its citation; none removes a counted figure. Counted figures after the findings: 107 (98 research, 9 register), unchanged from gate 3 (pagecheck in the copy: 107, research 98, register 9/9). Floors (A6): READY 30 with 20 research: holds (107 / 98). Landing 25 with 15: holds. If the verifier instead deletes the FAQ 6 clause in A1-9 the $4.19 million still counts in `#supply`; no fix here changes the count.

## Pages opened (27, WebFetch; none refused)
esmis.nal.usda.gov crop1026.pdf; dlr.sd.gov lbart_oct2026_occupational_demand; lbart_jul2026_industry_projections; lbart_dec2025_population; lbart_apr2026_nonfarm_year_in_review; economic_snapshot.aspx; qcew2025_2_summary; qcew2025_7_county_annual_pay; qcew2025_9_rcmsa; qcew2025_10_sfmsa; sdhousing.org 2025-pit-count-numbers-released-ntfn9; incomelimits2026; affordable-housing-awards-2025 (twice); bls.gov laus_10202026.htm; countyemploymentandwages_southdakota_20260904.htm; siouxfalls.business ?p=174122; ?p=185065; sdvisit.com 2025 tourism release; dor.sd.gov 2026 rally collections; dot.sd.gov rally day ten; fred SDMFG; SDLEIH; MEDLISPRI33580; siouxfalls.gov permit-stats.

Severity tally: BLOCKER 0; MAJOR-FACTUAL 5 (A1-1 to A1-5); MAJOR-NONFACTUAL 0; MINOR 7 (A1-6 to A1-12, A1-12 record only).
