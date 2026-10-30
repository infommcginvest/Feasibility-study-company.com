# GEO-5 t4 freeze 1, attacker A (figures, dates, floors, research hygiene): /states/north-dakota/

Reviewed: frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t4/` (rendered `states/north-dakota/index.html`, sha256 25e9ec7a...2de91; source `src/pages/states/north-dakota.html`, sha256 16ba0e93...b020f0, byte equal to `drafts/geo-5/pages/north-dakota.html`), research `ST-NORTH-DAKOTA.md` and `MT-NORTH-DAKOTA.md` (cited by file line, as the pre-count does), `facts/north-dakota.facts.json`, `facts/north-dakota-PRECOUNT.md`, `GATES-t4-f0.txt`. No metro page stands (all six markets folded).

Fetches: 31 source reads (24 WebFetch, 7 API calls by curl to api.fdic.gov and the OpenFEMA API). No 403, 429, robots refusal or bot check was met; nothing was worked around; www2.census.gov was not touched.

Pagecheck rerun from inside the copy (`scripts/qa/pagecheck.py --root . --stage ready --figures /states/north-dakota/`): 64 counted (research 56, register 8/8), 7,178 words, overlap 0.51%; equal to gate 3 in `GATES-t4-f0.txt`.

## Findings

### A1-1 BLOCKER: "two-year" moratorium, a figure the cited article does not carry
- Page: /states/north-dakota/, #rules, "Data centers and other large power users".
- Text: "In October 2026 Harmony Township, also in Cass County, had before it a proposed two-year moratorium on data centers, concerning Geronimo Power's Harmony Energy Park and its two data center buildings, and cancelled the special meeting it had set for October 22 [^33]."
- Reproduction: research ST line 142 records "proposed 2-year moratorium" from the Grand Forks Herald article of 2026-10-23. WebFetch of that URL, asked to search the full text for "two-year", "2-year", "two years" and "year": no length or duration of the moratorium appears in the text, subhead or captions. The only "2-year" is in the URL slug of a linked, different article (`harmony-township-board-to-consider-2-year-data-center-moratorium`), whose link text reads "the proposed moratorium". The article calls it "a moratorium for large developments, including data centers". A value read from a URL slug is not the document's (I176 dropped slug-only titles on the same reasoning), so the figure is attributed to a source that does not carry it (I86). Research hygiene: the row's Value cell was taken from the slug.
- Fix: delete "two-year " (leaving "a proposed moratorium on data centers").

### A1-2 MAJOR-FACTUAL: Baker Hughes's 24 rigs is not dated "July" by the article
- Page: #bakken, paragraph 3.
- Text: "and Baker Hughes's monthly average for July was <span data-fsc-nocount>24</span> rigs [^1]."
- Reproduction: research ST line 83 gives Period "Jul 2026". WebFetch of the Minot Daily News article (2026-08-25): the director "said 24 rigs are actively working, according to the Baker Hughes number", followed by "the Baker Hughes number is a monthly average number". The article attaches July to the national count ("July was at approximately 588"), not to North Dakota's 24. The month is the researcher's inference; the source carries the value but not that period.
- Fix: delete "for July" ("and Baker Hughes's monthly average was 24 rigs [^1]"). The value stays dated by the article's publication date (I77(a)) and stays nocount.

### A1-3 MAJOR-FACTUAL: Fort Berthold's 3,040 active wells are not tied to June by the article
- Page: #overview paragraph 2 and #bakken paragraph 4 (counted figure).
- Text: "Producing wells reached 19,961 the same month, another all-time high, and 3,040 wells were active on the Fort Berthold Reservation [^1]." and "On the Fort Berthold Reservation, 3,040 wells were active in June 2026 and the report counted a single rig working there [^1]."
- Reproduction: research ST line 86 gives Period "Jun 2026". WebFetch of the article: "production is up slightly with 160,651 barrels of oil produced in June", then "The total number of active permits was 132, an increase from last month, and 3,040 wells were active." June is attached to the production figure; the well count carries no month. The reading is plausible (same monthly report) but the source does not state the period the page prints. Lower confidence than A1-2; the verifier may grade it MINOR.
- Fix: in #bakken delete "in June 2026" ("3,040 wells were active and the report counted a single rig working there [^1]"); in #overview delete ", and 3,040 wells were active on the Fort Berthold Reservation" so the value is not placed in "the same month" as 19,961. The value stays printed and counted once in #bakken, dated by the article (count unchanged: pagecheck counts the value once).

### A1-4 MAJOR-FACTUAL: Stacker's Fargo permit count is "metro-level" data; "peak" is the research's own reading
- Page: #supply, paragraph after the listing table.
- Text: "Stacker's reading of Redfin data counted <span data-fsc-nocount>281</span> building permits in Fargo in July 2025, the peak month of its series [^37], and <span data-fsc-nocount>71</span> in Bismarck in August 2025, the peak there [^38]."
- Reproduction: WebFetch of both Stacker articles (2026-05-01). Each carries the methodology note "metro-level permit data is the non-seasonally adjusted total number of permits issued per month." The Fargo metro (Fargo, ND-MN) takes in Clay County, Minnesota (MT line 16 and line 27 notes), which the page says is left out of every Fargo figure (#overview: "the Minnesota side of each is left to the Minnesota page"; #metros lede: "Every figure in these sections is for a North Dakota county or city"). The Fargo article's own table also gives 11.3 permits per 10k population for July 2025 beside 281, a base near 249,000, far above the city (corroboration only; I do not ask the page to print that arithmetic). Research MT line 29 records the Fargo row as "Building permits in Fargo" without the metro label that MT line 78 records for Bismarck ("article labels series metro-level"). Neither article uses the word "peak": both labels come from the research's What-it-measures cells (MT lines 29 and 78), a comparison across the article's months that the research made itself (I55, I59, I60(b)).
- Fix: delete "<span data-fsc-nocount>281</span> building permits in Fargo in July 2025, the peak month of its series [^37], and " and ", the peak there"; rewrite as the smallest deletion leaves it, or delete the sentence and source 37 with it (source 37 is cited only here). The following sentence "Neither article names the government dataset behind it" then needs "Neither article" changed or deleted with it. Count unchanged (both values are nocount).

### A1-5 MINOR: $200.4 million printed as a rise with no end value
- Page: #capital paragraph 1 (counted figure).
- Text: "and it reports that net income rose from $200.4 million in 2024 [^2]."
- Reproduction: WebFetch of the BND release (2026-06-29): "BND reported net income of $231.8 million, up from $200.4 million in 2024". The 2025 value is left off the page because the fact sheet marks it taken by /states/kentucky/ (a value collision, `taken` at facts line 545). "Rose from" with only the base printed is a comparison whose inputs the reader cannot see (I60(b)); the source does make the comparison, so this is form, not substance.
- Fix (verbatim restoration): "and it reports net income of <span data-fsc-nocount>$231.8 million</span>, up from $200.4 million in 2024 [^2]." Or delete the clause (research count 56 to 55).

### A1-6 MINOR: comparisons in words without both values in the sentence (I60(b))
- (a) #bakken h2 "a rig count that rose into August" and #williston "and rig counts that rose between July 13 and August 19, 2026 [^1]". The article does say "a positive change of plus seven on the rig count", but the research (ST lines 81, 82) records only the two counts, and neither sentence prints them. Fix: delete ", and a rig count that rose into August" from the h2; delete "and rig counts that rose between July 13 and August 19, 2026" in #williston (leaving "the June 2026 production and well records [^1]").
- (b) #minot: "Three readings, each below the one before, are a reason to test asking prices against recorded sales before a for-sale or rental study relies on either." Values are in the preceding sentence, not this one. Fix: delete the sentence.
- (c) #fargo: "A listing count higher in September than in May is a signal that a study of homes for sale or rent checks against closed sales before it prices units." Fix: delete the sentence.
- (d) #metros card: "two counties whose wage files sit far apart" (no values on the card). Fix: delete "whose wage files sit far apart" and "two counties" phrase as one clause: "The capital and Mandan across the Missouri."
- (e) #economy: "a wage assumption copied from the statewide average is wrong almost everywhere a project is likely to sit" is a conclusion drawn across six county values. Fix: delete "The table makes one point plainly: a wage assumption copied from the statewide average is wrong almost everywhere a project is likely to sit." (the next sentence prints the values and makes the point).

### A1-7 MINOR: "Director's Cut" and "briefing" are not the article's words
- Page: source 1 publisher field, hero, stats label, FAQ 2, #overview, #bakken, events table.
- Reproduction: the article says "The new natural gas production record was announced Thursday, Aug. 20, during the monthly oil and gas report", presented by the DMR director. It never uses "Director's Cut" or "briefing". Both words come from the research's Note cell (ST line 78: "Original: DMR Director's Cut briefing of 20 Aug 2026"), so the page follows the research; both publishers (DMR as original, Minot Daily News as secondary) are named everywhere the figures appear, as the integrator asked. Recorded for the record; no fix needed unless the integrator wants the article's "monthly oil and gas report".

### A1-8 MINOR: Bismarck metro composition stated without a source
- Page: #bismarck-mandan paragraph 1: "BEA's and FHFA's Bismarck metropolitan area reaches beyond those two counties".
- Reproduction: no research row states the Bismarck MSA's counties (MT lines 73 and 77 say only "Bismarck ND MSA"); the Oliver County fact is in the pre-count's flag 1, not the research. Fix: delete "BEA's and FHFA's Bismarck metropolitan area reaches beyond those two counties, so " leaving "the two figures here that describe the wider area say so" recast, or delete the sentence.

### A1-9 MINOR: the freeze record is empty
- `FREEZE-t4 north-dakota-f1.txt` (note the space in the name) prints blank fields: "source   copy", "rendered /states// ", "src/pages/states tree ", "gates READY ; landing 3,9 site-wide ". No hash ties this copy to the freeze. My readings for the record: source 16ba0e9300ff2efe15882edcaa6b80eeff8e497987e456bf6690f53693b020f0 (draft and copy equal), rendered 25e9ec7ab0f428e326414bb39a45b1d3115f80592dae0a3823f5ec5e2ec2de91, GATES-t4-f0.txt cb4b2dd514e9306ee29c6abab4e26e0e743eb670e1c0b8e9495f926de26e6fcf, GATES-t4-f0-landing.txt bde7af72014e0e174caee786a06e3e0b395c4b1c24821d45f489ab0af2b52d58. Fix: rewrite the freeze record (Alaska's t5 record has the same defect).

### A1-10 MINOR: stats tile reads "3.58B" above "Billion cubic feet"
- Rendered: `stat-num` "3.58<span>B" with label "Billion cubic feet of natural gas produced per day...". The unit letter doubles the label's first word and reads like the $10.7B tile beside it. Fix: drop `"unit": "B"` from the first stat (the label carries the unit).

## The integrator's items, tested

1. Oil and gas via the Minot Daily News: both publishers are named in the hero, the stats label, FAQ 2, #overview, #bakken, the events table and source 1 ("Minot Daily News (reporting the North Dakota Department of Mineral Resources' ... ; secondary)"). Values against the article (fetched twice): 34.583 million barrels and 1.153 million a day, 3.58 BCF a day (record, beating September 2024), May 3.52, 19,961 producing wells (all-time high, up 129), 33 rigs on Aug. 19 and 26 on July 13, 74 completions in July, one rig on Fort Berthold, 3,040 active wells: all printed by the article. Two period attributions are the research's, not the article's: A1-2 (24 rigs "for July") and A1-3 (3,040 "in June").
2. FDIC rows: every printed FDIC value carries the reporting period the research gives ("reporting year 2025"; "2025 Summary of Deposits", "survey-year figure") and sits in nocount. API reproduced: CB_2025_ND ASSET 59,309,013, DEP 51,007,223; SI_2025_ND ASSET 4,765,228; SOD 2025 sums and record counts Burleigh 5,087,586/40, Ward 3,185,567/21, Williams 2,067,624/11, McKenzie 1,365,949/5, Stark 1,967,308/16. Meta prints only an index createTimestamp (2026-09-16, 2026-09-18), no release date, as the page says. Pass under I77(c) with D12's borderline status kept (none counted).
3. Fargo and Grand Forks, North Dakota only: every Fargo-section and Grand Forks-section value is a Cass County, Grand Forks County or Hector International value (BLS county file, FRED county series, NDAC releases). The one Fargo value outside those sections is not: A1-4 (Stacker's metro-level permit count).
4. citypopulation.de: none of the 15 values (200,945; 136,275; 41,175; 103,107; 34,194; 77,963; 25,061; 73,771; 60,365; 40,763; 14,782; 29,522; 6,378; 33,767; 25,870) occurs in the rendered page. Pass.
5. Earlier-period nocount values, each against its own dated source (I86): 3.52 and 129 (MDN 2026-08-25, confirmed); 515.80 and 523.49 (FRED NDSTHPI updated Aug 25, 2026, confirmed); 389.85 (FRED ATNHPIUS13900Q, Aug 25, 2026, confirmed); $517,900 and $486,900 (MEDLISPRI38015, Oct 1, 2026, confirmed); $350,000 and $384,900 (MEDLISPRI38101, confirmed); $469,000 (MEDLISPRI38035, confirmed); 512 and 712 (ACTLISCOU38017, confirmed); 546,787 and 309,337 (Inforum 2026-01-23, confirmed); 46,258 and 23,891 (NDAC 2026-10-21, confirmed); 27,623 (NDAC 2025-04-17, confirmed); 47,277 and 48,387 (MDN 2026-05-14, confirmed: "stabilized at 47,277 in 2024", "the 2020 official census of 48,387"). The article does not say which Census vintage its 2024 value comes from; it reports the release of May 14, 2026, so a reading of 47,277 as Vintage 2025's 2024 value is likely but not printed (ruling 10 risk only; no register value for Minot city is on the page). The one earlier-period value without its stated period in the source is the 24 rigs (A1-2).
6. First-half 2025: only 654,304 is printed (FAQ 3, #airports), cited to the release of July 14, 2025 [^6] (confirmed: "a combined 654,304 passenger boardings"). 654,350 (the 2026 release's comparison) occurs nowhere on the page. The 1.8 percent is attributed to the 2026 release, which prints it. Pass.
7. Source titles with numbers: "North Dakota Airports See 10% Growth in Passenger Boardings in First Half of 2025" (source 6), "... See 20% Passenger Surge ..." (source 29), "Company announces plan for $3 billion data center north of Fargo" (source 32). In the rendered page 10%, 20% and $3 billion occur only in those titles and in the `sba:` equity markers (10%, 20%); no body sentence, stat, table or FAQ prints them; pagecheck's counted list contains none of them. They are the documents' titles verbatim (I176) and are not read as page figures. Pass.

## Re-derived figures (value; citation; research row; result)

Fetched and confirmed on the source for the stated period unless marked:
1. 34.583 million bbl, 1.153 million/day, June 2026; [^1]; ST 78; confirmed.
2. 3.58 BCF/day, June 2026, record; [^1]; ST 79; confirmed.
3. 3.52 (May, nocount); [^1]; ST 79 note; confirmed.
4. 19,961 producing wells, June 2026; [^1]; ST 80; confirmed.
5. 129 (nocount); [^1]; ST 80 note; confirmed.
6. 33 rigs Aug 19, 26 rigs Jul 13 (nocount); [^1]; ST 81, 82; confirmed.
7. 24 Baker Hughes (nocount); [^1]; ST 83; value confirmed, "July" not in source (A1-2).
8. 74 completions July 2026 (nocount); [^1]; ST 85; confirmed.
9. 3,040 Fort Berthold wells; [^1]; ST 86; value confirmed, month not in source (A1-3).
10. $10.7 billion assets, 2025 year end; [^2]; ST 50; confirmed.
11. 4.69% return to state, 2025; [^2]; ST 52; confirmed.
12. $200.4 million, 2024; [^2]; ST 49; confirmed (A1-5).
13. A+ stable, 2025 review; [^2]; ST 54; confirmed.
14. 448.7 thousand Aug 2026, 447.3 thousand Sep 2026 preliminary; [^3]; ST 25, 24; confirmed (Table 3 row "446.4 447.5 448.7 447.3").
15. 420,702 March 2026, down 0.5 percent; [^8]; ST 30; confirmed.
16. $1,333 Q1 2026; [^8]; ST 31; confirmed.
17. Burleigh 57,385 and $1,346; [^8]; MT 68, 69; confirmed.
18. Morton 12,010 and $1,126; [^8]; MT 70, 71; confirmed.
19. Grand Forks 40,695 and $1,204; [^8]; MT 100, 101; confirmed.
20. Ward 30,481 and $1,234; [^8]; MT 121, 122; confirmed.
21. Williams 25,925 and $1,767; [^8]; MT 141, 142; confirmed.
22. McKenzie $1,818; [^8]; MT 144; confirmed.
23. Stark 18,719 and $1,349; [^8]; MT 168, 169; confirmed.
24. Cass 126,659, down 0.6%; [^8]; MT 21; confirmed.
25. $82,349.8 million GDP 2025; [^22]; ST 39; confirmed (FRED NDNGSP updated Sep 30, 2026).
26. $9,430.711 million Bismarck MSA 2023, discontinued, last updated Dec 4, 2024; [^40]; MT 73; confirmed.
27. 539.91 Q2 2026 (and 515.80, 523.49); [^36]; ST 70; confirmed.
28. 413.83 Q2 2026 (and 389.85), 1995:Q1=100; [^41]; MT 77; confirmed.
29. $499,923 Sep 2026 (and Aug, May); [^9]; MT 76; confirmed.
30. $326,200 Sep 2026 (and Aug, May); [^12]; MT 125; confirmed.
31. $407,183 Sep 2026 (and May $469,000); [^11]; MT 105; confirmed.
32. 712 and 512 active listings, Cass; [^39]; MT 26; confirmed.
33. 1,322,791 boardings 2025; [^7]; ST 107; confirmed (Inforum, data NDAC 2025 annual report).
34. 590,542 Hector 2025 (prior 546,787 in 2024); [^7]; MT 44; confirmed.
35. 309,533 Bismarck 2025 (prior 309,337 in 2019); [^7]; MT 81; confirmed.
36. 654,304 first half 2025; [^6]; ST 108; confirmed.
37. 642,823 first half 2026, 1.8 percent lower; [^5]; ST 109; confirmed.
38. 50,959 Hector June 2026 record; [^5]; MT 46; confirmed.
39. United's fourth daily Denver departure at Minot; [^5]; MT 127 NOT FOUND note; confirmed.
40. 104,380 Sep 2026 record, 973,044 Jan to Sep, 84 percent, 1,662 departures; [^4]; ST 110, 111; confirmed.
41. 49,464 Hector Sep 2026 (prior 46,258, 2025); [^4]; MT 45; confirmed.
42. 25,218 Bismarck Sep 2026 (prior 23,891, 2019); [^4]; MT 82; confirmed.
43. Delta ended Sep 7, Sun Country from Sep 10, 2026 at Williston; [^4]; MT 156; confirmed.
44. 123,180 March 2025, "highest monthly total in state history"; [^29]; ST 112; confirmed (the page's "monthly state record" is right).
45. 29,343 Bismarck March 2025 (prior 27,623, 2019); [^29]; MT 83; confirmed.
46. 799,358 state, 68,233 Ward, 75,694 Ward plus McHenry plus Renville, July 1, 2025; [^15]; ST 14, MT 116, 117; confirmed.
47. 47,308 Minot city 2025 (47,277 in 2024, 48,387 in 2020); [^43]; MT 118; confirmed.
48. FDIC state summary and five county SOD totals and record counts; [^17], [^42], [^44] to [^47]; ST 59, 60, 62, MT 74, 124, 147, 148, 170; confirmed by API.
49. DR-4852, 4888, 4895, 4934 with dates, programs and county lists; FM-5540 and FM-5541 of Oct 6, 2024; [^13], [^14]; ST 123 to 132; confirmed by both OpenFEMA queries (19 and 7 and 7 and 2 counties; PA true, IA false, HM true only for 4852).
50. 281 Fargo and 71 Bismarck permits; [^37], [^38]; MT 29, 78; values confirmed, geography and "peak" not (A1-4).
51. Harmony Township meeting of Oct 22, two data center buildings, Cass County; [^33]; ST 142; confirmed; "two-year" not in source (A1-1).
52. Polaris Forge 2 at Harwood, first facility in the second half of 2026, Cass County Electric Cooperative; [^32]; ST 140; confirmed.
53. Glen Ullin ethanol plant, construction spring 2027, operations 2028; [^34]; ST 141; confirmed.
54. Two U.S. 85 projects starting in 2026, McKenzie County JDA down payment program; [^35]; MT 150, 152; confirmed.
55. Burleigh County's 2025 mill levies for 2026 taxes, Bismarck's plan, reported Oct 27, 2026; [^31]; MT 84; confirmed (page prints "Oct. 27, 2026 at 8:02 PM"; URL path says 10/28, the page date is the research's).

Not fetched, checked against research and register: county real GDP values (MT 23, 72, 102, 123, 145), 65,268.3 (ST 40), and the ten `mkt:` values, which equal `data/markets/series/<series>.json` for `nd` (sba7a_loans fy2016_2025 1,326; sba7a_volume 439,220,300; sba504_loans 546; sba504_volume 373,331,000; acs5 76,657, 249,900, 954; acs1 unemployment 0.019102; BEA 57,153,353,000 and 71,749), none null or flagged for `nd`.

Rules checked with no finding beyond those above: every printed number has a dated source (I77, I86) except A1-1; single-property values (Polaris Forge's $3 billion and 280 MW, the ethanol plant's $800 million) are not printed in the body (I64, I66); one vintage per series per geography (ruling 10): state population printed once (V2025 via MDN), no register population on the page; source titles equal the research's verbatim for all 43 research-backed sources, and the six register and SBA sources (18 to 21, 48, 49) use the titles 22 to 46 served state pages already use (I176); no research-computed sum (I55).

## Count after my confirmed findings

None of A1-1 to A1-4 or A1-6 to A1-10 removes a counted value. A1-5 by restoration keeps 56; by deletion it removes $200.4 million.

- Restoration route: 64 counted (research 56, register 8).
- Deletion route: 63 counted (research 55, register 8).

Floors (A6, READY): 30 in all with 20 research. The page clears both by 33 or more in all and 35 or more research on either route.
