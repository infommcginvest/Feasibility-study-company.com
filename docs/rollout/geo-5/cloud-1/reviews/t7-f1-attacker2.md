# GEO-5 t7 freeze 1, attacker two (gates, links, sameness, buyer intent, claims)

Page: /states/district-of-columbia/ (no metro page). Source `src/pages/states/district-of-columbia.html` in the frozen copy `scratchpad/copies/f1-district-of-columbia/`. Line numbers below are the source's (529 lines).

Comparison set: every landed source in the copy's `src/pages/` (104 files, landed Colorado, Denver, Virginia, Northern Virginia, South Dakota, Maryland and the Montana model among them), the four other GEO-5 drafts in the handoff `pages/` folder (North Dakota, Alaska, Wyoming, Vermont, each at its freeze 1), and the frames recorded in the t3, t4 and t5 attacker-two files.

## What I ran

- Hashes: copy source sha256 `480d775e607ce5a77200f5e83100a91182a036e902c86319bab416d328bef6f5`, byte equal to handoff `pages/district-of-columbia.html` and to the freeze record; rendered `states/district-of-columbia/index.html` `c5ff00e29aaaa37aa4e125769ba005560d59dbd842351fddb234488a1975a8d0`, as the freeze record states.
- Gates rerun from inside the copy (`FSC_PRIVATE=... timeout 900 python3 scripts/qa/gates.py --root . --git-dir /home/user/wt/geo-5 --urls /states/district-of-columbia/ --stage ready --only 3,4,9 --skip-look`): 3, 4, 5 and 9 GREEN. Counted 56 (research 48, register 8/8), overlap max 0.72% (/states/virginia/), inbound under 3: 0, required edges all present. Same numbers as `GATES-f1-district-of-columbia.txt`. That file's gate 13 is RED only because the headless shell path is the Mac's; `GATES-f1-district-of-columbia-g13.txt` reruns it GREEN (1440 and 390, no overflow). The gate outputs agree with the copy.
- Register detail: the page prints 10 `mkt:` values; pagecheck counts 8. Owner-occupied 134,683 and renter-occupied 189,808 are taken as rounded repeats of Michigan's 134,700 and Louisiana's 189,800 (`Site.taken`). That is how the tool works, and it is attacker one's lane; recorded only so the "8/8" is explained.
- Gate 9 inbound, re-implemented (`body_links` over every served page, index set excluded). Ten distinct non-index pages link /states/district-of-columbia/:
  - mesh term `state-district-of-columbia` (requests.json `geo-5-23`): /asset-classes/childcare-and-daycare/, /asset-classes/hotel/, /asset-classes/laundromat/, /asset-classes/private-school/, /asset-classes/quick-service-restaurant/, /asset-classes/self-storage/, /states/hawaii/, /states/massachusetts/, /states/maryland/, /states/virginia/;
  - the generated "Neighboring Markets" lists on /states/maryland/ and /states/virginia/ (topics.json `state_neighbors`).
  - Every term link sits on a mention of the District itself ("37 states and the District of Columbia", "the lowest of the states and the District of Columbia", "a Virginian who commutes to an office in the District of Columbia", and so on). None sits on an institution's name. Without the term the count is 2, as D27 says; with it, 10. The requirement of 3 holds.
- Washington metro section (lines 495 to 504): every figure is metro-wide (BLS Economy at a Glance for the MSA, DOES's MSA labor force, WJLA's metro federal count), DC-MD division (DOES) or broker (Matthews, geography unstated; Yardi Matrix, metro). The section prints no figure for any single Virginia county, and names none. The only Virginia place names on the page are inside the metro's official name. D7 holds.
- `tools/sameness.py --ours <copy source> --against <copy src/pages> <ND, AK, WY, VT drafts>`: max 0.87% (/states/colorado/denver/). With `sba:` marker text and register row labels set aside, the only 8-word runs are listed in A2-24.
- My own pass (scratchpad `t7a2-work/norm.py`): state and place names folded to one token, digits and `sba:`/`mkt:` regions dropped, 6, 7 and 8-word shingles against the same set. The hits are used below. `tools/frames.py` was run on all four drafts and on landed Colorado, Denver, Virginia, Northern Virginia, South Dakota, Montana and Maryland. FAQ h2s, stats labels and section order were compared across all landed state sources. The section order is the page's own.
- Rendered `<main>` visible text (sources list removed), keyword cap (I89): "District of Columbia feasibility study consultant" 1 (FAQ 7 question), "District of Columbia feasibility study company" 1 (#capital, line 513), bare "District of Columbia feasibility study" 3 (those two plus line 381). H1 "District of Columbia Feasibility Studies". Within the cap. Title "District of Columbia Feasibility Study Consultants | Feasibility Study Company" (house pattern); title and H1 unique across the copy. Description 156 characters.
- Forbidden service claims: scan of the visible text for fee, price, turnaround, week, days, guarantee, approval, staff, local, on the ground, our team, we, our, licens, certif, credential, site visit, deliver, require, must. No hit is a claim about the firm. "guarantee" hits are USDA program names; "local" is "state and local government"; "staff" is "staffing plan", "staff and visitors" and "draws staff"; "licens" and "certif" are rules the study consults (liquor and child care licensing, certificate of occupancy, certificate of need); "deliverable that program requires" is the home page's record wording ("the deliverable your program requires"). No fee, price, turnaround, delivery time, guarantee, approval rate, office, local staff, site visit, licence or credential is promised.
- SBA wording (ruling 8): no "SBA requires". The 13 CFR 120.160(b) text is the `sba:` marker ("may require"); pagecheck's SBA_REQUIRES finds nothing.
- Closing band (rendered `section.cta-band`): the only digits are "2026". It carries no figure (I181). Its claims are A2-3.
- WebFetch: `https://does.dc.gov/release/washington-metros-unemployment-rate-45-percent`, NOT FETCHED: getaddrinfo ENOTFOUND does.dc.gov (the host is outside this session's allowed network domains). No further site was tried. No finding turns on a source document; A2-3 rests on the research row.

## Findings

### A2-1 MAJOR-NONFACTUAL: the mesh puts the Maine and Connecticut state links on District street names
- Page: rendered /states/district-of-columbia/, the term links that `mesh.py` places in #conversions (source lines 380 and 382).
- Text (rendered): `899 <a href="/states/maine/" data-fsc-term="state-maine">Maine</a> Avenue SW near The Wharf` and `The Geneva on <a href="/states/connecticut/" data-fsc-term="state-connecticut">Connecticut</a> Avenue NW`.
- Reproduction: I listed every `data-fsc-term` link in `<main>` with its context; these two are the only state links in the body apart from the writer's own Maryland link. `terms.json` defines `state-maine` ["Maine"] and `state-connecticut` ["Connecticut"]. `term_pattern` blocks only a letter, digit or hyphen next to the term, so a street name matches. A site-wide scan for a state term link followed by "Avenue" or "Street" finds these two and nothing else. A reader who clicks "Maine" in a District address lands on the Maine state page, and the District's streets are named for states, so any later page that gives a DC address will do the same.
- Smallest fix (page only, deletions): line 380 replace "at 2121 Virginia Avenue NW in Foggy Bottom and 899 Maine Avenue SW near The Wharf" with "in Foggy Bottom and near The Wharf"; line 382 replace "The Geneva on Connecticut Avenue NW" with "The Geneva"; line 476 replace "the conversion at 899 Maine Avenue SW near The Wharf" with "the conversion near The Wharf". The page then has no other "Maine" or "Connecticut" (grep). Rerun `mesh.py` and `mesh.py --check`. For the integrator, separately: make `term_pattern` refuse a state term followed by "Avenue".

### A2-2 MAJOR-FACTUAL: the SBA 504 equity rule leaves out its 20% tier, and "meets both tests on projections" misstates both rules
- Page: #capital, line 509.
- Text: "a 504 borrower in business for two years or less, or one whose building is special-purpose, puts in <!--sba:equity.sba_504_new_or_special.value-->15%<!--/sba:...--> of the project cost [^36]. A District hotel or a new restaurant meets both tests on projections, which is where a study's market figures enter the credit file."
- Reproduction: `data/regulatory/sba.json` in the copy holds `equity.sba_504_new_or_special` 15% ("New Business (two years or less) or Limited or Special Purpose Property") and `equity.sba_504_new_and_special` 20% (both R31). `valuation.special_purpose_list` names hotels and does not name restaurants. So a new District hotel is at 20%, not 15%: it is the page's own first example. The next sentence is wrong on both tests:
  - the 504 contribution is an injection of cash or property, not something met "on projections";
  - `dscr.sba_504_basis` reads "historical EBITDA ... projections analysed only where history falls short";
  - the 7(a) coverage floor and the 504 contribution belong to different loans, so no single loan meets "both".
  The precedents are t3 A2-4 (South Dakota) and t5 A2-14 (Alaska), both confirmed or raised as MAJOR-FACTUAL. Landed Colorado prints the 20% tier.
- Smallest fix: after "puts in ...15%... of the project cost", insert ", and <!--sba:equity.sba_504_new_and_special.value-->20%<!--/sba:equity.sba_504_new_and_special.value--> when both apply" before " [^36]". Delete "A District hotel or a new restaurant meets both tests on projections, which is where a study's market figures enter the credit file." Rerun `regulatory.py --check`. `sba:` values are outside the count.

### A2-3 MAJOR-FACTUAL: the closing band claims an October 2026 federal-job release the page never shows, and promises a currency the page's own federal figures do not have
- Page: `cta.h2` (line 94) and `cta.p` (line 95).
- Text: h2 "Three geographies carry the District's federal job loss, the city, its DC-MD division and the Washington metro, and the newest of their releases is dated October 2026." p "A study commissioned now is written to the October releases rather than to a summer count a later release may have restated, and it says whether its demand is drawn from the District, the division or the metro."
- Reproduction: the page's federal-job figures and their releases are:
  - the city: 169,000, from ORA's release of January 28, 2026 [^1] (ST line 42);
  - the division: -25,800 for August 2025 to August 2026, from the DOES release of September 30, 2026 [^5] (MT line 91);
  - the metro: 375,800 to 312,500, from WJLA of July 21, 2026 [^6] (ST line 165).
  The two October releases the page cites, [^18] of October 20 and [^28] of October 28, are used only for sector jobs, labor force and division employment. A reader therefore finds no October federal figure behind the h2. The research holds one (MT line 89: -26,300 for the division, September 2025 to September 2026, published 2026-10-28), but the page does not print it. Instead FAQ 1 (line 65) and #washington-metro (line 498) print the August count, which is exactly the "summer count a later release may have restated" that the band says a study avoids. The band's first p sentence is also a promise about every study that no record states (WRITER-BRIEF records: framework, deliverable, next steps).
- Smallest fix: h2: delete ", and the newest of their releases is dated October 2026" and change the comma after "federal job loss" to a colon ("...federal job loss: the city, its DC-MD division and the Washington metro."). p: delete "A study commissioned now is written to the October releases rather than to a summer count a later release may have restated, and it says whether its demand is drawn from the District, the division or the metro. " and change "To open one," to "To open a study,".

### A2-4 MAJOR-FACTUAL: "than most state records" and "mostly housing and energy capital" have no source
- Page: #economy opening paragraph (line 326); #capital (line 511).
- Text: "The District's record changed faster in 2025 and 2026 than most state records did, and a reviewer judges a District study first on whether its figures are current and whether each one describes the place the project sells to. The first of those records is the payroll." / "The District's own capital is mostly housing and energy capital."
- Reproduction: no row in ST-DISTRICT-OF-COLUMBIA or MT-DISTRICT-OF-COLUMBIA compares the pace of the District's record with the states' records. No row sizes the District's capital programs against one another: the page itself says the SSBCI allocation, DC Green Bank's lending totals and CDFI awards "were not found in a dated source". Both are comparisons in words (I59, I60) with no values. The first is also a study-first sentence in the opening paragraph, the move t5 A2-13 recorded for Alaska. The precedent is t5 A2-15 ("most" claims with no source, MAJOR-FACTUAL).
- Smallest fix: line 326 delete "The District's record changed faster in 2025 and 2026 than most state records did, and a reviewer judges a District study first on whether its figures are current and whether each one describes the place the project sells to. The first of those records is the payroll." (The paragraph keeps the firm sentence, and the next paragraph opens on the ORA record.) Line 511 delete "The District's own capital is mostly housing and energy capital. " (the paragraph then opens "DMPED's July 2026 release reports ...").

### A2-5 MAJOR-FACTUAL: a District median set against metro asking rents in words
- Page: #economy, line 367.
- Text: "and the five-year gross rent median runs well behind the current asking rents a broker reports, so it describes the existing stock rather than what a new building can charge."
- Reproduction: the values behind the comparison are:
  - the register's District median gross rent, $1,954 (ACS 2020 to 2024);
  - Matthews' $2,227, whose geography the report does not state (MT line 100);
  - Yardi's $2,191, metro-level, December 2025 (MT line 109).
  None of the three is printed in the sentence, which is the I60(b) test. The sentence also compares gross rent with advertised asking rent. And it sets a District value against rents that the page itself (line 503) says "Neither describes the District alone." The conclusion drawn ("what a new building can charge") rests on that cross-geography comparison.
- Smallest fix: delete ", and the five-year gross rent median runs well behind the current asking rents a broker reports, so it describes the existing stock rather than what a new building can charge". The sentence ends "The tenure counts are the base a multifamily study starts from."

### A2-6 MAJOR-NONFACTUAL: the hero opens on the firm sentence and then on a sentence about every study, with the lead fact last
- Page: `hero_sub`, line 9.
- Text: "Feasibility Study Company prepares feasibility studies in Washington, DC, ... they borrow from. Each one states which geography a figure describes, because the federal job loss is measured for the District, for the DC-MD division and for the whole metro, and the three counts are not one series. In the Office of Revenue Analysis's reading ... 169,000 of them were federal [^1]."
- Reproduction:
  - I81(1): every later hero "opens on its own lead fact, never on a sentence about the study". Here the first two sentences come before any fact. The first is about the firm; the second is "Each one", that is every study.
  - Firm-first is landed South Dakota's opener ("Feasibility Study Company prepares feasibility studies in South Dakota for ... The lead fact on this page is a tax share"). t3 A2-8 already recorded that the two heroes share it.
  - The "Each one/each is ..." move is landed Colorado's ("Each is built on county records such as ..."), North Dakota's ("The first thing each one settles is ...") and Alaska's ("Each one sets the borough's ... record").
  - The geography argument is landed Denver's hero ("This page measures five counties ... a broker's figure carries the market that firm names").
  - "Each one states which geography a figure describes" also describes every study's content, which no record states. The page's own Matthews figures cannot meet it (lines 81 and 502: the report "does not state its geography").
  - The hero also drops the body's "preliminary" from 739,200 (body line 327: "a preliminary figure it described as the lowest ...").
- Smallest fix: delete the second sentence and move the ORA sentence to the front, restoring "preliminary". Result: "In the Office of Revenue Analysis's reading of the November 2025 employment report the District held 739,200 jobs, a preliminary count it described as the lowest since the year after the COVID-19 lows, and 169,000 of them were federal [^1]. Feasibility Study Company prepares feasibility studies in Washington, DC for owners, developers and their SBA, USDA and bank lenders." (The firm sentence also takes A2-7's fix.) Fact then firm is the house minimum (t5 A2-3's ruling).

### A2-7 MAJOR-NONFACTUAL: both firm sentences use the clients-and-readers construction of four sibling pages
- Page: `hero_sub` (line 9) and the opening paragraph (line 326).
- Text: hero "written for the owners and developers who commission them and read by the SBA, USDA and bank lenders they borrow from"; opening "independent, lender-grade analyses written for the owner or developer who commissions them and for the bank, SBA lender or other capital source that has to approve the loan".
- Reproduction (frames.py and the first paragraph of every sibling):
  - North Dakota hero: "the owners and developers who commission it and the bank, SBA or USDA lender who decides on the loan". The 6-word folded run "the owners and developers who commission" is shared.
  - Vermont: "serves two readers: whoever builds or buys the property, and the bank, SBA lender or USDA program that must approve its loan". The 7-word folded run "and for the bank SBA lender or" is shared with Vermont's hero.
  - Alaska: "the owner or developer who proposes the project and the lender who has to approve it".
  - Landed South Dakota: "The clients are owners and developers, and the readers are the SBA lenders, USDA Rural Development and banks".
  - Wyoming: "The client is the owner or developer ..., and the reader is whoever will lend on it".
  t3 A2-10 and t4 A2-15 recorded this construction as taken.
- Smallest fix: hero as in A2-6 ("... in Washington, DC for owners, developers and their SBA, USDA and bank lenders."). Opening: replace "independent, lender-grade analyses written for the owner or developer who commissions them and for the bank, SBA lender or other capital source that has to approve the loan." with "independent, lender-grade analyses for owners, developers and their lenders."

### A2-8 MAJOR-NONFACTUAL: the description is landed Denver's description, office vacancy and all
- Page: `description`, line 6.
- Text: "Feasibility Study Company prepares feasibility studies for owners, developers and SBA, USDA or bank lenders in Washington, DC, with office vacancy at 23.5%."
- Reproduction:
  - Landed Denver: "Feasibility Study Company prepares feasibility studies in Denver for owners, developers and the SBA, USDA and bank lenders behind them. Downtown vacancy: 40.1%." It has the same construction (firm sentence, then a trailing office vacancy rate).
  - Wyoming: "... for owners, developers and bank, SBA or USDA lenders, citing $67.4 million of lodging tax."
  - The SEO brief allows "No frame another landed page or GEO-5 draft uses". t3 A2-9 is the precedent.
  - The description's first eight words, "Feasibility Study Company prepares feasibility studies for owners, developers and", are an 8-word run shared with four served case pages (grocery Ness City, self-storage Bardstown, medical office Lebanon, restaurant Sevierville; sameness.py).
  - The figure is printed with no period and no "citywide, all classes" (body line 372: third quarter of 2026), so it is not written as the body writes it (I77, I86; t5 A2-18 is the precedent).
- Smallest fix (158 characters, one counted figure as the body has it, line 327): "Washington, DC feasibility studies for owners, developers and SBA, USDA or bank lenders, by Feasibility Study Company; 169,000 jobs were federal in Nov. 2025."

### A2-9 MAJOR-NONFACTUAL: the closing band's move is landed Denver's and Virginia's
- Page: `cta.h2`, `cta.p` (lines 94 to 95).
- Text: "... and the newest of their releases is dated October 2026." / "A study commissioned now is written to the October releases ..."
- Reproduction: landed Denver: "Denver's third-quarter 2026 broker figures are dated October. A study written now reads the market as it stands." Landed Virginia: "Virginia's 2026 record is already in print: September payrolls, third-quarter broker reports and a tax that began on July 1." / "A study written against those releases carries their dates into the credit file." The move is the same: the newest releases are dated X, and a study written now is written to them. I115 bars a shared CTA move. The 7-word run "a study commissioned now is written to" is also in North Dakota's freeze 1 band; t4 A2-17 assigns the fix to North Dakota.
- Smallest fix: A2-3's deletions remove the move. The h2 then states the three geographies, which is the page's own lead.

### A2-10 MAJOR-NONFACTUAL: the engagement sentences reuse landed Northern Virginia's, Denver's and Virginia's constructions
- Page: in-body CTA (#washington-metro, line 504), FAQ 7 (lines 88 to 89), `cta.p` (line 95).
- Text and match:
  - In-body CTA: "can start with three facts: what is to be built, bought or converted; the ward or submarket that holds the site, or the Maryland county if the site sits on that side of the division; and the capital being sought, be it bank debt, an SBA-backed loan, ..." Landed Northern Virginia: "To start a study, send three things: what is to be built, bought or refinanced; which of the five jurisdictions holds the site, or the submarket if the parcel is not fixed yet; and where the money is coming from, whether an SBA lender, ...". Same count, same three clauses, same "or" alternative inside the second, same list of sources. The folded 7-word run "what is to be built bought or" is shared. Landed Denver: "needs three things from you: what is being built or bought ..., the county or submarket where the site sits, and the lender or program".
  - FAQ 7 answer: "The sponsor's first message gives the project, the ward or submarket that holds the site and the capital it is seeking. What comes back is the analytical framework the study will apply, ..." Landed Virginia's band: "An inquiry that names the project, the city or county that holds the site and the capital source is answered with the analytical framework ..." (7-word run "that holds the site and the capital"). Landed Northern Virginia: "The answer is the analytical framework the study will follow" (7-word run "is the analytical framework the study will").
  - FAQ 7 question: "..., and what does the sponsor send first?" This is the two-part programs-plus-what-starts-it question of landed Northern Virginia ("Which financing programs is a feasibility study in Northern Virginia written for, and what starts one?"), landed Denver ("..., and for which programs?"), landed South Dakota ("..., and what opens the engagement?") and Wyoming ("..., and what does an inquiry carry?").
  - `cta.p`: "the ward or submarket where the site sits and" is a 7-word folded run with Denver's "the county or submarket where the site sits".
- Smallest fix:
  - In-body CTA: replace "A sponsor with a District project can start with three facts: what is to be built, bought or converted; the ward or submarket that holds the site, or the Maryland county if the site sits on that side of the division; and the capital being sought, be it bank debt, an SBA-backed loan, a Rural Development guarantee from USDA or money raised from EB-5 investors. In return the sponsor gets the analytical framework the study will apply, the form of report that lender or program looks for, and the order of the work that follows." with "Send the project, its ward or submarket (or its Maryland county, on that side of the division) and the capital it seeks, whether bank, SBA, USDA Rural Development or EB-5; the reply names the analytical framework, the program's deliverable and the next steps." Keep the button.
  - FAQ 7: delete ", and what does the sponsor send first" from the question. Delete the answer's last two sentences, from "The sponsor's first message" to "starting evidence.". The question stays an engagement question (which programs), as the SEO brief asks.
  - `cta.p`: "where the site sits" to "of the site" (with A2-3's fix).

### A2-11 MAJOR-NONFACTUAL: the #cases plan is landed Colorado's (and Vermont's, North Dakota's and Alaska's)
- Page: #cases, line 518.
- Text: "A District version of either would keep the case's structure and change three inputs: the payroll series from the economy section instead of a state count, a broker's submarket table instead of a statewide rate, and the building's TOPA status and abatement award instead of another jurisdiction's rules."
- Reproduction:
  - Landed Colorado: "A Colorado feasibility study would follow the same structure with this page's inputs in place of theirs: county wages from the first-quarter 2026 file, ...".
  - Vermont: "A Vermont version of any of them would keep the method and change the inputs: the county wage ... in place of the payroll line, ...".
  - North Dakota: "A North Dakota version of any of them would replace the wage line ...".
  - Alaska: "Their structure carries over to Alaska; their inputs do not. Here the payroll line comes from ...".
  The same move: a version for this state keeps the structure and swaps a list of inputs led by the payroll or wage line. Colorado landed first and holds it (I84: a landed frame is not exempt). The page's first sentence ("the two property types most of this page's District records bear on") is the District's own; t3 A2-14 had South Dakota yield it. The claim checks: the copy serves five SBA hotel cases and six agency multifamily cases, and no case is set in the District.
- Smallest fix: delete the second sentence ("A District version of either ... rules.").

### A2-12 MAJOR-NONFACTUAL: six headings and a card repeat landed or sibling frames
- Page: `data-h2` of #costs (line 399), #supply (413), #events (421, with its lede at 423), #metros (448), #capital (507); FAQ h2 (line 61); the Capitol Riverfront card (line 452).
- Text and match:
  - #costs "Labor priced from the wage file; construction, insurance and public money priced by quote and by forecast." Landed South Dakota: "Labor and land carry dated prices; building costs and insurance premiums have to be quoted for the site." Landed Virginia: "Wages and power carry dated figures; insurance premiums and building costs do not." North Dakota: "Labor priced county by county, ... and building and insurance costs that need quotes." Vermont: "... labor priced by the county, and construction and insurance that need quotes."
  - #supply "Visitors, their spending and the housing count: the District's citywide tallies." Landed Montana, the writer brief's model: "Tank releases, liquor licences by quota area and small firms: Montana's statewide tallies."
  - #events "The District's dated record from the RENTAL Act vote to the October 2026 releases." North Dakota: "North Dakota's dated record from the October 2024 fires to the ethanol plant of October 2026." Wyoming: "Wyoming's dated record, from the 2024 wildfire declaration to the property tax ballot." Landed South Dakota: "South Dakota's dated record for 2025 and 2026, ...". The lede "A reviewer reading a District file in late 2026 checks ..." is also Vermont's "the dates a Vermont reviewer checks".
  - #metros "Five District markets: four submarkets of one city and the metropolitan area around it." Landed Colorado: "Eight Colorado markets: Denver on a page of its own and seven sections on this one." Landed Virginia: "Nine Virginia markets: eight read on this page and ...". Landed South Dakota: "Six South Dakota markets: two metro areas and four county markets, ...". The count in words is mandated; the colon split after it is the shared construction.
  - #capital "How a District project is financed: SBA and bank capital, EB-5, ..." Landed Virginia: "How Virginia projects are financed: SBA, USDA, banks and EB-5, and the totals the record does not give."
  - FAQ h2 "What lenders and sponsors ask about a District project." Landed Connecticut: "What lenders and sponsors ask about Connecticut projects." Landed South Dakota: "What lenders and sponsors ask before a South Dakota project closes."
  - Capitol Riverfront card "Two waterfront neighborhoods whose market readings a study has to gather itself." Wyoming #laramie: "a university town whose market record a study has to build"; Alaska #ketchikan: "a cruise port whose counts a study has to source".
- Smallest fix (headings only, no figure):
  - #costs "A first-quarter wage, no District cost index, and public money read against the September 2026 revenue estimate."
  - #supply "Citywide supply: the 2025 visitor year and DMPED's housing count since 2015."
  - #events "The RENTAL Act, the conversion awards, a sewer emergency and the 2026 releases, by date." Lede: delete "A reviewer reading a District file in late 2026 checks whether the study has caught up with these events. " so it opens "Two items a reviewer may raise ...".
  - #metros "Four city submarkets and the metro around them: the District's five markets."
  - #capital: delete "How a District project is financed: " and capitalize "SBA".
  - FAQ h2 "Federal payrolls, office space, conversions, hotel tax, rents and TOPA: what a District file is asked."
  - Card "Navy Yard, Buzzard Point and The Wharf, with no dated public figure for either district as a whole."

### A2-13 MAJOR-NONFACTUAL: FAQ answers repeat the body's argument in the body's words (I115)
- Page: FAQ 6 (lines 84 to 85), FAQ 3 (73), FAQ 4 (77), FAQ 5 (81), FAQ 1 (65).
- Reproduction (in-page 7-word shingles, digits and markers dropped):
  - FAQ 6 shares 37 with #rules (lines 389 to 390): the exemption, both cooling-off periods and "The date on which the law took effect after congressional review was not confirmed", with the same conclusion (the study names the regime it assumed).
  - FAQ 3 shares 7 with #conversions (line 381), including "a lender treats/will read a conditional award as a condition of the loan rather than as revenue/income in hand".
  - FAQ 4 shares 6 with #rules line 393 ("states the rate it assumes after that date and the authority").
  - FAQ 5 shares 5 with line 503 ("for the direction of the regional market", building the rent from the subject's own submarket inside the District line).
  - FAQ 1 shares 6 with line 497 (the division definition).
  I115 lets an in-page 7-word repeat block where it is a sentence frame or argument; these are arguments. The precedent is t4 A2-20.
- Smallest fix: delete FAQ 6 whole (its figures are nocount and all stand in #rules; its citation [^13] stays in use; six FAQs remain). In FAQ 3 replace "; a lender treats a conditional award as a condition of the loan rather than as revenue in hand." with ".". FAQ 4, 5 and 1: recorded, no edit required.

### A2-14 MAJOR-NONFACTUAL: the one-broker-per-figure argument for Q3 2026 office is landed Northern Virginia's, and the page makes it four times
- Page: FAQ 2 (line 69), #office (lines 372 to 374), #downtown-dc (line 463).
- Text: FAQ 2 "Because a second broker draws its inventory differently, a study takes vacancy, rent and absorption from one firm's report, names it, and asks that firm for the submarket table its citywide rate belongs to." #office "In each case the study cites one firm's vacancy, rent and absorption together and says which firm it chose, rather than pairing one broker's positive absorption with another broker's vacancy rate."
- Reproduction: landed Northern Virginia FAQ 3: "How does a market study for an Arlington or Alexandria office project handle two brokers' Q3 2026 figures?" "One broker per statement, named, and never a blend. Cushman & Wakefield prints ... CBRE prints ... The study quotes the report whose boundary holds the site". Its sources lede: "Where CBRE and Cushman & Wakefield both report a measure, the page keeps each broker's number in its own statement". The topic is the same (Q3 2026 office, the same two brokers, the adjacent market) and so is the argument. Inside the District page the same instruction recurs at lines 372, 373, 374 ("asks the broker for the submarket table that matches its citywide figure") and 463 ("so that vacancy, rent and absorption come from one inventory").
- Smallest fix: delete FAQ 2's last sentence (from "Because a second broker" to "belongs to."). Delete the #office sentence quoted above. The facts (the two firms draw their inventories differently, so the readings cannot be netted) stay at line 372.

### A2-15 MINOR: buyer intent: the "consultant" form never reaches the hero, the opening or a call to action
- Page: hero (9), opening paragraph (326), in-body CTA (504), `cta` (94 to 95), description (6).
- Reproduction: "District of Columbia feasibility study consultant" occurs once, in FAQ 7's question. The "company" form occurs once, in #capital line 513. The hero, the opening, both CTAs and the description use only the brand name with "Washington, DC". The bare form is already at the I89 cap (3), so a mention has to move rather than be added. The owner's rule asks the title, H1, meta, opening and CTA to target the consultant and company forms.
- Fix: opening, "Feasibility Study Company prepares feasibility studies for projects in Washington, DC:" to "Feasibility Study Company is a District of Columbia feasibility study consultant for projects in Washington, DC:". Line 381, "In a District of Columbia feasibility study the abatement" to "In a District study the abatement". Counts after: consultant 2, company 1, bare 3.

### A2-16 MINOR: the generated neighbours heading reads "States that border District of Columbia."
- Page: rendered `#neighbors` (`mesh.py` line 224, `state_name` from the H1).
- Reproduction: `grep -o "States that border [^<]*"` on the rendered page. The article is missing; Maryland and Virginia render correctly. A future District case would render "Worked cases in District of Columbia." the same way.
- Fix (integrator, `mesh.py`): give the District its article ("the District of Columbia") in `state_name`, then rerun `mesh.py`.

### A2-17 MINOR: the Washington metro section points to the Maryland side but not to the Virginia side
- Page: #washington-metro, line 497.
- Text: "The Maryland side of that division, and the rest of Maryland's share of the metro, is read on the Maryland page. This section prints metro and division totals only, and no figure for any single Virginia county."
- Reproduction: D7 gives the Virginia jurisdictions' figures to /states/virginia/northern-virginia/, and D16 names the neighbours' "Washington metro passages" as that page's inbound links. Northern Virginia's hero names the District, but no rendered page links the District page from it (my inbound list). The DC body links Maryland but never Virginia or Northern Virginia; Virginia appears only in the generated list.
- Fix: replace "and no figure for any single Virginia county." with "and no figure for any single Virginia county; Fairfax, Arlington, Loudoun, Prince William and Alexandria are read on the <a href="/states/virginia/northern-virginia/">Northern Virginia page</a>." (no figure added).

### A2-18 MINOR: plain claims with no source
- Line 327 "For a city whose office stock, restaurants and hotels were built around a federal workforce, that is the starting fact of almost any demand case." Fix: delete.
- Line 346 "and on the commuters behind it, many of whom live in the Maryland and Virginia counties covered in the Washington metro section". No row counts commuters. Fix: end the sentence at "draws on the job count".
- Line 375 "and in the District the answer usually runs through the conversion program in the next section". Fix: replace with "and in the District one answer is the conversion program in the next section".
- Line 390 "where it can shorten a sale by weeks". Fix: delete the clause.
- Line 393 ", as almost every one does,". Fix: delete.
- Line 423: "a Commanders stadium agreement for the RFK site" and "the 2025 federal deployment in the District" are named as events with no source. ST line 173 lists both as NOT FOUND. Fix: keep them as gaps but say so: "the terms of any stadium agreement for the RFK site, and a dated measure of visitor traffic in 2025". Same at line 492.
- Line 459 "the newest buildings east of it gain occupancy": Cushman & Wakefield (MT line 10) says the East End's gain was led by Class A, not by the newest buildings. Fix: "Class A buildings east of it".
- Line 470 "Union Market, east of the rail yards, appears on the same page as an area where more mixed-use space is expected over the next five years." The paragraph carries no citation. Fix: add [^30].
- Line 512 "USDA Rural Development's business guarantees are written for rural areas" and "An EB-5 offering counts the jobs a project creates": rules stated with no source (t3 A2-15 and t4 A2-14 recorded the same). Fix: cite the practice-area pages the sentence already links, or delete the two clauses.

### A2-19 MINOR: research-process failures printed as content
- Line 402 "and the cost consultant page tried for the metro did not load"; "because the state energy profile read for the research did not carry District data". Line 408 "The FEMA page itself did not load for the research, and the relay is a secondary source." Line 470 "and the BID's annual report was not readable for this page". Line 480 "which were not reached for this page".
- A buyer reads the firm's fetch errors (t5 A2-20 is the precedent). Fix: delete each clause. At line 408 keep "The relay is a secondary source.".

### A2-20 MINOR: the #economy heading sets counts against each other in words
- Page: `data-h2` of #economy, line 324.
- Text: "Fewer federal jobs and fewer jobs in all: the District's payroll from August 2025 to September 2026."
- Reproduction: the page prints no District federal count for August 2025 or September 2026. "Fewer jobs in all" sets against each other the measures that line 329 says "are listed by release below and not set against each other" (DOES 751,000 from the September 2025 release, BLS 719.9 thousand seasonally adjusted for September 2026). The research supports the direction (ORA, ST lines 41 to 43; the QCEW release's -4.5% for March 2025 to March 2026, ST line 39 note), but a heading cannot carry the citations I60(b) asks for.
- Fix: "The District's payroll by release, August 2025 to September 2026."

### A2-21 MINOR: the engagement list is said three times, and a card sentence is repeated in its section
- The project, ward or submarket and capital list appears in FAQ 7, the in-body CTA and the band. The in-body CTA is mandated; the band's restatement falls under I89's judgment reading (t3 A2-20). Fix: none required beyond A2-10.
- The Wards 7 and 8 card (line 453) "the record is the District's own development program rather than a broker's survey" and the section's first sentence (line 490) "the record is the District's own development program rather than a market count" share a 7-word frame. Fix: card "Wards east of the Anacostia, read through St. Elizabeths East, Skyland and Congress Heights."

### A2-22 MINOR: the #capital gap list is landed Colorado's and Alaska's construction
- Page: lines 510 to 511.
- Text: "SBA's fiscal 2025 results for its Washington-area district office were not found for this page"; "The District's SSBCI allocation, DC Green Bank's 2025 lending totals, CDFI awards and FDIC deposit totals were not found in a dated source."
- Reproduction: landed Colorado: "SBA's fiscal 2025 totals for Colorado, CHFA's 2025 production, the state's SSBCI allocation and deployment, ... and FDIC deposit totals were not found on dated primary pages" (folded 7-word run "and FDIC deposit totals were not found"). Alaska: "SBA's fiscal 2025 results for its Alaska district, ..., FDIC deposit totals, CDFI awards" (folded run "SBA's fiscal results for its <place>"). F4 asks for gaps, so the content is right; the list construction is shared.
- Fix: line 511 "DC Green Bank's 2025 lending totals and the District's SSBCI allocation were not found; nor were CDFI awards or deposit totals." (no figure).

### A2-23 MINOR: the index request calls the metro a submarket
- Page: `docs/rollout/geo-5/requests.json` `geo-5-18` (index_entry for /states/, applied at landing).
- Text: "Federal job losses read for the District, its division and the metro, office vacancy and conversions, and five submarkets."
- Reproduction: the page's #metros counts "four submarkets of one city and the metropolitan area around it" (line 448).
- Fix: "... office vacancy and conversions, four submarkets and the metro."

### A2-24 MINOR: the remaining shared 8-word runs
- FAQ 7 "the deliverable that program requires and the next steps" = /asset-classes/skilled-nursing/ ("The reply sets out the analytical framework, the deliverable that program requires and the next steps."). This is the home page's record wording, lightly edited. A2-10's FAQ 7 deletion removes it.
- Description with four case pages: removed by A2-8.
- Line 499 and Vermont's #economy, digits dropped: "thousand in government, thousand in professional and business services". These are BLS supersector labels, the category I115 allows. Record only.

## Counted figures after my confirmed findings

No finding deletes or wraps a counted figure:
- A2-2's change is `sba:` marker text, which pagecheck does not count;
- the addresses A2-1 removes (2121, 899) are not figures under pagecheck's rule;
- FAQ 6 (A2-13) holds only nocount values and a date, and its citation stays in use;
- A2-8 moves a counted figure into the description, which is not page text;
- A2-6 reorders the hero without removing a figure.
The page holds 56 counted figures (48 research, 8 register): over the READY floors (30 in all, 20 research) and the landing floors (25 and 15).

Severity tally: BLOCKER 0; MAJOR-FACTUAL 4 (A2-2 to A2-5); MAJOR-NONFACTUAL 10 (A2-1, A2-6 to A2-14); MINOR 10 (A2-15 to A2-24).
