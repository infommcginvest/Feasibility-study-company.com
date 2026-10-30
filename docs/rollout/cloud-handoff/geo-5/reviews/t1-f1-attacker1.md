# GEO-5 t1 freeze 1, attacker A (figures, dates, floors, research hygiene)

Pages: /states/colorado/ and /states/colorado/denver/, frozen copy ~/Downloads/fsc-rollout/tmp/geo-5/t1/ (sources src/pages/states/colorado.html and src/pages/states/colorado/denver.html). Research: research/ST-COLORADO.md, research/MT-COLORADO.md. Counts reproduced with `python3 scripts/qa/pagecheck.py --root . --stage ready --figures /states/colorado/ /states/colorado/denver/` inside the copy: Colorado 94 (85 research, 9 register), Denver 55 (46 research, 9 register), matching GATES-t1-f0.

Documents opened with WebFetch (23; no 403, 429, robots stop or bot check met; www2.census.gov not touched): DOLA bulletin 4065eb6; SnowBrains tourism article; KJCT tourism article; CBRE Denver Downtown Office, Denver Office, Denver Multifamily and Denver Retail Figures Q3 2026; Cushman and Wakefield MarketBeat Denver Office and Industrial Q3 2026; Matthews Denver multifamily Q2 2026 (twice) and Denver industrial Q2 2026; Visit Denver 2025 release; BLS Colorado regional page; BLS County Employment and Wages in Colorado Q1 2026; BLS OEWS Denver May 2025; FRED NGMP19740, BPPRIV008005, ACTLISCOU19740 and a FRED search for a current Denver metro GDP series; Aviation Industry News DEN article; Vail Daily budget article; FEMA releases of 15 Sep and 28 Sep 2026; KUNC 14 Apr 2026 article.

## Findings

### A1-1 MAJOR-FACTUAL, Denver: CBRE's suburban absorption is "more than 320,000", printed as an exact value and as the term of a sum
- Page text (four places): "net absorption of positive 320,000 square feet outside downtown, which left metro net absorption at negative 161,000 square feet [^6]" (#office); table row "-161,000 sq ft (+320,000; -483,000)"; FAQ 1 "The same firm's metro report shows the suburbs absorbing 320,000 square feet in that quarter [^6]"; #corridors cites the same.
- Reproduction: CBRE Denver Office Figures Q3 2026 (9 Oct 2026) prints "The suburbs recorded more than 320,000 sq. ft. of positive net absorption." The floor word is in the document; research row MT line 37 dropped it ("suburbs +320,000 sq. ft." in its What cell), so this is a research-hygiene error carried to the page. "Which left metro net absorption at negative 161,000" also states a result of arithmetic in words (I59): +320,000 and -483,000 make -163,000, not -161,000; the sentence only holds because the source's 320,000 is a floor.
- Fix: prose "net absorption of positive 320,000 square feet outside downtown, which left metro net absorption at negative 161,000 square feet" to "net absorption of more than 320,000 square feet outside downtown, and metro net absorption of negative 161,000 square feet"; FAQ 1 "absorbing 320,000 square feet" to "absorbing more than 320,000 square feet"; table "(+320,000; -483,000)" to "(more than +320,000; -483,000)". Count unchanged (320,000 still counts).

### A1-2 MAJOR-FACTUAL, Denver: the Matthews multifamily report does not credit CoStar
- Page text: "Matthews Real Estate Investment Services, whose report charts credit CoStar, reads the quarter before." (#supply) and source 2 publisher "Matthews Real Estate Investment Services (report charts credited to CoStar)".
- Reproduction: the Matthews page https://www.matthews.com/insights/denver-multifamily-q2-2026 (13 Aug 2026), fetched twice: no charts, and the word CoStar appears nowhere on it. Research rows MT lines 71 to 74 name the publisher as "Matthews Real Estate Investment Services" with no CoStar note. The credit came from the pre-count's spot check of a different report (Colorado Springs industrial). An attribution the document does not carry.
- Fix: delete ", whose report charts credit CoStar," (sentence becomes "Matthews Real Estate Investment Services reads the quarter before."); source 2 publisher to "Matthews Real Estate Investment Services" (the research's wording, I79). No count change.

### A1-3 MAJOR-FACTUAL, Colorado: "January 28, 2026" for DEN's release is in no document the research opened
- Page text: "as Aviation Industry News reported the airport's January 28, 2026 release [^23]" (#supply); events row "January 28, 2026 | Denver International Airport reports its record 2025 passenger year | [^23]"; source 23 publisher "Aviation Industry News (reporting the Denver International Airport release of January 28, 2026)".
- Reproduction: the Aviation Industry News article (29 Jan 2026) confirms 82,427,962, 4,867,484, 5.9% and "an all-time record" but names no release date and no 28 January release. ST line 164's note says the original is "the DEN press release of 2026-01-28 (flydenver.com returned 403)": the researcher could not open it, so the date traces to no dated document in the research (I69, I86). The page attributes it to [^23], which does not carry it.
- Fix (deletions): "reported the airport's January 28, 2026 release [^23]" to "reported the airport's release [^23]"; delete the events table row; source 23 publisher to "Aviation Industry News (reporting a Denver International Airport release)". No count change.

### A1-4 MAJOR-FACTUAL (ruling 4), Colorado: a Denver metro figure counts on the state page while Denver stands
- Page text: "SnowBrains puts the Denver metro's travel spending at about $14.2 billion, 48.5% of the statewide total in the article's own reckoning [^7]." Both $14.2 billion and 48.5% are in pagecheck's counted list for /states/colorado/. The metros section then says of Denver "none of its figures are repeated here."
- Reproduction: SnowBrains (2 Sep 2026) prints "Denver and its surrounding metro area ... at roughly $14.2 billion, or 48.5% of all travel spending in Colorado", so the values are sourced (ST line 155; not research arithmetic). But it is a Denver-metro fact; ruling 4 gives counted figures to the most specific page (metro over state), and the pre-count flagged ST 155 for exactly this. The state counts it only because the Denver page does not print it.
- Fix: wrap "about $14.2 billion, 48.5%" in `<span data-fsc-nocount>...</span>` (the figure may stay as context for the concentration sentence). Colorado falls to 92 counted (83 research). Alternative: move the clause to Denver's visitor paragraph (Denver would gain 2), which needs new wording.

### A1-5 MINOR, Colorado: the 28 July release date is cited to KJCT, which does not print it
- Page text: "The Colorado Tourism Office's research for 2025, released on July 28, 2026 and prepared by Dean Runyan Associates and Longwoods International, put travel spending ... as KJCT reported the next day [^3]."; events row "July 28, 2026 | Colorado Tourism Office releases its 2025 research | [^3]".
- Reproduction: KJCT (headline as cited, "Updated: Jul. 29, 2026") confirms $29.2 billion, "roughly 2%" over $28.5 billion and both firms, but gives no release date. SnowBrains (source 7) prints "released on July 28". ST line 150's note carries the date; the citation points at the wrong document.
- Fix: "[^3]" to "[^3,7]" in that sentence and in the events row.

### A1-6 MINOR, Colorado: 14 April 2026 is the report date, not a dated FEMA decision
- Page text: FAQ 6 "For the 2025 Lee and Elk fires FEMA refused aid and, on April 14, 2026, the appeal [^9]."; #hazards "FEMA first denied the request in December 2025 and denied the appeal on April 14, 2026 [^9]"; events row "April 14, 2026 | FEMA denies the appeal ...".
- Reproduction: KUNC (published 14 Apr 2026) says "FEMA has denied Colorado's appeal" and "When Colorado's initial request was denied last December"; it gives no date for the appeal decision. ST line 127's note asserts "denied the appeal 14 Apr 2026" beyond the document.
- Fix (deletions): FAQ 6 delete ", on April 14, 2026," ("refused aid and the appeal"); #hazards delete " on April 14, 2026" (the sentence already opens "KUNC reported on April 14, 2026"); events row text to "KUNC reports FEMA's denial of the appeal for the 2025 fires and flooding" or delete the row.

### A1-7 MINOR (ruling 10), Denver: two ACS products of one measure for one geography
- Page text: register rows "Median household income ... (B19013)" $105,762 (2020 to 2024, five-year, [^8]) and "Median household income ... (B19013), one-year" $108,046 (2024, one-year, [^14]), both on cbsa-19740.
- Reproduction: both values equal data/markets/series/acs5_median_hh_income.json and acs1_median_hh_income.json for cbsa-19740 (no flag, not null). A scan of every src/pages file for a geo carrying the same measure in both acs1_ and acs5_ markers finds only this pair on the whole site. Ruling 10 says never two vintages of one series on one page; GEO-5 D20 applied it to two population vintages. The two products of B19013 read as one series in two vintages.
- Fix: delete the one-year row; source 14 (ACS 1-Year, cited only by that row) then goes too, citations renumbered by the integrator. Denver register falls to 8 counted; Denver 54 (46 research, 8 register).

### A1-8 MINOR, Denver: Cherry Creek construction is "approximately 439,100 sf" in the document
- Page text: "counts 439,100 square feet under construction in Cherry Creek across four projects" and table "439,100 sq ft".
- Reproduction: Cushman and Wakefield MarketBeat Denver Office Q3 2026 (15 Oct 2026): "four projects underway totaling approximately 439,100 sf". MT line 49 dropped "approximately".
- Fix: "counts 439,100 square feet" to "counts approximately 439,100 square feet" (restores the source's qualifier). No count change.

### A1-9 MINOR (I60(b)), Denver: a comparison in words without its values
- Page text (#lenders): "both the industrial and the retail sales totals in the supply section rose sharply over the year in Q3 2026."
- Reproduction: the values (80.5%, 95.7%) are not in that sentence; "rose sharply" is a characterization without the inputs beside it.
- Fix: delete the sentence's second clause, or the sentence "Investment sales are the clearest sign ... in Q3 2026." whole.

### A1-10 MINOR (I64, ruling 4; doubtful rows), Colorado: DEN passenger counts
- Page text: "Denver International Airport handled 82,427,962 passengers in 2025, a record, of whom 4,867,484 were international passengers [^23]." Both count on the state page.
- Reproduction: values confirmed (Aviation Industry News). They are one facility's traffic, inside the Denver page's five counties; the pre-count held ST 164 and 165 as doubtful and outside its harshest stack. The page argues the airport serves the whole state.
- Fix (integrator's call): nocount both values; Colorado would then be 90 (81 research). Not applied in my count below.

### A1-11 MINOR (research hygiene), Colorado: place names beyond the research rows
- Page text: "Longmont's Resilient St. Vrain project", "Coal Creek channel restoration and flood control in Erie".
- Reproduction: MT lines 162 and 163 carry neither town. FEMA R8-26-NR-025 (15 Sep 2026) prints "the Longmont Resilient St. Vrain project" and "the Erie Coal Creek channel restoration", so the document carries them; recorded, no edit needed.

## Integrator items tested, no finding
- Colorado hero "births numbered 65,380, the most since 2017": ST line 13 ("the highest since 2017"); DOLA bulletin (27 Jan 2026): "65,380 ... a 4.6% increase ... and is the highest amount since 2017." Confirmed, with 6,012,561, 0.4%, 12,100, 15,356 and 3,256.
- Description "12,100 net lost to other states to June 2025": DOLA prints "12,100 more domestic migrants left Colorado than arrived between July 1, 2024 and June 30, 2025." Correct. The meta description carries no citation by design (I89).
- Five Denver figures taken from What or Note cells: each is printed by the cited document for that period. 38.1%: CBRE downtown "direct vacancy increased 150 bps to 38.1%". $236,593: CBRE multifamily "down 2.3% against the $236,593 average last quarter". $0.26: Cushman industrial "increased $0.26 per square foot (psf) QOQ". 20.1 million and 17.6 million: Visit Denver Key Data "20.1 million overnight visitors and 17.6 million day visitors" (the release's own parts sum to 37.7 against its 37.6; the page repeats the release and does not add them).
- BLS borderline rows: only the regional Colorado page is printed (ST lines 28 to 30: 2,973.8, 3,047.4, 131.9, up 0.4%), all confirmed seasonally adjusted and preliminary for September 2026; no release date on the page; counted under D12 / I77(c). Its printed heading is "Colorado"; the source title "BLS Mountain-Plains Information Office: Colorado" is the research's (I176), probably descriptive. No MT area-page row (4.3%, 1,645.7 and so on) is printed on either page.
- Discontinued FRED metro GDP rows (Denver $311,876.352 million; Colorado Springs, Fort Collins, Boulder, Greeley, Pueblo, Grand Junction): values dated 4 Dec 2024 for 2023 and labelled discontinued on the page. A FRED search finds no live Denver metro total GDP series (only discontinued NGMP, RGMP, QGMP), so no newer vintage of the same series is in reach (ruling 10 not engaged).
- Source titles with a dash replaced by a comma: confirmed on the documents. BLS prints "County Employment and Wages in Colorado" and "First Quarter 2026" joined by an em dash, and "Occupational Employment and Wages in Denver-Aurora-Centennial" and "May 2025" the same way. The pages use the research's comma form, which I176 requires and gate 10 forces. No edit. (FRED titles carry the series id in parentheses as the research gives them.)
- Denver's register "9 of 9 counted" against 10 markers: the uncounted marker is cbsa-19740.acs5_renter_occupied, 439,123. Not taken by another page (no hit in the repeat index). pagecheck's own-page check drops it: at four significant digits it rounds to 439,100, the page's own research figure (Cushman's Cherry Creek construction, counted first), so `own.has(key)` is true. The two are different facts; the drop is a conservative false match and costs nothing below the cap.
- Register values: all 19 markers (9 Colorado on `co`, 10 Denver on `cbsa-19740`) equal data/markets/series values; none null, none carries an `f` flag (acs5_pop65 carries only an MOE note).

## Figures re-derived (value, citation, research row, document check)

Colorado (36):
| Value | Cite | Research row | Document |
|---|---|---|---|
| 6,012,561 | 1 | ST 11 | DOLA, confirmed |
| 0.4% (growth, context) | 1 | ST 12 | DOLA, confirmed |
| 65,380; 4.6%; since 2017 | 1 | ST 13 | DOLA, confirmed |
| 12,100 | 1 | ST 14 | DOLA, confirmed |
| +15,356 | 1 | ST 15 | DOLA, confirmed |
| +3,256 | 1 | ST 16 | DOLA, confirmed |
| 2,973.8 thousand; 0.4% | 12 | ST 30 | BLS Colorado page, confirmed |
| 3,047.4 thousand | 12 | ST 28 | BLS Colorado page, confirmed |
| 131.9 thousand | 12 | ST 29 | BLS Colorado page, confirmed |
| 2,848,514; -0.7% | 2 | ST 31 | BLS QCEW, confirmed |
| $1,774; 5.4% | 2 | ST 32 | BLS QCEW, confirmed |
| 301,647; $1,437 | 2 | MT 92, 93 | BLS QCEW, confirmed |
| 167,827; $1,627; 11.5%; largest of nine | 2 | MT 130, 131 | BLS QCEW, confirmed |
| 185,013; $2,107 | 2 | MT 155, 156 | BLS QCEW, confirmed |
| 122,224; $1,446 | 2 | MT 180, 181 | BLS QCEW, confirmed |
| 60,303; $1,120 | 2 | MT 198, 199 | BLS QCEW, confirmed |
| 66,300; $1,178 | 2 | MT 215, 216 | BLS QCEW, confirmed |
| 35,814; $1,316; 19,181; $1,623; 23,889; $1,248 | 2 | MT 228 to 235 | BLS QCEW, confirmed |
| $304 million | 17 | ST 67 | Vail Daily, confirmed ("$304 million decrease by the end of the 2025-26 fiscal year compared to ... September") |
| $87 million, $850 million, 50% (nocount) | 17 | ST 68, 66, 70 | Vail Daily, confirmed |
| $29.2 billion; about 2% | 3 | ST 150 | KJCT, confirmed |
| 96.8 million; 1.4% | 7 | ST 151 | SnowBrains, confirmed |
| 187,860; 0.6% | 7 | ST 152 | SnowBrains, confirmed |
| $1.91 billion; 1.9% | 7 | ST 154 | SnowBrains, confirmed |
| $14.2 billion; 48.5% | 7 | ST 155 | SnowBrains, confirmed (A1-4) |
| 82,427,962; 4,867,484; 5.9% | 23 | ST 164, 165 | Aviation Industry News, confirmed (A1-3, A1-10) |
| more than $784,000 | 8 | ST 122 | FEMA R8-26-NR-032, confirmed |
| more than $90M, $28M, $62M (nocount) | 36 | ST 123 to 125 | FEMA R8-26-NR-025, confirmed |
| more than $8M; more than $2.6M (nocount) | 36 | MT 115, 116 | FEMA, confirmed (embankments included) |
| $13.9M, $14M, $2.4M, $1.7M, $1M (nocount) | 36 | MT 161 to 165 | FEMA, confirmed (A1-11) |
| more than $1.8M Kersey (nocount) | 36 | MT 185 | FEMA, confirmed |
| almost $14 million (nocount) | 9 | ST 128 | KUNC, confirmed |
| $194/SF; 391,462 SF; $10.74; 357,000; 290,000; 61,000 | 5, 4 | MT 98 to 112 | research rows read; spot-checked by the pre-count (#12, #17), not refetched |
| 609,250.7; 462,626.5 | 15, 16 | ST 45, 46 | research rows; pre-count #7 confirmed 609,250.7 |
| 53,092.641 and the five other metro GDP values | 44 etc. | MT 117 to 220 | rows read; series family checked on FRED (discontinued, no live successor) |
| $564,000; 34,082; 853.19 | 20 to 22 | ST 54, 55, 57 | rows read, not fetched |

Denver (31):
| Value | Cite | Research row | Document |
|---|---|---|---|
| 40.1%; 150 bps | 1 | MT 42 | CBRE downtown, confirmed |
| 38.1% | 1 | MT 42 (What) | CBRE downtown, confirmed |
| -483,000 | 1 | MT 44 | CBRE downtown, confirmed |
| $41.00; -2.2% | 1 | MT 43 | CBRE downtown, confirmed |
| 293,000; 61% (nocount, I64) | 1 | ST 174 / MT 44 | CBRE downtown, confirmed |
| -161,000 | 6 | MT 37 | CBRE office, confirmed |
| 320,000 | 6 | MT 37 (What) | CBRE office prints "more than 320,000" (A1-1) |
| 461,000; -36.4%; Cherry Creek | 6 | MT 40 | CBRE office, confirmed |
| $33.80 | 9 | MT 47 | Cushman office, confirmed |
| 439,100; four projects | 9 | MT 49 | Cushman office, "approximately" (A1-8) |
| $1,776; 0.6%; -2.9% | 3 | MT 66 | CBRE multifamily, confirmed |
| 7,346 | 3 | MT 67 | CBRE multifamily, confirmed |
| 6,481; 12.0% | 3 | MT 68 | CBRE multifamily, confirmed |
| $231,212; 2.3%; $236,593 | 3 | MT 70 | CBRE multifamily, confirmed |
| 5.74%; 6.84% | 2 | MT 71 | Matthews multifamily, confirmed |
| 5.36% | 2 | MT 72 | Matthews multifamily, confirmed |
| 15,493 | 2 | MT 73 | Matthews multifamily, confirmed |
| 5,902; 58.0% | 2 | MT 74 | Matthews multifamily, confirmed (CoStar credit absent, A1-2) |
| 1.89 million | 11 | MT 75 | Matthews industrial, confirmed (charts credit CoStar Group) |
| $10.23; $0.26 | 10 | MT 57 | Cushman industrial, confirmed |
| $364.7 million; 80.5% | 10 | MT 60 | Cushman industrial, confirmed |
| $20.28; 0.5% | 18 | MT 62 | CBRE retail, confirmed |
| $293.2 million; 95.7% | 18 | MT 64 | CBRE retail, confirmed |
| 37.6 million (record, domestic) | 5 | MT 76 | Visit Denver, confirmed |
| 20.1 million; 17.6 million | 5 | MT 76 (Note) | Visit Denver, confirmed |
| 73,200 (metro area) | 5 | MT 78 | Visit Denver, confirmed |
| 551,034; -1.3%; $2,354; 4.4% | 4 | MT 18, 19 | BLS QCEW, confirmed |
| 339,426; $1,929; 242,964; $1,484; 240,128; $1,753; 147,131; $1,913 and changes | 4 | MT 20 to 27 | BLS QCEW, confirmed |
| $39.28 | 12 | MT 17 | BLS OEWS Denver, confirmed |
| $311,876.352 million (2023) | 13 | MT 80 | FRED NGMP19740, confirmed; last updated 4 Dec 2024 |
| 3,599 units; 13,365 listings | 15, 17 | MT 29, 34 | FRED, confirmed (unit label "Units"; updated 28 May 2026 and 1 Oct 2026) |

Other rules checked: every printed number on both pages has a dated source in the research or the register except the dates in A1-3 and A1-6; no research-computed sum is printed (I55); single-property values (TIAA 293,000 and 61%, the Colorado Enterprise Fund figures, HB values and statute numbers) are nocount (I64); one vintage per series except A1-7; no figure is attributed to a source that lacks it except A1-1 (qualifier), A1-2 (credit), A1-3 and A1-5 (dates).

## Counted figures after my confirmed findings
- /states/colorado/: 92 (83 research, 9 register) after A1-4. With A1-10 also applied: 90 (81 research, 9 register).
- /states/colorado/denver/: 54 (46 research, 8 register) after A1-7. A1-1, A1-2, A1-8 and A1-9 change no count.
- Floors (A6): READY 30 in all with 20 research, landing 25 with 15: both pages hold on every reading above.

Tally: BLOCKER 0; MAJOR-FACTUAL 4 (A1-1 to A1-4); MAJOR-NONFACTUAL 0; MINOR 7 (A1-5 to A1-11).
