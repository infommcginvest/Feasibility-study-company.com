# GEO-5 t5 freeze 1, attacker A (figures, dates, floors, research hygiene)

Page: `/states/alaska/` (no metro page). Frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t5/`; source `src/pages/states/alaska.html` (byte equal to `drafts/geo-5/pages/alaska.html`, cmp). Research: `research/ST-ALASKA.md`, `research/MT-ALASKA.md` (cited below as ST line n, MT line n). Pre-count `facts/alaska-PRECOUNT.md`.

Baseline (pagecheck, `--stage ready --figures`, run in the copy): words 6,264; counted 71 (research 66, register 5/5); overlap 0.51%. Agrees with GATES-t5-f0.

Fetches (WebFetch, 2026-10-28): 15 distinct source URLs opened, listed in the re-derivation table. One extra `curl` GET of the BLS county release returned 403; recorded, not worked around (the WebFetch read of the same URL had already been made). No www2.census.gov fetch.

## Findings

### A1-1 MAJOR-FACTUAL: two vintages of DOLWD's population components on one page (ruling 10)
Page, #population, paragraph 2: "A year earlier the department had estimated net out-migration of 1,163 for 2023 to 2024, as the Peninsula Clarion reported in January 2025 [^25]; that vintage has since been revised, so the figure describes what the department said then, not the current series."
Reproduction: ST line 21 (1,163, Peninsula Clarion 2025-01-07, note "Original: DOLWD estimate of that vintage, since revised"). The same section prints the current vintage of the same series and geography: net migration 1,740 for 2024 to 2025 and the revised July 2024 base 737,088 (ST lines 13, 16). ROLLOUT-1 ruling 10: "Never put two vintages of one series on one page." D20 applied exactly this to South Dakota (2024 vintage clause deleted). The sentence itself says the vintage was revised. D20's exemption (different publishers) does not reach this: both are DOLWD.
Fix: delete the whole paragraph "The direction of migration is not new. A year earlier ... not the current series." Source [^25] stays cited by the Kenai section (no orphan). Count: -1 (1,163).

### A1-2 MAJOR-FACTUAL: source [^5] carries a title that is not the page's own (I176)
Page, #economy paragraphs 1 and 2 and FAQ 1: 365.2 thousand labor force, "construction held 17.7 thousand jobs (-5.3%), government 76.8 thousand (-3.0%) and manufacturing 13.9 thousand (+14.9%)" and "BLS counted 76.8 thousand government jobs ... [^5]"; source 5: title "Alaska Economy at a Glance", URL https://www.bls.gov/regions/west/alaska.htm.
Reproduction: WebFetch of that URL: page title "Alaska : U.S. Bureau of Labor Statistics", H1 "Alaska"; "Alaska Economy at a Glance" is only the caption of a table on it (and the `<title>` of https://www.bls.gov/eag/eag.ak.htm, which the page already lists as source 17 under the same title). The values themselves are on the page as printed (365.2; 17.7, -5.3; 76.8, -3.0; 13.9, 14.9; all (p) preliminary, seasonally adjusted). Research: ST line 43 (365.2) puts "Alaska Economy at a Glance" in the Title cell but its own note says "page title not printed in the fetch"; ST lines 45 to 47 (the three sector figures) hold only a placeholder ("Alaska BLS regional page (title not printed in the fetch)"). So the three sector figures borrow a title the research gives for another row, and that title is the eag page's, not this URL's. Answer to the integrator's question: no, it is not that page's own title. The pre-count already called these rows weak (flag 6).
Fix (I176 practice, Rhode Island: a source whose title the research does not hold is dropped with the claims resting only on it): delete from #economy paragraph 1 ", and a seasonally adjusted civilian labor force of 365.2 thousand [^5]"; delete #economy paragraph 2's sentence "In BLS's seasonally adjusted September 2026 figures, all preliminary, construction held ... as printed [^5]."; delete #economy paragraph 3 whole (it reads only the deleted lines: "The government count", "The construction count", "The manufacturing line"); delete FAQ 1's last sentence "BLS counted 76.8 thousand government jobs ... [^5]."; drop source 5 and renumber. Lighter alternative for the integrator: keep 365.2 under row ST 43's title and drop only the sector sentence, paragraph 3 and the FAQ sentence. Count: -4 strict (365.2, 17.7, 76.8, 13.9), -3 light.
Note: the paragraph 2 sentence after the deleted one ("The department's Alaska Economic Trends for August 2026 ... and federal employers sit inside the government line.") points at the government line; under the strict fix delete its last clause ", and federal employers sit inside the government line" too.

### A1-3 MAJOR-FACTUAL: "unrestricted mining revenue" is not what the forecast's 102.0 measures
Page, #oil-and-treasury paragraph 3: "Mining adds its own line, with unrestricted mining revenue forecast at 102.0 million dollars for fiscal 2027 [^1]." and table row "Unrestricted mining revenue, forecast | 102.0 million dollars | Fiscal 2027".
Reproduction: ST line 80 labels it "Unrestricted mining revenue forecast". WebFetch of the Spring 2026 Revenue Forecast: 102.0 is the row "Mining" (FY2025 43.3, FY2026 50.8, FY2027 102.0) under "Other Tax", inside "Subtotal Unrestricted Non-Petroleum Taxes" of Table 2 "Unrestricted General Fund Revenue". The same document's text says the mining sector "is expected to contribute $189 million of direct unrestricted revenue" in FY 2027 (mining license tax, corporate income tax and royalties). So the page's label states a measure the source gives a different value for. The research's label carries the error.
Fix: delete the sentence and the table row (preferred). If kept, restore the source's own label ("the Mining line of unrestricted non-petroleum taxes"), which needs a capped review (I68). Count: -1 if deleted (102.0 million).

### A1-4 MAJOR-FACTUAL: "10-year program from 2022" is not on the cited page
Page, FAQ 5: "$54M for the state's loan guarantee program, part of a 10-year program from 2022"; #capital: "The state's loan guarantee program holds $54M within a 10-year program from 2022 ... [^10]".
Reproduction: WebFetch of https://aksbdc.org/ssbci/ (last modified October 14, 2026): the string "2022" does not appear; the only "10-year" sentence is "Alaska is allocated approximately $59 million throughout this 10-year program." The year comes only from the research's Period cell (ST lines 94, 95). $54M and $83.1M and "August 1, 2024" are on the page as printed.
Fix: delete " from 2022" in both places. No count change.

### A1-5 MAJOR-FACTUAL: the Ketchikan section says the BLS county release omits the borough; it does not
Page, #ketchikan paragraph 1: "BLS's quarterly county release does not include the borough among its selected areas,". Related, #kodiak: "nor were employment and wage rows for the borough".
Reproduction: WebFetch of the county release (source 6): Table 2 is "all Alaska county equivalents, first quarter 2026" and prints "Ketchikan Gateway Borough | 625 | 6,266 | 1,327" and "Kodiak Island Borough | 476 | 5,890 | 1,145"; the text says levels are "also available for the 29 small county equivalents in Alaska". The research's NOT FOUND (MT line 156: "not in the BLS county table selected areas") is wrong, and the page turns it into a statement about BLS's release, contradicted by a source the page cites.
Fix: delete "BLS's quarterly county release does not include the borough among its selected areas, " (the sentence then reads "The department's labor force page lists Ketchikan without an unemployment rate, and the department's area rental figures ..."; keep the existing "and"). Kodiak's "were not found" is true of the research, but misleading against source 6: delete "employment and wage rows for the borough or " (MINOR part). No count change; the values are not research rows and must not be added.

### A1-6 MAJOR-FACTUAL: a comparison in words with one value hidden (I59, I60(b))
Page, #access paragraph 1: "The airport system's own report, as relayed in October 2026, prints a different cargo figure for 2025 [^13]; a study cites one, with its publisher, and does not present the two as separate years or places."
Reproduction: MT line 45 (3.82 million tonnes, AEDC via Alaska Business, a record) and MT line 46 (more than 3.85 million metric tons, AIAS via Alaska Public Media). WebFetch: Alaska Business 2026-01-30 prints "The 3.82 million tonnes of air cargo landed in 2025 set a record"; Alaska Public Media 2026-10-12 prints "more than 3.85 million metric tons of cargo in 2025", from the 2026 AIAS Development Report. "Prints a different cargo figure" states the result of comparing two sourced values while only one is printed, which I60(b) cuts. Printing 3.85 would put the same fact at two values (I82; pre-count flag 3). Only 3.82 is printed elsewhere on the page (stats tile, FAQ 7, #anchorage): correct.
Fix: delete the whole sentence. Source 13 stays cited (460,000). No count change.

### A1-7 MAJOR-FACTUAL: the two September job readings are explained to each other beyond the research (I59)
Page, #economy paragraph 1: "The two are different series from different publishers, each with its own basis, and a study that needs a statewide job count picks one, names it and does not average or reconcile them."
Reproduction: each reading has its own source and neither is compared by value: BLS 340.7 thousand and +1.2% (ST line 42, eag.ak.htm; WebFetch confirms 340.7 and 1.2, seasonally adjusted, preliminary) and DOLWD "up 0.1%" in nocount (ST line 35, release 26-19; WebFetch: the 0.1% is in the headline, the body gives "+300", and the release states no seasonal basis for the job count and does not mention BLS). The sentence is uncited and goes past the research: "different series" is the researcher's note on ST line 35, "each with its own basis" has no support for DOLWD (its basis is unstated), and the sentence's purpose is to account for the gap between the two, which the integrator wants nowhere on the page. I59: say only what the research says, with its citation, or drop it.
Fix: delete the sentence. The two readings then stand side by side, each with its source, compared nowhere. No count change.

### A1-8 MAJOR-FACTUAL: the two population estimates are given an uncited methods claim
Page, #population paragraph 3: "The Census and state figures are separate estimates built by separate methods, and this page uses ..."
Reproduction: ST line 19 (737.270 thousand, FRED AKPOP, 2026-03-03; note "differs from the DOLWD 738,737") says nothing on methods. WebFetch: FRED names the Census release "Annual Estimates of the Population for the U.S. and States" and no method; DOLWD release 26-2 mentions no Census estimate or method. Values confirmed: 737.270 (2025), 738,737 (July 1, 2025). Nothing else on the page compares, ranks or reconciles the two.
Fix: delete " built by separate methods". No count change.

### A1-9 MAJOR-FACTUAL: a pointer left by the $1,579 recast names a row the table no longer has
Page, #costs paragraph 1: "The quarterly county release gives average weekly wages by borough for the first quarter of 2026, which the table below sets out for Anchorage, Juneau, the Kenai Peninsula and the Mat-Su [^6]."
Reproduction: diff of `work/alaska.pre-1579.html` against the frozen source: the Anchorage row ("Municipality of Anchorage | $1,579") was deleted from the table; the table now holds Juneau $1,449, Kenai Peninsula $1,297, Matanuska-Susitna $1,154 only. `grep -c 1,579` on the source and the rendered page: 0 and 0 (every mention is gone, as D20 says).
Fix: delete "Anchorage, " from that sentence. No count change.

### A1-10 MINOR: the other three $1,579 recasts
Checked each recast (D20): (1) FAQ 2 now gives Mat-Su $1,154 and Juneau $1,449 (both Table 2 values, confirmed by WebFetch; "Mantanuska-Susitna" in the source, see A1-12): clean. (2) #anchorage paragraph 1 dropped the wage clause; the following sentence still says a study uses "the Municipality's for a payroll or wage input", where the Municipality's figures now printed are a job count and establishments only. Fix: delete " or wage". (3) #mat-su paragraph 2: "the Mat-Su's average weekly wage of $1,154 [^6], and AEDC's average home price of about $474,200 beside Anchorage's $481,000 [^38]" puts both home prices in one sentence with their citation (I60(b) allows it); no comparison word. Clean, though $1,154 now prints five times on the page (FAQ 2, table, three in #mat-su), which counts once.

### A1-11 MINOR: attribution of the July passenger figure
Page, #access and FAQ 7: "Nearly 460,000 passengers ... as Alaska Public Media reported from the Alaska International Airport System [^13]".
Reproduction: WebFetch: the article gives the figure in a quote from the spokesperson for Ted Stevens Anchorage International Airport ("It was the busiest month ever recorded at Fairbanks and Anchorage airports, with nearly 460,000 passengers"); the AIAS report is the source of the cargo figure, not this one. ST line 149 says "Original: AIAS". The airport is part of the system, so this is loose rather than false. Fix if taken: none needed beyond the record; or delete " from the Alaska International Airport System" in both places.

### A1-12 MINOR (clean): the Matanuska-Susitna spelling
Page, #mat-su: 'BLS's quarterly county release, which spells the borough "Mantanuska-Susitna", counts 29,137 jobs ...'. WebFetch: Table 2 prints only "Mantanuska-Susitna Borough | 2,962 | 29,137 | 1,154". The rendered page spells the name correctly ("Matanuska-Susitna") 9 times and the misspelling once, inside that quotation. No fix.

### A1-13 MINOR: research hygiene
(a) Source 24's title is the research's lowercase, comma-less form ("alaska population rises slightly but more people continue ..."), which ST line 16 says was taken "as shown in the search listing", against the file's own hygiene line "no row relies on a search snippet". I176 makes the research's form the page's, so no page fix; recorded for the research. (b) ST line 42's note puts the BLS sector table on the regional URL with "page title not printed in the fetch", yet ST line 43 types the eag page's title into the regional URL's Title cell (A1-2). (c) Uncited general claims: "The manufacturing line takes in seafood processing" (#economy paragraph 3, #kodiak paragraph 2); no research row says so (falls away with A1-2's strict fix in #economy; in #kodiak delete "takes in seafood processing, but it" if the integrator wants it gone).

### Checked and clean (integrator's list)
- GDP: sources 21 to 23 name "U.S. Bureau of Economic Analysis, via FRED (Federal Reserve Bank of St. Louis)", both names, as landed pages do ("U.S. Census Bureau ... via FRED" is landed form). Values confirmed by WebFetch: AKNGSP 2025 73,634.8; AKRGSP 2025 56,335.0; AKRQGSP 2025 Q2 56,342.4 and 2026 Q2 56,159.6 (SAAR); all updated Sep 30, 2026, source BEA. One vintage. The two quarters are printed with no comparison word. The FRED entries carry no "secondary" tag while the lede says news reports are "each marked secondary"; the lede is accurate as written (it marks the news reports). No finding.
- The stats tile and FAQ 4 print DOLWD's 738,737 only; 737.270 appears once, in #population, with its own source. No ranking anywhere.
- Register: the five `mkt:` values equal `data/markets/series/*.json` at `ak` (acs5 median household income 92788, BEA per capita 76234, acs1 median home value 376500, sba7a_loans fy2016_2025 919, sba504_volume fy2016_2025 104,387,000), none null or flagged; no PEP series used.

## Re-derivation (37 counted figures; 15 URLs fetched)

| # | Page value | Cite | Research | Fetched | Result |
|---|---|---|---|---|---|
| 1 | 459.2 / 518.5 thousand b/d, FY26/FY27 | 1 | ST 74, 75 | yes (Revenue forecast) | confirmed (459,200; 518,500) |
| 2 | $75.26, FY26 | 1 | ST 72 | yes | confirmed |
| 3 | 6,491.9 / 6,725.3 million | 1 | ST 76, 77 | yes | consistent ($6.5B, $6.7B in text; table values per research) |
| 4 | 3,798.9 million transfer | 1 | ST 78 | yes | consistent ($3.8B) |
| 5 | $87.6 billion, Jan 31 2026 | 1 | ST 79 | yes | confirmed |
| 6 | 102.0 million mining | 1 | ST 80 | yes | value confirmed, label wrong (A1-3) |
| 7 | 340.7 thousand, +1.2% | 17 | ST 42 | yes (eag.ak) | confirmed, SA, (p) |
| 8 | 365.2 thousand | 5 | ST 43 | yes (regions) | value confirmed; title (A1-2) |
| 9 | 17.7 / 76.8 / 13.9 thousand | 5 | ST 45 to 47 | yes | values confirmed; title (A1-2) |
| 10 | 0.1% (nocount) | 18 | ST 35 | yes (26-19) | confirmed (headline) |
| 11 | 30,293 / 23,914 / +6,379 | 20 | ST 48 to 50 | no (pre-count spot check 15) | research consistent |
| 12 | 73,634.8 million | 21 | ST 61 | yes | confirmed |
| 13 | 56,335.0 million | 22 | ST 62 | yes | confirmed |
| 14 | 56,342.4 / 56,159.6 million | 23 | ST 63, 64 | yes | confirmed |
| 15 | 738,737; +1,649; +3,389; 1,740 | 4 | ST 11 to 14 | yes (26-2) | confirmed |
| 16 | +1,696 Mat-Su | 4 | MT 64 | yes (26-2) | confirmed |
| 17 | 737.270 thousand | 26 | ST 19 | yes (FRED AKPOP) | confirmed |
| 18 | 737,088 | 24 | ST 16 | no (pre-count spot check 9) | research consistent |
| 19 | 1,163 | 25 | ST 21 | no | vintage (A1-1) |
| 20 | 3.82 million tonnes | 3 | MT 45 | yes (Alaska Business) | confirmed, record |
| 21 | nearly 460,000 | 13 | ST 149 | yes (Alaska Public Media) | confirmed; attribution (A1-11) |
| 22 | 1,733,016 | 7 | MT 119 | yes (CruiseMapper) | confirmed; Oct 6; 4th consecutive |
| 23 | 1,688,738 | 8 | MT 120 | partly (CruiseMapper prints it too) | consistent |
| 24 | 145,080; 8,754 | 6 | MT 22, 24 | yes (CEW) | confirmed |
| 25 | 29,137; $1,154; 2,962 | 6 | MT 66 to 68 | yes | confirmed |
| 26 | 35,985; 2,497 | 6 | MT 92, 94 | yes | confirmed |
| 27 | 16,413; $1,449; 1,185 | 6 | MT 113 to 115 | yes | confirmed |
| 28 | 20,214; $1,297 | 6 | MT 134, 135 | yes | confirmed |
| 29 | $36.14; 17,980 | 14 | MT 25, 26 | yes (OEWS Anchorage) | confirmed; June 18, reissued June 24 |
| 30 | $35.32 | 29 | MT 91 | no | research consistent |
| 31 | $54M; $83.1M | 10 | ST 95, 96 | yes (SBDC) | confirmed; "from 2022" absent (A1-4) |
| 32 | 289,221; 97,083; 31,182; 61,327; 13,377; 12,430 | 27 | MT 12, 85, 112, 131, 150, 162 | no (pre-count spot check 12) | research consistent |
| 33 | 183.4; 200.5 thousand | 42 | MT 15, 17 | no (pre-count spot check 10) | research consistent, NSA |
| 34 | 38.2 thousand | 45 | MT 87 | no | research consistent |
| 35 | $57.5 million; 492,000; 526,000 | 28 | MT 49, 50 | no (pre-count 15) | research consistent |
| 36 | 40.5; $481,000; $474,200 | 38 | MT 40, 43, 74 | no (pre-count 6) | research consistent |
| 37 | $69.48; 477,000 | 16; 15 | ST 82, 83 | no | research consistent |

Fetched URLs (15): bls.gov/regions/west/alaska.htm; bls.gov/eag/eag.ak.htm; labor.alaska.gov news26-19; labor.alaska.gov news26-2; BLS county employment and wages Alaska (twice); Alaska Public Media airports 2026-10-12; Alaska Business AEDC 2026-01-30; FRED AKPOP, AKNGSP, AKRGSP, AKRQGSP; tax.alaska.gov Spring 2026 forecast (twice); CruiseMapper 16846; aksbdc.org/ssbci (twice); BLS OEWS Anchorage. Doors: one curl 403 (BLS county release), recorded.

Dates: every printed figure traces to a dated research row (I77, I86); the FEMA rows carry their own declaration dates; the BLS area pages are periodic (D12). Single-property values (Touchmark, hotels, UAF, LNG, rail grant) are printed without numbers or with none counted (I64). No arithmetic on the page: +6,379 and +1,649 are the publishers' own printed changes.

## Count after my confirmed findings
Deletions that remove counted figures: A1-1 (1,163), A1-3 (102.0 million), A1-2 strict (365.2, 17.7, 76.8, 13.9).
- Strict: 71 - 6 = 65 counted (research 60, register 5).
- With A1-2's lighter option: 66 counted (research 61, register 5).
Floors (A6): READY 30 with 20 research, landing 25 with 15: both hold on either reading with a margin of 40 research. Every other fix is a deletion of words with no counted figure.

Severity tally: BLOCKER 0; MAJOR-FACTUAL 9 (A1-1 to A1-9); MAJOR-NONFACTUAL 0; MINOR 4 (A1-10 to A1-13; A1-12 is a clean check).
