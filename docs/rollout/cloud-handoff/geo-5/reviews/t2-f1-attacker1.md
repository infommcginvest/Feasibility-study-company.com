# GEO-5 t2 freeze 1, attacker A (figures, dates, floors, research hygiene)

Tranche t2: `/states/virginia/` and `/states/virginia/northern-virginia/`. Frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t2/`. Hashes of both sources and both rendered pages match FREEZE-t2-f1.txt (shasum run). The drafts in `drafts/geo-5/pages/` are the same files as the copy's `src/pages/states/` sources (diff empty).

Instruments run: `scripts/qa/pagecheck.py --root . --stage ready --new /states/virginia/,/states/virginia/northern-virginia/ --figures` from inside the copy (state 117 = research 107 + register 10; Northern Virginia 47 = research 37 + register 10, both as the gate output). Register values read from `data/markets/series/*.json`. WebFetch on 23 distinct source URLs (list at the end); no 403, 429, robots refusal or bot check met; www2.census.gov not fetched.

Page source paths below are relative to `drafts/geo-5/pages/`.

## Findings

### A1-1 MAJOR-FACTUAL: the seasonally adjusted permit figure is FRED's own computation, printed to five decimals and attributed to the Census Bureau
- Page: `/states/virginia/`, supply section (`virginia.html`), and source 26.
- Text: "The Census Bureau's permit series, as FRED relays it, counts 2,641 new private housing units authorized in Virginia in September 2026 before seasonal adjustment [^25], and 3,274.12673 units for the same month on the seasonally adjusted series [^26]. A single month is a thin base for a housing study. The adjusted figure removes the seasonal swing, and neither is a full-year total, which a study takes from the annual series for its own county or city." Source 26 publisher: "Federal Reserve Bank of St. Louis (FRED), relaying the U.S. Census Bureau".
- Reproduction: WebFetch https://fred.stlouisfed.org/series/VABPPRIVSA: the value is printed as 3,274.12673 for Sep 2026, "Units, Seasonally Adjusted", updated Oct 27, 2026; the page states that the Federal Reserve Bank of St. Louis seasonally adjusts this series itself (Python statsmodels running X-13ARIMA-SEATS). So the value is on the cited page, but it is not a Census figure "relayed": it is a model output FRED computes, and its five decimals are fractional housing units that no permit office counted. The research row (ST-VIRGINIA line 65, "Original: U.S. Census Bureau") carries the same misattribution; the pre-count flag 6 asked for it "rounded and labelled adjusted", which the page did not do either. The not seasonally adjusted value 2,641 (ST line 64; https://fred.stlouisfed.org/series/VABPPRIV, 2,641, Units, Not Seasonally Adjusted, updated Oct 27, 2026) is right.
- Answer to the integrator's question: yes, 3,274.12673 is what the cited page prints; no, it is not a sensible figure to print (spurious precision on a FRED-made adjustment, under a Census attribution).
- Smallest fix: delete the adjusted clause and source 26 (renumber 27 onward), e.g. old "before seasonal adjustment [^25], and 3,274.12673 units for the same month on the seasonally adjusted series [^26]. A single month is a thin base for a housing study. The adjusted figure removes the seasonal swing, and neither is a full-year total, which" new "before seasonal adjustment [^25]. A single month is a thin base for a housing study, and it is not a full-year total, which". If the verifier prefers to keep the source, the alternative is to relabel source 26's publisher "Federal Reserve Bank of St. Louis (FRED), seasonally adjusted by FRED from U.S. Census Bureau data" and wrap the value in `data-fsc-nocount`, but deletion is cleaner. Count effect: state research 107 to 106.

### A1-2 MAJOR-FACTUAL: "Camden, Currituck and Gates" is OEWS's definition only; the BLS payroll table names Currituck alone and the FHFA and BEA series name no counties
- Page: `/states/virginia/`, metros overview and Hampton Roads section (`virginia.html`).
- Text 1: "BLS, FHFA and BEA publish Hampton Roads as the Virginia Beach-Chesapeake-Norfolk metro, or the Virginia Beach-Norfolk-Newport News metro in FHFA's and BEA's naming, and both versions take in Camden, Currituck and Gates counties in North Carolina [^9]."
- Text 2: "BLS, FHFA and BEA publish the metro with Camden, Currituck and Gates counties in North Carolina included [^9], so every metro-wide figure below includes them and every city figure does not."
- Reproduction: WebFetch of source 8 (https://www.bls.gov/regions/mid-atlantic/data/xg-tables/ro3fx9537.htm, the source of 832.9, 864,565, 164.5 and 53.5): the area footnote lists Gloucester, Isle of Wight, James City, Mathews, Surry and York counties, nine Virginia cities "and Currituck County in North Carolina"; Camden and Gates are not named. WebFetch of source 9 (OEWS, July 10, 2026) does list Camden, Currituck and Gates. WebFetch of https://fred.stlouisfed.org/series/NGMP47260 (source 46): title "VA-NC", no county list. The research (MT line 127 note) says only "MSA includes North Carolina counties"; the three-county list comes from the pre-count's OEWS check and was extended to BLS payrolls, FHFA and BEA without support. The payroll figures "below" therefore do not include Camden and Gates on their own source's definition.
- Smallest fix: Text 1 new "BLS, FHFA and BEA publish Hampton Roads as the Virginia Beach-Chesapeake-Norfolk metro, or the Virginia Beach-Norfolk-Newport News metro in FHFA's and BEA's naming, and each version reaches into North Carolina: the occupational survey names Camden, Currituck and Gates counties [^9] and the payroll table Currituck County [^8]." Text 2 new "BLS, FHFA and BEA publish the metro with North Carolina counties included [^8,9], so every metro-wide figure below includes them and every city figure does not." (keeps the North Carolina label the integrator requires; drops the unsupported list).

### A1-3 MAJOR-FACTUAL: a Hampton Roads metro-wide figure printed without its North Carolina label
- Page: `/states/virginia/`, FAQ 3 (`virginia.html` front matter).
- Text: "In the two largest markets on this page the nearest count is BLS's government line for September 2026, 116.1 thousand jobs in Richmond [^35] and 164.5 thousand in Hampton Roads [^8], and that line holds federal, state, county and city employers together."
- Reproduction: 164.5 thousand is MT line 129, "Government employment, same MSA" (Virginia Beach-Chesapeake-Norfolk, VA-NC); WebFetch of ro3fx9537 confirms 164.5 for Sep 2026 (p) and the Currituck County, NC footnote. The page defines Hampton Roads as "the Virginia side" of that metro, so "164.5 thousand in Hampton Roads" states a VA-NC count as a Virginia-side one. Every other Hampton Roads metro-wide figure on the page carries the label (832.9 and 864,565 "North Carolina counties included"; 41,190 and $30.83 "again for the whole metro"; 388.95 "North Carolina counties included"; 127,459.149 in the same sentence). All Winchester metro-wide figures (70.8 thousand in FAQ 5 and the section; 373.01; 9,988.848) carry the West Virginia label; no finding there.
- Smallest fix: old "and 164.5 thousand in Hampton Roads [^8]" new "and 164.5 thousand in the Hampton Roads metro, which reaches into North Carolina [^8]".

### A1-4 MAJOR-FACTUAL (I60): the two data center cost estimates are compared in words
- Page: `/states/virginia/`, power section (`virginia.html`).
- Text: "Both outlets were reporting on the commission's work, and they print different amounts."
- Reproduction: $928.6 million and $685 million sit in the two previous sentences, each with its own citation, not in this one; "they print different amounts" is a comparison of two sourced values whose inputs are not in its sentence (I60 b). WebFetch of the H&K alert (August 20, 2026): "data centers saved $928.6 million in sales taxes in FY 2023 alone", from "A December 2024 report by Virginia's Joint Legislative Audit and Review Commission (JLARC)"; no state or local split stated. WebFetch of Governing (Kate Seltzer, The Virginian-Pilot, Nov. 26, 2025): "The state lost out on $1 billion through the data center exemption in fiscal 2024, up from $685 million in fiscal 2023", attributed to JLARC's annual economic incentives report. So both figures are on their sources for FY2023 and "both outlets were reporting on the commission's work" is true (two different JLARC reports). The FAQ 2 sentence ("is printed two ways, $928.6 million ... [^1] and $685 million ... [^6]") has both values and both citations in one sentence and passes I60. ST line 89 (row 45) is right to call the $685 million FY2023.
- Smallest fix: old "Both outlets were reporting on the commission's work, and they print different amounts." new "Both outlets were reporting on the commission's work."

### A1-5 MAJOR-FACTUAL (I60): the two Northern Virginia brokers' figures are compared in words
- Page: `/states/virginia/northern-virginia/`, supply section (`virginia/northern-virginia.html`).
- Text: "Their figures for the same quarter therefore differ, and this page states each broker's number in its own sentence, never averaged, ranked or set against the other."
- Reproduction: the CBRE and C&W values ($37.80 and $36.45; +355,000 and +413,800; $18.10 and $18.73) are printed in later sentences, never in this one; "differ" is the comparison the integrator asked to be absent, and the sentence contradicts itself ("never ... set against the other"). Every other broker passage on the page keeps each broker in its own statement (FAQ 3 and FAQ 7, both h3 pairs, the table). WebFetch of the C&W office MarketBeat (10/8/2026) and CBRE industrial figures (September 30, 2026) confirm the values.
- Smallest fix: old "Their figures for the same quarter therefore differ, and this page states" new "This page states".

### A1-6 MAJOR-FACTUAL (I60): Richmond's two broker vacancy rates are compared without being printed
- Page: `/states/virginia/`, Richmond section (`virginia.html`).
- Text: "The two brokers define the Richmond office market in their own ways and report different vacancy rates for the quarter, so each reading here stays with its broker, and an office study names the survey it relies on."
- Reproduction: the two vacancy rates (CBRE 12.3%, MT line 98; C&W 12.5%, MT line 101) are `taken` and not printed anywhere on the page, and the sentence carries no citation. WebFetch of CBRE Richmond Office Figures Q3 2026 confirms 12.3%, $22.18 and "negative 281,000 sq. ft.". A bare comparison of unprinted values is I60 (b).
- Smallest fix: old "in their own ways and report different vacancy rates for the quarter, so each" new "in their own ways, so each".

### A1-7 MAJOR-FACTUAL (I60, I69): Charlottesville's two population sets are compared, and one side is not in the research
- Page: `/states/virginia/`, Charlottesville section (`virginia.html`).
- Text: "the same article prints the Weldon Cooper Center's estimates, which differ for both [^56]."
- Reproduction: the Weldon Cooper values are not printed on the page. The research holds only the Albemarle value (MT line 210 note, 119,479); the city value (46,923) is known only from the pre-count's own fetch (PRECOUNT spot check 12), which cannot support a statement under I69. "Differ" compares unprinted values (I60 b).
- Smallest fix: old "the Weldon Cooper Center's estimates, which differ for both [^56]" new "the Weldon Cooper Center's estimates as well [^56]".

### A1-8 MINOR (I60): Richmond office against industrial absorption in words
- Page: `/states/virginia/`, Richmond section.
- Text: "Industrial space moved the other way."
- Reproduction: the conclusion compares CBRE office absorption (-281,000, previous paragraph, [^39]) with industrial (668,000, next sentence, [^40]); neither value is in the sentence. True on the sources, but I60 (b).
- Smallest fix: delete the sentence.

### A1-9 MINOR: "not seasonally adjusted" is not on the source for the statewide unemployed count
- Page: `/states/virginia/`, economy section.
- Text: "FFXnow, reporting state data released on April 16, 2026, gave 173,934 unemployed Virginians for January 2026, not seasonally adjusted and preliminary [^14]."
- Reproduction: WebFetch of the FFXnow article (April 20, 2026): "Statewide, the number of unemployed was up 18.7% to 173,934"; "All January 2026 figures are preliminary"; "non-seasonally-adjusted" is said only of the county and national rates. The research row (ST line 35) added "not seasonally adjusted" for the statewide figure; the value, date and release date (April 16, Virginia Department of Workforce Development and Advancement) are right.
- Smallest fix: old "for January 2026, not seasonally adjusted and preliminary [^14]" new "for January 2026, preliminary [^14]".

### A1-10 MINOR: the BLS Northern Virginia region reads as exhaustive
- Page: `/states/virginia/northern-virginia/`, economy section.
- Text: "for a region that also takes in Fauquier, Stafford and Spotsylvania counties and the city of Fredericksburg [^8]."
- Reproduction: WebFetch of ro3fx9538: the footnote adds Clarke, Culpeper, Rappahannock and Warren counties and the cities of Fairfax, Falls Church, Manassas and Manassas Park; 1,647,917 employed, Sep 2026 (p), not seasonally adjusted, confirmed. The research note (MT line 26) says "and others"; the page dropped it.
- Smallest fix: old "and the city of Fredericksburg [^8]" new "and the city of Fredericksburg, among others [^8]".

### A1-11 MINOR (I64, judgment for the verifier): Alexandria's +377,800 sf is one occupier's move and is counted
- Page: `/states/virginia/northern-virginia/`, FAQ 3, supply section and table.
- Text: "net absorption of +377,800 square feet in Alexandria that it attributes to the National Science Foundation taking space on Dulany Street [^3]"; "+377,800 in Alexandria, a city figure it attributes to the National Science Foundation occupying space at 401 Dulany Street [^3]"; table row "Cushman &amp; Wakefield, net absorption, Alexandria city (driven by one occupier) | +377,800 sf".
- Reproduction: WebFetch of the C&W office MarketBeat: "Alexandria posted the strongest quarterly performance with positive 377,800 sf", "as the National Science Foundation occupied 386,600 sf at 401 Dulany St." The single occupancy (386,600) is larger than the city's whole net figure, so the rest of Alexandria was net negative and the counted value describes one property; the page itself says so ("treats a quarter made by one federal occupier as that occupier's quarter"). The pre-count counted it only by its own override (MT 57) and removed it in its harshest stack. Under I64 it should be cited but not counted.
- Smallest fix: wrap "+377,800" in `<span data-fsc-nocount>` at all three uses. Count effect: Northern Virginia research 37 to 36.

## Items the integrator named, tested

- 3,274.12673: A1-1.
- 8.88 million: WebFetch of the Weldon Cooper page (February 24, 2026): "Virginia's population reached 8.88 million as of July 1, 2025". The description ("8.88 million people on July 1, 2025"), the stat band ("Virginia residents on July 1, 2025, by the Weldon Cooper Center's estimate [^5]") and the body ("8.88 million Virginia residents on July 1, 2025 ... published on February 24, 2026 [^5]") carry the same value, date and publisher (ST line 10). The FRED 8,880.107 thousand (ST line 11) is not printed. One population source per geography: Weldon Cooper for the state, Census Vintage 2025 for Charlottesville and Albemarle (MT 209, 210), Winchester's Vintage 2024 value left out. No finding.
- Data center estimates: values and FY2023 attributions confirmed on both sources; compared once in words (A1-4); FAQ 2 is clean.
- FRED relays: 35 of the state's 77 sources and 8 of Northern Virginia's 19 (43). Opened: VABPPRIVSA (A1-1), VABPPRIV (2,641), BPPRIV051059 (2,862, title "Structures", unit label "Units", updated May 28, 2026), NGMP47260 (127,459.149, 2023, "(DISCONTINUED)", updated Dec 4, 2024). All values match; the structures/units mismatch is disclosed on both pages.
- Hampton Roads and Winchester labels: A1-2 and A1-3; Winchester is clean.
- Northern Virginia margin: see Floors.
- Register: the ten Northern Virginia pairs (co-51059, co-51013, co-51107, co-51153, co-51510 by acs5_median_hh_income and acs5_median_home_value) and the ten `va` pairs equal the series files' `v` values exactly; none is in `nulls`, none carries an `f` flag; all acs5 are "2020-2024 (ACS 5-year)", BEA "calendar year 2024".
- "about 61%": WebFetch of CBRE Northern Virginia Industrial Figures Q3 2026 (September 30, 2026): "with about 61% of newly delivered space still available"; research MT line 63 carries it. It is dated and sourced (I86 met); the nocount wrap is not required by any rule but is harmless (it could count, +1, if the margin ever needed it). No finding.
- Broker conflicts: no average, rank or arithmetic anywhere; two comparisons in words (A1-5, A1-6). FAQ 3's "$36.76 in the city of Alexandria against an average of $36.45" is one broker's two values in one sentence with the citation (passes I60).

## Re-derived figures

Each: value | citation | research row | result. "Opened" means the source URL was fetched in this review and showed the value for that period.

State page (34):
1. 8.88 million | 5 | ST 10 | opened, confirmed
2. 138,044,772 MWh | 2 | ST 78 | opened (EIA, released Nov 10, 2025, data 2024)
3. 10.62 cents per kWh | 2 | ST 79 | opened
4. 29,147 MW | 2 | ST 80 | opened
5. $928.6 million | 1 | ST 81 | opened (H&K Aug 20, 2026, JLARC Dec 2024)
6. $685 million | 6 | ST 89 | opened (Governing Nov 26, 2025, FY2023)
7. 22,400 | 3 | ST 44 | opened (ARLnow Jan 8, 2026: statewide, year over year, 11.5%)
8. 173,934 | 14 | ST 35 | opened (A1-9 on the qualifier)
9. $1,665 | 4 | ST 25 | opened (BLS Sep 2, 2026)
10. 324,758 | 4 | ST 26 | opened
11. 4,250.6 thousand | 13 | ST 20 | research row, Economy at a Glance (borderline c), not opened
12. 4,461.2 thousand | 13 | ST 23 | as 11
13. 197,863; 196,049; 43,606; 33,616 | 15 | ST 27 to 30 | research rows, not opened
14. 807,925.0 million | 16 | ST 54 | research row
15. 639,147.7 million | 17 | ST 55 | research row
16. 46.6 million | 18 | ST 126 | opened (WDBJ7 Aug 11, 2026, domestic and international)
17. 2,641 | 25 | ST 64 | opened
18. 3,274.12673 | 26 | ST 65 | opened, A1-1
19. $455,953; 26,222; 11,204 | 27 to 29 | ST 66 to 68 | research rows
20. 780.93 | 30 | ST 63 | research row
21. 41,190; $30.83 | 9 | MT 133, 132 | opened (OEWS July 10, 2026)
22. $29.13 | 21 | MT 175 | research row
23. $1,868; 167,696 | 4 | MT 92, 91 | opened
24. $1,215; 180,830; 142,220; 105,954; $1,531 | 4 | MT 138, 135 to 137, 140 | opened
25. 832.9 thousand; 864,565; 164.5 thousand; 53.5 thousand | 8 | MT 127 to 131 | opened (A1-2, A1-3 on scope)
26. 127,459.149 million | 46 | MT 149 | opened
27. 2,156; 6,680 | 47 | MT 152, 153 | opened (C&W Hampton Roads multifamily Q3 2026; the page shows no date, research dates it by listing, c)
28. $22.18; 281,000 | 39 | MT 99, 100 | opened (negative absorption, printed with its minus sign)
29. 67,038; 37,252; 40,208; 47,378; 44,767; 31,957; 25,663 | 4 | MT 176, 177, 196, 220, 235, 254, 255 | opened
30. 70.8 thousand | 36 | MT 253 | opened (Winchester VA-WV EAG, extracted Oct 28, 2026; WV county not named there)
31. 4,922,994; 4,892,594 | 11, 12 | MT 116, 162 | research rows (pre-count opened MT 162)
32. 724.2 thousand; 116.1 thousand; 123.7 thousand; 708,583 | 35 | MT 85, 88, 89, 87 | research rows
33. 44,388; 118,356 | 56 | MT 209, 210 | research rows (A1-7 on the Weldon Cooper clause)
34. $603.5 million; $427.7 million; 7,217 | 34 | MT 205, 206, 208 | research rows

Northern Virginia (all 37 research figures; the page's 37 equal the pre-count's 37 free ids, MT lines 11 to 16, 18 to 20, 28, 30, 33, 35 to 41, 43, 44, 47, 51 to 57, 61, 63, 65, 66, 73 to 76):
- 622,779; 206,071; 146,398; 171,969; 79,023; $2,451; $1,292; $2,901; $1,944 | 1 | MT 11 to 16, 18 to 20 | opened: all match, and every direction word ("fewer", "higher", "above", "below") matches the release's printed over-the-year change (-2.1, 2.8, 1.0, -4.5, -2.6; wages +3.4, +2.5, +8.8, +6.1). Loudoun's wage $1,762 is on the release and not printed (taken), as the page says.
- 1,647,917 | 8 | MT 28 | opened (A1-10)
- 23,749 | 9 | MT 30 | opened (17,744 a year earlier, so "more" is the article's own)
- 2,862; 1,340; 1,309 | 11, 7, 12 | MT 33, 35, 36 | 2,862 opened; others research rows
- $724,900; $782,450; $599,995; $619,648; $534,950 | 13, 6, 5, 14, 15 | MT 37 to 41 | research rows (pre-count opened MT 37)
- +355,000; 941,000; $37.80 | 4 | MT 43, 44, 47 | research rows (pre-count opened MT 43)
- $36.45; $40.63; $36.76; $35.44; $28.87; +413,800; +377,800 | 3 | MT 51 to 57 | opened, all match (A1-11)
- $18.10; 283,000 | 16 | MT 61, 63 | opened
- $18.73; +168,600 | 17 | MT 65, 66 | research rows
- 29.01 million; 10.53 million; 24.89 million; more than 53.9 million | 2 | MT 73 to 76 | opened (MWAA Feb 24, 2026; both Dulles values called records; Reagan down 5.3% from 26.29 million)

Dates: every printed number on both pages carries a dated source (I77, I86); the nocount rule values ($0.011 per kWh, $600 million, $150 million, 50 new jobs, 1.5 times, 4.3%) are dated by publication (H&K Aug 20, 2026; Governing Nov 26, 2025) and confirmed on the pages. The Governing article does not itself call 4.3% the "state portion", but calls it the rate of "the state's sales and use tax"; not raised. Source titles equal the research's titles for every research source (scripted check); the four register and SBA sources are not research titles by design.

## Floors after my findings

Applying A1-1 (state minus one) and A1-11 (Northern Virginia minus one); no other finding removes a counted figure.
- `/states/virginia/`: 116 counted (106 research, 10 register). READY 30/20 and landing 25/15 hold.
- `/states/virginia/northern-virginia/`: 46 counted (36 research, 10 register). READY 30/20 holds (36 research); landing 25/15 holds. On the pre-count's harshest stack (secondary, borderline, scope, both sides of every conflict, override) it stays at 20 research, 30 in all, because that stack already removed +377,800; the margin is unchanged and still sits exactly on the floor. If the verifier refutes A1-11, the counts are 47 (37 research). Unwrapping "about 61%" would add one.

## Sources opened (23 URLs, 24 fetches, no door closed)
coopercenter.org 2025 estimates; FRED VABPPRIVSA, VABPPRIV, BPPRIV051059, NGMP47260; governing.com data center article (twice); hklaw.com alert; arlnow.com ?p=395804; ffxnow.com April 20 article; bls.gov county employment and wages Virginia; bls.gov ro3fx9537 (twice) and ro3fx9538; bls.gov OEWS Virginia Beach; bls.gov EAG Winchester; eia.gov Virginia profile; vpm.org federal jobs article; wdbj7.com tourism article; mwaa.com 2025 passengers; cushmanwakefield.com Northern Virginia office and Hampton Roads multifamily; cbre.com Northern Virginia industrial and Richmond office.

## Count by severity
BLOCKER 0; MAJOR-FACTUAL 7 (A1-1 to A1-7); MAJOR-NONFACTUAL 0; MINOR 4 (A1-8 to A1-11).
