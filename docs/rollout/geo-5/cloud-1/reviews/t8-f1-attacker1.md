# GEO-5 t8 freeze 1, attacker A (figures, dates, floors, research hygiene): /states/vermont/

Reviewed (cloud session, paths per CLOUD-PATHS.md): frozen copy `scratchpad/copies/f1-vermont/`, source `src/pages/states/vermont.html` (sha256 8715941a...a01818b, equal to the freeze record and to the handoff draft `pages/vermont.html`), rendered `states/vermont/index.html` (sha256 be4e4f56...872c507d, equal to the freeze record). Research: `ST-VERMONT.md`, `ST-VERMONT-2.md`, `MT-VERMONT.md` (cited by file line, as the pre-count and fact sheet do: "ST line n", "ST-2 line n", "MT line n"); `facts/vermont.facts.json`, `facts/vermont-PRECOUNT.md`, `assign/vermont.json`; `GATES-f1-vermont.txt` and `-g13.txt`. No metro page stands; all six markets are folded sections.

Baseline, rerun by me from the scratchpad (`timeout 600 python3 <copy>/scripts/qa/pagecheck.py --root <copy> --stage ready --new /states/vermont/ --figures /states/vermont/`): 6,007 body words; counted 77 (research 69, register 8/8); overlap 0.59% (/asset-classes/self-storage/). Equal to gate 3 and gate 4 in GATES-f1-vermont.txt. The page carries no `data-fsc-nocount` span at all.

## Fetches and closed doors (read this first)

WebFetch could not reach the source hosts from this cloud session. Attempted, in order, 2026-10-30:
- https://www.bls.gov/regions/new-england/news-release/countyemploymentandwages_vermont.htm: NOT FETCHED, `getaddrinfo ENOTFOUND www.bls.gov` (host outside the session's allowed network domains).
- https://www.bls.gov/regions/new-england/vermont.htm: NOT FETCHED, same.
- https://www.bls.gov/regions/new-england/vt_burlington_msa.htm: NOT FETCHED, same.
- https://fred.stlouisfed.org/data/VTNGSP: NOT FETCHED, `getaddrinfo ENOTFOUND fred.stlouisfed.org`, same reason.

The tool's own error text says that once a second host fails this way no further sites are to be tried until the network setting is changed, so no other source host was attempted (vermontbiz.com, vtdigger.org, labor.vermont.gov, nass.usda.gov, legacy.sba.gov, veda.org, accd.vermont.gov, fema.gov, rd.usda.gov, api.census.gov and the rest: NOT FETCHED, not attempted). No proxy, curl, cache or archive was used to get round it. Nothing on www2.census.gov was touched.

Consequence: the brief's "at least 12 source URLs opened" is NOT met (0 of 12). Every "source carries the value" judgement below rests on the research row and on the pre-count's own spot check of 2026-10-28 (15 fetches, 14 confirmed, 1 partial), and is marked as such. Rows that no second fetch has ever confirmed are listed under "Open checks" for the verifier, to be fetched once www.bls.gov, fred.stlouisfed.org and the news hosts are allowed.

One WebSearch was run (a query on the VTDigger Stowe registration article) before I judged that a search engine's summary of a page would stand in for the closed door. Nothing in this file rests on it.

## Findings

### A1-1 MAJOR-FACTUAL: the transit-area exemption is stated without its conditions (FAQ 6, #rules, #burlington)
- Page: /states/vermont/, FAQ 6 ("Does Act 250 still apply to an apartment project near transit in Chittenden County?"), #rules paragraph 2, #burlington paragraph 6.
- Text: FAQ 6: "Inside the transit-area map it does not. In October 2026 the Land Use Review Board's map expanded the areas in which a housing project near transit is exempt from Act 250, with the Chittenden County map enlarged; the notice printed no effective date [^32]." #rules: "In October 2026 the Board's transit-area map expanded the areas in which a housing project near transit is exempt from Act 250, with the Chittenden County map enlarged; the notice printed no effective date [^32]. For an apartment sponsor in the Burlington area the exemption bears on the schedule first: a project inside the map does not go through Act 250 review, so the study's pre-development period and carrying cost depend on which side of the line the parcel falls." #burlington: "The transit-area exemption in the rules section reaches Chittenden County first."
- Reproduction: the only research rows on the exemption are ST line 88 (value "up to 50 housing units on 10 acres or less, within one quarter mile of transit"; note "Applies to urbanized areas of population over 50,000; at least 51% of parcel inside the area. No effective date printed"; VBM 2026-10-16, the page's source 32) and MT line 39 ("50 units on 10 acres or less, within one quarter mile of transit"). The exemption is limited by size, acreage, distance and parcel share. The page answers its own question with a flat "it does not" for any apartment project inside the map and says "a project inside the map does not go through Act 250 review": a project of more than 50 units, or on more than 10 acres, inside the map is not exempt on the research's own terms. That is a wrong statement of rule. "Reaches Chittenden County first" adds an order no row gives (the rows say the Chittenden map was enlarged, nothing about first). Source 32 itself not opened (host not tried, see above).
- Fix (verbatim restoration of the research's terms, rule values kept out of the count; I86 is met, both rows are dated 2026-10-16):
  - FAQ 6: old "Inside the transit-area map it does not. In October 2026 the Land Use Review Board's map expanded the areas in which a housing project near transit is exempt from Act 250" new "In October 2026 the Land Use Review Board's map expanded the areas in which a housing project of up to <span data-fsc-nocount>50</span> units on <span data-fsc-nocount>10</span> acres or less, within one quarter mile of transit, is exempt from Act 250".
  - #rules: old "in which a housing project near transit is exempt from Act 250, with the Chittenden County map enlarged; the notice printed no effective date [^32]. For an apartment sponsor in the Burlington area the exemption bears on the schedule first: a project inside the map does not go through Act 250 review, so the study's" new "in which a housing project of up to <span data-fsc-nocount>50</span> units on <span data-fsc-nocount>10</span> acres or less, within one quarter mile of transit, is exempt from Act 250, with the Chittenden County map enlarged; the notice printed no effective date [^32]. For an apartment sponsor in the Burlington area the exemption bears on the schedule first: the study's".
  - #burlington: old "reaches Chittenden County first." new "reaches Chittenden County."
  - Deletion-only alternative if the integrator wants no added words: delete "Inside the transit-area map it does not. " (FAQ 6) and "a project inside the map does not go through Act 250 review, so " (#rules) and " first" (#burlington); the generic "a housing project near transit is exempt" then remains loose but no longer states a rule the research contradicts.
- Count: no change.

### A1-2 MAJOR-FACTUAL: "the whole of the dated public record this research found for Rutland" is false
- Page: #rutland paragraph 2.
- Text: "That is the whole of the dated public record this research found for Rutland, and a study there sources the rest."
- Reproduction: the paragraph before prints three Rutland figures ($1,195, 266.91, $458,725). The research holds more dated Rutland rows: ST-2 line 91 (Rutland County covered employment 25,265, March 2026, BLS release of 2026-09-04, primary: the same release as the page's source 2; the fact sheet marks it taken by /states/texas/dallas-fort-worth/, so it cannot count, but it was found); MT line 57 (county permits 89, 2025, FRED stamp 2026-05-28); MT line 60 (active listings 258, September 2026, 2026-10-01); MT line 61 (median days on market 77, September 2026); MT lines 62 to 69 (dated single-property and single-employer rows: the downtown hotel and its $8 million state loan, the Loretto Home redevelopment, VEDA's Center & Wales financing, Rutland Regional Medical Center's 145 beds and about 1,700 employees, the mental health urgent care); MT line 70 (Rutland County over 10% of statewide visitor spending, 2024); ST-2 lines 93 and 94 (Templewood Court, Roofs Over Rutland, both 2026 primary). The sentence tells a lender the record holds nothing else.
- Fix: old "That is the whole of the dated public record this research found for Rutland, and a study there sources the rest." new "A study there sources the rest." (deletion with one capital, the I176 precedent). Count: no change.

### A1-3 MAJOR-FACTUAL: FAQ 7 says no USDA Rural Development announcement for Vermont turned up; the site's own New Hampshire page cites joint Vermont and New Hampshire releases of March 2026 on maple funding
- Page: FAQ 7 ("Is there a USDA production record behind a dairy processing or maple sugarhouse loan in Vermont?").
- Text: "No USDA Rural Development announcement for Vermont in 2025 or 2026 turned up, so this page cites none."
- Reproduction: the served page /states/new-hampshire/ (in the frozen copy, `states/new-hampshire/index.html`, and `src/pages/states/new-hampshire.html` lines 470 to 473) says "USDA serves New Hampshire through a combined Vermont and New Hampshire state office [44], and its announcements are made for the two states together: the releases of March 20 to 23, 2026 on funding for maple syrup producers report one figure for both states [63]", source 63 "USDA Rural Development, News Releases for Vermont and New Hampshire, March 20 to 23, 2026", https://www.rd.usda.gov/newsroom/news-releases/vt-nh. The Vermont research records the gap as its own (ST line 79 NOT FOUND: "USDA Rural Development Vermont state office FY2025 announcements"; ST-2 line 43: "USDA Rural Development Vermont announcements"). FAQ 7 drops that qualifier and states it as a fact about the world, in an answer about maple sugarhouse loans, while a landed page of the same site cites 2026 USDA Rural Development releases covering Vermont maple producers. The #programs sentence ("No Vermont announcement from USDA for 2025 or 2026 turned up in the research, and this page cites none.") keeps the qualifier and is true of the research; it can stay. rd.usda.gov not opened (host not tried).
- Fix: delete "No USDA Rural Development announcement for Vermont in 2025 or 2026 turned up, so this page cites none. " from FAQ 7. Count: no change.

### A1-4 MINOR: the September 2026 payroll value is said to fall outside the research; the research holds it
- Page: #labor paragraph 3.
- Text: "That table's September 2026 column falls outside this page's research and is not quoted; a study pulls the newest column from the current release on the day it is written and names the month it used."
- Reproduction: ST line 23 holds Vermont total nonfarm employment, seasonally adjusted, preliminary, September 2026: 311.0 thousand (BLS Economy at a Glance, eag.vt.htm). The fact sheet marks it taken by /states/maryland/ (countable false), which is why it cannot count; it is not outside the research. The pre-count's flag 2 ("the first is not in the research") is the origin of the error (see A1-12 a). Literally the sentence speaks of "that table's" column (laus.t03), which the research did not record, so it is misleading rather than false; hence MINOR.
- Fix: old "That table's September 2026 column falls outside this page's research and is not quoted; a study pulls" new "A study pulls". Count: no change.

### A1-5 MINOR: "a year apart" for July 2025 and September 2026
- Page: #burlington paragraph 4.
- Text: "the two list prices are single months a year apart in a seasonal market"
- Reproduction: the two list prices are $577,925 for September 2026 (MT line 23) and $614,900 for July 2025 (MT line 27): fourteen months apart, not a year.
- Fix: old "single months a year apart in a seasonal market" new "single months in a seasonal market". Count: no change.

### A1-6 MINOR: the markets lede says every figure in the sections is a county or metro figure
- Page: #metros, data-lede.
- Text: "Every figure in these sections belongs to a Vermont county or to the Burlington-South Burlington metro, which lies wholly in Vermont; where a federal area joins a Vermont county to New Hampshire, the section reads the Vermont county alone."
- Reproduction: #resort-towns prints Stowe's town counts, "about 1,450 short-term rentals in Stowe" (MT line 100, "Town: Stowe") and "1,039 short-term rental properties registered in Stowe" (MT line 101); #burlington prints "$4.40 a gallon across 100 Burlington stations" (MT line 45). None is a county or metro figure.
- Fix: old "Every figure in these sections belongs to a Vermont county or to the Burlington-South Burlington metro, which lies wholly in Vermont; where a federal area" new "Where a federal area". Count: no change.

### A1-7 MINOR: the St. Albans card says Franklin County's record is one payroll count and one wage
- Page: #metros, St. Albans card.
- Text: "A county inside the Burlington metro whose own record is one payroll count and one wage."
- Reproduction: the research also holds Franklin County's median listing price, $431,000 for September 2026 (MT line 141, FRED stamp 2026-10-01; taken by /states/nevada/las-vegas/), its 2025 permits, 209 (MT line 140), its active listings, 200 (MT line 142), and dated single-property rows (MT lines 143, 144; ST-2 lines 146, 147). The section prints two figures; the county's record holds more.
- Fix: old "A county inside the Burlington metro whose own record is one payroll count and one wage." new "A county inside the Burlington metro." Count: no change.

### A1-8 MINOR: two comparisons in words with a value off the page (I59, I60(b))
- Page: #events paragraph 1; #labor paragraph 5.
- Text: (a) "and $372.6 million for the General, Transportation and Education Funds together, also above their combined target [^40]"; (b) "they show how much hiring and shedding runs beneath a payroll that moves little from month to month".
- Reproduction: (a) the combined target is $346.8 million (ST line 160), not printed; the sentence states the result of a comparison with a value the reader does not see. The source prints a variance (+$25.8M, ST line 160 note), so the conclusion is the source's, but I60(b) wants both inputs in the sentence or no conclusion. The General Fund clause before it prints both values ($276.5 million against $251.7 million) and is clean. (b) "moves little from month to month" is the writer's reading of 311.2 (September 2025) and 310.8 (August 2026), a year apart, plus values not on the page (July 2026 311.0 in the ST-2 line 16 note; September 2026 311.0 at ST line 23); no research row says the payroll moves little month to month (ST line 24 gives a 12-month change of -0.1%, not printed).
- Fix: (a) old "Education Funds together, also above their combined target [^40]" new "Education Funds together [^40]"; (b) old "runs beneath a payroll that moves little from month to month, and" new "runs beneath a payroll, and". Count: no change.

### A1-9 MINOR: statements that go past the research (I59: say only what the research says)
- Page and text, with reproduction:
  - #burlington: "OMRON agreed on October 10, 2026 to acquire OnLogic, a South Burlington maker of industrial computers [^44]". ST line 54 and MT line 46 say only "South Burlington based OnLogic"; what it makes is in no row.
  - #burlington: "The series title counts structures while its unit label says units, and the difference is large where apartment buildings are permitted, so a study states which it read". MT line 19 notes only "Series title says structures; unit label printed Units"; the size of the difference is the writer's.
  - #rules: "Vermont's certificate of need rules for health care facilities, its liquor licence rules, child care licensing capacity and any statewide short-term rental registry were not found." and #supply: "no count of senior housing units, licensed beds, hotel rooms or child care slots was reached". No NOT FOUND line in the three files mentions child care (ST line 93 lists certificate of need, liquor licence and a statewide rental registry; ST line 153 senior housing and licensed beds; ST-2 line 68 hotel room supply). The page reports a search the research does not record.
  - #costs: "and no carrier withdrawal or approved rate change for Vermont property was found". ST line 103 records only "Vermont Department of Financial Regulation homeowners or commercial property rate filing figures (DFR consumer advisory carried no numbers)"; carrier withdrawals are not in it.
  - #floods (optional): "Recovery money then came through HUD's disaster block grant". No row names HUD. True in fact (CDBG-DR is HUD's program); the integrator may leave it.
- Fix: (1) old "to acquire OnLogic, a South Burlington maker of industrial computers [^44]" new "to acquire OnLogic, a South Burlington company [^44]" (or delete " maker of industrial computers" and "a South Burlington" with it: "to acquire OnLogic [^44]"); (2) old "says units, and the difference is large where apartment buildings are permitted, so" new "says units, so"; (3) old "its liquor licence rules, child care licensing capacity and any statewide" new "its liquor licence rules and any statewide", and old "A care facility, restaurant, child care or rental study" new "A care facility, restaurant or rental study"; (4) old "licensed beds, hotel rooms or child care slots was reached" new "licensed beds or hotel rooms was reached"; (5) old "rate figures, and no carrier withdrawal or approved rate change for Vermont property was found." new "rate figures." Count: no change.

### A1-10 MINOR: two event-table dates the research does not give for the event
- Page: #events table.
- Text: "October 16, 2026 | The transit-area map expands the Act 250 housing exemption | [^32]"; "November 2025 | CDBG-DR approved funding posted by the Agency of Commerce and Community Development | [^4]".
- Reproduction: (a) ST line 88's Period is "Map update Oct 2026"; 2026-10-16 is Vermont Business Magazine's publication date of the relay, not a date of the map. The #rules text says "In October 2026", which the row is not entitled to sharpen. (b) ST-2 line 55: "Month from the page title; no day shown"; the title gives the month of the approvals, not of any posting. ST line 115 (Vermont Public, 2025-12-10) and the ST line 76 note put the first round's announcement in December 2025, so "posted" in November is not supported.
- Fix: (a) delete the row "<tr><td>October 16, 2026</td><td>The transit-area map expands the Act 250 housing exemption</td><td>[^32]</td></tr>" (source 32 stays cited in #rules and FAQ 6); (b) old "CDBG-DR approved funding posted by the Agency of Commerce and Community Development" new "CDBG-DR approved funding, by the title of the Agency of Commerce and Community Development's page". Count: no change.

### A1-11 MINOR: the register row label "Aggregate household income (B19313)"
- Page: #capital register table.
- Text: "<td>Aggregate household income (B19313)</td><td>...$31,682.5 million...</td>"
- Reproduction: the value equals the register (`acs1_aggregate_income` vt 31,682,535,700, 2024 ACS 1-year, not null, not flagged), and the label is the register's own (`scripts/markets_census.py` line 260). But the register defines its own per capita income as "B19313 aggregate income over B01003 population" (`acs1_per_capita_income` label), which is the person-level aggregate: Census table B19313 is aggregate income of the population 15 years and over; household aggregate income is B19025. "Household" misnames the series. Not page-specific: the same label is served on the South Dakota and Virginia pages. The Census API variables page was not opened (host not tried); the verifier should confirm at api.census.gov/data/2024/acs/acs1/variables/B19313_001E.json.
- Fix on this page: old "<td>Aggregate household income (B19313)</td>" new "<td>Aggregate income (B19313)</td>"; the register label is an integrator item. Count: no change.

### A1-12 MINOR: research hygiene (no page fix unless stated)
- (a) Pre-count flag 2 says the September 2026 total nonfarm 311.0 "is not in the research"; ST line 23 holds it (taken by Maryland). This produced A1-4.
- (b) MT line 101 gives the 1,039 Stowe registrations the Period "Jan 2026"; the pre-count's fetch (flag 4) found them in a September letter reported on 2026-01-16. The page follows the pre-count (source 9's date note, FAQ 4, #resort-towns). Not re-verified here (vtdigger.org not tried).
- (c) Source 37 cites `stateOverview.php?state=Vermont&year=2025`; ST line 145's URL has no `year` parameter, and the pre-count's fetch of the bare URL found the 2025 edition titled "2025 State Agriculture Overview for Vermont" (research title: "2025 State Agriculture Overview, Vermont", which the page uses, I176). The `year=2025` URL was opened by neither the researcher nor the pre-count. It follows pre-count flag 3 and is the stable form, so no fix, but the verifier should confirm it serves 2,513,000,000 lb.
- (d) ST line 143's note credits the $353,000 to "Vermont Association of Realtors and state tax data"; pre-count flag 14 says "Vermont Housing Finance Agency records". The page names no original, so no fix.
- (e) ST lines 20 to 22 carry URL labor.vermont.gov/node/6071; the page cites labor.vermont.gov/economic-data/employment-report (ST-2 line 17's URL) for all four DOL values. The pre-count's fetch of the second URL shows 347,408 and 337,877 on it; 329,128 and 8,749 were not re-checked there.
- (f) ST line 4 lists fema.gov as a closed door (403) while ST-2 lines 49 to 53 read four fema.gov notices the same day. The page's "FEMA's declaration pages with dollar totals refused the connection" matches ST line 175 (/disaster/4720 and /4793, 403). No fix.

## Open checks for the verifier (not findings: none could be reproduced with the hosts closed)
1. laus.t03.htm: is August 2026 marked (P)? BLS's state Table 3 usually flags the two latest months. If so, the page's "310.8 thousand in August 2026" and the table row "Nonfarm employees, seasonally adjusted | 310.8 thousand | August 2026" need "preliminary" (pre-count flag 2). The pre-count's spot check mentions (p) only on September's 311.0.
2. Source 18's title "Vermont Economy at a Glance" for https://www.bls.gov/regions/new-england/vermont.htm is the research's (ST lines 24 to 35, no "inferred" note), so the page meets I176. But t5 A1-2 reproduced on the same BLS template that "<State> Economy at a Glance" is a table caption there and the `<title>` of the eag page. Source 41's title is the research's "inferred from page heading" (MT line 11 note; pre-count flag 12).
3. "adopted a cap in July 2026" (#rules, #resort-towns, FAQ 4, events row "July 2026"): the month is MT line 99's Period cell ("Adopted Jul 2026"). If the VTDigger article of 2026-08-01 does not print July, the month falls (the I142 pattern) and the events row goes.
4. Rows no second fetch has confirmed (researcher's fetch only; not in the pre-count's spot check nor its "first-pass confirmations stand" list): MT lines 21, 22, 58, 59, 80, 81, 126 (FHFA and Realtor.com county values, FRED); ST line 100 and MT line 45 (gasoline); ST line 112 ($25,987,190.49); ST line 162 ($88.2 million, $2,362.3 million); ST line 67 ($57.9 million); ST lines 21, 22 (329,128; 8,749).

## Re-derivation (all 69 counted research figures and all 10 register values; 0 URLs fetched, see above)

Dating: (a) publication or release date in the row; (b) edition year in the title; (c) periodic release (I77(c), D12). "Spot check" = confirmed by the pre-count's fetch of 2026-10-28; "first pass" = in the pre-count's "first-pass confirmations stand" list; "researcher only" = no second fetch.

| # | Page value (section) | Cite | Research row | Dated | Kind | Second fetch | Result |
|---|---|---|---|---|---|---|---|
| 1 | 337,877 (hero, stats, #labor, table, FAQ 2) | 1 | ST line 20 | (a) 2026-10-20 | primary | spot check | consistent; URL per A1-12 e |
| 2 | 329,128 | 1 | ST line 21 | (a) | primary | researcher only | consistent |
| 3 | 8,749 | 1 | ST line 22 | (a) | primary | researcher only | consistent |
| 4 | 347,408, Sep 2025 SA | 1 | ST-2 line 17 | (a) | primary, prior period | spot check | consistent |
| 5 | 337,142, Sep 2026 NSA (p) | 16 | ST-2 line 13 | (c) summary page 2026-10-28 | borderline | spot check | consistent, "marked preliminary" |
| 6 | 347,040, Sep 2025 NSA | 16 | ST-2 line 14 | (c) | borderline, prior period | spot check | consistent |
| 7 | 62.1% | 15 | ST line 37 | (a) 2026-10-20 | secondary | first pass | consistent |
| 8 | 311.2 thousand, Sep 2025 | 17 | ST-2 line 15 | (c) Last Modified 2026-10-20 | borderline | spot check | consistent |
| 9 | 310.8 thousand, Aug 2026 | 17 | ST-2 line 16 | (c) | borderline | spot check | consistent; (p) open check 1 |
| 10 | 65.5 thousand | 18 | ST line 25 | (c) | borderline | first pass (EAG) | consistent, SA, preliminary |
| 11 | 56.8 thousand | 18 | ST line 27 | (c) | borderline | first pass | consistent |
| 12 | 31.4 thousand | 18 | ST line 30 | (c) | borderline | first pass | consistent |
| 13 | 27.9 thousand | 18 | ST line 28 | (c) | borderline | first pass | consistent |
| 14 | 19,658 gross losses | 18 | ST line 34 | (c) | borderline | first pass | consistent, Jun to Sep 2025 |
| 15 | 16,739 gross gains | 18 | ST line 35 | (c) | borderline | first pass | consistent |
| 16 | 33,374 establishments | 2 | ST-2 line 11 | (a) 2026-09-04 | primary | spot check | consistent, "preliminary" |
| 17 | 304,200, Mar 2026, "decrease" | 2 | ST line 32 | (a) | primary | spot check (304,184 unrounded) | consistent (down 1.0%); I82: 304,184 not printed |
| 18 | $1,322, "increase" | 2 | ST line 33 | (a) | primary | researcher only | consistent (up 3.0%) |
| 19 | $49,657.5 million, 2025 | 19 | ST line 49 | (a) FRED 2026-09-30 | secondary | first pass | consistent |
| 20 | $25,987,190.49 | 22 | ST line 112 | (a) 2024-07-11 | secondary, stale | researcher only | consistent; "FEMA and SBA" per row |
| 21 | $49,991,445 | 4 | ST-2 line 55 | (a) month in title | primary | spot check | consistent; no "first round" (flag 5) |
| 22 | $67,845,000, 28 projects | 5 | ST line 76 | (a) 2026-10-15 | secondary | first pass | consistent; total alone (flag 13 e) |
| 23 | $61.5 million | 11 | ST line 64 | (a) 2025-10-31 | secondary | first pass | consistent |
| 24 | 1,748 jobs | 11 | ST line 65 | (a) | secondary | first pass | consistent |
| 25 | $57.9 million, Jul 18 2022 | 12 | ST line 67 | (a) 2022-07-18 | primary, stale | researcher only | consistent; split per note |
| 26 | $1,586,902 per week | 13 | ST-2 line 37 | (a) 2025-10-21 | primary | spot check | consistent; called an estimate |
| 27 | 16 million (stats "16 M", #visitors, FAQ 3) | 3 | ST line 126 | (a) 2025-12-11 | secondary | first pass | consistent |
| 28 | 31,780 direct jobs | 3 | ST line 129 | (a) | secondary | first pass | consistent; WCAX's "almost 32,000" not printed (I82) |
| 29 | 339,046 | 29 | ST line 134 | (a) 2026-06-04 | secondary | spot check | consistent |
| 30 | $4.34, Oct 26 2026 | 33 | ST line 100 | (a) | secondary | researcher only | consistent, dated to the day |
| 31 | 902.53, 2026 Q2, 1980:Q1=100 | 34 | ST line 52 | (a) FRED 2026-08-25 | secondary | spot check | consistent |
| 32 | about $353,000, 2024 | 35 | ST line 143 | (a) 2025-09-11 | secondary | first pass | consistent; "about" kept |
| 33 | 2,513,000,000 lb | 37 | ST line 145 | (b) 2025 edition | borderline | spot check (bare URL) | consistent; URL A1-12 c |
| 34 | 3,091,000 gallons | 38 | ST-2 line 65 | (b) 2026 edition | borderline | spot check | consistent; one maple value only (flag 3) |
| 35 | $88.2 million | 39 | ST line 162 | (a) 2025-08-05 | secondary | researcher only | consistent |
| 36 | $2,362.3 million target | 39 | ST line 162 (What cell) | (a) | secondary | researcher only | consistent; counts as its own figure |
| 37 | $276.5 million (with $251.7 million, not counted) | 40 | ST line 159 | (a) 2026-10-19 | secondary | spot check | consistent; both values in one sentence |
| 38 | $372.6 million | 40 | ST line 160 | (a) | secondary | spot check | consistent; "also above" A1-8 a |
| 39 | 126.2 thousand LF, Sep 2026 | 41 | MT line 12 | (c) | borderline | first pass | consistent, NSA, preliminary |
| 40 | 125.2 thousand nonfarm | 41 | MT line 13 | (c) | borderline | first pass | consistent |
| 41 | 130,114, Sep 2025 | 16 | ST-2 line 77 | (c) | borderline, prior period | spot check | consistent; same series as 126.2 (spot check: 126,230) |
| 42 | 126,589, Aug 2026 (p) | 16 | ST-2 line 78 | (c) | borderline, prior period | spot check | consistent, "preliminary" |
| 43 | $35.75, May 2025 | 18 | MT line 16 | (c) | borderline | first pass | consistent; metro, not county |
| 44 | 100,700, "decrease" | 2 | MT line 14 | (a) | primary | researcher only | consistent (down 1.8%) |
| 45 | $1,521, "increase" (hero, #burlington) | 2 | MT line 15 | (a) | primary | researcher only | consistent (up 3.4%) |
| 46 | 422.61, 1995:Q1 base | 7 | MT line 21 | (a) FRED 2026-08-25 | secondary | researcher only | consistent |
| 47 | 322.44, 2000 base | 42 | MT line 22 | (a) FRED 2026-03-31 | secondary | researcher only | consistent |
| 48 | $577,925, Sep 2026 | 6 | MT line 23 | (a) FRED 2026-10-01 | secondary | spot check | consistent |
| 49 | $614,900, Jul 2025 | 36 | MT line 27 | (a) 2025-08-22 | secondary | first pass | consistent; "a year apart" A1-5 |
| 50 | 1,026 structures, 2025 | 43 | MT line 19 | (a) FRED 2026-05-28 | secondary | first pass | consistent; structures/units noted |
| 51 | 24.5% | 3 | MT line 44 | (a) 2025-12-11 | secondary | first pass | consistent |
| 52 | $4.40, 100 stations | 33 | MT line 45 | (a) 2026-10-26 | secondary | researcher only | consistent |
| 53 | $1,195 Rutland | 2 | ST-2 line 92 | (a) | primary | spot check | consistent, county |
| 54 | 266.91 Rutland | 45 | MT line 58 | (a) FRED 2026-03-31 | secondary | researcher only | consistent |
| 55 | $458,725 Rutland | 46 | MT line 59 | (a) FRED 2026-10-01 | secondary | researcher only | consistent |
| 56 | 32,975 Washington | 2 | ST-2 line 103 | (a) | primary | spot check | consistent |
| 57 | 334.90 Washington | 47 | MT line 80 | (a) | secondary | researcher only | consistent |
| 58 | $443,200 Washington | 48 | MT line 81 | (a) | secondary | researcher only | consistent |
| 59 | 12,865 Lamoille | 2 | ST-2 line 120 | (a) | primary | spot check | consistent, county not town |
| 60 | $1,170 Lamoille | 2 | ST-2 line 121 | (a) | primary | spot check | consistent |
| 61 | 22,478 Windsor | 2 | ST-2 line 122 | (a) | primary | spot check | consistent |
| 62 | $1,265 Windsor | 2 | ST-2 line 123 | (a) | primary | spot check | consistent |
| 63 | about 1,450 Stowe | 8 | MT line 100 | (a) 2026-08-01 | secondary | first pass | consistent, "town data"; month open check 3 |
| 64 | 1,039 Stowe | 9 | MT line 101 | (a) 2026-01-16 | secondary | spot check (partial) | consistent with the spot check (September letter; not "as of January") |
| 65 | 21,211 Windham | 2 | ST-2 line 132 | (a) | primary | spot check | consistent |
| 66 | $1,094 Windham (hero, #brattleboro) | 2 | ST-2 line 133 | (a) | primary | spot check | consistent |
| 67 | 271.97 Windham | 50 | MT line 126 | (a) | secondary | researcher only | consistent |
| 68 | 15,967 Franklin | 2 | ST-2 line 144 | (a) | primary | spot check | consistent |
| 69 | $1,255 Franklin | 2 | ST-2 line 145 | (a) | primary | spot check | consistent |

Printed, not counted (checked the same way): $525,000 (ST line 144, source 36; taken by the served Lebanon, Tennessee case), $625,000 (MT line 112, source 49; taken by /states/delaware/ and two cases), $251.7 million (ST line 159). Not printed though assigned: $13,883,650 (ST-2 line 32; the page prints only "32 projects in ten counties", both dated by the 2026-04-01 release) and MT line 20's discontinued 2023 metro GDP.

Register (10 printed, 8 counted), each against `data/markets/series/<series>.json` at geo `vt`, none null (nulls lists hold no `vt` key) and none flagged:

| Row | Page | Series value | Result |
|---|---|---|---|
| 7(a) gross approval, net, FY2021 to FY2025 | $196.0 million | sba7a_volume all fy2021_2025 195,998,200 (as of 2026-06-30) | equal; not counted (pagecheck reads it as a repeat of Iowa's nocount "$196 million") |
| 504 | $71.4 million | sba504_volume all fy2021_2025 71,444,000 | equal; counted |
| Households B11001 | 285,548 | acs1_households 285,548 | equal; counted |
| Owner-occupied B25003 | 209,117 | 209,117 | equal; counted |
| Renter-occupied B25003 | 76,431 | 76,431 | equal; counted |
| Median household income B19013 | $82,730 | 82,730 | equal; counted |
| Per capita income B19301 | $48,856 | 48,856 | equal; counted |
| Aggregate income B19313 | $31,682.5 million | 31,682,535,700 | equal; counted; label A1-11 |
| Median gross rent B25064 | $1,319 | 1,319 | equal; counted |
| Personal income CAINC1 line 1, 2024 | $46,229.3 million | bea_personal_income 46,229,260,000 | equal; not counted (rounded repeat of Kentucky's "$46.2 billion") |

Ruling 10: no PEP population and no ACS median home value printed (pre-count flag 14); the research holds no ACS, BEA personal income or SBA FOIA series, so no two vintages of one series. Sources 26 to 28 dates match `data/markets/sources.json` (SBA FOIA retrieved 2026-10-16, as of 2026-06-30; ACS 2024 1-year and BEA CAINC1 retrieved 2026-10-16). The SBA FOIA geography is ProjectState (`foia-geocoding.json`), so "for projects in Vermont" is right. The `sba:` markers equal `data/regulatory/sba.json` (SOP 50 10 8.1 effective 2026-10-01; $5 million; 1.15x; 1.25x; 10%; the 13 CFR 120.160(b) text).

Other checks with no finding: every source title equals the research's title (I176; a script matched all 52 sources against the three files by URL: 46 match by URL and title, source 37's URL is not the research's (A1-12 c) but its title is ST line 145's, sources 26 to 28 are the register's and 51 and 52 equal `tools/sba-rule-sources.json`); every source date equals the research's Published value or its stated periodic or edition dating; every citation points to the source that carries the row; no single-property value is printed as a counted figure (OnLogic's $675 million is only in source 44's title; the VEDA, CDBG-DR and Treasurer project rows are not printed); no arithmetic on the page (the +/- words "decrease" and "increase" are BLS's own); the DR-4720 and DR-4810 county lists match ST-2 lines 49 and 53, and the five counties said to be on both notices are their intersection, with both lists printed in the two sentences before; SA and NSA labor force values are each printed with their publisher and adjustment (pre-count flag 8).

## Count of counted figures after my confirmed findings

No fix above deletes a counted figure; A1-1's restored rule values are wrapped in `data-fsc-nocount`. The page stays at 77 counted: research 69, register 8 (of 10 printed). A6 floors: READY 30 with 20 research, landing 25 with 15: both hold, research 49 over the READY research floor.

For the integrator: on the pre-count's own harshest stack the frozen page holds 20 research and 28 in all, not the pre-count's 21 and 31, because it does not print $13,883,650 (ST-2 line 32, one of the 21) and only 8 register values count (two collide with Iowa and Kentucky). Striking the 15 QCEW rows as preliminary as well leaves 5. The main reading binds (R9, I183), so this is not a floor failure, but the pre-count's "margin of 1" does not survive to the page.

Severity tally: BLOCKER 0; MAJOR-FACTUAL 3 (A1-1 to A1-3); MAJOR-NONFACTUAL 0; MINOR 9 (A1-4 to A1-12). Fetches: 0 of the required 12 (www.bls.gov and fred.stlouisfed.org fail DNS in this session; no other host tried).
