# GEO-5 t1 freeze 1, attacker B (gates, links, sameness, buyer intent, claims)

Pages: `/states/colorado/` (source `src/pages/states/colorado.html`) and `/states/colorado/denver/` (source `src/pages/states/colorado/denver.html`), frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t1/`.

## Setup and reproduction base

- Hashes checked against `FREEZE-t1-f1.txt` before and after my gate rerun: sources 16c81ff9... and f98aaaa9..., rendered 7cf9c1cc... and 6d03beba... All four match; the copy is unchanged.
- Gate rerun from inside the copy: `gates.py --root . --git-dir ~/Downloads/wt-rollout-geo-5 --urls /states/colorado/,/states/colorado/denver/ --new ... --stage ready --only 7,9,10 --skip-look` (output to my scratchpad, not into the drafts): 7, 9 and 10 GREEN, required edges all present, SBA mandate sentences 0. `pagecheck.py --figures` reproduces gate 3: Colorado 6,960 words, 94 counted (85 research, 9 register); Denver 3,359 words, 55 counted (46 research, 9 register; the register list counted is the ten Denver markers less `acs5_renter_occupied`). The gate outputs agree with the copy.
- Sameness: `drafts/geo-5/tools/sameness.py --ours <both sources> --against <copy>/src/pages <the eight other GEO-5 drafts, Colorado excluded>` (98 files), then Colorado against Denver; frames with `tools/frames.py` over every GEO-5 draft and the landed Montana, Idaho, Utah, Nebraska, Treasure Valley and Houston sources; a hero and description scan over every landed source for migration openers; a cases and metros section scan over every landed state source.

## Findings

### A2-1 BLOCKER (forbidden claim: site visit). Colorado, #supply
Quoted: "For Boulder, Greeley, Pueblo, Grand Junction and the resort counties no current broker report was found, and a study for one of those markets builds its supply count from county assessor records and a site survey."
Reproduction: line 583 of the source. The writer brief and the review brief forbid any site visit claim (no record states one). A "site survey" that builds a supply count is field work at or around the site: a site visit in substance.
Smallest fix: delete " and a site survey" (old "from county assessor records and a site survey." new "from county assessor records.").

### A2-2 MAJOR-FACTUAL (rule: ruling 10). Denver, #economy register table
Quoted rows: "Median household income, inflation-adjusted dollars (B19013) ... $105,762 ... 2020 to 2024, five-year" and "Median household income, inflation-adjusted dollars (B19013), one-year ... $108,046 ... 2024, one-year".
Reproduction: `grep -o 'mkt:[a-z0-9.-]*_[a-z0-9_]*'` on the Denver source shows both `cbsa-19740.acs5_median_hh_income` and `cbsa-19740.acs1_median_hh_income`; pagecheck counts both in the register 9. Ruling 10: "Never put two vintages of one series on one page"; the tranche's own assignment (`assign/colorado.json`, register rule) reads "acs1 and acs5 of the same measure are one series for this rule". The Colorado page obeys it (acs5 income, acs1 rent only); Denver does not.
Smallest fix: delete the whole one-year row (`<tr><td>Median household income, inflation-adjusted dollars (B19013), one-year</td>...[^14]</td></tr>`). Source 14 is then cited nowhere on the page; drop it from the sources list (gate 7 counts uncited sources). Denver falls to 54 counted (46 research, 8 register), above every floor.

### A2-3 MAJOR-FACTUAL (wrong statement about the page itself). Colorado, #costs
Quoted: "Labor cost is better documented: each market section prints its county's first-quarter 2026 average weekly wage and its metro's May 2025 mean hourly wage, which together set a starting point for an operator's payroll."
Reproduction: the #mountain-resort-counties section prints weekly wages for Eagle, Pitkin, Routt and Summit and no mean hourly wage (it is four counties, not a metro; `grep -n 'mean hourly' colorado.html` returns the six metro sections only).
Smallest fix: old "and its metro's May 2025 mean hourly wage" new "and each metro section its metro's May 2025 mean hourly wage".

### A2-4 MAJOR-NONFACTUAL (opening move against landed neighbours, I74, I81, I84). Colorado, hero_sub sentence 1, and the plan it carries through FAQ 1 and the CTA
Quoted: "From July 2024 to June 2025, 12,100 more people moved out of Colorado to other states than moved in from them, while net international migration was +15,356 and births numbered 65,380, the most since 2017, ..."
Reproduction: a scan of every landed source's hero_sub and description for migration openers. Landed Nebraska (a live neighbour) opens: "Nebraska counted 2,018,006 residents on July 1, 2025, with two migration streams running in opposite directions, net domestic migration of -366 against net international migration of +6,599 ... so a feasibility study here begins by saying which stream the trade area draws on". Landed Utah (a live neighbour) opens on births as the driver of the same Vintage 2025 year. Colorado's hero is Nebraska's construction (domestic out against international in, same Census year) with Utah's births added, and its CTA ("A demand case written today stands on births, arrivals from abroad and the county payroll rather than on in-movers from other states") is Nebraska's "which stream the trade area draws on" move. Missouri, Texas, Florida and Hawaii also open on migration components. Under I81 and I84 the landed page keeps the plan.
Smallest fix: the integrator's call, since the lead fact is the page's own. Either lead the hero on a Colorado-only story the page already carries (the 2024 to 2026 housing laws and the HOME Act deadlines, or the record 2025 travel spending with fewer tourism jobs) and move the migration components to the second sentence, or keep migration but drop the "opposite directions" pairing from the hero (print only the state's own Vintage 2025 births record there and leave the domestic and international components to #migration and FAQ 1).

### A2-5 MAJOR-NONFACTUAL (hero plan shared with GEO-5 drafts) plus a soft service claim. Colorado, hero_sub sentence 3
Quoted: "Each is built on county records such as the first-quarter 2026 wage file, which puts Pueblo County at $1,120 a week and Boulder County at $2,107 [^2]."
Reproduction: frames.py over the GEO-5 drafts. The hero plan "lead fact, firm statement, then 'Each (one / study) <is built on or sets out> records'" is Alaska's ("Each one sets the borough's or census area's own population, payroll and wage record beside that state forecast"), Virginia's ("each study built from dated records like the ones on this page") and the District's ("Each one states which geography a figure describes"). "Each is built on county records" is also a promise about every study that no record states.
Smallest fix: delete sentence 3 whole. $1,120 and $2,107 stay in #pueblo and #boulder with citation [^2]; the hero keeps its cited counted figures (12,100, +15,356, 65,380); no count changes.

### A2-6 MAJOR-NONFACTUAL (section frame of a landed page). Colorado, #metros h2
Quoted: "Eight Colorado markets: Denver on a page of its own and seven sections on this one."
Reproduction: landed California's #metros h2 is "Eight California markets: Sacramento on its own page, and seven in the sections that follow."; landed Idaho's is "The Treasure Valley on a page of its own, and six Idaho counties read in the sections below." Colorado's is California's construction word for word in plan (count, standing metro on its own page, seven sections).
Smallest fix: a heading in Colorado's own geography that still counts the markets in words, for example "Eight Colorado markets from the Front Range to the Western Slope and the ski counties, Denver among them with a page of its own." (run sameness.py on it before accepting).

### A2-7 MAJOR-NONFACTUAL (cases frames; one introduced by the D18 rewording). Colorado #cases lede; Denver #cases h2 and body
Quoted (Colorado, D18 text): "The case library holds no Colorado project yet."
Quoted (Denver): h2 "The case library has not yet reached Denver, Arapahoe, Jefferson, Adams or Douglas." and body "None of the published cases is sited in these five counties."
Reproduction: a scan of every landed state source's #cases section, and the GEO-5 drafts. Landed Idaho's lede is "The case library holds no Idaho site, live or promised." (the writer brief names Idaho's frame as one to avoid); the Wyoming draft's lede is "The case library does not yet hold a Wyoming project."; Vermont's "The case library has no Vermont project". D18 replaced Colorado's Delaware echo with Idaho's frame. Denver's h2 is the Northern Virginia draft's frame ("The case library has nothing yet from Fairfax, Arlington, Loudoun, Prince William or Alexandria."), and its first body sentence paraphrases landed Charlotte's ("No published case names a site in the eleven counties."), a page the brief names as a model never to copy.
Smallest fix: Colorado lede, for example "Hotels, apartments, glamping and child care have worked cases on this site, none of them in Colorado."; Denver h2, for example "Worked cases near Denver: none sited in the five counties so far." and delete Denver's first body sentence (the h2 then carries the fact). Rerun sameness.py and the cases scan on the new text.

### A2-8 MAJOR-NONFACTUAL (shared 8-word runs and plan in the in-body CTAs). Colorado #mountain-resort-counties last paragraph; Denver #lenders last paragraph
Quoted (Colorado): "A briefing request for any of the markets above, or for Denver, needs only a description of the project, the county or market section where its site sits, and the capital source the sponsor is approaching. The reply sets out the analytical framework the study will use, the deliverable that program asks for and the next steps."
Quoted (Denver): "A briefing request needs three things from you: what is being built or bought and at what size, the county or submarket where the site sits, and the lender or program expected to fund it. Our reply sets out the analytical framework, ..."
Reproduction: sameness.py reports Colorado sharing with the Virginia draft "the reply sets out the analytical framework the", "the deliverable that program asks for and the", "that program asks for and the next steps", "program asks for and the next steps request", "asks for and the next steps request a", "for and the next steps request a methodology", "and the next steps request a methodology briefing" (Virginia line 694: "The reply sets out the analytical framework, the deliverable that program asks for and the next steps."). D18 says only register labels, sba text and practice-area names remained shared; this run is prose. Plan: Denver's "needs three things" is Virginia's ("A first message about a Virginia project needs three things") and North Dakota's ("can ask for a briefing with three facts"); Colorado and Denver open the same way ("A briefing request ... needs").
Smallest fix: Colorado, old "The reply sets out the analytical framework the study will use, the deliverable that program asks for and the next steps." new "In return comes the analytical framework the study would follow, the deliverable required by that program and what happens next." Denver, old "A briefing request needs three things from you:" new "To open a Denver briefing, send" (the colon list then reads as the object). Rerun sameness.py on both.

### A2-9 MAJOR-NONFACTUAL (FAQ frames shared with sibling drafts; the same answer move on parent and child) and a self-contradiction. Colorado FAQ 2; Denver FAQ 7
Quoted (Colorado Q): "Which loan programs does the study serve, and what starts a Colorado engagement?" Answer ends: "The county is asked for first because one quarter can move a county's average: Larimer County's weekly wage was $1,627 ..."
Quoted (Denver Q): "What does Feasibility Study Company need to start a Denver project, and for which programs?" Answer ends: "The county is the first question because the year to March 2026 split the five: ..."
Reproduction: frames.py. Northern Virginia's draft asks "Which financing programs is a feasibility study in Northern Virginia written for, and what starts one?" (Colorado's frame); Virginia's asks "What does a feasibility consultant need to start a study in Virginia?" (Denver's frame). Both Colorado and Denver close the answer with the same move ("The county is asked for first / is the first question because ..."), against ruling 4 (FAQ answers unique per page). Each closing sentence also contradicts the sentence before it in the same answer, which lists the project first and the county second; the in-body CTAs list the project first as well. "One quarter can move a county's average" turns the body's hedge on Larimer ("can reflect a few large employers") into a statement.
Smallest fix: delete the closing sentence of each answer (from "The county is asked for first" to the end in Colorado; from "The county is the first question" to the end in Denver); every figure in them stays in the body with its citation, so no count changes. Reword both questions off the sibling frames, for example Colorado "Which capital sources is a Colorado study written for?" and Denver "What goes into a Denver briefing request?" and rerun frames.py against all GEO-5 drafts.

### A2-10 MAJOR-NONFACTUAL (CTA band plan shared with the District draft). Denver, cta
Quoted: h2 "Denver's third-quarter 2026 broker figures are dated October. A study written now reads the market as it stands."
Reproduction: frames.py. The District draft's CTA: "... and the newest of their releases is dated October 2026. // A study commissioned now is written to the October releases rather than to a summer count ...". Same plan: releases dated October, then "A study written / commissioned now". Virginia ("already in print ... A study written against those releases carries their dates") and North Dakota share the family.
Smallest fix: a band from Denver's own lead, for example h2 "Downtown and the suburbs moved in opposite directions in Q3 2026; a Denver study says which side its building is on." keeping the p's first sentence and dropping no figure (the band carries none now and must not, I181).

### A2-11 MAJOR-NONFACTUAL (description plan shared with in-flight drafts). Denver, description
Quoted: "Feasibility Study Company prepares feasibility studies in Denver for owners, developers and the SBA, USDA and bank lenders behind them. Downtown vacancy: 40.1%." (160 characters, counted.)
Reproduction: frames.py. The District draft: "Feasibility Study Company prepares feasibility studies for owners, developers and SBA, USDA or bank lenders in Washington, DC, with office vacancy at 23.5%." Same plan and the same appended figure type (office vacancy). Northern Virginia, Wyoming and Virginia also run firm statement first with one figure appended. "lenders ... behind them" is also Colorado's hero ("whichever SBA, USDA and bank lenders stand behind them").
Smallest fix (157 characters, counted): "Downtown Denver office vacancy hit 40.1% in Q3 2026. Feasibility Study Company prepares Denver studies for owners, developers and SBA, USDA and bank lenders."

### A2-12 MAJOR-NONFACTUAL (neighbour mention not earned by a fact; imprecise geography). Colorado, #greeley paragraph 1
Quoted: "The Greeley metro is Weld County alone, which runs north to Wyoming and east to <a href="/states/nebraska/">Nebraska</a>; a site near either line may draw customers from across it, and the figures here stop at the Colorado border."
Reproduction: no row in ST-COLORADO or MT-COLORADO concerns Wyoming or Nebraska (grep for Wyoming, Nebraska, border: none in the Greeley rows). Nothing on the page makes either line matter to a Greeley market; "may draw customers from across it" is an uncited demand claim. Nebraska touches Weld only at its northeast corner along the 41st parallel (Kimball County), so "east to Nebraska" is imprecise. The link is not needed for any edge: the generated band `#neighbors` already links Kansas, Nebraska, New Mexico, Oklahoma and Utah, and gate 9 required edges are state and metro only. Wyoming has no page and is unlinked, which is right, but its mention carries no fact either.
Smallest fix: old "The Greeley metro is Weld County alone, which runs north to Wyoming and east to <a href="/states/nebraska/">Nebraska</a>; a site near either line may draw customers from across it, and the figures here stop at the Colorado border." new "The Greeley metro is Weld County alone, and the figures here stop at its edges."

### A2-13 MINOR (neighbour link without a fact). Colorado, #grand-junction paragraph 2
Quoted: "Mesa County runs to the <a href="/states/utah/">Utah</a> line. The metro is Mesa County alone, so the figures here stop at the state border; a highway, lodging or retail project drawing on traffic from Utah sources that side from Utah's own series."
Reproduction: no research row on Utah traffic or cross-border demand; the claim that projects draw on traffic from Utah is uncited. Utah is already linked from the generated neighbour band. The border is real (register: Mesa is a one-county CBSA at the state line), so the scope statement can stay; the link and the demand clause are the part with no fact.
Smallest fix: old "Mesa County runs to the <a href="/states/utah/">Utah</a> line. The metro is Mesa County alone, so the figures here stop at the state border; a highway, lodging or retail project drawing on traffic from Utah sources that side from Utah's own series." new "The metro is Mesa County alone, so the figures here stop at the Utah line."

### A2-14 MINOR (plain claim with no citation). Denver, #corridors
Quoted: "Two features of these roads change how a count reads. E-470 is a toll road, so its mainline volume includes drivers who reach a corner only by exiting and paying. And where the nearest station sits on a different road ..."
Reproduction: MT-COLORADO holds no E-470 row and records "Denver CDOT traffic counts" as NOT FOUND (line 82). Outside the record the statement is broadly right (a WebSearch shows E-470 is all-electronic with five mainline and 34 ramp toll gantries, results from wikipedia.org/wiki/E-470 and e-470.com's 2020 study PDF), but the page cites nothing and the toll mechanics vary by interchange.
Smallest fix: old "Two features of these roads change how a count reads. E-470 is a toll road, so its mainline volume includes drivers who reach a corner only by exiting and paying. And where the nearest station" new "Where the nearest station".

### A2-15 MINOR (plain claim with no citation). Denver, #rules
Quoted: "Aurora reaches into Arapahoe, Adams and Douglas counties, so the county line alone does not settle which code applies."
Reproduction: no research row (grep Aurora in MT-COLORADO: only the CBSA name). True by general knowledge, uncited.
Smallest fix: delete the sentence.

### A2-16 MINOR (plain claim with no citation). Denver, #rules
Quoted: "Water and sewer service on the Front Range is provided by a patchwork of city utilities and special districts, so the study attaches a written will-serve letter ..."
Reproduction: no research row on water or sewer providers (grep water, sewer, special district: none). Uncited generalization.
Smallest fix: old "Water and sewer service on the Front Range is provided by a patchwork of city utilities and special districts, so the study attaches" new "The study attaches".

### A2-17 MINOR (uncited rule claim). Colorado, #capital USDA
Quoted: "... it is checked there rather than assumed from a county name; a town in a metro county can qualify and a resort town in a rural county may not."
Reproduction: no research or practice-area citation. Under the program population limits (Business and Industry excludes places over 50,000; Community Facilities 20,000) every Colorado resort town is population-eligible, so "may not" has no stated basis.
Smallest fix: delete "; a town in a metro county can qualify and a resort town in a rural county may not" (end the sentence after "county name").

### A2-18 MINOR (implied acceptance; uncited generalization). Denver, #economy paragraph 1
Quoted: "Owners who look for a Denver feasibility study company usually need one document that their lender's credit officer will accept."
Reproduction: "will accept" placed before "Feasibility Study Company prepares ..." reads as a promise that the firm's study is accepted, next to the forbidden guarantee and approval claims. "usually" has no record.
Smallest fix: "will accept" to "will review" (keeps the keyword mention, one of one for that form).

### A2-19 MINOR (comparison in words, I60(b); unsupported inference). Denver, #lenders paragraph 1
Quoted: "Investment sales are the clearest sign of lender and buyer appetite in the record: both the industrial and the retail sales totals in the supply section rose sharply over the year in Q3 2026."
Reproduction: "rose sharply" states a comparison with no value in the sentence (the +80.5% and +95.7% are two sections up); sales volume says nothing direct about lender appetite.
Smallest fix: delete the sentence.

### A2-20 MINOR (uncited underwriting rule). Denver, #lenders paragraph 2
Quoted: "In Denver the coverage test is where the county payroll split shows up: a business whose customers come from a county that lost covered jobs needs its revenue case cut back before coverage is tested."
Reproduction: no SBA rule or research row says this; it reads as a lender requirement.
Smallest fix: delete the sentence.

### A2-21 MINOR (shared 8-word runs outside the allowed categories)
- Colorado #migration p1 and Denver #economy p1 share "Feasibility Study Company prepares independent, lender-grade feasibility studies for" (sameness.py, Colorado against Denver); Colorado shares "independent lender grade feasibility studies for projects in" with the Northern Virginia draft (its service description). Fix: Colorado old "prepares independent, lender-grade feasibility studies for projects in Colorado" new "writes independent feasibility studies to lender standard for Colorado projects".
- Colorado #capital "a 504 project that is a new business or a special-purpose property puts in" shares "a new business or a special purpose property" with landed Texas, two hubs and two cases (prose beside the sba marker, not marker text). Fix: old "a 504 project that is a new business or a special-purpose property puts in" new "a 504 borrower in business two years or less, or buying special-purpose property, puts in".
- D18's own rewording created one: Colorado "The tests are explained on the SBA 7(a) and 504 lending page." shares "tests are explained on the sba 7 a and" with landed Sacramento ("SBA's own program tests are explained on the SBA 7(a) and 504 lending page."). Fix: new "The <a href="/practice-areas/sba-7a-504/">SBA 7(a) and 504 lending</a> page covers those tests."

### A2-22 MINOR (echo of a taken frame). Colorado, #rules paragraph 1
Quoted: "... and so they change the inputs of a residential or mixed-use pro forma before the market is read at all."
Reproduction: the taken-frames list holds Ohio's "rules write the budget before the market does".
Smallest fix: old "how fast it can be approved, and so they change the inputs of a residential or mixed-use pro forma before the market is read at all." new "how fast it can be approved."

### A2-23 MINOR (description wording; I89 judgment). Colorado, description
Quoted: "12,100 net lost to other states to June 2025. Feasibility Study Company prepares ..." (160 characters, counted.)
Reproduction: "12,100 net lost" is not a sentence and "to June 2025" drops the period's start. The same fact is also in the hero, the stats band, FAQ 1, #migration, the events table and, in words, the CTA h2: the description is past the fourth restatement I89 warns about.
Smallest fix (155 characters, counted): "Net domestic migration, year to June 2025: -12,100. Feasibility Study Company prepares Colorado studies for owners, developers, SBA, USDA or bank lenders." If A2-4 moves the lead, the description should follow the new lead.

### A2-24 MINOR (FAQ frame repeated between parent and child; geography theme of the District draft)
Colorado FAQ 5 "What does Colorado's record 2025 tourism year mean for a hotel or restaurant study?" and Denver FAQ 5 "What does the Denver visitor count tell a hotel study?" are one frame on parent and child. Denver FAQ 4 "What area does each figure on this page describe?" and its sources_lede ("Each figure names its publisher, its date and the area it covers") carry the District draft's hero theme ("Each one states which geography a figure describes"). Fix: reword Denver FAQ 5, for example "How many overnight visitors does a Denver hotel study start from?"

### A2-25 MINOR (rank, ruling 4). Colorado, #tourism
Quoted: "SnowBrains puts the Denver metro's travel spending at about $14.2 billion, 48.5% of the statewide total in the article's own reckoning [^7]."
Reproduction: pagecheck counts $14.2 billion and 48.5% on the state page. They describe the Denver metro, and ruling 4 places a metro's counted figure on the most specific page. The Denver page does not print them, so nothing double counts, but the state page counts a Denver figure while its #metros paragraph says Denver's record is read on its own page.
Smallest fix: wrap the clause in `data-fsc-nocount` on the state page (Colorado 92 counted), or move it to the Denver #economy visitor paragraph.

## Tested and not raised
- Buyer-intent fields: titles in the house pattern (66 and 62 characters); H1s "Colorado Feasibility Studies" and "Denver Feasibility Studies"; descriptions 160 and 160 characters; both heroes carry the firm statement for owners, developers and SBA, USDA and bank lenders and cited counted figures. A scan of both sources for fee, price, turnaround, days, weeks, guarantee, approval, office, local staff, "on the ground", "our team", licence, credential found none beyond A2-1 and A2-18 ("local" occurs only for local governments and codes; "staff" only for Legislative Council Staff, a city's planning staff and operators' staff).
- In-body CTAs: one each, Colorado at the end of the last market section, Denver at the end of #lenders, both linking `/#contact`; content limited to the record (framework, deliverable, next steps).
- SBA wording: only `sba:` marker text with "may require"; gate 7 rerun: mandate sentences 0. "the deliverable the lender's program requires" (Denver CTA p) is the home page's sanctioned wording, not a mandate.
- Keyword cap (I89) on rendered visible text: Colorado "colorado feasibility study consultant" 1, "company" 1, bare "Colorado feasibility study/studies" 2 (H1 and #cases), "feasibility studies in Colorado" 1; Denver 1, 1, 2, 1. All within three.
- Closing bands carry no figure (I181): Colorado has no digit; Denver only dates (Q3 2026, October).
- Links: required edges present both ways (Colorado links `/states/colorado/denver/` five times in main; Denver links `/states/colorado/` four times and four sibling sections); gate 9 rerun GREEN.
- Denver uncited claims that hold on the register: "Boulder County ... is a separate metro area" (`data/markets/geographies.json`: 08013 sits in CBSA 14500, not 19740), the ten-county list of Denver-Aurora-Centennial (CBSA 19740 counties 001, 005, 014, 019, 031, 035, 039, 047, 059, 093), and Colorado Springs taking in more than El Paso (Teller in CBSA 17820). "Denver is both a city and a county" is common knowledge; not raised.
- D18 rewordings, read sentence by sentence against `work/pre-sameness/`: the CTA h2 ("the moves out to other states outnumbered the moves in from them"), "On January 27, 2026 the State Demography Office summarized ...", "jobs in March 2026 at employers covered by unemployment insurance", "The two job counts are separate series, and a study keeps them apart.", "stood at 853.19 for the second quarter of 2026, against a base of 100 ...", "Under it, a standard 7(a) loan has to clear a debt service coverage of 1.15x", "For studies, the governing text is 13 CFR 120.160(b)", Denver "Studies fall under 13 CFR 120.160(b)": all grammatical and true. Two did not escape sameness: the cases lede (A2-7) and "tests are explained on the" (A2-21).
- Colorado "the largest wage increase among the nine large Colorado counties", "the most since 2017", "no over-the-year change" for Pueblo and Mesa, Denver "lowest in at least five years", "almost all of it in Cherry Creek", the TIAA 61% and "reports no metro-wide construction total": each is in its research row's own wording (MT-COLORADO lines 131, 73, 40, 44, 49, 198, 215, rows 107, 63, 30, 34, 39, 153, 163; ST-COLORADO line 13).

## Counts by severity
BLOCKER 1 (A2-1); MAJOR-FACTUAL 2 (A2-2, A2-3); MAJOR-NONFACTUAL 9 (A2-4 to A2-12); MINOR 13 (A2-13 to A2-25).

## Counted figures after my confirmed findings
- `/states/colorado/`: 94 (85 research, 9 register). No fix above removes a counted figure; if A2-25 is applied by nocount, 92 (83 research, 9 register).
- `/states/colorado/denver/`: 54 (46 research, 8 register), after A2-2 deletes the one-year median household income row.
- Both stay above the A6 READY floors (30 in all, 20 research) and the landing floors (25, 15).
